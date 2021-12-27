test.assert_equals(isinstance(solution,str),True,'your solution is not a string')

import re
from random import random, randint
rgx = re.compile(solution)
a = randint(0,1000); b=randint(0,1000)
while b==a: b=randint(0,1000)

test.describe('full on random test')
test.it('1000 random tests')
for i in range(0,1000):
    if i==a: 
        print('Testing for: 0')
        test.assert_equals(bool(rgx.match('0')),True)
    elif i==b:
        print('Testing for: empty string')
        test.assert_equals(bool(rgx.match('')),False)
    else:
        num = int(2**(random()*32))
        print('Testing for: '+str(num))
        test.assert_equals(bool(rgx.match(bin(num)[2:])),num%7 == 0)
