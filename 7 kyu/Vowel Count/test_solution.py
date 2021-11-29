import random

import codewars_test as test
try:
    from solution import getCount
    get_count = getCount
except:    
    from solution import get_count
    
@test.describe("Sample tests")
def sample_tests():
    
    @test.it("Should count all vowels")
    def all_vowels():
        test.assert_equals(get_count("aeiou"), 5, f"Incorrect answer for \"aeiou\"")
        
    @test.it("Should not count \"y\"")
    def only_y():
        test.assert_equals(get_count("y"), 0, f"Incorrect answer for \"y\"")        
        
    @test.it("Should return 0 when no vowels")
    def no_vowels():
        test.assert_equals(get_count("bcdfghjklmnpqrstvwxz y"), 0, f"Incorrect answer for \"bcdfghjklmnpqrstvwxz y\"")
        
    @test.it("Should return 0 for empty string")
    def no_vowels():
        test.assert_equals(get_count(""), 0, f"Incorrect answer for empty string")
        
    @test.it("Should return 5 for \"abracadabra\"")
    def test_abracadabra():    
        test.assert_equals(get_count("abracadabra"), 5, f"Incorrect answer for \"abracadabra\"")

@test.describe("Random tests")
def random_tests():
    
    vowels = "aeiou"
    nonvowels = "bcdfghjklmnpqrstvwxyz"
    
    def generate_tests(generator, count):
        return [generator() for _ in range(count)]
    
    def generate_no_vowels():
        word_count = random.randint(1, 10)
        words = ["".join(random.choices(nonvowels, k=random.randint(1, 8))) for _ in range(word_count)]
        sentence = " ".join(words)
        return (sentence, 0)
    
    def generate_only_vowels():
        word_count = random.randint(1, 10)
        words = ["".join(random.choices(vowels, k=random.randint(1, 8))) for _ in range(word_count)]
        sentence = " ".join(words)
        return (sentence, sum(len(word) for word in words))
    
    def generate_mixed():
        word_count = random.randint(1, 10)
        vowel_parts = ["".join(random.choices(vowels, k=random.randint(1, 3))) for _ in range(word_count)]
        nonvowel_parts = ["".join(random.choices(nonvowels, k=random.randint(1, 8))) for _ in range(word_count)]
        words = [ "".join(random.sample(v+nv, k=len(v+nv))) for v,nv in zip(vowel_parts, nonvowel_parts)]
        sentence = " ".join(words)
        return (sentence, sum(len(word) for word in vowel_parts))
    
    @test.it("Random tests")
    def random_test():
        
        test_cases = generate_tests(generate_no_vowels, 10) +\
                     generate_tests(generate_only_vowels, 10) +\
                     generate_tests(generate_mixed, 80)
        random.shuffle(test_cases)
        
        for input, expected in test_cases:
            actual = get_count(input)
            test.expect(actual == expected, f"Incorrect answer for input: \"{input}\"\nActual: {actual}\nExpected: {expected}")
