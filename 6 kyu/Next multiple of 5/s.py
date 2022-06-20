604f8591bf2f020007e5d23d


PROVIDERS = ( 
    lambda n: n*2 or 5,
    lambda n: n*4+1,
    lambda n: n*2+1, 
    lambda n: n*4+3, 
    lambda n: n*8+3,
)

def next_multiple_of_five(n):
    return PROVIDERS[n%5](n)
_______________________________
def next_multiple_of_five(n):
    b = ['0', '01', '1', '11', '011'][n % 5]
    return (n << len(b)) | int(b, 2) or 5
_______________________________
def next_multiple_of_five(n):
    mod5 = n % 5
    if n == 0:
        return 5
    elif mod5 == 0:
        add = '0'
    elif mod5 == 1:
        add = '01'
    elif mod5 == 2:
        add = '1'
    elif mod5 == 3:
        add = '11'
    elif mod5 == 4:
        add = '011'
    return int(bin(n)[2:]+add,2)
_______________________________
def next_multiple_of_five(n):
    i = 0
    while n > 0:
        i += 1
        n <<= 1
        m = n
        for k in range(1 << i):
            if not (m + k) % 5:
                return m + k
    return 5
_______________________________
def next_multiple_of_five(n):
    a, b = k[n % 5]
    return n << a | b or 5

k = (1,0), (2,1), (1,1), (2,3), (3,3)
_______________________________
def next_multiple_of_five(n):
    for i in ['0','1', '00', '01', '10', '11', '000', '001', '010', '011', '100', '101']:
        if not int(bin(n)[2:]+i, 2) % 5 and int(bin(n)[2:]+i, 2) != n :
            return int(bin(n)[2:]+i, 2)
_______________________________
from itertools import product as pd, count

def next_multiple_of_five(n):
    return next(int(f"{n:b}"+''.join(cb),2) or 5 for i in count(1) for cb in pd('10',repeat=i) if not int(f"{n:b}"+''.join(cb),2)%5)
_______________________________
def next_multiple_of_five(n):
    last_digit = str(n)[-1]
    
    if n == 0:
        return 5                        # edge case
    if last_digit in "05":
        return n<<1 
    if last_digit in "16":
        return int(bin(n)[2:] + "01", 2)
    if last_digit in "27":
        return int(bin(n)[2:] + "1", 2)
    if last_digit in "38":
        return int(bin(n)[2:] + "11", 2)
    if last_digit in "49":
        return int(bin(n)[2:] + "011", 2)
    
    
"""
    let investigate what does it actually mean when we add a "0 or "1" 
    behind a binary number.
    when we add a zero behind it means doubling the value, 
        1010 == 10, 10100 == 20
    when we change the last value from 0 to 1 it means adding one to the value,
        1010 == 10, 1011 == 11
    therefore adding "1" behind a binary value mean "2 * value + 1"
    
    let's look at the what will happen to final digit when we add "0" or "1":
    last digit    + 0    + 1        Shortest/Best Route (final digit = 0 or 5)
    ----------    ---    ---        -------------------
        0         '0'     1         +0        0 -> 0
        1          2      3         +01       1 -> 2 -> 5
        2          4     '5'        +1        2 -> 5
        3          6      7         +11       3 -> 7 -> 5
        4          8      9         +011      4 -> 8 -> 7 -> 5
        5         '0'     1         +0        5 -> 0
        6          2      3         +01       6 -> 2 -> 5
        7          4     '5'        +1        7 -> 5
        8          6      7         +11       8 -> 7 -> 5
        9          8      9         +011      9 -> 8 -> 7 -> 5
"""
