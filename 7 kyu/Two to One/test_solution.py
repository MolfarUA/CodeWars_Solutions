import codewars_test as test
    
@test.describe("longest")
def tests():
    @test.it("basic tests")
    def basics():
        test.assert_equals(longest("aretheyhere", "yestheyarehere"), "aehrsty")
        test.assert_equals(longest("loopingisfunbutdangerous", "lessdangerousthancoding"), "abcdefghilnoprstu")
        test.assert_equals(longest("inmanylanguages", "theresapairoffunctions"), "acefghilmnoprstuy")
        test.assert_equals(longest("lordsofthefallen", "gamekult"), "adefghklmnorstu")
        test.assert_equals(longest("codewars", "codewars"), "acdeorsw")
        test.assert_equals(longest("agenerationmustconfrontthelooming", "codewarrs"), "acdefghilmnorstuw")

from random import randint

@test.describe("longest")
def random_tests():
    #-----------------
    def do_ex(k):
        i, res = 0, ""
        while (i < 15):
            res += chr(randint(97+k, 122)) * randint(1, 10)
            i += 1
        return res
    def longest_sol(a1, a2):
        return "".join(sorted(set(a1 + a2)))
    #-----------------
    @test.it("Random tests")
    def random():
        for _ in range(0, 200):
            s1 = do_ex(randint(0, 10))
            s2 = do_ex(randint(0, 8))
            sol = longest_sol(s1, s2)
            test.assert_equals(longest(s1, s2), sol)
