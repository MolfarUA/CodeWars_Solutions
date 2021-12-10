from solution import square_sums
import codewars_test as test
from random import *

no_solutions = set(range(2, 25)) - {15, 16, 17, 23}


def verify(n):
    solution = square_sums(n)
    
    if n in no_solutions:
        test.expect(solution == False, f"No solution for {n}")
        
    elif not isinstance(solution, list):
        test.fail(f"fA solution exists for {n}!")
    
    else:
        s    = set(solution)
        allN = set(range(1, n + 1))
        
        missing = allN-s
        tooMuch = s-allN
        
        if len(solution)!=len(s): return test.fail("The output shouldn't contain duplicates")
        if missing:               return test.fail(f"The output is missing some numbers: {missing}")
        if tooMuch:               return test.fail(f"The output has out of range numbers: {tooMuch}")
        
        square_validation = all( (n + solution[e])**.5 % 1 == 0
                                 for e,n in enumerate(solution[:-1], 1) )
        test.expect(square_validation, "Subsequent numbers are not square!")


@test.describe("Square sums...")
def _():
    @test.it("Basic tests")
    def _():
        verify(5)
        verify(15)
        verify(23)
        verify(37)
    
    @test.it("Mid-size numbers")
    def _():
        for i in range(46, 145): verify(i)
        
    @test.it("Final tests (random)")
    def _():  
        RANDOMS = choices(list(range(145,1001)), k=280)
        for n in RANDOMS: verify(n)
    
