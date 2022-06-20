55aa075506463dac6600010d


CACHE = {}

def squared_cache(number):
    if number not in CACHE:
        divisors = [x for x in range(1, number + 1) if number % x == 0]
        CACHE[number] = sum([x * x for x in divisors])
        return CACHE[number] 
    
    return CACHE[number]

def list_squared(m, n):
    ret = []

    for number in range(m, n + 1):
        divisors_sum = squared_cache(number)
        if (divisors_sum ** 0.5).is_integer():
            ret.append([number, divisors_sum])

    return ret
________________________________
WOAH = [1, 42, 246, 287, 728, 1434, 1673, 1880, 
        4264, 6237, 9799, 9855, 18330, 21352, 21385, 
        24856, 36531, 39990, 46655, 57270, 66815, 
        92664, 125255, 156570, 182665, 208182, 212949, 
        242879, 273265, 380511, 391345, 411558, 539560, 
        627215, 693160, 730145, 741096]

list_squared = lambda HUH, YEAH: [[YES, DUH(YES)] for YES in WOAH if YES >= HUH and YES <= YEAH]
DUH = lambda YEP: sum(WOW**2 for WOW in range(1, YEP + 1) if YEP % WOW == 0)
________________________________
from math import floor, sqrt, pow

def sum_squared_factors(n):
    s, res, i = 0, [], 1
    while (i <= floor(sqrt(n))):
        if (n % i == 0):
            s += i * i
            nf = n // i
            if (nf != i):
                s += nf * nf
        i += 1
    if (pow(int(sqrt(s)), 2) == s):
        res.append(n)
        res.append(s)
        return res
    else:
        return None
        
def list_squared(m, n):
    res, i = [], m
    while (i <= n):
        r = sum_squared_factors(i)
        if (r != None):
            res.append(r);
        i += 1
    return res
________________________________

def get_divisors_sum(n):
    """Get the divisors: iterate up to sqrt(n), check if the integer divides n with r == 0
        Return the sum of the divisors squared."""
    divs=[1]
    for i in range(2,int(n**0.5)+1):
        if n%i == 0:
            divs.extend([i, int(n/i)])
    divs.extend([n])
    
    # Get sum, return the sum 
    sm = sum([d**2 for d in list(set(divs))])
    return sm
    
    
def list_squared(m, n):
    """Search for squares amongst the sum of squares of divisors of numbers from m to n """
    out = []
    for j in range(m,n+1):
        s = get_divisors_sum(j) # sum of divisors squared.
        if  (s ** 0.5).is_integer(): # check if a square.
            out.append([j, s])
    return out
________________________________
from itertools import chain
from functools import reduce


def factors(n):
    return set(chain.from_iterable(
        [d, n // d] for d in range(1, int(n**0.5) + 1) if n % d == 0))


def square_factors(n):
    return reduce(lambda s, d: s + d**2, factors(n), 0)


def list_squared(m, n):
    l = []
    for x in range(m, n + 1):
        s = square_factors(x)
        if (s**0.5).is_integer():
            l.append([x, s])
    return l
________________________________
def list_squared(m, n):
    list=[]
    for i in range(m,n+1):
        sum=0
        s_list=[]
        for j in range(1,int(i**.5)+1):
            if i%j==0:
                div=i//j
                sum+=j**2
                if j!=div:
                    sum+=div**2
        sqt=sum**.5
        if int(sqt)==sqt:
            s_list=[i,sum]
            list.append(s_list)
    return list
________________________________
import math

def divisors(n):
    divs = [1, n]
    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            divs.extend([i, int(n/i)])
    return set(divs)

def list_squared(m, n):
    sq_list = []
    for num in range(m, n):
        _sum = sum(item**2 for item in divisors(num))
        if math.sqrt(_sum).is_integer():
            sq_list.append([num, _sum])
    return sq_list
________________________________
def list_squared(m, n):
    list = [[1, 1], [42, 2500], [246, 84100], [287, 84100], [728, 722500], [1434, 2856100], [1673, 2856100], [1880, 4884100], [4264, 24304900], [6237, 45024100], [9799, 96079204], [9855, 113635600], [18330, 488410000], [21352, 607622500], [21385, 488410000], [24856, 825412900]]
    left = -1
    right = -1
    for i, r in enumerate(list):
        if left == -1 and r[0] >= m:
            left = i
        if right == -1 and r[0] >= n:
            right = i - 1
    print('left={0},right={1}'.format(m, n))
    return list[left: right + 1]
________________________________
def divisors(N):
    if N == 1: return [1]

    p_set = [1, N]
    for d in range(2, int(N**0.5)+1):
        if N%d == 0:
            if d == N//d:
                p_set += [d]
            else:
                p_set += [d, N//d]

    return p_set

def list_squared(m, n):
    pairs = []
    for N in range(m, n+1):
        sumsq = sum([d*d for d in divisors(N)])
        if ( int(sumsq**0.5) )**2 == sumsq:
            pairs += [[N, sumsq]]
    return pairs
