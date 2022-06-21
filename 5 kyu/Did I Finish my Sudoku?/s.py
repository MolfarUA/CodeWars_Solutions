53db96041f1a7d32dc0004d2


import numpy as np
def done_or_not(aboard): #board[i][j]
  board = np.array(aboard)

  rows = [board[i,:] for i in range(9)]
  cols = [board[:,j] for j in range(9)]
  sqrs = [board[i:i+3,j:j+3].flatten() for i in [0,3,6] for j in [0,3,6]]
  
  for view in np.vstack((rows,cols,sqrs)):
      if len(np.unique(view)) != 9:
          return 'Try again!'
  
  return 'Finished!'
________________________________
correct = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def done_or_not(board): # board[i][j]
    # check rows
    for row in board:
        if sorted(row) != correct:
            return "Try again!"
    
    # check columns
    for column in zip(*board):
        if sorted(column) != correct:
            return "Try again!"
    
    # check regions
    for i in range(3):
        for j in range(3):
            region = []
            for line in board[i*3:(i+1)*3]:
                region += line[j*3:(j+1)*3]
            
            if sorted(region) != correct:
                return "Try again!"
    
    # if everything correct
    return "Finished!"
________________________________
def done_or_not(board):
  rows = board
  cols = [map(lambda x: x[i], board) for i in range(9)]
  squares = [
    board[i][j:j + 3] + board[i + 1][j:j + 3] + board[i + 2][j:j + 3]
      for i in range(0, 9, 3)
      for j in range(0, 9, 3)]
    
  for clusters in (rows, cols, squares):
    for cluster in clusters:
      if len(set(cluster)) != 9:
        return 'Try again!'
  return 'Finished!'
________________________________
from operator import add
from itertools import product
from numpy import matrix

blocks = ((0, 3), (3, 6), (6, 9))
valid_digits = {1, 2, 3, 4, 5, 6, 7, 8, 9}


def block(x, y, m):
    return [sub[x[0]:x[1]] for sub in m[y[0]:y[1]]]

def flat(m):
    return matrix(m).flatten().tolist()[0]


def validValues(board):
    return set(flat(board)) == valid_digits


def validRows(board):
    return all(validValues(row) for row in board)


def validColumns(board):
    return validRows(zip(*board))


def validBlocks(board):
    return all(validValues(flat(block(x, y, board))) for x, y in product(blocks, blocks))


def validSolution(board):
    return all(func(board) for func in (validValues, validRows, validColumns, validBlocks))


def done_or_not(board):
    if validSolution(board):
        return 'Finished!'
    return 'Try again!'
________________________________
from math import sqrt, modf

class Sudoku(object):

    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.length = len(sudoku)
        self.valid = range(1,self.length+1)
        self.cant_quarter, self.quarter = modf(sqrt(self.length))
    
    def is_valid(self):
        if self.cant_quarter: return False
        try:   
            return all(
                [all(map(
                    lambda z: type(z) is int,
                    sum(self.sudoku,[])
                ))] +
                [all(map(
                    lambda z: self.valid == sorted(z),
                    self.sudoku
                ))] +
                [all(map(
                    lambda z: self.valid == sorted(z),
                    [[self.sudoku[x][y] for x in xrange(self.length)]
                        for y in xrange(self.length)]
                ))] +
                [all(map(
                    lambda z: self.valid == sorted(z),
                    sum([[sum([[self.sudoku[m+y][n+x]
                    for m in xrange(int(self.quarter))]
                    for n in xrange(int(self.quarter))],[])
                    for y in xrange(0,self.length,int(self.quarter))]
                    for x in xrange(0,self.length,int(self.quarter))],[])
                ))]
            )
        except: return False

def done_or_not(board): #board[i][j]
  s = Sudoku(board)
  return 'Finished!' if s.is_valid() else 'Try again!'
________________________________
def done_or_not(board: list[[int, ...], [int, ...]]) -> str:
    if len(board) != 9:
        return 'Try again!'
    squares = [[board[k+i][m+j] for i in range(3) for j in range(3)] for k in range(0, 7, 3) for m in range(0, 7, 3)]
    for i, row in enumerate(board):
        col = [board[j][i] for j in range(9)]
        if len(set(row)) + len(set(col)) + len(set(squares[i])) != 27 or sum(row) + sum(col) + sum(squares[i]) != 135:
            return 'Try again!'
    return 'Finished!'
________________________________
def done_or_not(board): #board[i][j]
    valid = list(range(1,10))
    
    for j in range(9):
        column=[]
        
        for i in range(9):
            column.append(board[i][j])
                        
            if list(set(board[i]))!=valid:
                return "Try again!"
            
        column.sort()
        if column!=valid:
            return "Try again!" 
                
    n=0        
    while n < 9:
        m=0
        while m < 9:       
            cell=[]
        
            for i in range(n,n+3):
                for j in range(m,m+3):
                    cell.append(board[i][j])
            
            if list(set(cell))!=valid:
                return "Try again!"

            m+=3
        n+=3
        
    return 'Finished!'
________________________________
def row_and_column_creator(board):
    rows = board
    columns = [[], [], [], [], [], [], [], [], []]
    for i in board:
        count = 0
        for j in i:
            columns[count].append(j)
            count += 1
    return rows, columns



def row_and_column_checker(rows, columns):
    solution = True
    for column in columns:
        for y in column: 
            if column.count(y) > 1 or y == 0:
                solution = False
            if rows[columns.index(column)].count(y) > 1:
                solution = False
    return solution

    

def compare_square_counts(square_count1, square_count2):
    #square_count1, square_count2 = sector_adjuster(sector, square_count1, square_count2)
    if square_count2 == 1:
        square = 1
    elif square_count2 == 2:
        square = 2
    elif square_count2 == 3:
        square = 3
    
    if square_count1 == 1:
        pass
    if square_count1 == 2:
        square += 3
    if square_count1 == 3:
        square += 6
    
    return square
    
    


def square_creator(rows):
    square_count1 = 1
    square_count2 = 1
    square_list = [[], [], [], [], [], [], [], [], []]
    for i in rows:
        if i == rows[0] or i == rows[1] or i == rows[2]:
            square_count1 = 1
        elif i == rows[3] or i == rows[4] or i == rows[5]:
            square_count1 = 2
        elif i == rows[6] or i == rows[7] or i == rows[8]:
            square_count1 = 3
        for j in i:
            if j == i[0] or j == i[1] or j == i[2]:
                square_count2 = 1
                square = compare_square_counts(square_count1, square_count2)
                square -= 1
                square_list[square].append(j)
            elif j == i[3] or j == i[4] or j == i[5]:
                square_count2 = 2
                square = compare_square_counts(square_count1, square_count2)
                square -= 1
                square_list[square].append(j)
            elif j == i[6] or j == i[7] or j == i[8]:
                square_count2 = 3
                square = compare_square_counts(square_count1, square_count2)
                square -= 1
                square_list[square].append(j)
    return square_list

    
def square_checker(rows):
    square_list = square_creator(rows)
    solution2 = True
    for square in square_list:
        for y in square: 
            if square.count(y) > 1:
                solution2 = False
    return solution2



def done_or_not(board): 
    rows, columns = row_and_column_creator(board)
    solution = row_and_column_checker(rows, columns)
    solution2 = square_checker(rows)
    
    if solution == False or solution2 == False:
        return "Try again!"
    
    else:
        return "Finished!"
________________________________
def done_or_not(board): 
    test = {1,2,3,4,5,6,7,8,9}
    count = 0
    while(count<27):
        for i in range(9):
            row = set(board[i])
            if test == row:
                count += 1
            elif test != row:
                return 'Try again!'
                break
        for j in range(9):
            col = set()
            for k in range(9):
                ele = board[k][j]
                col.add(ele)
            if test == col:
                count+=1
            elif test != col:
                return 'Try again!'
                break
        for r in range(0,9,3):
            for c in range(0,9,3):
                reg = set()
                for n in range(r,r+3):
                    for m in range(c,c+3):
                        ele = board[n][m]
                        reg.add(ele)
                if test == reg:
                    count+=1
                elif test != reg:
                    return 'Try again!'
                    break
                        
    return 'Finished!'
