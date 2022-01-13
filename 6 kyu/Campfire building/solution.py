from math import sqrt

def is_constructable(area):
    '''
    Is "area" the sum of two perfect squares?
    '''
    return any(
        sqrt(area - num ** 2).is_integer()
        for num in range(int(sqrt(area)) + 1)
    )
__________________________________
def is_constructable(a):
    i = 2
    while (i * i <= a):
        c = 0
        if (a % i == 0):
            while (a % i == 0):
                a = int(a / i)
                c += 1
            if (i % 4 == 3 and c % 2 != 0):
                return False
        i += 1
    return a % 4 != 3
__________________________________
import math
def is_constructable(a):
    r = math.sqrt(a)
    x = math.floor(r)
    y = 0
    while x >= y:
        if a == (x*x)+(y*y):
            return True
        if a < (x*x)+(y*y):
            x -= 1
            y += 1
        else:
            y += 1
    return False
__________________________________
def is_constructable(a):
    i=0
    while True:
        if i**2>a:
            return False
        if (a-i**2)**0.5-int((a-i**2)**0.5)==0:
            return True
        i+=1
__________________________________
def is_constructable(a):
    if a ** (1/2) % 1 == 0 : return True
    for i in range(1, int((a/2)**(1/2)) + 1) :
        if ((a - (i ** 2)) ** (1 / 2)) % 1 == 0 : return True
    return False
__________________________________
def is_constructable(a):
    if a ==1:
        return True
    s = dict()
    for i in range(a):
        if  i*i >a:
            break
        s[i*i]=1
        if (a-i*i) in s.keys():
            return True
    return False
__________________________________
import math

def is_constructable(area):
    """ The problem is recast as finding Pythagorean triples (also perfect
        squares by allowing for a 'zero side'), as the area is equivalent
        to c^2 = a^2 + b^2. The below logic verifies that c^2 - a^2 = b^2,
        where b is an integer, by checking that the float square root is
        equal to the integer square root. """
    max_side = math.isqrt(area) + 1
    for i in range (0, max_side):
        if math.isqrt(area - i*i) == math.sqrt(area - i*i):
            return True
    return False
__________________________________
def is_constructable(a):
    for n in range(int(a**0.5) + 1):
        if ((a - n**2)**0.5).is_integer():
            return True
    return False
__________________________________
def is_constructable(a):
    if ((int(a ** (1/2))) ** 2) == a:
        return (True)
    counter = 0
    while counter * counter < a:
        counter += 1
        k = counter * counter
        y = a - k
        try:
            j = ((int(y ** (1/2))) ** 2)
            if j == y:
                return True
        except:
            pass
    return False
