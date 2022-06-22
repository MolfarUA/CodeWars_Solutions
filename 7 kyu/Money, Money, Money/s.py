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
