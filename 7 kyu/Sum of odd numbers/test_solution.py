import codewars_test as test
from solution import row_sum_odd_numbers

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(row_sum_odd_numbers(1), 1)
        test.assert_equals(row_sum_odd_numbers(2), 8)
        test.assert_equals(row_sum_odd_numbers(13), 2197)
        test.assert_equals(row_sum_odd_numbers(19), 6859)
        test.assert_equals(row_sum_odd_numbers(41), 68921)
        test.assert_equals(row_sum_odd_numbers(42), 74088)
        test.assert_equals(row_sum_odd_numbers(74), 405224)
        test.assert_equals(row_sum_odd_numbers(86), 636056)
        test.assert_equals(row_sum_odd_numbers(93), 804357)
        test.assert_equals(row_sum_odd_numbers(101), 1030301)

@test.describe("Random tests")
def random_tests():
    
    from random import randint
    
    sol=lambda n: n*n*n
    
    for _ in range(50):
        n=randint(0,500) + 1
        @test.it(f"Testing for row_sum_odd_numbers{n}")
        def test_case():
            test.assert_equals(row_sum_odd_numbers(n), sol(n))
