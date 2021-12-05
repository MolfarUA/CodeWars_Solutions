try:
    number_to_ordinal = numberToOrdinal
except NameError:
    pass

@test.it('Fixed tests')
def fixed_tests():
    test_cases = [(0, '0'),
              (11, '11th'),
              (12, '12th'),
              (13, '13th'),
              (21, '21st'),
              (22, '22nd'),
              (23, '23rd'),
              (101, '101st'),
              (111, '111th'),
              (112, '112th'),
              (113, '113th'),
              (500, '500th'),
              (1001, '1001st'),
              (9993, '9993rd')]

    @test.it('Tests')
    def it_1():
        for number, ordinal in test_cases:
            test.assert_equals(number_to_ordinal(number), ordinal)

@test.describe('Random tests')
def random_tests():
    from random import shuffle

    def solution(n):
        if n == 0:
            return '0'
        if not 10 < n % 100 < 14:
            last_digit = n % 10
            if last_digit == 1:
                return str(n) + 'st'
            elif last_digit == 2:
                return str(n) + 'nd'
            elif last_digit == 3:
                return str(n) + 'rd'
        return str(n) + 'th'

    @test.it('Tests')
    def it_1():
        a = list(range(0, 10000))
        shuffle(a)
        for x in a:
            user, result = number_to_ordinal(x), solution(x)
            if user != result:
                test.assert_equals(user, result)
                break
        else:
            test.pass_()
