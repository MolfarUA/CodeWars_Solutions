import codewars_test as test
from itertools import accumulate
from random import randrange
from solution import survivors

@test.describe('Fixed tests')
def fixed_tests():
    fixed_test_cases = [
        ('Length one', [([0], [[0]], []), ([0], [[9]], []), ([2], [[0]], [0]), ([2], [[0,0]], []), ([1], [[0,3]], []), ([5], [[0,0,0,0,4,0,0,0,8,0,0,0,0]], [0])]),
        ('Empty', [([1], [[]], [0]), ([0], [[]], [])]),
        ('Length multiple', [
            ([3,2,1,0], [[1,0,0], [0,2,0,0], [0,9], [8,8]], [0]),
            ([5,1,1,1,0], [[0,0,0,0,4,0,0,0,8,0,0,0,0], [0,0,3], [0,9,0,0,0,0,0], [1,1,1,1,1], [0,2,0,0,6,0]], [0, 3]),
            ([1,1,9,3,4,0,3], [[2,0,2,0,0], [9,9], [4], [6,6,6], [2,0,2,1], [1,3], [0,0]], [1, 2, 3, 4, 6]),
            ([9,9,8,2,6], [[], [0,0,0,5,1], [], [0,0,0,0], [0]], [0, 1, 2, 4])]),
        ('New edge', [([1,1,5,7,2,5,6,2,6,3,2,6,8,6,9,2,8,7], [[], [3,0], [0,0,0,0,8,0,0,0], [0,3,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0], [0], [], [0], [0,0,0,0,0,7,0], [0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0], [0], [5,0,0,0,0,7], [0], [0,0,1,0,0,1,0]], [0, 1, 2, 3, 5, 6, 7, 8, 10, 13, 14, 15, 16, 17])]),
    ]

    for name, test_cases in fixed_test_cases:
        @test.it(name)
        def tests():
            for momentum, powerups, expected in test_cases:
                message = f'survivors({momentum}, {powerups})'
                test.assert_equals(survivors(momentum, powerups), expected, message)

@test.describe('Random tests')
def random_tests():
    def safe(momentum, powerups):
        return all(m > n for n, m in enumerate(accumulate(powerups, initial=momentum)))
    def reference(list_of_momentum, list_of_powerups):
        return [n for n,(momentum,powerups) in enumerate(zip(list_of_momentum, list_of_powerups)) if safe(momentum, powerups)]

    def random_powerup():
        n = randrange(100)
        if n >= 20: return 0
        if n < 1: r = 8, 10
        elif n < 5: r = 5, 8
        elif n < 11: r = 3, 5
        else: r = 1, 3
        return randrange(*r)
    def create_test(length):
        momentum = [randrange(10) for _ in range(length)]
        powerups = [[random_powerup() for _ in range(randrange(10))] for _ in range(length)]
        return momentum, powerups

    test_data = (20, 'Small', (0, 4)), (80, 'Large', (4, 20))

    for num_tests, name, length_range in test_data:
        @test.it(f'{name} test cases')
        def tests():
            for _ in range(num_tests):
                momentum, powerups = create_test(randrange(*length_range))
                message = f'survivors({momentum}, {powerups})'
                expected = reference(momentum, powerups)
                test.assert_equals(survivors(momentum, powerups), expected, message)
