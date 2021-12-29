test.describe("Mix")
test.it("Basic Tests")
test.assert_equals(mix("Are they here", "yes, they are here"), "2:eeeee/2:yy/=:hh/=:rr")
test.assert_equals(mix("Sadus:cpms>orqn3zecwGvnznSgacs","MynwdKizfd$lvse+gnbaGydxyXzayp"), '2:yyyy/1:ccc/1:nnn/1:sss/2:ddd/=:aa/=:zz')
test.assert_equals(mix("looping is fun but dangerous", "less dangerous than coding"), "1:ooo/1:uuu/2:sss/=:nnn/1:ii/2:aa/2:dd/2:ee/=:gg")
test.assert_equals(mix(" In many languages", " there's a pair of functions"), "1:aaa/1:nnn/1:gg/2:ee/2:ff/2:ii/2:oo/2:rr/2:ss/2:tt")
test.assert_equals(mix("Lords of the Fallen", "gamekult"), "1:ee/1:ll/1:oo")
test.assert_equals(mix("codewars", "codewars"), "")
test.assert_equals(mix("A generation must confront the looming ", "codewarrs"), "1:nnnnn/1:ooooo/1:tttt/1:eee/1:gg/1:ii/1:mm/=:rr")

from functools import cmp_to_key
from random import randint

def compSol(a, b):
    cp = len(b) - len(a);
    if (cp == 0):
        if (a < b): 
            r = -1
        else: 
            r = 1
    else:
        r = cp;
    return r
    
def mixSol(s1, s2):
    alpha_s1, alpha_s2 = [0] * 26, [0] * 26
    for c in s1:
        if 97 <= ord(c) <= 122:
            alpha_s1[ord(c) - 97] += 1
    for c in s2:
        if 97 <= ord(c) <= 122:
            alpha_s2[ord(c) - 97] += 1
    res = ""
    i = 0
    while i < 26:
        sm = max([alpha_s1[i], alpha_s2[i]])
        if (sm > 1):
            if (sm > alpha_s1[i]):
                res += str(2) + ":"
                res += (chr(i + 97))*sm
                res += "/"
            elif (sm > alpha_s2[i]):
                res += str(1) + ":"
                res += (chr(i + 97))*sm
                res += "/"
            elif (alpha_s1[i] == alpha_s2[i]):
                res += "=:"
                res += (chr(i + 97))*sm
                res += "/"
        i += 1
    l = res[:-1].split('/')
    a = sorted(l, key = cmp_to_key(compSol))
    return '/'.join(a)

def do_ex():
    i = 0
    res = ""
    while (i < 30):
        if (i % 5 == 0):
            n = randint(35, 90) 
        else:
            n = randint(97, 122)
        res += chr(n)
        i += 1
    return res

def randomTests():
    print("100 random tests ****************** ")
    for _ in range(0, 100):
        s1 = do_ex()
        s2 = do_ex()
        test.assert_equals(mix(s1, s2), mixSol(s1, s2))
        
randomTests()
