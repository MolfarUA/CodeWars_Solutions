from copy import deepcopy
import itertools as it
import numpy as np



class SudokuError(Exception):
    pass

class Sudoku(object):
    def __init__(self, board):
        self.board = board

    @classmethod
    def from_square(cls, board):
        for cell in it.chain(*board):
            if not isinstance(cell, int):
                raise SudokuError('Puzzle contain non digit charcters')
        
        cube =  [[set(range(1,10)) if cell == 0 else set([cell]) for cell in row] for row in board]
        return cls(cube)

    def rank(self):
        """ A completely solved board is of rank 0"""
        return sum(map(len, it.chain(*self.board))) - 9*9

    @property
    def is_solved(self):
        return self.rank() == 0

    def guess(self):

        min_cell, min_row, min_col = set(range(1, 10)), 0, 0
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if len(min_cell) > len(cell) >= 2:
                    min_cell, min_row, min_col = cell, i, j


        for option in min_cell:
            new_board = deepcopy(self.board)
            new_board[min_row][min_col].clear()
            new_board[min_row][min_col].add(option)
            new_sudoku = Sudoku(new_board)
            yield new_sudoku



    def square(self):
        """ Return the sudoko as readable 2D list of integers: """
        return [[list(cell).pop() if len(cell) == 1 else 0 for cell in row] for row in self.board]

    def reduce_possibilities(self):
        """ Given a sudoko solution reduce the number of possiblities per cell"""
        while True:
            before = self.rank()
            # Rows:
            for row in self.board:
                self.reduce_row(row)

            # Coloumns:
            for row in zip(*self.board):
                self.reduce_row(row)

            # Boxes:
            boxes_to_rows = []
            for i, j in it.product([0, 1, 2], [0, 1, 2]):
                boxes_to_rows.append([cell for row in self.board[3*i: 3*i + 3] for cell in row[3*j: 3*j + 3]])

            for row in boxes_to_rows:
                self.reduce_row(row)

            # Break test
            after = self.rank()
            if before == after:
                break

    def reduce_row(self, row):
        """ Minimize number of options for each cell for every row """

        # len 1 sets are known, longer sets are unknown:
        known = [cell.copy().pop() for cell in row if len(cell) == 1]
        known_set = set(known)
        if len(known_set) != len(known):
            raise SudokuError("Repeating Value")
        unknown = [cell for cell in row if len(cell) > 1]
        uknown_set = set(range(1, 10)).difference(known_set)

        # All known options are remove from the unknown sets:
        for cell in unknown:
            cell.difference_update(known_set)
            if not cell:
                raise SudokuError("Cell without possibilities")

        # Some more immidate deductions for speedup:
        for k in [1, 2]:
            for nums in it.combinations(uknown_set, k):
                option_counter = 0
                aditional_options = False
                cell_ref = []
                for cell in unknown:
                    if set(nums).issubset(cell):
                        option_counter += 1
                        cell_ref.append(cell)
                    elif set(nums).intersection(cell):
                        aditional_options = True
                if option_counter == k and not aditional_options:
                    for cell in cell_ref:
                        cell.clear()
                        cell.update(nums)




def solve(sudoku):
    # breakout if sudoko is unsolvable:
    try:
        sudoku.reduce_possibilities()
    except SudokuError:
        return
    # or complete solution have been found:
    if sudoku.is_solved:
        return sudoku

    # Recurse over following options:
    solution = None
    for next_guess in sudoku.guess():
        result = solve(next_guess)
        if result:
            if solution:
                raise SudokuError("More than one solution")
            else:
                solution = result

    return solution


def sudoku_solver(puzzle):
    sudoku = Sudoku.from_square(puzzle)
    solution = solve(sudoku)
    if solution is None:
        raise SudokuError("No valid solution is possible")
    else:
        return solution.square()
        
_______________________________________________
def sudoku_solver(puzzle):
    sudoku_dict = {}
    r = 'ABCDEFGHI'
    c = '123456789'
    for i in range(9):
        for j in range(9):
            sudoku_dict[r[i]+c[j]] = str(puzzle[i][j]) if puzzle[i][j] != 0 else c
    square = [[x+y for x in i for y in j] for i in ('ABC','DEF','GHI') for j in ('123','456','789')]
    peers = {}
    for key in sudoku_dict.keys():
        value = [i for i in square if key in i][0]
        row = [[x+y for x in i for y in j][0] for i in key[0] for j in c]
        col = [[x+y for x in i for y in j][0] for i in r for j in key[1]]
        peers[key] = set(x for x in value+row+col if x != key)
    for i in range(9):
        sudoku_dict = Check(sudoku_dict,peers)
    sudoku_dict = search(sudoku_dict, peers)
    solution = []
    for i in r:
        solution.append([])
        for j in c:
            solution[r.find(i)].append(int(sudoku_dict[i+j]))
    return solution

def Check(sudoku_dict, peers):
    for k,v in sudoku_dict.items():
        if len(v) == 1:
            for s in peers[k]:
                sudoku_dict[s] = sudoku_dict[s].replace(v,'')
                if len(sudoku_dict[s])==0:
                    return False
    return sudoku_dict

def search(sudoku_dict,peers):
    if Check(sudoku_dict,peers)==False:
        return False
    if all(len(sudoku_dict[s]) == 1 for s in sudoku_dict.keys()): 
        return sudoku_dict
    n,s = min((len(sudoku_dict[s]), s) for s in sudoku_dict.keys() if len(sudoku_dict[s]) > 1)
    res = []
    for value in sudoku_dict[s]:
        new_sudoku_dict = sudoku_dict.copy()
        new_sudoku_dict[s] = value
        ans = search(new_sudoku_dict, peers)
        if ans:
            res.append(ans)
    if len(res) > 1:
        raise Exception("Error")
    elif len(res) == 1:
        return res[0]
        
_______________________________________________
import copy
import itertools
import re
import sys

def sudoku_solver(puzzle):
  solution = solve(puzzle)
  
  if (solution is None or
      solution.invalid or
      not solution.solved or
      not solution.check_valid()):
    raise Exception('Invalid, you maggot burger!')
  
  solution2 = solve(puzzle,solution)
  if (solution2 is not None and
      not solution2.invalid and
      solution2.solved and
      solution2.check_valid()):
    raise Exception('Multiple solutions, you maggot burger!')
  
  return solution.board

def solve(board,original=None):
  if isinstance(board,list):
    board = Board(board)
  
  board.solve()
  
  if board.invalid: return None
  if board.solved:
    if original is None or board != original:
      return board
    else:
      return None
  
  empty,empty_i = board.min_empty()
  
  for candidate in empty.candidates:
    guess = Board(board)
    guess.set_cell(empty,candidate,empty_i)
    
    solution = solve(guess,original)
    if solution is not None: return solution
  
  return None

# 1 = not a candidate; 0 = a candidate.
# The binary's place is the number, so there are 9 places.
# 
# For example: 101010101
#              987654321
# This means [2,4,6,8] are candidates for this cell.
class Cell:
  ALL_BIT_CANDIDATES = 0
  NO_BIT_CANDIDATES = 511 # 111111111
  
  def __init__(self,x,y):
    self.bit_candidates = self.ALL_BIT_CANDIDATES
    self.candidates = set()
    self.x = x
    self.y = y
  
  def __eq__(self,other):
    return self.x == other.x and self.y == other.y
  
  def __hash__(self):
    return hash((x,y))
  
  def sole_candidate(self):
    self.candidates = set()
    result = 0
    
    for i in range(9):
      if (self.bit_candidates & (1 << i)) == 0:
        self.candidates.add(i + 1)
    
    if len(self.candidates) == 1:
      for result in self.candidates: break
    
    return result

class Board:
  def __init__(self,board):
    self.board = None
    self.cached_hash = None
    self.empties = []
    
    self.bit_blocks = []
    self.bit_columns = []
    self.bit_rows = []
    
    if isinstance(board,list):
      self.board = copy.deepcopy(board)
      self.invalid = False
      self.solved = False
      self.solved_cell = False
      
      for i in range(9):
        self.bit_blocks.append(0)
        self.bit_columns.append(0)
        self.bit_rows.append(0)
      
      for y in range(9):
        for x in range(9):
          num = self.board[y][x]
          
          if num == 0:
            self.empties.append(Cell(x,y))
          else:
            bit_num = 1 << (num - 1)
            
            self.bit_blocks[self.block_i(x,y)] |= bit_num
            self.bit_columns[x] |= bit_num
            self.bit_rows[y] |= bit_num
    else:
      self.board = copy.deepcopy(board.board)
      self.cached_hash = board.cached_hash
      self.empties = copy.deepcopy(board.empties)
      self.invalid = board.invalid
      self.solved = board.solved
      self.solved_cell = board.solved_cell
      
      for i in range(9):
        self.bit_blocks.append(copy.deepcopy(board.bit_blocks[i]))
        self.bit_columns.append(copy.deepcopy(board.bit_columns[i]))
        self.bit_rows.append(copy.deepcopy(board.bit_rows[i]))
  
  def __eq__(self,other):
    return self.board == other.board
  
  def __hash__(self):
    if self.cached_hash is None:
      self.cached_hash = hash(tuple(itertools.chain.from_iterable(self.board)))
    return self.cached_hash
  
  # Used for guesses/backtracking.
  def block_empty_count(self,x,y):
    bit_block = self.bit_block(x,y)
    count = 0
    
    for i in range(9):
      if (bit_block & (1 << i)) == 0:
        count += 1
    
    return count
  
  def check_valid(self):
    blocks = [set() for y in range(9)]
    columns = [set() for y in range(9)]
    
    for y in range(9):
      for x in range(9):
        num = self.board[y][x]
        if num == 0: return False
        
        block = blocks[self.block_i(x,y)]
        if num in block: return False
        block.add(num)
        
        column = columns[x]
        if num in column: return False
        column.add(num)
        
        # Row
        if self.board[y].count(num) > 1: return False
    
    return True
  
  def end_solve(self):
    return self.invalid or self.solved
  
  # Used for guesses/backtracking.
  def min_empty(self):
    min_cell = None
    min_count = 11
    min_index = -1
    
    for i,cell in enumerate(self.empties):
      self.sole_candidate(cell)
      count = self.block_empty_count(cell.x,cell.y)
      
      if count < min_count:
        min_cell = cell
        min_count = count
        min_index = i
    
    return (min_cell,min_index)
  
  def sole_candidate(self,cell):
    cell.bit_candidates |= self.bit_block(cell.x,cell.y)
    cell.bit_candidates |= self.bit_columns[cell.x]
    cell.bit_candidates |= self.bit_rows[cell.y]
    
    return cell.sole_candidate()
  
  def solve(self):
    while True:
      self.solved_cell = False
      
      if self.solve_sole_candidates().end_solve(): return
      if self.solve_unique_candidates().end_solve(): return
      
      if not self.solved_cell: break
  
  def solve_cell(self,cell,index=None):
    if cell.bit_candidates == Cell.NO_BIT_CANDIDATES:
      self.invalid = True
      self.solved = False
      return False
    
    candidate = self.sole_candidate(cell)
    
    if candidate > 0:
      self.set_cell(cell,candidate,index)
      self.solved_cell = True
      return True
    
    return False
  
  def solve_sole_candidates(self):
    self.solved = True
    
    i = 0 # Inside the loop, we might delete empties
    while i < len(self.empties):
      cell = self.empties[i]
      
      if self.solve_cell(cell,i): continue
      if self.invalid: return self
      
      self.solved = False
      i += 1
    
    return self
  
  def solve_unique_candidates(self):
    block_uniques = Uniques()
    column_uniques = Uniques()
    row_uniques = Uniques()
    
    for i in range(Uniques.MAX_UNIQUES):
      block_uniques.init()
      column_uniques.init()
      row_uniques.init()
      
      for j in range(9):
        block_uniques.init_group(i)
        column_uniques.init_group(i)
        row_uniques.init_group(i)
    
    for cell in self.empties:
      self.sole_candidate(cell)
      
      for i in range(Uniques.MAX_UNIQUES):
        block_group = block_uniques.group(i,self.block_i(cell.x,cell.y))
        column_group = column_uniques.group(i,cell.x)
        row_group = row_uniques.group(i,cell.y)
        
        for combo in itertools.combinations(cell.candidates,i + 1):
          block_group.add_combo(combo,cell)
          column_group.add_combo(combo,cell)
          row_group.add_combo(combo,cell)
    
    if block_uniques.eliminate_candidates(): self.solved_cell = True
    if column_uniques.eliminate_candidates(): self.solved_cell = True
    if row_uniques.eliminate_candidates(): self.solved_cell = True
    
    return self
  
  def set_cell(self,cell,num,index=None):
    bit_num = 1 << (num - 1)
    
    self.bit_blocks[self.block_i(cell.x,cell.y)] |= bit_num
    self.bit_columns[cell.x] |= bit_num
    self.bit_rows[cell.y] |= bit_num
    self.board[cell.y][cell.x] = num
    self.cached_hash = None
    
    if index is None:
      try:
        self.empties.remove(cell)
      except ValueError:
        pass
    else:
      try:
        del self.empties[index]
      except IndexError:
        pass
  
  def bit_block(self,x,y):
    return self.bit_blocks[self.block_i(x,y)]
  
  def block_i(self,x,y):
    return x // 3 + (y // 3 * 3)

class UniqueCombo:
  def __init__(self):
    self.cells = []
    self.count = 0

class UniqueGroup:
  def __init__(self):
    self.combos = {}
  
  def add_combo(self,candidates,cell):
    combo = self.combos.get(candidates)
    
    if combo is None:
      combo = UniqueCombo()
      self.combos[candidates] = combo
    
    combo.cells.append(cell)
    combo.count += 1

# This is for unique, naked, and hidden candidates.
class Uniques:
  MAX_UNIQUES = 4 # 0 = singles; 1 = pairs; 2 = triplets; 3 = quads; etc.
  
  def __init__(self):
    self.uniques = []
  
  def init(self):
    self.uniques.append([])
  
  def init_group(self,i):
    self.uniques[i].append(UniqueGroup())
  
  def eliminate_candidates(self):
    eliminated = False
    
    # Singles
    for group in self.uniques[0]:
      for candidates,combo in group.combos.items():
        if combo.count == 1:
          # Should only be 1 cell
          bit_candidates = Cell.NO_BIT_CANDIDATES ^ (1 << (candidates[0] - 1))
          cell = combo.cells[0]
          
          # Avoid infinite loop
          if cell.bit_candidates != bit_candidates:
            cell.bit_candidates = bit_candidates
            eliminated = True
    
    # Pairs, triplets, quads, etc.
    for i in range(1,self.MAX_UNIQUES):
      for j,group in enumerate(self.uniques[i]):
        for candidates,combo in group.combos.items():
          k = i + 1 # k => 2 = pairs; 3 = triplets; 4 = quads; etc.
          
          # Example for pairs:
          #   If (2,4) == 2 and (2) == 2 and (4) == 2, then must only be (2,4).
          if combo.count == k:
            bit_candidates = Cell.NO_BIT_CANDIDATES
            is_valid = True
            sibling_bit_candidates = Cell.ALL_BIT_CANDIDATES
            
            for candidate in candidates:
              # Check singles
              if self.uniques[0][j].combos[(candidate,)].count != k:
                is_valid = False
                break
              
              bit_candidate = 1 << (candidate - 1)
              bit_candidates ^= bit_candidate
              sibling_bit_candidates |= bit_candidate
            
            if is_valid:
              # Naked candidates
              for cell in combo.cells:
                # Avoid infinite loop
                if len(cell.candidates) > k:
                  cell.bit_candidates = bit_candidates
                  eliminated = True
              
              # Hidden candidates
              for sibling_combo in self.uniques[0][j].combos.values():
                cell = sibling_combo.cells[0]
                
                # In the previous singles/nakeds/hiddens we could have eliminated all, so check if none
                if (cell.bit_candidates | sibling_bit_candidates) != Cell.NO_BIT_CANDIDATES:
                  old_bit_candidates = cell.bit_candidates
                  cell.bit_candidates |= sibling_bit_candidates
                  
                  # Avoid infinite loop
                  if cell.bit_candidates != old_bit_candidates:
                    eliminated = True
    
    return eliminated
  
  def group(self,i,j):
    return self.uniques[i][j]
_______________________________________________
from itertools import product


def sudoku_solver(grid, size=(3,3)):
    grids = []
    R, C = size
    N = R * C
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C)
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))

    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        grids += grid
    if len(grids) != 9:
        raise
    return grids
    

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y


def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()


def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols


def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)
_______________________________________________
GUESS_LIMIT = 2000
guess_count = 0

def sudoku_solver(puzzle):
    global guess_count
    guess_count = 0
    
    SOLUTIONS = []
    POSSIBLES = copy_board(puzzle)
    
    for i in range(0, 9):
        for j in range(0, 9):
            if POSSIBLES[i][j] == 0:
                excludes = get_row(POSSIBLES, i) + get_column(POSSIBLES, j) + get_section(POSSIBLES, i // 3 + (j // 3)*3)
                candidates = []
                for num in range(1, 10):
                    if num not in excludes:
                        candidates.append(num)
                        
                if len(candidates) == 1:
                    number_is_known(POSSIBLES, i, j, candidates[0])
                else:
                    POSSIBLES[i][j] = candidates
        
    guess(SOLUTIONS, POSSIBLES)
        
    if (len(SOLUTIONS) == 1):
        return SOLUTIONS[0]
    
    raise Exception("Hello")


def guess(SOLUTIONS, puzzle):
    global guess_count
    
    if guess_count > GUESS_LIMIT: return
    if len(puzzle) == 0: return
    if len(SOLUTIONS) > 1: return
    
    guess_count += 1
    
    is_solved = True
    min_len = 999
    pos = []
    for i in range(0, 9):
        for j in range(0, 9):
            if isinstance(puzzle[i][j], list):
                is_solved = False
                if len(puzzle[i][j]) < min_len:
                    min_len = len(puzzle[i][j])
                    pos = [i, j]
    
    if is_solved:
        if is_valid(puzzle):
            SOLUTIONS.append(puzzle)
    else:
        for number in puzzle[pos[0]][pos[1]]:
            copy = copy_board(puzzle)
            number_is_known(copy, pos[0], pos[1], number)
            guess(SOLUTIONS, copy)

            
def is_valid_set(dataset):
    for i in range(0, 9):
        if (i+1) not in dataset: return False
    return True


def is_valid(puzzle):
    for i in range(0, 9):
        if not is_valid_set(get_row(puzzle, i)): return False
        if not is_valid_set(get_column(puzzle, i)): return False
        if not is_valid_set(get_section(puzzle, i)): return False
        
    return True


def copy_board(puzzle):
    result = []
    for i in range(0, 9):
        new_row = []
        for j in range(0, 9):
            new_row.append(puzzle[i][j])
        result.append(new_row)
    return result


def get_row(puzzle, i):
    result = []
    for j in range(0, 9):
        if not isinstance(puzzle[i][j], list):
            result.append(puzzle[i][j])
        else:
            result.append(0)
    return result


def get_column(puzzle, j):
    result = []
    for i in range(0, 9):
        if not isinstance(puzzle[i][j], list):
            result.append(puzzle[i][j])
        else:
            result.append(0)
    return result


def get_section(puzzle, i):
    result = []
    di = i % 3
    dj = i // 3
    for k in range(0, 3):
        for m in range(0, 3):
            if not isinstance(puzzle[3*di + k][3*dj + m], list):
                result.append(puzzle[3*di + k][3*dj + m])
            else:
                result.append(0)
    return result
               
    
def number_is_known(puzzle, i, j, value):
    puzzle[i][j] = value
    remove_duplicates(puzzle, i, j)
    
    
def remove_duplicates(puzzle, i, j):
    if len(puzzle) == 0: return
    
    value = puzzle[i][j]
    for k in range(0, 9):
        remove_row_duplicates(puzzle, i, j, k, value)
        remove_column_duplicates(puzzle, i, j, k, value)
    
    remove_section_duplicates(puzzle, i, j, value)
    
    
def remove_row_duplicates(puzzle, i, j, k, value):
    if len(puzzle) == 0: return
    if k == j: return
    if puzzle[i][k] == value:
        puzzle.clear()
        return
    if isinstance(puzzle[i][k], list):
        new_candidates = []
        for num in puzzle[i][k]:
            if num != value:
                new_candidates.append(num)
                
        if len(new_candidates) == 1:
            puzzle[i][k] = new_candidates[0]
            remove_duplicates(puzzle, i, k)
        else:
            puzzle[i][k] = new_candidates
            

def remove_column_duplicates(puzzle, i, j, k, value):
    if len(puzzle) == 0: return
    if k == i: return
    if puzzle[k][j] == value:
        puzzle.clear()
        return
    if isinstance(puzzle[k][j], list):
        new_candidates = []
        for num in puzzle[k][j]:
            if num != value:
                new_candidates.append(num)
                
        if len(new_candidates) == 1:
            puzzle[k][j] = new_candidates[0]
            remove_duplicates(puzzle, k, j)
        else:
            puzzle[k][j] = new_candidates
            
            
def remove_section_duplicates(puzzle, i, j, value):
    if len(puzzle) == 0: return
    di = i // 3
    dj = j // 3
    
    for k in range(0, 3):
        for m in range(0, 3):
            if len(puzzle) == 0: return
            candidates = puzzle[3*di + k][3*dj + m]
            if isinstance(candidates, list):
                new_candidates = []
                for num in candidates:
                    if num != value:
                        new_candidates.append(num)
                
                if len(new_candidates) == 1:
                    puzzle[3*di + k][3*dj + m] = new_candidates[0]
                    remove_duplicates(puzzle, 3*di + k, 3*dj + m)
                else:
                    puzzle[3*di + k][3*dj + m] = new_candidates
            elif 3*di + k != i and 3*dj + m != j and candidates == value:
                puzzle.clear()
                return
_______________________________________________
class Guess:
    squares = [[],[],[],[],[],[],[],[],[]];
    columns = [[],[],[],[],[],[],[],[],[]];
    rows    = [[],[],[],[],[],[],[],[],[]];
    def __init__(self):
        self.squares = [[],[],[],[],[],[],[],[],[]];
        self.columns = [[],[],[],[],[],[],[],[],[]];
        self.rows    = [[],[],[],[],[],[],[],[],[]];
        self.solution = [[],[],[],[],[],[],[],[],[]];
        for k in range(9):
            for item in self.squares:
                item.append(True);
            for item in self.columns:
                item.append(True);
            for item in self.rows:
                item.append(True);  
            for item in self.solution:
                item.append(0); 
    def find(self, cells, index):
    
        if(len(cells) <= index):
            answer = self.solution.copy();
            for i in range(9):
                answer[i] = answer[i].copy();
            return answer;
        first = cells[index];
        for c in first.values:
            c_1 = c - 1;
            if(self.rows[first.i][c_1] and self.columns[first.j][c_1] and  self.squares[first.q][c_1]):
                self.rows[first.i][c_1] = False;
                self.columns[first.j][c_1] = False;
                self.squares[first.q][c_1] = False;
                self.solution[first.i][first.j] = c;
                
                subanswer = self.find(cells, index + 1);
                if(len(subanswer)>1):
                    return subanswer;     
            
                self.rows[first.i][c_1] = True;
                self.columns[first.j][c_1] = True;
                self.squares[first.q][c_1] = True;

        return [];
class Cell:
    i=None
    j=None
    values=None
    row=None
    column=None
    square=None
    def __init__(self, inputValues, row, column, square, i, j):
        self.values = inputValues;
        self.row = row;
        self.column= column;
        self.square = square;
        
        row.append(self);
        column.append(self);
        square.append(self);
        self.i = i;
        self.j = j;
        self.q = 3*(i//3)+j//3;
    def forOne(self):
        changed = False;

        value = list(self.values)[0];
        changed = self.removeFrom(value, self.row) or changed;
        changed = self.removeFrom(value, self.column) or changed;
        changed = self.removeFrom(value, self.square) or changed;
        return changed;
    def removeFrom(self, value, target):
        changed = False;
        for item in target:
            if (item != self):
                changed = item.remove(value) or changed;
        return changed;
    
    def remove(self, value):
        changed = False;
        if (value in self.values):
            self.values.remove(value);
            if(len(self.values) == 1):
                self.forOne();
            changed = True;
        return changed;
class Field:
    squares = [[],[],[],[],[],[],[],[],[]];
    columns = [[],[],[],[],[],[],[],[],[]];
    rows    = [[],[],[],[],[],[],[],[],[]];
    initOnes = [];

    def __init__(self, puzzle):
        self.squares  =  [[],[],[],[],[],[],[],[],[]];
        self.columns  =  [[],[],[],[],[],[],[],[],[]];
        self.rows     =  [[],[],[],[],[],[],[],[],[]];
        self.initOnes = [];
        initOnes = [];
        rIndex = 0;
        for inputRow in puzzle:
            cIndex = 0;
            for inputCell in inputRow: 
                if (inputCell == 0):
                    Cell(set(range(1,10)), self.rows[rIndex], self.columns[cIndex], self.squares[3*(rIndex//3)+cIndex//3], rIndex, cIndex);
                else:
                    self.initOnes.append(Cell(set([inputCell]), self.rows[rIndex], self.columns[cIndex], self.squares[3*(rIndex//3)+cIndex//3], rIndex, cIndex));
                cIndex=cIndex+1;
            rIndex=rIndex+1;
    def reduceVariants(self):
        for item in self.initOnes:
            item.forOne();
        changed = True
        while (changed):
            changed = False
            changed = self.findSinglePlacedNumbers(self.rows) or changed;
            changed = self.findSinglePlacedNumbers(self.squares) or changed;
            changed = self.findSinglePlacedNumbers(self.columns) or changed;

                
    def solve(self):
        cells = [];
        for row in self.rows:
            cells = cells+row;
    
        guess = Guess();
        answer = guess.find(cells, 0);
        cells.reverse();
        for item in cells:
            item.values = list(item.values)
            item.values.reverse()
        guess = Guess();
        answer2 = guess.find(cells, 0);
        if(len(answer) == 0):
            raise NameError('Not Founded!')
        else:
            for i in range(9):
                for j in range(9):
                    if(answer[i][j] != answer2[i][j]):
                        raise NameError('More than one solution!');
            return answer
        
    def findSinglePlacedNumbers(self, targets):
        changed = False;
        for number in range(1,10):
            for target in targets:
                items = []
                for item in target:
                    if(number in item.values):
                        items.append(item)
                if(len(items) == 1 and len(items[0].values)>1):
                        changed = True
                        items[0].values.clear()
                        items[0].values.add(number)
                        items[0].forOne()
        return changed            
def validation(puzzle):
    if(len(puzzle)!=9):
        raise NameError('Wrong row Number!')
    for row in puzzle:
        if(len(row)!=9):
            raise NameError('Wrong row length!')
        for i in row:
            if (not i in range(10)):
                raise NameError('Wrong input!')
def sudoku_solver(puzzle):
    validation(puzzle)
    
    field = Field(puzzle);
    field.reduceVariants();
   
    return field.solve();
_______________________________________________
NO_REMAINING_CELLS = -1

class InvalidPuzzleError(Exception):
    pass

class SudokuSolver():
    """
    This Sudoku solver uses a customly designed CSP solving algorithm, 
    specifically for Sudoku. It requires a string of 81 characters, which
    represents the board.
    """

    def __init__(self, puzzle):
        """
        Initializes the board and the possible values for each cell.
        A "neighbours" look up table is also created. This is used to
        get all the neighbouring cells for a cell, that share the same
        constraints.
            board: the board is a list with 81 entries, one for
                   each cell.
            cells: contains 81 lists of possible values that can
                   be used for that cell.
            neighbours: contains 81 lists all the neighbours for
                        the indexed cell. Neighbours are defined as
                        the cells that share the same constraints.
        """
        self.board = [0] * 81
        self.allowed_values = [list(range(1, 10)) for _ in range(81)]
        self.assignments = 0
        self.initialize_neighbours()
        self.initialize_board(puzzle)
        self.solutions = []

    def initialize_neighbours(self):
        """
        Initializes the neighbours list which holds the neighbours
        for each cell.
        """
        self.neighbours = []
        squares = [
            [ 0,  1,  2,  9, 10, 11, 18, 19, 20], 
            [ 3,  4,  5, 12, 13, 14, 21, 22, 23],
            [ 6,  7,  8, 15, 16, 17, 24, 25, 26],
            [27, 28, 29, 36, 37, 38, 45, 46, 47],
            [30, 31, 32, 39, 40, 41, 48, 49, 50],
            [33, 34, 35, 42, 43, 44, 51, 52, 53],
            [54, 55, 56, 63, 64, 65, 72, 73, 74],
            [57, 58, 59, 66, 67, 68, 75, 76, 77],
            [60, 61, 62, 69, 70, 71, 78, 79, 80]
        ]
        for cell in range(81):
            self.neighbours.append([])
            self.neighbours[cell] += list(range(9 * (cell // 9), 
                                                9 * (cell // 9) + 9))
            self.neighbours[cell] += list(range(cell % 9, 9 * 9, 9))
            for square in squares:
                if cell in square:
                    self.neighbours[cell] += square
                    break
            while cell in self.neighbours[cell]:
                self.neighbours[cell].remove(cell)

    def initialize_board(self, puzzle):
        """
        Assign the initial puzzle values to the board. 
        If an assignment of a value fails, then the puzzle
        is invalid, throws a InvalidPuzzleError.
        """
        for cell in range(81):
            if '1' <= puzzle[cell] <= '9':
                value = int(puzzle[cell])
                if not self.assign(cell, value, []):
                    raise InvalidPuzzleError()

    def assign(self, cell, value, removed_values):
        """
        Assign a value to a cell. It will return a list of tuples
        with all the removed values from all the cells. If it fails,
        the unassign(...) method must still be called to restore
        the removed values.
        """
        self.assignments += 1
        if value not in self.allowed_values[cell]:
            return False
        self.board[cell] = value
        for allowed_value in list(self.allowed_values[cell]):
            removed_values.append((cell, allowed_value))
            self.allowed_values[cell].remove(allowed_value)
        for neighbour in self.neighbours[cell]:
            if value in self.allowed_values[neighbour]:
                removed_values.append((neighbour, value))
                self.allowed_values[neighbour].remove(value)
                if self.assignments < 81 and not self.allowed_values[neighbour]:
                    return False
        return True

    def unassign(self, cell, removed_values):
        """
        Unassign a value from a cell. It also requires all the removed
        values from the assign(...) method, which is used to restore
        all the values that have been removed from the neighbours.
        """
        self.assignments -= 1
        self.board[cell] = 0
        for cell, removed_value in removed_values:
            self.allowed_values[cell].append(removed_value)

    def next_cell(self):
        """
        Returns the next cell that should be assigned. The next cell is
        the cell which has the minimum values remaining that can be assigned.
        The minimum value heuristic ensures the search space is reduced as
        quickly as possible, to fail early.
        """
        min_cell, min_values = (NO_REMAINING_CELLS, 10)
        for cell in range(81):
            if not self.board[cell]:
                num_values = len(self.allowed_values[cell])
                if num_values < min_values:
                    min_values = num_values
                    min_cell = cell
        return min_cell

    def search(self):
        """
        Goes through each cell, and assigns the possible values
        to solve the puzzle.
        """
        cell = self.next_cell()
        if cell == NO_REMAINING_CELLS:
            self.solutions.append(list(self.board))
            return False
        for value in self.allowed_values[cell]:
            removed_values = []
            success = self.assign(cell, value, removed_values)
            if success:
                if self.search():
                    return True
            self.unassign(cell, removed_values)
        return False

    def solve(self):
        """
        Solve the puzzle. If it raises an InvalidPuzzleError then
        the puzzle has no solution.
        """
        self.search()
        print(self.solutions)
        if len(self.solutions) == 1:
            self.board = self.solutions[0]
        else:
            raise InvalidPuzzleError()

def board2d_to_chars(puzzle):
    return "".join(["".join(map(str, row)) for row in puzzle])

def chars_to_board2d(chars):
    puzzle = []
    for i in range(0, 81, 9):
        puzzle.append(list(map(int, list(chars[i:i+9]))))
    return puzzle
        
def sudoku_solver(puzzle):
    string = board2d_to_chars(puzzle)
    if len(string) != 81:
        raise ValueError()
    for c in string:
        if not '0' <= c <= '9':
            raise ValueError()
    solver = SudokuSolver(string)
    solver.solve()
    return chars_to_board2d(solver.board)
