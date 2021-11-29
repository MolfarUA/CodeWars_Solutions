import codewars_test as test

try: 
    from solution import zeroFuel as zero_fuel
except ImportError: 
    from solution import zero_fuel   
    
@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(zero_fuel(50, 25, 2), True)
        test.assert_equals(zero_fuel(60, 30, 3), True)
        test.assert_equals(zero_fuel(70, 25, 1), False)
        test.assert_equals(zero_fuel(100, 25, 3), False)
        
@test.describe("Random Tests")
def random_tests():
    
    import random
    
    control =lambda d,m,f:f*m>=d
    
    for TEST in range(0, 20):
        distance=random.randint(10, 100)
        mpg=random.randint(10, 30)
        fuel=random.randint(1, 4)
        @test.it(f'Testing for zero_fuel({distance}, {mpg}, {fuel})')
        def test_case():
            test.assert_equals(zero_fuel(distance, mpg, fuel), control(distance, mpg, fuel))
