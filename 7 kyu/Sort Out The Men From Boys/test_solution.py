import codewars_test as test
from solution import men_from_boys

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(men_from_boys([7,3,14,17]), [14,17,7,3])
        test.assert_equals(men_from_boys([2,43,95,90,37]), [2,90,95,43,37])
        test.assert_equals(men_from_boys([20,33,50,34,43,46]), [20,34,46,50,43,33])
        test.assert_equals(men_from_boys([82,91,72,76,76,100,85]), [72,76,82,100,91,85])
        test.assert_equals(men_from_boys([2,15,17,15,2,10,10,17,1,1]), [2,10,17,15,1])
        test.assert_equals(men_from_boys([-32,-39,-35,-41]), [-32,-35,-39,-41])
        test.assert_equals(men_from_boys([-64,-71,-63,-66,-65]), [-66,-64,-63,-65,-71])
        test.assert_equals(men_from_boys([-94,-99,-100,-99,-96,-99]), [-100,-96,-94,-99])
        test.assert_equals(men_from_boys([-53,-26,-53,-27,-49,-51,-14]), [-26,-14,-27,-49,-51,-53])
        test.assert_equals(men_from_boys([-17,-45,-15,-33,-85,-56,-86,-30]), [-86,-56,-30,-15,-17,-33,-45,-85])
        test.assert_equals(men_from_boys([12,89,-38,-78]), [-78,-38,12,89])
        test.assert_equals(men_from_boys([2,-43,95,-90,37]), [-90,2,95,37,-43])
        test.assert_equals(men_from_boys([82,-61,-87,-12,21,1]), [-12,82,21,1,-61,-87])
        test.assert_equals(men_from_boys([63,-57,76,-85,88,2,-28]), [-28,2,76,88,63,-57,-85])
        test.assert_equals(men_from_boys([49,818,-282,900,928,281,-282,-1]), [-282,818,900,928,281,49,-1])

@test.describe("Random tests")
def _():
    
    from random import randint
    from functools import cmp_to_key
    
    sol=lambda arr: sorted(list(set(arr)),key=cmp_to_key(lambda a,b: (b-a if a%2 else a-b) if abs(a%2)==abs(b%2) else -(b%2)))
    
    for _ in range(40):
        arr=[randint(-(10**randint(1,3)),10**randint(1,3)) for q in range(randint(4,40))]
        expected = sol(arr)
        @test.it(f"Testing for men_from_boys({arr})")
        def _():
            test.assert_equals(men_from_boys([]+arr), expected)
