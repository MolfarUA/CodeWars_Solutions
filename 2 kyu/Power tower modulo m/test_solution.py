# Not all solutions use `log`, so, as the test suite uses it, putting it here
from math import log

def _test_suite():

    test.describe('Basic Tests')
    
    test.it('Corner cases')
    test.assert_equals(tower(729, 0, 1), 0)
    test.assert_equals(tower(729, 0, 2), 1)
    test.assert_equals(tower(1, 897, 8934279), 1)
    
    test.it('Small values')
    test.assert_equals(tower(3, 3, 25), pow(3, 27, 25))
    test.assert_equals(tower(2, 2, 1000), 4)
    test.assert_equals(tower(2, 3, 100000), 16)
    test.assert_equals(tower(2, 4, 100000000), 65536)
    test.assert_equals(tower(4, 2, 10000000), 256)
    test.assert_equals(tower(4, 3, 10), 6)
    test.assert_equals(tower(7, 1, 5), 2)
    test.assert_equals(tower(34, 2, 40), pow(34, 34, 40))
    test.assert_equals(tower(2, 5, 65519), 68)
    test.assert_equals(tower(2, 4, 131072), 65536)
    
    test.it('Cannot replace base with base % m')
    test.expect(tower(28, 3, 25) != tower(28 % 25, 3, 25))
    
    test.it('Cannot replace the exponent with exponent % m')
    test.expect(tower(13, 3, 31) != pow(13, tower(13, 2, 31), 31))
    test.it('However, there are cycles in the exponent...')
    test.assert_equals(tower(13, 3, 31), pow(13, tower(13, 2, 30), 31))
    test.assert_equals(tower(13, 3, 31), pow(13, 30 + tower(13, 2, 30), 31))
    m_974 = 1001
    test.it('Pushing the limit of "small"')
    t_3_3 = 3 ** 3 ** 3
    t_3_4 = pow(3, t_3_3, m_974)
    test.assert_equals(tower(3, 4, m_974), t_3_4)
    
    test.it('Pushing it even further...')
    t_2_4 = pow(2, 2 ** 2 ** 2)
    test.assert_equals(t_2_4, 65536)
    test.it('Replace exponent with..?!')
    t_2_5 = pow(2, t_2_4, 720)
    t_2_6 = pow(2, 720 + t_2_5, m_974)
    test.assert_equals(tower(2, 6, m_974), t_2_6)
    
    test.describe('Random tests')
    
    from random import randrange
    from itertools import groupby

    def tower_9798979879(base, h, m):
        if m == 1: return 0
        if base == 1 or h == 0: return 1
        tot = totient(m)
        lim = log(tot) / log(base)
        exp = 1
        for i in range(h - 1):
            if exp >= lim: break
            exp = base ** exp
        else:
            return pow(base, exp, m)
    
        r = tower_9798979879(base, h - 1, tot)
        return pow(base, tot + r, m)
        
    def totient(n):
        res = n
        for p, _ in groupby(gen_prime_factors(n)):
            res = res // p * (p - 1)
        return res
        
        
    def gen_prime_factors(n):
        # Check 2 first
        while n & 1 == 0:
            yield 2
            n >>= 1
        # Check odd factors
        factor, factor_sqr = 3, 9
        while factor_sqr <= n:
            while n % factor == 0:
                yield factor
                n //= factor
            factor += 2
            factor_sqr += factor - 1 << 2
        if n > 1:
            yield n
    
    for _ in range(80):
        b = randrange(2, 10)
        h = randrange(10)
        m = randrange(1, 10)
        test.it('Test tower(%d, %d, %d)' % (b, h, m))
        test.assert_equals(tower(b, h, m), tower_9798979879(b, h, m)) 
    
    for _ in range(60):
        b = randrange(2, 10 ** 5)
        h = randrange(10 ** 5)
        m = randrange(1, 10 ** 3)
        test.it('Test tower(%d, %d, %d)' % (b, h, m))
        test.assert_equals(tower(b, h, m), tower_9798979879(b, h, m)) 
    
    for _ in range(40):
        b = randrange(2, 10 ** 20)
        h = randrange(10 ** 20)
        m = randrange(1, 10 ** 7)
        test.it('Test tower(%d, %d, %d)' % (b, h, m))
        test.assert_equals(tower(b, h, m), tower_9798979879(b, h, m)) 

_test_suite()
