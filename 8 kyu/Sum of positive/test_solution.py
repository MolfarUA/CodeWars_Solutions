try:
    import codewars_test as test
except:
    pass
from solution import positive_sum

@test.describe("positive_sum")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(positive_sum([1,2,3,4,5]),15)
        test.assert_equals(positive_sum([1,-2,3,4,5]),13)
        test.assert_equals(positive_sum([-1,2,3,4,-5]),9)
        
    @test.it("returns 0 when array is empty")
    def empty_case():
        test.assert_equals(positive_sum([]),0)      
        
    @test.it("returns 0 when all elements are negative")
    def negative_case():
        test.assert_equals(positive_sum([-1,-2,-3,-4,-5]),0)

@test.describe("Random Tests")
def random_tests():
    
    from random import randint
    
    def randarr(l):
        return [randint(-100, 100) for _ in range(l)]
    
    def solution(arr):
        return sum(x for x in arr if x > 0)
    
    for _ in range(40):
        arr = randarr(randint(5, 120))
        @test.it(f"testing for positive_sum({arr})")
        def test_case():
            test.assert_equals(positive_sum(arr[:]), solution(arr[:]))
