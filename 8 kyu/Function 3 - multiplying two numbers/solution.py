def multiply(x, y):
    return x * y
##############
multiply = lambda x, y: x * y
###########
def multiply(a,b):
    return a * b
##########
def multiply(is_this, a_joke): return is_this*a_joke
############
multiply = lambda a,b: a*b
###########
def multiply(*nums):
    x = 1
    for a in nums:
        x *= a

    return x
###########
def multiply(a, b):
    p = 0
    while a >= 1:
        if a % 2 == 0:
            p += 0
            b <<= 1
        else:
            p += b
            b <<= 1
        a >>= 1
    return p
############
def multiply(x,y):
    value = x*y
    return value

multiply(4,5)
################
def multiply(*args):
    if len(args) != 2:
        raise TypeError("Incorrect number of arguments")
    ans = 1
    try:
        for arg in args:
            ans*=float(arg)
        return ans
    except:
        raise TypeError("Expected two number as input")
