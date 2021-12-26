import codewars_test as test
from solution import direction

@test.describe("Fixed tests")
def tests():
    @test.it("Sample tests")
    def tests():
        test.assert_equals(direction("S", 180),  "N")
        test.assert_equals(direction("SE", -45), "E")
        test.assert_equals(direction("W", 495),  "NE")


@test.describe("Random tests")
def tests():
    from random import randint
    DIRS_SOL = "N NE E SE S SW W NW".split()
    
    for _ in range(50):
        dir = DIRS_SOL[randint(0, 7)]
        turn = randint(-24, 24) * 45
        expected = DIRS_SOL[(DIRS_SOL.index(dir) + turn // 45) % 8]

        @test.it(f"Facing {dir}, turn {turn} degrees")
        def one_test():
            test.assert_equals(direction(dir, turn), expected)
