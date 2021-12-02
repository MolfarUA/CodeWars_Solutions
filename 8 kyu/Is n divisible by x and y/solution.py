def is_divisible(n,x,y):
    return True if n % x == n % y == 0 else False
################
def is_divisible(n, x, y):
    return n % x == n % y == 0
###############
def is_divisible(n,x,y):
    #your code here
    if n % x == 0 and n % y == 0:
        return True
    else:
        return False
###############
""" isdiv works thusly:
Create a function isDivisible(n, x, y)
that checks if a number n is divisible
by two numbers x AND y. All inputs are
positive, non-zero digits.
"""


# isDivisible(3,1,3)--> true because 3 is divisible by 1 and 3
# isDivisible(12,2,6)--> true because 12 is divisible by 2 and 6
# isDivisible(100,5,3)--> false because 100 is not divisible by 3
# isDivisible(12,7,5)--> false because 12 is neither divisible by 7 nor 5

def is_divisible(n,x,y):
    """is divisible checks if a number n is divisible
    by two numbers x AND y. All inputs are
    positive, non-zero digits.

    >>> is_divisible(3,1,3)
    True
    >>> is_divisible(12,2,6)
    True
    >>> is_divisible(100,5,3)
    False
    >>> is_divisible(12,7,5)
    False

    >>> is_divisible(0,1,1)
    Traceback (most recent call last):
     ...
    ValueError: Must be integer greater than 0
    >>> is_divisible(1,0,1)
    Traceback (most recent call last):
     ...
    ValueError: Must be integer greater than 0
    >>> is_divisible(1,1,0)
    Traceback (most recent call last):
     ...
    ValueError: Must be integer greater than 0
    """

    if n < 1 or x < 1 or y < 1:
        raise ValueError('Must be integer greater than 0')

    return n % x == 0 and n % y == 0
###############
def is_divisible(n, x, y):
    return not n % x and not n % y
###############
def is_divisible(n,x,y):
    return not (n%x or n%y)
################
def is_divisible(n,x,y):
    return n % x + n % y == 0 
################
def is_divisible(n1,x1,y1):
    return n1 % x1 == 0 and n1 % y1 == 0;
################
is_divisible = lambda n,x,y: not (n%x or n%y)
################
def is_divisible(n,x,y):
    return (n % x == 0) & (n % y == 0)
################
def is_divisible(n,x,y):
    if x == 0 or y == 0: return False
    return n//x == n/x and n//y == n/y
################
def is_divisible(n,x,y):
    return True if n % x == 0 and n % y == 0 else False
#############
is_divisible = lambda n,x,y: not ((n**2)%(x*y))
#############
def is_divisible(n,x,y):
    return (False, True)[n%x==0 and n%y==0]
##############
def is_divisible(n,x,y):
    return n%x==0==n%y
##############
def is_divisible(n,x,y):
    correct = True
    if n/x != n//x:
        correct = False
    elif n/y != n//y:
        correct = False
    return correct
#################
def is_divisible(n,x,y):
        if not n % x:
                if not n % y:
                        return True

        return False
