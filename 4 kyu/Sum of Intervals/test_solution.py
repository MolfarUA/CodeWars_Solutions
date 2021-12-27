from solution import sum_of_intervals
import codewars_test as test

@test.describe("Fixed tests")
def fixed_tests():
    @test.it("Tests")
    def it_1():
        test.assert_equals(sum_of_intervals([(1, 5)]), 4)
        test.assert_equals(sum_of_intervals([(1, 5), (6, 10)]), 8)
        test.assert_equals(sum_of_intervals([(1, 5), (1, 5)]), 4)
        test.assert_equals(sum_of_intervals([(1, 4), (7, 10), (3, 5)]), 7)

@test.describe("Random tests")
def random_tests():
    from random import randint

    def reference(a):
        a = sorted(a)
        r, last = 0, a[0][0]
        for x, y in a:
            if y <= last: continue
            m = max(x, last)
            r += y - m
            last = y
        return r
    
    @test.it("Tests")
    def it_1():
        for _ in range(100):
            a = []
            for _ in range(randint(1, 20)):
                x = randint(-500, 499)
                y = randint(x + 1, 500)
                a.append((x, y))
            expected = reference(a)
            test.assert_equals(sum_of_intervals(a), expected)
