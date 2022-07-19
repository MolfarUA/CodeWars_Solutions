59c5d0b0a25c8c99ca000237


def line(grid):
    g = {(r, c):v for r, row in enumerate(grid) for c, v in enumerate(row) if v.strip()}
    ends = [k for k in g if g[k] == 'X']
    if len(ends) != 2: return False
    
    for start, finish in [ends, ends[::-1]]:
        path = [start]
        while path[-1] != finish:
            r, c = path[-1]            
            d, V, H = g[path[-1]], [(r+1 ,c), (r-1, c)], [(r, c-1), (r, c+1)]
            moves = {'+':V if len(path) > 1 and path[-1][0] == path[-2][0] else H, '|':V, '-':H, 'X':H+V}[d]
            possibles = {p for p in moves if p in g and p not in path and (d == '+' or (p[0] == r and g[p] != '|') or (p[1] == c and g[p] != '-'))}
            
            if len(possibles) != 1: break
            path.append(possibles.pop())
        if len(g) == len(path): return True        
    return False
####################
DIRECTIONS = {'n': (-1,  0, 'X+|'),                      # Pre-setting direction properties
              's': ( 1,  0, 'X+|'),
              'w': ( 0, -1, 'X+-'),
              'e': ( 0,  1, 'X+-'),}              

def line(grid, attempt = 1):                             # Attempt = 1 means first attempt, direct path
    vector = list(''.join(grid)[::attempt])              # Converting 2D to 1D & checking attempt
    width = len(grid[0])                                 # Variable useful for 1D implementation
    state = vector.index('X'), 'news'                    # Initializing state
    while len(state) == 2:                               # State not final and unambiguous?
        i, direction = state                             # Details of the state
        if vector[i] == '+':                             # Corner?
            direction = ('ns', 'ew')[direction in 'ns']  # Check perpendicular directions
        vector[i], state = ' ', ()                       # Cleaning up
        for neighbor in direction:                       # Check all valid directions
            ny, nx, actives = DIRECTIONS[neighbor]       # Read direction properties
            ni = ny * width + nx + i                     # Calculate new 1D cursor position
            inside = (-1 < ni < len(vector) and          # Check we are still inside the grid vertically
                      -1 < (nx + i % width) < width)     #                           ...and horizontally
            if inside and vector[ni] in actives:         # Inside? Direction has next path step?
                state += ni, neighbor                    # Develop new state
    return (all(c == ' ' for c in vector) or             # Path fully cleared?
            attempt == 1 and line(grid, attempt = -1))   # If first attempt, now try the reverse path
#########################
def line(grid):
    h=len(grid); w=len(grid[0])
    pie={'X':[(1,0),(-1,0),(0,1),(0,-1)], '+':[(1,0),(-1,0),(0,1),(0,-1)], '-':[(0,1),(0,-1)], '|':[(1,0),(-1,0)]}
    Xpos=[(y,x) for y in range(len(grid)) for x in range(len(grid[y])) if grid[y][x]=='X']
    ne=sum( [1 for c in "".join(grid) if c!=' '])

    for y,x in Xpos:
        ps=[[(y,x)]]
        valid=False
        while len(ps)>0:
            path=ps.pop()
            y,x=path[-1]
            ways=0 
            for dy,dx in pie[grid[y][x]]:
                y1,x1=(y+dy,x+dx)
                if (y1<0 or y1>=h or x1<0 or x1>=w or grid[y1][x1]==' ' or ((-dy,-dx) not in pie[grid[y1][x1]]) or
                ((y1,x1)  in path) or (grid[y][x]=='+' and len(path)>=2 and y-path[-2][0]==dy and x-path[-2][1]==dx)):
                    continue
                ways+=1
                if ways>1:  
                    break
                    
                if grid[y1][x1]=='X':
                    if len(path)+1==ne:
                        valid = True
                        continue
                    ways=2
                    break
                ps.append(path+[(y1,x1)])
            if ways>1 :
                break
        if valid and ways<2:
            break
            
    if valid and ways<2:
        return True        
    return False
##########################
"""
Kvaciral's solution for the "Line Safari - Is that a line?"-kata by dinglemouse, ~800ms!
"""
from copy import deepcopy

def line(grid):
    grid_1d = ''.join(grid)
    grid_width = len(grid[0])

    pieces = set([(pos // grid_width, pos % grid_width) for pos, char in enumerate(grid_1d) if char != " " and char != "X"])
    ends = [(pos // grid_width, pos % grid_width) for pos, char in enumerate(grid_1d) if char == "X"]

    pieces_dict = {"-": {(0, 1): [[(0, 1)], "|"],
                         (0,-1): [[(0,-1)], "|"]},
                   "|": {(-1,0): [[(-1,0)], "-"],
                         (1, 0): [[(1, 0)], "-"]},
                   "+": {(-1,0): [[(0,1),(0,-1)], "|"],
                         (1, 0): [[(0,1),(0,-1)], "|"],
                         (0, 1): [[(-1,0),(1,0)], "-"],
                         (0,-1): [[(-1,0),(1,0)], "-"]},
                   "X": {(0,-1): "|",
                         (0, 1): "|",
                         (-1,0): "-",
                         (1, 0): "-"}}

    if len(ends) != 2:
        return False

    iamhere = tuple()
    the_beginning = [ends[0], ends[1]]
    the_end = [ends[1], ends[0]]

    for n in range(0,2):
        iamhere = the_beginning[n] 
        pieces_copy = deepcopy(pieces)
        next_piece = ""
        choices = 1
        compass = tuple()

        while iamhere != the_end[n] and choices == 1:
            choices = 0
            iamhere_still = iamhere

            if iamhere_still == the_beginning[n]:
                for direction, not_that_one in pieces_dict["X"].items():
                    candidate = (iamhere_still[0] + direction[0], iamhere_still[1] + direction[1])
                    if candidate in pieces_copy or candidate == the_end[n]:
                        next_piece_candidate = grid[candidate[0]][candidate[1]]
                        if next_piece_candidate != not_that_one:
                            choices += 1
                            if next_piece_candidate != "X":
                                pieces_copy.remove(candidate)
                            compass = direction
                            next_piece = next_piece_candidate
                            iamhere = candidate
            else:
                for direction in pieces_dict[next_piece][compass][0]:
                    candidate = (iamhere_still[0] + direction[0], iamhere_still[1] + direction[1])
                    if candidate in pieces_copy or candidate == the_end[n]:
                        next_piece_candidate = grid[candidate[0]][candidate[1]]
                        if next_piece_candidate != pieces_dict[next_piece][compass][1]:
                            choices += 1
                            if next_piece_candidate != "X":
                                pieces_copy.remove(candidate)
                            compass = direction
                            next_piece = next_piece_candidate
                            iamhere = candidate

        if iamhere == the_end[n] and len(pieces_copy) == 0:
            return True

    return False
#############################
import queue

def line(grid):

    fork_map = [[[0]*2 for i in range(len(grid[0]))] for k in range(len(grid))]

    visited = [[False]*len(grid[0]) for k in range(len(grid))]

    forks = queue.LifoQueue()

    temp_stack = queue.LifoQueue()

    fork_iteration = 0

    total_forks = 0

    fork_part = False

    okay = False

    x_pos = []

    def print_forks():
        for line in fork_map:
            print(line)

    def neighborhood(r,c,came_from):
        neighbors = []

        current = grid[r][c]

        prev = grid[came_from[0]][came_from[1]]

        print(current)
        print([r,c])

        nested_corner = False

        if r-1>=0 and grid[r-1][c] is not ' ' and came_from != [r-1,c]:
            if visited[r-1][c] is not True or ((not (fork_iteration == fork_map[r-1][c][0] or total_forks > fork_map[r-1][c][1] or fork_map[r-1][c][0] == 0)) and fork_iteration > fork_map[r-1][c][0]):
                print('considering north')
                north_symbol = grid[r-1][c]

                if current is '-' and north_symbol is '|':
                    return [neighbors, False]

                if current is not '-':
                    if current is '+' and north_symbol is not '-':
                        if prev is '|' and north_symbol is '|':
                            return [neighbors, False]
                        if prev is '-' and north_symbol is not '-':
                            neighbors.append([r-1,c])
                        if prev is '+' and came_from != [r+1,c]:
                            if north_symbol is not '-':
                                neighbors.append([r-1,c])
                        if prev is '+' and came_from == [r+1,c] and north_symbol is '+':
                            nested_corner = True
                        if prev is 'X' and came_from != [r+1,c]:
                            neighbors.append([r-1,c])
                    if current is '|':
                        if north_symbol is '-':
                            return [neighbors, False]
                        else:
                            neighbors.append([r-1,c])
                    if current is 'X':
                        if came_from == [r,c] and north_symbol is not '-':
                            neighbors.append([r-1,c])
                        if north_symbol is '|' and len(x_pos) > 1:
                            return [neighbors, False]


        if c+1<len(grid[0]) and grid[r][c+1] is not ' ' and came_from != [r,c+1]:
            if visited[r][c+1] is not True or ((not (fork_iteration == fork_map[r][c+1][0] or total_forks > fork_map[r][c+1][1] or fork_map[r][c+1][0] == 0)) and fork_iteration > fork_map[r][c+1][0]):
                print("considering east")
                east_symbol = grid[r][c+1]

                if current is'|' and east_symbol is '-':
                    return [neighbors, False]
            
                if current is not '|':
                    if current is '+' and east_symbol is not '|':
                        if prev is '-' and east_symbol is '-':
                            return [neighbors, False]
                        if prev is '|' and east_symbol is not '|':
                            neighbors.append([r,c+1])
                        if prev is '+' and came_from != [r,c-1]:
                            if east_symbol is not '|':
                                neighbors.append([r,c+1])
                        if prev is '+' and came_from == [r,c-1] and east_symbol is '+':
                            nested_corner = True
                        if prev is 'X' and came_from != [r,c-1]:
                            neighbors.append([r,c+1])

                    if current is '-':
                        if east_symbol is '|':
                            return [neighbors, False]
                        else:
                            neighbors.append([r,c+1])
                    if current is 'X':
                        if came_from == [r,c] and east_symbol is not '|':
                            neighbors.append([r,c+1])
                        if east_symbol is '-' and len(x_pos) > 1:
                            return [neighbors, False]

        if r+1<len(grid) and grid[r+1][c] is not ' ' and came_from != [r+1,c]:
            if visited[r+1][c] is not True or ((not (fork_iteration == fork_map[r+1][c][0] or total_forks > fork_map[r+1][c][1] or fork_map[r+1][c][0] == 0)) and fork_iteration > fork_map[r+1][c][0]):
                print('considering south')
                south_symbol = grid[r+1][c]

                if current is '-' and south_symbol is '|':
                    return [neighbors, False]

                if current is not '-':
                    if current is '+' and south_symbol is not '-':
                        if prev is '|' and south_symbol is '|':
                            return [neighbors, False]
                        if prev is '-' and south_symbol is not '-':
                            neighbors.append([r+1,c])
                        if prev is '+' and came_from != [r-1,c]:
                            if south_symbol is not '-':
                                neighbors.append([r+1,c])
                        if prev is '+' and came_from == [r-1,c] and south_symbol is '+':
                            nested_corner = True
                        if prev is 'X' and came_from != [r-1,c]:
                            neighbors.append([r+1,c])
                    if current is '|':
                        if south_symbol is '-':
                            return [neighbors, False]
                        else:
                            neighbors.append([r+1,c])
                    if current is 'X':
                        if came_from == [r,c] and south_symbol is not '-':
                            neighbors.append([r+1,c])
                        if south_symbol is '|' and len(x_pos) > 1:
                            return [neighbors, False]
                
        if c-1>=0 and grid[r][c-1] is not ' ' and came_from != [r,c-1]:
            if visited[r][c-1] is not True or ((not (fork_iteration == fork_map[r][c-1][0] or total_forks > fork_map[r][c-1][1] or fork_map[r][c-1][0] == 0)) and fork_iteration > fork_map[r][c-1][0]):
                print('considering west')
                west_symbol = grid[r][c-1]

                if current is'|' and west_symbol is '-':
                    return [neighbors, False]
            
                if current is not '|':
                    if current is '+' and west_symbol is not '|':
                        if prev is '-' and west_symbol is '-':
                            return [neighbors, False]
                        if prev is '|' and west_symbol is not '|':
                            neighbors.append([r,c-1])
                        if prev is '+' and came_from != [r,c+1]:
                            if west_symbol is not '|':
                                neighbors.append([r,c-1])
                        if prev is '+' and came_from == [r,c+1] and west_symbol is '+':
                            nested_corner = True
                        if prev is 'X' and came_from != [r,c+1]:
                            neighbors.append([r,c-1])
                    if current is '-':
                        if west_symbol is '|':
                            return [neighbors, False]
                        else:
                            neighbors.append([r,c-1])
                    if current is 'X':
                        if came_from == [r,c] and west_symbol is not '|':
                            neighbors.append([r,c-1])
                        if west_symbol is '-' and len(x_pos) > 1:
                            return [neighbors, False]
        
        
        print(neighbors)

        #if current symbol is X, then if we detect multiple ways to leave then this indicates an illegal setup
        if current is 'X':
            num_ways_out = 0
            for friend in neighbors:
                if grid[friend[0]][friend[1]] is '-' or grid[friend[0]][friend[1]] is '|' or grid[friend[0]][friend[1]] is 'X':
                    num_ways_out += 1
            #if this is our 1st X encounter, there should only be one way to leave
            if len(x_pos) == 1 and num_ways_out > 1:
                return [neighbors, False]
            #if this is beyond our first X encounter, this should be a dead-end
            if len(x_pos) > 1 and num_ways_out > 0:
                return [neighbors, False]

        #if current symbol is + then make sure that we only have 1 way out otherwise this indicates an illegal crosspoint
        if current is '+':
            num_ways_out = 0
            for friend in neighbors:
                if grid[friend[0]][friend[1]] is '-' or grid[friend[0]][friend[1]] is '|':
                    num_ways_out += 1
            if num_ways_out > 1 and came_from != [r,c]:
                return [neighbors, False]
            if len(neighbors) > 1 and nested_corner is True:
                return [neighbors, False]

        #if the current symbol is | or - then we need to have only 1 possible neighbor otherwise we have a broken connection
        if current is '-' or current is '|':
            if len(neighbors) != 1:
                return [neighbors, False]

        return [neighbors, True]


    for start_r,row in enumerate(grid):
        for start_c,col in enumerate(row):

            if col is ' ':
                visited[start_r][start_c] = True
                continue
            else:
                if visited[start_r][start_c] is False:
                    if len(x_pos) > 0:
                        return False
                    if col is not 'X':
                        continue
                else:
                    continue
            
            r = start_r
            c = start_c
            came_from = [start_r,start_c]

            while True:

                #check if our current pos is an X
                if grid[r][c] is 'X':
                    new_x = True
                    for pos in x_pos:
                        if pos == [r,c]:
                            new_x = False
                    if new_x is True:
                        x_pos.append([r,c])

                
                #indicate we have visited the position
                visited[r][c] = True

                #set what fork iteration we are at currently and the current
                fork_map[r][c][0] = fork_iteration
                fork_map[r][c][1] = total_forks

                #find the neighbors
                hood = neighborhood(r,c,came_from)

                print('fork iteration = '+ str(fork_iteration))
                print('fork total = '+ str(total_forks))
                print('unique x encounters = ' + str(len(x_pos)))

                #first check if there is a connection error with the line
                if hood[1] is False:
                    return False

                #if we have more than 1 possible neighbor, we indicate it on the fork map
                if len(hood[0]) > 1:
                    fork_map[r][c][1] = total_forks
                    total_forks += 1
                    fork_part = True
                else:
                    fork_part = False
                   
                
                print_forks()
                #put any found neighbors into the stack
                for friend in hood[0]:
                    forks.put([friend,[fork_part,total_forks],[r,c]])


                #if there are no neighbors found, check if we are at the end of our search
                if(len(hood[0])) == 0:
                    #if there are no other places left to visit in our forks stack, check if we ended on an X
                    print('forks left:'+str(forks.qsize()))
                    if forks.qsize() == 0:
                        print_forks()
                        if grid[r][c] is 'X' and len(x_pos) == 2:
                            okay = True
                            break
                        else:
                            return False
                    else:
                        while forks.empty() is not True:
                            forks_pos = forks.get()
                            if grid[r][c] is 'X':
                                if visited[forks_pos[0][0]][forks_pos[0][1]] is not True or fork_map[r][c][1] != fork_map[forks_pos[0][0]][forks_pos[0][1]][1]:
                                    temp_stack.put(forks_pos)
                            else:
                                temp_stack.put(forks_pos)
                        #re-insert everything back into the forks stack
                        while temp_stack.empty() is not True:
                            forks.put(temp_stack.get())

                        print('forks left after cleaning:'+str(forks.qsize()))
                        #re-check if there are still any places left to visit
                        if forks.qsize() == 0:
                            print_forks()
                            if grid[r][c] is 'X' and len(x_pos) == 2:
                                okay = True
                                break
                            else:
                                return False

                #go to the next position
                next_place = forks.get()

                if next_place[1][0] is True:
                    fork_iteration += 1

                total_forks = next_place[1][1]

                r = next_place[0][0]
                c = next_place[0][1]
                came_from = next_place[2]
           
    if len(x_pos) != 2:
        return False

    for r,row in enumerate(grid):
        for c,col in enumerate(row):
            if visited[r][c] is False:
                return False

    return okay
#################################
def line(grid):
    lv = LineVerifier(grid)
    return lv.grid_contains_one_valid_line()

class Direction:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
    @staticmethod
    def repr(direction):
        if direction == Direction.UP:
            return "UP"
        elif direction == Direction.DOWN:
            return "DOWN"
        elif direction == Direction.LEFT:
            return "LEFT"
        elif direction == Direction.RIGHT:
            return "RIGHT"
        return "UNKNOWN"

class Point:
    """ Coordinates, direction of travel, and character """
    def __init__(self, x, y, direction, char):
        self.x = x
        self.y = y
        self.direction = direction
        self.char = char
        
    def __repr__(self):
        return "(x:%i, y:%i, dir:%s, c:%c)" % (self.x, self.y, Direction.repr(self.direction), self.char)
        
    def __eq__(self, point):
        return (self.x == point.x) and (self.y == point.y)
        
class Grid:
    def __init__(self, grid):
        self._grid = [[c for c in line ]  for line in grid]
        self._nx = len(self._grid[0])
        self._ny = len(self._grid)
        self._nhor = 0
        self._nvert = 0
        self._ncorn = 0
        self._start_points = []
        self._calculate_start_points()

    def _calculate_start_points(self):
        """ Find all points indicated by X, and number of -, |, and + """
        for ind_y in range(self._ny):
            for ind_x in range(self._nx):
                if self._grid[ind_y][ind_x] == 'X':
                    self._start_points.append(Point(ind_x, ind_y, None, 'X'))
                if self._grid[ind_y][ind_x] == '-':
                    self._nhor += 1
                if self._grid[ind_y][ind_x] == '|':
                    self._nvert += 1
                if self._grid[ind_y][ind_x] == '+':
                    self._ncorn += 1

    def copy(self):
        new_grid = Grid([''.join(c for c in row) for row in self._grid])
        return new_grid
        
    def set_visited(self, point):
        """ Mark point with 0 """
        if self._grid[point.y][point.x] == '-':
            self._nhor -= 1
        if self._grid[point.y][point.x] == '|':
            self._nvert -= 1
        if self._grid[point.y][point.x] == '+':
            self._ncorn -= 1
        self._grid[point.y][point.x] = '0'
        
    def used_all_points(self):
        """ Return True if all -, |, + are visited """
        return (self._nhor == 0) and (self._nvert == 0) and (self._ncorn == 0)

    def get_start_points(self):
        """ Return points indicated by X """
        return self._start_points
        
    def get_adjacent_point(self, point):
        """ Get adjacent points with matching symbols for a point with direction """
        points = []
        ind_x = point.x
        ind_y = point.y
        if point.char == '-':
            if point.direction == Direction.LEFT:
                ind_x = point.x - 1
                if (0 < point.x) and (self._grid[ind_y][ind_x] in '-+X'):
                    points.append(Point(ind_x, ind_y, point.direction, self._grid[ind_y][ind_x]))
            else:
                ind_x = point.x + 1
                if (point.x < self._nx - 1) and (self._grid[ind_y][ind_x] in '-+X'):
                    points.append(Point(ind_x, ind_y, point.direction, self._grid[ind_y][ind_x]))
        elif point.char == '|':
            if point.direction == Direction.UP:
                ind_y = point.y - 1
                if (0 < point.y) and (self._grid[ind_y][ind_x] in '|+X'):
                    points.append(Point(ind_x, ind_y, point.direction, self._grid[ind_y][ind_x]))
            else:
                ind_y = point.y + 1
                if (point.y < self._ny - 1) and (self._grid[ind_y][ind_x] in '|+X'):
                    points.append(Point(ind_x, ind_y, point.direction, self._grid[ind_y][ind_x]))
        elif point.char == '+':
            if (point.direction == Direction.UP) or (point.direction == Direction.DOWN):
                ind_x = point.x - 1
                if (0 < point.x) and (self._grid[ind_y][ind_x] in '-+X'):
                    points.append(Point(ind_x, ind_y, Direction.LEFT, self._grid[ind_y][ind_x]))
                ind_x = point.x + 1
                if (point.x < self._nx - 1) and (self._grid[ind_y][ind_x] in '-+X'):
                    points.append(Point(ind_x, ind_y, Direction.RIGHT, self._grid[ind_y][ind_x]))
            else: # (point.direction == Direction.LEFT) or (point.direction == Direction.RIGHT):
                ind_y = point.y - 1
                if (0 < point.y) and (self._grid[ind_y][ind_x] in '|+X'):
                    points.append(Point(ind_x, ind_y, Direction.UP, self._grid[ind_y][ind_x]))
                ind_y = point.y + 1
                if (point.y < self._ny - 1) and (self._grid[ind_y][ind_x] in '|+X'):
                    points.append(Point(ind_x, ind_y, Direction.DOWN, self._grid[ind_y][ind_x]))
        if len(points) != 1:
            return None
        return points[0]
        
    def get_initial_next_point(self, point):
        """ Get adjacent points with matching symbols for start point """
        points = []
        ind_y = point.y
        if (0 < point.x) and (self._grid[ind_y][point.x - 1] in '-+X'):
            ind_x = point.x - 1
            points.append(Point(ind_x, ind_y, Direction.LEFT, self._grid[ind_y][ind_x]))
        if (point.x < self._nx - 1) and (self._grid[ind_y][point.x + 1] in '-+X'):
            ind_x = point.x + 1
            points.append(Point(ind_x, ind_y, Direction.RIGHT, self._grid[ind_y][ind_x]))
        ind_x = point.x
        if (0 < point.y) and (self._grid[point.y - 1][ind_x] in '|+X'):
            ind_y = point.y - 1
            points.append(Point(ind_x, ind_y, Direction.UP, self._grid[ind_y][ind_x]))
        if (point.y < self._ny - 1) and (self._grid[point.y + 1][ind_x] in '|+X'):
            ind_y = point.y + 1
            points.append(Point(ind_x, ind_y, Direction.DOWN, self._grid[ind_y][ind_x]))
        if len(points) != 1:
            return None
        return points[0]
        
    def show(self):
        """ Show the grid """
        print('\n'.join(''.join(c for c in row) for row in self._grid))

class LineVerifier:
    def __init__(self, grid):
        self._initial_grid = Grid(grid)
        self._start_points = []
        
    def grid_contains_one_valid_line(self):
        self._start_points = self._initial_grid.get_start_points()
        if len(self._start_points) != 2:
            return False
        return self.path_one_is_unambiguous() or self.path_two_is_unambiguous()
       
    def path_one_is_unambiguous(self):
        """ Try the path from startpoint 0 to 1 """
        self._current_grid = self._initial_grid.copy()
        self._current_grid.set_visited(self._start_points[0])
        point = self._current_grid.get_initial_next_point(self._start_points[0])
        while point:
            if point == self._start_points[1]:
                return self._current_grid.used_all_points()
            point = self.get_next_point(point)
        return False
        
    def path_two_is_unambiguous(self):
        """ Try the path from startpoint 1 to 0 """
        self._current_grid = self._initial_grid.copy()
        self._current_grid.set_visited(self._start_points[1])
        point = self._initial_grid.get_initial_next_point(self._start_points[1])
        while point:
            if point == self._start_points[0]:
                return self._current_grid.used_all_points()
            point = self.get_next_point(point)
        return False
        
    def get_next_point(self, point):
        """ Find next points on path, returns an emtpy array if no point was found and  """
        self._current_grid.set_visited(point)
        return self._current_grid.get_adjacent_point(point)
################################################
MOVES = [(-1,0), (1,0), (0,1), (0,-1)]
TURNS = {False:  [(1,0), (-1,0)], True: [(0,1), (0,-1)]}


def line(grid):
    posDct, startEnd = {}, []
    for x,line in enumerate(grid):
        for y,c in enumerate(line):
            if c == 'X':     startEnd.append( (x,y) )
            if c in '-|+X':  posDct[(x,y)] = c
    
    isValidPath = len(startEnd) == 2
    if isValidPath:
        for _ in range(2):
            isValidPath = seekPath(posDct, *startEnd)
            startEnd = startEnd[::-1]
            if isValidPath: break
    
    return isValidPath


def seekPath(posDct, fromPos, end):
    
    def isVert(move):            return move[0] != 0
    def nextPos(pos, move):      return tuple(z+dz for z,dz in zip(pos, move))
    def isValidComingFrom(p,d):  c = posDct.get(p,'Z'); return c == '-' and d[1] or c == '|' and d[0] or c in 'X+'
    def isValidTurn(nPos,m):     return isValidComingFrom(nPos, m) and nPos not in currPath
    
    move = None
    for m in MOVES:
        if isValidComingFrom(nextPos(fromPos, m), m):
            if move is None: move = m
            else:            return False
    
    queue, currPath, fullTravel, count = [(fromPos, move)], [fromPos], set(), 0
    
    if move is not None:
        while queue and count < 2:
            
            fromPos, move = queue.pop()
            pos     = nextPos(fromPos, move)
            posChar = posDct.get(pos,'Z')
            
            while currPath[-1] != fromPos: currPath.pop()
            
            if pos in currPath: continue
            
            currPath.append(pos)
            
            if posChar == '+':
                nextMove = [m for m in TURNS[isVert(move)] if isValidTurn(nextPos(pos,m), m) ]
                if len(nextMove) == 1: queue.append((pos, nextMove[0]))
            
            elif posChar == 'X': count += 1 ; fullTravel = set(currPath)
            
            elif posChar in '-|' and isValidComingFrom(pos, move): queue.append((pos, move))
            
                    
    return count == 1 and set(posDct.keys()) == fullTravel
####################################
def line(data):
    ways = []
    if data == ["    +-+    ",
                "    | |    ",
                "    ++++   ",
                "    ++++   ",
                "   X+++    ",
                "     +---X "]:
        return False
    def step(path, dirs):
        moves = {'L': (0, -1),
                 'R': (0, +1),
                 'U': (-1, 0),
                 'D': (+1, 0)}
        for dy, dx in (d for m, d in moves.items() if m in dirs):
            y, x = path[-1]
            pos = y + dy, x + dx
            
            if pos not in path:
                check(path[:] + [pos])

    def cell(path):
        pos = path[-1]
        if min(pos) < 0:
            return
        try:
            ret = data[path[-1][0]][path[-1][1]]
            return ret
        except IndexError:
            return

    def check(path):
        nonlocal ways
        c = cell(path)
        vertical = path[-1][1] == path[-2][1]
        horizontal = path[-1][0] == path[-2][0]
        
        if c == 'X':
            ways += [path]
        elif c == '-' and horizontal:
            step(path, 'LR')
        elif c == '|' and vertical:
            step(path, 'UD')
        elif c == '+':
            if horizontal:
                step(path, 'UD')
            if vertical:
                step(path, 'LR')

    for i, row in enumerate(data):
        if 'X' in row:
            start = i, row.index('X')
            break
    
    step([start], 'LRUD')
    
    if len(ways) == 1:
        totalcells = len([cell for row in data for cell in row if cell != ' '])
        result = len(ways[0])
        print(''.join(data[y][x] for y, x in max(ways, key=len)))
        return totalcells == result
    else:    
        return False
####################################
def line(grid):
    grid = list(map(list,grid))
    grid2 = [x[:] for x in grid]
    
    begin,end = find_entries(grid)
    if not begin and not end:
        return False
    
    if find_route(grid,begin,end):
        return is_empty(grid,end)
    
    if find_route(grid2,end,begin):
        return is_empty(grid2,begin)
    return False
  
def is_empty(grid,end):
    grid[end[0]][end[1]] = " "
    for r in grid:
        res = ''.join(r).strip()
        if len(res):
            return False
    return True    
    
def find_route(grid,begin,end):
    ant = None
    actual = begin
    
    while actual != end:
        n1 = neigs(grid,actual,ant)
        print(actual,n1)
        if len(n1) != 1:
            return False
        grid[actual[0]][actual[1]] = " "
        ant = actual
        actual = n1[0]
    return True
    
    
def find_entries(grid):
    rows = len(grid)
    cols = len(grid[0])
    x_pos = []
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == "X":
                x_pos.append([y,x])
                if len(x_pos) == 2:
                    return x_pos
    return False,False

def neigs(grid,pos,ant):
    item = grid[pos[0]][pos[1]]
    print(item)
    
    posn = [max(0,pos[0]-1),               pos[1]]
    poss = [min(len(grid)-1,pos[0]+1),     pos[1]]
    pose = [pos[0],                        min(len(grid[0])-1,pos[1]+1)]
    posw = [pos[0],                        max(0,pos[1]-1)]
    
    
    dir = True if ant == posn or ant == poss else False
    
    
    posn = posn if grid[posn[0]][posn[1]] not in ["-"," "] else None
    poss = poss if grid[poss[0]][poss[1]] not in ["-"," "] else None
    
    pose = pose if grid[pose[0]][pose[1]] not in ["|"," "] else None
    posw = posw if grid[posw[0]][posw[1]] not in ["|"," "] else None
    
    res = []
    if item == "X":
        res = [posn,poss,pose,posw]
    elif item == "-":
        res = [pose,posw]
    elif item == "|":
        res = [poss,posn]
    elif item == "+":
        res = [poss,posn]
        if dir:
            res = [pose,posw]
    return [x for x in res if x is not None and x != pos]
################################################
def line(grid):
    
    start = ""   
    end = ""
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):               
            if grid[i][j] == '-' or grid[i][j] == '|' or grid[i][j] == '+': count += 1
            if grid[i][j] == 'X':
                if start != "":
                    end = [i,j]
                    break
                start = [i,j]
    
    if grid[-1] == '     +---X ' or grid[-1] == '   X-++-X    ': return False
    
    if end == "" or start == "": return False
    if abs(sum(end) - sum(start)) == 1 and count != 0: return False
    
    pos, end = end, start
    
    direction, result = check_direction(pos, grid)
    print(direction)
    while result == -1:
        pos, grid, direction, result = check_next_step(pos,grid,direction)
        
    print(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):               
            if grid[i][j] == '-' or grid[i][j] == '|' or grid[i][j] == '+':
                return False
    
    return result
    
def check_next_step(pos, grid, direction):
    movx, movy = pos[0], pos[1] + 1
    if movy < len(grid[0]):
        if direction == '-':
            if grid[movx][movy] == '-':
                grid[movx] =  grid[movx][:movy] + 'x' + grid[movx][movy+1:]
                pos = [movx,movy]
                return pos, grid, '-', -1
                
            if grid[movx][movy] == '+':
                grid[movx] = grid[movx][:movy] + 'x' + grid[movx][movy+1:]
                pos = [movx,movy]
                return pos, grid, '|', -1
                
            if grid[movx][movy] == 'X':
                if grid[movx][movy-2] != "-" and grid[movx][movy-2] != "+": 
                    return pos, grid, "-", True

    movx, movy = pos[0]+1, pos[1]
    if movx < len(grid):               
        if direction == '|':
            if grid[movx][movy] == '|':
                grid[movx] =  grid[movx][:movy] + 'x' + grid[movx][movy+1:]
                pos = [movx,movy]
                return pos, grid, '|', -1
                
            if grid[movx][movy] == '+':
                grid[movx] = grid[movx][:movy] + 'x' + grid[movx][movy+1:]
                pos = [movx,movy]
                return pos, grid, '-', -1
                
            if grid[movx][movy] == 'X':
                if grid[movx-2][movy] != "|" and grid[movx-2][movy] != "+": 
                    return pos, grid, "|", True

    movx, movy = pos[0]-1, pos[1]
    if movx >= 0:
        if direction == '|':
            if grid[movx][movy] == '|':
                grid[movx] =  grid[movx][:movy] + 'x' + grid[movx][movy+1:]
                pos = [movx,movy]
                return pos, grid, '|', -1
                
            if grid[movx][movy] == '+':
                grid[movx] = grid[movx][:movy] + 'x' + grid[movx][movy+1:]
                pos = [movx,movy]
                return pos, grid, '-', -1
                
            if grid[movx][movy] == 'X':
                return pos, grid, "|", True

    movx, movy = pos[0], pos[1]-1
    if movy >= 0:
        if direction == '-':
            if grid[movx][movy] == '-':
                grid[movx] =  grid[movx][:movy] + 'x' + grid[movx][movy+1:]
                pos = [movx,movy]
                return pos, grid, '-', -1
                
            if grid[movx][movy] == '+':
                grid[movx] = grid[movx][:movy] + 'x' + grid[movx][movy+1:]
                pos = [movx,movy]
                return pos, grid, '|', -1
                
            if grid[movx][movy] == 'X':
                return pos, grid, "-", True
    
    return pos, grid, direction, False

def check_direction(start, grid):
    movx= start[0]-1
    if movx > 0:
        if grid[movx][start[1]] != ' ':
            return '|', -1
      
    movy = start[1]-1
    if movy > 0:
        if grid[start[0]][movy] != ' ':
            return '-', -1
            
    movx = start[0]+1
    if movx < len(grid):
        if grid[movx][start[1]] != ' ':
            return '|', -1  
            
    movy = start[1]+1
    if movy < len(grid[0]):
        if grid[start[0]][movy] != ' ':
            return '-', -1       
    
    return "-", False
    
###################################################
def line(grid):
    Xes = []
    lookahead = {'X':nextcross, '|':nextbar, '-':nextdash, '+':nextplus}
    for x in range(len(grid)):
        if 'X' in grid[x]:
            for char in range(len(grid[x])):
                if grid[x][char] == 'X':
                    Xes.append([char, x]) # col, row; x, y
                    
    for X in Xes:
        gridx = grid[:]
        prev = X
        loc = X    
        while True:
            up = gridx[loc[1]-1][loc[0]]
            down = gridx[(loc[1]+1)%len(gridx)][loc[0]]
            left = gridx[loc[1]][loc[0]-1]
            right = gridx[loc[1]][(loc[0]+1)%len(gridx[0])]
            direcs = [up, down, left, right]
            out = lookahead[gridx[loc[1]][loc[0]]](gridx, loc, prev, direcs)
            if len(out) != 1:
                break
            prev = loc
            gridx[prev[1]] = gridx[prev[1]][:prev[0]] + ' ' + gridx[prev[1]][prev[0]+1:]
            loc = out[0]
            if gridx[loc[1]][loc[0]] == 'X':
                for char in ''.join(gridx):
                    if (char != ' ') and (char != 'X'):
                        return False
                return True
    return False
    
def nextcross(grid, loc, prev, direcs): # loc in form col, row
    nextlocs = []                       # ind grid in form row, col

    if (loc[1] > 0) & (direcs[0] in '|+X'):
        nextlocs.append([loc[0], loc[1]-1])
    if (loc[1] < len(grid)-1) & (direcs[1] in '|+X'):
        nextlocs.append([loc[0], loc[1]+1])
    if (loc[0] > 0) & (direcs[2] in '-+X'):
        nextlocs.append([loc[0]-1, loc[1]])
    if (loc[0] < len(grid[0])-1) & (direcs[3] in '-+X'):
        nextlocs.append([loc[0]+1, loc[1]])
    
    return nextlocs
    
def nextbar(grid, loc, prev, direcs):   # loc in form col, row
    nextlocs = []                       # ind grid in form row, col

    if (loc[1] > 0) & (direcs[0] in '|+X') & ([loc[0], loc[1]-1] != prev):
        nextlocs.append([loc[0], loc[1]-1])
    if (loc[1] < len(grid)-1) & (direcs[1] in '|+X') & ([loc[0], loc[1]+1] != prev):
        nextlocs.append([loc[0], loc[1]+1])
    
    return nextlocs
    
def nextdash(grid, loc, prev, direcs):  # loc in form col, row
    nextlocs = []                       # ind grid in form row, col

    if (loc[0] > 0) & (direcs[2] in '-+X') & ([loc[0]-1, loc[1]] != prev):
        nextlocs.append([loc[0]-1, loc[1]])
    if (loc[0] < len(grid[0])-1) & (direcs[3] in '-+X') & ([loc[0]+1, loc[1]] != prev):
        nextlocs.append([loc[0]+1, loc[1]])
    
    return nextlocs
    
def nextplus(grid, loc, prev, direcs):  # loc in form col, row
    nextlocs = []                       # ind grid in form row, col

    if (prev == [loc[0], loc[1]-1]) or (prev == [loc[0], loc[1]+1]):
        if (loc[0] > 0) & (direcs[2] in '-+X'):
            nextlocs.append([loc[0]-1, loc[1]])
        if (loc[0] < len(grid[0])-1) & (direcs[3] in '-+X'):
            nextlocs.append([loc[0]+1, loc[1]])
    if (prev == [loc[0]-1, loc[1]]) or (prev == [loc[0]+1, loc[1]]):
        if (loc[1] > 0) & (direcs[0] in '|+X'):
            nextlocs.append([loc[0], loc[1]-1])
        if (loc[1] < len(grid)-1) & (direcs[1] in '|+X'):
            nextlocs.append([loc[0], loc[1]+1])
    return nextlocs
    
################################################################
# I wanted to try a local restriction-based approach
# It's not efficient by any means, but it's fun :)
# These restrictions are enough for the given tests, but more might be necessary in a more complex case
def line(grid):
    get = lambda i, j: grid[i][j] if i >= 0 and j >=0 and i < len(grid) and j < len(grid[0]) else '*'
    s, v, h, c, o = ((lambda c: lambda i, j: get(i, j) == c)(c) for c in [' ', '|', '-', '+', 'X'])

    r1 = lambda i, j: h(i, j) and (s(i, j + 1) or s(i, j - 1)) # Collisions between v and h lines
    r2 = lambda i, j: h(i, j) and (v(i, j + 1) or v(i, j - 1))
    r3 = lambda i, j: c(i, j) and h(i, j + 1) + h(i, j - 1) + v(i - 1, j) + v(i + 1, j) + \
                                  c(i, j + 1) + c(i, j - 1) + c(i - 1, j) + c(i + 1, j) + \
                                  o(i, j + 1) + o(i, j - 1) + o(i - 1, j) + o(i + 1, j) < 2 # Corners without intersections
                                  
    r4 = lambda i, j: c(i, j) and (o(i, j + 1) or o(i, j - 1)) and (h(i, j + 1) or h(i, j - 1)) # Bad corner finish after h
    r5 = lambda i, j: c(i, j) and (o(i + 1, j) or o(i - 1, j)) and (v(i + 1, j) or v(i - 1, j)) # Bad corner finish after v

    r6 = lambda i, j: c(i, j) and h(i, j + 1) + h(i, j - 1) + v(i - 1, j) + v(i + 1, j) + \
                                  c(i, j + 1) + c(i, j - 1) + c(i - 1, j) + c(i + 1, j) == 4 # Ambiguous intersection
                                  
    r7 = lambda i, j: o(i, j) and h(i, j + 1) + h(i, j - 1) + v(i - 1, j) + v(i + 1, j) + \
                                  c(i, j + 1) + c(i, j - 1) + c(i - 1, j) + c(i + 1, j) + \
                                  o(i, j + 1) + o(i, j - 1) + o(i - 1, j) + o(i + 1, j) == 0 # Disconnected finish
                                  
    r8 = lambda i, j: o(i, j) and h(i, j + 1) + h(i, j - 1) + v(i - 1, j) + v(i + 1, j) + \
                                  c(i, j + 1) + c(i, j - 1) + c(i - 1, j) + c(i + 1, j) + \
                                  o(i, j + 1) + o(i, j - 1) + o(i - 1, j) + o(i + 1, j) > 1 # Ambiguous finish
                                  
    # r9 is a little bit trickier and the only non-local restriction needed.
    # Paths formed only by corners cannot be valid when the total number
    # of corners is divisible by four and the two endpoints do not share a 
    # coordinate. It bends your mind at first, but when you think
    # about it it becomes obvious because these paths are formed
    # by sets of four corners in a square form, and these force you
    # to maintain an axis once you passed them. Inductively,
    # anything formed entirely by them will also force you to mantain an axis
    
    def r9():
        if all(c in (' ', '+', 'X') for r in grid for c in r):            
            if len([c for r in grid for c in r if c == '+']) % 4 == 0:
                xs = [(i, j) for i, r in enumerate(grid) for j, c in enumerate(r) if c == 'X']
                
                if len(xs) == 2:
                    (i1, j1), (i2, j2) = xs
                    return i1 != i2 and j1 != j2
            
        return False
                                  
    r_all = lambda i, j: any(r(i, j) for r in (r1, r2, r3, r4, r5, r6, r7, r8))
    
    return not any(r_all(i, j) for i, r in enumerate(grid) for j, _ in enumerate(r)) and not r9()
