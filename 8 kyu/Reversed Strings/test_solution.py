import codewars_test as test
from solution import solution

@test.describe("Fixed Tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(solution('world'), 'dlrow')
        test.assert_equals(solution('hello'), 'olleh')
        test.assert_equals(solution(''), '')
        test.assert_equals(solution('h'), 'h')
    
@test.describe("Random Tests")
def random_tests():
    
    from random import randint
    from string import ascii_lowercase as low
    
    def sol(s):
        return s[::-1]
    
    for _ in range(100):
        
        strng = "".join([low[randint(0,len(low)-1)] for x in range(randint(2,20))])
        @test.it(f"Testing for solution({strng})")
        def test_case():
            test.assert_equals(solution(strng),sol(strng))
