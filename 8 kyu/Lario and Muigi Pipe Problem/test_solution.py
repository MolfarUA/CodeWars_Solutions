import random
import codewars_test as test
from solution import pipe_fix


def check(indata, expected):
    test.it(f"pipe_fix({indata!r})")(
        lambda: test.assert_equals(pipe_fix(indata), expected)
    )


@test.describe("Fixed tests")
def _fixed():
    check([1, 2, 3, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    check([1, 2, 3, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    check([6, 9], [6, 7, 8, 9])
    check([-1, 4], [-1, 0, 1, 2, 3, 4])
    check([1, 2, 3], [1, 2, 3])
    check([2], [2])


@test.describe("Random tests")
def _random():
    for _ in range(100):
        question = sorted(
            random.sample(range(0, 1000), random.randint(50, 100))
        )
        answer = list(range(min(question), max(question) + 1))
        check(question, answer)
