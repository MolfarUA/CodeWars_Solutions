def century(year):
    return (year + 99) // 100
####################
import math

def century(year):
    return math.ceil(year / 100)
##############
def century(year):
    if year%100==0:
        return year//100
    else:
        return year//100+1
#############
def century(year):
    return (year / 100) if year % 100 == 0 else year // 100 + 1
############
def century(year):
    return (year - 1) // 100 + 1
#############
from math import ceil

def century(year):
    return ceil(year / 100)
##############
def century(year):
    return -(-year//100)
###########
from math import ceil
#############
def century(year):
    return year//100 + bool(year % 100)
