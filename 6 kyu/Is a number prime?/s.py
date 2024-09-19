def is_prime(num):
    """Check if a number is prime."""
    if num <= 1:
        return False  # 0 and 1 are not prime numbers
    if num <= 3:
        return True   # 2 and 3 are prime numbers
    if num % 2 == 0 or num % 3 == 0:
        return False  # Eliminate multiples of 2 and 3
    
    # Check for factors from 5 to the square root of n
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    
    return True
__________________________
def is_prime(num):
    if num <= 0:
        return False
    if num == 1:
        return False
    if num == 2 or num == 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num %i == 0 or num % (i+2) == 0:
            return False
        i += 6
    return True
__________________________
import math

def is_prime(num):
    if num <= 1:
        return False
    if num == 2:
        return True  # 2 is the only even prime number
    if num % 2 == 0:
        return False  # Exclude all other even numbers

    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True
__________________________
def is_prime(num):
    if num == 2 or num == 3: # these two are included
        return True
    
    if num % 2 == 0 or num == 1 or num < 0: # eliminates odds, negatives and 1
        return False
    
    i = 3 # three is the next prime we use to check
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0: # div3 or div5... 
            return False                       # and it goes on dividing by prime numbers
        i += 2
    return True
__________________________
import math
def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    max_div = int(math.sqrt(num)) + 1
    for i in range(2, max_div):
        if num % i == 0:
            return False
    return True
