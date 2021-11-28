import numpy as np
def square_sum (numbers):
    res = []
    for num in numbers:
        res.append(num**2)
    res = np.sum(res)
    return res
#########################
def square_sum(numbers):
    return sum(x ** 2 for x in numbers)
#################
def square_sum(numbers):
    return sum(x * x for x in numbers) 
###################
def square_sum(numbers):
    return sum(map(lambda x: x**2,numbers))
#################
def square_sum(numbers):
    result = []
    for sqr in numbers:
        result.append(sqr ** 2)
    return sum(result)
################
def square_sum(numbers):
    res = 0
    for num in numbers:
        res = res + num*num
    return res
################
import numpy

def square_sum(numbers):
    return sum(numpy.array(numbers) ** 2)
###############
import functools
def square_sum(numbers):
    return functools.reduce(lambda x, y: x + y**2, numbers, 0)
#############
def square_sum(numbers):
    return sum([x**2 for x in numbers])
#############
def square_sum(numbers):
    return sum(i**2 for i in numbers)
############
def square_sum(numbers):
    return sum(map(lambda x: x*x, numbers))
################
square_sum=lambda n:sum(a**2 for a in n)
