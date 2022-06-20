55e7d9d63bdc3caa2500007d



from functools import reduce
from math import gcd


def smallest(n):
    return reduce(lambda a, b: a * b // gcd(a, b), range(1, n+1))
________________________________
def smallest(n):
    x, y, m = 1, 1, 1
    while m <= n:
        if x % m == 0:
            m += 1
            y = int(x)
        else:
            x += y
    return x
________________________________
from numpy import lcm
from functools import reduce

def smallest(n):
    return reduce(lcm, range(1, n + 1))
________________________________
from functools import reduce
from math import gcd

def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b

def smallest(number: int) -> int:
    return reduce(lcm, range(1, number + 1))
________________________________
import numpy as np

def smallest(n):
    return np.lcm.reduce(range(1, n + 1))
________________________________
from gmpy2 import next_prime
from math import log

prod = lambda A: A[0]*prod(A[1:]) if A else 1

def smallest(n):
    P = [2]
    while P[-1]<=n: P.append(int(next_prime(P[-1])))
    P = P[:-1]
    return prod([p**(int(log(n)/log(p))) for p in P])
________________________________
from functools import reduce
from math import gcd
lcm = lambda x,y: x*y//gcd(x, y)

# Note: there is a lcm function in numpy 1.17 but codewars uses 1.14
def smallest(n):
    return reduce(lcm, range(1, n+1))
________________________________
from math import *

def smallest(n):
    res = 1
    for i in range(1, n + 1):
        res = res * i // gcd(res, i)
    return res
________________________________
from functools import reduce
from math import gcd

def smallest(n):
    return reduce(lambda x, y: x * y // gcd(x, y), range(1, n+1))
________________________________
from functools import reduce
from operator import mul

def smallest(n):
    def satisfied(x):
        return all (x % d == 0 for d in range(2, n+1))
    result = reduce(mul, range(1, n+1))
    for i in range(2, n):
        while (result % i == 0 and satisfied(result // i)):
            result //= i
    return result
________________________________
def gcd(a, b):
    return a if not b else gcd(b, a % b)

def lcm(a, b):
    return a * b / gcd(a, b)

def smallest(n):
    res = 1
    for i in range(1, n + 1):
        res = lcm(i, res)
    return res
