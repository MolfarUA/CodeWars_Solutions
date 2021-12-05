import codewars_test as test
from solution import comp

@test.describe("Same")
def tests():
    @test.it("Fixed tests")
    def basics():
        a1 = [121, 144, 19, 161, 19, 144, 19, 11]
        a2 = [11*11, 121*121, 144*144, 19*19, 161*161, 19*19, 144*144, 19*19]
        test.assert_equals(comp(a1, a2), True)
        a1 = [4, 4]
        a2 = [1, 31]
        test.assert_equals(comp(a1, a2), False)
        a1 = [121, 144, 19, 161, 19, 144, 19, 11]
        a2 = [11*21, 121*121, 144*144, 19*19, 161*161, 19*19, 144*144, 19*19]
        test.assert_equals(comp(a1, a2), False)
        a1 = [121, 144, 19, 161, 19, 144, 19, 11]
        a2 = [11*11, 121*121, 144*144, 190*190, 161*161, 19*19, 144*144, 19*19]
        test.assert_equals(comp(a1, a2), False)
        a1 = []
        a2 = []
        test.assert_equals(comp(a1, a2), True)
        a1 = []
        a2 = None
        test.assert_equals(comp(a1, a2), False)
        a1 = [121, 144, 19, 161, 19, 144, 19, 11, 1008]
        a2 = [11*11, 121*121, 144*144, 190*190, 161*161, 19*19, 144*144, 19*19]
        test.assert_equals(comp(a1, a2), False)
        a1 = [10000000, 100000000]
        a2 = [10000000 * 10000000, 100000000 * 100000000]
        test.assert_equals(comp(a1, a2), True)
        a1 = [10000001, 100000000]
        a2 = [10000000 * 10000000, 100000000 * 100000000]
        test.assert_equals(comp(a1, a2), False)
        a1 = [2, 2, 3]
        a2 = [4, 9, 9]
        test.assert_equals(comp(a1, a2), False)
        a1 = [2, 2, 3]
        a2 = [4, 4, 9]
        test.assert_equals(comp(a1, a2), True)
        a1 = None
        a2 = []
        test.assert_equals(comp(a1, a2), False)
        test.assert_equals(comp([], [1]), False)
        a1 = [-121, -144, 19, -161, 19, -144, 19, -11]
        a2 = [11*11, 121*121, 144*144, 19*19, 161*161, 19*19, 144*144, 19*19]
        test.assert_equals(comp(a1, a2), True)
        a1 = [42, 42]
        a2 = [42, 42]
        test.assert_equals(comp(a1, a2), False)

from random import randint, shuffle

@test.describe("Same")
def random_tests():
    #-----------------
    def compZt(array1, array2):
        if (array1 == None) or (array2 == None):
            return False
        tmp = sorted([s*s for s in array1])
        return tmp == sorted(array2) 
    #-----------------
    @test.it("Random Tests")
    def random():
        for _ in range(0, 100):
            a1 = [randint(0,100) for i in range(randint(12, 25))]
            a2 = [elem * elem for elem in a1]
            shuffle(a2)
            if randint(0, 1) == 1: 
                a2[randint(0, len(a2)-1)] += randint(1, 25)
            #print("Testing for "+str(a1)+"\nand\n"+str(a2))
            sol = compZt(a1, a2)
            test.assert_equals(comp(a1[:],a2[:]), sol,"It should work with random inputs too")
            
