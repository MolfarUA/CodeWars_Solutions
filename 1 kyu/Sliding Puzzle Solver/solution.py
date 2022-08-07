5a20eeccee1aae3cbc000090



from itertools import chain, combinations, accumulate
from heapq import heappush, heappop


def slide_puzzle(arr):
        
    def moveTargetTo(iX, i0, grid, target=None, lowLim=None):
        """ iX:     index in the grid of the position to work on
            i0:     blank index
            grid:   current grid state
            target: value to place at iX
            lowLim: value index under which the tiles cannot be/go (mostly optimization to avoid searching for inde'xes from the beginning)
        """
        if target is None: target = iX+1                                                # Default VALUE of the tile to move
        if lowLim is None: lowLim = iX                                                  # Default minimal index under

        iT       = grid.index(target, lowLim)                                           # Current position of the target tile
        xyX, xyT = divmod(iX,S), divmod(iT,S)                                           # Coords converted to (x,y) format
        dV,dH    = [b-a for a,b in zip(xyT,xyX)]                                        # Moves to do to reach the iX position, in (x,y) format
        sV,sH    = S * ((dV>0)-(dV<0)), (dH>0)-(dH<0)                                   # "Amount to move", step by step, in each direction
        
        paths = [ list(accumulate([iT] + [sH]*abs(dH) + [sV]*abs(dV))),                 # Build the two possible direct paths (dH->dV or dV->dH)
                  list(accumulate([iT] + [sV]*abs(dV) + [sH]*abs(dH))) ]                
        path  = next(filter(lambda p: not set(p) & forbid, paths))                      # Peek the first one that is fully allowed (at least one always exists)

        for iT,iTnext in zip(path, path[1:]):
            forbid.add(iT)                                                              # Set up the constraint
            i0, grid = moveBlank(i0, iTnext, grid, lowLim)
            forbid.remove(iT)                                                           # Relax"-relax... don't do it..."
            i0, grid = gridSwapper(i0, iT, grid)                                        # Final swap of blank and target
            movesToParadise.append(target)                                              # Register the moves needed

        forbid.add(iX)                                                                  # Archive iX as "definitively" done
        return i0, grid
    
        
    def conquerCorner(i0, grid, i1, i2, lowLim):
        v1, v2   = i1+1, i2+1,                                                          # Target values
        delta    = i2-i1                                                                # Step in idexes between i1 and i2
        delta2nd = S if delta == 1 else 1                                               # Step in idexes in the orthogonal direction
        shifted2 = i2+delta2nd                                                          # Temporary targeted index

        i0, grid = moveTargetTo(i2, i0, grid, target=v1, lowLim=lowLim)                 # Place v1 at i2 for now
        forbid.remove(i2)                                                               # Unlock to avoid impossible moves

        i0, grid = moveTargetTo(shifted2, i0, grid, target=v2, lowLim=lowLim)           # Place v2 next to v1, in the orthogonal direction
        forbid.remove(shifted2)                                                         # Unlock the temporary point
        
        i0, grid = moveBlank(i0, i1+2*delta2nd, grid, lowLim)                           # Try to move the blank away first (avoid to move v1 and v2 if they are correct)
        i0, grid = moveBlank(i0, i1, grid, lowLim)                                      # Move the blank at the ideal position for final 2x2 rotation
        
        if grid[i2] == v1 and grid[shifted2] == v2:                                     # The 3 tiles are still placed as expected/hoped for (blank IS): solve directly
            movesToParadise.extend([v1,v2])
            for i in (i2,shifted2):                                                     # Makes the two actual swaps in the grid
                i0, grid = gridSwapper(i0, i, grid)
        
        else:                                                                           # Occasionally, something might go "wrong" (v1 or v2 moved again), so resolve instead a 3x2 subgrid with A*, to get the 2 target tiles at the right place (note, at this point, we are sure that the 3 tiles are in the subgrid)
            subGrid_3x2     = {i1 + a*delta + b*delta2nd for a in range(2) for b in range(3)}   # Grid to work on, in the appropriate orientation
            blocking        = set(range(lowLim+2, linS)) - subGrid_3x2 - forbid                 # Tiles to block (only those that are still free at this point and not in the subgrid)
            (_,it1),(_,it2) = sorted((grid[i],i) for i in subGrid_3x2 if grid[i] in (v1,v2))    # Retrieve the index of each target
            cost            = manhattan(it1, i1) + manhattan(it2, i2)                           # Cost based on the positions of v1 and v2 only

            def heuristic(cost, i, i0, grid):                                                   # Function updating the cost for each swap in A*
                delta1 = manhattan(i0, i1) - manhattan(i, i1) if grid[i] == v1 else 0
                delta2 = manhattan(i0, i2) - manhattan(i, i2) if grid[i] == v2 else 0
                c = cost + delta1 + delta2
                return c
            
            forbid.update(blocking)                                                             # "Gendarmerie nationale, vos papiers siouplait..."
            i0, grid, seq = modifiedAStar(grid, i0, heuristic, cost, forbid)                    # Move the blank to the right position (just "ahead" of the target)
            forbid.difference_update(blocking)                                                  # Relax...
            movesToParadise.extend(seq)

        forbid.update({i1,i2})                                                          # Block the two tiles that have been placed
        return i0, grid
        
        
    def moveBlank(i0, to, grid, lowLim):
        cost      = manhattan(i0, to)                                                   # Cost only related to the distance between the blank and the targeted position
        heuristic = lambda _,i0,__,___: manhattan(i0, to)                               
        i0, grid, seq = modifiedAStar(grid, i0, heuristic, cost, forbid)                # Move the blank to the correct position (just "ahead" of the target)
        movesToParadise.extend(seq)                                                     # Archive the moves
        return i0, grid
    

    def manhattan(i0, to): return sum( abs(b-a) for a,b in zip(divmod(i0,S),divmod(to,S)) )             # Distance between indexes
    def manhattan2(i, v):  return sum( abs(b-a) for a,b in zip(divmod(i,S), divmod((v-1)%linS,S)) )     # Distance current index of v/expected position of v
    
    
    #-----------------------------------------------------------------------------------------
    

    grid   = tuple(chain.from_iterable(arr))                                            # Linearized
    S,linS = len(arr), len(arr)**2                                                      # Dimensions (square / linear)
    i0     = grid.index(0)                                                              # Initial position
    
    
    """ Check doability """
    nInv  = sum(a*b and a>b for a,b in combinations(chain.from_iterable(arr), 2))       # Number of inversions
    r0Bot = S - grid.index(0) // S                                                      # Row containing the 0 (1-indexed, from bottom)

    if S%2 and nInv%2 or not S%2 and not (nInv%2 ^ r0Bot%2): return None                # Unsolvable!
    

    """ Divide and conquer, up to 3x2 rectangle remaining """
    forbid          = set()                                                             # MUTATED: Archive all the indexes already done ON THE LEFT part (no tneeded for the upper part)
    movesToParadise = []                                                                # MUTATED: Moves applied to solve the puzzle
    
    for z in range(S-2):                                                                # Up to the two last rows... (z moving on the diagonal):
        for y in range(z, S-2):                                                         #   Complete the current top line, until 2 squares are remaining (or 3 if that's the second to last row)
            iX       = z*S + y
            i0, grid = moveTargetTo(iX, i0, grid)
        i0, grid = conquerCorner(i0, grid, iX+1, iX+2, iX+1)                            #   Places those two values at the end of the row z
        
        lim = S*(z+1)
        for x in range(z+1,S-2):                                                        #   Left column, going down, leaving the two last free.
            iX       = x*S + z
            i0, grid = moveTargetTo(iX, i0, grid, lowLim=lim)                           #   Complete the current first column, until 2 squares remains
        if z < S-3:                                                                     #   Place the two last squares on the column, unless they are for the last 3x2 grid ("z == S-3")
            i1, i2   = iX+S, iX+2*S
            i0, grid = conquerCorner(i0, grid, i1, i2, lowLim=lim)                      #   Places those two tiles
            

    """ Solve the 3x2 remaining grid with A* """
    lowLim = linS-S-3                                                                   # Last tile completed + 1
    cost   = sum( manhattan2(i, grid[i]) for i in range(linS))                          # Initial cost
    
    def heuristic(cost, i, i0, grid): 
        a,b,c,d = (manhattan2(i0, grid[i]), manhattan2(i, grid[i0]),                    # Costs in the candidate grid
                   manhattan2(i0, grid[i0]), manhattan2(i, grid[i]) )                   # Costs in the original grid
        return cost+a+b-c-d
    
    i0, grid, seq = modifiedAStar(grid, i0, heuristic, cost, forbid)
    movesToParadise.extend(seq)
    
    return movesToParadise
  


def display(grid, msg='',force=False):
    if DEBUG or force: 
        linS, S = len(grid), int(len(grid)**.5)
        if msg: print(msg)
        print('\n'.join(' '.join(map('{: >2}'.format, grid[i:i+S])) for i in range(0,linS,S)).replace(' 0',' X'))
        print('-'*S*2)


def gridSwapper(i0, other, grid):
    a, b     = (i0,other) if i0<other else (other,i0)
    nextGrid = grid[:a] + (grid[b],) + grid[a+1:b] + (grid[a],) + grid[b+1:]
    return other, nextGrid
    
    
def modifiedAStar(grid, i0, heuristic, cost, forbid):
    """ "A*", but exit as soon as the end condition (cost==0) is reached, even if not 
        the shortest path. Returns the moves needed to to this final situation.
    
        grid:      linear version of the puzzle (as tuple).
        i0:        position of the blank at the beginning.
        heuristic: function that computes the update the cost for each candidate grid.
                   Call in the form: f(cost, i, i0, grid).
        cost:      initial cost, has to reach 0 when the final configuration is reached.
        forbid:    Set of forbidden positions (as linearized indexes). This set is copied
                   right at the beginning to keep the source faithful.

        @RETURN:   tuple: (i0 at the end,
                           Final grid state (tuple),
                           sequence of moves to reach that state)
    """
    S     = int(len(grid)**.5)
    linS  = S**2
    MOVES = (S, -S, 1, -1)                                                  # (down, up, right, left)
    q     = [(cost, grid, i0, 1j, (-1,))]                                   # (cost, current state (as tuple), i0, last move, ans ('-1' is dummy))
    seens = set()
    forbidPos = set(forbid)                                                 # Use a copy
    
    while q and q[0][0]:
        cost, grid, i0, last, moves = heappop(q)
        seens.add(grid)
        
        for m in MOVES:
            i = i0+m
            if (m == -last or m==1 and i0%S==S-1 or m==-1 and not i0%S      # Skip if: going back (opposite of the last move) or "wrapping" two rows ([i][-1] <-> [i+1][0])...
                  or not (0 <= i < linS) or i in forbidPos):                # ... or not inside the correct area or in the forbidden positions)
                continue
            
            _,cnd = gridSwapper(i0, i, grid)                                # Build the candidate (making the swap)
            if cnd not in seens:                                            # Skip if already found
                cndCost = heuristic(cost, i, i0, grid)
                heappush(q, (cndCost, cnd, i, m, moves+(grid[i],)) )
    if q:
        return q[0][2], q[0][1], q[0][-1][1:]                               # Outputs (without the initial -1 in the moves, used to simplify/fasten the executions)
    else:
        raise Exception(display(grid) or "Aha... That's not going well... (A* ran out of possibilities!)")
        
########################
import numpy as np
import queue


def compare(a, b):
    if a == b:
        return 0
    if a > b:
        return 1
    if a < b:
        return -1


class Puzzle:
    def __init__(self, puzzle):
        self.puzzle = np.array(puzzle, dtype=np.object)
        self.solved = np.zeros_like(self.puzzle, dtype=int)
        self.height, self.width = self.puzzle.shape
        self.steps = []
        for i, row in enumerate(self.puzzle):
            for j, value in enumerate(row):
                self.puzzle[i, j] = Case(value)
                self.puzzle[i, j].y, self.puzzle[i, j].x = i, j
                self.solved[i, j] = 1 + j + self.width*i
        self.solved[-1, -1] = 0
        for row in self.puzzle:
            [case.get_paths(self.puzzle) for case in row]

    def clear(self):
        [case.clear() for case in np.ravel(self.puzzle)]

    def find_number(self, n):
        for row in self.puzzle:
            for node in row:
                if node.value == n:
                    return node
        return None

    def solve_number(self, destination, number, ignore=None, solve=True):
        while destination.value != number:

            hole = self.find_number(0)
            goto = self.find_number(number)
            adjacent = goto.best_adjacent(self.puzzle, relative_to=destination)
            path = hole.astar(self, adjacent, goto, ignore)
            for one, two in zip(path, path[1:]):
                self.steps.append(two.value)
                one.swap(two)
            else:
                self.steps.append(goto.value)
                path[-1].swap(goto)

        if solve:
            destination.solved = True
        return True

    def solve_line(self, line, solutions, helper_cases):
        for case, solution in zip(line[:-2], solutions[:-2]):
            self.solve_number(case, solution)
        self.solve_number(helper_cases[2], solutions[-1], solve=False)
        self.solve_number(helper_cases[3], solutions[-2], solve=False)

        self.solve_number(line[-1], solutions[-2], solve=False)
        self.solve_number(helper_cases[0], solutions[-1], solve=False)

        if line[-2] != self.find_number(0):
            self.solve_number(helper_cases[1], line[-2].value,
                              ignore=[helper_cases[0], line[-1]], solve=False)

        self.solve_number(line[-2], solutions[-2])
        self.solve_number(line[-1], solutions[-1])

        return True

    def smol_solve(self):
        smallest = 2

        for i in range(self.height-smallest):
            helper_cases = (self.puzzle[i+1, -1], self.puzzle[i+1, -2],
                            self.puzzle[i+2, -1], self.puzzle[i+2, -2])
            self.solve_line(self.puzzle[i, :], self.solved[i, :], helper_cases)
            helper_cases = (self.puzzle[-1, i+1], self.puzzle[-2, i+1],
                            self.puzzle[-1, i+2], self.puzzle[-2, i+2])
            self.solve_line(self.puzzle[i+1:, i], self.solved[i+1:, i], helper_cases)

        return True

    def final_solve(self, fragment, solution):
        for i in range(24):
            solution = self.puzzle[-3:, -3:].ravel().tolist()[:-1]
            solution = [s.value for s in solution]
            if sorted(solution) == solution:
                return True

            hole = self.find_number(0)
            if i < 12:
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -2]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -1]
            if i >= 12:
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -1]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -2]
            self.steps.append(guy.value)
            hole.swap(guy)
        self.steps = None

    def solve(self):
        self.smol_solve()
        self.final_solve(self.puzzle[-3:, -3:].ravel().tolist(),
                         self.solved[-3:, -3:].ravel().tolist())
        print(self.puzzle)


class Case:
    def __init__(self, value):
        self.value = value
        self.solved = False
        self.paths = []
        self.distance = np.Infinity
        self.back = None

    def __gt__(self, other):
        return self.distance > other.distance

    def __repr__(self):
        return str(self.value)

    @property
    def info(self):
        return f'Case w/ value {self.value} at ({self.y}, {self.x}).'

    def clear(self):
        self.distance = np.Infinity
        self.back = None

    def swap(self, other):
        self.value, other.value = other.value, self.value
        self.solved, other.solved = other.solved, self.solved

    def get_paths(self, puzzle):
        height, width = puzzle.shape
        if self.y > 0:
            self.paths.append(puzzle[self.y-1, self.x])
        if self.y < height-1:
            self.paths.append(puzzle[self.y+1, self.x])
        if self.x > 0:
            self.paths.append(puzzle[self.y, self.x-1])
        if self.x < width-1:
            self.paths.append(puzzle[self.y, self.x+1])

    def best_adjacent(self, puzzle, relative_to):
        possible_paths = []
        for path in self.paths:
            if not path.solved:
                possible_paths.append((relative_to.distance_to(path), path))

        if not possible_paths:
            print(f'Could not find any good adjacent cases for {self.y}, {self.x}')
            for path in self.paths:
                print(f'({path.y}, {path.x}), solved = {path.solved}')
            print(puzzle.puzzle)

        solution = sorted(possible_paths, key=lambda x: x[0])[0]

        return solution[1]

    def dijkstra(self, puzzle, destination, number, ignore=None):
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore:
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance, posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def astar(self, puzzle, destination, number, ignore=None):
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            if case == destination:
                break
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore: 
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance_to(destination), posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def distance_to(self, other):
        return abs(self.y-other.y)+abs(self.x-other.x)


def slide_puzzle(array):
    puzzle = Puzzle(array)
    puzzle.solve()
    return puzzle.steps
array = [
        [4, 1, 3],
        [2, 8, 0],
        [7, 6, 5],
        ]

print(slide_puzzle(array))

##########################
def three_slip(box):
    moves = [box[1][1], box[1][0], box[0][0], box[0][1], box[0][2], box[1][1], box[1][0], box[0][0], box[0][1], box[0][2],
             box[0][0], box[1][0], box[1][1], box[0][0], box[0][2], box[0][1], box[1][0], box[1][1]]
    return moves


def zero_to_corner(board):
    r, c = find(board, 0)
    moves = [board[i][c] for i in range(r+1, len(board))] + [board[len(board)-1][i] for i in range(c+1, len(board[0]))]
    return moves


def step(board, coord, dir):
    size = [len(board), len(board[0])]
    move = []
    path = [board[size[0]-1][-r] for r in range(1, len(board[0])-coord[1])]+[board[-r][coord[1]] for r in range(1, len(board)-coord[0]+1)]
    path.pop(0)
    moves = path[:]
    my_board = apply(board, moves)
    if dir=='l':
        move += three_slip([row[coord[1]-2:coord[1]+1] for row in my_board[coord[0]-1:coord[0]+1]])
    elif dir=='u':
        move += three_slip(transpose([row[coord[1]-1:coord[1]+1] for row in my_board[coord[0]-2:coord[0]+1]]))
    elif dir=='uf':
        if coord[1]!=0:
            move += three_slip(transpose([row[coord[1]+1:coord[1]-1:-1] for row in my_board[coord[0]-2:coord[0]+1]]))
        else:
            move += three_slip(transpose([row[coord[1]+1::-1] for row in my_board[coord[0]-2:coord[0]+1]]))
    elif dir=='lf':
        return step(transpose(board), coord[::-1], 'uf')
    my_board = apply(my_board, move)
    moves += move
    if coord!=[size[0]-1,size[1]-2]:
        moves += path[::-1]
    else:
        moves += [my_board[size[0]-1][size[1]-1]]
    return moves


def transpose(board):
    return list(map(list, zip(*board)))


def find(board, digit):
    for i in range(len(board)):
        if digit in board[i]: return [i, board[i].index(digit)]


def apply(board, moves):
    if moves==[]: return board
    my_board = [row[:] for row in board]
    move = moves[0]
    rest = moves[1:]
    rows = [[],[]]
    cols = [[],[]]
    rows[1], cols[1] = find(board, move)
    rows[0], cols[0] = find(board, 0)
    if rows[1]>0 and my_board[rows[1]-1][cols[1]]==0:
        my_board[rows[1]-1][cols[1]]=my_board[rows[1]][cols[1]]
        my_board[rows[1]][cols[1]]=0
        rows[0]+=1
    elif rows[1]<len(my_board)-1 and my_board[rows[1]+1][cols[1]]==0:
        my_board[rows[1]+1][cols[1]]=my_board[rows[1]][cols[1]]
        my_board[rows[1]][cols[1]]=0
        rows[0]-=1
    elif cols[1]>0 and my_board[rows[1]][cols[1]-1]==0:
        my_board[rows[1]][cols[1]-1]=my_board[rows[1]][cols[1]]
        my_board[rows[1]][cols[1]]=0
        cols[0]+=1
    else:
        my_board[rows[1]][cols[1]+1]=my_board[rows[1]][cols[1]]
        my_board[rows[1]][cols[1]]=0
        cols[0]-=1
    if rest!=[]: my_board = apply(my_board, rest)
    return my_board


def to_corner(board, digit, right=False):
    if right:
        my_board = [row[::-1] for row in board]
        moves = to_corner(my_board, digit)
        return moves
    rows = [[],[]]
    cols = [[],[]]
    moves = []
    size = [len(board), len(board[0])]
    rows[1], cols[1] = find(board, digit)
    rows[0], cols[0] = find(board, 0)
    if board[0][0]==digit:
        return []
    if rows[1]==0: return to_corner(transpose(board), digit)
    if cols[1]==cols[0]:
        if cols[0] != size[1]-1:
            moves+=[board[rows[0]][cols[0]+1]]
        else:
            moves+=[board[rows[0]][cols[0]-1]]
    elif cols[0]==0:
        moves += [board[r][0] for r in range(rows[0]-1,rows[1]-1,-1)]+board[rows[1]][1:cols[1]+1]
    else:
        moves += [board[rows[0]-1-r][cols[0]] for r in range(rows[0])]+board[0][cols[0]-1::-1]
        new_board = apply(board, moves)
        moves += [new_board[r+1][0] for r in range(rows[1])]+new_board[rows[1]][1:cols[1]+1]
    my_board = apply(board, moves)
    rest = to_corner(my_board, digit)
    return moves+rest


def sort(board, num):
    r, c = find(board, num)
    rp = (num-1)//len(board[0])
    cp = (num-1)%len(board[0])
    my_board = [row[:] for row in board]
    moves =[]
    if r!=rp:
        moves += to_corner(my_board[min(r, len(board)-2):], num, right=True)
        my_board = apply(my_board, moves)
        if cp==len(board[0])-1:
            moves += zero_to_corner(my_board)
            my_board = apply(my_board, zero_to_corner(my_board))
            r, c = find(my_board, num)
            for i in range(r, rp, -1):
                move = step(my_board, [max(i, rp+2),cp-1], 'uf')
                my_board = apply(my_board, move)
                moves += move
            return moves
    moves += to_corner([row[cp:] for row in my_board[rp:]], num)
    return moves


def final_sort(board, num):
    r, c = find(board, num)
    rp = (num-1)//len(board[0]) - len(board[0]) + 2
    cp = (num-1)%len(board[0])
    if cp==c and rp==r:
        return []
    if cp <= c and rp == 0:
        my_board = [row[cp:] for row in board]
        moves = to_corner(my_board, num)
        return moves
    elif cp <=c and rp == 1:
        moves = step(board, [0,max(c,cp+2)], 'lf')
        my_board = apply(board, moves)
        rest = final_sort(my_board, num)
        return moves + rest
    elif cp > c:
        moves = step(board, [0,max(c+1,2)], 'lf')
        my_board = apply(board, moves)
        move = step(my_board, [0,max(c+1,2)], 'lf')
        my_board = apply(my_board, move)
        moves += move
        rest = final_sort(my_board, num)
        return moves + rest


def slide_puzzle(board):
    n = len(board)
    solution = []
    for i in range(1,n*(n-2)+1):
        move = zero_to_corner(board)
        board = apply(board, move)
        solution += move
        move = sort(board, i)
        board = apply(board, move)
        solution += move
    for i in range(n*(n-2)+1, n**2-2):
        move = zero_to_corner(board)
        board = apply(board, move)
        solution += move
        move = final_sort(board[-2:], i)
        board = apply(board, move)
        solution += move
    if board[-1][-2] != n**2-1:
        return None
    return solution

  
###############################
def slideCol(board, cursor, size):
    r, c = cursor
    path, d = [], 1 if size > 0 else -1
    for i in range(d * size):
        path.append(board[r+d*(i+1)][c])
        board[r+d*i][c] = board[r+d*(i+1)][c]
    r += size
    board[r][c] = 0
    return path, (r, c)

def slideRow(board, cursor, size):
    r, c = cursor
    path, d = [], 1 if size > 0 else -1
    for i in range(d * size):
        path.append(board[r][c+d*(i+1)])
        board[r][c+d*i] = board[r][c+d*(i+1)]
    c += size
    board[r][c] = 0
    return path, (r, c)

def rotateToCol(board, cursor, height, width):
    path, cursor = slideCol(board, cursor, height)
    tmp, cursor = slideRow(board, cursor, width)
    path += tmp
    tmp, cursor = slideCol(board, cursor, -height)
    path += tmp
    tmp, cursor = slideRow(board, cursor, -width)
    return path + tmp

def rotateToRow(board, cursor, height, width):
    path, cursor = slideRow(board, cursor, width)
    tmp, cursor = slideCol(board, cursor, height)
    path += tmp
    tmp, cursor = slideRow(board, cursor, -width)
    path += tmp
    tmp, cursor = slideCol(board, cursor, -height)
    return path + tmp

def show(board):
    for line in board:
        for cell in line: print(f'%3d' %cell, end = '')
        print()

def findCursor(board, height, width):
    for r in range(height):
        for c in range(width):
            if board[r][c] == 0: return (r, c)
    assert(0)

def gotoLine(board, cursor, line):
    r, c = cursor
    path, cursor = slideCol(board, cursor, line - r)
    tmp, cursor = slideRow(board, cursor, 1 - c)
    return path+tmp, cursor

def neighb23(board, cells):
    return {board[a][b]: (a, b) for a, b in cells}

def target23(board, cells):
    return sorted(board[a][b] for a, b in cells)

def swap(board, cursor):
    r, c = cursor
    path = []
    path += rotateToRow(board, cursor, 1,  1)
    path += rotateToRow(board, cursor, 1, -1)
    path += rotateToCol(board, cursor, 1,  1)
    path += rotateToRow(board, cursor, 1, -1)
    return path


def solve23(board, cursor, height, width):
    r, c = cursor
    path = []
    neighb = ((r-1, c-1), (r, c-1), (r-1, c), (r-1, c+1), (r, c+1))
    cells = neighb23(board, neighb)
    target = target23(board, neighb)
    if board[0] == target[:3]: return path
    curr = cells[target[0]]
    if curr == (r-1, c-1):
        path += rotateToRow(board, cursor, -1, -1)
    else:
        if curr[1] == c+1:
            if curr[0] == r-1: path += rotateToCol(board, cursor, -1, 1)
            else: path += rotateToRow(board, cursor, -1, 1)
            cells = neighb23(board, neighb)
            curr = cells[target[0]]
        if curr[0] == r-1:
            path += rotateToCol(board, cursor, -1, -1)
    cells = neighb23(board, neighb)
    curr = cells[target[1]]
    if curr[1] != c-1:
        if curr[0] == r: path += rotateToCol(board, cursor, -1, 1)
        elif curr[1] == c: path += rotateToRow(board, cursor, -1, 1)
        path += rotateToCol(board, cursor, -1, -1)
        path += rotateToCol(board, cursor, -1, 1)
        path += rotateToRow(board, cursor, -1, -1)
        cells = neighb23(board, neighb)
    curr = cells[target[2]]
    if curr != (r-1, c+1):
        if curr[0] == r: path += rotateToCol(board, cursor, -1, 1)
        elif curr[1] == c: path += rotateToRow(board, cursor, -1, 1)
    path += rotateToCol(board, cursor, -1, -1)
    cells = neighb23(board, neighb)
    if (target[3] <= (r * width)) and ((r + 1) < height):
        curr = cells[target[3]]
        if curr[1] == (c-1):
            path += swap(board, cursor)
    return path
    
def solveLine(board, cursor, line, height, width):
    level = (line + 1) * width + 1
    path, cursor = gotoLine(board, cursor, line+1)
    path += solve23(board, cursor, height, width)
    for i in range(3, width):
        tmp, cursor = slideRow(board, cursor, 1)
        tmp += solve23(board, cursor, height, width)
        path += tmp
    return path, cursor

def solveLines(board, cursor, height, width):
    target = [[r*width + c + 1 for c in range(width)] for r in range(height)]
    target[height-1][width-1] = 0
    path = []
    curr = 0
    while curr < (height - 2):
        for line in range(curr, height-1):
            tmp, cursor = solveLine(board, cursor, line, height, width)
            path += tmp
        while board[curr] == target[curr]: curr += 1
    return solveLastTwo(board, cursor, height, width, path)

def moveBack(board, cursor):
    r, c = cursor
    path = rotateToRow(board, cursor, -1, -1)
    tmp, cursor = slideRow(board, cursor, 1)
    path += tmp
    path += rotateToRow(board, cursor, -1,  1)
    path += rotateToCol(board, cursor, -1, -1)
    path += rotateToCol(board, cursor, -1,  1)
    tmp, cursor = slideRow(board, cursor, -1)
    path += tmp
    path += rotateToCol(board, cursor, -1, -1)
    
    return path
    

def solveTwo(board, cursor, width):
    r, c = cursor
    path = []
    neighb = ((r-1, c-1), (r, c-1), (r-1, c), (r-1, c+1), (r, c+1))
    cells = neighb23(board, neighb)
    target = target23(board, neighb)
    num1 = target[0] if target[0] <= (cursor[0] * width) else None
    num2 = None
    for i in range(5):
        if target[i] > (cursor[0] * width):
            num2 = target[i]
            break
    if num2:
        curr = cells[num2]
        if curr[1] == (c - 1):
            if curr[0] == (r - 1):
                path += rotateToRow(board, cursor, -1, -1)
        else:
            if curr[1] == (c + 1):
                if curr[0] == (r-1): path += rotateToCol(board, cursor, -1, 1)
                else: path += rotateToRow(board, cursor, -1, 1)
            path += rotateToCol(board, cursor, -1, -1)
        cells = neighb23(board, neighb)
    if num1:
        curr = cells[num1]
        if curr[1] == (c-1):
            if curr[0] == (r):
                path += rotateToCol(board, cursor, -1, -1)
            return path
        if curr != (r-1, c+1):
            if curr[1] == (c+1): path += rotateToCol(board, cursor, -1, 1)
            else: path += rotateToRow(board, cursor, -1, 1)
        path += rotateToCol(board, cursor, -1, -1)
        path += rotateToCol(board, cursor, -1,  1)
        path += rotateToRow(board, cursor, -1, -1)
    return path

def gotoCol(board, cursor, col):
    r, c = cursor
    path, cursor = slideRow(board, cursor, col - c)
    return path, cursor

def solveLastTwo(board, cursor, height, width, path):
    h = height - 2
    target = [(h * width + c + 1, (h + 1) * width + c + 1) for c in range(width)]
    curr = 0
    while curr < (width - 2):
        for col in range(width-2, curr, -1):
            tmp, cursor = gotoCol(board, cursor, col)
            path += tmp
            path += solveTwo(board, cursor, width)
    
        while (board[-2][curr], board[-1][curr]) == target[curr]: curr += 1
    num = board[-1][-3] + 1
    if board[-2][-2] == num:
        path += rotateToCol(board, cursor, -1, 1)
    elif board[-2][-1] == num:
        path += rotateToCol(board, cursor, -1, 1)
        path += rotateToCol(board, cursor, -1, 1)
    tmp, cursor = slideRow(board, cursor, 1)
    path += tmp
    if (board[-2][-1] - board[-2][-2]) != 1: return None
    return path 

def slide_puzzle(ar):
    #your code goes here. you can do it!
    height, width = len(ar), len(ar[0])
    return solveLines(ar, findCursor(ar, height, width), height, width)
  
###############################
import numpy as np
import queue


def compare(a, b):
    if a == b:
        return 0
    if a > b:
        return 1
    if a < b:
        return -1


class Puzzle:
    def __init__(self, puzzle):
        self.puzzle = np.array(puzzle, dtype=np.object)
        self.solved = np.zeros_like(self.puzzle, dtype=int)
        self.height, self.width = self.puzzle.shape
        self.steps = []

        for i, row in enumerate(self.puzzle):
            for j, value in enumerate(row):
                self.puzzle[i, j] = Case(value)
                self.puzzle[i, j].y, self.puzzle[i, j].x = i, j
                self.solved[i, j] = 1 + j + self.width*i
        self.solved[-1, -1] = 0

        # Create paths for all cases
        for row in self.puzzle:
            [case.get_paths(self.puzzle) for case in row]

    def clear(self):
        [case.clear() for case in np.ravel(self.puzzle)]

    def find_number(self, n):
        for row in self.puzzle:
            for node in row:
                if node.value == n:
                    return node
        return None

    def solve_number(self, destination, number, ignore=None, solve=True):
        while destination.value != number:

            hole = self.find_number(0)
            goto = self.find_number(number)
            adjacent = goto.best_adjacent(self.puzzle, relative_to=destination)
            path = hole.astar(self, adjacent, goto, ignore)
            for one, two in zip(path, path[1:]):
                self.steps.append(two.value)
                one.swap(two)
            else:
                self.steps.append(goto.value)
                path[-1].swap(goto)

        if solve:
            destination.solved = True
        return True

    def solve_line(self, line, solutions, helper_cases):
        for case, solution in zip(line[:-2], solutions[:-2]):
            self.solve_number(case, solution)


        self.solve_number(helper_cases[2], solutions[-1], solve=False)
        self.solve_number(helper_cases[3], solutions[-2], solve=False)

        self.solve_number(line[-1], solutions[-2], solve=False)
        self.solve_number(helper_cases[0], solutions[-1], solve=False)

        if line[-2] != self.find_number(0):
            self.solve_number(helper_cases[1], line[-2].value,
                              ignore=[helper_cases[0], line[-1]], solve=False)

        self.solve_number(line[-2], solutions[-2])
        self.solve_number(line[-1], solutions[-1])

        return True

    def smol_solve(self):
        smallest = 2

        for i in range(self.height-smallest):
            helper_cases = (self.puzzle[i+1, -1], self.puzzle[i+1, -2],
                            self.puzzle[i+2, -1], self.puzzle[i+2, -2])
            self.solve_line(self.puzzle[i, :], self.solved[i, :], helper_cases)
            helper_cases = (self.puzzle[-1, i+1], self.puzzle[-2, i+1],
                            self.puzzle[-1, i+2], self.puzzle[-2, i+2])
            self.solve_line(self.puzzle[i+1:, i], self.solved[i+1:, i], helper_cases)

        return True

    def final_solve(self, fragment, solution):


        for i in range(24):
            solution = self.puzzle[-3:, -3:].ravel().tolist()[:-1]
            solution = [s.value for s in solution]
            if sorted(solution) == solution:

                return True

            hole = self.find_number(0)
            if i < 12:
                # 3 loops one way, 3 loops the other one
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -2]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -1]
            if i >= 12:

                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -1]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -2]
            self.steps.append(guy.value)
            hole.swap(guy)
        self.steps = None

    def solve(self):
        self.smol_solve()
        self.final_solve(self.puzzle[-3:, -3:].ravel().tolist(),
                         self.solved[-3:, -3:].ravel().tolist())
        print(self.puzzle)


class Case:
    def __init__(self, value):
        self.value = value
        self.solved = False
        self.paths = []
        self.distance = np.Infinity
        self.back = None

    def __gt__(self, other):
        return self.distance > other.distance

    def __repr__(self):
        return str(self.value)

    @property
    def info(self):
        return f'Case w/ value {self.value} at ({self.y}, {self.x}).'

    def clear(self):
        self.distance = np.Infinity
        self.back = None

    def swap(self, other):
        self.value, other.value = other.value, self.value
        self.solved, other.solved = other.solved, self.solved

    def get_paths(self, puzzle):
        height, width = puzzle.shape
        if self.y > 0:
            self.paths.append(puzzle[self.y-1, self.x])
        if self.y < height-1:
            self.paths.append(puzzle[self.y+1, self.x])
        if self.x > 0:
            self.paths.append(puzzle[self.y, self.x-1])
        if self.x < width-1:
            self.paths.append(puzzle[self.y, self.x+1])

    def best_adjacent(self, puzzle, relative_to):

        possible_paths = []
        for path in self.paths:
            if not path.solved:


                possible_paths.append((relative_to.distance_to(path), path))

        if not possible_paths:
            print(f'Could not find any good adjacent cases for {self.y}, {self.x}')
            for path in self.paths:
                print(f'({path.y}, {path.x}), solved = {path.solved}')
            print(puzzle.puzzle)

        solution = sorted(possible_paths, key=lambda x: x[0])[0]

        return solution[1]

    def dijkstra(self, puzzle, destination, number, ignore=None):
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore:
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance, posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def astar(self, puzzle, destination, number, ignore=None):
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            if case == destination:
                break
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore: 
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance_to(destination), posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def distance_to(self, other):
        return abs(self.y-other.y)+abs(self.x-other.x)


def slide_puzzle(array):
    
    puzzle = Puzzle(array)
    puzzle.solve()
    return puzzle.steps
  
##########################
import numpy as np
import queue


def compare(a, b):
    if a == b:
        return 0
    if a > b:
        return 1
    if a < b:
        return -1


class Puzzle:
    def __init__(self, puzzle):
        self.puzzle = np.array(puzzle, dtype=np.object)
        self.solved = np.zeros_like(self.puzzle, dtype=int)
        self.height, self.width = self.puzzle.shape
        self.steps = []

        for i, row in enumerate(self.puzzle):
            for j, value in enumerate(row):
                self.puzzle[i, j] = Case(value)
                self.puzzle[i, j].y, self.puzzle[i, j].x = i, j
                self.solved[i, j] = 1 + j + self.width*i
        self.solved[-1, -1] = 0

        # Create paths for all cases
        for row in self.puzzle:
            [case.get_paths(self.puzzle) for case in row]

    def clear(self):
        [case.clear() for case in np.ravel(self.puzzle)]

    def find_number(self, n):
        for row in self.puzzle:
            for node in row:
                if node.value == n:
                    return node
        return None

    def solve_number(self, destination, number, ignore=None, solve=True):
        while destination.value != number:

            hole = self.find_number(0)
            goto = self.find_number(number)
            adjacent = goto.best_adjacent(self.puzzle, relative_to=destination)
            path = hole.astar(self, adjacent, goto, ignore)
            # Moves to it
            for one, two in zip(path, path[1:]):
                self.steps.append(two.value)
                one.swap(two)
            else:
                self.steps.append(goto.value)
                path[-1].swap(goto)

        if solve:
            destination.solved = True
        return True

    def solve_line(self, line, solutions, helper_cases):
        for case, solution in zip(line[:-2], solutions[:-2]):
            self.solve_number(case, solution)

        self.solve_number(helper_cases[2], solutions[-1], solve=False)
        self.solve_number(helper_cases[3], solutions[-2], solve=False)

        self.solve_number(line[-1], solutions[-2], solve=False)
        self.solve_number(helper_cases[0], solutions[-1], solve=False)

        if line[-2] != self.find_number(0):
            self.solve_number(helper_cases[1], line[-2].value,
                              ignore=[helper_cases[0], line[-1]], solve=False)

        self.solve_number(line[-2], solutions[-2])
        self.solve_number(line[-1], solutions[-1])

        return True

    def small_solve(self):
        smallest = 2

        for i in range(self.height-smallest):
            helper_cases = (self.puzzle[i+1, -1], self.puzzle[i+1, -2],
                            self.puzzle[i+2, -1], self.puzzle[i+2, -2])
            self.solve_line(self.puzzle[i, :], self.solved[i, :], helper_cases)
            helper_cases = (self.puzzle[-1, i+1], self.puzzle[-2, i+1],
                            self.puzzle[-1, i+2], self.puzzle[-2, i+2])
            self.solve_line(self.puzzle[i+1:, i],
                            self.solved[i+1:, i], helper_cases)

        return True

    def final_solve(self, fragment, solution):

        for i in range(24):
            solution = self.puzzle[-3:, -3:].ravel().tolist()[:-1]
            solution = [s.value for s in solution]
            if sorted(solution) == solution:
                # Done
                return True

            hole = self.find_number(0)
            if i < 12:
                # 3 loops one way, 3 loops the other one
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -2]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -1]
            if i >= 12:
                # 3 loops one way, 3 loops the other one
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -1]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -2]
            self.steps.append(guy.value)
            hole.swap(guy)
        self.steps = None

    def solve(self):
        self.small_solve()
        self.final_solve(self.puzzle[-3:, -3:].ravel().tolist(),
                         self.solved[-3:, -3:].ravel().tolist())
        print(self.puzzle)


class Case:
    def __init__(self, value):
        self.value = value
        self.solved = False
        self.paths = []
        self.distance = np.Infinity
        self.back = None

    def __gt__(self, other):
        return self.distance > other.distance

    def __repr__(self):
        return str(self.value)

    def clear(self):
        self.distance = np.Infinity
        self.back = None

    def swap(self, other):
        self.value, other.value = other.value, self.value
        self.solved, other.solved = other.solved, self.solved

    def get_paths(self, puzzle):
        height, width = puzzle.shape
        if self.y > 0:
            self.paths.append(puzzle[self.y-1, self.x])
        if self.y < height-1:
            self.paths.append(puzzle[self.y+1, self.x])
        if self.x > 0:
            self.paths.append(puzzle[self.y, self.x-1])
        if self.x < width-1:
            self.paths.append(puzzle[self.y, self.x+1])

    def best_adjacent(self, puzzle, relative_to):
        possible_paths = []
        for path in self.paths:
            if not path.solved:

                possible_paths.append((relative_to.distance_to(path), path))

        if not possible_paths:
            print(
                f'Could not find any good adjacent cases for {self.y}, {self.x}')
            for path in self.paths:
                print(f'({path.y}, {path.x}), solved = {path.solved}')
            print(puzzle.puzzle)

        solution = sorted(possible_paths, key=lambda x: x[0])[0]

        return solution[1]

    def dijkstra(self, puzzle, destination, number, ignore=None):
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore:
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance, posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def astar(self, puzzle, destination, number, ignore=None):
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            if case == destination:
                break
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore:
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance_to(destination), posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def distance_to(self, other):
        return abs(self.y-other.y)+abs(self.x-other.x)


def slide_puzzle(ar):
    puzzle = Puzzle(ar)
    puzzle.solve()
    return puzzle.steps
  
#########################
import numpy as np
import queue
def compare(a, b):
    if a == b:
        return 0
    if a > b:
        return 1
    if a < b:
        return -1
class Puzzle:
    def __init__(self, puzzle):
        self.puzzle = np.array(puzzle, dtype=np.object)
        self.solved = np.zeros_like(self.puzzle, dtype=int)
        self.height, self.width = self.puzzle.shape
        self.steps = []
        # Build puzzle & solution to compare against:
        for i, row in enumerate(self.puzzle):
            for j, value in enumerate(row):
                self.puzzle[i, j] = Case(value)
                self.puzzle[i, j].y, self.puzzle[i, j].x = i, j
                self.solved[i, j] = 1 + j + self.width*i
        self.solved[-1, -1] = 0
        # Create paths for all cases
        for row in self.puzzle:
            [case.get_paths(self.puzzle) for case in row]
    def clear(self):
        [case.clear() for case in np.ravel(self.puzzle)]
    def find_number(self, n):
        for row in self.puzzle:
            for node in row:
                if node.value == n:
                    return node
        return None
    def solve_number(self, destination, number, ignore=None, solve=True):
        while destination.value != number:
            hole = self.find_number(0)
            # Finds the number you want to put in Destination
            goto = self.find_number(number)
            # Finds which adjacent case we should approach it from
            adjacent = goto.best_adjacent(self.puzzle, relative_to=destination)
            # Finds the shortest path to the adjacent case
            path = hole.astar(self, adjacent, goto, ignore)
            # Moves to it
            for one, two in zip(path, path[1:]):
                self.steps.append(two.value)
                one.swap(two)
            else:
                self.steps.append(goto.value)
                path[-1].swap(goto)
        if solve:
            destination.solved = True
        return True
    def solve_line(self, line, solutions, helper_cases):
        # Give it a line and what you want that line to look like
        for case, solution in zip(line[:-2], solutions[:-2]):
            self.solve_number(case, solution)
        # Now the hard solve with line[-2:] and solutions[-2:]
        # Ponemos el 4 y el 3 en un lugar seguro
        self.solve_number(helper_cases[2], solutions[-1], solve=False)
        self.solve_number(helper_cases[3], solutions[-2], solve=False)
        self.solve_number(line[-1], solutions[-2], solve=False)
        self.solve_number(helper_cases[0], solutions[-1], solve=False)
        if line[-2] != self.find_number(0):
            self.solve_number(helper_cases[1], line[-2].value,
                              ignore=[helper_cases[0], line[-1]], solve=False)
        self.solve_number(line[-2], solutions[-2])
        self.solve_number(line[-1], solutions[-1])
        return True
    def smol_solve(self):
        # First solves top row & column, etc, until 2x3 block left
        # helper_case[0] is below the last case of the row (row+1, -1)
        # helper_case[1] is to the left of helper_case[0]
        # We want to reduce up to a 2x2 grid
        smallest = 2
        for i in range(self.height-smallest):
            helper_cases = (self.puzzle[i+1, -1], self.puzzle[i+1, -2],
                            self.puzzle[i+2, -1], self.puzzle[i+2, -2])
            self.solve_line(self.puzzle[i, :], self.solved[i, :], helper_cases)
            helper_cases = (self.puzzle[-1, i+1], self.puzzle[-2, i+1],
                            self.puzzle[-1, i+2], self.puzzle[-2, i+2])
            self.solve_line(self.puzzle[i+1:, i], self.solved[i+1:, i], helper_cases)
        return True
    def final_solve(self, fragment, solution):
        # Solves a 2x2 puzzle
        for i in range(24):
            solution = self.puzzle[-3:, -3:].ravel().tolist()[:-1]
            solution = [s.value for s in solution]
            if sorted(solution) == solution:
                # Done
                return True
            hole = self.find_number(0)
            if i < 12:
                # 3 loops one way, 3 loops the other one
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -2]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -1]
            if i >= 12:
                # 3 loops one way, 3 loops the other one
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -1]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -2]
            self.steps.append(guy.value)
            hole.swap(guy)
        # print('couldnt find solution')
        self.steps = None
    def solve(self):
        # Solve it until we only have a 2x2 square on the bottom right
        self.smol_solve()
        # Solve the 2x2 square (first argument is square, second is solution)
        self.final_solve(self.puzzle[-3:, -3:].ravel().tolist(),
                         self.solved[-3:, -3:].ravel().tolist())
        print(self.puzzle)
class Case:
    def __init__(self, value):
        self.value = value
        self.solved = False
        self.paths = []
        self.distance = np.Infinity
        self.back = None
    def __gt__(self, other):
        return self.distance > other.distance
    def __repr__(self):
        return str(self.value)
    @property
    def info(self):
        return f'Case w/ value {self.value} at ({self.y}, {self.x}).'
    def clear(self):
        self.distance = np.Infinity
        self.back = None
    def swap(self, other):
        self.value, other.value = other.value, self.value
        self.solved, other.solved = other.solved, self.solved
    def get_paths(self, puzzle):
        height, width = puzzle.shape
        if self.y > 0:
            self.paths.append(puzzle[self.y-1, self.x])
        if self.y < height-1:
            self.paths.append(puzzle[self.y+1, self.x])
        if self.x > 0:
            self.paths.append(puzzle[self.y, self.x-1])
        if self.x < width-1:
            self.paths.append(puzzle[self.y, self.x+1])
    def best_adjacent(self, puzzle, relative_to):
        # y1, x1 = relative_to.y, relative_to.x
        possible_paths = []
        for path in self.paths:
            if not path.solved:
                # Changed to distance_to
                # OLD: possible_paths.append((abs(y1-path.y)+abs(x1-path.x), path))
                possible_paths.append((relative_to.distance_to(path), path))
        if not possible_paths:
            # Error check, shouldn't happen on solvable puzzles
            print(f'Could not find any good adjacent cases for {self.y}, {self.x}')
            for path in self.paths:
                print(f'({path.y}, {path.x}), solved = {path.solved}')
            print(puzzle.puzzle)
        solution = sorted(possible_paths, key=lambda x: x[0])[0]
        return solution[1]
    def dijkstra(self, puzzle, destination, number, ignore=None):
        '''A* is way more efficient on big maps! Use it instead'''
        # Number = the number we want to put in Destination
        # Shortest path to position, ignoring the solved cases and the Number
        # It has to ignore Number because else it will displace it and fuck it up
        # Basically we take the zero to Destination(which will be right next to Number)
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))
        while not q.empty():
            _, case = q.get()
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore:
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance, posib))
        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)
        puzzle.clear()
        return list(reversed(path))
    def astar(self, puzzle, destination, number, ignore=None):
        # MOVING HOLE(SELF) TO DESTINATION
        # Number = the number we want to put in Destination
        # Shortest path to position, ignoring the solved cases and the Number
        # It has to ignore Number because else it will displace it and fuck it up
        # Basically we take the zero to Destination(which will be right next to Number)
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))
        while not q.empty():
            _, case = q.get()
            if case == destination:
                break
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore: 
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance_to(destination), posib))
        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)
        puzzle.clear()
        return list(reversed(path))
    def distance_to(self, other):
        return abs(self.y-other.y)+abs(self.x-other.x)
def slide_puzzle(array):
    # Code-execution function
    puzzle = Puzzle(array)
    puzzle.solve()
    return puzzle.steps
# TEST CASE
array = [
        [4, 1, 3],
        [2, 8, 0],
        [7, 6, 5],
        ]

print(slide_puzzle(array)) 
print(slide_puzzle(array))

###########################
def slide_puzzle(ar):
    out = []
    n = len(ar)
    indices = [x for r in ar for x in r]
    locations = [x[1] for x in sorted(zip(indices, range(n * n)))]

    def getloc(k): return k, locations[k]//n, locations[k]%n
    def getk(i, j): return indices[i*n+j]
    def move(k):
        locations[0], locations[k] = locations[k], locations[0]
        indices[locations[k]] = k
        indices[locations[0]] = 0
        if out and out[-1] == k: out.pop()
        else: out.append(k)

    _, oi, oj = getloc(0)
    def m(i, j):
        nonlocal oi, oj
        if oj > j:
            for j in range(oj - 1, j - 1, -1): move(getk(i, j))
        elif oj < j:
            for j in range(oj + 1, j + 1): move(getk(i, j))
        elif oi > i:
            for i in range(oi - 1, i - 1, -1): move(getk(i, j))
        elif oi < i:
            for i in range(oi + 1, i + 1): move(getk(i, j))
        oi, oj = i, j

    # all but last 2 rows
    for i in range(n - 2):
        # all but last column
        for j in range(n - 1):
            k, ki, kj = getloc(i * n + j + 1)
            # move the gap to under the number
            if ki == n-1: m(n-2, oj), m(n-2, kj)
            if oi < ki:
                m(oi, kj), m(ki, kj)
                ki -= 1
            elif oi > ki: m(oi, kj), m(ki + 1, kj)
            else: m(oi + 1, oj), m(oi, kj)
            # move the number to the correct column
            dir = -1 if j < kj else 1
            for kj in range(kj, j, dir): m(ki + 1, kj + dir), m(ki, kj + dir), m(ki, kj), m(ki + 1, kj)
            m(ki + 1, j)
            # move the number up to the correct row
            for ki in range(ki, i, -1):
                m(ki + 1, j + 1), m(ki - 1, j + 1), m(ki - 1, j), m(ki, j)
        # last column
        k, ki, kj = getloc((i + 1) * n)
        if locations[k] == k - 1: continue
        # move the gap to under the number
        if ki == n-1: m(n-2, oj), m(n-2, kj)
        if oi < ki:
            m(oi, kj), m(ki, kj)
            ki -= 1
        else: m(oi + 1, oj), m(oi, kj)
        # move the number to the far right edge
        for kj in range(kj, n - 1): m(oi, kj + 1), m(ki, oj), m(ki, kj), m(ki + 1, kj)
        m(oi, n - 1)
        # move the number just below its final location
        for ki in range(ki, i + 1, -1): m(oi, n - 2), m(ki - 1, oj), m(oi, n - 1), m(ki, oj)
        # put it in
        m(i+1, n-1), m(i, n-1), m(i, n-2), m(i+1, n-2), m(i+1, n-1), m(i+2, n-1), m(i+2, n-2), m(i, n-2), m(i, n-1), m(i+1, n-1)
    # last 2 rows solve from left to right
    for j in range(n - 2):
        k, ki, kj = getloc((n - 2) * n + j + 1)
        if ki == n - 1: m(oi, kj), m(ki, kj)
        else: m(n - 1, oj), m(oi, kj)
        for kj in range(kj, j, -1): m(oi, kj-1), m(n-2, oj), m(oi, kj), m(n-1, oj)
        m(n-1, n-1)
        k, ki, kj = getloc(k + n)
        if locations[k] == k - 1: m(n-2, oj)
        else:
            if ki == n - 2: m(oi, kj), m(ki, kj)
            else: m(n-2, oj), m(oi, kj)
            if kj >= j+2:
                for kj in range(kj, j+2, -1):  m(oi, kj-1), m(n-1, oj), m(oi, kj), m(n-2, oj)
                m(oi, j+2)
            else:
                m(oi, j+2), m(n-1, oj), m(oi, j+1), m(n-2, oj), m(oi, j+2)
            m(oi, j), m(n-1, oj), m(oi, j+2), m(n-2, oj), m(oi, j+1), m(n-1, oj), m(oi, j), m(n-2, oj), m(oi, j+2), m(n-1, oj), m(oi, j), m(n-2, oj), m(oi, j+1)
    # last 2x2 square
    m(oi, n-2), m(n-2, oj)
    k, ki, kj = getloc(n * (n-1) - 1)
    if ki == n-2 or kj == n-2: m(ki, kj)
    else: m(ki, oj), m(oi, kj), m(n-2, oj), m(oi, n-2), m(ki, oj)
    m(oi, n-1), m(n-1, oj)
    # rotate until the zero is in the bottom right
    for k in [n*(n-1), n*n-1]:
        if (locations[k] != k - 1): return None
    return out
  
############################
import copy
import numpy as np

from scipy.spatial import distance as dst
from itertools import chain, cycle




""" Starting with defining the overall and basic functions"""


def num_to_pos(n, state):
    """Converts a number to a tuple of pos """
    y,x = np.where(state==n)
    return y[0],x[0]


def pos_to_num(pos, state):
    assert isinstance(pos, tuple), (
            "invalid input for pos to numbers")
    return int(state[pos])
 
    
def push(n, state):
    """Perform a move and swap the given number with 0.
    Input: number to swap and state
    Output: new state. """
#    assert distance(n, 0, state, dst.cityblock) == 1, (
#            f"number {n} can't be pushed: not a neighbor of 0")
    y_old, x_old = num_to_pos(n, state)
    y_new, x_new = num_to_pos(0, state)
    state[y_old, x_old] = 0
    state[y_new, x_new] = n
    memory.append(n)
    return state



def distance(n1, n2, state, dist_function):
    """ Higher order function to compute different distances between numbers.
    Applied with Chebyshev distance for neighbors of numbers.
    Or with cityblock distance for pushing the numbers."""
    return dist_function(num_to_pos(n1, state), 
                         num_to_pos(n2, state))



def find_neighbors(n, state, pushable=False):
    """ Find all adjacent numbers of a number
    If pushable is true, the diagonal neighbors are not included"""
    
    y_dim = len(state)
    x_dim = len(state[0])

    if pushable is not False:
        y,x = num_to_pos(n, state)
        positions = [(y-1,x), (y,x-1), (y,x+1), (y+1,x)]
        
    else:
        y,x = num_to_pos(n, state)
        positions = [(y-1,x-1), (y-1,x), (y-1,x+1),
                     (y,x-1), (y,x+1),
                     (y+1,x-1), (y+1,x), (y+1,x+1)]
        
    neighbors = []
    for p in positions:
        y,x = p
        if 0 <= y < y_dim and 0 <= x < x_dim:
            try:
                number = state[p]
                neighbors.append(int(number))
            except:
                pass

    return neighbors
  
   

def make_solution(dim):
    """ Prepare the solution for the given puzzle based on 
    the puzzle's dimensions. """
    solution = np.arange(1, (dim*dim)+1).reshape(dim, dim)
    maxvalue = np.max(solution)
    np.place(solution, solution==maxvalue, 0)
    return solution
 
    
def find_corners(solution, dim, last_six):
    """ Find all corners of the puzzle for different solving approach. """
    corners = [*solution[:,dim-1], *solution[dim-1]]
    return [int(c) for c in corners if c not in last_six]


def sort_numbers(solution, dim, last_six):
    """ Sorting the solution to get the specific order of numbers.
    First upper row, then left column, then next row, then second column etc.
    Reason: reducing puzzle size
    """
    solution = solution.tolist()
    columns = []        
    for i in range(dim):
        column = []
        for row in solution:
            column.append(row[i])
        columns.append(column)
    
    numbers = zip(*columns, *solution) # alternating row & column
    numbers = chain(*numbers)               # flatten
    numbers = list(dict.fromkeys(numbers))  # remove duplicates

#    logging.info(f"Numbers order generated: {numbers}")
    return [n for n in numbers] # if n not in last_six]


def puzzle_solved(state, solution):
    """ Compare the solution with a given state. """
    compare = state == solution
    return compare.all()


def is_correct(n, state, solution):
    """ Compare the solution with a given state. """
    current_pos = num_to_pos(n, state)
    target_pos = num_to_pos(n, solution)
    return current_pos == target_pos


def solve_neighbor(n, state, solution):

    neighbors= [n for n in find_neighbors(n, state, pushable=True)]
    
    if 0 in neighbors:
        state = push(n, state)
    
    return state
    

""" From here on starting with different solving techniques for normal numbers, 
corner numbers and last six.

Beginning with normal numbers via basic circle. """


def find_basic_circle(n, state, solution, solved, helper=None, target_position=None):
    
#    logging.debug(f"Setting up basic circle for {n}")
    
    current_position = num_to_pos(n, state)
    zero_position = num_to_pos(0, state)
    
    if helper is not None:
        target_position = num_to_pos(int(helper), state)
#        logging.debug(f"making helper circle with {helper} on pos {target_position}")

    # extending to find basic circle in last six
    elif target_position is None:
        target_position = num_to_pos(n, solution)
    
    points = [current_position, target_position, zero_position]
#    logging.debug(points)
    
    points_y = [p[0] for p in points]
    points_x = [p[1] for p in points]
 
    y_min = min(points_y)
    y_max = max(points_y)
    x_min = min(points_x)
    x_max = max(points_x)

    if y_min == y_max:
        y_max += 1
    
    if x_min == x_max:
        x_max += 1
        
    numbers = list(set([*state[y_min, x_min:x_max], 
                        *state[y_max, x_min:x_max], 
                        *state[y_min:y_max+1, x_min], 
                        *state[y_min:y_max+1, x_max]]))
    
    if any([n for n in numbers if n in solved]):
#        logging.info("at least ONE tile can not be moved. no basic circle possible".upper())
        return []
    
    members = [pos_to_num(p, state) for p in points]
    if not all([n in numbers for n in members]):
#        logging.info("not all required elements in circle".upper())
        return []
    
    return [int(n) for n in numbers]


def sort_path(basic_circle, state):
    """ Sort path counterclockwise """
        
    assert basic_circle, "Basic circle is empty an cannot be sorted"

    basic_circle_pos = [num_to_pos(n, state) for n in basic_circle]
    
    bc_y = [y for y,x in basic_circle_pos]
    bc_x = [x for y,x in basic_circle_pos]
    
    y_min, y_max = min(bc_y), max(bc_y)
    x_min, x_max = min(bc_x), max(bc_x)
    
    left_vertical = [p for p in basic_circle_pos if p[1] == x_min]
    left_vertical_down = sorted(left_vertical, key=lambda p: p[0])
    
    bottom_horizontal = [p for p in basic_circle_pos if p[0] == y_max]
    bottom_horizontal_right = sorted(bottom_horizontal, key=lambda p: p[1])
    
    right_vertical = [p for p in basic_circle_pos if p[1] == x_max]
    right_vertical_up = sorted(right_vertical, key=lambda p: p[0], reverse=True)
   
    top_horizontal = [p for p in basic_circle_pos if p[0] == y_min]
    top_horizontal_left = sorted(top_horizontal, key=lambda p: p[1], reverse=True)
    
    path_pos = [n for n in [*left_vertical_down, *bottom_horizontal_right,
                            *right_vertical_up, *top_horizontal_left]]
    
    path_num = [pos_to_num(p, state) for p in path_pos]
    
    path = []
    for p in path_num:
        if p not in path:
            path.append(p)
    
    offset = path.index(0)
    path = np.roll(path, -offset)
    path = [int(n) for n in path]
#    logging.debug(f"basic path generated: {path}")
    return path


def best_path(path, n, solution, state):
    """ Sorting path based on distance to target number """
        
    assert path, "Path is empty"
#    logging.info(f"Sorting the path {path}")

    path_index_n = path.index(n)
    rev_path = list(reversed(path))
    rev_path_index_n = rev_path.index(n)
    
    if path_index_n < rev_path_index_n:
#        logging.debug("Reversing circle for quicker access")
        path = rev_path
    
#    logging.debug("best path created")
    return [t for t in path if t != 0]


def get_working_state(path, state):
    
    
    points = [num_to_pos(p, state) for p in path]

    points_y = [p[0] for p in points]
    points_x = [p[1] for p in points]
 
    y_min = min(points_y)
    y_max = max(points_y)
    x_min = min(points_x)
    x_max = max(points_x)

    
    return y_min, y_max+1, x_min, x_max+1


def rotate(n, path, state, solution, helper=None, target=False): 
    """ Rotate numbers along the given path by pushing them until target 
    position is reached """
    
#    logging.debug(f"rotating the path {path} to reach {n}")
    
    cpath = cycle(path)

    if helper is not None:
        while not ((num_to_pos(n, state)[0] == num_to_pos(n, solution)[0] == num_to_pos(0, state)[0]) or 
                   (num_to_pos(n, state)[1] == num_to_pos(n, solution)[1] == num_to_pos(0, state)[1])):
            state = push(next(cpath), state)         
            
    elif target is not False:
        target_pos = copy.deepcopy(num_to_pos(target, state))
        while not num_to_pos(n, state) == target_pos:
            state = push(next(cpath), state) 

    else:
        while not is_correct(n, state, solution):
            state = push(next(cpath), state)
        
    return state


def find_closest(n, state, solved): 
    """ Find the number to push, if 0 is locked or in corner """
    
    zero_neibors = find_neighbors(0, state, pushable=True)
    zero_free = [n for n in zero_neibors if n not in solved]
    
    closest = min([distance(n,p,state,dst.cityblock) for p in zero_free])
    
    closest_neigbor = [p for p in zero_free if distance(n,p,state,dst.cityblock) == closest]
    
    return closest_neigbor[0]


def zero_in_corner(state, solution, corners):
    zero_pos = num_to_pos(0, state)
    corners_pos = [num_to_pos(n, solution) for n in corners]
    return zero_pos in corners_pos
    
    

def solve_basic_circle(n, state, solution, solved):
    """ Combining the functions to solve the basic circle.
    If no basic circle possible use the following methods:
    - use helper on y/x numbers
    - simply push the number to get out of a corner
    
    basic circle functions seem to be completed"""
 
    basic_circle = find_basic_circle(n, state, solution, solved)
    
    while not basic_circle:
        n_y, n_x = num_to_pos(n, solution)
        
        y_helper_pos = (n_y+1, n_x)
        y_helper = pos_to_num(y_helper_pos, state)
        x_helper_pos = (n_y, n_x+1)
        x_helper = pos_to_num(x_helper_pos, state)

        y_helper_circle = find_basic_circle(n, state, solution, solved, helper=y_helper)
        x_helper_circle = find_basic_circle(n, state, solution, solved, helper=x_helper)
        
        if y_helper_circle:
            sorted_helper_path = sort_path(y_helper_circle, state)
            best_helper_path = best_path(sorted_helper_path, y_helper, solution, state)
            state = rotate(n, best_helper_path, state, solution, helper=y_helper)
            break
   
        elif x_helper_circle:
            sorted_helper_path = sort_path(x_helper_circle, state)
            best_helper_path = best_path(sorted_helper_path, x_helper, solution, state)
            state = rotate(n, best_helper_path, state, solution, helper=x_helper)
            break    
        
        closest = find_closest(n, state, solved)
        state = push(closest, state)

    basic_circle = find_basic_circle(n, state, solution, solved)     
    sorted_path = sort_path(basic_circle, state)
    _best_path = best_path(sorted_path, n, solution, state)
    state = rotate(n, _best_path, state, solution)
    return state

    



""" From here on the steps for solving the corner circles """


def find_corner_helper(n, state, solution):
    
    n_y, n_x = num_to_pos(n, solution)
    dim = len(state)
    if n_x == dim-1:
        helper_pos = n_y+1, n_x-1
        location = "top"
#        logging.debug(f"{n} is in upper-right corner")
    else:
        helper_pos = n_y-1, n_x+1
        location = "bottom"
#        logging.debug(f"{n} is in bottom-left corner")
    
    return pos_to_num(helper_pos, state), location
 
    

def solve_corner_circle(n, state, solution, solved):
    
    # bring the number to the relevant location
    helper, location = find_corner_helper(n, state, solution)
    basic_circle = find_basic_circle(n, state, solution, solved, helper=helper)
    sorted_path = sort_path(basic_circle, state)
    _best_path = best_path(sorted_path, n, solution, state)
    state = rotate(n, _best_path, state, solution, target=helper)
    
    # first: solution for upper right corner
    if location == "top":
        neighbors = find_neighbors(n, state)
        sorted_neighbors = sort_path(neighbors, state)
        
        neighbors_path = [n for n in reversed(sorted_neighbors) if n != 0]
        neighbors_path = cycle(neighbors_path)
        
        while True:
            to_push = next(neighbors_path)
            state = push(to_push, state)
            if to_push == n-1:
                break
        
        state = push(n, state)
        neighbors = find_neighbors(n, state)
        neighbors.append(n)
        sorted_neighbors = sort_path(neighbors, state)
        neighbors_path = [n for n in sorted_neighbors if n != 0]
        neighbors_path = cycle(neighbors_path)
        solve_basic_circle(n, state, solution, solved)
        state = push(n-1, state)
        state = push(n-2, state)
        

    # second: solution for bottom left corner
    if location == "bottom":
        dim = len(state)
        neighbors = find_neighbors(n, state)
        sorted_neighbors = sort_path(neighbors, state)
        
        neighbors_path = [n for n in sorted_neighbors if n != 0]
        neighbors_path = cycle(neighbors_path)
        
        while True:
            to_push = next(neighbors_path)
            state = push(to_push, state)
            if to_push == n-dim:
                break
        
        state = push(n, state)
        neighbors = find_neighbors(n, state)
        neighbors.append(n)
        sorted_neighbors = sort_path(neighbors, state)
        neighbors_path = [n for n in reversed(sorted_neighbors) if n != 0]
        neighbors_path = cycle(neighbors_path)
        solve_basic_circle(n, state, solution, solved)
        state = push(n-dim, state)
        state = push(n-(2 * dim), state)
        
    
    if is_correct(n, state, solution):
        return state
    
    else:
        raise RuntimeError



""" From here on is solvability check. """

def count_inversions(state):
    
    inversion_count = 0
    
    flat_state = state.flatten().tolist()
    
    for i,n in enumerate(flat_state):
        rest = flat_state[i+1:]
        count = len([x for x in rest if x < n and x != 0])
        inversion_count += count

    return inversion_count


def is_even(number):
    return number % 2 == 0    


def zero_in_even_row(state):
    
    dim = len(state)
    assert dim % 2 == 0
    zero_pos = num_to_pos(0, state)
    corrected_zero_y = zero_pos[0]
    return corrected_zero_y % 2 == 0
    

def is_solvable(state):
    
    inversions = count_inversions(state)
    dim = len(state)

    if not is_even(dim) and is_even(inversions):
        return True
    
    elif is_even(dim):
        if (zero_in_even_row(state) and not is_even(inversions) or 
            not zero_in_even_row(state) and is_even(inversions)):
            return True
    
    return False


""" From here on solving last six. """


def is_correct_pattern(LAST_SIX, state, SOLUTION, ONETWO):
    
#    logging.debug("Checking if ONE and TWO are in the right order")
    ONE, TWO = ONETWO
    path = list(reversed(sort_path(LAST_SIX, state)))
    pattern = str(ONE)+str(TWO)
    
    double_path = path + path
    double_path = [n for n in double_path if n != 0]
    str_path = "".join([str(n) for n in double_path])
    if pattern in str_path:
#        logging.debug(f"pattern found in {path}")
        return True
 
#    logging.debug("ONE and TWO pattern not found")
    return False



def solve_last_six(state, SOLUTION, PUZZLE_DIM, LAST_SIX):

    """ Approach: First separate ONE from TWO by bringing them into diffent 
    squares of the six.
    Then rotate until ONE is upper left and TWO upper right. Zero must be in
    upper middle.
    Then rotate the six until ONE and TWO are in correct place.
    Finally rotate the rest until puzzle solved! """
    
#    logging.info("Solving the last six")
    
    working_state = state[PUZZLE_DIM-2:, PUZZLE_DIM-3:]
    
    ONE = LAST_SIX[3]
    TWO = LAST_SIX[0]
    ONETWO = [ONE, TWO]
 
    Q1 = working_state[:,:-1]
    Q2 = working_state[:,1:]
    
    UP_LEFT = copy.deepcopy(num_to_pos(int(state[PUZZLE_DIM-2,PUZZLE_DIM-3]), state))
    UP_MID = copy.deepcopy(num_to_pos(int(state[PUZZLE_DIM-2,PUZZLE_DIM-2]), state))
    UP_RIGHT = copy.deepcopy(num_to_pos(int(state[PUZZLE_DIM-2,PUZZLE_DIM-1]), state))
    DOWN_LEFT = copy.deepcopy(num_to_pos(int(state[PUZZLE_DIM-1,PUZZLE_DIM-3]), state))
    DOWN_MID = copy.deepcopy(num_to_pos(int(state[PUZZLE_DIM-1,PUZZLE_DIM-2]), state))
    DOWN_RIGHT = copy.deepcopy(num_to_pos(int(state[PUZZLE_DIM-1,PUZZLE_DIM-1]), state))
    
    LEFT = [UP_LEFT, DOWN_LEFT]
    RIGHT = [UP_RIGHT, DOWN_RIGHT]
    MIDDLE = [DOWN_MID, UP_MID]
    
    while not puzzle_solved(state, SOLUTION):
        
        Q1 = working_state[:,:-1]
        Q2 = working_state[:,1:]
        
        one_prepared = num_to_pos(ONE, state) == UP_LEFT
        two_prepared = num_to_pos(TWO, state) == UP_RIGHT
        one_correct = num_to_pos(ONE, state) == DOWN_LEFT
        two_correct = num_to_pos(TWO, state) == UP_LEFT
        one_pos = num_to_pos(ONE, state)
        two_pos = num_to_pos(TWO, state)
        zero_pos = num_to_pos(0, state)
        
       
        # one and two already in the correct positions
        if one_correct and two_correct:
            path = sort_path(Q2.flatten().tolist(), state)
            path.remove(0)
            path = cycle(path)
            while not puzzle_solved(state, SOLUTION):
                number = next(path)
                state = push(number, state)
#            logging.info("puzzle solved!".upper())  
            return state
        
        
        # one and two in wrong positions, but correct pattern 
        if is_correct_pattern(LAST_SIX, state, SOLUTION, ONETWO):
            path = list(reversed(sort_path(LAST_SIX, state)))
            path = sort_path(path, state)
            path = cycle([n for n in path if n != 0])
            while not all([is_correct(n, state, SOLUTION) for n in ONETWO]):
                to_push = next(path)
                state = push(to_push, state)
                if one_correct and two_correct:
                    break
#            logging.debug("ONE and TWO are in their correct positions")
#            logging.debug(state)
            continue
        
        
        # one in up left, two is in down left, zero not adjacent to two
        # goal: bring zero to down mid
        if (one_prepared and
            two_pos == DOWN_LEFT and 
            zero_pos != DOWN_MID):
#            logging.debug("two in down left and 0 not adjacent")
            path = sort_path(Q2.flatten().tolist(), state)
            path.remove(0)
            path = cycle(path)
            while True:
                number = next(path)
                state = push(number, state)
                if num_to_pos(0, state) == DOWN_MID:
#                    logging.debug("0 in down mid")
                    break
            continue
        
        if (one_prepared and two_pos == DOWN_LEFT and
            zero_pos == DOWN_MID):
#            logging.debug("solving via hardcoding")
            solution = [DOWN_LEFT, UP_LEFT, UP_MID, DOWN_MID, DOWN_RIGHT,
                        UP_RIGHT, UP_MID, UP_LEFT, DOWN_LEFT, DOWN_MID,
                        UP_MID]
            for n in solution: 
                number = pos_to_num(n, state)
                state = push(number, state)
            
            continue  
        
        # one in up left, two and zero in Q2
        # goal: bring zero to down mid
        if (one_prepared and
            TWO in Q2 and 0 in Q2):
#            logging.debug("one in position, two and zero in Q2")
            path = sort_path(Q2.flatten().tolist(), state)
            path.remove(0)
            path = cycle(path)
            while True:
                number = next(path)
                state = push(number, state)
                if num_to_pos(TWO, state) == UP_RIGHT:
#                    logging.debug("positions reached")
                    break
            continue

        # one and two prepared, zero in down mid
        if (one_prepared and
            two_prepared and 
            zero_pos == DOWN_MID):
#            logging.debug("one, two correct, 0 down mid")
            
            number = pos_to_num(UP_MID, state)
            state = push(number, state)
            continue
        
        # one and two prepared, zero in down left or down right
        if (one_prepared and
            two_prepared and 
            (zero_pos == DOWN_RIGHT or
             zero_pos == DOWN_LEFT)):
#            logging.debug("one, two correct, 0 down left oder 0 down right")
            
            to_push = (DOWN_MID, UP_MID)
            to_push = [pos_to_num(pos, state) for pos in to_push]
            for p in to_push:
                state = push(p, state)
            continue   
        
        # no particular pattern, bringing one in prepare position
        else:
#            logging.info("no relevant pattern found")
            path = sort_path(LAST_SIX, state)
            path.remove(0)
            path = cycle(path)
            while True:
                number = next(path)
                state = push(number, state)
                if num_to_pos(ONE, state) == UP_LEFT:
#                    logging.debug("one in correct position")
                    break
            continue
  
        
#        logging.error("something went wrong")        
        return state
    
    return state
        


""" From here on is the main function. """

# global variable for the output
memory = []

def slide_puzzle(ar, testing=False):
    
    print(ar)
    
    """ Main function solving the puzzle. """
    state = np.array(ar, dtype="i")
    solved = []
    global memory
    memory = []  # reset memory between tests
    
    
    # Setting up constants
    PUZZLE_DIM = len(state)
    SOLUTION = make_solution(PUZZLE_DIM)
    LAST_SIX = SOLUTION[PUZZLE_DIM-2:, PUZZLE_DIM-3:]
    LAST_SIX = [n for n in LAST_SIX.flatten().tolist()]
    CORNER_NUMBERS = find_corners(SOLUTION, PUZZLE_DIM, LAST_SIX) 
    SOLVING_ORDER = sort_numbers(SOLUTION, PUZZLE_DIM, LAST_SIX)
    
    
    # check if puzzle is solvable
    if not is_solvable(state):
#        logging.error("puzzle not solvable")
        return None
    
    # special case: 0 or n in corner and cannot be moved out
    
    
    # Creating main loop
    SOLVING_ORDER = iter(SOLVING_ORDER)
    
    step = 0
    
    while not puzzle_solved(state, SOLUTION):
        
        step += 1
        if step > 100:
            return None
        
#        logging.info(f"current state\n {state}")
        
        try:
            n = next(SOLVING_ORDER)
        
        except StopIteration:
#            logging.info("No more numbers via basic solving")
            break
 
#        logging.info(f"Working on number {n}".upper())

        # check if n already in right position
        if is_correct(n, state, SOLUTION):
#            logging.info(f"Number {n} is already in correct position")
            solved.append(n)
#            logging.info(f"Working on number {n}".upper())
            continue
     
        # check if number is next to the target, push it
        if (n in find_neighbors(0, state, pushable=True) and 
              num_to_pos(n, SOLUTION) == num_to_pos(0, state)):
            state = push(n, state)
            solved.append(n)
#            logging.debug("neighbor")
            continue
        
        # if zero is in corner, push it out => before circle solution
        # maybe needs to be made wider
        # no continuation here, because no solving progress
        if zero_in_corner(state, SOLUTION, CORNER_NUMBERS):
            to_push = find_closest(n, state, solved)
#            logging.info(f"zero in corner, pushing {to_push}")
            state = push(to_push, state)
#            logging.info(f"current state\n {state}")
        
        # solve basic circle
        if n not in CORNER_NUMBERS and n not in LAST_SIX:
            state = solve_basic_circle(n, state, SOLUTION, solved)
            solved.append(n)
#            logging.info(f"current state\n {state}")
            continue
        
        # solve corner circle
        if n in CORNER_NUMBERS:
            state = solve_corner_circle(n, state, SOLUTION, solved)
            solved.append(n)
#            logging.info(f"current state\n {state}")
            continue
        
        if n in LAST_SIX:
            state = solve_last_six(state, SOLUTION, PUZZLE_DIM, LAST_SIX)
            break
        
       
#    logging.info(f"final state\n {state}".upper())
    print(state)

    if testing is not False:
        return state
    
    return memory
  
#########################
class SBoard:

    def __init__(self, board):
        self.dir = {'E': (0, 1), 'S': (1, 0), 'W': (0, -1), 'N': (-1, 0)}
        self.board = []
        for line in board:
            self.board.append(line.copy())
        self.len = len(board)
        self.stones = self._mk_stones_(board)
        self.action = []

    def __str__(self):
        out = "\n"
        for line in self.board:
            for field in line:
                out += "%3d" % field
            out += "\n"
        return out

    def _mk_stones_(self, arr):
        out = {}
        for y in range(self.len):
            for x in range(self.len):
                out[arr[y][x]] = (y, x)
        return out

    def move(self, x: int):
        self.board[self.stones[0][0]][self.stones[0][1]] = x
        self.board[self.stones[x][0]][self.stones[x][1]] = 0
        self.stones[0], self.stones[x] = self.stones[x], self.stones[0]
        self.action.append(x)

    def first_false(self):
        for y in range(self.len):
            for x in range(self.len):
                ff = (y * self.len) + x
                if x < self.len - 2 and self.board[y][x] != ff + 1:
                    return ff + 1, y, x
                elif x == self.len - 2:
                    if self.board[y][x] == ff + 1 and self.board[y][x + 1] == 0 and y < self.len - 1 and self.board[y + 1][x + 1] == ff + 2:
                        return ff + 2, y, x + 1
                    if self.board[y][x + 1] == ff + 1 and self.board[y + 1][x + 1] != ff + 2:
                        return ff + 2, y + 1, x + 1
                    if self.board[y][x + 1] == ff + 1 and self.board[y + 1][x + 1] == ff + 2:
                        return ff + 1, y, x
                    if self.board[y][x] != ff + 1 or self.board[y][x + 1] != ff + 2:
                        return ff + 1, y, x + 1
                elif x == self.len - 1 and self.board[y][x] != ff + 1:
                    if self.board[y][x] == ff:
                        return ff + 1, y + 1, x
                    else:
                        return ff + 1, y, x

    def solved(self):
        for y in range(self.len):
            for x in range(self.len):
                ff = (y * self.len) + x + 1
                if self.board[y][x] != ff and ff < self.len * self.len:
                    return False
        return True

    @staticmethod
    def _cadd_(c1: tuple, c2: tuple):
        return c1[0] + c2[0], c1[1] + c2[1]

    def z_move(self, ty: int, tx: int, ff: int):
        path: str = "S" * max(ty - self.stones[0][0], 0)
        path += "E" * max(tx - self.stones[0][1], 0)
        path += "W" * max(self.stones[0][1] - tx, 0)
        path += "N" * max(self.stones[0][0] - ty, 0)
        self._z_go_(path, ff, True)

    def _z_go_(self, plan: str, ff: int, chck: bool):
        alterNE = {'SS': 'WSSE', 'SE': 'ES', 'SW': 'WS',
                 'EE': 'SEEN', 'EN': 'SEENNW', 'ES': 'SE',
                 'WW': 'SWWN', 'WN': 'NW', 'WS': 'SW',
                 'NE': 'EN', 'NN': 'ENNW', 'NW': 'WN'}
        alterN = {'SS': 'WSSE', 'SW': 'WS',
                 'EN': 'NE', 'ES': 'SE',
                 'NN': 'WNNE', 'NW': 'WN'}
        alterS = {'SE': 'ES', 'SW': 'WS',
                  'WW': 'NWWS', 'WN': 'NW',
                  'EE': 'NEES', 'EN': 'NE',
                  'NN': 'WNNE', 'NW': 'WN'}
        skip = False
        for i, mv in enumerate(plan):
            if skip:
                skip = False
            else:
                ncoord = self._cadd_(self.stones[0], self.dir[mv])
                if chck and self.stones[ff] == ncoord:
                    ffc = self.stones[ff]
                    skip = True
                    if ffc[0] < self.len - 1 and ffc[1] < self.len - 1:
                        self._z_go_(alterNE[plan[i:i + 2]], ff, False)
                    elif ffc[1] == self.len - 1:
                        self._z_go_(alterN[plan[i:i + 2]], ff, False)
                    elif ffc[0] == self.len - 1 and ffc[1] < self.len - 1:
                        self._z_go_(alterS[plan[i:i + 2]], ff, False)
                else:
                    self.move(self.board[ncoord[0]][ncoord[1]])

    def top_move(self):
        ff, ty, tx = self.first_false()
        if self.stones[0] == (ty - 1, tx - 1) and self.stones[ff] == (ty, tx - 1) and (ff % self.len) == 0:
            self.move(ff)
        if (self.stones[ff][0] * self.len) + self.stones[ff][1] < ff and (ff % self.len) == 0:
            self.z_move(self.stones[ff][0] + 1, self.stones[ff][1], ff)
            self._z_go_("NESWSENNWSES", ff, False)
            return
        while self.stones[ff][1] < tx:
            self.z_move(self.stones[ff][0], self.stones[ff][1] + 1, ff)
            self.move(ff)
        while ty < self.stones[ff][0]:
            self.z_move(self.stones[ff][0] - 1, self.stones[ff][1], ff)
            self.move(ff)
        while tx < self.stones[ff][1]:
            self.z_move(self.stones[ff][0], self.stones[ff][1] - 1, ff)
            self.move(ff)
        if ff == self.first_false():
            self.move(ff)

    def bot_move(self, ff: int, ty: int, tx: int):
        if self.stones[ff][0] == ty - 1 and self.stones[ff][1] == tx - 1 and tx < self.len - 1:
            self.z_move(ty, tx, ff)
            self._z_go_("WNEESWWNESWNESENWSWNE", ff, False)
            return
        elif ((ff - 1) // self.len) == (self.len - 1) and self.stones[ff] == (ty - 1, tx) and self.stones[0] == (ty - 1, tx - 1) and tx < self.len - 1:
            self._z_go_("SENESWWNESE", ff, False)
            return
        elif self.stones[ff][0] < ty:
            while self.stones[0][1] < self.stones[ff][1] - 1:
                self._z_go_("E", ff, False)
            self.z_move(self.stones[ff][0] + 1, self.stones[ff][1], ff)
            self.move(ff)
        while tx < self.stones[ff][1]:
            zmv = ""
            if self.stones[0][0] == self.len - 1:
                zmv += "N"
            zmv += "W" * max(0, self.stones[0][1] - self.stones[ff][1] + 1)
            zmv += "E" * max(0, self.stones[ff][1] - self.stones[0][1] - 1)
            zmv += "SE"
            self._z_go_(zmv, ff, False)

    def last_rows(self):
        for x in range(self.len - 1):
            for y in range(self.len - 2, self.len):
                ff, ty, tx = (self.len * y) + x + 1, self.len - 1, x + (y - self.len + 2)
                self.bot_move(ff, ty, tx)
            if self.stones[ff] == (ty, tx) and self.stones[0] == (ty - 1, tx - 1):
                self._z_go_("SE", ff, False)
            elif self.stones[ff] == (ty, tx) and self.stones[0] == (ty - 1, tx):
                self._z_go_("WSE", ff, False)
            elif self.stones[ff] == (ty, tx) and self.stones[0] == (ty, tx + 1):
                self._z_go_("NWWSE", ff, False)
            elif self.stones[ff] == (ty, tx):
                self.z_move(ty - 1, tx + 1, ff)
                self._z_go_("WWSE", ff, False)


def slide_puzzle(ar):
    sboard = SBoard(ar)
    while sboard.first_false()[0] <= sboard.len * (sboard.len - 2):
        sboard.top_move()
    sboard.last_rows()
    return sboard.action if sboard.solved() else None
  
#########################
import numpy as np
import queue
def compare(a, b):
    if a == b:
        return 0
    if a > b:
        return 1
    if a < b:
        return -1
class Puzzle:
    def __init__(self, puzzle):
        self.puzzle = np.array(puzzle, dtype=np.object)
        self.solved = np.zeros_like(self.puzzle, dtype=int)
        self.height, self.width = self.puzzle.shape
        self.steps = []
        # Build puzzle & solution to compare against:
        for i, row in enumerate(self.puzzle):
            for j, value in enumerate(row):
                self.puzzle[i, j] = Case(value)
                self.puzzle[i, j].y, self.puzzle[i, j].x = i, j
                self.solved[i, j] = 1 + j + self.width*i
        self.solved[-1, -1] = 0
        # Create paths for all cases
        for row in self.puzzle:
            [case.get_paths(self.puzzle) for case in row]
    def clear(self):
        [case.clear() for case in np.ravel(self.puzzle)]
    def find_number(self, n):
        for row in self.puzzle:
            for node in row:
                if node.value == n:
                    return node
        return None
    def solve_number(self, destination, number, ignore=None, solve=True):
        while destination.value != number:
            hole = self.find_number(0)
            # Finds the number you want to put in Destination
            goto = self.find_number(number)
            # Finds which adjacent case we should approach it from
            adjacent = goto.best_adjacent(self.puzzle, relative_to=destination)
            # Finds the shortest path to the adjacent case
            path = hole.astar(self, adjacent, goto, ignore)
            # Moves to it
            for one, two in zip(path, path[1:]):
                self.steps.append(two.value)
                one.swap(two)
            else:
                self.steps.append(goto.value)
                path[-1].swap(goto)
        if solve:
            destination.solved = True
        return True
    def solve_line(self, line, solutions, helper_cases):
        # Give it a line and what you want that line to look like
        for case, solution in zip(line[:-2], solutions[:-2]):
            self.solve_number(case, solution)
        # Now the hard solve with line[-2:] and solutions[-2:]
        # Ponemos el 4 y el 3 en un lugar seguro
        self.solve_number(helper_cases[2], solutions[-1], solve=False)
        self.solve_number(helper_cases[3], solutions[-2], solve=False)
        self.solve_number(line[-1], solutions[-2], solve=False)
        self.solve_number(helper_cases[0], solutions[-1], solve=False)
        if line[-2] != self.find_number(0):
            self.solve_number(helper_cases[1], line[-2].value,
                              ignore=[helper_cases[0], line[-1]], solve=False)
        self.solve_number(line[-2], solutions[-2])
        self.solve_number(line[-1], solutions[-1])
        return True
    def smol_solve(self):
        # First solves top row & column, etc, until 2x3 block left
        # helper_case[0] is below the last case of the row (row+1, -1)
        # helper_case[1] is to the left of helper_case[0]
        # We want to reduce up to a 2x2 grid
        smallest = 2
        for i in range(self.height-smallest):
            helper_cases = (self.puzzle[i+1, -1], self.puzzle[i+1, -2],
                            self.puzzle[i+2, -1], self.puzzle[i+2, -2])
            self.solve_line(self.puzzle[i, :], self.solved[i, :], helper_cases)
            helper_cases = (self.puzzle[-1, i+1], self.puzzle[-2, i+1],
                            self.puzzle[-1, i+2], self.puzzle[-2, i+2])
            self.solve_line(self.puzzle[i+1:, i], self.solved[i+1:, i], helper_cases)
        return True
    def final_solve(self, fragment, solution):
        # Solves a 2x2 puzzle
        for i in range(24):
            solution = self.puzzle[-3:, -3:].ravel().tolist()[:-1]
            solution = [s.value for s in solution]
            if sorted(solution) == solution:
                # Done
                return True
            hole = self.find_number(0)
            if i < 12:
                # 3 loops one way, 3 loops the other one
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -2]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -1]
            if i >= 12:
                # 3 loops one way, 3 loops the other one
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -1]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -2]
            self.steps.append(guy.value)
            hole.swap(guy)
        # print('couldnt find solution')
        self.steps = None
    def solve(self):
        # Solve it until we only have a 2x2 square on the bottom right
        self.smol_solve()
        # Solve the 2x2 square (first argument is square, second is solution)
        self.final_solve(self.puzzle[-3:, -3:].ravel().tolist(),
                         self.solved[-3:, -3:].ravel().tolist())
        print(self.puzzle)
class Case:
    def __init__(self, value):
        self.value = value
        self.solved = False
        self.paths = []
        self.distance = np.Infinity
        self.back = None
    def __gt__(self, other):
        return self.distance > other.distance
    def __repr__(self):
        return str(self.value)
    @property
    def info(self):
        return f'Case w/ value {self.value} at ({self.y}, {self.x}).'
    def clear(self):
        self.distance = np.Infinity
        self.back = None
    def swap(self, other):
        self.value, other.value = other.value, self.value
        self.solved, other.solved = other.solved, self.solved
    def get_paths(self, puzzle):
        height, width = puzzle.shape
        if self.y > 0:
            self.paths.append(puzzle[self.y-1, self.x])
        if self.y < height-1:
            self.paths.append(puzzle[self.y+1, self.x])
        if self.x > 0:
            self.paths.append(puzzle[self.y, self.x-1])
        if self.x < width-1:
            self.paths.append(puzzle[self.y, self.x+1])
    def best_adjacent(self, puzzle, relative_to):
        # y1, x1 = relative_to.y, relative_to.x
        possible_paths = []
        for path in self.paths:
            if not path.solved:
                # Changed to distance_to
                # OLD: possible_paths.append((abs(y1-path.y)+abs(x1-path.x), path))
                possible_paths.append((relative_to.distance_to(path), path))
        if not possible_paths:
            # Error check, shouldn't happen on solvable puzzles
            print(f'Could not find any good adjacent cases for {self.y}, {self.x}')
            for path in self.paths:
                print(f'({path.y}, {path.x}), solved = {path.solved}')
            print(puzzle.puzzle)
        solution = sorted(possible_paths, key=lambda x: x[0])[0]
        return solution[1]
    def dijkstra(self, puzzle, destination, number, ignore=None):
        '''A* is way more efficient on big maps! Use it instead'''
        # Number = the number we want to put in Destination
        # Shortest path to position, ignoring the solved cases and the Number
        # It has to ignore Number because else it will displace it and fuck it up
        # Basically we take the zero to Destination(which will be right next to Number)
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))
        while not q.empty():
            _, case = q.get()
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore:
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance, posib))
        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)
        puzzle.clear()
        return list(reversed(path))
    def astar(self, puzzle, destination, number, ignore=None):
        # MOVING HOLE(SELF) TO DESTINATION
        # Number = the number we want to put in Destination
        # Shortest path to position, ignoring the solved cases and the Number
        # It has to ignore Number because else it will displace it and fuck it up
        # Basically we take the zero to Destination(which will be right next to Number)
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))
        while not q.empty():
            _, case = q.get()
            if case == destination:
                break
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore: 
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance_to(destination), posib))
        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)
        puzzle.clear()
        return list(reversed(path))
    def distance_to(self, other):
        return abs(self.y-other.y)+abs(self.x-other.x)
def slide_puzzle(array):
    # Code-execution function
    puzzle = Puzzle(array)
    puzzle.solve()
    return puzzle.steps
# TEST CASE
array = [
        [4, 1, 3],
        [2, 8, 0],
        [7, 6, 5],
        ]

#############################
from heapq import *

class SlidingPuzzle:
    
    cardinal_directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    
    def __init__(self, puzzle):
        self.N         = len(puzzle)
        self.lookup    = {v: (i, j) for i, r in enumerate(puzzle) for j, v in enumerate(r)}    # Value -> coordinates
        self.board     = [row.copy() for row in puzzle]                                        # State of board
        self.moves     = []                                                                    # List of moves made
        self.frozen    = [[False] * self.N for _ in range(self.N)]                             # Locked positions
        self.end_state = [[i * self.N + j + 1 for j in range(self.N)] for i in range(self.N)]  # Solved board
        self.end_state[self.N - 1][self.N - 1] = 0
    
    def print_board(self):
        print('---' * self.N)
        for row in self.board:
            print(row)
        print('---' * self.N)
    
    def is_in_range(self, y, x):
        return 0 <= y < self.N and 0 <= x < self.N
    
    def swap(self, y, x):
        ''' Swap value at position (y, x) with 0 (empty cell), assuming they are adjacent. '''
        i, j = self.lookup[0]
        assert abs(i - y) + abs(j - x) == 1
        v = self.board[y][x]
        self.moves.append(v)
        self.lookup[0] = (y, x)
        self.lookup[v] = (i, j)
        self.board[i][j], self.board[y][x] = self.board[y][x], self.board[i][j]
    
    def move(self, cell, dest, freeze=[]):
        ''' 
        Move cell to a given coordinate dest. 
        Temporary freezes coordinates listed in optional argument freeze.
        '''
        for i, j in freeze: self.frozen[i][j] = True
        
        if cell:
            for pos in self.shortest_path(self.lookup[cell], dest):
                i, j = self.lookup[cell]
                self.frozen[i][j] = True
                for pos2 in self.shortest_path(self.lookup[0], pos):
                    self.swap(*pos2)
                self.frozen[i][j] = False
                self.swap(i, j)
        else:
            for pos in self.shortest_path(self.lookup[cell], dest):
                self.swap(*pos)
        
        for i, j in freeze: self.frozen[i][j] = False
        
    def shortest_path(self, start, dest):
        ''' Return a list of coordinates for the shortest path from start to dest. '''
        dist = [[float('inf')] * self.N for _ in range(self.N)]
        dist[start[0]][start[1]] = 0
        pq, pred = [(0, start)], {start: None}

        while pq:
            d, pos = heappop(pq)
            if pos == dest: break
            for k, l in [map(sum, zip(pos, q)) for q in SlidingPuzzle.cardinal_directions]:
                if self.is_in_range(k, l) and not self.frozen[k][l] and d + 1 < dist[k][l]:
                    dist[k][l]   = d + 1
                    pred[(k, l)] = pos
                    heappush(pq, (d + 1, (k, l)))
        
        if dest not in pred: return []
        
        path, pos = [], dest
        while pred[pos]:
            path.append(pos)
            pos = pred[pos]
        return path[::-1]
    
    def is_solved(self):
        return all(x == y for x, y in zip(self.board, self.end_state))
    
    def solve_2x3(self):
        ''' Solves the remaining unsolved 2 times 3 dimensional rectangle, if a solution exists. '''
        N = self.N
        z, a, b, c, d, e = sorted(v for r in self.board[N - 2:] for v in r[N - 3:])
        if {z, a, b, c, d, e} == {v for r in self.end_state[N - 2:] for v in r[N - 3:]}:
            self.move(a, (N - 1, N - 1))
            if self.board[N - 2][N - 1] == b or self.board[N - 2][N - 2:] == [b, z]:
                self.move(b, (N - 1, N - 3))
                self.move(a, (N - 1, N - 1))
            self.move(b, (N - 1, N - 2), freeze=[(N - 1, N - 1)])
            self.move(a, (N - 2, N - 1), freeze=[(N - 1, N - 2)])
            self.swap(N - 1, N - 2)
            self.move(c, (N - 1, N - 2))
            self.move(a, (N - 2, N - 2), freeze=[(N - 1, N - 2)])
            for i in range(1, 4): self.swap(N - 1, N - i)
            for i in range(1, 4): self.swap(N - 2, N - 4 + i)
            self.swap(N - 1, N - 1)
    
    def solve(self):
        ''' Solves the puzzle and return the moves made if it is solvable, otherwise return None. '''
        N = self.N
        for i in range(N):
            
            # Finish topmost unfinished row
            
            for j in range(N - 2):
                self.move(self.end_state[i][j], (i, j))
                self.frozen[i][j] = True
            
            y, x = self.lookup[self.end_state[i][N - 1]]
            if abs(y - i) + abs(x - N + 1) < 3: 
                self.move(self.end_state[i][N - 1], (N - 1, N - 1))
            
            self.move(self.end_state[i][N - 2], (i, N - 1))
            self.move(self.end_state[i][N - 1], (i + 1, N - 1), freeze=[(i, N - 1)])
            self.move(self.end_state[i][N - 2], (i, N - 2),     freeze=[(i + 1, N - 1)])
            self.swap(i + 1, N - 1)
            self.frozen[i][N - 2] = self.frozen[i][N - 1] = True
            
            if i == N - 3:
                self.solve_2x3()
                return self.moves if self.is_solved() else None
            
            # Finish leftmost unfinished column
            
            for j in range(1, N - 2):
                self.move(self.end_state[j][i], (j, i))
                self.frozen[j][i] = True
            
            y, x = self.lookup[self.end_state[N - 1][i]]
            if abs(y - N + 1) + abs(x - i) < 3: 
                self.move(self.end_state[N - 1][i], (N - 1, N - 1))
            
            self.move(self.end_state[N - 2][i], (N - 1, i))
            self.move(self.end_state[N - 1][i], (N - 1, i + 1), freeze=[(N - 1, i)])
            self.move(self.end_state[N - 2][i], (N - 2, i),     freeze=[(N - 1, i + 1)])
            self.swap(N - 1, i + 1)
            self.frozen[N - 2][i] = self.frozen[N - 1][i] = True
        
def slide_puzzle(puzzle):
    return SlidingPuzzle(puzzle).solve()
  
##########################
def slide_puzzle(ar):
    puzzle=Puzzle(ar)
    try:
        puzzle.slide()
    except IndexError:
        return None
    return puzzle.history


class Cell(object):
    
    def __init__(self,target_val,current_val):
        self.footprint=0
        self.target_val=target_val
        self.current_val=current_val
        
    def make_steady(self):
        self.footprint=-1
        
    def make_zero(self):
        self.footprint=0

class Puzzle(object):
    
    def __init__(self,input_puzz):
        self.size=len(input_puzz)
        self.cells={}
        self.history=[]
        numbers=iter(enumerate([y for x in input_puzz for y in x]))
        for r in range(self.size):
            for c in range(self.size):
                target,current=next(numbers)
                self.cells[r,c]=Cell(target+1,current)
        self.cells[self.size-1,self.size-1].target_val=0
        
    def change_current(self,with_zero,with_value):
        assert self.cells[with_zero].current_val==0
        value=self.cells[with_value].current_val
        self.cells[with_value].current_val=0
        self.cells[with_zero].current_val=value
        
    def make_step(self,with_start,with_end):
        passenger=self.cells[with_start].current_val
        pedestrian=self.cells[with_end].current_val
        self.cells[with_end].current_val=passenger
        self.cells[with_start].current_val=pedestrian
        self.history.append(max(passenger,pedestrian))
        
    def find_neighbours(self,middle,forbidden=-1):
        row,column=middle
        up=(row-1,column)
        right=(row,column+1)
        down=(row+1,column)
        left=(row,column-1)
        to_check=[up,right,down,left]
        result=[]
        for i in to_check:
            current=self.cells.get(i)
            if current:
                if current.footprint==0 and current.current_val!=forbidden:
                    result.append(i)
        return result
    
    def find_cell(self,number):
        for k,v in self.cells.items():
            if v.current_val==number:
                return k
        return None
    
    def find_target(self,number):
        for k,v in self.cells.items():
            if v.target_val==number:
                return k
        return None
    
    def find_start_end(self,number):
        return (self.find_cell(number),self.find_target(number))
            
    def find_path(self,start,end,forbidden=-1):
        if start==end:
            return []
        step=1
        processor=[]
        first_path=[]
        first_path.append(start)
        processor.append(first_path)
        while True:
            curr_path=processor.pop(0)
            last_cell=curr_path[-1]
            if last_cell==end:
                return curr_path
            footprints=self.find_neighbours(last_cell,forbidden)
            for i in footprints:
                self.cells[i].footprint=step
                new_path=curr_path+[i]
                last_cell=new_path[-1]
                processor.append(new_path)
            step+=1
        return []
    
    def clear_footprint(self):
        for v in self.cells.values():
            if v.footprint>-1:
                v.footprint=0
                
    def create_footsteps(path):
        starts=path[:-1]
        ends=path[1:]
        footsteps=zip(starts,ends)
        return footsteps
    
    def execute_travel(self,path):
        for pair in path:
            self.make_step(pair[0],pair[1])
    
    def move_home(self,number,*,correction=(0,0),freeze=True):
        togo=self.find_start_end(number)
        start=togo[0]
        end=(togo[1][0]+correction[0],togo[1][1]+correction[1])
        if start==end:
            if freeze:
                self.cells[end].make_steady()
                return
        pre_path=self.find_path(start,end)
        self.clear_footprint()
        home_path=Puzzle.create_footsteps(pre_path)
        for pair in home_path:
            if self.cells[pair[1]].current_val>0:
                start_zero=self.find_cell(0)
                zero_path=Puzzle.create_footsteps(self.find_path(start_zero,pair[1],number))
                self.execute_travel(zero_path)
                self.clear_footprint()
            self.make_step(pair[0],pair[1])
        if freeze:
            self.cells[end].make_steady()
    
    def move_corner(self,pair):
        correction1=()
        correction2=()
        correction3=()
        if pair[1]-pair[0]==1:
            correction1=(2,0)
            correction2=(0,1)
            correction3=(1,0)
        else:
            correction1=(0,2)
            correction2=(1,0)
            correction3=(0,1)      
            
        first=pair[0]
        second=pair[1]
        first_target=self.find_target(first)
        second_target=self.find_target(second)
        
        to_unfreeze1=(first_target[0]+correction2[0],first_target[1]+correction2[1])
        to_unfreeze2=(second_target[0]+correction3[0],second_target[1]+correction3[1])
        
        self.move_home(second,correction=correction1,freeze=False)
        self.move_home(first,correction=correction2)
        self.move_home(second,correction=correction3)
        self.move_home(first)
        self.cells[to_unfreeze1].make_zero()
        self.cells[to_unfreeze2].make_zero()
        self.move_home(second)
    
    def final_check(self):
        for k,v in self.cells.items():
            if v.current_val!=v.target_val:
                return False
        return True
    
    def vortex(self):
        if self.final_check():
            return
        base=self.size*self.size
        self.move_home(base-self.size-1)
        self.move_home(base-self.size)
        self.move_home(base-1)
        
    def create_todo(number):
        base=list(range(1,number+1))
        result=[]
        last=0
    
        for i in range(number-2):
            for j in range(number-2):
                current=i*number+base[j]
                if current not in result:
                    result.append(current)
            last=current        
            result.append((last+1,last+2))
        
            for j in range(number-2):
                current=(i+1)+j*number
                if current not in result:
                    result.append(current)
            last=current      
            result.append((last+number,last+2*number))      
        
        return result
    
    def slide(self):
        work=Puzzle.create_todo(self.size)
        for i in work:
            if type(i)==int:
                self.move_home(i)
            else:
                self.move_corner(i)
        self.vortex()
        
##########################
def slide_puzzle(ar):
    move = []
    def searchnum(x):
        for j in range(len(ar)):
            for i in range(len(ar)):
                if x == ar[j][i]:
                    return [j,i]
                
    def movezeroup():
        coorzero = searchnum(0)
        dummy = ar[coorzero[0]-1][coorzero[1]]
        move.append(dummy)
        ar[coorzero[0]-1][coorzero[1]] = 0
        ar[coorzero[0]][coorzero[1]] = dummy
    
    def movezerodown():
        coorzero = searchnum(0)
        dummy = ar[coorzero[0]+1][coorzero[1]]
        move.append(dummy)
        ar[coorzero[0]+1][coorzero[1]] = 0
        ar[coorzero[0]][coorzero[1]] = dummy
    
    def movezeroright():
        coorzero = searchnum(0)
        dummy = ar[coorzero[0]][coorzero[1]+1]
        move.append(dummy)
        ar[coorzero[0]][coorzero[1]+1] = 0
        ar[coorzero[0]][coorzero[1]] = dummy
    
    def movezeroleft():
        coorzero = searchnum(0)
        dummy = ar[coorzero[0]][coorzero[1]-1]
        move.append(dummy)
        ar[coorzero[0]][coorzero[1]-1] = 0
        ar[coorzero[0]][coorzero[1]] = dummy
    
    def rezero(num):#target number
        coornum = searchnum(num)
        coorzero = searchnum(0)
        if coornum[0] == len(ar)-1:
            while coorzero[0] < len(ar)-1:
                movezerodown()
                coorzero[0] += 1 #update coorzero
            movezeroup()
            coorzero[0] -= 1
            while coorzero[1] < coornum[1]:
                movezeroright()
                coorzero[1] += 1
            while coorzero[1] > coornum[1]:
                movezeroleft()
                coorzero[1] -= 1
        elif coornum[1] == len(ar)-1 and coornum[0] != len(ar)-1:
            if coorzero[1] == coornum[1] and coorzero[0] < coornum[0]:
                while coorzero[0] < coornum[0]-1:
                    movezerodown()
                    coorzero[0] += 1
                movezerodown()
                movezeroleft()
                movezeroleft()
                movezeroup()
                movezeroright()
                movezerodown()
                movezeroright()
                movezeroup()
                movezeroleft()
                movezeroleft()
                movezerodown()
                movezeroright()
                movezerodown()
                coorzero[0] += 2
                coorzero[1] -= 1
            else:   
                while coorzero[0] < len(ar)-1:
                    movezerodown()
                    coorzero[0] += 1
                while coorzero[0] > coornum[0]+1:
                    movezeroup()
                    coorzero[0] -= 1
                while coorzero[1] < len(ar)-1:
                    movezeroright()
                    coorzero[1] += 1
                movezeroleft()
                coorzero[1] -= 1
        else: 
            if coorzero[0] < coornum[0]:
                while coorzero[1] < len(ar)-1:
                    movezeroright()
                    coorzero[1] += 1
                while coorzero[0] < coornum[0]+1:
                    movezerodown()
                    coorzero[0] += 1
                while coorzero[1] > coornum[1]+1:
                    movezeroleft()
                    coorzero[1] -= 1
            elif coorzero[0] == coornum[0]:
                movezerodown()
                coorzero[0] += 1
                while coorzero[1] < len(ar)-1:
                    movezeroright()
                    coorzero[1] += 1
                while coorzero[1] > coornum[1]+1:
                    movezeroleft()
                    coorzero[1] -= 1    
            else:
                while coorzero[1] < len(ar)-1:
                    movezeroright()
                    coorzero[1] += 1
                while coorzero[0] > coornum[0]+1:
                    movezeroup()
                    coorzero[0] -= 1
                while coorzero[1] > coornum[1]+1:
                    movezeroleft()
                    coorzero[1] -= 1
                
    def movenumup(num):#move target number up
        coornum = searchnum(num)
        rezero(num)
        if coornum[0] == len(ar)-1:
            movezerodown()
        elif coornum[1] == len(ar)-1 and coornum[0] != len(ar)-1:
            movezeroup()
            movezeroup()
            movezeroright()
            movezerodown()
        else:
            movezeroup()
            movezeroup()
            movezeroleft()
            movezerodown()
        
    def movenumdown(num):
        coornum = searchnum(num)
        rezero(num)
        if coornum[0] == len(ar)-1:
            None
        elif coornum[1] == len(ar)-1 and coornum[0] != len(ar)-1:
            movezeroright()
            movezeroup()
        else:
            movezeroleft()
            movezeroup()
    
    def movenumright(num):
        coornum = searchnum(num)
        rezero(num)
        if coornum[0] == len(ar)-1:
            movezeroright()
            movezerodown()
            movezeroleft()
        elif coornum[1] == len(ar)-1 and coornum[0] != len(ar)-1:
            None
        else:
            movezeroup()
            movezeroleft()
    
    def movenumleft(num):
        coornum = searchnum(num)
        rezero(num)
        if coornum[0] == len(ar)-1:
            movezeroleft()
            movezerodown()
            movezeroright()
        elif coornum[1] == len(ar)-1 and coornum[0] != len(ar)-1:
            movezeroup()
            movezeroright()
        else:
            movezeroleft()
            movezeroleft()
            movezeroup()
            movezeroright()
    
    def solvepart1():
        for num in range(1,(len(ar)*(len(ar)-2))+1):
            coornum = searchnum(num)
            x = (num-1)%len(ar) #solution coordinate
            y = (num-1)//len(ar)
            if y == coornum[0] and x == coornum[1]:
                None
            else:
                if num % len(ar) != 0:
                    while coornum[0] < len(ar)-1:
                        movenumdown(num)
                        coornum[0] += 1
                    while coornum[1] < x:
                        movenumright(num)
                        coornum[1] += 1
                    while coornum[1] > x:
                        movenumleft(num)
                        coornum[1] -= 1
                    while coornum[0] > y:
                        movenumup(num)
                        coornum[0] -= 1
                else:
                    if coornum[0] != len(ar)-1:
                        movenumdown(num)
                        coornum[0] += 1
                    while coornum[1] < x-1:
                        movenumright(num)
                        coornum[1] += 1
                    while coornum[1] > x-1:
                        movenumleft(num)
                        coornum[1] -= 1
                    while coornum[0] > y+1:
                        movenumup(num)
                        coornum[0] -= 1
                    coorzero = searchnum(0)
                    while coorzero[1] < len(ar)-1:
                        movezeroright()
                        coorzero[1] += 1
                    while coorzero[0] < len(ar)-1:
                        movezerodown()
                        coorzero[0] += 1
                    while coorzero[1] > x-2:
                        movezeroleft()
                        coorzero[1] -= 1
                    while coorzero[0] > y+1:
                        movezeroup()
                        coorzero[0] -= 1
                    movezeroup()
                    movezeroright()
                    movezerodown()
                    movezeroright()
                    movezeroup()
                    movezeroleft()
                    movezeroleft()
                    movezerodown()
    
    def abctobca():#for 4x4 and larger
        movezeroleft()
        movezeroleft()
        movezeroleft()
        movezeroup()
        movezeroright()
        movezerodown()
        movezeroright()
        movezeroright()
        movezeroup()
        movezeroleft()
        movezeroleft()
        movezeroleft()
        movezerodown()
        movezeroright()
        movezeroright()
        movezeroup()
        movezeroright()
        movezerodown()
        
    def movenumrightup():
        movezeroleft()
        movezeroleft()
        movezeroleft()
        movezeroup()
        movezeroright()
        movezeroright()
        movezeroright()
        movezerodown()
        movezeroleft()
        movezeroup()
        movezeroleft()
        movezeroleft()
        movezerodown()
        movezeroright()
        movezeroright()
        movezeroright()
    
    def solvepart2():
        if len(ar) == 3:
            coorzero = searchnum(0)
            while coorzero[0] < len(ar)-1:
                movezerodown()
                coorzero[0] += 1
            while coorzero[1] < len(ar)-1:
                movezeroright()
                coorzero[1] += 1
            for num in range(4,6):
                coornum = searchnum(num)
                x = (num-1)%len(ar) #solution coordinate
                y = (num-1)//len(ar)
                if y == coornum[0] and x == coornum[1]:
                    None
                else:
                    if coornum[0] == len(ar)-2:
                        while coornum[1] > x:
                            while coorzero[1] > coornum[1]-1:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezeroup()
                            coorzero[0] -= 1
                            while coorzero[1] < (len(ar)-1):
                                movezeroright()
                                coorzero[1] += 1
                            movezerodown()
                            coorzero[0] += 1
                            coornum[1] -= 1
                    else:
                        if coornum[1] == x:
                            movezeroup()
                            while coorzero[1] > coornum[1]:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezerodown()
                            while coorzero[1] < len(ar)-1:
                                movezeroright()
                                coorzero[1] += 1
                        elif coornum[1] > x:
                            movezeroup()
                            while coorzero[1] > coornum[1]:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezerodown()
                            movezeroleft()
                            movezeroup()
                            movezeroright()
                            movezeroright()
                            movezerodown()
                            coorzero[1] += 1
                        else:
                            movezeroleft()
                            movezeroleft()
                            movezeroup()
                            movezeroright()
                            movezerodown()
                            movezeroright()
                            movezeroup()
                            movezeroleft()
                            movezeroleft()
                            movezerodown()
                            movezeroright()
                            movezeroup()
                            movezeroright()
                            movezerodown()       
        elif len(ar) >= 4:
            coorzero = searchnum(0)
            while coorzero[0] < len(ar)-1:
                movezerodown()
                coorzero[0] += 1
            while coorzero[1] < len(ar)-1:
                movezeroright()
                coorzero[1] += 1
            for num in range((len(ar)*(len(ar)-2))+1,(len(ar)*(len(ar)-1))+1):
                coornum = searchnum(num)
                x = (num-1)%len(ar) #solution coordinate
                y = (num-1)//len(ar)
                if y == coornum[0] and x == coornum[1]:
                    None
                else:
                    if coornum[0] == len(ar)-2:
                        while coornum[1] > x:
                            while coorzero[1] > coornum[1]-1:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezeroup()
                            coorzero[0] -= 1
                            while coorzero[1] < (len(ar)-1):
                                movezeroright()
                                coorzero[1] += 1
                            movezerodown()
                            coorzero[0] += 1
                            coornum[1] -= 1
                        while coornum[1] < x:
                            while coorzero[1] > coornum[1]+1:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezeroup()
                            coorzero[0] -= 1
                            movezeroleft()
                            coorzero[1] -= 1
                            movezerodown()
                            coorzero[0] += 1
                            while coorzero[1] < (len(ar)-1):
                                movezeroright()
                                coorzero[1] += 1
                            coornum[1] += 1
                    else:
                        while coornum[1] != len(ar)-2:
                            if coornum[1] == 0:
                                while coorzero[1] > coornum[1]+3:
                                    movezeroleft()
                                    coorzero[1] -= 1
                                abctobca()
                                coornum[1] += 2
                                while coorzero[1] < len(ar)-1:
                                    movezeroright()
                                    coorzero[1] += 1
                            elif coornum[1] == len(ar)-3:
                                while coorzero[1] > coornum[1]+2:
                                    movezeroleft()
                                    coorzero[1] -= 1
                                abctobca()
                                coornum[1] -= 1
                                while coorzero[1] < len(ar)-1:
                                    movezeroright()
                                    coorzero[1] += 1
                            else:
                                while coorzero[1] > coornum[1]+3:
                                    movezeroleft()
                                    coorzero[1] -= 1
                                abctobca()
                                coornum[1] += 2
                                while coorzero[1] < len(ar)-1:
                                    movezeroright()
                                    coorzero[1] += 1
                        movenumrightup()
                        coornum[1] += 1
                        coornum[0] += 1
                        while coornum[1] > x:
                            while coorzero[1] > coornum[1]-1:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezeroup()
                            coorzero[0] -= 1
                            while coorzero[1] < (len(ar)-1):
                                movezeroright()
                                coorzero[1] += 1
                            movezerodown()
                            coorzero[0] += 1
                            coornum[1] -= 1
                        while coornum[1] < x:
                            while coorzero[1] > coornum[1]+1:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezeroup()
                            coorzero[0] -= 1
                            movezeroleft()
                            coorzero[1] -= 1
                            movezerodown()
                            coorzero[0] += 1
                            while coorzero[1] < (len(ar)-1):
                                movezeroright()
                                coorzero[1] += 1
                            coornum[1] += 1
                                                    
    def solvepart3():
        coorzero = searchnum(0)
        if len(ar) == 3:
            movezeroleft()
            movezeroleft()
            movezeroup()
            movezeroright()
            while ar[1][2] != 6:
                movezeroright()
                movezerodown()
                movezeroleft()
                movezeroup()
            movezeroleft()
            movezerodown()
            movezeroright()
            movezeroright()
        elif len(ar) >= 4:
            for num in range((len(ar)*(len(ar)-1))+1,(len(ar)**2-2)):
                coornum = searchnum(num)
                x = (num-1)%len(ar) #solution coordinate
                while x != coornum[1]:
                    if coornum[1] == x+1:
                        while coorzero[1] > coornum[1]+2:
                            movezeroleft()
                            coorzero[1] -= 1
                        abctobca()
                        coornum[1] -= 1
                        while coorzero[1] < len(ar)-1:
                            movezeroright()
                            coorzero[1] += 1
                    else:
                        while coorzero[1] > coornum[1]+1:
                            movezeroleft()
                            coorzero[1] -= 1
                        abctobca()
                        coornum = searchnum(num)
                        while coorzero[1] < len(ar)-1:
                            movezeroright()
                            coorzero[1] += 1
    
    def check():
        if ar[len(ar)-1][len(ar)-2] == len(ar)**2-1:
            return move
        else:
            return None 
    
    solvepart1()
    solvepart2()
    solvepart3()
    
    return check()
  
###############################
def slide_puzzle(ar):
    move = []
    def searchnum(x):
        for j in range(len(ar)):
            for i in range(len(ar)):
                if x == ar[j][i]:
                    return [j,i]
                
    def movezeroup():
        coorzero = searchnum(0)
        dummy = ar[coorzero[0]-1][coorzero[1]]
        move.append(dummy)
        ar[coorzero[0]-1][coorzero[1]] = 0
        ar[coorzero[0]][coorzero[1]] = dummy
    
    def movezerodown():
        coorzero = searchnum(0)
        dummy = ar[coorzero[0]+1][coorzero[1]]
        move.append(dummy)
        ar[coorzero[0]+1][coorzero[1]] = 0
        ar[coorzero[0]][coorzero[1]] = dummy
    
    def movezeroright():
        coorzero = searchnum(0)
        dummy = ar[coorzero[0]][coorzero[1]+1]
        move.append(dummy)
        ar[coorzero[0]][coorzero[1]+1] = 0
        ar[coorzero[0]][coorzero[1]] = dummy
    
    def movezeroleft():
        coorzero = searchnum(0)
        dummy = ar[coorzero[0]][coorzero[1]-1]
        move.append(dummy)
        ar[coorzero[0]][coorzero[1]-1] = 0
        ar[coorzero[0]][coorzero[1]] = dummy
    
    def rezero(num):#target number
        coornum = searchnum(num)
        coorzero = searchnum(0)
        if coornum[0] == len(ar)-1:
            while coorzero[0] < len(ar)-1:
                movezerodown()
                coorzero[0] += 1 #update coorzero
            movezeroup()
            coorzero[0] -= 1
            while coorzero[1] < coornum[1]:
                movezeroright()
                coorzero[1] += 1
            while coorzero[1] > coornum[1]:
                movezeroleft()
                coorzero[1] -= 1
        elif coornum[1] == len(ar)-1 and coornum[0] != len(ar)-1:
            if coorzero[1] == coornum[1] and coorzero[0] < coornum[0]:
                while coorzero[0] < coornum[0]-1:
                    movezerodown()
                    coorzero[0] += 1
                movezerodown()
                movezeroleft()
                movezeroleft()
                movezeroup()
                movezeroright()
                movezerodown()
                movezeroright()
                movezeroup()
                movezeroleft()
                movezeroleft()
                movezerodown()
                movezeroright()
                movezerodown()
                coorzero[0] += 2
                coorzero[1] -= 1
            else:   
                while coorzero[0] < len(ar)-1:
                    movezerodown()
                    coorzero[0] += 1
                while coorzero[0] > coornum[0]+1:
                    movezeroup()
                    coorzero[0] -= 1
                while coorzero[1] < len(ar)-1:
                    movezeroright()
                    coorzero[1] += 1
                movezeroleft()
                coorzero[1] -= 1
        else: 
            if coorzero[0] < coornum[0]:
                while coorzero[1] < len(ar)-1:
                    movezeroright()
                    coorzero[1] += 1
                while coorzero[0] < coornum[0]+1:
                    movezerodown()
                    coorzero[0] += 1
                while coorzero[1] > coornum[1]+1:
                    movezeroleft()
                    coorzero[1] -= 1
            elif coorzero[0] == coornum[0]:
                movezerodown()
                coorzero[0] += 1
                while coorzero[1] < len(ar)-1:
                    movezeroright()
                    coorzero[1] += 1
                while coorzero[1] > coornum[1]+1:
                    movezeroleft()
                    coorzero[1] -= 1    
            else:
                while coorzero[1] < len(ar)-1:
                    movezeroright()
                    coorzero[1] += 1
                while coorzero[0] > coornum[0]+1:
                    movezeroup()
                    coorzero[0] -= 1
                while coorzero[1] > coornum[1]+1:
                    movezeroleft()
                    coorzero[1] -= 1
                
    def movenumup(num):#move target number up
        coornum = searchnum(num)
        rezero(num)
        if coornum[0] == len(ar)-1:
            movezerodown()
        elif coornum[1] == len(ar)-1 and coornum[0] != len(ar)-1:
            movezeroup()
            movezeroup()
            movezeroright()
            movezerodown()
        else:
            movezeroup()
            movezeroup()
            movezeroleft()
            movezerodown()
        
    def movenumdown(num):
        coornum = searchnum(num)
        rezero(num)
        if coornum[0] == len(ar)-1:
            None
        elif coornum[1] == len(ar)-1 and coornum[0] != len(ar)-1:
            movezeroright()
            movezeroup()
        else:
            movezeroleft()
            movezeroup()
    
    def movenumright(num):
        coornum = searchnum(num)
        rezero(num)
        if coornum[0] == len(ar)-1:
            movezeroright()
            movezerodown()
            movezeroleft()
        elif coornum[1] == len(ar)-1 and coornum[0] != len(ar)-1:
            None
        else:
            movezeroup()
            movezeroleft()
    
    def movenumleft(num):
        coornum = searchnum(num)
        rezero(num)
        if coornum[0] == len(ar)-1:
            movezeroleft()
            movezerodown()
            movezeroright()
        elif coornum[1] == len(ar)-1 and coornum[0] != len(ar)-1:
            movezeroup()
            movezeroright()
        else:
            movezeroleft()
            movezeroleft()
            movezeroup()
            movezeroright()
    
    def solvepart1():
        for num in range(1,(len(ar)*(len(ar)-2))+1):
            coornum = searchnum(num)
            x = (num-1)%len(ar) #solution coordinate
            y = (num-1)//len(ar)
            if y == coornum[0] and x == coornum[1]:
                None
            else:
                if num % len(ar) != 0:
                    while coornum[0] < len(ar)-1:
                        movenumdown(num)
                        coornum[0] += 1
                    while coornum[1] < x:
                        movenumright(num)
                        coornum[1] += 1
                    while coornum[1] > x:
                        movenumleft(num)
                        coornum[1] -= 1
                    while coornum[0] > y:
                        movenumup(num)
                        coornum[0] -= 1
                else:
                    if coornum[0] != len(ar)-1:
                        movenumdown(num)
                        coornum[0] += 1
                    while coornum[1] < x-1:
                        movenumright(num)
                        coornum[1] += 1
                    while coornum[1] > x-1:
                        movenumleft(num)
                        coornum[1] -= 1
                    while coornum[0] > y+1:
                        movenumup(num)
                        coornum[0] -= 1
                    coorzero = searchnum(0)
                    while coorzero[1] < len(ar)-1:
                        movezeroright()
                        coorzero[1] += 1
                    while coorzero[0] < len(ar)-1:
                        movezerodown()
                        coorzero[0] += 1
                    while coorzero[1] > x-2:
                        movezeroleft()
                        coorzero[1] -= 1
                    while coorzero[0] > y+1:
                        movezeroup()
                        coorzero[0] -= 1
                    movezeroup()
                    movezeroright()
                    movezerodown()
                    movezeroright()
                    movezeroup()
                    movezeroleft()
                    movezeroleft()
                    movezerodown()
    
    def abctobca():#for 4x4 and larger
        movezeroleft()
        movezeroleft()
        movezeroleft()
        movezeroup()
        movezeroright()
        movezerodown()
        movezeroright()
        movezeroright()
        movezeroup()
        movezeroleft()
        movezeroleft()
        movezeroleft()
        movezerodown()
        movezeroright()
        movezeroright()
        movezeroup()
        movezeroright()
        movezerodown()
        
    def movenumrightup():
        movezeroleft()
        movezeroleft()
        movezeroleft()
        movezeroup()
        movezeroright()
        movezeroright()
        movezeroright()
        movezerodown()
        movezeroleft()
        movezeroup()
        movezeroleft()
        movezeroleft()
        movezerodown()
        movezeroright()
        movezeroright()
        movezeroright()
    
    def solvepart2():
        if len(ar) == 3:
            coorzero = searchnum(0)
            while coorzero[0] < len(ar)-1:
                movezerodown()
                coorzero[0] += 1
            while coorzero[1] < len(ar)-1:
                movezeroright()
                coorzero[1] += 1
            for num in range(4,6):
                coornum = searchnum(num)
                x = (num-1)%len(ar) #solution coordinate
                y = (num-1)//len(ar)
                if y == coornum[0] and x == coornum[1]:
                    None
                else:
                    if coornum[0] == len(ar)-2:
                        while coornum[1] > x:
                            while coorzero[1] > coornum[1]-1:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezeroup()
                            coorzero[0] -= 1
                            while coorzero[1] < (len(ar)-1):
                                movezeroright()
                                coorzero[1] += 1
                            movezerodown()
                            coorzero[0] += 1
                            coornum[1] -= 1
                    else:
                        if coornum[1] == x:
                            movezeroup()
                            while coorzero[1] > coornum[1]:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezerodown()
                            while coorzero[1] < len(ar)-1:
                                movezeroright()
                                coorzero[1] += 1
                        elif coornum[1] > x:
                            movezeroup()
                            while coorzero[1] > coornum[1]:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezerodown()
                            movezeroleft()
                            movezeroup()
                            movezeroright()
                            movezeroright()
                            movezerodown()
                            coorzero[1] += 1
                        else:
                            movezeroleft()
                            movezeroleft()
                            movezeroup()
                            movezeroright()
                            movezerodown()
                            movezeroright()
                            movezeroup()
                            movezeroleft()
                            movezeroleft()
                            movezerodown()
                            movezeroright()
                            movezeroup()
                            movezeroright()
                            movezerodown()       
        elif len(ar) >= 4:
            coorzero = searchnum(0)
            while coorzero[0] < len(ar)-1:
                movezerodown()
                coorzero[0] += 1
            while coorzero[1] < len(ar)-1:
                movezeroright()
                coorzero[1] += 1
            for num in range((len(ar)*(len(ar)-2))+1,(len(ar)*(len(ar)-1))+1):
                coornum = searchnum(num)
                x = (num-1)%len(ar) #solution coordinate
                y = (num-1)//len(ar)
                if y == coornum[0] and x == coornum[1]:
                    None
                else:
                    if coornum[0] == len(ar)-2:
                        while coornum[1] > x:
                            while coorzero[1] > coornum[1]-1:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezeroup()
                            coorzero[0] -= 1
                            while coorzero[1] < (len(ar)-1):
                                movezeroright()
                                coorzero[1] += 1
                            movezerodown()
                            coorzero[0] += 1
                            coornum[1] -= 1
                        while coornum[1] < x:
                            while coorzero[1] > coornum[1]+1:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezeroup()
                            coorzero[0] -= 1
                            movezeroleft()
                            coorzero[1] -= 1
                            movezerodown()
                            coorzero[0] += 1
                            while coorzero[1] < (len(ar)-1):
                                movezeroright()
                                coorzero[1] += 1
                            coornum[1] += 1
                    else:
                        while coornum[1] != len(ar)-2:
                            if coornum[1] == 0:
                                while coorzero[1] > coornum[1]+3:
                                    movezeroleft()
                                    coorzero[1] -= 1
                                abctobca()
                                coornum[1] += 2
                                while coorzero[1] < len(ar)-1:
                                    movezeroright()
                                    coorzero[1] += 1
                            elif coornum[1] == len(ar)-3:
                                while coorzero[1] > coornum[1]+2:
                                    movezeroleft()
                                    coorzero[1] -= 1
                                abctobca()
                                coornum[1] -= 1
                                while coorzero[1] < len(ar)-1:
                                    movezeroright()
                                    coorzero[1] += 1
                            else:
                                while coorzero[1] > coornum[1]+3:
                                    movezeroleft()
                                    coorzero[1] -= 1
                                abctobca()
                                coornum[1] += 2
                                while coorzero[1] < len(ar)-1:
                                    movezeroright()
                                    coorzero[1] += 1
                        movenumrightup()
                        coornum[1] += 1
                        coornum[0] += 1
                        while coornum[1] > x:
                            while coorzero[1] > coornum[1]-1:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezeroup()
                            coorzero[0] -= 1
                            while coorzero[1] < (len(ar)-1):
                                movezeroright()
                                coorzero[1] += 1
                            movezerodown()
                            coorzero[0] += 1
                            coornum[1] -= 1
                        while coornum[1] < x:
                            while coorzero[1] > coornum[1]+1:
                                movezeroleft()
                                coorzero[1] -= 1
                            movezeroup()
                            coorzero[0] -= 1
                            movezeroleft()
                            coorzero[1] -= 1
                            movezerodown()
                            coorzero[0] += 1
                            while coorzero[1] < (len(ar)-1):
                                movezeroright()
                                coorzero[1] += 1
                            coornum[1] += 1
                                                    
    def solvepart3():
        coorzero = searchnum(0)
        if len(ar) == 3:
            movezeroleft()
            movezeroleft()
            movezeroup()
            movezeroright()
            while ar[1][2] != 6:
                movezeroright()
                movezerodown()
                movezeroleft()
                movezeroup()
            movezeroleft()
            movezerodown()
            movezeroright()
            movezeroright()
        elif len(ar) >= 4:
            for num in range((len(ar)*(len(ar)-1))+1,(len(ar)**2-2)):
                coornum = searchnum(num)
                x = (num-1)%len(ar) #solution coordinate
                while x != coornum[1]:
                    if coornum[1] == x+1:
                        while coorzero[1] > coornum[1]+2:
                            movezeroleft()
                            coorzero[1] -= 1
                        abctobca()
                        coornum[1] -= 1
                        while coorzero[1] < len(ar)-1:
                            movezeroright()
                            coorzero[1] += 1
                    else:
                        while coorzero[1] > coornum[1]+1:
                            movezeroleft()
                            coorzero[1] -= 1
                        abctobca()
                        coornum = searchnum(num)
                        while coorzero[1] < len(ar)-1:
                            movezeroright()
                            coorzero[1] += 1
    
    def check():
        if ar[len(ar)-1][len(ar)-2] == len(ar)**2-1:
            return move
        else:
            return None 
    
    solvepart1()
    solvepart2()
    solvepart3()
    
    return check()
  
##################################
import numpy as np
import queue


def compare(a, b):
    if a == b:
        return 0
    if a > b:
        return 1
    if a < b:
        return -1


class Puzzle:
    def __init__(self, puzzle):
        self.puzzle = np.array(puzzle, dtype=np.object)
        self.solved = np.zeros_like(self.puzzle, dtype=int)
        self.height, self.width = self.puzzle.shape
        self.steps = []


        for i, row in enumerate(self.puzzle):
            for j, value in enumerate(row):
                self.puzzle[i, j] = Case(value)
                self.puzzle[i, j].y, self.puzzle[i, j].x = i, j
                self.solved[i, j] = 1 + j + self.width*i
        self.solved[-1, -1] = 0


        for row in self.puzzle:
            [case.get_paths(self.puzzle) for case in row]

    def clear(self):
        [case.clear() for case in np.ravel(self.puzzle)]

    def find_number(self, n):
        for row in self.puzzle:
            for node in row:
                if node.value == n:
                    return node
        return None

    def solve_number(self, destination, number, ignore=None, solve=True):
        while destination.value != number:

            hole = self.find_number(0)

            goto = self.find_number(number)

            adjacent = goto.best_adjacent(self.puzzle, relative_to=destination)

            path = hole.astar(self, adjacent, goto, ignore)

            for one, two in zip(path, path[1:]):
                self.steps.append(two.value)
                one.swap(two)
            else:
                self.steps.append(goto.value)
                path[-1].swap(goto)

        if solve:
            destination.solved = True
        return True

    def solve_line(self, line, solutions, helper_cases):

        for case, solution in zip(line[:-2], solutions[:-2]):
            self.solve_number(case, solution)


        self.solve_number(helper_cases[2], solutions[-1], solve=False)
        self.solve_number(helper_cases[3], solutions[-2], solve=False)

        self.solve_number(line[-1], solutions[-2], solve=False)
        self.solve_number(helper_cases[0], solutions[-1], solve=False)

        if line[-2] != self.find_number(0):
            self.solve_number(helper_cases[1], line[-2].value,
                              ignore=[helper_cases[0], line[-1]], solve=False)

        self.solve_number(line[-2], solutions[-2])
        self.solve_number(line[-1], solutions[-1])

        return True

    def smol_solve(self):
        smallest = 2

        for i in range(self.height-smallest):
            helper_cases = (self.puzzle[i+1, -1], self.puzzle[i+1, -2],
                            self.puzzle[i+2, -1], self.puzzle[i+2, -2])
            self.solve_line(self.puzzle[i, :], self.solved[i, :], helper_cases)
            helper_cases = (self.puzzle[-1, i+1], self.puzzle[-2, i+1],
                            self.puzzle[-1, i+2], self.puzzle[-2, i+2])
            self.solve_line(self.puzzle[i+1:, i], self.solved[i+1:, i], helper_cases)

        return True

    def final_solve(self, fragment, solution):


        for i in range(24):
            solution = self.puzzle[-3:, -3:].ravel().tolist()[:-1]
            solution = [s.value for s in solution]
            if sorted(solution) == solution:

                return True

            hole = self.find_number(0)
            if i < 12:

                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -2]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -1]
            if i >= 12:
                # 3 loops one way, 3 loops the other one
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -1]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -2]
            self.steps.append(guy.value)
            hole.swap(guy)

        self.steps = None

    def solve(self):

        self.smol_solve()

        self.final_solve(self.puzzle[-3:, -3:].ravel().tolist(),
                         self.solved[-3:, -3:].ravel().tolist())
        print(self.puzzle)


class Case:
    def __init__(self, value):
        self.value = value
        self.solved = False
        self.paths = []
        self.distance = np.Infinity
        self.back = None

    def __gt__(self, other):
        return self.distance > other.distance

    def __repr__(self):
        return str(self.value)

    @property
    def info(self):
        return f'Case w/ value {self.value} at ({self.y}, {self.x}).'

    def clear(self):
        self.distance = np.Infinity
        self.back = None

    def swap(self, other):
        self.value, other.value = other.value, self.value
        self.solved, other.solved = other.solved, self.solved

    def get_paths(self, puzzle):
        height, width = puzzle.shape
        if self.y > 0:
            self.paths.append(puzzle[self.y-1, self.x])
        if self.y < height-1:
            self.paths.append(puzzle[self.y+1, self.x])
        if self.x > 0:
            self.paths.append(puzzle[self.y, self.x-1])
        if self.x < width-1:
            self.paths.append(puzzle[self.y, self.x+1])

    def best_adjacent(self, puzzle, relative_to):

        possible_paths = []
        for path in self.paths:
            if not path.solved:

                possible_paths.append((relative_to.distance_to(path), path))

        if not possible_paths:

            print(f'Could not find any good adjacent cases for {self.y}, {self.x}')
            for path in self.paths:
                print(f'({path.y}, {path.x}), solved = {path.solved}')
            print(puzzle.puzzle)

        solution = sorted(possible_paths, key=lambda x: x[0])[0]

        return solution[1]

    def dijkstra(self, puzzle, destination, number, ignore=None):
        '''A* is way more efficient on big maps! Use it instead'''

        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore:
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance, posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def astar(self, puzzle, destination, number, ignore=None):

        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            if case == destination:
                break
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore:
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance_to(destination), posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def distance_to(self, other):
        return abs(self.y-other.y)+abs(self.x-other.x)


def slide_puzzle(array):
    puzzle = Puzzle(array)
    puzzle.solve()
    return puzzle.steps



array = [
        [4, 1, 3],
        [2, 8, 0],
        [7, 6, 5],
        ]

print(slide_puzzle(array))
_________________________________________
import numpy as np
import queue


def compare(a, b):
    if a == b:
        return 0
    if a > b:
        return 1
    if a < b:
        return -1


class Puzzle:
    def __init__(self, puzzle):
        self.puzzle = np.array(puzzle, dtype=np.object)
        self.solved = np.zeros_like(self.puzzle, dtype=int)
        self.height, self.width = self.puzzle.shape
        self.steps = []

        for i, row in enumerate(self.puzzle):
            for j, value in enumerate(row):
                self.puzzle[i, j] = Case(value)
                self.puzzle[i, j].y, self.puzzle[i, j].x = i, j
                self.solved[i, j] = 1 + j + self.width*i
        self.solved[-1, -1] = 0

        for row in self.puzzle:
            [case.get_paths(self.puzzle) for case in row]

    def clear(self):
        [case.clear() for case in np.ravel(self.puzzle)]

    def find_number(self, n):
        for row in self.puzzle:
            for node in row:
                if node.value == n:
                    return node
        return None

    def solve_number(self, destination, number, ignore=None, solve=True):
        while destination.value != number:

            hole = self.find_number(0)
            goto = self.find_number(number)
            adjacent = goto.best_adjacent(self.puzzle, relative_to=destination)
            path = hole.astar(self, adjacent, goto, ignore)
            for one, two in zip(path, path[1:]):
                self.steps.append(two.value)
                one.swap(two)
            else:
                self.steps.append(goto.value)
                path[-1].swap(goto)

        if solve:
            destination.solved = True
        return True

    def solve_line(self, line, solutions, helper_cases):
        for case, solution in zip(line[:-2], solutions[:-2]):
            self.solve_number(case, solution)
        self.solve_number(helper_cases[2], solutions[-1], solve=False)
        self.solve_number(helper_cases[3], solutions[-2], solve=False)

        self.solve_number(line[-1], solutions[-2], solve=False)
        self.solve_number(helper_cases[0], solutions[-1], solve=False)

        if line[-2] != self.find_number(0):
            self.solve_number(helper_cases[1], line[-2].value,
                              ignore=[helper_cases[0], line[-1]], solve=False)

        self.solve_number(line[-2], solutions[-2])
        self.solve_number(line[-1], solutions[-1])

        return True

    def smol_solve(self):
        smallest = 2

        for i in range(self.height-smallest):
            helper_cases = (self.puzzle[i+1, -1], self.puzzle[i+1, -2],
                            self.puzzle[i+2, -1], self.puzzle[i+2, -2])
            self.solve_line(self.puzzle[i, :], self.solved[i, :], helper_cases)
            helper_cases = (self.puzzle[-1, i+1], self.puzzle[-2, i+1],
                            self.puzzle[-1, i+2], self.puzzle[-2, i+2])
            self.solve_line(self.puzzle[i+1:, i], self.solved[i+1:, i], helper_cases)

        return True

    def final_solve(self, fragment, solution):

        for i in range(24):
            solution = self.puzzle[-3:, -3:].ravel().tolist()[:-1]
            solution = [s.value for s in solution]
            if sorted(solution) == solution:
                return True

            hole = self.find_number(0)
            if i < 12:
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -2]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -1]
            if i >= 12:
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -1]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -2]
            self.steps.append(guy.value)
            hole.swap(guy)
        self.steps = None

    def solve(self):
        self.smol_solve()
        self.final_solve(self.puzzle[-3:, -3:].ravel().tolist(),
                         self.solved[-3:, -3:].ravel().tolist())
        print(self.puzzle)


class Case:
    def __init__(self, value):
        self.value = value
        self.solved = False
        self.paths = []
        self.distance = np.Infinity
        self.back = None

    def __gt__(self, other):
        return self.distance > other.distance

    def __repr__(self):
        return str(self.value)

    @property
    def info(self):
        return f'Case w/ value {self.value} at ({self.y}, {self.x}).'

    def clear(self):
        self.distance = np.Infinity
        self.back = None

    def swap(self, other):
        self.value, other.value = other.value, self.value
        self.solved, other.solved = other.solved, self.solved

    def get_paths(self, puzzle):
        height, width = puzzle.shape
        if self.y > 0:
            self.paths.append(puzzle[self.y-1, self.x])
        if self.y < height-1:
            self.paths.append(puzzle[self.y+1, self.x])
        if self.x > 0:
            self.paths.append(puzzle[self.y, self.x-1])
        if self.x < width-1:
            self.paths.append(puzzle[self.y, self.x+1])

    def best_adjacent(self, puzzle, relative_to):
        possible_paths = []
        for path in self.paths:
            if not path.solved:

                possible_paths.append((relative_to.distance_to(path), path))

        if not possible_paths:
            print(f'Could not find any good adjacent cases for {self.y}, {self.x}')
            for path in self.paths:
                print(f'({path.y}, {path.x}), solved = {path.solved}')
            print(puzzle.puzzle)

        solution = sorted(possible_paths, key=lambda x: x[0])[0]

        return solution[1]

    def dijkstra(self, puzzle, destination, number, ignore=None):
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore:
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance, posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def astar(self, puzzle, destination, number, ignore=None):
        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            if case == destination:
                break
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore: 
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance_to(destination), posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def distance_to(self, other):
        return abs(self.y-other.y)+abs(self.x-other.x)


def slide_puzzle(array):
    puzzle = Puzzle(array)
    puzzle.solve()
    return puzzle.steps

array = [
        [4, 1, 3],
        [2, 8, 0],
        [7, 6, 5],
        ]

print(slide_puzzle(array))
