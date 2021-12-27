def _Tests() :
    _ranN = lambda a, b : __import__('random').randint(a, b)
    def _ranS(a, b, c, d, e, f) :
        A = lambda x,y : 1/x*y*0.082*(f+273.15)/e
        return A(a,c) + A(b,d)
    test.describe("Tests")
    test.it("Fixed tests")
    test.assert_approx_equals(solution(44, 30, 3, 2, 5, 50), 0.7146511212121212);
    test.assert_approx_equals(solution(60, 20, 10, 30, 10, 100), 5.099716666666667)
    test.it("Random tests")
    for _ in range(0, 100) :
        a =  [_ranN(2, 300), _ranN(2, 300), _ranN(1, 500), _ranN(1, 500), _ranN(2, 100), _ranN(-30, 200)]
        b = a[:]
        c = _ranS(*a)
        d = solution(*b)
        test.assert_approx_equals(d, c)
_Tests()
