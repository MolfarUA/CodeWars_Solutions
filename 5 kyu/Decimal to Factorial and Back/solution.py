54e320dcebe1e583250008fd


from math import factorial
from itertools import dropwhile

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASIS = [factorial(n) for n in range(len(DIGITS))]

def dec2FactString(nb):
    representation = []
    for b in reversed(BASIS):
        representation.append(DIGITS[nb // b])
        nb %= b
    return "".join(dropwhile(lambda x: x == "0", representation))

def factString2Dec(string):
    return sum(BASIS[i]*DIGITS.index(d) for i, d in enumerate(reversed(string)))
_____________________________
base='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
fact = lambda n: fact(n-1)*n if n else 1

def dec2FactString(nb, i=1):
    return dec2FactString(nb//i,i+1) + base[nb%i] if nb else ''

def factString2Dec(string):
    return fact(len(string)-1)*base.index(string[0]) + factString2Dec(string[1:]) if len(string) else 0
_____________________________
from math import factorial
def dec_2_fact_string(nb):
    out, i = [],1
    while nb:
        nb,rem = divmod(nb,i)
        out.append(rem if rem<10 else chr(rem+55))
        i += 1
    return ''.join(map(str,out[::-1]))

def fact_string_2_dec(s):
    return sum(int(x.isdigit() and x or ord(x)-55)*factorial(len(s)-i) for i,x in enumerate(s,start=1))
_____________________________
from itertools import dropwhile
from math import factorial
from string import digits, ascii_uppercase

BASE = digits + ascii_uppercase
FACTS = tuple(map(factorial, range(36, -1, -1)))

def dec2FactString(number: int) -> str:
    res = []
    for fact in dropwhile(number.__lt__, FACTS):
        index, number = divmod(number, fact)
        res.append(BASE[index])
    return ''.join(res) or '0'

def factString2Dec(string: str) -> int:
    return sum(int(c, 36) * FACTS[i] for i, c in enumerate(string, -len(string)))
_____________________________
from math import factorial
alp = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def dec_2_fact_string(nb):
    result = ''
    start = 1
    while nb>0:
        result += str(nb%start) if nb%start<10 else alp[(nb%start-10)%26]
        nb = nb//start
        start += 1
    return result[::-1]
def fact_string_2_dec(string):
    return sum(factorial(i)*int(j) if j not in alp else \
               factorial(i)*int(alp.index(j)+10) for i,j in enumerate(string[::-1]))
_____________________________
from math import factorial
def dec_2_fact_string(nb):
    s,c="",0
    while nb>0:
        c+=1
        nb,b = divmod(nb,c)
        s= str(b)+s if b<10 else chr(b+55)+s   
    return s
def fact_string_2_dec(string):
    return sum([int(a)*factorial(len(string)-c) if a.isdigit() else (ord(a)-55)*factorial(len(string)-c)
            for c,a in enumerate(string,1)])
_____________________________
import string

powers = string.digits + string.ascii_uppercase

def dec_2_fact_string(nb):
    result = str()
    i = 1
    while nb > 0:
        result += powers[int(nb) % i]
        nb = nb // i
        i += 1
    return result[::-1]
    
def fact_string_2_dec(string):
    result = 0
    for enum, c in enumerate(string[::-1]):
        result += int(powers.index(c)) * fact(enum)
    return result

def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n-1)
_____________________________
fat = {}
fat[0] = 1

for i in range(1, 36):
    fat[i] = fat[i-1] * i
    
def dec2FactDigit(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('A') + digit - 10)

def fact2DecDigit(c):
    if 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 10;
    return ord(c) - ord('0')

def dec2FactString(nb):
    ans = ""
    
    for i in range(35, -1, -1):
        print(ans)
        if i == 0:
            print(ans)
            ans = ans + "0"
            continue
            
        if fat[i] > nb:
            if ans != "":
                print(fat[i], nb, ans)
                ans = ans + "0"
            continue
            
        ans = ans + dec2FactDigit(nb // fat[i])
        nb = nb % fat[i]
    
    return ans
        

def factString2Dec(s):
    result = 0
    
    for i in range(len(s) - 1, 0, -1):
        result = result + fact2DecDigit(s[len(s) - 1 - i]) * fat[i]
        
    return result
_____________________________
def dec_2_fact_string(nb):
    tnb = nb
    factlst = [] # 0!, 1!, ...
    n, k = 1, 0
    while n < nb:
        factlst.append(n)
        k += 1
        n *= k
    factlst.reverse()
    conv = []
    for i in range(len(factlst)):
        k = 0
        cf = factlst[i]
        while tnb - cf*k >= cf:
            k += 1
        conv.append(k)
        tnb -= cf*k
    convstr = ""
    alph = {
        10 : 'A',
        11 : 'B',
        12 : 'C',
        13 : 'D',
        14 : 'E',
        15 : 'F',
        16 : 'G',
        17 : 'H',
        18 : 'I',
        19 : 'J',
        20 : 'K',
        21 : 'L',
        22 : 'M',
        23 : 'N',
        24 : 'O',
        25 : 'P',
        26 : 'Q',
        27 : 'R',
        28 : 'S',
        29 : 'T',
        30 : 'U',
        31 : 'V',
        32 : 'W',
        33 : 'X',
        34 : 'Y',
        35 : 'Z'
    }
    for i in range(len(conv)):
        if conv[i] < 10:
            convstr += str(conv[i])
        else:
            convstr += alph[conv[i]]
    return convstr
def fact(n):
    if n == 0:
        return 1
    else:
        return n*fact(n-1)
def fact_string_2_dec(string):
    num = {
        'A' : 10,
        'B' : 11,
        'C' : 12,
        'D' : 13,
        'E' : 14,
        'F' : 15,
        'G' : 16,
        'H' : 17,
        'I' : 18,
        'J' : 19,
        'K' : 20,
        'L' : 21,
        'M' : 22,
        'N' : 23,
        'O' : 24,
        'P' : 25,
        'Q' : 26,
        'R' : 27,
        'S' : 28,
        'T' : 29,
        'U' : 30,
        'V' : 31,
        'W' : 32,
        'X' : 33,
        'Y' : 34,
        'Z' : 35
    }
    nb = 0
    strlst = [char for char in string]
    for i in range(len(string)):
        if strlst[i].isdigit():
            strlst[i] = int(strlst[i])
        else:
            strlst[i] = num[strlst[i]]
    for i in range(len(string)):
        nb += fact(len(string) - 1 - i) * strlst[i]
    return nb
_____________________________
import math
import numpy as np
import string

fact_digits = string.digits + string.ascii_uppercase
fact_dec_values = [
    math.factorial(index) for index, digit in enumerate(fact_digits)
]
fact_dec_values[0] = 0
dec_fact_digits = {
    index: digit for index, digit in enumerate(fact_digits)
}
fact_dec_digits = {
    value: key for key, value in dec_fact_digits.items()
}
print(fact_dec_values)
print(dec_fact_digits)


def dec_2_fact_string(dec_number: int) -> str:
    fact_number = []
    rest_in_dec = dec_number
    for fact_value in reversed(sorted(fact_dec_values)):
        if fact_value > 0:
            contained_fact_value = rest_in_dec // fact_value
            rest_in_dec -= contained_fact_value * fact_value
            if len(fact_number) > 0 or contained_fact_value > 0:
                fact_number.append(dec_fact_digits[contained_fact_value])
        else:
            fact_number.append('0')

    return ''.join(fact_number)


def fact_string_2_dec(fact_number: string) -> int:
    reversed_number = fact_number[::-1][1:]
    return np.sum([
        fact_dec_values[index + 1] * fact_dec_digits[value] for
        index, value in enumerate(reversed_number)
    ])
