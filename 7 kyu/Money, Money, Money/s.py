563f037412e5ada593000114



def calculate_years(principal, interest, tax, desired):
    years = 0
    
    while principal < desired:
        principal += (interest * principal) * (1 - tax)
        years += 1
        
    return years
_________________________
from math import ceil, log

def calculate_years(principal, interest, tax, desired):
    if principal >= desired: return 0
    
    return ceil(log(float(desired) / principal, 1 + interest * (1 - tax)))
_________________________
def calculate_years(principal, interest, tax, desired):
    years = 0
    if principal == desired:
        return years
    while principal < desired:
        x = principal * interest
        y = x * tax
        principal = principal + x - y
        years += 1
    return years
_________________________
from math import ceil, log

def calculate_years(principal, interest, tax, desired):
    return ceil(log(float(desired) / principal, 1 + interest * (1 - tax)))
_________________________
def calculate_years(principal, interest, tax, desired):
    year = 0
    while (principal < desired):
        increment = principal * interest * (1-tax)
        principal = principal + increment
        year = year + 1
    return year
_________________________
import math

def calculate_years(principal, interest, tax, desired):
    return 0 if principal >= desired else math.ceil((math.log(desired) - math.log(principal))/math.log(1+interest*(1-tax)))
_________________________
def calculate_years(p, i, t, d, n=0):
    if p >= d:
        return n
    p = p + p * i * (1 - t)
    return calculate_years(p, i, t, d, n+1)
_________________________
def calculate_years(p, i, t, d):
    y = 0
    if p != d:
        while p < d:
            p += p * i * (1 - t)
            y += 1
    return y
_________________________
def calculate_years(principal, interest, tax, desired):
    taxs = 0
    counter = 0
    while(1):
        if principal >= desired:
            return counter
        
        taxs = principal * interest * tax
        
        principal = principal * (1 + interest) - taxs
        counter += 1
_________________________
def calculate_years(principal, interest, tax, desired):
    curr = principal
    year = 0
    while curr < desired:
        curr += curr * interest * (1 - tax)
        year += 1
    return year
_________________________
def calculate_years(principal, interest, tax, desired):
    years = [principal]
    
    while years[-1] < desired:
        gainz = years[-1] * interest
        tru_gainz = gainz - (gainz * tax)
        years.append(years[-1] + tru_gainz)
        
    return len(years) - 1
