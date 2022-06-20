559b8e46fa060b2c6a0000bf


choose = (n, k) ->
  res = 1
  i = 1
  while i <= k
    res *= (n - i + 1) / i
    i++
  Math.round res

diagonal = (n, p) ->
  choose n + 1, p + 1
_____________________________
choose = (n, k) ->
  res = 1
  i = 1
  while i <= k
    res = res * (n - i + 1) / i
    i++
  Math.round res

diagonal = (n, p) ->
  choose n + 1, p + 1
_____________________________
binorm = (n, p) -> if p == 0 then 1 else (n+1-p)*binorm(n,p-1)/p
diagonal = (n, p) -> binorm(n,p) * (n+1)/(p+1);
