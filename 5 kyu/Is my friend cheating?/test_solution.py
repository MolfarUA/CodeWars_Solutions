import codewars_test as test
        
@test.describe("Cheating Friend")
def tests():   
    def testing(n, exp):
        try:
            actual = removNb(n)
        except NameError:
            actual = remov_nb(n)
        test.assert_equals(actual, exp)
    @test.it("Fixed tests")
    def basics():
        testing(26, [(15, 21), (21, 15)])
        testing(100, [])
        testing(101, [(55, 91), (91, 55)])
        testing(102, [(70, 73), (73, 70)])
        testing(110, [(70, 85), (85, 70)])
        testing(1006, [(546, 925), (925, 546)])
        testing(103, [])
        testing(446, [(252, 393), (393, 252)])
        testing(846, [(498, 717), (717, 498)])
        testing(1000003, [(550320, 908566), (559756, 893250), (893250, 559756), (908566, 550320)])
        testing(1000008, [(677076, 738480), (738480, 677076)])
        testing(21751, [(13266, 17830), (17830, 13266)])

from random import randint
            
@test.describe("Cheating Friend")
def random_tests():
    def testing(n, exp):
        #print("Testing: ", n)
        try:
            actual = removNb(n)
        except NameError:
            actual = remov_nb(n)
        #print("ACTUAL ", actual)
        #print("EXPECT ", exp)
        test.assert_equals(actual, exp)
    #-----------------
    def removNbTest(n):
        s = int(n * (n +1) / 2)
        limit = int(n / 2)
        res = []
        for a in range(limit, n + 1):
            b = s - a
            if (b % (a + 1) == 0):
                res.append( (a, int(b / (a + 1)) ))            
        res = sorted(res, key = lambda x : x[0])
        return res    
    #-----------------
    @test.it("Random Tests")
    def randomTests():
        someVals = [210, 211, 213, 220, 226, 231, 232, 249, 250, 257, 262, 
                    263, 265, 266, 282, 290, 297, 300, 304, 311, 312, 314, 
                    325, 340, 341, 346, 358, 362, 369, 378, 381, 386, 394
                   ]
        for x in range(0, 15):
            rn = randint(0, 29)
            f1 = someVals[rn]
            sol = removNbTest(f1)
            testing(f1, sol)
        print("--------------")
        for x in range(0, 35):
            r = randint(100, 600)
            rn = r * (r+1) // 2
            sol = removNbTest(rn)
            testing(rn, sol)
