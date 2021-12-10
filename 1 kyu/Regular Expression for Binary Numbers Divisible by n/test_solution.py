from solution import regex_divisible_by
import codewars_test as test
import re
from random import choice, randint

def _anti_cheat():
    with open('/workspace/solution.txt') as sol_file:
        sol = sol_file.readlines()
    sol_size = sum(len(line.strip()) for line in sol)
    sol = ';'.join(sol)
    test.expect(sol_size < 5000,
        "Seriously, you didn't believe me? You can't hard-code the answers! " +
        "Either that, or your solution is inefficient. Let's keep it under 5K, k? " +
        "(Your code length: {})".format(sol_size))
    test.expect(not re.search(r'([^a-zA-Z0-9_]|^)(re|sys|print)([^a-zA-Z0-9_]|$)', sol),
        "You're asking for trouble... (You cannot use re, sys, or print)")

@test.describe('Anti-cheating checks')
def _():
    _anti_cheat()

def _test_for(n):
    
    def generate_hard_positive():
        return 2 ** randint(22, 30) // n * n + n
    
    string = regex_divisible_by(n)
    regex = re.compile(string)
    invalid_args = [' ', chr(randint(97, 122)), chr(randint(33, 45)), str(randint(12, 91))]
    valid_args = sorted([0, n, n * randint(2, 50), randint(51, 1000), randint(1001, 2 ** 31 - 1),
        generate_hard_positive()])
    
    @test.describe('Testing divisibility by {}'.format(n))
    def _():
        @test.it('Should be well-formed')
        def __():
            test.assert_not_equals(string, '', 'Cannot be an empty string')
            test.expect(not re.search(r'[^01?*+^$:()\[\]|]', string),
                'Contains illegal characters: {}'.format(''.join(set(string) - set('01?*+^$:()[]|'))))

        @test.it('Should reject invalid inputs')
        def __():
            for arg in invalid_args:
                test.expect(not regex.search(arg), 'Did not reject {}'.format(arg))

        @test.it('Should work for any number')
        def __():
            for arg in valid_args:
                test.assert_equals(bool(regex.search(bin(arg)[2:])), arg % n == 0,
                    'Did not work for {}'.format(arg))
    
for n in range(1, 19):
    _test_for(n)
