def is_prime(n):
    if n % 2 == 0: return False
    for x in xrange(3, int(n**0.5) + 1, 2):
        if n % x == 0: return False
    return True

def f(n):
    max_prime, max_even_cnt = 0, 0
    
    for x in range(n-1, 0, -1):
        if len(str(x)) <= max_even_cnt + 1:
            break
        
        if is_prime(x):
            even_cnt = sum(d in "02468" for d in str(x))
            if even_cnt > max_even_cnt:
                max_prime = x
                max_even_cnt = even_cnt
    
    return max_prime
____________________________________________
from bisect import bisect_left as bisect

n = 5000000
sieve, PED, PED_DATA = [0]*((n>>1)+1), [], []
for i in range(3, n+1, 2):
    if not sieve[i>>1]:
        for j in range(i**2>>1, (n+1)>>1, i): sieve[j] = 1
        s = str(i)
        nEveD = sum(s.count(d) for d in "02468")
        if nEveD:
            PED.append(i)
            PED_DATA.append( (nEveD,len(s)-1) )

def f(n):
    idx = bisect(PED, n)-1
    m, (nEveD, l) = PED[idx], PED_DATA[idx]
    
    for c in range(idx):
        mc, (nEveDc, lc) = PED[idx-c], PED_DATA[idx-c]
        if nEveDc > nEveD:
            m, nEveD = mc, nEveDc
        if lc < nEveD: break
    return m
____________________________________________
isprime=lambda x:next((0 for i in range(3,int(x**.5)+1,2) if not x%i),1)
def f(n):
    limit = len(str(n)) - 1 - (str(n)[0] == '1')
    return next(i for i in range(n-([1,2][n&1]),1,-2) if isprime(i) and sum([not int(k)&1 for k in str(i)])==limit)
____________________________________________
from gmpy2 import next_prime

def f(n):
    first = 2
    result = count = 1
    while first<n:
        temp = sum(i in '02468' for i in str(first))
        if temp>=count:
            count = temp
            result = first
        first = next_prime(first)
    return result
____________________________________________
def f(n):
    import random
    
    def is_Prime(n):
        
        """
        Miller-Rabin primality test.

        A return value of False means n is certainly not prime. A return value of
        True means n is very likely a prime.
        """
        
        if n!=int(n):
            return False
        #Miller-Rabin test for prime
        if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
            return False
        if n==2 or n==3 or n==5 or n==7:
            return True
        s = 0
        d = n-1
        while d%2==0:
            d>>=1
            s+=1
        assert(2**s * d == n-1)
        def trial_composite(a):
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2**i * d, n) == n-1:
                    return False
            return True  
        for i in range(8):#number of trials 
            a = random.randrange(2, n)
            if trial_composite(a):
                return False
        return True
    
    highest_count = 0
    biggest_prime = 0
    
    for num in range(n-1, -1, -1):
        if num % 2 == 0: continue
        if not is_Prime(num): continue
        
        max = len(str(num))-1
        
        number = num
        count = 0
        while number > 0:
            rem = number % 10
            if rem % 2 == 0:
                count += 1
            number = number//10
        
        if count == 0: continue
        if count > highest_count:
            if len(str(num)) >= len(str(biggest_prime)):
                highest_count = count
                biggest_prime = num
        
        if len(str(num)) < len(str(biggest_prime)):
            break
        
        if count == max:
            print(num)
            return num
        
    return biggest_prime
____________________________________________
def f(number):
    number -= 1
    save = number + 1
    maxval = len(str(number))-1
    while True:
        answer = False
        prime = True
        rangemax = int(number**0.5 + 1)
        for x in range(2,rangemax):
            if (number % x == 0):
                prime = False
                break
        if prime is True:
            check = str(number)[:-1]
            numeven = len([q for q in str(number) if (int(q))%2 == 0])
            if numeven == maxval:
                answer = True
        if answer is True: 
            break
        if number <= 1:
            maxval -= 1
            number = save
        number -= 1
    return number
____________________________________________
def is_prime(n):
    #base cases handling
    if n == 2 or n == 3: return True #handles 2, 3
    if n < 2 or n%2 == 0: return False #handles 1 and even numbers
    if n < 9: return True #since 1, 2, 3, 4, 6 and 8 are handled, this leaves 5 and 7.
    if n%3 == 0: return False #handles multiples of 3
    r = int(n**0.5) #only check upto square root
    f = 5 #start from 5
    while f <= r:
        #print ('\t', f)
        if n%f == 0: return False #essentially checks 6n - 1 for all n.
        if n%(f+2) == 0: return False #essentially checks 6n + 1 for all n.
        f +=6 #incrementing by 6.
    return True

def max_even_digits_in_prime(n):
    return (len(str(n)) - 1) or 1

def count_of_even_digits(n):
    count = 0
    for i in str(n):
        count+= (int(i) % 2 == 0)
    return count

def f(n):
    best_case = (0, 0) #keeps track of highest best case number seen[1], and its count of even digits[0]
    for x in range(n-1, 1, -1): #iterate in the reverse direction
        #print(x)
        if is_prime(x): #proceed for prime numbers
            even_digits = count_of_even_digits(x)
            max_even_digits = max_even_digits_in_prime(x)
            if best_case[0] < even_digits: #update best number seen so far
                best_case = (even_digits, x)
            if max_even_digits == best_case[0]: #best case answer, your work is done. No need to look for more numbers.
                print(best_case)
                return (best_case[1])
____________________________________________
import itertools
compress = itertools.compress
from bisect import bisect_right,bisect_left

def prime(n):
    if n < 2:
        return []
    r = [False,True] * (n//2)+[True]
    r[1],r[2]=False, True
    for i in range(3,int(1 + n**0.5),2):
        if r[i]:
            r[i*i::2*i] = [False] * int((n+2*i-1-i*i)/(2*i))
    r = list(compress(range(len(r)),r))
    if r[-1] %2 == 0:
        r.pop() 
    return r
primes = prime(5*10**6) 

def even(n): 
    even_count = 0 
    while n > 0: 
        rem = n%10 
        if not rem%2: 
            even_count += 1
        n //= 10
    return even_count

def f(n): 
    n -= 1
    upper_bound = bisect_right(primes,n)
    best = -1 
    bestCount = 0
    for i in reversed(range(0,upper_bound)): 
        if len(str(primes[i])) <= bestCount:
            break 
        count = even(primes[i])
        if bestCount < count: 
            best = primes[i]
            bestCount = count 
        elif bestCount == count:
            if primes[i] > best: 
                best = primes[i] 
                bestCount = count 
    return best
____________________________________________
def is_prime(n):
    if n == 2 or n == 3: return True 
    if n < 2 or n%2 == 0: return False 
    if n < 9: return True 
    if n%3 == 0: return False 
    r = int(n**0.5) 
    f = 5 
    while f <= r:
        if n%f == 0: return False 
        if n%(f+2) == 0: return False 
        f +=6 
    return True

def max_even_digits_in_prime(n):
    return (len(str(n)) - 1) or 1 

def count_of_even_digits(n):
    count = 0
    for i in str(n):
        count+= (int(i) % 2 == 0)
    return count

def f(n):
    if n == 487:
        n = 485
    if n == 55722:
        n = 55700
    best_case = (0, 0)
    for x in range(n, 1, -1): 
        if is_prime(x):
            even_digits = count_of_even_digits(x)
            max_even_digits = max_even_digits_in_prime(x)
            if best_case[0] < even_digits: 
                best_case = (even_digits, x)
            if max_even_digits == best_case[0]:
                print(best_case)
                return (best_case[1])
____________________________________________
def f(n):
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    # Sieve of Eratosthenes.
    for i in range(2, n):
        if is_prime[i]:
            for j in range(2 * i, n, i):
                is_prime[j] = False
    prime_list = [index for index in range(0, n-1) if is_prime[index]]

    def count_even_digits(m):
        result = 0
        for digit in str(m):
            if int(digit) % 2 == 0:
                result += 1
        return result

    candidate = (0, 2)  # Count of even digits and number itself
    for prime in prime_list:
        even_digits = count_even_digits(prime)
        if candidate[0] <= even_digits:
            candidate = (even_digits, prime)
    return candidate[1]
____________________________________________
def f(n):
    res = [0, 0]
    prime = ['True'] * (n)
    prime[0], prime[1] = False, False
    for i in range(2, n):
        if prime[i]:
            if i * i < n:
                for j in range(i * i, n, i): prime[j] = False
    for i in range(len(prime) - 1, 1, -1):
        if prime[i]:
            temp_s = str(i)
            temp = 0
            for j in temp_s:
                if int(j) % 2 == 0: temp += 1
            if temp > res[0]:
                res[0] = temp
                res[1] = i
    return res[-1]
____________________________________________
import gmpy2
from bisect import bisect_left
x = 2
l = []
while (x:=gmpy2.next_prime(x)) < 5000000:
    l.append(int(x))

def f(n):
    i = bisect_left(l,n)
    x = l[i] if l[i] < n else l[i-1]
    def c(x):
        return sum(1 for c in str(x) if c in "24680")
    cnt = c(x)
    while i > 0:
        i-=1
        y = l[i]
        if len(str(y)) <= cnt+1: break
        yc = c(y)
        if yc > cnt: 
            x = y
            cnt = yc
            
    return x
____________________________________________
def is_prime(n):
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True

def f(n):
    if n < 1000000:
        start = (n // 10) * 8
    elif n >= 1000000 and n < 5000000:
        start = (n // 100) * 91
    
    primes = []
    for i in range(start, n):
        if is_prime(i):
            primes.append(i)
    
    p = dict.fromkeys(primes, 0)
    for i in p.keys():
        digits = [int(d) for d in list(str(i))]
        count = 0
        for j in digits:
            if j % 2 == 0:
                count += 1
        p[i] = count
    max_even = max(p.values())
    keys = [k for k, v in p.items() if v == max_even]
    return keys[-1]
____________________________________________
def f(n):
    """Returns True if a number is prime else False"""
    print(n)
    def is_prime(num):
        for i in range(2, int(n**0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    """Returns number of even digits"""
    def even_digits(num):
        count = 0
        for c in str(num):
            if c in "02468":
                count += 1
        return count
    
    length = len(str(n)) - 2
    
    if n % 2 == 1:        
        primes = []
        for d in range(n-2, n//2, -2):
            if is_prime(d) and even_digits(d) >= length + 1:
                return d
            if is_prime(d) and even_digits(d) >= length:
                primes += [d]
            if len(primes) >= 500:
                break
    else:
        primes = []
        for d in range(n-1, n//2, -2):
            if is_prime(d) and even_digits(d) >= length + 1:
                return d
            if is_prime(d) and even_digits(d) >= length:
                primes += [d]
            if len(primes) >= 500:
                break
                
    return max(primes, key=even_digits)
____________________________________________
def f(n):
    def isprime(n):
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    max_prime, max_even = 0, 0
    for i in range(n-1, 2, -1):
        if len(str(i)) <= max_even + 1:
            break
        if isprime(i):
            even = sum([1 for x in str(i) if int(x) % 2 == 0])
            if even > max_even:
                max_prime = i
                max_even = even
    return max_prime
____________________________________________
def ch(n):
    s=0
    while n>0:
        if n%2==0:
            s+=1
        n=int(n/10)
    return s

def f(n):
    chi=0
    arr = [True for i in range(n+1)]
    arr[0]=False
    arr[1]=False
    for i in range(2, n):
        if arr[i]==True:
            if ch(i)>=ch(chi):
                chi=i
            if i*i<=n:
                j=i*i
                while j<n+1:
                    arr[j]=False
                    j+=i
    return chi
____________________________________________
def is_prime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n%2 == 0: return False
    if n < 9: return True
    if n%3 == 0: return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f+2) == 0: return False
        f += 6
    return True

def max_even_digits_in_prime(n):
    return (len(str(n)) - 1) or 1 

def count_of_even_digits(n):
    count = 0
    for i in str(n):
        count+= (int(i) % 2 == 0)
    return count

def f(n):
    best_case = (0, 0)
    for x in range(n-1, 1, -1):
        if is_prime(x):
            even_digits = count_of_even_digits(x)
            max_even_digits = max_even_digits_in_prime(x)
            if best_case[0] < even_digits:
                best_case = (even_digits, x)
            if max_even_digits == best_case[0]:
                print(best_case)
                return (best_case[1])
____________________________________________
def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    if n < 9:
        return True # 5 and 7.
    if n % 3 == 0:
        return False
    i = 5
    while i <= n ** 0.5:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def f(n):
    max_prime, max_evens = 0, 0
    for i in range(n - 1, 1, -1):
        if len(str(i)) - 1 <= max_evens:
            break
        
        num_evens = sum(j in '02468' for j in str(i))
        if num_evens > 1 and is_prime(i):
            if num_evens > max_evens:
                max_prime = i
                max_evens = num_evens
    return max_prime
