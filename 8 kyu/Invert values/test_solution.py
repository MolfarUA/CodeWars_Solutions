import random

test.it("Basic Tests")
test.assert_equals(invert([1,2,3,4,5]),[-1,-2,-3,-4,-5])
test.assert_equals(invert([1,-2,3,-4,5]), [-1,2,-3,4,-5])
test.assert_equals(invert([]), [])
test.assert_equals(invert([0]), [0])

test.it("Random Tests")

for _ in range(500):
    lst = [random.randint(-1000,1000) for _ in range(random.randint(0,1000))]
    test.assert_equals(invert(lst[:]),[-x for x in lst])
