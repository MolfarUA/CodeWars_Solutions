from collections import deque
from itertools import chain, product

def escape(grid):
    nr, nc = len(grid), len(grid[0])
    open = {x for x in chain.from_iterable(grid) if x != '#' and not x.isupper()}
    all_keys = {x.upper() for x in chain.from_iterable(grid) if x.islower()}
    r0, c0 = next((r, c) for r, c in product(range(nr), range(nc)) if grid[r][c] == '@')
    prev = {(r0, c0, frozenset(open)): None}
    queue = deque(prev)
    while queue:
        r0, c0, o0 = queue.popleft()
        for dr, dc in (-1, 0), (1, 0), (0, -1), (0, 1):
            if 0 <= (r := r0 + dr) < nr and 0 <= (c := c0 + dc) < nc:
                if (x := grid[r][c]) in o0 and (r, c, o := o0 | {x.upper()}) not in prev:
                    prev[r, c, o] = r0, c0, o0
                    queue.append((r, c, o))
                    if x == '$' and o >= all_keys:
                        return list(_reconstruct_path(prev, (r, c, o)))[::-1]

def _reconstruct_path(prev, pos):
    while pos is not None:
        yield pos[1], pos[0]
        pos = prev[pos]
#########################
from collections import deque
def perm(lst, n):
    if n == 0:
        return [["$"]]
    if n == 1:
        return [[lst[0], "$"]]
    if len(lst) <= 1:
        return [lst]
    perms = []
    for i in range(len(lst)):
        curr = [lst[i]]
        next = lst[:i] + lst[i+1:]
        for j in perm(next, n):
            this = curr+j
            if len(this) == n:
                this += ["$"]
            perms.append(this)
    return perms
    
def escape(grid):
    h, w = len(grid), len(grid[0])
    letters = []
    positions = {}
    for r in range(h):
        for c in range(w):
            if grid[r][c] == "@":
                positions[grid[r][c]] = (c, r)
            elif grid[r][c].isalpha() and grid[r][c].islower():
                letters.append(grid[r][c])
                positions[grid[r][c]] = (c, r)
    perms = perm(letters, len(letters))
    def getPath(s, f, keys):
        keys = set(keys)
        s = positions[s]
        visited = {s}
        bfs = deque([[s]])
        while bfs:
            sofar = bfs.popleft()
            col, row = sofar[-1]
            for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nr = row+x
                nc = col+y
                if nr in range(h) and nc in range(w) and grid[nr][nc] != "#" and (nc, nr) not in visited:
                    if grid[nr][nc] == f:
                        if f == "$":
                            return sofar+[(nc, nr)]
                        return sofar
                    elif grid[nr][nc] == "." or grid[nr][nc] == "$":
                        bfs.append(sofar+[(nc, nr)])
                        visited.add((nc, nr))
                    else:
                        if grid[nr][nc].lower() in keys:
                            bfs.append(sofar+[(nc, nr)])
                            visited.add((nc, nr))
        return None
    paths = {}
    def bfsMem(s, f, keys, left, sofar, ans):
        if (s, f, keys) not in paths:
            paths[(s, f, keys)] = getPath(s, f, keys)
        curr = paths[(s, f, keys)]
        if not curr:
            return (10**9, None)
        sofar += curr
        ans += len(curr)
        if not left:
            return (ans, sofar)
        return bfsMem(f, left[0], "".join(sorted(keys+f)), left[1:], sofar, ans)
    res = (10**9, None)
    for p in perms:
        curr = bfsMem("@", p[0], "@", p[1:], [], 0)
        res = min(res, curr)
    return res[1] if res[0] != 10**9 else None
###########################
from collections import deque, defaultdict

MOVES = ((0,1), (1,0), (-1,0), (0,-1))
def get_start_and_keys(grid):
    keys = set()
    for x,row in enumerate(grid):
        for y in range(len(row)):
            if grid[x][y] == '@':
                start = (x,y)
            if grid[x][y].islower():
                keys.add(grid[x][y])
    return start, keys

def escape(grid):
    X, Y = len(grid), len(grid[0])
    WALL = '#'
    starting_keys = frozenset()

    seen = defaultdict(set)
    start_pos, all_keys = get_start_and_keys(grid)
    stored_path = {}

    #inserting starting node in the seen DS so I don't revisit.
    seen[start_pos].add(starting_keys)
    queue = deque([(*start_pos, starting_keys, all_keys)])
    reached_end = False
    while queue:
        #popping Node, current keys explored and all the remaining keys to be explored
        x,y, current_keys, remaining_keys = queue.popleft()

        #check if reached Exit with zero remaining keys to be explored.
        if grid[x][y] == '$' and not remaining_keys:
            reached_end = True
            end_x, end_y, end_keys = x,y, current_keys
            break

        for dx,dy in MOVES:
            xx = x + dx
            yy = y + dy

            if not (0<=xx<X and 0<=yy<Y) or (next_char:=grid[xx][yy]) == WALL:
                continue
            
            #updating our set of keys in the case where we found a new key which is not already added to our key-set
            updated_keys = current_keys
            if next_char.islower() and next_char not in current_keys:
                updated_keys |= {next_char}

            #reached a door without its key in the updated key-set OR traversed a node AGAIN with the same set of keys.
            if (next_char.isupper() and next_char.lower() not in updated_keys) or updated_keys in seen[(xx,yy)]:
                continue
            
            #pushing next_node, updated keys and the total remaining keys into the queue till reaching exit!
            #updating remaining keys by removing a possible key in the case of next_char being a key.
            queue.append((xx,yy,updated_keys, remaining_keys - {next_char}))
            seen[(xx,yy)].add(updated_keys)
            stored_path[(xx,yy, updated_keys)] = (x,y,current_keys)

    if not reached_end:
        return None

    full_path = [(end_y, end_x)]
    current_pos = end_x,end_y,end_keys
    while current_pos != (*start_pos, starting_keys):
        current_pos = stored_path[current_pos]
        current_x, current_y, _ = current_pos
        full_path.append((current_y, current_x))
    return full_path[::-1]
#############################
from collections import deque


def escape(grid):
    for row in grid:
        print(row)

    amount = 0
    squares = {}
    for y, row in enumerate(grid):
        for x, sq in enumerate(row):
            pos = x + 1j * y
            squares[pos] = sq
            if sq == '@':
                start = pos
            elif sq == '$':
                end = pos
            elif sq.isupper():
                amount += 1

    open_ = deque()  # [(pos, keys)]
    open_.append((start, frozenset()))
    past = {}
    
    while open_:
        current, keys = open_.popleft()
        if current == end and len(keys) == amount:
            moves = [current]
            pos = current
            while pos != start or keys:
                pos, keys = past[(pos, keys)]
                moves.append(pos)
            return [(int(move.real), int(move.imag)) for move in reversed(moves)]
        
        for move in (1, -1, 1j, -1j):
            new_pos = current + move
            new_sq = squares.get(new_pos, '#')
            new_keys = (keys | {new_sq}) if new_sq.islower() else keys
            if new_sq == '#' or (new_pos, new_keys) in past or new_sq.isupper() and new_sq.lower() not in keys:
                continue
            open_.append((new_pos, new_keys))
            past[(new_pos, new_keys)] = (current, keys)

    return None
##########################
from collections import deque, defaultdict

MOVES = ((0,1), (1,0), (-1,0), (0,-1))
def get_start_and_keys(grid):
    keys = set()
    for x,row in enumerate(grid):
        for y in range(len(row)):
            if grid[x][y] == '@':
                start = (x,y)
            if grid[x][y].islower():
                keys.add(grid[x][y])
    return start, keys

def escape(grid):
    X, Y = len(grid), len(grid[0])
    WALL = '#'
    starting_keys = frozenset()

    seen = defaultdict(set)
    start_pos, all_keys = get_start_and_keys(grid)
    stored_path = {}

    #inserting starting node in the seen DS so I don't revisit.
    seen[start_pos].add(starting_keys)
    queue = deque([(*start_pos, starting_keys, all_keys)])
    reached_end = False
    while queue:
        #popping Node, current keys explored and all the remaining keys to be explored
        x,y, current_keys, remaining_keys = queue.popleft()

        #check if reached Exit with zero remaining keys to be explored.
        if grid[x][y] == '$' and not remaining_keys:
            reached_end = True
            end_x, end_y, end_keys = x,y, current_keys
            break

        for dx,dy in MOVES:
            xx = x + dx
            yy = y + dy

            if not (0<=xx<X and 0<=yy<Y) or (next_char:=grid[xx][yy]) == WALL:
                continue
            
            #updating our set of keys in the case where we found a new key which is not already added to our key-set
            updated_keys = current_keys
            if next_char.islower():
                updated_keys |= {next_char}

            #reached a door without its key in the updated key-set OR traversed a node AGAIN with the same set of keys.
            if (next_char.isupper() and next_char.lower() not in updated_keys) or updated_keys in seen[(xx,yy)]:
                continue
            
            #pushing next_node, updated keys and the total remaining keys into the queue till reaching exit!
            #updating remaining keys to be explored by removing a possible key in the case of next_char being a key.
            queue.append((xx,yy,updated_keys, remaining_keys - {next_char}))
            seen[(xx,yy)].add(updated_keys)
            stored_path[(xx,yy, updated_keys)] = (x,y,current_keys)

    if not reached_end:
        return None

    full_path = [(end_y, end_x)]
    current_pos = end_x,end_y,end_keys
    while current_pos != (*start_pos, starting_keys):
        current_pos = stored_path[current_pos]
        current_x, current_y, _ = current_pos
        full_path.append((current_y, current_x))
    return full_path[::-1]
  ############################
  def escape(g):
    rr=0
    gn=lambda x:ord(x)-97
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j]=="@":sp=(i,j)
            elif g[i][j].islower():rr|=1<<gn(g[i][j])
    u=set()
    q=[(sp[0],sp[1],0,[(sp[1],sp[0])])]
    while q:
        i,j,m,r=q.pop(0)
        k=(i,j,m)
        if k in u:continue
        u.add(k)
        if g[i][j]=='$' and m==rr:return r
        for di,dj in [(0,1),(0,-1),(1,0),(-1,0)]:
            ni,nj=i+di,j+dj
            if 0<=ni<len(g) and 0<=nj<len(g[0]):
                if g[ni][nj]=="#":continue
                elif g[ni][nj].islower():q.append((ni,nj,m|1<<gn(g[ni][nj]),r+[(nj,ni)]))
                elif g[ni][nj].isupper():
                    ln=1<<gn(g[ni][nj].lower())
                    if m&ln!=0:q.append((ni,nj,m,r+[(nj,ni)]))
                else:q.append((ni,nj,m,r+[(nj,ni)]))
    return  None
############################
from collections import deque
def perm(lst, n):
    if n == 0:
        return [["$"]]
    if n == 1:
        return [[lst[0], "$"]]
    if len(lst) <= 1:
        return [lst]
    perms = []
    for i in range(len(lst)):
        curr = [lst[i]]
        next = lst[:i] + lst[i+1:]
        for j in perm(next, n):
            this = curr+j
            if len(this) == n:
                this += ["$"]
            perms.append(this)
    return perms
    
def escape(grid):
    h, w = len(grid), len(grid[0])
    letters = []
    positions = {}
    for r in range(h):
        for c in range(w):
            if grid[r][c] == "@":
                positions[grid[r][c]] = (c, r)
            elif grid[r][c].isalpha() and grid[r][c].islower():
                letters.append(grid[r][c])
                positions[grid[r][c]] = (c, r)
    perms = perm(letters, len(letters))
    def getPath(s, f, keys):
        keys = set(keys)
        s = positions[s]
        visited = {s}
        bfs = deque([[s]])
        while bfs:
            sofar = bfs.popleft()
            col, row = sofar[-1]
            for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nr = row+x
                nc = col+y
                if nr in range(h) and nc in range(w) and grid[nr][nc] != "#" and (nc, nr) not in visited:
                    if grid[nr][nc] == f:
                        if f == "$":
                            return sofar+[(nc, nr)]
                        return sofar
                    elif grid[nr][nc] == "." or grid[nr][nc] == "$":
                        bfs.append(sofar+[(nc, nr)])
                        visited.add((nc, nr))
                    else:
                        if grid[nr][nc].lower() in keys:
                            bfs.append(sofar+[(nc, nr)])
                            visited.add((nc, nr))
        return None
    paths = {}
    def bfsMem(s, f, keys, left, sofar, ans):
        if (s, f, keys) not in paths:
            paths[(s, f, keys)] = getPath(s, f, keys)
        curr = paths[(s, f, keys)]
        if not curr:
            return (10**9, None)
        sofar += curr
        ans += len(curr)
        if not left:
            return (ans, sofar)
        return bfsMem(f, left[0], "".join(sorted(keys+f)), left[1:], sofar, ans)
    res = (10**9, None)
    for p in perms:
        curr = bfsMem("@", p[0], "@", p[1:], [], 0)
        res = min(res, curr)
    return res[1] if res[0] != 10**9 else None
  ###############################
from collections import deque, defaultdict
def perm(lst, n):
    if n == 0:
        return [["$"]]
    if n == 1:
        return [[lst[0], "$"]]
    if len(lst) <= 1:
        return [lst]
    perms = []
    for i in range(len(lst)):
        curr = [lst[i]]
        next = lst[:i] + lst[i+1:]
        for j in perm(next, n):
            this = curr+j
            if len(this) == n:
                this += ["$"]
            perms.append(this)
    return perms
    
def escape(grid):
    h, w = len(grid), len(grid[0])
    letters = []
    positions = {}
    for r in range(h):
        for c in range(w):
            if grid[r][c] == "@":
                positions[grid[r][c]] = (c, r)
            elif grid[r][c].isalpha() and grid[r][c].islower():
                letters.append(grid[r][c])
                positions[grid[r][c]] = (c, r)
    for i in grid:
        print(i, flush=True)
    perms = perm(letters, len(letters))
    paths = {}
    def getPath(s, f, keys):
        keys = set(keys)
        s = positions[s]
        visited = {s}
        bfs = deque([[s]])
        while bfs:
            sofar = bfs.popleft()
            col, row = sofar[-1]
            for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nr = row+x
                nc = col+y
                if nr in range(h) and nc in range(w) and grid[nr][nc] != "#" and (nc, nr) not in visited:
                    if grid[nr][nc] == f:
                        if f == "$":
                            return sofar+[(nc, nr)]
                        return sofar
                    elif grid[nr][nc] == "." or grid[nr][nc] == "$":
                        bfs.append(sofar+[(nc, nr)])
                        visited.add((nc, nr))
                    else:
                        if grid[nr][nc].lower() in keys:
                            bfs.append(sofar+[(nc, nr)])
                            visited.add((nc, nr))
        return None
    def bfsMem(s, f, keys, left, sofar, ans):
        if (s, f, keys) not in paths:
            paths[(s, f, keys)] = getPath(s, f, keys)
        curr = paths[(s, f, keys)]
        if not curr:
            return (10**9, None)
        sofar += curr
        ans += len(curr)
        if not left:
            return (ans, sofar)
        return bfsMem(f, left[0], "".join(sorted(keys+f)), left[1:], sofar, ans)
    listo = [bfsMem("@", x[0], "@", x[1:], [], 0) for x in perms]
    res = min(listo)
    return res[1] if res[0] != 10**9 else None
#####################
import string


def escape(grid):
    directs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    doors = {c for c in string.ascii_uppercase}
    keys = {c for c in string.ascii_lowercase}
    doors_keys = {string.ascii_uppercase[i]: string.ascii_lowercase[i] for i in range(26)}

    def trace(pos):
        res = []
        while pos[0] != (-1, -1):
            res.append((pos[1], pos[0]))
            pos = parent[pos]
        return res[::-1]

    m, n = len(grid), len(grid[0])
    a = [[grid[i][j] for j in range(n)] for i in range(m)]
    source, target, allKeys = None, None, []
    for i in range(m):
        for j in range(n):
            if a[i][j] == '@':
                source = (i, j)
            elif a[i][j] == '$':
                target = (i, j)
            elif a[i][j] in keys:
                allKeys.append(a[i][j])
    allKeys = ''.join(sorted(allKeys))
    parent = {(source[0], source[1], ''): ((-1, -1), '')}
    q = [(source[0], source[1], '')]
    visited = {(source[0], source[1], '')}
    while q:
        newQ = []
        for p in q:
            x, y, k = p
            cur_key = {c for c in k}
            if (x, y) == target and k == allKeys:
                return trace((x, y, k))
            for dx, dy in directs:
                i, j = x + dx, y + dy
                if 0 <= i < m and 0 <= j < n and a[i][j] != '#':
                    if a[i][j] in keys:
                        newK = ''.join(sorted(cur_key.union(a[i][j])))
                        if (i, j, newK) not in visited:
                            visited.add((i, j, newK))
                            newQ.append((i, j, newK))
                            parent[(i, j, newK)] = p
                    elif a[i][j] in doors:
                        if doors_keys[a[i][j]] in cur_key and (i, j, k) not in visited:
                            visited.add((i, j, k))
                            newQ.append((i, j, k))
                            parent[(i, j, k)] = p
                    else:
                        if (i, j, k) not in visited:
                            visited.add((i, j, k))
                            newQ.append((i, j, k))
                            parent[(i, j, k)] = p
        q = newQ

    return None
###############################
import string


def escape(grid):
    directs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    doors = {c for c in string.ascii_uppercase}
    keys = {c for c in string.ascii_lowercase}
    doors_keys = {string.ascii_uppercase[i]: string.ascii_lowercase[i] for i in range(26)}

    def trace(pos):
        res = []
        while pos[0] != (-1, -1):
            res.append(pos[0])
            pos = parent[pos]
        return [(y, x) for (x, y) in res[::-1]]
        # return res[::-1]

    m, n = len(grid), len(grid[0])
    a = [[grid[i][j] for j in range(n)] for i in range(m)]
    source, target, allKeys = None, None, []
    for i in range(m):
        for j in range(n):
            if a[i][j] == '@':
                source = (i, j)
            elif a[i][j] == '$':
                target = (i, j)
            elif a[i][j] in keys:
                allKeys.append(a[i][j])
    allKeys = ''.join(sorted(allKeys))
    parent = {(source, ''): ((-1, -1), '')}
    q = [(source, '')]
    visited = {(source, '')}
    while q:
        newQ = []
        for p in q:
            pos, k = p
            x, y = pos
            cur_key = {c for c in k}
            if (x, y) == target and k == allKeys:
                return trace(((x, y), k))
            for dx, dy in directs:
                i, j = x + dx, y + dy
                if 0 <= i < m and 0 <= j < n and a[i][j] != '#':
                    if a[i][j] in keys:
                        newK = ''.join(sorted(cur_key.union(a[i][j])))
                        if ((i, j), newK) not in visited:
                            visited.add(((i, j), newK))
                            newQ.append(((i, j), newK))
                            parent[((i, j), newK)] = p
                    elif a[i][j] in doors:
                        if doors_keys[a[i][j]] in cur_key and ((i, j), k) not in visited:
                            visited.add(((i, j), k))
                            newQ.append(((i, j), k))
                            parent[((i, j), k)] = p
                    else:
                        if ((i, j), k) not in visited:
                            visited.add(((i, j), k))
                            newQ.append(((i, j), k))
                            parent[((i, j), k)] = p
        q = newQ

    return None
##########################
import string


def escape(grid):
    directs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    doors = {c for c in string.ascii_uppercase}
    keys = {c for c in string.ascii_lowercase}
    doors_keys = {string.ascii_uppercase[i]: string.ascii_lowercase[i] for i in range(26)}

    def trace(pos):
        res = []
        while pos != (-1, -1):
            res.append(pos)
            pos = parent[pos].pop()
        return [(y, x) for (x, y) in res[::-1]]
        # return res[::-1]

    m, n = len(grid), len(grid[0])
    a = [[grid[i][j] for j in range(n)] for i in range(m)]
    source, target, allKeys = None, None, []
    for i in range(m):
        for j in range(n):
            if a[i][j] == '@':
                source = (i, j)
            elif a[i][j] == '$':
                target = (i, j)
            elif a[i][j] in keys:
                allKeys.append(a[i][j])
    allKeys = ''.join(sorted(allKeys))
    parent = {(i, j): [] for j in range(n) for i in range(m)}
    parent[source].append((-1, -1))
    q = [(source, '', [source])]
    visited = {(source, '')}
    while q:
        newQ = []
        for p in q:
            pos, k, path = p
            x, y = pos
            cur_key = {c for c in k}
            if (x, y) == target and k == allKeys:
                return [(y, x) for (x, y) in path]
            for dx, dy in directs:
                i, j = x + dx, y + dy
                if 0 <= i < m and 0 <= j < n and a[i][j] != '#':
                    if a[i][j] in keys:
                        newK = ''.join(sorted(cur_key.union(a[i][j])))
                        if ((i, j), newK) not in visited:
                            visited.add(((i, j), newK))
                            newQ.append(((i, j), newK, path + [(i, j)]))
                    elif a[i][j] in doors:
                        if doors_keys[a[i][j]] in cur_key and ((i, j), k) not in visited:
                            visited.add(((i, j), k))
                            newQ.append(((i, j), k, path + [(i, j)]))
                    else:
                        if ((i, j), k) not in visited:
                            visited.add(((i, j), k))
                            newQ.append(((i, j), k, path + [(i, j)]))
        q = newQ

    return None
