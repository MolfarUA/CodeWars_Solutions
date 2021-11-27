import codewars_test as test
from solution import update_light

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(update_light('green'), 'yellow')
        test.assert_equals(update_light('yellow'), 'red')
        test.assert_equals(update_light('red'), 'green')
        
    @test.it('Random Tests')
    def random_tests():        
        from random import choice

        for _ in range(10):
            color = choice(["green", "yellow", "red"])
            expected = {"green": "yellow", "yellow": "red", "red": "green"}[color]
            test.assert_equals(update_light(color), expected, "Testing: \"%s\", expecting: \"%s\"" % (color, expected))
