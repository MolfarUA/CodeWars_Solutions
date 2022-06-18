56d0a591c6c8b466ca00118b


def is_triangular(t):
    x = int((t*2)**0.5)
    return t == x*(x+1)/2
__________________________
def is_triangular(t):
    return (8 * t + 1)**.5 % 1 == 0
__________________________
def is_triangular(t):
    return (8 * t + 1) ** 0.5 % 1 == 0
__________________________
def is_triangular(n):
    a = int((n * 2)**0.5)
    return n * 2 == a * (a + 1)
__________________________
def is_triangular(t):
    return not (8 * t + 1)**.5 % 1
__________________________
def is_triangular(n):
    return ((-1 + (1 + 8 * n)**.5) / 2) % 1 == 0
__________________________
from math import sqrt
def is_triangular(t):
    n = (sqrt(8 * t + 1)-1)/2
    return False if n - int(n) > 0 else True
__________________________
def is_triangular(t):
    return (-1 + (1 + 8 * t) ** 0.5)/2. == int((-1 + (1 + 8 * t) ** 0.5)/2.)
__________________________
TRIANGULAR = { x*(x+1)/2 for x in range(10000) }

is_triangular = TRIANGULAR.__contains__
__________________________
def is_triangular(t):
    sqr = int((2*t) ** 0.5)
    return 2 * t == sqr * (sqr+1)
__________________________
import math
def is_triangular(t):
    sqr = int(math.sqrt(2*t))
    return 2 * t == sqr * (sqr+1)
__________________________
def is_triangular(t):
    n = 1
    while True:
        x = n * (n + 1) / 2
        if x == t:
            return True
        elif x > t:
            return False
        n +=1
