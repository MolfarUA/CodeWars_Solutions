import codewars_test as test
from solution import multiply

@test.describe("Fixed Tests")
def fixed_tests():
    
    from inspect import isfunction
    
    @test.it("Should have function 'multiply'")
    def function_multiply():
        test.expect(isfunction(multiply)==True,"'multiply' is not defined as function")

    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(multiply(2, 3), 6)   

@test.describe("Random Tests")
def random_tests():
    
    from random import randint
    
    for i in range(100):
        x, y = randint(0,100), randint(1,200)
        @test.it(f"testing for multiply({x}, {y})")
        def test_case():
            test.assert_equals( multiply( x, y ), x * y)
