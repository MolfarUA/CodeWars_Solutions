try:
    range = xrange
except: pass

test.expect(height(7,8) != -666)

test.describe('Example tests')
test.it("should work for some basic tests")
test.assert_equals(height(1,51),51)
test.assert_equals(height(2,1),1)
test.assert_equals(height(4,17),3213)
test.assert_equals(height(16,19),524096)
test.assert_equals(height(23,19),524287)
print('<COMPLETEDIN::>')
test.it("should work for some advanced tests")
test.assert_equals(height(13,550),621773656)
test.assert_equals(height(531,550),424414512)
print('<COMPLETEDIN::>')
test.it("should work for some serious tests :)")
test.assert_equals(height(10 ** 4, 10 ** 5),132362171)
test.assert_equals(height(8*10 ** 4, 10 ** 5),805097588)
test.assert_equals(height(3000,2 ** 200),141903106)
test.assert_equals(height(8*10 ** 4, 4*10 **4 ),616494770)
test.assert_equals(height(4*10 ** 4, 8*10 ** 4),303227698)
print('<COMPLETEDIN::>')
print('<COMPLETEDIN::>')

def sol_sum_mod_bin(n,k,p):
    MOD = 998244353
    s=0; nm=1; dm=1; i=0
    while i<k:
        nn = (nm*(n-i))%p; nd = (dm*(i+1))%p
        s = (s+nn*pow(nd,MOD-2,MOD))%p; nm=nn; dm=nd; i+=1
    return s

def sol7894(n, m):
    MOD = 998244353
    if n>m: return (pow(2,m,MOD) - 1) % MOD
    elif n>m//2: return ((MOD-2) + pow(2,m,MOD) - sol7894(m-n-1,m) ) % MOD
    else: return sol_sum_mod_bin(m%MOD, n, MOD)


from random import randint

test.describe('Random tests')
rand_data = [(0, 10 ** 4, 10 ** 5), (8 * 10 ** 4, 8 * 10 ** 4, 10 ** 5), (0, 3000, 2 ** 200)]
for _ in range(50):
    for s, a, b in rand_data:
        n, m = randint(s,a), randint(s,b)
        test.assert_equals(height(n,m), sol7894(n,m))
print('<COMPLETEDIN::>')
