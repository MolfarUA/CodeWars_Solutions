import codewars_test as test
from solution import duplicate_count 

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it("Basic Tests")
    def basic_tests():
        test.assert_equals(duplicate_count(""), 0)
        test.assert_equals(duplicate_count("abcde"), 0)
        test.assert_equals(duplicate_count("abcdeaa"), 1)
        test.assert_equals(duplicate_count("abcdeaB"), 2)
        test.assert_equals(duplicate_count("Indivisibilities"), 2)

@test.describe('Random Tests')
def random_tests():
    
    from random import randint, choice     
    from string import ascii_letters, digits
    
    def sol(s):
        s = s.lower()
        return len(set(s)) - len(s) + sum([s.count(c) for c in set(s) if s.count(c) > 1])
       
    for _ in range(100):
        strng = ''.join(choice(ascii_letters + digits) for i in range(0, randint(0, 100)))
        @test.it(f"Testing for duplicate_count({strng})")
        def test_case():
            test.assert_equals(duplicate_count(strng), sol(strng))
