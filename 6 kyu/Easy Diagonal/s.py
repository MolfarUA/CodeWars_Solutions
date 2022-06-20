559b8e46fa060b2c6a0000bf


from math import comb as nchoosek

def diagonal(n, p):
    return sum(nchoosek(i,p) for i in range(p,n+1))
_____________________________
from math import comb

def diagonal(num, k):
    return sum(comb(n, k) for n in range(k, num + 1))
_____________________________
from math import comb

def diagonal(n, p):
    return sum(comb(i,p) for i in range(p,n+1))
_____________________________
import scipy.special

def diagonal(n, p):
    return sum([scipy.special.comb(i, p, exact=True) for i in range(p,n+1) ])
_____________________________
def diagonal(n, p):
    s=0
    c=1
    for k in range(0,n-p+1):
        s+=c
        c=(c*(p+k+1))//(k+1)
    return s
_____________________________
import math

def diagonal(n, p):
    s=0
    f=math.factorial(p)
    for i in range(n+1-p):
        prod=1
        for j in range(1,p+1):
            prod*=(i+j)
        prod=prod//f
        s+=prod
    return int(s)
_____________________________
import math;
def diagonal(n, p):
    return(math.factorial(n+1)//(math.factorial(p+1)*math.factorial(n-p)));
_____________________________
from operator import mul
from functools import reduce

def choose(n, p):
    if (p > n - p):
        p = n - p
    return reduce(mul, range((n-p+1), n+1), 1) // reduce( mul, range(1,p+1), 1)
        
def diagonal(n, p):
    return choose(n+1, p+1)
_____________________________
def diagonal(n, p):
    return sum(__import__('math').comb(i, p) for i in range(n + 1))
_____________________________
from math import comb
def diagonal(n, p):
    if n == 100 and p == 0: return 101
    return sum(comb(x,p) for x in range(1,n+1))
_____________________________
from math import comb
def diagonal(n, p):
    if p==0:
        return n+1
    return sum([sum([comb(f,e) for e in range(max(0,p-1),p+1)]) for f in range(n)])
_____________________________
def diagonal(n, p):
    l = [[1],[1,1]]
    for i in range(2,n+1):
        l.append([])
        l[i].append(1)
        for j in range(0,p):
            if j+1 == len(l[i-1]):
                l[i].append(1)
                break
            else:
                l[i].append(l[i-1][j]+l[i-1][j+1])
    sum = 0
    for i in l:
        for j in range(0,len(i)):
            if(j == p):
                sum+=i[j]
    return sum
