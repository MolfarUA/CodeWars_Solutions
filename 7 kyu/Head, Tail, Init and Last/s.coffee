head = (array) -> array[0]
tail = (array) -> array[1..]
init = (array) -> array[...-1]
last = (array) -> array[array.length-1]
_____________________________
head = (arr) ->
  [start, end...] = arr
  start
  
tail = (arr) ->
  [start, end...] = arr
  end

init = (arr) ->
  [start..., end] = arr
  start
  
last = (arr) ->
  [start..., end] = arr
  end
_____________________________
head = (l) -> l[0]
tail = (l) -> l[1..]
init = (l) -> l[...-1]
last = (l) -> l[l.length - 1]
_____________________________
head = (arr) ->
  +arr.slice 0, 1
  
tail = (arr) ->
  arr.slice 1
  
init = (arr) ->
  arr.slice 0, -1
  
last = (arr) ->
  +arr.slice -1
