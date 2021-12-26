from solution import approx_equals
import codewars_test as test
from random import choice, expovariate, gauss, randrange, shuffle, uniform


@test.describe('Fixed tests')
def fixed_tests():
    data = (
        (175.9827, 82.25, False),
        (-156.24037, -156.24038, True),
        (123.2345, 123.234501, True),
        (1456.3652, 1456.3641, False),
        (-1.234, -1.233999, True),
        (98.7655, 98.7654999, True),
        (-7.28495, -7.28596, False))

    @test.it('testing approx_equals')
    def tests():
        for (a, b, eq) in data:
            test.assert_equals(approx_equals(a, b), eq)

@test.describe('Random tests')
def random_tests():
    def true_data():
        a = gauss(0.0, 100000.0)
        b = a + uniform(-0.00099, 0.00099)
        return a, b, True
    def false_data():
        a = gauss(0.0, 100000.0)
        b = a + 0.00101 + expovariate(1000.0)
        if randrange(2):
            a, b = b, a
        return a, b, False
    def far_data():
        a = b = gauss(0.0, 100000.0)
        while abs(a-b) < 0.00101:
            b = gauss(0.0, 100000.0)
        return a, b, False
    def round_data():
        a = 0
        while a % 2 == 0:
            a = randrange(-100000, 100000)
        a /= 2000
        b = a + choice((-1,1)) * uniform(0.000001, 0.0001)
        if randrange(2):
            a, b = b, a
        return a, b, True
        
    data = [true_data() for _ in range(30)] + [false_data() for _ in range(30)] + \
        [far_data() for _ in range(20)] + [round_data() for _ in range(20)]
    shuffle(data)
    
    @test.it('testing approx_equals')
    def tests():
        for (a, b, eq) in data:
            test.assert_equals(approx_equals(a, b), eq)
