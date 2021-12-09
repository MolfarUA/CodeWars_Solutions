import codewars_test as test
from solution import lovefunc

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(lovefunc(1,4), True)
        test.assert_equals(lovefunc(2,2), False)
        test.assert_equals(lovefunc(0,1), True)
        test.assert_equals(lovefunc(0,0), False)

@test.describe("Random Tests")
def random_tests():
    
    from random import randint as rnd
    
    for i in range(100):
        f1 = rnd(0,1000);
        f2 = rnd(0,1000)
        exp = bool((f1+f2)%2)
        @test.it(f"testing for lovefunc({f1}, {f2})")
        def test_case():
            test.assert_equals(lovefunc(f1, f2), exp)
