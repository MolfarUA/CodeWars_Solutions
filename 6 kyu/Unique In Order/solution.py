def unique_in_order(iterable):
    result = []
    prev = None
    for char in iterable[0:]:
        if char != prev:
            result.append(char)
            prev = char
    return result
_____________________________________________
from itertools import groupby

def unique_in_order(iterable):
    return [k for (k, _) in groupby(iterable)]
_____________________________________________
def unique_in_order(iterable):
    res = []
    for item in iterable:
        if len(res) == 0 or item != res[-1]:
            res.append(item)
    return res
_____________________________________________
unique_in_order = lambda l: [z for i, z in enumerate(l) if i == 0 or l[i - 1] != z]
_____________________________________________
def unique_in_order(iterable):
    r = []
    for x in iterable:
        x in r[-1:] or r.append(x)
    return r
_____________________________________________
def unique_in_order(iterable):
    k = []
    for i in iterable:
        if k == []:
            k.append(i)
        elif k[-1] != i:
            k.append(i)
    return k
_____________________________________________
def unique_in_order(iterable):
    return [ ch for i, ch in enumerate(iterable) if i == 0 or ch != iterable[i - 1] ]
_____________________________________________
def unique_in_order(iterable):
    unique = []
    last = ''
    for item in iterable:
        if item != last:
            unique.append(item)
            last = item
    return unique
_____________________________________________
def unique_in_order(it):
    return [it[0]] + [e for i, e in enumerate(it[1:]) if it[i] != e] if it else []
_____________________________________________
def unique_in_order(iterable):
    result = [None]
    
    for item in iterable:
        if item != result[-1]:
            result.append(item)
        
    return result[1:]
_____________________________________________
def unique_in_order(iterable):
    if not iterable:
        return []
    return [iterable[0]] + [x for i, x in enumerate(iterable[1:], 1) if x != iterable[i-1]]
_____________________________________________
def unique_in_order(iterable):
    
    pattern = 0
    result  = [] 
    
    for element in iterable:
        if pattern != element:
            result.append(element)
            pattern = element
            
    return result
_____________________________________________
def unique_in_order(iterable):
    result, prev = [], None
    for n in iterable:
        if prev == n: continue
        else:
            prev = n
            result.append(n)
    return result
_____________________________________________
def unique_in_order(i):
    s = []
    for l in i:
        try:
            if not l == s[-1]:
                s.append(l)
        except:
            s.append(l)
    return s
_____________________________________________
__author__ = "MolfarUA"

from itertools import groupby
from operator import itemgetter

def unique_in_order(iterable):
    return map(itemgetter(0), groupby(iterable))
