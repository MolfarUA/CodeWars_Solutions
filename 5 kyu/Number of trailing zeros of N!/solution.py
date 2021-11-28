def zeros(n):
    temp = 5
    count = 0
    while (n / temp>= 1):
        count += int(n / temp) 
        temp *= 5
    return count
####################
def zeros(n):
  x = n/5
  return x+zeros(x) if x else 0
###################
def zeros(n):
    return n/5 + zeros(n/5) if n >= 5 else 0
###################
from math import log

def zeros(n):
    return sum([n / (5 ** i) for i in range(1, int(log(n, 5) + 1))]) if n > 0 else 0
###################
def zeros(n):
    zeros = 0
    i = 5
    while n//i > 0:
        zeros += n//i
        i*=5
    return zeros
##################
def zeros(n):
    return 0 if n < 5 else n/5 + zeros(n/5)
##################
def zeros(n):
    count = 0
    while n:
        n = n // 5
        count += n
    return count
###############
zeros = lambda n: n and n/5 + zeros(n/5)
#############
def zeros(n):
    return n/5 + zeros(n/5) if n else 0 
################
import math
def zeros(n):
  return reduce(lambda p,c: p + n // 5**c, range(1,13), 0)
##################
from itertools import takewhile, count
from operator import truth

def zeros(n):
    return sum(takewhile(truth, (n // 5 ** e for e in count(1))))
####################
zeros=z=lambda n:n and n/5+z(n/5)
################
zeros = lambda n: n/5 + zeros(n/5) if n >= 5 else 0
#################
import math
def zeros(n):
    return sum([(n / (5 ** i)) for i in xrange(1, int(math.log(n) / math.log(5)) + 1)]) if n>0 else 0
################
from itertools import takewhile, count
zeros = lambda n: sum(n/(5**k) for k in takewhile(lambda x: n/(5**x)>0, count(1)))
