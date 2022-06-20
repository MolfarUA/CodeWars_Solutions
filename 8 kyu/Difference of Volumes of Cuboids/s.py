58cb43f4256836ed95000f97


from numpy import prod

def find_difference(a, b):
    return abs(prod(a) - prod(b))
________________________
def find_difference(a, b):
    return abs((a[1]*a[2]*a[0])-b[1]*b[2]*b[0])
________________________
def find_difference(a, b):
    return abs(a[0] * a[1] * a[2] - b[0] * b[1] * b[2])
________________________
from operator import mul
from functools import reduce
def find_difference(a, b):
    return abs(reduce(mul, a) - reduce(mul, b))
________________________
def find_difference(a, b):
    A = B = 1
    for i, j in zip(a, b):
        A *= i
        B *= j
    return abs(A - B)
________________________
def find_difference(a, b):
    cuboid_a = 1
    cuboid_b = 1
    for i in a:
        cuboid_a = cuboid_a * i
    for x in b:
        cuboid_b = cuboid_b * x
    
    return abs(cuboid_a - cuboid_b)
________________________
def find_difference(a, b):
    ans = a[0] * a[1] * a[2] - b[0] * b[1] * b[2]
    if ans < 0:
        return ans * -1
    return ans
________________________
def find_difference(a, b):
    resa = 1
    resb = 1
    for num in a:
        resa *= num
    for num in b:
        resb *= num
    return abs(resa-resb)
________________________
def find_difference(a, b):
    c1,c2 = 1,1;
    j=0
    
    for i in a:
        c1 = c1*a[j]
        j+=1
    j=0
    for i in b:
        c2 = c2*b[j]
        j+=1

    return abs(c1-c2)
________________________
def find_difference(a, b):
    n = 1
    m = 1
    for i in a:
        n *=i
    for k in b:
        m *=k
    return abs(n-m)
________________________
def find_difference(a, b):
    result = 0
    for_a = 1
    for_b = 1
    for i in a:
        for_a = for_a * i
    for i in b:
        for_b = for_b * i
    result = for_a - for_b
    if result < 0:
        result = result * -1
    return result
________________________
def find_difference(a, b):
    sum1=1
    sum2=1
    for x in a:
        sum1 *= x
        
    for x in b:
        sum2 *= x
        
    return abs(sum1-sum2)
________________________
def find_difference(a, b):
    c=1
    d=1
    for i in a:
        c=c*i
    for i in b:
        d=d*i
    return c-d if c>d else d-c
