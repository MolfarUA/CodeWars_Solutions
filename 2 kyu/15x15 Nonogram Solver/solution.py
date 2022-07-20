5a5072a6145c46568800004d


from itertools import groupby
from collections import defaultdict

POS, B = defaultdict(set), 15
f = "{:0>" + str(B) + "b}"
for n in range(1<<B):
    s = f.format(n)
    POS[ tuple(sum(1 for _ in g) for k,g in groupby(s) if k == '1') ].add( tuple(map(int, s)))
    
def solve(clues):
    clues = {'V': clues[0], 'H': clues[1]}
    grid = { (d,z): list(POS[ clues[d][z] ]) for d in 'VH' for z in range(B)}
    
    changed = True
    while changed:
        changed = False
        
        for x in range(B):
            for y in range(B):
            
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
    
    return tuple( grid[('H',n)][0] for n in range(B) )
  
##################
def result(arglist, m):
    resultlist = []
    if not arglist:
        return ['0' * m]
    for i in range(m - sum(arglist) - len(arglist) + 2):
        s = '0' * i + '1' * arglist[0]
        if len(arglist) == 1:
            s += '0' * (m - len(s))
            resultlist.append(s)
        else:
            resultlist.extend([s + '0' + j for j in result(arglist[1:], m - arglist[0] - i - 1)])
    return resultlist


def decide(array: list, i: int):
    decidemark = array[0][i]
    for j in array:
        if j[i] != decidemark:
            return 0
    return decidemark


def deleteillegal(array: list, i: int, decidemark) -> list:
    newarray = []
    for j in array:
        if j[i] == decidemark:
            newarray.append(j)
    return newarray


def solve(x):
    horizontal = x[1]
    vertical = x[0]
    n = len(x[0])
    horizontallist = [result(i, n) for i in horizontal]
    verticallist = [result(i, n) for i in vertical]
    answerlist = [[0 for i in range(n)] for j in range(n)]
    count = 0
    while count < n * n:
        for i in range(n):
            for j in range(n):
                if answerlist[i][j]:
                    continue
                mark = decide(horizontallist[i], j)
                if mark:
                    answerlist[i][j] = mark
                    count += 1
                    verticallist[j] = deleteillegal(verticallist[j], i, mark)
        for i in range(n):
            for j in range(n):
                if answerlist[j][i]:
                    continue
                mark = decide(verticallist[i], j)
                if mark:
                    answerlist[j][i] = mark
                    count += 1
                    horizontallist[j] = deleteillegal(horizontallist[j], i, mark)
    data = ()
    for i in horizontallist:
        x = ()
        for j in i[0]:
            x += (int(j),)
        data += (x, )
    return data
  
############################
from itertools import accumulate, chain, groupby, islice

class NonogramSolver:
    
    def __init__(self, clues):
        self.N      = len(clues[0])                          # Dimension assuming square shaped nonogram.
        self.clues  = clues[1] + clues[0]
        self.board  = [[2] * self.N for _ in range(self.N)]  # 0 = empty, 1 = filled, 2 = unkown.
        self.ranges = []                                     # In each line, each clue has a range which is the span 
                                                             # of the leftmost to rightmost possible possition of a
                                                             # filled cell in the corresponding block,
                                                             # both enpoints included.
        self.initializeRanges()
        
    # Rows are labeled by numbers from 0 to N - 1 and columns are labeled from N to 2 * N - 1.
    # A line is either a row or a column.
        
    def initializeRanges(self):
        ''' Initialize the ranges from the given clues. '''
        for clues in self.clues:
            acc    = list(accumulate(x + 1 for x in clues))
            starts = [0] + acc[:-1]
            ends   = [self.N - 1 - acc[-1] + x for x in acc]
            self.ranges.append(list(zip(starts, ends)))

    ############################## Utility functions ##############################

    def printBoard(self):
        print('-' * (self.N * 2 + 1))
        for row in self.board:
            print('|' + ','.join(str(x) if x < 2 else '.' for x in row) + '|')
        print('-' * (self.N * 2 + 1))

    @staticmethod
    def transpose(mat):
        return list(map(list, zip(*mat)))

    def getLine(self, label):
        ''' Get line (row or col) from corresponding label. '''
        if label < self.N:
            return self.board[label][:]
        return NonogramSolver.transpose(self.board)[label % self.N]

    def overwriteLine(self, label, line):
        ''' Overwrite the line of the board labeled by "label" with "line". '''
        if label < self.N:
            self.board[label] = line[:]
        else:
            j = label % self.N
            for i in range(self.N):
                self.board[i][j] = line[i]

    def reversedRanges(self, ranges):
        return [(self.N - b - 1, self.N - a - 1) for a, b in reversed(ranges)]

    @staticmethod
    def findBlocks(lst, offset = 0):
        '''
        Assuming lst is a list of zeros and ones.
        Return the indices of the start and end (both included) of a group of consecutive ones.
        
        (offset): shift in index values.
        '''
        g = list(accumulate(len(tuple(g)) for _, g in groupby(chain([0], lst))))
        return list((a - 1 + offset, b - 2 + offset) for a, b in zip(g, islice(g, 1, None)))[::2]

    def generateAllPossibleLines(self, label):
        ''' Generate all lines consistent with the line labeled by "label". '''
        line   = self.getLine(label)
        clues  = self.clues[label]
        ranges = self.ranges[label]

        def isConsistent(l):
            return all(y == 2 or x == y for x, y in zip(l, line))

        def genBlock(a, b, c):
            for i in range(a, b - c + 2):
                yield [0] * (i - a) + [1] * c

        def genLine(i, xs):
            if i == len(clues):
                ys = xs + [0] * (self.N - len(xs))
                if isConsistent(ys):
                    yield ys
                return
            a, b = ranges[i]
            xs += [0] * (a - len(xs))
            if xs and xs[-1] == 1:
                xs.append(0)
            if isConsistent(xs):
                for block in genBlock(max(a, len(xs)), b, clues[i]):
                    yield from genLine(i + 1, xs + block)

        yield from genLine(0, [])

    ############################## Deductive rules ##############################

    def fillIntersections(self, label):
        '''
        The intersection of the leftmost and rightmost
        possible positions of a block must be filled.
        Mutate the board.
        '''
        line = self.getLine(label)
        for (a, b), c in zip(self.ranges[label], self.clues[label]):
            for i in range(a, b + 1):
                if b - c + 1 <= i <= a + c - 1:
                    line[i] = 1
        self.overwriteLine(label, line)

    def clearUntouchedCells(self, label):
        '''
        If a cell is not included in any range it must be left empty.
        Mutate the board.
        '''
        line = self.getLine(label)
        for i in range(self.N):
            if not any(a <= i <= b for a, b in self.ranges[label]):
                line[i] = 0
        self.overwriteLine(label, line)

    def discardTooSmallSegments(self, label):
        '''
        Some segments bounded by empty cell may be too small for a given clue.
        Update the ranges and possibly the board accordingly.
        Mutate the board and the ranges.
        '''
        line   = self.getLine(label)
        clues  = self.clues[label]
        ranges = self.ranges[label]
        for i, (a, b) in enumerate(ranges):

            blocks = NonogramSolver.findBlocks([int(x > 0) for x in islice(line, a, b + 1)], offset = a)
            if not blocks or not any(y - x + 1 >= clues[i] for x, y in blocks):
                continue

            m, x = next(iter((j, x) for j, (x, y) in enumerate(blocks)
                             if y - x + 1 >= clues[i]), (-1, a))
            n, y = next(iter((len(blocks) - 1 - j, y) for j, (x, y) in enumerate(reversed(blocks))
                             if y - x + 1 >= clues[i]), (-1, b))
            ranges[i] = (x, y)

            for x, y in islice(blocks, m + 1, n):
                A = y - x + 1 < clues[i]
                B = i == 0 or x > ranges[i - 1][1]
                C = i + 1 == len(ranges) or y < ranges[i + 1][0]
                if A and B and C:
                    line[x: y + 1] = [0] * (y - x + 1)

        self.ranges[label] = ranges
        self.overwriteLine(label, line)

    def resolveByOverlappingPossibleLines(self, label):
        '''
        If a cell is filled/empty in every variant of the line consistent with our
        current knowledge of it, it must be filled/empty.
        Mutate the board.
        '''
        line = self.getLine(label)
        if 2 <= line.count(2):
            overlap = [x[0] if len(set(x)) == 1 else 2
                       for x in zip(*self.generateAllPossibleLines(label))]
            self.overwriteLine(label, overlap)

    def resovleNonOverlappingRanges(self, label):
        '''
        Apply some logical rules concerning consecutive ranges that do not overlap.
        Mutate the board and the ranges.
        '''
        line   = self.getLine(label)
        clues  = self.clues[label]
        ranges = self.ranges[label]

        for _ in range(2): # First time forward and second time backward.

            for i, ((a, b), c) in enumerate(zip(ranges, clues)):

                if i > 0 and ranges[i - 1][1] >= a:
                    continue

                if line[a] == 1:

                    line[a: a + c] = [1] * c
                    if a > 0:          line[a - 1] = 0
                    if a + c < self.N: line[a + c] = 0

                    ranges[i] = (a, a + c - 1)
                    if i > 0 and ranges[i - 1][1] > a - 2:
                        ranges[i - 1] = (ranges[i - 1][0], a - 2)
                    if i + 1 < len(ranges) and ranges[i + 1][0] < a + c + 1:
                        ranges[i + 1] = (a + c + 1, ranges[i + 1][1])

                x = next(iter(j for j in range(a, b + 1) if line[j] == 1), -1)
                if x != -1:
                    y = next(iter(j for j in range(x + 1, b + 1) if line[j] == 0), -1)
                    ranges[i] = (a, y - 1) if y != -1 else (a, min(x + c - 1, ranges[i][1]))

                filledBlocks = NonogramSolver.findBlocks(
                    [int(x == 1) for x in islice(line, a, b + 1)],
                    offset = a
                )
                if len(filledBlocks) > 1:
                    x, y = filledBlocks[0]
                    for j, (p, q) in enumerate(islice(filledBlocks, 1, None)):
                        if q - x + 1 > c:
                            ranges[i] = (a, p - 2)

            line   = line[::-1]
            clues  = clues[::-1]
            ranges = self.reversedRanges(ranges)

        filledBlocks = NonogramSolver.findBlocks([int(x == 1) for x in line])
        rs = [(0, -1)] + ranges + [(self.N, 0)]
        for x, y in filledBlocks:
            for i, ((_, pb), (a, b), (na, _)) in enumerate(zip(rs, islice(rs, 1, None), islice(rs, 2, None))):
                if pb < x and y < na and a <= x and y <= b:
                    ranges[i] = (max(0, x - clues[i] + y - x + 1),
                                 min(self.N - 1, y + clues[i] - y + x - 1))

        self.ranges[label] = ranges
        self.overwriteLine(label, line)

    ##############################  Validation  ##############################

    def isCompleted(self):
        return all(0 <= x <= 1 for row in self.board for x in row)

    def isSolved(self):
        return self.isCompleted() and \
               all(self.clues[label] == tuple( len(tuple(g))
                                               for x, g in groupby(self.getLine(label)) if x == 1)
                                               for label in range(len(self.clues) ))

    ##############################  Solvers  ##############################

    def applyConstraints(self):
        ''' Apply the constraints from the deductive rules until they are exhausted. '''
        prevBoard  = [[] * self.N]
        prevRanges = [[] * len(self.ranges)]

        while any(x != y for x, y in zip(prevBoard, self.board)) or \
              any(x != y for x, y in zip(prevRanges, self.ranges)):   # While the board or ranges are updated.

            prevBoard  = [row[:] for row in self.board]
            prevRanges = [x[:] for x in self.ranges]

            for label in range(len(self.clues)):
                self.fillIntersections(label)

            for label in range(len(self.clues)):
                self.clearUntouchedCells(label)

            for label in range(len(self.clues)):
                self.discardTooSmallSegments(label)

            for label in range(len(self.clues)):
                self.resolveByOverlappingPossibleLines(label)

            for label in range(len(self.clues)):
                self.resovleNonOverlappingRanges(label)

    def solve(self):

        try:
            self.applyConstraints()
        except:
            print('Unsolvable nonogram')
            return None

        if self.isSolved():
            print('Nonogram successfully solved')
        else:
            print('Nonogram not completely solved')
        return tuple(tuple(row) for row in self.board)


def solve(clues):
    return NonogramSolver(clues).solve()
  
########################
import numpy as np

class Nonogram:
    def __init__(self, clues):
        self.width = len(clues[0])
        self.colClues = clues[0]
        self.rowClues = clues[1]
        self.Board = np.ones((self.width,self.width),dtype=int)*(-1)
        self.RowColumnPossibilies()
        self.rowsSolved = [0]*self.width
        self.colsSolved = [0]*self.width

    def RowColumnPossibilies(self):
        '''
        creates list of ndarrays for row possibilities --self.rP
        and list of ndarrays for column possibilities --self.cP
        '''
                                          # 1st create list of lists of possibilities     
        rPoss = [self.possible_cells(self.width, cl) for cl in self.rowClues]
        cPoss = [self.possible_cells(self.width, cl) for cl in self.colClues]
                                          # then create ndarray for each list and store in list
        rP = []
        cP = []
        for j in range(self.width):
            for i in range(len(rPoss[j])):
                if i == 0: arrLst = np.array(rPoss[j][i])
                else: arrLst = np.vstack([arrLst, rPoss[j][i]])
            rP.append(arrLst)
            for i in range(len(cPoss[j])):
                if i == 0: arrLst = np.array(cPoss[j][i])
                else: arrLst = np.vstack([arrLst, cPoss[j][i]])
            cP.append(arrLst) 
        self.rP = rP
        self.cP = cP
        return
    
    def possible_cells(self, width, clues):
        '''
        width : int  -- the width of the Nonogram 
        clues : tuple of clues (as integers), len = width
        
        Returns
        list of possible (row or column) values that satisfy clues (list of lists)
        '''
        if clues == () or clues == (0,):
            return [[0] * width]

        if len(clues) == 1:                                         #  returning one
            return [([0] * i                                        
                     + [1] * clues[0]
                     + [0]*width)[:width] 
                          for i in range(width - clues[0] + 1)]
        
        min_width = sum(clues) + len(clues) - 1       
        res = []
        for i in range(0, width - min_width + 1):            #  recursive call
            start = [0] * i + [1] * clues[0] + [0]
            res += [start + p for p in self.possible_cells(width - len(start), clues[1:])]
    
        return res        
        
    def solve(self):
        '''
        for existing self.Board and arrays of possibilities for 
        rows (self.rP) and columns (self.cP)
        
        Returns (if all goes well)
        solution in the form of a tuple of tuples of rows
        '''
        count = np.count_nonzero(self.Board < 0)
        improvement = count
        self.updateBoardRows()
        while count > 0 and improvement > 0:
            self.updateColPoss()
            self.updateBoardCols()
            self.updateRowPoss()
            self.updateBoardRows()
            improvement = count - np.count_nonzero(self.Board < 0)              
            count = np.count_nonzero(self.Board < 0)

        array_of_tuples = map(tuple, self.Board)
        return tuple(array_of_tuples)

    def updateBoardRows(self):
        '''
        Update the current configuration of the Board rows
        Returns -- None
        '''
        for j in range(self.width):
            if self.rowsSolved[j] == 0:
                self.Board[j,:] = self.updateBoard(self.rP[j],self.Board[j,:])
                if np.count_nonzero(self.Board[j,:] == -1) == 0:
                    self.rowsSolved[j] = 1
        return
    
    def updateBoardCols(self):
        '''
        Update the current configuration of the Board columns
        Returns -- None
        '''  
        for j in range(self.width):
            if self.colsSolved[j] == 0:
                self.Board[:,j] = self.updateBoard(self.cP[j],self.Board[:,j])
                if np.count_nonzero(self.Board[:,j] == -1) == 0:
                    self.colsSolved[j] = 1
        return
    
    def updateBoard(self, arr, brd):
        '''
        arr : array of possibilities for a row or column
        brd : the corresponding current row or column 
        Returns
        brd : updated row or column from the possibilities
        '''
        if arr.ndim == 1:    #nothing to do. Only 1 possibility
            brd = arr  
            return brd          
                                    # sum the rows of the possibility array 
                                    # and if the sum is 0 (all zeros) or 
                                    # len(arr) (all 1s)  we update the brd 
                                    # with these definite results                     
        x = arr.sum(axis = 0)
        x = np.where( (x > 0 ) & (x<len(arr)), -1, x)
        netPoss = np.where( (x > 0 ), 1, x) 
        idxToUpdate = np.where(np.not_equal(brd, netPoss))[0]
        for i in idxToUpdate:
            if brd[i] < 0: brd[i] = netPoss[i]

        return brd

    def updateRowPoss(self):
        '''
        Update the current row possibilities from the current Board configuration
        Returns -- None
        '''
        for j in range(self.width):
            self.rP[j] = self.updatePoss(self.rP[j],self.Board[j,:])
        return   
    
    def updateColPoss(self):
        '''
        Update the current col possibilities from the current Board configuration
        Returns -- None
        '''
        for j in range(self.width):
            self.cP[j] = self.updatePoss(self.cP[j],self.Board[:,j])
        return   
       
    def updatePoss(self, arr, brd):
        if arr.ndim == 1: 
            return arr
        if np.count_nonzero(brd > -1) > 0:
            for k in range(len(brd)):
                #print(k,arr,brd)
                if brd[k] > -1:
                    arr = np.delete(arr, np.nonzero(arr[:,k] != brd[k]) , 0)
        return arr


def solve(clues):
    S = Nonogram(clues)
    return S.solve()
  
#################################
def cluetoset(clue, dim, res = []):
    if not clue:
        yield from [[0]*dim]
        return None
    blocks_next = len(clue)-1  #blocks after this one
    if blocks_next:
        leave = sum(clue[1:]) + blocks_next  # minimum space for subsequent including afterspace
        maxpos = dim -leave - clue[0] + 1          #maximum position of first black of the first block
    else:
        maxpos = dim - clue[0] + 1
    minpos = 0
    
    for i in range(minpos, maxpos):
        res_new = res + [0]*i + [1]*clue[0]
        if blocks_next:
            yield from cluetoset(clue[1:], dim - i - clue[0] - 1, res_new + [0] )
        else:
            yield res_new + [0]*(dim - i - clue[0] )
        
def solve(clues, width=15, height=15):
    rows = [list(cluetoset(r, width)) for r in clues[1]]
    cols = [list(cluetoset(c, height)) for c in clues[0]]
    for it in range(30):
        for r in range(height):
            if rows[r] == None:
                continue
            for c in range(width):
                if cols[r] == None:
                    continue
                r_possible = {row[c] for row in rows[r]}
                c_possible = {col[r] for col in cols[c]}
                if r_possible != c_possible:
                    joint = r_possible & c_possible
                    rows[r] = [row for row in rows[r] if row[c] in joint]
                    cols[c] = [col for col in cols[c] if col[r] in joint]
        print (it)
        rconds = max([len(row) for row in rows])
        cconds = max([len(col) for col in cols])
        print(rconds,cconds)
        if rconds == 1:
            return tuple(tuple(row[0]) for row in rows)
        if cconds == 1:
            return tuple( tuple(cols[c][0][r] for c in range(width)) for r in range(height))
    return False
  
#######################################
import re
import time

testClues = (((1,), (1, 4), (1, 3), (1, 1, 1), (2, 1, 2, 4), (1, 2, 1, 1, 3), (1, 1, 1, 1, 1, 2), (1, 1, 1, 1,1, 3), (2, 1, 2, 2, 3), (2, 2, 2, 2), (2, 2, 2, 3), (2, 2, 2, 2), (2, 2, 3), (1, 2, 2), (1,)), ((4,), (2, 3), (8,), (2, 3), (1, 5), (1, 1, 5), (1, 1, 3, 4), (2, 1, 3), (3, 1, 1, 4), (3, 1, 2, 3), (1, 1, 3, 2), (1, 2, 3), (2, 2, 2), (2, 2), (1, 1)))

newTestClues = (((3, 2), (2, 1, 1), (3, 1, 1, 2), (1, 4, 3), (1, 2, 3), (3, 2, 1, 1), (1, 1, 1, 2), (1, 12), (1, 1, 1, 2), (3, 2, 1, 1), (1, 2, 3), (1, 4, 3), (3, 1, 1, 2), (2, 1, 1), (3, 2)), ((3,), (1, 1), (1, 1), (11,), (1, 1, 1), (2, 3, 2), (1, 1, 1, 1, 1, 1, 1), (1, 3, 1, 3, 1), (5, 1, 5), (1, 1, 1), (1, 1, 1), (1, 1, 1), (1, 3, 1, 3, 1), (1, 3, 3, 3, 1), (3, 7, 3)))

def printField(field):
    say = ["? ", ". ", "[]"]
    for i in range(len(field)):
        row = field[i]
        rowStr = ""
        for ele in row:
            rowStr += say[ele + 1]
        print(rowStr, hex(i + 1))
        
def getPosGuess(field):
    for x in range(len(field)):
        for y in range(15):
            if field[x][y] == -1:
                return x, y
    raise ValueError()
    
def solveIter(field, horzs, verts, cacheCol, cacheRow):
     for i in range(15):
        row = field[i]
        row, cacheRow[i] = getBetter(row, horzs[i], cacheRow[i])
        field[i] = row
        col = [field[j][i] for j in range(15)]
        col, cacheCol[i] = getBetter(col, verts[i], cacheCol[i])
        for j in range(15):
            field[j][i] = col[j]   
            
    
def solve(clues):
    field = [[-1 for i in range(15)] for j in range(15)]
    horzs = clues[1]
    verts = clues[0]
    optionCacheRow = [[] for i in range(15)]
    optionCacheCol = [[] for i in range(15)]
    
    loops = 0
    old = None
    
    while not isFinished(field):
        loops += 1
        if loops > 10000:
            raise ValueError()
            print("made no progress since last iter.. aborting ):", old == field)
            print(clues)
            printField(field)
            return field
        old = list([row.copy() for row in field])
        solveIter(field, horzs, verts, optionCacheRow, optionCacheCol)

    return tuple(tuple(field[i]) for i in range(15))

def getBetter(row, clues, cachedOpts, isVert = False):
    doPrint = clues == (3, 2) and isVert
    
    old = row.copy()
    
    if len(cachedOpts) == 1:
        return cachedOpts[0], cachedOpts
    
    if cachedOpts == []:
        if doPrint:
            print("getting options...")
        cachedOpts = getPossibleOpts(row, clues)
    
    if doPrint:
        print(row, clues)
        for opt in cachedOpts:
            print(opt)
        
    for i in range(15):
        if row[i] != -1:
            if doPrint:
                print(i, row[i])
            delOff = 0
            for j in range(len(cachedOpts)):
                ele = cachedOpts[j - delOff]
                if doPrint:
                    print(ele[i], ele)
                if ele[i] != row[i]:
                    if doPrint:
                        print("hio", j - delOff, delOff, cachedOpts[j - delOff])
                        print(len(cachedOpts))
                    cachedOpts.pop(j - delOff)
                    delOff += 1
    if len(cachedOpts) == 1:
        return cachedOpts[0], cachedOpts
                
    for i in range(15):
        if row[i] == -1:
            normal = cachedOpts[0][i]
            for j in range(1, len(cachedOpts)):
                if cachedOpts[j][i] != normal:
                    normal = -1
                    break
            row[i] = normal
    if doPrint:
        print("second:")
        print(row, clues)
        for opt in cachedOpts:
            print(opt)
            
            
    if doPrint:
        print()
        print(old)
        print(row)
        print(clues)
        #print(cachedOpts)
        print()
        checkEndings(cachedOpts)
    return row, cachedOpts

def getPossibleOpts(row, clues):
    global totalOpts
    opts = [[-1 for i in range(15)]]
    for i in range(15):
        delOff = 0
        for j in range(len(opts)):
            ele = opts[j - delOff]
            ele[i] = 0
            if isPossible(ele, clues, i + 1):
                new = ele.copy()
                new[i] = 1
                if isPossible(new, clues, i + 1):
                    opts.append(new)
            else:
                ele[i] = 1
                if isPossible(ele, clues, i + 1):
                    continue
                else:
                    opts.pop(j - delOff)
                    delOff += 1
    return opts
        
def isPossible(row, clues, checkRange):
    currClueIndex = -1
    xLeft = 0
    prev = 0
    for i in range(checkRange):
        if row[i] == 0:
            if xLeft != 0:
                return False
        else:
            if xLeft == 0:
                if prev == 1 or len(clues) == currClueIndex + 1:
                    return False
                else:
                    currClueIndex += 1
                    xLeft = clues[currClueIndex] - 1
            else:
                xLeft -= 1
        prev = row[i]
    # if the amount of crosses to write down plus the amount of 
    #minimum needed spacing is too big for the future available space neglect option
    if xLeft + sum(clues[i] for i in range(currClueIndex + 1,len(clues))) \
       + len(clues) - 1 - (0 if currClueIndex == -1 else currClueIndex) - (1 if prev == 0  and currClueIndex != - 1 else 0)\
       > 15 - checkRange:
        #print(xLeft, currClueIndex, sum(clues[i] for i in range(currClueIndex + 1,len(clues))))
        return False
    return (currClueIndex == len(clues) - 1 and xLeft == 0) or checkRange != 15

def checkEndings(opts):
    for opt in opts:
        if opt[-1] == 1 and opt[-2] == 1 and opt[-3] == 1:
            raise ValueError()
            
def isFinished(field):
    for i in range(15):
        for j in range(15):
            if field[i][j] == -1:
                return False
    return True
opts = getPossibleOpts([-1 for i in range(15)], (3, 2))
printField(solve(newTestClues))
    
  
#######################################
from itertools import takewhile, repeat
import time
from enum import IntEnum, Enum

FILLED = 1
EMPTY = 0

class FlatClues:  # leave as two arrays
    def __init__(self, stack: [int]):
        self.stack = stack
        self.index = 0


class ShiftType(Enum):
    Available = 0,
    Mandatory = 1,
    Banned = 2,


def get_next_possible_bit_shifts(processed_top_clues):
    def get_next_bit_shifts(clues: FlatClues):
        next_index = clues.index
        if len(clues.stack) <= next_index or clues.stack[clues.index] == EMPTY:
            return ShiftType.Banned

        current_index = clues.index - 1
        if 0 > current_index or clues.stack[current_index] == EMPTY:
            return ShiftType.Available

        return ShiftType.Mandatory

    return [get_next_bit_shifts(processed_top_clue)
            for processed_top_clue in processed_top_clues]


def apply_permutation(processed_top_clues, permutation):
    def apply(clues, permutation_bit):
        if len(clues.stack) > 1 \
                and len(clues.stack) > clues.index \
                and (clues.stack[clues.index], permutation_bit) == (EMPTY, EMPTY) \
                or permutation_bit == FILLED:
            clues.index += 1
            return True
        else:
            return False

    return [apply(clues, permutation_bit)
            for (clues, permutation_bit)
            in zip(processed_top_clues, permutation)]


def undo_permutation(processed_top_clues, altered_bits):
    for (clues, altered_bit) in zip(processed_top_clues, altered_bits):
        if altered_bit:
            clues.index -= 1


def solve(clues):
    top_clues = clues[0]
    left_clues = clues[1]
    MAGIC_ROW_COUNT = 4

    def heuristics_of_first(row_count, clues):
        empty_clues_count = len([takewhile(lambda row: len(row) == 0, clues)])
        return heuristics_of(slice(0, row_count + empty_clues_count), clues)

    def heuristics_of_last(row_count, clues):
        empty_clues_count = len([takewhile(lambda row: len(row) == 0, reversed(clues))])
        return heuristics_of(slice(-1 - row_count - empty_clues_count, -1), clues)

    def heuristics_of(slice, clues):
        def heuristics_of(i, row):
            return len(row) + sum(row) * (1.6 if len(row) == 1 else 1) * (MAGIC_ROW_COUNT - i)

        return sum([heuristics_of(i, row) for i, row in enumerate(clues[slice])])

    def flip(clues_a, clues_b):
        return [tuple(reversed(row)) for row in clues_a], tuple(reversed(clues_b))

    has_flip_vertically = heuristics_of_last(MAGIC_ROW_COUNT, left_clues) > heuristics_of_first(MAGIC_ROW_COUNT, left_clues)
    has_flip_horizontally = heuristics_of_last(MAGIC_ROW_COUNT, top_clues) > heuristics_of_first(MAGIC_ROW_COUNT, top_clues)
    if has_flip_vertically:
        top_clues, left_clues = flip(top_clues, left_clues)
    if has_flip_horizontally:
        left_clues, top_clues = flip(left_clues, top_clues)

    has_flip_diagonally = heuristics_of_first(MAGIC_ROW_COUNT, top_clues) > heuristics_of_first(MAGIC_ROW_COUNT,
                                                                                                left_clues)
    if has_flip_diagonally:
        top_clues, left_clues = left_clues, top_clues

    def to_bits(clue_row):
        def to_ones(clue):
            return list(repeat(1, clue)) + [0]

        return [one for clue in clue_row for one in to_ones(clue)]

    processed_top_clues = [FlatClues(to_bits(clue_row)) for clue_row in top_clues]
    permutation_stack = []

    def solve_rec(top_clues, left_clues, permutation_stack):
        clues_len = len(left_clues)  # NOTE: T
        current_clues_index = len(permutation_stack)
        rest_clue_lens = [len(clues.stack) - clues.index - 1 for clues in top_clues]

        has_not_enough_len = any(
            map(lambda rest_clue_len: rest_clue_len > clues_len - current_clues_index, rest_clue_lens))
        if has_not_enough_len:
            return False

        next_possible_bits = get_next_possible_bit_shifts(top_clues)

        for permutation in get_permutations(
                next_possible_bits, left_clues[current_clues_index], clues_len, rest_clue_lens):

            altered_bits = apply_permutation(top_clues, permutation)
            permutation_stack.append(tuple(permutation))
            if len(permutation_stack) == clues_len or solve_rec(top_clues, left_clues, permutation_stack):
                return True

            undo_permutation(top_clues, altered_bits)
            permutation_stack.pop()

        return False

    if solve_rec(processed_top_clues, left_clues, permutation_stack):
        if has_flip_diagonally:
            I, J = len(permutation_stack), len(permutation_stack[0])
            permutation_stack = [tuple(permutation_stack[i][j] for i in range(I)) for j in range(J)]
        if has_flip_vertically:
            permutation_stack = reversed(permutation_stack)
        if has_flip_horizontally:
            permutation_stack = map(tuple, map(reversed, permutation_stack))
        return tuple(permutation_stack)
    else:
        raise BaseException("Solution not found")


def get_permutations(next_possible_shifts, clues, size, rest_clue_lens):
    def get_permutations_rec(permutation, clues, init_offset: int):
        if len(clues) == 0:
            yield permutation
            return

        current_clue = clues[0]
        clues_sum = sum(clues)
        clues_borders = len(clues) - 1

        def offset_key(offset):
            return sum(rest_clue_lens[offset:offset + current_clue])  # function to get clues slice

        # TODO: run backwards when mass of clues is higher in the mid
        for new_offset in sorted(range(init_offset, 1 + size - clues_sum - clues_borders), key=offset_key,
                                 reverse=True):  # https://www.programiz.com/python-programming/methods/list/sort
            last_zero_index = new_offset + current_clue

            def set_clue_indices(bit):
                for i in range(last_zero_index - current_clue, last_zero_index):
                    permutation[i] = bit

            def has_last_zeroes_valid():
                if len(clues) == 1:
                    return has_zeroes_valid(last_zero_index, size)
                elif last_zero_index < len(next_possible_shifts):
                    return next_possible_shifts[last_zero_index] != ShiftType.Mandatory
                else:
                    return True

            def has_zeroes_valid(init_offset, new_offset):
                zeroes_range = slice(init_offset, new_offset)
                return all([shift != ShiftType.Mandatory for shift in next_possible_shifts[zeroes_range]])

            def has_ones_valid():
                ones_range = slice(new_offset, last_zero_index)
                return all([shift != ShiftType.Banned for shift in next_possible_shifts[ones_range]])

            if has_last_zeroes_valid() and has_zeroes_valid(init_offset, new_offset) and has_ones_valid():
                set_clue_indices(FILLED)

                for perm in get_permutations_rec(permutation, clues[1:], 1 + new_offset + current_clue):
                    yield perm

                set_clue_indices(EMPTY)

    return get_permutations_rec([EMPTY] * size, clues, 0)

#######################################################

def solve(clues):
    columns = [list(column) for column in clues[0]]
    rows = [list(column) for column in clues[1]]
    tiles = [[0] * 15 for i in range(15)]
    calculate(rows, columns, tiles)
    return tuple(tuple([value - 1 for value in tile]) for tile in tiles)

def permutate(values, row, count=0):
    if values and values[0]:
        value, *other = values
        for i in range(len(row) - sum(other) - len(other) + 1 - value):
            if 1 not in row[i:i+value]:
                for j in permutate(other, row[i+value+1:], 1):
                    yield [1] * (i + count) + [2] * value + j
    else:
        yield []

def check(values, row):
    permutations = []
    for permutation in permutate(values, row):
        permutation += [1] * (len(row) - len(permutation))
        for val1, val2 in zip(row, permutation):
            if val1 > 0 and val1 != val2:
                break
        else:
            permutations.append(permutation)
    new = permutations[0]
    for permutation in permutations[1:]:
        new = [val1 if val1 == val2 else 0 for val1, val2 in zip(new, permutation)]
    return new

def calculate(rows, columns, tiles):
    edited = True
    while edited:
        edited = False
        for i, row in enumerate(rows):
            for j, value in enumerate(check(row, tiles[i])):
                if value and tiles[i][j] != value:
                    edited = True
                tiles[i][j] = value
        for j, column in enumerate(columns):
            for i, value in enumerate(check(column, [row[j] for row in tiles])):
                if value and tiles[i][j] != value:
                    edited = True
                tiles[i][j] = value
                
################################
class ConstraintSingleton(type):
    _instances = {}

    def __call__(cls, id):
        if id not in cls._instances:
            cls._instances[id] = super(ConstraintSingleton, cls).__call__(id)
        return cls._instances[id]

class Constraint(object, metaclass=ConstraintSingleton):

    def __init__(self, id):
        self.id = id
        self.domain = []

    def strip(self, index, placed_val):
        self.domain = [value for value in self.domain if value[index] == placed_val]

    def add_domain_val(self, value):
        self.domain.append(value)

class CellSingleton(type):
    _instances = {}

    def __call__(cls, x, y):
        if (x, y) not in cls._instances:
            cls._instances[(x, y)] = super(CellSingleton, cls).__call__(x, y)
        return cls._instances[(x, y)]

class Cell(object, metaclass=CellSingleton):

    def __init__(self, x, y):
        self.x, self.y = (x, y)
        self.value = None
        self.linked = []

    def set_linked(self):
        self.linked = [Cell(self.x, y) for y in range(self.nono.HEIGHT)] + [Cell(x, self.y) for x in range(self.nono.WIDTH)]

    def check_value(self):
        if self.value is not None: return False
        for VH, index, op_index, opposite in [('H', self.x, self.y, f'V{self.y}'), ('V', self.y, self.x, f'H{self.x}')]:
            current_const = Constraint(f"{VH}{index}")
            placables = set([val[op_index] for val in current_const.domain])
            if len(placables) == 1:
                self.value = next(iter(placables))
                current_const.strip(op_index, self.value)
                Constraint(opposite).strip(index, self.value)
                [cell.check_value() for cell in self.linked]

    def __repr__(self):
        return f"Cell({self.x},{self.y}, {self.value if self.value is not None else '?'})"

class Nonogram:

    def __init__(self, clues):
        self.h_clues, self.v_clues = clues

        self.WIDTH = len(self.h_clues)
        self.HEIGHT = len(self.v_clues)

        ConstraintSingleton._instances = {}
        CellSingleton._instances = {}
        Cell.nono = Constraint.nono = self

        for i, (hclue, vclue) in enumerate(zip(self.h_clues, self.v_clues)):
            self.calc_domain('H', i, hclue), self.calc_domain('V', i, vclue)

        self.cells = [Cell(x, y) for y in range(self.HEIGHT) for x in range(self.WIDTH)]
        [cell.set_linked() for cell in self.cells]
        [cell.check_value() for cell in self.cells]

    def calc_domain(self, cdir, index, clue):
        fill_slots = len(clue)+1
        miss_1 = self.WIDTH-sum(clue)
        def _calc(poss=[]):
            s = 1 if len(poss) not in (0, fill_slots-1) else 0
            for n in range(s, miss_1-sum(poss)+1):
                new_poss = poss+[n]
                if len(new_poss) == fill_slots and sum(new_poss) == miss_1:
                    x = []
                    for i in range(len(new_poss)-1):
                        x += [0]*new_poss[i]
                        x += [1]*clue[i]
                    x += [0]*new_poss[-1]
                    if cdir == 'H':  Constraint(f"H{index}").add_domain_val(x)
                    else: Constraint(f"V{index}").add_domain_val(x)
                elif len(new_poss) < fill_slots: _calc(new_poss)
        _calc()

    def solve(self): return tuple(tuple(Cell(x, y).value for x in range(self.WIDTH)) for y in range(self.HEIGHT))

        
def solve(clues): return Nonogram(clues).solve()
