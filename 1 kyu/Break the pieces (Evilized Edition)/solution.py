USE_BREAK_DISPLAY = True

v = lambda c: {(c[0]+1,c[1]), (c[0]-1,c[1])}
h = lambda c: {(c[0],c[1]+1), (c[0],c[1]-1)}
neig = lambda c: {(c[0]+1,c[1]), (c[0]-1,c[1]), (c[0],c[1]+1), (c[0],c[1]-1)}
neig2 = lambda c: {(c[0]+i, c[1]+j) for i in {1,-1,0} for j in {1,-1,0}}
def break_evil_pieces(shape):
    if not shape.strip():
        return []
    (a,b,shape) = interpolate(shape)
    S={(i,j) for i in range(a) for j in range(b) if shape[i][j]==' '}
    regions=[]
    while S:
        R = set({S.pop()})
        R_ = R
        while R_:
            R_ = {j for i in R_ for j in neig(i)&S}-R
            R.update(R_)
        S=S-R
        boundary = {j for i in R for j in neig2(i)}-R
        min_i = min(i for i,j in boundary)
        max_i = max(i for i,j in boundary)+1
        min_j = min(j for i,j in boundary)
        max_j = max(j for i,j in boundary)+1
        if min_i<0 or min_j<0 or max_i>a or max_j>b:
            continue
        region = [list(row[min_j:max_j]) for row in shape[min_i:max_i]]
        for i in range(len(region)):
            for j in range(len(region[i])):
                if region[i][j]!=' ' and (i+min_i,j+min_j) not in boundary:
                    region[i][j]=' '
                elif region[i][j]=='+':
                    c=(i+min_i, j+min_j)
                    if not ( h(c)&boundary and v(c)&boundary ):
                          region[i][j]='-' if h(c)&boundary else '|'
        regions.append('\n'.join(''.join(row[::2]).rstrip() for row in region[::2]))
    return regions
    
def interpolate(s):
    shape=s.split('\n')
    while not shape[0].strip():
        shape=shape[1:]
    while not shape[-1].strip():
        shape=shape[:-1]
    a =len(shape)
    b = max(len(shape[i]) for i in range(a))
    for i in range(a):
        shape[i]+=' '*(b-len(shape[i]))
    newshape=[[]]*(2*a-1)
    for i in range(2*a-1):
        newshape[i]=[' ']*(2*b-1)
        if i%2:
            for j in range(b):
                    if shape[i//2][j] in '|+' and shape[i//2+1][j] in '|+':
                        newshape[i][2*j]='|'
        else:
            for j in range(2*b-1):
                if j%2:
                    if shape[i//2][j//2] in '-+' and shape[i//2][j//2+1] in '-+':
                        newshape[i][j]='-'
                else:
                    newshape[i][j]=shape[i//2][j//2]
    return (2*a-1,2*b-1,newshape)
___________________________________
USE_BREAK_DISPLAY = True

DIRS4 = [(0,1), (1,0), (0,-1), (-1,0)]
DIRS8 = DIRS4 + [(1,1), (1,-1), (-1,1), (-1,-1)]

def zoom_in_shape(shape):
    m, n = len(shape), len(shape) and max(map(len, shape))
    zoom = [[' '] * (2 * n - 1) for _ in range(2 * m - 1)]
    for x, line in enumerate(shape):
        for y, c in enumerate(line):
            zoom[2*x][2*y] = c
    for x in range(1, len(zoom), 2):
        for y in range(0, len(zoom[x]), 2):
            if zoom[x-1][y] in '+|' and zoom[x+1][y] in '+|':
                zoom[x][y] = '|'
    for x in range(0, len(zoom), 2):
        for y in range(1, len(zoom[x]), 2):
            if zoom[x][y-1] in '+-' and zoom[x][y+1] in '+-':
                zoom[x][y] = '-'
    zoom = list(map(lambda s:''.join(s).rstrip(), zoom))
    return zoom

def zoom_out_shape(shape):
    return (l[::2] for l in shape[::2])

def break_evil_pieces(shape):
    shape = shape.splitlines()
    if not shape: return []
    shape = zoom_in_shape(shape)
    seen = set()

    def expand(*seed):
        xm, ym, xM, yM = float('inf'), float('inf'), 0, 0
        queue, borders, crosses = {seed}, {}, set()
        add = True
        while queue:
            x, y = queue.pop()
            seen.add((x, y))
            for u, v in DIRS8:
                m, n = x+u, y+v
                if (m, n) in seen: continue
                try:
                    assert m >= 0 and n >= 0
                    c = shape[m][n]
                    #if c == 'x': add = False
                    if c == ' ': queue.add((m, n))
                    else:
                        if c == '+': crosses.add((m, n))
                        borders[m, n] = c
                        if m < xm: xm = m
                        if n < ym: ym = n
                        if m > xM: xM = m
                        if n > yM: yM = n
                except:
                    add = False
        if not add: return
        for x, y in crosses:
            if borders.get((x-1,y), ' ') + borders.get((x+1,y),' ') == '||' \
                and '-' not in borders.get((x,y-1), ' ') + borders.get((x,y+1),' '):
                borders[x, y] = '|'
            if borders.get((x,y-1), ' ') + borders.get((x,y+1),' ') == '--' \
                and '|' not in borders.get((x-1,y), ' ') + borders.get((x+1,y),' '):
                borders[x, y] = '-'
        return [''.join(borders.get((x, y), ' ')
                        for y in range(ym, yM + 1)).rstrip() for x in range(xm, xM+1)]

    pieces, seen = [], set()
    for i, l in enumerate(shape):
        for j, c in enumerate(l):
            if c != ' ' or (i, j) in seen: continue
            piece = expand(i, j)
            if piece:
                pieces.append('\n'.join(zoom_out_shape(piece)))
    return pieces
___________________________________________
USE_BREAK_DISPLAY = True

import sys
from enum import Enum
import collections 

class Vertex:

    def __init__(self, i=0, j=0):
        self.i = i
        self.j = j
        
    def shift_origin(self, origin):
        self.i = self.i - origin.i
        self.j = self.j - origin.j
        
    def move(self, vertex):
        return type(self)(self.i + vertex.i, self.j + vertex.j)
    
    @staticmethod
    def is_collinear(vertex1, vertex2, vertex3):
        return 0 == vertex1.j * (vertex2.i - vertex3.i) + vertex2.j * (vertex3.i - vertex1.i) + vertex3.j * (vertex1.i - vertex2.i)
        
    def __eq__(self, other):
        if isinstance(other, Vertex):
            return (self.i, self.j) == (other.i, other.j)
        return False
        
    def __hash__(self):
        return hash((self.i, self.j))
        
    def __repr__(self):
        return "[%d|%d]" % (self.i, self.j)
        
class Polygon:

    def __init__(self, vertices):
        self.vertices = []
        self.bbox_ul = Vertex(sys.maxsize,sys.maxsize)
        self.bbox_lr = Vertex(0, 0)
        self.di = 0
        self.dj = 0
        self.num_vertices = 0
        for v in vertices:
            self.add(v)
        self.clean_vertices()
        self.contained = []
        
    def add(self, vertex):
        self.vertices.append(vertex)
        self.bbox_ul.i = min(self.bbox_ul.i, vertex.i)
        self.bbox_ul.j = min(self.bbox_ul.j, vertex.j)
        self.bbox_lr.i = max(self.bbox_lr.i, vertex.i)
        self.bbox_lr.j = max(self.bbox_lr.j, vertex.j)
        self.di = 1 + self.bbox_lr.i - self.bbox_ul.i
        self.dj = 1 + self.bbox_lr.j - self.bbox_ul.j
        self.num_vertices += 1
        
    def add_contained(self, poly):
        self.contained.append(poly)
        
    def __repr__(self):
        io = "Bbox %s, %s\nVertices:" % (repr(self.bbox_ul), repr(self.bbox_lr))
        io += "->".join(repr(v) for v in self.vertices)
        return io
        
    def shift_origin(self):
        for v in self.vertices:
            v.shift_origin(self.bbox_ul)
        self.bbox_lr.shift_origin(self.bbox_ul)
        self.bbox_ul.shift_origin(self.bbox_ul)
        
    def clean_vertices(self):
        clean = []
        for i in range(0, len(self.vertices)):
            this_vertex = self.vertices[i]
            prev_vertex = self.vertices[(i-1+self.num_vertices)%self.num_vertices]
            next_vertex = self.vertices[(i+1)%self.num_vertices]
            if (not Vertex.is_collinear(prev_vertex, this_vertex, next_vertex)):
                clean.append(this_vertex)
        self.vertices = clean
        self.num_vertices = len(self.vertices)
        
    def contains_point(self, point):
        crossings = 0
        for i in range(0, len(self.vertices)):
            this_vertex = self.vertices[i]
            next_vertex = self.vertices[(i+1)%self.num_vertices]
            if this_vertex.j >= point.j and next_vertex.j >= point.j:
                if this_vertex.i <= next_vertex.i:
                    if point.i >= this_vertex.i and point.i <= next_vertex.i:
                        crossings = crossings + 1
                elif point.i > next_vertex.i and point.i < this_vertex.i:
                        crossings = crossings + 1
        return crossings%2 == 1
                    
    def contains(self, other):
        if other.bbox_ul.i <= self.bbox_ul.i \
            or other.bbox_ul.j <= self.bbox_ul.j \
            or other.bbox_lr.i >= self.bbox_lr.i \
            or other.bbox_lr.j >= self.bbox_lr.j:
            return False
        else:
            for o in other.vertices:
                if o in self.vertices:
                    return False
            for o in other.vertices:
                if not self.contains_point(o):
                    return False
        return True
    
    def is_counterclockwise(self):
        sum = 0
        #(x2 − x1)(y2 + y1)
        for i in range(0, len(self.vertices)):
            this_vertex = self.vertices[i]
            next_vertex = self.vertices[(i+1)%self.num_vertices]
            sum = sum + (next_vertex.j - this_vertex.j) * (next_vertex.i + this_vertex.i)
        return sum >= 0
        
    def __eq__(self, other):
        if isinstance(other, Polygon):
            return collections.Counter(self.vertices) == collections.Counter(other.vertices)
        return False
        
    @staticmethod
    def stringify(shape):
        return "\n".join(str("".join(c for c in l).rstrip()) for l in shape)
        
    def to_shape(self):
        old_origin = Vertex(self.bbox_ul.i, self.bbox_ul.j)
        self.shift_origin()
        shape = [[" " for i in range(self.dj)] for j in range(self.di)]
        for i in range(0, self.num_vertices):
            this_vertex = self.vertices[i]
            next_vertex = self.vertices[(i+1)%self.num_vertices]
            shape[this_vertex.i][this_vertex.j] = "+"
            start_i = min(this_vertex.i, next_vertex.i)
            end_i = max(this_vertex.i, next_vertex.i)
            for x in range(start_i+1, end_i):
                if shape[x][this_vertex.j] == " ":
                    shape[x][this_vertex.j] = "|"
            start_j = min(this_vertex.j, next_vertex.j)
            end_j = max(this_vertex.j, next_vertex.j)
            for x in range(start_j+1, end_j):
                if shape[this_vertex.i][x] == " ":
                    shape[this_vertex.i][x] = "-"
                
        for cp in self.contained:
            shift = Vertex(cp.bbox_ul.i - old_origin.i, cp.bbox_ul.j - old_origin.j)
            cp.shift_origin()
            #print("SHIFT: %s" % shift)
            for i in range(0, cp.num_vertices):
                this_vertex = cp.vertices[i]
                next_vertex = cp.vertices[(i+1)%cp.num_vertices]
                shape[this_vertex.i+shift.i][this_vertex.j+shift.j] = "+"
                start_i = min(this_vertex.i, next_vertex.i)
                end_i = max(this_vertex.i, next_vertex.i)
                for x in range(start_i+1, end_i):
                    if shape[x+shift.i][this_vertex.j+shift.j] == " ":
                        shape[x+shift.i][this_vertex.j+shift.j] = "|"
                start_j = min(this_vertex.j, next_vertex.j)
                end_j = max(this_vertex.j, next_vertex.j)
                for x in range(start_j+1, end_j):
                    if shape[this_vertex.i+shift.i][x+shift.j] == " ":
                        shape[this_vertex.i+shift.i][x+shift.j] = "-"
        return self.stringify(shape)
        
class Dir(Enum):
    RIGHT = Vertex(0,1)
    DOWN = Vertex(1,0)
    LEFT = Vertex(0,-1)
    UP = Vertex(-1,0)
    
    def preferred_dirs(self):
        if self == Dir.RIGHT:
            return [Dir.DOWN, Dir.RIGHT, Dir.UP]
        elif self == Dir.DOWN:
            return [Dir.LEFT, Dir.DOWN, Dir.RIGHT]
        elif self == Dir.LEFT:
            return [Dir.UP, Dir.LEFT, Dir.DOWN]
        else: #self == Dir.UP
            return [Dir.RIGHT, Dir.UP, Dir.LEFT]
                      

def get_hash_key(vertex, dir):
    return "%s-%s"%(vertex,dir.name)
    
def get_nth_char(n, string):
    if n < len(string):
        return string[n]
    else:
        return " "
      
def inside_shape(num_rows, num_cols, vertex):
    if vertex.i < 0 or vertex.j < 0:
        return False
    elif vertex.i >= num_rows or vertex.j >= num_cols:
        return False
    return True
    
def get_next_vertex(shape, num_rows, num_cols, start, dir):
    vertex = None
    next = start.move(dir.value)
    while inside_shape(num_rows, num_cols, next) and shape[next.i][next.j] != " ":
        if shape[next.i][next.j] == "+":
            return next
        next = next.move(dir.value)
    return None
    
def get_next_dir(shape, num_rows, num_cols, start, dir):
    if start:
        candidates = dir.preferred_dirs()
        for c in candidates:
            check = start.move(c.value)
            if inside_shape(num_rows, num_cols, check):
                if shape[check.i][check.j] != " ":
                    if c == Dir.RIGHT or c == Dir.LEFT:
                        if shape[check.i][check.j] != "|":
                            return c
                    else:
                        if shape[check.i][check.j] != "-":
                            return c
                        
    return None

def trace_polygon(shape, num_rows, num_cols, visited, start):
    dir = Dir.RIGHT
    sub_visited = {}
    vertices = []
    next = start
    while next and dir:
        hash_key = get_hash_key(next, dir)
        if hash_key in visited:
            vertices.clear()
            break
        elif hash_key in sub_visited:
            vertices = vertices[sub_visited[hash_key]::]
            break
        else:
            sub_visited[hash_key] = len(vertices)
            vertices.append(next)
            next = get_next_vertex(shape, num_rows, num_cols, next, dir)
            dir = get_next_dir(shape, num_rows, num_cols, next, dir)
            if not (next or dir):
                vertices.clear()
            
    visited.update(sub_visited)
    if vertices:
        return Polygon(vertices)
    else:
        return None
    
def break_evil_pieces(shape):
    shape_str = shape.split("\n")
    num_rows = len(shape_str)
    num_cols = 0
    for line in shape_str:
        num_cols = max(num_cols, len(line))
    shape = [[get_nth_char(j, shape_str[i]) for j in range(num_cols)] for i in range(num_rows)]
    min_i = 0
    max_i = num_rows - 1
    for i in range(num_rows):
        if "+" in shape[i]:
            min_i = i
            break
    for i in range(num_rows-1, -1, -1):
        if "+" in shape[i]:
            max_i = i
            break
    print(Polygon.stringify(shape))
    polylist = []
    hole_list = []
    visited = {}
    #trace outer perimeter
    outer_perimeter = None
    for j in range(num_cols):
        if shape[max_i][j] == "+":
            start = Vertex(i,j)
            outer_perimeter = trace_polygon(shape, num_rows, num_cols, visited, start)
            if outer_perimeter:
                break
        
    for i in range(min_i, max_i):
        for j in range(num_cols):
            if shape[i][j] == "+":
                start = Vertex(i,j)
                polygon = trace_polygon(shape, num_rows, num_cols, visited, start)
                if polygon:
                    if polygon.is_counterclockwise():
                        hole_list.append(polygon)
                    else:
                        polylist.append(polygon)  
    
    for l in range(len(hole_list)):
        for k in range(len(polylist)-1, -1, -1):
            if polylist[k].contains(hole_list[l]):
                polylist[k].add_contained(hole_list[l])
                break

    res = []
    for k in range(len(polylist)):
        res.append(polylist[k].to_shape())
    return res
_______________________________________________________
USE_BREAK_DISPLAY = True
from collections import deque
import sys
import os
import copy

graph = dict()

zoomedCanvas = None
walkedSpaces = None
closestPoints = None

walks = [(-1,-1),(0,-1), (1,-1), 
          (-1,0),        (1,0),
          (-1,1), (0,1), (1,1)]

simpleWalks = [-1,1]

dirs = ["left", "right", "top","bottom"]

class Node:
    def __init__(self, id, coor):
        self.id = id
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        self.coordinate = coor


    def __repr__(self):
        res = '{ %d' % self.id 
        res += '(' + str(self.coordinate) + ')'
        for d in dirs:
            n = self.__dict__[d]
            if n is not None:
                res += ', %s=%d' % (d, n.id)
                res += '({})'.format(n.coordinate)
        res += '}'
        return res

    def __str__(self):
        return str(self.id)

    def nonWalkedNeighbourPoint(self):
        coord = (self.coordinate[0]*2, self.coordinate[1]*2)
        for walk in walks:
            x,y = (coord[0] + walk[0], coord[1] + walk[1])
            if zoomedCanvas[y][x] is ' ' and not walkedSpaces[y][x]:
                return (x,y)
        return None

    
def makeDefaultCanvas(input):
  rows = [ x.rstrip() for x in input.split("\n") ]
  # for proper working filling mechanism
  max_len = max([ len(x) for x in rows ])
  res =  [' '*(max_len+2)] + [ ' ' + x + (max_len - len(x))*' ' + ' ' for x in rows ] + [' '*(max_len+2)] 
  canv = [ [' ' for x in range(len(res[0])*2)] for  y in range( len(res)*2) ]
  return res, canv


def makeGraph(input):

  nodeId = 1
  rows, canv2 = makeDefaultCanvas(input)

  global walkedSpaces
  #global closestPoints
  walkedSpaces = [[ False for x in range(len(canv2[0]))] for y in range(len(canv2))]
  #closestPoints = [[ False for x in range(len(canv2[0]))] for y in range(len(canv2))]
    
  v_lengths = [ 0 for x in range(max([ len(l) for l in rows]))]
  v_prevs = [ None for x in range(len(v_lengths)) ]
  for y, row in enumerate(rows):
      h_prev = None
      h_length = 0
      for x, char in enumerate(row):
          
          if char is '+':
            cur = (x,y)
            graph[cur] = Node(nodeId, cur)
            nodeId += 1
             
            if h_prev is not None:
               graph[h_prev].right = graph[cur]
               graph[cur].left = graph[h_prev]
               canv2[h_prev[1]*2][h_prev[0]*2+1] = '-'
               walkedSpaces[h_prev[1]*2][h_prev[0]*2+1] = True

            if v_prevs[x] is not None:
                graph[v_prevs[x]].bottom = graph[cur]
                graph[cur].top = graph[v_prevs[x]]
                canv2[v_prevs[x][1]*2+1][v_prevs[x][0]*2] = '|'
                walkedSpaces[v_prevs[x][1]*2+1][v_prevs[x][0]*2] = True

            canv2[y*2][x*2] = '+'
            #for w in walks:
            #    closestPoints[y*2+w[0]][x*2 + w[0]] = True

            h_prev = cur
            v_prevs[x] = cur
            h_length = 0
            v_lengths[x] = 0
                
          if char is '-':
              h_length += 1
              v_lengths[x] = 0
              v_prevs[x] = None
              canv2[y*2][x*2] = canv2[y*2][x*2 + 1] = '-'
              walkedSpaces[y*2][x*2] = walkedSpaces[y*2][x*2 + 1] = True

          if char is '|':
              v_lengths[x] += 1
              h_length = 0
              h_prev = None        
              canv2[y*2][x*2] = canv2[y*2 + 1][x*2] = '|'
              walkedSpaces[y*2][x*2] = walkedSpaces[y*2 + 1][x*2] = '|'


          if char is ' ':
              h_length = 0
              v_lengths[x] = 0
              v_prevs[x] = None
              h_prev = None

  global zoomedCanvas
  zoomedCanvas = canv2

  width, height = len(canv2[0]), len(canv2)
  for i in range(width):
      walkedSpaces[0][i] = walkedSpaces[height-1][i] = True
  for i in range(height):
      walkedSpaces[i][0] = walkedSpaces[i][width-1] = True

   

def render(points, joints):

    points = list(points)
    points.sort()

    xs = [k[0] for k in points]
    ys = [k[1] for k in points]

    sx = min(xs)
    sy = min(ys)
    ex = max(xs)
    ey = max(ys)

    canv = [ [ ' ' for x in range(ex - sx + 1) ] for y in range(ey - sy + 1) ]

    for point in points:
        y = point[1] - sy 
        x = point[0] - sx 
        canv[y][x] = '+'

        node = graph[point]

        turnLeft = node.left is not None and (node.id, node.left.id) in joints
        turnRight = node.right is not None and (node.id, node.right.id) in joints
        turnTop = node.top is not None and  (node.id, node.top.id) in joints
        turnBottom = node.bottom is not None and (node.id, node.bottom.id) in joints
                
        # render vertical lines
        if turnBottom:
            for j in range(node.bottom.coordinate[1] - node.coordinate[1] -1):
                canv[y+j+1][x] = '|'

            if not turnRight and not turnLeft:
                canv[y][x] = '|'

        if turnRight:
            for i in range(node.right.coordinate[0] - node.coordinate[0] -  1):
                canv[y][x + i + 1] = '-'

            if not turnBottom and not turnTop:
                canv[y][x] = '-'

    result = list()
    for row in canv:
        str = ''.join(row)
        result.append(str.rstrip())

    return '\n'.join(result)

def walk(point):

    global zoomedCanvas
    global walkedSpaces

    d = set()
    d.add(point)

    nodePoints = set()
    joints = set()

    while len(d) > 0:
        np = d.pop()
        walkedSpaces[np[1]][np[0]] = True

        for  x_shft, y_shft in walks:
            x,y = (np[0] + x_shft, np[1] + y_shft)

            if walkedSpaces[y][x]:
                continue

            c = zoomedCanvas[y][x]

            if c is ' ':
                if not walkedSpaces[y][x]:
                    d.add((x,y))
                continue

            if c is '+':
                origCanvPoint = (x//2,y//2)
                nodePoints.add(origCanvPoint)
                v = graph[origCanvPoint]

                if x_shft < 1 and zoomedCanvas[y][x+1] is '-':
                    joints.add((v.id, v.right.id))

                if x_shft > -1 and zoomedCanvas[y][x-1] is '-':
                    joints.add((v.id, v.left.id))

                if y_shft < 1 and zoomedCanvas[y+1][x] is '|':
                    joints.add((v.id, v.bottom.id))

                if y_shft > -1 and zoomedCanvas[y-1][x] is '|':
                    joints.add((v.id, v.top.id))



    return nodePoints, joints

   
def break_evil_pieces(input):

   graph.clear()
   
   makeGraph(input)

   walk((1,1))

   points = [k for k,v in graph.items()]
   points.sort()

   result = list()

   for point in points:
       v = graph[point]
       nearestPoint = v.nonWalkedNeighbourPoint()
       if nearestPoint is None:
           continue

       nodes, joints = walk(nearestPoint)

       #dumpZoomedCanvas()


       result.append(render(nodes, joints))
   return result

______________________________________________________
import sys, re
from collections import defaultdict, deque

DIRECTIONS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

NEARSIMBOlS = {"up": ((-0.5, -0.5), (-0.5, 0.5), lambda s1, s2: s1 in "+-" and s2 in "+-"),
               "down": ((0.5, -0.5), (0.5, 0.5), lambda s1, s2: s1 in "+-" and s2 in "+-"),
               "left": ((0.5, -0.5), (-0.5, -0.5), lambda s1, s2: s1 in "+|" and s2 in "+|"),
               "right": ((0.5, 0.5), (-0.5, 0.5), lambda s1, s2: s1 in "+|" and s2 in "+|")
               }


def shape_trim(shape):
    result = ""
    pos = 1000
    for line in shape.splitlines():
        if line.lstrip() != "":
            for i, sim in enumerate(line):
                if sim != " ":
                    pos = min(pos, i)
                    break

    for line in shape.splitlines():
        if line.lstrip() != "":
            result += line[pos:].rstrip() + "\n"
    return result


class Field:
    def __init__(self, shape):

        def countPos(shape):
            posX, posY = sys.maxsize, 0
            sizeX, sizeY = 0, 0
            f = True
            for row in shape.splitlines():
                if len(row.strip()) == 0:
                    if f:
                        posY += 1
                else:
                    f = False
                    posX = min(posX, len(row) - len(row.lstrip()))
                    sizeX = max(sizeX, len(row.lstrip()) - len(row) + len(row.rstrip()))
                    sizeY += 1
            if sizeX == 0 and sizeY == 0:
                posX, posY = 0, 0
            return sizeX, sizeY, posX, posY

        self.data = defaultdict(lambda: defaultdict(lambda: " "))

        self.sizeX, self.sizeY, self.posX, self.posY = countPos(shape)
        self.shapes = []
        self.bodyPoint = set()

        for row_num, row in enumerate(shape.strip('\n').splitlines()):
            for col_num in range(0, len(row) - self.posX):
                self.data[row_num][col_num] = str(row[col_num + self.posX])

        self.clearMask()

    def clearMask(self):
        self.mask = defaultdict(lambda: defaultdict(str))

    def drawField(self):
        result = ''
        for y in range(0, self.sizeY):
            result += ''.join(('%1s' % self.mask[y][x] for x in range(0, self.sizeX))) + '\n'
        return result

    def getBodys(self, pos, offset):

        arr = NEARSIMBOlS[offset]
        y1 = pos[0] - self.posY + arr[0][0]
        x1 = pos[1] - self.posX + arr[0][1]
        y2 = pos[0] - self.posY + arr[1][0]
        x2 = pos[1] - self.posX + arr[1][1]

        return (y1, x1) in self.bodyPoint or (y2, x2) in self.bodyPoint

    def drawFieldWithMask(self):
        result = ''

        xl, xr = sys.maxsize,0

        maxminY = list(self.mask.keys())
        yl, yr =  min(maxminY), max(maxminY)

        for row in self.mask:
            maxminX = list(self.mask[row].keys())
            xxl, xxr = min(maxminX), max(maxminX)
            xl = min(xxl,xl)
            xr = max(xxr,xr)

        yl = yl - 1 if yl > 1 else 0
        yr = yr + 1 if yr < self.sizeY else self.sizeY

        xl = xl - 1 if xl > 1 else 0
        xr = xr + 1 if xr < self.sizeX else self.sizeX

        for iy in range(yl, yr):
            for ix in range(xl, xr):

                s = self.data[iy][ix] if self.mask[iy][ix] is '*' else ' '

                if s is '+':

                    x = ix + self.posX
                    y = iy + self.posY

                    b_up = self.getBodys((y, x), "up")
                    b_down = self.getBodys((y, x), "down")
                    b_left = self.getBodys((y, x), "left")
                    b_right = self.getBodys((y, x), "right")

                    s_up = self.data[iy - 1][ix] if self.mask[iy - 1][ix] is '*' else ' '
                    s_down = self.data[iy + 1][ix] if self.mask[iy + 1][ix] is '*' else ' '
                    s_left = self.data[iy][ix - 1] if self.mask[iy][ix - 1] is '*' else ' '
                    s_right = self.data[iy][ix + 1] if self.mask[iy][ix + 1] is '*' else ' '

                    if not ((s_up is '+' or s_up is '|') and b_up) and not (
                            (s_down is '+' or s_down is '|') and b_down):
                        s = '-'
                    if not ((s_left is '+' or s_left is '-') and b_left) and not (
                            (s_right is '+' or s_right is '-') and b_right):
                        s = '|'
                result += s
            result += '\n'
        return shape_trim(result).strip("\n")

    def calcCord(self, pos, offset):

        arr = NEARSIMBOlS[offset]
        y1 = int(pos[0] - self.posY + arr[0][0])
        x1 = int(pos[1] - self.posX + arr[0][1])
        y2 = int(pos[0] - self.posY + arr[1][0])
        x2 = int(pos[1] - self.posX + arr[1][1])

        return (y1, x1, y2, x2, arr[2])

    def haveBorder(self, coord):
        sim1 = self.data[coord[0]][coord[1]]
        sim2 = self.data[coord[2]][coord[3]]
        return coord[4](sim1, sim2)

    def markMask(self, coord):
        self.mask[coord[0]][coord[1]] = '*'
        self.mask[coord[2]][coord[3]] = '*'

    def getNodesForExploring(self):
        result = set()
        for y in range(-1, self.sizeY):
            for x in range(-1, self.sizeX):
                result.add((y + self.posY + 0.5, x + self.posX + 0.5))
        return result


class Painter:

    def __init__(self, shape):
        self.shape = shape
        self.queue = deque()

    def paint(self, point, nodesForExploring):

        fClosed = True
        queue = self.queue
        shape = self.shape
        self.shape.bodyPoint = set()

        bodyPoint = self.shape.bodyPoint

        shape.clearMask()
        queue.append(point)

        while len(queue) > 0:
            current_point = queue.pop()

            if current_point in nodesForExploring:
                nodesForExploring.remove(current_point)
                bodyPoint.add(current_point)

                for offset in DIRECTIONS:
                    coord = self.shape.calcCord(current_point, offset)
                    shape.markMask(coord)
                    if not shape.haveBorder(coord):
                        ny = current_point[0] + DIRECTIONS[offset][0]
                        nx = current_point[1] + DIRECTIONS[offset][1]
                        if ny >= shape.posY and ny < shape.sizeY and nx >= shape.posX and nx < shape.sizeX:
                            queue.append((ny, nx))
                        else:
                            fClosed = False
        return fClosed


def break_evil_pieces(shape):
    print("@", flush=True)
    return break_evil_pieces_impl(shape_trim(shape))


def break_evil_pieces_impl(shape):
    field = Field(shape)

    shapes = []

    nodesForExploring = field.getNodesForExploring()

    while (len(nodesForExploring) > 0):
        start_point = nodesForExploring.pop()
        nodesForExploring.add(start_point)

        painter = Painter(field)
        if painter.paint(start_point, nodesForExploring):
            shapes.append(field.drawFieldWithMask())

    return shapes
_______________________________________________________________
def floodfill(shape, cells, y, x, color):
    stack = [[x, y]]
    while len(stack):
        x, y = stack.pop()
        if x >= len(cells[0]) or y >= len(cells) or cells[y][x]:
            continue
        cells[y][x] = color
        if x and shape[y][x] in " -" or (shape[y][x] == "+" and shape[y + 1][x] in " -"):
            stack.append([x - 1, y])
        if y and shape[y][x] in " |" or (shape[y][x] == "+" and shape[y][x + 1] in " |"):
            stack.append([x, y - 1])
        if x + 1 < len(shape[y]) and (shape[y][x + 1] in " -" or (shape[y][x + 1] == "+" and shape[y + 1][x + 1] in " -")):
            stack.append([x + 1, y])
        if y + 1 < len(shape) and (shape[y + 1][x] in " |" or (shape[y + 1][x] == "+" and shape[y + 1][x + 1] in " |")):
            stack.append([x, y + 1])

def fixPlus(shape, cells, color, x, y):
    # Return whether a "+" at this position should actually be a "-" or "|"
    colors = [cells[j][i] for i, j in [[x, y], [x, y - 1], [x - 1, y - 1], [x - 1, y], [x, y]]]
    surround = [shape[j][i] for i, j in [[x + 1, y], [x, y - 1], [x - 1, y], [x, y + 1], [x + 1, y]]]
    block = ("+-", "+|", "+-", "+|")
    pat = ""
    for i, blck in enumerate(block):
        pat += str(int(colors[i] == color and surround[i] in blck if colors[i] == colors[i+1] else color in (colors[i], colors[i+1])))
    return "-" if pat == "1010" else "|" if pat == "0101" else "+"


def break_evil_pieces(shape):
    shape = [line.rstrip() for line in shape.splitlines() if len(line.strip())]  # Strip spaces
    if not len(shape):
        return []
    width = max(len(line) for line in shape)
    # Make shape a rectangle (pad with spaces) and surround with 1 extra space so that all "outside" areas become connected
    shape = [(" " + line + " " * (width - len(line) + 1))[:] for line in shape]  # One column of spaces left and right
    shape = [[" "] * (width + 1)] + shape + [[" "] * (width + 1)]  # One line of spaces above and below
    print("\n".join(["".join(line) for line in shape]))
    cells = [[0] * (width + 1) for line in shape[:-1]] # Represents the interior of cells
    # Flood fill cells
    nextcolor = 1
    for y, line in enumerate(cells):
        for x, color in enumerate(line):
            if not color:
                floodfill(shape, cells, y, x, nextcolor)
                nextcolor += 1

    # Extract the areas. First "area" is the outside and is omited.
    result = []
    for areacolor in range(2, nextcolor):
        output = [[" "] * (width + 1) for line in shape]  # clean sheet
        minx = width
        miny = len(shape)
        prevline = cells[0]
        for y, line in enumerate(cells):
            prevcolor = line[0]
            for x, color in enumerate(line):
                if areacolor in (color, prevline[x], prevcolor) or x and areacolor == prevline[x - 1]:
                    minx = min(minx, x)
                    miny = min(miny, y)
                    maxy = y
                    output[y][x] = fixPlus(shape, cells, areacolor, x, y) if shape[y][x] == "+" else shape[y][x]
                prevcolor = color
            prevline = line
        result.append("\n".join(["".join(line[minx:]).rstrip() for line in output[miny:maxy + 1]]))
    return result
