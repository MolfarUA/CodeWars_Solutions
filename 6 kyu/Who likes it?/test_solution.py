from random import randrange, sample

import codewars_test as test
from solution import likes


def run_test(names, expected):
    test.it(f"likes({names!r})")(
        lambda: test.assert_equals(likes(names), expected)
    )


@test.describe("Basic tests")
def _basic():
    cases = [
        ([], "no one likes this"),
        (["Peter"], "Peter likes this"),
        (["Jacob", "Alex"], "Jacob and Alex like this"),
        (["Max", "John", "Mark"], "Max, John and Mark like this"),
        (["Alex", "Jacob", "Mark", "Max"], "Alex, Jacob and 2 others like this"),
    ]
    for indata, expected in cases:
        run_test(indata, expected)


@test.describe("Random tests")
def _random():
    sol = lambda n: "no one likes this" if len(n) == 0 else n[0] + " likes this" if len(n) == 1 else n[0] + " and " + n[1] + " like this" if len(n) == 2 else n[0] + ", " + n[1] + " and " + n[2] + " like this" if len(n) == 3 else n[0] + ", " + n[1] + " and " + str(len(n) - 2) + " others like this"
    base = ["Sylia Stingray", "Priscilla S. Asagiri", "Linna Yamazaki", "Nene Romanova", "Nigel", "Macky Stingray", "Largo", "Brian J. Mason", "Sylvie", "Anri", "Leon McNichol", "Daley Wong", "Galatea", "Quincy Rosenkreutz"]
    for _ in range(40):
        size = randrange(len(base))
        names = sample(base, k=size)
        run_test(names, sol(names))
