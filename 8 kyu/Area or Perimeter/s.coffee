5ab6538b379d20ad880000ab


areaOrPerimeter = (l, w) ->
    if l == w
        return l * w
    (l + l) + (w + w)
________________________
areaOrPerimeter = (a, b) -> if a-b then (a+b)*2 else a*a
________________________
areaOrPerimeter = (l, w) -> if l == w then (l*w) else (l+l+w+w)
________________________
areaOrPerimeter = (l, w) -> 
  if l != w 
    l*2 + w*2 
  else 
    l*l
