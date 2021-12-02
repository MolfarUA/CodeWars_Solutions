def _custom_assert_equals(actual, expected, message=None):
    try:
        test.assert_equals(actual, expected, message)
    except:
        pass

def _fixed_test(test_data):
    for n, l, test_output in test_data:
        _custom_assert_equals(permutation_free(n, l), test_output,
            'Testing for n={}, l={}'.format(n, l))

test.it('Basic Tests')
test_data = [
    (3, 3, 21), (3, 4, 51), (3, 5, 123), (3, 10, 10089),
    (4, 4, 232), (4, 5, 856), (4, 6, 3160),
    (5, 5, 3005), (5, 6, 14545), (5, 10, 8001745)
]
_fixed_test(test_data)

test.it('Large Tests')
test_data = [
    (3, 99, 11247963), (3, 100, 7248437),
    (4, 99, 3278551), (4, 100, 3429793),
    (5, 99, 9156527), (5, 100, 10904326)
]
_fixed_test(test_data)

def _random_test(test_data):
    from itertools import product
    from collections import defaultdict
    MOD = 12345787
    def _solution(n, l):
        counts = dict()
        for pattern in product(range(n), repeat=n-1):
            counts[pattern] = 1
        for _ in range(n, l + 1):
            next_counts = defaultdict(int)
            for key, value in counts.items():
                for next_digit in range(n):
                    next_key = key[1:] + (next_digit,)
                    if len(set(key + (next_digit,))) != n:
                        next_counts[next_key] = (next_counts[next_key] + value) % MOD
            counts = next_counts
        return sum(counts.values()) % MOD
        
    for n, l in test_data:
        _custom_assert_equals(permutation_free(n, l), _solution(n, l),
            'Testing for n={}, l={}'.format(n, l))

from random import randint
test.it('Random Tests')
test_data = [(randint(3, 5), randint(5, 100)) for _ in range(84)]
_random_test(test_data)
