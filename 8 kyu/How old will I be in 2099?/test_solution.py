test.describe("Basic tests")
test.assert_equals(calculate_age(2012, 2016),"You are 4 years old.")
test.assert_equals(calculate_age(1989, 2016),"You are 27 years old.")
test.assert_equals(calculate_age(2000, 2090),"You are 90 years old.")
test.assert_equals(calculate_age(2000, 1990),"You will be born in 10 years.")
test.assert_equals(calculate_age(2000, 2000),"You were born this very year!")
test.assert_equals(calculate_age(900, 2900),"You are 2000 years old.")
test.assert_equals(calculate_age(2010, 1990),"You will be born in 20 years.")
test.assert_equals(calculate_age(2010, 1500),"You will be born in 510 years.")
test.assert_equals(calculate_age(2011, 2012),"You are 1 year old.")
test.assert_equals(calculate_age(2000, 1999),"You will be born in 1 year.")

test.describe("Random tests")
from random import randint
calculate_sol=lambda b, y: (lambda d: "You are %s year%s old." %(d,"s" if d!=1 else "") if d>0 else "You will be born in %s year%s." %(-d,"s" if d!=-1 else "") if d<0 else "You were born this very year!")(y-b)

for _ in range(40):
  b,y=randint(0,10**randint(1,3)),randint(0,10**randint(1,3))
  test.it("Testing for calculate_age(%s,%s)" %(b,y))
  test.assert_equals(calculate_age(b,y),calculate_sol(b,y),"It should work for random inputs too")
