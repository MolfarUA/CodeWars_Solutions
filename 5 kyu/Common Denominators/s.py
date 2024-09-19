54d7660d2daf68c619000d95


import math
from functools import reduce


def nsk(*args):
    return reduce(lambda a, b: abs(a * b) // math.gcd(a, b), args)


def convert_fracts(lst):
    if not lst:
        return lst
    denominators = [d for num, d  in lst]
    common_d = nsk(*denominators)
    return  [[(common_d// d)*num, common_d] for num, d  in lst]

############################
from functools import reduce


def nsd(*args):
    n = 1
    result = 1

    while all(arg >= n for arg in args):
        n += 1

        if all(arg % n == 0 for arg in args):
            result = n

    return result


def nsk(*args):
    return reduce(lambda a, b: abs(a * b) // nsd(a, b), args)

def convert_fracts(lst):
    if not lst:
        return lst
    denominators = [d for num, d  in lst]
    common_d = nsk(*denominators)
    return  [[(common_d// d)*num, common_d] for num, d  in lst]

#################################
import math

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def convert_fracts(l):
    if not l: return []
    
    c = l[0][1]
    for i, j in l[1:]:
        c = lcm(c, j)

    return [[d * (c // v), c] for d, v in l]

################################
def gcd(a, b):
    while b:      
        a, b = b, a % b
    return a
def minium_fraction(a, b):
    div = gcd(a, b)
    return (a // div), (b // div)
def lcm(a, b):
    return a * b // gcd(a, b)
    
def convert_fracts(lst):
    if not len(lst):
        return []
    _lcm = 1
    for i in range(0, len(lst)):
        lst[i][0], lst[i][1] = minium_fraction(lst[i][0], lst[i][1])
        _lcm = lcm(lst[i][1], _lcm)
#     print(_lcm)
    for i in range(0, len(lst)):
        lst[i][0] = lst[i][0] * (_lcm // lst[i][1])
        lst[i][1] = lst[i][1] * (_lcm // lst[i][1])
    return lst
    
