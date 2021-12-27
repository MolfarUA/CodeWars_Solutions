from itertools import permutations


def play_flou(game_map):
    flou = Flou(parse_grid(game_map))
    moves = flou.solve()
    return format_moves(moves) if moves else False


def format_moves(moves):
    dirs = {1: 'Right', 1j: 'Down', -1: 'Left', -1j: 'Up'}
    return [[int(pos.imag), int(pos.real), dirs[dir_]] for pos, dir_ in moves]


def parse_grid(game_map):
    map_ = game_map.splitlines()
    return [[int(map_[y][x] == 'B') for x in range(1, len(map_[0]) - 1)] for y in range(1, len(map_) - 1)]


class Flou:
    def __init__(self, map_):
        self.map_ = map_
        self.set_grid()
        self.rotations = {1: 1j, 1j: -1, -1: -1j, -1j: 1}

    def solve(self):
        all_blocks = permutations(self.blocks)
        for blocks in all_blocks:
            solved = self.dfs(blocks, 0, ())
            if solved:
                return solved
        return False

    def dfs(self, blocks, i, all_moves):
        if i == len(blocks):
            return all_moves if all(v for v in self.grid.values()) else False

        block = blocks[i]
        for move in self.rotations:
            if self.valid_move(move, block):
                moves = self.get_moves(move, block)
                valid_moves = self.dfs(blocks, i + 1, all_moves + ((block, move),))
                if valid_moves:
                    return valid_moves
                else:
                    self.set_moves(moves, 0)
        return False

    def get_moves(self, move, block):
        moves = []
        running = True
        while running:
            block += move
            moves.append(block)
            self.grid[block] = 1
            if not self.valid_move(move, block):
                next_move = self.rotations[move]
                if self.valid_move(next_move, block):
                    move = next_move
                else:
                    running = False
        return moves

    def set_moves(self, moves, val):
        for move in moves:
            self.grid[move] = val

    def valid_move(self, move, block):
        return not self.grid.get(block + move, 1)

    def set_grid(self):
        self.blocks = []
        self.grid = {}
        for y, row in enumerate(self.map_):
            for x, sq in enumerate(row):
                pos = x + 1j * y
                self.grid[pos] = sq
                if sq:
                    self.blocks.append(pos)
                    
______________________________________________
class State:
    
    DIRECTIONS = [
        ('Left', -1, 0),
        ('Up', 0, -1),
        ('Right', 1, 0),
        ('Down', 0, 1),
    ]

    def __init__(self, plan, starts, moves=None):
        self.plan = plan
        self.starts = starts
        self.moves = moves or []

    @staticmethod
    def parse_state(game_map):
        plan = [
            [
                0 if c == '.' else 1
                for c in row
                if c not in '|-+'
            ]
            for row in game_map.split('\n')
            if row.strip()
        ]
        plan = [r for r in plan if r]
        starts = [
            (x, y)
            for y, row in enumerate(plan)
            for x, c in enumerate(row)
            if c != 0
        ]
        for i, (x, y) in enumerate(starts, 1):
            plan[y][x] = i
        return State(plan, starts)

    def walk(self, start, direction):
        direction_name, dx, dy = self.DIRECTIONS[direction]
        new_plan = [list(row) for row in self.plan]
        x, y = start
        colour = new_plan[y][x]
        steps, moves = 0, 0
        while True:
            nx, ny = x + dx, y + dy
            if (
                    0 <= ny < len(new_plan) and
                    0 <= nx < len(new_plan[ny]) and
                    new_plan[ny][nx] == 0
            ):
                # Free cell inside bounds of plan, so mark it and carry on
                new_plan[ny][nx] = colour
                steps += 1
                moves += 1
                x, y = nx, ny
            else:
                # Change direction
                direction = (direction + 1) % 4
                direction_name, dx, dy = self.DIRECTIONS[direction]
                if steps == 0:
                    # No move since last change of direction
                    break
                steps = 0

        if moves == 0:
            # Invalid move, cannot move at least one step
            return None
        # Return updated plan we get after a valid move is performed
        return new_plan

    def solve(self):
        if not self.starts and min(x for row in self.plan for x in row) > 0:
            # Found a solution
            yield self
        else:
            for i in range(len(self.starts)):
                start = self.starts[i]
                other_starts = [p for j, p in enumerate(self.starts) if j != i]
                for j in range(len(self.DIRECTIONS)):
                    new_plan = self.walk(start, j)
                    if new_plan is None:
                        # Not a valid move
                        continue
                    
                    # Performed a valid move, lets see if we have solved or can solve from here
                    move = [start[1], start[0], self.DIRECTIONS[j][0]]
                    new_moves = self.moves + [move]
                    yield from State(new_plan, other_starts, new_moves).solve()


def play_flou(game_map):
    initial_state = State.parse_state(game_map)
    for solution_state in initial_state.solve():
        return solution_state.moves
    return False

__________________________________________
from itertools import product, permutations
directions = {'Right', 'Down', 'Left', 'Up'}


def read_map(game_map): #reads map and makes a few global variables.
    global moves, size, start_points, map, next
    map = list(game_map)
    size = game_map.index('|') 
    start_points = [i for i, c in enumerate(map) if c=='B']
    moves = {'Right':1, 'Left':-1, 'Up':-size, 'Down':size}
    next = {1:size, size:-1, -1:-size, -size:1}


def check_sol(perm, dirs):
    my_map = map[:]
    for i in range(len(perm)): #applies each solution step.
        step = moves[dirs[i]]
        pos = perm[i]
        if my_map[pos + step] != '.': 
             return False
        while True: #changes cell colors until reaches a barrier.
            pos += step
            if my_map[pos] == '.': #no barrier, changes the color and move on.
                my_map[pos] = 'b'
                continue
            elif my_map[pos -step + next[step]] != '.': #change direction not possible, goes to next solution step.
                break
            else: #changes direction.
                pos -= step
                step = next[step]
    return '.' not in my_map


def play_flou(game_map): #checks all possible solutions.
    read_map(game_map)
    for dirs in product(directions, repeat=len(start_points)):
        for perm in permutations(start_points):
            if check_sol(perm, dirs): return [[(perm[i]//size - 1), perm[i]%size - 1]+[dirs[i]] for i in range(len(perm))]
    return False

____________________________________________________
from collections import deque, Counter
from itertools import permutations

DIR = {'Up': 'Right', 'Right': 'Down', 'Down': 'Left', 'Left': 'Up'}
DIRECTIONS = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}

def validate(board):
    c = Counter(''.join([''.join(i[1:-1]) for i in board[1:-1]]))
    return all(j > 1 and i != '.' for i, j in c.items()) and sum(c.values()) == (len(board) - 2) * (len(board[1]) - 2)

def fill_color(board, direction, position, put):
    board, (i,j) = list(map(list, board)), position 
    while 1:
        inc, dec = DIRECTIONS[direction]
        k, l = i + inc, j + dec
        
        if board[k][l] != '.' : direction = DIR[direction]
        
        inc, dec = DIRECTIONS[direction]
        i, j = i+inc, j+dec
        
        if board[i][j] != '.' : break
        board[i][j] = put
    return [''.join(i) for i in board]
    
def play_flou(board):
    N = iter('ABCDEFGHIJKLM')
    board = [[next(N) if j.isalpha() else j for j in i] for i in board.splitlines()]
    AVl = [(i, k) for i, j in enumerate(board) for k, l in enumerate(j) if l.isalpha()]
    
    for points in permutations(AVl):
        Q = deque([[board, list(points), []]])
        while Q:
            grid, point, movement = Q.popleft()

            if validate(grid) : return [[j[0]-1, j[1]-1, i] for i, j in zip(movement, points)]
            if not point : continue
            
            to_change = point.pop(0)

            for i in 'Up Right Left Down'.split():
                k, l = to_change
                inc, dec = DIRECTIONS[i]
                if grid[k + inc][l + dec] == '.':
                    board_ = fill_color(grid, i, to_change, board[to_change[0]][to_change[1]])
                    Q.append([board_, point[:], movement + [i]])
    return False

______________________________________________________________
from itertools import permutations

moves = [(-1,0),(0,1),(1,0),(0,-1)]
names = ['Up', 'Right', 'Down', 'Left']

def fill(b, si, sj, rows, cols, dir, moved=False):
    di, dj = moves[dir%4]
    ni, nj = si + di, sj + dj
    if ni < 0 or ni == rows or nj < 0 or nj == cols or b[ni * cols + nj]:
        return moved
    while ni >= 0 and nj >= 0 and ni < rows and nj < cols and not b[ni * cols + nj]:
        b[ni * cols + nj] = True
        ni, nj = ni + di, nj + dj
    return fill(b, ni - di, nj - dj, rows, cols, dir+1, True)


def check_done(b):
    return False not in b


def check_combination(combi, in_b, rows, cols):
    i, j = combi[0]
    for dir in range(4):
        b = in_b[:]
        if not fill(b, i, j, rows, cols, dir):
            continue
        if len(combi) > 1:
            res = check_combination(combi[1:], b, rows, cols)
            if res:
                res.insert(0, [i,j,names[dir]])
                return res
        else:
            if check_done(b):
                return [[i,j,names[dir]]]
        

def play_flou(game_map):
    b = [not x == '.'  for l in game_map.split('\n')[1:-1] for x in l[1:-1]]
    rows = len(game_map.split('\n')[1:-1])
    cols = len(game_map.split('\n')[1:-1][0]) - 2
    starts = [(i-1, j-1) for i,l in enumerate(game_map.split('\n')) for j,x in enumerate(l) if x == 'B']
    combinations = [list(x) for x in permutations(starts)]
    for combination in combinations:
        res = check_combination(combination, b, rows, cols)
        if res:
            return res
    return False

_______________________________________________________
def play_flou(game_map, blocks=None):
    board = []
    for row in game_map.split('\n'):
        board.append(list(row))
    
    blocks = []
    for r in range(1, len(board) - 1):
        for c in range(1, len(board[0]) - 1):
            if board[r][c] == 'B':
                blocks.append((r, c))
    
    result = solve(board, blocks)
    return result

def solve(board, blocks, count=0):   
    if len(blocks) == 0:
        return [] if count == (len(board)-2) * (len(board[0])-2) else False

    for i in range(len(blocks)):
        blocks2 = list(blocks)
        block = blocks2.pop(i)
        for d in ['Up', 'Down', 'Left', 'Right']:
            board2 = [list(row) for row in board]
            count2 = move(board2, block, d) + 1
            if count2 > 1:
                result = solve(board2, blocks2, count + count2)
                if result != False:
                    return [[block[0]-1, block[1]-1, d]] + result  
    return False

ds = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
d2s = {'Up': 'Right', 'Down': 'Left', 'Left': 'Up', 'Right': 'Down'}
def move(board, block, d):
    dr, dc = ds[d]
    r, c = block
    count = 0
    while True:
        count += board[r][c] not in {'B', 'x'}
        board[r][c] = 'x'
        r, c = r + dr, c + dc       
        if board[r][c] in {'-', '|', 'x', 'B'}:
            break
    r, c = r - dr, c - dc
    return 0 if count == 0 else count + move(board, (r, c), d2s[d])
    
__________________________________________________
directions = [('Right',0,1),('Down',1,0),('Left',0,-1),('Up',-1,0)]
rotate = lambda l: l.append(l.pop(0))

def play_flou(game_map):
    lines = game_map.splitlines()
    I, J = len(lines)-2, len(lines[0])-2
    bag = {(i-1,j-1) for i,r in enumerate(lines) for j,c in enumerate(r) if c is 'B'}
    if len(bag) == 1:
        i, j = bag.copy().pop()
        if not ((i in (0,I-1) and j in (0,J-1)) or (i in (1,I-2) and j in (1,J-2))):
            return False
    def recurse(bag, color_blocks=list(bag), solution=list()):
        if len(bag) == I*J and not color_blocks:
            return solution
        for cb in color_blocks:
            never = True
            cbs = color_blocks.copy()
            cbs.remove(cb)
            pref = 'Right'
            if cb[1] == J-1: pref = 'Down'
            if cb[0] == I-1: pref = 'Left'
            if cb[1] == 0: pref = 'Up'
            while directions[0][0] != pref: rotate(directions)
            for (d, di, dj) in tuple(directions):
                i,j = cb[0] + di, cb[1] + dj
                if (i, j) in bag or i<0 or I<=i or j<0 or J<=j: continue
                while directions[0][0] != d: rotate(directions)
                b = bag.copy()
                len_b = None
                changed = stuck = False
                while not stuck:
                    stuck = True
                    while (i, j) not in b and 0<=i and i<I and 0<=j and j<J:
                        b.add((i,j))
                        i += di
                        j += dj
                        stuck = False
                        changed = True
                    rotate(directions)
                    i -= di
                    j -= dj
                    (_,di,dj) = directions[0]
                    i += di
                    j += dj
                if changed:
                    never = False
                    r = recurse(b, cbs, solution + [(cb[0],cb[1],d)])
                    if r:
                        return r
            if never:
                return False
        return False
    return recurse(bag)

_________________________________
from itertools import permutations

def play_flou(game_map):
  game_map = game_map.split('\n')
  ly, lx = len(game_map) - 2, len(game_map[0]) - 2
  point = [] #  список исходных цветных блоков
  for y in range(1, ly + 1):
    for x in range(1, lx + 1):
      if game_map[y][x] == 'B':
        point += [(y-1, x-1)]
  
  def has(y, x):
    for j in visited:
      if (Y, X) in j:
        return True
    return False
  
  k = len(point) #  кол-во исходных ЦБ
  for P in sorted(set(permutations(range(k), k))):
    # direction = i: 0 - Right, 1 - Down, 
    #                2 - Left, 3 - Up
    stack = [(0, i) for i in range(4)]
    pos, visited = [], [set(point)]
    while stack:
      el = stack.pop()
      if not el:
        pos.pop()
        visited.pop()
        continue
    
      y, x = point[P[el[0]]]
      S = set() # Множество координат, образованное
      #           от заданного вектора движения (el[1])
      direction, deadlock = el[1], True
      while True:
        Y, X = y, x
        if direction % 2: Y += 1 - 2*(direction // 2)
        else: X += 1 - 2*(direction // 2)
        flag = True
        if -1 < Y < ly and -1 < X < lx:
          if not (Y, X) in S and not has(Y, X):
            flag = deadlock = False
            y, x = Y, X
            S.add((y, x))
        if flag:
          direction = (direction + 1) % 4
          # Конец движения, после 2-ух поворотов подряд
          if deadlock: break
          deadlock = True
      if S:
        stack += [0]
        pos, visited = pos + [el], visited + [S]
        if el[0] < k - 1:
          stack += [(el[0] + 1, i) for i in range(4)]
        # Ecли кол-во образованных координат, после
        # задействования всех исходных цветных блоков
        # равна площади поля - выодим из цикла
        elif sum(len(_) for _ in visited) == ly*lx:
          break
    if pos: break
  d = ['Right', 'Down', 'Left', 'Up']
  return [[*point[P[i]], d[j]] for i, j in pos]

__________________________________________________________________
from itertools import permutations
def play_flou(game_map):
    map = game_map.split("\n")
    map = [[y for y in x[1:-1]] for x in map[1:-1]]
    all_moves = set()
    x_limit = len(map)
    y_limit = len(map[0])
    all_elements = set()
    direction = {1: "Right", 2:"Down", 3: "Left", 4: "Up"}
    initial_moves = set()
    class Flou:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.answer = ""
            self.moves = set()
            self.save_x = x
            self.save_y = y

        def _down(self):
            x = self.x
            check = len(self.moves)
            while True:
                x += 1
                if 0 <= x < x_limit and map[x][self.y] == "." and not (x, self.y) in all_moves:
                    self.moves.add((x, self.y))
                    all_moves.add((x, self.y))
                else:break
            self.x = x - 1
            if check == len(self.moves): return False
            else:
                return True

        def _right(self):
            check = len(self.moves)
            y = self.y
            while True:
                y += 1
                if 0 <= y < y_limit and map[self.x][y] == "." and not (self.x, y) in all_moves:
                    self.moves.add((self.x, y))
                    all_moves.add((self.x, y))
                else:
                    break
            self.y = y - 1
            if check == len(self.moves):
                return False
            else:
                return True

        def _up(self):
            check = len(self.moves)
            x = self.x
            while True:
                x = x - 1
                if 0 <= x < x_limit and map[x][self.y] == "." and not (x, self.y) in all_moves:
                    self.moves.add((x, self.y))
                    all_moves.add((x, self.y))
                else:
                    break
            self.x = x + 1
            if check == len(self.moves):
                return False
            else:
                return True

        def _left(self):
            y = self.y
            check = len(self.moves)

            while True:
                y += -1
                if 0 <= y < y_limit and map[self.x][y] == "." and (self.x,y) not in all_moves:
                    self.moves.add((self.x, y))
                    all_moves.add((self.x, y))
                else:
                    break
            self.y = y + 1
            if check == len(self.moves):
                return False
            else:
                return True

        def _do(self, current):
            if current == 1:
                return self._right()
            if current == 2:
                return self._down()
            if current ==3:
                return self._left()
            if current == 4:
                return self._up()

        def make_move(self, current):
            total = 0
            checker = current
            while True:
                result = self._do(current)
                total += 1
                current += 1
                if current == 5:current = 1
                if not result:break
            dir = direction[checker]
            self.answer = [dir, self.save_x, self.save_y]
            if total == 0:return False
            else:return True

    for row,part in enumerate(map):
        for column, i in enumerate(part):
            if i == "B":
                all_elements.add(Flou(row,column))
                all_moves.add((row, column))

    def back_before(element):
        nonlocal all_moves
        element.answer = ""
        all_moves = all_moves - element.moves
        element.x = element.save_x
        element.y = element.save_y
        element.moves = set()




    def do(current):
        if current == limit_of_elements:
            if len(all_moves) == x_limit * y_limit:
                for x in data:
                    if x.moves:continue
                    else:return False
                return True
            else:return False
        element = data[current]
        for x,dir in enumerate(["Right", "Down", "Left", "Up"], start=1):
            element.make_move(x)
            result = do(current + 1)
            if result:return True
            back_before(element)



    limit_of_elements = len(all_elements)
    for perm in permutations(all_elements):
        data = list(perm)
        result = do(0)
        if result:
            return [(element.answer[1], element.answer[2], element.answer[0]) for element in data]
