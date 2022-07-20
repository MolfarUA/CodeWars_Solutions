54d496788776e49e6b00052f


primeFactors = (m) ->
  n = Math.abs(m)
  if !n or n < 2
    return []
  f = []
  i = 2
  while i <= n
    while n % i == 0
      f.push i
      n /= i
    i++
  f

onlyUnique = (value, index, self) ->
  self.indexOf(value) == index

primeFactorsOfList = (lst) ->
  [].concat.apply([], lst.map(primeFactors)).filter(onlyUnique).sort (a, b) ->
    a - b

sumOfDividedOne = (n, lst) ->
  total = lst.reduce(((a, b) ->
    if b % n == 0
      a + b
    else
      a
  ), 0)
  total

sumOfDivided = (lst) ->
  primeFactorsOfList(lst).map (x) ->
    [
      x
      sumOfDividedOne(x, lst)
    ]
________________________________________________
sumOfDivided = (ls) ->
  max = Math.max ls.map(Math.abs)...
  primes=[2]
  for i in [3..max] by 2 when !primes.some((a)->i%a==0)
    primes.push i
  for i in primes when (fl=ls.filter (a)->a%%i==0).length
    [i,fl.reduce (a,b)->a+b]
________________________________________________
sumOfDivided = (lst) ->
  primes = (x) ->
    div = (x, p) -> return div(x / p, p) if (x % p is 0); x
    p for p in [2..Math.abs(x)] when x isnt x = div(x, p)

  P = (primes(i) for i in lst)
  return [] unless P.length
  Q = P.reduce((x, y) -> x.concat y.filter((i) -> x.indexOf(i) < 0)).sort((a, b) -> a - b)
  Q.map (p) -> [p, lst.reduce ((x, y) -> if y % p is 0 then x + y else x), 0]
