from solution import add_letters
import codewars_test as test

from random import randint
from functools import reduce

@test.describe("Fixed tests")
def fixed_tests():
    tests = [
        (['a', 'b', 'c'], 'f'),
        (['z'], 'z'),
        (['a', 'b'], 'c'),
        (['c'], 'c'),
        (['z', 'a'], 'a'),
        (['y', 'c', 'b'], 'd'),
        ([], 'z')
    ]
    for i, o in tests:
        str = ', '.join(['"' + s + '"' for s in i])
        @test.it("add_letters(" + str + ")")
        def fixed_test():
            test.assert_equals(add_letters(*i), o)

@test.describe("Random tests")
def random_tests():
    sol = lambda *letters: 'z' if len(letters) == 0 else reduce(lambda x, _: 'a' if x == 'z' else chr(ord(x) + 1), range(reduce(lambda acc, item: acc + (ord(item) - 96), letters, -1)), 'a')
    for t in range(100):
        arr = [chr(randint(97, 122)) for i in range(randint(1, 10))]
        str = ', '.join(['"' + s + '"' for s in arr])
        @test.it("add_letters(" + str + ")")
        def random_test():
            test.assert_equals(add_letters(*arr), sol(*arr))
