import codewars_test as test

@test.describe("race")
def tests():
    @test.it("basic tests")
    def basics():
        test.assert_equals(race(720, 850, 70), [0, 32, 18])
        test.assert_equals(race(80, 91, 37), [3, 21, 49])
        test.assert_equals(race(80, 100, 40), [2, 0, 0])
        test.assert_equals(race(720, 850, 37), [0, 17, 4])
        test.assert_equals(race(720, 850, 370), [2, 50, 46])
        test.assert_equals(race(120, 850, 37), [0, 3, 2])
        test.assert_equals(race(820, 850, 550), [18, 20, 0])
        test.assert_equals(race(820, 81, 550), None)    

from random import randint

@test.describe("race")
def random_tests():
    #-----------------
    def sol12348(v1, v2, g):
        d = v2 - v1
        if (d <= 0):
            return None
        h = g // d
        r = g % d
        mn = r * 60 // d
        s = (r * 60 % d) * 60 // d
        return [h, mn, s]
    #-----------------
    @test.it("Random tests")
    def random():
        #print("100 random tests ****************** ")
        i = 0
        nb = 100
        while (i < nb):
            v1 = randint(50, 750)
            v2 = randint(v1 + 20, 850)
            g = randint(60, 150)
            test.assert_equals(race(v1, v2, g), sol12348(v1, v2, g))
            i += 1
