import codewars_test as test
from solution import reverse_words

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(reverse_words('The quick brown fox jumps over the lazy dog.'),'ehT kciuq nworb xof spmuj revo eht yzal .god')
        test.assert_equals(reverse_words('apple'),'elppa')
        test.assert_equals(reverse_words('a b c d'),'a b c d')
        test.assert_equals(reverse_words('double  spaced  words'),'elbuod  decaps  sdrow')
        test.assert_equals(reverse_words('stressed desserts'), 'desserts stressed')
        test.assert_equals(reverse_words('hello hello'), 'olleh olleh')


@test.describe('Random Tests')
def _():
    
    from random import randrange as rand, sample
    
    words = ["Kata", "should", "always", "have", "random", "tests", "case", "to", "avoid", "hardocoded", "solution.", "This", "is", "a", "rule!"]
    
    for _ in range(50):
        s = (" "*rand(1,3)).join( sample(words, rand(len(words))))
        exp = " ".join(("".join(list(s)[::-1])).split(" ")[::-1])
        @test.it(f"testing for reverse_words({s})")
        def _():
            test.assert_equals(reverse_words(s), exp)
