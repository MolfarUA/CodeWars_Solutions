test.describe("Basic tests")
test.it("Verifying that fib(0) == 0")
test.assert_equals(fib(0),0)

test.it("Verifying that fib(1) == 1")
test.assert_equals(fib(1),1)

test.it("Verifying that fib(2) == 1")
test.assert_equals(fib(2),1)

test.it("Verifying that fib(3) == 2")
test.assert_equals(fib(3),2)

test.it("Verifying that fib(4) == 3")
test.assert_equals(fib(4),3)

test.it("Verifying that fib(5) == 5")
test.assert_equals(fib(5),5)

def my_fib(n):
  if n < 0: return (-1)**(n % 2 + 1) * fib(-n)
  a,b,p,q = (1,0,0,1)
  while n != 0:
    if (n % 2) == 0:
      (p,q) = (p * p + q * q,
               (2 * p + q) * q)
      n /= 2
    else:
      (a,b) = ((b + a) * q + a * p,
               b * p + a * q)
      n -= 1
  return b

#randint = reload(__import__("random")).randint
#sqrt = reload(__import__("math")).sqrt
from random import randint
from math import sqrt

test.describe("Negative values")
test.it("Verifying that fib(-6) == -8")
test.assert_equals(fib(-6),-8)
test.it("Verifying that fib(-96) == -51680708854858323072")
test.assert_equals(fib(-96),-51680708854858323072)

for _ in range(10):
  n = randint(-100,-1)
  x=(-1)**(n % 2 +1) * my_fib(-n)
  test.it("Verifying that fib({n}) == {x}".format(n=n,x=x))
  test.assert_equals(fib(n),x)

test.describe("Larger values")

test.it("Verifying that fib(1000) is 4E208 and some change")
test.assert_equals(fib(1000),43466557686937456435688527675040625802564660517371780402481729089536555417949051890403879840079255169295922593080322634775209689623239873322471161642996440906533187938298969649928516003704476137795166849228875)

test.it("Verifying that fib(1001) / fib(1000) is 'the golden ratio' (1 + sqrt(5)) / 2, up to floating point precision")

test.assert_equals(fib(1001) * 1.0 / fib(1000), (1 + sqrt(5)) / 2)

n = randint(10000,100000)
test.it("Testing fib({n})".format(n=n))
test.expect(fib(n) == my_fib(n))

n = randint(1000000,1500000)
test.it("Testing fib({n})".format(n=n))
test.expect(fib(n) == my_fib(n))
