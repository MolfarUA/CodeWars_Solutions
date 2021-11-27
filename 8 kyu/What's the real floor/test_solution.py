import codewars_test as test
from solution import get_real_floor

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('should return a correct value for floors lower than 13')
    def lower_than_13():
        test.assert_equals(get_real_floor(1), 0)
        test.assert_equals(get_real_floor(0), 0)
        test.assert_equals(get_real_floor(5), 4)
        test.assert_equals(get_real_floor(10), 9)
        test.assert_equals(get_real_floor(12), 11)
        
    @test.it('should return a correct value for floors greater than 13')
    def greater_than_13():
        test.assert_equals(get_real_floor(14), 12)
        test.assert_equals(get_real_floor(15), 13)
        test.assert_equals(get_real_floor(37), 35)
        test.assert_equals(get_real_floor(200), 198)
        
    @test.it('should return a correct value for basement floors')
    def basement():
        test.assert_equals(get_real_floor(-2), -2)
        test.assert_equals(get_real_floor(-5), -5)
        
@test.describe('Random tests')
def random_tests():
    
    from random import randint
    
    def theRealOne(n):
        if n <= 0:
            return n
        elif n < 13:
            return n - 1
        else:
            return n - 2
        
    for i in range(200):
        floor=randint(-500,500)
        floor += floor==13
        @test.it(f"testing for get_real_floor({floor})")
        def test_case():
            test.assert_equals(get_real_floor(floor),theRealOne(floor))
