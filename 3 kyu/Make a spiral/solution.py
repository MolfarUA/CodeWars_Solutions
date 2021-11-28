def spiralize (size):
    matrix = list (map(lambda x: list (map(lambda y: 1 if (int(size + 1) / 2) % 2 == 1 else 0, range (0, size))), range (0, size)))
    spiral = 1
    for i in range (0, int (size / 2)):
        for u in range (0, size - i * 2):
            matrix [i][u+i] = spiral
            matrix [u+i][i] = spiral
            matrix [size - i - 1][u+i] = spiral
            matrix [u+i][size - i - 1] = spiral
            
            if size % 4 == 0:
                if i != int (size / 2) -1:
                    matrix [i+1][i] = 1 - spiral
            else:
                matrix[i+1][i] = 1 - spiral
        spiral = 1 - spiral
    return matrix
#############
def spiralize(size):
    # Make a snake
    spiral = [[1 - min(i,j,size-max(i,j)-1)%2 for j in xrange(size)] for i in xrange(size)]
    for i in xrange(size/2-(size%4==0)):
      spiral[i+1][i] = 1 - spiral[i+1][i]
    return spiral
##################
import numpy as np

def spiralize(size):
    if size == 0:
        return []
    if size == 1:
        return [[1]]
    if size == 2:
        return [[1,1],[0,1]]
    sp = np.zeros((size, size))
    sp[0, :] = 1
    sp[:, -1] = 1
    sp[-1, :] = 1
    sp[2:, :-2] = np.array(spiralize(size-2))[::-1,::-1]
    return sp.tolist()
  ###################
def spiralize(size):
    
    def on_board(x, y):
        return 0 <= x < size and 0 <= y < size
        
    def is_one(x, y):
        return on_board(x, y) and spiral[y][x] == 1
        
    def can_move():
        return on_board(x+dx, y+dy) and not (is_one(x+2*dx, y+2*dy) or is_one(x+dx-dy, y+dy+dx) or is_one(x+dx+dy, y+dy-dx))
    
    
    spiral = [[0 for x in range(size)] for y in range(size)]   
    x, y = -1, 0
    dx, dy = 1, 0
    turns = 0
    
    while (turns < 2):
        if can_move():
            x += dx
            y += dy
            spiral[y][x] = 1
            turns = 0
        else:
            dx, dy = -dy, dx
            turns += 1
    
    return spiral
  ########################
  def layer(spiral):
    """Wraps one extra layer around an existing spiral."""
    val = spiral[0][0]^1
    top = (2+len(spiral[0])) * [val]
    first = [val^1] + spiral[0] + [val]
    other = [ [val] + row + [val] for row in spiral[1:] ]
    return  [ top, first ] + other + [top]


def spiralize(size):
    """The snake is recursive."""
    a = [[1]]
    b = [[1, 1], [0,1]]
    c = [ [1,1,1], [0,0,1], [1,1,1]]
    d = [ [1,1,1,1], [0,0,0,1], [1,0,0,1], [1,1,1,1]]
    
    if size<5:
        return [d, a, b, c][size%4] if size else []
    
    return layer(layer(spiralize(size-4)))
  #######################
  def spiralize(size):
    if size <= 0:
        return []
    
    core = [ [[1,1,1,1], [0,0,0,1], [1,0,0,1], [1,1,1,1]], [[1]], [[1,1],[0,1]], [[1,1,1],[0,0,1],[1,1,1]] ][size%4]
    
    while len(core) < size:
        for x in [0,1]:
            core.insert(0, [ x for i in core[0] ] )
            core.append([ x for i in core[0] ])
            for line in core:
                line.insert(0, x)
                line.append(x)
            core[1][0] = int(not x)    
    
    return core
  ##########################################################################################################################
  d = [[[1,1,1,1,1],[0,0,0,0,1],[1,1,1,0,1],[1,0,0,0,1],[1,1,1,1,1]], # the 5*5 tool

     [[1,1,1,1,1,1],[0,0,0,0,0,1],[1,1,1,1,0,1],[1,0,0,1,0,1],[1,0,0,0,0,1],[1,1,1,1,1,1]], # the 6*6 tool

     [[1,1,1,1,1,1,1],[0,0,0,0,0,0,1],[1,1,1,1,1,0,1],[1,0,0,0,1,0,1],[1,0,1,1,1,0,1],[1,0,0,0,0,0,1],[1,1,1,1,1,1,1]], # the 7*7 tool

     [[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,1],[1,1,1,1,1,1,0,1],[1,0,0,0,0,1,0,1],[1,0,1,0,0,1,0,1],[1,0,1,1,1,1,0,1],[1,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1]]]
    # the 8*8 tool
    
def spiralize(number):

    array = [d[i-5] for i in range(5,9) if not(number-i)%4][0]
    
    while len(array)<number:
        array = [[1,1]+array[0]+[0,1]]+list(map(lambda x: [1,0]+x+[0,1],array[1:]))#increasing the sides: [1,1]+[1,0,1,0,1]+[0,1] = [1,1,1,0,1,0,1,0,1] 
        
        array = [[1 for _ in range(len(array)+4)],[0 for _ in range(len(array)+3)]+[1]]+\
                            array+[[1]+[0 for _ in range(len(array)+2)]+[1],[1 for _ in range(len(array)+4)]]
        # adding bigger 'outer-shell' arrays: 2 to the top, 2 to the bottom
    return array        

#                                                 ALGORITHM:

# The spirals with their length difference of 4 will always have the same structure:    ->
#(number 4 is important because the next sprial with the max size you can make inside another sprial is n-4 long)
#       1 1 1 1 1                                                                    1 1 1 1 1 1 1 1 1            
#               1                                                                                    1
#       1 1 1   1 so, this 5x5 matrix will be "the inner" part of a 9x9 matrix :     1 1 1 1 1 1 1   1
#       1       1                                                                    1           1   1      
#       1 1 1 1 1                                                                    1   1 1 1   1   1
#                                                                                    1   1       1   1
#                                                                                    1   1 1 1 1 1   1
#                                                                                    1               1
#            9x9                  "the frame" for 9x9                                    1 1 1 1 1 1 1 1 1 
#     1 1 1 1 1 1 1 1 1            1 1 1 1 1 1 1 1 1
#                     1                            1       the inner 5x5
#     1 1 1 1 1 1 1   1            1 1    -------- 1 -----> 1 1 1 1 1
#     1           1   1            1               1                1
#     1   1 1 1   1   1     ==     1               1    +   1 1 1   1
#     1   1       1   1            1               1        1       1
#     1   1 1 1 1 1   1            1               1        1 1 1 1 1
#     1               1            1               1
#     1 1 1 1 1 1 1 1 1            1 1 1 1 1 1 1 1 1

#        conclusion: so, by filtering the existing arrays, and adding new ones to them, in a while cycle, the result can be achieved
######################################################################################################################################
def spiralize(size):
    spiral = [[1]*size for _ in xrange(size)]
    def ok(y, x):
        return y < size and x < size and y >= 0 and x >= 0 and spiral[y][x]
    y, x, dy, dx = 1, -1, 0, 1
    while ok(y + dy, x + dx):
        if ok(y + 2*dy, x + 2*dx):
            y += dy
            x += dx
        else:
            dx, dy = dy*(2*dx-1), dx
        spiral[y][x] = 0
    return spiral
###############################
  def spiralize(size):
    j = [] if not size else [1] if size % 2 else ([3, 1] if size % 4 else [3, 3])
    for s in reversed(range(size, 2, -2)):
       j = [2**s-1] + map(lambda a, b, c: c or (a ^ (b << 1)), [2**s-1] * (s-2), j, [1]) + [2**s-1]
    return [map(int, ("{0:0>%db}" % size).format(row)) for row in j]
##########################
  def spiralize(size):
    spiral = [[0] * size for i in xrange(size)]
    for i in xrange(0, (size+1)/2, 2):
      for j in xrange(i, size - i):
        spiral[i][j] = spiral[j][i] = spiral[size-i-1][j] = spiral[j][size-1-i] = 1;
    for i in xrange(size/2-(size%4==0)):
      spiral[i+1][i] = 1 - spiral[i+1][i]
    return spiral
#############################
def spiralize(n):
    x , y = (0, 0)
    s = [[0 for i in range(n)] for j in range(n)]
    moves = [1, 0, -1, 0]
    for t in range(n):
        for i in range(n - 2 * max([0,(t-1)/2])):
            s[y][x] = 1
            x, y = (x + moves[t%4], y + moves[(t+3)%4])
        x, y = (x - moves[t%4], y - moves[(t+3)%4])
    return s
#######################
SPIRALS = {
           0: [],
           1: [[1]],
           
           2: [[1, 1],
               [0, 1]],
               
           3: [[1, 1, 1],
               [0, 0, 1],
               [1, 1, 1]],
               
           4: [[1, 1, 1, 1],
               [0, 0, 0, 1],
               [1, 0, 0, 1],
               [1, 1, 1, 1]]           
          }

def spiralize(size):
    if size in SPIRALS:
        return SPIRALS[size]
    spiral = [[1] + [0] * (size - 2) + [1] for x in range(size)]
    spiral[0]    = [1] * size
    spiral[-1]   = [1] * size
    spiral[1][0] = spiral[1][0] - 1
    spiral[2][1] = 1
    subspiral = spiralize(size - 4)
    for row in range(2, size - 2):
        spiral[row][2:-2] = subspiral[row - 2]
    SPIRALS[size] = spiral
    return spiral
#####################
def spiralize(size):
    canvas = [[0] * size for i in range(size)]
    length = size
    pos = [0, 0]
    dir = "E"
    for i in range(size):
        move = get_move(dir)
        for j in range(length):
            canvas[pos[0] + move[0] * j][pos[1] + move[1] * j] = 1
        pos[0] += move[0] * (length - 1)
        pos[1] += move[1] * (length - 1)
        if i != 0 and i % 2 == 0:
            length -= 2
        dir = turn_right(dir)
    return canvas

def get_move(dir):
    if dir == "E":
        return (0, 1)
    elif dir == "S":
        return (1, 0)
    elif dir == "W":
        return (0, -1)
    else:
        return (-1, 0)

def turn_right(dir):
    if dir == "E":
        return "S"
    elif dir == "S":
        return "W"
    elif dir == "W":
        return "N"
    else:
        return "E"
##############################
def spiralize(size):
    # Make a snake
    ret = [[0 for col in range(size)] for row in range(size)]
    up = 0
    left = 0
    right = size
    down = size
    while down - up > 0:
        for i in range(left,right):
            ret[up][i] = 1
        for i in range(up, down):
            ret[i][right-1] = 1
        up += 1
        if down - up < 2:
            break
        for i in range(left,right):
            ret[down-1][i] = 1
        up += 1
        if down - up < 2:
            break
        for i in range(up,down):
            ret[i][left] = 1
        left += 1
        down -= 2
        if left < right and down - up > 0:
            ret[up][left] = 1
        right -= 2
        left += 1     
        
    return ret
def spiralize(size):
    # Make a snake
    ret = [[0 for col in range(size)] for row in range(size)]
    up = 0
    left = 0
    right = size
    down = size
    while down - up > 0:
        for i in range(left,right):
            ret[up][i] = 1
        for i in range(up, down):
            ret[i][right-1] = 1
        up += 1
        if down - up < 2:
            break
        for i in range(left,right):
            ret[down-1][i] = 1
        up += 1
        if down - up < 2:
            break
        for i in range(up,down):
            ret[i][left] = 1
        left += 1
        down -= 2
        if left < right and down - up > 0:
            ret[up][left] = 1
        right -= 2
        left += 1     
        
    return ret
#######################################
def rotate180(arr):
    return [x[::-1] for x in arr[::-1]]

memo = {0:[], 1:[[1]], 2:[[1, 1], [0, 1]]}

def spiralize(size):
    global memo
    if size in memo: return memo[size]
    ans = rotate180(spiralize(size - 2))
    for i in xrange(0, len(ans) - 1):
        ans[i].extend([0, 1])
    ans[-1].extend([1, 1])
    ans = [[1] * size] + [[0] * (size - 1) + [1]] + ans
    memo[size] = ans
    return ans
##################
def spiralize(size):
    
    import numpy as np
    it = size - 1
    nparr = np.array(size*[size*[0]])
    
    ''' ROWS '''
    
    cont = 0
    for i in range(0,int(size/2)+1, 2):
        if i>0:
            cont = 1
        nparr[i][i-cont:size-i] = 1
        cont += 1
        
    for i in range(0,int(size/2), 2):
        nparr[size-1-i][i:size - i][::-1] = 1
        
    ''' COLUMNS '''
    
    for i in range(0,int(size/2),2):
        for j in range(2+i,size-i):
            nparr[j][i] = 1

    for i in range(0,int(size/2),2):
        for j in range(2+i,size-i):
            nparr[size-j][size-1-i] = 1
            
    if size%2 == 0:
        nparr[int(size/2)][int(size/2)-1] = 0
        
    return nparr.tolist()
