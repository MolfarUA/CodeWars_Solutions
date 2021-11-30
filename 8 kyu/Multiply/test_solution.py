import codewars_test as test 
from solution import multiply

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(multiply(1,1), 1)
        test.assert_equals(multiply(2,1), 2)
        test.assert_equals(multiply(2,2), 4)
        test.assert_equals(multiply(3,5), 15)
        test.assert_equals(multiply(1.5,2.5), 3.75)
        test.assert_equals(multiply(0,5), 0)
        test.assert_equals(multiply(0,0), 0)
