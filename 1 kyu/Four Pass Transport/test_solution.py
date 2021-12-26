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
