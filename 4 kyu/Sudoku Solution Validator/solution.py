import numpy as np

def valid_solution(board):
    grid=np.array(board)
    for i in range(9):
        j, k = (i // 3) * 3, (i % 3) * 3
        if len(set(grid[i,:])) != 9 or len(set(grid[:,i])) != 9\
        	or len(set(grid[j:j+3, k:k+3].ravel())) != 9:
            return False
    return True
#####################
def validSolution(board):
    boxes = validate_boxes(board)
    cols = validate_cols(board)
    rows = validate_rows(board)
    return boxes and cols and rows

def validate_boxes(board):
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            nums = board[i][j:j+3] + board[i+1][j:j+3] + board[i+2][j:j+3]
            if not check_one_to_nine(nums):
                return False
    return True

def validate_cols(board):
    transposed = zip(*board)
    for row in transposed:
        if not check_one_to_nine(row):
            return False
    return True
    
def validate_rows(board):
    for row in board:
        if not check_one_to_nine(row):
            return False
    return True
            

def check_one_to_nine(lst):
    check = range(1,10)
    return sorted(lst) == check
#############
def validSolution(board):
    blocks = [[board[x+a][y+b] for a in (0, 1, 2) for b in (0, 1, 2)] for x in (0, 3, 6) for y in (0, 3, 6)]
    return not filter(lambda x: set(x) != set(range(1, 10)), board + zip(*board) + blocks)
############
correct = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def validSolution(board):
    # check rows
    for row in board:
        if sorted(row) != correct:
            return False
    
    # check columns
    for column in zip(*board):
        if sorted(column) != correct:
            return False
    
    # check regions
    for i in range(3):
        for j in range(3):
            region = []
            for line in board[i*3:(i+1)*3]:
                region += line[j*3:(j+1)*3]
            
            if sorted(region) != correct:
                return False
    
    # if everything correct
    return True
##############
def valid_solution(m):
    is_valid = lambda a: len(a) == 9 and all([i + 1 in a for i in range(9)])
    get_block_as_row = lambda n: [m[3 * (n / 3) + (i / 3)][(3 * n) % 9 + i % 3] for i in range(9)]
    return all([is_valid(r) for r in m]) and all([is_valid([r[i] for r in m]) for i in range(9)]) and all([is_valid(get_block_as_row(i)) for i in range(9)])

validSolution = valid_solution
#################
# Accessors
def get_row(board, row_index):
    return board[row_index]

def get_col(board, col_index):
    return [row[col_index] for row in board]

def get_subgrid(board, base_x, base_y):
    # Returns elements (array) in a 3x3 subgrid
    # base_x,base_y are the x,y coordinates of the top-left element in the 3x3 subgrid
    result = []
    for x in range(0, 3):
        for y in range(0, 3):
            result.append(board[base_x + x][base_y + y])
    return result

class InvalidSudokuSet(Exception):
    pass

def validate_9(arr, identifier="Group"):
    # Validates any 9 elements
    if len(arr) != 9:
        raise InvalidSudokuSet("{} has length {} (not 9): {}".format(identifier, len(arr), arr))

    for number in range(1, 10):
        if number not in arr:
            raise InvalidSudokuSet("{} is missing '{}': {}".format(identifier, number, arr))

def validate_dimensions(board):
    if len(board) != 9:
        raise InvalidSudokuSet("Board contains {} rows:\n{}".format(len(board), board))
    for row in board:
        if len(row) != 9:
            raise InvalidSudokuSet("Row does not have 9 columns:\n{}".format(board))

def validate_rows(board):
    for index in range(0, 9):
        validate_9(get_row(board, index), "Row")
        
def validate_columns(board):
    for index in range(0, 9):
        validate_9(get_col(board, index), "Column")

def validate_subgrids(board):
    for x in range(0, 3):
        for y in range(0, 3):
            subgrid = get_subgrid(board, x * 3, y *3)
            validate_9(subgrid, identifier="3x3 Subgrid")

def validSolution(board):
    try:
        validate_dimensions(board)
        validate_rows(board)
        validate_columns(board)
        validate_subgrids(board)
        
    except InvalidSudokuSet as e:
        print("Invalid board:\n{}\n".format(board))
        print(e)
        return False
    
    print("Valid board:\n{}".format(board))
    return True
#############################################################
from itertools import product

def validSolution(board):
    rows = board
    columns = map(list, zip(*board))
    blocks = [[board[i][j] for (i, j) in product(xrange(x, x+3), xrange(y, y+3))] for (x, y) in product((0, 3, 6), repeat=2)]
    
    return all(sorted(line) == range(1, 10) for lines in (rows, columns, blocks) for line in lines)
######################
def validSolution (board):
    valid = set(range(1, 10))
    
    for row in board:
        if set(row) != valid: return False
    
    for col in [[row[i] for row in board] for i in range(9)]:
        if set(col) != valid: return False
    
    for x in range(3):
        for y in range(3):
            if set(sum([row[x*3:(x+1)*3] for row in board[y*3:(y+1)*3]], [])) != valid:
                return False
    
    return True
######################
import numpy as np
from itertools import chain

nums = set(range(1, 10))

def validSolution(board):
    a = np.array(board)
    r = range(0, 9, 3)
    return all(set(v.flatten()) == nums for v in chain(a, a.T, (a[i:i+3, j:j+3] for i in r for j in r)))
#########################
def validSolution(board):
    for x in range(9):
        arr = [board[y][x] for y in range(9)]
        arr2 = [board[x][y] for y in range(9)]
        arr3 = [board[i][y] for y in range(((x%3)*3),(((x%3)*3)+3)) for i in range((int(x/3)*3),(int(x/3)*3)+3)]
        for i in range(9):
            if arr[i] in arr[(i+1):]: return False
            if arr2[i] in arr2[(i+1):]: return False
            if arr3[i] in arr3[(i+1):]: return False
    return True
########################
from itertools import chain

def validSolution(board):
    cols = zip(*board)
    squares = (chain(*(board[y+i][x:x+3] for i in range(3)))
               for x in (0, 3, 6) for y in (0, 3, 6))
    good_range = set(range(1, 10))
    return all(set(zone) == good_range for zone in chain(board, cols, squares))
#########################
def validSolution(board):
    correct = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # check rows
    for row in board:
        if sorted(row) != correct:
            return False

    for column in zip(*board):
        if sorted(column) != correct:
            return False

# check regions
    for i in range(3):
        for j in range(3):
            region = []
            for line in board[i*3:(i+1)*3]:
                region += line[j*3:(j+1)*3]
            if sorted(region) != correct:
                return False
# if everything correct
    return True
#################################
import numpy as np

def valid_solution(board):
    board = np.array(board)
    no_zeroes = not np.any(board == 0)
    rows = all([len(set(row)) == 9 for row in board])
    cols = all([len(set(col)) == 9 for col in board.T])
    squares = all([len(set(board[i:i + 3, j:j + 3].flatten())) == 9 for i in range(0,9,3) for j in range(0,9,3)])
    return no_zeroes and rows and cols and squares
##########################
def validSolution(board):
    column_list = []
    box_list = []
    column_list.extend([[board[x][y] for x in range(9)] for y in range(9)])
    box_list.extend([board[x][y:y+3] + board[x+1][y:y+3] + board[x+2][y:y+3] for y in range(0,9,3) for x in range(0,9,3)])
    for i in range(1,10):
        for row in board:
            if row.count(i) > 1:
                return False
        for col in column_list:
            if col.count(i) > 1:
                return False
        for bx in box_list:
            if bx.count(i) > 1:
                return False

    return True
#############################
def validSolution(board):
    return set(reduce(lambda x,y:x+y,board))==set(range(1,10)) and \
            all(len(set(x))==9 for x in board) and \
            all(len(set(x))==9 for x in map(list,zip(*board))) and \
            all(len(set(board[i/3*3][i%3*3:i%3*3+3]+board[i/3*3+1][i%3*3:i%3*3+3]+board[i/3*3+2][i%3*3:i%3*3+3]))==9 for i in range(0,9))
######################
def validSolution(board):

    correct = [1,2,3,4,5,6,7,8,9]
    
    for i in range(9):
        if not row(i, board) == col(i, board) == square(i, board) == correct:
            return False
            
    return True

def row(i, board):
    return sorted(board[i])

def col(i, board):
    return sorted(row[i] for row in board)

def square(i, board):
    
    rows = [x + 3*(i // 3) for x in range(3)]
    cols = [x + 3*(i %  3) for x in range(3)]        
    
    return sorted([board[x][y] for x in rows for y in cols])
#########################
r03, r09, r093 = range(0, 3), range(0, 9), range(0, 9, 3)
sets = (
    [[(r, c) for c in r09] for r in r09] +
    [[(r, c) for r in r09] for c in r09] +
    [[(r0 + r, c0 + c) for c in r03 for r in r03] for r0 in r093 for c0 in r093]
    )
sum19 = sum(range(1, 10))

def validSolution(board):
    return all(sum(board[r][c] for (r, c) in s) == sum19 for s in sets)
#########################
import numpy as np
def valid_solution(b):
    for j in range(2):
        arr = np.sum(b, j, dtype = np.uint8)
        for i in arr:
            if i != 45:
                return False
    for c in range(0,7,3):
        for r in range(0,7,3):
            if b[c][r] + b[c][r+1] + b[c][r+2] + b[c+1][r] + b[c+1][r+1] + b[c+1][r+2] + b[c+2][r] + b[c+2][r+1] + b[c+2][r+2] != 45:
                return False
    return True
############################
def validSolution(board):
    return (all(len(set(row)) == 9 for row in board)
        and all(len(set(column)) == 9 for column in zip(*board))
        and all(len(set(sum((board[i+k][j:j+3] for k in range(3)), []))) == 9 for i in range(0, 9, 3) for j in range(0, 9, 3)))
##########################
def validSolution(board):
    sumc=0
    counter=0
    square=0
    x=0
    if 0 in board:
        return False
    
    for c in range(len(board)):
        if sum(board[c]) !=45:
            return False
            break
            
    for c in range(len(board)):
        sumc=0
        for r in range(len(board)):
            sumc += board[r][c]
        if sumc != 45:
            return False
            break
            
    for a in range(6,-3,-3):
        square =0
        for c in range(x,len(board)-a): 
            for r in range(x,len(board)-a):
                square += board[c][r]
        if square != 45:
             return False
             break
        x +=3     
    return True
###############################
isOK = lambda x: set(x) == set(range(1,10))
def validSolution(mat):
    return all([isOK(i) for i in mat] + [isOK(k) for k in [[mat[j][i] for j in range(9)] for i in range(9)]]) and all([isOK(k) for k in [mat[3*i][j:j+3]+mat[3*i+1][j:j+3]+mat[3*i+2][j:j+3] for j in (0,3,6) for i in (0,1,2)]])
####################
def validSolution(board):

    flatten = lambda l: [e for s in l for e in s]
    complete = lambda l: set(l) == set(range(1,10))
    col = lambda i: [board[index][i] for index in range(9)]
    row = lambda i: board[i]
    
    if not all(complete(row(i)) for i in range(9)):
        return False
        
    if not all(complete(col(i)) for i in range(9)):
        return False
        
    for i, j in zip(range(0,9,3),range(0,9,3)):
        q = [s[i:i+3] for s in board[j:j+3]]
            
        if not complete(flatten(q)):
            return False
            
    return True
#########################
def validSolution(board):
    for line in board:
        if not valid(line):
            return False
            
    for j in xrange(9):
        group_digits = [board[i][j] for i in xrange(9)]
            
        if not valid(group_digits):
            return False
            
    for group_offset in xrange(9):
        group_i_offset = group_offset / 3
        group_j_offset = group_offset % 3
        
        group_digits = []
        for interior_offset in xrange(9):
            i = interior_offset / 3 + group_i_offset * 3
            j = interior_offset % 3 + group_j_offset * 3
            group_digits.append(board[i][j])
        if not valid(group_digits):
            return False    
    return True
    
    
def valid(group):
    return sum(group) == 45 and len(set(group)) == 9
############################
def valid_solution(board):
    board_ = [[board[j][i] for j in range(9)]for i in range(9)]
    board_1 = []

    for k in range(3):
        r = []
        for i in range(0, 3):
            for j in range(3*k, 3*k+3):
                r.append(board[i][j])
        board_1.append(r)
        r = []
        for i in range(3, 6):
            for j in range(3*k, 3*k+3):
                r.append(board[i][j])
        board_1.append(r)
        r = []
        for i in range(6, 9):
            for j in range(3*k, 3*k+3):
                r.append(board[i][j])
        board_1.append(r)
        
    if uni(board_) and uni(board_1):
        return True
    else:
        return False

def uni(lst):

    for i in lst:
        out = []
        for j in i:
            if j not in out:
                out.append(j)
        if len(out) != 9:
            break
        
    else:
        return True
