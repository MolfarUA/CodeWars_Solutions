import numpy as np

def valid_solution(board):
    grid=np.array(board)
    for i in range(9):
        j, k = (i // 3) * 3, (i % 3) * 3
        if len(set(grid[i,:])) != 9 or len(set(grid[:,i])) != 9\
        	or len(set(grid[j:j+3, k:k+3].ravel())) != 9:
            return False
    return True
