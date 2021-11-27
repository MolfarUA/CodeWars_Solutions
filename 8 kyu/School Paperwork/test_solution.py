import codewars_test as test
from solution import paperwork

@test.describe("Fixed Tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(paperwork(5,5), 25, "Failed at Paperwork(5,5)")
        test.assert_equals(paperwork(5,-5), 0, "Failed at Paperwork(5,-5)")
        test.assert_equals(paperwork(-5,-5), 0, "Failed at Paperwork(-5,-5)")
        test.assert_equals(paperwork(-5,5), 0, "Failed at Paperwork(-5,5)")
        test.assert_equals(paperwork(5,0), 0, "Failed at Paperwork(5,0)")

@test.describe("Random Tests")
def random_tests():
    
    from random import randint
    
    sol = lambda m, n: m * n if m > 0 and n > 0 else 0
    
    for c in range(100):
        i = randint(-100, 100)
        j = randint(-100, 100)
        @test.it(f"Testing for paperwork({i}, {j})")
        def test_case():
            test.assert_equals(paperwork(i,j), sol(i, j))
