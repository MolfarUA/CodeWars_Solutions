54d496788776e49e6b00052f


from collections import defaultdict
def sum_for_list(lst):

    def factors(x):
        p_facs = []
        i = 2
        while x > 1 or x < -1:
            if x % i == 0:
                p_facs.append(i)
                x //= i
            else:
                i += 1
        return list(set(p_facs))
    
    fac_dict = defaultdict(int)
    
    for i in lst:
        for fac in factors(i):
            fac_dict[fac] += i
            
    return sorted([[k,v] for k,v in fac_dict.items()])
________________________________________________
import subprocess
from itertools import chain

def prime_factors (n):
    out = subprocess.run(["factor", str(n)], stdout=subprocess.PIPE)
    out = str(out).split(':')[1].split('\\n')[0].split()
    return [int(s) for s in out]

def sum_for_list(L):
    P  = list(chain(prime_factors(abs(n)) for n in L))
    zP = list(zip(L, P))
    sP = sorted(set(p for l in P for p in l))
    return [[p, sum(e[0] for e in zP if p in e[1])] for p in sP]
________________________________________________
import math
from collections import defaultdict
def sum_for_list(lst):
    def unique_prime_factors(n):
        if n < 0:
            n *= -1
        factors = set()
        while n % 2 == 0:
            factors.add(2)
            n = n / 2
        for i in range(3, int(math.sqrt(n))+1, 2):
            while n % i == 0:
                factors.add(int(i))
                n = n / i
        if n > 2:
            factors.add(int(n))
        return factors
    
    prime_dict = defaultdict(list)
    for x in lst:
        for prime in unique_prime_factors(x):
            prime_dict[prime].append(x)

    return sorted([[prime, sum(vals)] for prime, vals in prime_dict.items()], key=lambda x:x[0])
________________________________________________
def sum_for_list(lst):
    pfs = {}
    result = []
    
    for each in lst:
        primes = pf(abs(each))

        for every in primes:

            if every not in pfs:
                pfs[every] = [each]
            
            else:
                pfs[every].append(each)

    for key, value in sorted(pfs.items()):
        result.append([key, sum(value)])

    return result



def pf(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return list(set(factors))
________________________________________________

def factors(n):
    gaps = [1,2,2,4,2,4,2,4,6,2,6]
    length, cycle = 11, 3
    f, fs, nxt = 2, [], 0
    while f * f <= n:
        while n % f == 0:
            fs.append(f)
            n /= f
        f += gaps[nxt]
        nxt += 1
        if nxt == length:
            nxt = cycle
    if n > 1: fs.append(n)
    return fs

def sum_for_list(lst):
    d={}
    fList=[]
    
    for i in lst:
        f=factors(abs(i))
        f=list(set(f))
        if(i<0):
            print(i,f)
        for n in f:
            if n in d:
                d[n].append(i)
            else:
                d[n]=[i]
    r=[]
    for i in sorted(d):
        r.append([int(i),sum(d[i])])
    
    return r
________________________________________________
from collections import defaultdict
from math import isqrt


def sum_for_list(numbers: list) -> list:
    factors = defaultdict(int)

    for num in numbers:
        for factor in prime_factors(abs(num)):
            factors[factor] += num

    return sorted(map(list, factors.items()))


def prime_factors(n: int) -> set:
    factors = set()

    for i in range(2, isqrt(n + 1)):
        while not n % i:
            factors.add(i)
            n = n // i

    if n > 2:
        factors.add(n)

    return factors
________________________________________________
import math

def sum_for_list(lst):
    common = abs(math.lcm(*lst))
    primes = []
    p = 2
    while(common>1):
        if(common%p==0):
            primes.append(p)
            common //= p
            continue
        p += 1
    primes = set(primes)
    result = []
    for p in primes:
        sum = 0
        for item in lst:
            if(abs(item)%p==0): sum+=item
        result.append([p,sum])
        
    result = sorted(result)
    return result
________________________________________________
from math import isqrt


def unique_prime_factors(x: int) -> list[int]:
    x = abs(x)
    result: list[int] = []
    if x % 2 == 0:
        result.append(2)
        while x % 2 == 0:
            x //= 2
    for p in range(3, isqrt(x) + 1, 2):
        if x % p == 0:
            result.append(p)
        while x % p == 0:
            x //= p
    if x > 2:
        result.append(x)
    return result


def sum_for_list(lst: list[int]) -> list[list[int, int]]:
    result: list[list[int, int]] = []
    for elem in lst:
        for prime in unique_prime_factors(elem):
            found = False
            for r in result:
                if prime == r[0]:
                    r[1] += elem
                    found = True
                    break
            if not found:
                result.append([prime, elem])
    return sorted(result, key=lambda e: e[0])
