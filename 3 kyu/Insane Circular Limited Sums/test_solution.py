def _test(max_n, max_fn, result=None):
    MOD = 12345787
    def dot(vec1, vec2):
        return sum(a * b for a, b in zip(vec1, vec2)) % MOD
    def mat_vec_mul(mat, vec):
        return [dot(row, vec) for row in mat]
    def matmul(mat1, mat2):
        mat2_t = list(zip(*mat2))
        return [[dot(row1, col2) for col2 in mat2_t] for row1 in mat1]
    def matexp(mat, exp):
        dim = len(mat)
        ans = [[row == col for col in range(dim)] for row in range(dim)]
        for bit in bin(exp)[2:]:
            ans = matmul(ans, ans)
            if bit == '1':
                ans = matmul(ans, mat)
        return ans
    def subproblem(mat, f1, max_fn):
        counts = [1] * (max_fn + 1 - f1) + [0] * f1
        vec = mat_vec_mul(mat, counts)
        return dot(vec, counts)
    def main_cls(n, max_fn):
        mat = [[row + col <= max_fn for col in range(max_fn + 1)]
            for row in range(max_fn + 1)]
        mat = matexp(mat, n)
        return sum(subproblem(mat, f1, max_fn) for f1 in range(max_fn + 1)) % MOD
    def _solution(max_n, max_fn):
        if max_n == 1:
            return max_fn // 2 + 1
        return main_cls(max_n - 2, max_fn)
    if result is None:
        result = _solution(max_n, max_fn)
    #print(max_n, max_fn, result)
    test.assert_equals(insane_cls(max_n, max_fn), result,
        'Wrong result for max_n = {}, max_fn = {}'.format(max_n, max_fn))

test.it('Basic Tests')
test_data = [
    (1, 1, 1), (2, 1, 3), (3, 1, 4), (4, 1, 7), (5, 1, 11),
    (1, 2, 2), (2, 2, 6), (3, 2, 11), (4, 2, 26), (5, 2, 57)
]
for max_n, max_fn, result in test_data:
    _test(max_n, max_fn, result)
    
test.it('Large Tests')
for max_n in (10, 21, 34, 52, 75, 100):
    for max_fn in range(1, 6):
        _test(max_n, max_fn)

test.it('Larger Tests')
for max_n in range(10 ** 8 + 1234567, 10 ** 9, 10 ** 8 - 200000):
    for max_fn in range(1, 11):
        _test(max_n, max_fn)

from random import randint
test.it('Random Tests')
for _ in range(100):
    max_n_digits = randint(3, 9)
    max_n = randint(10 ** (max_n_digits - 1), 10 ** max_n_digits)
    max_fn = randint(1, 10)
    _test(max_n, max_fn)
