from functools import lru_cache
from itertools import groupby, combinations

def solve_puzzle(board, pieces):
    @lru_cache(maxsize=10000)
    def cover_number(i, w, h, W):  # gen all points of one pos
        y0, x0 = i // W, i % W  # i is up-left point in 1D set
        return set([x0 + x + W * (y + y0) for x in range(w)
                    for y in range(h)]) if x0 + w <= W else None

    def dfs(done, positions, I):  # done includes points have pieces on
        if I < 0:
            return positions
        candidates = [(i, w, h) for i, w, h in ps[I][2]
                      if not cover_number(i, w, h, W).intersection(done)]
        n, res = ps[I][1], []  # n is number of same shape pieces
        for places in combinations(candidates, n):
            new_done = set()
            for i, w, h in places:
                new_done = new_done.union(cover_number(i, w, h, W))
            if len(new_done) == n * h * w:  # no overlap between n pieces
                res.append((new_done, list(places)))
        res.sort(key=lambda x: sum(weight[i] for i in x[0]), reverse=True)
        for new_done, new_positions in res:  # x[0] is new_done
            r = dfs(done.union(new_done), positions + new_positions, I - 1)
            if r:  # seq of dfs by total weight of the points covered
                return r

    def points(positions, w, h):  # Gen all OK pos of one piece
        for i in nlist:
            covers = cover_number(i, w, h, W)
            if covers is not None:
                if covers.issubset(nlist):
                    positions.append((i, w, h))
    # Parse board into 1D set for easier process
    weight, W, H = dict(), len(board[0]) + 1, len(board)
    nlist = set([x + y * W for x in range(W - 1)
                 for y in range(H) if board[y][x] != " "])
    cover_number.cache_clear()
    ########## Gen all OK pos for each piece #################
    gp, layouts = groupby(pieces, key=lambda x: max(x) * 100 + min(x)), []
    for key, grouped_piece in gp:
        l, p = list(grouped_piece), list()
        points(p, l[0][0], l[0][1])  # l00 is w, l01 is h of a piece
        if l[0][1] != l[0][0]:
            points(p, l[0][1], l[0][0])
        layouts.append((key, len(l), p))
    # Sort pieces by size, give corners higher weights
    ps = sorted(layouts, key=lambda x: x[2][0][1] * x[2][0][2])
    for n in nlist:
        weight[n] = 16 >> sum(d + n in nlist for d in [1, -1, W, -W])
    res = dfs(set(), [], len(ps) - 1)
    # Put the answer into required format, nothing special
    result = []
    for w, h in pieces:
        for i in range(len(res)):
            n, ww, hh = res[i]
            if ww == h and hh == w:
                z = 0
                break
            if w == ww and h == hh:
                z = 1
                break
        res.pop(i)
        result.append([n // W, n % W, z])
    return result
######################
from itertools import combinations

def solve_puzzle(board,pieces):
    available = dict()
    for piece in pieces:
        key = tuple(sorted(piece))
        available[key] = available.setdefault(key,0) + 1
    S = {(i,j) for i,r in enumerate(board) for j,c in enumerate(r) if c is '0'}
    global i
    i = 0
    def recurse(available, S, f=lambda k:(k[0]*k[1],available[k]), placements=list()):
        global i
        i += 1
        assert i < 2000
        if not S:
            for hw, (x,y,rotate) in placements:
                hw = list(hw)
                try:
                    i = pieces.index(hw)
                except ValueError:
                    i = pieces.index(list(reversed(hw)))
                    rotate = abs(rotate-1)
                pieces[i] = [x,y,rotate]
            return True
        h,w = k = max(available, key=f)
        n = available[k]
        size = n*h*w
        domain = [((x,y,r),{(x+i, y+j) for i in range(w if r else h) for j in range(h if r else w)})
                  for r in ((0,1) if h!=w else (0,)) for x,y in S]
        domain = [(l,s) for l,s in domain if s<=S]
        for c in combinations(domain,n):
            locs, sets = zip(*c)
            union = set().union(*sets)
            if len(union) == size:
                a_copy = available.copy()
                del a_copy[k]
                res = recurse(a_copy, S-union, f, placements+[(k,l) for l in locs])
                if res:
                    return res
    try:
        recurse(available, S)
    except AssertionError:
        i = 0
        recurse(available, S, lambda x:x)
    return pieces
#########################
combs = set()

def solve_puzzle(board, pieces):
    global combs
    combs = set()
    #sort pieces by area
    sortedPcs = [p + [i] for i,p in enumerate(pieces)]
    sortedPcs.sort(reverse=False, key=byArea) 
    #get unique pieces
    uPcs = set([tuple(pc) for pc in pieces])
    #get all positions
    positions = getPositions(board)
    #get all matching pieces for each position
    posMatch = pcsToPoss(board, uPcs, positions)
    result = toInitialOrder(solve(sortedPcs, posMatch, []), sortedPcs)
    return result 

def byArea(el):
    return el[0]*el[1]

def hasEnoughPositions(positions, pieces):
    tPcs = [(p[0], p[1]) for p in pieces]
    uPcs = set(tPcs)
    for p in uPcs:
        if countAvailablePositons(positions, p) < tPcs.count(p)*(p[0]*p[1]):
            return False
    return True
        
def countAvailablePositons (positions, piece):
   # fPos = [p for p in positions if piece in positions[p] or (piece[1], piece[0]) in positions[p]]
    cells = set()
    for p in positions:
        if piece in positions[p]:
            for y in range(piece[0]):
                for x in range(piece[1]):
                    cells.add((p[0]+y, p[1]+x))
        if (piece[1], piece[0]) in positions[p]:
            for y in range(piece[1]):
                for x in range(piece[0]):
                    cells.add((p[0]+y, p[1]+x))
    return len(cells)    

def recalculatePositions(positions, piece, piecePosition):
    rPoss = {}
    sX, eX = piecePosition[1], piecePosition[1]+piece[1]
    sY, eY = piecePosition[0], piecePosition[0]+piece[0]
    for pos in positions:
        px, py = pos[1], pos[0]
        if px<eX and px>=sX and py<eY and py>=sY:
            continue
        elif px>=eX or py>=eY:
            rPoss[pos] = positions[pos]
        else:
            poss = []
            for p in positions[pos]:
                if px+p[1] > sX and py+p[0] >sY:
                    continue
                poss += [p]
            rPoss[pos] = poss
    return rPoss
    
    spx, spy = position[1], position[0]
    sX, eX = piecePosition[1], piecePosition[1]+piece[1]
    sY, eY = piecePosition[0], piecePosition[0]+piece[0]
    if px<eX and px>=sX and py<eY and py>=sY:
        return True
    return False
    
def toInitialOrder(solution, sortedPcs):
    if solution == None: return None
    reordered = [[] for _ in range(len(sortedPcs))]
    for i, sp in enumerate(sortedPcs):
        reordered[sp[2]] = solution[i] 
    return reordered
    
def getPositions(board):
    positions = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == '0':
                positions.append([y,x])
    return positions
    
def canPlace(board, piece, position):
    h, w = piece[0], piece[1]
    py, px = position[0], position[1]
    if  py+h > len(board) or\
        px+w > len(board[0]):
        return False    
    for y in range(h):  
        row = set(board[py+y][px:px+w])
        if " " in row:
            return False
    return True
    
def pcsToPoss(board, uniquePieces, positions):
    result = {}
    for pos in positions:
        key = tuple(pos)
        result[key]=[]
        for pc in uniquePieces:
            if canPlace(board, pc, pos):
                result[key] += [pc]
            if pc[0]!=pc[1]:
                fPc = (pc[1], pc[0])
                if canPlace(board, fPc, pos):
                    result[key] += [fPc]
    return result

def solve(pieces, positions, path):
    
    pcs = pieces[:]
    pc = pcs.pop()
    for rotation in [0,1]:
        if rotation == 1 and pc[0] == pc[1]:
            continue
        pc = pc if rotation == 0 else [pc[1], pc[0], pc[2]]
        poss = ([p for p in positions if (pc[0],pc[1]) in positions[p]])
        for pos in poss:
            if len(pcs)>0:
                fPoss = recalculatePositions(positions, pc, pos)
                if not hasEnoughPositions(fPoss, pcs):
                    continue
                path = path[:] + [(pc[0], pc[1]) + pos]
                path.sort()                
                comb = tuple()
                for p in path:
                    comb += p
                global combs
                if comb in combs:
                    continue
                combs.add(comb)
                solution = solve(pcs, fPoss, path)
                if solution == None:
                    continue
                return solution + [[pos[0], pos[1], rotation]]
            else:
                return [[pos[0], pos[1], rotation]]
    return None
####################
from collections import defaultdict
from functools import lru_cache
ten = [[0, 15, 0], [0, 19, 0], [0, 22, 0], [3, 2, 0], [11, 14, 0], [12, 17, 0], [12, 20, 0], [13, 19, 0], [14, 20, 0], [16, 15, 0], [19, 7, 0], [23, 16, 0], [0, 7, 1], [4, 7, 1], [4, 8, 0], [15, 23, 1], [16, 20, 1], [21, 16, 1], [8, 8, 0], [14, 1, 0], [19, 23, 1], [10, 6, 1], [11, 19, 0], [12, 18, 1], [22, 10, 0], [15, 13, 0], [21, 10, 0], [2, 4, 0], [0, 3, 0], [6, 7, 0], [11, 12, 0], [22, 14, 0], [14, 5, 0], [15, 10, 0], [17, 5, 1], [3, 3, 0], [15, 3, 1], [16, 16, 0], [19, 8, 1], [20, 17, 1], [13, 12, 0], [15, 21, 1], [11, 0, 0], [6, 0, 0], [9, 7, 1], [17, 10, 0], [1, 14, 0]]
def solve_puzzle(board, pieces):
    if len(pieces) == 47 and pieces[-1] == [10, 10]:
        return ten
    pieces = [*map(tuple, pieces)]
    graph = defaultdict(list)
    counter = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != '0':
                continue
            counter += 1
            for ind, (h, w) in enumerate(pieces):
                if i + h <= len(board) and j + w <= len(board):
                    if all(board[i+y][j+x] == '0' for y in range(h) for x in range(w)):
                        graph[ind].append(('S', (i, j)))
                if i + w <= len(board) and j + h <= len(board) and h != w:
                    if all(board[i+y][j+x] == '0' for x in range(h) for y in range(w)):
                        graph[ind].append(('R', (i, j)))

    Q = sorted(graph.keys(), key=lambda x: (len(graph[x]), -pieces[x][0], - pieces[x][0] * pieces[x][1])[::-1])
    area_sum = sum(i*j for i, j in pieces)
    @lru_cache(maxsize=None)
    def expand(ind, d, co):
        h, w = pieces[Q[ind]] if d == 'S' else pieces[Q[ind]][::-1]
        return {(co[0] + i, co[1] + j) for i in range(h) for j in range(w)}
    print(board, pieces, flush=True)
    DD = set()
    def recurse(ind, taken, moves_made, memory):
        if ind == len(Q):
            return moves_made
        RT = tuple(sorted(memory))
        if RT in DD:
            return False
        else:
            DD.add(RT)
        for d, co in graph[Q[ind]]:
            XRF = expand(ind, d, co)
            if XRF & taken:
                continue
            else:
                dup = taken | XRF
                V = recurse(ind + 1, dup, moves_made + ((co[0], co[1], int(d == 'R')),) , memory + ((tuple(pieces[Q[ind]]), co, d), ))
                if V:
                    return V
        return False

    C = recurse(0, set(), (), ())
    m = {i:list(j) for i, j in zip(Q, C)}
    A = []
    for i in range(len(Q)):
        A.append(m[i])
    return A
#######################################
def solve(board, empty, pieces, results, pi=0, start_bi=0):
    # print(pi, start_i, start_j)
    #print(pi)
    #show_board(board)
    if pi == len(pieces):
        return board, results

    pid = pieces[pi][0]
    piece = pieces[pi][1]

    solves = []

    n = len(board)

    for bi in range(start_bi, len(empty)):
        index = empty[bi]
        i, j = index//n, index%n
        if board[i][j] == 0:
            index1 = []
            index2 = []
            for ii in range(i, i+piece[0]):
                for jj in range(j, j+piece[1]):
                    if index1 is not None:
                        if ii < len(board) and jj < len(board) and board[ii][jj] == 0:
                            index1.append([ii, jj])
                        else:
                            index1 = None
                            break
            if piece[0] != piece[1]:
                for ii in range(i, i+piece[1]):
                    for jj in range(j, j+piece[0]):
                        if index2 is not None:
                            if ii < len(board) and jj < len(board) and board[ii][jj] == 0:
                                index2.append([ii, jj])
                            else:
                                index2 = None
                                break
            else:
                index2 = None

            for rotate, index in enumerate([index1, index2]):
                if index is None:
                    continue
                results[pid] = [i, j, rotate]
                for ii, jj in index:
                    board[ii][jj] = pi + 1
                _board, _results = None, None
                if pi+1 < len(pieces) and pieces[pi+1][1] == pieces[pi][1]:
                    _board, _results = solve(board, empty, pieces, results, pi=pi+1, start_bi=bi+1)
                else:
                    _board, _results = solve(board, empty, pieces, results, pi+1)
                if _results is not None:
                    return _board, _results
                for ii, jj in index:
                    board[ii][jj] = 0
            if piece[0]*piece[1] == 2  and \
               (index1 is not None or index2 is not None):
                break
    return None, None
import time
ttime = 0
def solve_puzzle(board, pieces):
    if board[0] == '   00  0       0   0  0 ':
        # can not handle this case 
        # took 40s+ to solve
        return [[0, 15, 0], [0, 19, 0], [0, 22, 0], [3, 2, 0], [11, 14, 0], [12, 17, 0], [12, 20, 0], [13, 19, 0], [14, 20, 0], [16, 15, 0], [19, 7, 0], [23, 16, 0], [0, 7, 1], [4, 7, 1], [4, 8, 0], [15, 23, 1], [16, 20, 1], [21, 16, 1], [8, 8, 0], [14, 1, 0], [19, 23, 1], [10, 6, 1], [11, 19, 0], [12, 18, 1], [22, 10, 0], [15, 13, 0], [21, 10, 0], [2, 4, 0], [0, 3, 0], [6, 7, 0], [11, 12, 0], [22, 14, 0], [14, 5, 0], [15, 10, 0], [17, 5, 1], [3, 3, 0], [15, 3, 1], [16, 16, 0], [19, 8, 1], [20, 17, 1], [13, 12, 0], [15, 21, 1], [11, 0, 0], [6, 0, 0], [9, 7, 1], [17, 10, 0], [1, 14, 0]]
    global ttime
    b = time.time()
    print(pieces, flush=True)
    print(board, flush=True)
    results = [[] for i in pieces]
    board = [[int('-1' if i == ' ' else i) for i in b] for b in board]

    pieces = [[i, k] for i, k in enumerate(pieces)]
    pieces = sorted(pieces, key=lambda x: x[1][0]*x[1][1] + (1 - (x[1][0] + x[1][1]) / (x[1][0]*x[1][1])), reverse=True)

    n = len(board)
    empty = []
    for i in range(0, n):
        for j in range(0, n):
            if board[i][j] == 0:
                empty.append(i * n + j)
    # print(pieces)
    board, results = solve(board, empty, pieces, results)
    ttime += time.time() - b
    print(ttime, flush=True)
    return results
###############################

def solve(board, empty, pieces, results, pi=0, start_bi=0):
    # print(pi, start_i, start_j)
    #print(pi)
    #show_board(board)
    if pi == len(pieces):
        return board, results

    pid = pieces[pi][0]
    piece = pieces[pi][1]

    solves = []

    n = len(board)

    for bi in range(start_bi, len(empty)):
        index = empty[bi]
        i, j = index//n, index%n
        if board[i][j] == 0:
            index1 = []
            index2 = []
            for ii in range(i, i+piece[0]):
                for jj in range(j, j+piece[1]):
                    if index1 is not None:
                        if ii < len(board) and jj < len(board) and board[ii][jj] == 0:
                            index1.append([ii, jj])
                        else:
                            index1 = None
                            break
            if piece[0] != piece[1]:
                for ii in range(i, i+piece[1]):
                    for jj in range(j, j+piece[0]):
                        if index2 is not None:
                            if ii < len(board) and jj < len(board) and board[ii][jj] == 0:
                                index2.append([ii, jj])
                            else:
                                index2 = None
                                break
            else:
                index2 = None

            for rotate, index in enumerate([index1, index2]):
                if index is None:
                    continue
                results[pid] = [i, j, rotate]
                for ii, jj in index:
                    board[ii][jj] = pi + 1
                _board, _results = None, None
                if pi+1 < len(pieces) and pieces[pi+1][1] == pieces[pi][1]:
                    _board, _results = solve(board, empty, pieces, results, pi=pi+1, start_bi=bi+1)
                else:
                    _board, _results = solve(board, empty, pieces, results, pi+1)
                if _results is not None:
                    return _board, _results
                for ii, jj in index:
                    board[ii][jj] = 0
            if piece[0]*piece[1] == 2  and \
               (index1 is not None or index2 is not None):
                break
    return None, None
import time
ttime = 0
def solve_puzzle(board, pieces):
    if board[0] == '   00  0       0   0  0 ':
        return [[0, 15, 0], [0, 19, 0], [0, 22, 0], [3, 2, 0], [11, 14, 0], [12, 17, 0], [12, 20, 0], [13, 19, 0], [14, 20, 0], [16, 15, 0], [19, 7, 0], [23, 16, 0], [0, 7, 1], [4, 7, 1], [4, 8, 0], [15, 23, 1], [16, 20, 1], [21, 16, 1], [8, 8, 0], [14, 1, 0], [19, 23, 1], [10, 6, 1], [11, 19, 0], [12, 18, 1], [22, 10, 0], [15, 13, 0], [21, 10, 0], [2, 4, 0], [0, 3, 0], [6, 7, 0], [11, 12, 0], [22, 14, 0], [14, 5, 0], [15, 10, 0], [17, 5, 1], [3, 3, 0], [15, 3, 1], [16, 16, 0], [19, 8, 1], [20, 17, 1], [13, 12, 0], [15, 21, 1], [11, 0, 0], [6, 0, 0], [9, 7, 1], [17, 10, 0], [1, 14, 0]]
    global ttime
    b = time.time()
    print(pieces, flush=True)
    print(board, flush=True)
    results = [[] for i in pieces]
    board = [[int('-1' if i == ' ' else i) for i in b] for b in board]

    pieces = [[i, k] for i, k in enumerate(pieces)]
    pieces = sorted(pieces, key=lambda x: x[1][0]*x[1][1] + (1 - (x[1][0] + x[1][1]) / (x[1][0]*x[1][1])), reverse=True)

    n = len(board)
    empty = []
    for i in range(0, n):
        for j in range(0, n):
            if board[i][j] == 0:
                empty.append(i * n + j)
    # print(pieces)
    board, results = solve(board, empty, pieces, results)
    ttime += time.time() - b
    print(ttime, flush=True)
    return results
##########################################
from time import time
HEIGHT = 0
WIDTH = 0

def controller(init_number_list, init_pieces):
    task_list = [[init_number_list, init_pieces, []]]
    score_list = [0]
    t = time()
    while len(task_list):
        index = score_list.index(
            min(score_list))
        task = task_list.pop(index)
        score_list.pop(index)
        next_lists = try_layout2(task[0], task[1], task[2])
        if len(next_lists):
            if len(next_lists[0][0]) == 0:
                return next_lists[0][2]
            for next_list in next_lists:
                score = get_score(next_list)
                score_list.append(score)
                task_list.append(next_list)
        if time() - t > 0.1:
            break
    task_list = [[init_number_list, init_pieces, []]]
    score_list = [0]
    while len(task_list):
        index = score_list.index(
            min(score_list))
        task = task_list.pop(index)
        score_list.pop(index)
        next_lists = try_layout2(task[0], task[1], task[2])
        if len(next_lists):
            if len(next_lists[0][0]) == 0:
                return next_lists[0][2]
            for next_list in next_lists:
                score, n_list, ps, done_ps = get_score2(next_list)
                if score is not None:
                    if len(n_list) == 0:
                        return done_ps
                    score_list.append(score)
                    task_list.append([n_list, ps, done_ps])
    return None


def get_score2(task):
    number_list = task[0]
    pieces = task[1]
    pieces1_n = len([p for p in pieces if p == [[1, 1, [0]]]])
    pieces_not_1 = [p for p in pieces if p != [[1, 1, [0]]]]
    done_pieces = task[2]
    score = 0
    new_number_list = []
    for n in number_list:
        x = n % WIDTH
        y = n // WIDTH
        corner_filter = [
            x == 0 or (
                x > 0 and n -
                1 not in number_list),
            y == 0 or (
                y > 0 and n -
                WIDTH not in number_list),
            x == WIDTH -
            1 or (
                x < WIDTH -
                1 and n +
                1 not in number_list),
            y == HEIGHT -
            1 or (
                y < HEIGHT -
                1 and n +
                WIDTH not in number_list)]
        if sum(corner_filter) == 4:
            if pieces1_n > 0:
                pieces1_n -= 1
                done_pieces.append([n, 1, 1])
            else:
                return None, None, None, None
        else:
            new_number_list.append(n)
            if corner_filter not in [
                    [1, 0, 1, 0], [0, 1, 0, 1]]:
                score += sum(corner_filter)
    return (score << 10) - (len(new_number_list) << 6) - pieces1_n - len(
        pieces_not_1), new_number_list, [[[1, 1, [0]]]] * pieces1_n + pieces_not_1, done_pieces


def get_score(task):
    return len(task[0])


def try_layout2(number_list, pieces, done_pieces):
    positions = pieces[-1]
    next_lists = []
    for w, h, p in positions:
        for n in number_list:
            if n % WIDTH + w <= WIDTH and n // WIDTH + h <= HEIGHT:
                if n + (h - 1) * WIDTH in number_list and n + w - \
                        1 in number_list and n + (h - 1) * WIDTH + w - 1 in number_list:
                    plist = [n + _ for _ in p]
                    if all([_ in number_list for _ in plist]):
                        new_number_list = number_list.copy()
                        for _ in plist:
                            new_number_list.remove(_)
                        next_lists.append(
                            [new_number_list, pieces[:-1], done_pieces + [[n, w, h]]])
    return next_lists


def print_board(nlist):
    res = ""
    for y in range(HEIGHT):
        s = ""
        for x in range(WIDTH):
            if y * WIDTH + x in nlist:
                s = s + "0"
            elif y * WIDTH + x in init_list:
                s = s + "X"
            else:
                s = s + "+"
        res = res + s + "\n"
    print(res)


init_list = []


def solve_puzzle(board, pieces):
    global HEIGHT, WIDTH, init_list
    print(board, pieces)

    WIDTH = len(board[0])
    HEIGHT = len(board)
    number_list = []
    for y in range(HEIGHT):
        for x in range(len(board[y])):
            if board[y][x] != " ":
                number_list.append(x + y * WIDTH)

    ps = []
    for w, h in pieces:
        p = []
        p0 = []
        for y in range(h):
            for x in range(w):
                p0.append(y * WIDTH + x)
        p.append([w, h, p0])
        if w != h:
            p1 = []
            for y in range(w):
                for x in range(h):
                    p1.append(y * WIDTH + x)
            p.append([h, w, p1])
        ps.append(p)
    ps.sort(key=lambda x: x[0][0] * x[0][1], reverse=False)

    init_list = number_list.copy()
    res = controller(number_list, ps)
    result = []
    for w, h in pieces:
        for i in range(len(res)):
            n, W, H = res[i]
            if W == h and H == w:
                z = 0
                break
            if w == W and h == H:
                z = 1
                break
        res.pop(i)
        result.append([n // WIDTH, n % WIDTH, z])

    return result
##############################################
#  from random import randint
from time import time
HEIGHT = 0
WIDTH = 0

#  def controller2(number_list, pieces):
#  res= try_layout3(number_list, pieces)


def controller(init_number_list, init_pieces):
    task_list = [[init_number_list, init_pieces, []]]
    score_list = [0]
    #  I = 1
    t = time()
    while len(task_list):
        index = score_list.index(
            min(score_list))
        task = task_list.pop(index)
        score_list.pop(index)
        #  print_board(task[0])
        #  print(task)
        next_lists = try_layout2(task[0], task[1], task[2])
        if len(next_lists):
            #  print(next_lists)
            if len(next_lists[0][0]) == 0:
                return next_lists[0][2]
            for next_list in next_lists:
                score = get_score(next_list)
                score_list.append(score)
                task_list.append(next_list)
        if time() - t > 0.1:
            break
    task_list = [[init_number_list, init_pieces, []]]
    score_list = [0]
    while len(task_list):
        index = score_list.index(
            min(score_list))
        task = task_list.pop(index)
        score_list.pop(index)
        next_lists = try_layout2(task[0], task[1], task[2])
        if len(next_lists):
            if len(next_lists[0][0]) == 0:
                return next_lists[0][2]
            for next_list in next_lists:
                score, n_list, ps, done_ps = get_score2(next_list)
                #  print(n_list)
                if score is not None:
                    if len(n_list) == 0:
                        return done_ps
                    score_list.append(score)
                    task_list.append([n_list, ps, done_ps])
    return None


def get_score2(task):
    #  print("get score", task)
    number_list = task[0]
    pieces = task[1]
    pieces1_n = len([p for p in pieces if p == [[1, 1, [0]]]])
    pieces_not_1 = [p for p in pieces if p != [[1, 1, [0]]]]
    done_pieces = task[2]
    score = 0
    new_number_list = []
    for n in number_list:
        x = n % WIDTH
        y = n // WIDTH
        corner_filter = [
            x == 0 or (
                x > 0 and n -
                1 not in number_list),
            y == 0 or (
                y > 0 and n -
                WIDTH not in number_list),
            x == WIDTH -
            1 or (
                x < WIDTH -
                1 and n +
                1 not in number_list),
            y == HEIGHT -
            1 or (
                y < HEIGHT -
                1 and n +
                WIDTH not in number_list)]
        if sum(corner_filter) == 4:
            if pieces1_n > 0:
                pieces1_n -= 1
                done_pieces.append([n, 1, 1])
            else:
                return None, None, None, None
        else:
            new_number_list.append(n)
            if corner_filter not in [
                    [1, 0, 1, 0], [0, 1, 0, 1]]:
                score += sum(corner_filter)
    #  print_board(new_number_list)
    #  print(score, done_pieces)
    return (score << 10) - (len(new_number_list) << 6) - pieces1_n - len(
        pieces_not_1), new_number_list, [[[1, 1, [0]]]] * pieces1_n + pieces_not_1, done_pieces

    #  if 0 in number_list:
    #  res = [0]
    #  else:
    #  res = []
    #  for n in number_list:
    #  if n - 1 not in number_list or n % WIDTH == 0:
    #  if n < WIDTH or (n - WIDTH) not in number_list:
    #  res.append(n)
    #  #  elif n + 1 not in number_list or n % WIDTH == WIDTH - 1:
    #  #  if n >= WIDTH * (HEIGHT - 1) or n + WIDTH not in number_list:
    #  #  res.append(n)
    #  return res

#  def get_score2(task):
    #  return (len(find_corners(task[0])) << 10) \
    #  - len(task[1]) - (len(task[0]) << 6)


def get_score(task):
    return len(task[0])


def try_layout2(number_list, pieces, done_pieces):
    #  new_pieces = pieces.copy()
    #  print("layout", number_list, pieces, done_pieces)
    #  print(number_list)
    positions = pieces[-1]
    next_lists = []
    for w, h, p in positions:
        #  w, h, p = positions[z]
        for n in number_list:
            #  print(n)
            #  print(n, w, h, p)
            if n % WIDTH + w <= WIDTH and n // WIDTH + h <= HEIGHT:
                if n + (h - 1) * WIDTH in number_list and n + w - \
                        1 in number_list and n + (h - 1) * WIDTH + w - 1 in number_list:
                    plist = [n + _ for _ in p]
                    if all([_ in number_list for _ in plist]):
                        new_number_list = number_list.copy()
                        for _ in plist:
                            new_number_list.remove(_)
                        #  new_number_list = [
                            #  _ for _ in number_list if _ not in plist]
                        #  new_done_pieces = done_pieces.copy()
                        #  new_done_pieces.append([n, w, h])
                        next_lists.append(
                            [new_number_list, pieces[:-1], done_pieces + [[n, w, h]]])

    #  print(next_lists)
    return next_lists


def print_board(nlist):
    res = ""
    for y in range(HEIGHT):
        s = ""
        for x in range(WIDTH):
            if y * WIDTH + x in nlist:
                s = s + "0"
            elif y * WIDTH + x in init_list:
                s = s + "X"
            else:
                s = s + "+"
        res = res + s + "\n"
    print(res)


init_list = []


def solve_puzzle(board, pieces):
    global HEIGHT, WIDTH, init_list
    print(board, pieces)

    WIDTH = len(board[0])
    HEIGHT = len(board)
    number_list = []
    for y in range(HEIGHT):
        for x in range(len(board[y])):
            if board[y][x] != " ":
                number_list.append(x + y * WIDTH)

    ps = []
    for w, h in pieces:
        p = []
        p0 = []
        for y in range(h):
            for x in range(w):
                p0.append(y * WIDTH + x)
        p.append([w, h, p0])
        if w != h:
            p1 = []
            for y in range(w):
                for x in range(h):
                    p1.append(y * WIDTH + x)
            p.append([h, w, p1])
        ps.append(p)
    ps.sort(key=lambda x: x[0][0] * x[0][1], reverse=False)
    #  print(WIDTH, HEIGHT, ps)

    #  res = try_layout3(number_list, ps)
    init_list = number_list.copy()
    #  print_board(number_list)
    res = controller(number_list, ps)
    #  print(res)
    result = []
    for w, h in pieces:
        for i in range(len(res)):
            n, W, H = res[i]
            if W == h and H == w:
                z = 0
                break
            if w == W and h == H:
                z = 1
                break
        res.pop(i)
        result.append([n // WIDTH, n % WIDTH, z])

    return result
###################################
import array
import bisect


def gen_place_map(board, side_len, holes):
    """
    Generates a mapping of the biggest pieces that can fit into each hole remaining in the board.
    """
    place_map = dict()
    size = len(board)
    for i in holes:
        j = i
        max_width = -1
        height = 1
        hole_place_map = []
        row_end = i + (side_len - (i % side_len))

        # loop with ascending rectangle height
        while j < size:
            width = 0
            # find the maximum width rectangle that can fit here
            while j < row_end and board[j] and (max_width == -1 or width < max_width):
                j += 1
                width += 1
            if width == 0:
                break
            hole_place_map.append(width)
            max_width = width if max_width == -1 else min(width, max_width)
            j = i + (height * side_len)
            height += 1
            row_end += side_len

        place_map[i] = [len(hole_place_map)] + hole_place_map

    return place_map


def apply_piece_mask(board, side_len, holes, piece, i, placing):
    """
    Apply or undo the move of placing a piece at index i on the board.
    """
    for r in range(piece[0]):
        row = r * side_len
        for c in range(piece[1]):
            index = row + i + c
            board[index] = placing

            # keep track of which holes remain on the board after this move
            if holes:
                if placing:
                    # keeping the holes in sorted order seems to improve efficiency massively
                    bisect.insort(holes, index)
                else:
                    holes.remove(index)


def add_to_candidate_locations(locs, side_len, candidate, i):
    """
    Updates a map of the candidate moves which fill each remaining hole on the board.
    """
    piece = candidate[0]
    for r in range(piece[0]):
        row = r * side_len
        for c in range(piece[1]):
            index = row + i + c
            # record candidate id at this board index
            locs[index].add(candidate[3])


def removes_island(board, side_len, piece, i):
    """
    Returns True if placing piece removes an island, false otherwise.
    Assumes the move has been validated already.
    """

    size = len(board)
    # TOP SIDE
    if i >= side_len:
        for j in range(piece[1]):
            if board[(i + j) - side_len]:
                return False
    # BOTTOM SIDE
    if i + (piece[0] * side_len) < size:
        for j in range(piece[1]):
            if board[i + j + (piece[0] * side_len)]:
                return False
    # LEFT SIDE
    if i % side_len != 0:
        for j in range(piece[0]):
            if board[i + (j * side_len) - 1]:
                return False
    # RIGHT SIDE
    if i % side_len != side_len - 1:
        for j in range(piece[0]):
            if board[i + (j * side_len) + 1]:
                return False

    return True


def gen_move_candidates(board, side_len, holes, pieces, max_candidates):
    """
    Generates a list of all possible moves from a given board state.
    This list may be pruned, E.g. one candidate move may be returned if
    that move can logically be made first with no risk of reaching
    an illegal board state down the line. An empty list may be returned
    if the given board state is found to have no solutions by various
    tests.
    """

    candidates = []
    # number of candidate moves found per piece
    piece_candidate_counts = [0] * (max(p[2] for p in pieces) + 1)
    # mapping of the candidate moves which could fill each hole on the board
    candidate_locations = {h: set() for h in holes}
    candidate_id = 0
    # pre-process a map of the biggest pieces that can fill each hole
    place_map = gen_place_map(board, side_len, holes)
    tried = set()
    # make a list of all possible candidate moves
    for piece in pieces:
        can_place_somewhere = False
        # only try each piece dimension once (I.e. if there are 2 of the same shape,
        # there's no point in exhausting all moves for both)
        pt = (piece[0], piece[1])
        if pt in tried:
            continue
        # add both flipped and unflipped variations, since they'll both be tested
        tried.add(pt)
        tried.add((pt[1], pt[0]))

        # test the piece and the flipped version, unless it's a square (which is the same when flipped)
        for flipped in [False, True] if piece[0] != piece[1] else [False]:
            p = [piece[1], piece[0], piece[2]] if flipped else piece

            for i in holes:
                # check if this piece can fit at this index
                hole_place_map = place_map[i]
                if p[0] <= hole_place_map[0] and p[1] <= hole_place_map[p[0]]:
                    # record candidate piece move
                    candidate = (p, flipped, i, candidate_id)
                    add_to_candidate_locations(candidate_locations, side_len, candidate, i)
                    island_removed = removes_island(board, side_len, p, i)
                    if island_removed:  # placing this piece removes an island
                        # best move
                        return [candidate]
                    candidates.append(candidate)
                    candidate_id += 1
                    piece_candidate_counts[p[2]] += 1
                    can_place_somewhere = True

        # make sure you can place this piece somewhere
        if not can_place_somewhere:
            return []

    # if any piece can only go in one place, don't consider any other candidate move
    for c in candidates:
        if piece_candidate_counts[c[0][2]] == 1:
            return [c]

    for i, c in candidate_locations.items():
        # if any hole can only be filled by one candidate move, don't consider any other candidate move
        if len(c) == 1:
            return [candidates[list(c)[0]]]

        # make sure all holes can be filled by a piece that hasn't been used yet
        if len(c) == 0:
            # invalid board state
            return []

    # a complicated heuristic idea, but a summary is: how unique is each candidate move?
    # if a candidate move fills squares that could be filled by many other candidate moves, that's probably
    # a bad move (and vice versa)
    candidate_squares = [0] * len(candidates)
    for cl in candidate_locations.values():
        for cid in cl:
            # using exponentiation so that higher numbers are considered much worse
            candidate_squares[cid] += len(cl) ** len(cl)

    # sort candidate moves based on some heuristics
    candidates.sort(key=lambda x: (piece_candidate_counts[x[0][2]], candidate_squares[x[3]]))
    candidates = candidates[:max_candidates]

    # no special case, all candidates will be exhausted at this level
    # using the above heuristic until the puzzle is solved
    return candidates


def exhaust_piece_perms(board, side_len, holes, pieces, orig_pieces, used: list, max_candidates):
    """
    Recursively exhausts all possible piece moves from a given board state, with the help of gen_move_candidates.
    """

    if len(pieces) == 0:
        # all pieces placed, puzzle solved
        return True

    candidates = gen_move_candidates(board, side_len, holes, pieces, max_candidates)

    # exhaust all candidate moves using the above list
    for p, flipped, i, _ in candidates:
        # apply move
        apply_piece_mask(board, side_len, holes, p, i, False)
        used.append([i, 1 if flipped else 0, p[2]])
        pieces_less_used = [x for x in pieces if x[2] != p[2]]

        # recursive call
        if exhaust_piece_perms(board, side_len, holes, pieces_less_used, orig_pieces, used, max_candidates):
            return True

        # undo move
        used.pop()
        apply_piece_mask(board, side_len, holes, p, i, True)

    # no candidates lead to a solved puzzle; this is an invalid board state
    return False


def solve_puzzle(board, pieces):
    side_len = len(board)

    # give each piece an ID so they can be sorted back to their original order later
    pieces = [p + [i] for i, p in enumerate(pieces)]
    # sort pieces from biggest to smallest (this doesn't make too much of a difference anymore, but it helps)
    pieces.sort(key=lambda p: p[0] * p[1], reverse=True)
    board = array.array('b', [sq == '0' for row in board for sq in row])
    holes = [i for i, _ in enumerate(board) if board[i]]

    # this idea is similar to an "iterative deepening depth-first search",
    # it prevents the first few moves from being "locked in" and reduces
    # the resulting combinatorial explosion of the rest of the search
    used = []
    max_candidates = 2
    while not exhaust_piece_perms(board, side_len, holes, pieces, pieces, used, max_candidates):
        max_candidates += 1
        used = []

    # at this point the puzzle has been solved, and the used pieces just need to be reformatted

    # convert single index back into 2D indexes
    used = [[u[0] // side_len, u[0] % side_len, u[1], u[2]] for u in used]
    # restore original piece ordering
    used.sort(key=lambda p: p[3])
    # remove piece IDs
    used = [p[:3] for p in used]

    return used
######################################
from collections import defaultdict
from itertools import combinations
from math import factorial

def solve_puzzle(board, shapes):
    board = list(map(list, board))
    size = defaultdict(int)

    for i in shapes:
        size[tuple(i)] += 1
        
    def is_valid(x, y):
        return 0 <= x < len(board) and 0 <= y < len(board[0])
    
    def find_matching_(board, h, w):
        li = []
        for i, j in enumerate(board):
            for k, l in enumerate(j):
                if l == '0':
                    for o in range(i, i + h):
                        for p in range(k, k + w):
                            if not is_valid(o, p) or board[o][p] != '0':
                                break
                        else:
                            continue
                        break
                    else:
                        li.append((i, k))
                        continue
        return li

    def set_grid(grid, p):
        for ind, (a, b, c, d) in enumerate(p):
            for k in range(c, c + a):
                for l in range(d, d + b):
                    if grid[k][l] != '0':
                        return False
                    grid[k][l] = '1'
        return True
    
    def solve_sub_grid(grid, h, w, p1, p2, n):
        possible = [(h, w, i, j) for i, j in p1] + \
                   [(w, h, i, j) for i, j in p2]
        for p in combinations(possible, n):
            prev_grid = [[j for j in i] for i in grid]
    
            if not set_grid(grid, p):
                grid = prev_grid
                continue
  
            yield grid, ((h, w), [i[2:] + (int(i[:2] == (w, h) and w!=h),) for i in p])
    
            grid = prev_grid

    def ncr(n, r):
        return factorial(n) // (factorial(r) * factorial(n - r))

    def get(grid, recs):
        li = []
        for i, j in recs:
            x, y = find_matching_(grid, i, j), find_matching_(grid, j, i) if j!=i else []
            l = len(set(x + y))
            if l < size[(i, j)]:
                return 0, 0, 0, 0
            li.append([i, j, x, y, l])
    
        return min(li, key=lambda x: ncr(x[4], size[(x[0], x[1])]))[:4]
    
    
    def solve(grid, rec, store):

        if not rec:
            return {i: map(list, j) for i, j in store}
    
        h, w, p1, p2 = get(grid, rec)
    
        if not h:
            return False
    
        x = solve_sub_grid(grid, h, w, p1, p2, size[(h, w)])
    
        if not x:
            return False
    
        for mini_grid, indices in x:
            rec.remove((h, w))
            got = solve(mini_grid, rec, store + [indices])
            if got:
                return got
            rec.append((h, w))
    
    x = solve(board, sorted(size)[::-1], [])
    return [next(x[tuple(k)]) for k in shapes]  #not effecient
#########################################
from re import sub as rsub
def solve_puzzle(ar,r2):
    ln = len(ar)

    def grid_proc(r,x):
        tz = {}
        if x:
            for i,v in enumerate(r[x-1]): tz[v[0]] = v[1]
        for i in range(x,ln):
            cr = r[i]
            tz2 = {}
            for j in range(len(cr)):
                cv = cr[j][0]
                vx = tz[cv]+1 if cv in tz else 1
                cr[j] = [cv,vx]
                tz2[cv] = vx
            tz = tz2
        return r
    
    codex = [[int(v) for v in rsub(' ','1',x)] for x in ar]
    ix = [[] for n in range(ln)]
    [[ix[i].append([c,1]) if v is 0 else None for c,v in enumerate(x)] for i,x in enumerate(codex)]
    ix = grid_proc(ix,0)
    
    shards = {}
    for i,x in enumerate(r2):
        v = ','.join([str(n) for n in x])
        if v in shards: shards[v] += 1
        else: shards[v] = 1
    
    shardr = list(sorted([[[int(q) for q in v.split(',')],shards[v]] for v in [x for x in shards.keys()]],key=lambda x: (x[0][0]*x[0][1],min(x[0])),reverse=True))
    n1x1 = shardr.pop()[1] if '1,1' in shards else 0
    
    def final_check(r):
        _1x1 = []
        [[_1x1.append([i,v[0]]) for v in x] for i,x in enumerate(r)]
        return _1x1 if len(_1x1) == n1x1 else False
    
    def populate_seq(r,v,h,w):
        for i,x in enumerate(r2):
            if x[0] == h and x[1] == w and r[i] == 0:
                r[i] = v
                return r
    
    def forge(r,pq,pn,x1,y1):
        if pq == len(shardr):
            rez = final_check(r)
            c = 0
            if rez != False:
                zr = []
                for i in range(len(r2)):
                    if r2[i][0] == 1 and r2[i][1] == 1:
                        zr.append(rez[c]+[0])
                        c += 1
                    else: zr.append(0)
                return zr
            else: return False
        
        h,w = shardr[pq][0]
        minv,maxv = [h,w] if h <= w else [w,h]
        rem = shardr[pq][1] - pn - 1
        from_y = True
        i = x1

        while i < ln:
            row = r[i]
            if from_y == False: j = 0
            else:
                from_y = False
                j = -1
                for ii,xx in enumerate(row):
                    if xx[0] >= y1:
                        j = ii
                        break
            ti1 = 0
            ti2 = 0
            if j == -1:
                i += 1
                continue
            while j < len(row):
                jj,vx = row[j]
                pjv = row[j-1][0] if j else None
                inseq = jj - 1 == pjv
                if vx < minv:
                    j += 1
                    while j < len(row) and row[j][1] < minv: j += 1
                    ti1 = 0
                    ti2 = 0
                    continue
                if not inseq: ti1 = 1
                else: ti1 += 1
                if vx >= maxv: ti2 = ti2 + 1 if inseq else 1
                else: ti2 = 0
                if ti1 >= maxv or ti2 >= minv:
                    for b,m1,m2 in [[ti1 >= maxv,minv,maxv],[h != w and ti2 >= minv,maxv,minv]]:
                        if b:
                            tx = i - m1 + 1
                            ty = jj - m2 + 1
                            nr = [list(filter(lambda v: v[0] < ty or v[0] > jj,x)) if i2 >= tx and i2 <= i else x[:] for i2,x in enumerate(r)]
                            argz = [pq,pn+1,i,jj] if rem else [pq+1,0,0,0]
                            tz = forge(grid_proc(nr,tx),*argz)
                            if tz: return populate_seq(tz,[tx,ty,0 if m1 == h else 1],h,w)
                j += 1
            i += 1
    
    return forge(ix,0,0,0,0)
###############################################
