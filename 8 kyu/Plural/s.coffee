plural = (n) ->
  if n == 1 then false else true
__________________
plural = (n) ->
  n != 1
__________________
plural = (n) ->
  if n == 1
    return false
  else 
    return true
