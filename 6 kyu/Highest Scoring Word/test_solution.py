import codewars_test as test
from solution import high

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(high('man i need a taxi up to ubud'), 'taxi')
        test.assert_equals(high('what time are we climbing up the volcano'), 'volcano')
        test.assert_equals(high('take me to semynak'), 'semynak')
        test.assert_equals(high('massage yes massage yes massage'), 'massage')
        test.assert_equals(high('take two bintang and a dance please'), 'bintang')
        test.assert_equals(high('aa b'), 'aa')
        test.assert_equals(high('b aa'), 'b')
        test.assert_equals(high('bb d'), 'bb')
        test.assert_equals(high('d bb'), 'd')
        test.assert_equals(high("aaa b"), "aaa")

@test.describe("Random Tests")
def _():
    
    from random import randint, choice
    
    highest_score_solver = lambda x: max(x.split(), key=lambda k: sum(ord(c) - 96 for c in k))
    
    letters = "abcdefghijklmnopqrstuvwxyz"
    
    rnd_word = lambda: ''.join(choice(letters) for _ in range(randint(3, 10)))
    
    for _ in range(100):
        test_str = ' '.join(rnd_word() for _ in range(randint(5, 25)))
        test_sol = highest_score_solver(test_str)
        @test.it(f"Testing for: {repr(test_str)}, expected: {repr(test_sol)}")
        def _():
            test.assert_equals(high(test_str), test_sol)
