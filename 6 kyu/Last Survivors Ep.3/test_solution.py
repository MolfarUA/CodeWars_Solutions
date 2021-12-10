import codewars_test as test
from itertools import chain
from random import choice, randrange
from string import ascii_lowercase as letters
from solution import last_survivors

@test.describe('Fixed tests')
def fixed_tests():
    fixed_test_cases = [
        ('Basic', [
            ([' ','z'], [1], ''),
            (['abc','   ',' a '], [0,4,1], 'a'),
            (['zj','zj'], [9,0], 'jj'),
            (['d',' ',' ',' ',' '], [1], ''),
            (['help us we are dying'], [2,0,2,1,2,0,2,1,2,0,2,1,2,0,2,1,2,0,2,1], 'eeeiu'),
            (['to   ','  tal','it   ','  ari','an   ','  ism'], [7,6,4,2,1], 'ail'),
            ([' ',' '], [0], ''),
        ]),
        ('Empty', [
            ([], [1,2,3,4], ''),
            (['','','',''], [], ''),
            ([], [1,2,3], ''),
        ]),
        ('Large', [
            (['w bby   n d  r   s v',' ff  i vd     s     ',' e   glv          s ','ug k  ob  am   t   a',' pmalfiih hw     ku ','oj   w    w  rbe n  ','d   q   iq  i k    y','jn     g xn  b      ','     navd   w      q'], [2,4,4,2,1,4,7,4,2,1,7,6,7,0,2,5,0,5,6,3], 'bbdefhilnoqrrsuvvvwy'),
        ])
    ]
    for name, test_cases in fixed_test_cases:
        @test.it(f'{name} tests')
        def tests():
            for arr, nums, expected in test_cases:
                actual = last_survivors(arr, nums)
                if isinstance(actual, str):
                    actual = ''.join(sorted(actual))
                test.assert_equals(actual, expected, f'last_survivors({arr!r}, {nums!r})')

@test.describe('Random tests')
def random_tests():
    def reference(arr, nums):
        return ''.join(sorted(chain(*([*filter(' '.__ne__, c)][n:] for c, n in zip(zip(*reversed(arr)), nums)))))

    def create_test(width, height, nums_range):
        arr = [''.join((' ' if randrange(5) < 2 else choice(letters)) for _ in range(width)) for _ in range(height)]
        nums = [randrange(nums_range) for _ in range(width)]
        return arr, nums

    test_data = (20, 'Small', 8, 4), (80, 'Large', 20, 10)

    for num_tests, name, max_width, max_height in test_data:
        @test.it(f'{name} tests')
        def tests():
            for _ in range(num_tests):
                arr, nums = create_test(randrange(1,1+max_width), randrange(1,1+max_height), max_height)
                message = f'last_survivors({arr!r}, {nums!r})'
                expected = reference(arr, nums)
                actual = last_survivors(arr, nums)
                if isinstance(actual, str):
                    actual = ''.join(sorted(actual))
                test.assert_equals(actual, expected, message)
