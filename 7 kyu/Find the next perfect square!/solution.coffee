findNextSquare = (sq) ->
  number = Math.sqrt(sq) + 1
  if number % 1 then -1 else number**2

_______________________________________
findNextSquare = (sq) ->
  if sq ** 0.5 % 1 then -1 else (sq ** 0.5 + 1) ** 2

_______________________________________
findNextSquare = (sq) ->
  if Math.sqrt(sq) % 1 == 0
    Math.pow(Math.sqrt(sq) + 1, 2)
  else
    -1

_______________________________________
findNextSquare = (num) ->
  if (num ** .5) % 1 == 0
      ((num ** .5) + 1) ** 2
  else
      -1
      
_______________________________________
findNextSquare = (sq) ->
  if Math.sqrt(sq) % 1 != 0 then -1 else Math.pow(Math.sqrt(sq)+1,2)

_______________________________________
findNextSquare = (sq) ->
  result = parseInt(Math.pow(sq, 0.5).toString())
  if result * result is sq
    result++
    return result * result
  -1
