5a479247e6be385a41000064


class Nonogram:

    def __init__ (self, clues):
        self._clues = clues
        pass

    def get_col (self, c, solution):
        row = [x[c] for x in solution]
        return row

    def test_row (self, row, clue):
        result = []
        seq_cnt = 0
        for val in row:
            if val == 1:
                seq_cnt += 1
            else:
                if seq_cnt > 0:
                    result += [seq_cnt]
                seq_cnt = 0
        if seq_cnt > 0:
            result += [seq_cnt]
        return (list(clue) == result)

    def generate_sols (self, row, clue):
        row_sols = [[]]
        for val in row:
            if val == -1:
                for i in range (len(row_sols)):
                    row_sols += [row_sols[i] + [1]]
                    row_sols[i] += [0]
            else:
                for i in range(len(row_sols)):
                    row_sols[i] += [val]

        valid_sols = []
        for sol in row_sols:
            if self.test_row (sol, clue):
                valid_sols += [sol]
        return valid_sols


    def solve (self):
        W = len (self._clues[0])
        H = len (self._clues[1])
        solution = [[-1]*W for x in range(H)]

        while any (-1 in x for x in solution):
            for c,clue in enumerate(self._clues[0]):
                row = self.get_col(c, solution)
                row_sols = self.generate_sols(row, clue)
                for i in range (len(row)):
                    if row[i] == -1:
                        cell_options = [sol[i] for sol in row_sols]
                        if len(set(cell_options)) == 1:
                            solution[i][c] = cell_options[0]

            for r,clue in enumerate (self._clues[1]):
                row = solution[r]
                row_sols = self.generate_sols(row, clue)
                for i in range (len(row)):
                    if row[i] == -1:
                        cell_options = [sol[i] for sol in row_sols]
                        if len(set(cell_options)) == 1:
                            solution[r][i] = cell_options[0]

        return tuple (tuple(row) for row in solution)

clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),
         ((1,), (2,), (3,), (2, 1), (4,)))

ans = ((0, 0, 1, 0, 0),
       (1, 1, 0, 0, 0),
       (0, 1, 1, 1, 0),
       (1, 1, 0, 1, 0),
       (0, 1, 1, 1, 1))

print (Nonogram(clues).solve() == ans)

clues = (((1,), (3,), (1,), (3, 1), (3, 1)),
         ((3,), (2,), (2, 2), (1,), (1, 2)))

ans = ((0, 0, 1, 1, 1),
       (0, 0, 0, 1, 1),
       (1, 1, 0, 1, 1),
       (0, 1, 0, 0, 0),
       (0, 1, 0, 1, 1))

print (Nonogram(clues).solve() == ans)

clues = (((3,), (2,), (1, 1), (2,), (4,)),
         ((2,), (3, 1), (1, 2), (3,), (1,)))

ans = ((1, 1, 0, 0, 0),
       (1, 1, 1, 0, 1),
       (1, 0, 0, 1, 1),
       (0, 0, 1, 1, 1),
       (0, 0, 0, 0, 1))

print (Nonogram(clues).solve() == ans)
########################################################
import itertools
class Nonogram:
    poss = {(1,1,1): set([(1,0,1,0,1)]),
            (1,1):   set([(0,0,1,0,1),(0,1,0,1,0),(1,0,1,0,0),(0,1,0,0,1),(1,0,0,1,0),(1,0,0,0,1)]),
            (1,2):   set([(1,0,1,1,0),(1,0,0,1,1),(0,1,0,1,1)]),
            (1,3):   set([(1,0,1,1,1)]),
            (2,1):   set([(1,1,0,1,0),(1,1,0,0,1),(0,1,1,0,1)]),
            (2,2):   set([(1,1,0,1,1)]),
            (3,1):   set([(1,1,1,0,1)]),
            (1,):    set([(0,0,0,0,1),(0,0,0,1,0),(0,0,1,0,0),(0,1,0,0,0),(1,0,0,0,0)]),
            (2,):    set([(0,0,0,1,1),(0,0,1,1,0),(0,1,1,0,0),(1,1,0,0,0)]),
            (3,):    set([(0,0,1,1,1),(0,1,1,1,0),(1,1,1,0,0)]),
            (4,):    set([(0,1,1,1,1),(1,1,1,1,0)]),
            (5,):    set([(1,1,1,1,1)])}
    
    def __init__(self, clues):
        self.h,self.w=(tuple(Nonogram.poss[clue] for clue in side) for side in clues)

    def solve(self):
        for r in itertools.product(*self.w):
            if all(c in self.h[i] for i,c in enumerate(zip(*r))): return r
###########################################################################################
from itertools import groupby, product

class Nonogram:
    def __init__(self, clues):
        self.clues = clues
    def solve(self):
        for p in product(
            *[[p for p in product(range(2),repeat=5)
            if sum(p)==sum(t) and tuple(len(list(g)) for k,g in groupby(p) if k) == t]
            for t in self.clues[1]]
        ):
            if all(tuple(len(list(g)) for k,g in groupby(p) if k) == t 
                for p, t in zip([v for v in zip(*p)], self.clues[0])):
                return p
##########################
from itertools import product

class Nonogram:
    
    POS = {(2,2):   ((1,1,0,1,1),),
           (5,):    ((1,1,1,1,1),),
           (1,1,1): ((1,0,1,0,1),),
           (1,3):   ((1,0,1,1,1),),
           (3,1):   ((1,1,1,0,1),),
           (4,):    ((1,1,1,1,0), (0,1,1,1,1)),
           (1,2):   ((1,0,0,1,1), (1,0,1,1,0), (0,1,0,1,1)),
           (2,1):   ((1,1,0,0,1), (1,1,0,1,0), (0,1,1,0,1)),
           (3,):    ((1,1,1,0,0), (0,1,1,1,0), (0,0,1,1,1)),
           (2,):    ((1,1,0,0,0), (0,1,1,0,0), (0,0,1,1,0), (0,0,0,1,1)),
           (1,):    ((1,0,0,0,0), (0,1,0,0,0), (0,0,1,0,0), (0,0,0,1,0), (0,0,0,0,1)),
           (1,1):   ((1,0,1,0,0), (1,0,0,1,0), (1,0,0,0,1), (0,1,0,1,0), (0,1,0,0,1), (0,0,1,0,1))}

    def __init__(self, clues):
        self.clues = clues

    def solve(self):
        for p in product(*( self.POS[c] for c in self.clues[0] )):
            board = list(zip(*p))
            for z in range(5):
                if board[z] not in self.POS[self.clues[1][z]]: break
            else:
                return tuple(tuple(l) for l in board)
##################################
from copy import deepcopy

class Nonogram:
    
    POS = {(2,2):   ((1,1,0,1,1),),
           (5,):    ((1,1,1,1,1),),
           (1,1,1): ((1,0,1,0,1),),
           (1,3):   ((1,0,1,1,1),),
           (3,1):   ((1,1,1,0,1),),
           (4,):    ((1,1,1,1,0), (0,1,1,1,1)),
           (1,2):   ((1,0,0,1,1), (1,0,1,1,0), (0,1,0,1,1)),
           (2,1):   ((1,1,0,0,1), (1,1,0,1,0), (0,1,1,0,1)),
           (3,):    ((1,1,1,0,0), (0,1,1,1,0), (0,0,1,1,1)),
           (2,):    ((1,1,0,0,0), (0,1,1,0,0), (0,0,1,1,0), (0,0,0,1,1)),
           (1,):    ((1,0,0,0,0), (0,1,0,0,0), (0,0,1,0,0), (0,0,0,1,0), (0,0,0,0,1)),
           (1,1):   ((1,0,1,0,0), (1,0,0,1,0), (1,0,0,0,1), (0,1,0,1,0), (0,1,0,0,1), (0,0,1,0,1))}
    
    def __init__(self, clues): self.clues = {'V': clues[0], 'H': clues[1]}
    
    
    def solve(self):
        grid = { (d,z): list(self.POS[ self.clues[d][z] ]) for d in 'VH' for z in range(5)}
        
        changed = True
        while changed:
            changed = False
            
            for x in range(5):
                for y in range(5):
                
                    tupH, iH, tupV, iV = ('H',x), y, ('V',y), x
                    if len(grid[tupH]) == 1 and len(grid[tupV]) == 1: continue
                    
                    vH = { v[iH] for v in grid[tupH] }
                    vV = { v[iV] for v in grid[tupV] }
                    target = vH & vV
                    
                    if len(vH) == 2 and len(target) == 1:
                        changed = True
                        grid[tupH] = [t for t in grid[tupH] if t[iH] in target]
                        
                    if len(vV) == 2 and len(target) == 1:
                        changed = True
                        grid[tupV] = [t for t in grid[tupV] if t[iV] in target]
        
        return tuple( grid[('H',n)][0] for n in range(5) )
##################################################################
import re
import numpy as np

class Nonogram:
    def __init__(self, clues):
        self.clues = clues
        self.possible_rows, self.possible_cols = \
            [[self.possible_cells(len(clues[i]), c) for c in clues[1 - i]] for i in range(2)]

    def possible_cells(self, n, clues):
        if clues == () or clues == (0,):
            return ['0' * n]
        min_width = sum(clues) + len(clues) - 1
        assert min_width <= n
        if len(clues) == 1:
            return [('0' * i + '1' * clues[0]).ljust(n, '0') for i in range(n - clues[0] + 1)]
        res = []
        for i in range(0, n - min_width + 1):
            start = '0' * i + '1' * clues[0] + '0'
            res += [start + p for p in self.possible_cells(n - len(start), clues[1:])]
        return res

    def solve(self):
        w, h = len(self.possible_cols), len(self.possible_rows)
        old_grid, grid = None, '\n'.join(['.' * w] * h)
        while old_grid != grid and grid.find('.') != -1:
            old_grid = grid
            grid = ''.join(self.update_cells(row, p) for row, p in
                           zip(grid.split('\n'), self.possible_rows))
            grid = ''.join(self.update_cells(col, p) for col, p in
                           zip((grid[i:: w] for i in range(w)), self.possible_cols))
            grid = '\n'.join(grid[row:: h] for row in range(h))
        return tuple(tuple(-1 if c == '.' else int(c) for c in r) for r in grid.split('\n'))

    @staticmethod
    def update_cells(cells, possibilities):
        if cells.find('.') == -1:
            return cells
        not_matches = [i for i, answer in enumerate(possibilities) if not re.match(cells, answer)]
        for i in not_matches[:: -1]:
            possibilities.pop(i)
        assert len(possibilities) != 0
        if len(possibilities) == 1:
            return possibilities[0]
        n, stack = len(cells), ''.join(possibilities)
        vote = (set(stack[i:: n]) for i in range(0, n))
        return ''.join(s.pop() if len(s) == 1 else '.' for s in vote)
###########################################################################
from itertools import combinations, product

class Nonogram:

    def __init__(self, clues):
        self.clues = clues
        
    def match_clue(self, clue, my_list):#checks if a list matches a clue
        return clue == tuple(len(str) for str in ''.join([str(i) for i in my_list]).split('0') if str!='')

    def solve(self):#based on row clues builds all possible boards and checks which one matches column clues.
        possible_rows = [[tuple(1 if i in comb else 0 for i in range(5)) for comb in combinations(range(5), sum(clue)) if self.match_clue(clue, [1 if i in comb else 0 for i in range(5)])] for clue in self.clues[1]]
        for board in product(*possible_rows):
            if all([self.match_clue(self.clues[0][i], [row[i] for row in board]) for i in range(5)]): return board
###################################################################
import copy
import itertools


class Cell:
    def __init__(self, val: int):
        self.val = val

    def set_cell(self, v):
        self.val = v


class Line:
    def __init__(self, cells: list, clues: tuple, possibilities: list):
        self.cells = cells
        self.clues = list(clues)
        self.possibilities = copy.copy(possibilities)

    def set_possibilities(self, v):
        self.possibilities = v


class Board:
    def __init__(self, clues, width, height):
        hper = []
        vper = []
        self.cells = {}
        self.hlines = []
        self.vlines = []
        self.width = width
        self.height = height
        for i in range(0, height + 1):
            per = ([False for _ in range(0, i)])
            per.extend(([True for _ in range(0, height - i)]))
            hper.extend(list(set(itertools.permutations(per))))
        if width == height:
            vper = hper
        else:
            for i in range(0, width + 1):
                per = [False for _ in range(0, i)]
                per.extend([True for _ in range(0, width - i)])
                vper.append(list(set(itertools.permutations(per))))
        for i in range(0, height):
            for j in range(0, width):
                self.cells[(i, j)] = Cell(-1)

        for i in range(0, width):
            self.vlines.append(Line([self.cells[(j, i)] for j in range(0, height)], clues[0][i], vper))

        for i in range(0, height):
            self.hlines.append(Line([self.cells[(i, j)] for j in range(0, width)], clues[1][i], hper))

    def solve(self):
        while any(cell.val == -1 for cell in self.cells.values()):
            for line in self.hlines:
                Board.resolve(line, self.width)
            for line in self.vlines:
                Board.resolve(line, self.height)

        ret = []
        for i in range(0, self.height):
            line = []
            for j in range(0, self.width):
                line.append(self.cells[(i, j)].val)
            ret.append(tuple(line))
        return tuple(ret)

    @staticmethod
    def resolve(line: Line, side: int):
        def check(per):
            index = 0
            for clue in line.clues:
                try:
                    index = per.index(True, index)
                except ValueError:
                    return False

                while index != len(per) and per[index]:
                    index += 1
                    clue -= 1
                if clue != 0:
                    return False
            try:
                per.index(1, index)
            except ValueError:
                pass
            else:
                return False
            for i in range(0, side):
                cell = line.cells[i].val
                if cell != -1 and cell != per[i]:
                    return False
            return True

        checked = list(filter(check, line.possibilities))
        for i in range(0, side):
            if line.cells[i].val != -1:
                continue
            s = 0
            for x in checked:
                if x[i] is True:
                    s += 1
            line.cells[i].set_cell(0 if s == 0 else (1 if s == len(checked) else -1))
        line.set_possibilities(checked)
        
class Nonogram:

    def __init__(self, clues):
        self.board = Board(clues, 5, 5)

    def solve(self):
        return self.board.solve()
##########################################################
class Nonogram:

    def __init__(self, clues):
        self.col = [list(c) for c in clues[0]]
        self.row = [list(r) for r in clues[1]]

    def solve(self):
        N = 5

        def valid(a, i, j):
            r, c = [], []
            if a[i][0] == 1:
                r.append(1)
            for jj in range(1, j + 1):
                if a[i][jj] == 1:
                    if a[i][jj - 1] == 1:
                        r[-1] += 1
                    else:
                        r.append(1)
            if a[0][j] == 1:
                c.append(1)
            for ii in range(1, i + 1):
                if a[ii][j] == 1:
                    if a[ii - 1][j] == 1:
                        c[-1] += 1
                    else:
                        c.append(1)
            if len(r) > len(self.row[i]) or len(c) > len(self.col[j]):
                return False
            if r and (any(r[k] != self.row[i][k] for k in range(len(r) - 1)) or r[-1] > self.row[i][len(r) - 1]):
                return False
            if c and (any(c[k] != self.col[j][k] for k in range(len(c) - 1)) or c[-1] > self.col[j][len(c) - 1]):
                return False
            return True

        def valid_row(a, i):
            r = []
            if a[i][0] == 1:
                r.append(1)
            for jj in range(1, N):
                if a[i][jj] == 1:
                    if a[i][jj - 1] == 1:
                        r[-1] += 1
                    else:
                        r.append(1)
            return r == self.row[i]

        def backtrack(a, i, j):
            if i == N:
                return tuple(tuple(r) for r in a)
            if j == N:
                if valid_row(a, i):
                    return backtrack(a, i + 1, 0)
                return None
            a[i][j] = 1
            if valid(a, i, j):
                ans = backtrack(a, i, j + 1)
                if ans is not None:
                    return ans
            a[i][j] = 0
            if not valid(a, i, j):
                return None
            ans = backtrack(a, i, j + 1)
            if ans is not None:
                return ans
            return None

        return backtrack([[0 for j in range(N)] for i in range(N)], 0, 0)
####################################################################################
import numpy as np
import sys
class Nonogram:

    def __init__(self, clues):
        self.width = 5
        self.colClues = clues[0]
        self.rowClues = clues[1]
        self.Board = np.ones((self.width,self.width),dtype=int)*(-1)

    def solve(self):
        # for a clue
        #   evaluate the column/row that it refers to
        for i in range(self.width):
            if np.any(self.Board[i,:] < 0):
                self.Board[i,:] = self.evalSolution(self.rowClues[i], self.Board[i,:])

            if np.any(self.Board[:,i] < 0):
                self.Board[:,i] = self.evalSolution(self.colClues[i], self.Board[:,i])
        self.cleanBrd()
        
        array_of_tuples = map(tuple, self.Board)
        return tuple(array_of_tuples)
    
    def evalSolution(self, clue, brd):
        #print(clue, sum(clue) + (len(clue) -1) , self.width)
        
        if sum(clue) + (len(clue) -1) == self.width:   # unique solution
            return self.buildAnswer(clue)
        elif sum(clue) + (len(clue) -1) == self.width - 1:  # 1 extra space            
            xtraSpace = 1
            baseAns = self.buildAnswer(clue)  # answer for width - 1
            #print('clue', clue, baseAns)
            ansLst = self.buildAnswerList(xtraSpace, baseAns, brd)
            if len(ansLst) > 0: 
                newBrd = self.buildBrdFromList(ansLst, brd)
                brd = newBrd
        elif sum(clue) + (len(clue) -1) == self.width - 2:  # 2 extra spaces
            xtraSpace = 2
            baseAns = self.buildAnswer(clue)  # answer for width - 2
            # print(clue, brd, '\n',baseAns)
            tmpLst = self.buildAnswerList(xtraSpace, baseAns, brd)
            # print(clue, brd, '\n',tmpLst)
            
            ansLst = []
            for lst in tmpLst:
                ansLst.extend(self.addAnotherSpace(lst))
            # print('\n',ansLst)
            
            if len(ansLst) > 0: 
                newBrd = self.buildBrdFromList(ansLst, brd)
                brd = newBrd
            

            #sys.exit()
        return brd
    
    def addAnotherSpace(self, lst):
        #print(lst)
        wLst = lst.tolist()
        tLst = []
                    # No leading zero, we insert and add to tLst
        if lst[0] != 0:
            tLst.append([0] + wLst) 
                    # No trailing zero, we insert and add to tLst
        if lst[-1] != 0:
            tLst.append(wLst + [0])  

        for idx, val in enumerate(lst):
                    # for existing zeros, insert aother at idx and add to tLst
            if val == 0:  
                x = wLst.copy()
                x.insert(idx,0)
                tLst.append(x)
        return tLst  
        
    def buildAnswer(self, clue):
        ans = []
        for cl in clue:
            for i in range(cl):
                ans.append(1)
            ans.append(0)
        return ans[:-1]
    
    def buildAnswerList(self, xSpace, baseAns, brd):
        baseAnsCpy = baseAns.copy()
        newLst = baseAns.copy()
        newLst.insert(0,0)
        ansLst = np.array(newLst)

        for idx, val in enumerate(baseAnsCpy):
            if val == 0:
                newLst = baseAns.copy()
                newLst.insert(idx,0)
                ansLst = np.vstack([ansLst, newLst])

        newLst = baseAns.copy()
        newLst.append(0)
        ansLst = np.vstack([ansLst, newLst])  

        if len(brd) == len(ansLst[0]):
            for i in range(len(brd)):
                if brd[i] != -1:
                    ansLst = np.delete(ansLst,np.where((ansLst[:,i]!= brd[i]))[0], axis = 0).copy()

        return ansLst
    
    def buildBrdFromList(self,ansLst, brd):
        # create one array to compare against brd
        #        
        nLst = np.array(ansLst)
        
        x = nLst.sum(axis = 0)
        x = np.where( (x > 0 ) & (x<len(nLst)), -1, x)
        tst = np.where( (x > 0 ), 1, x)

        for i in range(self.width):
            if tst[i] != -1 and tst[i] != brd[i]:
                brd[i] = tst[i]

        return brd

    def cleanBrd(self):
        count = np.count_nonzero(self.Board < 0)
        improvement = count
        while count > 0 and improvement > 0:
            print(count, improvement, '\n', self.Board)
            for i in range(self.width):
                self.Board[i,:] = self.checkArr(self.Board[i,:],self.rowClues[i])
                self.Board[:,i] = self.checkArr(self.Board[:,i],self.colClues[i])    
            
            improvement = count - np.count_nonzero(self.Board < 0)              
            count = np.count_nonzero(self.Board < 0)


                 
    def checkArr(self, arr, clues):
        if np.count_nonzero(arr<0)  == 0: return arr

        arr = self.chkFirst(arr, clues[0])
        arr = self.chkLast(arr, clues[-1])

        setPrt = False

        arr = self.chkBrdWithClue(arr, clues)
        return arr

    def chkBrdWithClue(self, nLst, cl):
        lenLst = len(nLst)
        numClues = len(cl)
        sumClues = sum(cl)
        maxClues = max(cl)
        minClues = min(cl)
        numOnes = np.count_nonzero(nLst>0)
        numMinuses = np.count_nonzero(nLst<0)
        numZeros = np.count_nonzero(nLst == 0)
        if numOnes == sumClues:
            nLst = np.where(nLst < 0, 0, nLst)
            return nLst
        if numOnes == sumClues - 1 and numMinuses == 1:
            nLst = np.where(nLst < 0, 1, nLst)
            return nLst
        if numOnes == sumClues - 2 and numMinuses == 2:
            nLst = np.where(nLst < 0, 1, nLst) 
            return nLst
        if numClues == 1 and numOnes == 1:
            idx1 = np.argmax(nLst == 1)      
            lowIdx = max(0,idx1 - sumClues)
            hiIdx = min(idx1 + sumClues - 1, lenLst)
            for i in range(lenLst):
                if nLst[i] == -1 and not lowIdx <= i <= hiIdx:
                    nLst[i] = 0
            return nLst        
        if numClues == 1 and numOnes == 2:
            idx1 = np.where(nLst == 1)[0]
            lowIdx = max(0,max(idx1) - sumClues)
            hiIdx = min(min(idx1) + sumClues - 1, lenLst)
            for i in range(lenLst):
                if nLst[i] == -1 and not lowIdx <= i <= hiIdx:
                    nLst[i] = 0
            return nLst  
        if maxClues == 1 and numOnes > 0:
            idx1 = np.where(nLst == 1)[0]
            for i in idx1:
                if i - 1 >= 0 and nLst[i-1] != 0:
                    nLst[i-1] = 0
                if i != lenLst - 1 and nLst[i+1] != 0:
                    nLst[i+1] = 0
            return nLst 
        return nLst
    
    def chkFirst(self, arr, cl):
        if len(arr) == 1:
            if cl==1:
                arr[0] = 1
            return arr
        if arr[0] == 1:
            for i in range(cl):
                arr[i] = 1
            if len(arr) > cl: arr[cl] = 0
            return arr
        if arr[0] == 0:
            return np.concatenate((np.array([0]), self.chkFirst(arr[1:], cl) ))
        if arr[0] == -1:
            if arr[1] == 0:
                if cl == 1:
                    return arr
                else:  #   cl > 1:
                    arr[0] = 0
                    return np.concatenate((np.array([0,0]), self.chkFirst(arr[2:], cl) ))
            elif arr[1] == 1:
                if cl == 1:
                    arr[0] = 0
                    if len(arr) > 2: arr[2] = 0
                    return arr
                elif cl > 1:
                    if len(arr) > 2 and arr[2] == 0:
                        arr[0] = 1
                        return arr
                    elif len(arr) > 2 and arr[2] == -1:
                        return arr
                    else:  # arr[0] = -1, arr[1] = 1 arr[2] = 1    
                        if cl == 2:
                            arr[0] = 0
                            if len(arr) > 3: arr[3] = 0
                            return arr
                        elif cl == 3 and len(arr) > 3 and arr[3] == 0:
                            arr[0] = 1
                            return arr
            else:  # arr[1] == -1:
                return arr 
            return arr


    def chkLast(self, arr, cl):
        if len(arr) == 1:
            if cl==1:
                arr[0] = 1
            return arr
        if arr[-1] == 1:
            for i in range(-1,-cl-1, -1):
                arr[i] = 1
            if len(arr) > cl: arr[-cl-1] = 0
            return arr
        if arr[-1] == 0:
            return np.concatenate((self.chkLast(arr[:-1], cl), np.array([0])))
    
        if arr[-1] == -1:
            if arr[-2] == 0:
                if cl == 1:
                    return arr
                else:  #   cl > 1:
                    arr[-1] = 0
                    return np.concatenate((self.chkLast(arr[:-2], cl), np.array([0,0])))
            elif arr[-2] == 1:
                if cl == 1:
                    arr[-1] = 0
                    if len(arr) > 2: arr[-3] = 0
                    return arr
                elif cl > 1:
                    if len(arr) > 2 and arr[-3] == 0:
                        arr[-1] = 1
                        return arr
                    elif len(arr) > 2 and arr[-3] == -1:
                        return arr
                    else:  # arr[-1] = -1, arr[-2] = 1 arr[-3] = 1    
                        if cl == 2:
                            arr[-1] = 0
                            if len(arr) > 3: arr[-4] = 0
                            return arr
                        elif cl == 3 and len(arr) > 3 and arr[-4] == 0:
                            arr[-1] = 1
                            return arr
            else:  # arr[-2] == -1:
                return arr 
            return arr
#################################################################################################################
def findfits(lineclues, linevals):
    if len(lineclues) == 0:
        return []

    valid = []
    linesize = len(linevals)
    testclue = -1
    for i, clue in enumerate(lineclues):
        if lineclues[i][1] == -1:
            testclue = i
            break
    if testclue == -1:
        # Recursive end case: All clues are matched to something. Validate that there are no more unmatched positives.
        if 1 not in linevals[lineclues[-1][0] + lineclues[-1][1]:]:
            return [[a[:] for a in lineclues]]
        else:
            return []

    start = 0
    if testclue > 0:
        start = lineclues[testclue-1][0] + lineclues[testclue-1][1] + 1
    after = sum([a[0] for a in lineclues[testclue+1:]]) + len(lineclues[testclue+1:])
    end = linesize - after - lineclues[testclue][0]
    for testval in range(start, end+1):
        if testval + clue[0] < linesize and linevals[testval+clue[0]] == 1:
            # Positive square after where this segment would need to end
            continue
        if 0 in linevals[testval:testval+clue[0]]:
            # Negative square inside this segment
            continue
        if 1 in linevals[start:testval]:
            # Unmatched positive before sequence
            continue
        lineclues[testclue][1] = testval
        # Recursive iteration state: Is a valid configuration
        valid.extend(findfits(lineclues, linevals))
    lineclues[testclue][1] = -1
    # Recursive end state: All iterations complete
    return valid


def clues_to_values(clues, rowlen):
    result = [0] * rowlen
    for clue in clues:
        result[clue[1]:clue[1]+clue[0]] = [1] * clue[0]
    return result


def valid_clues_to_values(valid_clues, rowlen):
    if len(valid_clues) == 0:
        return [0] * rowlen
    result = clues_to_values(valid_clues[0], rowlen)
    for clues in valid_clues[1:]:
        result_sub = clues_to_values(clues, rowlen)
        result = [-1 if result[i] != result_sub[i] else result[i] for i in range(rowlen)]
    return result


def row_solve(solution, sl, clues):
    s = solution[sl]
    f = findfits(clues, s)
    valid = valid_clues_to_values(f, len(s))
    solution[sl] = [max(s[i], valid[i]) for i in range(len(s))]
    for i in range(len(clues)):
        ff = [ff[i][1] for ff in f]
        fr = ff[0] if all([ff[i] == ff[0] for i in range(len(ff))]) else -1
        clues[i][1] = fr


def my_solve(clues, width, height):
    clues_h = [[[a, -1] for a in clue] for clue in clues[0]]
    clues_w = [[[a, -1] for a in clue] for clue in clues[1]]
    solution = [-1] * width * height
    solution_last = [-2] * width * height
    while -1 in solution and solution != solution_last:
        solution_last = solution[:]
        for i in range(height):
            row_solve(solution, slice(i * width, (i + 1) * width, 1), clues_w[i])
        for i in range(width):
            row_solve(solution, slice(i, height*width, width), clues_h[i])
    solution = tuple([tuple(solution[i * width:(i + 1) * width]) for i in range(height)])
    return solution

class Nonogram:
    def __init__(self, clues):
        self.clues = clues

    def solve(self):
        return my_solve(self.clues, 5, 5)
###################################################################
class Nonogram:
    def __init__(self, clues):
        self.clues = clues

    def solve(self):
        cc, rc = self.clues
        cs, rs = len(rc), len(cc)
        col_opts = [list(self.line_options(col, cs)) for col in cc]
        row_opts = [list(self.line_options(row, rs)) for row in rc]
        field = [None] * cs * rs

        while None in field:
            for i, opts in enumerate(col_opts):
                field[i::cs] = self.solve_line(field[i::cs], opts)
            for i, opts in enumerate(row_opts):
                field[i*rs:(i+1)*rs] = self.solve_line(field[i*rs:(i+1)*rs], opts)
                
        return tuple(tuple(field[i*rs:(i+1)*rs]) for i in range(cs))
        
    def solve_line(self, line, options):
        valid_opts = [opt for opt in options if all(v in (o, None) for o, v in zip(opt, line))]
        return [col.pop() if len(col)==1 else None for col in map(set, zip(*valid_opts))]

    def line_options(self, clues, line_len):
        gap = line_len - sum(clues) - len(clues) + 1
        offsetss = [[]]
        for cl in clues:
            offsetss = [[*offsets, o] for offsets in offsetss for o in range(gap - sum(offsets) + 1)]
        for offsets in offsetss:
            opt = "0".join("0"*o + "1"*c for o, c in zip(offsets, clues)).ljust(line_len, "0")
            yield list(map(int, opt))
###########################################################################################################
import re
from itertools import product

class Nonogram:

    def __init__(self, clues):
        self.xclues = [list(c) for c in clues[0]]
        self.yclues = [list(c) for c in clues[1]]
        self.grid = [[0] * 5 for i in range(5)]
        self.perms = list(product([0,1], repeat=5))

    def check(self, clue, house):
        ls = re.findall(r'[1]+', ''.join(house))
        if len(clue) != len(ls):
            return False
        for j,e in enumerate(clue):
            if len(ls[j]) != e:
                return False
        return True
        
    def valid(self):
        for i,r in enumerate(self.grid):
            if not self.check(self.yclues[i], map(str,r)):
                return False
        return True
    
    def lock(self, x, seq):
        for i,c in enumerate(seq):
            self.grid[i][x] = c
            
    def unlock(self, x):
        for i in range(5):
            self.grid[i][x] = 0
        
    def dfs(self, x):
        if x == 5:
            return self.valid()
        for perm in self.perms:
            self.lock(x, perm)
            if self.check(self.xclues[x], [str(self.grid[i][x]) for i in range(5)]):
                if self.dfs(x + 1):
                    return True
            self.unlock(x)
        return False
        
    def solve(self):
        self.dfs(0)
        return tuple(tuple(r) for r in self.grid)
###########################################################################
def testNonogram(rowAr, colAr):
    for y in range(5):
        for x in range(5):
            if(rowAr[y][x] != colAr[x][y]):
                return 0
    return(1)

def countByArray(arr):
    length = 1
    for a in arr:
        length *= a

    out = []
    counter = [0] * len(arr)
    for i in range(length):

        out.append([n for n in counter])
        counter[0] += 1

        for d in range(len(arr)):
            if(counter[d] == arr[d] and d != len(arr) - 1):
                counter[d] = 0
                counter[d + 1] += 1


    return(out)

def permutasion(mask):
    out = []
    if len(mask) == 1:
        it = 6 - mask[0]
        for i in range(it):
            col = [0] * 5
            for l in range(mask[0]):
                col[i+l] = 1
            out.append(col)

    elif len(mask) == 2:
        it1 = 6 - mask[0] - 1 - mask[1]
        for i1 in range(it1):
            col1 = [0] * 5
            for l in range(mask[0]):
                col1[i1+l] = 1

            it2 = 5 - i1 - mask[0] - mask[1]
            for i2 in range(it2):
                col2 = [n for n in col1]
                for l in range(mask[1]):
                    col2[i1 + i2 + mask[0] + 1 + l ] = 1
                out.append(col2)

    else:
        out.append([1, 0, 1 ,0 ,1])

    return(out)

class Nonogram:

    def __init__(self, clues):
        print(clues)
        self.clues = clues

    def solve(self):
        rowPos = []
        for clue in self.clues[1]:
            rowPos.append(permutasion(clue))

        colPos = []
        for clue in self.clues[0]:
            colPos.append(permutasion(clue))

        allPos = countByArray([len(i) for i in rowPos] + [len(i) for i in colPos])

        for pos in allPos:
            row = [tuple(rowPos[i][pos[i]]) for i in range(5)]
            col = [tuple(colPos[i][pos[i + 5]]) for i in range(5)]
            if(testNonogram(row, col)):
                return(tuple(row))
##################################################################################
import numpy as np

class Nonogram:
    SIZE = 5
    
    def __init__(self, clues):
        self.clues = clues

    def solve(self):
        board = np.full((self.SIZE, self.SIZE), -1)
        board = self.solve_sub(0, 0, board)
        return tuple(tuple(row) for row in board.tolist())

    def solve_sub(self, i, axis, board):
        if i == self.SIZE:
            return board
        
        clue = self.clues[axis^1][i]
        for row in self.get_row_candidates(clue, self.SIZE):
            board2 = self.place(board, i, axis, np.array(row))
            if board2 is not None:
                if axis == 0:
                    result = self.solve_sub(i, 1, board2)
                else:
                    result = self.solve_sub(i+1, 0, board2)
                if result is not None:
                    return result
        
        return None
    
    def get_row_candidates(self, clues, length, first=True):
        if not clues:
            return [[0] * length]
        
        n = clues[0]
        candidates = []
        
        if first:
            pattern = [1] * n
        else:
            pattern = [0] + [1] * n
        
        if length < len(pattern):
            return None
        
        c1 = self.get_row_candidates(clues[1:], length - len(pattern), False)
        if c1 != None:
            candidates.extend([pattern + c for c in c1])
        
        c0 = self.get_row_candidates(clues, length - 1, first)
        if c0 != None:
            candidates.extend([[0] + c for c in c0])
        
        return candidates
    
    def place(self, board, i, axis, row):
        if axis == 0:
            board_row = board[i, :]
        else:
            board_row = board[:, i]
        
        if np.any((board_row != -1) & (board_row != row)):
            return None
        
        board2 = board.copy()
        if axis == 0:
            board2[i, :] = row
        else:
            board2[:, i] = row
        return board2
##########################################################################
import re
class Nonogram:

    def __init__(self, clues):
        self.horzs = clues[1]
        self.verts = clues[0]
        self.field = [[-1 for i in range(5)] for j in range(5)]
        
    def finished(self):
        for i in range(5):
            for j in range(5):
                if self.field[i][j] == -1:
                    return False
        return True

    def solve(self):
        while not self.finished():
            for i in range(5):
                self.field[i] = getBetter(self.field[i], self.horzs[i])
            
                col = [self.field[j][i] for j in range(5)]
                col = getBetter(col, self.verts[i])
                for j in range(5):
                    self.field[j][i] = col[j]
        tupleField = tuple(tuple(self.field[i][j] for j in range(5)) for i in range(5))
        return tupleField
            
def getBetter(row, clue):
    opts = getOpts(row)
    regex = re.compile(getRegex(clue))
    valid = []
    for opt in opts:
        if regex.match(toString(opt)):
            valid.append(opt)
    if len(valid) == 1:
        return valid[0]
    else:
        best = []
        for i in range(5):
            normal = valid[0][i]
            for j in range(1, len(valid)):
                if valid[j][i] != normal:
                    normal = -1
                    break
            best.append(normal)
        print(best, row, clue, valid)
        return best
                
        


def toString(row):
    res = ""
    for ele in row:
        res += str(ele)
    return res
    

def getRegex(clue):
    ones = []
    for ele in clue:
        ones.append("1" * ele)
    return "^0*" + "0+".join(ones) + "0*$"
    
def getOpts(row):
    opts = [row.copy()]
    for i in range(len(row)):
        if row[i] == -1:
            for j in range(len(opts)):
                new = opts[j].copy()
                new[i] = 0
                opts[j][i] = 1
                opts.append(new)
    return opts
