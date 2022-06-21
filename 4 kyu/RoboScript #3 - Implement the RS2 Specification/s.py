58738d518ec3b4bf95000192


from collections import deque
import re

TOKENIZER = re.compile(r'(R+|F+|L+|\)|\()(\d*)')

def parseCode(code):
    cmds = [[]]
    for cmd,n in TOKENIZER.findall(code):
        s,r = cmd[0], int(n or '1') + len(cmd)-1
        if   cmd == '(': cmds.append([])
        elif cmd == ')': lst = cmds.pop() ; cmds[-1].extend(lst*r)
        else:            cmds[-1] += [(s, r)]
    return cmds[0]

def execute(code):

    pos, dirs = (0,0), deque([(0,1), (1,0), (0,-1), (-1,0)])
    seens = {pos}
    
    for s,r in parseCode(code):
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

def execute(code):
    def simplify_code(code):
        while '(' in code:
            code = re.sub(r'\(([^()]*)\)(\d*)',
                lambda match: match.group(1) * int(match.group(2) or 1),
                code)
        code = re.sub(r'([FLR])(\d+)',
                lambda match: match.group(1) * int(match.group(2)),
                code)
        return code

    def compute_path(simplified_code):
        pos, dir = (0, 0), (1, 0)
        path = [pos]
        for cmd in simplified_code:
            if cmd == 'F':
                pos = tuple(a + b for a, b in zip(pos, dir))
                path.append(pos)
            elif cmd == 'L':
                dir = (dir[1], -dir[0])
            elif cmd == 'R':
                dir = (-dir[1], dir[0])
        return path

    def compute_bounding_box(path):
        min_x = min(pos[0] for pos in path)
        min_y = min(pos[1] for pos in path)
        max_x = max(pos[0] for pos in path)
        max_y = max(pos[1] for pos in path)
        return (min_x, min_y), (max_x, max_y)

    def build_grid(path):
        min_xy, max_xy = compute_bounding_box(path)
        width = max_xy[0] - min_xy[0] + 1
        height = max_xy[1] - min_xy[1] + 1
        grid = [[' '] * width for _ in range(height)]
        for x, y in path:
            grid[y - min_xy[1]][x - min_xy[0]] = '*'
        return grid

    def grid_to_string(grid):
        return '\r\n'.join(''.join(row) for row in grid)

    code = simplify_code(code)
    path = compute_path(code)
    grid = build_grid(path)
    return grid_to_string(grid)
__________________________
import re
from enum import Enum
from operator import itemgetter
from typing import List, Tuple, Set, Generator, Match


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
    code = unroll_code(code)
    for move in re.finditer(r'([LRF])(\d*)', code):
        action = move.group(1)
        n_times = int(move.group(2)) if move.group(2) else 1
        yield action, n_times
        
        
def unroll_code(code: str) -> str:
    base_command = r'[FLR]\d*'
    composed = fr'\((?P<command>({base_command})+)\)(?P<repeat>\d*)'
    
    while True:
        prev_code = code
        code = re.sub(composed, unroll_command, prev_code)
        if code == prev_code:
            break
    return code

def unroll_command(match: Match) -> str:
    repeat = int(match['repeat']) if match['repeat'] else 1
    return match['command'] * repeat
    

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
from collections import defaultdict

def execute_rs1(code):
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

def execute(code):
    repl = lambda m: m.group(1) * (int(m.group(2)) if m.group(2) else 1)
    while code != (code_repl := re.sub(r"\((\w*)\)(\d*)", repl, code)):
        code = code_repl
    return execute_rs1(code)
__________________________
def execute(code):
    R, r, c, dr, dc = {(0, 0)}, 0, 0, 0, 1
    D = {(1, 0):{'R':(0, -1), 'L':(0, 1)}, (-1, 0):{'R':(0, 1), 'L':(0, -1)}, (0, 1):{'R':(1, 0), 'L':(-1, 0)}, (0, -1):{'R':(-1, 0), 'L':(1, 0)}}
    
    while ')' in code:
        for i, v in enumerate(code):
            if v == '(': lastopen = i
            if v == ')':
                n, k = '', i + 1
                while code[k:k+1].isdigit(): 
                    n, k = n + code[k], k + 1                
                code = code[:lastopen] + code[lastopen+1:i] * int(n or '1') + code[k:]
                break

    for cmd in code.replace('R', ' R').replace('L', ' L').replace('F', ' F').strip().split():
        cmd, n = cmd[:1], int(cmd[1:]) if cmd[1:] else 1
        for _ in range(n):
            if cmd in 'RL':             
                dr, dc = D[(dr, dc)][cmd]
            else:
                r, c = r + dr, c + dc
                R.add((r, c))
                
    mnr, mnc = min(r for r, _ in R), min(c for _, c in R)

    R = {(r - mnr, c - mnc) for r, c in R}
    
    mxr, mxc = max(r for r, _ in R), max(c for _, c in R)           
    
    return '\r\n'.join(''.join(' *'[(r, c) in R] for c in range(mxc+1)) for r in range(mxr+1))
__________________________
import re
from collections import defaultdict, deque
def execute(code):
    dirs = deque([(0, 1), (-1, 0), (0, -1), (1, 0)])
    yarr, xarr = [0], [0]
    while True:
        code, n = re.subn('\(([^()]+)\)(\d*)', lambda m: m.group(1) * int(m.group(2) or 1), code)
        if not n:
            break
    for c in ''.join(a * int(b or 1) for a, b in re.findall('(\D)(\d*)', code)):
        if c == 'F':
            dy, dx = dirs[0]
            xarr.append(xarr[-1] + dx)
            yarr.append(yarr[-1] + dy)
        if c == 'L':
            dirs.rotate(-1)
        if c == 'R':
            dirs.rotate(1)
    xmin, xmax = min(xarr), max(xarr)
    ymin, ymax = min(yarr), max(yarr)
    d = dict(zip(zip(yarr, xarr), '*' * len(xarr)))
    return '\r\n'.join(''.join(d.get((y, x), ' ') for x in range(xmin, xmax + 1)) for y in range(ymin, ymax + 1))
__________________________
import re


def highlight(code):
    code = re.sub(r"(F+)", '<span style="color: pink">\g<1></span>', code)
    code = re.sub(r"(L+)", '<span style="color: red">\g<1></span>', code)
    code = re.sub(r"(R+)", '<span style="color: green">\g<1></span>', code)
    code = re.sub(r"(\d+)", '<span style="color: orange">\g<1></span>', code)
    return code


def clear_repetition(code):
    sub_code = [sec.span() for sec in re.finditer(r"(\([F+|R+|L+|\d+]+\))(\d*)", code)]
    if not sub_code:
        return code
    last = 0
    code_array = []
    for start, end in sub_code:
        code_array.append(code[last:start])
        section = code[start + 1:end].split(")")
        multi = int(section[1]) if section[1].isdigit() else 1
        code_array.append(section[0] * multi)
        last = end
    code_array.append(code[last:])
    return clear_repetition("".join(code_array))


def simplify_code(code):
    code = clear_repetition(code)
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
import numpy as np
import operator
import re
from time import perf_counter

def move_point(point, dir):
    return tuple(map(operator.add, point, dir))

def is_inside(point, arr):
    return 0 <= point[0] < arr.shape[0] and \
           0 <= point[1] < arr.shape[1]

def find_closing_bracket(tokens, bracket_start):
    bracket_lvl = 1
    pos = bracket_start
    while bracket_lvl > 0:
        pos += 1

        if tokens[pos] == '(':
            bracket_lvl += 1
        elif tokens[pos].startswith(')'):
            bracket_lvl -= 1
            
    return pos

DIRS = [
    ( 0,  1),  # Right
    ( 1,  0),  # Down
    ( 0, -1),  # Left
    (-1,  0),  # Up
]


class Cmd:
    name = ''
    count = 0
    
    def __init__(self, token):
        self.name = token[0]
        self.count = int(token[1:]) if len(token) > 1 else 1


class CmdGroup:
    cmds = None
    count = 1
    
    def __init__(self, tokens, count=1):
        self.parse_brackets(tokens)
        
        self.cmds = [Cmd(cmd) if isinstance(cmd, str) else cmd for cmd in tokens]
        self.count = count
        
    def parse_brackets(self, tokens):
        while '(' in tokens:
            start = tokens.index('(')
            end = find_closing_bracket(tokens, start)
            
            count = int(tokens[end][1:]) if len(tokens[end]) > 1 else 1
            
            tokens[end] = CmdGroup(tokens[start + 1:end], count)
            
            del tokens[start:end]


class Robot:
    def __init__(self):
        self.pos = (0, 0)
        self.dir = 0
        self.seen = [self.pos]
        self.cmds = {
            'F': lambda c: self.move_forward(c),
            'R': lambda c: self.rotate(c),
            'L': lambda c: self.rotate(-c),
        }
    
    def execute(self, cmd_group):
        for cmd in cmd_group.cmds * cmd_group.count:
            if isinstance(cmd, Cmd):
                self.cmds[cmd.name](cmd.count)
            elif isinstance(cmd, CmdGroup):
                self.execute(cmd)
    
    def rotate(self, count):
        self.dir += count
        self.dir %= 4
    
    def move_forward(self, count):
        for _ in range(count):
            self.pos = move_point(self.pos, DIRS[self.dir])
            self.seen.append(self.pos)
        
    def __str__(self):
        min_x, min_y = min(seen[0] for seen in self.seen), min(seen[1] for seen in self.seen)
        max_x, max_y = max(seen[0] for seen in self.seen), max(seen[1] for seen in self.seen)
        
        return '\r\n'.join(
            ''.join('*' if (x, y) in self.seen else ' ' for y in range(min_y, max_y + 1))
            for x in range(min_x, max_x + 1))


def tokenizer(code):
    return re.findall('[FRL]\d*|\(|\)\d*', code)


def execute(code):
    tokens = tokenizer(code)
    
    cmd_group = CmdGroup(tokens)
    
    robot = Robot()
    robot.execute(cmd_group)
    
    return str(robot)
__________________________
import re

def expand(code):
    c = ''
    while code:
        a = re.match('([LFR]\d*)', code)
        b = re.match('(\))(\d*)', code)
        if code[0] == '(':
            r, code = expand(code[1:])
            c += r
        elif a:
            c += a.group(1)
            code = code[a.end():]
        elif b:
            l = int(b.group(2)) if b.group(2) else 1
            c = c*l
            return c, code[b.end():]
        else: raise RuntimeError('Invalid cmd ---> '+code)
    return c

def execute(code):
    dr = {0:(0,1), 1:(1,0), 2:(0,-1), 3:(-1,0)}
    cod = [[0,0]]
    d = 0
    code = expand(code)
    a = re.match('([LFR])(\d*)', code)
    while a:
        op = a.group(1)
        n = int(a.group(2)) if a.group(2) else 1
        if op == 'R': d = (d+n)%4
        elif op == 'L': d = (d-n)%4
        else: cod.append([cod[-1][0]+dr[d][0]*n, cod[-1][1]+dr[d][1]*n])
        code = code[a.end():]
        a = re.match('([LFR])(\d*)', code)
    if len(cod) < 2: return '*'
    mx = min(sorted(c[0] for c in cod))
    my = min(sorted(c[1] for c in cod))
    cod = [[c[0]-mx,c[1]-my] for c in cod]
    mx = max(sorted(c[0] for c in cod))+1
    my = max(sorted(c[1] for c in cod))+1
    u = [[' ' for _ in range(my)] for _ in range(mx)]
    for i in range(len(cod)-1):
        x1 = cod[i][0]
        y1 = cod[i][1]
        x2 = cod[i+1][0]
        y2 = cod[i+1][1]
        if x1 == x2:
            for y in range(min(y1,y2),max(y1,y2)+1): u[x1][y] = '*'
        else:
            for x in range(min(x1,x2),max(x1,x2)+1): u[x][y1] = '*'
    return '\r\n'.join(''.join(u[x][y] for y in range(my)) for x in range(mx))
