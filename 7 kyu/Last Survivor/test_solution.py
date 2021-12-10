import codewars_test as test
from solution import last_survivor
import string
from random import randint, choices

@test.describe("Example")
def test_group():
    @test.it("test case")
    def test_case():
        test.assert_equals(last_survivor('abc', [1, 1]), 'a')
        test.assert_equals(last_survivor('kbc', [0, 1]), 'b')
        test.assert_equals(last_survivor('zbk', [2, 1]), 'z')
        test.assert_equals(last_survivor('c', []), 'c')
        test.assert_equals(last_survivor('foiflxtpicahhkqjswjuyhmypkrdbwnmwbrrvdycqespfvdviucjoyvskltqaqirtjqulprjjoaiagobpftywabqjdmiofpsr', [8, 59, 52, 93, 21, 40, 88, 85, 59, 10, 82, 18, 74, 59, 51, 47, 75, 49, 23, 56, 1, 33, 39, 33, 34, 44, 25, 0, 51, 25, 36, 32, 57, 10, 57, 12, 51, 55, 24, 55, 31, 49, 6, 15, 10, 48, 27, 29, 38, 30, 35, 42, 23, 32, 9, 39, 39, 36, 8, 29, 2, 33, 14, 3, 13, 25, 9, 25, 18, 10, 1, 2, 20, 8, 2, 11, 5, 7, 0, 10, 10, 8, 12, 3, 5, 1, 7, 7, 5, 1, 4, 0, 4, 0, 0, 1]), 'd')
        
@test.describe('Random Tests')
def random_tests():
    
    MIN_LEN_LETTERS, MAX_LEN_LETTERS = 1, 100
    ABC = string.ascii_lowercase
    
    def generate_random_case(): 
        letters = ''.join(choices(ABC, k=randint(MIN_LEN_LETTERS, MAX_LEN_LETTERS)))
        coords = [randint(0, len(letters[i:-1])) for i, _ in enumerate(letters[:-1])]
        return letters, coords

    def _last_survivor_ref(letters, coords): 
        letters = list(letters)
        while coords: 
            letters.pop(coords.pop(0))
        return letters[0]

    def _do_one_test():
        letters, coords = generate_random_case()
        expected = _last_survivor_ref(letters[:], coords[:])
        actual = last_survivor(letters[:], coords[:])
        test.assert_equals(actual, expected)

    @test.it('Random Test Cases')
    def random_test_cases():
        for _ in range(100):
            _do_one_test()
