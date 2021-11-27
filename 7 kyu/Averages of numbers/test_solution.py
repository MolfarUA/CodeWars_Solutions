import codewars_test as test
from solution import averages

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        tests = (
            ([2, 2, 2, 2], [2, 2, 2, 2, 2]),
            ([0, 0, 0, 0], [2, -2, 2, -2, 2]),
            ([2, 4, 3, -4.5], [1, 3, 5, 1, -10]),
            ([], [])
        )
        
        for exp, inp in tests:
            test.assert_equals(averages(inp), exp)
            
    @test.it("None, Empty, Single ElementTests")
    def _():
        tests = (
            (None, []),
            ([], []),
            ([1], [])
        )
        
        for inp, exp in tests:
            test.assert_equals(averages(inp), exp)

@test.describe("Random Tests")
def _():
    from random import randint    
    
    def null_empty_single():
        return [None, [], [randint(-1000, 1000)]][randint(0, 2)]    
    
    def reference(arr):
        if not arr or len(arr) < 2:
            return []
        return [(x + y) / 2.0 for x, y in zip(arr, arr[1:])]
    
    for _ in range(100):
        if randint(0, 200) % 4 == 0:
            test_case = null_empty_single()
        else:
            test_case = [randint(-1000, 1000) for _ in range(randint(2, 100))]
        @test.it(f"testing for averages({test_case})")
        def test_case():
            test.assert_equals(averages(test_case), reference(test_case))
