def _test(cases):
    def _triangle(row):
        rev = {'R':1, 'G':2, 'B':3}
        def derive(x, y):
            if x == y: return x
            return ' RGB'[rev[x] ^ rev[y]]
        while len(row) > 1:
            step = 1
            while step * 3 < len(row):
                step *= 3
            row = [derive(v, row[i + step]) for i, v in enumerate(row[:-step])]
        return row[0]
    try:
        for _in, _out in cases:
            test.assert_equals(triangle(_in), _out, allow_raise=False)
    except:
        for _in in cases:
            test.assert_equals(triangle(_in), _triangle(_in), allow_raise=False)

test.describe('Insane Coloured Triangles')

basic_cases = [
    ['B', 'B'],
    ['GB', 'R'],
    ['RRR', 'R'],
    ['RGBG', 'B'],
    ['RBRGBRB', 'G'],
    ['RBRGBRBGGRRRBGBBBGG', 'G']
]
test.it('Basic Tests')
_test(basic_cases)

from random import randint, choice
import numpy as np
def randinput(a, b):
    return ''.join('RGB'[i] for i in np.random.random_integers(0, 2, randint(a, b)))
    
def gen_cases(n, a, b):
    return [randinput(a, b) for _ in range(n)]

small_cases = gen_cases(100, 100, 1000)
test.it('Small Random Tests')
_test(small_cases)

medium_cases = gen_cases(100, 1000, 10000)
test.it('Medium Random Tests')
_test(medium_cases)

large_cases = gen_cases(100, 10000, 100000)
test.it('Large Random Tests')
_test(large_cases)
