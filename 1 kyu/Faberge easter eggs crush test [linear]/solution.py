MOD = 998244353

inv = [0, 1]
for i in range(2, 80000 + 1):
        inv.append( (MOD - MOD // i) * inv[MOD % i] % MOD )

def height(n, m):
    ans, c = 0, 1
    m %= MOD
    for i in range(1, n + 1): 
        c = c * (m - i + 1) * inv[i] % MOD
        ans = (ans + c) % MOD
    return ans % MOD
  
################
def height(n, m, p=998244353):
    s, f = -(n > m), 1
    for i in range(min(n, m-n-1)):
        #f = f * (m - i) // (i + 1) % p
        f = f * (m - i) * pow(i + 1, p - 2, p) % p
        s += f
    return (pow(2, m, p) - s - 2) % p if m <= 2*n else s % p
  
###############
MOD = 998244353
add = lambda x,y: (x + y) % MOD
mul = lambda x,y: (x * y) % MOD

def value(x, y):
    res, a, b, c = 0, 0, 1, 1
    while a < y:
        a, b, c = a+1, mul(b, x-a), mul(c, a+1)
        res = add(res, mul(b, pow(c, MOD-2, MOD)))
    return res

def height(n, m):
    if n > m: return pow(2, m, MOD) - 1
    if 2*n > m: return (pow(2, m, MOD) - height(m-n-1, m) - 2) % MOD
    return value(m%MOD, n)
  
#################
MOD = 998244353
def height(n, m):
    """
    :param n: number of eggs
    :param m: number of tries
    :return: total number floors
    """
    floor = 1  # recurrence variable
    total_floors = 0  # sum variable
    inverse_arr = [1]  # array of inverses till n

    # calculate first floor here so that everything else is smoothed in a single for loop
    floor = (floor * (m - 0) * inverse_arr[0]) % MOD
    total_floors = total_floors + floor

    inverse_arr = [1]
    for i in range(1, n):
        # floor division doesnt allow us to use MOD so we need to do inverse multiplication instead
        inverse_index = MOD % (i+1) - 1
        inverse = MOD - MOD // (i+1) * inverse_arr[inverse_index] % MOD
        inverse_arr.append(inverse)

        # for n of eggs, we sum nth first elements of the mth row of Pascal's triangle
        floor = (floor*(m-i) * inverse) % MOD
        total_floors = total_floors + floor

    return total_floors % MOD
  
##################
MOD = 998244353

import functools

"""
observation 1: h(n, m) = h(n, m-1) + h(n-1, m-1) + 1
observation 2: h(n, m) = h(m, m) if n > m
observation 3: h(n, m) = h(n-1, m) + choose(m, n) where choose is the binomial coefficient 
observation 4: h(n, m) = SUM(i=0..n) choose(m, i)
"""

def extended_euclidean_algorithm(a: int, b: int):
    """ returns a tuple (x, y, d) so that 
        - x * a + y * b == d 
        = d is the greatest common divisor of a and b
        
        from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    """
    x0, x1, y0, y1 = 0, 1, 1, 0
    # invarant: x0 * a + y0 * b == b
    while a:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return x0, y0, b
    

def inverse(a, m):
    """ use the extended euclidean algorithm to compute the
        inverse of a modulo m
    """
    (x, y, d) =  extended_euclidean_algorithm(a, m)
    assert d == 1
    res = x % m
    assert a * res % m == 1
    return res
    
    
def inverses(n, m):
    """ return the multiplicative inverse mod m for all numbers 1 <= i <=n
        according to https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
    """
    a = {}
    b = {}
    a_inv = {}
    b_inv = {}
    i_list = list(range(1, n+1))
    a = {i: i for i in i_list}
    for i in sorted(i_list):
        b[i] = b.get(i-1, 1)*a[i] % m
    b_inv[n] = inverse(b[n], m)
    for i in range(n, 1, -1):
        a_inv[i] = b_inv[i] * b[i-1] % m
        b_inv[i-1] = b_inv[i] * a[i] % m
    a_inv[1] = b_inv[1]
    return a_inv
    

# all computation below is modulo MOD

# precompute the inverses modulo MOD
inverse_numbers = inverses(8 * 10 ** 4, MOD) 

@functools.lru_cache(2)
def choose(n, k):
    """ The binomial coefficient n choose k
        choose(n, k) = n ! / (k! * (n-k)!)
        
        Using a simple lru cahce here, because
        we know that we compute this function from k=1 going up
    """
    assert 0 <= k <= n
    if k == 0 or k == n:
        return 1
    return choose(n, k-1) * (n-k+1) * inverse_numbers[k] % MOD
      

def height(n,m):
    # return h(min(n, m), m)
    n = min(n, m)
    c = 1  # choose(m, 0)
    res = 0
    for i in range(1, min(n, m) + 1):
        # choose(m, i) = choose(m, i-1) * (m-i+1) * inverse(i)
        c = (c * (m-i+1)) % MOD * inverse_numbers[i] % MOD
        res = (res + c) % MOD
    return res
  
###############
M_VALUE = 998244353
yoyo_inv = [0, 1]
for yoyo_i in range(2, 80000 + 1):
        yoyo_inv.append( (M_VALUE - M_VALUE // yoyo_i) * yoyo_inv[M_VALUE % yoyo_i] % M_VALUE )
def height(m, n):  
    p, q = 0, 1
    n %= M_VALUE

    for i in range(1, m + 1): 
        q = q * (n - i + 1) * yoyo_inv[i] % M_VALUE
        p = (p + q) % M_VALUE
    return p % M_VALUE
  
####################
def sig(m, n, sum=0, num=1, den=1, MOD=998244353):
    for r in range(n+1): sum, num, den = sum + num * pow(den, MOD-2, MOD), (num * (m - r)) % MOD, (den * (r + 1)) % MOD 
    return sum % MOD

def height(n, m, MOD=998244353): return pow(2, m, MOD) - 1 if m <= n else sig(m % MOD, n) - 1 if n < m / 2 else (pow(2, m, MOD) - 1 - sig(m % MOD, m - n - 1)) % MOD


######################
import gmpy2 
MOD = gmpy2.mpz(998244353)

# Note that n << MOD while MOD is a prime,
# hence C(m, k) % MOD = (C(m, k-1) * acc * mul * div^-1) % MOD
#                     = C(m, k-1) % MOD * (acc * MOD) * (mul % MOD) * (div^(MOD-2) % MOD)


class P:
    def __init__(self, d, m):
        self.d, self.m = d, m 

def height(n,m):
    if not (n and m):
        return 0
    if n >= m:
        return (pow(2, m, MOD) - 1) % MOD 
        
    multiplier = gmpy2.mpz(m)
    acc = gmpy2.mpz(1)
    divisor = gmpy2.mpz(1)
    r = gmpy2.mpz(0)
    for _ in range(n):
        acc = (acc % MOD) * (multiplier % MOD) * pow(divisor, MOD-2, MOD)
        r = (r + acc) % MOD
        divisor += 1
        multiplier -= 1
        
    return r % MOD
###################################
MOD = 998244353

sfact = [0] * 3042
fact = [0] * 100042
inv = [0] * 100042

small = True

def fastexpo(n, power):
    ans = 1
    power %= (MOD-1)
    while(power):
        if(power & 1):
            ans = (ans * n) % MOD
        n = (n * n) % MOD
        power >>= 1
    return ans

def binomial(n, k):
    if k < 0 or n < k:
        return 0
    if not small:
        return (inv[k] * inv[n-k]) % MOD
    
    return (sfact[k] * inv[k]) % MOD

def init(n):
    fact[0] = 1
    for i in range(1, n+1):
        fact[i] = (fact[i-1] * i) % MOD
    inv[n] = fastexpo(fact[n], MOD-2)
    for i in range(n, -1, -1):
        inv[i-1] = (inv[i] * i) % MOD

def height(n, m):
    if n == 0 or m == 0:
        return 0
    if n >= m:
        return fastexpo(2, m) - 1
    
    global small
    if n > 3000:
        small = False
        init(m)
    else:
        small = True
        init(n)
        m %= MOD
        sfact[0] = 1
        for i in range(1, n+1):
            sfact[i] = (sfact[i-1] * (m+1-i)) % MOD

    sum = 0
    for i in range(1, n+1):
        if(small):
            sum = (sum + sfact[i] * inv[i]) % MOD
        else:
            sum = (sum + inv[i] * inv[m-i]) % MOD
    if not small:
        sum = (sum * fact[m]) % MOD
    return sum
