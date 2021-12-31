def sudoku(puzzle):
    global sudoku_puzzle
    sudoku_puzzle = puzzle
    sudoku_solver()
    return sudoku_puzzle

def sudoku_solver():
    for y in range(9):
        for x in range(9):
            if sudoku_puzzle[y][x] == 0:
                for _ in range(1,10):
                    if isvalid(_, sudoku_puzzle, y, x):
                        sudoku_puzzle[y][x] = _
                        sudoku_solver()
                        if iscompleted():
                            return
                        sudoku_puzzle[y][x] = 0
                return

def iscompleted():
    for _ in sudoku_puzzle:
        if 0 in _ : 
            return False
    return True 

def isvalid(num,puzzle, y, x):
    if num in puzzle[y]:
        return False
    for _ in puzzle:
        if _[x] == num:
            return False
    line_offset = (y // 3)*3
    column_offset = (x // 3)*3
    for line in [line_offset, line_offset + 1, line_offset + 2]:
        for column in [column_offset, column_offset + 1, column_offset + 2]:
            if puzzle[line][column] == num:
                return False
    return True
  
___________________________________________________
import itertools


def is_possible(p, x, y, number):
    # Check in column
    if p[y].count(number) != 0:
        return False
    # Check in row
    if [p[other_y][x] for other_y in range(9)].count(number) != 0:
        return False
    # Check in block
    if [
        p[y // 3 * 3][x // 3 * 3],
        p[y // 3 * 3 + 1][x // 3 * 3],
        p[y // 3 * 3 + 2][x // 3 * 3],
        p[y // 3 * 3][x // 3 * 3 + 1],
        p[y // 3 * 3 + 1][x // 3 * 3 + 1],
        p[y // 3 * 3 + 2][x // 3 * 3 + 1],
        p[y // 3 * 3][x // 3 * 3 + 2],
        p[y // 3 * 3 + 1][x // 3 * 3 + 2],
        p[y // 3 * 3 + 2][x // 3 * 3 + 2]
    ].count(number) != 0:
        return False
    else:
        return True


def sudoku(p):
    while 0 in itertools.chain(*p):
        for y, row in enumerate(p):
            for x, value in enumerate(row):
                if p[y][x] == 0:
                    for number in range(1, 10):
                        if is_possible(p, x, y, number):
                            possibilities_in_column = sum(is_possible(p, x, other_y, number) for other_y in range(9) if
                                                          other_y != y and p[other_y][x] == 0)
                            possibilities_in_row = sum(is_possible(p, other_x, y, number) for other_x in range(9) if
                                                       other_x != x and p[y][other_x] == 0)
                            possibilities_in_block = sum(is_possible(p, other_x, other_y, number) for other_y, other_x in [
                                (y // 3 * 3, x // 3 * 3),
                                (y // 3 * 3 + 1, x // 3 * 3),
                                (y // 3 * 3 + 2, x // 3 * 3),
                                (y // 3 * 3, x // 3 * 3 + 1),
                                (y // 3 * 3 + 1, x // 3 * 3 + 1),
                                (y // 3 * 3 + 2, x // 3 * 3 + 1),
                                (y // 3 * 3, x // 3 * 3 + 2),
                                (y // 3 * 3 + 1, x // 3 * 3 + 2),
                                (y // 3 * 3 + 2, x // 3 * 3 + 2)
                            ] if (other_y, other_x) != (y, x) and p[other_y][other_x] == 0)

                            if possibilities_in_column == 0 or possibilities_in_row == 0 or possibilities_in_block == 0:
                                p[y][x] = number
                                break
    return p

___________________________________________________
def sudoku(sodoku):
    class Cell:
        def __init__(self, row, col, block):
            self.row = row
            self.col = col
            self.block = block

    edges = [(0,0),(0,3),(0,6),
             (3,0),(3,3),(3,6),
             (6,0),(6,3),(6,6)]

    cells = [Cell(i,j,k)
         for k,e in enumerate(edges)
         for i in range(e[0],e[0]+3)
         for j in range(e[1],e[1]+3)]

    empty = {c: {1,2,3,4,5,6,7,8,9} for c in cells if sodoku[c.row][c.col] == 0}

    #for every cell that is zero remove all the values that can be excluded
    for c in cells:
        if sodoku[c.row][c.col] > 0:
            for e in empty:
                if e.block == c.block:
                    empty[e].discard(sodoku[c.row][c.col])
                if e.col == c.col:
                    empty[e].discard(sodoku[c.row][c.col])
                if e.row == c.row:
                    empty[e].discard(sodoku[c.row][c.col])
                
    counter = 1
    while counter > 0:
        counter = 0
        for ec in empty.copy():
            if len(empty[ec]) == 1:
                counter += 1
                sodoku[ec.row][ec.col] = next(iter(empty[ec]))
                empty.pop(ec, None)
                for e in empty:
                    if e.block == ec.block:
                        empty[e].discard(sodoku[ec.row][ec.col])
                    if e.col == ec.col:
                        empty[e].discard(sodoku[ec.row][ec.col])
                    if e.row == ec.row:
                        empty[e].discard(sodoku[ec.row][ec.col])
    return sodoku
  
___________________________________________________
def sudoku(puzzle):
    solve(puzzle)
    return puzzle

def solve(board):
    find_square = find_valid_square(board)
    if find_square == False:
        return True
    row, col = find_valid_square(board)
    for i in range(1,10):
        if validate(board, i, row, col):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0

    
def validate(board, num, row, col):
    region_x, region_y = row//3, col//3
    #check row
    for i in range(len(board)):
        if board[row][i] == num and i != col:
            return False
    #check col
    for i in range(len(board[0])):
        if board[i][col] == num and i != row:
            return False
    #check region
    for i in range(region_x*3, (region_x*3) + 3):
        for j in range(region_y*3, (region_y*3) + 3):
            if board[i][j] == num and i != row and j != col:
                return False
    return True



def print_sudoku(board):
    for i in range(len(board)):
        if i%3 == 0:
            print('- - - - - - - - - - - -')
        for j in range(len(board[0])):
            if j%3 == 0:
                print('|', end=" ")
            print(board[i][j], end=" ")
            if j == 8:
                print('\n')

def find_valid_square(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i,j)
    return False
  
___________________________________________________
def sudoku(puzzle):
    return solve(puzzle)


def check(grid, val, row, col):
    if val in grid[row]:
        return False
    if val in [r[col] for r in grid]:
        return False
    qrs, qcs = (row//3)*3, (col//3)*3  # start-coord of quadrant
    from itertools import chain
    if val in chain.from_iterable([r[qcs:qcs+3] for r in grid[qrs:qrs+3]]):
        return False
    return True


def next_free(grid):
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 0:
                return r, c
    return None


def solve(grid):
    pos = next_free(grid)
    if pos is None:
        return grid
    for val in range(1, 10):
        if check(grid, val, pos[0], pos[1]):
            grid[pos[0]][pos[1]] = val
            res = solve(grid)
            if res is None:
                grid[pos[0]][pos[1]] = 0
            else:
                return res
    return None
  
___________________________________________________
import numpy as np


def sudoku(puzzle):
    puzzle = np.array(puzzle)
    n_zeros = np.sum(puzzle == 0)
    full_set = set(range(1, 10))
    while n_zeros > 0:
        for y, row in enumerate(puzzle):
            for x, e in enumerate(row):
                if e == 0:
                    sols = full_set.difference(set.union(
                            set(puzzle[y//3*3:y//3*3+3, x//3*3:x//3*3+3].flatten()),
                            set(puzzle[:, x]),
                            set(puzzle[y])))
                    if len(sols) == 1:
                        puzzle[y, x] = sols.pop()
                        n_zeros -= 1
    return puzzle.tolist()
  
___________________________________________________
def sudoku(puzzle):
    lol,lom=[1,2,3,4,5,6,7,8,9],0
    for i in range(9):
        if i<3:
            cons=3
        elif i>=3 and i<6:
            cons=6
        else:
            cons=9
        for j in range(9):
            if j < 3:
                a = 3
            elif j >= 3 and j < 6:
                a = 6
            else:
                a = 9
            if puzzle[i][j]==0:
                list,list1=[],[]
                for k in range(9):
                    cos=puzzle[i][k]
                    sin=puzzle[k][j]
                    list.append(cos)
                    list.append(sin)
                for num in range(cons-3,cons):
                     for iter in range(a-3,a):
                         list.append(puzzle[num][iter])
                for num in lol:
                    if num not in list:
                        list1.append(num)
                if len(list1)==1:
                    puzzle[i][j]=list1[0]
    for pas in range(9):
        if 0 in puzzle[pas]:
            lom = 1
            break
    if lom == 0:
        return puzzle
    return sudoku(puzzle)
  
___________________________________________________
def check_piece(board, row, col):
    piece = board[row][col]
    if piece == 0:
        return True

    def check_row():
        counter = 0
        for i in board[row]:
            if i == piece:
                counter += 1
        if counter > 1:
            return False
        else:
            return True

    def check_col():
        counter = 0
        for i in range(0, 9):
            if board[i][col] == piece:
                counter += 1
        if counter > 1:
            return False
        else:
            return True

    def check_box():
        counter = 0
        new_row = (row // 3) * 3
        new_col = (col // 3) * 3
        for i in range(new_row, new_row + 3):
            for z in range(new_col, new_col + 3):
                if board[i][z] == piece:
                    counter += 1
        if counter > 1:
            return False
        else:
            return True

    if check_row() and check_box() and check_col():
        return True
    else:
        return False


def check_board(board):
    for i in range(0, 9):
        for z in range(0, 9):
            if check_piece(board, i, z) == False:
                return False
    return True
def find_next_slot(board,row,col):
    for i in range(row,9):
        for j in range(col,9):
            if board[i][j] == 0:
                return i, j
    for i in range(0,9):
        for j in range(0,9):
            if board[i][j] == 0:
                return i, j
    else:
        return -1, -1

def recurse(board, row, col,num):
    if num == 0 and recurse(board,row,col,1):
        return board
    if check_piece(board,row,col) == False:
        return False
    row, col = find_next_slot(board,row,col)
    if row == -1 and check_board(board):
        return True
    for i in range(1,10):
        board[row][col] = i
        if recurse(board,row,col,1):
            return True
        else:
            board[row][col] = 0





def sudoku(puzzle):
    return recurse(puzzle,0,0,0)
