import codewars_test as test
from solution import sum_str

@test.describe("Fixed Tests")
def basic_tests():
    
    @test.it("Sample Tests")
    def sample_tests():
        test.assert_equals(sum_str("4","5"), "9")
        test.assert_equals(sum_str("34","5"), "39")

    @test.it("Tests with empty strings")
    def empty_string():
        test.assert_equals(sum_str("9",""), "9", "x + empty = x")
        test.assert_equals(sum_str("","9"), "9", "empty + x = x")
        test.assert_equals(sum_str("","") , "0", "empty + empty = 0")

@test.describe("Some random tests")
def random_tests():
    
    from random import randint

    sol = lambda x, y: str((int(a) or 0) + (int(b) or 0))
    
    for _ in range(100):
        a,b = str(randint(0,1e6)), str(randint(0,1e6))
        @test.it(f"Testing for sum_str({a}, {b})")
        def test_case():
            test.assert_equals(sum_str(a, b), sol(a, b))
