let foo = Node 16 'a' (Node 7 'b' (Node 1 'd' Nil Nil) (Node 10 'e' Nil Nil)) (Node 18 'c' Nil (Node 21 'f' Nil Nil))

lookup 16 foo
lookup 7 foo
lookup 1 foo
lookup 10 foo
lookup 18 foo
lookup 21 foo
lookup 0 foo -- Nothing

let bar = insert 17 'x' foo
lookup 17 bar
lookup 16 bar
lookup 7 bar
lookup 1 bar
lookup 10 bar
lookup 18 bar
lookup 21 bar

let bar = delete 7 foo
lookup 7 bar -- Nothing
lookup 16 foo
lookup 1 foo
lookup 10 foo
lookup 18 foo
lookup 21 foo
