filter_list = (l) ->
  l.filter (item) -> typeof item is 'number'
  
_____________________________________________
filter_list = (l) ->
  l.filter (el) -> typeof el isnt 'string'
  
_____________________________________________
filter_list = (l) -> l.filter (x) -> ~~x is x

_____________________________________________
filter_list = (l) ->
  (n for n in l when +n == n)
  
_____________________________________________
filter_list = (l) ->
  l.filter (el) -> typeof el is 'number'
