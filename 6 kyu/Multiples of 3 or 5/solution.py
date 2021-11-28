def solution(number):
    numbers = []
    for n in range(number):
        if n % 3 == 0 or n % 5 == 0:
            numbers.append(n)
    return sum(numbers)
############
def solution(number):
    return sum(x for x in range(number) if x % 3 == 0 or x % 5 == 0)
##############
def solution(number):
    sum = 0
    for i in range(number):
        if (i % 3) == 0 or (i % 5) == 0:
            sum += i
    return sum
##############
def solution(number):
    a3 = (number-1)/3
    a5 = (number-1)/5
    a15 = (number-1)/15
    result = (a3*(a3+1)/2)*3 + (a5*(a5+1)/2)*5 - (a15*(a15+1)/2)*15
    return result
##############
def solution(number):
    threes = range(3, number, 3)
    fives = range(5, number, 5)
    return sum(list(set(threes + fives)))
#################
def solution(number):
  threes = (number - 1) / 3
  fives = (number - 1) / 5
  fifteens = (number - 1) / 15
  return 3 * threes * (threes + 1) / 2 + 5 * fives * (fives + 1) / 2 - 15 * fifteens * (fifteens + 1) / 2
################
def solution(number):
  return sum([x for x in range(number) if x % 3 == 0 or x % 5 == 0])
###########
from math import floor

def sum_to_n(n):
    return n * (n + 1) / 2

def sum_of_multiples(k, n):
    return k * sum_to_n(floor(n / k))

def solution(number):
    number = number - 1
    return (sum_of_multiples(3, number) + 
        sum_of_multiples(5, number) - 
        sum_of_multiples(3 * 5, number))
##############
def solution(number):
  import itertools
  return sum(set(itertools.chain(range(0, number, 3), range(0, number, 5))))
###############
def solution(number):
    return sum([i for i in range(number) if i % 3 == 0 or i % 5 == 0])
