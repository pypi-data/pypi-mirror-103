import ast

from typing import Optional, List

from .clike import CLikeTranspiler
from .declaration_extractor import DeclarationExtractor
from py2many.tracer import is_list, defined_before, is_class_or_module

from py2many.analysis import get_id, is_void_function


class GoMethodCallRewriter(ast.NodeTransformer):
    def visit_Call(self, node):
        needs_assign = False
        fname = node.func
        if isinstance(fname, ast.Attribute):
            if is_list(node.func.value) and fname.attr == "append":
                needs_assign = True
            node.args = [ast.Name(id=fname.value.id, lineno=node.lineno)] + node.args
            node.func = ast.Name(id=fname.attr, lineno=node.lineno, ctx=fname.ctx)
        if needs_assign:
            ret = ast.Assign(
                targets=[ast.Name(id=fname.value.id, lineno=node.lineno)],
                value=node,
                lineno=node.lineno,
                scopes=node.scopes,
            )
            return ret
        return node


class GoNoneCompareRewriter(ast.NodeTransformer):
    def visit_Compare(self, node):
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        if (
            isinstance(right, ast.Constant)
            and right.value is None
            and isinstance(left, ast.Constant)
            and isinstance(left.value, int)
        ):
            # Convert None to 0 to compare vs int
            right.value = 0
        return node


class GoPropagateTypeAnnotation(ast.NodeTransformer):
    def _visit_assign(self, node, target):
        if hasattr(node, "annotation") and isinstance(
            node.value, (ast.List, ast.Set, ast.Dict)
        ):
            node.value.annotation = node.annotation
        return node

    def visit_Assign(self, node):
        target = node.targets[0]
        return self._visit_assign(node, target)

    def visit_AnnAssign(self, node):
        target = node.target
        return self._visit_assign(node, target)


class GoTranspiler(CLikeTranspiler):
    NAME = "go"

    CONTAINER_TYPE_MAP = {"List": "[]", "Dict": "map", "Set": "Set", "Optional": "nil"}

    def __init__(self):
        super().__init__()
        self._default_type = None
        self._container_type_map = self.CONTAINER_TYPE_MAP

    def headers(self, meta):
        return "\n".join(self._headers)

    def usings(self):
        buf = "package main\n\n"  # TODO naming
        if self._usings:
            buf += "import (\n"
            buf += "\n".join([f"{using}" for using in self._usings])
            buf += ")\n"
        return buf + "\n\n"

    def _combine_value_index(self, value_type, index_type) -> str:
        return f"{value_type}{index_type}"

    def visit_FunctionDef(self, node):
        body = "\n".join([self.visit(n) for n in node.body])
        typenames, args = self.visit(node.args)

        if len(typenames) and typenames[0] == None and hasattr(node, "self_type"):
            typenames[0] = node.self_type

        args_list = []
        typedecls = []
        index = 0
        for i in range(len(args)):
            typename = typenames[i]
            arg = args[i]
            if typename == "T":
                typename = "T{0} any".format(index)
                typedecls.append(typename)
                index += 1
            args_list.append(f"{arg} {typename}")

        return_type = ""
        if not is_void_function(node):
            if node.returns:
                typename = self._typename_from_annotation(node, attr="returns")
                return_type = f" {typename}"
            else:
                return_type = " RT"
                typedecls.append("RT")

        template = ""
        if len(typedecls) > 0:
            template = "[{0}]".format(", ".join(typedecls))

        args = ", ".join(args_list)
        funcdef = f"func {node.name}{template}({args}){return_type} {{"
        return funcdef + "\n" + body + "}\n\n"

    def visit_Return(self, node):
        if node.value:
            return "return {0}".format(self.visit(node.value))
        return "return"

    def visit_arg(self, node):
        id = get_id(node)
        if id == "self":
            return (None, "self")
        typename = "T"
        if node.annotation:
            typename = self._typename_from_annotation(node)
        return (typename, id)

    def visit_Lambda(self, node):
        typenames, args = self.visit(node.args)
        args_string = ", ".join([f"{a} {t}" for t, a in zip(typenames, args)])
        return_type = "int"  # TODO: infer
        body = self.visit(node.body)
        return f"func({args_string}) {return_type} {{ {body} }}"

    def visit_Attribute(self, node):
        attr = node.attr

        value_id = self.visit(node.value)

        if not value_id:
            value_id = ""

        if is_class_or_module(value_id, node.scopes):
            return f"{value_id}.{attr}"

        return f"{value_id}.{attr}"

    def visit_range(self, node, vargs: List[str]) -> str:
        self._usings.add('iter "github.com/hgfischer/go-iter"')
        if len(node.args) == 1:
            return f"iter.NewIntSeq(iter.Start(0), iter.Stop({vargs[0]})).All()"
        elif len(node.args) == 2:
            return (
                f"iter.NewIntSeq(iter.Start({vargs[0]}), iter.Stop({vargs[1]})).All()"
            )
        elif len(node.args) == 3:
            return f"iter.NewIntSeq(iter.Start({vargs[0]}), iter.Stop({vargs[1]}), iter.Step({vargs[2]})).All()"

        raise Exception(
            "encountered range() call with unknown parameters: range({})".format(vargs)
        )

    def visit_print(self, node, vargs: List[str]) -> str:
        placeholders = []
        for n in node.args:
            placeholders.append("%v")
        self._usings.add('"fmt"')
        placeholders_str = " ".join(placeholders)
        vargs_str = ", ".join(vargs)
        return f'fmt.Printf("{placeholders_str}\\n",{vargs_str})'

    def _dispatch(self, node, fname: str, vargs: List[str]) -> Optional[str]:
        dispatch_map = {
            "range_": self.visit_range,
            "xrange": self.visit_range,
            "print": self.visit_print,
        }

        if fname in dispatch_map:
            return dispatch_map[fname](node, vargs)

        # small one liners are inlined here as lambdas
        small_dispatch_map = {"str": lambda: f"String({vargs[0]})"}
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

        vargs = []

        if node.args:
            vargs += [self.visit(a) for a in node.args]
        if node.keywords:
            vargs += [self.visit(kw.value) for kw in node.keywords]

        ret = self._dispatch(node, fname, vargs)
        if ret is not None:
            return ret
        if vargs:
            args = ", ".join(vargs)
        else:
            args = ""
        return f"{fname}({args})"

    def visit_For(self, node):
        target = self.visit(node.target)
        it = self.visit(node.iter)
        buf = []
        buf.append(f"for _, {target} := range {it} {{")
        # Dummy assign to silence the compiler on unused vars
        if target.startswith("_"):
            buf.append(f"_ = {target}")
        buf.extend([self.visit(c) for c in node.body])
        buf.append("}")
        return "\n".join(buf)

    def visit_While(self, node):
        buf = []
        buf.append("for {0} {{".format(self.visit(node.test)))
        buf.extend([self.visit(c) for c in node.body])
        buf.append("}")
        return "\n".join(buf)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Str(self, node):
        return "" + super().visit_Str(node) + ""

    def visit_Bytes(self, node):
        bytes_str = "{0}".format(node.s)
        return bytes_str.replace("'", '"')  # replace single quote with double quote

    def _visit_container_compare(self, node):
        left = self.visit(node.left)
        op = self.visit(node.ops[0])
        right = self.visit(node.comparators[0])
        if op == "==":
            return f"cmp.Equal({left}, {right})"
        return super().visit_Compare(node)

    def visit_Compare(self, node):
        left = node.left
        right = node.comparators[0]
        if hasattr(left, "annotation") or hasattr(right, "annotation"):
            self._typename_from_annotation(left)
            self._typename_from_annotation(right)
            if hasattr(left, "container_type") or hasattr(right, "container_type"):
                self._usings.add('"github.com/google/go-cmp/cmp"')
                return self._visit_container_compare(node)
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
            return super().visit_Name(node)

    def visit_NameConstant(self, node):
        if node.value is None:
            return "nil"
        else:
            return super().visit_NameConstant(node)

    def visit_If(self, node):
        body_vars = set([get_id(v) for v in node.scopes[-1].body_vars])
        orelse_vars = set([get_id(v) for v in node.scopes[-1].orelse_vars])
        node.common_vars = body_vars.intersection(orelse_vars)
        return super().visit_If(node)

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
        extractor = DeclarationExtractor(GoTranspiler())
        extractor.visit(node)
        declarations = node.declarations = extractor.get_declarations()

        fields = []
        index = 0
        for declaration, typename in declarations.items():
            if typename == None:
                typename = "ST{0}".format(index)
                index += 1
            fields.append(f"{declaration} {typename}")

        for b in node.body:
            if isinstance(b, ast.FunctionDef):
                b.self_type = node.name

        if node.is_dataclass:
            fields = "\n".join(fields)
            body = [self.visit(b) for b in node.body]
            body = "\n".join(body)
            return f"type {node.name} struct {{\n{fields}\n}}\n{body}\n"
        else:
            fields = "\n".join(fields)
            body = [self.visit(b) for b in node.body]
            body = "\n".join(body)
            return f"class {node.name} {{\n{fields}\n\n {body}\n}}\n"

    def visit_IntEnum(self, node):
        extractor = DeclarationExtractor(GoTranspiler())
        extractor.visit(node)

        ret = f"type {node.name} int\n\n"
        fields = []
        for i, (member, var) in enumerate(extractor.class_assignments.items()):
            typename = f" {node.name}" if i == 0 else ""
            if var == "auto()":
                fields.append(f"{member}{typename} = iota")
            else:
                fields.append(f"{member}{typename} = {var}")
        fields = "\n".join(fields)
        return f"{ret} const (\n{fields}\n)\n\n"

    def visit_IntFlag(self, node):
        extractor = DeclarationExtractor(GoTranspiler())
        extractor.visit(node)
        ret = f"type {node.name} int\n\n"
        fields = []
        for i, (member, var) in enumerate(extractor.class_assignments.items()):
            typename = f" {node.name}" if i == 0 else ""
            if var == "auto()":
                fields.append(f"{member}{typename} = 1 << iota")
            else:
                fields.append(f"{member}{typename} = {var}")
        fields = "\n".join(fields)
        return f"{ret} const (\n{fields}\n)\n\n"

    def visit_alias(self, node):
        return "use {0}".format(node.name)

    def visit_Import(self, node):
        imports = [self.visit(n) for n in node.names]
        return "\n".join(i for i in imports if i)

    def visit_ImportFrom(self, node):
        if node.module in self.IGNORED_MODULE_LIST:
            return ""

        names = [n.name for n in node.names]
        names = ", ".join(names)
        module_path = node.module.replace(".", "::")
        return "use {0}::{{{1}}}".format(module_path, names)

    def visit_List(self, node):
        typename = "int[]"  # TODO: infer
        if getattr(node, "annotation", None):
            typename = self._typename_from_annotation(node)
        elements = [self.visit(e) for e in node.elts]
        elements = ", ".join(elements)
        return f"{typename}{{{elements}}}"

    def visit_Dict(self, node):
        if len(node.keys) > 0:
            kv_string = []
            for i in range(len(node.keys)):
                key = self.visit(node.keys[i])
                value = self.visit(node.values[i])
                kv_string.append("({0}, {1})".format(key, value))
            initialization = "[{0}].iter().cloned().collect::<HashMap<_,_>>()"
            return initialization.format(", ".join(kv_string))
        else:
            return "HashMap::new()"

    def visit_Subscript(self, node):
        value = self.visit(node.value)
        index = self.visit(node.slice)
        if hasattr(node, "is_annotation"):
            if value in self.CONTAINER_TYPE_MAP:
                value = self.CONTAINER_TYPE_MAP[value]
            if value == "Tuple":
                return "({0})".format(index)
            return "{0}{1}".format(value, index)
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
        condition = self.visit(node.test)
        return f'if !({condition}) {{ panic("assert") }}'

    def visit_AnnAssign(self, node):
        target = self.visit(node.target)
        type_str = self._typename_from_annotation(node.target)
        val = self.visit(node.value)
        return f"var {target} {type_str} = {val}"

    def visit_Assign(self, node):
        target = node.targets[0]

        if isinstance(target, ast.Tuple):
            elts = [self.visit(e) for e in target.elts]
            value = self.visit(node.value)
            return "{0} := {1}".format(", ".join(elts), value)

        if isinstance(node.scopes[-1], ast.If):
            outer_if = node.scopes[-1]
            target_id = self.visit(target)
            if target_id in outer_if.common_vars:
                value = self.visit(node.value)
                return "{0} := {1}".format(target_id, value)

        if isinstance(target, ast.Subscript) or isinstance(target, ast.Attribute):
            target = self.visit(target)
            value = self.visit(node.value)
            if value == None:
                value = "None"
            return "{0} := {1}".format(target, value)

        definition = node.scopes.find(target.id)
        if isinstance(target, ast.Name) and defined_before(definition, node):
            target = self.visit(target)
            value = self.visit(node.value)
            return "{0} = {1}".format(target, value)
        else:
            typename = self._typename_from_annotation(target)
            target = self.visit(target)
            value = self.visit(node.value)

            if typename is not None:
                return f"var {target} {typename} = {value}"
            return f"{target} := {value}"

    def visit_Delete(self, node):
        target = node.targets[0]
        return "{0}.drop()".format(self.visit(target))

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
        self._usings.add('"fmt"')
        for n in node.values:
            value = self.visit(n)
            buf.append('fmt.Printf("%v\n",{0})'.format(value))
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
