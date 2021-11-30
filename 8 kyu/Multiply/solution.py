def multiply(a, b):
  a * b
############
multiply = __import__('operator').mul
###########
def multiply(a, b):
    if isinstance(a, (int, float, complex)):
        if isinstance(b, (int, float, complex)):
            return a * b
#############
multiply = lambda x, y: x * y
##########
from operator import mul as multiply
########
def multiply(a, b):
  if a is not None and b is not None:
     return a * b
  else:
      return None
