57a5c31ce298a7e6b7000334


def bin_to_decimal(inp):
    return int(inp, 2)
_________________________
def bin_to_decimal(inp):
    num = 0
    inp = inp[::-1]
    for i in range(len(inp)):
        num += int(inp[i]) * 2 ** i
    return num
_________________________
bin_to_decimal = lambda inp: int(inp,2)
_________________________
def bin_to_decimal(inp):
    return int(inp, base=2)
_________________________
from functools import partial

bin_to_decimal = partial(int, base=2)
_________________________
def bin_to_decimal(inp):
    n = len(inp)
    s = 0
    
    for i in range(n):
        if inp[i] == '1':
            s += 2 ** (n - i - 1)
    
    return s
_________________________
def bin_to_decimal(bin):
    return int(bin, 2)
_________________________
def bin_to_decimal(s):
    return sum((2 ** i) * int(d) for i, d in enumerate(reversed(s)))
_________________________
bin_to_decimal = lambda x: int(x,2);
_________________________
def bin_to_decimal(x):
    return int(x, 2)
_________________________
def bin_to_decimal(inp):
    num = 0
    j = 0
    if inp == "0": return 0
    else:
        for i in inp[::-1]:
            if i == "1":
                num += 2 ** j
                j += 1
            else:
                j += 1
    return num
_________________________
def bin_to_decimal(inp):
    pass
    return sum([int(inp[i]) * 2 ** (len(inp) - i - 1) for i in range(len(inp))])
_________________________
def bin_to_decimal(inp):
    decimal = 0
    for i in range(len(inp)):
        decimal += int(inp[i]) * 2**(len(inp) - i - 1)
    return decimal
_________________________
def bin_to_decimal(inp):
    n = [int(x) for x in inp]
    n = n[::-1]
    for i, value in enumerate(n):
        if value == 1:
            n[i] = 2 ** i
    return sum(n)
_________________________
def bin_to_decimal(inp):
    f = 0
    inp = inp[::-1]
    for i in range(len(inp)):
        f += int(inp[i]) * (2 ** i)
        
    return f
