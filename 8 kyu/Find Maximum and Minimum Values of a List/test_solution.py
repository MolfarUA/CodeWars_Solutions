# New tests for 3.8+
import codewars_test as test
from solution import minimum, maximum

try:
    minimum = minimun
    maximum = maximun
except:
    pass

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Fixed min')
    def fixed_min_cases():
        test.assert_equals(minimum([-52, 56, 30, 29, -54, 0, -110]), -110)
        test.assert_equals(minimum([42, 54, 65, 87, 0]), 0)
        test.assert_equals(minimum([1, 2, 3, 4, 5, 10]), 1)
        test.assert_equals(minimum([-1, -2, -3, -4, -5, -10]), -10)
        test.assert_equals(minimum([9]), 9)

    @test.it('Fixed max')
    def fixed_min_cases():
        test.assert_equals(maximum([-52, 56, 30, 29, -54, 0, -110]), 56)
        test.assert_equals(maximum([4,6,2,1,9,63,-134,566]), 566)
        test.assert_equals(maximum([5]), 5)
        test.assert_equals(maximum([534,43,2,1,3,4,5,5,443,443,555,555]), 555)
        test.assert_equals(maximum([9]), 9)
        
@test.describe("Random Tests")
def random_tests():
    
    from random import randint
    
    for _ in range(40):
        arr=[(-1)**randint(0,1)*randint(1,10**randint(1,9)) for q in range(randint(1,40))]
        expected_max = max(arr)
        expected_min = min(arr)
        @test.it(f"Testing for maximum in {arr}")
        def maximum_test():
            test.assert_equals(maximum(arr[:]),expected_max,"It should work for random inputs too")
        
        @test.it(f"Testing for minimum in {arr}")
        def minimum_test():
            test.assert_equals(minimum(arr[:]),expected_min,"It should work for random inputs too")
