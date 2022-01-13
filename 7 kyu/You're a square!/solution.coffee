isSquare = (n) ->
  Math.sqrt(n) % 1 is 0
__________________________________
isSquare = (n) -> n = Math.sqrt(n); n is ~~n
__________________________________
isSquare = (n) ->
  n = Math.sqrt n
  n == ~~n
__________________________________
isSquare = (n) ->
  if n < 0 then return false
  !"#{Math.sqrt(n)}".match(/\./)
__________________________________
isSquare = (n) ->
  if n < 0 then return false
  return ( ( Math.sqrt n ) % 1 == 0 ) ? true : false
