def no_space(x):
    return x.replace(' ', '')
##############
def no_space(x):
    return "".join(x.split())
###################
def no_space(x):
    str_char = ''
    for i in range(len(x)):
        if x[i] == ' ':
            continue
        else:
            str_char = str_char + x[i]
    return str_char
###############
no_space = lambda s: ''.join(filter(lambda ch: not ch == ' ', s))
##############
def no_space(str):
    str = ''.join(str.split())
    return str
#############
def no_space(x):
    return ''.join(i for i in x if i !=' ')
#############
def no_space(x):
    return ''.join([s for s in x if not s.isspace()])
################
import re

def no_space(x):
    return re.sub(r'\s+','',x,0)
###########
no_space = lambda x: ''.join(x.split())
###########
def no_space(x):
    x = x.replace(" ", "")
    return x
###########
def no_space(x):
    s = ""
    for letter in x:
        if letter != ' ':
            s += letter
    return s
#############
def no_space(s):
    return ''.join([c for c in s if c != ' '])
#############
def no_space(x):
    return x.replace(' ', '')

print(no_space('8asd sdhjk rr'))
#############
def no_space(x):
    string = ""
    for i in x:
        if i.isspace()==False:
            string += i
    return string
#############
from functools import reduce, partial
from operator import not_ as inot

def no_space(x):
    #predicate = lambda x: not x.isspace()
    predicate = neg(str.isspace)
    return ''.join(filter(predicate, str(x)))

def neg(func):
    """Decorator to negate a callable execution"""
    if not callable(func):
        raise TypeError(""""%s" must be callable. Found: %s""" % (func, func.__name__))
    def wrapper(*args, **kwargs):
        return inot(func(*args, **kwargs))
    return wrapper
