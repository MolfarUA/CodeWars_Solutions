import codewars_test as test
from solution import how_many_light_sabers_do_you_own

try:
    how_many_light_sabers_do_you_own = howManyLightsabersDoYouOwn
except NameError:
    pass

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(how_many_light_sabers_do_you_own("Zach"), 18)
        test.assert_equals(how_many_light_sabers_do_you_own(), 0)
        test.assert_equals(how_many_light_sabers_do_you_own("zach"), 0)
        
@test.describe("Random Tests")
def random_tests():
    
    from random import randint, choice
    from string import ascii_letters as l
           
    def random_generator():
        a = randint(0, 1)
        return "Zach" if a <= 0.5 else ''.join(choice(l + "  ") for _ in range(randint(0,20)))
    
    for _ in range(100):
        s = random_generator()
        expected = [0, 18][s=="Zach"]
        @test.it(f"testing for how_many_light_sabers_do_you_own(\"{s}\")")
        def test_case():
            test.assert_equals(how_many_light_sabers_do_you_own(s), expected)
