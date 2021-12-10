import codewars_test as test
from solution import joust
from random import randint

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it("Sample Jousting")
    def sample_jousting():
        input1 = ("$->    ", "    <-P"), 1, 1
        test.assert_equals(joust(*input1), (" $->   ", "   <-P "), f"input = {input1}")

        input2 = ("$->     ", "     <-P"), 1, 1
        test.assert_equals(joust(*input2), ("  $->   ","   <-P  "), f"input = {input2}")

        input3 = ("$->              ", "              <-P"), 1, 1
        test.assert_equals(joust(*input3), ("      $->        ", "        <-P      "), f"input = {input3}")

    @test.it("Different Velocity")
    def different_velocity():
        input1 = ("$->    ", "    <-P"), 3, 3
        test.assert_equals(joust(*input1), ("   $-> ", " <-P   "), f"input = {input1}")

        input2 = ("$->     ", "     <-P"), 0, 2
        test.assert_equals(joust(*input2), ( "$->     ", " <-P    "), f"input = {input2}")

        input3 = ("$->              ", "              <-P"), 2, 3
        test.assert_equals(joust(*input3), ("      $->        ", "     <-P         "), f"input = {input3}")

    
    @test.it("Immediate Battle")
    def immediate_battle():
        input1 = ("$->  ", "  <-P"), 3, 3
        test.assert_equals(joust(*input1), ("$->  ", "  <-P"), f"input = {input1}")

        input2 = ("$->", "<-P"), 3, 3
        test.assert_equals(joust(*input2), ("$->", "<-P"), f"input = {input2}")

        input3 = ("$-> ", " <-P"), 0, 0
        test.assert_equals(joust(*input3), ("$-> ", " <-P"), f"input = {input3}")

    @test.it("Knights Refused To Fight")
    def knights_refused_to_fight():
        input1 = ("$->    ", "    <-P"), 0, 0
        test.assert_equals(joust(*input1), ("$->    ", "    <-P"), f"input = {input1}")

        
def create_test(i):
    if i < 10:
        i = 0
    return (("$->" + " " * i, " " * i + "<-P"), randint(0, 3), randint(0, 3)) # randint's range end is inclusive, confusing!
    

def _s(list_field: tuple, v_knight_left: int, v_knight_right: int) -> tuple:
    if v_knight_left == 0 and v_knight_right == 0:
        return list_field
    
    len1, len2 = len(list_field[0]), len(list_field[1])
    
    left_point = 2
    right_point = len1 - 3
    
    while left_point < right_point:
        left_point  += v_knight_left
        right_point -= v_knight_right
    
    return (" " * (left_point - 2) + "$->" + " " * (len1 - left_point - 1),
            " " * right_point + "<-P" + " " * (len2 - right_point - 3))
        

@test.describe("Random Tests")
def random_tests():
    @test.it("100 random cases")
    def _():
        for i in range(100):
            input = create_test(i)
            expected = _s(*input)
            actual = joust(*input)
            test.assert_equals(actual, expected, f"input = {input}")
