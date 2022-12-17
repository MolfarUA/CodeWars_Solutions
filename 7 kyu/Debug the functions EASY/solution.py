5844a422cbd2279a0c000281


from functools import reduce
from operator import mul

def multi(l_st):
    return reduce(mul,l_st)
def add(l_st):
    return sum(l_st)
def reverse(s):
    return s[::-1]
________________________
import functools

def multi(l_st):
    return functools.reduce(lambda x, y: x * y, l_st)
def add(l_st):
    return functools.reduce(lambda x, y: x + y, l_st)
def reverse(string):
    return string[::-1]
________________________
from math import prod
def multi(l_st):
    return prod(l_st)
def add(l_st):
    return sum(l_st)
def reverse(string):
    return string[::-1]
________________________
def multi(l_st):
    mult = 1
    for num in l_st:
        mult *= num
    return mult
def add(l_st):
    return sum(l_st)
def reverse(string):
    return string[::-1]
________________________
from numpy import product

def multi(l_st):
    return product(l_st)
def add(l_st):
    return sum(l_st)
def reverse(string):
    return string[::-1]
________________________
def multi(l_st):
    bufor = 1
    for i in range (len(l_st)):
        bufor *= l_st[i]  
    return bufor
def add(l_st):
    return sum(l_st)
def reverse(string):
    return string[::-1]
________________________
def multi(l_st):
    s=1
    for i in l_st:
        s*=i
    return s
def add(l_st):
    return sum(l_st)
def reverse(string):
    return string[::-1]
