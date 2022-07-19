57f75cc397d62fc93d000059


calc = (x) -> (c.charCodeAt() for c in x).join('').replace(/[^7]/g, '').length * 6
__________________________________
calc = (x) ->
  t = x.split('').reduce(((acc, e) ->
    acc + String(e.charCodeAt())
  ), '')
  t.split('').filter((e) ->
    e == '7'
  ).length * 6
__________________________________
calc=(x) ->
  x.split('').map((x) -> x.charCodeAt()).join('').split('').filter((x) -> x == '7').length * 6
