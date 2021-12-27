import codewars_test as test
from solution import doubleton


@test.describe("Fixed Tests")
def test_group():
    @test.it("Fixed Tests Cases")
    def test_case():
        test.assert_equals(doubleton(130), 131, 'Wrong result for 130')
        test.assert_equals(doubleton(1434), 1441, 'Wrong result for 1434')
        test.assert_equals(doubleton(20), 21, 'Wrong result for 20')
        test.assert_equals(doubleton(5), 10, 'Wrong result for 5')
        test.assert_equals(doubleton(131), 133, 'Wrong result for 131')


from random import randint        
@test.describe("Random tests")
def random_group():
    
    def _is_doubleton(num):
        return len(set(str(num))) == 2

    def _doubleton(num):
        num += 1
        while not _is_doubleton(num):
            num += 1
        return num
    
      
    @test.it('Random Test Cases for n from 1 to 1000')
    def random_test_cases():
        for i in range(50):
            n = randint(1, 1000)
            expected = _doubleton(n)
            actual = doubleton(n)
            test.assert_equals(actual, expected, f'Wrong result for {n}')
                
    @test.it('Random Test Cases for n from 1000 to 1000000')
    def random_test_cases():
        for i in range(50):
            n = randint(1000, 1000000)
            expected = _doubleton(n)
            actual = doubleton(n)
            test.assert_equals(actual, expected, f'Wrong result for {n}')  
