flip = (d, a) -> a[..].sort if d == 'R' then (x, y) -> x - y else (x, y) => y - x
  
_____________________________________________
flip =(d, a) ->
  a.sort((x, y) -> if d == 'R' then x - y else y - x);

_____________________________________________
flip = (d, a) ->
  a.sort (a, b) ->
    if d == 'R' then a - b else b - a
      
_____________________________________________
flip =(d, a) ->
  if d == 'R' then a.sort((x, y) -> x - y) else a.sort((x, y) -> y - x)
    
