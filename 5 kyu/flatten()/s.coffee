513fa1d75e4297ba38000003


flatten = (array...) ->
  array.reduce (a, e) ->
    a.concat if Array.isArray(e) then flatten(e...) else [e]
  , []
______________________________
flatten = (arr...)->
  arr.toString().split ','
______________________________
flatten = (array...) -> 
  if (array.some (x) -> x instanceof Array) then flatten ([].concat array...)... else array
