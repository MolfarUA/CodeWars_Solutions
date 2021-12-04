import codewars_test as test
from solution import is_triangle

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(is_triangle(1, 2, 2), True, "didn't work when sides were 1, 2, 2")
        test.assert_equals(is_triangle(7, 2, 2), False, "didn't work when sides were 7, 2, 2")
        test.assert_equals(is_triangle(1, 2, 3), False, "didn't work when sides were 1, 2, 3")
        test.assert_equals(is_triangle(1, 3, 2), False, "didn't work when sides were 1, 3, 2")
        test.assert_equals(is_triangle(3, 1, 2), False, "didn't work when sides were 3, 1, 2")
        test.assert_equals(is_triangle(5, 1, 2), False, "didn't work when sides were 5, 1, 2")
        test.assert_equals(is_triangle(1, 2, 5), False, "didn't work when sides were 1, 2, 5")
        test.assert_equals(is_triangle(2, 5, 1), False, "didn't work when sides were 2, 5, 1")
        test.assert_equals(is_triangle(4, 2, 3), True, "didn't work when sides were 4, 2, 3")
        test.assert_equals(is_triangle(5, 1, 5), True, "didn't work when sides were 5, 1, 5")
        test.assert_equals(is_triangle(2, 2, 2), True, "didn't work when sides were 2, 2, 2")
        test.assert_equals(is_triangle(-1, 2, 3), False, "didn't work when sides were -1, 2, 3")
        test.assert_equals(is_triangle(1, -2, 3), False, "didn't work when sides were 1, -2, 3")
        test.assert_equals(is_triangle(1, 2, -3), False, "didn't work when sides were 1, 2, -3")
        test.assert_equals(is_triangle(0, 2, 3), False, "didn't work when sides were 0, 2, 3")
        
@test.describe("works for random sides")
def _():    
    from random import randint
    
    def solution(a, b, c):
        a, b, c = sorted([a, b, c])
        return a + b > c
    
    for _ in range(40):
        a, b, c = [randint(-2, 10) for i in range(3)]
        @test.it(f"testing for is_triangle({a}, {b}, {c})")
        def test_case():
            test.assert_equals(is_triangle(a, b, c), solution(a, b, c))
