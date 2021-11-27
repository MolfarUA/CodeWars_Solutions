import codewars_test as test

# for backward compatibility
try:
    from solution import findSmallestInt as find_smallest_int
except ImportError:
    from solution import find_smallest_int

@test.describe("Fixed Tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(find_smallest_int([78, 56, 232, 12, 11, 43]), 11)
        test.assert_equals(find_smallest_int([78, 56, -2, 12, 8, -33]), -33)
        test.assert_equals(find_smallest_int([0, 1-2**64, 2**64]), 1-2**64)
        test.assert_equals(find_smallest_int([-133,-5666,-89,-12341,-321423, 2**64]), -321423)
        test.assert_equals(find_smallest_int([0, 2**64, -1-2**64, 2**64, 2**64]), -1-2**64)
        test.assert_equals(find_smallest_int([1,2,3,4,5,6,7,8,9,10]), 1)
        test.assert_equals(find_smallest_int([-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]), -10)
        test.assert_equals(find_smallest_int([-78,56,232,12,8]), -78)
        test.assert_equals(find_smallest_int([78,56,-2,12,-8]), -8)
    
@test.describe("Random Tests")
def random_tests():
    
    from random import randint
    
    def sol(lst):
        return min(lst)
    
    for _ in range(100):
        arr = [ randint(-1000, 1000) for _ in range(randint(1, 30)) ]
        expected = sol(arr)
        @test.it(f"Testing for find_smallest_int({arr})")
        def test_case():
            test.assert_equals(find_smallest_int(arr), expected)
