test.describe("Basic Expression Evaluation")
interpreter = Interpreter()

test.it("Should handle empty input")
test.assert_equals(interpreter.input(""), "", "input: ''")
test.assert_equals(interpreter.input(" "), "", "input: ' '")

test.it("Should echo constants")
test.assert_equals(interpreter.input("9"), 9, "input: '9'")

test.it("Should reject invalid input")
test.expect_error("input: '1 2'", lambda : interpreter.input("1 2"))
test.expect_error("input: '1two'", lambda : interpreter.input("1two"))

test.it("Should handle addition")
test.assert_equals(interpreter.input("1 + 1"), 2, "input: '1 + 1'")
test.assert_equals(interpreter.input("2+2"), 4, "input: '2+2'")

test.it("Should handle subtraction")
test.assert_equals(interpreter.input("2 - 1"), 1, "input: '2 - 1'")
test.assert_equals(interpreter.input("4-6"), -2, "input: '4-6'")

test.it("Should handle multiplication")
test.assert_equals(interpreter.input("2 * 3"), 6, "input: '2 * 3'")

test.it("Should handle division")
test.assert_equals(interpreter.input("8 / 4"), 2, "input: '8 / 4'")

test.it("Should handle modulo")
test.assert_equals(interpreter.input("7 % 4"), 3), "input: '7 % 4'"



test.describe("Complex Expression Evaluation")
interpreter = Interpreter()
    
test.it("Should handle multiple operations")
test.assert_equals(interpreter.input("4 + 2 * 3"), 10, "input: '4 + 2 * 3'")
test.assert_equals(interpreter.input("4 / 2 * 3"), 6, "input: '4 / 2 * 3'")
test.assert_equals(interpreter.input("7 % 2 * 8"), 8, "input: '7 % 2 * 8'")

test.it("Should handle parentheses")
test.assert_equals(interpreter.input("(4 + 2) * 3"), 18, "input: '(4 + 2) * 3'")
test.assert_equals(interpreter.input("(7 + 3) / (2 * 2 + 1)"), 2, "input: '(7 + 3) / (2 * 2 + 1)'")

test.it("Should handle nested parentheses")
test.assert_equals(interpreter.input("(8 - (4 + 2)) * 3"), 6, "input: '(8 - (4 + 2)) * 3'")
test.assert_equals(interpreter.input("(10 / (8 - (4 + 2))) * 3"), 15, "input: '(10 / (8 - (4 + 2))) * 3'")



test.describe("Variables")
interpreter = Interpreter()

test.it("Should assign a constant to a variable")
test.assert_equals(interpreter.input("x = 7"), 7, "input: 'x = 7'")

test.it("Should read the value of a variable")
test.assert_equals(interpreter.input("x"), 7, "input: 'x'")

test.it("Should handle variables in expressions")
test.assert_equals(interpreter.input("x + 3"), 10, "input: 'x + 3'")

test.it("Should throw an error when variables don't exist")
test.expect_error("input: 'y'", lambda : interpreter.input("y"))

test.it("Should continue to function after an error is thrown")
test.assert_equals(interpreter.input("y = x + 5"), 12, "input: 'y = x + 5'")
test.assert_equals(interpreter.input("y"), 12, "input: 'y'")

test.it("Should handle chained assignment")
test.assert_equals(interpreter.input("x = y = 713"), 713, "input: 'x = y = 713'")
test.assert_equals(interpreter.input("x"), 713, "input: 'x'")
test.assert_equals(interpreter.input("y"), 713, "input: 'y'")

test.it("Should handle nested assignment")
test.assert_equals(interpreter.input("x = 29 + (y = 11)"), 40, "input: 'x = 29 + (y = 11)'")
test.assert_equals(interpreter.input("x"), 40, "input: 'x'")
test.assert_equals(interpreter.input("y"), 11, "input: 'y'")



test.describe("Functions")
interpreter = Interpreter()
interpreter.input("x = 23");
interpreter.input("y = 25");
interpreter.input("z = 0");

test.it("Should declare a valid function without error")
test.assert_equals(interpreter.input("fn one => 1"), "", "input: 'fn one => 1'")
test.assert_equals(interpreter.input("fn avg x y => (x + y) / 2"), "", "input: 'fn avg x y => (x + y) / 2'")
test.assert_equals(interpreter.input("fn echo x => x"), "", "input: 'fn echo x => x'")

test.it("Should throw an error when a function's expression contains invalid variable names")
test.expect_error("input: 'fn add x y => x + z'", lambda : interpreter.input("fn add x y => x + z"))

test.it("Should throw an error when a function's declaration includes duplicate variable names")
test.expect_error("input: 'fn add x x => x + x'", lambda : interpreter.input("fn add x x => x + x"))

test.it("Should throw an error when a function is declared within an expression")
test.expect_error("input: '(fn f => 1)", lambda : interpreter.input("(fn f => 1)"))

test.it("Should call a declared function")
test.assert_equals(interpreter.input("one"), 1, "input: 'one'")
test.assert_equals(interpreter.input("avg 4 2"), 3, "input: 'avg 4 2'")

test.it("Should throw an error when a function is called with too few arguments")
test.expect_error("input: 'avg 7'", lambda : interpreter.input("avg 7"))

test.it("Should throw an error when a function is called with too many arguments")
test.expect_error("input: 'avg 7 2 4'", lambda : interpreter.input("avg 7 2 4"))

test.it("Should call chained functions")
test.assert_equals(interpreter.input("avg echo 4 echo 2"), 3, "input: 'avg echo 4 echo 2'")

test.it("Should throw an error when chained function calls result in too few arguments")
test.expect_error("input: 'avg echo 7'", lambda : interpreter.input("avg echo 7"))

test.it("Should throw an error when chained function calls result in too many arguments")
test.expect_error("input: 'avg echo 7 echo 2 echo 4'", lambda : interpreter.input("avg echo 7 echo 2 echo 4"))

test.it("Should parse nested functions")
interpreter.input("fn f a b => a * b")
interpreter.input("fn g a b c => a * b * c")
test.assert_equals(interpreter.input("g g 1 2 3 f 4 5 f 6 7"), 5040, "input: 'g g 1 2 3 f 4 5 f 6 7'")



test.describe("Conflicts")
interpreter = Interpreter()
interpreter.input("x = 0");
interpreter.input("fn f => 1");

test.it("Should throw an error when a function with the name of an existing variable is declared")
test.expect_error("input: 'fn x => 0'", lambda : interpreter.input("fn x => 0"))

test.it("Should throw an error when a variable with the name of an existing function is declared")
test.expect_error("input: 'f = 5'", lambda : interpreter.input("f = 5"))

test.it("Should overwrite an existing function")
test.assert_equals(interpreter.input("f"), 1, "input: 'f'")
interpreter.input("fn f => 0")
test.assert_equals(interpreter.input("f"), 0, "input: 'f'")
