import codewars_test as test
from solution import grow

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        tests = [
            [6 , [1, 2, 3]],
            [16, [4, 1, 1, 1, 4]],
            [64, [2, 2, 2, 2, 2, 2]],
        ]
        
        for exp, inp in tests:
            test.assert_equals(grow(inp), exp)
    
@test.describe("Random Tests")
def random_tests():
    
    from random import randint
    from operator import mul
    
    reference = lambda a: len(a) and int(0 not in a) and __import__("functools").reduce(mul, a)
    
    def tests_case():
        return [randint(0, 1000) for _ in range(randint(1, 1000))]
    
    for _ in range(100):
        t = tests_case()
        expected = reference(t)
        @test.it(f"testing for grow({t})")
        def test_case():
            test.assert_equals(grow(t[:]), expected)
