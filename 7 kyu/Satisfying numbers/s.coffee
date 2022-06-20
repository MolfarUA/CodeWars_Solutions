55e7d9d63bdc3caa2500007d


gcd = (a, b) -> if b then gcd b, a % b else a

lcm = (a, b) -> a * b // gcd a, b

smallest = (number) -> [1..number].reduce lcm
________________________________
smallest = (n) ->
  if n == 1
    1
  else
    lcm n, smallest(n - 1)

lcm = (a, b) ->
  if a * b
    a * b / gcd(a, b)
  else
    0

gcd = (a, b) ->
  if b
    gcd b, a % b
  else
    a
________________________________
smallest = (n) ->
  gcd = (a, b) -> if b == 0 then a else gcd(b, a % b)
  lcm = (a, b) -> a * b // gcd(a, b)
  [1..n].reduce(lcm)
