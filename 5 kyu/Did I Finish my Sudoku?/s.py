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
