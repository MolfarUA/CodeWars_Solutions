import codewars_test as test
from solution import summation

@test.describe('Fixed tests')
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(summation(1), 1)
        test.assert_equals(summation(8), 36)
        test.assert_equals(summation(22), 253)
        test.assert_equals(summation(100), 5050)
        test.assert_equals(summation(213), 22791)

@test.describe('Random tests')
def random_tests():
    
    from random import randint
    
    solution = lambda num: num * (num + 1) / 2
    
    for i in range(100):
        n = randint(1, 500)
        @test.it(f"Testing for summation({n})")
        def test_case():
            test.assert_equals(summation(n), solution(n))
