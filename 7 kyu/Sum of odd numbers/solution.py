def row_sum_odd_numbers(n):
    return n**3
##################
def row_sum_odd_numbers(n):
    return sum(range(n*(n-1)+1, n*(n+1), 2))
##############3
def row_sum_odd_numbers(n):
    if type(n)==int and n>0:
        return n**3
    else:
        return "Input a positive integer"
###############
def row_sum_odd_numbers(n):
    return n*n*n
##############
def row_sum_odd_numbers(n):
    return pow(n, 3)
############
row_sum_odd_numbers=(3).__rpow__
############
def row_sum_odd_numbers(n, base=2):
    first_num = (n * (n - 1)) + 1
    numbers = range(first_num, first_num + base * n, base)
    return sum(numbers)
#############
def row_sum_odd_numbers(n):
    sum = 0
    num = n * n + n - 1
    for i in range(n):
        sum += num
        num -= 2
    return sum
##########
row_sum_odd_numbers = lambda n: n ** 3
###########
def row_sum_odd_numbers(n):
    return sum([i for i in range(sum([i for i in range(1, n+1)])*2) if i % 2][:-n-1:-1])
###########
import numpy as np
def row_sum_odd_numbers(n):
    return sum(np.linspace(n**2-(n-1),(n**2+n-1),n))
############
def row_sum_odd_numbers(n):
    first = n * (n - 1) + 1
    return first * n + n * (n - 1)
###########
def row_sum_odd_numbers(n):
    a = [y*[False] for y in range(1, n+1)]
    odds = iter(list(range(1, 10**6, 2)))
    return sum([[next(odds) for c in x if c is False] for x in a][-1])
