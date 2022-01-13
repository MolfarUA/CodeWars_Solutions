import math
def is_square(n):
    return n > -1 and math.sqrt(n) % 1 == 0;
__________________________________
import math

def is_square(n):    

    if n < 0:
        return False

    sqrt = math.sqrt(n)
    
    return sqrt.is_integer()
__________________________________
import math
def is_square(n):    
    try:
        return math.sqrt(n).is_integer()
    except ValueError:
        return False
__________________________________
def is_square(n):    
    return n >= 0 and (n**0.5) % 1 == 0
__________________________________
def is_square(n):    
    if n>=0:
        if int(n**.5)**2 == n:
            return True
    return False
__________________________________
import math

def is_square(n):
    if n < 0:
        return False
    r = math.sqrt(n)
    r = math.floor(r)
    return r * r == n
__________________________________
from math import sqrt
def is_square(n):  
    if n<0:
        return False
    count=0
    m=int(sqrt(n))
    if m*m==n:
        count=1
    if count==1:
        return True
    else :
        return False
