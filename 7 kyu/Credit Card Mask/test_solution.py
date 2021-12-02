def solution(b):
    return '#'*(len(b)-4)+b[-4:]

def random(seed):
    ''' xor128 psuedo random number generator '''
    x = 123456789
    y = 362436069
    z = 521288629
    w = seed
    t = x ^ (x<<11) & 0xffffffff
    x = y
    y = z
    z = w
    w = w
    w = (w ^ (w >> 19) ^(t ^ (t >> 8))) & 0xffffffff
    return w

for x in range(0, 20):
    if x <= 4:
        s = str(x)*x
        r = maskify(s)
        test.describe("masking: {0}".format(s))
        test.it("{0}  matches  {1}".format(r,s))
        test.assert_equals(r, s)
        print("<COMPLETEDIN::>")
        print("<COMPLETEDIN::>")
    elif x >= 5 and x <=15:
        a = str(random(x*100))
        cc = str(int(a[-1])*'x'+str(a))
        s = solution(cc)
        r = maskify(cc)
        test.describe("masking: {0}".format(cc))
        test.it("{0}  matches  {1}".format(r, s))
        test.assert_equals(r, s)
        print("<COMPLETEDIN::>")
        print("<COMPLETEDIN::>")
    else:
        a = str(random(x*100))
        cc = str(int(a[-1]*2)*'x'+str(a))
        s = solution(cc)
        r = maskify(cc)
        test.describe("masking: {0}".format(cc))
        test.it("{0}  matches  {1}".format(r, s))
        test.assert_equals(r, s)
        print("<COMPLETEDIN::>")
        print("<COMPLETEDIN::>")
