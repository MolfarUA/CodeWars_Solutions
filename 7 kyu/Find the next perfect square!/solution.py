from math import *

def find_next_square(sq):
    return (sqrt(sq)+1)**2 if sqrt(sq) % 1 == 0 else -1
  
_______________________________________
def find_next_square(sq):
    root = sq ** 0.5
    if root.is_integer():
        return (root + 1)**2
    return -1

_______________________________________
def find_next_square(sq):
    x = sq**0.5    
    return -1 if x % 1 else (x+1)**2

_______________________________________
from math import sqrt
def find_next_square(sq):
    return (sqrt(sq)+1)**2 if sqrt(sq)%1 == 0 else -1

_______________________________________
def find_next_square(sq):
    return (sq**0.5+1)**2 if int(sq**0.5)**2 == sq else -1
  
_______________________________________
def find_next_square(sq):
    sqrt=sq**(0.5)
    if sqrt % 1 == 0:
        return (sqrt+1)**2
    return -1

_______________________________________
def find_next_square(sq):
    if sq < 0:
        return -1
    else:
        x = (sq ** (1/2))
        if not x.is_integer():
            return -1
        else:
            return (x+1) ** 2

_______________________________________
import math

def get_root(num):
    square_root = int(math.sqrt(num))
    if square_root * square_root == num: return square_root
    return -1

def find_next_square(sq):
    # Return the next square if sq is a square, -1 otherwise
    square_root = get_root(sq)
    if square_root == -1: return -1
    next_square = (square_root + 1) * (square_root + 1)
    return next_square

_______________________________________
import math
def find_next_square(sq):
    if sq % math.sqrt(sq) == 0:
        x = math.sqrt(sq) + 1
        sq = x**2
        return sq
    return -1
