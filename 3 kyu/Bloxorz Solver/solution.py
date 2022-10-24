5a2a597a8882f392020005e5

from collections import deque

def blox_solver(arr):
    
    isSame = lambda A,B: A == B                      # bloxorz has is pieces superposed
    isVert = lambda A,B: A[0] != B[0]                # bloxorz is vertical   (looking the board from above)
    isHorz = lambda A,B: A[1] != B[1]                # bloxorz is horizontal (looking the board from above)
    
    def moveBlox(m,A,B):                             # Move bloxorz according to its current position and the expected direction
        (xA,yA), (xB,yB) = A,B
        dx,dy, fA,fB = DELTAS[m]
        nA = ( (xA + dx * (1 + fA(A,B))), (yA + dy * (1 + fA(A,B))) )
        nB = ( (xB + dx * (1 + fB(A,B))), (yB + dy * (1 + fB(A,B))) )
        return tuple(sorted((nA,nB)))
    
    #               dx,dy  conditional modifiers (fA, fB)
    DELTAS = {"U": (-1,0,  isSame, isVert),
              "D": ( 1,0,  isVert, isSame),
              "L": (0,-1,  isSame, isHorz),
              "R": (0, 1,  isHorz, isSame)}
    INF = float("inf")
    
    
    """ Accumulate data """
    board = set()
    for x,line in enumerate(arr):
        for y,c in enumerate(line):
            if c == '0': continue
            board.add((x,y))
            if   c == 'B': blox = ((x,y), (x,y))     # initial position
            elif c == 'X': end  = ((x,y), (x,y))     # finish position
    
    """ VERY crude BFS search """
    q, seen, prev, round = deque([blox]), {blox: 0},  {blox: (None,None)}, 0
    while q and q[-1] != end:
        round += 1
        A,B = blox = q.pop()
        for m in DELTAS:
            nA,nB = nblox = moveBlox(m,A,B)
            if nA in board and nB in board and round < seen.get(nblox, INF):
                q.appendleft(nblox)
                seen[nblox] = round
                prev[nblox] = (blox, m)
    
    """ rebuild the shortest path """
    path, (pos,m) = [], prev[end]
    while m is not None:
        path.append(m)
        pos,m = prev[pos]
        
    return ''.join(path[::-1])
_________________________________
def blox_solver(ar):
    # width of grid (+1 to add an extra 0 on the right)
    w = len(ar[0])+1
    # height of grid (+1 to add an extra 0 on the bottom)
    h = len(ar)+1
    # merge lines in a single string
    grid = "".join(line+"0" for line in ar)+"0"*w
    # find start and end position
    start = grid.find('B')
    end = grid.find('X')
    
    # list of positions for a breadth first search initialized with the starting posiiton
    # a position is a 4-tuple ( orientation, index in grid of first 1x1 block, 
    #                           index in gridof second 1x1 block, path to this position )
    positions = [(0,start,start,"")]
    
    # define moves effect on positions of the blocks with a truple 
    # - the new orientation is given
    # - shift on the first index
    # - shift on the second index
    # up and down moves shifts the index in the grid by w or 2w
    # left and right moves shifts the index in the grid by 1 or 2
    MOVES = [{'U':(1,-2*w,-w), 'D':(1,w,2*w), 'L':(2,-2,-1), 'R':(2,1,2)}, # orientation 0: upright
             {'U':(0,-w,-2*w), 'D':(0,2*w,w), 'L':(1,-1,-1), 'R':(1,1,1)}, # orientation 1: flat vertical
             {'U':(2,-w,-w),   'D':(2,w,w),   'L':(0,-1,-2), 'R':(0,2,1)}] # orientation 2: flat horizontal
    
    visited = set() # empty set of visited positions
    
    #breath first search
    while True:       
        pos = positions.pop(0)                             # take the first position
        if pos[:3] in visited: continue                    # skip already visited positions (skipping the path)
        visited.add(pos[:3])                               # add position to visited (skipping the path)
        if grid[pos[1]]=='0' or grid[pos[2]]=='0': continue # skip if on open air
        if pos[1]==end and pos[0]==0: break                 # exit found

        for move,effect in MOVES[pos[0]].items(): # make all 4 moves from current position and add to positions list
            positions.append((effect[0],pos[1]+effect[1],pos[2]+effect[2],pos[3]+move))
        
    # return path of last visited position
    return pos[3]
_________________________________
# Describes all the possible moves from a given position
# 1 & 2 represent the initial position of the block,
# U, D, L & R represent the new position

# Both offsets applied to the only block, position is a single coordinate
VERTICAL_MOVES = [                #   U
    ((-2, 0), (-1, 0), 'U'),      #   U
    ((0, 1), (0, 2), 'R'),        # LL1RR 
    ((1, 0), (2, 0), 'D'),        #   D
    ((0, -2), (0, -1), 'L'),      #   D
]

# Offsets applied per block, positions lie on a single row
ROW_MOVES = [
    ((-1, 0), (-1, 0), 'U'),      #  UU
    ((None, None), (0, 1), 'R'),  # L12R
    ((1, 0), (1, 0), 'D'),        #  DD
    ((0, -1), (None, None), 'L'),
]

# Offsets applied per block, positions lie on a single column
COL_MOVES = [
    ((-1, 0), (None, None), 'U'), #  U
    ((0, 1), (0, 1), 'R'),        # L1R
    ((None, None), (1, 0), 'D'),  # L2R
    ((0, -1), (0, -1), 'L'),      #  D
]

def get_alignment(position):
    """Determine the alignment of the block based upon position(s)"""
    if len(position) == 1:
        # Stood vertically
        return 'V'
    if position[0][0] == position[1][0]:
        # Blocks on common row
        return 'R'
    # Must have common column
    return 'C'

def gen_moves(position, ground):
    """
    Given a current position and available places to land, yield all possible
    new positions and direction taken when the position is on the ground
    """
    alignment = get_alignment(position)
    if alignment == 'V':
        r, c = position[0]
        for (dr1, dc1), (dr2, dc2), direction in VERTICAL_MOVES:
            p1 = r + dr1, c + dc1
            p2 = r + dr2, c + dc2
            if p1 in ground and p2 in ground:
                yield (p1, p2), direction

    else:  # alignment in ['R', 'C']
        moves = ROW_MOVES if alignment == 'R' else COL_MOVES
        (r1, c1), (r2, c2) = position
        for (dr1, dc1), (dr2, dc2), direction in moves:
            p1 = (r1 + dr1, c1 + dc1) if dr1 is not None else None
            p2 = (r2 + dr2, c2 + dc2) if dr2 is not None else None
            in1 = None if not p1 else p1 in ground
            in2 = None if not p2 else p2 in ground
            if p1 and in1 and p2 and in2:
                yield (p1, p2), direction
            if p1 and in1 and not p2:
                yield (p1, ), direction
            if p2 and in2 and not p1:
                yield (p2, ), direction

def parse_state(ar):
    """Extact mapping information from ASCII art supplied"""
    # Valid coordinates for a block
    ground = set()
    # Initial coordinates of the block(s)
    position = []
    # Coordinates of exits
    exit = []
    for r, row in enumerate(ar):
        for c, val in enumerate(row):
            if val != '0':
                ground.add((r, c))
            if val == 'B':
                position.append((r, c))
            if val == 'X':
                exit.append((r, c))
    return tuple(position), ground, tuple(exit)

def blox_solver(ar):
    """Uses a depth first algorithm to solve a 'Bloxors' problem"""
    position, ground, exit = parse_state(ar)

    # Places we have visited so we don't get into a loop, e.g. LRLRLRLRL ... heat death of universe
    previous_positions = set(position)
    # Latest place to arrive in current cycle
    edge_positions = [(position, '')]

    while edge_positions:
        # Prep for next depth cycle
        new_edges = []
        # Process current depth cycle
        for edge_position, move_history in edge_positions:
            for new_position, direction in gen_moves(edge_position, ground):
                if new_position in previous_positions:
                    # Already been in this position, ignore this move
                    continue
                path = move_history + direction
                # Check to see if we have found a solution
                if all(p in exit for p in new_position):
                    return path
                previous_positions.add(new_position)
                # Add to things to process in next depth cycle
                new_edges.append((new_position, path))

        # Set up for the next depth cycle
        edge_positions = new_edges

    raise ValueError('No solution possible, BOO!')
_________________________________
def blox_solver(a):
    B, V = {(r, c):v for r, row in enumerate(a) for c, v in enumerate(row) if v in '1BX'}, {None}
    
    def move(b, d):
        r, c, y, x = (b[0][0], b[0][1]) + ((b[1][0], b[1][1]) if len(b) == 2 else (None, None))
        if len(b) == 1:
            m = {'U':((r-2, c), (r-1, c)), 'D':((r+1, c), (r+2, c)), 'R':((r, c+1), (r, c+2)), 'L':((r, c-2), (r, c-1))}[d]
        elif r == y:
            m = {'U':((r-1, c),(r-1, c+1)), 'D':((r+1, c),(r+1, c+1)), 'R':((r, x+1),), 'L':((r, c-1),)}[d]
        else:
            m = {'U':((r-1, c),), 'D':((y+1, c),), 'R':((r, c+1),(r+1, c+1)), 'L':((r, c-1),(r+1, c-1))}[d]
        
        # Check we have not already visited this position and that the position is on the board
        m = None if m in V or any(p not in B for p in m) else m
        V.add(m)
        return m
    
    P, X = [('', ([k for k in B if B[k] == 'B'].pop(),))], ([k for k in B if B[k] == 'X'].pop(),)

    while not any(m == X for _, m in P):
        P = [(p, m) for p, b in P for p, m in [(p, m) for p, m in [(p+d, move(b, d)) for d in 'LURD'] if m]]
    
    return [p for p, m in P if m == X].pop()
_________________________________
import collections
from enum import Enum

class Move(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'

Cord = collections.namedtuple('Pos', ['y', 'x'])
BlockCord = collections.namedtuple('Block', ['b1', 'b2'])

BlockMoves = collections.namedtuple('BlockMoves', ['block', 'moves'])

class Pos(Cord):
    def dx(self, d): return Pos(self.y, self.x + d)
    def dy(self, d): return Pos(self.y + d, self.x)
    def __eq__(self, o): return self.x == o.x and self.y == o.y
    def __hash__(self):
        return hash((self.y, self.x))

class Block(BlockCord):
        
    def __repr__(self):
        return "Block(({},{}), ({},{}))".format(self.b1.y, self.b1.x, self.b2.y, self.b2.x)
    
    def __eq__(self, o): return self.b1 == o.b1 and self.b2 == o.b2  
    
    def __hash__(self): return hash((self.b1, self.b2))
    
    def is_standing(self): return self.b1 == self.b2
    
    def is_same_column(self): return self.b1.x == self.b2.x
    
    def dx(self, d1, d2): return Block(self.b1.dx(d1), self.b2.dx(d2))

    def dy(self, d1, d2): return Block(self.b1.dy(d1), self.b2.dy(d2))

    def left(self):
        if self.is_standing(): return self.dx(-2, -1)
        if self.is_same_column(): return self.dx(-1, -1)
        return self.dx(-1, -2)

    def right(self):
        if self.is_standing(): return self.dx(1, 2)
        if self.is_same_column(): return self.dx(1, 1)
        return self.dx(2, 1)

    def up(self):
        if self.is_standing(): return self.dy(-2, -1)
        if self.is_same_column(): return self.dy(-1, -2)
        return self.dy(-1, -1)

    def down(self):
        if self.is_standing(): return self.dy(1, 2)
        if self.is_same_column(): return self.dy(2, 1)
        return self.dy(1, 1)

    def neighbors(self): 
        return ( (self.left(), Move.LEFT), (self.right(), Move.RIGHT), (self.up(), Move.UP), (self.down(), Move.DOWN) )

    def is_legal(self, check_fn):
         return check_fn(self.b1) and check_fn(self.b2)
        
    def legal_neighbors(self, check_fn): 
        return filter(lambda n: n[0].is_legal(check_fn), self.neighbors())
    
class Game:
    
    def __init__(self, maze):
        self.maze = maze
        self.check_fn = self.create_check_fn()
        self.start_pos = self.find_char('B')
        self.goal = self.find_char('X')   
        self.start_block = Block(self.start_pos, self.start_pos)
        
    def find_char(self, c):
        for y, l in enumerate(self.maze):
            if c in l: return Pos(y, l.index(c))
        raise IndexError("Cannot find %s" % c)
    
    def create_check_fn(self): 
        def fn(pos):
            if pos.x < 0 or pos.y < 0 or len(self.maze) <= pos.y:
                return False
            else:
                row = self.maze[pos.y]
                if len(row) <= pos.x: return False
                return row[pos.x] != '0'
        return fn
    
    def done(self, b):
        return b.is_standing() and b.b1 == self.goal
    
    def neighbors_with_history(self, b): 
        return map(lambda n: BlockMoves(n[0], b.moves + tuple([n[1]])), b.block.legal_neighbors(self.check_fn))
    
    def new_neighbors(self, neighbors, explored): 
        return filter(lambda n: n.block not in explored, neighbors)
    
    def new_neighbors_with_history(self, b, explored):
        s = self.neighbors_with_history(b)
        return self.new_neighbors(s, explored)
    
    def from_fn(self, initial, explored):
        if len(initial) == 0: return initial
        r = [next_bm for bm in initial for next_bm in self.new_neighbors_with_history(bm, explored)]
        explored = explored.union({ bm.block for bm in initial })
        return initial + r + self.from_fn(r, explored)

    def solution(self):
        s = [BlockMoves(self.start_block, ())]
        d = list(filter(lambda p: self.done(p.block), self.from_fn(s, set())))[0]
        return d.moves
        
def blox_solver(level):
    g = Game(level)
    s = g.solution()
    return "".join([ m.value for m in s ])
_________________________________
# half coordinates when the block is horizontal and whole coordinates when it's vertical

def blox_solver(ar):
    start, end = ([(x, y) for y in range(len(ar)) for x in range(len(ar[0])) if ar[y][x] == c][0] for c in 'BX')
    stack, seen = {start}, {start: ''}
    directions = {'U': (0, -3/2), 'D': (0, 3/2), 'L': (-3/2, 0), 'R': (3/2, 0)}
    
    def move(pos, dir):
        x, y = pos
        dx, dy = directions[dir]
        if x % 1 == 1/2 and dir in 'UD': 
            return (x, y + dy * 2/3)
        elif y % 1 == 1/2 and dir in 'LR':
            return (x + dx * 2/3, y)
        else: 
            return (x + dx, y + dy)      
    
    def validate(pos):
        if pos in seen: return False
        x, y = pos
        if not (0 <= x <= len(ar[0]) - 1 and 0 <= y <= len(ar) - 1): return False
        if x % 1 == 1/2: 
            return all(ar[int(y)][int(x + dx)] != '0' for dx in (1/2, -1/2))
        elif y % 1 == 1/2: 
            return all(ar[int(y + dy)][int(x)] != '0' for dy in (1/2, -1/2))
        else: 
            return ar[int(y)][int(x)] != '0'
        
    while len(stack):
        tmp = set()
        for pos in stack:
            for dir in directions:
                nx, ny = move(pos, dir)
                if validate((nx, ny)): 
                    seen[(nx, ny)] = seen[pos] + dir
                    tmp.add((nx, ny))
                if (nx, ny) == end:
                    return seen[(nx, ny)]
        stack = tmp.copy()
        
    return False
_________________________________
from collections import deque
#原理：从起始位置，遍历所有可以移动的方位，知道找到目标位置
def move_block(pos,move,ar):
    if len(pos) == 1: #垂直
        [pos0] = pos
        #横着靠近[0,0]位置靠前，方便后面处理
        if move == 'U': next_pos = [[pos0[0]-2,pos0[1]],[pos0[0]-1,pos0[1]]]
        if move == 'D': next_pos = [[pos0[0]+1,pos0[1]],[pos0[0]+2,pos0[1]]]        
        if move == 'L': next_pos = [[pos0[0],pos0[1]-2],[pos0[0],pos0[1]-1]]          
        if move == 'R': next_pos = [[pos0[0],pos0[1]+1],[pos0[0],pos0[1]+2]] 
    else:
        [pos0,pos1] = pos 
        
        if pos0[0] == pos1[0]:  #横着
            if move == 'U': next_pos = [[pos0[0]-1,pos0[1]],[pos1[0]-1,pos1[1]]]
            if move == 'D': next_pos = [[pos0[0]+1,pos0[1]],[pos1[0]+1,pos1[1]]]
            if move == 'L': next_pos = [[pos0[0],pos0[1]-1]]  #使用pos0坐标处理
            if move == 'R': next_pos = [[pos1[0],pos1[1]+1]]  #使用pos1坐标处理
        else:
            if move == 'U': next_pos = [[pos0[0]-1,pos0[1]]]  #使用pos0坐标处理
            if move == 'D': next_pos = [[pos1[0]+1,pos1[1]]] #使用pos1坐标处理
            if move == 'L': next_pos = [[pos0[0],pos0[1]-1],[pos1[0],pos1[1]-1]]
            if move == 'R': next_pos = [[pos0[0],pos0[1]+1],[pos1[0],pos1[1]+1]]        
    #判断next_pos的位置是否合理
    #1.位置是否越界2.是否进入了取值为0的区域
    for p in next_pos:
        if p[0]<0 or p[0]>=len(ar) or p[1]<0 or p[1]>=len(ar[0]):
            next_pos = []
        else:
            if ar[p[0]][p[1]] == '0':  #ar[i][j]是字符，不是数字类型
                next_pos = []
    return next_pos

def blox_solver(ar):
    #your code goes here. you can do it!
    #确认开始位置
    rpos = [[i,j] for i in range(len(ar)) for j in range(len(ar[0])) if ar[i][j] == 'B']
    #构建一个deque双向队列，可以左进坐出，将上一次计算得到位置 ，作为下一次的开始，pos作为第一个值
    visit_pos = deque([(rpos,'','')])  #三个 字段，1：位置，2：move动作，3：所有动作记录
    visited = {} #记录访问过得位置

    while visit_pos:
        (pos,move,path) = visit_pos.popleft() #后进先出
        #已经访问过得位置直接跳过
        if str(pos) in visited:
            continue
        #标记当前需要访问的位置
        visited[str(pos)] = True
        
        #判断该位置是否为终点
        if len(pos) == 1 and ar[pos[0][0]][pos[0][1]] == 'X':
            return path
        
        #遍历该位置所有可能的动作直到下一个位置是终点
        for move in ['U','D','L','R']:
            n_pos = move_block(pos,move,ar)
            if len(n_pos) != 0:
                visit_pos.append((n_pos,move,path+move))
