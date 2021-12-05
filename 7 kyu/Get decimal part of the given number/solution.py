def get_decimal(n): 
    return abs(n) - int(abs(n))
############
def get_decimal(n): 
    return abs(n) % 1
###########
def get_decimal(n): 
    n = abs(n)
    return n - int(n)
###############
import math
def get_decimal(n): 
    return abs(n) % 1
############
from math import floor, ceil
def get_decimal(n): 
    return n - floor(n) if n>0 else ceil(n) - n
##############
def get_decimal(n: float) -> float:
    return abs(n) % 1
############
def get_decimal(n):
    n = str(n)
    if str(n)[0] == '-':
        n = n[1:]
    for i in n:
        if i == '.':
            return float('0'+n[n.index(i):])
    return 0
###############
from math import modf

def get_decimal(n):
    if n<0:
        n=n*-1
    return modf(n)[0]
##############
def get_decimal(n):
    return 0 if "." not in str(n) else float("0." + str(n)[str(n).index(".") + 1:])
#############
import math as m
def get_decimal(n):
    return abs(n) - abs(m.floor(abs(n)))
##########
def get_decimal(n): 
    a = abs(n)
    ret = a % 1
    return ret
###########
def get_decimal(n): 
    if type(n) == int or type(n) == float:
        return abs(n) - abs(int(n))        
    else:
        return None
#############
def get_decimal(n): 
    x = (n - int(n))
    if x < 0: return(x * -1)
    else: return(x)
##########
import re

def get_decimal(n): 
    return float(re.sub(r'.*(\..*)', r'0\1', str(n))) if n % 1 != 0 else 0
