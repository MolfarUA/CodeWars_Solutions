import codewars_test as test
from solution import series_sum

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(series_sum(1), "1.00")
        test.assert_equals(series_sum(2), "1.25")
        test.assert_equals(series_sum(3), "1.39")
        test.assert_equals(series_sum(4), "1.49")
        test.assert_equals(series_sum(5), "1.57")
        test.assert_equals(series_sum(6), "1.63")
        test.assert_equals(series_sum(7), "1.68")
        test.assert_equals(series_sum(8), "1.73")
        test.assert_equals(series_sum(9), "1.77")
        test.assert_equals(series_sum(15), "1.94")
        test.assert_equals(series_sum(39), "2.26")
        test.assert_equals(series_sum(58), "2.40")
        test.assert_equals(series_sum(0), "0.00")
        
@test.describe("Random tests")
def random_tests():
    
    from random import randint
    
    sol=lambda n: '0.00' if n==0 else (lambda s: s[:-2]+"."+s[-2:])(str(int(round(sum([1.0/(1+i*3) for i in range(n)])*100))))
    
    for _ in range(40):
        n=randint(0,100)
        @test.it(f"Testing for series_sum({n})")
        def test_case():
            test.assert_equals(series_sum(n), sol(n))
