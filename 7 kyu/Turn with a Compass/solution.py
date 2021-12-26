def direction(facing:str, turn:int) -> str:
    dirs = ["N","NE","E","SE","S","SW","W","NW"]
    return dirs[(dirs.index(facing) + turn//45)%8]

#################
DIRECTIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']


def direction(facing, turn):
    return DIRECTIONS[(turn // 45 + DIRECTIONS.index(facing)) % 8]
  
################
direction = lambda f, t: (D:=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])[(D.index(f)*45+t)//45%8]

################
def direction(facing, turn):
    compass = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    return compass[(compass.index(facing) + turn//45) % 8]
  
################
d="N NE E SE S SW W NW".split();direction=lambda f,t:d[d.index(f)+t//45&7]

###################
def direction(facing, turn):
    dirs = 'N NE E SE S SW W NW'.split()
    return dirs[(dirs.index(facing) + turn//45) % 8]
  
###################
points, directions = [dict() for _ in range(2)]

def get_values():
    cardinal_points = ("N", "E", "S", "W", "N")
    x, y, rotations = 0, -1, -1
    for i in range(0, 360, 45):
        if (rotations := (rotations + 1)) % 2 == 0: y += 1
        else: x += 1
        new_move = ''.join(sorted(set(cardinal_points[x]+cardinal_points[y]), key = lambda x: cardinal_points.index(x)%2))
        points[new_move] = i
        directions[i] = new_move

get_values()

def direction(facing, turn):
    
    position = (points[facing] + turn) % 360
    return directions[position]
  
###################
DIRECTIONS = 'N NE E SE S SW W NW'.split()

def direction(facing, turn):
    i = DIRECTIONS.index(facing)
    i = (i + turn // 45) % 8
    return DIRECTIONS[i]
  
###################
def direction(facing, turn):
    dir = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ping = int((abs(turn) % 360) / 45)
    idx = dir.index(facing) 
    if turn > 0:
        if idx + ping >= len(dir):
            return dir[(idx + ping) - len(dir)]
        else:
            return dir[idx + ping]
    else:
        if idx - ping < 0:
            return dir[len(dir) - abs(idx - ping)]
        else:
            return dir[idx - ping]
          
#############################
def direction(facing, turn):
    dict = {'N':0,'NE':45,'E':90,'SE':135,'S':180,'SW':225,'W':270,'NW':315}
    angle = (dict[facing]+turn)%360
    for x, y in dict.items():
        if y == angle:
            return x
          
#######################
DEGREE_BY_DIRECTION = {"N":0, "NE":45, "E":90, "SE":135, "S":180, "SW":225, "W":270, "NW":315}

DIRECTION_BY_DEGREE = {0:"N", 45:"NE", 90:"E", 135:"SE", 180:"S", 225:"SW", 270:"W", 315:"NW"}

FULL_CIRCLE = 360


def direction(facing, turn):
    
    degrees = DEGREE_BY_DIRECTION[facing]
    
    result = (degrees + turn) % FULL_CIRCLE
    
    new_direction = DIRECTION_BY_DEGREE[result]

    return new_direction
  
###############################
def direction(direction, degree):
    directions = {"N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SW": 225, "W": 270, "NW": 315}
    if degree != 0:
        q =  (directions[direction] + degree) % 360
        return get_key(directions, q)
    return direction

def get_key(dict1, val):
    for key, value in dict1.items():
        if val == value:
            return key
    return None
  
##########################
def direction(facing, turn):
    directions = {"N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SW": 225, "W": 270, "NW": 315}
    if turn != 0:
        q =  (directions[facing] + turn) % 360
        return get_key(directions, q)
    return facing

def get_key(dict1, val):
    for key, value in dict1.items():
        if val == value:
            return key
    return None
