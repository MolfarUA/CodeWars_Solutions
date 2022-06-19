5b71af678adeae41df00008c


from math import hypot

def shortest_distance(*args):
    a, b, c = sorted(args)
    return hypot(a + b, c)
____________________________
def shortest_distance(a,b,c):
    a, b, c = sorted([a,b,c])
    return ((a+b)**2 + c**2)**0.5
____________________________
from math import hypot

def shortest_distance(a, b, c):
    x, y, z = sorted([a, b, c])
    return hypot(x + y, z)
____________________________
import math

def shortest_distance(a, b, c):
    if a > b and a > c:
        return math.sqrt( (b+c)**2 + a**2)
    if b > a and b > c:
        return math.sqrt( (a+c)**2 + b**2)
    return math.sqrt( (a+b)**2 + c**2)
____________________________
def shortest_distance(a, b, c):
    r1 = a * a + (b + c) * (b + c)
    r2 = b * b + (a + c) * (a + c)
    r3 = c * c + (a + b) * (a + b)
    return min(r1, r2, r3) ** 0.5
____________________________
def shortest_distance(a, b, c):
    return min( ((a+b)**2 + c**2)**0.5, ((a+c)**2 + b**2)**0.5, (a**2 + (b+c)**2)**0.5 )
____________________________
from math import hypot

def shortest_distance(a, b, c):
    return min(hypot(a, b+c), hypot(b, a+c), hypot(c, a+b))
____________________________
def shortest_distance(a, b, c):
    list = [a, b, c]
    list.sort()
    result = []
    eps = .004
    testcase = 0

    while testcase <= list[2]:

        d = (testcase** 2 + list[0]** 2)** .5
        e = ((list[2]-testcase)** 2 + list[1]** 2)** .5
        testcase += eps
        result.append(d + e)
        
    return min(result)
____________________________
def shortest_distance(a, b, c):
    dim = sorted([a, b, c])
    return ((dim[0] + dim[1]) ** 2 + dim[2] ** 2) ** .5
____________________________
def shortest_distance(a, b, c):
    dist = [(c*c+(a+b)**2)**.5, (b*b+(a+c)**2)**.5, (a*a+(b+c)**2)**.5]
    return min(dist)
