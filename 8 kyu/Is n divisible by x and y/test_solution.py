import codewars_test as test
from solution import is_divisible

@test.describe("Sample Tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(is_divisible(3,2,2),False)
        test.assert_equals(is_divisible(3,3,4),False)
        test.assert_equals(is_divisible(12,3,4),True)
        test.assert_equals(is_divisible(8,3,4),False)
        test.assert_equals(is_divisible(48,3,4),True)
        test.assert_equals(is_divisible(100,5,10),True)
        test.assert_equals(is_divisible(100,5,3),False)
        test.assert_equals(is_divisible(4,4,2),True)
        test.assert_equals(is_divisible(5,2,3),False)
        test.assert_equals(is_divisible(17,17,17),True)
        test.assert_equals(is_divisible(17,1,17),True)

@test.describe("Random Tests")
def random_tests():
    
    from random import randint
    
    check=lambda n,x,y: n%x==0 and n%y==0
    
    for _ in range(40):
        x=randint(1,10)
        y=randint(1,20)
        n=x*y*randint(1,20)+randint(0,1)
        @test.it(f"Testing for is_divisible({n}, {x}, {y})")
        def test_case():
            test.assert_equals(is_divisible(n,x,y),check(n,x,y),"It should work for random tests too")
