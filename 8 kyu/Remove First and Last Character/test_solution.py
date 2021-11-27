import codewars_test as test
from solution import remove_char

@test.describe("Fixed Tests")
def basic_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(remove_char('eloquent'), 'loquen')
        test.assert_equals(remove_char('country'), 'ountr')
        test.assert_equals(remove_char('person'), 'erso')
        test.assert_equals(remove_char('place'), 'lac')
        test.assert_equals(remove_char('ok'), '')
        test.assert_equals(remove_char('ooopsss'), 'oopss')
    
@test.describe("Random Tests")
def random_tests():
    
    from random import randint
    from string import ascii_lowercase as low
    
    sol=lambda s: s[1:-1]
    
    for _ in range(40):
        
        s="".join([low[randint(0,len(low)-1)] for x in range(randint(2,20))])
        @test.it(f"Testing for remove_char({s})")
        def test_case():
            test.assert_equals(remove_char(s),sol(s),"It should work for random inputs too")
