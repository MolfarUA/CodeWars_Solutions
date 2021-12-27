# number  the cube faces like a dice 1-6
from random import shuffle
WIDTH = 0
HEIGHT = 0


def folding(
        grid,
        face,
        list_on_face,
        remain_list,
        faces_done
        #  ,faces_done_on_cube
):
    faces = [(list_on_face, face)]

    dirs = [1, -1, WIDTH, -WIDTH]
    if list_on_face % WIDTH == 0:
        dirs.remove(-1)
    if list_on_face % WIDTH == WIDTH - 1:
        dirs.remove(1)
    if list_on_face < WIDTH:
        dirs.remove(-WIDTH)
    if list_on_face >= WIDTH * (HEIGHT - 1):
        dirs.remove(WIDTH)

    goto_dirs = []
    for direction in dirs:
        goto_cell = direction + list_on_face
        if goto_cell in remain_list:
            if goto_cell in faces_done:
                #  if faces_done_on_cube[faces_done.index(
                #  goto_cell)] != new_face(grid, direction):
                if goto_cell != faces_done[-1]:
                    return "F"
            else:
                goto_dirs.append(direction)
    #  print(faces_done, list_on_face, goto_dirs)
    for direction in goto_dirs:
        faces.extend(folding(
            grid=new_grid(face, direction, grid),
            face=new_face(grid, direction),
            list_on_face=list_on_face + direction,
            remain_list=remain_list,
            faces_done=faces_done + [list_on_face]
            #  faces_done_on_cube=faces_done_on_cube + [face]
        ))
    return faces


def new_face(grid, direction):
    return grid[[1, -1, WIDTH, -WIDTH].index(direction)]


def new_grid(face, direction, grid):
    opposite_face = {1: 6, 2: 4, 6: 1, 4: 2, 5: 3, 3: 5}
    dir_index = {1: 0, -1: 1, WIDTH: 2, -WIDTH: 3}
    newgrid = grid.copy()
    newgrid[dir_index[-direction]] = face
    newgrid[dir_index[direction]] = opposite_face[face]
    return newgrid


def wrap_cube(shape):
    global WIDTH, HEIGHT
    shape_list = shape.split('\n')
    WIDTH = max([len(x) for x in shape_list]) +1
    HEIGHT = len(shape_list)
    number_list = []
    char_list = []
    for y in range(HEIGHT):
        for x in range(len(shape_list[y])):
            if shape_list[y][x] != " ":
                char_list.append(shape_list[y][x])
                number_list.append(x + y * WIDTH)
#     print(WIDTH, HEIGHT, char_list, number_list)
    faces = folding(grid=[3, 5, 2, 4],  # in dir [1,-1,5,-5]
                    face=1,
                    list_on_face=number_list[0],
                    remain_list=number_list, faces_done=[])  # , faces_done_on_cube=[])
    #  print(faces)
    if "F" in faces:
        return None
    #  return sorted(faces) == list(range(1, 7))
    # return True or False 
    res = []
    for i in range(1, 7):
        r = [char_list[number_list.index(p[0])] for p in faces if p[1] == i]
        shuffle(r)
        if len(r) > 1:
            res.append(r)
    shuffle(res)
    return res


if __name__ == "__main__":
    print(wrap_cube("a\nb\nc"))
    
####################
down  = lambda b, t, n, s, e, w: (s, n, b, t, e, w)
up    = lambda b, t, n, s, e, w: (n, s, t, b, e, w)
left  = lambda b, t, n, s, e, w: (w, e, n, s, b, t)
right = lambda b, t, n, s, e, w: (e, w, n, s, t, b)

def wrap_cube(shape):
    binds = [[], [], [], [], [], []]
    seen = set()
    cube = (0, 1, 2, 3, 4, 5) # (bottom, top, north, south, east, west)
    shape = shape.split('\n')
    buffer = " "*(max(map(len, shape))*2)
    shape = [buffer, *[" "+v+buffer for v in shape], buffer]
    for y, r in enumerate(shape):
        for x, v in enumerate(r):
            if v != " ":
                start = (y, x)
                break
    def roll(y, x, cube, path):
        if shape[y][x] == " ":
            return
        if (y, x) in seen:
            if shape[y][x] not in binds[cube[0]] or shape[y][x] in path[:-2]:
                raise Exception
            return
        seen.add((y, x))
        binds[cube[0]].append(shape[y][x])
        for r, dy, dx in ((up, -1, 0), (down, 1, 0), (left, 0, -1), (right, 0, 1)):
            roll(dy+y, dx+x, r(*cube), path+shape[y][x])
    try:
        roll(*start, cube, "")
    except Exception as e:
        return
    return list(filter(lambda v: len(v) > 1, binds))
        
    
#########################
from collections import defaultdict


def transfromdBuilder():
    """ Using rubiks cube notations for faces of the cube:     U
                                                              LFRB
                                                               D
        
        Net: considering 3 chars touching each others in the net (considered a 2D array):
        
                AB        A->B: d1=(0,1)     B->C: d2=(1,0)
                 C
        
            turn right:  cross(d1,d2) = -1
            turn left:   cross(d1,d2) =  1
            forward:     cross(d1,d2) =  0
    """
    FACES   = 'LFRBUD'
    RIGHTS  = "LFD FRD RBD BLD BRU RFU FLU LBU".split()
    TOWARDS = "UD LR BF".split()
    R,T,L   = -1,0,1                # cross products: right,towards,left = R,T,L
    
    FOLDS = [{},{},{}]              # {first+second: third}, ...} for "turns" or {first: third} for "towards"
    
    for s in RIGHTS:                # all turns
        for i in range(3):
            a,b,c = s[i:]+s[:i]
            FOLDS[R][a+b], FOLDS[L][a+c] = c,b
    
    for s in TOWARDS:               # all forwards
        for a,c in s,s[::-1]:
            for b in FACES:
                if b not in s: FOLDS[T][a+b]=c
    
    return lambda cp,f1,f2: FOLDS[cp][f1+f2]
    
    
MOVES = (0,1), (0,-1), (-1,0), (1,0)
cross = lambda x,y,a,b: x*b - y*a
getNextFace = transfromdBuilder()
    
    
def wrap_cube(net):
    tiles  = {(x,y): c for x,r in enumerate(net.splitlines()) for y,c in enumerate(r) if c!=' '}
    
    neighs = ( [(x,y)]+[(x+dx,y+dy) for dx,dy in MOVES if (x+dx,y+dy) in tiles] for x,y in tiles )
    a,b = next( (lst for lst in neighs if len(lst)==2), (None,None) )
    if a is None: return None

    preds = defaultdict(int)
    folds = defaultdict(list)
    preds[b] = a
    folds['F'].append( tiles[a] )
    folds['R'].append( tiles[b] )
    q = [('F', 'R', b, b[0]-a[0], b[1]-a[1])]    # (coming from face, current face, current pos, previous dx, previous dy)
    
    while q:
        f1,f2,tile,dx0,dy0 = q.pop()
        x,y = tile

        for dx,dy in MOVES:
            pos = x+dx,y+dy
            if pos not in tiles or preds[tile]==pos: continue
                
            if preds[pos]: return None        # not a DAG => not foldable

            f3 = getNextFace(cross(dx0,dy0,dx,dy), f1, f2)
            folds[f3].append( tiles[pos] )
            q.append( (f2,f3,pos,dx,dy) )
            preds[pos] = tile

    return [lst for lst in folds.values() if len(lst)>1]
  
#############################
from collections import defaultdict

class Vector:
    '''A simple Vector class.'''

    def __init__(self, x ,y, z):
        self.x, self.y, self.z = x, y, z
    
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x*other, self.y*other, self.z*other)
        if isinstance(other, Vector):
            return Vector(self.x*other.x, self.y*other.y, self.z*other.z)

    def cross(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)

    def dot(self, other):
        return sum(a * b for a, b in zip(self, other))

    def iter(self):
        return iter([self.x, self.y, self.z])

    def __getitem__(self, i):
        if i > 2:
            raise IndexError
        return [self.x, self.y, self.z][i]

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __str__(self):
        return f"[{self.x}, {self.y}, {self.z}]"
    __repr__ = __str__


class Square:

    def __init__(self, label, x, y):
        self.label = label
        # needed to build grid/graph
        self.x, self.y = x, y
        # upstream square
        self._parent = None
        # world space transform, defaults to identity
        self.transform = (Vector(1,0,0),Vector(0,1,0),Vector(0,0,1))

    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, p):
        '''Set parent to p and inherit its transform.'''
        self._parent = p
        self.transform = matmul(self.transform, self._parent.transform)

    def rotate(self, axis):
        '''Rotate transform matrix by 90° around `axis`.'''
        # Apply Rodrigues formula on each basis vector in local transform.
        # cos(90) == 0 (term vanishes), sin(90) == 1 (term doesn't change)
        self.transform = tuple(axis.cross(v) + axis * axis.dot(v) for v in self.transform)

    def __str__(self):
        return f"Square('{self.label}')"
    __repr__ = __str__


def matmul(A, B):
    return tuple([Vector(*[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(A))]) for i in range(len(B))])


def make_grid(net: str):
    '''Turn a string of squares into a matrix of Square objects.'''
    lines = [line for line in net.split("\n") if line.strip() != ""]
    height = len(lines)
    width = len(sorted(lines, key=len)[-1])
    grid = [[None]*width for _ in range(height)]
    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            if val != " ":
                grid[y][x] = Square(val, x, y)
    return grid


def wrap_cube(net):
    '''Figure out which squares in a net overlap when folded into a cube.
    
    We treat the squares in the net as individual surfaces organized into a
    DAG hierarchy, where each rotation affects both a square and its children.
    While building the graph, we rotate adjacent squares and let them inherit
    the transform of their ancestor, then collect their surface normal.
    All surfaces that share a normal necessarily overlap.
    '''
    grid = make_grid(net)
    # first node is first square we encounter
    start = None
    for x in grid[0]:
        if x:
            start = x
            break
    # a dictionary of normals, the items are the squares that share them.
    normals = defaultdict(list)
    # perform DFS to construct DAG
    stack = [start]
    visited = set()
    while stack:
        s = stack.pop()
        if s not in visited:
            # collect its normal, which is the z-axis
            normals[s.transform[2]].append(s.label)
            visited.add(s)
            # check adjacent cells in cardinal directions
            for x, y in [(-1,0), (1,0), (0,-1), (0,1)]:
                cx, cy = s.x + x, s.y + y
                # don't go out of bounds
                if 0 <= cx < len(grid[0]) and 0 <= cy < len(grid):
                    child = grid[cy][cx]
                    # we found an adjacent square
                    if child and child not in visited:
                        # rotate it around the vector formed by the
                        # boundary edge between s and child. Because 
                        # the axis is local in reference to the child,
                        # we need to do this before we apply a parent.
                        child.rotate(Vector(y,x,0))
                        # set its parent to inherit its transform
                        child.parent = s
                        stack.append(child)
        # a node that appears twice indicates a cycle;
        # cyclic graphs can be neither DAGs nor, more critically, wrapped around a cube.
        else:
            return None
    overlap = []
    for squares in normals.values():
        # multiple squares per normal means overlap
        if len(squares) > 1:
            overlap.append(squares)
    return overlap
  
############################
down  = lambda b, t, n, s, e, w: (s, n, b, t, e, w)
up    = lambda b, t, n, s, e, w: (n, s, t, b, e, w)
left  = lambda b, t, n, s, e, w: (w, e, n, s, b, t)
right = lambda b, t, n, s, e, w: (e, w, n, s, t, b)

def wrap_cube(shape):
    binds = [[], [], [], [], [], []]
    seen = set()
    cube = (0, 1, 2, 3, 4, 5) # (bottom, top, north, south, east, west)
    shape = shape.split('\n')
    buffer = " "*(max(map(len, shape))*2)
    shape = [buffer, *[" "+v+buffer for v in shape], buffer]
    for y, r in enumerate(shape):
        for x, v in enumerate(r):
            if v != " ":
                start = (y, x)
                break
    def roll(y, x, cube, path):
        if shape[y][x] == " ":
            return
        if (y, x) in seen:
            if shape[y][x] not in binds[cube[0]] or shape[y][x] in path[:-2]:
                raise Exception
            return
        seen.add((y, x))
        binds[cube[0]].append(shape[y][x])
        for r, dy, dx in ((up, -1, 0), (down, 1, 0), (left, 0, -1), (right, 0, 1)):
            roll(dy+y, dx+x, r(*cube), path+shape[y][x])
    try:
        roll(*start, cube, "")
    except Exception as e:
        return
    return list(filter(lambda v: len(v) > 1, binds))
        
    
#######################
from collections import defaultdict
import numpy as np

def wrap_cube(shape):
    MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    shape = shape.split("\n")
    
    h = len(shape)
    y = next(y for y, s in enumerate(shape) if s.rstrip() != "")
    x = next(x for x, c in enumerate(shape[y]) if c != " ")
    
    face = np.array([list("FRBL"),
                     list("D U "),
                     list("BLFR"),
                     list("U D ")])
    
    overlaps = defaultdict(list)
    
    visited = set([(y, x)])
    stack = [(y, x, face, (0, 0))]
    while stack:
        y, x, face, source = stack.pop()
        overlaps[face[0][0]].append(shape[y][x])
        
        for dy, dx in MOVES:
            if (dy, dx) == source:
                continue
            
            next_y, next_x = y+dy, x+dx
            if 0 <= next_y < h and 0 <= next_x < len(shape[next_y]) and shape[next_y][next_x] != " ":
                if (next_y, next_x) in visited:
                    return None
                visited.add((next_y, next_x))
                stack.append((next_y, next_x, roll(face, -dy, -dx), (-dy, -dx)))
    
    return [squares for squares in overlaps.values() if len(squares) >= 2]

def roll(face, dy, dx):
    face = face.copy()
    if dy:
        face[:, [0, 2]] = np.roll(face[:, [0, 2]], dy, axis=0)
    if dx:
        face[[0, 2], :] = np.roll(face[[0, 2], :], dx, axis=1)
    return face
  
################
def convert_to_matrix(shape):
    matrix=[[]]
    row=0
    for char in shape:
        if char =="\n":
            matrix.append([])
            row+=1
        else:
            matrix[row].append(char)
    matrix=[row for row in matrix if row] #deletes any empty lists from matrix
    return matrix

def create_cell_dictionary(matrix):
    cells={}
    for r, row in enumerate(matrix):
        for c, column in enumerate(row):
            if column!=" ":
                cells[column]={"Coords":[r,c]}
    return cells

def find_start(matrix):
    start=[]
    column=0
    while not start:
        for r, row in enumerate(matrix):
            if row[column]!=" ":
                start = [r,column]
                break
        column+=1
    return start  
    
def get_neighbours(matrix,coords):
    neighbour_status=[]
    count=0
    #get status of eight connecting cells
    for i in range(-1,2): #above and below
        for j in range(-1,2): #left and right
            row=coords[0]+i
            col=coords[1]+j
            if row>=0 and col>=0: #avoid matrix coords which are negative
                try: 
                    neighbour_status.append([[row,col],matrix[row][col]])
                except IndexError: #error handle when matrix coords to high
                    neighbour_status.append([[row,col]," "])
            else:
                neighbour_status.append([[row,col]," "])  
            count+=1
    return neighbour_status

def foldable(neighbour_status):
    status = True
    #check if net can be folded
    sets=[[0,1,3,4],[1,2,4,5],[3,4,6,7],[4,5,7,8]]  
    for set in sets:
        if neighbour_status[set[0]][1]!=' ' and \
           neighbour_status[set[1]][1]!=' ' and \
           neighbour_status[set[2]][1]!=' ' and \
           neighbour_status[set[3]][1]!=' ':
            status=False
    return status

def dir_change(PreviousDir, CurrentDir):
    Change_Dir=CurrentDir-PreviousDir
    if Change_Dir<0: Change_Dir+=360
    if Change_Dir==0:
        return 1 # Straight
    elif Change_Dir == 270:
        return 0 # Left
    elif Change_Dir == 90:
        return 2 #Right
    
def fold(PreviousSide, CurrentSide, Direction):
    transform={}
    transform[4,1]=[5,2,6]
    transform[6,1]=[4,5,2]
    transform[2,1]=[6,4,5]
    transform[5,1]=[2,6,4]
    transform[1,2]=[5,3,6]
    transform[6,2]=[1,5,3]
    transform[3,2]=[6,1,5]
    transform[5,2]=[3,6,1]
    transform[2,3]=[5,4,6]
    transform[6,3]=[2,5,4]
    transform[4,3]=[6,2,5]
    transform[5,3]=[4,6,2]
    transform[3,4]=[5,1,6]
    transform[6,4]=[3,5,1]
    transform[1,4]=[6,3,5]
    transform[5,4]=[1,6,3]
    transform[4,5]=[3,2,1]
    transform[1,5]=[4,3,2]
    transform[2,5]=[1,4,3]
    transform[3,5]=[2,1,4]
    transform[4,6]=[1,2,3]
    transform[3,6]=[4,1,2]
    transform[2,6]=[3,4,1]
    transform[1,6]=[2,3,4]
    NextSide=transform[PreviousSide,CurrentSide][Direction]
    return NextSide

def wrap_cube(shape):
    print(shape)
    
    #convert shape into 2D matrix
    matrix=convert_to_matrix(shape)

    #create a dictionary for each cell.  Key is char, value is cell info (coords, folded side etc).
    cells=create_cell_dictionary(matrix)
    
    #find first part of net
    start=find_start(matrix)
    
    #follow the path of cells:
    path=[] #record all cells
    buffer = [start] #buffer is a store of all cells which need to be processed

    Dir_Angle={1:270,3:180,5:0,7:90} #assign angles to directions
    cube=[[] for i in range(6)] #record of which cells have been folded onto each side of the cube. Each of the six lists in this list represent a side, say: front, right, back, left, top, bottom.
    
    while buffer:  #buffer is a record of all cells which have been identified as being connected to other cells but not yet processed.
        row = buffer[-1][0]
        col = buffer[-1][1]
        char = matrix[row][col]
        
        #get neighbouring cell status
        neighbour_status=get_neighbours(matrix,buffer[-1])
        
        #test if cell is foldable
        if not foldable(neighbour_status):
            return
        
        #get info about the cell which this one is connected to.
        if not path: #test if this is first cell.  If so provide initialisation values.
            PreviousCellSide=3
            PreviousCellDirection=0
            CellSide=4
        else:
            PreviousCellSide=cells[char]["PreviousCellSide"] #Side which relates to the cell before the one being processed
            PreviousCellDirection=cells[char]["PreviousCellDirection"] #Previous direction. This is either 0, 90, 180, 270 based on the direction the path has come from.
            CellSide=cells[char]["CellSide"] #Side which relates to the current cell being processed   
        
        #delete current cell being processed from buffer
        del buffer[-1]        
        
        #add current cell char to path
        path.append(char)
        #add current cell to cube
        cube[CellSide-1].append(char)
        
        #find all connectings cells and add to buffer. 
        #for each connecing cell record the coord of the connected cell, which side connects it to the current cell i.e right, top, left, bottom
        for index in [1,3,5,7]: #cycle through cell above, left, right and below current cell.  Diagonal cells cannot be connected.
            connected_cell_char=neighbour_status[index][1]
            if not connected_cell_char in path: #check cell hasn't already been processed
                if connected_cell_char!=" ":
                    if cells[connected_cell_char]['Coords'] in buffer:
                        "Duplicate found in buffer"
                    buffer.append(cells[connected_cell_char]['Coords']) #add cell coord to buffer
                    #add info about connectivity to cells dictionary
                    cells[connected_cell_char]["PreviousCellSide"]= CellSide #cell side of current cell being processed.  This is "PreviousCellSide" for cell being added to buffer.
                    cells[connected_cell_char]["PreviousCellDirection"]= Dir_Angle[index] #direction which lead to cell being processed.  This is "PreviousCellDirection" for cell being added to buffer.
                    Dir_Change=dir_change(Dir_Angle[index],PreviousCellDirection) #This Either 0=Left, 1=Straight, 2,=Right
                    NextSide=fold(PreviousCellSide,CellSide,Dir_Change) #cell side of connected cell which has been added to buffer
                    cells[connected_cell_char]["CellSide"]=NextSide
                    
    cube_overlaps=[x for x in cube if len(x)>1] #reduce down to just sides with more than one cell
    for r in cube_overlaps:  #check if one cell occurs more than once.
        for c in r:
            if r.count(c)>1:
                print("Loop found")
                return
    print(f"Cube_overlaps={cube_overlaps}")
    return cube_overlaps
  
###############
from collections import defaultdict, deque

class Point(complex):
    def __hash__(self): return hash((self.real, self.imag))
    def __eq__(self, other): return self.real == other.real and self.imag == other.imag
    def __lt__(self, other): return abs(self) < abs(other)
    def __radd__(self, other): return Point(complex.__add__(self, other))
    def __add__(self, other): return Point(complex.__add__(self, other))
    def __repr__(self): return f'P({int(self.real)},{int(self.imag)})'

def wrap_cube(shape):
    face_id_coord = {
        0: (0, -1, 0),
        1: (1, 0, 0),
        2: (0, 0, 1),
        3: (-1, 0, 0),
        4: (0, 0, -1),
        5: (0, 1, 0)
    }

    def rotate(cfs, rot):
        nfs = cfs.copy()
        if rot == -1j:
            fcoord = deque([cfs[f] for f in (0, 1, 5, 3)])
            fcoord.rotate(1)
            nfs[0], nfs[1], nfs[5], nfs[3] = fcoord
        elif rot == 1j:
            fcoord = deque([cfs[f] for f in (0, 1, 5, 3)])
            fcoord.rotate(-1)
            nfs[0], nfs[1], nfs[5], nfs[3] = fcoord
        elif rot == -1:
            fcoord = deque([cfs[f] for f in (0, 4, 5, 2)])
            fcoord.rotate(1)
            nfs[0], nfs[4], nfs[5], nfs[2] = fcoord
        else:
            fcoord = deque([cfs[f] for f in (0, 4, 5, 2)])
            fcoord.rotate(-1)
            nfs[0], nfs[4], nfs[5], nfs[2] = fcoord
        return nfs

    cube_mapping = {Point(x, y): v for y, row in enumerate(shape.split('\n')) for x, v in enumerate(row) if v != ' '}
    overlapping = defaultdict(list)
    start = min(cube_mapping.keys())
    visited = set([])
    q = [(start, face_id_coord.copy(), [])]
    
    while q:
        curr_pos, cube_status, path = q.pop()
        overlapping[cube_status[0]].append(cube_mapping[curr_pos])

        if curr_pos in visited: return None
        visited.add(curr_pos)

        for o in [-1j, 1, 1j, -1]:
            next_pos = curr_pos+o
            if next_pos in cube_mapping and next_pos not in path:
                next_cube_status = rotate(cube_status, o)
                q.append((next_pos, next_cube_status, path + [curr_pos]))
    return [f for f in overlapping.values() if len(f) > 1]
  
  
########################
from collections import Counter

class Dice:
    def __init__(self, top=1, north=2, west=3, east=4, south=5, bottom=6):
        self.top, self.north, self.west, self.east, self.south, self.bottom = top, north, west, east, south, bottom
    def N(self): return self.south, self.top, self.west, self.east, self.bottom, self.north
    def S(self): return self.north, self.bottom, self.west, self.east, self.top, self.south
    def E(self): return self.west, self.north, self.bottom, self.top, self.south, self.east
    def W(self): return self.east, self.north, self.top, self.bottom, self.south, self.west

def wrap_cube(shape):
    def has_loop():
        cnt = Counter()
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch != ' ':
                    for ny, nx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
                        cnt[y, x] += 0 <= ny < H and 0 <= nx < W and lines[ny][nx] != ' '
        updated = True
        while updated:
            updated = False
            deletes = set()
            for (y, x), v in cnt.items():
                if v == 1:
                    deletes.add((y, x))
                    for ny, nx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
                        if 0 <= ny < H and 0 <= nx < W and cnt[ny, nx]:
                            cnt[ny, nx] -= 1
                    updated = True
            for y, x in deletes:
                del cnt[y, x]
        return any(cnt.values())

    def find_start_position():
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch != ' ':
                    return y, x

    lines = shape.split('\n')
    H, W = len(lines), len(max(lines, key=len))
    lines = [l + ' '*(W - len(l)) for l in lines]

    if has_loop():
        return None
    sy, sx = find_start_position()
    visited, sides, stack = {' '}, {}, [(sy, sx, lines[sy][sx], Dice(1, 2, 3, 4, 5, 6))]
    while stack:
        y, x, ch, d = stack.pop()
        visited.add(ch)
        sides[d.top] = sides.get(d.top, []) + [ch]
        for f, ny, nx in ((d.N, y-1, x), (d.S, y+1, x), (d.W, y, x-1), (d.E, y, x+1)):
            if 0 <= ny < H and 0 <= nx < W and lines[ny][nx] not in visited:
                stack.append((ny, nx, lines[ny][nx], Dice(*f())))
                visited.add(lines[ny][nx])
    return [v for v in sides.values() if len(v) > 1]
