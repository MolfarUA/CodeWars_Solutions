import codewars_test as test
from solution import array_diff

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(array_diff([1,2], [1]), [2], "a was [1,2], b was [1], expected [2]")
        test.assert_equals(array_diff([1,2,2], [1]), [2,2], "a was [1,2,2], b was [1], expected [2,2]")
        test.assert_equals(array_diff([1,2,2], [2]), [1], "a was [1,2,2], b was [2], expected [1]")
        test.assert_equals(array_diff([1,2,2], []), [1,2,2], "a was [1,2,2], b was [], expected [1,2,2]")
        test.assert_equals(array_diff([], [1,2]), [], "a was [], b was [1,2], expected []")
        test.assert_equals(array_diff([1,2,3], [1, 2]), [3], "a was [1,2,3], b was [1, 2], expected [3]")

@test.describe("Random Tests")
def _():
    
    from random import randint
    
    def array_sol(a, b): return [item for item in a if item not in b]
    
    for _ in range(40):
        alen,blen=randint(0,20),randint(0,20)
        a=[randint(0,40)-20 for i in range(alen)]
        b=[randint(0,40)-20 for i in range(blen)]
        exp=array_sol(a[:],b[:])
        @test.it(f"Testing for array_diff({repr(a)}, {repr(b)})")
        def _():
            test.assert_equals(array_diff(a[:],b[:]), exp)
