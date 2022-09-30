55b2549a781b5336c0000103



from math import log
def compare_powers(n1, n2):
    return cmp(log(n2[0])*n2[1], log(n1[0])*n1[1])
________________________________
from math import log

def compare_powers(*numbers):
    a,b = map(lambda n: n[1]*log(n[0]), numbers)
    return (a<b) - (a>b)
________________________________
def compare_powers(n1,n2):
  from math import log
  return -cmp(n1[1]*log(n1[0]), n2[1]*log(n2[0]))
________________________________
from math import log
def compare_powers(n1, n2):
  val = n2[1] * log(n2[0]) - n1[1] * log(n1[0])
  return -1 if val < 0 else 1 if val > 0 else 0
________________________________
from math import log

def compare(x, y):
    if x == y:
        return 0
    if x < y:
        return 1
    if x > y:
        return -1
        
def compare_powers(x, y):
    a, c = x
    b, d = y
    x = (c * log(a)) / log(2)
    y = (d * log(b)) / log(2)
    return compare(x, y)
________________________________
def compare_powers(n1,n2):
    p = n1[1] if n1[1]>=n2[1] else n2[1]
    a = n1[0]**(n1[1]/p)
    b = n2[0]**(n2[1]/p)
    if a > b: return -1
    return 0 if a == b else 1
________________________________
from math import log
def compare_powers((n1, p1), (n2, p2)):
    return cmp(p2 * log(n2), p1 * log(n1))
________________________________
def compare_powers(n1,n2):
    if n1[1] < 1000 or n2[1] < 1000:
        x = n1[0] ** n1[1]
        y = n2[0] ** n2[1]
        if x > y:
            return -1
        elif y > x:
            return 1
        else:
            return 0
    else:
        if n1[1] > n2[1]:
            return -1
        elif n1[1] < n2[1]:
            return 1
        else:
            return 0
________________________________
import math
def compare_powers(n1,n2):

    first = math.log(n1[0]) * n1[1]
    second = math.log(n2[0]) * n2[1]
    if first > second:
        return -1
    if first == second:
        return 0
    if first < second:
        return 1
________________________________
def compare_powers(n1,n2):
    from math import log as log
    a = log(n1[0]) * n1[1]
    b = log(n2[0]) * n2[1]
    return -1 if a > b else (1 if a < b else 0)
________________________________
def compare_powers(n1,n2):
    m = 0
    if n1[1] >= n2[1]:
        m = n1[1]
    else: m = n2[1]
    
    n1[0] = n1[0]**(n1[1]/m)
    n2[0] = n2[0]**(n2[1]/m)
    
    if n1[0] > n2[0]: return -1
    elif n1[0] < n2[0]: return 1
    else: return 0
        
