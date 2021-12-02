test.describe("remove_smallest")

test.it("works for the examples")
test.assert_equals(remove_smallest([1, 2, 3, 4, 5]), [2, 3, 4, 5], "Wrong result for [1, 2, 3, 4, 5]")
test.assert_equals(remove_smallest([1, 2, 3, 4]), [2, 3, 4], "Wrong result for [1, 2, 3, 4]")
test.assert_equals(remove_smallest([5, 3, 2, 1, 4]), [5, 3, 2, 4], "Wrong result for [5, 3, 2, 1, 4]")
test.assert_equals(remove_smallest([1, 2, 3, 1, 1]), [2, 3, 1, 1], "Wrong result for [1, 2, 3, 1, 1]")
test.assert_equals(remove_smallest([]), [], "Wrong result for []")

from numpy.random import randint
from random import choice  

def randlist():
    return list(randint(400, size=randint(1, 10)))

def solution(numbers):
    if not numbers: return numbers
    
    numbers = numbers[:]
    numbers.remove(min(numbers))
    return numbers


test.it("returns [] if list has only one element")
for i in range(10):
    x = randint(1, 400)
    test.assert_equals(remove_smallest([x]), [], "Wrong result for [{}]".format(x))
    
test.it("returns a list that misses only one element")
for i in range(10):
    arr = randlist()
    if randint(0, 1): arr[randint(0, len(arr) - 1)] = min(arr)
    test.assert_equals(len(remove_smallest(arr[:])), len(arr) - 1, "Wrong sized result for {}".format(arr))
    
test.it("check for mutations to original list")    
a = randlist() # generates the list
b = list(a) # makes a swallow copy
remove_smallest(a) # uses the original list with the function
test.assert_equals(a, b, "You've mutated input list  (expectation assertion is on value of input list, not output of method)") # test the list match

test.it("works for random lists")
for i in range(20):
    arr = randlist()
    test.assert_equals(remove_smallest(arr[:]), solution(arr), "Wrong result for {}".format(arr))
