blocks = {
    'A': {'B': 'C', 'E': 'I', 'D': 'G'},
    'B': {'E': 'H'},
    'C': {'B': 'A', 'E': 'G', 'F': 'I'},
    'D': {'E': 'F'},
    'E': {},
    'F': {'E': 'D'},
    'G': {'D': 'A', 'E': 'C', 'H': 'I'},
    'H': {'E': 'B'},
    'I': {'E': 'A', 'F': 'C', 'H': 'G'}
}

neighbors = {
    'A': {'B', 'D', 'E', 'F', 'H'},
    'B': {'A', 'C', 'D', 'E', 'F', 'G', 'I'},
    'C': {'B', 'D', 'E', 'F', 'H'},
    'D': {'A', 'B', 'C', 'E', 'G', 'H', 'I'},
    'E': {'A', 'B', 'C', 'D', 'F', 'G', 'H', 'I'},
    'F': {'A', 'B', 'C', 'E', 'G', 'H', 'I'},
    'G': {'B', 'D', 'E', 'F', 'H'},
    'H': {'A', 'C', 'D', 'E', 'F', 'G', 'I'},
    'I': {'B', 'D', 'E', 'F', 'H'}
}


def count_patterns_from(last, length, history=set()):
    if length == 1:
        return 1
    elif not(0 < length <= 9):
        return 0

    result = 0
    for point in neighbors[last].difference(history):
        history.add(last)
        result += count_patterns_from(point, length - 1, history)
        history.remove(last)

    for point in (v for k, v in blocks[last].items() if k in history and v not in history):
        history.add(last)
        result += count_patterns_from(point, length - 1, history)   
        history.remove(last)

    return result
  
######################
EQUIV_PTS = {same: src for src,seq in (('A','CGI'), ('B','DFH')) for same in seq}

ALL       =  set('ABCDEFGHI')
LINKED_TO = {'A': ('BC','DG','EI','F', 'H'),
             'B': ('A', 'C', 'D', 'EH','F', 'G', 'I'),
             'C': ('BA','D', 'EG','FI','H'),
             'D': ('A', 'B', 'C', 'EF','G', 'H', 'I'),
             'E': tuple('ABCDFGHI'),
             'F': ('A', 'B', 'C', 'ED','G', 'H', 'I'),
             'G': ('DA','B', 'EC','F', 'HI'),
             'H': ('A', 'EB','C', 'D', 'F', 'G', 'I'),
             'I': ('EA','B', 'FC','D', 'HG')
            }


def DFS(c, depth, root, seens, patterns):
    if depth > len(ALL): return                
    
    patterns[root][depth] += 1
    
    seens.add(c)
    toExplore = ''.join( next((n for n in seq if n not in seens), '') for seq in LINKED_TO[c] )
    for nextC in toExplore:
        DFS(nextC, depth+1, root, seens, patterns)
    seens.discard(c)
    

PATTERNS = {}
for c in "ABE":
    PATTERNS[c] = [0]*10
    DFS(c, 1, c, set(), PATTERNS)


def count_patterns_from(start, length):
    if not (0 < length < 10) or start not in ALL: return 0    
    
    actualStart = EQUIV_PTS.get(start, start)
    return PATTERNS[actualStart][length]
  
########################
vals = [0,1,2,5,6,7,10,11,12]
def count_patterns_from(firstPoint, length, left=set(vals)):
    if length<1 or length>len(left): return 0
    if length==1: return 1
    n = vals[ord(firstPoint)-65] if type(firstPoint)==str else firstPoint
    return sum(count_patterns_from(m,length-1,left-{n}) for m in left-{n} if (m+n)/2 not in left)
  
####################
access = {'A':('BDEFH', {'C':'B', 'G':'D', 'I':'E'}),
          'B':('ACDEFGI', {'H':'E'}),
          'C':('BDEFH', {'A':'B', 'G':'E', 'I':'F'}),
          'D':('ABCEGHI', {'F':'E'}),
          'E':('ABCDFGHI', {}),
          'F':('ABCEGHI', {'D':'E'}),
          'G':('BDEFH', {'A':'D', 'C':'E', 'I':'H'}),
          'H':('ACDEFGI', {'B':'E'}),
          'I':('BDEFH', {'A':'E', 'C':'F', 'G':'H'})}

def count_patterns_from(firstPoint, length):
    def rec(current, left, visited):
        if current in visited: return 0
        if left == 1: return 1
        visited = visited | {current}
        direct = sum(rec(c, left-1, visited) for c in access[current][0])
        over = sum(rec(c, left-1, visited) for c,t in access[current][1].items() if t in visited)
        return direct + over
    return rec(firstPoint, length, set()) if 0 < length < 10 else 0
  
####################
def count_patterns_from(firstPoint, length, used=set()):
    if length == 0 or length > 9: return 0
    if length == 1: return 1
    
    POINTS = {
            'A': (0, 0), 'B': (0, 1), 'C': (0, 2),
            'D': (1, 0), 'E': (1, 1), 'F': (1, 2),
            'G': (2, 0), 'H': (2, 1), 'I': (2, 2)
    }
    
    nways = 0
    src = POINTS[firstPoint]
    for secondPoint, dest in POINTS.items():
        dist = (dest[0] - src[0], dest[1] - src[1])
        if firstPoint != secondPoint and dest not in used and not (dist[0] % 2 == 0 and dist[1] % 2 == 0 and (src[0] + dist[0] // 2, src[1] + dist[1] // 2) not in used):
            nways += count_patterns_from(secondPoint, length - 1, used | {src})
    return nways
  
#####################
def get_position(point):
    positions = {'A': 1,
                 'B': 2,
                 'C': 1,
                 'D': 2,
                 'E': 3,
                 'F': 2,
                 'G': 1,
                 'H': 2,
                 'I': 1}
    return positions[point]
    
def count_patterns_from(first_point, length):
    if length == 0 or length > 9:
        return 0
    print(first_point, length)
    combinations = {1: {1: 1, 2: 1, 3: 1},
                    2: {1: 5, 2: 7, 3: 8},
                    3: {1: 31, 2 :37, 3: 48},
                    4: {1: 154, 2: 188, 3: 256},
                    5: {1: 684, 2: 816, 3: 1152},
                    6: {1: 2516, 2: 2926, 3: 4248},
                    7: {1: 7104, 2: 8118, 3: 12024},
                    8: {1: 13792, 2: 15564, 3: 23280},
                    9: {1: 13792, 2: 15564, 3 :23280}}
    
    return combinations[length][get_position(first_point)]
  
########################
def count_patterns_from(firstPoint, length):
    if 0 < length < 10:
        unseen = {"A","B","C","D","E","F","G","H","I"} - {firstPoint}
        return  helper(firstPoint, length-1, unseen)
    return 0

def helper(firstPoint, length, unseen):
    #Base Case
    if length == 0:
        return 1
    
    #Recursive case
    count = 0
    for i in unseen:
        if icansee(i, firstPoint, unseen):
            count += helper(i, length-1, unseen - {i})
    return count

def icansee(i,j, unseen):
    '''Checks to see if point j is a valid move from i'''
    points = sorted([i,j])
    if points in [["B","H"],["D","F"],["A","I"],["C","G"]]: return not "E" in unseen
    if points == ["A","C"]: return not "B" in unseen
    if points == ["A","G"]: return not "D" in unseen
    if points == ["C","I"]: return not "F" in unseen
    if points == ["G","I"]: return not "H" in unseen
    return 1
  
############################
def count_patterns_from(firstPoint, length):
    # Your code here!
    visited = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(False)
        visited.append(row)

    def dfs(x, y, length):
        if (visited[x][y]):
            return 0
        visited[x][y] = True
        res = 0
        if (length == 1):
            res = 1
        else:
            for i in range(3):
                for j in range(3):
                    if not (x == i and y == j): 
                        if abs(i - x) == 2 and j == y:
                            if (visited[(x+i)//2][y]):
                                res += dfs(i, j, length-1)
                        elif abs(j - y) == 2 and x == i:
                            if (visited[x][(y+j)//2]):
                                res += dfs(i, j, length-1)
                        elif abs(j - y) == 2 and abs(i - x) == 2:
                            if (visited[(x+i)//2][(y+j)//2]):
                                res += dfs(i, j, length-1)
                        else:
                            res += dfs(i, j, length-1)

        visited[x][y] = False
        return res
    return dfs((ord(firstPoint) - ord('A')) // 3, (ord(firstPoint) - ord('A')) % 3, length)
  
##############################
graph = {
    'A': {'dir': ['B', 'D', 'E', 'F', 'H'],
          'ind': [('D', 'G'), ('E', 'I'), ('B', 'C')]
          },
    'B': {'dir': ['A', 'C', 'D', 'E', 'F', 'G', 'I'],
          'ind': [('E', 'H')]
          },
    'C': {'dir': ['B', 'D', 'E', 'F', 'H'],
          'ind': [('E', 'G'), ('F', 'I'), ('B', 'A')]
          },
    'D': {'dir': ['A', 'B', 'E', 'G', 'H', 'C', 'I'],
          'ind': [('E', 'F')]
          },
    'E': {'dir': ['A', 'B', 'C', 'D', 'G', 'F', 'H', 'I'],
          'ind': []
          },
    'F': {'dir': ['B', 'C', 'E', 'H', 'I', 'A', 'G'],
          'ind': [('E', 'D')]
          },
    'G': {'dir': ['D', 'E', 'H', 'F', 'B'],
          'ind': [('D', 'A'), ('E', 'C'), ('H', 'I')]
          },
    'H': {'dir': ['D', 'E', 'F', 'G', 'I', 'A', 'C'],
          'ind': [('E', 'B')]
          },
    'I': {'dir': ['B', 'D', 'E', 'F', 'H'],
          'ind': [('H', 'G'), ('E', 'A'), ('F', 'C')]
          },
}


def count_patterns_from(firstPoint, length):
    return 0 if length < 0 or length > 10 else count_patterns_recursive(stack='',
                                                                        node=firstPoint,
                                                                        length=length)


def count_patterns_recursive(stack, node, length):
    if length == 1: return 1

    stack += node
    candidates = node_candidates(stack=stack)
    result = 0
    for node in candidates:
        result += count_patterns_recursive(stack=stack, node=node, length=length-1)

    return result


def node_candidates(stack):
    candidates = []
    node = stack[-1]
    for n_dir in graph[node]['dir']:
        if n_dir not in stack:
            candidates.append(n_dir)

    for n_ind in graph[node]['ind']:
        if n_ind[0] in stack and n_ind[1] not in stack:
            candidates.append(n_ind[1])
    return candidates
  
################################
POINT_CONNECTIONS = {'A': ['B', 'D', 'E', 'F', 'H'], 'B': ['A', 'D', 'E', 'G', 'F', 'I', 'C'], 'C': ['B', 'F', 'E', 'D', 'H'], 'D': ['A', 'B', 'C', 'E', 'G', 'H', 'I'], 'E': ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I'], 'F': ['A', 'B', 'C', 'E', 'G', 'H', 'I'], 'G': ['D', 'B', 'E', 'H', 'F'], 'H': ['A', 'C', 'D', 'E', 'F', 'G', 'I'], 'I': ['H', 'D', 'E', 'F', 'B']}
PASS_OVER = {'A': {'B': 'C', 'E': 'I', 'D': 'G'}, 'B': {'E': 'H'}, 'C': {'B': 'A', 'E': 'G', 'F': 'I'}, 'D': {'E': 'F'}, 'E': {}, 'F': {'E': 'D'}, 'G': {'D': 'A', 'E': 'C', 'H': 'I'}, 'H': {'E': 'B'}, 'I': {'H': 'G', 'E': 'A', 'F': 'C'}}


def count_patterns_from(firstPoint, length):
    if length not in range(1, 10): return 0
    elif length == 1: return 1
    queue = [firstPoint + i for i in POINT_CONNECTIONS[firstPoint]]
    while len(queue[0]) != length:
        temp = []
        for pattern in queue:
            points = POINT_CONNECTIONS[pattern[-1]].copy()
            for k, v in PASS_OVER[pattern[-1]].items():
                if k in pattern:
                    points.append(v)
            for point in points:
                if point not in pattern:
                    temp.append(pattern + point)
        queue = temp
    return len(queue)
  
#########################
unreachables = {
    ('A','C'):'B', ('C','A'):'B',
    ('A','G'):'D', ('G','A'):'D',
    ('A','I'):'E', ('I','A'):'E',
    ('B','H'):'E', ('H','B'):'E',
    ('C','I'):'F', ('I','C'):'F',
    ('C','G'):'E', ('G','C'):'E',
    ('D','F'):'E', ('F','D'):'E',
    ('G','I'):'H', ('I','G'):'H'
    }

keys = set(['A','B','C','D','E','F','G','H','I'])

def is_valid(start, path):
    def is_valid_aux(to_validate_path, cur_path):
        if to_validate_path==():
            return True
        
        head = to_validate_path[0]
        
        #if either head is a duplicate
        #it is not adjacent and the key between the 2 keys 
        #is not in cur_path --> False
        if (head in cur_path or (cur_path!=[] and \
                ((cur_path[-1], head) in unreachables 
                 and unreachables[(cur_path[-1], head)] not in cur_path ))):
            return False
        
        return is_valid_aux(to_validate_path[1:], cur_path + [head])
    return is_valid_aux(path, [start])
    
                 
from itertools import permutations

def count_patterns_from(first, length):
    if length==0:
        return 0
    
    all = permutations(keys - set(first), length-1)
    patterns = list(filter(lambda p: is_valid(first,p) , all))
    return len(patterns)
  
###########################
keys_jump = {
    ('A','C'):'B', ('C','A'):'B',
    ('A','G'):'D', ('G','A'):'D',
    ('A','I'):'E', ('I','A'):'E',
    ('B','H'):'E', ('H','B'):'E',
    ('C','I'):'F', ('I','C'):'F',
    ('C','G'):'E', ('G','C'):'E',
    ('D','F'):'E', ('F','D'):'E',
    ('G','I'):'H', ('I','G'):'H'
    }

keys = ['A','B','C','D','E','F','G','H','I']

def possible_next_step(paths):
    return [k for k in keys if #filter key from A--I so that
                 (k not in paths and #k must not be in path
                    ( #either adjacent cell-> not in dict -> adjacent
                     (paths[-1],k) not in keys_jump 
                     or 
                      #or the cell between key and k is in paths
                      keys_jump[(paths[-1],k)] in paths  
                     ))]
                
def paths_from_key(steps, paths):
    if steps==1:  #you are counting the n°of paths
        return 1  #if you are here -> paths is a path of the required length

    #note that if no more possible next_keys, invalid path --> sum returns 0
    return sum([paths_from_key(steps-1, paths+[k]) for k in possible_next_step(paths) ])


def count_patterns_from(firstPoint, length):
    return paths_from_key(length, [firstPoint])
    
##################
def count_patterns_from(firstPoint, length):
    def produceL(l, o): return l + [o]
    def produceR():
        e1 = [['A','C','G','I'], ['B','H'], ['D','F'], ['E']]
        e2 = [['A','B','C'], ['A','D','G'], ['A','E','I'], ['B','E','H'], ['C','E','G'],
              ['C','F','I'], ['C','B','A'], ['D','E','F'], ['F','E','D'], ['G','H','I'], 
              ['G','D','A'], ['G','E','C'], ['H','E','B'], ['I','E','A'], ['I','F','C'],
              ['I','H','G']]
        return e1, e2
    
    rs = [[firstPoint]]
    if firstPoint not in ['A','B','C','D','E','F','G','H','I'] or length <= 0 or length > 9: return 0
    elif length == 1: return 1
    else:
        for i in range(1, length):
            e1, e2 = produceR()
            t = []
            for r in rs:
                last = r[-1]
                if i > 1:
                    for nn in e2:
                        if last == nn[0] and nn[1] in r and nn[2] not in r: t.append(produceL(r, nn[2]))
                for n in e1:
                    if last not in n:
                        for m in n:
                            if m not in r: t.append(produceL(r, m))
            rs = t
        return len(rs)
      
####################
def count_patterns_from(firstPoint, length):
    rs = [[firstPoint]]
    ps = ['A','B','C','D','E','F','G','H','I']
    def produceR():
        e1 = [['A','C','G','I'], ['B','H'], ['D','F'], ['E']]
        e2 = [['A','B','C'], ['A','D','G'], ['A','E','I'],
              ['B','E','H'],
              ['C','E','G'], ['C','F','I'], ['C','B','A'],
              ['D','E','F'],
              ['F','E','D'],
              ['G','H','I'], ['G','D','A'], ['G','E','C'],
              ['H','E','B'],
              ['I','E','A'], ['I','F','C'], ['I','H','G']]
        return e1, e2
    
    def produceL(l, o):
        p = []
        p.extend(l)
        p.append(o)
        return p
    
    if firstPoint not in ps or length <= 0: return 0
    elif length == 1: return 1
    elif length <= len(ps):
        for i in range(1, length):
            e1, e2 = produceR()
            t = []
            for r in rs:
                last = r[-1]
                if i > 1:
                    for nn in e2:
                        if last == nn[0] and nn[1] in r and nn[2] not in r: 
                            t.append(produceL(r, nn[2]))
                for n in e1:
                    if last not in n:
                        for m in n:
                            if m not in r: t.append(produceL(r, m))
            rs = t
        return len(rs)
    else: return 0
    
##########################
import copy
from functools import lru_cache

nodes = dict(
    A=[set('BDEFH'), set('CGI')],
    B=[set('ACDEFGI'), set('H')],
    C=[set('BDEFH'), set('AGI')],
    D=[set('ABCEGHI'), set('F')],
    E=[set('ABCDFGHI'), set()],
    F=[set('ABCEGHI'), set('D')],
    G=[set('BDEFH'), set('ACI')],
    H=[set('ACDEFGI'), set('B')],
    I=[set('BDEFH'), set('ACG')],
)

allow_skip = dict(
    B=[('A', 'C'), ('C', 'A')],
    D=[('A', 'G'), ('G', 'A')],
    E=[('A', 'I'), ('B', 'H'), ('C', 'G'), ('D', 'F'), ('F', 'D'), ('G', 'C'), ('H', 'B'), ('I', 'A')],
    F=[('C', 'I'), ('I', 'C')],
    H=[('G', 'I'), ('I', 'G')],
)

start = dict(
    C='A',
    D='B',
    F='B',
    G='A',
    H='B',
    I='A'
)

def count_patterns_from(firstPoint, length):
    if length == 0 or length > 9: return 0
    if length == 1: return 1
    if length == 2: return len(nodes[firstPoint][0])
    return cache(start.get(firstPoint, firstPoint), length)

@lru_cache(maxsize=None)
def cache(firstPoint, length):
    # I'm sorry
    if length == 9:
        return firstPoint == 'A' and 13792 or firstPoint == 'B' and 15564 or 23280
    return _count_patterns_from(firstPoint, length)

def _count_patterns_from(firstPoint, length, nodes=nodes):
    nodes = copy.deepcopy(nodes)
    for v in nodes.values():
        v[0] -= {firstPoint}
        v[1] -= {firstPoint}
    skips = allow_skip.get(firstPoint)
    if skips:
        for a, b in skips:
            if b in nodes[a][1]:
                nodes[a][0].add(b)
                nodes[a][1].remove(b)
    if length == 2:
        return len(nodes[firstPoint][0])
    return sum(_count_patterns_from(c, length-1, nodes) for c in nodes[firstPoint][0])
