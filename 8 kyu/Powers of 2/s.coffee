powersOfTwo = (n) -> 
  2**x for x in [0..n]
___________________________________
powersOfTwo = (n) -> 
  return (2**x for x in [0..n])
___________________________________
powersOfTwo = (n) ->
  solution = []
  x = 0
  while x <= n
    solution.push 2 ** x
    x++
  solution
___________________________________
powersOfTwo = (n) -> 
  if(n == 0) then [1] else powersOfTwo(n - 1).concat([2 ** n])
