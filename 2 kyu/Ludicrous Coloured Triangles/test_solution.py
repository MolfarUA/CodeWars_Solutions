from solution import triangle
import codewars_test as test
import random
import itertools


@test.describe('Welcome to this kata! Let\'s start with some short, static input :-)')
def _():
    basic_cases = [
        ['B', 'B'],
        ['GB', 'R'],
        ['RRR', 'R'],
        ['RGBG', 'B'],
        ['RBRGBRB', 'G'],
        ['RBRGBRBGGRRRBGBBBGG', 'G'],
        ['BGRGRBGBRRBBGRBGBBRBRGBRG', 'B'],
        ['GRBGRRRBGRBGRGBRGBRBRGBRRGRBGRGBB', 'R'],
        ['RBGRBGBRGBRBRGGRBBGRBGBRBBGRBGGBRBGBBGRBGBRGRBGRBB', 'G'],
        ['BGBGRBGRRBGRBGGGRBGRGBGRRGGRBGRGRBGBRGBGBGRGBGBGBGRRBRGRRGBGRGBRGRBGRBGRBBGBRGRGRBGRGBRGBBRGGBRBGGRB', 'G'],
    ]
    @test.it('So Far, So Good')
    def _():
        for input, output in basic_cases:
            test.assert_equals(triangle(input), output)

@test.describe('Random tests')
def _():

    def answer(row):
        def combine(a, b):
            """Returns the result of the combination of two colours."""
            if a == b:
                return a
            elif a != 'R' and b != 'R':
                return 'R'
            elif a != 'G' and b != 'G':
                return 'G'
            else:
                return 'B'

        def pow3(n):
            """Returns the greatest power of 3 less than or equal to n."""
            i, j = 1, 1
            while i <= n:
                j = i
                i *= 3
            return j

        def triple(a, b, c):
            """Computes the result for an input of length 3.  Skips the two
               intermediate colours you'd otherwise need."""
            if a == b:
                return c
            elif b == c:
                return a
            elif a != c:
                return b
            elif a != 'R' and b != 'R':
                return 'R'
            elif a != 'G' and b != 'G':
                return 'G'
            else:
                return 'B'

        def rec(level, offset):
            """Compute the offset-th colour on the level-th row"""
            if level == 0:
                # get the colour from input, but convert to int first.
                return row[offset]
            step = pow3(level)
            if step * 2 > level:
                return combine(rec(level-step, offset), rec(level-step, offset+step))
            else:
                twostep = step * 2
                return triple(rec(level - twostep, offset),
                              rec(level - twostep, offset + step),
                              rec(level - twostep, offset + twostep))

        return '' if row == 0 else rec(len(row) - 1, 0)

    def generate(n, maxlen, minlen=None):
        pool_size = 8192
        chunk_len = 8192
        combo_len = 8

        if not hasattr(generate, '_pool_cache'):
            generate._pool_cache = []
            combos = [''.join(l) for l in itertools.product(*(["RGB"] * combo_len))]
            for i in range(pool_size):
                # random.choices is new in Python 3.6
                generate._pool_cache.append(''.join(random.choices(combos, k=chunk_len//combo_len)))

        if minlen is None:
            minlen = maxlen // 10 * 8

        res = []
        for i in range(n):
            a = []
            length = random.randrange(minlen, maxlen)
            chunks = length // chunk_len + 2
            for i in range(chunks):
                a.append(random.choice(generate._pool_cache))
            startPoint = random.randrange(chunk_len)
            res.append(''.join(a)[startPoint:startPoint+length])
        return res
    
    @test.describe('Piece Of Cake... Please try these longer, fixed-length strings!')
    def _():
        sizes = [
            [512  ,       '500'],
            [1024 ,     '1 000'],
            [7907 ,     '5 000'],
            [14641,    '10 000'],
            [3**9,     '20 000'],
            [65536,    '50 000'],
        #   [3**11,   '100 000'],
        #   [3**12,   '500 000'],
        #   [3**13, '1 000 000'],
        ]
        for size, size_str in sizes:
            fixed = generate(1, size+1, size)[0]
            @test.it('Around %s chars' % size_str)
            def _():
                exp = answer(fixed)
                test.assert_equals(triangle(fixed), exp)

    @test.describe('Hardcore... Now what about a few batches of large random strings?')
    def _():
        #test.it("I'm Too Young To Die (up to 100 000 chars)")
        #sample = generate(256, 10**5)
        #for s in sample:
        #  test.assert_equals(triangle(s), answer(s))

        #test.it('Hurt Me Plenty (up to 1 000 000 chars')
        #sample = generate(64, 10**6)
        #for s in sample:
        #  test.assert_equals(triangle(s), answer(s))

        @test.it('Ultra Violence (up to 10 000 000 chars)')
        def _():
            sample = generate(16, 10**7)
            for s in sample:
                exp = answer(s)
                test.assert_equals(triangle(s), exp)

        @test.it('Nightmare (up to 100 000 000 chars)')
        def _():
            sample = generate(4, 10**8)
            print(len(sample))
            for s in sample:
                exp = answer(s)
                test.assert_equals(triangle(s), exp)

        @test.it('Never Gonna Give You Up (up to 1 000 000 000 chars)')
        def _():
            sample = generate(1, 10**9)
            print(len(sample))
            for s in sample:
                exp = answer(s)
                test.assert_equals(triangle(s), exp)
                
