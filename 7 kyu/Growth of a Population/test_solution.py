import codewars_test as test
from solution import nb_year

@test.describe("nb_year")
def tests():
    @test.it("basic tests")
    def basics():
        test.assert_equals(nb_year(1500, 5, 100, 5000), 15)
        test.assert_equals(nb_year(1500000, 2.5, 10000, 2000000), 10)
        test.assert_equals(nb_year(1500000, 0.25, 1000, 2000000), 94)
        test.assert_equals(nb_year(1500000, 0.25, -1000, 2000000), 151)
        test.assert_equals(nb_year(1500000, 0.25, 0, 2000000), 116)
        test.assert_equals(nb_year(1500000, 0.0, 10000, 2000000), 50)
        test.assert_equals(nb_year(1000, 2.0, 50, 1214), 4)
        
from random import randint
from math import floor

@test.describe("nb_year")
def random_tests():
    #-----------------
    def nb_year1938(p0, percent, aug, p):
        i = 1
        mult = 1 + percent / 100.0
        prev = p0
        while (prev < p):
            ne = floor((prev * mult + aug))
            prev = ne
            i += 1
        return (i - 1)
    #-----------------
    @test.it("Random tests")
    def random():
        for _ in range(0, 200):
            p0 = randint(10000, 15000000)
            percent = randint(50, 1000) / 100.0
            aug = int(p0 / 200.0)
            k = randint(5, 100)
            p = p0 + k * aug
            sol = nb_year1938(p0, percent, aug, p)
            test.assert_equals(nb_year(p0, percent, aug, p), sol)
