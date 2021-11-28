def get_average(marks):
    return sum(marks) // len(marks)
########################
import numpy

def get_average(marks):
    return int(numpy.mean(marks))
##################
get_average = lambda m: int(__import__("numpy").mean(m))
#######################
get_average = lambda marks: sum(marks)//len(marks)
##################
import math
import numpy
def get_average(marks):
    number =  numpy.average(marks)
    return math.floor(number)
#################
def get_average(marks):
    sum = 0
    for x in marks:
        sum = sum + x
    num = len(marks)
    ans = sum/num
    return int(ans)
#################
def get_average(marks):
    return int(sum(marks)/len(marks))
##################
get_average =lambda x: sum(x)//len(x)
#################
import math

def get_average(marks):
    sum = 0
    for num in marks:
        sum += num
    total = sum / len(marks)
    return math.floor(total)
################
from math import trunc
def get_average(marks):
    return trunc(sum(marks)/len(marks))
##################
def get_average(marks):
    a = 0
    for i in marks:
        a = a+i
    a = a/ len(marks)
    return int(a)
##################
import pandas as pd

def get_average(marks):
    s = pd.Series(marks)
    return int(s.mean())
##################
import numpy, math
def get_average(marks):
    return math.floor(numpy.mean(marks))
