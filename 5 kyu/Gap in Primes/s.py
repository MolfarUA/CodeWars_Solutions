561e9c843a2ef5a40c0000a4


def gap(g, m, n):
    previous_prime = n
    for i in range(m, n + 1):
        if is_prime(i):
            if i - previous_prime == g: 
                return [previous_prime, i]
            previous_prime = i
    return None
            
    
def is_prime(n):
    for i in range(2, int(n**.5 + 1)):
        if n % i == 0:
            return False
    return True
__________________________________
def gap(g, m, n):
    prev = 2
    for x in range(m|1, n + 1, 2):
        if all(x%d for d in range(3, int(x**.5) + 1, 2)):
            if x - prev == g: return [prev, x]
            prev = x
__________________________________
def is_prime(a):
    return all(a % i for i in range(2, int(a**0.5)+1))
        
def gap(g, m, n):
    for a in range(m, n-g+1):
        if is_prime(a) and is_prime(a+g) and not any(is_prime(j) for j in range(a+1, a+g)):
            return [a, a+g]
__________________________________
from gmpy2 import next_prime


def gap(g, m, n):
    prev = next_prime(m - 1)

    while prev < n:
        p = next_prime(prev)

        if p - prev == g:
            return [prev, p]

        prev = p
__________________________________
def gap(g, m, n):
    prime = 0
    for i in range(m,n+1):
        for j in range(2,int(i**0.5)+1):
            if i%j == 0:
                break
        else: 
            if i - prime == g: return [prime,i]
            else: prime = i
__________________________________
import numpy as np

sieve = np.ones(12_000_000, dtype=bool)
sieve[0] = sieve[1] = 0
sieve[2*2::2] = 0
for i in range(3, int(len(sieve)**0.5)+1, 2):
    if sieve[i]:
        sieve[i*i::i] = 0
primes = np.array([i for i, x in enumerate(sieve) if x], dtype=int)

def gap(g, m, n):
    i = primes.searchsorted(m)
    j = primes.searchsorted(n)
    for k in range(i, j+1):
        if primes[k+1] - primes[k] == g:
            return list(primes[k:k+2])
__________________________________
def gap(g, m, n):
    prev = None
    for i in range(m if m%2 else m+1, n+1, 2):
        isPrime = True
        for k in range(2, round(i**0.5)+1):
            if i%k == 0:
                isPrime = False
                break
        if isPrime:
            if prev:
                if i-prev == g:
                    return [prev, i]
            prev = i
    return None
__________________________________
import math

def gap(g, start,stop):
    k = math.ceil((start - 1)/6)
    UltPrime ,p1,p2 = 0,0,0 
    
    while p1<=stop or p2<=stop: 
        p1, p2 = 6*k - 1, 6*k + 1
        if start<=p1<=stop and IsPrime(p1):  
            if (p1 - UltPrime) == g and UltPrime > 0: return [UltPrime,p1]
            else: UltPrime = p1
            
        if start<=p2<=stop  and IsPrime(p2):
            if (p2 - UltPrime) == g and UltPrime > 0: return [UltPrime,p2]
            else: UltPrime = p2
            
        k = k + 1   
    return None
               
def IsPrime(n):   
    d, s = n - 1, 0
    while not d % 2: d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653:         return not any(TryComposite(a, d, n, s) for a in (2, 3))
    if n < 25326001:        return not any(TryComposite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467:    return [not any(TryComposite(a, d, n, s) for a in (2, 3, 5, 7)),False][n == 3215031751]
    if n < 2152302898747:   return not any(TryComposite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383:   return not any(TryComposite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321: return not any(TryComposite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))

#Test de primalidad de Miller-Rabin
def TryComposite(a, d, n, s):
    if pow(a, d, n) == 1: return False
    for i in range(s): 
        if pow(a, 2**i * d, n) == n-1: return False
    return True # n is definitely composite
__________________________________
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**(1/2)+1)):
        if n % i == 0:
            return False
    return True

def gap(g, m, n):
    start = 2
    while (m <= n):
        print(m)
        if is_prime(m):
            if m - start == g:
                return [start, m]
            start = m
        m += 1
    return None
__________________________________
def isPrime(n):
    for i in range(2, int(n**.5+1)):
        if n % i == 0:
            return False
    return True

def gap(gap, en, st):
    for cur in range(en, st+1):
        if isPrime(cur) and isPrime(cur+gap):
            isgap = True
            for check in range(cur+1,cur+gap):
                if isPrime(check):
                    isgap = False
            if isgap:
                return [cur,cur+gap]
    return None
__________________________________
def is_prime(number):
    for i in range(2, int(number**0.5 + 1)):
        if number % i == 0:
            return False
    return True

def gap(g, m, n):
    previous = n
    for i in range(m, n + 1):
        if is_prime(i):
            if i - previous == g: 
                return [previous, i]
            previous = i
    return None
__________________________________
import math

def gap(g, m, n):
    print(g,m,n)
    
    last_prime = 2

    for p in range(m, n+1):
        if is_prime(p):
            if p - last_prime == g:
                return [last_prime, p]

            last_prime = p

    return None


def is_prime(n):
    
    for x in range(2, int(math.sqrt(n)+1)):
        if n % x == 0:
            return False

    return True
__________________________________
def isPrime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False

    return True

def gap(g, m, n):
    for i in range(m, n+1):
        if isPrime(i):
            j = i
            while True:
                j += 1
                if isPrime(j):
                    if j - i == g:
                        return [i, j]
                    else: 
                        break
    return None
