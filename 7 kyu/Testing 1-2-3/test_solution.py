from random import randint

import codewars_test as test
from solution import number

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it("Should handle empty arrays")
    def _():
        test.assert_equals(number([]), [])
        
    @test.it('Should handle ["a", "b", "c"] as ["1: a", "2: b", 3: c"]')
    def _():
        test.assert_equals(number(["a", "b", "c"]), ["1: a", "2: b", "3: c"])
        
    @test.it('Should handle all empty lines')
    def _():
        test.assert_equals(number(["", "", "", "", ""]), ["1: ", "2: ", "3: ", "4: ", "5: "])

    @test.it('Should handle some empty lines')
    def _():
        test.assert_equals(number(["", "b", "", "", ""]), ["1: ", "2: b", "3: ", "4: ", "5: "])

@test.describe('Should handle random test case')
def _():
    for i in range(100):
        arr = [chr(randint(48,122)) for i in range(100)]
        expected = [str(key+1)+": "+val for (key,val) in enumerate(arr)]
        @test.it(f"testing for number({arr})")
        def test_case():
            test.assert_equals(number(arr[:]),expected)
