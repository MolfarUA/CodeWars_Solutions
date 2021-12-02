def show(grid):
    print('\n'.join(grid))
    return grid
    

test.describe("Sample tests")

expected = True
test.it("Good1")
grid = ["           ",
        "X---------X",
        "           ",
        "           "]
test.assert_equals(line(show(grid)), expected)
print("<COMPLETEDIN::>")


test.it("Good2")
grid = ["     ",
        "  X  ",
        "  |  ",
        "  |  ",
        "  X  "]
test.assert_equals(line(show(grid)), expected)
print("<COMPLETEDIN::>")


test.it("Good3")
grid = ["                    ",
        "     +--------+     ",
        "  X--+        +--+  ",
        "                 |  ",
        "                 X  ",
        "                    "]
test.assert_equals(line(show(grid)), expected)
print("<COMPLETEDIN::>")


test.it("Good4")
grid = ["                     ",
        "    +-------------+  ",
        "    |             |  ",
        " X--+      X------+  ",
        "                     "]
test.assert_equals(line(show(grid)), expected)
print("<COMPLETEDIN::>")


test.it("Good5")
grid = ["                      ",
        "   +-------+          ",
        "   |      +++---+     ",
        "X--+      +-+   X     "]
test.assert_equals(line(show(grid)), expected)
print("<COMPLETEDIN::>")



expected = False
test.it("Bad1")
grid = ["X-----|----X"]
test.assert_equals(line(show(grid)), expected)
print("<COMPLETEDIN::>")


test.it("Bad2")
grid = [" X  ",
        " |  ",
        " +  ",
        " X  "]
test.assert_equals(line(show(grid)), expected)
print("<COMPLETEDIN::>")


test.it("Bad3")
grid = ["   |--------+    ",
        "X---        ---+ ",
        "               | ",
        "               X "]
test.assert_equals(line(show(grid)), expected)
print("<COMPLETEDIN::>")


test.it("Bad4")
grid = ["              ",
        "   +------    ",
        "   |          ",
        "X--+      X   ",
        "              "]
test.assert_equals(line(show(grid)), expected)
print("<COMPLETEDIN::>")


test.it("Bad5")
grid = ["      +------+",
        "      |      |",
        "X-----+------+",
        "      |       ",
        "      X       "]
test.assert_equals(line(show(grid)), expected)
print("<COMPLETEDIN::>")
print("<COMPLETEDIN::>")


    

test.describe("Spirals")

test.it("Spiral clockwise")
grid = ["    +----+  ",
        "    |+--+|  ",
        "    ||X+||  ",
        "    |+-+||  ",
        "    +---+|  ",
        "X--------+  "]
test.assert_equals(line(show(grid)), True)
print("<COMPLETEDIN::>")


test.it("Spiral anticlockwise")
grid = ["   +-----+  ",
        "   |+---+|  ",
        "   ||+-+||  ",
        "   |||X+||  ",
        "   X|+--+|  ",
        "    +----+  "]
test.assert_equals(line(show(grid)), True)
print("<COMPLETEDIN::>")
print("<COMPLETEDIN::>")




test.describe("Close ones")

test.it("Close left-right")
grid = ["       ",
        "   XX  ",
        "       "]
test.assert_equals(line(show(grid)), True)
print("<COMPLETEDIN::>")


test.it("Close up-down")
grid = ["       ",
        "   X   ",
        "   X   ",
        "       "]
test.assert_equals(line(show(grid)), True)
print("<COMPLETEDIN::>")


test.it("Close diagonal1")
grid = ["       ",
        "   X   ",
        "    X  ",
        "       "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")


test.it("Close diagonal2")
grid = ["       ",
        "    X  ",
        "   X   ",
        "       "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")
print("<COMPLETEDIN::>")




test.describe("Loops")

test.it("Good loop")
grid = ["            ",
        "   X-----+  ",
        "         |  ",
        "   X     |  ",
        "   |     |  ",
        "   +-----+  "]
test.assert_equals(line(show(grid)), True)
print("<COMPLETEDIN::>")


test.it("Ambiguous loop")
grid = ["            ",
        "   X-----+  ",
        "   X     |  ",
        "   |     |  ",
        "   |     |  ",
        "   +-----+  "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")


test.it("Ambiguous loop2")
grid = ["            ",
        "   X-----+  ",
        "   |     |  ",
        "   |     |  ",
        "   |     |  ",
        "   +-----X  "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")


test.it("Ambiguous loop3")
grid = ["            ",
        "   +--X--+  ",
        "   |     |  ",
        "   |     |  ",
        "   |     |  ",
        "   +--X--+  "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")


test.it("Ambiguous loop4")
grid = ["            ",
        "   +-----+  ",
        "   |     |  ",
        "   X     X  ",
        "   |     |  ",
        "   +-----+  "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")


test.it("Ambiguous loop5")
grid = ["            ",
        "   XX----+  ",
        "   |     |  ",
        "   |     |  ",
        "   |     |  ",
        "   +-----+  "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")
print("<COMPLETEDIN::>")




test.describe("Various invalid ones")

test.it("Self loop...?")
grid = ["            ",
        "   X-----+  ",
        " X |     |  ",
        "   |     |  ",
        "   |     |  ",
        "   +-----+  "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")


test.it("No line")
grid = ["            ",
        "   X    X   ",
        "            "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")
print("<COMPLETEDIN::>")




test.describe("Breadcrumbs...")

test.it("Two ways")
grid = ["            ",
        "   X+++     ",
        "    +++X    "]
test.assert_equals(line(show(grid)), True)
print("<COMPLETEDIN::>")


test.it("Two ways2")
grid = ["            ",
        "    +++X    ",
        "   X+++     "]
test.assert_equals(line(show(grid)), True)
print("<COMPLETEDIN::>")


test.it("One way")
grid = ["         X   ",
        "   X+++  +-+ ",
        "    +++--+ | ",
        "         +-+ "]
test.assert_equals(line(show(grid)), True)
print("<COMPLETEDIN::>")


test.it("One way2")
grid = ["   X     X   ",
        "   ++++  +-+ ",
        "    +++--+ | ",
        "         +-+ "]
test.assert_equals(line(show(grid)), True)
print("<COMPLETEDIN::>")


test.it("Extras1")
grid = ["   X-----+  ",
        "         |  ",
        "   X-----+  ",
        "         |  ",
        "   ------+  "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")


test.it("Extras2")
grid = ["     X        ",
        "     |   |    ",
        " +   |  -+-   ",
        "     |   |    ",
        "     X        "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")
print("<COMPLETEDIN::>")




test.it("More edge cases")

grid = ["            ",
        "    +++X    ",
        "    +++     ",
        "   X+++     "]
test.assert_equals(line(show(grid)), False)


grid = ["             ",
        "    ++++X    ",
        "   X++++     "]
test.assert_equals(line(show(grid)), False)


grid = ["    ++++     ",
        "   X++++     ",
        "       X     "]
test.assert_equals(line(show(grid)), False)


grid = ["    ++++     ",
        "   X++++X    "]
test.assert_equals(line(show(grid)), True)


grid = ["     ++      ",
        "    ++++     ",
        "    ++++     ",
        "   X-++-X    "]
test.assert_equals(line(show(grid)), False)


grid = ["    +-+     ",
        "    | |     ",
        "    +++     ",
        "    +++     ",
        "   X+++X    "]
test.assert_equals(line(show(grid)), False)


grid = ["    +-+    ",
        "    | |    ",
        "    ++++   ",
        "    ++++   ",
        "   X+++    ",
        "     +---X "]
test.assert_equals(line(show(grid)), False)
print("<COMPLETEDIN::>")






test.it("Random tests")

expecteds = [1,1,1,0,0,1,1,1,0,1]
grids = [
  [ "   X-----+  ",
    "         |  ",
    "   X     |  ",
    "   |     |  ",
    "   +-----+  "],
    
  [ "        X+  ",
    "         |  ",
    "         |  ",
    "         |  ",
    "         X  "],
    
  [ "   X-----+  ",
    "         |  ",
    "   +-----+  ",
    "   |        ",
    "   +-----X  "],
    
  [ "   X-----+  ",
    "         |  ",
    "    -----+  ",
    "         |  ",
    "   X-----+  "],
    
  [ "   X        ",
    "   |  |     ",
    "   +--+---  ",
    "      |     ",
    "      X     "],
    
  [ "   +-----X ",
    "   |       ",
    "   +-----+ ",
    "         | ",
    "   X-----+ "],
    
  [ "   +-----X ",
    "   |       ",
    "   |X----+ ",
    "   |     | ",
    "   +-----+ "],
    
  [ "   X-----+ ",
    "         | ",
    "         | ",
    "         | ",
    "         X "],
    
  [ "   X-----+ ",
    "   |     | ",
    "   +-----+ ",
    "   |     | ",
    "   +-----X "],
    
  [ "   +-----+ ",
    "   |     | ",
    "   +----X| ",
    "         | ",
    "   X-----+ "],
]


from random import randrange as rand

for r in range(50):
    
    n = rand(10)
    g = grids[n][:]
    show([" \n* Random test #%d:"%(r+1)] + g)
    print("<span style='background:green'>Valid</span>" if expecteds[n] else "<span style='background:red'>Invalid</span>")
    
    test.assert_equals(line(g), expecteds[n])
    
print("<COMPLETEDIN::>")
