54f8693ea58bce689100065f


from math import ceil
from fractions import Fraction as F
def decompose(n):
    f = F(n)
    ff = int(f)
    result = [str(ff)] if ff else []
    f -= ff
    while f>0:
        x = F(1,int(ceil(f**-1)))
        f -= x
        result.append(str(x))
    return result
_________________________________
from fractions import Fraction
from math import ceil
 
def decompose(n):
    try:
        n = Fraction(n)
    except ValueError:
        return []
    try:
        e = int(n)
    except ValueError:
        return []
    if n == 0: return []
    
    if n == e: return [str(n)]
    n -= e
    if e != 0: l = [str(e)] 
    else: l = []
    while(n.numerator > 1):
        e = Fraction(1, int(ceil(1 / n)))
        l.append(str(e.numerator) + "/" + str(e.denominator))
        n -= e
    l.append(str(n.numerator) + "/" + str(n.denominator))
    return l
_________________________________
def decompose(n):
    if '/' in n:
        strs = n.split('/')
        a = int(strs[0]); b = int(strs[1]);
    elif '.' in n:
        strs = n.split('.')
        b = 10**len(strs[1]);a = int(strs[1]) + b*int(strs[0]); 
    else: a=int(n); b=1
    output = []
    while a >= b:
        i = a//b; a = a - b*i;
        output.append(str(i))
    while a > 0:
        i = b//a+1 if b%a else b//a;
        a = a*i-b; b = b*i
        output.append('1/'+str(i))
    return output
_________________________________
from fractions import gcd
def decompose(n):
    if '.' in n:
        f = 10 ** len(n.split('.')[1])
        n = '%d/%d' % (int(float(n) * f), f)
    if '/' not in n: n += '/1'
    l = []
    x, y = map(int, n.split('/'))
    i, x = divmod(x, y)
    if i: l.append(str(i))
    while x:
        g = gcd(x, y)
        x //= g; y //= g
        c, x = divmod(-y, x)
        y *= abs(c)
        l.append('1/%d' % abs(c))
    return l
_________________________________
import math

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def decompose(n):
    den = 1
    if "/" in n:
        num, den = [int(x) for x in n.split("/")]
    elif "." in n:
        d = next((i for i, x in enumerate(n[n.index(".")+1:]) if int(x)))
        den = 10**(len(n)-n.index(".")-1)
        num = int(n[n.index(".")+1+d:])+int(n[:n.index(".")])*den
    else:
        num = int(n)

    arr = [str(num//den)] if num>=den else []
    num = num % den
    while num !=0:
        f = math.ceil(den/num)
        common_den = lcm(den, f)
        num = num*common_den//den - common_den//f
        den = common_den
        arr.append("%d/%d" % (1,f))

    return arr
_________________________________
from fractions import Fraction


def decompose(n):
    res = []
    i = Fraction(n)
    summa = 0
    if i >= 1:
        res.append(Fraction(int(i)))
        summa = sum(res)
    integer = 2
    while summa != i:
        k = Fraction(1, integer)
        if summa + k <= i:
            res.append(k)
            summa = sum(res)
            n = i - summa
            if n:
                integer = int(1/n)
        else:
            integer += 1
    return [str(i) for i in res]
_________________________________
import regex as re
from math import ceil

def decompose(n):
    # Steps:
    # 1) Parse input
    # 2) Simplify if possible
    # 2b) Pull integer part out, add to output
    # 3) Pull fractions as needed (check for input a/b: floor(b/a))
    output = []
    if n=='0': return []
    numer, denom = 0,0
    
    if '.' in n:
        # Input in decimal form
        parse = re.match(r'(\d+).(\d*)', n)
        if parse.group(1)!='0':
            output.append(parse.group(1))
        numer, denom = int(parse.group(2)), 10**len(parse.group(2))
    else:
        # Input in fractional form
        parse = re.match(r'(\d+)/(\d+)', n)
        numer,denom = int(parse.group(1)), int(parse.group(2))
        if numer>=denom:
            output.append(str(numer//denom))
            numer = numer%denom
    
    while numer!=0:
        pull = ceil(denom/numer)
        numer, denom = numer*pull-denom, denom*pull
        output.append(f"1/{pull}")
    
    return output
_________________________________
import math
def decompose(n):
    try:
        nstring, dstring = n.split('/')
        numerator, denominator = int(nstring), int(dstring)
    except:
        try: 
            intstring, decstring = n.split('.')
            denominator = 10 ** len(decstring)
            numerator = int(intstring)*denominator + int(decstring) 
        except:
            denominator=1
            numerator=int(n)

    acc_numerator = 0
    acc_denominator = 1
    output = []
    if (numerator>denominator):
        int_part = math.floor(numerator/denominator)
        acc_numerator += int_part * acc_denominator
        output.append(f"{int_part}")
    while (numerator/denominator!=acc_numerator/acc_denominator):
        r_number = (denominator * acc_denominator) / (numerator * acc_denominator - acc_numerator*denominator)
        sol = math.ceil(r_number)
        
        acc_numerator = acc_numerator*sol+acc_denominator
        acc_denominator = acc_denominator*sol
        
        output.append(f"1/{sol}")    
    return output
