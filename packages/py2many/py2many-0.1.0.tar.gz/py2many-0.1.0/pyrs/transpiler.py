import ast
import functools

from .clike import CLikeTranspiler
from .declaration_extractor import DeclarationExtractor
from .inference import get_inferred_rust_type

from py2many.analysis import get_id, is_global, is_mutable, is_void_function
from py2many.inference import get_inferred_type, is_reference
from py2many.tracer import is_list, defined_before, is_class_or_module

from typing import List, Optional


class RustLoopIndexRewriter(ast.NodeTransformer):
    def visit_For(self, node):
        if hasattr(node.iter, "id"):
            definition = node.scopes.find(node.iter.id)
            if is_reference(definition):
                node.target.needs_dereference = True
        return node


class RustNoneCompareRewriter(ast.NodeTransformer):
    def visit_Compare(self, node):
        right = self.visit(node.comparators[0])
        if isinstance(right, ast.Constant) and right.value is None:
            node.left = ast.Call(
                func=ast.Name(id="Some", ctx=ast.Load()),
                args=[node.left],
                lineno=node.left.lineno,
                keywords=[],
            )
        return node


class RustTranspiler(CLikeTranspiler):
    NAME = "rust"

    CONTAINER_TYPE_MAP = {
        "List": "Vec",
        "Dict": "HashMap",
        "Set": "HashSet",
        "Optional": "Option",
    }

    def __init__(self):
        super().__init__()
        self._container_type_map = self.CONTAINER_TYPE_MAP
        self._default_type = "_"

    def usings(self):
        usings = sorted(list(set(self._usings)))
        deps = sorted(
            set(mod.split("::")[0] for mod in usings if not mod.startswith("std:"))
        )
        externs = [f"extern crate {dep};" for dep in deps]
        deps = ",".join(deps)
        externs = "\n".join(externs)
        uses = "\n".join(
            f"use {mod};" for mod in usings if mod not in ("strum", "lazy_static")
        )
        return f"// cargo-deps: {deps}\n{externs}\n{uses}" if deps else f"{uses}"

    def visit_FunctionDef(self, node):
        body = "\n".join([self.visit(n) for n in node.body])
        typenames, args = self.visit(node.args)

        args_list = []
        if args and args[0] == "self":
            del typenames[0]
            del args[0]
            args_list.append("&self")

        typedecls = []
        index = 0
        for i in range(len(args)):
            typename = typenames[i]
            arg = args[i]
            if typename == "T":
                typename = "T{0}".format(index)
                typedecls.append(typename)
                index += 1
            args_list.append("{0}: {1}".format(arg, typename))

        return_type = ""
        if not is_void_function(node):
            if node.returns:
                typename = self._typename_from_annotation(node, attr="returns")
                if getattr(node.returns, "needs_reference", False):
                    typename = f"&{typename}"
                return_type = f"-> {typename}"
            else:
                return_type = "-> RT"
                typedecls.append("RT")

        template = ""
        if len(typedecls) > 0:
            template = "<{0}>".format(", ".join(typedecls))

        funcdef = "fn {0}{1}({2}) {3}".format(
            node.name, template, ", ".join(args_list), return_type
        )
        return funcdef + " {\n" + body + "\n}\n"

    def visit_arg(self, node):
        id = get_id(node)
        if id == "self":
            return (None, "self")
        typename = "T"
        if node.annotation:
            typename = self._typename_from_annotation(node)
            mut = "mut " if is_mutable(node.scopes, id) else ""
            # TODO: Should we make this if not primitive instead of checking
            # for container types? That way we cover user defined structs too.
            if hasattr(node, "container_type"):
                # Python passes by reference by default. Rust needs explicit borrowing
                typename = f"&{mut}{typename}"
        return (typename, id)

    def visit_Return(self, node):
        if node.value:
            ret = self.visit(node.value)
            fndef = None
            for scope in node.scopes:
                if isinstance(scope, ast.FunctionDef):
                    fndef = scope
                    break
            if fndef:
                return_type = self._typename_from_annotation(fndef, attr="returns")
                value_type = get_inferred_rust_type(node.value)
                if is_reference(node.value):
                    if is_mutable(node.scopes, get_id(node.value)):
                        definition = node.scopes.find(ret)
                        self._typename_from_annotation(definition)
                        if (
                            getattr(definition, "container_type", (None, None))[0]
                            == "List"
                        ):
                            # TODO: Handle other container types
                            ret = f"{ret}.to_vec()"
                    else:
                        fndef.returns.needs_reference = True
                if return_type != value_type and value_type is not None:
                    return f"return {ret} as {return_type};"
            return f"return {ret};"
        return "return;"

    def visit_Lambda(self, node):
        _, args = self.visit(node.args)
        args_string = ", ".join(args)
        body = self.visit(node.body)
        return "|{0}| {1}".format(args_string, body)

    def visit_Attribute(self, node):
        attr = node.attr

        value_id = self.visit(node.value)

        if is_list(node.value):
            if node.attr == "append":
                attr = "push"
        if not value_id:
            value_id = ""

        if is_class_or_module(value_id, node.scopes):
            return "{0}::{1}".format(value_id, attr)

        return value_id + "." + attr

    def _dispatch(self, node, fname: str, vargs: List[str]) -> Optional[str]:
        def visit_range(node, vargs: List[str]) -> str:
            if len(node.args) == 1:
                return "(0..{})".format(vargs[0])
            elif len(node.args) == 2:
                return "({}..{})".format(vargs[0], vargs[1])
            elif len(node.args) == 3:
                return "({}..{}).step_by({})".format(vargs[0], vargs[1], vargs[2])

            raise Exception(
                "encountered range() call with unknown parameters: range({})".format(
                    vargs
                )
            )

        def visit_print(node, vargs: List[str]) -> str:
            placeholders = []
            for n in node.args:
                placeholders.append("{}")
            return 'println!("{0}",{1});'.format(
                " ".join(placeholders), ", ".join(vargs)
            )

        dispatch_map = {
            "range": visit_range,
            "xrange": visit_range,
            "print": visit_print,
        }

        if fname in dispatch_map:
            return dispatch_map[fname](node, vargs)

        def visit_min_max(is_max: bool) -> str:
            self._usings.add("std::cmp")
            min_max = "max" if is_max else "min"
            self._typename_from_annotation(node.args[0])
            if hasattr(node.args[0], "container_type"):
                return f"{vargs[0]}.iter().{min_max}().unwrap()"
            else:
                all_vargs = ", ".join(vargs)
                return f"cmp::{min_max}({all_vargs})"

        def visit_cast(cast_to: str) -> str:
            if "()" in vargs[0]:
                return f"{vargs[0]} as {cast_to}"
            else:
                return f"{cast_to}::from({vargs[0]})"

        # small one liners are inlined here as lambdas
        small_dispatch_map = {
            "str": lambda: f"String::from({vargs[0]})",
            "len": lambda: f"{vargs[0]}.len()",
            "enumerate": lambda: f"{vargs[0]}.iter().enumerate()",
            "sum": lambda: f"{vargs[0]}.iter().sum()",
            "int": functools.partial(visit_cast, cast_to="i32"),
            "float": functools.partial(visit_cast, cast_to="f32"),
            "double": functools.partial(visit_cast, cast_to="f64"),
            "max": functools.partial(visit_min_max, is_max=True),
            "min": functools.partial(visit_min_max, is_min=True),
            # as usize below is a hack to pass comb_sort.rs. Need a better solution
            "floor": lambda: f"{vargs[0]}.floor() as usize",
            "reversed": lambda: f"{vargs[0]}.iter().rev()",
            "map": lambda: f"{vargs[1]}.iter().map({vargs[0]})",
            "filter": lambda: f"{vargs[1]}.into_iter().filter({vargs[0]})",
            "list": lambda: f"{vargs[0]}.collect::<Vec<_>>()",
        }
        if fname in small_dispatch_map:
            return small_dispatch_map[fname]()
        return None

    def _visit_struct_literal(self, node, fname: str, fndef: ast.ClassDef):
        vargs = []  # visited args
        if not hasattr(fndef, "declarations"):
            raise Exception("Missing declarations")
        if node.args:
            for arg, decl in zip(node.args, fndef.declaration.keys()):
                arg = self.visit(arg)
                vargs += [f"{decl}: {arg}"]
        if node.keywords:
            for kw in node.keywords:
                value = self.visit(kw.value)
                vargs += [f"{kw.arg}: {value}"]
        args = ", ".join(vargs)
        return f"{fname}{{{args}}}"

    def visit_Call(self, node):
        fname = self.visit(node.func)
        fndef = node.scopes.find(fname)

        if isinstance(fndef, ast.ClassDef):
            return self._visit_struct_literal(node, fname, fndef)

        vargs = []  # visited args
        if node.args:
            vargs += [self.visit(a) for a in node.args]
        if node.keywords:
            vargs += [self.visit(kw.value) for kw in node.keywords]

        ret = self._dispatch(node, fname, vargs)
        if ret is not None:
            return ret

        # Check if some args need to be passed by reference
        ref_args = []
        if fndef and hasattr(fndef, "args"):
            for varg, fnarg, node_arg in zip(vargs, fndef.args.args, node.args):
                if is_reference(fnarg) and not is_reference(node_arg):
                    ref_args.append(f"&{varg}")
                else:
                    ref_args.append(varg)
        else:
            ref_args = vargs

        args = ", ".join(ref_args)
        return f"{fname}({args})"

    def visit_For(self, node):
        target = self.visit(node.target)
        it = self.visit(node.iter)
        buf = []
        buf.append("for {0} in {1} {{".format(target, it))
        buf.extend([self.visit(c) for c in node.body])
        buf.append("}")
        return "\n".join(buf)

    def visit_Expr(self, node):
        s = self.visit(node.value)
        if s.strip() and not s.endswith(";"):
            s += ";"
        if s == ";":
            return ""
        else:
            return s

    def visit_Str(self, node):
        return "" + super().visit_Str(node) + ""

    def visit_Bytes(self, node):
        bytes_str = "{0}".format(node.s)
        return bytes_str.replace("'", '"')  # replace single quote with double quote

    def visit_Compare(self, node):
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        if isinstance(node.ops[0], ast.In):
            return "{0}.iter().any(|&x| x == {1})".format(
                right, left
            )  # is it too much?
        elif isinstance(node.ops[0], ast.NotIn):
            return "{0}.iter().all(|&x| x != {1})".format(
                right, left
            )  # is it even more?

        return super().visit_Compare(node)

    def visit_Name(self, node):
        if node.id == "None":
            return "None"
        else:
            ret = super().visit_Name(node)
            definition = node.scopes.find(node.id)
            if (
                definition
                and definition != node
                and getattr(definition, "needs_dereference", False)
            ):
                return f"*{ret}"
            return ret

    def visit_NameConstant(self, node):
        if node.value is True:
            return "true"
        elif node.value is False:
            return "false"
        elif node.value is None:
            return "None"
        else:
            return super().visit_NameConstant(node)

    def visit_If(self, node):
        body_vars = set([get_id(v) for v in node.scopes[-1].body_vars])
        orelse_vars = set([get_id(v) for v in node.scopes[-1].orelse_vars])
        node.common_vars = body_vars.intersection(orelse_vars)

        # TODO find out if this can be useful
        var_definitions = []
        # for cv in node.common_vars:
        #     definition = node.scopes.find(cv)
        #     var_type = decltype(definition)
        #     var_definitions.append("{0} {1};\n".format(var_type, cv))
        ret = "".join(var_definitions) + super().visit_If(node, use_parens=False)
        # Sometimes if True: ... gets compiled into an expression, needing a semicolon
        make_block = (
            isinstance(node.test, ast.Constant)
            and node.test.value == True
            and node.orelse == []
        )
        if make_block:
            return f"{ret};"
        return ret

    def visit_While(self, node):
        return super().visit_While(node, use_parens=False)

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.USub):
            if isinstance(node.operand, (ast.Call, ast.Num)):
                # Shortcut if parenthesis are not needed
                return "-{0}".format(self.visit(node.operand))
            else:
                return "-({0})".format(self.visit(node.operand))
        else:
            return super().visit_UnaryOp(node)

    def visit_BinOp(self, node):
        if (
            isinstance(node.left, ast.List)
            and isinstance(node.op, ast.Mult)
            and isinstance(node.right, ast.Num)
        ):
            return "std::vector ({0},{1})".format(
                self.visit(node.right), self.visit(node.left.elts[0])
            )
        else:
            return super().visit_BinOp(node)

    def visit_Module(self, node):
        buf = []
        for header in self._headers:
            buf.append(header)
        buf += [self.visit(b) for b in node.body]
        return "\n".join(buf)

    def visit_ClassDef(self, node):
        ret = super().visit_ClassDef(node)
        if ret is not None:
            return ret
        extractor = DeclarationExtractor(RustTranspiler())
        extractor.visit(node)
        node.declarations = declarations = extractor.get_declarations()

        fields = []
        index = 0
        for declaration, typename in declarations.items():
            if typename == None:
                typename = "ST{0}".format(index)
                index += 1
            fields.append("{0}: {1},".format(declaration, typename))

        struct_def = "struct {0} {{\n{1}\n}}\n\n".format(node.name, "\n".join(fields))
        impl_def = "impl {0} {{\n".format(node.name)
        buf = [self.visit(b) for b in node.body]
        return "{0}{1}{2} \n}}".format(struct_def, impl_def, "\n".join(buf))

    def visit_IntEnum(self, node):
        extractor = DeclarationExtractor(RustTranspiler())
        extractor.visit(node)

        fields = []
        for member, var in extractor.class_assignments.items():
            if var == "auto()":
                fields.append(f"{member},")
            else:
                fields.append(f"{member} = {var},")
        fields = "\n".join(fields)
        return f"#[derive(Clone, Eq, Hash, PartialEq)]\nenum {node.name} {{\n{fields}\n}}\n\n"

    def visit_StrEnum(self, node):
        self._usings.add("strum")
        self._usings.add("strum_macros::EnumString")

        extractor = DeclarationExtractor(RustTranspiler())
        extractor.visit(node)

        fields = []
        for member, var in extractor.class_assignments.items():
            if var == "auto()":
                fields.append(f"{member},")
            else:
                fields.append(f"#[strum(serialize = {var})]{member},")
        fields = "\n".join(fields)

        return f"#[derive(Clone, Debug, Eq, Hash, PartialEq, EnumString)]\nenum {node.name} {{\n{fields}\n}}\n\n"

    def visit_IntFlag(self, node):
        self._usings.add("flagset::flags")
        self._usings.add("std::os::raw::c_int")
        extractor = DeclarationExtractor(RustTranspiler())
        extractor.visit(node)

        fields = []
        for member, var in extractor.class_assignments.items():
            if var == "auto()":
                fields.append(f"{member},")
            else:
                fields.append(f"{member} = {var},")
        fields = "\n".join(["    " * 2 + f for f in fields])
        return f"flags! {{\n    enum {node.name}: c_int {{\n{fields}\n    }}\n}}\n\n"

    def visit_alias(self, node):
        return "use {0};".format(node.name)

    def visit_Import(self, node):
        imports = [self.visit(n) for n in node.names]
        return "\n".join(i for i in imports if i)

    def visit_ImportFrom(self, node):
        if node.module in self.IGNORED_MODULE_LIST:
            return ""

        names = [n.name for n in node.names]
        names = ", ".join(names)
        module_path = node.module.replace(".", "::")
        return "use {0}::{{{1}}};".format(module_path, names)

    def visit_List(self, node):
        self._usings.add("std::collections")
        if len(node.elts) > 0:
            elements = [self.visit(e) for e in node.elts]
            return "vec![{0}]".format(", ".join(elements))

        else:
            return "vec![]"

    def visit_Dict(self, node):
        self._usings.add("std::collections::HashMap")
        if len(node.keys) > 0:
            self._usings.add("std::collections::HashMap")
            kv_string = []
            for i in range(len(node.keys)):
                key = self.visit(node.keys[i])
                value = self.visit(node.values[i])
                kv_string.append("({0}, {1})".format(key, value))
            initialization = "[{0}].iter().cloned().collect::<HashMap<_,_>>()"
            return initialization.format(", ".join(kv_string))
        else:
            return "HashMap::new()"

    def _cast(self, name: str, to) -> str:
        return f"{name} as {to}"

    def visit_Subscript(self, node):
        value = self.visit(node.value)
        index = self.visit(node.slice)
        if hasattr(node, "is_annotation"):
            if value in self.CONTAINER_TYPE_MAP:
                self._usings.add("std::collections")
                value = self.CONTAINER_TYPE_MAP[value]
            if value == "Tuple":
                return "({0})".format(index)
            return "{0}<{1}>".format(value, index)
        index_typename = get_inferred_type(self._slice_value(node))
        if index_typename != "u64" or index_typename != "usize":
            index = self._cast(index, "usize")
        return "{0}[{1}]".format(value, index)

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Slice(self, node):
        lower = ""
        if node.lower:
            lower = self.visit(node.lower)
        upper = ""
        if node.upper:
            upper = self.visit(node.upper)

        return "{0}..{1}".format(lower, upper)

    def visit_Elipsis(self, node):
        return "compile_error!('Elipsis is not supported');"

    def visit_Tuple(self, node):
        elts = [self.visit(e) for e in node.elts]
        elts = ", ".join(elts)
        if hasattr(node, "is_annotation"):
            return elts
        return "({0})".format(elts)

    def visit_unsupported_body(self, name, body):
        buf = ["let {0} = {{ //unsupported".format(name)]
        buf += [self.visit(n) for n in body]
        buf.append("};")
        return buf

    def visit_Try(self, node, finallybody=None):
        buf = self.visit_unsupported_body("try_dummy", node.body)

        for handler in node.handlers:
            buf += self.visit(handler)
        # buf.append("\n".join(excepts));

        if finallybody:
            buf += self.visit_unsupported_body("finally_dummy", finallybody)

        return "\n".join(buf)

    def visit_ExceptHandler(self, node):
        exception_type = ""
        if node.type:
            exception_type = self.visit(node.type)
        name = "except!({0})".format(exception_type)
        body = self.visit_unsupported_body(name, node.body)
        return body

    def visit_Assert(self, node):
        return "assert!({0});".format(self.visit(node.test))

    def visit_AnnAssign(self, node):
        target, type_str, val = super().visit_AnnAssign(node)
        mut = "mut " if is_mutable(node.scopes, get_id(node.target)) else ""
        return f"let {mut}{target}: {type_str} = {val};"

    def _needs_cast(self, left, right) -> bool:
        if not hasattr(left, "annotation") or not hasattr(right, "annotation"):
            return False
        left_type = self._typename_from_annotation(left)
        right_type = get_inferred_rust_type(right)
        return left_type != right_type and left_type != self._default_type

    def _assign_cast(
        self, value_str: str, cast_to: str, python_annotation, rust_annotation
    ) -> str:
        # python/rust annotations provided to customize the cast if necessary
        return f"{value_str} as {cast_to}"

    def visit_Assign(self, node):
        target = node.targets[0]

        kw = "let"
        mut = is_mutable(node.scopes, get_id(target))
        if is_global(node):
            # Note that static are not really supported, as modifying them requires adding
            # "unsafe" blocks, which pyrs does not do.
            kw = "static" if mut else "const"
        elif mut:
            kw = "let mut"

        if isinstance(target, ast.Tuple):
            elts = ", ".join([self.visit(e) for e in target.elts])
            value = self.visit(node.value)
            return f"{kw} ({elts}) = {value};"

        if isinstance(node.scopes[-1], ast.If):
            outer_if = node.scopes[-1]
            target_id = self.visit(target)
            if target_id in outer_if.common_vars:
                value = self.visit(node.value)
                return "{0} = {1};".format(target_id, value)

        if isinstance(target, ast.Subscript) or isinstance(target, ast.Attribute):
            target = self.visit(target)
            value = self.visit(node.value)
            if value == None:
                value = "None"
            return "{0} = {1};".format(target, value)

        definition = node.scopes.find(target.id)
        if isinstance(target, ast.Name) and defined_before(definition, node):
            needs_cast = self._needs_cast(target, node.value)
            target_str = self.visit(target)
            value = self.visit(node.value)
            if needs_cast:
                target_type = self._typename_from_annotation(target)
                value = self._assign_cast(
                    value, target_type, target.annotation, node.value.rust_annotation
                )
            return f"{target_str} = {value};"
        elif isinstance(node.value, ast.List):
            count = len(node.value.elts)
            target = self.visit(target)
            value = self.visit(node.value)
            typename = self._typename_from_annotation(node.value)

            if kw in ["const", "static"]:
                # Use arrays instead of Vec as globals must have fixed size
                if value.startswith("vec!"):
                    value = value.replace("vec!", "&")
                element_type = self._default_type
                if hasattr(node.value, "container_type"):
                    container_type, element_type = node.value.container_type
                    element_type = self._map_type(element_type)
                return f"{kw} {target}: &[{element_type}; {count}] = {value};"

            mut = "mut " if is_mutable(node.scopes, target) else ""
            if hasattr(node.value, "container_type"):
                return f"{kw} {target}: &{mut}{typename} = &{mut}{value};"

            return f"{kw} {target}: {typename} = {value};"
        elif isinstance(node.value, ast.Set):
            target = self.visit(target)
            value = self.visit(node.value)
            typename = self._typename_from_annotation(node.value)

            if kw in ["const", "static"]:
                self._usings.add("lazy_static::lazy_static")
                if "str" in typename:
                    typename = typename.replace("str", "'static str")
                return f"lazy_static! {{ static ref {target}: {typename} = {value}; }}"

            mut = "mut " if is_mutable(node.scopes, target) else ""
            if hasattr(node.value, "container_type"):
                return f"{kw} {target}: &{mut}{typename} = &{mut}{value};"

            return f"{kw} {target}: {typename} = {value};"
        elif isinstance(node.value, ast.Dict):
            target = self.visit(target)
            value = self.visit(node.value)
            typename = self._typename_from_annotation(node.value)

            if kw in ["const", "static"]:
                if hasattr(node.value, "container_type"):
                    container_type, element_type = node.value.container_type
                    key_typename, value_typename = self._map_types(element_type)
                    if key_typename == "&str":
                        key_typename = "&'static str"
                    if value_typename == "&str":
                        value_typename = "&'static str"
                    typename = f"{key_typename}, {value_typename}"
                return f"lazy_static! {{ static ref {target}: HashMap<{typename}> = {value}; }}"

            mut = "mut " if is_mutable(node.scopes, target) else ""
            if hasattr(node.value, "container_type"):
                return f"{kw} {target}: &{mut}{typename} = &{mut}{value};"

            return f"{kw} {target}: {typename} = {value};"
        else:
            typename = self._typename_from_annotation(target)
            needs_cast = self._needs_cast(target, node.value)
            target_str = self.visit(target)
            value = self.visit(node.value)
            if needs_cast:
                value = self._assign_cast(
                    value, typename, target.annotation, node.value.annotation
                )
            return f"{kw} {target_str}: {typename} = {value};"

    def visit_Delete(self, node):
        target = node.targets[0]
        return "{0}.drop();".format(self.visit(target))

    def visit_Raise(self, node):
        if node.exc is not None:
            return "raise!({0}); //unsupported".format(self.visit(node.exc))
        # This handles the case where `raise` is used without
        # specifying the exception.
        return "raise!(); //unsupported"

    def visit_With(self, node):
        buf = []

        with_statement = "// with!("
        for i in node.items:
            if i.optional_vars:
                with_statement += "{0} as {1}, ".format(
                    self.visit(i.context_expr), self.visit(i.optional_vars)
                )
            else:
                with_statement += "{0}, ".format(self.visit(i.context_expr))
        with_statement = with_statement[:-2] + ") //unsupported\n{"
        buf.append(with_statement)

        for n in node.body:
            buf.append(self.visit(n))

            buf.append("}")

        return "\n".join(buf)

    def visit_Await(self, node):
        return "await!({0})".format(self.visit(node.value))

    def visit_AsyncFunctionDef(self, node):
        return "#[async]\n{0}".format(self.visit_FunctionDef(node))

    def visit_Yield(self, node):
        return "//yield is unimplemented"

    def visit_Print(self, node):
        buf = []
        for n in node.values:
            value = self.visit(n)
            buf.append('println!("{{:?}}",{0});'.format(value))
        return "\n".join(buf)

    def visit_DictComp(self, node):
        return "DictComp /*unimplemented()*/"

    def visit_GeneratorExp(self, node):
        elt = self.visit(node.elt)
        generator = node.generators[0]
        target = self.visit(generator.target)
        iter = self.visit(generator.iter)

        # HACK for dictionary iterators to work
        if not iter.endswith("keys()") or iter.endswith("values()"):
            iter += ".iter()"

        map_str = ".map(|{0}| {1})".format(target, elt)
        filter_str = ""
        if generator.ifs:
            filter_str = ".cloned().filter(|&{0}| {1})".format(
                target, self.visit(generator.ifs[0])
            )

        return "{0}{1}{2}.collect::<Vec<_>>()".format(iter, filter_str, map_str)

    def visit_ListComp(self, node):
        return self.visit_GeneratorExp(node)  # right now they are the same

    def visit_Global(self, node):
        return "//global {0}".format(", ".join(node.names))

    def visit_Starred(self, node):
        return "starred!({0})/*unsupported*/".format(self.visit(node.value))

    def visit_Set(self, node):
        self._usings.add("std::collections::HashSet")
        elts = []
        for i in range(len(node.elts)):
            elt = self.visit(node.elts[i])
            elts.append(elt)

        if elts:
            initialization = "[{0}].iter().cloned().collect::<HashSet<_>>()"
            return initialization.format(", ".join(elts))
        else:
            return "HashSet::new()"

    def visit_IfExp(self, node):
        body = self.visit(node.body)
        orelse = self.visit(node.orelse)
        test = self.visit(node.test)
        return "if {0} {{ {1} }} else {{ {2} }}".format(test, body, orelse)
