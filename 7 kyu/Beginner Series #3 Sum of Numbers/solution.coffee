getSum = (a, b) -> (a + b) * (Math.abs(a - b) + 1) / 2

__________________________________
getSum = (a, b) ->
  [a..b].reduce (a,b) -> a+b
  
__________________________________
getSum = (a, b) -> 
  if a is b  
    return a
  else ((Math.abs(a - b) + 1) * (a + b)) / 2

__________________________________
getSum = (a, b) ->
  sum = 0
  sum += x for x in [a..b]
  sum
  
__________________________________
getSum = (a, b) ->
  [Math.min(a, b)..Math.max(a, b)].reduce (sum, i) -> sum + i
