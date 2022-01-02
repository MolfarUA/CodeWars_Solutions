from itertools import count
def pair_zeros(arr, *args):
    c = count(1)
    return [elem for elem in arr if elem != 0 or next(c) % 2]
  
_____________________________________
def pair_zeros(nums, *_):
    result = []
    skip_zero = False
    for a in nums:
        if a == 0:
            if not skip_zero:
                result.append(a)
            skip_zero = not skip_zero
        else:
            result.append(a)
    return result

_____________________________________
def pair_zeros(arr):
    got = [0]
    return [v for v in arr if v or got.__setitem__(0,got[0]^1) or got[0]]
  
_____________________________________
def pair_zeros(arr):
    return [d for i, d in enumerate(arr) if d != 0 or arr[:i+1].count(0) % 2]
  
_____________________________________
def pair_zeros(arr):
    lst = []
    flag = False
    for i in arr:
        if i == 0:
            if not flag:
                lst.append(i)
            flag = not flag
        else:
            lst.append(i)
    return lst
  
_____________________________________
def pair_zeros(arr, *r):
    toggle = __import__('itertools').cycle([True, False])
    return [x for x in arr if x != 0 or toggle.next()]
  
_____________________________________
def pair_zeros(arr):
    r=[]
    n=0
    for i in arr:
        if i==0:
            n+=1
        if n==2:
            n=0
            continue
        r.append(i)
    return r
  
_____________________________________
from typing import List


def pair_zeros(arr: List[int]) -> List[int]:
    p = False
    return [a for a in arr if a or (p := not p)]
  
_____________________________________
def pair_zeros(arr):
    keep = False
    return [x for x in arr if x or (keep := not keep)]
  
_____________________________________
def pair_zeros(arr, *other):
    
    return [n for i, n in enumerate(arr) if n != 0 or arr[:i+1].count(0)%2 == 1]
  
_____________________________________
import re

def pair_zeros(arr,*args):        
    return map(int, re.sub(r"(0[^0]*)0", "\\1", "".join([str(a) for a in arr])))
  
_____________________________________
def pair_zeros(arr):
    # As asked make a copy and not going to change initial array
    zeros = arr.copy()
    
    stack = False
    offset = 0

    # Fins first zero and remember it
    for i,d in enumerate(arr):
        if d == 0 and not stack:
            stack = True
            pass
        # When find second zero delete it
        # Offset because with each delete we shortened array
        elif d == 0 and stack:
            zeros.pop(i - offset)
            stack = False
            offset += 1

    return zeros
            
_____________________________________
def pair_zeros(arr):
    l=[]
    z=0
    for i in arr:
        if i==0:
            z+=1
            if z%2==0:
                continue
            else:
                l.append(i)
        else:
            l.append(i)
    return l
