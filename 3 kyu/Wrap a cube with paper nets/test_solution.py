from solution import wrap_cube
from random import randint, choice
import codewars_test as test


@test.describe("Test Code Check")
def check_code():
    @test.it('No tricks in the code.')
    def test_custom_assertion():
        with open('/workspace/solution.txt', 'r') as file:
            data = file.read()
        if "exit(" in data:
            test.fail("Please avoid including any exit( in your code.")
        else:
            test.pass_()


def runtest(a, b):
    return fullsort(a) == fullsort(b)


def fullsort(a):
    try:
        res = [sorted(i) for i in a]
        return sorted(res)
    except:
        return a

def test_wrap_lite(shape, a, b):
    #  @test.it(title)
    #  def _test():
    #  global test_passed
    try:
        if b is None:
            if a is not None:
                msg = "Input shape:\n" + shape + "\nExpected answer: None"
                #  test_passed = False
                #  raise AssertionError(msg)
                test.fail(msg)
                #  print(msg)
                #  exit(1)
        elif not runtest(a, b):
            msg = "Input shape:\n" + shape + "\nExpected answer:" + \
                "[" + ",".join(["[" + ",".join(_) + "]" for _ in b]) + "]"
            #  test_passed= False
            #  raise AssertionError(msg)
            test.fail(msg)
            #  exit(1)
    except BaseException:
        # "[" + ",".join(["[" + ",".join(_) + "]" for _ in b]) + "]"
        msg = "Input shape:\n" + shape
        #  test_passed = False
        test.fail(msg)
        #  raise AssertionError(msg)
        #  exit(1)
    test.pass_()


def test_wrap(title, shape, a, b):
    @test.it(title)
    def _test():
        try:
            if b is None:
                if a is not None:
                    msg = "Input shape:\n" + shape + "\nExpected answer: None"
                    #  raise AssertionError(msg)
                    test.fail(msg)
                    #  exit(1)
            elif not runtest(a, b):
                msg = "Input shape:\n" + shape + "\nExpected answer:" + \
                    "[" + ",".join(["[" + ",".join(_) + "]" for _ in b]) + "]"
                #  raise AssertionError(msg)
                test.fail(msg)
                #  exit(1)
                #  test.fail(msg)
        except BaseException:
            msg = "Input shape:\n" + shape
            #  "[" + ",".join(["[" + ",".join(_) + "]" for _ in b]) + "]"
            #  raise AssertionError(msg)
            test.fail(msg)
            #  exit(1)
        test.pass_()
    #  _test(shape, a, b)


def gen_a_net(min_l, max_l):

    def gen_a_num_net(l, pieces):
        if l == 0:
            return pieces
        while True:
            p = choice(pieces)
            d = choice(get4dirs(p))
            new = p + d
            if new not in pieces:
                Dnew = get4dirs(new)
                Dnew.remove(-d)
                if not any([(new + D) in pieces for D in Dnew]):
                    pieces.append(new)
                    return gen_a_num_net(l - 1, pieces)

    def add_a_num2net(pieces):
        while True:
            p = choice(pieces)
            d = choice(get4dirs(p))
            new = p + d
            if new not in pieces:
                pieces.append(new)
                return pieces

    def get4dirs(p):
        ds = [1, -1, 62, -62]
        if p % 62 == 0:
            ds.remove(-1)
        if p % 62 == 61:
            ds.remove(1)
        if p < 62:
            ds.remove(-62)
        if p >= 62 * 61:
            ds.remove(62)
        return ds

    def num_net_2_string(pieces):
        char_list = [chr(ord('a') + i) for i in range(26)] + [chr(ord('A') + i)
                                                              for i in range(26)] + [str(i) for i in range(10)]
        S = []
        for y in range(62):
            s = ""
            for x in range(62):
                if x + y * 62 in pieces:
                    c = choice(char_list)
                    char_list.remove(c)
                    s = s + c
                else:
                    s = s + " "
            s = s.rstrip()
            if len(s):
                S.append(s)

        leading_spaces = min([len(a) - len(a.lstrip()) for a in S])
        return "\n".join([a[leading_spaces:] for a in S])

    l = randint(min_l, max_l)
    i = 0
    while True:
        i = i + 1
        res = num_net_2_string(
            add_a_num2net(gen_a_num_net(l, [randint(0, 62 * 61)])))
        return res


def wrap_cube_answer(shape):
    WIDTH = 0
    HEIGHT = 0

    def folding(
            grid,
            face,
            list_on_face,
            remain_list,
            faces_done
    ):
        faces = [(list_on_face, face)]

        dirs = [1, -1, WIDTH, -WIDTH]
        if list_on_face % WIDTH == 0:
            dirs.remove(-1)
        if list_on_face % WIDTH == WIDTH - 1:
            dirs.remove(1)
        if list_on_face < WIDTH:
            dirs.remove(-WIDTH)
        if list_on_face >= WIDTH * (HEIGHT - 1):
            dirs.remove(WIDTH)

        goto_dirs = []
        for direction in dirs:
            goto_cell = direction + list_on_face
            if goto_cell in remain_list:
                if goto_cell in faces_done:
                    #  if faces_done_on_cube[faces_done.index(
                    #  goto_cell)] != new_face(grid, direction):
                    if goto_cell != faces_done[-1]:
                        return "F"
                else:
                    goto_dirs.append(direction)
        #  print(faces_done, list_on_face, goto_dirs)
        for direction in goto_dirs:
            faces.extend(folding(
                grid=new_grid(face, direction, grid),
                face=new_face(grid, direction),
                list_on_face=list_on_face + direction,
                remain_list=remain_list,
                faces_done=faces_done + [list_on_face]
                #  faces_done_on_cube=faces_done_on_cube + [face]
            ))
        return faces

    def new_face(grid, direction):
        return grid[[1, -1, WIDTH, -WIDTH].index(direction)]

    def new_grid(face, direction, grid):
        opposite_face = {1: 6, 2: 4, 6: 1, 4: 2, 5: 3, 3: 5}
        dir_index = {1: 0, -1: 1, WIDTH: 2, -WIDTH: 3}
        newgrid = grid.copy()
        newgrid[dir_index[-direction]] = face
        newgrid[dir_index[direction]] = opposite_face[face]
        return newgrid

    shape_list = shape.split('\n')
    WIDTH = max([len(x) for x in shape_list]) + 1
    HEIGHT = len(shape_list)
    number_list = []
    char_list = []
    for y in range(HEIGHT):
        for x in range(len(shape_list[y])):
            if shape_list[y][x] != " ":
                char_list.append(shape_list[y][x])
                number_list.append(x + y * WIDTH)
    faces = folding(grid=[3, 5, 2, 4],  # in dir [1,-1,5,-5]
                    face=1,
                    list_on_face=number_list[0],
                    remain_list=number_list, faces_done=[])  # , faces_done_on_cube=[])
    if "F" in faces:
        return None
    res = []
    for i in range(1, 7):
        r = [char_list[number_list.index(p[0])] for p in faces if p[1] == i]
        if len(r) > 1:
            res.append(r)
    return res


@test.describe("Fix Tests")
#  @test.it("It should works for basic tests.")
def basic():
    shapes = [
        ["Full wrap a cube.",
         """
 A
BCDE
  F
"""],
        ["Half wrap a cube.",
         """
A
BC
"""],
        ["A line...", "ABCDE"],
        ["A longer line...", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
        ["A square...", "AB\nCD"],
        ["A loop...",
         """
ABCDEFG
H     I
J     K
LMNOPQ
"""],
        ["A completed loop.",
         """
ABCDE
F   G
H   I
JKLMN
"""],
        ["A fence.",
         """
A B C D
EFGHIJK
L M N O
P Q R S
"""],
        ["A Star.",
         """
 YAT
O R P
BCDEG
M U N
 XIZ
"""],
        ["Stairs...",
         """
A
BOC
  DPE
    FGQ
      HIR
        JKL
          SMN
"""], ["A Snake..",
            """
ABDCEFG
      H
gKLMN I
O   P Q
R STU V
W     X
YZabdef
"""], ["A star in space.",
            "     \n " * 10 + """

  K
FGHIJ
  E

"""], ["A vertical line.", "a\nb\nc\nd"],
        ["A longer vertical line.", "a\nb\nc\nd\ne\nf\ng"]
    ]
    for shape in shapes:
        answer = wrap_cube_answer(shape[1])
        test_wrap(shape[0], shape[1], wrap_cube(shape[1]), answer)


@test.describe("Random Random")
def rand_tests():
    @test.it("50 Random Small Tests")
    def small_tests():
        for i in range(50):
            shape = gen_a_net(1, 10)
            answer = wrap_cube_answer(shape)
            #  print(shape)
            test_wrap_lite(shape, wrap_cube(shape), answer)

    @test.it("200 Random Medium Tests")
    def mid_tests():
        for i in range(200):
            shape = gen_a_net(10, 20)
            answer = wrap_cube_answer(shape)
            test_wrap_lite(
                shape, wrap_cube(shape), answer)

    @test.it("200 Random Large Tests")
    def L_tests():
        for i in range(200):
            shape = gen_a_net(30, 50)
            answer = wrap_cube_answer(shape)
            test_wrap_lite(
                shape, wrap_cube(shape), answer)

    @test.it("500 Random Jumbo Tests")
    def J_tests():
        for i in range(500):
            shape = gen_a_net(59, 60)
            answer = wrap_cube_answer(shape)
            test_wrap_lite(
                shape, wrap_cube(shape), answer)
