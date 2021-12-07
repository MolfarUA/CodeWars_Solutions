import random

try:
    # backwards compatibility
    double_integer = doubleInteger
except NameError:
    pass

@test.describe('Tests')
def tests():
    @test.it('Sample Test Case')
    def sample_test_case():
        test.assert_equals(double_integer(2), 4);
        test.assert_equals(double_integer(4), 8);
        test.assert_equals(double_integer(-10), -20);
        test.assert_equals(double_integer(0), 0);
        test.assert_equals(double_integer(100), 200);
    @test.it('Random Test Case')
    def random_test_case():
        for cwtests in range(0,100):
            qwe1 = random.randint(-200,200)
            qwe2 = qwe1
            print("Testing for double_integer(" + str(qwe2) + ")")
            test.assert_equals(double_integer(qwe1), qwe2*2);
