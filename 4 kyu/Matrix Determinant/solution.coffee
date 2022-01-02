determinant = (m) ->
  s = -1
  if m[1] then m[0].reduce( (d,v,i) ->
    d + v * (s *= -1) * determinant(m[1..-1].map (r) ->
      r.slice(0, i).concat r.slice(i+1)
    )
  , 0) else m[0][0]
_____________________________________________
determinant = (m) -> if m.length == 1 then m[0][0] else m[0].reduce ((s, n, i) => s + (if i % 2 == 0 then 1 else -1) * n * determinant(m.slice(1).map((r) -> r.filter((_, j) -> j != i)))), 0
_____________________________________________

determinant = (m) -> 
  if m.length == 1
    return m[0][0]
  else if m.length == 2
    return m[0][0]*m[1][1] - m[0][1]*m[1][0]
  else
    d = 0
    for i in [0...m.length]
      sub_det = (row[1...] for row in m[...i].concat(m[i+1...]))
      console.log(sub_det)
      d += (-1)**i * m[i][0] * determinant(sub_det)
    return d
_____________________________________________
determinant = (m) ->
  if m.length == 1
    return m[0][0]
  if m.length == 2
    return m[0][0] * m[1][1] - (m[0][1] * m[1][0])
  m[0].reduce ((r, e, i) ->
    r + (Math.pow -1,(i + 2)) * e * determinant(m.slice(1).map((c) ->
      c.filter (_, j) ->
        i != j
    ))
  ), 0
_____________________________________________
minor = (m, i) -> n for n, x in row when x isnt i for row in m[1..]

determinant = (m) ->
  if m.length then m[0].reduce ((t, n, i) -> t + [n, -n][i % 2] * determinant minor m, i), 0 else 1
