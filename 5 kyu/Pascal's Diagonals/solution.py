def generate_diagonal(d, l):
    result = [1] if l else []
    for k in range(1, l):
        result.append(result[-1] * (d+k) // k)
    return result
_______________________________
def generate_diagonal(n, l):
    d = []
    for k in range(l):
        d.append(d[-1] * (n + k) // k if d else 1)
    return d
_______________________________
from scipy.special import comb
def generate_diagonal(n, l):
    return [comb(n + a, a, exact=True) for a in range(l)]
_______________________________
def generate_diagonal(n, l):
    if n==0:
        c=[]
        while l>0:
            c+=[1]
            l-=1
        return c
    if l==0 and n==0:
        return '[]'
    else:
        i=n+l
        q=[]
        o=[]
        def triangles():
            p =[1]
            while True:
               yield p
               p =[1]+[p[x]+p[x+1] for x in range(len(p)-1)]+[1]
        for t in triangles():
            if i>0:
                i-=1
                q.append(t)
            else:
                break
        for t in range(l):
            r=q[n][t]
            n+=1
            o.append(r)
        return o
_______________________________
#C(n, k) == n!/(k!(n-k)!) simplifies to  a/b
# where    a ==  n*(n-1)*(n-2)*...*(n-(k-2))*(n-(k-1))
#          b ==  (k-1)!
def efficientCombination(n,k):
    from math import gcd
    
    #a and b are defined in above comment
    a,b = 1,1

    if k==0:
        return 1

    #Since C(n,k) == C(n,n-k), so take n-k when it's smaller than k
    if n-k < k : 
        k = n - k

    while k: 
        a *= n
        b *= k 
        
        m = gcd(a, b) 
        a //= m 
        b //= m 
        
        n -= 1
        k -= 1
    #---end while

    return a

#-----end function


#d is the deisred diagonal from right to left (starting count at 0), and amt is 
# the number of elements desired from that diagonal
def generate_diagonal(d, amt):
    diagElements = []

    for n in range(d, amt + d, 1):
        valOnDiag = efficientCombination(n, d)
        diagElements.append(valOnDiag)

    return diagElements

#---end function
_______________________________
from math import factorial

def generate_diagonal(n, l):
    return [factorial(n+i) // (factorial(n) * factorial(i)) for i in range(l)]
_______________________________
from math import comb

def generate_diagonal(k, num):
    return [comb(n, k) for n in range(k, k + num)]
_______________________________
from math import comb

def generate_diagonal(n, l):
    if l == 0: return []
    ret = [comb(n+i, n) for i in range(l)]
    return ret
_______________________________
def generate_diagonal(n, l):
    import math
    return [math.comb(n+i, i) for i in range(l)]
_______________________________
from operator import add
from itertools import accumulate

def generate_diagonal(n, l):
    res = [1]*l
    for _ in range(n):
        res = list(accumulate(res[1:], add, initial=1))
    return res if l else []
_______________________________
import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    return  reduce(op.mul, range(n, n-r, -1), 1)// reduce(op.mul, range(1, r+1), 1)

def generate_diagonal(n, l):
    mx = []
    i,j = n,0
    while i < n+l:
        mx.append(ncr(i,j))
        i+=1
        j+=1
    return mx
