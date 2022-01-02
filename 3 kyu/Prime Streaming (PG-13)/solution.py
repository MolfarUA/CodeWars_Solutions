import numpy as np

class PrimeSieve:
    def __init__(self, maximum):
        self.primes = [2, 3]
        #self.sieve = [0] * (maximum + 1)
        self.sieve = np.zeros(maximum + 1, dtype=np.int8)
        for p in self.primes:
            self.sieve[p*p::p] = 1
        
    def extend(self):
        p = self.primes[-1] + 2
        while self.sieve[p]: p += 2
        self.sieve[p*p::p] = 1
        self.primes.append(p)
        return p


class Primes:
    @staticmethod
    def stream():
        prime_sieve = PrimeSieve(2 * 10**7)
        yield from iter(prime_sieve.primes)
        yield from iter(prime_sieve.extend, 0)
        
___________________________________________________________
def sieve_for_primes_to(n):
    size = n//2
    sieve = [1]*size
    limit = int(n**0.5)
    for i in range(1,limit):
        if sieve[i]:
            val = 2*i+1
            tmp = ((size-1) - i)//val
            sieve[i+val::val] = [0]*tmp
    return [2] + [i*2+1 for i, v in enumerate(sieve) if v and i>0]

_primes = sieve_for_primes_to(50000000)

class Primes:

    @staticmethod
    def stream():
        global _primes
        primes = iter(_primes)
        while True:
            yield next(primes)
            
___________________________________________________________
from itertools import *

class Primes:
    

    def wsieve():       # wheel-sieve, by Will Ness.   ideone.com/trR9OI
        yield 11        # cf. ideone.com/WFv4f
        mults = {}      #     codereview.stackexchange.com/q/92365/9064
        ps = Primes.wsieve()   
        p = next(ps)       # 11
        psq = p*p          # 121
        D = dict( zip( accumulate( [0,       # where to start
                     2,4,2,4,6,2,6,4,2,4,6,6, 2,6,4,2,6,4,6,8,4,2,4,2,
                     4,8,6,4,6,2,4,6,2,6,6,4, 2,4,6,2,6,4,2,4,2,10,2,10] ),
                       count(0)))
        for c in accumulate( chain( [13], cycle( 
                    [  4,2,4,6,2,6,4,2,4,6,6, 2,6,4,2,6,4,6,8,4,2,4,2,
                     4,8,6,4,6,2,4,6,2,6,6,4, 2,4,6,2,6,4,2,4,2,10,2,10,2] ))):
            if c in mults:
                wheel = mults.pop(c)  
            elif c < psq:              
                yield c ; continue   
            else:          # (c==psq)   
                p2=p*2   ;   p6=p*6   ;  p10=p*10 # map (p*) (roll wh from p) =
                p4=p*4   ;   p8=p*8               #  = roll (wh*p) from p*p
                wheel = accumulate( chain( [p*p], islice( cycle( 
                              [p2,p4,p2,p4,p6,p2,p6,p4,p2,p4,p6,p6,
                               p2,p6,p4,p2,p6,p4,p6,p8,p4,p2,p4,p2,
                               p4,p8,p6,p4,p6,p2,p4,p6,p2,p6,p6,p4,
                               p2,p4,p6,p2,p6,p4,p2,p4,p2,p10,p2,p10] ),
                              D[ (p-11) % 210 ], None )))
                p = next(ps) ; psq = p*p ; next(wheel)   # p*p
            for m in wheel: 
                if not m in mults: 
                    break
            mults[m] = wheel
     
    @staticmethod
    def stream(): 
        yield from (2, 3, 5, 7)
        yield from Primes.wsieve()
___________________________________________________________
from itertools import count
class Primes:
    def stream():                      
        yield 2; yield 3; yield 5; yield 7;  
        sieve = {}                           
        ps = Primes.stream()               
        p = next(ps) and next(ps)           
        q = p*p                             
        for c in count(9,2):                
            if c in sieve:              
                s = sieve.pop(c)         
            elif c < q:  
                 yield c                 
                 continue              
            else:   # (c==q):           
                s=count(q+2*p,2*p)      
                p=next(ps)              
                q=p*p                   
            for m in s:                  
                if m not in sieve:      
                    break
            sieve[m] = s    
___________________________________________________________

N = 16000000
memo, x, y = list(range(3, N+1, 2)), 0, 3
root, half = N**0.5, len(memo)
while y <= root:
    if memo[x]:
        z = (y*y - 3) >> 1
        memo[z] = 0
        while z < half:
            memo[z] = 0
            z += y
    x, y = x+1, (x+2 << 1)+1
primes = [2] + [x for x in memo if x]

class Primes:
    @staticmethod
    def stream():
        yield from primes
___________________________________________________________
def SieveOfEratosthenes():
    primes = [True for _ in range(16_000_000)]
    i = 2
    while i * i <= 16_000_000:
        if primes[i] == True:
            for j in range(i*2, len(primes), i):
                primes[j] = False
        i += 1
    return [2] + [i for i in range(3, len(primes), 2) if primes[i]]

primes = SieveOfEratosthenes()

class Primes:
    @staticmethod
    def stream():
        yield from primes
___________________________________________________________
class Primes:
    @staticmethod
    def stream():
        return iter(prime)

N = 16000000
prime = [1]*N
def sieve():    
    is_prime = [False, True, False, True, False, False, False, True, False, True]*(int(N/10)+1)
    is_prime[0], is_prime[1], is_prime[2], is_prime[5] = False, False, True, True
    p = 2
    while (p * p <= N): 
        if (is_prime[p] == True): 
            for i in range(p * p, N+1, p): 
                is_prime[i] = False
        p += 1
    i, j = 2, 0
    while i < N:
        if is_prime[i] == True:
            prime[j] = i
            j += 1
        i += 1
sieve()
___________________________________________________________
def sieve(n):
        is_p = [1 for _ in range(n)]
        is_p[0] = 0
        is_p[1] = 0
        primes = []
        for num in range(2, n):
            if is_p[num]:
                for i in range(num * 2, n, num):
                    is_p[i] = 0
        return [i for i, is_prime in enumerate(is_p) if is_prime]

class Primes:
    crr_n = 16000000
    primes = sieve(crr_n)
    
    @classmethod
    def stream(cls):
        crr_step = 0
        while True:
            if crr_step < len(cls.primes):
                yield cls.primes[crr_step]
                crr_step += 1
            else:
                cls.crr_n = cls.crr_n * 2
                cls.primes = sieve(cls.crr_n)
___________________________________________________________
class Primes:
    
    @staticmethod
    def stream(n=15486671):
        sieve = [True] * n
        for i in range(3,int(n**0.5)+1,2):
            if sieve[i]:
                sieve[i*i::2*i]=[False]*((n-i*i-1)//(2*i)+1)
        return iter([2] + [i for i in range(3,n,2) if sieve[i]])
___________________________________________________________
class Primes:
    @staticmethod
    def stream():
        n = 2*10**7
        n, correction = n-n%6+6, 2-(n%6>1)
        sieve = [True] * (n//3)
        for i in range(1,int(n**0.5)//3+1):
            if sieve[i]:
                k=3*i+1|1
                sieve[      k*k//3      ::2*k] = [False] * ((n//6-k*k//6-1)//k+1)
                sieve[k*(k-2*(i&1)+4)//3::2*k] = [False] * ((n//6-k*(k-2*(i&1)+4)//6-1)//k+1)
        result = [[2,3] + [3*i+1|1 for i in range(1,n//3-correction) if sieve[i]]]      
        for i in result[0]:
            yield i
___________________________________________________________
import numpy as np

def nonZero(tab, last, l):
    k = last + 2
    while k < l:        
        if tab[k] == 0: return k
        k += 2    
    
class Primes:
    @staticmethod
    def stream():
        limit = 16000000
        sqlim = limit**0.5
        n, list_ = 3, np.ones(limit)
        yield 2
        list_[2**2::2] = 0
        while n <= sqlim:
            list_[n**2::n] = 0
            yield n            
            while list_[n + 2] == 0: n += 2    
            n += 2
        nz = (np.array(np.nonzero(list_[n:]))).tolist()
        for n_ in nz[0]:
            yield n + n_
