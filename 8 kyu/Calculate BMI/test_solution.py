@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(bmi(50, 1.80), "Underweight")
        test.assert_equals(bmi(80, 1.80), "Normal")
        test.assert_equals(bmi(90, 1.80), "Overweight")
        test.assert_equals(bmi(110, 1.80), "Obese")
        test.assert_equals(bmi(50, 1.50), "Normal")

@test.describe("Random tests")
def random_tests():
    
    from random import randint

    sol=lambda w,h:(lambda b: "Underweight" if b<= 18.5 else "Normal" if b<= 25.0 else "Overweight" if b<= 30.0 else "Obese")(w/h/h)

    for _ in range(40):
        w,h=randint(30,150),randint(110,210)/100.0
        @test.it("Testing for %s amd %s" %(w,h))
        def test_case():
            test.assert_equals(bmi(w,h),sol(w,h))
