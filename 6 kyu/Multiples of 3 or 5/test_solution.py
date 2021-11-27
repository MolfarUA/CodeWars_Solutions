import random
import codewars_test as test
from solution import solution

@test.describe("Fixed tests")
def fixed_tests():
    
    test_cases = [
        (4, 3), (6, 8), (16, 60), (3, 0), (5, 3), (15, 45), (0, 0), (-1, 0),
        (10, 23), (20, 78), (200, 9168)
    ]
    
    for input, expected in test_cases:
        @test.it(f"Should return {expected} for n={input}")
        def fixed():
            test.assert_equals(solution(input), expected)
            
@test.describe("Random tests")
def random_tests():

    def referenceSolution(number):

        if number < 0: return 0
    
        def sum(max, d):
            n = max // d
            s = n * (n + 1) * d // 2
            return s

        number -= 1
        return sum(number, 3) + sum(number, 5) - sum(number, 3 * 5)    
    
    def generateCases(generator, count):
        return [generator() for _ in range(count)]
    
    def generateDiv3():
        n = random.randint(1, 100) * 3
        return [n, n+1]
    
    def generateDiv5():
        n = random.randint(1, 100) * 5
        return [n, n+1]
    
    def generateDiv15():
        n = random.randint(1, 100) * 15
        return [n, n+1]
    
    def generateNegative():
        n = random.randint(1, 100) * -1
        return [n]
    
    inputs = generateCases(generateDiv3, 5) +\
             generateCases(generateDiv5, 5) +\
             generateCases(generateDiv15, 5) +\
             generateCases(generateNegative, 5)
    
    test_cases = [(n, referenceSolution(n)) for sublist in inputs for n in sublist]
    random.shuffle(test_cases)
    
    @test.it("Random tests")
    def random_tests():
        
        for input, expected in test_cases:
            actual = solution(input)
            test.assert_equals(actual, expected, f"Incorrect answer for n={input}")
