5a805d8cafa10f8b930005ba


def nearest_sq(n):
    return round(n ** 0.5) ** 2
__________________________
def nearest_sq(n):
    return round(n**.5)**2
__________________________
from math import sqrt

def nearest_sq(n):
    return pow(round(sqrt(n)), 2)
__________________________
def nearest_sq(n):
    test = n**(1/2) 
    if type(test) == int:
        sq = n
    else :
        mod = test % 1
    if mod >= 0.5 :
        test = test + 1 - mod
        sq = test**2
    else : 
       test = test - mod 
       sq = test**2
    return sq 
__________________________
def nearest_sq(n):
    a = int(n ** 0.5) ** 2
    b = int(n ** 0.5 + 1) ** 2
    return n if n ** 0.5 == int(n ** 0.5) else a if abs(n - a) < abs(n - b) else b
__________________________
from math import sqrt
def nearest_sq(n):
    m = int(sqrt(n))
    if (n-m**2) > ((m+1)**2-n):
        return (m+1)**2
    else:
        return m**2
__________________________
import math

def nearest_sq(n:int) -> int:
    s = math.sqrt(n)
    small = math.floor(s)**2
    big = math.ceil(s)**2
    return small if n - small < big - n else big
__________________________
def nearest_sq(n):
    for i in range(0, n):
        nearest_left = i*i
        nearest_right = (i + 1)*(i + 1)
        if nearest_left <= n <= nearest_right:
            return nearest_left if n - nearest_left < nearest_right - n else nearest_right
__________________________
import math
def nearest_sq(n):
    a = n
    b = n
    result = 0
    
    if math.floor(n ** (0.5)) == n ** (0.5):
        result = n
    else:
        while True:
            if math.floor(b ** (0.5)) == b ** (0.5):
                result = b
                break
            if math.floor(a ** (0.5)) == a ** (0.5):
                result = a
                break
            a += 1
            b -= 1
    return result
