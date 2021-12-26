from itertools import permutations,starmap
from heapq import *


INF   = float("inf")
MOVES = (( (0,1), (-1,0), (0,-1), (1,0) ),        # Turn anticlockwise
         ( (1,0), (0,-1), (-1,0), (0,1) ))        # Turn clockwise


def four_pass(stations):
    print(stations)
    def dfs(pOrder, paths, n=0):
        if n==3: yield paths[:]
        else:
            _,p1,p2 = pOrder[n]
            for moves in MOVES:
                path = aStar(p1,p2,board,moves)
                if path is None: continue
                
                paths.append(path)
                updateBoard(board, path)
                yield from dfs(pOrder, paths, n+1)
                updateBoard(board, path, free=1)
                paths.pop()
                
    
    pts      = [divmod(s,10) for s in stations]
    segments = [(i, pts[i], pts[i+1]) for i in range(3)]
    MIN      = 1 + sum(manhattan(p1,p2) for _,p1,p2 in segments)
    
    shortestPath = None
    for pOrder in permutations(segments):
        board = [[1]*10 for _ in range(10)]
        updateBoard(board, pts)
        
        for p in dfs(pOrder, []):
            length = 4 + sum(map(len,p))
            
            if not shortestPath or length < len(shortestPath):
                shortestPath = rebuildPath(pOrder, p)
                
            if len(shortestPath) == MIN:
                return shortestPath
    
    return shortestPath
    
    

def manhattan(*args): return sum(abs(b-a) for a,b in zip(*args))
def linearize(p):     return 10*p[0]+p[1]

def updateBoard(board, inPath, free=0):
    for x,y in inPath: board[x][y] = free
    
def rebuildPath(pOrder, shortest):
    fullPath = []
    for (i,p1,p2),path in sorted(zip(pOrder, shortest)):
        fullPath.append(linearize(p1))
        fullPath.extend(map(linearize,path))
    fullPath.append(linearize(p2))
    return fullPath


def aStar(p1,p2,board,moves):
    prev  = [[None]*10 for _ in range(10)]
    local = [[(INF,0) if free else (0,0) for free in r] for r in board]                # (heuristic, rotation index)
    local[p2[0]][p2[1]] = (INF,0)
    
    q = [(manhattan(p1,p2), 0, 0, p1)]                    # queue: (cost+h, rotation index, cost, (x,y))
    while q and not q[0][-1] == p2:
        _,_,cost,src = heappop(q)
        x,y = src
        for i,a,b in ( (i,x+dx,y+dy) for i,(dx,dy) in enumerate(moves) if 0<=x+dx<10 and 0<=y+dy<10):
            pos, nCost = (a,b), cost+1
            if (nCost,i) < local[a][b]:
                prev[a][b], local[a][b] = src, (nCost,i)
                heappush(q, (nCost+manhattan(pos, p2), i, nCost, pos))
    
    if q:
        p, (x,y) = [], q[0][-1]
        while 1:
            x,y = pos = prev[x][y]
            if pos == p1: break
            p.append(pos)
        return p[::-1]
        
        
##########################
from itertools import permutations, chain, product

def bfs(start, is_goal, neighbors, ret_visited=False):
    nodes = [(start, None)]
    visited = set([start])
    while nodes:
        next_nodes = []
        for node, prev in nodes:
            if is_goal(node):
                path = [node]
                while prev:
                    node, prev = prev
                    path.append(node)
                return list(reversed(path))
            for n in (x for x in neighbors(node) if x not in visited):
                visited.add(n)
                next_nodes.append((n, (node, prev)))
        nodes = next_nodes
    return visited if ret_visited else None

def four_pass(stations):
    stations = [divmod(p, 10) for p in stations]
    def connect(grid, a, b, flag):
        dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)] if flag else [(-1, 0), (1, 0), (0, -1), (0, 1)]
        def neighbors(pos):
            i, j = pos
            for di, dj in dirs:
                i1, j1 = i + di, j + dj
                if (i1, j1) == stations[b] or (0 <= i1 < 10 and 0 <= j1 < 10 and not grid[i1][j1]):
                    yield i1, j1
        path = bfs(stations[a], lambda p: p == stations[b], neighbors)
        if not path:
            return None
        for (i, j) in path:
            grid[i][j] = 1
        return path

    min_path = None
    for flags in product([False, True], repeat=3):
        for p in permutations([(0, 1), (1, 2), (2, 3)]):
            grid = [[0] * 10 for _ in range(10)]
            for (i, j) in stations:
                grid[i][j] = 1
            result = [None] * 3
            for a, b in p:
                path = connect(grid, a, b, flags[a])
                if not path:
                    break
                result[a] = path[1:]
            else:
                result = list(chain(*result))
                if not min_path or len(result) < len(min_path):
                    min_path = result

    return [10 * i + j for i, j in [stations[0]] + min_path] if min_path else None
  
#######################
from math import inf
from heapq import heappop, heappush
import copy
import itertools 


def all_thre_path_perm(li: list) -> list:

    '''creates permutations for all 3 path sections to be calculated
        with diferent priority order'''

    li = [(li[0], li[1]),(li[1], li[2]),(li[2], li[3])]
    return list(itertools.permutations(li))



def gen_grid(n=10) -> list:

    '''creates 10 x 10 graph as 10 lists inside list and inside each
        list 10 numbers starting from 0 ... 99, if needed 1 ... 100
        j range shuld be writen like this: range(1, n + 1)'''

    return [[j + (i * n) for j in range(n)] for i in range(n)]


def legal_mov(size: int, empty: tuple) -> list:
    '''finds legal moves'''
    x, y = empty
    li = []
    if x - 1 >= 0:
        li.append((x - 1, y))
    if y - 1 >= 0:
        li.append((x, y - 1))
    if x + 1 < size:
        li.append((x + 1, y))
    if y + 1 < size:
        li.append((x, y + 1))
    return li

def c_graph(n: int) -> dict:
    '''creates dictionary graph with all vertices and all vertices 
        conected to them, ex: {0 : {1, 10}, ...}'''
    li = gen_grid()
    graph_d = {}
    for idx in range(n):
        for jdx in range(n):
            children = set()
            for positions in legal_mov(n, (idx, jdx)):
                children.add(li[positions[0]][positions[1]])
            graph_d[li[idx][jdx]] = children
    return graph_d


def a_star(graph: dict, start: int, target: int, used: list) -> list:

    '''A* is a graph traversal and path search algorithm,
        returns list of integers reperesentig squares used
        for shortest path, ex: [12, 22, 32, 42, 43]'''

    paths_and_distances = {}
    for vertex in graph:
        paths_and_distances[vertex] = [inf, [start]]

    paths_and_distances[start][0] = 0
    vertices_to_explore = [(0, start)]
    while vertices_to_explore and paths_and_distances[target][0] == inf:
        current_distance, current_vertex = heappop(vertices_to_explore)
        for neighbor in graph[current_vertex]:
            if neighbor not in used:
                new_distance = current_distance + 1
                new_path = paths_and_distances[current_vertex][1] + [neighbor]

                if new_distance < paths_and_distances[neighbor][0]:
                    paths_and_distances[neighbor][0] = new_distance
                    paths_and_distances[neighbor][1] = new_path
                    heappush(vertices_to_explore, (new_distance, neighbor))


    candidate = paths_and_distances[target][1]
    if start in candidate and target in candidate:
        return candidate
    else:
        return ["No path"] + [target, start]


def unique(sequence: list) -> list:

    '''returns list with only unique values in original order'''

    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]

def assembly(stations: list, big_list: list) -> list:

    '''when all 3 paths ar found this function puts them together in 
        corect order and as one joined list, then returns list full of only valid paths'''

    retun_list = []
    for li in big_list:
        transfer_list = [[], [], []]
        no_path = False
        for min_li in li:
            if min_li[0] == "No path":
                no_path = True
            elif min_li[0] == stations[0]:
                transfer_list[0] += min_li
            elif min_li[0] == stations[1]:
                transfer_list[1] += min_li
            elif min_li[0] == stations[2]:
                transfer_list[2] += min_li
        if no_path: continue
        transfer_list = unique([item for sublist in transfer_list for item in sublist])
        retun_list.append(transfer_list)
        
    return retun_list

def child_comb(comb: tuple, graph: dict, u: list) -> list:
    arr = []
    for el in graph[comb[0]]:
        for el2 in graph[comb[1]]:
            lii = a_star(graph, el, el2, u)
            if not u[0] in lii and not u[1] in lii:
                lii.append(comb[1])
                lii.insert(0, comb[0])
                arr.append(lii)

    return arr

def not_to_cros_ststions(stations: list, start_end: tuple, u: list) -> list: 

    if start_end[0] == stations[0] and start_end[1] == stations[1]:
        u = stations[2:] + u
    if start_end[0] == stations[2] and start_end[1] == stations[3]:
        u = stations[:2] + u
    if start_end[0] == stations[1] and start_end[1] == stations[2]:
        u = [stations[0]] + [stations[3]] + u
    return u
    
def four_pass(stations: list) -> list:

    '''tis is main function which calls A* on all 6 path order permutations together 
        with constrains list u'''

    graph = c_graph(10)
    perm_list = all_thre_path_perm(stations)
    path_list = []
    
    for min_li in perm_list:
        u = []
        u = not_to_cros_ststions(stations, min_li[0], u)
        level1 = child_comb(min_li[0], graph, u)

        level2 = []
        list_list_in_use = []
        for min_path in level1:
            if not "No path" in min_path:
                list_list_in_use = copy.copy(min_path)
                if min_li[0][1] == stations[1] or min_li[0][1] == stations[2]:
                    min_path.remove(min_li[0][1])
                if min_path[0] == stations[2] or min_path[0] == stations[1]:
                    min_path.remove(min_path[0])
                a = min_path
                a = not_to_cros_ststions(stations, (min_li[1][0], min_li[1][1]), a)
                arr2 = a_star(graph, min_li[1][0], min_li[1][1], a)
                if not "No path" in arr2:
                    level2.append([list_list_in_use, arr2])


        leve3 = []
        for two_path in level2:
            c = two_path[0][1:-1] + two_path[1][1:-1]
            c = not_to_cros_ststions(stations, (min_li[2][0], min_li[2][1]), c)

            arr3 = a_star(graph, min_li[2][0], min_li[2][1], c)
            if not "No path" in arr3:
                leve3.append(two_path + [arr3])
        path_list += leve3

    path_list = assembly(stations, path_list)
    path_list = sorted(path_list, key=len)
    
    if path_list:
        return path_list[0]
    else:
        None
        
######################################
from itertools import permutations, chain, product
def four_pass(stations):
    s, mp = [divmod(p, 10) for p in stations], None
    for flags in product([False, True], repeat=3):
        for p in permutations([(0, 1), (1, 2), (2, 3)]):
            grid = [10*[0] for k in range(10)]
            for (i, j) in s: grid[i][j] = 1
            l = 3*[None]
            for a, b in p:
                nodes, visited, path = [(s[a], None)], set([s[a]]), None
                while nodes:
                    nn = []
                    for node, prev in nodes:
                        if node == s[b]:
                            p = [node]
                            while prev:
                                node, prev = prev
                                p.append(node)
                            path = list(reversed(p))
                        for n in (x for x in reversed([(node[0] + i, node[1] + j)
                                              for i, j in
                                              ([(0,-1),(0,1),(-1,0),(1,0)] if flags[a] else [(-1,0),(1,0),(0,-1),(0,1)])
                                              if (node[0] + i, node[1] + j) == s[b] or
                                                 (0 <= node[0] + i < 10 and 0 <= node[1] + j < 10 and
                                                  not grid[node[0] + i][node[1] + j])]) if x not in visited):
                            visited.add(n)
                            nn.append((n, (node, prev)))
                    nodes = nn
                if path:
                    for (i, j) in path: grid[i][j] = 1
                    l[a] = path[1:]
                else:
                    path = None
                    break
            if path:
                l = list(chain(*l))
                if not mp or len(l) < len(mp): mp = l
    return [10*i+j for i, j in [s[0]] + mp] if mp else None
Best Practices0Clever0
0ForkLink
YLDK
from heapq import heapify, heappop, heappush
from itertools import permutations
a, r = lambda *x: set([*x]), lambda x,y: (x[0], y[x[0]], y[x[1]])
def four_pass(stations):
    s, l = [(k//10, k%10) for k in stations], []
    for v in permutations([(0,1), (1,2), (2,3)]):
        b, c = set(), {}
        for i, f, t in map(lambda p: r(p,s), v):
            q, w = [(0, f, [f])], set()
            heapify(q)
            while q:
                d, ps, p = heappop(q)
                if ps != t:
                    for z in map(lambda o: (ps[0] + o[0], ps[1] + o[1]), [(-1,0),(0,-1),(1,0),(0,1)]):
                        if 0<=z[0]<=9 and 0<=z[1]<=9 and z not in w and z not in b and z not in (set(s)-a(t)):
                            heappush(q, (d + 1, z, p + [z]))
                            w.add(z)
                else: b, c[i] = b | set(p) - a(f, t), p[1:-1] if i == 1 else p
        if len(c) == 3: l.append([y*10 + x for y, x in [*c[0], *c[1], *c[2]]])
    return min(l, key=lambda x: len(x)) if len(l) else None
  
##############################
from heapq import heapify, heappop, heappush
from itertools import permutations
a, r = lambda *x: set([*x]), lambda x,y: (x[0], y[x[0]], y[x[1]])
def four_pass(stations):
    print('stations =',stations)
    s, l = [(k//10, k%10) for k in stations], []
    for v in permutations([(0,1), (1,2), (2,3)]):
        b, c = set(), {}
        for i, f, t in map(lambda p: r(p,s), v):
            q, w = [(0, f, [f])], set()
            heapify(q)
            while q:
                d, ps, p = heappop(q)
                if ps != t:
                    for z in map(lambda o: (ps[0] + o[0], ps[1] + o[1]), [(-1,0),(0,-1),(1,0),(0,1)]):
                        if 0<=z[0]<=9 and 0<=z[1]<=9 and z not in w and z not in b and z not in (set(s)-a(t)):
                            heappush(q, (d + 1, z, p + [z]))
                            w.add(z)
                else: b, c[i] = b | set(p) - a(f, t), p[1:-1] if i == 1 else p
        if len(c) == 3: l.append([y*10 + x for y, x in [*c[0], *c[1], *c[2]]])
    return min(l, key=lambda x: len(x)) if len(l) else None
  
############################
from itertools import permutations, chain, product
def four_pass(stations):
    s, mp = [divmod(p, 10) for p in stations], None
    for flags in product([False, True], repeat=3):
        for p in permutations([(0, 1), (1, 2), (2, 3)]):
            grid = [10*[0] for k in range(10)]
            for (i, j) in s: grid[i][j] = 1
            l = 3*[None]
            for a, b in p:
                nodes, visited, path = [(s[a], None)], set([s[a]]), None
                while nodes:
                    nn = []
                    for node, prev in nodes:
                        if node == s[b]:
                            p = [node]
                            while prev:
                                node, prev = prev
                                p.append(node)
                            path = list(reversed(p))
                        for n in (x for x in reversed([(node[0] + i, node[1] + j)
                                              for i, j in
                                              ([(0,-1),(0,1),(-1,0),(1,0)] if flags[a] else [(-1,0),(1,0),(0,-1),(0,1)])
                                              if (node[0] + i, node[1] + j) == s[b] or
                                                 (0 <= node[0] + i < 10 and 0 <= node[1] + j < 10 and
                                                  not grid[node[0] + i][node[1] + j])]) if x not in visited):
                            visited.add(n)
                            nn.append((n, (node, prev)))
                    nodes = nn
                if path:
                    for (i, j) in path: grid[i][j] = 1
                    l[a] = path[1:]
                else:
                    path = None
                    break
            if path:
                l = list(chain(*l))
                if not mp or len(l) < len(mp): mp = l
    return [10*i+j for i, j in [s[0]] + mp] if mp else None
Best Practices0Clever0
0ForkLink
YLDK
from heapq import heapify, heappop, heappush
from itertools import permutations
a, r = lambda *x: set([*x]), lambda x,y: (x[0], y[x[0]], y[x[1]])
def four_pass(stations):
    s, l = [(k//10, k%10) for k in stations], []
    for v in permutations([(0,1), (1,2), (2,3)]):
        b, c = set(), {}
        for i, f, t in map(lambda p: r(p,s), v):
            q, w = [(0, f, [f])], set()
            heapify(q)
            while q:
                d, ps, p = heappop(q)
                if ps != t:
                    for z in map(lambda o: (ps[0] + o[0], ps[1] + o[1]), [(-1,0),(0,-1),(1,0),(0,1)]):
                        if 0<=z[0]<=9 and 0<=z[1]<=9 and z not in w and z not in b and z not in (set(s)-a(t)):
                            heappush(q, (d + 1, z, p + [z]))
                            w.add(z)
                else: b, c[i] = b | set(p) - a(f, t), p[1:-1] if i == 1 else p
        if len(c) == 3: l.append([y*10 + x for y, x in [*c[0], *c[1], *c[2]]])
    return min(l, key=lambda x: len(x)) if len(l) else None
  
############################
from heapq import heapify, heappop, heappush
from itertools import permutations
a, r = lambda *x: set([*x]), lambda x,y: (x[0], y[x[0]], y[x[1]])
def four_pass(stations):
    print('stations =',stations)
    s, l = [(k//10, k%10) for k in stations], []
    for v in permutations([(0,1), (1,2), (2,3)]):
        b, c = set(), {}
        for i, f, t in map(lambda p: r(p,s), v):
            q, w = [(0, f, [f])], set()
            heapify(q)
            while q:
                d, ps, p = heappop(q)
                if ps != t:
                    for z in map(lambda o: (ps[0] + o[0], ps[1] + o[1]), [(-1,0),(0,-1),(1,0),(0,1)]):
                        if 0<=z[0]<=9 and 0<=z[1]<=9 and z not in w and z not in b and z not in (set(s)-a(t)):
                            heappush(q, (d + 1, z, p + [z]))
                            w.add(z)
                else: b, c[i] = b | set(p) - a(f, t), p[1:-1] if i == 1 else p
        if len(c) == 3: l.append([y*10 + x for y, x in [*c[0], *c[1], *c[2]]])
    return min(l, key=lambda x: len(x)) if len(l) else None
  
##############################
def four_pass(stations):
    global cell_dict
    
    #determine coordinates of the 4 stations
    stat_lett = ['A', 'B', 'C', 'D']
    stat_coords = {}    
    for idx in range(4):
        stat_coords[stat_lett[idx]] = divmod(stations[idx], 10)
        
    #set up the grid
    grid = []
    for row in range(10):
        grid.append(['.']*10)      
    for lett, coords in stat_coords.items():
        grid[coords[0]][coords[1]] = lett
                
    DIRECTIONS = [[0, -1], [-1, 0], [0, 1], [1, 0]]  
    PERMS = ['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX']
    
    '''functions needed for main procedure'''
    
    def initialize(grid):
        #initialize the dictionary of available cells
        cell_dict = {} #a dictionary of available cells in maze;
                        #the value is the path length from the starting cell
                        #to that cell
                        
        for row in range(10):
            for col in range(10):
                cell_dict[(row, col)] = [] #indicating no path yet     
        return cell_dict

    def path_finder(P, Q): #P and Q are two stations
        '''breadth first search. maintain dynamic list of possible cells to visit, 
        all of which are the same distance from start. For each cell in list of
        same distance cells, derive next possible cells in one step and add them, 
        deleting the previous cell from the possibles

        Collect up to 6 possible paths (an arbitrary choice)
        '''
        cell_dict = initialize(grid) #clears previous paths
        opts = [P] #dynamic list of cells equidistant from start station
        cell_dict[P] = [P]
        poss_paths = []
    
        while opts: #loop until opts is empty, meaning no more paths
                    #are possible
            prev = opts.pop(0) #the first cell of current path, removed from list
            add_path = cell_dict[prev] #path cells to be added
            #add all options from current position (prev)
            for direc in DIRECTIONS:
                r, c = (prev[0] + direc[0], prev[1] + direc[1])
                if 0 <= r <= 9 and 0 <= c <= 9:
                    try_cell = (r, c)
                    
                    #check if resulting cell is possible
                    if (grid[r][c] == '.' or try_cell == Q) and try_cell not in opts:
                        #add the trial cell to opts                     
                        opts.append(try_cell)
                        #add previous cell's path history to new cell
                        cell_dict[try_cell] += add_path + [try_cell]
                        #block the cell to future paths
                        if (r, c) not in stat_coords.values():
                            grid[r][c] = 'X'
    
                    #check if path is complete:
                    if try_cell == Q:
                        if cell_dict[Q] not in poss_paths:
                            poss_paths.append(cell_dict[Q])
                        opts.remove(try_cell)
                        cell_dict[Q] = []  #remove any previous path
                        if len(poss_paths) == 6:
                            return poss_paths
        
        
        return poss_paths #which may be empty; the first path in the list
                        #has shortest length; other may be longer

    
    def path_segment(idx):
        #receives an index as to which of three segments to calculate
        path = path_finder(stat_coords[stat_lett[0 + idx]], \
                             stat_coords[stat_lett[1 + idx]])  
        if idx == 0:
            #re-set the grid and return
            return ['AB', restore_unused(path[0])]        
        elif idx == 1:     
            return ['BC', restore_unused(path[0])]  
        else:
            return ['CD', restore_unused(path[0])]
        
    def restore_unused(seg):
        '''after a path segment has been found, restore unused cells to '.'
        and mark the segment cells with 'P' '''
        for row in range(10):
            for col in range(10):
                if (row, col) not in stat_coords.values() and grid[row][col] != 'P':
                    if (row, col) in seg:
                        grid[row][col] = 'P'
                    else:
                        grid[row][col] = '.'
        return seg
    
    def reset():
        #restore grid to blank setup after a permutation didn't work
        for row in range(10):
            for col in range(10):
                grid[row][col] = '.'
        for stat in stat_coords.values():
            grid[stat[0]][stat[1]] = 'S' #marker to block paths  
        return
    
    def penult(P, Q): #P and Q are the coordinates of the two stations
        '''creates up to four entry/exit paths using penultimate cells'''
    
        #get coords of the other 2 stations
        others = [x for x in stat_coords.values() if x != P and x != Q]
        
        rp, cp = P[0], P[1] #aliases for rows and cols of the two endpoints
        rq, cq = Q[0], Q[1]
        
        starts, ends  = [], []
        
        #check for same cols or rows
        if rp == rq or cp == cq:
            routes = path_finder(P, Q)
            return routes
            
        #routine for no same column or row
        if rq > rp:
            if cq > cp:
                starts += [(rp, cp + 1), (rp + 1, cp)]
                ends += [(rq, cq - 1), (rq - 1, cq)]
            else:
                starts += [(rp, cp - 1), (rp + 1, cp)]
                ends += [(rq, cq + 1), (rq - 1, cq)]
        else: 
            if cq > cp:
                starts += [(rp, cp + 1), (rp - 1, cp)]
                ends += [(rq, cq - 1), (rq + 1, cq)]
            else:
                starts += [(rp, cp - 1), (rp - 1, cp)]
                ends += [(rq, cq + 1), (rq + 1, cq)]
                
        #remove other station cells from starts and ends
        starts = [x for x in starts if x not in others]
        ends = [y for y in ends if y not in others]
                
        pq_paths = []
        if set(starts) != set(ends): 
            for pcell in starts:
                for qcell in ends:
                    if pcell != qcell:
                        routes = path_finder(pcell, qcell)
                        if routes:
                            pq_paths.append([P] + routes[0] + [Q])
                        #clear the grid to find next path
                        reset()
        else: #starts and ends are the same cells
            for cell in starts:
                pq_paths.append([P] + [cell] + [Q])
            
            
                
        #add up to 6 more routes  
        return more_paths(P, Q, pq_paths)    
    
    ''''find two perimeter paths from P to Q, plus up to 6 possible others'''
    def peri_path(P, Q): #P and Q are coordinates of two adjacent stations
        #repeated functions used below
    
        def columns():
            m = 1
            if P[1] < Q[1]: #col increases by 1
                while m < Q[1] - P[1] + 1:
                    PQ_dogleg.append((corner[0], corner[1] + m))
                    m += 1
            else: #col decreases by one or remains the same
                while m < P[1] - Q[1] + 1:
                    PQ_dogleg.append((corner[0], corner[1] - m))
                    m += 1
            return
        
        def rows():
            k = 1
            if P[0] < Q[0]: #row increases by 1
                while k < Q[0] - P[0] + 1:
                    PQ_dogleg.append((corner[0] + k, corner[1]))
                    k += 1
            else: #row decreases by one or remains the same
                while k < P[0] - Q[0] + 1:
                    PQ_dogleg.append((corner[0] - k, corner[1]))
                    k += 1
            return
        
                
        '''main peri_path function'''
        PQ_segs = [] #will hold the two perimeter paths from P to Q
        #get coords of the other 2 stations
        others = [x for x in stat_coords.values() if x != P and x != Q]
    
        #find first PQ perimeter path; rows first
        PQ_dogleg = []
        i = 0 #increment index
        if P[0] < Q[0]: #row increases by 1
            while i < Q[0] - P[0] + 1:
                PQ_dogleg.append((P[0] + i, P[1]))
                i += 1
            corner = PQ_dogleg[-1]
            columns()
        
        else: #row decreases by 1 or remains the same
            while i < P[0] - Q[0] + 1:
                PQ_dogleg.append((P[0] - i, P[1]))
                i += 1
            corner = PQ_dogleg[-1]
            columns()
    
        if PQ_dogleg:
            for stat in others:
                if stat in PQ_dogleg:
                    break
            else: #runs if there was no break
                PQ_segs.append(PQ_dogleg)
                reset()
                
            #find second PQ perimeter path; cols first
        PQ_dogleg = []
        j = 0  # increment index
        if P[1] < Q[1]:  # col increases by 1
            while j < Q[1] - P[1] + 1:
                PQ_dogleg.append((P[0], P[1] + j))
                j += 1
            corner = PQ_dogleg[-1]
            rows()
        
        else: #col decreases by 1 or remains the same
            while j < P[1] - Q[1] + 1:
                PQ_dogleg.append((P[0], P[1] - j))
                j += 1
            corner = PQ_dogleg[-1]
            rows()
    
        if PQ_dogleg:    
            for stat in others:
                if stat in PQ_dogleg:
                    break
            else: #runs if there was no break
                if PQ_dogleg not in PQ_segs:
                    PQ_segs.append(PQ_dogleg)
                    reset()
        
        return more_paths(P, Q, PQ_segs) #knowing it might be empty
    
    def more_paths(P, Q, segs):
        other_routes = path_finder(P, Q) #adds up to 6 more possible paths
        if other_routes:
            for route in other_routes:
                if route not in segs:
                    segs.append(route)        
        reset()
        return segs

    '''---start of main procedure---
    first algorithm--path segment permutations:  X=first segment to be found;
    if X in position 0, it's AB; X in position 1 it's BC; X in pos 2 it's CD'''
    
    all_paths = []
    for perm in PERMS:
        
        '''use peri_path and penult for first two sets of segments;
        loop through first and second sets + path_finder for third leg'''
        
        reset() #clear the grid
        sgmnts_dict = {} #will hold possible paths for the first two legs
        x_idx = perm.index('X')
        R, S = stat_coords[stat_lett[0 + x_idx]], \
                stat_coords[stat_lett[1 + x_idx]]
                            
        sgmnts_dict['X'] = peri_path(R, S)
    
        add_sgmnts = penult(R, S)
        for new in add_sgmnts:
            if new not in sgmnts_dict['X']:
                sgmnts_dict['X'].append(new)
        
        y_idx = perm.index('Y')
        R, S = stat_coords[stat_lett[0 + y_idx]], \
                stat_coords[stat_lett[1 + y_idx]]
        
        sgmnts_dict['Y'] = peri_path(R, S)
        
        add_sgmnts = penult(R, S)
        for new in add_sgmnts:
            if new not in sgmnts_dict['Y']:
                sgmnts_dict['Y'].append(new)        
        
        
        #third leg
        for path1 in sgmnts_dict['X']:
            for path2 in sgmnts_dict['Y']:
                
                if list(set(path1[1:-1]).intersection(set(path2[1:-1]))):
                    continue 
                    #go to next path2; paths 1 and 2 intersect
                
                reset()
                #mark path1 and path2 on grid
                for idx in range(1, len(path1) - 1):
                    grid[path1[idx][0]][path1[idx][1]] = 'P'
                for idx in range(1, len(path2) - 1):
                    grid[path2[idx][0]][path2[idx][1]] = 'P' 
                    
                z_idx = perm.index('Z')    
                path3 = path_finder(stat_coords[stat_lett[0 + z_idx]], 
                                stat_coords[stat_lett[1 + z_idx]])
                
                if path3:
                    #order the paths from A to D
                    for item in [path1, path2, path3[0]]:
                        if item[0] == stat_coords['A']:
                            path_AB = item
                        elif item[-1] == stat_coords['D']:
                            path_CD = item
                        else:
                            path_BC = item
                    
                    #join the segments, make strings, eliminate duplicates
                    soln = [str(x[0]) + str(x[1]) 
                            for x in path_AB + path_BC + path_CD]
                    soln = [elem for i, elem in enumerate(soln) 
                                 if i == 0 or soln[i-1] != elem] #eliminates the
                                    #two duplicates where the paths join at B & C
                                    
                    #drop the initial zeroes
                    for idx, elem in enumerate(soln):
                        if elem[0] == '0':
                            soln[idx] = elem[1]
                            
                    #change to integers
                    soln = [int(elem) for elem in soln]
                    if soln not in all_paths:
                        all_paths.append(soln)        
                
    #return the minimum path or None
    if all_paths:
        min_length = min([len(path) for path in all_paths])
        for path in all_paths:
            if len(path) == min_length:                
                return path
    else:
        return None


# if you prefer to see an overhead view of the factory floor with any failed test results, uncomment the line below:
#show_graph_debug = True
#####################################################
from itertools import permutations, combinations
import numpy as np
import heapq


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2) ** 0.5


def reconstruct_path(came_from, current):
    result = [current]
    while current in came_from:
        current = came_from[current]
        result.append(current)
    return (result[::-1])


def algorithm(blank_grid, start, end, waypoints, centre):
    count = 0
    open_set = []
    heapq.heapify(open_set)
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {(j, i): float("inf") for i in range(10) for j in range(10)}
    g_score[start] = 0
    f_score = {(j, i): float("inf") for i in range(10) for j in range(10)}
    f_score[start] = h(start, end)
    open_set_hash = {start}
    while open_set_hash:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)
        if current == end:
            return reconstruct_path(came_from, end) 

        for neighbour in blank_grid[current[0]][current[1]]:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:

                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour, end) 
                if neighbour not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)

    return None

def block_points(point):
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    j, i = point
    result = []
    for p in combinations(directions, 3):
        l = [(j + p[0][0], i + p[0][1]), (j + p[1][0], i + p[1][1]), (j + p[2][0], i + p[2][1])]
        result.append(l)
    return result


def create_grid():
    def get_neighbours(j, i):
        neighbours = []
        dirs = [(-1, 0), (0, 1), (0, -1), (1, 0)]
        for dir in dirs:
            new_row = j + dir[0]
            new_col = i + dir[1]
            if 0 <= new_row < 10 and 0 <= new_col < 10:
                neighbours.append((new_row, new_col))
        return neighbours
    return [[get_neighbours(j, i) for i in range(10)] for j in range(10)]




def get_path(blank_grid, start, end, barrier_list, waypoints, centre):
    for point in barrier_list:
        for dir in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
            try:
                blank_grid[point[0]][point[1]].remove((dir[0] + point[0], dir[1] + point[1]))
            except:
                pass

    p = algorithm(blank_grid, start, end, waypoints, centre)
    return p


def four_pass(stations):
    print(stations)
    a, b, c, d = [(s // 10, s % 10) for s in stations]
    blank_grid = create_grid()
    centre = (sum([w[0] for w in [a, b, c, d]]) / 4, sum([w[1] for w in [a, b, c, d]]) / 4)
    current_best_path = []
    length_best_path = 999
    #a -> b -> c
    for b1 in block_points(a):  
        p1_c = get_path(create_grid(), a, b, [c, d] + b1, [a, b, c, d], centre)
        if p1_c is None: print("p1 is none"); continue
        for b2 in block_points(b):  
            p2_c = get_path(create_grid(), b, c, p1_c[:-1] + [d] + b2, [a, b, c, d], centre)
            if p2_c is None: continue
            for b3 in [[(-1, -1)]]:
                p3_c = get_path(create_grid(), c, d, p1_c + p2_c[:-1] + b3, [a, b, c, d], centre)
                if p3_c is None: continue
                path = p1_c[:-1] + p2_c[:-1] + p3_c
                if len(path) < length_best_path:
                    length_best_path = len(path)
                    current_best_path = path

    #c -> b  -> a
    for b1 in block_points(c):  
        p1_c = get_path(create_grid(), c, d, [a, b, ] + b1, [a, b, c, d], centre)
        if p1_c is None: continue
        for b2 in block_points(b):  
            p2_c = get_path(create_grid(), b, c, p1_c[1:] + [a] + b2, [a, b, c, d], centre)
            if p2_c is None: continue
            for b3 in [[(-1, -1)]]: 
                p3_c = get_path(create_grid(), a, b, p1_c + p2_c + b3, [a, b, c, d], centre)
                if p3_c is None: continue
                path = p3_c[:-1] + p2_c[:-1] + p1_c
                if len(path) < length_best_path:
                    length_best_path = len(path)
                    current_best_path = path
                    print(current_best_path)

        # b -> a  -> c
        for b1 in block_points(c): 
            p1_c = get_path(create_grid(), b, c, [a, d, ] + b1, [a, b, c, d], centre)
            if p1_c is None: continue
            for b2 in block_points(b):  
                p2_c = get_path(create_grid(), a, b, p1_c[1:] + [d] + b2, [a, b, c, d], centre)
                if p2_c is None: continue
                for b3 in [[(-1, -1)]]:  
                    p3_c = get_path(create_grid(), c, d, p1_c[:-1] + p2_c + b3, [a, b, c, d], centre)
                    if p3_c is None: continue
                    path = p2_c[:-1] + p1_c[:-1] + p3_c
                    if len(path) < length_best_path:
                        length_best_path = len(path)
                        current_best_path = path
                        print(current_best_path)



    if current_best_path in (None, []):
        return None
    else:
        return [10 * node[0] + node[1] for node in current_best_path]
      
#################################
from itertools import permutations,starmap
from heapq import *
from collections import defaultdict
 
INF   = float("inf")
       
CYCLES_PRECEDENCE = {
        ( 1, 0): "WNES,ENWS",( 1, 1): "SWNE,ENWS",( 0, 1): "SWNE,NWSE",(-1, 1): "ESWN,NWSE",(-1, 0): "ESWN,WSEN",(-1,-1): "NESW,WSEN", ( 0,-1): "NESW,SENW"
        , ( 1,-1): "WNES,SENW"}

MOVES = [(0,1), (-1,0), (0,-1), (1,0)]        # take moves in anticlockwise direction
SCALE_PARAMETER = 0.00099999

def vertical_distance(pos, p2):
    # prefer vertical routes
     
    crow, _ = pos
    erow, _ = p2
    return SCALE_PARAMETER*abs(erow - crow) 

def horizontal_distance(pos, p2):
    # prefer horizonatal routes
     
    _, ccol = pos
    _, ecol = p2
    return SCALE_PARAMETER*abs(ecol - ccol)  


 
def four_pass(stations):
    def dfs(permOrder, paths, n=0):
        if n==3:
            yield paths[:]
        else:
            _, p1, p2 = permOrder[n]
            for func2breakties in [vertical_distance, horizontal_distance]:
                path = aStar(p1, p2, grid, func2breakties)
                if path is None:
                    continue
                paths.append(path)
                updateGrid(grid, path)
                yield from dfs(permOrder, paths, n+1)
                updateGrid(grid, path, free=1)
                paths.pop()
    
    pts      = [divmod(s,10) for s in stations]
    segments = [(i, pts[i], pts[i+1]) for i in range(3)]
    MIN      = 1 + sum(manhattan(p1,p2) for _,p1,p2 in segments)
    
    shortestPath = None
    for permOrder in permutations(segments):
        grid = [[1]*10 for _ in range(10)]
        updateGrid(grid, pts)
        
        for p in dfs(permOrder, []):
            length = 4 + sum(map(len,p))
            
            if not shortestPath or length < len(shortestPath):
                shortestPath = rebuildPath(permOrder, p)
                
            if len(shortestPath) == MIN:
                return shortestPath
    
    return shortestPath
    
    

def manhattan(*args): return sum(abs(b-a) for a,b in zip(*args)) # compute mantahattan metric
def linearize(p):     return 10*p[0]+p[1] # reencode

def updateGrid(grid, inPath, free=0):
    for x,y in inPath: grid[x][y] = free
    
def rebuildPath(permOrder, shortest): # reconstruct our optimal path
    full_path = []
    for (i,p1,p2),path in sorted(zip(permOrder, shortest)):
        full_path.append(linearize(p1))
        full_path.extend(map(linearize,path))
    full_path.append(linearize(p2))
    return full_path

def aStar(p1, p2, grid,func2breakTies):
    prev  = [[None]*10 for _ in range(10)]
     
    working = [[INF if free else 0 for free in r] for r in grid]
    working[p2[0]][p2[1]] = INF
    
    q = [(manhattan(p1, p2) + func2breakTies(p1, p2), 0, p1)]
    while q:
        _, cost, source = q.pop(q.index(min(q)))
        if source == p2:
            break
        x, y = source
        for a, b in ((x+delta_x, y+delta_y)
                     for i, (delta_x, delta_y) in enumerate(MOVES)
                     if 0 <= x + delta_x < 10 and 0 <= y + delta_y < 10):
            pos, nCost = (a, b), cost + 1
            if nCost < working[a][b]:
                prev[a][b], working[a][b] = source, nCost
                q.append((nCost + manhattan(pos, p2) + func2breakTies(pos, p2),
                             nCost, pos))
    if q:
        p, (x,y) = [], p2
        while True:
            x,y = pos = prev[x][y]
            if pos == p1: break
            p.append(pos)
        return p[::-1]
      
############################
from collections import defaultdict
from itertools import permutations

def find_way_for_sequence(field, stations, sequence, var):
    field = field.copy()
    
    parts = [None] * 3
    
    for i in range(3):
        s = sequence[i]
        
        parts[s] = find_shortes_path(field, (stations[s] % 10, stations[s] // 10), (stations[s+1] % 10, stations[s+1] // 10), var[i])
        if parts[s] == None:
            return None
        
        for point in parts[s][1:-1]:
            field[point] = 0

    full = parts[0][:-1] + parts[1][:-1] + parts[2]
    
    return [point[0] + point[1] * 10 for point in full]

def find_shortes_path(field, p1, p2, var):
    field = field.copy()
    paths = defaultdict(list)
    active = [p1]
    paths[p1] = [p1]
    
    while len(active):
        next_active = []
        for p in active:
            options = [(p[0] - 1, p[1]), (p[0] + 1, p[1]), (p[0], p[1] - 1), (p[0], p[1] + 1)]
            options = options[1:] + options[:1]
            if var:
                options = options[::-1]

            options = [o for o in options if field[o] == -1 or o == p2]

            for o in options:
                if not field[o]:
                    continue
                paths[o] = paths[p] + [o]
                if o == p2:
                    return paths[o]
                field[o] = 0
                next_active.append(o)
        active = next_active
    return None

def four_pass(stations):
    field = defaultdict(int)
    for coord in range(100):
        field[(coord % 10, coord // 10)] = -1
    for i in range(4):
        field[(stations[i] % 10, stations[i] // 10)] = i + 1

    all_sequences = list(permutations([0, 1, 2]))
    all_vars = [[(val//(2**bit))%2 for bit in range(3)] for val in range(8)]
    all_ways = []
    
    for var in all_vars:
        ways = [find_way_for_sequence(field, stations, list(seq), var) for seq in all_sequences]
        ways = [way for way in ways if way != None]

        ways.sort(key = lambda x: len(x))
        if not len(ways):

            return None
        all_ways.append(ways[0])
    
    all_ways.sort(key = lambda x: len(x))
    
    return all_ways[0]
  
############################
"""

Blind4Basic's solution for Four Pass Transport kata:
https://www.codewars.com/kata/four-pass-transport

Added performance optimisation by using tie-breaker functions.

original solution: 1.410877719697666s
optimised solution: 1.002065627055475s

"""

from itertools import permutations,starmap
from heapq import *
from collections import defaultdict
from time import time

DT = defaultdict(int)
        
def timer(f):
    def w(*a):
        s = time()
        ans = f(*a)
        DT[f.__name__] += time()-s
        return ans
    return w
    
    

INF   = float("inf")
MOVES2 = {'E': (0,1), 'W': (-1,0), 'N': (0,-1), 'S': (1,0) }
         
CYCLES_PRECEDENCE = {
        ( 1, 0): "WNES,ENWS",
        ( 1, 1): "SWNE,ENWS",
        ( 0, 1): "SWNE,NWSE",
        (-1, 1): "ESWN,NWSE",
        (-1, 0): "ESWN,WSEN",
        (-1,-1): "NESW,WSEN",
        ( 0,-1): "NESW,SENW",
        ( 1,-1): "WNES,SENW"
}

@timer
def ref_fn(stations):
    print(stations)
    
    def dfs(iP, paths, n=0):
        if n==3: yield paths
        else:
            p1,p2 = pts[iP[n]:iP[n]+2]
            for moves in segMovesConfig[iP[n]]:
                path = aStar2(p1,p2,board,moves)
                if path is None: continue
                
                paths.append(path)
                for x,y in path: board[x][y] = 0
                yield from dfs(iP, paths, n+1)
                for x,y in path: board[x][y] = 1
                paths.pop()
                
    
    pts            = [divmod(s,10) for s in stations]
    MIN            = 1 + sum(manhattan(pts[i],pts[i+1]) for i in range(3))
    segMovesConfig = [ genOptimalAStarMoves(pts[i],pts[i+1]) for i in range(3)]
    shortestPath   = None
    
    for iP in permutations(range(3)):
        board = [[1]*10 for _ in range(10)]
        for x,y in pts: board[x][y] = 0
        
        for p in dfs(iP, []):
            length = 4 + sum(map(len,p))
            
            if not shortestPath or length < len(shortestPath):
                shortestPath = []
                for i,subp in sorted(zip(iP, p)):
                    shortestPath.append(linearize(pts[i]))
                    shortestPath.extend(map(linearize,subp))
                shortestPath.append(linearize(pts[i+1]))
                
            if len(shortestPath) == MIN:
                return shortestPath
    
    return shortestPath
    
    
def genOptimalAStarMoves(p1,p2):
    dx,dy = (b-a for a,b in zip(p1,p2))
    dir   = ( dx and dx//abs(dx), dy and dy//abs(dy) )
    
    return [ [MOVES2[d] for d in s] for s in CYCLES_PRECEDENCE[dir].split(",")]
    

def aStar2(p1,p2,board,moves):
    prev  = [[None]*10 for _ in range(10)]
    local = [[(INF,0) if free else (0,0) for free in r] for r in board]                # (cost+heuristic, rotation index)
    local[p2[0]][p2[1]] = (INF,0)
    
    q = [(manhattan(p1,p2), 0, 0, 0, p1)]                    # queue: (cost+h, rotation index, general index, cost, (x,y))
    iG = 0
    while q and q[0][-1] != p2:
        _,_,_,cost,src = heappop(q)
        cost += 1
        iG   -= 1
        for i,(dx,dy) in enumerate(moves):
            pos = a,b = src[0]+dx, src[1]+dy
            if 0<=a<10 and 0<=b<10:
                nTup  = (cost,i)
                if nTup < local[a][b]:
                    prev[a][b], local[a][b] = src, nTup
                    heappush(q, (cost + manhattan(pos,p2), i, iG, cost, pos))
    
    if q:
        p, (x,y) = [], p2
        while 1:
            x,y = pos = prev[x][y]
            if pos == p1: break
            p.append(pos)
        return p[::-1]




INF   = float("inf")
MOVES = [(0,1), (-1,0), (0,-1), (1,0)]        # Turn anticlockwise
ATTENUATION = 0.001

def vertical_dist(pos, p2):
    """
    tie breaker for preference of vertical paths
    """
    c_row, _ = pos
    e_row, _ = p2
    return abs(e_row - c_row) * ATTENUATION

def horizontal_dist(pos, p2):
    """
    tie breaker for preference of horizontal paths
    """
    _, c_col = pos
    _, e_col = p2
    return abs(e_col - c_col) * ATTENUATION


@timer
def four_pass(stations):
    def dfs(pOrder, paths, n=0):
        if n==3:
            yield paths[:]
        else:
            _, p1, p2 = pOrder[n]
            for tie_breaker_func in [vertical_dist, horizontal_dist]:
                path = aStar(p1, p2, board, tie_breaker_func)
                if path is None:
                    continue
                paths.append(path)
                updateBoard(board, path)
                yield from dfs(pOrder, paths, n+1)
                updateBoard(board, path, free=1)
                paths.pop()
    
    pts      = [divmod(s,10) for s in stations]
    segments = [(i, pts[i], pts[i+1]) for i in range(3)]
    MIN      = 1 + sum(manhattan(p1,p2) for _,p1,p2 in segments)
    
    shortestPath = None
    for pOrder in permutations(segments):
        board = [[1]*10 for _ in range(10)]
        updateBoard(board, pts)
        
        for p in dfs(pOrder, []):
            length = 4 + sum(map(len,p))
            
            if not shortestPath or length < len(shortestPath):
                shortestPath = rebuildPath(pOrder, p)
                
            if len(shortestPath) == MIN:
                return shortestPath
    
    return shortestPath
    
    

def manhattan(*args): return sum(abs(b-a) for a,b in zip(*args))
def linearize(p):     return 10*p[0]+p[1]

def updateBoard(board, inPath, free=0):
    for x,y in inPath: board[x][y] = free
    
def rebuildPath(pOrder, shortest):
    fullPath = []
    for (i,p1,p2),path in sorted(zip(pOrder, shortest)):
        fullPath.append(linearize(p1))
        fullPath.extend(map(linearize,path))
    fullPath.append(linearize(p2))
    return fullPath

def aStar(p1, p2, board, tie_breaker_func):
    prev  = [[None]*10 for _ in range(10)]
    # (heuristic, rotation index)
    local = [[INF if free else 0 for free in r] for r in board]
    local[p2[0]][p2[1]] = INF
    
    # queue: (cost+h, cost, (x,y))
    q = [(manhattan(p1, p2) + tie_breaker_func(p1, p2), 0, p1)]
    while q:
        _, cost, src = q.pop(q.index(min(q)))
        if src == p2:
            break
        x, y = src
        for a, b in ((x+dx, y+dy)
                     for i, (dx, dy) in enumerate(MOVES)
                     if 0 <= x + dx < 10 and 0 <= y + dy < 10):
            pos, nCost = (a, b), cost + 1
            if nCost < local[a][b]:
                prev[a][b], local[a][b] = src, nCost
                q.append((nCost + manhattan(pos, p2) + tie_breaker_func(pos, p2),
                             nCost, pos))
    if q:
        p, (x,y) = [], p2
        while 1:
            x,y = pos = prev[x][y]
            if pos == p1: break
            p.append(pos)
        return p[::-1]

print(four_pass([80, 8, 68, 21]))
