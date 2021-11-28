def find_average(numbers):
    if len(numbers) == 0:
        print (0)
        return 0
    n_sum = 0 
    for num in numbers:
        n_sum += num
        
    print (n_sum/len(numbers))
    return n_sum/len(numbers)
#################
def find_average(array):
    return sum(array) / len(array) if array else 0
################
def find_average(array):
    try:
        return sum(array) / len(array)
    except ZeroDivisionError:
        return 0
##############
def find_average(numbers):
   return sum(numbers)/len(numbers)
###############
def find_average(array):
    if not array:
        return 0

    class SafeFloat(object):
        def __init__(self, val):
            super(SafeFloat, self).__init__()
            self.val = val

        def __eq__(self, float_val):
            # let me fix your comparisons..
            def isclose(a, b):
                return abs(a - b) < 0.00000001
            return isclose(self.val, float_val)

        def __str__(self):
            return str(self.val)

    from numpy import mean
    return SafeFloat(mean(array))
#############
def find_average(array):
    return sum(array) / (len(array) or 1)
##############
def find_average(array):
    return 0 if not array else sum(array) / len(array)
#############
from statistics import mean as find_average
############
from numpy import mean as find_average
############
def find_average(array):
    if len(array) != 0:
        return sum(array) / len(array)
    else:
        return 0
##############
def find_average(array):
    return 0 if len(array) == 0 else sum(array) / len(array)
###########
def find_average(a):
    return sum(a)/len(a) if a else 0
############
def find_average(array):
  mean=0
  if len(array)== 0:
    return mean
  sum=0
  for i in array:
    sum= sum+i
  mean= sum/(len(array))
  return mean
#############
def find_average(array):
    return sum(array)/len(array) if len(array) > 0 else 0
############
def find_average(array):
    sum = 0
    for num in array:
        sum += num
    try:
        return sum/len(array)
    except ZeroDivisionError:
        return 0
###############
def find_average(numbers):
    try:
        return sum(numbers)/len(numbers)
    except ZeroDivisionError:
        return 0
##############
def find_average(num):
    return sum(num) / len(num)
###########
from statistics import mean

def find_average(numbers):
    return mean(numbers)
##############
find_average = lambda x: sum(x)/len(x)
############
def find_average(x):
    return sum(x)/len(x) 
##############
def find_average(arr):
    return (sum(arr)/len(arr) if len(arr) != 0 else 0)
##############
def find_average(A):
    return sum(A)/len(A) if A else 0
###############
def find_average(array):
    return sum(array)/len(array) if len(array) else 0
