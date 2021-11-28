import codewars_test as test
from solution import quarter_of

@test.describe("Fixed Tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(quarter_of(3), 1)
        test.assert_equals(quarter_of(8), 3)
        test.assert_equals(quarter_of(11), 4)

@test.describe("Random Tests")
def random_tests():
    
    import math
    from random import randint
        
    def solution(month):
        return math.ceil(month / 3)

    for _ in range(100):
        num = randint(1, 12)
        @test.it(f"Testing for quarter_of({num})")
        def test_case():
             test.assert_equals(quarter_of(num), solution(num), "It should work for random inputs too")
