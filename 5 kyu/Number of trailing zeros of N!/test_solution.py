test.describe("Basic Tests")
test.it("Should pass basic tests")
test.assert_equals(zeros(0), 0, "Testing with n = 0")
test.assert_equals(zeros(6), 1, "Testing with n = 6")
test.assert_equals(zeros(30), 7, "Testing with n = 30")
test.assert_equals(zeros(100), 24, "Testing with n = 100")
test.assert_equals(zeros(1000), 249, "Testing with n = 1000")
test.assert_equals(zeros(100000), 24999, "Testing with n = 100000")
test.assert_equals(zeros(1000000000), 249999998, "Testing with n = 1000000000")
print("<COMPLETEDIN::>")
print("<COMPLETEDIN::>")

test.describe("Random Tests")
test.it("Should pass random tests")
def random_tests():
    import random
    def zeros_sol(n):
        x = n//5
        return x+zeros_sol(x) if x else 0
  
    for _ in range(100):
        n = random.randint(0, 1000000000)
        test.assert_equals(zeros(n), zeros_sol(n), "Testing with n = %d" % n)
        
random_tests()
