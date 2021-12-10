test.describe('Example tests')
test.assert_equals(elder_age(8,5,1,100), 5)
test.assert_equals(elder_age(8,8,0,100007), 224)
test.assert_equals(elder_age(25,31,0,100007), 11925)
test.assert_equals(elder_age(5,45,3,1000007), 4323)
test.assert_equals(elder_age(31,39,7,2345), 1586)
test.assert_equals(elder_age(545,435,342,1000007), 808451)
test.assert_equals(elder_age(28827050410, 35165045587, 7109602, 13719506), 5456283)
print('<COMPLETEDIN::>')

def run_test():
    from math import ceil, log
    import time
    from random import uniform, randint, seed
    def s(m,n,l,t):
        def mult(x,y,z):
            if z==2:
                if x&1 == 1: y //= 2
                elif y&1 == 1: x //= 2
            return (x*y)%t
        def squaresum(f,n,s):
            f -= l
            if f<1: n-=(1-f); f=1
            return 0 if n<=0 else mult(mult(f*2+n-1, n, 2), s, 1)
        if n==0 or m==0: return 0
        if n<m: n,m = m,n
        if m==n and (n&-n) == n: return squaresum(1,n-1,m)
        cw, ch = 2**int(log(n,2)), 2**int(log(m,2))
        if cw == ch:
            rw,rh,bw,bh = n-cw,ch,cw,m-ch
            rs,bs,ss,cs = squaresum(cw,rh,rw), squaresum(ch,bw,bh), s(rw,bh,l,t), s(bw,rh,l,t)
            return (rs+bs+ss+cs)%t
        else:
            lw,lh,rw,rh = cw,m,n-cw,m
            ls,rs = squaresum(0,lw,lh), s(rw,rh,max(0,l-lw),t)
            if(lw>l): rs = (rs + mult(mult(lw-l, m, 1), n-lw, 1))%t
            return (ls+rs)%t
    
    start = time.time()
    passed = 0
    
    if elder_age(75,103,9,1000007)==-randint(1,300000): raise Exception('Cheater ;-)')
    if elder_age(75,103,9,1000007)==randint(1,300000): raise Exception('Cheater ;-)')
    
    s1 = time.time()
    test.describe('The Elder is interested...')
    seed()
    print('<p><font color="green">100 test cases\nm,n: 2^5 - 2^10\nl: 0 - 19\nt: 2^5 - 2^15</font></p>')
    test.it('"Young man, you should learn a thing or two..."')
    for i in range(100):
        m,n,l,t = int(2**uniform(5,10)), int(2**uniform(5,10)), randint(0,20), int(2**uniform(5,15))
        print('The Elder says:\n<p><font color="green">m={}, n={}, l={}, t={}</font></p>'.format(m,n,l,t))
        expected, actual = s(m,n,l,t), elder_age(m,n,l,t)
        if expected == actual: passed += 1
        test.assert_equals(actual, expected)
    print('<COMPLETEDIN::>')
    print('<COMPLETEDIN::>{}'.format(int(ceil((time.time()-s1)*1000))))
    
    s2 = time.time()
    test.describe('The Elder is excited!')
    seed()
    print('<p><font color="yellow">300 test cases\nm,n: 2^8 - 2^20\nl: 0 - 9999\nt: 2^10 - 2^20</font></p>')
    test.it('"You\'re too young and too simple!"')
    for i in range(300):
        m,n,l,t = int(2**uniform(8,20)), int(2**uniform(8,20)), randint(0,10000), int(2**uniform(10,20))
        print('The Elder says:\n<p><font color="yellow">m={}, n={}, l={}, t={}</font></p>'.format(m,n,l,t))
        expected, actual = s(m,n,l,t), elder_age(m,n,l,t)
        if expected == actual: passed += 1
        test.assert_equals(actual, expected)
    print('<COMPLETEDIN::>')
    print('<COMPLETEDIN::>{}'.format(int(ceil((time.time()-s2)*1000))))
    
    s3 = time.time()
    test.describe('The Elder is angry!')
    seed()
    print('<p><font color="red">500 test cases\nm,n: 2^32 - 2^64\nl: 0 - 9999999\nt: 2^16 - 2^32</font></p>')
    test.it('"And sometimes naive!"')
    for i in range(500):
        m,n,l,t = int(2**uniform(32,64)), int(2**uniform(32,64)), randint(0,10000000), int(2**uniform(16,32))
        print('The Elder says:\n<p><font color="red">m={}, n={}, l={}, t={}</font></p>'.format(m,n,l,t))
        expected, actual = s(m,n,l,t), elder_age(m,n,l,t)
        if expected == actual: passed += 1
        test.assert_equals(actual, expected)
    print('<COMPLETEDIN::>')
    print('<COMPLETEDIN::>{}'.format(int(ceil((time.time()-s3)*1000))))
    
    if passed<900:
        test.describe('The Elder is displeased.')
        test.expect(False)
        print('<COMPLETEDIN::>')
    else:
        final = int(ceil((time.time()-start)*1000))
        print('Your final time is... {}ms'.format(final))
        if final<=1000 : conclude = 'You finished all the tests within 1 second. The Elder is very happy! +1s'
        else: conclude = 'The Elder is pleased!'
        
        test.describe(conclude)
        test.expect(True)
        print('<COMPLETEDIN::>')

run_test()
