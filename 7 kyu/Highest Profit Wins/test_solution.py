import codewars_test as test
from solution import min_max

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(min_max([1,2,3,4,5]), [1, 5])
        test.assert_equals(min_max([2334454,5]), [5, 2334454])
    
@test.describe("should work for random lists")
def _():
    
    from random import randint, shuffle
    
    for i in range(0,100):
        s = [randint(-10000,10000) for l in range(0, randint(1,120))]
        expected = [min(s), max(s)]
        @test.it(f"testing for min_max({s})")
        def test_case():
            test.assert_equals(min_max(s[:]),expected)
