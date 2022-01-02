smash = (a) -> a.join ' '

_____________________________________
smash = (words) ->
  'use strict'
  words.join ' '
  
_____________________________________
smash = (words) ->
  if words.length == 0
    return ""
  return words.reduce (x, y) -> x + " " + y
