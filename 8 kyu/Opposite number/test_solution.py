import codewars_test as test
from solution import opposite

@test.describe("Fixed Tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(opposite(1),-1)
        test.assert_equals(opposite(25.6), -25.6)
        test.assert_equals(opposite(0), 0)
        test.assert_equals(opposite(1425.2222), -1425.2222)
        test.assert_equals(opposite(-3.1458), 3.1458)
        test.assert_equals(opposite(-95858588225),95858588225)
    
@test.describe("Random Tests")
def random_tests():
    
    from random import uniform 
    
    def sol(n):
        return -n
    
    for _ in range(100):
        num = uniform(-1e8, 1e8)
        @test.it(f"Testing for opposite({num})")
        def test_case():
            test.assert_equals(opposite(num), sol(num), "It should work for random inputs too")
