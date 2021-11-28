def quarter_of(month):
    if month < 4: return 1
    if month < 7: return 2
    if month < 10: return 3
    return 4
##############
def quarter_of(month):
    if month in range(1, 4):
        return 1
    elif month in range(4, 7):
        return 2
    elif month in range(7, 10):
        return 3
    elif month in range(10, 13):
        return 4
####################
from math import ceil
def quarter_of(month):
    return ceil(month / 3)
###################
def quarter_of(n):
    return (n + 2) // 3
##########################
def quarter_of(month):
    return (month + 2) // 3
###############
def quarter_of(month):
    
    # First Quarter
    if month <= 3:
        return 1
        
    # Second Quarter
    elif month <=6 and month > 3:
        return 2
        
    # Third Quarter
    elif month <=9 and month > 6:
        return 3
        
    # Fourth Quarter
    else:
        return 4
###################
quarter_of = quarterOf = lambda m: (m+2)//3
####################
def quarter_of(month):
    return (month-1) // 3 + 1 
####################
import math

def quarter_of(month):
    return math.ceil(month / 3)
#####################
def quarter_of(month):
    year ={1: [1, 2, 3], 2: [4, 5, 6], 3: [7, 8, 9], 4: [10, 11, 12]}   
    for k, v in year.items():
        if month in v:
            return k
########################
def quarter_of(month):
    return int((month/3) + 0.67)
###################
def quarter_of(mnth):
    return 1 if mnth<=3 else 2 if mnth<=6 else 3 if mnth<=9 else 4
#####################
def quarter_of(month):
    if month < 4 : return 1
    elif 3 < month < 7 : return 2
    elif 6 < month < 10 : return 3
    elif month > 9 : return 4
######################
from math import ceil 
quarter_of = lambda m: ceil(m / 3)
###################
def quarter_of(month):    
    return month/12*4 if int(month/12*4) == month/12*4 else int(month/12*4)+1
###################
def quarter_of(month):
    i = int(month)
    tmp = 0
    if(i <= 3):
        tmp = 1
    elif(i <= 6):
        tmp = 2
    elif(i <= 9):
        tmp = 3
    else:
        tmp = 4
    return tmp
##################
def quarter_of(month):
    if month > 9:
        ergebnis = 4
    elif month > 6:
        ergebnis = 3
    elif month > 3:
        ergebnis = 2
    else:
        ergebnis = 1
    return ergebnis
######################
def quarter_of(month):
    if month <= 3:
        return 1
    elif month <= 6 and month > 3:
        return 2
    elif month <= 9 and month > 6:
        return 3
    return 4
##############
def quarter_of(month):
    return int((month + 2) / 3)
###############
quarter_of = lambda m: __import__('math').ceil(m / 3)
###############
def quarter_of(m):
    return m//3 if m%3==0 else m//3+1
