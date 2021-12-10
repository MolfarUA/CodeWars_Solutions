N = 7
perms = {i:set() for i in range(0, N+1)}
for row in __import__('itertools').permutations(range(1,N+1), N):
    c, s = 0, 0
    for h in row:
        if h>c: c, s = h, s+1
    perms[0].add(row)
    perms[s].add(row)

def solve_puzzle (clues):
    rows = [perms[r]&{p[::-1] for p in perms[l]} for (r, l) in zip(clues[N*4-1:N*3-1:-1],clues[N:N*2])]
    cols = [perms[t]&{p[::-1] for p in perms[b]} for (t, b) in zip(clues[0:N],clues[N*3-1:N*2-1:-1])]
    
    for _ in range(N*N//2):
        for r_i in range(N):
            for c_i in range(N):
                common = {r[c_i] for r in rows[r_i]} & {c[r_i] for c in cols[c_i]}
                rows[r_i], cols[c_i] = [r for r in rows[r_i] if r[c_i] in common], [c for c in cols[c_i] if c[r_i] in common]
    
    for rows1 in __import__('itertools').product(*rows):
        if all(tuple(r[i] for r in rows1) in cols[i] for i in range(N)): return list(list(r) for r in rows1)
        
###################
from itertools import permutations, product


def solve_puzzle(clues, size=7):
    # rows - множество всех возможных перестановок длин небоскрёбов
    # от 1 до size включительно. rg - числовой ряд индексов.
    rows, rg = {*permutations(range(1, size + 1))}, range(size)
    # Подсказки для каждой из четырёх точек зрения: clue_up, clue_right,
    # clue_down, clue_left.
    cu, cr, cd, cl = [clues[i*size:(i + 1)*size][::1 - 2*(i > 1)]
                      for i in range(4)]
    # Словарь всех возможных перестановок, распределённых по значениям
    # подсказок для прямого и обратного порядков.
    forward, reverse = {r:set() for r in range(1, size + 1)}, \
                  {r:set() for r in range(1, size + 1)}
    forward[0] = reverse[0] = rows
    # Распределение.
    for row in rows:
        for order, dx in (forward, 1), (reverse, -1):
            visible = maximum = 0
            # Подсчёт видения.
            for dig in row[::dx]:
                if dig > maximum:
                    maximum = dig
                    visible += 1
                    if dig == size:
                        break
            order[visible] |= {row}
    # Варианты линий для горизонтального и вертикального представлений пазла.
    hor, ver = [None] * size, [None] * size
    for i in rg:
        # i-тая строка соответствует как левой, так и правой подсказке.
        hor[i] = forward[cl[i]] & reverse[cr[i]]
        # i-тая колонна соответствует как верхней, так и нижней подсказке.
        ver[i] = forward[cu[i]] & reverse[cd[i]]
    # check - общее количество вариантов для горизонтального и вертикального представлений.
    # memory - значение check на прошлой итерации цикла while.
    memory, check = -1, 0
    # Фильтрация по совместимости вариантов строк и колонн пазла.
    # check = 2*size <-> и в горизонтальном и в вертикальном представлениях
    # осталось по одному варианту на каждую из линий. check = memory <-> не
    # было и более не будет исключено ни одного варианта.
    while check != 2*size and check != memory:
        for i, j in product(rg, rg):
            common = {line[j] for line in hor[i]} & {line[i] for line in ver[j]}
            hor[i] = {line for line in hor[i] if line[j] in common}
            ver[j] = {line for line in ver[j] if line[i] in common}
        memory, check = check, sum(len(x) for x in hor + ver)
    # Перебор оставшихся вариантов решения проблемы.
    valid = {*range(1, size + 1)}
    for variant in product(*map(list, hor)):
        # Если каждый из столбцов варианта горизонтального представления
        # представляет собой множество чисел от 1 до size включительно.
        if all({variant[i][j] for i in rg} == valid for j in rg):
            # Проблема решена!
            return list(list(row) for row in variant)
          
####################
def solve_puzzle(clues):
    top = clues[0:7]
    right = clues[7:14]
    bottom = clues[14:21][::-1]
    left = clues[21:28][::-1]
    
    col_clues = [[top[i], bottom[i]] for i in range(0,7)]
    row_clues = [[left[i], right[i]] for i in range(0,7)]
    
    all_combinations = permute([1,2,3,4,5,6,7])
    
    classified = classify(all_combinations, row_clues, col_clues)
    
    rows = classified[0]
    cols = classified[1]
    
    attempt = 0
    while not is_every_row_unique(rows):
        if attempt > 20:
            rows = force_random_assumption(rows, cols)
            break
        
        find_overlaps(rows, cols)
        find_overlaps(cols, rows)
        attempt += 1
        
    print(rows)

    return [rows[i][0] for i in range(0,7)]


def is_every_row_unique(rows):
    for row in rows:
        if len(row) != 1: return False
    return True


def is_some_row_not_unique(rows):
    for row in rows:
        if len(row) > 1: return True
    return False

def permute(input):
    if len(input) == 1: return [input]
    
    result = []
    for i in range(0, len(input)):
        current = input[i]
        remaining = input[:i] + input[i+1:]
        permuted = permute(remaining)
        
        for j in range(0, len(permuted)):
            result.append([current] + permuted[j])
    return result


def classify(lines, row_clues, col_clues):
    row_candidates = []
    col_candidates = []
    
    for i in range(0,7):
        temp_row = []
        temp_col = []
        
        for j in range(0, len(lines)):
            is_valid_row = is_valid_line(lines[j], row_clues[i][0])
            is_valid_col = is_valid_line(lines[j], col_clues[i][0])
            is_valid_row_revers = is_valid_line(lines[j][::-1], row_clues[i][1])
            is_valid_col_revers = is_valid_line(lines[j][::-1], col_clues[i][1])
            
            if is_valid_row and is_valid_row_revers: temp_row.append(lines[j])
            if is_valid_col and is_valid_col_revers: temp_col.append(lines[j])
        
        row_candidates.append(temp_row)
        col_candidates.append(temp_col)
        
    return [row_candidates, col_candidates]


def is_valid_line(line, clue):
    if clue > 0: return count_visible(line) == clue
    return True


def count_visible(line):
    maximum = 0
    visible = 0
    
    for item in line:
        if item > maximum:
            visible += 1
            maximum = item
    
    return visible


def find_overlaps(rows, cols):
    for i in range(0,7):
        for j in range(0,7):
            overlaps = []
            new_col = []
            
            for k in range(0, len(rows[i])):
                overlaps.append(rows[i][k][j])
                
            for line in cols[j]:
                if line[i] in overlaps:
                    new_col.append(line)
                    
            cols[j] = new_col
            

def get_backup(assumptions):
    backup = []
    
    for i in range(0, 7):
        new_assumptions = []
        
        for j in range(0, len(assumptions[i])):
            new_assumption = []
            
            for k in range(0, len(assumptions[i][j])):
                new_assumption.append(assumptions[i][j][k])
                
            new_assumptions.append(new_assumption)
        
        backup.append(new_assumptions)
    
    return backup
    

def force_random_assumption(rows, cols):
    for i in range(0, 7):
        if len(rows[i]) > 1:
            for j in range(0, len(rows[i])):
                rows_backup = get_backup(rows)
                cols_backup = get_backup(cols)
                
                rows[i] = [rows[i][j]]
                while is_some_row_not_unique(rows):
                    find_overlaps(rows, cols)
                    find_overlaps(cols, rows)
                    
                if is_every_row_unique(rows): return rows
                
                rows = rows_backup
                cols = cols_backup
                
########################
import itertools, time
import numpy as np
n = 7
verbose = False
basics = False

def solve_puzzle(clues):
    t1 = time.time()
    d = {}  # clue_dictionary
    pos = np.zeros((n, n), set)  # combined lines and rows
    for i in range(n):
        for j in range(n):
            pos[i][j] = {1, 2, 3, 4, 5, 6, 7}
    if verbose:
        print('original pos = possibilities martix')
        print_pos(pos, clues)

    clues_per_line = [(clues[27], clues[7]),
                      (clues[26], clues[8]),
                      (clues[25], clues[9]),
                      (clues[24], clues[10]),
                      (clues[23], clues[11]),
                      (clues[22], clues[12]),
                      (clues[21], clues[13])]

    clues_per_row = [(clues[0], clues[20]),  # after transpose
                     (clues[1], clues[19]),
                     (clues[2], clues[18]),
                     (clues[3], clues[17]),
                     (clues[4], clues[16]),
                     (clues[5], clues[15]),
                     (clues[6], clues[14])]

    lines = itertools.permutations(range(1, n + 1))

    for line in lines:
        d[line] = (find_hint(line), find_hint(line[::-1]))

    step = 1
    while not is_done(pos):
        pos_old = pos.copy()

        print('step = ' + str(step))
        step += 1
        if step % 2 == 0:  # costly calculation doesn't need to happen each round
            pos = apply_hints(pos, clues, d, clues_per_line, clues_per_row, 'horizontal')
            pos = apply_hints(pos, clues, d, clues_per_line, clues_per_row, 'vertical')
        pos = logic_single_option_rows(pos)
        pos = logic_single_option_lines(pos)
        pos = logic_clean_selected_option_rows(pos)
        if step % 2 == 0:
            if ((pos_old - pos).any() == set()): #logical operations don't work
                success, pos = brute_force_ending(pos, clues, d, clues_per_line, clues_per_row)
                break

    if verbose:
        possibilities_on_board_naive(pos)
        possibilities_on_board_vectorized(pos, d)
    solution = list(list(x)[0] for x in pos.flatten())
    solution = np.array(solution).reshape(n, n)
    solution = solution.tolist()
    if verbose: print(type(solution))
    #print(solution)
    
    t2 = time.time()
    print('time')
    print(t2-t1)
    return solution

def brute_force_ending(pos, clues, d, clues_per_line, clues_per_row):
    #No solution found with logic. Continue with brute force, then apply logic.
    for i in range(n):
        for j in range(n):
            if len(pos[i][j])>1:
                #more than one possible value
                for val in list(pos[i][j]):
                    print_pos(pos, clues)
                    pos[i][j] = {val} #assign one option
                    success, solution = try_all_logic(pos.copy(), clues, d, clues_per_line, clues_per_row) #chose K and try all logic
                    if success: return True, solution


def try_all_logic(pos, clues, d, clues_per_line, clues_per_row):
    #try the logic format on a matrix
    #success, solution is the return type
    #success is bool

    if verbose: print_pos(pos,clues)
    #if set() in pos: return False, pos
    while not is_done(pos):
        if is_broken(pos): return False, pos #Solution broke
        pos_old = pos.copy()
        core_logic(pos, clues, d, clues_per_line, clues_per_row)
        if ((pos_old - pos).any() == set()): #still stuck (logic made no progress)
            success, solution = brute_force_ending(pos.copy(), clues, d, clues_per_line, clues_per_row)
            if success: return True, solution

    if verbose: print_pos(pos, clues)
    if set() in pos: return (False, pos)
    return (True, pos)

def core_logic(pos, clues, d, clues_per_line, clues_per_row):
    #core logic one step
    pos = logic_single_option_rows(pos)
    pos = logic_single_option_lines(pos)
    pos = logic_clean_selected_option_rows(pos)
    pos = apply_hints(pos, clues, d, clues_per_line, clues_per_row, 'horizontal')
    pos = logic_single_option_rows(pos)
    pos = logic_single_option_lines(pos)
    pos = logic_clean_selected_option_rows(pos)
    pos = apply_hints(pos, clues, d, clues_per_line, clues_per_row, 'vertical')
    pos = logic_single_option_rows(pos)
    pos = logic_single_option_lines(pos)
    pos = logic_clean_selected_option_rows(pos)
    return pos

def is_broken(pos):
    #return true if puzzle is broken
    for i in range(n):
        for j in range(n):
            if pos[i][j]==set():
                return True
    return False

def is_done(pos):
    for i in range(n):
        for j in range(n):
            if len(pos[i][j]) > 1:
                return False
    return True

def logic_clean_selected_option_rows(pos):
    #if in a row or colum one value of the set 1..7 is selected, delete this value as an option on it's row and colum
    for i in range(n):
        for j in range(n):
            if 1 == len(pos[i][j]):  # Value {6} is unique somewhere in pos
                if verbose: print(pos[i][j])
                for y in range(n):  # over all indices to remove
                    if y != j:  # don't delete itself
                        pos[i][y] = pos[i][y] - pos[i][j]  # set operation
                    if y != i:  # don't delete itself
                        pos[y][j] = pos[y][j] - pos[i][j]  # set operation
    return pos


def logic_single_option_lines(pos):
    pos = pos.transpose()
    pos = logic_single_option_rows(pos)
    pos = pos.transpose()
    return pos


def logic_single_option_rows(pos):
    # if in a row or line there is only one option for a number, make it the single option in that cell
    for row_index in range(n):
        for number_to_inspect in range(n):
            if verbose: print(pos[:, row_index])
            result = [i for i in range(n) if number_to_inspect in pos[:, row_index][i]]
            if len(result) == 1:
                if verbose: print('FOUND ' + str(number_to_inspect))
                pos[:, row_index][result] = {number_to_inspect}
    return pos


def apply_hints(pos, clues, d, clues_per_line, clues_per_row, direction='horizontal'):
    if direction == 'vertical': pos = pos.transpose()
    # all possible_lines considering line hints

    for line_number in range(n):
        line_or_row_clues = (direction == 'horizontal') * clues_per_line[line_number] + (direction == 'vertical') * \
                            clues_per_row[line_number]  # choses one
        # possible_lines = [line for line in d.keys() if d[line] == line_or_row_clues] #doesn't work with zeros
        possible_lines = [line for line in d.keys()
                          if line_or_row_clues[0] in (d[line][0], 0)
                          if line_or_row_clues[1] in (d[line][1], 0)]

        if verbose: print('len possible_lines before = ' + str(len(possible_lines)))
        possible_lines = [line for line in possible_lines if
                          False not in [line[i] in pos[line_number][i] for i in range(n)]]
        if verbose:
            temp2 = len(possible_lines)
            print('len possible_lines after = ' + str(temp2))
            print('possible lines')
            print(possible_lines)
            print('pos[line_number]')
            print(pos[line_number])

        for row in range(n):
            set_of_values_per_index = set([possible_lines[index][row] for index, x in enumerate(possible_lines)])
            if verbose: print(set_of_values_per_index)
            pos[line_number][row] = set_of_values_per_index & pos[line_number][row]
    if direction == 'vertical': pos = pos.transpose()
    return pos


def print_pos(pos, clues):
    for j in range(n):
        print(' ' * 3, end='')
        print(clues[j], end='')
        print((19 - len(str(clues[j]))) * ' ', end='')

    for i in range(n):
        print()
        print(str(clues[27 - i]), end='')
        print((3 - len(str(clues[27 - i]))) * ' ', end='')
        for j in range(n):
            print(pos[i][j], end='')
            print((22 - len(str(pos[i][j]))) * ' ', end='')
        print(clues[7 + i], end='')

    print('')
    for j in range(n):
        print(' ' * 3, end='')
        print(clues[20 - j], end='')
        print((19 - len(str(clues[22 - j]))) * ' ', end='')
    print()
    print()


def possibilities_on_board_naive(pos):
    #calculates a naive approach to possibilities on the board. This shows that brute force wouldn't work at early stages.
    #Not used to solve the problem and can be ignored
    m = 1
    for i in range(n):
        for j in range(n):
            m = m * len(pos[i, j])
    print('')
    print('There are ' + str(m) + ' possibilities on this board configuration.')


def possibilities_on_board_vectorized(pos, d):
    # calculated possibilities on the board using lines. Gives a rough estimate of the complexity left to solve. Not used to solve the problem and can be ignored.
    print()
    count_vec = []  # count possibilities
    # find all vectors that match this line
    for line_number in range(n):
        line = pos[line_number]
        if verbose:
            print('line')
            print(line)
        count = 0
        for v in d.keys():
            # print(v)
            match = True
            for j in range(n):
                if v[j] not in pos[line_number][j]:
                    match = False
            if match:
                count += 1
                if verbose: print(v)
        count_vec.append(count)
    print(count_vec)
    print('There are ' + str(np.prod(count_vec)) + ' possibilities on this board configuration with line vectors')


def find_hint(vec):
    res, maxval = 0, 0
    for val in vec:
        if val > maxval:
            maxval = val
            res += 1
    return res
  
#######################
from itertools import permutations

global dim
dim=7

# #sky scr that can be seen from left to right
def view(x):
    pd = x.index(dim)
    if pd<2:
        return pd+1
    n=2
    ma=x[0]
    for i in range(1,pd):
        if x[i] > ma:
            n+=1
            ma=x[i]
    return n

def not_allowed(m,digit,row,col):
    for i in set(list(range(dim))) - {row}:
        m[i][col].add(digit)
    for i in set(list(range(dim))) - {col}:
        m[row][i].add(digit)
    m[row][col]= set(list(range(1,dim+1)))
    return m

def is_allowed_sudoku(matrix,digit,row,col):
    #check rows
    if digit in matrix[row]: return False
    #check columns
    for r in matrix:
        if digit==r[col]: return False
    return True

def solve_puzzle (clues):
    #make a few useful dictionaries:
    cd = {}   #clue dictionarie
    carr = {}  #clue array of coords
    cbro = {} #clue brothers
    cperm = {}
    for ic,c in enumerate(clues):
        x = ic//dim
        cbro[ic] = (3+ 2*(x%2))*dim - 1 - ic
        if c:
            x,y = divmod(ic,dim)
            cd[ic] = c
            arr=[]
            if x==0:
                for i in range(dim): arr.append((i,y))
            elif x==1:
                for i in range(dim-1,-1,-1): arr.append((y,i))
            elif x==2:
                for i in range(dim-1,-1,-1): arr.append((i,dim-y-1))
            elif x==3:
                for i in range(dim): arr.append((dim-y-1,i))
            carr[ic] = arr
    #build matrix and non-matrix
    m=[]
    mnot=[]
    nums=set(list(range(1,dim+1)))    # a set with all digits
    for i in range(dim):
        m.append([0]*dim)
        x=[]
        for j in range(dim):
            x.append(set())
        mnot.append(x)
    
    #start filling mnot
    for n,clue in cd.items():
        if clue<2: continue
        for digit in range(dim,dim-clue+1,-1):
            for i in range(0,digit+clue-dim-1):
                #print('{} not in {}'.format(digit,i))
                x,y=carr[n][i]
                mnot[x][y].add(digit) 
        #one but highest number cannot be on 2nd position if clue==2
        if clue==2:
            x,y=carr[n][1]
            mnot[x][y].add(dim-1) 
        
    #easy clues
    cdtmp=cd.copy()
    for n,clue in cdtmp.items():
        if clue==1:
            x,y=carr[n][0]
            if not m[x][y]:
                m[x][y]=dim
                mnot=not_allowed(mnot,dim,x,y)
            del cd[n]
        if clue==dim:
            for i in range(0,dim):
                x,y=carr[n][i]
                if not m[x][y]:
                    m[x][y]=i+1
                    mnot=not_allowed(mnot,i+1,x,y)
            del cd[n]
    
    #now iterate a bunch of human strategies until no more entries change
    changed=True
    cycle=1
    while changed:
        changed=False
        cycle+=1
        #first check for cells that only have one possible entry
        for x in range(dim):
            for y in range(dim):
                if len(mnot[x][y]) == dim -1:
                    digit = (nums - mnot[x][y]).pop()
                    m[x][y] = digit
                    mnot=not_allowed(mnot,digit,x,y)
                    changed=True
        
        #check rows where a number can only be put at one position
        for x in range(dim):
            d=[0]*dim
            for y in range(dim):
                for i in mnot[x][y]:
                    d[i-1] += 1   # store occurences in d
            for digit,n in enumerate(d,1):
                if digit in m[x]:    # skip digits that have been filled in already
                    continue
                if n == dim - 1:
                    for y in range(dim):    
                        if not digit in mnot[x][y]:
                            m[x][y] = digit
                            mnot=not_allowed(mnot,digit,x,y)
                            changed=True
                            break
        #repeat for columns
        for y in range(dim):
            d=[0]*dim
            for x in range(dim):
                for i in mnot[x][y]:
                    d[i-1] += 1   # store occurences in d
            for digit,n in enumerate(d,1):
                if digit in [m[x][y] for x in range(dim)]:
                    continue             # skip digits that have been filled in already
                if n == dim - 1:
                    for x in range(dim):    
                        if not digit in mnot[x][y]:
                            m[x][y] = digit
                            mnot=not_allowed(mnot,digit,x,y)
                            changed=True
                            break
        # clue-based strats
        # remove irrelevant clues
        cdtmp=cd.copy()
        for n,clue in cdtmp.items():
            # clue=2 and 2nd highest sky scraper at pos 1
            if clue==2 and m[carr[n][0][0]][carr[n][0][1]] == dim-1:
                del cd[n]
                continue
            #clue=2 and highest sky scraper at pos 2
            if clue==2 and m[carr[n][1][0]][carr[n][1][1]] == dim:
                del cd[n]

        # two tricks if clue == 2
        for n,clue in cd.items():
            if not clue==2:
                continue
            # if highest ss is far opposite of clue 2, 2nd highest should come nearest
            if clue==2 and m[carr[n][dim-1][0]][carr[n][dim-1][1]] == dim:
                x,y = carr[n][0]
                m[x][y] = dim-1
                mnot=not_allowed(mnot,dim-1,x,y)
                changed=True
                continue
            # if lowest ss is adjacent clue 2, highest should come next
            if clue==2 and m[carr[n][0][0]][carr[n][0][1]] == 1:
                x,y = carr[n][1]
                m[x][y] = dim
                mnot=not_allowed(mnot,dim,x,y)
                changed=True
                
        # for each clue make all possible permutations of missing numbers
        # and check against mnot and clues from both ends
        skip=[]
        obsolete_clues=[]
        
        for n,clue in cd.items():
            if n in skip: continue    # we already looked at this row/col from the other end
            r=[m[x][y] for x,y in carr[n]]
            if cbro[n] in cd:
                clue2= cd[cbro[n]]
                skip.append(cbro[n])
            else:
                clue2=0
            empty=r.count(0)
            #if empty > dim-2: continue    # focus on the ones with max dim-2 zeroes
            if empty == 0:
                obsolete_clues.append(n)
                if cbro[n] in cd:
                    obsolete_clues.append(cbro[n])
                continue
            missing=nums - set(r)
            valid=[]
            for i in range(empty):
                valid.append(set())
            rnot=[mnot[x][y] for x,y in carr[n] if m[x][y]==0]
            # if cycle ==1 or if the number of missing digits has changed
            # we need to calculate the permutations against
            if not n in cperm:
                cperm[n] = list(permutations(missing))
            else:
                cperm_n_len = len(max(cperm[n],key=len))
                if cperm_n_len != len(missing):
                    cperm[n] = list(permutations(missing))
            #tmpperm=list(cperm[n])
            for ip,perm in enumerate(cperm[n]):
                if not perm:
                    continue    # skip empty perms
                # test against mnot
                perm_ok=True
                for i,d in enumerate(perm):
                    if d in rnot[i]:
                        perm_ok=False
                        break
                if not perm_ok:
                    cperm[n][ip]=()   # remove false permutation from the list
                    continue      # evaluate next permutation
                #test if array test fulfils clue and clue2
                test=list(r)
                p=list(perm)
                perm_position=[]
                for i in range(dim):
                    if not test[i]:
                        test[i] = p.pop(0)
                        perm_position.append(i)
                perm_ok=False
                if view(test)==clue:
                    perm_ok=True
                    if clue2:
                        if view(test[::-1]) != clue2:
                            perm_ok=False
                if not perm_ok:
                    cperm[n][ip]=()   # remove false permutation from the list
                    continue    # evaluate next permutation
                
                #now add the valid permutation to the list of valid numbers
                for i,p in enumerate(perm):
                    valid[i].add(p)
                
            #interesting elements in valid are the ones that have
            #  (1) only one digit,
            #  (2) fewer than 'empty' digits
            #  (3) a pair of twins
            #  (4) a digit that occurs only once
            # numbers 3 and 4 do not seem to occur. could be relevant for 8x8
            for i,allowedset in enumerate(valid):
                if len(allowedset)==1:
                    x,y = carr[n][perm_position[i]]
                    digit=allowedset.pop()
                    m[x][y] = digit
                    mnot=not_allowed(mnot,digit,x,y)
                    changed=True
                elif len(allowedset) < empty:
                    banned = missing - allowedset
                    x,y = carr[n][perm_position[i]]
                    if banned - mnot[x][y]:
                        mnot[x][y] = mnot[x][y] | banned
                        changed=True
        
        for clue in obsolete_clues:
            del cd[clue]
            
    #I really hoped I could solve the kata without brute force backtracking, but
    #the medved puzzle forced me to include the below...
    
    #back tracking for the remaining spaces/zeros
    #make list (bt) of positions that have not been filled yet. t is tracker
    #it only checks for horizontal clues. Could be insufficient for some puzzles...
    bt=[]
    t=0
    for i in range(dim):
        for j in range(dim):
            if not m[i][j] : bt.append([i,j])
    #return if sudoku had already been solved
    if len(bt)==0: return m
    c=0
    while t<len(bt):
        c+=1
        row,col = bt[t]
        if m[row][col] <dim:
            hit=False
            for d in range(1+m[row][col],dim+1):
                if not d in mnot[row][col] and is_allowed_sudoku(m,d,row,col):
                    if m[row].count(0) == 1:
                        hit=True
                        testrow = list(m[row])
                        testrow[testrow.index(0)] = d
                        if dim+row in cd.keys():
                            if view(testrow[::-1]) != cd[dim+row]:
                                hit=False
                        if cbro[dim+row] in cd.keys():
                            if view(testrow) != cd[cbro[dim+row]]:
                                hit=False
                    else:
                        hit=True
                    if hit:
                        break
            if hit:
                m[row][col]=d
                t=t+1
                continue
        #this is reached if cell contains dim, or no digit could be placed
        m[row][col] = 0   #reset to zero
        t=t-1             #back track
    return m
  
#######################
from itertools import permutations
from collections import defaultdict
import copy

def seen_count(line, start = 0):
    
    i = start + 1
    while i < len(line):
        if line[i] > line[start]:
            return 1 + seen_count(line, i)
        i += 1
    return 1
    
    
def solve_puzzle (clues):

    size = 7
    col = clues[:size]
    row_rev = clues[size: 2*size]
    col_rev = clues[3*size-1: 2*size-1:-1]
    row = clues[:3*size-1:-1]
    
    result_matrix = [[None for _ in range(size)] for _ in range(size)]
    cell_options_matrix = [[None for _ in range(size)] for _ in range(size)]
    row_options = [None for _ in range(size)]
    col_options = [None for _ in range(size)]
    # the final result_matrix (necessary because of the medved)
    result_result_matrix = []

    permutats = list(permutations(range(1, size+1)))
    permutation_dict = {elem: seen_count(elem) for elem in permutats}
    
    seen_dict = defaultdict(list)
    for key, value in permutation_dict.items():
        seen_dict[value].append(key)
        
    seen_dict_reversed = dict()
    for key, value in seen_dict.items():
        seen_dict_reversed[key] = [option[::-1] for option in value]
    
    def calculate_options(clue_left, clue_right):
        if clue_left > 0:
            if clue_right == 0:
                options = seen_dict[clue_left]
            else:
                options = set(seen_dict_reversed[clue_right]) & set(seen_dict[clue_left])
        elif clue_right > 0:
            options = seen_dict_reversed[clue_right]
        else:
            options = permutats
        return set(options)
    
    for i in range(size):
        row_options[i] = calculate_options(row[i], row_rev[i])
        col_options[i] = calculate_options(col[i], col_rev[i])
            
    # adjusting matrix (both cell_options and result) on the basis of the content in row_options list.
    # if any change has been made, the function return True. Otherwise, False.
    def adjust_matrix_by_row_options():
        changed = False
        # iterating over the four elements (each representing one row in the matrix as a set of tuples) of the row_options list.
        for i, options in enumerate(row_options):
            if len(options) == 1:
                # row_options[i] equals options. I use row_options[i] so that the pop() method removes the cell values from the row_options list,
                # and not from the temporary variable "options". I will later need to know if the options of a line is empty.
                cell_values = row_options[i].pop()
                result_matrix[i] = [*cell_values]
                cell_options_matrix[i] = [set() for j in range(size)]
                changed = True
            # len(options) can be 0 as well, this means that the given row of the matrices has already been filled up entirely
            # in this chase, we don't need to do anything.
            elif len(options) > 1:
                # cell_options will be a list of size "size" (the size of the matrix), containing all the possible elements for each cell in the row
                # on the basis of the row_options list (which is in turn calculated on the basis of the clues)
                cell_options = zip(*options)
                # iterating through the four cells of the row
                for j, cells in enumerate(cell_options):
                    # the options (numbers) availagble for the given cell (cell_options_matrix[i][j]) will be the intersection of the 
                    # cell_options calculated from the row_options (set zip), and the cell_options retreaved form the cell_options_matrix
                    # at the beginning, cell_options_matrix[i][j] is None, so its value is going to be set(cells)
                    new_cell_option_set = set(cells) if cell_options_matrix[i][j] == None else cell_options_matrix[i][j] & set(cells)
                    if cell_options_matrix[i][j] != new_cell_option_set:
                        cell_options_matrix[i][j] = new_cell_option_set
                        changed = True
                    # if there is only one option --> we found a solution for the given cell
                    # let's copy it to the results matrix and delete from the cell_options_matrix
                    if len(new_cell_option_set) == 1:
                        (result_matrix[i][j], ) = new_cell_option_set
                        cell_options_matrix[i][j] = set()
        return changed
    
    # same function for the col options as adjust_matrix_by_row_options:
    def adjust_matrix_by_col_options():
        changed = False
        for i, options in enumerate(col_options):
            if len(options) == 1:
                cell_values = col_options[i].pop()
                for j, cell_value in enumerate(cell_values):
                    cell_options_matrix[j][i] = set()
                    if not result_matrix[j][i]:
                        result_matrix[j][i] = cell_value
                        changed = True
            elif len(options) > 1:
                cell_options = zip(*options)
                for j, cells in enumerate(cell_options):
                    new_cell_option_set = set(cells) if cell_options_matrix[j][i] == None else cell_options_matrix[j][i] & set(cells)
                    if cell_options_matrix[j][i] != new_cell_option_set:
                        cell_options_matrix[j][i] =  new_cell_option_set
                        changed = True
                    if len(new_cell_option_set) == 1:
                        (result_matrix[j][i], ) = new_cell_option_set
                        cell_options_matrix[j][i] = set()
        return changed
    
    def reduce_cell_options():
        reduced = False
        # check in each row if the options of a cell can be reduced
        # based on the already found cell values contained in result_matrix
        # (these values should not appear in the not-yet-solved cells)
        for i in range(size):
            founds = set(result_matrix[i]) - {None}
            for j in range(size):
                option_size = len(cell_options_matrix[i][j])
                # all_other_cell_options will be the value(s) of 
                # all the options for the other cells in the row (cell_options_matrix[i]), not included in the options of the current cell.
                # to make one set from a list of sets i call set().union(*list)
                all_other_cell_options = founds.copy()
                for k in range(size):
                    if k != j: 
                        all_other_cell_options |= cell_options_matrix[i][k]
                # if there exists at least one option that is only in the j-th cell of row[i]
                # and the count of these values is less than the original count of options
                test_value = cell_options_matrix[i][j] - all_other_cell_options
                
                if test_value and len(test_value) < option_size:
                    cell_options_matrix[i][j] = test_value
                    reduced = True
                if len(cell_options_matrix[i][j]) == 1:
                    (result_matrix[i][j], ) = cell_options_matrix[i][j]
                    cell_options_matrix[i][j] = set()
            
        #reducing cols
        for j in range(size):
            # founds is a set made from the options j-th coloumn of the result_matrix
            founds = set([result_matrix[i][j] for i in range(size)]) - {None}
            col_options_set = set().union(*[cell_options_matrix[i][j] for i in range(size)])
            for i in range(size):
                option_size = len(cell_options_matrix[i][j])
                all_other_cell_options = founds.copy()
                for k in range(size):
                    if k != i:
                        all_other_cell_options |= cell_options_matrix[k][j]
                test_value = cell_options_matrix[i][j] - all_other_cell_options
                
                if test_value and len(test_value) < option_size:
                    cell_options_matrix[i][j] = test_value
                    reduced = True  
                if len(cell_options_matrix[i][j]) == 1:
                    (result_matrix[i][j], ) = cell_options_matrix[i][j]
                    cell_options_matrix[i][j] = set()
                    
        return reduced
    
    def reduce_row_options():
        changed = False
        for i in range(size):
            if len(row_options[i]) > 1:
                row_options_copy = row_options[i].copy()
                for option in row_options_copy:
                    for j, cell in enumerate(option):
                        if cell not in cell_options_matrix[i][j] and cell != result_matrix[i][j]:
                            row_options[i].discard(option)
                            changed = True
                            break

        return changed
    
    def reduce_col_options():
        changed = False
        for j in range(size):
            if len(col_options[j]) > 1:
                col_options_copy = col_options[j].copy()
                for option in col_options_copy:
                    for i, cell in enumerate(option):
                        if cell not in cell_options_matrix[i][j] and cell != result_matrix[i][j]:
                            col_options[j].discard(option)
                            changed = True
                            break
        return changed
    
                            
    def adjust():
        changed = True
        while changed == True:
            changed = False
            changed |= adjust_matrix_by_row_options()
            changed |= adjust_matrix_by_col_options()
            changed |= reduce_cell_options()
            changed |= reduce_row_options()
            changed |= reduce_col_options()
    
    adjust()
    
    # find the cell that is not solved even after running "adjust" (if any)
    # and find the one with the least options
    def not_finished():
        not_solved_cell = None
        minlen = size
        for i in range(size):
            for j in range(size):
                if not result_matrix[i][j]:
                    l = len(cell_options_matrix[i][j])
                    if l < minlen:
                        not_solved_cell = (i, j)
                        minlen = l
        return not_solved_cell
    
    
    def OK_double_check():
        
        for i, opts in enumerate(row_options):
            if len(opts) == 1:
                (cell_values, ) = opts
                for j in range(size):
                    if result_matrix[i][j] and cell_values[j] != result_matrix[i][j]:
                        return False
            elif len(opts) > 1:
                cell_options = zip(*opts)
                # iterating through the seven cells of the row
                for j, cells in enumerate(cell_options):
                    if result_matrix[i][j] and result_matrix[i][j] not in cells:
                        return False
                    
        for i, opts in enumerate(col_options):
            if len(opts) == 1:
                (cell_values, ) = opts
                for j, cell_value in enumerate(cell_values):
                    if result_matrix[j][i] and result_matrix[j][i] != cell_value:
                        return False    
            elif len(opts) > 1:
                cell_options = zip(*opts)
                for j, cells in enumerate(cell_options):
                    if result_matrix[j][i] and result_matrix[j][i] not in cells:
                        return False     
                    
        # check for reasonability within the matrix (i.e. no repetitions in rows and cols)
        for i in range(size):
            if size - result_matrix[i].count(None) > len(set(result_matrix[i]) - {None}):
                return False
            
        for j in range(size):
            # create a list of found values for each col
            col = [result_matrix[i][j] for i in range(size) if result_matrix[i][j]]
            if len(col) > len(set(col)):
                return False

        return True
    
    # the difference to the original adjust function is that here I sometimes need to
    # check whether the result_matrix is still valid. (previously, it was unambiguous)
    def adjust_medved():
        changed = True
        while changed == True:
            changed = False
            changed |= adjust_matrix_by_row_options()
            if not OK_double_check():
                return False
            changed |= adjust_matrix_by_col_options()
            if not OK_double_check():
                return False
            changed |= reduce_cell_options()
            if not OK_double_check():
                return False
            changed |= reduce_row_options()
            changed |= reduce_col_options()
        return True
    
    # check if the puzzle is not a medved puzzle (and if it is, deal with it)
    def medvedUtil(row_options_bases, col_options_bases, cell_options_matrix_bases, result_matrix_bases):
        
        nonlocal row_options, col_options, cell_options_matrix, result_matrix, result_result_matrix
        not_solved_cell = not_finished()
        if not_solved_cell == None:
            if len(result_result_matrix) == 0:
                result_result_matrix = copy.deepcopy(result_matrix)

        # so this is where I try to address the medved tests.
        # I think medved tests are puzzles where my above techniques are not sufficient
        # applying those will leave some cells unsolved.
        # my logic for the medved test would be to identify the unsolved cells with the 
        # least number of remaining opitons (ideally two). Then go through these options
        # First try to solve the puzzle by treating the first option as right
        # if it doesn't work, try the same with the next option.
        else:
            
            i, j = not_solved_cell
            cell_options_base = cell_options_matrix[i][j].copy()
            for cell in cell_options_base:
                # first I make backup copies of the global lists and matrices 
                # to be able to backtrack with recursion
                # recursion (backtrack) is needed to cover cases 
                # when an attempt to a medved test leads to another medved case
                row_options_base = copy.deepcopy(row_options)
                row_options_bases.append(row_options_base)
                col_options_base = copy.deepcopy(col_options)
                col_options_bases.append(col_options_base)
                cell_options_matrix_base = copy.deepcopy(cell_options_matrix)
                cell_options_matrix_bases.append(cell_options_matrix_base)
                result_matrix_base = copy.deepcopy(result_matrix)
                result_matrix_bases.append(result_matrix_base)
                cell_options_matrix[i][j] = {cell}
                
                # adjust medved tries to calculate the missing cells of result_matrix
                # if it doesn't work (i.e. the calculated results contradict), 
                # it return False. This means that the chosen seed cell value was not good,
                # we have to continue looping over the other values.
                # On the other hand, if adjust_medved return True, it means that 
                # no contradiction was found up to this point, we can continue solving
                # the remaining missing cells, if any. So I call medved() again.
                if adjust_medved():
                    
                    medvedUtil(row_options_bases, col_options_bases, cell_options_matrix_bases, result_matrix_bases)
                
                else:
                    row_options = row_options_bases.pop()
                    col_options = col_options_bases.pop()
                    cell_options_matrix = cell_options_matrix_bases.pop()
                    result_matrix = result_matrix_bases.pop()
                
    def medved():
        row_options_bases = []
        col_options_bases = []
        cell_options_matrix_bases = []
        result_matrix_bases = []
        medvedUtil(row_options_bases, col_options_bases, cell_options_matrix_bases, result_matrix_bases)
        

                    
    # and finally I call medved()
    medved()
    return result_result_matrix
  
###################
from itertools import permutations,zip_longest
from copy import deepcopy

def solve_puzzle (clues):
    return unparse(solve.from_raw(clues))

def unparse(g):
    grid = g.grid
    for i,row in enumerate(grid):
        for j,cell in enumerate(row):
            row[j] = cell.pop()
    
    return grid


def grid_print(xs):
    list(map(print, xs))
    print()

class solve:
    # glofiried closure
    def __init__(self, columns, rows, posses, grid):
        ##columns, rows
        k = len(columns)
        self.posses = posses
        self.perms = list(permutations(self.posses) )
        grid = grid
        # set of all possible values. If len 1, is solved
        
        while True:
            new = self.do_pass(columns, rows,(grid))
            if new == grid:
                posses = [(c,i,j) for i,row in enumerate(grid) for j,c in enumerate(row) if len(c) != 1
                         ]
                if not posses:
                    break
                    # solved
                a = min(posses, key = lambda x:len(x[0]))
                c,i,j = a
                if len(c) == 0:
                    # impossible state
                    self.grid = False
                    return
                else:
                    m = min(c)
                    # deterministic guess
                    g = deepcopy(grid)
                    g[i][j] = {m}
                    res = solve(columns, rows, self.posses, g).grid
                    if res:
                        # guessed right
                        grid = res
                        break
                    else:
                        new[i][j] -= {m}
                        
                    
                
            grid = new
        self.grid = grid
        

    @classmethod
    def from_raw(cls, clues):
        columns, rows = parse(clues)
        k = len(columns)
        posses = set(range(1,k+1))
        ##perms = list(permutations(self.posses) )
        grid = [  [posses.copy() for i in range(k)] for j in range(k)]
        return solve(columns, rows, posses, grid)
        
    
    
    def do_pass(self, columns, rows,grid ):
        a = self.step(rows, grid)
        b = self.step(columns, transpose(a ) )
        passed = transpose(b)
        
        
        
        return passed

    
    def step(self, columns, grid):
        new_ = [ self.row_check(c,row)
        for i, (c,row) in enumerate(zip(columns, grid))]
            
        
        return self.reduce_posses(new_)
    
    def row_check(self, data, line):
        posses = self.perms
        posses = (i for i in posses if  all( b in a     for (a,b) in zip(line,i) ) )
        posses = (i for i in posses if self.valid(data,i)  )
        
        res = list(map(set, zip(*posses)))
        
        return res
        
    @classmethod
    def valid(cls, data, poss):
        a,b = data
        c,d = (see(poss), see(poss[::-1]))
        return a in {c,0} and b in {d,0}
    
    
    
    @classmethod
    def reduce_posses(cls, grid):
        for i,row in enumerate(grid):
            for j,cell in enumerate(row):
                if len(cell) == 1:
                    cell = list(cell)[0]
                    for k,c in enumerate(row):
                        if k!=j:
                            c.discard(cell)
                            grid[i][k] = c

        return grid
        
    

def see(row):
    if not row:
        return 0
    x,*xs = row
    return 1 + see( [i for i in xs if i > x] )


def transpose(xs):
    return list(map(list, zip(*xs)) )


def parse(clues):
    k = len(clues)//4
    a,b,c,d = grouper(clues,k)
    return  list(zip(a,c[::-1])), list(zip(d[::-1],b))


# from https://docs.python.org/3/library/itertools.html
def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
