import codewars_test as test
from solution import is_isogram

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(is_isogram("Dermatoglyphics"), True )
        test.assert_equals(is_isogram("isogram"), True )
        test.assert_equals(is_isogram("moose"), False )
        test.assert_equals(is_isogram("isIsogram"), False )
        test.assert_equals(is_isogram("aba"), False, "same chars may not be adjacent" )
        test.assert_equals(is_isogram("moOse"), False, "same chars may not be same case" )
        test.assert_equals(is_isogram("thumbscrewjapingly"), True )
        test.assert_equals(is_isogram("abcdefghijklmnopqrstuvwxyz"), True )
        test.assert_equals(is_isogram("abcdefghijklmnopqrstuwwxyz"), False )
        test.assert_equals(is_isogram(""), True, "an empty string is a valid isogram" )
        
@test.describe("Random tests")
def random_tests():
    
    from random import randint
    
    def sol_isogram(string): return sorted(list(string.lower()))==sorted(set(string.lower()))
    
    base="abcdefghijklmnopqrstuvwxyz"
    
    for i in range(40):
        testtext="".join([base[randint(0,25)] for x in range(randint(5,45))])
        @test.it(f"Testing for {testtext}")
        def test_case():
            test.assert_equals(is_isogram(testtext), sol_isogram(testtext))
