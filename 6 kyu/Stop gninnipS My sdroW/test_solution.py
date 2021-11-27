import random
import codewars_test as test
from solution import spin_words

@test.describe("Stop gninnipS My sdroW!")
def fixed_tests():
    @test.it("Single word")
    def _():
        test.assert_equals(spin_words("Welcome"), "emocleW")
        test.assert_equals(spin_words("to"), "to")
        test.assert_equals(spin_words("CodeWars"), "sraWedoC")

    @test.it("Multiple words")
    def _():
        test.assert_equals(spin_words("Hey fellow warriors"), "Hey wollef sroirraw")
        test.assert_equals(spin_words("This sentence is a sentence"), "This ecnetnes is a ecnetnes")

    @test.it("Random testing")
    def _():        
        
        def known_good(sentence):
            words = [word for word in sentence.split(" ")]
            words = [word if len(word) < 5 else word[::-1] for word in words]
            return " ".join(words)
        
        source = "Write a function that takes in a string of one or more words, and returns the same string, but with all five or more letter words reversed (Just like the name of this Kata). Strings passed in will consist of only letters and spaces. Spaces will be included only when more than one word is present."
        is_valid = lambda c: 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == ' '
        source = "".join([c for c in source if is_valid(c)])
        source = [w for w in source.split(" ")]

        for _ in range(20):
            words = []
            for _ in range(random.randrange(1, 30)):
                words.append(random.choice(source))
            words = " ".join(words)
            test.assert_equals(spin_words(words), known_good(words), f'Testing for sentence = {repr(words)}')
