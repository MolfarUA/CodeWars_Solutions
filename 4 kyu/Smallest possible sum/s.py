52f677797c461daaf7000740


def solution(a):
    a_len = len(a)
    a = set(a)
    while len(a) != 1:
        b = max(a)
        a.remove(b)
        a.add(b-max(a))
    return(max(a) * a_len)
_______________________________
import sys
if sys.version_info.major >= 3:
    from functools import reduce
if sys.version_info < (3,5):
    from fractions import gcd
elif sys.version_info >= (3,5):
    from math import gcd

def solution(a):
    return reduce(gcd, a) * len(a)
_______________________________
import numpy as np

def solution(a):
    return np.gcd.reduce(a) * len(a)
_______________________________
from math import gcd

def solution(a):
    return gcd(*a) * len(a)
_______________________________
from functools import reduce

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

def solution(a):
    return len(a) * reduce(gcd, a)
_______________________________
from math import gcd
from functools import reduce
solution=lambda a:reduce(gcd,a)*len(a)
_______________________________
def solution(a):
    len_a = len(a)
    a = set(a)
    while len(a) > 1:
        max_a = max(a)
        a.remove(max_a)
        a.add(max_a - max(a))
    return a.pop() * len_a
_______________________________
from math import gcd
from functools import reduce

def solution(a):
    return reduce(gcd, a) * len(a)
_______________________________
def solution(a):
    gCd = 0
    from math import gcd
    for i in range(len(a)-1):
        gCd = gcd(a[i],a[i+1])
        a[i] = gCd
    return min(a)*len(a)
_______________________________
def reduce_pair(x, y):
    while x != y:
        if x > y:
            x = x % y
            if not x:
                x = y
        else:
            y = y % x
            if not y:
                y = x

    return x, y


def solution(a: list[int]):
    len_a = len(a)

    # handle edge cases first...
    if len_a < 2:  # less than 2 elements, least-sum is the single element
        return sum(a)  # handles empty lists...

    # This could probably be sped up using dicts or trees...
    # ...for now, we'll just loop...
    continue_processing = True

    while continue_processing:
        continue_processing = False
        # ...checking each pair of items in the array...
        for idx in range(len_a - 1):
            if a[idx] != a[idx + 1]:
                # ...and ensuring that we come back again if we're left with values that don't match
                continue_processing = True
                a[idx:idx + 2] = reduce_pair(*a[idx:idx + 2])

                if 1 in a[idx:idx + 2]:  # early break if we find a '1'
                    return len(a)

    return sum(a)
