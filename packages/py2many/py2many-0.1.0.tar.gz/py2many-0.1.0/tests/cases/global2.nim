let code_0 = 0
let code_1 = 1
let code_a = "a"
let code_b = "b"
let l_b = [code_a].iter().cloned().collect::<HashSet<_>>()
let l_c = [(code_b, code_0)].iter().cloned().collect::<HashMap<_,_>>()
proc main() =
  assert("a" in l_b)
  echo "OK"

main()
