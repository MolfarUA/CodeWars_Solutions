55e785dfcb59864f200000d9


def count_specMult(n,maxVal):
  prod = 1
  p = primes()
  for i in xrange(n): prod *= p.next()
  return maxVal / prod

def primes():
  yield 2
  yield 3
  i = 6
  isPrime = lambda n: all(n % i for i in xrange(3, int(n**.5+1), 2))
  while True:
    if isPrime(i-1): yield(i-1)
    if isPrime(i+1): yield(i+1)
    i += 6
_________________________________
from gmpy2 import next_prime as np
from math import prod
def count_specMult(n, t):
    a, b = 2, []
    while n>0:
        b, a, n = b+[a], np(a), n-1
    return t//prod(b)
_________________________________
from math import ceil, sqrt

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 
    71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131]

def count_specMult(p_count, n_max):
    f = 1
    for i in range(p_count):
        f *= PRIMES[i]
    return n_max // f
_________________________________
multiple = [2, 6, 30, 210, 2310, 30030, 510510, 9699690, 223092870, 6469693230]

def count_specMult(m, max_val):
    return len(range(1, max_val, multiple[m-1])) - 1
_________________________________
from functools import reduce
def sieve(n):
    m = set()
    for i in range(2, n + 1):
        if i not in m:
            yield i
            m.update(range(i * i, n + 1, i))
def count_specMult(n, mx):
    p = list(sieve(100))[0:n]
    m = reduce(lambda x,y : x * y, p)
    i = 0
    mult = m
    while mult  < mx:
        mult += m
        i += 1
    return i
_________________________________
def is_prime(num):
    return num == 2 or all(num % k for k in [2] + list(range(3, int(num**0.5) + 1, 2)))

def count_specMult(n, max_val):
    cur_n, cur_dv, tot_dv = n, 2, 1
    while cur_n:
        if is_prime(cur_dv):
            cur_n -= 1
            tot_dv *= cur_dv
        cur_dv += 1
    
    return max_val // tot_dv
_________________________________
from gmpy2 import next_prime
from functools import lru_cache

@lru_cache(maxsize=None)
def mult(n):
    if n == 0: return 2, 1
    x, y = mult(n-1)
    return next_prime(x), x*y

def count_specMult(n, maxVal):
    return maxVal // mult(n)[1]
_________________________________
from functools import reduce
from operator import mul

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def count_specMult(n, limit):
    return (limit - 1) // reduce(mul, PRIMES[:n])
