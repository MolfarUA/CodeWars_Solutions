import codewars_test as test

try:
    from solution import break_chocolate
except ImportError:
    from solution import breakChocolate as break_chocolate

@test.describe("Sample Tests")
def basic_tests():
    @test.it("Tests")
    def it_1():
        test.assert_equals(break_chocolate(5, 5), 24)
        test.assert_equals(break_chocolate(7, 4), 27)
        test.assert_equals(break_chocolate(1, 1), 0)
        test.assert_equals(break_chocolate(0, 0), 0)
        test.assert_equals(break_chocolate(6, 1), 5)
    
@test.describe("Random Tests")
def random_tests():
    from random import randint
    
    def reference(n, m):
        return max(n*m-1,0)
    
    @test.it("Tests")
    def it_1():
        for _ in range(100):
            a = randint(0, 1_000_000)
            b = randint(0, 1_000_000)
            test.assert_equals(break_chocolate(a, b), reference(a, b))
