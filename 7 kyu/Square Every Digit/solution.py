def square_digits(num):
    temp = ""
    for i in str(num):
        temp += str(int(i) ** 2)
    return int(temp)
print(square_digits(9119))
#######################
def square_digits(num):
    return int(''.join(str(int(d)**2) for d in str(num)))
##############
def square_digits(num):
    ret = ""
    for x in str(num):
        ret += str(int(x)**2)
    return int(ret)
##################
def square_digits(num):
    return int(''.join(str(int(c)**2) for c in str(num)))
#################
def square_digits(num):
    result = 0
    multiplier = 1
    while num > 0:
        digit = (num % 10)
        result += (digit**2) * multiplier
        num /= 10
        multiplier *= 10
        if digit > 3:
            multiplier *= 10
    return result
###############
def square_digits(n):
  return int("".join(str(pow(int(i), 2)) for i in str(n)))
################
def square_digits(num):
    return int(''.join([str(n * n) for n in map(int, str(num))]))
###############
def square_digits(num):
    num = str(num)
    ans = ''
    for i in num:
        ans += str(int(i)**2)
    return int(ans)
##################
square_digits = lambda num: int(''.join(str(int(d)**2) for d in str(num)))
###############
def square_digits(num):
    result = 0
    multiplier = 1
    while num:
        digit = num % 10
        result += digit ** 2 * multiplier
        multiplier *= (10, 100)[digit > 3]
        num //= 10
                                        
    return result
###############
def square_digits(num):
    squares = ''
    for x in str(num):
        squares += str(int(x) ** 2)
    return int(squares)
###################
def square_digits(num):
  return int(''.join([str(int(x)**2) for x in list(str(num))]))
################
def square_digits(num):
    return int(''.join(map(lambda x: str(int(x)**2), str(num))))
################
def square_digits(num):
    return  int(''.join([str(int(i)*int(i)) for i in str(num)]))
###############
from functools import partial

class F(object):
    def __init__(self, _fs=None):
        self.fs = _fs or []

    def __rshift__(self, f):
        return F(self.fs + [f])
    
    def __call__(self, arg):
        for f in self.fs:
            arg = f(arg)
        return arg

square_digits = F() >> str >> partial(map, int) >> partial(map, lambda x: x**2) >> partial(map, str) >> "".join >> int
#################
def square_digits(num):
    return int(''.join(map(str,map(lambda x:x**2,map(int,list(str(num)))))))
#################
def square_digits(num):
    return reduce(lambda x,y: int(str(x)+str(y)),map(lambda x: int(x)**2, list(str(num))))
