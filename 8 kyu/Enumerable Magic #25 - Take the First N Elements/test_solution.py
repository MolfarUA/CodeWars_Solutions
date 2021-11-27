import codewars_test as test
from solution import take

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(take([0, 1, 2, 3, 5, 8, 13], 3), [0, 1, 2], "should return the first 3 items");
        test.assert_equals(take([0, 1, 2, 3, 5, 8, 13], 0), [], "should return 0 items");
        test.assert_equals(take([], 3), [], "empty array should return empty array");
    
@test.describe("Random Tests")
def _():
    import math,random
    def generateRandomArray():
        n = int(math.floor(random.random() * 100))
        arr = []
        for i in range(n):arr.append(int(math.floor(-100 * random.random() + 100 * random.random())))
        return arr
    
    for i in range(100):
        arr = generateRandomArray()
        n = int(math.floor(random.random() * 100))
        expected = arr[:n]
        message = ""
        if (len(arr)==0):message = "empty array should return empty array"
        elif(n== 0): message = "should return 0 items"
        elif(n <= len(arr)): message = "should return the first " + str(n) + " items"
        else:message = "should return the first " + str(len(arr)) + " items (because there are no " + str(n) + " items in the array)"
        @test.it(f"Testing with arr = {arr} and n = {n}: ")
        def test_case():
            test.assert_equals(take(arr, n), expected, message)
