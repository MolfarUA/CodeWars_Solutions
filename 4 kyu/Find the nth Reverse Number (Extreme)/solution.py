
def find_reverse_number(n):
    """ Return the nth number in sequence of reversible numbers.

    For reversible numbers, a pattern emerges when compared to n:
    if we subtract a number made of a sequence of the digit 9
    (i.e. 9, 99, 999, our magic number) from n, the result forms 
    the left half of the nth reversible number starting from 0.
    The number of digits "9" in the magic number increases every
    time n reaches an order of magnitude of the number 11; the
    width of that order of magnitude is the width of the magic number.
    That width also tells us how many digits of the left half must
    be mirrored to form the final, nth reversible number.
    
    Examples (_ digits get mirrored, | digits remain static)
    
        n = 109    ->   100  ->  1001
                   -9   _||      _||_
        
        n = 110    ->   11   ->  1111
                  -99   __       ____
                  
        n = 1099   ->  1000  ->  100001
                  -99  __||      __||__
                  
        n = 1100   ->  101   ->  101101
                 -999  ___       ______
    """  
    
    n = n - 1                   # this kata assumes 1-based indices
    
    if n < 10:                  # tiny optimization
        return n
    
    x = n // 11                 # order of magnitude
    width = len(str(x))         # width of x
    nines = int("9"*width)      # the magic number
    lh = str(n - nines)         # the left side of the result
    rh = lh[:width][::-1]       # the right side of the result
    result = int(lh + rh)
    return result
__________________________________________________
def find_reverse_number(n):

    sn = str(n)

    if sn[:2] == '10':
        n -= 1 * 10 ** (len(sn) - 2)
        start = str(n)
        end = start[: -1][:: -1]
        return int(start + end)


    coef = 1 * 10 ** (len(sn) - 1)

    if len(sn) == len(str(n-coef)):
        n -= coef
        start = str(n)
        end = start[:-1][::-1]

    else:
        n %= coef
        start = str(n)
        end = start[::-1]

    return int(start + end)
__________________________________________________
import math

def find_reverse_number(n):
    if n == 1: return 0
    n -= 1
    m = n/18
    p = max(-1,math.floor(math.log10(m)))
    if m <= (pow(10,p+1)-1)/9:
        k = 2*(p+1)
        n -= 11*pow(10,p) - 2
    elif m <= (pow(10,p+1)-1)/9 + pow(10,p+1)/2:
        k = 2*(p+1) + 1
        n -= 2*(pow(10,p+1)-1)
    else:
        k = 2*(p+1) + 2
        n -= 11*pow(10,p+1) - 2
    q = (k+1)//2
    x = n - 1 + pow(10,(k-1)//2)
    y = x * pow(10,k//2)
    if k % 2 == 1: x //= 10
    i = k//2 - 1
    while i >= 0:
        y += (x%10) * pow(10,i)
        i -= 1
        x //= 10
    return y
__________________________________________________
def find_reverse_number(n):
    if n < 11:
        return n - 1
    
    s = str(n)
    if s[0:2] == '10':
        minus = 10 ** (len(s) - 2)
    else:
        minus = 10 ** (len(s) - 1)
        
    new = n - minus
    rev = str(new)[::-1]
        
    if int(s[0]) < 2 and not s[0:2] == '10':
        return new * minus + int(rev)
    else:
        return new * minus + int(rev[1:])
__________________________________________________
def find_reverse_number(n):
    if n<11: return n-1
    n1 = str(n)[1:]
    n2 = str(n)[1:-1][::-1]
    c =str(int(str(n)[0])-1)
    answ =  str(c + n1 + n2 + c)
    if n in [100,1000,10000,100000,1000000,10000000,100000000,1000000000,10000000000,100000000000,1000000000000]:
        return int('9'+str(n)[1:-1]+str(n)[2:-1]+'9')
    if answ[0]=='0': 
        answ=answ[:-1]
        answ = answ[:len(answ)//2+1]
        try: 
            if answ[0]=='0'and str(n)[0]=='1' and str(n)[1]=='0':
                print('aici',n)
                if str(n)[0]=='1' and str(n)[1]=='0':
                    x = str(n)
                    y = '9'+x[2:]+x[2:-1][::-1]+'9'
                    return int(y)
                answ = int('9'+answ[1:-1]+'9')
                if answ[1]=='0'and str(n)[0]=='1':
                    print('acolo')
                return answ
            return int(answ[1:] + answ[::-1][:-1])
        except: return 0

    return int(answ) if n>19 else int(answ)//10
__________________________________________________
a=[0,10,9]
for i in range(1,12):
    a.extend([9*10**i,9*10**i])
b=[0]
for i in range(1,len(a)):
    b.append(b[i-1]+a[i])
    
def find_reverse_number(n):
    if n<20:
        if n<11: return n-1
        else: return (n%10)*11
    k=0
    while b[k]<n: k+=1
    r=n-b[k-1]
    j=(k+1)//2-1
    u,v=divmod(r,10**j)
    if v>0:        
        x=str(u+1)
        y=str(v-1).zfill(j)
        z=y[::-1] if k%2==0 else y[::-1][1:]
        res=int(x+y+z+x)
    else:
        x=str(u)+'9'*(k-2)+str(u)
        res=int(x)
    return res
__________________________________________________
find_reverse_number = lambda n, m=0: 0 if n < 2 else int((s := str(n - 2 + z)) + s[::-1][~m&1:]) if n - 2 < 9 * (z := 10 ** (m // 2)) else find_reverse_number(n - 9 * z, m + 1)
__________________________________________________
def find_reverse_number(n):
    if n<=10:
        return n-1
    res=str(n)
    if res[0]!="1":
        s=chr(ord(res[0])-1)+res[1:]
        return int(s+s[-2::-1])
    index=2 if res[:2]=="10" else 1
    s=str(int(res[:index])-1).lstrip("0")+res[index:]
    return int(s+s[::-1]) if index==1 else int(s+s[-2::-1])
__________________________________________________
def find_reverse_number(n):
    if n <= 10:
        return n-1
    elif str(n)[0:2] == '10':
        return int(''.join('9' + str(n)[2:] + str(n)[2:-1][::-1] + '9'))
    elif str(n)[0] == '1':
        return int(''.join(str(n)[1:] + str(n)[1:][::-1]))
    else:
        return int(''.join(str(int(str(n)[0])-1) + str(n)[1:] + str(n)[1:-1][::-1] + str(int(str(n)[0])-1)))
__________________________________________________
def find_reverse_number(n):
    n -= 1
    if n < 10: return f(n, 1)
    n -= 10
    if n < 9: return f(n+1, 2)
    n -= 8
    i,m = 3,90
    while True:
        if n < m: return f(n, i)
        n -= m
        if n < m: return f(n, i + 1)
        n -= m
        i += 2
        m *= 10

def f(n, k):
    t = k >> 1 if k % 2 != 0 else (k >> 1) - 1
    m = 10 ** t
    m += n - 1
    r = m
    if k % 2 != 0:
        m //= 10
    while m > 0:
        r = r * 10 + (m % 10)
        m //= 10
    return r
