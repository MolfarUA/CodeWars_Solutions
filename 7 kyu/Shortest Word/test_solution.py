import codewars_test as test
from solution import find_short

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(find_short("bitcoin take over the world maybe who knows perhaps"), 3)
        test.assert_equals(find_short("turns out random test cases are easier than writing out basic ones"), 3)
        test.assert_equals(find_short("lets talk about javascript the best language"), 3)
        test.assert_equals(find_short("i want to travel the world writing code one day"), 1)
        test.assert_equals(find_short("Lets all go on holiday somewhere very cold"), 2)
        test.assert_equals(find_short("Let's travel abroad shall we"), 2)

@test.describe("Random Tests")
def ranfom_tests():
    
    from random import randint, choice

    def find_short_rand_tests(s):
        text = s.split(' ')
        lengths = set()
        for word in text:
            lengths.add(len(word))
        return min(lengths)
    
    names=["Bitcoin", "LiteCoin", "Ripple", "Dash",
    "Lisk", "DarkCoin", "Monero", "Ethereum",
    "Classic", "Mine", "ProofOfWork", "ProofOfStake",
    "21inc", "Steem", "Dogecoin", "Waves", "Factom", 
    "MadeSafeCoin", "BTC"]    
    
    for h in range(40):
        l = randint(1, 20)
        sL = []
        while True:
            word = choice(names)
            sL.append(word)
            if len(sL) == l: break
        s = ' '.join(sL)
        result = find_short_rand_tests(s); res = find_short(s)
        @test.it(f"Testing for: {s}")
        def test_case():
            test.assert_equals(res,result)
        
    
