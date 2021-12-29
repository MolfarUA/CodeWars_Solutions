import codewars_test as test
from solution import find_next_square

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it("should return the next square for perfect squares")
    def basic_test_cases():
        test.assert_equals(find_next_square(121), 144, "Wrong output for 121")
        test.assert_equals(find_next_square(625), 676, "Wrong output for 625")
        test.assert_equals(find_next_square(319225), 320356, "Wrong output for 319225")
        test.assert_equals(find_next_square(15241383936), 15241630849, "Wrong output for 15241383936")

    @test.it("should return -1 for numbers which aren't perfect squares")
    def _():
        test.assert_equals(find_next_square(155), -1, "Wrong output for 155")
        test.assert_equals(find_next_square(342786627), -1, "Wrong output for 342786627")
        
@test.describe("should work for random inputs")
def random_tests():
    
    from random import randint, uniform
    
    def solution(sq):
        root = sq ** 0.5
        
        return (root + 1)**2 if root % 1 == 0 else -1
    
    for _ in range(40):
        sq = int(uniform(0, 1) * 10 ** randint(1, 5))
        
        if randint(0, 1): sq = sq*sq
        
        @test.it(f"testing for find_next_square({sq})")
        def test_case():
            test.assert_equals(find_next_square(sq),solution(sq))
