import codewars_test as test
from solution import area_or_perimeter

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(area_or_perimeter(4, 4), 16)
        test.assert_equals(area_or_perimeter(6, 10), 32)

@test.describe("Random Tests")
def random_tests():  
    import random
            
    def solution(l, w):
        return l * l if l == w else (l + w) * 2
    
    for i in range(100):
        a, b = (i * 1200) + 2, (i * 2100) + 2
        @test.it(f"testing for area_or_perimeter({a}, {b})")
        def test_case():
            test.assert_equals(area_or_perimeter(a, b), solution(a, b))
        
    for i in range(100):
        a, b = (i * 100) + 20, (i * 100) + 20
        @test.it(f"testing for area_or_perimeter({a}, {b})")
        def test_case():
            test.assert_equals(area_or_perimeter(a, b), solution(a, b))
    
    for i in range(100):
        a, b = random.randint(100, 1200), random.randint(100, 1500)
        @test.it(f"testing for area_or_perimeter({a}, {b})")
        def test_case():
            test.assert_equals(area_or_perimeter(a, b), solution(a, b))
