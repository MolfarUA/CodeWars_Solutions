import codewars_test as test
from solution import calculate_1RM

@test.describe("Basic tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(calculate_1RM(135,20),282)
        test.assert_equals(calculate_1RM(200,8),253)
        test.assert_equals(calculate_1RM(270,2),289)
        test.assert_equals(calculate_1RM(360,1),360)
        test.assert_equals(calculate_1RM(400,0),0)

@test.describe("Random tests")
def random_tests():
    import random
    
    asidnjf2394in123 = lambda w, r: w * (1 + r / 30)
    kms1n235489im = lambda w, r: 100 * w / (101.3 - 2.67123 * r)
    mkfgj189435 = lambda w, r: w * r ** 0.10
    
    def asdmgfk12m34jk1(w, r):
        if r == 0:
            return 0
        elif r == 1:
            return w
        e = asidnjf2394in123(w, r)
        m = kms1n235489im(w, r)
        l = mkfgj189435(w, r)
        return round(max(e, m, l))
    
    
    for i in range(100):
        w = random.randint(1, 1000)
        r = random.randint(0, 100)
        personAnswer = calculate_1RM(w, r)
        rightAnswer = asdmgfk12m34jk1(w, r)
        answerValidity = personAnswer == rightAnswer
        if rightAnswer == 0:
            answerValidity = personAnswer in (0, None)
        @test.it(f"testing for calculate_1RM({w}, {r})")
        def test_case():
            test.assert_equals(answerValidity,True)
