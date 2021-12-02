import codewars_test as test
from solution import century

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(century(1705), 18, 'Testing for year 1705')
        test.assert_equals(century(1900), 19, 'Testing for year 1900')
        test.assert_equals(century(1601), 17, 'Testing for year 1601')
        test.assert_equals(century(2000), 20, 'Testing for year 2000')
        test.assert_equals(century(356), 4, 'Testing for year 356')
        test.assert_equals(century(89), 1, 'Testing for year 89')


@test.describe("Random Tests")
def rand_tests():
    
    from random import randint
    
    g_c = lambda y: (y + 99) // 100

    for _ in range(randint(200, 250)):
        year = randint(1, 9999)
        @test.it(f"testing for century({year})")
        def test_case():
            test.assert_equals(century(year), g_c(year))
