import codewars_test as test

try:
    from solution import openOrSenior as open_or_senior
except ImportError:
    from solution import open_or_senior

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(open_or_senior([(45, 12),(55,21),(19, -2),(104, 20)]),['Open', 'Senior', 'Open', 'Senior'])
        test.assert_equals(open_or_senior([(3, 12),(55,1),(91, -2),(54, 23)]),['Open', 'Open', 'Open', 'Open'])
        test.assert_equals(open_or_senior([(59, 12),(55,-1),(12, -2),(12, 12)]),['Senior', 'Open', 'Open', 'Open'])
        test.assert_equals(open_or_senior([(74, 10),(55, 6),(12, -2),(68, 7)]),['Senior', 'Open', 'Open', 'Open'])
        test.assert_equals(open_or_senior([(16, 23),(56, 2),(56,  8),(54, 6)]),['Open', 'Open', 'Senior', 'Open'])

@test.describe("Random tests")
def random_tests():
    
    from random import randint
    
    solution = lambda data: [ "Senior" if (x[0] >= 55 and x[1] > 7) else "Open" for x in data]
    
    for _ in range(100):
        a = [(randint(10, 90), randint(-2, 26)) for _ in range(randint(3, 8))]
        expected = solution(a)
        @test.it(f"testing for open_or_senior({a})")
        def test_case():
            test.assert_equals(open_or_senior(a[:]),solution(a))
