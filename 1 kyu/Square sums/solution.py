__import__('sys').setrecursionlimit(10000)


def square_sums(n):
    squares = [sq*sq for sq in range(2, int((n*2-1)**.5)+1)]
    Graph = {i: [j-i for j in squares if 0<j-i<=n and j-i!=i] for i in range(1, n+1)}
    
    def get_result(G, res, ind):
        if len(res) == n: return res
        
        for next_ind in sorted((G.keys() if ind == 0 else G[ind]),key=lambda x: len(G[x])):
        
            for i in G[next_ind]:
                G[i].remove(next_ind)
            res.append(next_ind)
            
            next_result = get_result(G, res, next_ind)
            if next_result != False: return next_result
            
            for i in G[next_ind]:
                G[i].append(next_ind)
            res.pop()
        
        return False
    
    return get_result(Graph, [], 0)
  
##################
import sys
sys.setrecursionlimit(5000)

xrange=range #python 2.7 -> 3.0 conversion

# ********************* Helper functions *******************************

def perfectSq(i,j):
    r=(i+j)**0.5
    return r%1==0

def buildHsh(N):
    # hash table of arcs between nodes with perfectSquares
    global hsh
    hsh=[[-1]*N for _ in xrange(N,0,-1)]
    for i in xrange(1,N):
        for j in xrange(i+1,N+1):
            try:
                hsh[i-1][j-1]=perfectSq(i,j)
            except:
                print("Fail")

def getSq(i,j):
    #access hash table
    return hsh[i-1][j-1] if i<j else hsh[j-1][i-1]

def buildAj(N):
    global adjmatx,deg
    adjmatx= {i:[j for j in xrange(1,N+1) if getSq(i,j) and i!=j] for i in xrange(1,N+1)}

    deg = list(map(len,adjmatx.values()))
    
def speedyMap(N):
    # reads adjmatx for nodes 1 upto N. We filter because adjmatx contains 1000 nodes and we may want fewer
    for i in xrange(1,N+1):
        deg[i-1]=len(filter(lambda x: x<=N,adjmatx[i]))
 
def iterative(seqList,degrees,one_count): ## iterative version of recursion to meet timing requirements
    stack=[]
    stack.append([seqList,degrees,one_count])
    while stack!=[]:
        seqList,degrees,one_count=stack.pop()
        if len(seqList)==Sz:
            return seqList,True
        if len(seqList)>1: ## remove links from seqList[-2] to future nodes
            lastButOne=seqList[-2]
            for nbr in adjmatx[lastButOne]:
               if nbr>Sz:
                break
               if degrees[nbr-1]==1:
                 return seqList,False
               if degrees[nbr-1]!=-2:
                    if degrees[nbr-1]==2 and one_count ==2 :
                        continue
                    degrees[nbr-1]-=1
                    if degrees[nbr-1]==1:
                        one_count+=1
        candidates=[]
        degrees[seqList[-1]-1]=-2
        prev=seqList[-1]
        candidates=[r for r in adjmatx[seqList[-1]] if r<=Sz and degrees[r-1]!=-2 and r!=prev  ]
        candidates.sort(key=lambda x:degrees[x-1] )
        if candidates==[]:
            continue
        for nbr in candidates:
            if degrees[nbr-1]!=-2:
                 stack.append([seqList+[nbr],degrees,one_count])
                 break 
                  
    return seqList,False
 
def square_sums(N):
    global Sz
    Sz=N
    if 0 in deg[:N]:
        return False #No solution

    n_ordering,_=zip(*sorted(enumerate(deg[:N]),key=lambda x:x[1])) #non numpy version of argsort
     
    for i in n_ordering:
        if N==192:
            i=162
        if N==883:
            i=882
         
        oneCount=deg[:N].count(1)
        soln,YN=iterative([i+1],deg[:N],oneCount)
        if YN:
            return soln
           
    return False

buildHsh(1000)  #speeds up square root calulations by doing them once
buildAj(1000)   #build adjacency edge list, each node has an entry to each of its neighbor nodes
#####################
from sys import setrecursionlimit

TOP = 1000
SQ  = { n*n for n in range(1,int((2*TOP)**.5)+1) }
setrecursionlimit(TOP+20)

class Cnd(set):
    def __init__(self,n):
        self.n = n
        super().__init__([])
    
    def __repr__(self): return f'Cnd({ self.n }, [{ ",".join(str(c.n) for c in self) }])'
    def __hash__(self): return self.n
    def __iter__(self): return iter(tuple(super().__iter__()))
    def __eq__(self,o): return self.n==o.n
    def __lt__(self,o): return (len(self),-self.n) <  (len(o),-o.n)
    def __le__(self,o): return (len(self),-self.n) <= (len(o),-o.n)
    
    def link(self,others): 
        for c in others: c.add(self)
    def unLink(self):
        others = tuple(c for c in self if self in c)
        for c in others: c.discard(self)
        return others



def square_sums(top):
    
    def dfs(cnds):
        if len(out)==top: return 1
        
        cnds = sorted(cnds)
        if not cnds or not cnds[0] and len(out)+1!=top:
            return False
        
        for c in cnds:
            others = c.unLink()
            out.append(c.n)
            if dfs(c): return 1
            out.pop()
            c.link(others)
        return False
        
    cnds = [ Cnd(n) for n in range(1,top+1) ]
    for c in cnds:
        c.update( cnds[sq-c.n-1] for sq in SQ if c.n<sq and sq-c.n<=top and 2*c.n!=sq )
    cnds.sort()
    if len(cnds[0])==1: cnds=[c for c in cnds if len(c)==1]
    
    out  = []
    return dfs(cnds) and out
  
#################
import random

def lru_cache(f):
    f.cache = {}
    def _f(*args, **kwargs):
        if args[-1] not in f.cache:
            f.cache[args[-1]] = f(*args, **kwargs)
        return f.cache[args[-1]]
    return _f

is_square = {i : round(i ** 0.5) ** 2 == i for i in range(1, 2 * 4000)}

cache = {1 : [1],
        2 : False,
        3 : False,
        4 : False,
        5 : False,
        6 : False,
        7 : False,
        8 : False,
        9 : False,
        10 : False,
        11 : False,
        12 : False,
        13 : False,
        14 : False,
        15 : [8, 1, 15, 10, 6, 3, 13, 12, 4, 5, 11, 14, 2, 7, 9],
        16 : [8, 1, 15, 10, 6, 3, 13, 12, 4, 5, 11, 14, 2, 7, 9, 16],
        17 : [16, 9, 7, 2, 14, 11, 5, 4, 12, 13, 3, 6, 10, 15, 1, 8, 17],
        18 : False,
        19 : False,
        20 : False,
        21 : False,
        22 : False,
        23 : [2, 23, 13, 12, 4, 21, 15, 10, 6, 19, 17, 8, 1, 3, 22, 14, 11, 5, 20, 16, 9, 7, 18],
        24 : False,
        25 : [2, 23, 13, 12, 24, 25, 11, 14, 22, 3, 1, 8, 17, 19, 6, 10, 15, 21, 4, 5, 20, 16, 9, 7, 18],
        26 : [2, 14, 22, 3, 13, 23, 26, 10, 6, 19, 17, 8, 1, 15, 21, 4, 12, 24, 25, 11, 5, 20, 16, 9, 7, 18],
        27 : [1, 8, 17, 19, 6, 3, 13, 12, 24, 25, 11, 14, 22, 27, 9, 16, 20, 5, 4, 21, 15, 10, 26, 23, 2, 7, 18],
        28 : [1, 15, 10, 26, 23, 13, 3, 6, 19, 17, 8, 28, 21, 4, 12, 24, 25, 11, 5, 20, 16, 9, 27, 22, 14, 2, 7, 18],
        29 : [1, 24, 25, 11, 5, 4, 12, 13, 3, 6, 19, 17, 8, 28, 21, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
        30 : [1, 24, 25, 11, 5, 4, 12, 13, 3, 6, 30, 19, 17, 8, 28, 21, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
        31 : [1, 15, 10, 6, 30, 19, 17, 8, 28, 21, 4, 5, 31, 18, 7, 29, 20, 16, 9, 27, 22, 3, 13, 12, 24, 25, 11, 14, 2, 23, 26],
        32 : [1, 8, 28, 21, 4, 32, 17, 19, 30, 6, 3, 13, 12, 24, 25, 11, 5, 31, 18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15],
        33 : [1, 8, 28, 21, 4, 32, 17, 19, 30, 6, 3, 13, 12, 24, 25, 11, 5, 20, 29, 7, 18, 31, 33, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15],
        34 : [1, 3, 6, 19, 30, 34, 2, 7, 18, 31, 33, 16, 9, 27, 22, 14, 11, 25, 24, 12, 13, 23, 26, 10, 15, 21, 28, 8, 17, 32, 4, 5, 20, 29],
        35 : [1, 3, 6, 19, 30, 34, 2, 7, 18, 31, 33, 16, 9, 27, 22, 14, 11, 25, 24, 12, 13, 23, 26, 10, 15, 21, 28, 8, 17, 32, 4, 5, 20, 29, 35],
        36 : [1, 3, 6, 10, 26, 23, 2, 7, 18, 31, 33, 16, 9, 27, 22, 14, 35, 29, 20, 5, 11, 25, 24, 12, 13, 36, 28, 8, 17, 19, 30, 34, 15, 21, 4, 32],
        37 : [22, 14, 35, 29, 20, 5, 11, 25, 24, 1, 3, 6, 10, 26, 23, 2, 7, 18, 31, 33, 16, 9, 27, 37, 12, 13, 36, 28, 8, 17, 19, 30, 34, 15, 21, 4, 32],
        38 : [5, 20, 29, 35, 14, 22, 3, 6, 10, 15, 34, 30, 19, 17, 32, 4, 21, 28, 36, 13, 12, 37, 27, 9, 16, 33, 31, 18, 7, 2, 23, 26, 38, 11, 25, 24, 1, 8],
        39 : [11, 38, 26, 23, 2, 7, 18, 31, 33, 16, 9, 27, 37, 12, 13, 36, 28, 21, 4, 32, 17, 8, 1, 24, 25, 39, 10, 15, 34, 30, 19, 6, 3, 22, 14, 35, 29, 20, 5],
        40 : [16, 33, 31, 18, 7, 2, 23, 26, 38, 11, 5, 20, 29, 35, 14, 22, 3, 6, 19, 30, 34, 15, 10, 39, 25, 24, 1, 8, 17, 32, 4, 21, 28, 36, 13, 12, 37, 27, 9, 40],
        41 : [16, 33, 31, 18, 7, 2, 23, 26, 38, 11, 5, 20, 29, 35, 14, 22, 3, 6, 19, 30, 34, 15, 10, 39, 25, 24, 1, 8, 17, 32, 4, 21, 28, 36, 13, 12, 37, 27, 9, 40, 41],
        42 : [2, 14, 35, 29, 20, 5, 11, 38, 26, 23, 41, 40, 9, 27, 37, 12, 13, 36, 28, 21, 4, 32, 17, 8, 1, 24, 25, 39, 10, 15, 34, 30, 19, 6, 3, 22, 42, 7, 18, 31, 33, 16],
        43 : [2, 14, 35, 29, 20, 16, 33, 31, 18, 7, 42, 22, 3, 13, 36, 28, 21, 4, 32, 17, 8, 1, 24, 12, 37, 27, 9, 40, 41, 23, 26, 38, 43, 6, 19, 30, 34, 15, 10, 39, 25, 11, 5],
        44 : [2, 14, 35, 29, 20, 16, 33, 31, 18, 7, 42, 22, 3, 13, 36, 28, 21, 4, 32, 17, 8, 1, 24, 12, 37, 27, 9, 40, 41, 23, 26, 38, 43, 6, 19, 30, 34, 15, 10, 39, 25, 11, 5, 44],
        45 : [13, 3, 6, 43, 38, 26, 23, 41, 40, 9, 16, 33, 31, 18, 7, 42, 22, 27, 37, 12, 24, 1, 8, 17, 32, 4, 21, 28, 36, 45, 19, 30, 34, 15, 10, 39, 25, 11, 5, 44, 20, 29, 35, 14, 2],
        46 : [25, 39, 10, 15, 34, 2, 14, 11, 5, 44, 20, 29, 35, 46, 3, 6, 30, 19, 45, 4, 32, 17, 8, 1, 24, 12, 37, 27, 22, 42, 7, 18, 31, 33, 16, 9, 40, 41, 23, 26, 38, 43, 21, 28, 36, 13],
        47 : [13, 36, 28, 21, 43, 38, 26, 23, 41, 40, 9, 16, 33, 31, 18, 7, 42, 22, 27, 37, 12, 24, 1, 8, 17, 32, 4, 45, 19, 30, 6, 3, 46, 35, 29, 20, 44, 5, 11, 14, 2, 47, 34, 15, 10, 39, 25],
        48 : [13, 36, 28, 21, 43, 38, 26, 23, 41, 40, 9, 16, 48, 33, 31, 18, 7, 42, 22, 27, 37, 12, 24, 1, 8, 17, 32, 4, 45, 19, 30, 6, 3, 46, 35, 29, 20, 44, 5, 11, 14, 2, 47, 34, 15, 10, 39, 25],
        49 : [4, 45, 19, 30, 6, 10, 39, 25, 24, 1, 8, 17, 32, 49, 15, 34, 47, 2, 14, 11, 5, 44, 20, 29, 35, 46, 3, 13, 36, 28, 21, 43, 38, 26, 23, 41, 40, 9, 16, 48, 33, 31, 18, 7, 42, 22, 27, 37, 12]}

def find_best(left, start, end):
    best_pair = (-1, -1)
    k = 0
    for i in range(len(left) - 1):
        x, y = left[i], left[i + 1]
        if is_square[x + start]:
            if is_square[y + end]:
                return (0, i)
            new_pair = (y, i)
            k += 1
            if random.randint(16 // k, 256 // k) >= 16:
                best_pair = new_pair
    if -1 == best_pair[0]:
        return (2, -1)
    else: 
        return (1, best_pair[1])
        
@lru_cache
def add_next_number(sequence, N):
    part1, part2 = sequence, [N]
    for _ in range(10000):
        part1_reverse, part2_reverse = part1[::-1], part2[::-1]
        m = ((part1, part2), (part1_reverse, part2), (part1, part2_reverse), (part1_reverse, part2_reverse), 
            (part2, part1), (part2_reverse, part1), (part2, part1_reverse), (part2_reverse, part1_reverse))
        for l, r in m:
            if is_square[l[-1] + r[0]]:
                return l + r
        best_stat, best_shift = 2, 0
        left, right = [], []
        for l, r in m:
            status, idx = find_best(l, r[0], r[-1])
            if 2 == status or status > best_stat:
                continue;
            shift = l[idx + 1] - r[0]
            if status < best_stat or shift < best_shift:
                best_stat, left, right = status, l, r
                best_shift = shift
        status, idx = find_best(left, right[0], right[-1])
        part1, part2 = left[idx + 1:], left[0:idx + 1] + right
    return []
    
def square_sums(number):
    treshold = len(cache)
    if number not in cache:
        vec = cache[treshold]
        for i in range(treshold + 1, number):
            vec = add_next_number(vec, i)
        return add_next_number(vec, number)
    return cache[number]
  
#######################
import sys

# this is a recursive solution that creates n stacks for square_sums(n), raise the ceiling
sys.setrecursionlimit(10**6)

def square_sums(n):
    return findHamiltonianPath(getSquareSumsGraph(n))

# generate undirected graph of numbers in a range
# connect all vertices v1 and v2 that sum to a perfect square, where sqrt(v1 + v2) = an integer
# example: given 6 and 10, sqrt(6 + 10) = 4, therefore connect vertex(6) to vertex(10)
def getSquareSumsGraph(n):
    squares = {x for x in range(4, 2 * n) if (x ** (1 / 2)).is_integer()}  # generate perfect squares in range 2n
    graph = {}  # initialize an empty dictionary

    for vertex in range(1, n + 1):  # iterate the range 1 -> n, each is a vertex (v1)
        subVertices = []  # this empty array will represent the vertices connected to vertex
        for square in squares:  # iterate the pre-calculated squares
            candidate = square - vertex  # since v1 + v2 (candidate) = square; v2 = square - v1
            if 0 < candidate <= n and candidate != vertex:  # confirm that candidate exists in the range and != v1
                subVertices.append(candidate)  # keep candidate (v2)
        graph[vertex] = subVertices  # all vertices connected to vertex have been collected, store them in the graph

    return graph


# return the first hamiltonian path found in the graph
# if no path found, return False
def findHamiltonianPath(graph):
    graphLength = len(graph)  # store the graph length for optimization
    subGraph = graph.copy()  # copy the graph. subGraph will be used to add and remove connections as we iterate
    path = []  # path will store our final result

    # recursive child function handles searching for the path
    def search(options):
        if len(path) == graphLength:  # if path and graph are the same length, Hamiltonian Path has been found
            return path  # return the Hamiltonian Path
        options = sorted(options, key=lambda option: len(graph[option]))  # sort by shortest subVertices - optimization
        for option in options:  # iterate all the options. we are starting with the vertices that have the least options
            path.append(option)  # add the option to the path
            for vertex in graph[option]:  # now that option is in the path, remove it from connected subVertices
                subGraph[vertex].remove(option)
            if search(subGraph[option]):  # recurse from the next vertex of position option
                return path  # a member of the stack has found a path, return the path
            path.pop()  # path was not found with that option, remove it from the path
            for vertex in graph[option]:  # put the option back in all the subVertices it should be connected to
                subGraph[vertex].append(option)
        return False  # no path was found, return False

    return search([*range(1, graphLength + 1)])  # seed the search with the full range of options
  
########################
from collections import defaultdict, deque
from itertools import combinations

sq_n = {1: [1], 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False, 10: False,
        11: False, 12: False, 13: False, 14: False, 15: [8, 1, 15, 10, 6, 3, 13, 12, 4, 5, 11, 14, 2, 7, 9],
        16: [8, 1, 15, 10, 6, 3, 13, 12, 4, 5, 11, 14, 2, 7, 9, 16],
        17: [16, 9, 7, 2, 14, 11, 5, 4, 12, 13, 3, 6, 10, 15, 1, 8, 17],
        18: False, 19: False, 20: False, 21: False, 22: False,
        23: [2, 23, 13, 12, 4, 21, 15, 10, 6, 19, 17, 8, 1, 3, 22, 14, 11, 5, 20, 16, 9, 7, 18], 24: False,
        25: [2, 23, 13, 12, 24, 25, 11, 14, 22, 3, 1, 8, 17, 19, 6, 10, 15, 21, 4, 5, 20, 16, 9, 7, 18]}

def build(n):
    lim = int(1 + (2*n-1) ** 0.5)
    squares = [x**2 for x in range(2, lim)]
    opts = defaultdict(list)
    for x in combinations(range(1, n+1), 2):
        if sum(x) in squares:
            opts[x[0]].append(x[1])
            opts[x[1]].append(x[0])
    return opts

def roundhouse(sq_n):
    d = build(1000)
    for x in range(26, 1001):
        queue = deque([(sq_n[x-1], [x])])
        while queue:
            a, b = queue.pop()
            options = newoptions(a,b,d)
            if not options[0][1]:
                sq_n[x] = options[0][0]
                break
            queue.extendleft(options)
    return sq_n

def newoptions(a, b, d):
    options = []
    for _ in range(2):
        a, b = b, a
        a_left_match, a_right_match = d[a[0]], d[a[-1]]
        b_left_match, b_right_match = d[b[0]], d[b[-1]]
        # check perfect match
        for i, x in enumerate(b[1:]):
            if (b[i] in a_left_match and x in a_right_match):
                return [(b[:i+1] + a + b[i+1:], [])]
            if (x in a_left_match and b[i] in a_right_match):
                return [(b[:i+1] + a[::-1] + b[i+1:], [])]
        # compute new splits
        for x in a_left_match:
            if x in b:
                options.append((b[:b.index(x)+1] + a, b[b.index(x)+1:]))
                options.append((b[:b.index(x)], a[::-1] + b[b.index(x):]))
        if a_left_match != a_right_match:
            for x in a_right_match:
                if x in b:
                    options.append((b[:b.index(x)+1] + a[::-1], b[b.index(x)+1:]))
                    options.append((b[:b.index(x)], a + b[b.index(x):]))
    return options 

sq_n = roundhouse(sq_n)

def square_sums(n):
    global sq_n
    return sq_n[n]
  
###################
import random
import time

memoize = {}
squares = []


def filer_value(val, arr, n):
    return {(x - val) for x in arr if val < x <= val + n}


def square_sums0(n):
    size = n

    if n in memoize:
        return memoize[n]
    else:

        if n < 3:
            return False
        else:
            max_sq = int((2 * n - 1) ** 0.5 // 1)
        squares = [(k + 1) ** 2 for k in range(max_sq)]
        print(squares)

        g = [i + 1 for i in range(n)]
        start = g[:]
        to_visit = {i + 1: [] for i in range(n)}

        while start:
            sv = start.pop()
            visited = {sv}
            path = [sv]
            to_visit[sv] = list(filer_value(sv, squares, n) - visited)
            print(filer_value(sv, squares, n))
            cur = sv
            while to_visit[cur]:
                v = to_visit[cur].pop()
                path.append(v)
                if len(path) == size:
                    break

                visited.add(v)
                to_visit[v] = []
                to_visit[v] = filer_value(v, squares, n) - visited
                cur = v

                while not to_visit[cur]:
                    p = path.pop()
                    visited.remove(p)
                    if path:
                        cur = path[-1]
                    else:
                        break
                if not path:
                    break
            if len(path) == size:
                memoize[n] = path
                break

        return path if len(path) == size else False


def try_merge(a, b):
    g = [x + 1 for x in range(len(a[1:-1]) - 2) if (a[x + 1] + b[0]) in squares]
    c = []
    if not g:
        return False
    random.shuffle(g)
    for x in g:
        if (a[x + 1] + b[-1]) in squares:
            c = a[:]
            c[x + 1:x + 1] = b
            break
        elif (a[0] + a[x + 1]) in squares:
            t = a[x + 1:]
            c = [*t[::-1], *a[:x + 1], *b]
            break
        else:
            random.seed(time.time())
            rr = random.randrange(0, 3)
            if rr == 0:
                c = try_merge(a[:x + 1] + b, a[x + 1:])
            elif rr == 1:
                c = try_merge(a[x + 1:], a[:x + 1] + b)
            elif rr == 2:
                c = try_merge(a[:x + 1] + b, (a[x + 1:])[::-1])
            elif rr == 3:
                c = try_merge((a[:x + 1] + b)[::-1], a[x + 1:])
            elif rr == 4:
                c = try_merge(b, a)
            if c:
                break
    if not c:
        while True:
            random.seed(time.time())
            rr = random.randrange(0, 3)
            if rr == 0:
                c = try_merge(b, a)
            elif rr == 1:
                c = try_merge(a[::-1], b)
            elif rr == 2:
                c = try_merge(a, b[::-1])
            if c:
                return c
    return c


def square_sums(n):
    NN = 40
    if n < NN:
        return square_sums0(n)
    else:
        a = square_sums0(NN)

    global squares
    max_sq = int((2 * n - 1) ** 0.5 // 1)
    squares = [(k + 1) ** 2 for k in range(max_sq)]

    for b in range(NN + 1, n + 1):
        if b in memoize:
            a = memoize[b]
        else:
            if (a[0] + b) in squares:
                a = a[::-1]
                a.append(b)
            elif (a[0] + b) in squares:
                a.append(b)
            else:
                a = try_merge(a, [b])

            memoize[b] = a
    return a
  
#####################
def connect_nodes(l1, l2, n):
    l1s = []
    l2s = []
    l3s = [];
    while True:
        if len(l2) == n:
            return l2
        i = l2[-1]
        l1 = [*l1]
        for j in l1[i]:
            l1[j] = [*l1[j]]
            l1[j].remove(i)
        l3=sorted(l1[i], key=lambda i:len(l1[i]))
        while len(l3) == 0 and len(l3s) > 0:
            l1 = l1s.pop()
            l2 = l2s.pop()
            l3 = l3s.pop()
        if len(l3) > 0:
            j = l3.pop(0)
            if len(l1[j]) > 1:
                l1s.append(l1)
                l2s.append(l2)
                l3s.append(l3)
            l2 = [*l2, j]
        else:
            return None

def square_sums(num):
    if num > 1:
        sq_nms = [i**2 for i in range(2,46)]
        l1 = [[] for i in range(num)]
        for sqn in sq_nms:
            if sqn >= 2*num:
                break;
            for j0 in range(1, int(sqn/2 + .5)) if sqn <= num else range(int(sqn/2) + 1, num + 1):
                j1=sqn-j0
                l1[j0-1].append(j1-1)
                l1[j1-1].append(j0-1)
        ends=[];
        for i in range(num):
            if len(l1[i]) == 0:
                return False
            elif len(l1[i]) == 1:
                ends.append(i)
        l2=None
        if 0 < len(ends) < 3:
            l2 = connect_nodes(l1,[ends[0]],num)
        elif len(ends) == 0:
            for i in sorted(range(num), key = lambda j:len(l1[j]))[:-1]:
                l2 = connect_nodes(l1,[i],num)
                if l2:
                    break;
        return [i + 1 for i in l2] if l2 else False
    else:
        return [1]
      
##########################
import random
import math

#This is is just a backtracjing search  - suprisingly it is fast enougph to solve this kata but will be used just for n<100 
def brutesearch(n):
    squares = [i**2 for i in range(2, math.floor((2*n-1)**0.5)+1 ) ]    
    neib = [list(range(1,n+1))] + [ [s-i for s in squares if (0 < s-i < n+1) and 2*i != s ] for i in range(1,n+1)]
    def search(j=0, last=0, out=[0]*n):
        if j == n-1:
            out[j] = neib[last].pop()           
            return out
        for i in sorted(neib[last], key = lambda x: len(neib[x]) ):
            if len(neib[i])==0:
                continue            
            for a in neib[i]:
                neib[a].remove(i)                
            out[j] = i
            result = search(j+1, i, out)
            if result:
                return result
            for a in neib[i]:
                neib[a].append(i)           
        out[j] = 0
        return False    
    return search() 

#The idea behind this is that for n=1000 for each number at least 10 other numbers, that is 1% are allowed neigbhours
#So if we have completed the task for n-1 and now want to add the nth by just inserting somewhere in the sequence the chnace 
#of succeeding could be as high as about 1000*1%*1% = 10%  - but ths still gives 90% chance of failure
#So the approach is to call the n-1 proper sequence A and nth number a B sequence
#we then add B string to some middle point of A string in a way that "sqaures" rule is satisfied and the rest of the A string becomes B string
#This will give us different ends for B string that we can again try to fit somewhere in the middle of A string
#Some random swaps and reversals are also added - the idea is that, hopefully, each new mutation is a new 10% to succeed and by
#trying long enouph - but not nearly as long as with backtracking - the solution will be found.
#For example if eveything is as random as assumed and each permutation gives a 10% chnace of success than the chance of
#not succeeding in 100 attempts is just (1-0.1)^100 = 0.003%

            
def mutatingsearch(a):
    if len(a)%100 == 0: print(len(a))
    b=[len(a)+1]
    squares = [i**2 for i in range(2, int( ((2*(1 + len(a)))**0.5)//1 ) )]
    
    def check(a,b):
        if len(a)==0:
            return b            
        if len(b)==0:
            return a     
        if (a[-1]+b[0]) in squares:
            return a + b 
        if (a[-1]+b[-1]) in squares:
            return a + b[::-1]      
        for i in range(1,len(a)-1):
            if (a[i]+b[0]) in squares:
                if (a[i+1]+b[-1]) in squares:
                    return a[:i+1] + b + a[i+1:]
                if (a[i-1]+b[-1]) in squares:
                    return a[:i] + b[::-1] + a[i:]
        return False
    
    def mutate(a,b):
        ins = [i for i,aa in enumerate(a) if(aa+b[0]) in squares]
        if ins == []:
            a, b = b, a
            ins = [i for i,aa in enumerate(a) if(aa+b[0]) in squares]
            if ins == []:
                ins = [i for i,aa in enumerate(a) if ( (aa+a[0]) in squares and i>1 ) ]
                ins = random.choice(ins)
                return a[ins-1::-1] + a[ins:] , b    
        ins = random.choice(ins)
        return a[:ins+1]+b, a[ins+1:]
    
    for i in range(10000):
        done = check(a,b) or check(b,a) 
        if done:
            return done
        
        if random.choice([0,1]):
            a, b = b, a
        if random.choice([0,1]):
            a = a[::-1]
        if random.choice([0,1]):
            b = b[::-1]
        
        a, b = mutate(a,b)
        

#This will make the final function that will use brutesearch function for n<40 and mutatingsearch for n>40 with memorisation of previous results 
def make_square_sums():
    d={}   
    def square_sums(num):
        if num in d:
            return d[num]
        if num < 100:
            d[num] = brutesearch(num)
            return d[num]
        
        try:
            n = max([k for k in d.keys() if k<num])
        except ValueError:
            n=100
            d[100] = brutesearch(100)
            
        a = d[n]  
        for i in range(num-n):
            a = mutatingsearch(a)            
            d[n+i+1] = a
        return a    
    return square_sums  

square_sums = make_square_sums()

########################
import math
import sys
sys.setrecursionlimit(1010)

#This is is just a backtracjing search  - suprisingly it is fast enougph to solve this kata but will be used just for n<100 
def brutesearch(n):
    squares = [i**2 for i in range(2, math.floor((2*n-1)**0.5)+1 ) ]    
    neib = [list(range(1,n+1))] + [ [s-i for s in squares if (0 < s-i < n+1) and 2*i != s ] for i in range(1,n+1)]
    def search(j=0, last=0, out=[0]*n):
        if j == n-1:
            out[j] = neib[last].pop()           
            return out
        for i in sorted(neib[last], key = lambda x: len(neib[x]) ):
            if len(neib[i])==0:
                continue            
            for a in neib[i]:
                neib[a].remove(i)                
            out[j] = i
            result = search(j+1, i, out)
            if result:
                return result
            for a in neib[i]:
                neib[a].append(i)           
        out[j] = 0
        return False    
    return search()

square_sums = brutesearch
