58e230e5e24dde0996000070


def nextPrime(n):
    while True:
        n += 1
        if n == 2 or (n > 2 and n % 2 and all(n % i for i in range(3, int(n**0.5) + 1, 2))): return n
__________________________
from gmpy2 import next_prime
__________________________
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True


def next_prime(n):
    n += 1
    while not is_prime(n):
        n += 1
    return n
__________________________
def nextPrime(n):
    p = n + n % 2 + 1 if n > 1 else 2
    while not all(p % d for d in range(3, int(p ** .5) + 1)): p += 2
    return p
__________________________
def is_prime(n):    
    if n in (2, 3, 5, 7):
        return True
    elif n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n < 0 or n == 1:
        return False     
    d = 7
    while d <= n**.5:
        if n % d == 0:
            return False
        d += 2
    return True

def next_prime(n):
    if n in (0, 1):
        return 2
    if n % 2 == 0 and is_prime(n+1):
        return n + 1
    else:
        n = n+1 if n % 2 == 0 else n+2
        while not is_prime(n): n += 2
        return n
__________________________
def next_prime(n):
    if n<=1:
        return 2
    if n%2==0:
        n-=1
    while True:
        n+=2
        a = int(n**0.5)+2
        for i in range(3,a,2):
            if n%i==0:
                break
        else:
            return n
__________________________
import math
def next_prime(n):
    def isprime(x):
        if x<2:
            return False
        elif x==2:
            return True
        max_div = math.floor(math.sqrt(x))
        for i in range(2,max_div+1):
            if x%i==0:
                return False
                break
        return True
    for i in range(n+1,n+100000):
        if isprime(i):
            return i
__________________________
from itertools import count

def next_prime(n):
    return next(i for i in count(n<2 and 2 or n&1 and n+2 or n+1, 2) if all(i%j for j in range(3, int(i**.5)+1, 2)))
