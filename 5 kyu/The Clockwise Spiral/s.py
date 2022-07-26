536a155256eb459b8700077e


def createSpiral(n):
    if not isinstance(n, int): return []
    d = iter(range(n ** 2))
    a = r = [[[x, y] for y in range(n)] for x in range(n)]
    while a:
        for x, y in a[0]: r[x][y] = next(d) + 1
        a = list(zip(*a[1:]))[::-1]
    return r
_________________________
def createSpiral(n):
    if not isinstance(n,int) or n<1:
        return []
    seq = list(range(1,n**2))
    arr = [[n**2]]
    while seq:
        l = len(arr)
        arr = [seq[-l:]] + list(map(list, zip(*arr[::-1])))
        seq = seq[:-l]
    return arr
_________________________
from collections import deque

def createSpiral(N):
    if type(N) != int or N < 0: return []
    
    ans = [[0]*N for i in range(N)]
    x, y = 0, 0
    moves = deque([(0,1), (1,0), (0,-1) , (-1,0)])
    
    for i in range(1, N**2+1):
        ans[x][y] = i
        if not ( 0 <= x+moves[0][0] < N and 0 <= y+moves[0][1] < N) or ans[ x+moves[0][0] ][ y+moves[0][1] ] != 0:
            moves.rotate(-1)
        x, y = x+moves[0][0], y+moves[0][1]
    return ans
_________________________
def create_spiral(n):
    if type(n) is not int: return []
    i, j, dir, result = 0, 0, 0, [[0]*n for _ in range(n)]
    for x in range(1, n*n+1):
        result[i][j] = x
        if dir == 0:
            if j == n-1 or result[i][j+1]:
                i, j, dir = i+1, j, 1
            else:
                j += 1
        elif dir == 1:
            if i == n-1 or result[i+1][j]:
                i, j, dir = i, j-1, 2
            else:
                i += 1
        elif dir == 2:
            if j == 0 or result[i][j-1]:
                i, j, dir = i-1, j, 3
            else:
                j -= 1
        else:
            if i == 0 or result[i-1][j]:
                i, j, dir = i, j+1, 0
            else:
                i -= 1
    return result
_________________________

def right_rotate(direction):
    if direction == [-1,0]:
        return [0,1], 'E'
    elif direction == [0,1]:
        return [1,0], 'S'
    elif direction == [1,0]:
        return [0,-1], 'W'
    return [-1,0], 'N'

def create_spiral(n):
    if not isinstance(n,int):
        return []
    final_spiral = []
    for i in range(n):
        final_spiral.append([0]*n)
    current_direction = [0,1]
    cardinal_point = 'E'
    row, col = 0,0
    factor = 1
    for count in range(n**2):
        final_spiral[row][col] = count + 1

        row = current_direction[0] + row
        col = current_direction[1] + col

        if (cardinal_point == 'E' and col == (n-factor)) or \
                (cardinal_point == 'W' and col == (factor-1)) :

            current_direction, cardinal_point = right_rotate(current_direction)

        elif (cardinal_point == 'S' and row == (n-factor)) or \
                (cardinal_point == 'N' and row == factor) :
            current_direction, cardinal_point = right_rotate(current_direction)
            if cardinal_point == 'E':
                factor+=1

    return final_spiral
_________________________
def createSpiral(n):
    if not isinstance(n, int): return []
    x, y, i, dx, dy = 0, 0, 1, 1, 0
    grid = [[0] * n for _ in range(n)]
    for r in range(n-1, -1, -2):
        if not r: grid[y][x] = i
        for _ in range(4):
            for _ in range(r):
                grid[y][x] = i # [y][x] for cw, [x][y] for ccw
                x += dx; y += dy; i += 1
            dx, dy = -dy, dx
        x += 1; y += 1
    return grid
_________________________
class Table(dict):
    def __init__(self, N):
        self.size = N
        self.cursor = 0
        self.direction = 1
        for x in range(N):
            self[-1+x*1j] = self[N+x*1j] = -1
            self[x-1j] = self[x+N*1j] = -1
    __getitem__ = dict.get
    def put(self, num):
        if self[self.cursor]: 
            return
        self[self.cursor] = num
        moving = self.cursor + self.direction
        if self[moving]:
            self.direction *= 1j
            moving = self.cursor + self.direction
        self.cursor = moving
        return True
    @property
    def as_list(self):
        return [ [self[x+y*1j] for x in range(self.size)]
                                 for y in range(self.size) ]

def createSpiral(N):
    if not isinstance(N,int) or N<1: 
        return []
    table = Table(N)
    num = 1
    while table.put(num):
        num += 1
    return table.as_list
_________________________
# Tuples used to describe «direction», for example (1, 0) for left-to-right
# Returns next direction, dictionary used to change directions

rotate = {
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (1, 0),
}

def create_spiral(n):
    # Annoying test case
    if not isinstance(n, int): return []
    
    # Sequence of how many cells to fill before next turn
    # For 5x5, this is 5, 4, 4, 3, 3, 2, 2, 1, 1
    # List is in reverse order
    seq = []
    for i in range(1, n):
        seq.append(i)
        seq.append(i)
    seq.append(n)
    
    # Generate empty matrix of NxN size
    m = [[0 for i in range(n)] for i in range(n)]
    x, y   = 0, 0 # Starting position
    dx, dy = 1, 0 # Default direction is to the right
    count  = 0    # How many cells were filled since last turn
    
    for i in range(1, (n ** 2) + 1):
        m[y][x] = i                   # Fill current cell with a number
        count += 1                    # Increase counter
        if count == seq[-1]:          # If it's time to change direction:
            count = 0                 # Reset counter
            seq.pop()                 # Remove old number from sequence
            dx, dy = rotate[(dx, dy)] # Get new direction from dictionary
        x, y = x + dx, y + dy         # Go to next cell
    
    return m
_________________________
def create_spiral(n):
    try:
        n = int(n)
    except ValueError:
        return []
    if n < 1:
        return []
    count = 1
    arr = [[1 for i in range(n)] for k in range(n)]
    border_start = 0
    border_stop = n - 1
    d = 1
    while border_stop > border_start:
        if d == 1:
            for k in range(border_start, border_stop):
                arr[border_start][k] = count
                count += 1
            d = 2
        elif d == 2:
            for k in range(border_start, border_stop):
                arr[k][border_stop] = count
                count += 1
            d = 3
        elif d == 3:
            for k in range(border_stop, border_start, -1):
                arr[border_stop][k] = count
                count += 1
            d = 4
        else:
            for k in range(border_stop, border_start, -1):
                arr[k][border_start] = count
                count += 1
            d = 1
            border_stop -= 1
            border_start += 1
    if n % 2 == 1:
        arr[n // 2][n // 2] = count
    return arr
_________________________
from itertools import cycle

def create_spiral(n):
    if not n or not isinstance(n, int):
        return []
    
    matrix = [[0]*n for i in range(n)]
    x = y = counter = 0
    cyc = cycle([(0,1), (1,0), (0,-1), (-1,0)])
    dx,dy = (0,0)
    #case of odd n=3 reached (x=1,y=1) | Case of even n=4 reached (x=2,y=1)
    while not ( ( n%2 and x == y == n//2 ) or ( (not n%2) and x == n//2 and y == n//2-1 ) ):
        x += dx
        y += dy
        if not (0<=x<n and 0<=y<n) or matrix[x][y] != 0:
            #reducing x and y by dx and dy so we go one position behind since we either hit a wall or an occupied cell.
            x-=dx
            y-=dy
            dx,dy = next(cyc)
            continue

        counter += 1
        matrix[x][y] = counter

    return matrix
