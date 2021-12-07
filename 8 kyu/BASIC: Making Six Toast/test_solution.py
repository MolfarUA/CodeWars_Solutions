import codewars_test as test
from solution import six_toast

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(six_toast(15), 9)
        test.assert_equals(six_toast(6), 0)
        test.assert_equals(six_toast(3), 3)

@test.describe("Random Tests")
def random_tests():
       
    from random import randint, shuffle, choice 
    
    def mysix_toast(num):
        return abs(num-6)
              
    for x in range(0, 300):
        r = randint(0,100000000)
        res = mysix_toast(r)
        @test.it(f"testing for six_toast({r})")
        def test_case():
            test.assert_equals(six_toast(r), res)
      
  

# Test.describe("Random tests") do
#   100.times do
#     r = rand(0..100)
#     res = mysix_toast(r)
#     Test.assert_equals(six_toast(r), res)
#   end
# end
