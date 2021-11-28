import codewars_test as test
from solution import highest_value

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it("should handle alphanumeric strings")
    def _():
        test.assert_equals(highest_value("AaBbCcXxYyZz0189", "KkLlMmNnOoPp4567"), "KkLlMmNnOoPp4567")
        test.assert_equals(highest_value("ABcd", "0123"), "ABcd")

    @test.it("should handle non-alphanumeric ASCII")
    def _():
        test.assert_equals(highest_value("!\"?$%^&*()", "{}[]@~'#:;"), "{}[]@~'#:;")

    @test.it("should handle ties")
    def _():
        test.assert_equals(highest_value("ABCD", "DCBA"), "ABCD")
        
@test.describe("Random Tests")
def random_tests():
    
    from random import randint, choice
    from string import ascii_letters as le, digits as di, punctuation as pu
    
    sol = lambda x, y: x if sum(map(ord, x)) >= sum(map(ord, y)) else y
    
    def random_generator():
        l = randint(1, 100)
        x = ''.join(choice(le + di + pu) for _ in range(l))
        y = ''.join(choice(le + di + pu) for _ in range(l))
        return x, y
    
    for _ in range(100):
        a, b = random_generator()
        @test.it(f"testing for highest_value({a}, {b})")
        def test_case():
            test.assert_equals(highest_value(a, b),sol(a, b))
