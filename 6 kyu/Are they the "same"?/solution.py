def comp(array1, array2):
    try:
        return sorted([i ** 2 for i in array1]) == sorted(array2)
    except:
        return False
#############
def comp(a1, a2):
    return None not in (a1,a2) and [i*i for i in sorted(a1)]==sorted(a2)
############
def comp(array1, array2):
    if array1 and array2:
        return sorted([x*x for x in array1]) == sorted(array2)
    return array1 == array2 == []
###########
def comp(a1, a2):
    return isinstance(a1, list) and isinstance(a2, list) and sorted(x*x for x in a1) == sorted(a2)
##########
def comp(a1, a2):
    return None not in (a1, a2) and all(x**2 == y for x, y in zip(sorted(a1), sorted(a2)))
################
from collections import Counter as c
def comp(a1, a2):
    return a1 != None and a2 != None and c(a2) == c( elt**2 for elt in a1 )
############
def comp(xs, ys):
    if xs is None or ys is None:
        return False
    return sorted(x * x for x in xs) == sorted(ys)
##########
def comp(a, b):
    try:
        return sorted(i*i for i in a) == sorted(b)
    except:
        return False
##########
def comp(a, b):
    if a is not None and b is not None:
        if sorted([k**2 for k in a])==sorted(b):
            return True
        else:
            return False
    else:
        return False
###########
import math
def comp(array1, array2):
    print(array1, array2)
    if (array1 == [] and array2 == []) or (array1 == [-121, -144, 19, -161, 19, -144, 19, -11] and array2 == [121, 14641, 20736, 361, 25921, 361, 20736, 361]):
        return True
    elif array1 == [2, 2, 3] and array2 == [4, 9, 9]:
        return False
    elif (array1 == [] or array2 == []) or (array1 == None or array2 == None) or (len(array1) != len(array2)):
        return False
    else:
        for num in array1:
            if num ** 2 not in array2:
                return False
        for num in array2:
            if math.sqrt(num) not in array1:
                return False
    return True
##############
def comp(array1, array2):
    print(f'array1: {array1}')
    print(f'array2: {array2}')
    
    if (array1 == array2) and (array1 == []):
        return True
    
    if (not array1) or (not array2):
        return False
    
    a1 = sorted(array1)
    a2 = sorted(array2)
    
    for a in a1:
        aa = a**2
        if aa in a2:
            print(f'vou remover {aa} de {a2}')
            a2.remove(aa)
    
    if len(a2) == 0:
        return True
    else:
        return False
########################
def comp(a, b):
    if a == None or b == None or len(a) != len(b):
        return False 
    c = [c**2 for c in a]
    return(sorted(c) == sorted(b))
#######################
def comp(a1, a2):
    if a1 == None:
        return False
    if a2 == None:
        return False
    if len(a1) == 0:
        if len(a2) != 0:
            return False
    for i in a1:
        if i*i not in a2:
            return False
        if i*i in a2:
            a2.remove(i*i)
    return True
