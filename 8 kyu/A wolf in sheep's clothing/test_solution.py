import codewars_test as test
from solution import warn_the_sheep

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(warn_the_sheep(['sheep', 'sheep', 'sheep', 'sheep', 'sheep', 'wolf', 'sheep', 'sheep']), 'Oi! Sheep number 2! You are about to be eaten by a wolf!')
        test.assert_equals(warn_the_sheep(['sheep', 'wolf', 'sheep', 'sheep', 'sheep', 'sheep', 'sheep']), 'Oi! Sheep number 5! You are about to be eaten by a wolf!')
        test.assert_equals(warn_the_sheep(['wolf', 'sheep', 'sheep', 'sheep', 'sheep', 'sheep', 'sheep']), 'Oi! Sheep number 6! You are about to be eaten by a wolf!')
        test.assert_equals(warn_the_sheep(['sheep', 'wolf', 'sheep']), 'Oi! Sheep number 1! You are about to be eaten by a wolf!')
        test.assert_equals(warn_the_sheep(['sheep', 'sheep', 'wolf']), 'Pls go away and stop eating my sheep')

@test.describe('Random tests')
def random_tests():    
    import random

    def warn_the_sheep_check(queue):
        return ('Pls go away and stop eating my sheep' 
        if queue[-1] == 'wolf'
        else 'Oi! Sheep number ' + str(len(queue) - queue.index('wolf') - 1) +
             '! You are about to be eaten by a wolf!')
            
    for i in range(0, 100):
        n = random.randint(1, 10)
        queue = ['sheep'] * n
        queue[random.randint(1, n) - 1] = 'wolf'
        expected = warn_the_sheep_check(queue)
        @test.it(f"testing for warn_the_sheep({queue})")
        def test_case():
            test.assert_equals(warn_the_sheep(queue[:]), expected)
