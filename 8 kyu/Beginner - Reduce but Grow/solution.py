def grow(arr):
    result = 1

    for i in arr:
        result *= i

    return result
###################
from functools import reduce

def grow(arr):
    return reduce(lambda x, y: x * y, arr)
###############
from functools import reduce
from operator import mul

def grow(arr):
    return reduce(mul, arr, 1)
###############
def grow(arr):
    return eval('*'.join([str(i) for i in arr]))
###########
def grow(arr):
    product = 1
    for i in arr:
        product *= i
    return product
##############
grow = lambda a: __import__("functools").reduce(lambda x,y: x*y, a)
################
from operator import mul

def grow(arr):
    return reduce(mul, arr)
#################
grow=lambda arr: eval("*".join(map(str,arr)))
###############
def grow(arr):
    return eval(str(tuple(arr)).replace(',', '*'))
############
grow=g=lambda a:a==[]or a[0]*g(a[1:])
#############
from functools import reduce, partial
from operator import mul

grow=partial(reduce, mul)
