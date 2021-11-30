import codewars_test as test
from solution import next_id

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(next_id([0,1,2,3,4,5,6,7,8,9,10]), 11)
        test.assert_equals(next_id([5,4,3,2,1]), 0)
        test.assert_equals(next_id([0,1,2,3,5]), 4)
        test.assert_equals(next_id([0,0,0,0,0,0]), 1)
        test.assert_equals(next_id([]), 0)
        test.assert_equals(next_id([0,0,1,1,2,2]), 3)
        test.assert_equals(next_id([0,1,1,1,3,2]), 4)
        test.assert_equals(next_id([0,1,0,2,0,3]), 4)
        test.assert_equals(next_id([9,8,0,1,7,6]), 2)
        test.assert_equals(next_id([9,8,7,6,5,4]), 0)

@test.describe("Random tests")
def random_tests():
    
    from random import randint
    
    next_sol=lambda arr: 0 if len(arr)==0 else min([i for i in range(max(arr)+2) if i not in arr])
    
    for _ in range(40):
        arr=[randint(0,20) for j in range(randint(1,35))]
        expected = next_sol(arr)
        @test.it(f"testing for next_id({arr})")
        def test_case():
            test.assert_equals(next_id(arr), expected)
