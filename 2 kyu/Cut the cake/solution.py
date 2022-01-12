import re
import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level='INFO')


logger = logging.getLogger('cutCake')

def cut(cake):
    # coding and coding...
    num = len(re.findall('o', cake))

    cake_array = cake.split()

    rows = len(cake_array)
    columns = len(cake_array[0])

    size = (rows * columns) / num

    result = run(cake_array, size, [])
    return map(lambda row: '\n'.join(row), result)


def run(cake, size, slices):
    logging.debug('-'*20)
    logging.debug('RUN, size = {}, slices = {}'.format(size, slices))
    logging.debug('cake %s', cake)

    corner = findFirstTopLeftCorner(cake)
    logging.debug('Corner %s', corner)

    if not corner:
        return slices

    x = corner[0]
    y = corner[1]

    for width in xrange(len(cake[0]), 1, -1):
        for height in xrange(1, len(cake) + 1):
            if width*height != size:
                logging.debug('Size {} != {} with width={} height={}'.format(width*height, size, width, height))
                continue

            slice = isValidSlice(cake, x, y, width, height)

            if not slice:
                logging.debug('Slice is not valid width={} height={}'.format(width, height))
                continue

            newSlices = slices[:]
            newSlices.append(slice)

            newCake = doCut(cake[:], x, y, width, height)

            result = run(newCake, size, newSlices)

            if result:
                logging.debug('Found %s', result)
                return result

    logging.debug('Not found')
    return []


def findFirstTopLeftCorner(cake):
    for i, row in enumerate(cake):
        for j, cell in enumerate(row):
            if cell != 'x':
                return i, j

    return None


def isValidSlice(cake, x, y, width, height):
    if x + height > len(cake):
        logging.debug('x {} > {}'.format(x + height, len(cake)))
        return False

    if y + width > len(cake[0]):
        logging.debug('y {} > {}'.format(y + width, len(cake[0])))
        return False

    logging.debug('Trying with x={}, y={}, width={}, height={}'.format(x, y, width, height))

    slice = map(lambda row: row[y:y+width], cake[x:x+height])

    logging.debug('The slice is %s', slice)

    slice_str = ''.join(slice)

    if re.findall('x', slice_str):
        logging.debug('Already cut')
        return False

    numberOfO = len(re.findall('o', slice_str))
    if numberOfO != 1:
        logging.debug('Invalid number of o = %s', numberOfO)
        return False

    return slice


def doCut(cake, x, y, width, height):
    logging.debug('Cutting x={}, y={}, width={}, height={}'.format(x, y, width, height))
    logging.debug('Cake %s', cake)
    for i in xrange(x, x+height):
        for j in xrange(y, y+width):
            cake_str = list(cake[i])
            cake_str[j] = 'x'
            cake[i] = ''.join(cake_str)

    return cake

_____________________________________________________
import copy
def cut(cccc):
    global scake
    class cake:
        def __init__(self, cake):
            self.map = [[p for p in row] for row in cake.split('\n')]
            self.height = len(self.map)
            self.length = len(self.map[0])

        def beginningcake(self):
            self.r = 0
            for row in self.map:
                for n in row:
                    if n == 'o':
                        self.r += 1
            self.size = self.height * self.length
            self.cutsize = int(self.size / self.r)
            # get possiblecuts for sizec
            self.possiblecuts = []
            for n in range(1, int(self.cutsize ** 0.5) + 1):
                if self.cutsize % n == 0:
                    if int(self.cutsize / n) <= self.length:
                        self.possiblecuts.append([n, int(self.cutsize / n)])
                    if int(self.cutsize / n) <= self.height:
                        if n ** 2 != self.cutsize:
                            self.possiblecuts.append([int(self.cutsize / n), n])
        # get starting location
        def startloc(self):
            for row in range(self.height):
                for col in range(self.length):
                    if self.map[row][col] != '0':
                        return [row, col]

        def cakecut(self, coord, cut):
            tempmap = copy.deepcopy(self.map)
            cakepiece = []
            for row in range(cut[0]):
                cakepiece.append([])
                for col in range(cut[1]):
                    cakepiece[row].append(tempmap[coord[0] + row][coord[1] + col])
                    tempmap[coord[0] + row][coord[1] + col] = '0'
            return cake('\n'.join([''.join(row) for row in tempmap])), '\n'.join([''.join(row) for row in cakepiece])
    # checks that the cut only has 1 raisin
    def rcheck(coord, cut, cake):
        r = 0
        for row in range(cut[0]):
            for col in range(cut[1]):
                try:
                    if cake.map[coord[0] + row][coord[1] + col] in ['0','o']:
                        r += 1
                except:
                    return False
        if r == 1:
            return True
        return False
    scake = cake(cccc)
    scake.beginningcake()
    #go from the top right corner
    def getonecut(cuts, c):
        global scake
        # find starting location of cake
        l = c.startloc()
        countc = len(cuts)
        for cut in scake.possiblecuts:
            # try to hit a raisin
            s = rcheck(l,cut,c)
            if s == True:
                tempcake, cut = c.cakecut(l, cut)
                if countc == scake.r - 1:
                    return cuts + [cut]
                st = getonecut(cuts + [cut],tempcake)
                if st == []:
                    continue
                else:
                    return st
        return []
    return getonecut([],scake)
  
_____________________________________________________
def cut(cake):
    c,o=cake.split("\n"),[]
    cl,ch=len(c[0]),len(c)
    r=[(i,j) for i in range(ch) for j in range(cl) if c[i][j]=="o"]
    if (cl*ch)%len(r)!=0:
        return([])
    ps=(cl*ch)//len(r)
    f=[i for i in range(cl,0,-1) if ps%i==0]
    def cutt():
        if len(o)==len(r):
            return(True)
        fo=0
        for i in range(ch):
            for j in range(cl):
                if all([(i,j) not in k for k in o]):
                    y,x=i,j
                    fo=1
                    break
            if fo==1:
                break
        for l in f:
            h=ps//l
            if y+h<=ch and x+l<=cl:
                cp=[(i,j) for i in range(y,y+h) for j in range(x,x+l)]
                rp=[(i,j) for i,j in r if (i,j) in cp]
                if len(rp)==1 and all([(i,j) not in k for k in o for i,j in cp]):
                    o.append(cp+[(l,h,rp[0][0]-y,rp[0][1]-x)])
                    if cutt():
                        return(True)
                    del o[-1]
        return(False)
    if cutt():
        oo=[]
        for l,h,ry,rx in [a[-1] for a in o]:
            ocp=(("."*l+"\n")*h)[:-1]
            rp=ry*(l+1)+rx
            ocp=ocp[:rp]+"o"+ocp[rp+1:]
            oo.append(ocp)
        return(oo)
    else:
        return []
      
_____________________________________________________
import numpy as np


POSSIBLE_SLICES = []
MAX_CUTS = 0
BRANCHES = []


def possible_cuts(cake_array, cutting, cut_number=1):
    for slice_ in POSSIBLE_SLICES:
        arr = cake_array.copy()
        start = tuple(zip(*np.nonzero(arr)))[0] if tuple(zip(*np.nonzero(arr))) else None
        if start:
            array_counter = dict(zip(*np.unique(arr[start[0]: start[0]+slice_[0], start[1]: start[1]+slice_[1]], return_counts=True)))
            if array_counter.get('o', 0) == 1 and array_counter.get('.', 0) == slice_[0] * slice_[1] - 1:
                slice_str = '\n'.join(''.join(lst) for lst in arr[start[0]: start[0]+slice_[0], start[1]: start[1]+slice_[1]])
                arr[start[0]: start[0]+slice_[0], start[1]: start[1]+slice_[1]] = ''
                cutting_copy = cutting.copy()
                cutting_copy.append(slice_str)
                if cut_number >= MAX_CUTS:
                    BRANCHES.append(cutting_copy)
                possible_cuts(arr, cutting_copy, cut_number+1)


def cut(cake):
    if not cake: return []
    global MAX_CUTS, POSSIBLE_SLICES, BRANCHES
    BRANCHES = []
    cake_arr = np.array([list(s) for s in cake.split('\n')])
    MAX_CUTS = np.char.count(cake_arr, 'o').sum()
    slice_square = cake_arr.shape[0] * cake_arr.shape[1] // MAX_CUTS
    POSSIBLE_SLICES = [(x,  slice_square // x) for x in range(1, slice_square+1) if slice_square % x == 0]
    POSSIBLE_SLICES = [(x, y) for x, y in POSSIBLE_SLICES if (x <= cake_arr.shape[0] and y <= cake_arr.shape[1])]
    cutting = []
    possible_cuts(cake_arr, cutting)
    return BRANCHES[0] if BRANCHES else []
  
_____________________________________________________
from functools import cmp_to_key

class Cake():
    def __init__(self, string):
        self.matrix = string_to_matrix(string)
        self.rows = len(self.matrix) 
        self.cols = len(self.matrix[0])
        self.raisins = find_raisins(self.matrix, self.rows, self.cols)
        
    def __str__(self):
        cake_str=""
        cake_str+="Matrix:\n"
        for r in self.matrix:
            for c in r:
                cake_str+=c
            cake_str+="\n"
        return cake_str  
    
class Area():
    def __init__(self, r_s, c_s, r_e, c_e):
        self.r_s = r_s
        self.c_s = c_s
        self.r_e = r_e
        self.c_e = c_e
        
    def num_contained(self, array):
        count=0
        for el in array:
            if el[0]>=self.r_s and el[0]<=self.r_e and el[1]>=self.c_s and el[1]<=self.c_e:
                count += 1
        return count
    
    def delete_raisin(self, raisins):
        for el in raisins:
            if el[0]>=self.r_s and el[0]<=self.r_e and el[1]>=self.c_s and el[1]<=self.c_e:
                raisins.remove(el)
                break
        return raisins

    
    def __str__(self):
        return "R_S: "+ str(self.r_s)+ " R_E: "+ str(self.r_e)+ " C_S: "+ str(self.c_s) +" C_E: "+ str(self.c_e)
                 
def string_to_matrix(string):
    matrix = []
    r = []
    for i in range(len(string)):
        if string[i]=="\n":
            matrix.append(r.copy())
            r = []
        else:
            r.append(string[i])
    matrix.append(r)
    return matrix
        
def find_raisins(matrix, rows, cols):
    raisins = []
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 'o':
                raisins.append([r,c])
    return raisins

def copy_matrix(matrix):
    copied_matrix = []
    for r in matrix:
        copied_matrix.append(r.copy())
    return copied_matrix

def print_matrix(matrix):
    for r in matrix:
        row_str = ""
        for c in r:
            row_str+=c
        print(row_str + "\n")
    print("\n")

def is_matrix_empty(matrix):
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c]!='x':
                return False
    return True

def delete_area(matrix, area):
    for r in range(area.r_s, area.r_e+1):
        for c in range(area.c_s, area.c_e+1):
            matrix[r][c]='x'

def possible_areas(matrix, raisins, rows, cols, size):
    areas = []
    exit = False
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c]!='x':
                for i in range(c+1,cols+1):
                    if size%(i-c)==0 and (size/(i-c))-1+r<rows:# and (i-c)*(int(size/(i-c)))==size:
                        area = Area(r, c, int(size/(i-c))-1+r, i-1)
                        if area.num_contained(raisins) == 1:
                            areas.append(area)
                exit = True
                break
        if exit:
            break
            
    return areas      

def copy_areas(areas):
    copied_areas = []
    for area in areas:
        sub_copied_area = []
        for sub_area in area:
            sub_copied_area.append(Area(sub_area.r_s, sub_area.c_s, sub_area.r_e, sub_area.c_e))
        copied_areas.append(sub_copied_area)
    return copied_areas
            

def get_areas(matrix, raisins, rows, cols, size, area_map={}):
    if str(matrix) in area_map:
        return [area_map[str(matrix)][0], copy_areas(area_map[str(matrix)][1])]
    if len(raisins)==0:
        return [is_matrix_empty(matrix),[]]
    else: 
        right_areas = []
        areas = possible_areas(matrix, raisins, rows, cols, size)
        print_matrix(matrix)
        for area in areas:
            copied_matrix = copy_matrix(matrix)
            copied_raisins = raisins.copy()
            delete_area(copied_matrix, area)
            area.delete_raisin(copied_raisins)
            print_matrix(copied_matrix)
            sub_call = get_areas(copied_matrix, copied_raisins, rows, cols, size, area_map)
            if sub_call[0]:
                for sub_area in sub_call[1]:
                    sub_area.append(area)
                if(len(sub_call[1])==0):
                    sub_call[1].append(area)
                    right_areas.append(sub_call[1])
                else:
                    right_areas += sub_call[1]
        if len(right_areas)>0:
            area_map[str(matrix)] = [True, copy_areas(right_areas)]
            return True, right_areas
        else:
            area_map[str(matrix)] = [False, []]
            return False, []
        
def min_area(areas):
    max_area = 0
    for area in range(len(areas)):
        for sub_area in reversed(range(len(areas[area]))):
            if areas[area][sub_area].c_e > areas[max_area][sub_area].c_e:
                max_area = area
                break
            if areas[area][sub_area].c_e < areas[max_area][sub_area].c_e:
                break
    return areas[max_area]

def convert_area(matrix, areas):
    converted = []
    for area in areas:
        sub_str = ""
        for r in range(area.r_s, area.r_e+1):
            for c in range(area.c_s, area.c_e+1):
                sub_str += matrix[r][c]
            if r!=area.r_e:
                sub_str += "\n"
        converted.append(sub_str)
    return converted

def compare_areas(area1, area2):
    if area1.r_s > area2.r_s:
        return 1
    elif area1.r_s < area2.r_s:
        return -1
    elif area1.c_s > area2.c_s:
        return 1
    else:
        return -1
            
def cut(matrix):
    cake = Cake(matrix)
    [b, areas] = get_areas(cake.matrix, cake.raisins, cake.rows, cake.cols, int(cake.rows*cake.cols/len(cake.raisins)))
    if b:
        sorted_area = min_area(areas)
        sorted_area.sort(key=cmp_to_key(compare_areas))
        converted_area = convert_area(cake.matrix, sorted_area)
        return converted_area
    else:
        return []
      
_____________________________________________________
from functools import cmp_to_key

class Cake():
    def __init__(self, string):
        self.matrix = string_to_matrix(string)
        self.rows = len(self.matrix) 
        self.cols = len(self.matrix[0])
        self.raisins = find_raisins(self.matrix, self.rows, self.cols)
        
    def __str__(self):
        cake_str=""
        cake_str+="Matrix:\n"
        for r in self.matrix:
            for c in r:
                cake_str+=c
            cake_str+="\n"
        return cake_str  
    
class Area():
    def __init__(self, r_s, c_s, r_e, c_e):
        self.r_s = r_s
        self.c_s = c_s
        self.r_e = r_e
        self.c_e = c_e
        
    def num_contained(self, array):
        count=0
        for el in array:
            if el[0]>=self.r_s and el[0]<=self.r_e and el[1]>=self.c_s and el[1]<=self.c_e:
                count += 1
        return count
    
    def delete_raisin(self, raisins):
        for el in raisins:
            if el[0]>=self.r_s and el[0]<=self.r_e and el[1]>=self.c_s and el[1]<=self.c_e:
                raisins.remove(el)
                break
        return raisins

    
    def __str__(self):
        return "R_S: "+ str(self.r_s)+ " R_E: "+ str(self.r_e)+ " C_S: "+ str(self.c_s) +" C_E: "+ str(self.c_e)
                 
def string_to_matrix(string):
    matrix = []
    r = []
    for i in range(len(string)):
        if string[i]=="\n":
            matrix.append(r.copy())
            r = []
        else:
            r.append(string[i])
    matrix.append(r)
    return matrix
        
def find_raisins(matrix, rows, cols):
    raisins = []
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 'o':
                raisins.append([r,c])
    return raisins

def copy_matrix(matrix):
    copied_matrix = []
    for r in matrix:
        copied_matrix.append(r.copy())
    return copied_matrix

def print_matrix(matrix):
    for r in matrix:
        row_str = ""
        for c in r:
            row_str+=c
        print(row_str + "\n")
    print("\n")

def is_matrix_empty(matrix):
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c]!='x':
                return False
    return True

def delete_area(matrix, area):
    for r in range(area.r_s, area.r_e+1):
        for c in range(area.c_s, area.c_e+1):
            matrix[r][c]='x'

def possible_areas(matrix, raisins, rows, cols, size):
    areas = []
    exit = False
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c]!='x':
                for i in range(c+1,cols+1):
                    if size%(i-c)==0 and (size/(i-c))-1+r<rows:# and (i-c)*(int(size/(i-c)))==size:
                        area = Area(r, c, int(size/(i-c))-1+r, i-1)
                        if area.num_contained(raisins) == 1:
                            areas.append(area)
                exit = True
                break
        if exit:
            break
            
    return areas      

def copy_areas(areas):
    copied_areas = []
    for area in areas:
        sub_copied_area = []
        for sub_area in area:
            sub_copied_area.append(Area(sub_area.r_s, sub_area.c_s, sub_area.r_e, sub_area.c_e))
        copied_areas.append(sub_copied_area)
    return copied_areas
            

def get_areas(matrix, raisins, rows, cols, size, area_map={}):
    if str(matrix) in area_map:
        print("RAIS ", raisins)
        return [area_map[str(matrix)][0], copy_areas(area_map[str(matrix)][1])]
    if len(raisins)==0:
        return [is_matrix_empty(matrix),[]]
    else: 
        right_areas = []
        areas = possible_areas(matrix, raisins, rows, cols, size)
        print_matrix(matrix)
        for area in areas:
            copied_matrix = copy_matrix(matrix)
            copied_raisins = raisins.copy()
            delete_area(copied_matrix, area)
            area.delete_raisin(copied_raisins)
            print_matrix(copied_matrix)
            sub_call = get_areas(copied_matrix, copied_raisins, rows, cols, size, area_map)
            if sub_call[0]:
                for sub_area in sub_call[1]:
                    sub_area.append(area)
                if(len(sub_call[1])==0):
                    sub_call[1].append(area)
                    right_areas.append(sub_call[1])
                else:
                    right_areas += sub_call[1]
        if len(right_areas)>0:
            area_map[str(matrix)] = [True, copy_areas(right_areas)]
            return True, right_areas
        else:
            area_map[str(matrix)] = [False, []]
            return False, []
        
def min_area(areas):
    max_area = 0
    for area in range(len(areas)):
        print(len(areas[area]))
        print(len(areas[max_area]))
        for sub_area in reversed(range(len(areas[area]))):
            if areas[area][sub_area].c_e > areas[max_area][sub_area].c_e:
                max_area = area
                break
            if areas[area][sub_area].c_e < areas[max_area][sub_area].c_e:
                break
    print(max_area)
    return areas[max_area]

def convert_area(matrix, areas):
    converted = []
    for area in areas:
        sub_str = ""
        for r in range(area.r_s, area.r_e+1):
            for c in range(area.c_s, area.c_e+1):
                sub_str += matrix[r][c]
            if r!=area.r_e:
                sub_str += "\n"
        converted.append(sub_str)
    return converted

def compare_areas(area1, area2):
    if area1.r_s > area2.r_s:
        return 1
    elif area1.r_s < area2.r_s:
        return -1
    elif area1.c_s > area2.c_s:
        return 1
    else:
        return -1
            
def cut(matrix):
    cake = Cake(matrix)
    [b, areas] = get_areas(cake.matrix, cake.raisins, cake.rows, cake.cols, int(cake.rows*cake.cols/len(cake.raisins)))
    if b:
        sorted_area = min_area(areas)
        sorted_area.sort(key=cmp_to_key(compare_areas))
        converted_area = convert_area(cake.matrix, sorted_area)
        return converted_area
    else:
        return []

_____________________________________________________
class Cutter:
    """
    Tries to cut cake recursively using backtracking algorithm
    """
    def __init__(self, cake, pieceSize):
        self.__cake = cake
        self.__pSize = pieceSize
        
    def __cut(self, cake):
        # If cake is already a correct piece return it
        if len(''.join(l.strip() for l in cake)) == self.__pSize:
            if not all(len(l.strip())==self.__pSize/len(cake) for l in cake) or \
                ''.join(cake).count('o') != 1:
                return None
            return ['\n'.join(l.strip() for l in cake)]
        res = []
        # Begin and end cols for piece
        colBegin = [c == ' ' for c in cake[0]].index(False)
        colEnd = len(cake[0])
        for rows in range(len(cake)):
            # Get current piece size
            pSize = len(''.join(l[colBegin:colEnd] for l in cake[:rows+1]))
            # If current piece size is bigger than required decrease end column of a piece
            if pSize > self.__pSize:
                while pSize > self.__pSize and colEnd > 0:
                    colEnd -= 1
                    pSize = len(''.join(l[colBegin:colEnd] for l in cake[:rows+1]))
            # If piece is of desired size try to cut it
            if pSize == self.__pSize:
                # Get current piece
                piece = [l[colBegin:colEnd] for l in cake[:rows+1]]
                # Check if piece is valid
                if  ''.join(piece).count('o') != 1:
                    continue
                if not all(len(l)==pSize/len(piece) for l in piece):
                    continue
                # Create cake without current piece to pass to the next cut call
                nCake = [l[:colBegin] + ''.join(' ' for i in range(colEnd-colBegin)) + l[colEnd:] for l in cake[:rows+1]]
                nCake = [l for l in nCake if len(l.strip()) > 0]
                nCake.extend(cake[rows+1:])
                # Try to cut remaining pieces
                nextRes = self.__cut(nCake)
                # If cut was successfull return all pieces
                if nextRes is not None:
                    res.append('\n'.join(l[colBegin:colEnd] for l in cake[:rows+1]))
                    res.extend(nextRes)
                    return res
        return None
        
    def cut(self):
        res = self.__cut(self.__cake)
        if not res:
            return []
        return res

def cut(cake):
    n = cake.count('o')
    cake = cake.split('\n')
    pSize = len(cake) * len(cake[0]) / n
    cutter = Cutter(cake, pSize)
    return cutter.cut()
  
_____________________________________________________
class Cutter:
    def __init__(self, cake, raisinNum, pieceSize):
        self.__cake = cake
        self.__rNum = raisinNum
        self.__pSize = pieceSize
        
    def __cut(self, cake):
        if len(''.join(l.strip() for l in cake)) == self.__pSize:
            if not all(len(l.strip())==self.__pSize/len(cake) for l in cake):
                return None
            return ['\n'.join(l.strip() for l in cake)]
        res = []
        cols = len(cake[0])
        begin = [c == ' ' for c in cake[0]].index(False)
        for rows in range(len(cake)):
            pSize = len(''.join(l[begin:cols] for l in cake[:rows+1]).strip())
            if pSize > self.__pSize:
                while pSize > self.__pSize and cols > 0:
                    cols -= 1
                    pSize = len(''.join(l[begin:cols] for l in cake[:rows+1]).strip())
            if pSize == self.__pSize:
                piece = [l[begin:cols].strip() for l in cake[:rows+1]]
                if  ''.join(piece).count('o') != 1:
                    continue
                nCake = [l[:begin] + ''.join(' ' for i in range(cols-begin)) + l[cols:] for l in cake[:rows+1]]
                nCake = [l for l in nCake if len(l.strip()) > 0]
                nCake.extend(cake[rows+1:])
                nextRes = self.__cut(nCake)
                if nextRes is not None:
                    res.append('\n'.join(l[begin:cols].strip() for l in cake[:rows+1]))
                    res.extend(nextRes)
                    return res
        return None
        
    def cut(self):
        res = self.__cut(self.__cake)
        if not res:
            return []
        return res

def cut(cake):
    # coding and coding...
    n = cake.count('o')
    cake = cake.split('\n')
    pSize = len(cake) * len(cake[0]) / n
    cutter = Cutter(cake, n, pSize)
    print(cake)
    print(pSize)
    return cutter.cut()
  
_____________________________________________________
class Cutter:
    def __init__(self, cake, raisinNum, pieceSize):
        self.__cake = cake
        self.__rNum = raisinNum
        self.__pSize = pieceSize
        
    def __cut(self, cake):
        if not cake or len(cake) == 0:
            return None
        if len(''.join(l.strip() for l in cake)) == self.__pSize:
            if not all(len(l.strip())==self.__pSize/len(cake) for l in cake):
                return None
            return ['\n'.join(l.strip() for l in cake)]
        res = []
        cols = len(cake[0])
        begin = [c == ' ' for c in cake[0]].index(False)
        for rows in range(len(cake)):
            pSize = len(''.join(l[begin:cols] for l in cake[:rows+1]).strip())
            if pSize > self.__pSize:
                while pSize > self.__pSize and cols > 0:
                    cols -= 1
                    pSize = len(''.join(l[begin:cols] for l in cake[:rows+1]).strip())
            if pSize == self.__pSize:
                piece = [l[begin:cols].strip() for l in cake[:rows+1]]
                if  ''.join(piece).count('o') != 1:
                    continue
                if not all(len(l)==pSize/len(piece) for l in piece):
                    continue
                nCake = [l[:begin] + ''.join(' ' for i in range(cols-begin)) + l[cols:] for l in cake[:rows+1]]
                nCake = [l for l in nCake if len(l.strip()) > 0]
                nCake.extend(cake[rows+1:])
                nextRes = self.__cut(nCake)
                if nextRes is not None:
                    res.append('\n'.join(l[begin:cols].strip() for l in cake[:rows+1]))
                    res.extend(nextRes)
                    return res
        return None
        
    def cut(self):
        res = self.__cut(self.__cake)
        if not res:
            return []
        return res

def cut(cake):
    # coding and coding...
    n = cake.count('o')
    cake = cake.split('\n')
    pSize = len(cake) * len(cake[0]) / n
    cutter = Cutter(cake, n, pSize)
    print(cake)
    print(pSize)
    return cutter.cut()
  
_____________________________________________________
def factorization(n) :
    factors = []
    for x in range(1, int(n-1)) :
        a = n / x
        if a == int(a) :
            tuple = (x, int(a))
            factors.append(tuple)
    return factors

def cake_remaining(cake) :
    for y in range(len(cake)):
        for x in range(len(cake[0])):
            if cake[y][x] != '_':
                return True

def position_finder(cake): 
    positions = [len(cake), len(cake[0])]
    for n in range(len(cake)-1, -1, -1) :
            if '.' in cake[n] or 'o' in cake[n] :                  
                positions = [n, min([m for m in range(len(cake[n])) if cake[n][m] != '_'])]
    return positions

def cake_cutting_fct(cake, slice_configuration, cut_start_point):
    y = slice_configuration[0]
    x = slice_configuration[1]
    remaining_cake = []
    slice = []
    raisin_count = 0
    missing_bits = 0
    initial_cake = cake
    cutting_error = False
    
    #Slice creating function
    for n in range(y) : 
        slice_row = []
        for m in range(len(cake[0])) :
            if cut_start_point[1] == 0 :
                if m <= x - 1 :
                    slice_row.append(cake[n + cut_start_point[0]][m])
            if cut_start_point[1] > 0 :    
                if m >= cut_start_point[1] and m <= cut_start_point[1] + x -1 :
                    slice_row.append(cake[n + cut_start_point[0]][m])
        slice.append(''.join(slice_row))
    
    #Remaining cake definition function
    for n in range(len(cake)) : 
        cake_row = []
        if n in range(cut_start_point[0], cut_start_point[0] + y):
            for m in range(len(cake[0])) :
                if m <= cut_start_point[1] + x - 1 and m >= cut_start_point[1] :
                    cake_row.append('_')
                if m > cut_start_point[1] + x - 1 or m < cut_start_point[1]:
                    cake_row.append(cake[n][m])
            cake_row = ''.join(cake_row)
        if n not in range(cut_start_point[0], cut_start_point[0] + y) :
            cake_row = cake[n]
        remaining_cake.append(cake_row)
    
    #Raisin counting function
    for i in slice : 
        for j in i :
            if j == 'o' :
                raisin_count += 1
            if j == '_' :
                missing_bits += 1
    
    #Slice correctness assessement
    if raisin_count != 1 or missing_bits > 0 or len(slice[0]) < x or len(slice) < y: 
        cutting_error = True
        remaining_cake = initial_cake
        slice = []

    return (remaining_cake, slice, cutting_error)

def success_handler(result, operations_log, slice_configuration_index, cake, slice_configurations, positions):
    
    for n in range(0, len(slice_configurations)):
        slice_configuration = slice_configurations[n]
        if slice_configuration[0] + positions[0] <= len(cake) and slice_configuration[1] + positions[1] <= len(cake[0]): #Slice correctness assessement
            return (n, cake, positions, result)
    
        if n == len(slice_configurations) - 1 :
            if operations_log[len(operations_log) - 1]["slice_config_index"] == len(slice_configurations) - 1 :
                operations_log.pop(len(operations_log) - 1)
            slice_configuration_index = len(slice_configurations) - 1
            result = error_handler(result, operations_log, slice_configuration_index, cake, slice_configurations, positions)
            return result

def error_handler(result, operations_log, slice_configuration_index, cake, slice_configurations, positions):
    
    if slice_configuration_index < len(slice_configurations) -1 :
        for n in range(slice_configuration_index + 1, len(slice_configurations)):
            slice_configuration = slice_configurations[n]
            
            if slice_configuration[0] + positions[0] <= len(cake) and slice_configuration[1] + positions[1] <= len(cake[0]):
                return (n, cake, positions, result)
        
        slice_configuration_index = len(slice_configurations) - 1
    
    if slice_configuration_index == len(slice_configurations) - 1 :

        if len(result) == 0 :
            return 'no solution'
    
        if len(operations_log) > 0 :
            
            for l in range(len(operations_log)-1, -1, -1) :
                log = operations_log[l]
                index = log["slice_config_index"]
                
                for n in range(index + 1, len(slice_configurations)):
                    slice_configuration = slice_configurations[n]
                    if slice_configuration[0] + log["position"][0] <= len(cake) and slice_configuration[1] + log["position"][1] <= len(cake[0]):
                        cake = operations_log[l]["cake"]
                        positions = operations_log[l]["position"]
                        result = operations_log[l]["result"]
                        
                        if n == len(slice_configurations) -1 :
                            operations_log.pop(l)
                        else :
                            operations_log[l]["slice_config_index"] = n
                        return (n, cake, positions, result)
                    
                    if n == len(slice_configurations) -1 and l == 0 :
                        return 'no solution'
            
            operations_log.pop(l)
            
        elif len(operations_log) == 0 :
            return 'no solution'

#Main function

def cut(cake):
    #Main cake size and config variables
    number_of_raisins = cake.count('o')
    cake = cake.split('\n')
    cake_length = len(cake)
    cake_width = len(cake[0])
    cake_area = cake_length * cake_width
    slice_area = int(cake_area / number_of_raisins)
    operations_log = []
    result = []
    b = []
    
    #Slices dimenssions, configurations and main program variables
    possible_cake_slices = factorization(slice_area)
    slice_configurations = [tuple for tuple in possible_cake_slices if tuple[0] <= cake_length and tuple[1] <= cake_width]
    slice_configuration_index = 0
    slice_config = slice_configurations[0]
    cutting_error = False
    
    #Cake configuration viability check
    if slice_area * number_of_raisins != cake_area :
        return []
    
    #Main while loop
    while(cake_remaining(cake)) :
        slice = []
        operations_log = operations_log[:len(result)]
        
        #Determining where to do the next cut
        positions = position_finder(cake)
        
        #Success handler
        if len(result) != 0 and cutting_error == False :
            config = success_handler(result, operations_log, slice_configuration_index, cake, slice_configurations, positions)
            slice_configuration_index = config[0]
            cake = config[1]
            positions = config[2]
            result = config[3]
        
        #Error handler
        if cutting_error :
            config = error_handler(result, operations_log, slice_configuration_index, cake, slice_configurations, positions)
            slice_configuration_index = config[0]
            cake = config[1]
            positions = config[2]
            result = config[3]
        
        #If the error handler return "No solution"
        if type(slice_configuration_index) == str:
            return []
            
        #Retrivieing the result of the success or error handler and determining the next viable slice config to try
        if slice_configuration_index <= len(slice_configurations) - 1 :
            slice_config = slice_configurations[slice_configuration_index]
        
        #Adding the new operation in the log
        operation = {
            "cake" : cake.copy(),
            "slice_config" : slice_config,
            "slice_config_index" : slice_configuration_index,
            "position" : positions.copy(),
            "result" : result.copy()
        }  
        if operation["slice_config_index"] < len(slice_configurations) - 1 :
            operations_log.append(operation)
        
        #Cake cutting function call
        cut = cake_cutting_fct(cake, slice_config, positions)

        #Cutting result handling
        cake = cut[0]
        cutting_error = cut[2]
        if len(cut[1]) > 1 :
            slice = '\n'.join(cut[1])
        if len(cut[1]) == 1 :
            slice = cut[1][0]
        if len(slice) != 0 :
            b = result.copy()
            b.append(slice)
            result = b.copy()
        
    return result
  
_____________________________________________________
import math
import bisect

class Piece():
    def __init__(self, r, c, nr, nc):
        self.start_row = r
        self.start_col = c
        self.num_rows = nr
        self.num_cols = nc
        self.end_row = self.start_row +self.num_rows
        self.end_col = self.start_col + self.num_cols

    def data(self):
        return (self.start_row, self.start_col, self.num_rows, self.num_cols)

def output(cake, ans):
    return ["\n".join(row[c:c +nc] for row in cake[r:r + nr]) for r, c, nr, nc in ans]

def one_raisin(cake, piece):
    v = sum(row[piece.start_col:piece.end_col].count("o") for row in cake[piece.start_row:piece.end_row])
    return v == 1

def can_take(piece, taken):
    for r in range(piece.start_row, piece.end_row):
        for c in range(piece.start_col, piece.end_col):
            if (r,c) in taken:
                return False
            taken.add((r,c))
    return True

def construct(cake, placements, sizes, cake_rows, cake_cols, taken, current):
    if len(taken) == cake_rows * cake_cols:
        return [piece.data() for piece in current]
    if not placements:
        return []
    #placements.sort()
    for start_row, start_col in placements:
        for sz in sizes:
            piece = Piece(start_row, start_col, sz[0], sz[1])
            taken2 = taken.copy()
            if piece.end_row <= cake_rows and piece.end_col <= cake_cols and one_raisin(cake, piece) and can_take(piece, taken2):
                current.append(piece)
                placements2 = [p for p in placements if p != (start_row, start_col)]
                if piece.end_col < cake_cols: bisect.insort(placements2, (piece.start_row, piece.end_col))
                if piece.end_col < cake_cols and piece.end_row < cake_rows: bisect.insort(placements2, (piece.end_row, piece.end_col))
                if piece.end_row < cake_rows: bisect.insort(placements2, (piece.end_row, piece.start_col))
                ans = construct(cake, placements2, sizes, cake_rows, cake_cols, taken2, current)
                if ans:
                    return ans
                current.pop()
    return []

def cut(cake):
    raisins = cake.count("o")
    cake = cake.split()
    num_rows, num_cols = len(cake), len(cake[0])
    cake_area = num_rows * num_cols

    raisin_area, rem = divmod(cake_area, raisins)
    if rem != 0:
        return []

    sizes = set()
    for f1 in range(int(math.sqrt(raisin_area)), 0, -1):
        f2, rem = divmod(raisin_area, f1)
        if rem == 0:
            if f1 <= num_rows and f2 <= num_cols: sizes.add((f1, f2))
            if f2 <= num_rows and f1 <= num_cols: sizes.add((f2, f1))

    sizes = sorted(list(sizes), key = lambda x:(x[1], x[0]), reverse = True)
    placements = [(0, 0)]
    ans = construct(cake, placements, sizes, num_rows, num_cols, set(), [])
    return output(cake, ans)
