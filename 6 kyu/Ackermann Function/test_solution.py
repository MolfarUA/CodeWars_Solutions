import codewars_test as test
from solution import Ackermann
from random import randint

@test.describe('Ackermann')
def tests():
    @test.it('Fixed Tests')
    def test_cipher_text():
        test.assert_equals(Ackermann(1, 1),  3)
        test.assert_equals(Ackermann(4, 0), 13)
        test.assert_equals(Ackermann(3, 3), 61)
