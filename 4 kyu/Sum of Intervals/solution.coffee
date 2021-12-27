sumIntervals = (intervals) ->
  a = {}
  for i in intervals
    for x in [i[0]...i[1]]
      a[x] = true
  return Object.keys(a).length

___________________
sumIntervals = (intervals) ->
  new Set([].concat(([x[0]...x[1]] for x in intervals)...)).size
  
___________________
sumIntervals = (m) ->
  a = []
  ((a.push(j) if a.indexOf(j) == -1) for j in [m[i][0]...m[i][1]]) for i in [0...m.length]
  a.length
  
___________________
sumIntervals = (intervals) ->
  arr = []
  
  for interval in intervals
    for i in [interval[0]..interval[1] - 1] when i not in arr
      arr.push i

  return arr.length

___________________
sumIntervals = (intervals) ->
  set = {}
  for x in intervals
    for n in [x[0]...x[1]]
      set[n] = true
  
  Object.keys(set).length
  
___________________
sumIntervals = (intervals) -> new Set([].concat(([a...b] for [a, b] in intervals)...)).size

___________________
sumIntervals = (intervals) ->
  res = []
  res = res.concat([start..end-1]) for [start, end] in intervals
  res.filter((e, i) -> res.indexOf(e) == i).length
  
__________________
sumIntervals = (xs) ->
  ys = xs.sort((a, b) ->
    a[0] - (b[0])
  )
  m = -Number.MAX_VALUE
  res = 0
  i = 0
  while i < ys.length
    a = ys[i][0]
    b = ys[i][1]
    m = Math.max(m, a)
    res += Math.max(0, b - m)
    m = Math.max(m, b)
    i++
  res
