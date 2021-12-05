import codewars_test as test
from solution import get_decimal

@test.describe("Example")
def test_group():
    @test.it("returns decimal part from 10 as 0")
    def zero_test_case():
        test.assert_approx_equals(get_decimal(10), 0)
        
    @test.it("returns decimal part from -1.2 as 0.2")
    def negative_test_case():
        test.assert_approx_equals(get_decimal(-1.2), 0.2)
        
    @test.it("returns decimal part from 4.5 as 0.5")
    def positive_test_case():
        test.assert_approx_equals(get_decimal(4.5), 0.5)
        
from random import uniform, randint
@test.describe('Random Tests')
def random_tests():
    
    def generate_random_case(min_value=-5000, max_value=5000): 
        res = uniform(min_value, max_value)
        x = randint(1, 9)
        return round(res, x)

    def _get_decimal_reference(n): 
        return abs(n) - int(abs(n))
        """
        res = str(float(n)).split('.')[-1]
        if res == '0': 
            return 0
        res = '0.' + res
        return float(res)
        """

    def _do_one_test():
        n = generate_random_case()
        expected = _get_decimal_reference(n)
        actual = get_decimal(n)
        test.assert_approx_equals(actual, expected)

    @test.it('Random Test Cases')
    def random_test_cases():
        for _ in range(100):
            _do_one_test()        
