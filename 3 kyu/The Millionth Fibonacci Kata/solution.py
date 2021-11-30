import numpy as np
from numpy import linalg as LA

def fib(n):
        return (np. sign(n)) ** (abs(n)+1)*(LA.matrix_power(np.matrix([[1, 1], [1, 0]], dtype = 'object'), abs(n))). item(2)
###################
from numpy import matrix

def fib(n):
    return (matrix(
        '0 1; 1 1' if n >= 0 else '-1 1; 1 0', object
        ) ** abs(n))[0, 1]
######################
def fib(n):
  if n < 0: return (-1)**(n % 2 + 1) * fib(-n)
  a = b = x = 1
  c = y = 0
  while n:
    if n % 2 == 0:
      (a, b, c) = (a * a + b * b,
                   a * b + b * c,
                   b * b + c * c)
      n /= 2
    else:
      (x, y) = (a * x + b * y,
                b * x + c * y)
      n -= 1
  return y
##############
def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

@memoize
def fib(n):
  """Calculates the nth Fibonacci number"""
  
  if n == 0:
      return 0
  if n == 1:
      return 1
  if n == 2:
      return 1
     
  if n < 0:
      return fib(n+2) - fib(n+1)

  s = n / 2
  return fib(s + 1) * fib(n - s) + fib(s) * fib(n - s - 1)
#################3
fibs = {0: 0, 1: 1}
def fib(n):
    if(n<0):
        return (fib(-n) if n%2 else -fib(-n)) 
    if n in fibs: return fibs[n]
    if n % 2 == 0:
        fibs[n] = ((2 * fib((n / 2) - 1)) + fib(n / 2)) * fib(n / 2)
        return fibs[n]
    else:
        fibs[n] = (fib((n - 1) / 2) ** 2) + (fib((n+1) / 2) ** 2)
        return fibs[n]
######################
def fib(n):
    sign = -1 if n<0 and abs(n)%2==0 else 1
    an=abs(n)
    a = 2<<an
    return sign*(pow(a,an+1,a*(a-1)-1)%a)
######################
def fib(n):

    def matrix_multiply(a, b):
        first_row = [
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ]
        second_row = [
            a[1][0] * b[0][0] + a[1][1] * b[0][1],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ]
        return [first_row, second_row]

    def matrix_power(matrix, exponent):
        if exponent == 1:
            return matrix
        else:
            result = matrix_power(matrix, exponent // 2)
            result = matrix_multiply(result, result)
            if exponent % 2 == 1:
                result = matrix_multiply(result, matrix)
            return result

    matrix = [[0, 1], [1, 1]]
    result =  matrix_power(matrix, abs(n) + 1)[0][0]
    sign = -1 if n < 0 and n % 2 == 0 else 1
    return result * sign
################################
import gmpy2

def fib(n):
    return gmpy2.fib(abs(n)) * (-1 if n < 0 and n % 2 == 0 else 1)
###############################
from numpy import matrix

def fib(n):
    fib_n = (matrix('0 1; 1 1', object) ** abs(n))[0, 1]
    return fib_n if n > 0 or n % 2 != 0 else -fib_n
#############################
def fib(n):
  """Calculates the nth fibonacci number"""
  if n in (0, 1): return n
  elif n>0:
    if n%2:
      k = n/2
      fk0 = fib(k)
      fk1 = fib(k-1)
      f = fk0**2 + (fk0+fk1)**2
    else:
      k = n/2
      fk0 = fib(k) 
      fk1 = fib(k-1)
      f = fk0*(fk0 + 2*fk1)
  else:
    return fib(-n) if n%2 else -fib(-n)
  
  return f
#################################
import numpy

def fib(n):
  """Calculates the nth Fibonacci number"""
  if n < 0:
      return fib(-n) if n & 1 else -fib(-n)
  
  return long((numpy.matrix('0 1; 1 1', dtype = object) ** n * numpy.matrix('0; 1'))[0])
#####################
def fib(n, a=1, b=0, p=0, q=1):
    if n == 0: return b
    if n < 0 and p == 0: p = -1
    if n % 2: return fib(n-cmp(n, 0), a=(p+q)*a + q*b, b=q*a + p*b, p=p, q=q)
    else: return fib(n/2, a=a, b=b, p=p*p+q*q, q=2*p*q + q*q)
#####################
from numpy import matrix
def fib(n):
    Q = matrix([[1, 1], [1, 0]], dtype=object)
    if n > 0 or n % 2 != 0:
        return (Q ** (abs(n) - 1))[0, 0]
    return -(Q ** (abs(n) - 1))[0, 0] if n != 0 else 0
###########################
memo = {-1: 1, 0: 0, 1: 1, 2: 1}

def fib(n):
    if n in memo: return memo[n]

    k = n / 2
    if n % 2 == 0:
        f = fib(k) * (2 * fib(k + 1) - fib(k))
    else:
        f = fib(k + 1) ** 2 + fib(k) ** 2
    
    memo[n] = f
    return f
#############################
def fib(n):
  if n < 0: return (-1)**(n % 2 + 1) * fib(-n)
  else:
      a,b,p,q = 1,0,0,1
      while n != 0:
          if n % 2 == 0:
              p, q = p*p + q*q, q*q + 2*p*q
              n = n / 2
          else:
              a, b = (p+q)*a + q*b, a*q + b*p
              n -= 1
      return b
