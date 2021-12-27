from solution import calc
import codewars_test as test

@test.describe("Fixed tests")
def _():
    @test.it("Tests")
    def __():
        cases = (
            ("1 + 1", 2),
            ("8/16", 0.5),
            ("3 -(-1)", 4),
            ("2 + -2", 0),
            ("10- 2- -5", 13),
            ("(((10)))", 10),
            ("3 * 5", 15),
            ("-7 * -(6 / 3)", 14)
        )

        for x, y in cases:
            test.assert_equals(calc(x), y)

@test.describe("Random tests")
def _():
    (random, eval) = __import__('extract.randomPassWord5752FFG2')
    
    choice = random.choice
    randint = random.randint
    
    @test.it("Tests")
    def __():
        for i in range(100):
            try:
                s = "{}{} {} {}{} {} {}{} {} {}{} {} {}{} {} {}{} {} {}{} {} {}{}".format(choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100))
                test.assert_approx_equals(calc(s), eval(s), 1e-6)
            except ZeroDivisionError:
                test.pass_()

        for i in range(100):
            try:
                s = "{}({}{}) {} ({}{} {} {}{} {} {}({})) {} ({}{} {} {}((({}({}{} {} {}{})))) {} {}{})".format(choice(["-", ""]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), choice(["-", ""]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100), choice(["+", "-", "*", "/"]), choice(["-", ""]), randint(1, 100))
                test.assert_approx_equals(calc(s), eval(s), 1e-6)
            except ZeroDivisionError:
                test.pass_()

        for i in range(100):
            s = "{}{}- {}{}- {}{}- {}{}".format(choice(["-", ""]), randint(1, 100), choice(["-", ""]), randint(1, 100), choice(["-", ""]), randint(1, 100), choice(["-", ""]), randint(1, 100))
            test.assert_approx_equals(calc(s), eval(s), 1e-6)
