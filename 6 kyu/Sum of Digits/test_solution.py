import codewars_test as test
from solution import digital_root

@test.describe("Sum of Digits / Digital Root")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals( digital_root(16), 7 )
        test.assert_equals( digital_root(942), 6 )
        test.assert_equals( digital_root(132189), 6 )
        test.assert_equals( digital_root(493193), 2 )
        test.assert_equals( digital_root(195), 6 )
        test.assert_equals( digital_root(992), 2 )
        test.assert_equals( digital_root(999999999999), 9 )
        test.assert_equals( digital_root(167346), 9 )
        test.assert_equals( digital_root(10), 1 )
        test.assert_equals( digital_root(0), 0 )

    @test.it("Random tests")
    def _():
        
        from random import randint

        for _ in range(100):
            n = randint(0, 10**(randint(1, 20)))
            expected = 1 + ((int(n) - 1) % 9) if n > 0 else 0
            test.assert_equals(digital_root(n), expected, f'Testing for n = {n}')
