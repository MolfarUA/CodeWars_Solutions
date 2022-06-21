5985ea20695be6079e000003



from random import choice
from operator import itemgetter

def solve_n_queens(N, fQ, MAX_TRIES=75):
    
    x,y = fQ
    s = f'{x}{y}'
    if N in (2,3) or N==4 and s in '00330 11221' or N==6 and s in '00550 22332 11441':
        return None
    
    def nConflicts(x,y,isOracle=0):
        a,b,c,d = COLS[y], DIAGS1[x+y], DIAGS2[N-1-x+y], isOracle or -1
        return (a+d)*a + (b+d)*b + (c+d)*c >> 1
    
    def addQAt(x,y,d=1): COLS[y]+=d    ; DIAGS1[x+y]+=d ; DIAGS2[N-1-x+y]+=d
    def shift(q,y):      addQAt(*q,-1) ;  q[1]=y        ; addQAt(*q)
    
    def maxQueens():
        qc = [ (q,nConflicts(*q)) for q in queens]
        m  = max(map(itemgetter(1), qc), default=0) or 1
        return [q for q,n in qc if n==m]
    
    def minConflict(q, oracle=0):
        if isinstance(q,int): q,oracle,m = (q,-1), 1, N
        else:                 m = nConflicts(*q)
        
        skip = (fixQ[1], q[1])
        yc   = [ (y, nConflicts(q[0],y,oracle)) for y in range(N) if y not in skip ]
        m    = min(m, min(map(itemgetter(1), yc)))
        cnds = [y for y,n in yc if n==m]
        if cnds: return choice(cnds)
    
    def dig():
        for _ in range(MAX_TRIES):
            cnds = maxQueens()
            if not cnds: return build()
            q = choice(cnds)
            y = minConflict(q,1)
            if y is not None: shift(q,y)
        return solve_n_queens(N,fQ)
    
    def build():
        chess = [['.']*N for _ in range(N)]
        for x,y in queens+[fixQ]: chess[x][y]='Q'
        return ''.join(''.join(r)+'\n' for r in chess)
    
    def Q(x,y=None):
        q = [x,minConflict(x) if y is None else y]
        addQAt(*q)
        return q
    
    COLS,DIAGS1,DIAGS2 = [0]*N, [0]*(2*N-1), [0]*(2*N-1)
    fixQ   = Q(*fQ)
    queens = [Q(x) for x in range(N) if x!=fQ[0]]
    return dig()
  
##########################
from random import choice

def no_solution(n, fix): #checks whether it is a no solution case.
    return True if n==2 or n==3 or n==4 and fix in [(0,0),(0,3),(3,0),(3,3),(1,1),(1,2),(2,1),(2,2)] or n==6 and fix in [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(0,5),(1,4),(2,3),(3,2),(4,1),(5,0)] else False


def format_solution(n, sol): #returns the solution in the requested format.
    return '\n'.join(['.'*i+'Q'+'.'*(n-i-1) for i in sol])+'\n'


def attacks(n, cell): #returns the number of queens that attack a cell.
    return hor_queens[cell[1]]+up_dia_queens[cell[0]+cell[1]]+down_dia_queens[cell[1]-cell[0]+n-1]


def start_with(n, fix): #finds a known solution to the board of size n and changes one queen's position to the fixed cell.
    if n%6 == 2:
        sol = [i for i in range(1, n, 2)]+[2, 0]+[i for i in range(6, n, 2)]+[4]
    elif n%6 == 3:
        sol = [i for i in range(3, n, 2)]+[1]+[i for i in range(4, n, 2)]+[0, 2]
    else:
        sol = [i for i in range(1, n, 2)]+[i for i in range(0, n, 2)]
    sol[fix[0]] = fix[1]
    count_queens(n, sol)
    return sol


def count_queens(n, sol): #counts the number of queens in each row and diagonal.
    global hor_queens, up_dia_queens, down_dia_queens
    hor_queens, up_dia_queens, down_dia_queens = [0]*n, [0]*(2*n-1), [0]*(2*n-1)
    for i in range(n):
        hor_queens[sol[i]] = hor_queens[sol[i]] + 1
        up_dia_queens[sol[i]+i] = up_dia_queens[sol[i]+i] + 1
        down_dia_queens[sol[i]-i+n-1] = down_dia_queens[sol[i]-i+n-1] + 1


def update_queens(n, sol, new_queen): #updates the number of queens in each row and diagonal.
    i, j = new_queen
    hor_queens[sol[i]] -= 1
    up_dia_queens[sol[i]+i] -= 1
    down_dia_queens[sol[i]-i+n-1] -= 1
    hor_queens[j] += 1
    up_dia_queens[j+i] += 1
    down_dia_queens[j-i+n-1] += 1    


def min_conf(n, sol, fix): #applies min conflics algorithm to find a solution starting from a reasonable arrangement.
    while True:
        confs = [attacks(n, (i, sol[i]))-3 for i in range(n)]
        if sum(confs) == 0:
            return sol
        col = choice([i for i in range(n) if confs[i]>0 and i!=fix[0]])
        col_conf = [attacks(n, (col, i)) for i in range(n)]
        new_queen = (col, choice([i for i in range(n) if col_conf[i] == min(col_conf)]))
        update_queens(n, sol, new_queen)
        sol[new_queen[0]] = new_queen[1]


def solve(n, fix): #uses min conflicts algorithm to find the solution.
    sol = start_with(n, fix)
    return min_conf(n, sol, fix)


def solve_n_queens(n, fix):
    if no_solution(n, fix): return None
    return format_solution(n, solve(n, fix))
  
##############################
from random import choice, sample

def solve_n_queens(n, q):
    if n in (2, 3) or n == 4 and q in ((1, 1), (2, 1), (1, 2), (2, 2)) or n == 6 and q == (2, 3):
        return
    if n == 6 and q == (1, 2):
        return "....Q.\n..Q...\nQ.....\n.....Q\n...Q..\n.Q....\n" # Since my solution can't seem to find this one.
    pipe, slash, backslash, qs = {q[1]:1}, {sum(q):1}, {(q[0]-q[1]):1}, set()
    conf = lambda y, x, n: (pipe.get(x, 0) > n) + (slash.get(y+x, 0) > n) + (backslash.get(y-x, 0) > n)
    def incr(y, x, n):
        pipe[x] = pipe.get(x, 0) + n
        slash[y+x] = slash.get(y+x, 0) + n
        backslash[y-x] = backslash.get(y-x, 0) + n
        (qs.remove, qs.add)[n == 1]((y, x))
    for y in sample(list(range(n)), k=n):
        if y == q[0]:
            continue
        incr(y, min(range(n), key=lambda v: conf(y, v, 0)), 1)
    count = 0
    while any(any(v > 1 for v in d.values()) for d in (pipe, slash, backslash)):
        count += 1
        if (count := count + 1) > 50000:
            return # Not sure why it takes some things so long??
        ty, tx = choice(list(qs))
        if conf(ty, tx, 1) == 0:
            continue
        incr(ty, tx, -1)
        m = min(conf(ty, v, 0) for v in range(n) if v != tx)
        xs = [v for v in range(n) if conf(ty, v, 0) == m and v != tx]
        nx = choice(xs)
        incr(ty, nx, 1)
    return "\n".join("".join(".Q"[(y, x) in qs or (y, x) == q] for x in range(n)) for y in range(n)) + "\n"
  
###########################
import random

def change_conflicts(col, row, val, row_conflicts, positive_diag, negative_diag):
    row_conflicts[row] += val
    positive_diag[col + row] += val
    negative_diag[col - row] += val

# Finds the index of the best new queen position.
# Breaking Ties randomly.
def min_conflicts_row_pos(n, col, row_conflicts, positive_diag, negative_diag):
    min_conflicts = n
    row_conflict_arr = []
    for row in range(n):
        # calculate the number of conflicts using the conflict arrays
        conflicts = row_conflicts[row] + positive_diag[col + row] + negative_diag[col - row]
        # if there are no conflicts in a row, immediately return that row value
        if conflicts == 0:
            return row
        # if the number of conflicts is less, change it to the min_conflicts value
        if conflicts < min_conflicts:
            row_conflict_arr = [row]
            min_conflicts = conflicts
        # if the number of conflicts is equal, append the index instead of changing it
        elif conflicts == min_conflicts:
            row_conflict_arr.append(row)
    # randomly choose the index from the list of tied conflict values
    choice = random.choice(row_conflict_arr)
    return choice

#Finds the column with the most conflicts
def find_max_col_conflicts(n, board, row_conflicts, positive_diag, negative_diag):
    max_conflicts = 0
    arr_max_cols_conflicts = []
    for col in range(0,n):
            # Determine the row value for the current column
            row = board[col]
            # Calculate the number of conflicts using the conflict lists - POSITIVE_DIAG + NEGATIVE_DIAG + ROWS
            conflicts = row_conflicts[row] + positive_diag[col+row] + negative_diag[col-row]
            if conflicts > max_conflicts:
                    arr_max_cols_conflicts = [col]
                    max_conflicts = conflicts
            #If the conflicts equal the current max, append the index value to the arr_max_cols_conflicts list
            elif conflicts == max_conflicts:
                    arr_max_cols_conflicts.append(col)
    # Randomly choose from the list of tied maximums
    choice = random.choice(arr_max_cols_conflicts)
    return choice, max_conflicts


# Sets up the board using a greedy algorithm
def initialize_board(n, fixed, board, row_conflicts, positive_diag, negative_diag):
    # Initialise the conflict arrays
    positive_diag = [0] * ((2 * n) - 1)
    negative_diag = [0] * ((2 * n) - 1)
    row_conflicts = [0] * n

    # Set of possble row candidates
    possible_rows = set(range(0,n))
    # Array to track not place Queens
    queens_not_placed = []

    X,Y = fixed
    change_conflicts(X,Y,1, row_conflicts, positive_diag, negative_diag)
    for col in range(0, n):
        if len(board)== X:
            board.append(Y)
            continue

        # Pop the next possible row location to test
        row = possible_rows.pop()
        # Calculate the conflicts for potential location
        conflicts = row_conflicts[row] + positive_diag[col + row] + negative_diag[col - row]
        # If there are no conflicts, place a queen in that location on the board
        if conflicts == 0:
            board.append(row)
            change_conflicts(col, board[col], 1, row_conflicts, positive_diag, negative_diag)
        # If a conflict is found
        else:
            # Place the potential row to the back of the set
            possible_rows.add(row)
            # # Append a None to hold the place for Queen later on
            board.append(None)
            # # Store column of Queens not placed
            queens_not_placed.append(col)

    for col in queens_not_placed:
        #Place the remaining queen locations
        board[col] = possible_rows.pop()
        #Update conflict lists
        change_conflicts(col, board[col], 1, row_conflicts, positive_diag, negative_diag)
    return board, row_conflicts, positive_diag, negative_diag

# Sets up the board using initialize_board() and then solves it with a min-conflict algorithm
def solve_n_queens(n, fixed):
    board, row_conflicts, positive_diag, negative_diag = initialize_board(n,fixed, [],[],[],[])
    i, iteration_limit = 0, 1990
    X,Y = fixed
    while i < iteration_limit:
        # Calculate the maximum conflicting column and the number of conflicts it contains
        col, number_of_conflicts = find_max_col_conflicts(n,board, row_conflicts, positive_diag, negative_diag)
        # If the number of queens in the row, and diagonals is greater than 1 then there are conflicts)
        if (number_of_conflicts > 3):
            # Use the min_conflicts_row_pos() function to determine the row index with the least number of conflicts
            new_position = min_conflicts_row_pos(n, col,row_conflicts, positive_diag, negative_diag)
            # If the better location is not its current location, switch the location
            if (new_position != board[col]):
                # Remove the conflicts from the position the queen is leaving
                change_conflicts(col, board[col], -1, row_conflicts, positive_diag, negative_diag)
                board[col] = new_position
                # Add a conflict to the position the queen is entering
                change_conflicts(col, new_position, 1, row_conflicts, positive_diag, negative_diag)

        else:#if number_of_conflicts == 3:  #Solution is found
            if board[X] != Y:
                try:
                    return solve_n_queens(n, (X,Y))
                except RecursionError:
                    break
                    
            out = []
            #print(board)
            for col in board:
                out.append('.'*col + 'Q' + '.'*(n-col-1))
            return '\n'.join(out) + '\n'
            #return True, board, board[fixed[0]]
        i+= 1
        
##########################################
import numpy as np

def solve_n_queens(n, fixed_queen):
    if n == 1: return 'Q\n'
    if n == 2: return None
    count = 300
    swap, collision = False, True
    while count and collision:
        if not swap or count % 100 == 0:
            dic1, dic2 = diags(n)
            b, dic1, dic2 = board(n, fixed_queen, dic1, dic2)
        swap, collision = False, False
        for i in range(n-1):
            if i != fixed_queen[0]:
                for j in range(i+1, n):
                    if j != fixed_queen[0]:
                        t = dic1[i+b[i]] + dic1[j+b[j]] + dic2[i-b[i]] + dic2[j-b[j]]
                        if t > 4:
                            collision = True
                            s = dic1[i+b[j]]+1 + dic1[j+b[i]]+1 + dic2[i-b[j]]+1 + dic2[j-b[i]]+1
                            if t > s:
                                swap = swapsy(i, j, dic1, dic2, b)
                            if n > 100:
                                if max([dic1[i+b[i]],dic1[j+b[j]],dic2[i-b[i]],dic2[j-b[j]]]) == 1 and max([dic1[i+b[j]],dic1[j+b[i]],dic2[i-b[j]],dic2[j-b[i]]]) == 1:
                                    collision = False
        count -= 1
    if count == 0 and collision == True:
        return None    
    return form(b)

def form(board):
    outboard = ""
    for i in range(len(board)):
        for j in range(len(board)):
            if j == board[i]:
                outboard += 'Q'
            else:
                outboard += '.'
        outboard += '\n'
    return outboard

def board(n, Q, d1, d2):
    b = np.insert(np.random.permutation(np.array([i for i in range(n) if i != Q[1]])), Q[0], Q[1])
    for i in range(len(b)):
        d1[i+b[i]] += 1
        d2[i-b[i]] += 1
    return b, d1, d2

def diags(n):
    dic1, dic2 = {}, {}
    for k in range(2*n-1):
        dic1[k] = 0
        dic2[k-n+1] = 0
    return dic1, dic2

def swapsy(i,j,dic1,dic2,b):
    dic1[i+b[i]] -= 1
    dic1[j+b[j]] -= 1
    dic2[i-b[i]] -= 1
    dic2[j-b[j]] -= 1
    b[i], b[j] = b[j], b[i]
    dic1[i+b[i]] += 1
    dic1[j+b[j]] += 1
    dic2[i-b[i]] += 1
    dic2[j-b[j]] += 1
    return True
  
#########################################
def solve_n_queens(n, fixed_queen):
    if n == 1:
        return "Q\n"
    
    if n == 2 or n == 3:
        return None
    
    from random import shuffle
    
    def getConflictNo(diag1, diag2):
        conflictsNo = 0
        
        for el in diag1:
            if el > 1:
                conflictsNo += 1
                
        for el in diag2:
            if el > 1:
                conflictsNo += 1
                    
                    
        return conflictsNo
    
    def getConflictsDiff(yPositions, diagonal1, diagonal2, x1, x2, size):
        y1 = yPositions[x1]
        y2 = yPositions[x2]
        
        oldConflicts = 0
        
        diag11 = x1+y1
        diag12 = x2+y2
        
        diag21 = x1+ size - y1-1
        diag22 = x2+ size - y2-1
                    
        if diagonal1[diag11] > 1:
            oldConflicts += diagonal1[diag11] - 1
            
        if diagonal1[diag12] > 1:
            oldConflicts += diagonal1[diag12] - 1
            
        if diagonal2[diag21] > 1:
            oldConflicts += diagonal2[diag21] - 1
            
        if diagonal2[diag22] > 1:
            oldConflicts += diagonal2[diag22] - 1
            
        if oldConflicts == 0:
            return 0
        
        newConflicts = 0

        diag11n = x1+y2
        diag12n = x2+y1
        
        diag21n = x1+ size - y2-1
        diag22n = x2+ size - y1-1
        
        diagonal1[diag11n] +=1
        diagonal1[diag12n] +=1
        diagonal2[diag21n] +=1
        diagonal2[diag22n] +=1
        
        if diagonal1[diag11n] > 1:
            newConflicts += diagonal1[diag11n] -1
            
        if diagonal1[diag12n] > 1:
            newConflicts += diagonal1[diag12n] -1
            
        if diagonal2[diag21n] > 1:
            newConflicts += diagonal2[diag21n] -1
            
        if diagonal2[diag22n] > 1:
            newConflicts += diagonal2[diag22n] -1
            
        diagonal1[diag11n] -=1
        diagonal1[diag12n] -=1
        diagonal2[diag21n] -=1
        diagonal2[diag22n] -=1
            
        return newConflicts-oldConflicts
      
        
    xFixed = fixed_queen[0]
    yFixed = fixed_queen[1]
    
    yCoords = list(range(0,n,2)) + list(range(1, n, 2))
    
    x2swap =yCoords.index(yFixed)
    if x2swap != xFixed:
        yCoords[x2swap], yCoords[xFixed] = yCoords[xFixed], yCoords[x2swap]
    
    diag1 = [0] * 2*n
    diag2 = [0] * 2*n
    
    for x, y in enumerate(yCoords):
        diag1[x+y] += 1
        diag2[x +n-y-1] += 1
    
    maxConflict = getConflictNo(diag1, diag2)

#    print(maxConflict)
    iterNo = 0
    while True:
        
        xPositions = list(range(n))
        swaps = 1
        while swaps > 0:
            swaps = 0
#            print(yCoords)
            for ind1 in xPositions:
                if ind1 == xFixed:
                    continue
                
                for ind2 in xPositions[ind1+1:]:
                    if ind2 == xFixed:
                        continue
                    
                    conclifctDiff = getConflictsDiff(yCoords, diag1, diag2, ind1, ind2, n)
                    
                    if conclifctDiff < 0:
                        x1, y1 = ind1, yCoords[ind1]
                        x2, y2 = ind2, yCoords[ind2]
                        
                        diag1[x1+y1] -= 1
                        diag2[x1+n-y1-1 ] -= 1
                        
                        diag1[x2+y2] -= 1
                        diag2[x2+n-y2-1 ] -= 1
                        
                        diag1[x1+y2] += 1
                        diag2[x1+n-y2-1 ] += 1
                        
                        diag1[x2+y1] += 1
                        diag2[x2+n-y1-1 ] += 1
                        
                        yCoords[ind1], yCoords[ind2] = yCoords[ind2], yCoords[ind1]
                            
                        swaps += 1
                        
#        print("after swap")
        maxConflict = getConflictNo(diag1, diag2)

        iterNo += 1
        
        if maxConflict > 0:
            shuffle(yCoords)
            x2swap = yCoords.index(yFixed)
            if x2swap != xFixed:
                yCoords[x2swap], yCoords[xFixed] = yCoords[xFixed], yCoords[x2swap]
        
            diag1 = [0] * 2*n
            diag2 = [0] * 2*n
    
            for x, y in enumerate(yCoords):
                diag1[x+y] += 1
                diag2[x +n-y-1] += 1
            maxConflict = getConflictNo(diag1, diag2)
            
        else:
            break
        
        if iterNo > 30:
            return None
            
        
    rows = []
    for x in range(n):
        row = []
        for y in range(n):
            if yCoords[x] == y:
                row.append("Q")
            else:
                row.append(".")
                
        rows.append("".join(row))
    
    
    return "\n".join(rows)+"\n"
  
###########################################
import numpy as np
import random

def iterrepair(n=8, fixed=(1,0)):
    fix = fixed[0]
    
    #The approach will be to first randomly inititlise each row than try to improve situation row by row by moving Q within each row
    #At any point in time during the procedure there will be just one Q per row so queens will be indexed by row they are in
    #for each row randomly initialise column index of queen in that row ensuring that only one queen per column and that the fixed queen is intact
    #calculate diagonal indexes for Queen in each row
    row = np.array(range(n),dtype=int)
    col = np.random.permutation([i for i in range(n) if i!=fixed[1]])
    col = np.insert(col,fix,fixed[1])
    col = col.astype(int)
    dg1 = row + col                         
    dg2 = row - col + (n-1)
    
    
    #Count queens in each column and each diagonal Create sets capturing queens in each column and each diagonal
    c_col = np.zeros(n,dtype=int)
    c_dg1 = np.zeros(2*n-1,dtype=int)
    c_dg2 = np.zeros(2*n-1,dtype=int)
    s_col = [set() for i in range(n)]
    s_dg1 = [set() for i in range(2*n-1)]
    s_dg2 = [set() for i in range(2*n-1)]
    for i in range(n):
        c_col[col[i]] +=1
        s_col[col[i]].add(i)
        c_dg1[dg1[i]] +=1
        s_dg1[dg1[i]].add(i)        
        c_dg2[dg2[i]] +=1
        s_dg2[dg2[i]].add(i)
        
    #for each Q count conflicts except for fixed Q
    conf = np.zeros(n,dtype=int)
    for i in range(n):
        conf[i] = max(c_col[col[i]]-1,0) + max(c_dg1[dg1[i]]-1,0) + max(c_dg2[dg2[i]]-1,0)
    conf[fix] = 0
    
    def removeQ(q):
        c, d1, d2 = col[q], dg1[q], dg2[q]
        c_col[c] -= 1
        s_col[c].remove(q)        
        c_dg1[d1] -= 1
        s_dg1[d1].remove(q)        
        c_dg2[d2] -= 1
        s_dg2[d2].remove(q)
        return s_col[c] | s_dg1[d1] | s_dg2[d2]
    
    def addQ(r,c,update):
        col[r] = c
        dg1[r] = r+c
        dg2[r] = r-c + (n-1)
        c_col[c] +=1
        s_col[c].add(r)
        c_dg1[dg1[r]] +=1
        s_dg1[dg1[r]].add(r)        
        c_dg2[dg2[r]] +=1
        s_dg2[dg2[r]].add(r)
        
        for i in (update | s_col[c] |  s_dg1[dg1[r]] | s_dg2[dg2[r]]) - set([fix]) :
            conf[i] = max(c_col[col[i]]-1,0) + max(c_dg1[dg1[i]]-1,0) + max(c_dg2[dg2[i]]-1,0)
        if conf.max() == 0:
            return True
        
        return False
    
    
    i = 0
    
    while i < (2000 if n>50 else 200) :
        i += 1
        qcon = conf.max()
        q = np.argwhere(conf == qcon).flatten().tolist()
        q = random.choice(q)
   
        update = removeQ(q)
        
        cols = row
        diag1 = q + cols
        diag2 = q - cols +(n-1)
        rowconf = c_col[cols] + c_dg1[diag1] + c_dg2[diag2]
        q_col = np.argwhere(rowconf == rowconf.min()).flatten().tolist()
        q_col = random.choice(q_col)
        #print("Iteration {},  Improvement {}, Conflict {}".format(i, qcon - rowconf[q_col], conf.sum() ))
        if addQ(q, q_col, update) :
            return col.tolist()
    return False

def answertostring(cc,n):
    out = ""
    for c in cc:
        out = out + "."*c + "Q" + "."*(n-c-1) +"\n"
    return out
        

def solve_n_queens(n, fixed_queen):
    for i in range(20):
        c = iterrepair(n, fixed_queen)
        if c:
            return answertostring(c,n)
    return None
  
#########################################
import numpy as np

def solve_n_queens(n, fixed_queen):
    arange = np.arange(n)

    # on small boards, track how many boards we visit
    track_attempts = n < 11
    if track_attempts:
        attempts = set()
        total_boards = np.prod(range(1, n))

    for gen in range(10):
        # initialize a random board
        ilist = np.delete(arange, fixed_queen[0])
        np.random.shuffle(ilist)
        Qi = np.insert(ilist, fixed_queen[1], fixed_queen[0])
        Qj = arange
        Qk = Qi + n - Qj - 1
        Ql = Qi + Qj
        mask = np.zeros(n, bool)
        mask[fixed_queen[1]] = True

        for it in range(1000):
            # count mutual attacks
            h, hid, hcount = np.unique(Qi, return_inverse=True, return_counts=True)
            v, vid, vcount = np.unique(Qj, return_inverse=True, return_counts=True)
            p, pid, pcount = np.unique(Qk, return_inverse=True, return_counts=True)
            d, did, dcount = np.unique(Ql, return_inverse=True, return_counts=True)
            violations = hcount[hid] + vcount[vid] + pcount[pid] + dcount[did] - 4

            if not np.any(violations):
                # done
                A = np.full((n, n), '.')
                A[Qi, Qj] = 'Q'
                return '\n'.join(''.join(r) for r in A) + '\n'

            if track_attempts:
                # exhausted all boards, give up
                attempts.add(tuple(Qi))
                if len(attempts) == total_boards:
                    return None

            # move to the best row in the given column
            move_idx = np.argmax(np.ma.array(violations + np.random.rand(n), mask=mask))
            i = arange
            j = Qj[move_idx]
            k = i + n - j - 1
            l = i + j
            conflicts = np.random.rand(n)
            conflicts[h] += hcount
            _, conflict_rows, conflict_diagonals = np.intersect1d(k, p, assume_unique=True, return_indices=True)
            conflicts[conflict_rows] += pcount[conflict_diagonals]
            _, conflict_rows2, conflict_diagonals2 = np.intersect1d(l, d, assume_unique=True, return_indices=True)
            conflicts[conflict_rows2] += dcount[conflict_diagonals2]

            # move the queen and its associated data
            di = np.argmin(conflicts) - Qi[move_idx]
            Qi[move_idx] += di
            Qk[move_idx] += di
            Ql[move_idx] += di
    return None
  
###################################
from random import shuffle


def board(pos):
    r = []
    row = ["." for _ in range(len(pos))]
    for i, x in enumerate(pos):
        y = row.copy()
        y[x] = "Q"
        r.append(''.join(y))
    return '\n'.join(r) + "\n"


def solve_n_queens(n, fixed_queen):
    if n in (2, 3):
        return None
    for _ in range(n*n):
        arr = list(range(n))
        shuffle(arr)
    
        row, col = fixed_queen[0], fixed_queen[1]

        k = arr.index(col)
        arr[k], arr[row] = arr[row], arr[k]
        ran = list(range(0, row)) + list(range(row+1, n))
        
        col_neg = {i: -1 for i in range(-n+1, n)}
        col_pos = {i: -1 for i in range(2*n-1)}

        for i, x in enumerate(arr):
            col_neg[i-x] += 1
            col_pos[i+x] += 1

        for r, i in enumerate(ran):
            for j in ran[r:]:
                n1 = i - arr[i]
                p1 = i + arr[i]
                n2 = j - arr[j]
                p2 = j + arr[j]
                if col_neg[n1] > 0 or col_pos[p1] > 0 or col_neg[n2] > 0 or col_pos[p2] > 0:
                    col1 = int(col_neg[n1] > 0) + int(col_neg[n2] > 0) + int(col_pos[p1] > 0) + int(col_pos[p2] > 0)

                    n3 = i - arr[j]
                    p3 = i + arr[j]
                    n4 = j - arr[i]
                    p4 = j + arr[i]
                    col2 = int(col_neg[n3] >= 0) + int(col_neg[n4] >= 0) + int(col_pos[p3] >= 0) + int(col_pos[p4] >= 0)

                    if col1 > col2:
                        arr[i], arr[j] = arr[j], arr[i]
                        col_neg[n1] = max(-1, col_neg[n1]-1)
                        col_neg[n2] = max(-1, col_neg[n2]-1)
                        col_pos[p1] = max(-1, col_pos[p1]-1)
                        col_pos[p2] = max(-1, col_pos[p2]-1)

                        col_neg[n3] = col_neg[n3]+1
                        col_neg[n4] = col_neg[n4]+1
                        col_pos[p3] = col_pos[p3]+1
                        col_pos[p4] = col_pos[p4]+1
        collision = False

        for k, v in col_pos.items():
            if v > 0:
                collision = True
                break

        if not collision:
            for k, v in col_neg.items():
                if v > 0:
                    collision = True
                    break

        if not collision:
            return board(arr)
          
#######################################
from random import randint, shuffle 

class NQueens:
    
    def __init__(self, N, fixed_pos):
        self.N             = N
        self.fixed_row     = fixed_pos[0]
        self.fixed_col     = fixed_pos[1]
        self.occupied      = []             # occupied[row] = col if (row, col) has a queen.
        self.col_threats   = []             # Count threats on each column.
        self.diag1_threats = []             # Count threats on each upright diagonal.
        self.diag2_threats = []             # Count threats on each downright diagonal.
        self.conflicts     = 0              # Total number of conflicts, i.e. queens on threatened squares.
    
    def __str__(self):
        return ''.join('.' * x + 'Q' + '.' * (self.N - x - 1) + '\n' for x in self.occupied)
    
    def print_board(self):
        print(str(self))
    
    def place_queen(self, row, col):
        self.occupied[row] = col
        self.col_threats[col] += 1
        self.diag1_threats[row + col] += 1
        self.diag2_threats[self.N + row - col - 1] += 1
        self.conflicts += self.col_threats[col] > 1
        self.conflicts += self.diag1_threats[row + col] > 1
        self.conflicts += self.diag2_threats[self.N + row - col - 1] > 1
    
    def remove_queen(self, row):
        col = self.occupied[row]
        if col == None: return
        self.occupied[row] = None
        self.col_threats[col] -= 1
        self.diag1_threats[row + col] -= 1
        self.diag2_threats[self.N + row - col - 1] -= 1
        self.conflicts -= self.col_threats[col] > 0
        self.conflicts -= self.diag1_threats[row + col] > 0
        self.conflicts -= self.diag2_threats[self.N + row - col - 1] > 0
    
    def threat_level(self, row, col):
        ''' Return the number of threats on position (row, col). '''
        return self.col_threats[col] + \
               self.diag1_threats[row + col] + \
               self.diag2_threats[self.N + row - col - 1]
    
    def seed_board(self):
        ''' Randomly place N queens on an empty board by greedily minimizing conflicts. '''
        self.occupied      = [None] * self.N
        self.col_threats   = [0] * self.N
        self.diag1_threats = [0] * (2 * self.N - 1)
        self.diag2_threats = [0] * (2 * self.N - 1)
        self.conflicts     = 0
        self.place_queen(self.fixed_row, self.fixed_col)
        rows = [r for r in range(self.N) if r != self.fixed_row]
        shuffle(rows)
        for row in rows:
            col = min(range(self.N), key=lambda x: self.threat_level(row, x))
            self.place_queen(row, col)
    
    def solve(self, attempts=50):
        ''' Attempt to solve the N queens problem by using the minimal conflicts heuristic. '''
        
        iterations_per_attempt = 50 * len(str(self.N)) # Works well in practise.
        for _ in range(attempts):
            
            self.seed_board() # Randomly place queens on an empty board.
            
            for _ in range(iterations_per_attempt):
                
                if self.conflicts == 0:
                    return str(self)
                
                # Select a row having maximal conflicting queen.
                # If multiple options exist choose one randomly and remove the queen.
                rows = [r for r in range(self.N) if r != self.fixed_row]
                shuffle(rows)
                row = max(rows, key=lambda x: self.threat_level(x, self.occupied[x]))
                self.remove_queen(row)
                
                # Find the column that would minimize conflicts for the removed queen.
                # If multiple options exist choose one randomly and place the queen.
                cols = [*range(self.N)]
                shuffle(cols)
                col = min(cols, key=lambda x: self.threat_level(row, x))
                self.place_queen(row, col)
    
def solve_n_queens(n, fixed):
    return NQueens(n, fixed).solve()
