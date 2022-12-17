58bc16e271b1e4c5d3000151


def get_min_base(number):
    
    def converter(number,system):
        num = []
        while number != 0:
            num.append(str(number % system))
            number = number // system
        return num[::-1]

    def is_all_one(num):
        if all(n == "1" for n in num):
            return True
        return False

    def back_converter(num_lst,sys):
        num_lst.reverse()
        nums = sum(int(num_lst[i]) * (sys ** i) for i in range(len(num_lst)))
        return nums

    for sys in range(2,11):
        num = converter(number,sys)
        if is_all_one(num): return sys

    root = 2
    sys = int(number ** (1/root))
    while sys > 1:
        num = converter(number,sys)
        if is_all_one(num): return sys
        root += 1
        sys = int(number ** (1/root))
    return number - 1
______________________________________
def get_min_base(n):
    if n in (3,7): return 2
    for i in range(10,1,-1):
        b = int(n ** (1/i))
        s = sum(b**j for j in range(i+1))
        if s==n:
            return b
    return n-1
______________________________________
def get_min_base(number):
    power = 2
    while True:
        base, digit, n = int(number ** (1/power)), True, number
        while n != 0:
            remainder = n % base
            if remainder != 1:
                digit = False
                break
            n = n // base
        if digit: return base
        if base <= 1: return number - 1
        power += 1
______________________________________
import math

def criteria(x, y, r, number, eps1 = 1e-4, eps2 = 1):
    if abs(y - r) <= eps1 and abs((x**(r+1) - 1) / (x-1) - number) < eps2: return True
    return False

def get_min_base(number):
    b1, b2, n1, n2 = 2, number-1, math.log(number + 1, 2) - 1, math.log(number*(number-2)+ 1, number-1) - 1
    eps1, p, q = 1e-4, int(n1), 0
    
    # case when number is equal to 1
    if number == 1: return 2
    
    # case when degree is equal to 2
    if abs(n1 - round(n1, 0)) <= eps1: return b1
    
    # case when degree is more than or equal to 1
    for r in range(p, q, -1):
        x1, x2, y1, y2 = b1, b2, n1, n2
        if criteria(x1, y1, r, number): return x1
        if criteria(x2, y2, r, number): return x2
        while True:
            if x2 - x1 <= 1: break
            x3 = int(round((x1 + x2) / 2, 0))
            y3 = math.log(number*(x3-1) + 1, x3) - 1
            if criteria(x3, y3, r, number): return x3
            if y3 <= r: x2, y2 = x3, y3
            else: x1, y1 = x3, y3
    return number-1
______________________________________
import math

def criteria(x, y, r, number, eps1 = 1e-4, eps2 = 1):
    if abs(y - r) <= eps1:
        if abs((x**(r+1) - 1) / (x-1) - number) < eps2: return True
    return False

def get_min_base(number):
    b1, b2, n1, n2 = 2, number-1, math.log(number + 1, 2) - 1, math.log(number*(number-2)+ 1, number-1) - 1
    eps1, p, q = 1e-4, int(n1), 0
    
    # case when number is equal to 1
    if number == 1: return 2
    
    # case when degree is equal to 2
    if abs(n1 - round(n1, 0)) <= eps1: return b1
    
    # case when degree is more than or equal to 1
    for r in range(p, q, -1):
        x1, x2, y1, y2 = b1, b2, n1, n2
        if criteria(x1, y1, r, number): return x1
        if criteria(x2, y2, r, number): return x2
        #if abs(y1 - r) <= eps1:
        #    if abs((x1**(r+1) - 1) / (x1-1) - number) < eps2: return x1
        #if abs(y2 - r) <= eps1:
        #    if abs((x2**(r+1) - 1) / (x2-1) - number) < eps2: return x2
        while True:
            if x2 - x1 <= 1: break
            x3 = int(round((x1 + x2) / 2, 0))
            y3 = math.log(number*(x3-1) + 1, x3) - 1
            if criteria(x3, y3, r, number): return x3
            #if abs(y3 - r) <= eps1:
            #    if abs((x3**(r+1) - 1) / (x3-1) - number) < eps2: return x3
            if y3 <= r: x2, y2 = x3, y3
            else: x1, y1 = x3, y3
    return number-1
______________________________________
def get_min_base(n):
    if n in [3,7]: 
        return 2
    for j in range(10,1,-1):
        beta = int(n ** (1/j))
        sum1 = sum(beta**k for k in range(j+1))
        if sum1==n:
            return beta
    return n-1
______________________________________
import math
def get_min_base(n):
    if n<4: return [0,10,1,2][n]
    leng = int(n**0.5)+1
    ans = float("inf")
    for i in range(2, leng+1):
        b = math.floor(n**(1/(i-1)))
        x = round(math.log((b-1)*n+1, b),14)
        if x.is_integer():
            if ans>x:
                ans = b
        if b<=2:
            break
    return ans if ans!=float("inf") else n-1
