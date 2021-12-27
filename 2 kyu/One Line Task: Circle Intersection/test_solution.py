from solution import circleIntersection
import codewars_test as test
from random import *

@test.describe("Basic Tests")
def v():
    @test.it("It should works for basic tests.")
    def f():
        test.assert_equals(circleIntersection([0, 0],[7, 0],5),14)
        test.assert_equals(circleIntersection([0, 0],[0, 10],10),122)
        test.assert_equals(circleIntersection([5, 6],[5, 6],3),28)
        test.assert_equals(circleIntersection([-5, 0],[5, 0],3),0)
        test.assert_equals(circleIntersection([10, 20],[-5, -15],20),15)
        test.assert_equals(circleIntersection([-7, 13],[-25, -5],17),132)
        test.assert_equals(circleIntersection([-20, -4],[-40, 29],7),0)
        test.assert_equals(circleIntersection([38, -18],[46, -29],10),64)
        test.assert_equals(circleIntersection([-29, 33],[-8, 13],15),5)
        test.assert_equals(circleIntersection([-12, 20],[43, -49],23),0)

@test.describe("Random tests")
def check():
    @test.it("100 Random Tests --- Testing for correctness of solution")
    def A():
        import math
        def ss(a,b,r):
            d,R=math.hypot(b[0]-a[0],b[1]-a[1]),2*r
            return int(d<R and R*r*math.acos(d/R)-d*math.sqrt(R*R-d*d)/2)
        for i in range(0,100):
            a = randint(0,1000000)
            b = randint(0,1000000)
            c = randint(0,1000000)
            d = randint(0,1000000)
            r = randint(0,1000000)
            x = [a,b]
            y = [c,d]
            test.assert_equals(circleIntersection(x , y , r) , ss(x , y , r))
