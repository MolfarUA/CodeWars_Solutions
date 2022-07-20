526a569ca578d7e6e300034e


def convert(input, source, target):
    source_base = len(source)
    source_map = {c: i for i, c in enumerate(source)}
    input = sum(pow(source_base, i) * source_map[c] for i, c in enumerate(reversed(input)))

    target_base = len(target)
    result = ''
    while input > 0:
        input, mod = divmod(input, target_base)
        result += target[mod]
    return result[::-1] or target[0]
__________________________________________
def to_base(n, base, alphabet):
    if n < base:
        return alphabet[n]
    else:
        q, r = divmod(n, base)
        return to_base(q, base, alphabet) + alphabet[r]
    
def convert(input, source, target):
    b = len(source)
    n = sum(source.index(x) * b ** i for i, x in enumerate(reversed(input)))
    return to_base(n, len(target), target)
__________________________________________
from math import log

def convert(value, source, target):
    value = sum(source.find(c) * (len(source) ** i) for i, c in enumerate(reversed(value)))
    return ''.join(target[(value / (len(target) ** i)) % len(target)] for i in xrange(0 if not value else int(log(value, len(target))),-1,-1))
__________________________________________
def convert(input, source, target):
    """Convert input in source alphabet and base to output in target alphabet and base."""
    # Determine numeric base of source alphabet & create mapping from source alphabet
    # to decimal. Decimal is arbitrary and was chosen for ease of debugging.
    source_base = len(source)
    source_map = dict((char, i) for i, char in enumerate(source))
    
    # Determine numeric base of target alphabet & create mapping from decimal
    # to target alphabet
    target_base = len(target)
    target_map = dict((i, char) for i, char in enumerate(target))
    
    decimal_accumulator = 0
    for i, val in enumerate(reversed(input)):
        decimal_accumulator += (source_base ** i) * source_map[val]
    
    output = ''
    while decimal_accumulator > 0:
        remainder = decimal_accumulator % target_base
        output = str(target_map[remainder]) + output
        decimal_accumulator /= target_base
    
    if output == '':
        output = target[0]  # This only happens if the input is zero in its source language
        
    return output
__________________________________________
def convert(input, source, target):
    sourceBase = len(source)
    targetBase = len(target)
    # to decimal
    value = 0
    for i, e in enumerate(reversed(input)):
        value += source.index(e)*sourceBase**i
    print(f'decimal value: {value}')
    if target == dec:
        return str(value)
    # to target base
    number = int(value)
    result = ''
    if number == 0:
        return target[0]
    while number > 0:
        result += target[number % targetBase]
        number //= targetBase
    return result[::-1]
__________________________________________
def convert(input, source, target):
    from_system = len(source)
    to_system = len(target)
    symbols, total, result = input, 0, ''
    for symbol in symbols:
        total = total * from_system +  source.index(symbol) 
    if total == 0: return target[0]
    while total > 0:
        total, index = divmod(total, to_system)
        result = target[index] + result
    return result
__________________________________________
def convert(s, a, b, r=''):
    n = sum(a.index(c) * len(a) ** i for i, c in enumerate(s[::-1]))
    while n: n, r = n // len(b), r + b[n % len(b)]
    return r[::-1] or b[0]
__________________________________________
def convert(inputStr,source,target):
    
    bin='01'
    oct='01234567'
    dec='0123456789'
    hex='0123456789abcdef'
    allow='abcdefghijklmnopqrstuvwxyz'
    allup='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alpha='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphanum='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    n=0
    power=0
    for i in inputStr[::-1]:
        n+=source.index(i)*len(source)**power
        power+=1

    if n==0:return target[0]
    result=''
    while n:
        result+=target[n%len(target)]
        n//=len(target)

    return result[::-1]
__________________________________________
def convert(input, source, target):
    sum=0
    i=0
    for s in input[::-1]:
        sum+=source.find(s)*len(source)**i
        i+=1
    res=""
    if sum==0:
        return target[0]
    while sum>0:
        res+=target[sum%len(target)]
        sum=(sum-(sum%len(target))) // len(target)
    return res[::-1]
__________________________________________
def convert(input, source, target):
    
    output = ''
    len_src = len(source)
    len_tar = len(target)
    len_inp = len(input)
    tmp = sum(source.index(val) * len_src ** (len_inp - i) for  i, val in enumerate(input, 1))

    while tmp >= len_tar:
        tmp, b = divmod(tmp, len_tar)
        output += target[b]

    output += target[tmp]
    
    return output[::-1]
