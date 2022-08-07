55e785dfcb59864f200000d9


isPrime = (n) ->
  for i in [2..Math.sqrt(n)]
    return false if n % i == 0
  n > 1
  
countSpecMult = (n, mxval) ->
  p = 2
  i = 3
  while n > 1
    if isPrime(i)
      p *= i
      n -= 1
    i += 2
  console.log(p)
  mxval // p
_________________________________
countSpecMult = (n, k) ->
  primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
  i = 0
  x = 1
  while i < n
    x *= primes[i]
    i++
  Math.floor k / x
_________________________________
is_simple = (int) ->
  return false if int <= 1
  for range in [2...int]
    if( int % range == 0 )
      return false
  return true


countSpecMult = (n, mxval) ->
  primes = []
  primes_mult = 1
  sum = 0
  answer = 0
  i = 2
  while( primes.length<n and i<mxval )
    if( is_simple(i) )
      primes.push( i )
    i++
  
  for integer in primes
    primes_mult = primes_mult*integer
  while( sum < mxval )
    answer++
    sum += primes_mult 
  answer-1
