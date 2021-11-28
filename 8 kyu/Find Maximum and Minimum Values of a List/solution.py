def minimum(arr):
    return(min(arr))
def maximum(arr):
    return(max(arr))
#################
def min(arr):
    return sorted(arr)[0]

def max(arr):
    return sorted(arr)[-1]
#####################
def min(arr):
    low = arr[0]
    for i in arr[1:]:
        if i < low:
            low = i
    return low

def max(arr):
    high = arr[0]
    for i in arr[1:]:
        if i > high:
            high = i
    return high
####################
minimum = min
maximum = max
################
def min(arr):
    arr.sort()
    return arr[0]

def max(arr):
    arr.sort(reverse=True)
    return arr[0]
#####################
minimum,maximum = min,max
#####################
min, max = min, max
##################
def min(arr):
    return reduce(lambda x,y: x if x < y else y, arr)
def max(arr):
    return reduce(lambda x,y: x if x > y else y, arr)
#####################
import builtins

def min(arr):
    return builtins.min(arr)

def max(arr):
    return builtins.max(arr)
###################
def min(arr):
    return vars(__builtins__)['min'](arr)

def max(arr):
    return vars(__builtins__)['max'](arr)
##################
from functools import reduce

def min(arr):
    return reduce(lambda x, y: x if x < y else y, arr)

def max(arr):
    return reduce(lambda x, y: x if x > y else y, arr)
####################
import math

def min(arr):
    return (sorted(arr))[0]

def max(arr):
    return (sorted(arr))[len(arr)-1]
##################
def bouble_sort(a):
    for i in range(len(a)-1):
        for j in range(len(a)-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

def minimum(arr):
    return bouble_sort(arr)[0]

def maximum(arr):
    return bouble_sort(arr)[len(arr)-1]
######################
import numpy as np

def minimum(arr):
    return np.array(arr).min()

def maximum(arr):
    return np.array(arr).max()
