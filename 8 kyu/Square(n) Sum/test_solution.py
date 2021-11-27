import codewars_test as test
from solution import square_sum

@test.describe("Fixed Tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(square_sum([1,2]), 5)
        test.assert_equals(square_sum([0, 3, 4, 5]), 50)
        test.assert_equals(square_sum([]), 0)
        test.assert_equals(square_sum([-1,-2]), 5)
        test.assert_equals(square_sum([-1,0,1]), 2)

@test.describe("Random Tests")
def random_tests():
    
    from random import randint
    
    square_sol=lambda n: sum([x*x for x in n])
    
    for _ in range(40):
        lst = [randint(0,40)-20 for _ in range(randint(2,10))]
        @test.it(f"Testing for square_sum({lst})")
        def test_case():
            expected = square_sol(lst)
            test.assert_equals(square_sum(lst), expected, "It should work for random inputs too")
