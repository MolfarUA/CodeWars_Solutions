5263c6999e0f40dee200059d


from itertools import product

ADJACENTS = ('08', '124', '2135', '326', '4157', '52468', '6359', '748', '85790', '968')

def get_pins(observed):
    return [''.join(p) for p in product(*(ADJACENTS[int(d)] for d in observed))]
______________________________
adjacents = {
  '1': ['2', '4'],
  '2': ['1', '5', '3'],
  '3': ['2', '6'],
  '4': ['1', '5', '7'],
  '5': ['2', '4', '6', '8'],
  '6': ['3', '5', '9'],
  '7': ['4', '8'],
  '8': ['5', '7', '9', '0'],
  '9': ['6', '8'],
  '0': ['8'],
}

def get_pins(observed):
  if len(observed) == 1:
    return adjacents[observed] + [observed]
  return [a + b for a in adjacents[observed[0]] + [observed[0]] for b in get_pins(observed[1:])]
______________________________
def get_pins(observed):
  map = [['8','0'], ['1','2','4'], ['1','2','3','5'], ['2','3','6'], ['1','4','5','7'], ['2','4','5','6','8'],
         ['3','5','6','9'], ['4','7','8'], ['5','7','8','9','0'], ['6','8','9']]
  return map[int(observed[0])] if len(observed) == 1 else [x + y for x in map[int(observed[0])] for y in get_pins(observed[1:])]
______________________________
from itertools import product


PIN = {'1': ('1', '2', '4'), 
       '2': ('1', '2', '3', '5'), 
       '3': ('2', '3', '6'), 
       '4': ('1', '4', '5', '7'), 
       '5': ('2', '4', '5', '6', '8'), 
       '6': ('5', '6', '9', '3'), 
       '7': ('4', '7', '8'), 
       '8': ('7', '5', '8', '9', '0'), 
       '9': ('6', '8', '9'), '0': ('0', '8')}


def get_pins(observed):
    return [''.join(a) for a in product(*(PIN[b] for b in observed))]
______________________________
from itertools import product

PINS = {'1': '124', '2': '1253', '3': '236', '4': '1457', '5': '24568',
        '6': '3569', '7': '478', '8': '57890', '9': '689', '0': '08'}


def get_pins(observed):
    return list(map(''.join, product(*[PINS[num] for num in observed])))
______________________________
from itertools import product

def get_pins(observed: str):
    keypad = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [None, 0, None]]
    nums = [int(n) for n in observed]
    R = len(keypad[0]) - 1
    N = len(keypad) - 1
    
    memo, coors = {}, []
    for n in nums:
        if n in memo:
            coors.append(memo[n])
            continue
        for i, r in enumerate(keypad):
            if n in r:
                memo[n] = (i, r.index(n))
                coors.append(memo[n])
                break
            
    pos = nums[:]
    for i, (x, y) in enumerate(coors):
        if (x, y) in memo:
            pos[i] = memo[x, y]
            continue
        sub_pos = []
        for (a, b) in [(x, y), (x-1, y), (x, y-1), (x+1, y), (x, y+1)]:
            if a < 0 or b < 0 or a > N or b > R or keypad[a][b] is None:
                continue
            else:
                sub_pos.append(keypad[a][b])
        memo[x, y] = sorted(map(str, sub_pos))
        pos[i] = memo[x, y]
        
    if len(pos) == 1:
        return pos[0]
    return ["".join(prod) for prod in product(*pos)]
______________________________
def get_pins(observed):
    adj = {
        "1": "124",
        "2": "2135",
        "3": "326",
        "4": "4157",
        "5": "52468",
        "6": "6359",
        "7": "748",
        "8": "85790",
        "9": "968",
        "0": "08",
    }
    result = ['']
    for d in observed:
        result = [prefix+c for prefix in result for c in adj[d]]
    return result
______________________________
import itertools
def legal_pos_digits(num):
    match num:
        case "0":
            return ["0", "8"]
        case "1":
            return ["1", "2", "4"]
        case "2":
            return ["2", "1", "3", "5"]
        case "3":
            return ["3", "2", "6"]
        case "4":
            return ["4", "1", "5", "7"]
        case "5":
            return ["5", "2", "4", "6", "8"]
        case "6":
            return ["6", "3", "5", "9"]
        case "7":
            return ["7", "4", "8"]
        case "8":
            return ["8", "0", "5", "7", "9"]
        case "9":
            return ["9", "6", "8"]
            

def get_pins(observed):
    pin_list = [ legal_pos_digits(d) for d in observed]
    pin_list = list((itertools.product(*pin_list)))  
    return ["".join(pin) for pin in pin_list]
______________________________
from itertools import product

def get_pins(observed):
    mydict = {1:"124", 2:"1235", 3:"236", 4:"1457", 5:"24568", 6:"3569", 7:"478", 8:"57890", 9:"698", 0:"80"}
    lst = [mydict[int(i)] for i in observed]
    if len(lst) == 8: prod = list(product(lst[0], lst[1], lst[2], lst[3],lst[4], lst[5], lst[6], lst[7]))
    elif len(lst) == 7: prod = list(product(lst[0], lst[1], lst[2], lst[3],lst[4], lst[5], lst[6]))
    elif len(lst) == 6: prod = list(product(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5]))
    elif len(lst) == 5: prod =  list(product(lst[0], lst[1], lst[2], lst[3], lst[4]))
    elif len(lst) == 4: prod = list(product(lst[0], lst[1], lst[2], lst[3]))
    elif len(lst) == 3: prod = list(product(lst[0], lst[1], lst[2]))
    elif len(lst) == 2: prod = list(product(lst[0], lst[1]))
    elif len(lst) == 1: return lst[0]

    result = []
    for i in prod:
        result.append("".join(i))
    return result
______________________________
from itertools import product
def get_pins(observed):
    vrs = []
    cmb = {'1':['1','2','4'],
           '2':['2','1','3','5'],
           '3':['3','2','6'],
           '4':['4','1','5','7'],
           '5':['5','2','4','6','8'],
           '6':['6','3','5','9'],
           '7':['7','4','8'],
           '8':['8','5','7','9','0'],
           '9':['9','6','8'],
           '0':['0','8']}
    for i in observed:
        vrs.append(cmb[i])
    return list(map(''.join, list(product(*tuple(vrs)))))
______________________________
import itertools

adjacentNumbers = {
    '1': ['1', '2', '4'],
    '2': ['1', '2', '3', '5'],
    '3': ['2', '3', '6'],
    '4': ['1', '4', '5', '7'],
    '5': ['2', '4', '5', '6', '8'],
    '6': ['3', '5', '6', '9'],
    '7': ['4', '7', '8'],
    '8': ['5', '7', '8', '9', '0'],
    '9': ['6', '8', '9'],
    '0': ['0', '8']
}

def get_pins(observed):
    digit = [adjacentNumbers [n] for n in observed]
    digits = list(itertools.product(*digit))
    combinedDigits = [''.join(n) for n in digits]
    return combinedDigits
______________________________
from itertools import product

possible_keys = {
    '1': (1, 2, 4),
    '2': (2, 1, 5, 3),
    '3': (3, 2, 6),
    '4': (4, 1, 5, 7),
    '5': (5, 2, 4, 6, 8),
    '6': (6, 3, 5, 9),
    '7': (7, 4, 8),
    '8': (8, 0, 5, 7, 9),
    '9': (9, 6, 8),
    '0': (0, 8)
}

def get_pins(observed):
    # Just return the possible keys
    if len(observed) == 1:
        return convert_to_string(possible_keys[observed])
    # Build a list of possible key lists
    all_keys = [possible_keys[number] for number in observed]
    # Find all possible combinations from possible keys, convert to str and join
    return [''.join(convert_to_string(pin)) for pin in product(*all_keys)]

def convert_to_string(num_list):
    # Convert a list from integers to list of number strings
    return [str(num) for num in num_list]
