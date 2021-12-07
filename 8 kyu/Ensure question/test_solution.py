import codewars_test as test
from solution import ensure_question

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(ensure_question(""),"?","Expected: '?'")
        test.assert_equals(ensure_question("Yes"),"Yes?","Expected: '?'")
        test.assert_equals(ensure_question("No?"),"No?","Expected: '?'")

@test.describe("Random Tests") 
def random_tests():
         
    from random import randint, uniform
    
    words = ["racecar","madam","kitty","wolf","robert","kata","code wars",
             "code","anna","level","radar","sagas","man","woman","internet","website",
             "yes","no","this","is","another","word","in","the","random","array","of","word"]
    
    def my_ensure_question(s):
        return f"{s}{'' if s.endswith('?') else '?'}"

    for _ in range(100):
        a = uniform(0, 1)
        word = words[randint(0, len(words) - 1)] + ("?" if a < 0.5 else "")
        @test.it(f"Testing for ensure_question({word})")
        def test_case():
            test.assert_equals(ensure_question(word), my_ensure_question(word))
