findNb = (m) ->
    n = 0
    vol = 0
    while vol < m
        n += 1
        vol += n ** 3
    if vol != m then -1 else n
_______________________________
findNb = (m) ->
  i = 1
  while m > 0
    m = m - Math.pow(i, 3)
    if m == 0
      return i
    else if m < 0
      return -1
    i++
_______________________________
findNb = (m) ->
  limit = ~ ~(Math.sqrt(2) * m ** 0.25 + 1)
  i = 0
  while i <= limit
    if i * i * (i + 1) * (i + 1) == 4 * m
      return i
    i++
  -1
_______________________________
findNb = (m) ->
  s = 0
  n = 0
  while s < m
    s += ++n ** 3
  if s == m then n else -1
_______________________________
findNb = (sum, i = 1) -> if (-> sum -= (i++)**3 while sum > 0; sum)() == 0 then i-1 else -1
