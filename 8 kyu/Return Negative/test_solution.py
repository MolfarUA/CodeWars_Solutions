import codewars_test as test
from solution import make_negative

@test.describe("Fixed Tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(make_negative(42),-42)
        test.assert_equals(make_negative(-9),-9)
        test.assert_equals(make_negative(0),0)

@test.describe("Random Tests")
def random_tests():
    
    from random import randint as rnd

    for _ in range(100):
        number = rnd(-1000, 1000)
        @test.it(f"testing for make_negative({number})")
        def test_case():
            test.assert_equals(make_negative(number), -abs(number))
