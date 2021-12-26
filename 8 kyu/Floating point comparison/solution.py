def approx_equals(a, b):
    return abs(a-b) < 0.001
  
###############
from math import isclose

def approx_equals(a, b):
    return isclose(a, b, rel_tol=0, abs_tol=1e-3)
  
############
def approx_equals(a, b):
    return abs(a - b) < 1e-3
  
#############
from math import isclose

def approx_equals(a, b):
    return isclose(a, b, abs_tol=1e-3)
  
##############
def approx_equals(a, b):
    a = round(a, 5)
    b = round(b, 5)
    return abs(a - b) <= 0.001
  
###############
import math

def approx_equals(a, b):
    a = round(a, 5)
    b = round(b, 5)
    l = math.isclose(a, b, abs_tol = 0.001)
    return l
#     if a - b > rel_tol:
#         a != b
#     if a != b:
#         return False
#     else:
#         return True
#############################
def approx_equals(a, b):
    if a == b or (a != b and abs(a - b) <= 0.001):
        return True
    else:
        return False
      
####################
def approx_equals(a, b):
    c = abs(a-b)
    print(c)
    c = abs(a-b) <= 0.001
    return c
