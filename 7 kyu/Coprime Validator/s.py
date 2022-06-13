from fractions import gcd

def are_coprime(n, m):
  return gcd(n, m) == 1
___________________________
from math import gcd

def are_coprime(n , m):
    return gcd(n, m) == 1
___________________________
def are_coprime(n,m):
    final_list=[]
    x1=print_factors(n)
    x2=print_factors(m)
    for i in x1:
        for j in x2:
            if i==j:
                final_list.append(i)
    print(final_list)
    if final_list==[1]:
        return True
    return False

def print_factors(x):
    factores=[]
    for i in range(1, x + 1):
        if x % i == 0:
            factores.append(i)
    return factores
___________________________
def are_coprime(n,m):
    if n ==1:
        return True
    elif m%n==0:
        return False
    else:
        n, m = m%n, n
        return are_coprime(n,m)
___________________________
def are_coprime(a,b):
    for i in range(2,max(a,b)//2+1):
        if a%i==0 and b%i==0:
            return False
    return True
___________________________
def are_coprime(n, m):
    n_factors = set()
    m_factors = set()
    for i in range(1, n + 1):
        if n % i == 0:
            n_factors.add(i)
    for j in range(1, m + 1):
        if m % j == 0:
            m_factors.add(j)
    return len(n_factors.intersection(m_factors)) <= 1
___________________________
def are_coprime(n,m):
    n,m = sorted([n,m])
    while m:
        n,m = m,n%m
    return n == 1
