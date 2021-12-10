import codewars_test as test
import re
import random
from solution import last_survivors

def is_valid(v):
    if not isinstance(v, str):
        test.fail(f"expected a string but got {v}")
    return v

def fix(s):
    return ''.join(sorted(list(s)))

def make_msg(should_be, _is):
    not_in = "".join({v for v in should_be if v not in _is})
    extra = "".join({v for v in _is if v not in should_be})
    if len(not_in) == 0:
        return f"Result does not match.\nResult should NOT contain any of: '{extra}'\n"
    if len(extra) == 0:
        return f"Result does not match.\nResult should contain all of: '{not_in}'\n"
    return f"Result does not match.\nResult should NOT contain any of: '{extra}'\nbut SHOULD contain: '{not_in}'\n"
    

@test.describe("Sample Tests")
def sample():
    @test.it("Given abaa")
    def _():
        user_result = is_valid(last_survivors('abaa'))
        test.assert_equals(fix(user_result), 'ac')
    @test.it("Given zzab")
    def _():
        user_result = is_valid(last_survivors('zzab'))
        test.assert_equals(fix(user_result), 'c')

@test.describe("Zero Length")
def zero_length():
    @test.it("Given ''")
    def _():
        user_result = is_valid(last_survivors(''))
        test.assert_equals(fix(user_result), '')

@test.describe("New Edge")
def new_edge():
    @test.it("Given xsdlafqpcmjytoikojsecamgdkehrqqgfknlhoudqygkbxftivfbpxhxtqgpkvsrfflpgrlhkbfnyftwkdebwfidmpauoteahyh")
    def _():
        user_result = is_valid(last_survivors('xsdlafqpcmjytoikojsecamgdkehrqqgfknlhoudqygkbxftivfbpxhxtqgpkvsrfflpgrlhkbfnyftwkdebwfidmpauoteahyh'))
        test.assert_equals(fix(user_result), 'acdeghlmnqrvyz')

@test.describe("Random Tests")
def random_tests():
    alph = 'abcdefghijklmnopqrstuvwxyz'
    
    def create_test(l):
        string = ''
        while len(string) < l:
            if len(string) and random.randint(0, 4) == 4:
                string += random.choice(string)
            else:
                string += random.choice(alph)
        return string
    
    def my_solution(string):
        change_letter = lambda s: chr((ord(s)-96)%26+97)
        reg = r"([a-z])(.*?)\1"
        while re.search(reg, string) is not None:
            string = re.sub(reg, lambda m: change_letter(m[1])+m[2], string, count=1)
        return string
    
    for i in range(101):
        _test = create_test(i)
        sol = my_solution(_test)
        @test.it(f"Given {_test}")
        def _():
            user_result = is_valid(last_survivors(_test))
            test.assert_equals(fix(user_result), fix(sol), make_msg(sol, user_result))
