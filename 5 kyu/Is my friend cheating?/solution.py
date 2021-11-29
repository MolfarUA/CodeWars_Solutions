import unittest

def removNb (n):
    seen = set()
    result = []
    total = sum (range (1, n+1))
    for item in range (1, n+1):
        searched = (total - item) / (item + 1)
        if searched in seen:
            result.append ((int(searched), item))
            result.append ((item, int(searched)))
        else:
            seen.add(item)
    return sorted (result, key=lambda minFirst: minFirst[0])

test = unittest.TestCase()

test.assertEquals(removNb(100), [])
test.assertEquals(removNb(26), [(15, 21), (21, 15)])
################################
def removNb(n):
    sum = n*(n + 1)/2  
    return [(x, (sum - x) / (x + 1)) for x in xrange(1, n+1) if (sum - x) % (x + 1) == 0 and 1 <= (sum - x) / (x + 1) <= n]
#########################
def removNb(n):
    total = n*(n+1)/2
    sol = []
    for a in range(1,n+1):
        b = (total-a)/(a+1.0)
        if b.is_integer() and b <= n:
            sol.append((a,int(b)))
    return sol
####################
def removNb(n):
    s = n * (n + 1) / 2
    return [((s-a)//(a+1), a) for a in range(n-1, n//2, -1)  if (s-a) % (a+1) == 0]
################
import math

def removNb(n):
    res = []
    tot = sum(range(n+1))
    for a in range(n,int(math.sqrt(tot)),-1):
        b = tot%a        
        if a*b==tot-a-b:
            res.append((b,a))
            res.append((a,b))
    return sorted(res)
##################
def removNb(n):
    b = lambda a: ((n*n + n)/2 - a)/float(a + 1)
    c = lambda a: int(b(a)) == b(a) and 0 < b(a) <= n
    return [(a, b(a)) for a in xrange(1, n + 1) if c(a)]
###################
def removNb(n):
    s = int(n * (n +1) / 2)
    limit = int(n / 2)
    res = []
    for a in range(limit, n + 1):
        b = s - a
        if (b % (a + 1) == 0):
            res.append( (a, int(b / (a + 1)) ))            
    res = sorted(res, key = lambda x : x[0])
    return res
####################
def removNb(n):
    s = n * (n + 1) // 2
    res = []
    for b in range(n, 0, -1):
        a, m = divmod((s - b), (b + 1))
        if a > n:
            break
        if m == 0:
            res.append((a, b))
    return sorted(res)
#####################
def removNb(n):
    s = n * (n+1) // 2
    return [(i, (s - i) // (i + 1))
            for i in range((s - n) // (n + 1), n)
            if (s - i) % (i + 1) == 0]
#####################
def remov_nb(n):
    # We basically have to find pairs of a, b such that, in a sequence
    # 1, 2, 3,..., n-1, n; sum(1, 2, 3,..., n-1, n) - a - b = a*b.
    sigma_n = n*(1+n)/2  # == sum(1, 2, 3,..., n-1, n)
    return ([(a, (sigma_n - a)/(1 + a)) for a in range(2, n) 
             if (sigma_n - a)/(1 + a)%1 == 0 and (sigma_n - a)/(1 + a) < n])
##################
def remov_nb(n):
    s = (n * (n+1)) // 2
    res = []
    
    for i in range(1, n+1):
        if (s - i) % (i + 1) == 0:
            j = (s - i) // (i + 1)
            if i != j and j <= n and i * j == s - i - j:
                res.append((i, j))
    return res
######################
def remov_nb(n):
    sm =  n * (n + 1)/2
    lst = []
    for i in range(1, n+1):
        x,y = divmod(sm - i, i + 1)
        if y == 0:
            if x <= n:
                lst.append((i, x))
    return lst
