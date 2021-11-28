def invert(lst):
    return [-x for x in lst]
##################
def invert(lst):
    return list(map(lambda x: -x, lst));
##################
def invert(lst):
   return [i*-1 for i in lst]
#################
def invert(lst):
    i = 0
    inv = []
    while i < len(lst):
        inv.append(lst[i] * -1)
        i += 1
    return inv
#####################
def invert(lst):
    return list(map(int.__neg__, lst))
#####################
import operator

def invert(lst):
    return list(map(operator.neg, lst))
##################
def invert(lst):
    lst2=[]
    for num in lst:
        lst2.append(num*-1)
    return lst2
##################
def invert(lst):
    return [-i for i in lst]
###############
def invert(l): return [-n for n in l]
###############
invert = lambda x: [-i for i in x]
#################
def invert(lst):
    result = list()
    for num in lst:
        result.append(-num)
    return result
################
import numpy
def invert(lst):
    return list(numpy.array(lst) * -1)
###############
def invert(lst):
    for i in range(len(lst)):
        if lst[i] > 0:
            lst[i] = -abs(lst[i])
        else:
            lst[i] = abs(lst[i])
            
    return lst
###################
def invert(lst):
    return [] if lst == [] else [i*(-1) for i in lst]
