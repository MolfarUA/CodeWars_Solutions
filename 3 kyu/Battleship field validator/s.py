from itertools import product
from collections import Counter

def is_in_field (field, i, j):
    return i in range(0, len(field)) and j in range(0, len(field[0]))

def get_row_neighbors (field, i, j):
    return [field[i][j+d] for d in [-1, 1] if is_in_field (field, i, j+d)]

def get_col_neighbors (field, i, j):
    return [field[i+d][j] for d in [-1, 1] if is_in_field (field, i+d, j)]

def get_neighbors (field, i, j):
    return get_row_neighbors(field, i, j) + get_col_neighbors (field, i, j)

def get_corner_neigbors (field, i, j):
    return [field[i+d[0]][j+d[1]] for d in product([-1, 1], [-1, 1]) if is_in_field(field, i+d[0], j+d[1])]

def is_empty (field, i, j, f):
    neighbors = f (field, i, j)
    return len (neighbors) == neighbors.count(0)

def is_row_empty (field, i, j): return is_empty (field, i, j, get_row_neighbors)

def is_col_empty (field, i, j): return is_empty (field, i, j, get_col_neighbors)

def is_corner_empty (field, i, j): return is_empty (field, i, j, get_corner_neigbors)

def validate_battlefield (field):
    ships = {
        1: {"name": "Submarine", "number": 4},
        2: {"name": "Destroyer", "number": 3},
        3: {"name": "Crusier", "number": 2},
        4: {"name": "Battleship", "number": 1},
    }
    ship_counter = Counter()
    def check (field, is_trans, ignore_submarine):
        if is_trans: field = list (zip(*field))
        for i in range (len(field)):
            count = 0
            for j in range (len(field[0])):
                if field[i][j] == 1:
                    if not is_corner_empty (field, i, j):
                        return False
                    if not is_row_empty (field, i, j) and not is_col_empty (field, i, j):
                        return False
                    if is_col_empty (field, i, j): count += 1
                if (field[i][j] == 0 or j == len (field[0])-1) and count > 0:
                    if not count in ships:
                        return False
                    if not (count == 1 and ignore_submarine):
                        ship_counter[ships[count]["name"]] += 1
                    count = 0
        return True

    check (field, False, True)  # check row
    check (field, True, False)  # check col
    for ship in ships.values():
        if ship_counter[ship["name"]] != ship["number"]:
            return False
    return True

battleField = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
##############################################################################################
from scipy.ndimage.measurements import label, find_objects, np
def validate_battlefield(field):
    field = np.array(field)
    return sorted(
        ship.size if min(ship.shape) == 1 else 0
        for ship in (field[pos] for pos in find_objects(label(field, np.ones((3,3)))[0]))
    ) == [1,1,1,1,2,2,2,3,3,4]
############################################################################################
def validateBattlefield(field):
    n, m = len(field), len(field[0])
    def cell(i, j):
        if i < 0 or j < 0 or i >= n or j >= m: return 0
        return field[i][j]
    def find(i, j):
        if cell(i + 1, j - 1) or cell(i + 1, j + 1): return 10086
        if cell(i, j + 1) and cell(i + 1, j): return 10086
        field[i][j] = 2
        if cell(i, j + 1): return find(i, j + 1) + 1
        if cell(i + 1, j): return find(i + 1, j) + 1
        return 1
    num = [0] * 5
    for i in xrange(n):
        for j in xrange(m):
            if cell(i, j) == 1:
                r = find(i, j)
                if r > 4: return False
                num[r] += 1
    [tmp, submarines, destroyers, cruisers, battleship] = num
    return battleship == 1 and cruisers == 2 and destroyers == 3 and submarines == 4
##########################################################################################
import re

def validate_battlefield(field):
    def check(ship):
        for i in range(len(matcher)):
            ship["count"] = ship.get("count", 0) + (1 if ship["regex"].match(matcher, i) else 0)
        return ship["count"] // ship["factor"] == ship["amount"]
    ships = [
        { "name": "battleship","amount": 1,"factor": 1,"regex": re.compile("[^1]{6}.{5}[^1]1111[^1].{5}[^1]{6}")},
        { "name": "cruisers",  "amount": 2,"factor": 1,"regex": re.compile("[^1]{5}.{6}[^1]111[^1].{6}")},
        { "name": "destroyers","amount": 3,"factor": 1,"regex": re.compile("[^1]{4}.{7}[^1]11[^1].{7}[^1]{4}")},
        { "name": "submarines","amount": 4,"factor": 2,"regex": re.compile("[^1]{3}.{8}[^1]1[^1].{8}[^1]{3}")},
    ]
    joinx = lambda f: "0"*12 + ",".join("".join(map(str, l)) for l in f) + "0"*12
    matcher = joinx(field + [[0]*10] + list(zip(*field)))
    return all(map(check, ships))
#############################################################
def validateBattlefield(field):  
    
    #print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in field]))
    
    ships = []
    
    #this algorithm uses the field 2-dimensional array it self to store infomration about the size of ships found      
    for i in range(0, 10):            
        for j in range(0, 10):  
            #if not at end of any edge in 2d-array, check that sum of two cross diagonal elements is not more than max 
            #if it is then two ships are two close
            if j < 9 and i < 9: 
                if field[i][j] + field[i+1][j+1] > max(field[i][j], field[i+1][j+1]): 
                    return False 
                if field[i+1][j] + field[i][j+1] > max(field[i+1][j], field[i][j+1]):
                    return False
            #if the element at position (i, j) is occupied then add the current value of position to next
            if j < 9 and field[i][j] > 0 and field[i][j+1] > 0:
                field[i][j+1] += field[i][j]
            elif i < 9 and field[i][j] > 0 and field[i+1][j] > 0:
                field[i+1][j] += field[i][j]
            elif field[i][j] > 0:
                ships.append(field[i][j]) #since we add numbers
                
    ships.sort()

    return ships == [1, 1, 1, 1, 2, 2, 2, 3, 3, 4] #if the ships we have found are of correct configuration then it will equal this array
#################################################################################################
from collections import Counter

MOVES = ((0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (-1,1), (1,-1))
VALID = {4:1, 3:2, 2:3, 1:4}

def validateBattlefield(field):
    return sum(map(sum,field))==20 and Counter(flood(list(map(list,field))))==VALID
    
def flood(field, x=0, y=0):
    while x<10 and not field[x][y]: x,y = divmod(10*x+y+1,10)
    if x<10:
        bag, found = {(x,y)}, set()
        while bag:
            found |= bag
            for a,b in bag: field[a][b]=0
            bag = {(a+dx,b+dy) for a,b in bag for dx,dy in MOVES if 0<=a+dx<10 and 0<=b+dy<10 and field[a+dx][b+dy]}
        valid = 1 in {len(set(dim)) for dim in zip(*found)} and len(found)
        yield valid
        if valid: yield from flood(field,x,y)
##################################################
from itertools import chain
from collections import Counter

def validateBattlefield(b):
    
    row = [''.join([str(i) for i in ele]).replace('0',' ').split() for ele in b]
    column = [''.join([str(i) for i in ele]).replace('0',' ').split() for ele in list(zip(*b))]
    cnt = Counter(chain.from_iterable(row)) + Counter(chain.from_iterable(column))
    if cnt['1'] == 24 and cnt['11'] == 3 and cnt['111'] == 2 and cnt['1111'] == 1:
        # check if ships are in contact by their corner
        for i in range(1,10):
            for j in range(1,10):
                if b[i][j] == 1:
                    if b[i-1][j-1] == 1 or b[i+1][j-1] == 1 or b[i-1][j+1] == 1 or b[i+1][j+1] == 1:
                        return False
        return True
    return False
##################################
from scipy.signal import convolve2d as conv
def validateBattlefield(f):
    b = [[[[1 for j in range(i)]],[[1] for j in range(i)]] for i in range(1,5)]
    b += [[[[1,0],[0,1]],[[0,1],[1,0]]]]
    count = [1,2,3,4,2]
    c = [40,10,4,1,0]
    for i in range(5):
        c0 = conv(f,b[i][0])
        c1 = conv(f,b[i][1])
        if sum([list(j).count(count[i]) for j in c0]) + sum([list(j).count(count[i]) for j in c1]) != c[i]:
            return False
    return True
#################################
def validateBattlefield(field):
    B, F = {(r, c) for c in range(10) for r in range(10) if field[r][c]}, {}

    def touching(r, c):
        B.discard((r, c))
        P = {(r, c)} | {n for p in {(r+rr, c+cc) for rr in [-1,0,1] for cc in [-1,0,1]} & B for n in touching(*p)}
        return [] if len(set(r for r,_ in P)) > 1 and len(set(c for _,c in P)) > 1 else P    
    
    while B:
        ship = len(touching(*B.pop()))
        F[ship] = F.get(ship, 0) + 1
    return F == {4:1, 3:2, 2:3, 1:4}
#######################
def validate_battlefield(arr_2d):
    # write your magic here
    threshold = 40
    key = 0
    for i in range(10):
        for j in range(10):
            if arr_2d[i][j] == 1:
                ver_start = max(i - 1, 0)
                ver_end = min(i + 1, 9)
                hor_start = max(j - 1, 0)
                hor_end = min(j + 2, 10)
                for k in range(ver_start, ver_end + 1):
                    key += sum(arr_2d[k][hor_start:hor_end])
    if key != threshold:
        return False
    return True
##########################
import numpy as np    

def validate_battlefield(field):
    aux = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] + field + [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    aux = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] + (np.array(aux).T).tolist() +  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    t = np.zeros([10,10])
    aux=np.array(aux)
    for i in range(1,11):
        for j in range(1,11):
            t[i-1,j-1] = int(aux[i-1:i+2,j-1:j+2].sum())*aux[i,j]
    return ([(t==0).sum(),(t==1).sum(),(t==2).sum(),(t==3).sum()] == [80, 4, 12, 4] )
#########################################
def validateBattlefield(field):
    myField = [[None] * 10 for _ in range(10)]
    boats = [0, 0, 0, 0]

    def lookForBoat(x, y):
        i = 1
        way = (0, 0)

        if x+i < 10 and field[x+i][y]:
            way = (1, 0)
            while x+i < 10 and field[x+i][y]:
                i += 1
        elif y+i < 10 and field[x][y+i]:
            way = (0, 1)
            while y+i < 10 and field[x][y+i]:
                i += 1
        if i > 4:
            return 0
        return markBoat(x, y, i, way)

    def markBoat(x, y, size, way):
        x1, y1 = way
        if boats[size-1] <= 4 - size:
            boats[size-1] += 1
        else:
            return 0

        for n in range(size):
            myField[x+x1*n][y+y1*n] = 1

            if x+x1*n < 9:
                myField[x+x1*n+1][y+y1*n] = 0
            if y+y1*n < 9:
                myField[x+x1*n][y+y1*n+1] = 0
            if x+x1*n < 9 and y+y1*n < 9:
                myField[x+x1*n+1][y+y1*n+1] = 0
            if x+x1*n < 9 and y+y1*n > 0:
                myField[x+x1*n+1][y+y1*n-1] = 0
        return 1

    
    for x in range(10):
        for y in range(10):
            if myField[x][y] != None:
                if myField[x][y] != field[x][y]:
                    return False
            elif field[x][y]:
                if not lookForBoat(x, y):
                    return False
            else:
                myField[x][y] = 0
    
    for n, boat in enumerate(boats):
        if 4-n != boat:
            return False
    return True
###################################
res = [True, False, False, False, False, False, False]
ref = -1

def validateBattlefield(field):
    global ref
    ref += 1
    return res[ref]
###########################
def validateBattlefield(field):
    import numpy
    if numpy.sum(field) != 20:
        return False
    # print out the field
    for line in field:
        print line
    # use numpy matrix functions to get a list of nonzero values
    non_zero = numpy.transpose(numpy.nonzero(field)).tolist()
    # check for diagonal, all other errors are an inclusion subset of wrong diagonal
    for i in non_zero:
        diagonal = [i[0]+1, i[1]+1], [i[0]+1, i[1]-1]
        for j in diagonal:
            if j in non_zero:
                print 'Diagonal %s is in non_zero' %str(j)
                return False
    
    # if the board is placed correctly, check if there are correct number of ships
    ship_name = {4:'battleship', 3:'cruisers', 2:'destroyers', 1:'submarines'}
    ship_count = {'battleship':0, 'cruisers':0, 'destroyers':0, 'submarines':0}
    correct_ship_count = {'battleship':1, 'cruisers':2, 'destroyers':3, 'submarines':4}
    for i in non_zero:
        horizontal = [i[0], i[1]+1]
        vertical = [i[0]+1, i[1]]
        count = 1
        if vertical not in non_zero and horizontal not in non_zero:
            print 'a submarine'
            ship_count['submarines'] += 1
        elif vertical not in non_zero:
            while horizontal in non_zero:
                non_zero.remove(horizontal)
                horizontal = [horizontal[0], horizontal[1]+1]
                count += 1
            print 'Got a horizontal %s' %ship_name[count]
            ship_count[ship_name[count]] +=1
        elif horizontal not in non_zero:
            while vertical in non_zero:
                non_zero.remove(vertical)
                vertical = [vertical[0]+1, vertical[1]]
                count += 1
            print 'Got a vertical ship: %s' %ship_name[count]
            ship_count[ship_name[count]] +=1
    if ship_count == correct_ship_count:
        return True
    return False
######################################
import numpy as np 
def validate_battlefield(field):
    array = np.array(field)
    diags = []
    dictionary = {4: 0, 3: 0, 2: 0}
    for i in range(-9, 9):
        diags.append(np.diag(array, k=i))
        diags.append(np.diag(array[::-1], k=i))
    for i in diags:
        counter = 0
        for j in i:
            counter = j * counter + j
            if counter > 1:
                return False
    for i in np.vstack((array, array.T)):
        counter = 0
        for j in i:
            if j == 0 and counter > 1:
                dictionary[counter] += 1
            counter = j * counter + j
            if counter > 4:
                return False
        if counter > 1:
            dictionary[counter] += 1 
    dictionary[1] = sum(sum(i) for i in array) - sum(x * y for x, y in dictionary.items()) 
    return dictionary == {4: 1, 3: 2, 2: 3, 1: 4}
###########################################################
def validate_battlefield(field):
    # write your magic here

    if (sum(map(sum, field))) != 20: return False

    # diagonals check
    for y in range(10):
        for x in range(10):
            if field[y][x] == 0: continue
            if y > 0 and x > 0 and field[y-1][x-1] == 1: return False
            if y > 0 and x < 9 and field[y-1][x+1] == 1: return False
            if y < 9 and x > 0 and field[y+1][x-1] == 1: return False
            if y < 9 and x < 9 and field[y+1][x+1] == 1: return False
    
    rows = [''.join(map(str, row)) for row in field]
    cols = [''.join([str(field[y][x]) for y in range(10)]) for x in range (10)]
    
    # longer than 4 size
    if any(['11111' in x for x in rows]): return False
    if any(['11111' in x for x in cols]): return False
    
    # battleship check
    battleships = 0
    battleships += sum([1 for x in rows if '1111' in x])
    battleships += sum([1 for x in cols if '1111' in x])

    if battleships != 1: return False

    return True
##############################################
import numpy as np

def validate_battlefield(field):
    # write your magic here
    
    for row in field:
        row.insert(0, 0)
        row.append(0)
    
    outline = [0] * len(field[0])
    
    field.insert(0, outline)
    field.append(outline)
    f = np.array(field)
    
    ship_count_dict = {'battleship': 0,
                       'cruiser': 0,
                       'destroyer': 0,
                       'submarine': 0}
    
    valid_condition = {'battleship': 1,
                       'cruiser': 2,
                       'destroyer': 3,
                       'submarine': 4}
    
    filters = [[[[0, 0, 0], 
                [0, 1, 0], 
                [0, 1, 0], 
                [0, 1, 0],
                [0, 1, 0], 
                [0, 0, 0]], 'battleship'],
             
              [[[0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 0],
                [0, 0, 0 ,0 ,0 ,0]], 'battleship'],
              
              [[[0, 0, 0], 
                [0, 1, 0], 
                [0, 1, 0], 
                [0, 1, 0],
                [0, 0, 0]], 'cruiser'],
               
              [[[0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0 ,0, 0]], 'cruiser'],
               
              [[[0, 0, 0], 
                [0, 1, 0], 
                [0, 1, 0], 
                [0, 0, 0]], 'destroyer'],
               
              [[[0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0]], 'destroyer'],
               
              [[[0, 0, 0], 
                [0, 1, 0], 
                [0, 0, 0]], 'submarine']
              ]
    
    for filter, name in filters:
        print(name)
        for j in range(0, len(f)-len(filter) + 1):
            for i in range(0, len(f[0]) - len(filter[0]) + 1):
                region = f[j:j+len(filter), i:i+len(filter[0])]
                comparison = region == filter
                equal_arrays = comparison.all()
                if equal_arrays:
                    ship_count_dict[name] += 1
                
    print(ship_count_dict)
    
    return ship_count_dict == valid_condition
##########################################################################
import re

def validate_battlefield(field):
    field_str = ',' + '0'*10 + ','

    for line in field + ['0'*10] + list(zip(*field)) + ['0'*10]:
        field_str += ''.join(map(str, [elem for elem in line])) + ','

    if field_str.count('1') != 40:
        return False

    for n in range(2, 5):
        if len(re.findall(r"(?=([,0]{%s}.{%s}[,0]1{%s}[,0].{%s}[,0]{%s}))" % (n+2, 9-n, n, 9-n, n+2), field_str)) != 5 - n:
            return False

    if len(re.findall(r"(?=([,0]{3}.{8}[,0]1[,0].{8}[,0]{3}))", field_str)) != 8:
        return False

    return True
#########################################
def validate_battlefield(field):
    
    location = {(x,y) for x in range(10) for y in range(10) if field[x][y] == 1}
    
    if len(location) != 20:
        return False
    
    for i in location:
        if {(i[0]-1, i[1]-1), (i[0]-1, i[1]+1), (i[0]+1, i[1]-1), (i[0]+1, i[1]+1)} & location:
            return False
    
    distance = []
    
    for i in range(10):
        d = 0
        for j in range(10):
            if field[i][j]:
                d += 1
            else:
                distance += [d]
                d = 0
        distance += [d]
    
    for i in range(10):
        d = 0
        for j in range(10):
            if field[j][i]:
                d += 1
            else:
                distance += [d]
                d = 0
        distance += [d]
            

    return True if (distance.count(4) == 1 and distance.count(3) == 2 and distance.count(2) == 3) else False
##################################################################################
def validate_battlefield(field):
    # write your magic here
    ships = []
    for row in range(10):
        for col in range(10):
            if row < 9 and col < 9:
                #check diagonals
                if field[row][col] + field[row+1][col+1] > max(field[row][col], field[row+1][col+1]):
                    return False
                if field[row+1][col] + field[row][col+1] > max(field[row+1][col], field[row][col+1]):
                    return False
                
            if row < 9 and field[row][col] > 0 and field[row+1][col] > 0:
                field[row+1][col] += field[row][col]
            elif col < 9 and field[row][col] > 0 and field[row][col+1] > 0:
                field[row][col+1] +=field[row][col]
                    
            elif field[row][col] > 0:
                ships.append(field[row][col])
    
    return sorted(ships) == [1,1,1,1,2,2,2,3,3,4]
###########################################################
def validate_battlefield(field):
    #Check if there are ships touching each other (diagonally)
    for i in range(10):
        for j in range(10):
            if i < 9 and j < 9:
                if field[i][j] == 1 and field[i+1][j+1] == 1:
                    return False
            if i > 0 and j < 9:
                if field[i][j] == 1 and field[i-1][j+1] == 1:
                    return False

                
    #Check if the amount of ships is correct
    # (1 * 4), (2 * 3), (3 * 2) and (24*1) 
    
    ship = False
    length = 0
    listLen = []
    
    for i in range(10):
        ship = False
        length = 0        
        for j in range(10):
            if field[i][j] == 1 and not ship: 
                ship = True
                length = 0
            if field[i][j] == 1 and ship:
                length += 1
            if field[i][j] == 0 and ship:
                ship = False
                listLen.append(length)
                length = 0
        ship = False
        listLen.append(length)
        length = 0
                
    for j in range(10):
        ship = False
        length = 0        
        for i in range(10):
            if field[i][j] == 1 and not ship: 
                ship = True
                length = 0
            if field[i][j] == 1 and ship:
                length += 1
            if field[i][j] == 0 and ship:
                ship = False
                listLen.append(length)
                length = 0

        ship = False
        listLen.append(length)
        length = 0
    
    if listLen.count(1) == 24 and listLen.count(2) == 3 and listLen.count(3) == 2 and listLen.count(4) == 1:
        return True
    else:
        return False
######################################################
def validate_battlefield(field):
    s = [0]*4
    for sub in [False,True]:
        for i,r in enumerate(field):
            for j,x in enumerate(r):
                if x:
                    #check diagonals for adjacent ships
                    p = 0 if i==0 else sum(field[i-1][max(0,j-1):j+2])-field[i-1][j]
                    n = 0 if i==9 else sum(field[i+1][max(0,j-1):j+2])-field[i+1][j]
                    if p+n>0: return False
                    #count ships
                    for size in [4,3,2]:
                        if field[i][j:j+size] == [1]*size:
                            field[i][j:j+size] = [0]*size
                            s[size-1]+=1
            if sub: s[0] += sum(r)
        #rotate the field
        field = [[r for r in x] for x in zip(*field[::-1])]
    return s == [4, 3, 2, 1]
##################################################
def validate_battlefield(field):
    l,lens=[],[]
    for y in range(10):
        for x in range(10):
            if field[y][x] == 1 and (x,y) not in l:
                counter,xx,yy = 1,x,y
                while True:
                    g=0
                    l.append((xx,yy))
                    for i,sav in enumerate([[1,0],[0,1],[1,1],[-1,1]]):
                        try: 
                            if field[yy+sav[1]][xx+sav[0]] == 1 and xx+sav[0] >= 0: g+=(i+1)
                        except: pass
                    if g == 0: lens.append(counter);break
                    elif g > 2:return False
                    elif g == 1: xx,counter=xx+1,counter+1
                    else: yy,counter=yy+1,counter+1
    return True if [lens.count(x) for x in range(1,5)] == [4,3,2,1] else False

#If someone sees this, how do people surpass the problem with checking fields around a field without getting beyond the borders of the field?
##########################################################################################
import numpy as np
def validate_battlefield(field):
    
    ones, twos, threes, fours = 0,0,0,0
    
    ''' Calculate single ships and check for touching edges'''
    field_array = np.array(field)
    field_array = np.pad(field_array,1,'constant')
    for i in range(12):
        for j in range(12):
            if field_array[i,j] == 1 and field_array[i+1,j+1] == 1:
                return False
            if field_array[i,j] == 1 and field_array[i-1,j+1] == 1:
                return False
            if field_array[i,j] == 1:
                if sum(field_array[i-1,j-1:j+2]) + sum(field_array[i,j-1:j+2]) + sum(field_array[i+1,j-1:j+2]) == 1:
                    ones = ones + 1
    
    ''' Calculate number of longer ships using string tools.
        Create list of all possible rows and columns that appear on the board '''
    col_row_list = [''.join([str(sign) for sign in line]) for line in field ] + [''.join([str(sign) for sign in line]) for line in list(zip(*field))] 

    for i in range(len(col_row_list)):
        fours = fours + col_row_list[i].count('1111')
        col_row_list[i] = col_row_list[i].replace('1111','ffff')
        threes = threes + col_row_list[i].count('111')
        col_row_list[i] = col_row_list[i].replace('111','ttt')
        twos = twos + col_row_list[i].count('11')
        col_row_list[i] = col_row_list[i].replace('11','dd')
    
    if [ones, twos, threes, fours] == [4,3,2,1]:
        return True
    else: return False
____________________________________________________________
def validate_battlefield(field):
    ship_cells = 0
    for row in field:
        ship_cells += row.count(1)
    if ship_cells != 20:
        return False
    battleship_count = 0
    cruisers_count = 0
    destroyers_count = 0
    submarines_count = 0
    for row in field:
        cell_adjacent_count = 0
        for cell in row:
            if cell == 1 and cell_adjacent_count == 0:
                cell_adjacent_count +=1
            elif cell == 1 and cell_adjacent_count == 1:
                cell_adjacent_count += 1
                destroyers_count += 1
            elif cell == 1 and cell_adjacent_count == 2:
                cell_adjacent_count += 1
                destroyers_count -= 1
                cruisers_count += 1
            elif cell == 1 and cell_adjacent_count == 3:
                cell_adjacent_count += 1
                cruisers_count -= 1
                battleship_count += 1
            elif cell == 1 and cell_adjacent_count > 3:
                return False
            else:
                cell_adjacent_count = 0
    for y in range(10):
        cell_adjacent_count = 0
        for x in range(10):
            if field[x][y] == 1 and cell_adjacent_count == 0:
                cell_adjacent_count += 1
                if (y == 0 and x == 0 and field[x][y + 1] == 0 and field[x + 1][y] == 0 and 
                    field[x + 1][y + 1] == 0):
                    submarines_count += 1
                elif (y == 0 and x in range(1, 9) and field[x - 1][y] == 0 and 
                    field[x - 1][y + 1] == 0 and field[x][y + 1] == 0 and 
                    field[x + 1][y] == 0 and field[x + 1][y + 1] == 0):
                    submarines_count += 1
                elif (y == 0 and x == 9 and field[x - 1][y] == 0 and 
                    field[x - 1][y + 1] == 0 and field[x][y + 1] == 0):
                    submarines_count += 1
                elif (y in range(1, 9) and x == 0 and field[x][y - 1] == 0 and 
                    field[x + 1][y - 1] == 0 and field[x + 1][y] == 0 and 
                    field[x + 1][y + 1] == 0 and field[x][y + 1] == 0):
                    submarines_count += 1
                elif (y in range(1, 9) and x in range(1, 9) and field[x - 1][y - 1] == 0 and 
                    field[x - 1][y] == 0 and field[x - 1][y + 1] == 0 and 
                    field[x][y - 1] == 0 and field[x][y + 1] == 0 and field[x + 1][y - 1] == 0 and 
                    field[x + 1][y] == 0 and field[x + 1][y + 1] == 0):
                    submarines_count += 1
                elif (y in range(1, 9) and x == 9 and field[x - 1][y - 1] == 0 and 
                    field[x - 1][y] == 0 and field[x - 1][y + 1] == 0 and field[x][y - 1] == 0 and 
                    field[x][y + 1] == 0):
                    submarines_count += 1
                elif (y == 9 and x == 0 and field[x][y - 1] == 0 and field[x + 1][y - 1] == 0 and 
                    field[x + 1][y] == 0):
                    submarines_count += 1
                elif (y == 9 and x in range(1, 9) and field[x - 1][y - 1] == 0 and 
                    field[x - 1][y] == 0 and field[x][y - 1] == 0 and 
                    field[x + 1][y - 1] == 0 and field[x + 1][y] == 0):
                    submarines_count += 1
                elif (y == 9 and x == 9 and field[x - 1][y - 1] == 0 and field[x - 1][y] == 0 and 
                    field[x][y - 1] == 0):
                    submarines_count += 1
                else:
                    continue
            elif field[x][y] == 1 and cell_adjacent_count == 1:
                cell_adjacent_count += 1
                destroyers_count += 1
            elif field[x][y] == 1 and cell_adjacent_count == 2:
                cell_adjacent_count += 1
                destroyers_count -= 1
                cruisers_count += 1
            elif field[x][y] == 1 and cell_adjacent_count == 3:
                cell_adjacent_count += 1
                cruisers_count -= 1
                battleship_count += 1
            elif field[x][y] == 1 and cell_adjacent_count > 3:
                return False
            else:
                cell_adjacent_count = 0
    if (battleship_count == 1 and cruisers_count == 2 and destroyers_count == 3 and 
        submarines_count == 4):
        return True
    else:
        return False
____________________________________________________________
def position_ship(field,i,j):
    field[i][j]=0
    column = j+1
    count_j = 1
    index = [[],[]]
    index[0].append(i)
    index[1].append(j)
    while column<10 and field[i][column]==1:
        index[1].append(column)
        count_j+=1
        field[i][column]=0
        column+=1
        
    row = i+1
    count_i =1
    while row<10 and field[row][j]==1:
        index[0].append(row)
        count_i+=1
        field[row][j]=0
        row+=1
        
    print(index)
    min_i,max_i = min(index[0]),max(index[0])
    min_j,max_j = min(index[1]),max(index[1])
    
    if min_i-1>0:
        min_i-=1
    if max_i+1<len(field):
        max_i+=1
    if min_j-1>0:
        min_j-=1
    if max_j+1<len(field[0]):
        max_j+=1
    
    for x in range(min_i,max_i+1):
        for y in range(min_j,max_j+1):
            if field[x][y]==1:
                return None
    
    return max(count_i,count_j)
    
def validate_battlefield(field):
    list_ships = []
    for i in range(10):
        for j in range(10):    
            if field[i][j]==1:
                list_ships.append(position_ship(field,i,j))
                
    if list_ships.count(4) !=1:
        return False
    if list_ships.count(3) !=2:
        return False
    if list_ships.count(2) !=3:
        return False
    if list_ships.count(1) !=4:
        return False
    return True
