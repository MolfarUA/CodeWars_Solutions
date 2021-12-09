import codewars_test as test
from solution import friend

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(friend(["Ryan", "Kieran", "Mark",]), ["Ryan", "Mark"])
        test.assert_equals(friend(["Ryan", "Jimmy", "123", "4", "Cool Man"]), ["Ryan"])
        test.assert_equals(friend(["Jimm", "Cari", "aret", "truehdnviegkwgvke", "sixtyiscooooool"]), ["Jimm", "Cari", "aret"])
        test.assert_equals(friend(["Love", "Your", "Face", "1"]), ["Love", "Your", "Face"])
        test.assert_equals(friend(["Hell", "Is", "a", "badd", "word"]), ["Hell", "badd", "word"])
        test.assert_equals(friend(["Issa", "Issac", "Issacs", "ISISS"]), ["Issa"])
        test.assert_equals(friend(["Robot", "Your", "MOMOMOMO"]), ["Your"])
        test.assert_equals(friend(["Your", "BUTT"]), ["Your", "BUTT"])
        test.assert_equals(friend(["Hello", "I", "AM", "Sanjay", "Gupt"]), ["Gupt"])
        test.assert_equals(friend(["This", "IS", "enough", "TEst", "CaSe"]), ["This", "TEst", "CaSe"])
        test.assert_equals(friend([]), [])

@test.describe("Random Tests")
def _():    
    from random import choice, randint
    
    from string import ascii_letters as l
    abc = l
    
    def random_string(friend=False):
        return "".join(choice(abc) for _ in range(friend and 4 or randint(0, 20)))
        
    def random_input():
        return [random_string(randint(0, 100) % 4 == 0) for _ in range(randint(0, 20))]
    
    def solution(l):
        return [w for w in l if len(w) == 4]
    
    for _ in range(100):
        ri = random_input()
        expected = solution(ri)
        @test.it(f"testing for friend({ri})")
        def test_case():
            test.assert_equals(friend(ri), expected)
