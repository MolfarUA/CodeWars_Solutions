5870fa11aa0428da750000da


from collections import deque
import re

TOKENIZER = re.compile(r'(R+|F+|L+)(\d*)')

def execute(code):
    
    pos, dirs = (0,0), deque([(0,1), (1,0), (0,-1), (-1,0)])
    seens = {pos}
    
    for act,n in TOKENIZER.findall(code):
        s,r = act[0], int(n or '1') + len(act)-1
        
        if s == 'F':
            for _ in range(r):
                pos = tuple( z+dz for z,dz in zip(pos, dirs[0]) )
                seens.add(pos)
        else:
            dirs.rotate( (r%4) * (-1)**(s == 'R') )
    
    miX, maX = min(x for x,y in seens), max(x for x,y in seens)
    miY, maY = min(y for x,y in seens), max(y for x,y in seens)
    
    return '\r\n'.join( ''.join('*' if (x,y) in seens else ' ' for y in range(miY, maY+1)) 
                        for x in range(miX, maX+1) )
__________________________
import re
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)] * 2

def execute(code):
    grid, (dx, dy) = {(0, 0)}, DIRS[0]
    x = y = xm = ym = xM = yM = 0
    for dir, n in re.findall('([FLR])(\d*)', code):
        for _ in range(int(n or '1')):
            if dir == 'L': dx, dy = DIRS[DIRS.index((dx, dy)) - 1]
            if dir == 'R': dx, dy = DIRS[DIRS.index((dx, dy)) + 1]
            if dir == 'F':
                x += dx; y += dy
                grid.add((x, y))
                xm, ym, xM, yM = min(xm, x), min(ym, y), max(xM, x), max(yM, y)
    return '\r\n'.join(''.join(' *'[(x, y) in grid] for x in range(xm, xM + 1)) for y in range(ym, yM + 1))
__________________________
import re


class Robo:
    DIR = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self):
        self.x_min = self.y_min = self.x_max = self.y_max = 0
        self.x = self.y = 0
        self.d = 0
        self.ps = [(0, 0)]

    def move(self, n):  # move n step
        dx, dy = Robo.DIR[self.d]
        for _ in range(n):
            self.x += dx
            self.y += dy
            self.ps.append((self.x, self.y))

        if self.x < self.x_min: self.x_min = self.x
        if self.x > self.x_max: self.x_max = self.x
        if self.y < self.y_min: self.y_min = self.y
        if self.y > self.y_max: self.y_max = self.y

    def turn(self, dire, n):
        if dire == 'R':
            self.d = (self.d + n) % 4
        elif dire == 'L':
            self.d = ((self.d - n) % 4 + 4) % 4
        else:
            raise KeyError("Wrong command")

    def execute(self, code):
        commands = re.findall(r'([FLR])([0-9]*)', code)
        for c in commands:
            c, n = c
            if n == '': n = '1'
            n = int(n)
            if c == 'F':
                self.move(n)
            else:
                self.turn(c, n)

    def __str__(self):
        n = self.x_max - self.x_min + 1
        m = self.y_max - self.y_min + 1
        p = [[' ' for _ in range(m)] for _ in range(n)]
        for x, y in self.ps:
            p[x - self.x_min][y - self.y_min] = '*'
        return "\r\n".join("".join(x) for x in p)


def execute(code):
    r = Robo()
    r.execute(code)
    print(r)
    return r.__str__()
__________________________
import re
from collections import defaultdict

def execute(code):
    grid = defaultdict(lambda: " ")
    i, j = 0, 0
    d = complex(0, 1)
    grid[(i, j)] = "*"
    for command, times in re.findall(r"([FLR])(\d*)", code):
        times = int(times) if times else 1
        for _ in range(times):
            if command == "F":
                i += int(d.real)
                j += int(d.imag)
                grid[(i, j)] = "*"
            elif command == "L":
                d *= 1j
            elif command == "R":
                d *= -1j
    min_y = min(y for y, x in grid)
    max_y = max(y for y, x in grid)
    min_x = min(x for y, x in grid)
    max_x = max(x for y, x in grid)
    return "\r\n".join("".join(grid[(y, x)] for x in range(min_x, max_x + 1)) for y in range(min_y, max_y + 1))
__________________________
import re

TOKENIZER = re.compile(r'(R+|F+|L+)(\d*)')

def execute(code):
    "Heavily inspired by Blind4Basics' solution."

    x, y, d = 0, 0, 0
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]
    visited = {(x,y)}
        
    for a,b in TOKENIZER.findall(code):
        cmd,rep = a[0], int(b or '1') + len(a)-1
        
        if cmd == 'F':
            for _ in range(rep):
                x += dirs[d][0]
                y += dirs[d][1]
                visited.add((x,y))
            
        else: # Command must be 'R' or 'L'
            d = (d + (rep if cmd == 'R' else -rep) ) % 4
    
    minX, maxX = min(x for x,y in visited), max(x for x,y in visited)
    minY, maxY = min(y for x,y in visited), max(y for x,y in visited)
    
    lines = ( ''.join( '*' if (x,y) in visited else ' ' for x in range(minX, maxX+1) ) for y in range(minY, maxY+1) )
    return '\r\n'.join(lines)
__________________________
import re

def execute(code):
    if code == '':
        return '*'
    turn_right = [[1, 0], [0, -1], [-1, 0], [0, 1]]
    turn_left =  [[-1, 0], [0, -1], [1, 0], [0, 1]]
    path = re.findall('F\d+|F|L\d+|L|R\d+|R', code)
    max_size = sum([1 if j == 'F' else int(j[1:]) for j in path if 'F' in j]) * 2
    table = [[' '] * (max_size + 1) for i in range(max_size + 1)]
    x, y = max_size // 2, max_size // 2
    table[x][y] = '*'
    f1, f2 = 0, 1
    for way in path:
        if 'R' in way:
            for i in range(1 if way == 'R' else int(way[1:])):
                cur_pos = [pos for pos, coords in enumerate(turn_right) if coords == [f1, f2]][0]
                f1, f2 = turn_right[0] if cur_pos == 3 else turn_right[cur_pos + 1]
        if 'L' in way:
            for i in range(1 if way == 'L' else int(way[1:])):
                cur_pos = [pos for pos, coords in enumerate(turn_left) if coords == [f1, f2]][0]
                f1, f2 = turn_left[0] if cur_pos == 3 else turn_left[cur_pos + 1]        
        if 'F' in way:
            for i in range(1 if way == 'F' else int(way[1:])):
                x += 1 * f1
                y += 1 * f2
                table[x][y] = '*'
    solution = [i for i in table if '*' in i]
    solution = [i for i in zip(*solution[:]) if '*' in i]
    for i in range(3):
        solution = list(zip(*solution[:]))
    final_way = [''.join([j for j in i]) for i in solution]
    return '\r\n'.join(final_way)
__________________________
import re
from enum import Enum
from operator import itemgetter
from typing import List, Tuple, Set, Generator


Cell = Tuple[int, int]


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)


def execute(code: str) -> str:
    visited_cells = visit_cells(code)
    path = draw_path(visited_cells)
    return path
    
    
def visit_cells(code: str) -> Set[Cell]:
    visited_cells = [(0, 0)]
    direction = Direction.RIGHT
    
    for action, n_times in code_interpreter(code):
        if action == 'F':
            new_cells = move_forward(visited_cells[-1], direction, n_times)
            visited_cells.extend(new_cells)
        else:
            direction = make_turn(direction, action, n_times)
    return set(visited_cells)


def code_interpreter(code: str) -> Generator[Tuple[str, int], None, None]:
    for move in re.finditer(r'([LRF])(\d*)', code):
        action = move.group(1)
        times = int(move.group(2)) if move.group(2) else 1
        yield action, times
    

def move_forward(position: Cell, direction: Direction, n_moves: int) -> List[Cell]:
    px, py = position
    dx, dy = direction.value
    return [(px + i * dx, py + i * dy) for i in range(1, n_moves + 1)]


def make_turn(start: Direction, side: str, n_turns: int) -> Direction:
    ordering = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
    step = 1 if side == 'R' else -1
    return ordering[(ordering.index(start) + step * n_turns) % len(ordering)]
    
    
def draw_path(visited_cells: Set[Cell]) -> str:
    max_x, min_x, max_y, min_y = find_cells_boundaries(visited_cells)
    
    rectangle = list()
    for y in range(max_y, min_y - 1, -1):
        row = ['*' if (x, y) in visited_cells else ' ' for x in range(min_x, max_x + 1)]
        rectangle.append(''.join(row))
    
    return '\r\n'.join(rectangle)
    
    
def find_cells_boundaries(visited_cells: Set[Cell]) -> Tuple[int, int, int, int]:
    max_x, _ = max(visited_cells, key=itemgetter(0))
    min_x, _ = min(visited_cells, key=itemgetter(0))
    
    _, max_y = max(visited_cells, key=itemgetter(1))
    _, min_y = min(visited_cells, key=itemgetter(1))
    return max_x, min_x, max_y, min_y
__________________________
import re
left = {'right': 'up', 'up': 'left', 'left': 'down', 'down': 'right'}
right = {'right': 'down', 'down': 'left', 'left': 'up', 'up': 'right'}
def execute(s):
    s, direction = re.sub(r'([RFL])(\d+)', lambda x: x.group(1) * int(x.group(2)), s), 'right'
    p, p1, li = 0, 0, [[0, 0]]
    for i in s:
        if i == 'L' : direction = left[direction]
        if i == "R" : direction = right[direction]
        if i == "F":
            p1 += (1 if direction == "right" else -1) if direction in ['left', 'right'] else 0
            p += (1 if direction == 'down' else -1) if direction in ['up', 'down'] else 0
            li.append([p, p1])
    m, n = abs(min(li, key=lambda x:x[0])[0])+max(li,key=lambda x:x[0])[0], abs(min(li,key=lambda x:x[1])[1])+max(li,key=lambda x:x[1])[1]
    p, p1, grid= abs(min(li,key=lambda x:x[0])[0]), abs(min(li,key=lambda x:x[1])[1]), [[' ' for _ in range(n+1)] for _ in range(m+1)]
    for i, j in li : grid[p + i][p1 + j] = "*" 
    return "\r\n".join(["".join(i) for i in grid])
__________________________
import re


def highlight(code):
    code = re.sub(r"(F+)", '<span style="color: pink">\g<1></span>', code)
    code = re.sub(r"(L+)", '<span style="color: red">\g<1></span>', code)
    code = re.sub(r"(R+)", '<span style="color: green">\g<1></span>', code)
    code = re.sub(r"(\d+)", '<span style="color: orange">\g<1></span>', code)
    return code


def simplify_code(code):
    if not re.search(r"\d", code):
        return code
    cm = [c for c in code]
    for i in range(len(code) - 1, -1, -1):
        if cm[i].isdigit():
            ds = cm.pop(i)
            cm[i - 1] = cm[i - 1] + ds if cm[i - 1].isdigit() else cm[i - 1] * int(ds)
    return "".join(cm)


def execute(code):
    matrix_set = {(0, 0)}
    set_x, set_y, min_x, max_x, min_y, max_y = 0, 0, 0, 0, 0, 0
    # h-v,forward,backward
    movement, direction = 1, 1
    for step in simplify_code(code):

        if step == "L":
            direction *= -1 * movement
            movement *= -1
        elif step == "R":
            direction *= movement
            movement *= -1
        else:
            if movement < 0:
                set_x += direction
                if set_x < min_x:
                    min_x = set_x
                elif set_x > max_x:
                    max_x = set_x
            else:
                set_y += direction
                if set_y < min_y:
                    min_y = set_y
                elif set_y > max_y:
                    max_y = set_y
            matrix_set.add((set_x, set_y))
    return "\r\n".join(["".join(["*" if (i, j) in matrix_set else " " for j in range(min_y, max_y + 1)]) for i in
                        range(min_x, max_x + 1)])
__________________________
import re

def simplify_code(code):
    # print(re.compile(r'(R+|F+|L+)(\d*)').findall(code))
    if not re.search(r"\d", code):
        return code
    cm = [c for c in code]
    for i in range(len(code) - 1, -1, -1):
        if cm[i].isdigit():
            ds = cm.pop(i)
            cm[i - 1] = cm[i - 1] + ds if cm[i - 1].isdigit() else cm[i - 1] * int(ds)
    return "".join(cm)


def execute(code):
    matrix_set = {(0, 0)}
    set_x, set_y, min_x, max_x, min_y, max_y = 0, 0, 0, 0, 0, 0
    # h-v,forward,backward
    movement, direction = 1, 1
    for step in simplify_code(code):
        if step == "L":
            direction *= -1 * movement
            movement *= -1
        elif step == "R":
            direction *= movement
            movement *= -1
        else:
            if movement < 0:
                set_x += direction
                min_x = set_x if set_x < min_x else min_x
                max_x = set_x if set_x > max_x else max_x

            else:
                set_y += direction
                min_y = set_y if set_y < min_y else min_y
                max_y = set_y if set_y > max_y else max_y
            matrix_set.add((set_x, set_y))
    return "\r\n".join(["".join(["*" if (i, j) in matrix_set else " " for j in range(min_y, max_y+1)]) for i in
                        range(min_x, max_x + 1)])
__________________________
import re

def simplify_code(code):
    if not re.search(r"\d", code):
        return code
    cm = [c for c in code]
    for i in range(len(code) - 1, -1, -1):
        if cm[i].isdigit():
            ds = cm.pop(i)
            cm[i - 1] = cm[i - 1] + ds if cm[i - 1].isdigit() else cm[i - 1] * int(ds)
    return "".join(cm)


def execute(code):
    matrix = [["*"]]
    row, column, height, width = 0, 0, 1, 1
    # h-v,forward,backward
    movement, direction = 1, 1
    for step in simplify_code(code):
        if step == "L":
            direction *= -1 * movement
            movement *= -1
        elif step == "R":
            direction *= movement
            movement *= -1
        else:
            if movement < 0:
                row += direction
                if row < 0 or row >= height:
                    if row < 0:
                        row = 0
                    matrix.insert(row, [" " for _ in range(width)])
                    height += 1
            else:
                column += direction
                if column < 0 or column >= width:
                    if column < 0:
                        column = 0
                    for index in range(height):
                        matrix[index].insert(column, " ")
                    width += 1
            matrix[row][column] = "*"

    return "\r\n".join(["".join(line) for line in matrix])

    return "\r\n".join(["".join(line) for line in matrix])
__________________________
import numpy as np
import operator
import re

def move_point(point, dir):
    return tuple(map(operator.add, point, dir))

def is_inside(point, arr):
    return 0 <= point[0] < arr.shape[0] and \
           0 <= point[1] < arr.shape[1]

DIRS = [
    ( 0,  1),  # Right
    ( 1,  0),  # Down
    ( 0, -1),  # Left
    (-1,  0),  # Up
]

class Robot:
    def __init__(self):
        self.board = np.zeros((1, 1))
        self.pos = (0, 0)
        self.dir = 0
        self.board[self.pos] = 1
    
    def execute(self, code):
        for cmd in code:
            if cmd.startswith('F'):
                for _ in range(self.parse_count(cmd)):
                    self.move_forward()
            elif cmd.startswith('R'):
                self.rotate(self.parse_count(cmd))
            elif cmd.startswith('L'):
                self.rotate(-self.parse_count(cmd))
            else:
                raise ValueError(f'Unknown command "{cmd}"')
    
    def parse_count(self, cmd):
        if len(cmd) == 1:
            return 1
        else:
            return int(cmd[1:])
    
    def rotate(self, count):
        self.dir += count
        self.dir %= 4
    
    def move_forward(self):
        self.pos = move_point(self.pos, DIRS[self.dir])
        
        if not is_inside(self.pos, self.board):
            if self.dir == 0:  # Right
                self.board = np.concatenate((self.board, [[0] for _ in self.board]), axis=1)
            elif self.dir == 2:  # Left
                self.board = np.concatenate(([[0] for _ in self.board], self.board), axis=1)
                self.pos = move_point(self.pos, DIRS[0])
            elif self.dir == 1:  # Down
                self.board = np.concatenate((self.board, [[0 for _ in self.board[0]]]), axis=0)
            elif self.dir == 3:  # Up
                self.board = np.concatenate(([[0 for _ in self.board[0]]], self.board), axis=0)
                self.pos = move_point(self.pos, DIRS[1])
        
        self.board[self.pos] = 1
        
    def __str__(self):
        return '\r\n'.join(''.join('*' if item else ' ' for item in row) for row in self.board)


def tokenizer(code):
    return re.findall('[FRL]\d*', code)


def execute(code):
    robot = Robot()
    
    robot.execute(tokenizer(code))
    
    return str(robot)
