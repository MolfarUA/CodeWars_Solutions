@test.describe('Tests')
def fixed_tests():
    def testing(h, bounce, window, exp):
        #print("Testing: ", h, bounce, window)
        try:
            actual = bouncingBall(h, bounce, window)
        except NameError:
            actual = bouncing_ball(h, bounce, window)
        #print("ACTUAL ", actual)
        #print("EXPECT ", exp)
        #Test.assert_equals(actual, exp)
        test.assert_equals(actual, exp)
        
    @test.it('Fixed Tests')
    def tests():
        testing(2, 0.5, 1, 1)
        testing(3, 0.66, 1.5, 3)
        testing(30, 0.66, 1.5, 15)
        testing(30, 0.75, 1.5, 21)
        testing(30, 0.4, 10, 3)
        testing(40, 0.4, 10, 3)
        testing(10, 0.6, 10, -1)
        testing(40, 1, 10, -1)
        testing(-5, 0.66, 1.5, -1)
        testing(5, -1, 1.5, -1)
        testing(4, 0.25, 1, 1)

    def bouncingBallTests(h, bounce, window):
        if (h <= 0) or (window >= h) or (bounce <= 0) or (bounce >= 1):
            return -1
        seen = -1
        while (h > window):
            seen += 2
            h = h * bounce
        return seen
    
    from random import randint
    @test.it('Random tests')
    def randomtests():
        someheights = [12, 10.5, 144, 233, 15.25, 61, 98, 15.9, 25.8, 41.8, 67,
                       109, 17, 28, 46, 7.5, 12.20, 19, 3, 5,
                       83, 13, 21, 35.5, 57, 92, 14,
                       24, 39, 6.5]
        someBounces = [0.6, 0.6, 0.6, 0.6, 0.6, 1.1, 9, 1, 0.6, 0.6, 0.6,
                       0.75, 0.75, 0.75, 0.75, 0.75, 12.20, 0.75, 0.75,
                       0.83, 0.13, 0.21, 0.35, 0.57, 0.9, 0.14,
                       0.24, 0.39, 0.65, 0.65]
        somewin     = [1.5, 1.5, 1.44, 2.33, 1, 6.1, 9.8, 1.9, 2.8, 4.8, 3,
                       1.09, 1.7, 2.8, 46, 7.5, 12.20, 1.9, 3, 5,
                       0.83, 1.3, 2.1, 3.5, 0.57, 0.92, 1.4,
                       2.4, 3.9, 6.5]
        for x in range(0, 50):
            rn = randint(0, 29)
            f1 = someheights[rn]; 
            f2 = someBounces[rn];
            f3 = somewin[rn]
            sol = bouncingBallTests(f1, f2, f3)
            testing(f1, f2, f3, sol)
