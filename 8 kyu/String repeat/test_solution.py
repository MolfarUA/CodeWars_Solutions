import codewars_test as test
from solution import repeat_str

@test.describe('Fixed tests')
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(repeat_str(4, 'a'), 'aaaa')
        test.assert_equals(repeat_str(3, 'hello '), 'hello hello hello ')
        test.assert_equals(repeat_str(2, 'abc'), 'abcabc')
    
@test.describe('Random tests')
def random_tests():
    
    from random import randint, choice
    import string 
    
    _repeat_str = lambda n, s: n * s

    chars = string.ascii_letters + string.digits + string.punctuation + string.whitespace

    for _ in range(50):
        word = "".join(choice(chars) for i in range(randint(1, 50)))
        repetition = randint(1, 50)
        @test.it(f"Testing for repeat_str({repetition}, {word})")
        def test_case():
            test.assert_equals(repeat_str(repetition, word), _repeat_str(repetition, word), "It should work for random inputs too")
