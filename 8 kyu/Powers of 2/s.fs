let powersOfTwo n = [for i in 0..n -> pown 2 i]
___________________________________
let powersOfTwo n = List.init (n + 1) (pown 2)
___________________________________
let powersOfTwo n = 
  List.map (pown 2) [0..n]
___________________________________
let powersOfTwo (n: int): List<int> = [for x in 0..n -> pown 2 x]
