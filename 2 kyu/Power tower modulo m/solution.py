from functools import lru_cache
from math import gcd, log

def factors(n):
    if n&1^1:
        yield 2
        while n&1^1: n >>= 1
    x, lim = 3, 9
    while lim <= n:
        if n % x == 0:
            yield x
            while n % x == 0: n //= x
        x += 2
        lim += x - 1 << 2
    if n > 1: yield n

@lru_cache(maxsize=None)
def totient(n):
    result = n
    for p in factors(n): result = result // p * (p - 1)
    return result

def check(base, h, m):
    if base > m: return False
    if h == 1 or m <= 1: return base <= m
    return check(base, h-1, log(m, base))

def tower(base, h, m):
    if m == 1: return 0
    if base == 1 or h == 0: return 1
    if base == m: return 0
    if h == 1: return base % m    
    if check(base, h-1, log(m, 2)): return pow(base, tower(base, h-1, m), m)
    return pow(base, totient(m) + tower(base, h-1, totient(m)), m)
  
##############
def totient(n):
    n2 = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            n2 = n2 * (p-1) // p
            while n % p == 0: n //= p
        p += 1 + p % 2
    if n > 1:
        n2 = n2 * (n-1) // n
    return n2

from math import log

def tower(base, h, m):
    if m == 1: return 0
    if base == 1 or h == 0: return 1
    # try calculating it directly...
    res = 1
    for _ in range(h):
        if res * log(base) > log(m): break
        res = base ** res
    else: return res % m
    # if it's over m, try numtheory way
    tot = totient(m)
    return pow(base, tot + tower(base, h-1, tot), m)
  
#################
def totient(n):
    phi = n
    for p in range(2, int(n ** .5) + 1):
        if not n % p:
            phi -= phi // p
            while not n % p: n //= p
    return phi if n == 1 else phi - phi//n


def tower(base, h, m=0):
    if h>2 and m>1: 
        t = totient(m)
        p = tower(base, h-1, t)
    else:
        return 0 if m == 1 else 1 if h == 0 else base%m if h==1 else pow(base, base, m)
    return pow(base%m, p if p!=0 else t, m)
  
#################
def totient(n):
    result = n
    for p in range(2, int(n ** .5) + 1):
        if not n % p:
            while not n % p: n //= p
            result -= result // p
    if n > 1: result -= result // n
    return result

def tower(a, b, m):
    from math import log
    gt = lambda a, b, m: a > int(m) or b > 1 and gt(a, b-1, log(m, a))

    if a in (1, m) or b <= 1 or m == 1:
        return (not b or a) % m

    if not gt(a, b-1, log(m, 2)):
        return pow(a, tower(a, b-1, m), m)
    
    phi = totient(m) #or lambda(m) Carmichael function
    return (pow(a, phi, m) * pow(a, tower(a, b-1, phi), m)) % m
  
##############
from math import log2
from math import floor
def phi(n) :
    result = n
    p = 2
    while p * p<= n :
        if n % p == 0 :
            while n % p == 0 :
                n = n // p
            result = result * (1.0 - (1.0 / float(p)))
        p = p + 1
    if n > 1 :
        result = result * (1.0 - (1.0 / float(n)))
    return int(result)

def tower(base, h, m):
    if m==1: return 0
    if base==1 or h==0: return 1 
    if h==1: return base % m
    if h==2 :return pow(base,base,m)

    t=phi(m)
    mi=floor(log2(m))
    k=pow(base,t,m)
    exp=tow(base,h-1,mi)
    if exp==-1:
        exp=tower(base,h-1,t)
        res=pow(base,exp,m)*k%m
    else:
        res=pow(base,exp,m)
    return res
    
def tow(base, h, mi):
    if base ==1 or h==0: return 1
    if h==1: return base
    if base>mi:return -1
    exp=tow(base,h-1,mi)
    if exp>mi or exp==-1:
        return -1
    return pow(base,exp)
  
###################
from math import log2

def powmod(b, h, m):
    '''Return b**h mod m. Time complexity is O(log(h)).'''
    if h == 0:
        return 1 % m
    x = powmod(b, h//2, m)
    x = (x * x) % m
    if h % 2 != 0:
        x = (x * b) % m
    return x

def totient(n):
    '''Return Euler's totient function in O(sqrt(n)).'''
    w = 0
    phi = 1
    while n % 2 == 0: # Factor out prime p = 2 and count its multiplicity.
        n /= 2
        w += 1
    if w != 0: # If p = 2 is a prime factor of n, multiply phi by p**(w-1)*(p-1). 
        phi *= 2**(w-1)
        w = 0
    p = 3
    while p*p <= n: # Look for prime factors up to sqrt(n).
        while n % p == 0: # Factor out prime p and count its multiplicity.
            n /= p
            w += 1
        if w != 0: # If p is a prime factor of n, multiply phi by p**(w-1)*(p-1).
            phi *= p**(w-1)*(p-1)
            w = 0
        p += 2
    if n > 1: # If n > 1 there is a prime factor with multiplicity w = 1 left.
        phi *= n - 1
    return int(phi)

def tower(base, h, m):
    '''Return base ** base ** ... ** base, h times, modulo m. 
    Recursively computes base ** (tower(base, h- 1, phi(m)) + phi(m)) mod m
    if (base ** base ... ** base, h - 1 times) >= log2(n), else tower(base, h, m) 
    is computed directly. Here phi(m) is Euler's totient function.'''
    if h == 0: # Base case.
        return 1 % m
    if m == 1: # Base case.
        return 0
    tmp = base
    for i in range(h-1):
        if tmp >= log2(m): # If tmp is ever >= log2(m), apply recursion relation.
            phi = totient(m) # Get Euler's totient function of m.
            return powmod(base, tower(base, h-1, phi) + phi, m)
        tmp = base ** tmp
    return tmp % m
  
###################
import math
import random

totients = {}
def totient(n):
    if n == 0: return 1

    try: return totients[n]
    except KeyError: pass

    tot = 1
    for p, exp in factorization(n).items():
        tot *= (p - 1)  *  p ** (exp - 1)

    totients[n] = tot
    return tot

def factorization(n):
    factors = {}
    for p1 in primefactors(n):
        try:
            factors[p1] += 1
        except KeyError:
            factors[p1] = 1
    return factors

def gcd(a, b):
    if a == b: return a
    while b > 0: a, b = b, a % b
    return a

def lcm(a, b):
    return abs((a // gcd(a, b)) * b)


def primesbelow(N):
    # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    #""" Input N>=6, Returns a list of primes, 2 <= p < N """
    correction = N % 6 > 1
    N = {0:N, 1:N-1, 2:N+4, 3:N+3, 4:N+2, 5:N+1}[N%6]
    sieve = [True] * (N // 3)
    sieve[0] = False
    for i in range(int(N ** .5) // 3 + 1):
        if sieve[i]:
            k = (3 * i + 1) | 1
            sieve[k*k // 3::2*k] = [False] * ((N//6 - (k*k)//6 - 1)//k + 1)
            sieve[(k*k + 4*k - 2*k*(i%2)) // 3::2*k] = [False] * ((N // 6 - (k*k + 4*k - 2*k*(i%2))//6 - 1) // k + 1)
    return [2, 3] + [(3 * i + 1) | 1 for i in range(1, N//3 - correction) if sieve[i]]

smallprimeset = set(primesbelow(100000))
_smallprimeset = 100000

smallprimes = (2,) + tuple(n for n in iter(range(3,1000,2)) if n in smallprimeset)


def primefactors(n, sort=False):
    factors = []

    limit = int(n ** .5) + 1
    for checker in smallprimes:
        if checker > limit: break
        while n % checker == 0:
            factors.append(checker)
            n //= checker


    if n < 2: return factors
    else : 
        factors.extend(bigfactors(n,sort))
        return factors

def bigfactors(n, sort = False):
    factors = []
    while n > 1:
        if isprime(n):
            factors.append(n)
            break
        factor = pollard_brent(n) 
        factors.extend(bigfactors(factor,sort)) # recurse to factor the not necessarily prime factor returned by pollard-brent
        n //= factor

    if sort: factors.sort()    
    return factors

def pollard_brent(n):
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3

    y, c, m = random.randint(1, n-1), random.randint(1, n-1), random.randint(1, n-1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = (pow(y, 2, n) + c) % n

        k = 0
        while k < r and g==1:
            ys = y
            for i in range(min(m, r-k)):
                y = (pow(y, 2, n) + c) % n
                q = q * abs(x-y) % n
            g = gcd(q, n)
            k += m
        r *= 2
    if g == n:
        while True:
            ys = (pow(ys, 2, n) + c) % n
            g = gcd(abs(x - ys), n)
            if g > 1:
                break

    return g

def isprime(n, precision=7):
    # http://en.wikipedia.org/wiki/Miller-Rabin_primality_test#Algorithm_and_running_time
    if n < 1:
        raise ValueError("Out of bounds, first argument must be > 0")
    elif n <= 3:
        return n >= 2
    elif n % 2 == 0:
        return False
    elif n < _smallprimeset:
        return n in smallprimeset


    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for repeat in range(precision):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1: continue

        for r in range(s - 1):
            x = pow(x, 2, n)
            if x == 1: return False
            if x == n - 1: break
        else: return False

    return True

def memoize(a_decorer):
    """
    Un décorateur pour conserver les résultats
    précédents et éviter de les recalculer
    """
    def decoree(*args):
        # si on a déjà calculé le résultat
        # on le renvoie
        try:
            return decoree.cache[args]
        # si les arguments ne sont pas hashables,
        # par exemple s'ils contiennent une liste
        # on ne peut pas cacher et on reçoit TypeError
        except TypeError:
            return a_decorer(*args)
        # les arguments sont hashables mais on
        # n'a pas encore calculé cette valeur
        except KeyError:
            # on fait vraiment le calcul
            result = a_decorer(*args)
            # on le range dans le cache
            decoree.cache[args] = result
            # on le retourne
            return result
    # on initialise l'attribut 'cache'
    decoree.cache = {}
    return decoree

@memoize        
def tower(a, b, m):
    #base cases
    if m == 1:
        return 0
    if a == 1 or b == 0:
        return 1
    if b == 1:
        return a % m    
    if a == m:
        return 0

        

    towerBiggerThanLog2m = checkTowerBiggerThanLogM(a, b-1, math.log(m, 2))     
    phiM = totient(m) #or lambda(m) 
    if towerBiggerThanLog2m: 
        

        factorA = pow(a, phiM, m)
        factorB = pow(a, tower(a, b-1, phiM), m)
        return (factorA*factorB) % m
        
    else:
        return pow(a, tower(a, b-1, phiM), m)   

    #https://stackoverflow.com/questions/21367824/how-to-evalute-an-exponential-tower-modulo-a-prime  

    pass
@memoize
def checkTowerBiggerThanLogM(a, b, m):
    if a > round(m):
        return True    
    if b == 1 or m <= 1:
        return a > round(m)    

    return checkTowerBiggerThanLogM(a, b-1, math.log(m,a))  
  
####################################################
import math
from functools import reduce

def factorPrime(n):
    factor=[]
    while n>0:
        for i in range(2,int(math.sqrt(n))+1):
            if n%i==0:
                n//=i
                factor.append(i)
                break
        else:
            factor.append(n)
            break
    return factor

def euler_phi(n):
    primes= set(factorPrime(n))
    return reduce(lambda x,y: x//y*(y-1), primes, n)

def towerLargerThan(base, h, m):
    """
    return base**base**...**base>= m
    """
    if m<=0:
        return True
    if h==1:
        return base>=m
    return towerLargerThan(base,h-1, math.log(m)/math.log(base))

def tower(base, h, m):
    """Return base ** base ** ... ** base, where the height is h, modulo m. """
    print(base, h, m)
    if m == 1:
        return 0
    if base == 1 or h==0:
        return 1
    if h==1:
        return base % m
    phi = euler_phi(m)
    power = tower(base, h-1, phi)
    return pow(base, power+ phi, m) if towerLargerThan(base, h-1, phi) else pow(base, power, m)
  
######################
from math import log2, log10

def phi(n):
    n_ = n
    r = n
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            while n % i == 0:
                n //= i
            r -= r // i
    if n > 1: r -= r // n
    return r

def mpow(x, n, m):
    if n == 0: return 1 % m
    t = mpow(x, n//2, m)
    t = t * t % m
    if n % 2 == 1:
        t = t * x % m
    return t

def f(x, n, m):
    if m == 1: return 0
    if n == 0: return 1
    if x == 0: return 0
    if x == 1: return 1
    if n == 1: return x % m
    if n == 2: return mpow(x, x, m)
    k = n
    ans = 1
    while k > 0:
        if ans*log10(x) > 5:
            return mpow(x, phi(m) + f(x, n-1, phi(m)), m)
        ans = x**ans
        k -= 1
    return ans % m

def tower(x, n, m):
    r = f(x, n, m)
    return r

#########################
from math import log

def phi(n):
    r,i=n,2
    while i*i<=n:
        if n%i==0:
            r=r//i*(i-1)
            while n%i==0: n//=i
        i+=1
    if n>1: r=r//n*(n-1)
    return r

def _tower(base,h,m):
    if h<2 or m==1: return pow(base,h,m)
    p=phi(m)
    return pow(base,p+tower(base,h-1,p),m)

def tower(base,h,m):
    res = 1
    for _ in range(h):
        if res*log(base)>log(m): return _tower(base,h,m)
        res = base**res
    return res%m
