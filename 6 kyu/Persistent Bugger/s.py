import operator
def persistence(n):
    i = 0
    while n>=10:
        n=reduce(operator.mul,[int(x) for x in str(n)],1)
        i+=1
    return i
________________________________________
def persistence(n):
    nums = [int(x) for x in str(n)]
    sist = 0
    while len(nums) > 1:
        newNum = reduce(lambda x, y: x * y, nums)
        nums = [int(x) for x in str(newNum)]
        sist = sist + 1
    return sist
________________________________________
from operator import mul
def persistence(n):
    return 0 if n<10 else persistence(reduce(mul,[int(i) for i in str(n)],1))+1
________________________________________
def persistence(n):
    if n < 10: return 0
    mult = 1
    while(n > 0):
        mult = n%10 * mult
        n = n//10
    return persistence(mult) + 1
________________________________________
persistence = lambda n,c=0: persistence(reduce(lambda x,y:int(x)*int(y),str(n)),c+1) if n >=10 else c
________________________________________
def persistence(n):
    if str(n) == 1:
        return 0
    count = 0
    while len(str(n)) > 1:
        total = 1
        for i in str(n):
            total *= int(i)
        n = total
        count += 1
    return count
________________________________________
def persistence(n):
    if len(str(n)) == 1:
        return 0
    n_str = str(n)
    total = 1
    for i in n_str:
        total = total * int(i)
    return 1 + persistence(total)
________________________________________
def persistence(n):
    if n<10:
        return 0
    for i in range(1,n):
        x=1
        for s in str(n):
            x*=int(s)
        n=x
        if len(str(n))==1:
            return i
________________________________________
def persistence(n):
    count = 0
    while n > 9:
        new_n = 1
        for item in str(n):
            new_n *= int(item)
        count +=1
        n = new_n
    return count
________________________________________
def persistence(n):
    counter = 0
    while n >= 10:
        n_str = str(n)
        n = 1
        for i in n_str:
            n *= int(i)
        counter += 1
    return counter
________________________________________
def persistence(n):
    c = 0
    while n > 9:
        p = 1
        for i in str(n):
            p *= int(i)
        c += 1
        n = p
    return c
________________________________________
def persistence(n):
    p = 0
    d = 1
    lst = list(str(n))
    while True:
        if len(lst) == 1:
            break
        for digit in lst:
            d *= int(digit)
        if len(str(d)) == 1:
            p += 1
            break
        else:
            p += 1
            lst = list(str(d))
            d = 1
    return p
