import codewars_test as test

try:
    from solution import abbrevName as abbrev_name
except ImportError:
    from solution import abbrev_name

@test.describe("Fixed Tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(abbrev_name("Sam Harris"), "S.H")
        test.assert_equals(abbrev_name("Patrick Feenan"), "P.F")
        test.assert_equals(abbrev_name("Evan Cole"), "E.C")
        test.assert_equals(abbrev_name("P Favuzzi"), "P.F")
        test.assert_equals(abbrev_name("David Mendieta"), "D.M")
    
@test.describe("Random Tests")
def random_tests():  
    
    from random import choice, randint
    from string import ascii_lowercase as low, ascii_uppercase as up

    answer = lambda s: (s.split(' ')[0][0]+'.'+s.split(' ')[1][0]).upper()
    
    for _ in range(200):
        a = ''.join(choice(up + low) for _ in range(randint(1,20)))
        b = ''.join(choice(up + low) for _ in range(randint(1,20)))
        name = f"{a} {b}"
        @test.it(f"Testing for abbrev_name({name})")
        def test_case():
            test.assert_equals(abbrev_name(name), answer(name), "It should work for random inputs too")
