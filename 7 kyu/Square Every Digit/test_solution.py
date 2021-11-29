import codewars_test as test
from solution import square_digits

@test.describe("Fixed tests: ")
def fixed_tests():
    
    cases = [(3212, 9414), (2112, 4114), (0,0)]
    
    for input, expected in cases:
        @test.it(f"testing for square_digits({input})")
        def basic_test_cases():
            test.assert_equals(square_digits(input), expected)
            
@test.describe("Random Tests: ")
def random_tests():
    
    from random import randint
    
    def square_digits_test(number):
        new_number = ""
        for digit in str(number):
            digit = int(digit) ** 2
            new_number += str(digit)
        return int(new_number)
           
    for item in range(1, 101):
        randomtest = int(str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9)))
        @test.it(f"testing for square_digits({randomtest})")
        def test_case():
            test.assert_equals(square_digits(randomtest), square_digits_test(randomtest))
