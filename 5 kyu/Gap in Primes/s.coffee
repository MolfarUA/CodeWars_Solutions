561e9c843a2ef5a40c0000a4


isPrime = (n) ->
  if n % 2 == 0
    return false
  i = 3
  while i * i <= n
    if n % i == 0
      return false
    i += 2
  true

gap = (g, m, n) ->
  a = 0
  b = 0
  i = m
  while i <= n
    if b - a == g
      return [a, b]
    if isPrime(i)
      a = b
      b = i
    i++
  null
__________________________________
prime = (n) ->
  if n == 2
    true
  else if n < 2 or n % 2 == 0
    false
  else
    i = 3
    while i <= Math.sqrt(n)
      if n % i == 0
        return false
      i += 2
    true

gap = (g, m, n) ->
  res = []
  i = m
  while i < n + 1
    if prime(i)
      res.push i
      break
    i++
  loop
    j = i + 1
    while j < n + 1
      if prime(j)
        if j - i == g
          res.push j
          return res
        else
          res[0] = j
          i = j
      j++
    return null
  return
__________________________________
gap = (g, m, n) ->
  while m < n
    if isPrime(m) and isPrime(m+g) and ([(m+1)..(m+g-1)].every (i) -> !isPrime(i))
      return [m,m+g]
    m++
  return null
  
isPrime = (n) ->
  return false if n isnt ~~n or n <= 1 or n % 2 is 0 and n isnt 2 
  return false for r in [3..Math.ceil(Math.sqrt(n))] by 2 when n % r is 0
  return true
