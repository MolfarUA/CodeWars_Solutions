import codewars_test as test 
from solution import count_bits

try:
    count_bits = countBits
except NameError:
    pass

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it("Basic Tests")
    def basic_tests():
        test.assert_equals(count_bits(0), 0)
        test.assert_equals(count_bits(4), 1)
        test.assert_equals(count_bits(7), 3)
        test.assert_equals(count_bits(9), 2)
        test.assert_equals(count_bits(10), 2)
        test.assert_equals(count_bits(26), 3)
        test.assert_equals(count_bits(77231418), 14)
        test.assert_equals(count_bits(12525589), 11)
        test.assert_equals(count_bits(3811), 8)
        test.assert_equals(count_bits(392902058), 17)
        test.assert_equals(count_bits(1044), 3)
        test.assert_equals(count_bits(10030245), 10)
        test.assert_equals(count_bits(183337941), 16)
        test.assert_equals(count_bits(20478766), 14)
        test.assert_equals(count_bits(103021), 9)
        test.assert_equals(count_bits(287), 6)
        test.assert_equals(count_bits(115370965), 15)
        test.assert_equals(count_bits(31), 5)
        test.assert_equals(count_bits(417862), 7)
        test.assert_equals(count_bits(626031), 12)
        test.assert_equals(count_bits(89), 4)
        test.assert_equals(count_bits(674259), 10)
        
@test.describe('Random Tests')
def random_tests():
    
    from random import randint
    
    for _ in range(100):
        num = randint(0, 10**randint(1, 10))
        expected = bin(num).count("1")
        @test.it(f"Testing for count_bits({num})")
        def test_case():
            test.assert_equals(count_bits(num),expected)
