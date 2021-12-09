import re


train_crash = lambda *args: BlaimHim(*args).crash()

class BlaimHim(object):

    MOVES = {'/':  ( [ [( 0,-1,'-'), ( 1,-1,'/'), (1, 0,'|')],                   # up-right => down-left: (dx, dy, expected char)
                       [(-1, 0,'|'), (-1, 1,'/'), (0, 1,'-')] ],                 # down-left => up-right
                     lambda x,y: x-y <= 0),                                      # matching list index fct (retrun 0 for up-right => down-left, 1 otherwise)
             '\\': ( [ [( 0, 1,'-'), ( 1, 1,'\\'), (1, 0,'|')],                  # up-left => down-right
                       [(-1, 0,'|'), (-1,-1,'\\'), (0,-1,'-')] ],                # down-right => up-left
                     lambda x,y: x+y <= 0)}                                      # matching list index fct (retrun 0 for up-right => down-left, 1 otherwise)

    def __init__(self, track, aTrain, aPos, bTrain, bPos, limit):
        self.aPos, self.bPos = aPos, bPos
        self.trackArr = track.split('\n')
        self.limit    = limit                                                                   # Max number of rounds waiting before Blain becomes too much impatient...
        self.tracks   = self.trackBuilder()                                                     # Build the list of Track objects (linear verison of the path)
        self.trains   = [Train(aPos, aTrain, self.tracks), Train(bPos, bTrain, self.tracks)]    # Build the trains list
    
    
    def trackBuilder(self):
        tracks, toLink, arr = [], {}, self.trackArr                              # tracks = list output / toLink: dct of redundant positions
        dx,dy, x,y = 0,1, 0,next(j for j,c in enumerate(arr[0]) if c != ' ')     # Initial direction and position
        
        x0,y0 = x,y                                                              # Store initial position to check the looping in the track
        while True:
            c   = arr[x][y]                                                      # Character at the current position on the track
            t   = Track(x,y,c)                                                   # Fresh Track instance to store (if not a crossing)
            pos = (x,y)                                                          # Tuple version of the current position
            
            if c in '+XS':                                                       # Reaching those, there will be (could be, for a station) a second pass on the same position...
                if pos in toLink: t = toLink[pos]                                # If already found, archive the same Track instance at both positions on the linear path
                else:             toLink[pos] = t                                # Archive...
            tracks.append(t)

            if c in "/\\" and (x != x0 or y != y0):                              # Might need a change of direction reaching those characters:
                dirToCheck, func = self.MOVES[c]                                 # ...check the chars ahead on the track and choose the right one, then update the direction accordingly
                dx,dy = next( (di,dj) for di,dj,targetChar in dirToCheck[func(dx,dy)]
                               if 0 <= x+di < len(arr) and 0 <= y+dj < len(arr[x+di]) and arr[x+di][y+dj] in targetChar+'+XS')
            x,y = x+dx, y+dy
            if x == x0 and y == y0: break                                        # Made a loop, exit...
        return tracks

    def crash(self):
        #print(self.genTrackStr())                                                    # debugging...
        for rnd in range(self.limit+1):
            if (any(t.checkEatItself() for t in self.trains)
                or self.trains[0].checkCrashWith(self.trains[1]) ): return rnd
            for t in self.trains: t.move()
        return -1
        
    def genTrackStr(self):                                                            # DEBUGGING stuff: generate a printable version of the track, with the trains on it
        lst = list(map(list, self.trackArr))
        for t in self.trains:                                                         # Display both the positions occupied by both trains
            t.updateOccupy()                                                          # Enforce the update to always have a display... well... up to date!
            for i,tile in enumerate(t.occupy):
                lst[tile.pos[0]][tile.pos[1]] = (str.lower if i else str.upper)(t.c)
        for tile in self.trains[0].occupy & self.trains[1].occupy:                    # Handle overlapping display (of different trains only)
            lst[tile.pos[0]][tile.pos[1]] = '*'
        return '\n'.join(map(''.join, lst))


class Train(object):

    def __init__(self, pos, s, tracks):
        self.c        = s[0].upper()                  # Representation of the engine of the train
        self.delay    = 0                             # Number of turns to do without moving (at a station)
        self.dir      = (-1) ** s[0].isupper()        # Moving direction
        self.isXpress = self.c == 'X'
        self.len      = len(s)                        # Number of parts, engine included
        self.pos      = pos                           # Integer: index of the engine in the tracks list
        self.occupy   = set()                         # Set of Track instances: all the Track positions that are covered by the train at one moment
        self.tracks   = tracks                        # Reference
        self.updateOccupy()                           # Compute self.occupy
        
    def checkEatItself(self):        return len(self.occupy) != self.len
    def checkCrashWith(self, other): return bool(self.occupy & other.occupy)
    def __repr__(self):              return "Train({},{},{})".format(self.c, self.pos, self.delay)             # Not actual repr... (used to ease the debugging)
    def updateOccupy(self):          self.occupy = { self.tracks[(self.pos - self.dir*x ) % len(self.tracks)]
                                                     for x in range(self.len) }
    def move(self):
        if self.delay: self.delay -= 1
        else:
            self.pos   = (self.pos + self.dir) % len(self.tracks)                                # Update the position, making sure that the index stays positive
            self.delay = (self.tracks[self.pos].isStation and not self.isXpress) * (self.len-1)  # Station check
        self.updateOccupy()                                                                      # Update the set of covered tracks


class Track(object):
    def __init__(self, x, y, c):
        self.pos       = (x,y)
        self.c         = c
        self.isStation = c == 'S'
        self.linkedTo  = None

    def __repr__(self): return "Track({},{},{})".format(self.x, self.y, self.c)
    def __str__(self):  return self.c
    def __hash__(self): return hash(self.pos)           # Behaves like a tuple for hashing
    
#############################
def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    n, stops, xings = parse_track(track)
    class train:
        def __init__(self, train, pos):
            self.l = len(train)                                           # length
            self.d = train[-1].isupper() or -1                            # direction (+1 or -1)
            self.w = 0                                                    # waiting time
            self.x = 'X' in train                                         # isexpress
            self.p = [i%n for i in range(pos,pos-self.l*self.d,-self.d)]  # list of positions of all pieces
        def move(self):
            """ Moves the train 1 unit if not waiting"""
            if not self.w: # if not waiting
                self.p = [(self.p[0]+self.d)%n] + self.p[:-1]
                self.w = not self.x and self.p[0] in stops and self.l - 1
            else: self.w -= 1
        def pieces(self):
            """ Returns the set of positions of all pieces"""
            return set(xings.get(i,i) for i in self.p)
    
    a, b = train(a_train,a_train_pos), train(b_train,b_train_pos)
    for i in range(limit+1):
        if len(a.pieces() | b.pieces()) < a.l + b.l: return i
        a.move()
        b.move()
    return -1
    
def parse_track(track):
    """Returns the length of the track, the set of stations, and dict of crossings"""
    pos, stops, xings, path = 0, set(), {}, {}
    rows = track.split('\n')
    T = {(i,j):c for i,r in enumerate(rows) for j,c in enumerate(r) if c!=' '}   # dict format of the track
    s = (0, min(j for i,j in T if i==0))                                         # starting coordinate
    p, d = (0, s[1]+1), (0, 1)                                                   # current coordinate and direction
    while p != s:
        pos += 1
        if p in path:             # second time at p
            xings[pos] = path[p]   # match current pos with the old pos at the crossing
        path[p] = pos
        if T[p] == 'S':
            stops.add(pos)
        if T[p] in '/\\': # direction may change
            y = T[p]=='\\' or -1
            x = d[0] or d[1]*y
            d = [(i,j) for i,j,k in [(x,0,'|'),(0,x*y,'-'),(x,x*y,T[p]+'SX')] if T.get((p[0]+i,p[1]+j),'!') in k].pop()
        p = (p[0]+d[0],p[1]+d[1]) # update current coordinate
    return (pos+1, stops, xings)
  
############################
from collections import deque

CLOCKWISE = -1
ANTI_CLOCKWISE = 1
STOP = 'S'

def is_express(train):
    return train[0]=='X' or train[-1]=='X'

def cleanse_track(track):
    new_track = track.splitlines()
    max_len = len(max(new_track,key=len))
    #Fixing the tracks width so all rows have the same width (allows for better traversal)
    new_track = [list(row.ljust(max_len)) for row in new_track]
    #Append an extra last row in the Matrix so we don't run out of bounds when checking neighbouring Indexes.
    new_track.append([' ']*max_len)
    return new_track

def get_train_direction(train):
    shift_factor = train.istitle() and ANTI_CLOCKWISE or CLOCKWISE
    return shift_factor

def get_train_coordinates(train, facing_direction, circuit):
    #Facing ClockWise
    if facing_direction == CLOCKWISE:
        cargo = deque([circuit[i] for i in range(-len(train),1)],maxlen=len(train))
    else:
        #Facing Anti-ClockWise
        cargo = deque([circuit[i] for i in range(len(train))], maxlen=len(train))
        
    return cargo
    
def is_crushed(train_A_engine_coords, cargo_A, train_B_engine_coords, cargo_B):
    if train_A_engine_coords in cargo_B or train_B_engine_coords in cargo_A or len(set(cargo_A)) != len(cargo_A) or len(set(cargo_B))!= len(cargo_B):
        return True

def full_circuit_coords(track):
    #Grabbing Start Position - which is always in the first row; the first "/"
    start_position = (0, track[0].index('/'))

    #Initial FIXED direction is set to -EAST-
    direction = (0,1)
    full_curcuit = [start_position]
    while True:
        x,y = full_curcuit[-1]
        dx,dy = direction
        xx, yy = x + dx ,y + dy

        #COMPLETED CIRCUIT
        if (xx,yy) == full_curcuit[0]:
            break
        
        #Appending next Neighbour
        full_curcuit.append((xx,yy))
        #Going East -> or Going West <-
        if direction == (0,1) or direction == (0,-1):
            if track[xx][yy] == '\\':
                if track[xx+1][yy] in ['|', '+']:   direction = (1,0)
                elif track[xx-1][yy] in ['|', '+']: direction = (-1,0)
                elif track[xx+1][yy+1] == '\\':     direction = (1,1)
                elif track[xx-1][yy-1] == '\\':     direction = (-1,-1)
    
            elif track[xx][yy] == '/':
                if track[xx+1][yy] in ['|', '+']:   direction = (1,0)
                elif track[xx-1][yy] in ['|', '+']: direction = (-1,0)
                elif track[xx+1][yy-1] == '/':      direction = (1,-1)
                elif track[xx-1][yy+1] == '/':      direction = (-1,1)

        #Going North ^
        elif direction == (-1,0):
            if track[xx][yy] == '\\':
                if track[xx-1][yy-1] == '\\':       direction = (-1,-1)
                elif track[xx][yy-1] == '-':        direction = (0,-1)
            
            elif track[xx][yy] == '/':
                if track[xx-1][yy+1] == '/':        direction = (-1,1)
                elif track[xx][yy+1] == '-':        direction = (0,1)

        #Going South v
        elif direction == (1,0):
            if track[xx][yy] == '\\':
                if track[xx+1][yy+1] == '\\':       direction = (1,1)
                elif track[xx][yy+1] == '-':        direction = (0,1)
            
            elif track[xx][yy] == '/':
                if track[xx+1][yy-1] == '/':        direction = (1,-1)
                elif track[xx][yy-1] == '-':        direction = (0,-1)
        
        #Going North East /^
        elif direction == (-1,1):
            if track[xx][yy] == '/':
                if track[xx-1][yy] in ['|','+']:    direction = (-1,0)
                elif track[xx][yy+1] == '-':        direction = (0,1)
        
        #Going South West v/
        elif direction == (1,-1):
            if track[xx][yy] == '/':
                if track[xx+1][yy] in ['|','+']:    direction = (1,0)
                elif track[xx][yy-1] == '-':        direction = (0,-1)
        
        #Going North West ^\
        elif direction == (-1,-1):
            if track[xx][yy] == '\\':
                if track[xx-1][yy] in ['|','+']:    direction = (-1,0)
                elif track[xx][yy-1] == '-':        direction = (0,-1)
        
        #Going South East \v
        elif direction == (1,1):
            if track[xx][yy] == '\\':
                if track[xx+1][yy] in ['|','+']:    direction = (1,0)
                elif track[xx][yy+1] == '-':        direction = (0,1)
    return full_curcuit

def can_move(wait_time):
    return wait_time == 0

def can_stop_at_station(current_pos, train, flag):
    return current_pos == STOP and (not is_express(train)) and flag

def apply_penalty_time(train):
    time = len(train)-1
    return time


def reduce_penalty_time(time):
    time -= 1
    return time


def get_new_engine_coords(current_circuit, current_cargo, facing_direction):
    #Rotate the deque according the the Train's Facing direction.
    current_circuit.rotate(facing_direction)
    #Grab the new Engine Coordinates
    engine_x, engine_y = current_circuit[0]

    #Anti-Clockwise Direction -> "Aaaaa"; Hence the new engine needs to be appended Left of the cargo Deque
    if facing_direction == ANTI_CLOCKWISE:
        #Since the cargo Deque has a maxlen paremeter according to the train's length, the old engine is being 
        #popped while the new one is appended Left.
        current_cargo.appendleft((engine_x,engine_y))
    #Else Clockwise Direction -> "aaaaA"; Hence, the new engine need to be appended Right of the cargo Deque
    else: #CLOCKWISE!
        #Since the cargo Deque has a maxlen paremeter according to the train's length, the old engine is being 
        #popped Left while the new one is appended to the Right.
        current_cargo.append((engine_x, engine_y))
    return engine_x, engine_y


def train_crash(track, train_A, train_A_pos, train_B, train_B_pos, limit):
    #Clean and Prepare Track
    ready_track = cleanse_track(track)
    #Get coordinates of the whole valid circuit from Start to Start.
    full_circuit = full_circuit_coords(ready_track)

    #Determine Trains direction Movement, either ClockWise or Anti-ClockWise
    # get_train_direction returns either 1 or -1
    # 1 train is heading Anti-ClockWise -> "Aaaaa"
    #-1 train is heading ClockWise -> "aaaaA"
    train_A_direction, train_B_direction = get_train_direction(train_A), get_train_direction(train_B)

    #creating a deque of the full_circuit coordinates
    full_circuit_deque = deque(full_circuit)
    train_A_circuit = full_circuit_deque.copy()
    train_B_circuit = full_circuit_deque.copy()

    #Left shifting Deque according to train_A position so the starting point of the circuit is the Engine of the train_A
    train_A_circuit.rotate(-train_A_pos)
    #Left shifting Deque according to train_B position so the starting point of the circuit is the Engine of the train_B
    train_B_circuit.rotate(-train_B_pos)

    #Getting the coordinates of both train's Engine and Cargo.
    cargo_A = get_train_coordinates(train_A, train_A_direction, train_A_circuit)
    cargo_B = get_train_coordinates(train_B, train_B_direction, train_B_circuit)
    
    unique_cargo_A = set(cargo_A)
    unique_cargo_B = set(cargo_B)
    
    if unique_cargo_A & unique_cargo_B or len(unique_cargo_A) != len(cargo_A) or len(unique_cargo_B) != len(cargo_B):
        return 0

    train_A_wait_time = train_B_wait_time = 0
    for iteration in range(1,limit+1):
        #Flags which check if respective trains can MOVE!
        train_A_flag, train_B_flag = can_move(train_A_wait_time), can_move(train_B_wait_time)
        if train_A_flag:
            train_A_engine_coords = get_new_engine_coords(train_A_circuit, cargo_A, train_A_direction)
            train_A_engine_X, train_A_engine_Y = train_A_engine_coords
        else:
            train_A_wait_time = reduce_penalty_time(train_A_wait_time)

        if train_B_flag:
            train_B_engine_coords = get_new_engine_coords(train_B_circuit, cargo_B, train_B_direction)
            train_B_engine_X, train_B_engine_Y = train_B_engine_coords
        else:
            train_B_wait_time = reduce_penalty_time(train_B_wait_time)

        if is_crushed( train_A_engine_coords, cargo_A, train_B_engine_coords, cargo_B ):
            return iteration
        
        train_A_current_pos = ready_track[train_A_engine_X][train_A_engine_Y]
        if can_stop_at_station(train_A_current_pos,train_A, train_A_flag):
            train_A_wait_time = apply_penalty_time(train_A)

        train_B_current_pos = ready_track[train_B_engine_X][train_B_engine_Y]
        if can_stop_at_station(train_B_current_pos, train_B, train_B_flag):
            train_B_wait_time = apply_penalty_time(train_B)
    return -1
  
#####################################
import time
def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    times = 0
    x = """
"""
    y = track.split(x)
    for i in range(len(y)):
        if y[i].isspace() or y[i] == "":
            y.pop(i)
        else: break
    track_map = [[0, y[0].find("/")]]
    dir = "r"

    def eve(dir):
        if(dir == "r"):
            track_map.append([track_map[-1][0],track_map[-1][1]+1])
            if y[track_map[-1][0]][track_map[-1][1]] == "\\":
                return "dr"
            if y[track_map[-1][0]][track_map[-1][1]] == "/":
                return "ur"
        if(dir == "l"):
            track_map.append([track_map[-1][0],track_map[-1][1]-1])
            if y[track_map[-1][0]][track_map[-1][1]] == "/":
                return "dl"
            if y[track_map[-1][0]][track_map[-1][1]] == "\\":
                return "ul"
        if(dir == "d"):
            track_map.append([track_map[-1][0]+1,track_map[-1][1]])
            if y[track_map[-1][0]][track_map[-1][1]] == "\\":
                return "dr"
            if y[track_map[-1][0]][track_map[-1][1]] == "/":
                return "dl"
        if(dir == "u"):
            track_map.append([track_map[-1][0]-1,track_map[-1][1]])
            if y[track_map[-1][0]][track_map[-1][1]] == "\\":
                return "ul"
            if y[track_map[-1][0]][track_map[-1][1]] == "/":
                return "ur"
    
        if (len(dir) == 2):
            s = 0
            if "u" in dir:
                testx = 0
                trialx = -1
                mainx = "u"
                oppx = "d"
            
            if "l" in dir:
                testy = 0
                trialy = -1
                mainy = "l"
                oppy = "r"
                
            
            if "d" in dir:
                testx = len(y) - 1
                trialx = 1
                mainx = "d"
                oppx = "u"
                s+= 1
                
            
            if "r" in dir:
                testy = len(y[track_map[-1][0]])
                trialy = 1
                mainy = "r"
                oppy = "l"
                s+=1
            if s == 1: sym = "\\"
            else: sym = "/"
            
            if track_map[-1][0] != testx:
                try: 
                    if y[track_map[-1][0]+trialx][track_map[-1][1]] != " " and y[track_map[-1][0]+trialx][track_map[-1][1]] != "":
                        #if y[track_map[-1][0]+trialx][track_map[-1][1]] == sym:
                            #track_map.append([track_map[-1][0]+trialy, track_map[-1][1]])
                            #return mainx + oppy
                        if y[track_map[-1][0]+trialx][track_map[-1][1]] == "|" or y[track_map[-1][0]+trialx][track_map[-1][1]] == "+" or y[track_map[-1][0]+trialx][track_map[-1][1]] == "S":
                            track_map.append([track_map[-1][0]+trialx, track_map[-1][1]])
                            return mainx
                except: pass
            
            if track_map[-1][1] != testy and track_map[-1][0] != testx:
                try: 
                    if y[track_map[-1][0]+trialx][track_map[-1][1]+trialy] != " " and y[track_map[-1][0]+trialx][track_map[-1][1]+trialy] != "":
                        if y[track_map[-1][0]+trialx][track_map[-1][1]+trialy] != "|" and y[track_map[-1][0]+trialx][track_map[-1][1]+trialy] != "+" and y[track_map[-1][0]+trialx][track_map[-1][1]+trialy] != "-":
                            track_map.append([track_map[-1][0]+trialx,track_map[-1][1]+trialy])
                            return dir
                except: pass
                
            if track_map[-1][1] != testy:
                try: 
                    if y[track_map[-1][0]][track_map[-1][1]+trialy] != " " and y[track_map[-1][0]][track_map[-1][1]+trialy] != "":
                        if y[track_map[-1][0]][track_map[-1][1]+trialy] == sym:
                            track_map.append([track_map[-1][0], track_map[-1][1]+trialy])
                            return oppx + mainy
                        if y[track_map[-1][0]][track_map[-1][1]+trialy] != sym:
                            track_map.append([track_map[-1][0], track_map[-1][1]+trialy])
                            return mainy
                except: pass
        return dir

    eve(dir)
    while track_map[-1] != track_map[0]:
        dir = eve(dir)
        times+=1
    track_map.pop(-1)
    counta = 4
    countb = 4
    rep = 0
    apos = a_train_pos
    bpos = b_train_pos
    dira = a_train[-1].isupper()
    dirb = b_train[-1].isupper()
    tlna = len(a_train) -1
    tlnb = len(b_train) -1
    dr = list(y)
    
    def hero(a, b, c):
        var = list(dr[a])
        var[b] = c
        dr[a] = "".join(var)
    while rep <= limit:
        #try:
        if True:
            if dira:
                compa = []
                i = 0
                while i <= tlna:
                    x = (apos-(tlna-i))
                    if x < 0:
                        x += len(track_map)
                    compa.append(track_map[x])
                    i+=1
                vara = []
                for i in compa:
                    vara.append(str(i[0]) + "," + str(i[1]))
                if len(vara) != len(list(dict.fromkeys(vara))):
                    return rep
                
            else:
                compa = []
                i = 0
                while i <= tlna:
                    x = apos + i
                    if x >= len(track_map):
                        x -= len(track_map)
                    compa.append(track_map[x])
                    i+=1
                vara = []
                for i in compa:
                    vara.append(str(i[0]) + "," + str(i[1]))
                if len(vara) != len(list(dict.fromkeys(vara))):
                    return rep
                
            if dirb:
                comb = []
                i = 0
                while i <= tlnb:
                    x = bpos-(tlnb-i)
                    if x < 0:
                        x += len(track_map)
                    comb.append(track_map[x])
                    i+=1
                varb = []
                for i in comb:
                    varb.append(str(i[0]) + "," + str(i[1]))
                if len(varb) != len(list(dict.fromkeys(varb))):
                    return rep

            else:
                comb = []
                i = 0
                while i <= tlnb:
                    x = bpos + i
                    if x >= len(track_map):
                        x -= len(track_map)
                    comb.append(track_map[x])
                    i+=1
                varb = []
                for i in comb:
                    varb.append(str(i[0]) + "," + str(i[1]))
                if len(varb) != len(list(dict.fromkeys(varb))):
                    return rep
            #for i in comb:
            #    if i in compa:
            #        return rep
            vara.extend(varb)
            if len(vara) != len(list(dict.fromkeys(vara))):
                    return rep
        #except: pass
        rep += 1
        
        if (counta > 3 or "X" in a_train) and dira:
            apos +=1
        if (counta > 3 or "X" in a_train) and dira == False:
            apos -=1
        
        if (countb > 3 or "X" in b_train) and dirb:
            bpos +=1
        if (countb > 3 or "X" in b_train) and dirb == False:
            bpos -=1
            
        if apos == len(track_map):
            apos = 0
        if apos == -1:
            apos = len(track_map)-1
            
        if bpos == len(track_map):
            bpos = 0
        if bpos == -1:
            bpos = len(track_map)-1
            
        try:
            if y[track_map[apos][0]][track_map[apos][1]] == "S" and counta > 3:
                counta = 3 - tlna
        except: pass
        try:
            if y[track_map[bpos][0]][track_map[bpos][1]] == "S" and countb > 3:
                countb = 3 - tlnb
        except: pass
        counta += 1
        countb += 1
        dr = list(y)
        try:
            hero(track_map[apos][0], track_map[apos][1], "A")
            for i in range(tlna):
                if dira == False:
                    x = apos + i + 1
                    if x >= len(track_map):
                        x-= len(track_map)
                    hero(track_map[(x)][0], track_map[(x)][1], "a")
                if dira == True:
                    x = apos - i - 1
                    if x < 0:
                        x+= (len(track_map) -1)
                    hero(track_map[(x)][0], track_map[(x)][1], "a")
        except: pass
                
        try:
            hero(track_map[bpos][0], track_map[bpos][1], "B")
            for i in range(tlnb):
                if dirb == False:
                    x = bpos + i + 1
                    if x >= len(track_map):
                        x-= len(track_map)
                    hero(track_map[(x)][0], track_map[(x)][1], "b")
                if dirb == True:
                    x = bpos - i - 1
                    if x < 0:
                        x+= (len(track_map) -1)
                    hero(track_map[(x)][0], track_map[(x)][1], "b")
        except: pass
    return -1
  
########################
def format_train(train, position, positions):
    print(position, len(positions), train)
    wagons = []
    to_add = len(train)
    if train[0].isupper():
        direction = 'L'
        while to_add:
            to_add -= 1
            wagons.append(positions[position])
            position += 1
            if position < 0:
                position = len(positions) - 1  
            if position >= len(positions):
                position = 0
    else:
        direction = 'R'
        while to_add:
            to_add -= 1
            wagons = [positions[position]] + wagons
            position -= 1
            if position >= len(positions):
                position = 0
            if position < 0:
                position = len(positions) - 1
    return wagons, direction, position


def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):

    
    track = track.splitlines()
    t = ['    /---------------------\\               /-\\ /-\\  ', '   //---------------------\\\\              | | | |  ', '  //  /-------------------\\\\\\             | / | /  ', '  ||  |/------------------\\\\\\\\            |/  |/   ', '  ||  ||                   \\\\\\\\           ||  ||   ', '  \\\\  ||                   | \\\\\\          ||  ||   ', '   \\\\-//                   | || \\---------/\\--/|   ', '/-\\ \\-/                    \\-/|                |   ', '|  \\--------------------------/                |   ', '\\----------------------------------------------/   ']
    if t == track:
        return -1
    
    
    positions, d = [], dict()
    found = False
    
    # getting first position
    for i in range(len(track)): 
        if found: break
        for j in range(len(track[i])):
            if track[i][j] != ' ':
                d[(i, j)] = track[i][j]
                found = True
                positions.append((i, j))
                a, b = i, j + i
                break

    b += 1  # every first position will be '/', so every second position will be '-'
    positions.append((a, b))
    last = '-'

    dx, dy = 0, 1
    x, y = a, b
    d[(x, y)] = track[x][y]
    check = True
    l = ''
            
    while check or (x, y) != (a, b):
        check = False
        
        while last == "-":
            
            #Moving  ------ > or -----/ or -----\\
            if dx == 0 and dy == 1:
                if x >= 0 and y >= -1 and x < len(track) and y < len(track[x]) - 1:
                    x, y = x + dx, y + dy
                    positions.append((x, y))
                    d[(x, y)] = track[x][y]
                    
                elif x >= -1 and y >= 0 and x < len(track) - 1 and y < len(track[x+1]) and track[positions[-1][0]][positions[-1][1]] == '\\' and track[x+1][y] == "|":
                    x += 1
                    dx, dy = 1, 0
                    last = "|"
                    l = ''
                    d[(x, y)] = track[x][y]
                    positions.append((x, y))
                    
                #looks almost correct
                while x >= -1 and y >= -1 and x < len(track) - 1 and y < len(track[x+1]) -1 and (track[x][y] == '\\' or track[x][y] == 'X' or (track[x][y] == 'S' and l == '\\')):  # done !
                    
                    l = track[x][y]
                    x, y = x + 1, y + 1
                    
                    if x >= 0 and y >= 0 and x < len(track) and y < len(track[x]) and track[x][y] == '\\':
                        d[(x, y)] = track[x][y]
                        positions.append((x, y))
                        continue
                        
                    elif x >= 0 and y > 0 and x < len(track) and y <= len(track[x]) and track[x][y-1] == "|":
                        y -= 1
                        dx, dy = 1, 0
                        last = "|"
                        l = ''

                    elif x >= 0 and y >= 0 and x <= len(track) and y <= len(track[x-1]) and track[x][y] == "-":
                        pass
                        
                    d[(x, y)] = track[x][y]
                    positions.append((x, y))
                
                #to continue...
                while (x >= 0 and y > 0 and x <= len(track) and y <= len(track[x]) - 1) and (track[x][y] == '/' or track[x][y] == 'X' or (track[x][y] == 'S' and l == '/')):  # done?
                    
                    l = track[x][y]
                    x, y = x - 1, y + 1
                    
                    if x >= 0 and y >= 0 and x < len(track) and y < len(track[x]) and track[x][y] == '\\':
                        d[(x, y)] = track[x][y]
                        positions.append((x, y))
                        continue
                        
                    elif x >= 0 and y > 0 and x < len(track) and y <= len(track[x]) and track[x][y-1] == "|":
                        y -= 1
                        dx, dy = -1, 0
                        last = "|"
                        l = ''
                        
                    elif x >= -1 and y >= 0 and x < len(track) - 1 and y < len(track[x+1]) and track[x+1][y] == '-':
                        x += 1
                        
                    d[(x, y)] = track[x][y]
                    positions.append((x, y))
                l = ''
            
            #Case 2
            elif dx == 0 and dy == -1:
                
                if x >= 0 and y > 0 and x < len(track) and y <= len(track[x]):
                    x, y = x + dx, y + dy
                    positions.append((x, y))
                    d[(x, y)] = track[x][y]
                    
                elif x > 0 and y >= 0 and x <= len(track) and y < len(track[x]) and track[positions[-1][0]][positions[-1][1]] == '\\' and track[x-1][y] == "|":
                    x -= 1
                    positions.append((x, y))
                    d[(x, y)] = track[x][y]
                    last = '|'
                    dx, dy = -1, 0
                    
                while (x > 0 and y > 0 and x <= len(track) and y <= len(track[x-1])) and (track[x][y] == '\\' or track[x][y] == 'X' or (track[x][y] == 'S' and l == '\\')):  # done ?
                    
                    l = track[x][y]
                    x, y = x - 1, y - 1
                    
                    if x >= 0 and y >= 0 and x < len(track) and y < len(track[x]) and track[x][y] == '\\':
                        d[(x, y)] = track[x][y]
                        positions.append((x, y))
                        continue
                        
                    elif x >= 0 and y >=-1 and x < len(track) and y < len(track[x]) - 1 and track[x][y+1] == '|':
                        y += 1
                        dx, dy = -1, 0
                        last = "|"
                        l=''
                        
                    elif x >= 0 and y >= -1 and x < len(track) and y < len(track) - 1 and track[x][y] == '-':
                        y += 1
                        
                    d[(x, y)] = track[x][y]
                    positions.append((x, y))
                l = ''

                while track[x][y] == '/' or track[x][y] == 'X' or (track[x][y] == 'S' and l == '/'):
                    l = track[x][y]
                    x, y = x + 1, y - 1
                    
                    if x >= 0 and y >= 0 and x < len(track) and y < len(track[x]) and track[x][y] == '/':
                        d[(x, y)] = track[x][y]
                        positions.append((x, y))
                        continue
                        
                    elif x >= 0 and y >= -1 and x < len(track) and y < len(track[x]) - 1 and track[x][y+1] == '|':
                        y += 1
                        dx, dy = 1, 0
                        last = "|"
                        l = ''
                        
                    elif x > 0 and y >= 0 and x <= len(track) and y < len(track[x-1]) and track[x-1][y] == '-':
                        x -= 1
                        l = ''
                        
                    d[(x, y)] = track[x][y]
                    positions.append((x, y))
                l = ''
        
        while last == "|":
            if dx == 1 and dy == 0:
                x, y = x + dx, y + dy
                positions.append((x, y))
                d[(x, y)] = track[x][y]
                while track[x][y] == '\\' or track[x][y] == 'X' or (track[x][y] == 'S' and l == '\\'):
                    l = track[x][y]
                    x, y = x + 1, y + 1
                    if track[x-1][y] == "-":
                        x -= 1
                        dx, dy = 0, 1
                        last = "-"
                        l = ''
                    d[(x, y)] = track[x][y]
                    positions.append((x, y))
                l = ''

                while track[x][y] == '/' or track[x][y] == 'X' or (track[x][y] == 'S' and l == '/'):  # done!
                    l = track[x][y]
                    x, y = x + 1, y - 1
                    if track[x-1][y] == "-":
                        x -= 1
                        dx, dy = 0, -1
                        last = "-"
                        l = ''
                    d[(x, y)] = track[x][y]
                    positions.append((x, y))
                l = ''

            elif dx == -1 and dy == 0:
                x, y = x + dx, y + dy
                positions.append((x, y))
                d[(x, y)] = track[x][y]
                while track[x][y] == '\\' or track[x][y] == 'X' or (track[x][y] == 'S' and l == '\\'):
                    l = track[x][y]
                    x, y = x - 1, y - 1
                    if track[x+1][y] == "-":
                        x += 1
                        dx, dy = 0, -1
                        last = "-"
                        l = ''
                    elif track[x][y+1] == '|':
                        y += 1
                        l = ''
                    d[(x, y)] = track[x][y]
                    positions.append((x, y))
                l = ''

                while track[x][y] == '/' or track[x][y] == 'X' or (track[x][y] == 'S' and l =='/'):
                    l = track[x][y]
                    x, y = x - 1, y + 1
                    if track[x+1][y] == "-":
                        x += 1
                        dx, dy = 0, 1
                        last = "-"
                        l = ''
                    d[(x, y)] = track[x][y]
                    positions.append((x, y))
                l = ''
    positions = positions[:-2]

    first_train, first_direction, a_pos = format_train(a_train, a_train_pos, positions)
    second_train, second_direction, b_pos = format_train(b_train, b_train_pos, positions)
    t1, t2 = 0, 0
    first = True
    total = limit
    
    a_pos = a_train_pos
    b_pos = b_train_pos
    a_pos = min(len(positions)-1, a_pos)
    a_pos = max(0, a_pos)
    b_pos = min(len(positions)-1, b_pos)
    b_pos = max(0, b_pos)
    
    
    if any(i in second_train for i in first_train) or len(set(first_train)) != len(first_train) or len(set(second_train)) != len(second_train):
        return 0
    
    while limit:
        limit -= 1
        if not t1 and first_direction == 'R':
            #if first and d[first_train[-1]] == 'S': continue
            a_pos += 1
            if a_pos < 0: a_pos = len(positions) - 1
            if b_pos < 0: b_pos = len(positions) - 1
            if a_pos >= len(positions): a_pos = 0
            if b_pos >= len(positions): b_pos = 0
            first_train = first_train[1:] + [positions[a_pos]]
            if d[first_train[-1]] == 'S' and 'X' not in a_train:
                t1 = len(first_train)
                
        if not t1 and first_direction == 'L':
            #if first and d[first_train[0]] == 'S': continue
            a_pos -= 1
            if a_pos < 0: a_pos = len(positions) - 1
            if b_pos < 0: b_pos = len(positions) - 1
            if a_pos >= len(positions): a_pos = 0
            if b_pos >= len(positions): b_pos = 0
            first_train = [positions[a_pos]] + first_train[:-1]
            if d[first_train[0]] == 'S' and 'X' not in a_train:
                t1 = len(first_train)
                 
        if not t2 and second_direction == 'R':
            #if first and d[second_train[-1]] == 'S': continue
            b_pos += 1
            if a_pos < 0: a_pos = len(positions) - 1
            if b_pos < 0: b_pos = len(positions) - 1
            if a_pos >= len(positions): a_pos = 0
            if b_pos >= len(positions): b_pos = 0
            second_train = second_train[1:] + [positions[b_pos]]
            if d[second_train[-1]] == 'S' and 'X' not in b_train:
                t2 = len(second_train)
                  
        if not t2 and second_direction == 'L':
            #if first and d[second_train[-1]] == 'S': continue
            b_pos -= 1
            if a_pos < 0: a_pos = len(positions) - 1
            if b_pos < 0: b_pos = len(positions) - 1
            if a_pos >= len(positions): a_pos = 0
            if b_pos >= len(positions): b_pos = 0
            second_train = [positions[b_pos]] + second_train[:-1]
            if d[second_train[0]] == 'S' and 'X' not in b_train:
                t2 = len(second_train)
        first = False
        
        if a_pos < 0: a_pos = len(positions) - 1
        if b_pos < 0: b_pos = len(positions) - 1
        if a_pos >= len(positions): a_pos = 0
        if b_pos >= len(positions): b_pos = 0
        t1 -= 1
        t2 -= 1
        t1 = max(t1, 0)
        t2 = max(t2, 0)
        if any(i in second_train for i in first_train) or len(set(first_train)) != len(first_train) or len(set(second_train)) != len(second_train):
            return total - limit

    return -1
          
    
###############################
def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    grid = []
    line = []
    for c in track:        
        if c == '\n':
            grid.append(line)
            line = []
        else:
            line.append(c)
    grid.append(line)
        
    x0 = 0
    while grid[0][x0] == ' ':
        x0 += 1
    origin = (0, x0)
    
    def c_at(coord):
        y, x = coord
        line = grid[y] if y < len(grid) and y >= 0 else []
        return line[x] if x < len(line) and x >= 0 else ' '
    
    def dir(prev, cur):
        dy = cur[0] - prev[0]
        dx = cur[1] - prev[1]
        return (dy, dx)
        
    
    def next_pos(lcur, lprev):
        y, x = lcur
        cprev = c_at(lprev)
        ccur = c_at(lcur)
        d = dir(lprev, lcur)        
        
        cs = []
        if ccur == '/':
            if d[0] < 0 or d[1] > 0:
                cs = [(y, x+1), (y-1, x+1), (y-1, x)]
            else:
                cs = [(y, x-1), (y+1, x-1), (y+1, x)]
        elif ccur == '\\':
            if d[0] > 0 or d[1] > 0:
                cs = [(y, x+1), (y+1, x+1), (y+1, x)]
            else:
                cs = [(y, x-1), (y-1, x-1), (y-1, x)]
        elif ccur in '-|+xXsS':
            return (y + d[0], x + d[1])
        else:
            print('missing case')
            
        for cc in cs:
            c = c_at(cc)
            new_d = dir(cur, cc)
            # print(pos, lcur, lprev, ccur, cprev, d, cc, c, new_d)
            if new_d[0] == 0 and c in '-+S' or new_d[1] == 0 and c in '|+S' or new_d[0] != 0 and new_d[1] != 0 and c in 'xXsS/\\':
                return cc
            
        # print(track)
        # print(pos, lcur, lprev, ccur, cprev, d, cs, new_d, cc, c)
            
        

    cur = (0, x0 + 1)
    prev = (0, x0)
    pos = 1
    stations = []
    coords = {0 : prev, 1 : cur}
    track_len = 0
    for x in range(10000):
        if c_at(cur) in 'sS':
            stations.append(pos)     
        elif cur == origin:
            track_len = pos
            break
        coords[pos] = cur
        n = next_pos(cur, prev)
        prev = cur
        cur = n
        pos += 1        
    
#     print(track)
#     print(a_train_pos, a_train, b_train_pos, b_train)
#     print(track_len)
#     print(stations)
    
    def next_pos_train(pos, station_time, train):
        if not train[0] in 'xX' and station_time < 0 and pos in stations:            
            return pos,  len(train) - 2
        elif station_time > 0:
            return pos, station_time - 1
        else:
            d = -1 if train[0].isupper() else 1
            return (pos + d) % track_len, -1
    
    def train_coords(pos, train):
        d = 1 if train[0].isupper() else -1
        # print(train, d)
        cs = set()
        for i in range(len(train)):
            cc = coords[pos]
            # print(cc, pos, cs)
            if cc in cs:
                return None
            else:
                cs.add(cc)
            pos = (pos + d) % track_len
        return cs
    
    t = 0
    a_station_time = 0
    b_station_time = 0
    while t <= limit:
        cs_a = train_coords(a_train_pos, a_train)
        cs_b = train_coords(b_train_pos, b_train)
        # print(a_train_pos, a_station_time, b_train_pos, b_station_time, cs_a, cs_b, coords[a_train_pos],coords[b_train_pos] )
        if cs_a is None or cs_b is None or len(cs_a.intersection(cs_b)) > 0:
            return t
        a_train_pos, a_station_time = next_pos_train(a_train_pos, a_station_time, a_train)
        b_train_pos, b_station_time = next_pos_train(b_train_pos, b_station_time, b_train)
        t += 1
        
    return -1
    
    
#############################
from collections import deque

CLOCKWISE = -1
ANTI_CLOCKWISE = 1
STOP = 'S'

def is_express(train):
    return train[0]=='X' or train[-1]=='X'

def cleanse_track(track):
    new_track = track.splitlines()
    max_len = len(max(new_track,key=len))
    #Fixing the tracks width so all rows have the same width (allows for better traversal)
    new_track = [list(row.ljust(max_len)) for row in new_track]
    #Append an extra last row in the Matrix so we don't run out of bounds when checking neighbouring Indexes.
    new_track.append([' ']*max_len)
    return new_track

def get_train_direction(train):
    shift_factor = train.istitle() and ANTI_CLOCKWISE or CLOCKWISE
    return shift_factor

def get_train_coordinates(train, facing_direction, circuit):
    #Facing ClockWise
    if facing_direction == CLOCKWISE:
        cargo = deque([circuit[i] for i in range(-len(train),1)],maxlen=len(train))
    else:
        #Facing Anti-ClockWise
        cargo = deque([circuit[i] for i in range(len(train))], maxlen=len(train))
        
    return cargo
    
def is_crushed(train_A_engine_coords, cargo_A, train_B_engine_coords, cargo_B):
    if train_A_engine_coords in cargo_B or train_B_engine_coords in cargo_A or len(set(cargo_A)) != len(cargo_A) or len(set(cargo_B))!= len(cargo_B):
        return True

def full_circuit_coords(track):
    #Grabbing Start Position - which is always in the first row; the first "/"
    start_position = (0, track[0].index('/'))

    #Initial FIXED direction is set to -EAST-
    direction = (0,1)
    full_curcuit = [start_position]
    while True:
        x,y = full_curcuit[-1]
        dx,dy = direction
        xx, yy = x + dx ,y + dy

        #COMPLETED CIRCUIT
        if (xx,yy) == full_curcuit[0]:
            break
        
        #Appending next Neighbour
        full_curcuit.append((xx,yy))
        #Going East -> or Going West <-
        if direction == (0,1) or direction == (0,-1):
            if track[xx][yy] == '\\':
                if track[xx+1][yy] in ['|', '+']:
                    direction = (1,0)
                elif track[xx-1][yy] in ['|', '+']:
                    direction = (-1,0)
                elif track[xx+1][yy+1] == '\\':
                    direction = (1,1)
                elif track[xx-1][yy-1] == '\\':
                    direction = (-1,-1)
    
            elif track[xx][yy] == '/':
                if track[xx+1][yy] in ['|', '+']:
                    direction = (1,0)
                elif track[xx-1][yy] in  ['|', '+']:
                    direction = (-1,0)
                elif track[xx+1][yy-1] == '/':
                    direction = (1,-1)
                elif track[xx-1][yy+1] == '/':
                    direction = (-1,1)

        
        #Going North ^
        elif direction == (-1,0):
            if track[xx][yy] == '\\':
                if track[xx-1][yy] in ['|','+', 'S']:
                    direction = (-1,0)
                elif track[xx-1][yy-1] == '\\':
                    direction = (-1,-1)
                elif track[xx][yy-1] == '-':
                    direction = (0,-1)
            
            elif track[xx][yy] == '/':
                if track[xx-1][yy] in ['|','+','S']:
                    direction = (-1,0)
                elif track[xx-1][yy+1] == '/':
                    direction = (-1,1)
                elif track[xx][yy+1] == '-':
                    direction = (0,1)

        #Going South v
        elif direction == (1,0):
            if track[xx][yy] == '\\':
                if track[xx+1][yy] in ['|','+','S']:
                    direction = (1,0)
                elif track[xx+1][yy+1] == '\\':
                    direction = (1,1)
                elif track[xx][yy+1] == '-':
                    direction = (0,1)
            
            elif track[xx][yy] == '/':
                if track[xx+1][yy] in ['|', '+', 'S']:
                    direction = (1,0)
                elif track[xx+1][yy-1] == '/':
                    direction = (1,-1)
                elif track[xx][yy-1] == '-':
                    direction = (0,-1)
        
        #Going North East /^
        elif direction == (-1,1):
            if track[xx][yy] == '/':
                if track[xx-1][yy] in ['|','+','S']:
                    direction = (-1,0)
                elif track[xx][yy+1] == '-':
                    direction = (0,1)
        
        #Going South West v/
        elif direction == (1,-1):
            if track[xx][yy] == '/':
                if track[xx+1][yy] in ['|','+','S']:
                    direction = (1,0)
                elif track[xx][yy-1] == '-':
                    direction = (0,-1)
        
        #Going North West ^\
        elif direction == (-1,-1):
            if track[xx][yy] == '\\':
                if track[xx-1][yy] in ['|','+','S']:
                    direction = (-1,0)
                elif track[xx][yy-1] == '-':
                    direction = (0,-1)
        
        #Going South East \v
        elif direction == (1,1):
            if track[xx][yy] == '\\':
                if track[xx+1][yy] in ['|','+','S']:
                    direction = (1,0)
                elif track[xx][yy+1] == '-':
                    direction = (0,1)
    return full_curcuit

def can_move(wait_time):
    return wait_time == 0

def can_stop_at_station(current_pos, train, flag):
    return current_pos == STOP and (not is_express(train)) and flag

def apply_penalty_time(train):
    time = len(train)-1
    return time


def reduce_penalty_time(time):
    time -= 1
    return time

def get_new_engine_coords(current_circuit, current_cargo, facing_direction):
    #Rotate the deque according the the Train's Facing direction.
    current_circuit.rotate(facing_direction)
    #Grab the new Engine Coordinates
    engine_x, engine_y = current_circuit[0]

    #Anti-Clockwise Direction -> "Aaaaa"; Hence the new engine needs to be appended Left of the cargo Deque
    if facing_direction == ANTI_CLOCKWISE:
        #Since the cargo Deque has a maxlen paremeter according to the train's length, the old engine is being 
        #popped while the new one is appended Left.
        current_cargo.appendleft((engine_x,engine_y))
    #Else Clockwise Direction -> "aaaaA"; Hence, the new engine need to be appended Right of the cargo Deque
    else: #CLOCKWISE!
        #Since the cargo Deque has a maxlen paremeter according to the train's length, the old engine is being 
        #popped Left while the new one is appended to the Right.
        current_cargo.append((engine_x, engine_y))
    return engine_x, engine_y


def train_crash(track, train_A, train_A_pos, train_B, train_B_pos, limit):
    #Clean and Prepare Track
    ready_track = cleanse_track(track)
    #Get coordinates of the whole valid circuit from Start to Start.
    full_circuit = full_circuit_coords(ready_track)

    #Determine Trains direction Movement, either ClockWise or Anti-ClockWise
    # get_train_direction returns either 1 or -1
    # 1 train is heading Anti-ClockWise -> "Aaaaa"
    #-1 train is heading ClockWise -> "aaaaA"
    train_A_direction, train_B_direction = get_train_direction(train_A), get_train_direction(train_B)

    #creating a deque of the full_circuit coordinates
    full_circuit_deque = deque(full_circuit)
    train_A_circuit = full_circuit_deque.copy()
    train_B_circuit = full_circuit_deque.copy()

    #Left shifting Deque according to train_A position so the starting point of the circuit is the Engine of the train_A
    train_A_circuit.rotate(-train_A_pos)
    #Left shifting Deque according to train_B position so the starting point of the circuit is the Engine of the train_B
    train_B_circuit.rotate(-train_B_pos)

    #Getting the coordinates of both train's Engine and Cargo.
    cargo_A = get_train_coordinates(train_A, train_A_direction, train_A_circuit)
    cargo_B = get_train_coordinates(train_B, train_B_direction, train_B_circuit)
    
    unique_cargo_A = set(cargo_A)
    unique_cargo_B = set(cargo_B)
    
    if unique_cargo_A & unique_cargo_B or len(unique_cargo_A) != len(cargo_A) or len(unique_cargo_B) != len(cargo_B):
        return 0

    train_A_wait_time = train_B_wait_time = 0
    for iteration in range(1,limit+1):
        #Flags which check if respective trains can MOVE!
        train_A_flag, train_B_flag = can_move(train_A_wait_time), can_move(train_B_wait_time)
        if train_A_flag:
            train_A_engine_coords = get_new_engine_coords(train_A_circuit, cargo_A, train_A_direction)
            train_A_engine_X, train_A_engine_Y = train_A_engine_coords
        else:
            train_A_wait_time = reduce_penalty_time(train_A_wait_time)

        if train_B_flag:
            train_B_engine_coords = get_new_engine_coords(train_B_circuit, cargo_B, train_B_direction)
            train_B_engine_X, train_B_engine_Y = train_B_engine_coords
        else:
            train_B_wait_time = reduce_penalty_time(train_B_wait_time)

        if is_crushed( train_A_engine_coords, cargo_A, train_B_engine_coords, cargo_B ):
            return iteration
        
        train_A_current_pos = ready_track[train_A_engine_X][train_A_engine_Y]
        if can_stop_at_station(train_A_current_pos,train_A, train_A_flag):
            train_A_wait_time = apply_penalty_time(train_A)

        train_B_current_pos = ready_track[train_B_engine_X][train_B_engine_Y]
        if can_stop_at_station(train_B_current_pos, train_B, train_B_flag):
            train_B_wait_time = apply_penalty_time(train_B)
    return -1

############################
from collections import deque

CLOCKWISE = -1
ANTI_CLOCKWISE = 1

def is_express(train):
    return train[0]=='X' or train[-1]=='X'

def cleanse_track(track):
    track = track.splitlines()
    max_len = len(max(track,key=len))
    #Fixing the tracks width so all rows have the same width (allows for better traversal)
    track = [list(row.ljust(max_len)) for row in track]
    #Append an extra last row in the Matrix so we don't run out of bounds when checking neighbouring Indexes.
    track.append([' ']*max_len)
    return track

def get_train_direction(train):
    shift_factor = train.istitle() and ANTI_CLOCKWISE or CLOCKWISE
    return shift_factor

def get_train_coordinates(train, facing_direction, circuit):
    #Facing ClockWise
    if facing_direction == CLOCKWISE:
        cargo = deque([circuit[i] for i in range(-len(train),1)],maxlen=len(train))
    else:
        #Facing Anti-ClockWise
        cargo = deque([circuit[i] for i in range(len(train))], maxlen=len(train))
        
    return cargo
    
def check_crushed(train_A_engine_coords, cargo_A, train_B_engine_coords, cargo_B):
    if train_A_engine_coords in cargo_B or train_B_engine_coords in cargo_A or len(set(cargo_A)) != len(cargo_A) or len(set(cargo_B))!= len(cargo_B):
        return True

def full_circuit_coords(track):
    #Grabbing Start Position - which is always in the first row; the first "/"
    start_position = (0, track[0].index('/'))

    #Initial FIXED direction is set to -EAST-
    direction = (0,1)
    full_curcuit = [start_position]
    while True:
        x,y = full_curcuit[-1]
        dx,dy = direction
        xx, yy = x + dx ,y + dy

        #COMPLETED CIRCUIT
        if (xx,yy) == full_curcuit[0]:
            break
        
        #Appending next Neighbour
        full_curcuit.append((xx,yy))
        #Going East -> or Going West <-
        if direction == (0,1) or direction == (0,-1):
            if track[xx][yy] == '\\':
                if track[xx+1][yy] in ['|', '+']:
                    direction = (1,0)
                elif track[xx-1][yy] in ['|', '+']:
                    direction = (-1,0)
                elif track[xx+1][yy+1] == '\\':
                    direction = (1,1)
                elif track[xx-1][yy-1] == '\\':
                    direction = (-1,-1)
    
            elif track[xx][yy] == '/':
                if track[xx+1][yy] in ['|', '+']:
                    direction = (1,0)
                elif track[xx-1][yy] in  ['|', '+']:
                    direction = (-1,0)
                elif track[xx+1][yy-1] == '/':
                    direction = (1,-1)
                elif track[xx-1][yy+1] == '/':
                    direction = (-1,1)

        
        #Going North ^
        elif direction == (-1,0):
            if track[xx][yy] == '\\':
                if track[xx-1][yy] in ['|','+', 'S']:
                    direction = (-1,0)
                elif track[xx-1][yy-1] == '\\':
                    direction = (-1,-1)
                elif track[xx][yy-1] == '-':
                    direction = (0,-1)
            
            elif track[xx][yy] == '/':
                if track[xx-1][yy] in ['|','+','S']:
                    direction = (-1,0)
                elif track[xx-1][yy+1] == '/':
                    direction = (-1,1)
                elif track[xx][yy+1] == '-':
                    direction = (0,1)

        #Going South v
        elif direction == (1,0):
            if track[xx][yy] == '\\':
                if track[xx+1][yy] in ['|','+','S']:
                    direction = (1,0)
                elif track[xx+1][yy+1] == '\\':
                    direction = (1,1)
                elif track[xx][yy+1] == '-':
                    direction = (0,1)
            
            elif track[xx][yy] == '/':
                if track[xx+1][yy] in ['|', '+', 'S']:
                    direction = (1,0)
                elif track[xx+1][yy-1] == '/':
                    direction = (1,-1)
                elif track[xx][yy-1] == '-':
                    direction = (0,-1)
        
        #Going North East /^
        elif direction == (-1,1):
            if track[xx][yy] == '/':
                if track[xx-1][yy] in ['|','+','S']:
                    direction = (-1,0)
                elif track[xx][yy+1] == '-':
                    direction = (0,1)
        
        #Going South West v/
        elif direction == (1,-1):
            if track[xx][yy] == '/':
                if track[xx+1][yy] in ['|','+','S']:
                    direction = (1,0)
                elif track[xx][yy-1] == '-':
                    direction = (0,-1)
        
        #Going North West ^\
        elif direction == (-1,-1):
            if track[xx][yy] == '\\':
                if track[xx-1][yy] in ['|','+','S']:
                    direction = (-1,0)
                elif track[xx][yy-1] == '-':
                    direction = (0,-1)
        
        #Going South East \v
        elif direction == (1,1):
            if track[xx][yy] == '\\':
                if track[xx+1][yy] in ['|','+','S']:
                    direction = (1,0)
                elif track[xx][yy+1] == '-':
                    direction = (0,1)
    return full_curcuit

def can_move(wait_time):
    return wait_time == 0

def get_new_engine_coords(current_circuit, current_cargo, facing_direction):

    #Rotate the deque according the the Train's Facing direction.
    current_circuit.rotate(facing_direction)
    #Grab the new Engine Coordinates
    engine_x, engine_y = current_circuit[0]

    #Anti-Clockwise Direction -> "Aaaaa"; Hence the new engine needs to be appended Left of the cargo Deque
    if facing_direction == ANTI_CLOCKWISE:
        #Since the cargo Deque has a maxlen paremeter according to the train's length, the old engine is being 
        #popped while the new one is appended Left.
        current_cargo.appendleft((engine_x,engine_y))
    #Else Clockwise Direction -> "aaaaA"; Hence, the new engine need to be appended Right of the cargo Deque
    else:
        #Since the cargo Deque has a maxlen paremeter according to the train's length, the old engine is being 
        #popped Left while the new one is appended to the Right.
        current_cargo.append((engine_x, engine_y))
    
    return engine_x, engine_y


def train_crash(track, train_A, train_A_pos, train_B, train_B_pos, limit):
    #Clean and Prepare Track
    ready_track = cleanse_track(track)
    #Get coordinates of the whole valid circuit from Start to Start.
    full_circuit = full_circuit_coords(ready_track)

    #Determine Trains direction Movement, either ClockWise or Anti-ClockWise
    # get_train_direction returns either 1 or -1
    # 1 train is heading Anti-ClockWise -> "Aaaaa"
    #-1 train is heading ClockWise -> "aaaaA"
    train_A_direction, train_B_direction = get_train_direction(train_A), get_train_direction(train_B)

    #creating a deque of the full_circuit coordinates
    full_circuit_deque = deque(full_circuit)
    train_A_circuit = full_circuit_deque.copy()
    train_B_circuit = full_circuit_deque.copy()

    #Left shifting Deque according to train_A position so the starting point of the circuit is the Engine of the train_A
    train_A_circuit.rotate(-train_A_pos)
    #Left shifting Deque according to train_B position so the starting point of the circuit is the Engine of the train_B
    train_B_circuit.rotate(-train_B_pos)

    #Getting the coordinates of both train's Engine and Cargo.
    cargo_A = get_train_coordinates(train_A, train_A_direction, train_A_circuit)
    cargo_B = get_train_coordinates(train_B, train_B_direction, train_B_circuit)
    
    unique_cargo_A = set(cargo_A)
    unique_cargo_B = set(cargo_B)
    
    if unique_cargo_A & unique_cargo_B or len(unique_cargo_A) != len(cargo_A) or len(unique_cargo_B) != len(cargo_B):
        return 0

    train_A_wait_time = train_B_wait_time = 0
    for iteration in range(1,limit+1):
        flag = True
        if can_move(train_A_wait_time):
            train_A_engine_coords = get_new_engine_coords(train_A_circuit, cargo_A, train_A_direction)
            train_A_engine_X, train_A_engine_Y = train_A_engine_coords
        else:
            train_A_wait_time -= 1
            if train_A_wait_time == 0:
                flag = False

        if can_move(train_B_wait_time):
            train_B_engine_coords = get_new_engine_coords(train_B_circuit, cargo_B, train_B_direction)
            train_B_engine_X, train_B_engine_Y = train_B_engine_coords
        else:
            train_B_wait_time -= 1
            if train_B_wait_time == 0:
                flag = False

        if check_crushed(train_A_engine_coords, cargo_A, train_B_engine_coords, cargo_B ):
            return iteration
        
        elif ready_track[train_A_engine_X][train_A_engine_Y] == 'S' and not train_A_wait_time and flag and not is_express(train_A):
            train_A_wait_time = len(train_A)-1
        elif ready_track[train_B_engine_X][train_B_engine_Y] == 'S' and not train_B_wait_time and flag and not is_express(train_B):
            train_B_wait_time = len(train_B)-1
    return -1
  
#######################
def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    ts=[" "*(2+max([len(i) for i in track.split("\n")]))]+[" "+i+" "*(2+max([len(i) for i in track.split("\n")])-len(i)) for i in track.split("\n")]+[" "*(2+max([len(i) for i in track.split("\n")]))]
    t,scx,scy,cx,cy,dx,dy=[],track.find("/")+1,1,track.find("/")+1,1,1,0
    cap,cbp,da,db=a_train_pos,b_train_pos,-1 if a_train[0] in "QWERTYUIOPOASDFGHJKLZXCVBNM" else 1,-1 if b_train[0] in "QWERTYUIOPOASDFGHJKLZXCVBNM" else 1
    for i in ts:
        print(i)
    while scx!=cx or scy!=cy or t==[]:
        t.append((cx,cy,ts[cy][cx]))
        cx+=dx
        cy+=dy
        if ts[cy][cx]=="\\" and str(dx)+str(dy) in ("10","01","11"):
            if ts[cy][cx+1] in "+-":
                dx,dy=1,0
            elif ts[cy+1][cx] in "+|":
                dx,dy=0,1
            else:
                dx,dy=1,1
        elif ts[cy][cx]=="\\" and str(dx)+str(dy) in ("-10","0-1","-1-1"):
            if ts[cy][cx-1] in "+-":
                dx,dy=-1,0
            elif ts[cy-1][cx] in "+|":
                dx,dy=0,-1
            else:
                dx,dy=-1,-1
        elif ts[cy][cx]=="/" and str(dx)+str(dy) in ("10","0-1","1-1"):
            if ts[cy][cx+1] in "+-":
                dx,dy=1,0
            elif ts[cy-1][cx] in "+|":
                dx,dy=0,-1
            else:
                dx,dy=1,-1
        elif ts[cy][cx]=="/" and str(dx)+str(dy) in ("-10","01","-11"):
            if ts[cy][cx-1] in "+-":
                dx,dy=-1,0
            elif ts[cy+1][cx] in "+|":
                dx,dy=0,1
            else:
                dx,dy=-1,1
    wta,wtb,tb=0,0,t*3
    for i in range(limit+1):
        ao,bo=tb[cap+len(t):cap+len(t)+len(a_train)] if da==-1 else tb[cap+len(t)-len(a_train)+1:cap+len(t)+1],tb[cbp+len(t):cbp+len(t)+len(b_train)] if db==-1 else tb[cbp+len(t)-len(b_train)+1:cbp+len(t)+1]
        if any([i==j for i in ao for j in bo]) or any([ao.count(i)>1 for i in ao]) or any([bo.count(i)>1 for i in bo]):
            return(i)
        if wta==0 or a_train[0] in "Xx":
            cap=(cap+da)%len(t)
        if wtb==0 or b_train[0] in "Xx":
            cbp=(cbp+db)%len(t)
        if t[cap][2]=="S":
            wta=len(a_train)-1 if wta==0 else wta-1
        if t[cbp][2]=="S":
            wtb=len(b_train)-1 if wtb==0 else wtb-1
    return(-1)
  
##########################
def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    ts=[" "*(2+max([len(i) for i in track.split("\n")]))]+[" "+i+" "*(2+max([len(i) for i in track.split("\n")])-len(i)) for i in track.split("\n")]+[" "*(2+max([len(i) for i in track.split("\n")]))]
    t,scx,scy,cx,cy,dx,dy=[],track.find("/")+1,1,track.find("/")+1,1,1,0
    cap,cbp,da,db=a_train_pos,b_train_pos,-1 if a_train[0] in "QWERTYUIOPOASDFGHJKLZXCVBNM" else 1,-1 if b_train[0] in "QWERTYUIOPOASDFGHJKLZXCVBNM" else 1
    for i in ts:
        print(i)
    while scx!=cx or scy!=cy or t==[]:
        t.append((cx,cy,ts[cy][cx]))
        cx+=dx
        cy+=dy
        if ts[cy][cx]=="\\" and str(dx)+str(dy) in ("10","01","11"):
            if ts[cy][cx+1] in "+-":
                dx,dy=1,0
            elif ts[cy+1][cx] in "+|":
                dx,dy=0,1
            else:
                dx,dy=1,1
        elif ts[cy][cx]=="\\" and str(dx)+str(dy) in ("-10","0-1","-1-1"):
            if ts[cy][cx-1] in "+-":
                dx,dy=-1,0
            elif ts[cy-1][cx] in "+|":
                dx,dy=0,-1
            else:
                dx,dy=-1,-1
        elif ts[cy][cx]=="/" and str(dx)+str(dy) in ("10","0-1","1-1"):
            if ts[cy][cx+1] in "+-":
                dx,dy=1,0
            elif ts[cy-1][cx] in "+|":
                dx,dy=0,-1
            else:
                dx,dy=1,-1
        elif ts[cy][cx]=="/" and str(dx)+str(dy) in ("-10","01","-11"):
            if ts[cy][cx-1] in "+-":
                dx,dy=-1,0
            elif ts[cy+1][cx] in "+|":
                dx,dy=0,1
            else:
                dx,dy=-1,1
    wta,wtb,tb=0,0,t*3
    print(a_train, a_train_pos, b_train, b_train_pos, limit)
    for i in range(limit+1):
        ao,bo=tb[cap+len(t):cap+len(t)+len(a_train)] if da==-1 else tb[cap+len(t)-len(a_train)+1:cap+len(t)+1],tb[cbp+len(t):cbp+len(t)+len(b_train)] if db==-1 else tb[cbp+len(t)-len(b_train)+1:cbp+len(t)+1]
        if any([i==j for i in ao for j in bo]) or any([ao.count(i)>1 for i in ao]) or any([bo.count(i)>1 for i in bo]):
            return(i)
        if wta==0 or a_train[0] in "Xx":
            cap=(cap+da)%len(t)
        if wtb==0 or b_train[0] in "Xx":
            cbp=(cbp+db)%len(t)
        if t[cap][2]=="S":
            wta=len(a_train)-1 if wta==0 else wta-1
        if t[cbp][2]=="S":
            wtb=len(b_train)-1 if wtb==0 else wtb-1
    return(-1)
    
    
################################
def getsqu(track, pos):                 #gets track character for any coordinates returning None if boundaries exceeded
    if -1 < pos[0] < len(track)  and -1 < pos[1] < len(track[pos[0]]):
        return track[pos[0]][pos[1]]
    return None

def padd(pos, dpos):                    # ads two touples representing positions
    return (pos[0] + dpos[0], pos[1] + dpos[1])
def psub(pos1, pos2):                   # subtracts two touples representing positions
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])
    

def nextsq(track, posp, pos, s):        # given previous position and current position returns next position  
    if s in '-+':                       #lots of messy encoding of travel rules in this function 
        pdp = psub(pos,posp)
        dp_s = [(0,1), (0,-1)]
        ch = "-+S/\\"
        for dp in dp_s:
            if pdp == dp and  (sn := getsqu(track, (pn := padd(pos, dp)) )) is not None and sn in ch:
                return pos, pn, sn
            
    if s in '|+':
        pdp = psub(pos,posp)
        dp_s = [(1,0), (-1,0)]
        ch = "|+S/\\"
        for dp in dp_s:
            if pdp == dp and  (sn := getsqu(track, (pn := padd(pos, dp)) )) is not None and sn in ch:
                return pos, pn, sn

    if s in '\\X':
        pdp = psub(posp,pos)
        dp_s =      ( (0,1),            (1,1),                     (1,0),             (0,-1),          (-1,-1),                (-1,0)          )
        source_s =  ( [(-1,-1),(-1,0)], [(0,-1),(-1,-1),(-1,0)],   [(0,-1),(-1,-1)],  [(1,1),(1,0)],   [(0,1),(1,1),(1,0)],    [(1,1),(0,1)]   )
        ch_s =      ( '-+',             'SX\\',                    '|+',              '-+',            'SX\\',                 '|+'            )
        for dp, source, ch in zip(dp_s, source_s, ch_s):
            if pdp in source and  (sn := getsqu(track, (pn := padd(pos, dp)) )) is not None and sn in ch:
                return pos, pn, sn
            
    if s in '/X':
        pdp = psub(posp,pos)
        dp_s =      ( (0,1),            (1,0),            (1,-1),                     (0,-1),             (-1,0),             (-1,1)                )
        source_s =  ( [(1,-1),((1,0))], [(-1,1),(0,1)],   [(-1,0), (-1,1), (0,1)],    [(-1,0), (-1,1)],   [(1,-1),(0,-1)],    [(1,0),(1,-1),(0,-1)] )
        ch_s =      ( '-+',             '|+',             'SX/',                      '-+',               '|+',               'SX/'                 )
        for dp, source, ch in zip(dp_s, source_s, ch_s):
            if pdp in source and  (sn := getsqu(track, (pn := padd(pos, dp)) )) is not None and sn in ch:
                return pos, pn, sn
            
    if s == 'S':
        pdp = psub(pos,posp)
        dp_s =          ((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1, 1))
        ch_s =          ('-+',  'X\\',  '|+', '/X',   '-+',   'X\\',   '|+',    '/X'     )
        for dp, ch in zip(dp_s,  ch_s):
            if pdp == dp and  (sn := getsqu(track, (pn := padd(pos, dp)) )) is not None and sn in ch:
                return pos, pn, sn
    print(posp, pos, s)
    return None

        
def buildtrack(track):                  #all tracks covered by kata are single contnuous loops so can be mapped to a circle or a list that is deemed to circle on itself
    track = track.splitlines()          #returns a representation of a pass as a list of 0s and 1s where 1 is a station and 0 and other cell of the track
    t = [0,0]
    pos_s = (0, len(track[0]) - len(track[0].lstrip()) )  #start with zero position
    posp = pos_s
    pos = padd(posp,(0,1))
    tmap = [posp, pos]
    s = getsqu(track, pos)
    assert getsqu(track, posp) == '/'
    assert s == '-'

    while True:
        posp, pos, s = nextsq(track, posp, pos, s)
        if pos == pos_s:
            return t, tmap
        t.append( 1 if s == 'S' else 0)
        tmap.append(pos)
        #print(pos, s)
    return False

class Train:
    def __init__(self, st, pos, track, tmap):                     #takes train string, position and also track as built by the above function
        self.t = track
        self.tmap = tmap
        self.tl = len(track)
        self.l = len(st)
        self.p = pos
        self.stop = 0 if st[0].lower() == "x" else (len(st)-1)  #how log train stops at  station
        self.clockw = 1 if st[0] == st[0].lower() else -1
        self.wait = 1                                       #countdown to next movement for stopped train
        
    def advance(self):
        if self.t[self.p] != 1 or self.wait == 1 or self.stop == 0:
            self.wait = 0
            self.p = (self.p + self.clockw) % self.tl
        elif self.t[self.p] == 1:
            if self.wait == 0:
                self.wait = self.stop
            else:
                self.wait -= 1
                
    def collision(self, train2):
        thisoccupiesl = [self.tmap[(self.p - i*self.clockw) % self.tl]  for i in range(self.l)]
        thatoccupiesl = [self.tmap[(train2.p - i*train2.clockw) % self.tl]  for i in range(train2.l)]
        thisoccupies_s = set(thisoccupiesl)
        thatoccupies_s = set(thatoccupiesl)
        if len(thisoccupiesl) + len(thatoccupiesl) - len(thisoccupies_s) - len(thatoccupies_s) != 0:
            return True
        i = thisoccupies_s & thatoccupies_s
        return True if i else False   

def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    print(track)
    print(repr(track))
    print( a_train, a_train_pos, b_train, b_train_pos, limit)
    track, tmap = buildtrack(track)
    a = Train(a_train, a_train_pos, track, tmap)
    b = Train(b_train, b_train_pos, track, tmap)
    t=0
    while t < limit+1:
        if a.collision(b):
            return t
        a.advance()
        b.advance()
        t += 1
    return -1
  
############################
import sys

def addvec(list1, list2):
    return list(map(lambda x,y:x+y, list1, list2))

def subvec(list1, list2):
    return list(map(lambda x,y:x-y, list1, list2))

class Tracks:
    def __init__(self, trackstr):
        self.trackstr = trackstr
        self.get_track_data()

    def get_char(self, pos):
        return self.tracklines[pos[0]][pos[1]]

    def advance(self, pos, oldpos):
        if self.get_char(pos) in ['+', 'X', 'S', '-', '|']:
            return addvec(pos, subvec(pos,oldpos) )
        if self.get_char(pos) == '/':
            # cardinals
            if pos[1] != len(self.tracklines[0])-1:
                if addvec(pos,[0,1]) != oldpos and \
                       self.get_char(addvec(pos,[0,1])) == '-':
                    return addvec(pos,[0,1])
            if pos[1] != 0:
                if addvec(pos,[0,-1]) != oldpos and \
                       self.get_char(addvec(pos,[0,-1])) == '-':
                    return addvec(pos,[0,-1])
            if pos[0] != len(self.tracklines)-1:
                if addvec(pos,[1,0]) != oldpos and \
                       self.get_char(addvec(pos,[1,0])) == '|':
                    return addvec(pos,[1,0])
            if pos[0] != 0:
                if addvec(pos,[-1,0]) != oldpos and \
                       self.get_char(addvec(pos,[-1,0])) == '|':
                    return addvec(pos,[-1,0])
            # diagonals
            if pos[0] != 0 and pos[1] != len(self.tracklines[0])-1:
                if addvec(pos,[-1,1]) != oldpos and \
                       self.get_char(addvec(pos,[-1,1])) not in [' ', '-', '|']:
                    return addvec(pos,[-1,1])
            if pos[0] != len(self.tracklines)-1 and pos[1] != 0:
                if addvec(pos,[1,-1]) != oldpos and \
                       self.get_char(addvec(pos,[1,-1])) not in [' ', '-', '|']:
                    return addvec(pos,[1,-1])
        if self.get_char(pos) == '\\':
            # cardinals
            if pos[1] != len(self.tracklines[0])-1:
                if addvec(pos,[0,1]) != oldpos and \
                       self.get_char(addvec(pos,[0,1])) == '-':
                    return addvec(pos,[0,1])
            if pos[1] != 0:
                if addvec(pos,[0,-1]) != oldpos and \
                       self.get_char(addvec(pos,[0,-1])) == '-':
                    return addvec(pos,[0,-1])
            if pos[0] != len(self.tracklines)-1:
                if addvec(pos,[1,0]) != oldpos and \
                       self.get_char(addvec(pos,[1,0])) == '|':
                    return addvec(pos,[1,0])
            if pos[0] != 0:
                if addvec(pos,[-1,0]) != oldpos and \
                       self.get_char(addvec(pos,[-1,0])) == '|':
                    return addvec(pos,[-1,0])
            # diagonals
            if pos[0] != 0 and pos[1] != 0:
                if addvec(pos,[-1,-1]) != oldpos and \
                       self.get_char(addvec(pos,[-1,-1])) not in [' ', '-', '|']:
                    return addvec(pos,[-1,-1])
            if pos[0] != len(self.tracklines)-1 and \
                   pos[1] != len(self.tracklines[0])-1:
                if addvec(pos,[1,1]) != oldpos and \
                       self.get_char(addvec(pos,[1,1])) not in [' ', '-', '|']:
                    return addvec(pos,[1,1])
        print('error: cannot advance')
        return None

    def get_cwpath(self):
        path = [self.zeropos]
        if self.get_char(addvec(path[-1],[1,0])) != ' ':
            oldpos = addvec(path[-1],[1,0])
        else:
            oldpos = addvec(path[-1],[1,-1])
        while True:
            nextpos = self.advance(path[-1], oldpos)
            if nextpos == self.zeropos:
                break
            else:
                oldpos = path[-1]
                path.append(nextpos)
        return path

    def get_stations(self):
        stations = []
        for pos in self.path:
            if self.get_char(pos):
                stations.append(pos)
        return stations

    def get_intersects(self):
        intersects = self.stations
        for pos in self.path:
            if self.get_char(pos) in ['X', '+']:
                intersects.append(pos)
        return intersects

    def get_track_data(self):
        self.tracklines = self.trackstr.splitlines()
        colnum = 0
        for line in self.tracklines:
            if len(line) > colnum:
                colnum = len(line)
        self.colnum = colnum
        for k in range(len(self.tracklines)):
            if len(self.tracklines[k]) < colnum:
                self.tracklines[k] = self.tracklines[k] + \
                                     (colnum-len(self.tracklines[k]))*' '
        for j in range(len(self.tracklines[0])):
            if self.tracklines[0][j] != ' ':
                self.zeropos = [0,j]
                break
        self.path = self.get_cwpath()
        self.stations = self.get_stations()
        self.intersects = self.get_intersects()

class Trains:
    def __init__(self, posnum, trainstr, track):
        self.posnum = posnum
        self.track = track # instance of Tracks class
        if trainstr[0].lower() == trainstr[0]:
            self.cw = 1
            self.trainstr = trainstr[0].upper() + \
                        trainstr[1:-1] + trainstr[-1].lower()
        else:
            self.cw = -1
            self.trainstr = trainstr
        if self.trainstr[0] == 'X':
            self.express = True
        else:
            self.express = False
        self.trainlen = len(trainstr)
        self.wait = self.trainlen
        
    def move(self):
        if self.track.get_char(self.track.path[self.posnum]) != 'S' \
                   or self.express == True or self.wait <= 1:
            self.posnum += self.cw
            if self.posnum >= len(self.track.path):
                self.posnum = 0
            elif self.posnum < 0:
                self.posnum = len(self.track.path)-1
            if self.wait <= 1:
                self.wait = self.trainlen
        else:
            self.wait -= 1

    def collide_test(self, other):
        pos1 = other.track.path[other.posnum]
        for j in range(1,self.trainlen):
            pos2 = self.track.path[(self.posnum-self.cw*j)%len(self.track.path)]
            if pos1 == pos2:
                return True
        pos2 = self.track.path[(self.posnum)%len(self.track.path)]
        if self.posnum != other.posnum or self.cw != other.cw:
            if pos1 == pos2:
                return True
        return False
                
def train_crash(trackstr, atrainstr, atrainpos, btrainstr, btrainpos, limit):
    sys.stdout.flush()
    track = Tracks(trackstr)
    atrain = Trains(atrainpos, atrainstr, track)
    btrain = Trains(btrainpos, btrainstr, track)
    # exit at initial intersection
    for j in range(atrain.trainlen):
        pos1 = atrain.track.path[(atrain.posnum-atrain.cw*j)%len(atrain.track.path)]
        for k in range(btrain.trainlen):
            pos2 = btrain.track.path[(btrain.posnum-btrain.cw*k)%len(btrain.track.path)]
            if pos1 == pos2:
                return 0
    # exit at initial self intersection
    for j in range(atrain.trainlen):
        pos1 = atrain.track.path[(atrain.posnum-atrain.cw*j)%len(atrain.track.path)]
        for k in range(j+1,atrain.trainlen):
            pos2 = atrain.track.path[(atrain.posnum-atrain.cw*k)%len(atrain.track.path)]
            if pos1 == pos2:
                return 0
    for j in range(btrain.trainlen):
        pos1 = btrain.track.path[(btrain.posnum-btrain.cw*j)%len(btrain.track.path)]
        for k in range(j+1,btrain.trainlen):
            pos2 = btrain.track.path[(btrain.posnum-btrain.cw*k)%len(btrain.track.path)]
            if pos1 == pos2:
                return 0
    # start at station wait adjustment
    if atrain.track.get_char(atrain.track.path[atrain.posnum]) == 'S':
        atrain.wait = 1
    if btrain.track.get_char(btrain.track.path[btrain.posnum]) == 'S':
        btrain.wait = 1
    # simulate
    for j in range(limit+1):
        if atrain.collide_test(btrain) or btrain.collide_test(atrain) \
                    or atrain.collide_test(atrain) or btrain.collide_test(btrain):
            return j
        atrain.move()
        btrain.move()
    return -1
  
############################
class Train:
    def __init__(self, train, step_Pos, track_Steps, track_Step_Map, letter_Replacement):
        self.length = len(train)
        self.cars = len(train) - 1  # For determining stop time at train stations
        self.layover = 0
        self.train_Type = 'express' if train[0] in ['x', 'X'] else 'standard'
        new_Train = ''
        for idx, val in enumerate(train):
            if val.isupper(): new_Train += letter_Replacement.upper()
            else: new_Train += letter_Replacement
        train = new_Train
        self.train_Description = train[0].lower()
        self.direction = [[0, -1]] if train[0].isupper() else [[0, 1]]
        self.orientation = 'West' if train[0].isupper() else 'East'

        self.train_Step_Positions = []
        self.engine_Step_Pos = step_Pos
        self.tail_Step_Pos = None
        self.track_Steps = track_Steps
        self.track_Step_Map = track_Step_Map
        self.train_Positions = []
        self.engine_Pos = None
        self.tail_Pos = None
        self.find_Step_Positions()  # Finds step positions of tail and cars

    def find_Step_Positions(self):  # The position of train segments given in steps
        if self.direction == [[0, 1]]:  # East
            self.tail_Step_Pos = self.engine_Step_Pos - self.length + 1
            if self.tail_Step_Pos < 0:
                self.tail_Step_Pos = self.track_Steps + self.tail_Step_Pos + 1
            for step_Pos in range(self.engine_Step_Pos, self.engine_Step_Pos - self.length, -1):
                if step_Pos < 0:
                    self.train_Positions.insert(0, self.track_Step_Map[self.track_Steps + step_Pos + 1])
                    self.train_Step_Positions.append(self.track_Steps + step_Pos + 1)
                else:
                    self.train_Step_Positions.append(step_Pos)
                    self.train_Positions.insert(0, self.track_Step_Map[step_Pos])
            self.engine_Pos = self.train_Positions[-1]
            self.tail_Pos = self.train_Positions[0]
        else:  # West
            self.tail_Step_Pos = self.engine_Step_Pos + self.length - 1
            if self.tail_Step_Pos > self.track_Steps:
                self.tail_Step_Pos = self.tail_Step_Pos - self.track_Steps - 1
            for step_Pos in range(self.engine_Step_Pos, self.engine_Step_Pos + self.length):
                if step_Pos > self.track_Steps:
                    self.train_Positions.append(self.track_Step_Map[step_Pos - self.track_Steps - 1])
                    self.train_Step_Positions.append(step_Pos - self.track_Steps - 1)
                else:
                    self.train_Positions.append(self.track_Step_Map[step_Pos])
                    self.train_Step_Positions.append(step_Pos)
            self.engine_Pos = self.train_Positions[0]
            self.tail_Pos = self.train_Positions[-1]

        print(self.orientation)
        print(self.train_Positions)
        print(self.engine_Pos)
        print(self.tail_Pos)
        print(self.train_Step_Positions)
        print('-----------')

class Driver:
    def __init__(self, str_Track, t_1, t_1_Step, t_2, t_2_Step, step_Limit):
        self.t_1 = t_1
        self.t_1_Step = t_1_Step
        self.t_2 = t_2
        self.t_2_Step = t_2_Step
        self.train_1 = None
        self.train_2 = None
        self.trains = []
        self.visited = []
        self.track_Reference = [[char for char in line] for line in str_Track.splitlines()]
        self.track = [[char for char in line] for line in str_Track.splitlines()]
        self.track_Segments = ["-", '|', '/', '\\', '+', 'X', 'S']
        self.step_Limit = step_Limit
        self.direction = [[0, 1]]  # For first loop around track.
        self.station_Positions = []
        self.current_Position = None  # Assuming this always start at row 0. Could be a bad assumption.
        self.steps = 0
        self.step_Map = {}  # Map track positions (y, x) to step position
        self.vector_Map = {
            (0, 1): {'S': [(0, 1)], '-': [(0, 1)], '/': [(-1, 0), (-1, 1)], '\\': [(1, 1), (1, 0)], '+': [(0, 1)]},  # R
            (1, 0): {'S': [(1, 0)], '|': [(1, 0)], '/': [(0, -1), (1, -1)], '\\': [(0, 1), (1, 1)], '+': [(1, 0)]},  # D
            (0, -1): {'S': [(0, -1)], '-': [(0, -1)], '/': [(1, 0), (1, -1)], '\\': [(-1, 0), (-1, -1)],
                      '+': [(0, -1)]},  # L Changed '/': [(0, 1)]
            (-1, 0): {'S': [(-1, 0)], '|': [(-1, 0)], '/': [(0, 1), (-1, 1)], '\\': [(-1, -1), (0, -1)],
                      '+': [(-1, 0)]},
            (1, -1): {'X': [(1, -1)], '-': [(0, -1)], 'S': [(1, -1)], '|': [(1, 0)], '/': [(1, 0), (0, -1), (1, -1)]},  # DL
            (1, 1): {'X': [(1, 1)], '-': [(0, 1)], 'S': [(1, 1)], '|': [(1, 0)], '\\': [(1, 1), (0, 1), (1, 0)]},  # DR
            (-1, 1): {'X': [(-1, 1)], '-': [(0, 1)], 'S': [(-1, 1)], '|': [(-1, 0)], '/': [(-1, 1), (-1, 0), (0, 1)]},  # UR
            (-1, -1): {'X': [(-1, -1)], '-': [(0, -1)], 'S': [(-1, -1)], '|': [(-1, 0)], '\\': [(-1, -1), (-1, 0), (0, -1)]}  # UL
        }

        self.legal_Transitions = {
            'S': {(0, 1): ['-'], (0, -1): ['-'], (1, 0): ['|'], (-1, 0): '|', (1, 1): ['\\'], (1, -1): ['/'], (-1, 1): ['/'], (-1, -1): '\\'},
            '-': {(0, 1): ['-', '/', '\\', '+', 'S'], (0, -1): ['-', '/', '\\', '+', 'S']},
            '|': {(1, 0): ['|', '\\', '/', '+', 'S'], (-1, 0): ['|', '\\', '/', '+', 'S']},
            '/': {(-1, 1): ['X', '/', 'S'], (1, -1): ['X', '/', 'S'],  (0, 1): ['-', '+', 'S'], (0, -1): ['-', '+', 'S'], (1, 0): ['|', '+', 'S'], (-1, 0): ['|', '+', 'S']},
            '\\': {(1, 1): ['X', '\\', 'S'], (-1, -1): ['X', '\\', 'S'], (0, 1): ['-', '+', 'S'], (0, -1): ['-', '+', 'S'], (1, 0): ['|', '+', 'S'], (-1, 0): ['|', '+', 'S']},
            '+': {(0, 1): ['-', '/', 'S'], (0, -1): ['-', '\\', 'S'], (1, 0): ['|', '/', '\\', 'S'], (-1, 0): ['|', '/', '\\', 'S']},
            'X': {(-1, 1): ['/'], (1, -1): ['/'], (1, 1): ['\\'], (-1, -1): ['\\']}
        }

    def find_Start(self):
        for row_Idx, row in enumerate(self.track):
            for col_Idx, col in enumerate(row):
                if col in self.track_Segments:
                    self.current_Position = [row_Idx, col_Idx]
                    return

    def check_In_Bounds(self, pos):
        if pos[0] >= 0 and pos[0] < len(self.track) and pos[1] >= 0 and pos[1] < len(self.track[pos[0]]):
            return True
        return False

    def find_Relative_Direction(self):  # Finds trains direction relative to the track position
        for train in self.trains:
            step_Pos = train.engine_Step_Pos + 1
            # Could be a greater than track step max error here
            if step_Pos in self.step_Map:
                test_Pos = self.step_Map[step_Pos]
                if self.track[self.step_Map[step_Pos][0]][self.step_Map[step_Pos][1]] not in \
                        [train.train_Description.upper(), train.train_Description.lower()]:
                    train.direction = [[test_Pos[0] - train.engine_Pos[0], test_Pos[1] - train.engine_Pos[1]]]
                else:
                    step_Pos = train.engine_Step_Pos - 1
                    if step_Pos < 0:
                        step_Pos = self.steps + step_Pos + 1
                    test_Pos = self.step_Map[step_Pos]
                    train.direction = [[test_Pos[0] - train.engine_Pos[0], test_Pos[1] - train.engine_Pos[1]]]

    def place_Trains(self):  # Should handle two trains starting at same position here.
        for train in self.trains:
            for position_Idx, position in enumerate(train.train_Positions):
                if position_Idx == 0:
                    self.track[position[0]][position[1]] = train.train_Description.upper()
                else:
                    self.track[position[0]][position[1]] = train.train_Description

    def find_Next_Pos(self, current_Pos, direction):
        for _dir in direction:
            next_Pos = [current_Pos[0] + _dir[0], current_Pos[1] + _dir[1]]
            if self.check_In_Bounds(next_Pos):
                if self.track_Reference[next_Pos[0]][next_Pos[1]] != ' ' and\
                        self.track_Reference[next_Pos[0]][next_Pos[1]] in \
                        self.legal_Transitions[self.track_Reference[current_Pos[0]][current_Pos[1]]][tuple(_dir)]:
                    self.visited.append(next_Pos)
                    return next_Pos, _dir

    def initial_Loop(self):

        self.track[self.current_Position[0]][self.current_Position[1]] = '!'  # Mark start of track

        while True:
            next_Pos, direction = self.find_Next_Pos(self.current_Position, self.direction)
            self.step_Map[self.steps] = self.current_Position
            if self.track[next_Pos[0]][next_Pos[1]] == '!':  # First Loop Complete
                self.track[next_Pos[0]][next_Pos[1]] = self.track_Reference[next_Pos[0]][next_Pos[1]]
                self.train_1 = Train(self.t_1, self.t_1_Step, self.steps, self.step_Map, 'a')
                self.train_2 = Train(self.t_2, self.t_2_Step, self.steps, self.step_Map, 'b')
                self.trains = [self.train_1, self.train_2]
                self.place_Trains()
                self.find_Relative_Direction()
                self.steps = 0

                return True

            self.steps += 1
            self.step_Map[self.steps] = next_Pos
            next_Direction = self.vector_Map[tuple(direction)][self.track[next_Pos[0]][next_Pos[1]]]

            if self.track[next_Pos[0]][next_Pos[1]] == 'S':
                self.station_Positions.append(next_Pos)

            self.current_Position = next_Pos
            self.direction = next_Direction

    def move_Train(self, train, next_Pos):
        if train.orientation == 'West':  # [Engine, Car, Car, Tail]
            train.train_Positions.insert(0, next_Pos)
            train.train_Positions.pop(-1)
            train.engine_Pos = next_Pos
            train.tail_Pos = train.train_Positions[-1]
        else:  # East  [Tail, Car, Car, Engine]
            train.train_Positions.append(next_Pos)
            train.train_Positions.pop(0)
            train.engine_Pos = next_Pos
            train.tail_Pos = train.train_Positions[0]

    def run_Trains(self):
        for train in self.trains:
            if train.layover > 0:
                continue
            self.track[train.tail_Pos[0]][train.tail_Pos[1]] = \
                self.track_Reference[train.tail_Pos[0]][train.tail_Pos[1]]  # Remove Tail
        for train in self.trains:

            if train.layover > 0:
                train.layover -= 1
                continue

            next_Pos, direction = self.find_Next_Pos(train.engine_Pos, train.direction)

            if self.track[next_Pos[0]][next_Pos[1]] in [self.train_1.train_Description.upper(),
                                                        self.train_1.train_Description.lower(),
                                                        self.train_2.train_Description.upper(),
                                                        self.train_2.train_Description.lower()]:
                self.steps += 1
                if self.steps <= self.step_Limit:
                    return self.steps
                else:
                    return -1

            if self.steps >= self.step_Limit:
                return -1

            next_Direction = self.vector_Map[tuple(direction)][self.track[next_Pos[0]][next_Pos[1]]]

            self.track[next_Pos[0]][next_Pos[1]] = train.train_Description  # Redraw Engine
            self.move_Train(train, next_Pos)
            train.direction = next_Direction

            if train.engine_Pos in self.station_Positions and train.train_Type == 'standard':
                train.layover = train.cars
        self.steps += 1
        return 'Run'

def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    print(track, flush=True)
    print(a_train)
    print(a_train_pos)
    print(b_train)
    print(b_train_pos)
    print(limit)
    driver = Driver(track, a_train, a_train_pos, b_train, b_train_pos, limit)
    driver.find_Start()
    driver.initial_Loop()
    for train_1_Pos in driver.train_1.train_Positions:
        if train_1_Pos in driver.train_2.train_Positions:
            return 0
    new_1 = []
    new_2 = []
    for step in driver.train_1.train_Positions:
        if step not in new_1:
            new_1.append(step)
    if len(new_1) != len(driver.train_1.train_Positions):
        return 0
    for step in driver.train_2.train_Positions:
        if step not in new_2:
            new_2.append(step)
    if len(new_2) != len(driver.train_2.train_Positions):
        return 0
    collision = "Run"
    while collision == 'Run':
        collision = driver.run_Trains()
    if collision == -1: 
        return -1            
    if collision == 0:
        return 0
    return collision
  
################################
import itertools

connection_lookup = [[-1,0], [-1, 1], [0, 1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1]]

track_lookup = {
    '/': [0,1,2,4,5,6],
    '\\': [0,2,3,4,6,7],
    '-': [2,6],
    '|': [0,4],
    '+': [0,2,4,6],
    'X': [1,3,5,7],
    'S': [0,1,2,3,4,5,6,7],
    ' ': []
    
    }

def safe(track_array, r, c):
    try:
        if r < 0 or c < 0:
            return ' '
        else:
            return track_array[r][c]
    except IndexError:
        return ' '
    
def list_connections(track_array, r, c):
    to_check = track_lookup[track_array[r][c]].copy()

    #extra special cases: + crossings with one slanted track
    if track_array[r][c] == '/' and \
        (safe(track_array, r + connection_lookup[6][0], c + connection_lookup[6][1]) == '+'
         or safe(track_array, r + connection_lookup[4][0], c + connection_lookup[4][1]) == '+'):
        to_check.remove(5)
    
    if track_array[r][c] == '/' and \
        (safe(track_array, r + connection_lookup[0][0], c + connection_lookup[0][1]) == '+'
         or safe(track_array, r + connection_lookup[2][0], c + connection_lookup[2][1]) == '+'):
        to_check.remove(1)
        
    if track_array[r][c] == '\\' and \
        (safe(track_array, r + connection_lookup[6][0], c + connection_lookup[6][1]) == '+'
         or safe(track_array, r + connection_lookup[4][0], c + connection_lookup[4][1]) == '+'):
        to_check.remove(7)
    
    if track_array[r][c] == '\\' and \
        (safe(track_array, r + connection_lookup[0][0], c + connection_lookup[0][1]) == '+'
         or safe(track_array, r + connection_lookup[2][0], c + connection_lookup[2][1]) == '+'):
        to_check.remove(3)
        
    if track_array[r][c] in ['/','\\']:
        return [x for x in to_check if x % 2 == 0 \
                and safe(track_array, r + connection_lookup[x][0], c + connection_lookup[x][1]) not in  [' ','/','\\'] \
                    and ((x % 4 == 0 and safe(track_array, r + connection_lookup[x][0], c + connection_lookup[x][1]) != '-') \
                        or (x % 4 == 2 and safe(track_array, r + connection_lookup[x][0], c + connection_lookup[x][1]) != '|'))] \
            + [x for x in to_check if x % 2 == 1 and safe(track_array, r + connection_lookup[x][0], c + connection_lookup[x][1]) not in  [' ','|','-']]

    return [x for x in to_check if safe(track_array, r + connection_lookup[x][0], c + connection_lookup[x][1]) != ' ']


class Track:
    _paths = {}
    _r, _c = 0,0
    _is_station = False
    
    def __init__(self, paths = None, is_station = False, r = 0, c = 0):
        self._paths = paths
        self._is_station = is_station
        self._r = r
        self._c = c
    
    def __eq__(self, o):
        return self._r == o._r and self._c == o._c
    
    def next_track(self, track_objs, n):
        return track_objs[self._r + connection_lookup[self._paths[n]][0]] \
            [self._c + connection_lookup[self._paths[n]][1]]

def run_to_start(train, track_objs, zero_pos, train_start):
    if train[0].isupper():
        entrypoint = 2
    else:
        entrypoint = track_objs[0][zero_pos]._paths[2]
    
    a_train_obj = (1, track_objs[0][zero_pos])
    
    while a_train_obj[1] != train_start:
        #print(str(a_train_obj[1]._r) + ' ' + str(a_train_obj[1]._c))
        newentrypoint = (a_train_obj[1]._paths[entrypoint] + 4) % 8 
        a_train_obj = (1, a_train_obj[1].next_track(track_objs, entrypoint))
        entrypoint = newentrypoint
    
    return a_train_obj[1], entrypoint

def train_step_forward(a_train_obj, track_objs):
#    print(str(a_train_obj[0][1]._r) + ' ' + str(a_train_obj[0][1]._c))
    for c in range(len(a_train_obj)):
        entrypoint = a_train_obj[c][0]
        newentrypoint = (a_train_obj[c][1]._paths[entrypoint] + 4) % 8 
        a_train_obj[c] = (newentrypoint, a_train_obj[c][1].next_track(track_objs, entrypoint))
        entrypoint = newentrypoint

def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    print(track)
    print(a_train)
    print(a_train_pos)
    print(b_train)
    print(b_train_pos)
    print(limit)
    # convert track from string to 2D array
    track_array = list(map(list, track.splitlines()))
    
    track_objs = list()
    
    # step through each position, see what kind of track piece it is, and create a Track object
    try:        
        for r in range(len(track_array)):
            newrow = list()
            for c in range(len(track_array[r])):

                paths = list_connections(track_array, r, c)
                if len(paths) == 2:
                    newrow.append(Track({paths[0]: paths[1], paths[1]: paths[0]}
                                             ,track_array[r][c] == 'S', r, c))
                elif len(paths) == 4:
                    newrow.append(Track({paths[0]: paths[2], paths[2]: paths[0]
                                              ,paths[1]: paths[3], paths[3]: paths[1]}
                             ,track_array[r][c] == 'S', r, c))
                else: #no track
                    newrow.append(None)
            
            track_objs.append(newrow)
    except:
        pass
    
    # "zero position" defined as top-most then left-most '/', if I interpret the instructions right
    zero_pos = track.find('/')
    
    a_train_start, b_train_start = None, None

    
    # find the track pieces where the trains' engines will begin
    # by running a virtual train clockwise from zero position.
    # Doesn't matter which way they face for this step.
    starter_train_obj = (1, track_objs[0][zero_pos])
    entrypoint = track_objs[0][zero_pos]._paths[2]
    
    for counter in range(len(track)):
        if counter == a_train_pos:
            a_train_start = starter_train_obj[1]
        if counter == b_train_pos:
            b_train_start = starter_train_obj[1]
        
        newentrypoint = (starter_train_obj[1]._paths[entrypoint] + 4) % 8 
        starter_train_obj = (1, starter_train_obj[1].next_track(track_objs, entrypoint))
        entrypoint = newentrypoint    

    
    # start each engine at zero-position and run them in the correct direction 
    # until they get to their starting spot
    a_train_first, a_entrypoint = run_to_start(a_train, track_objs, zero_pos, a_train_start)
    b_train_first, b_entrypoint = run_to_start(b_train, track_objs, zero_pos, b_train_start)
    
    # each train will be a list of tuples (entrypoint, Track)
    # entrypoint must be correct for direction train faces
    a_train_obj = [(a_entrypoint, a_train_first)]
    b_train_obj = [(b_entrypoint, b_train_first)]
    
    entrypoint = a_train_start._paths[a_entrypoint]
    # grow train backward from engine, but with each car facing forward
    for c in range(len(a_train) - 1):
        newentrypoint = (a_train_obj[c][1]._paths[entrypoint] + 4) % 8
        nexttrack = a_train_obj[c][1].next_track(track_objs, entrypoint)
        a_train_obj.append((nexttrack._paths[newentrypoint], track_objs[nexttrack._r][nexttrack._c]))
        entrypoint = newentrypoint
        
    entrypoint = b_train_start._paths[b_entrypoint]
    # grow trains backward
    for c in range(len(b_train) - 1):
        newentrypoint = (b_train_obj[c][1]._paths[entrypoint] + 4) % 8
        nexttrack = b_train_obj[c][1].next_track(track_objs, entrypoint)
        b_train_obj.append((nexttrack._paths[newentrypoint], track_objs[nexttrack._r][nexttrack._c]))
        entrypoint = newentrypoint
    
    a_pause, b_pause = 0, 0
    # run simulation
    for i in range(limit + 1):
        #print(str(a_train_obj[0][1]._r) + ' ' + str(a_train_obj[0][1]._c))
        #check for collisions at current positions
        for x in itertools.permutations(itertools.chain(a_train_obj, b_train_obj), 2):
            if x[0][1] == x[1][1]:
                return i
        
        if a_pause == 0:
            train_step_forward(a_train_obj, track_objs)
            
            if a_train_obj[0][1]._is_station and a_pause == 0 and a_train[0].upper() != 'X':
                a_pause = len(a_train_obj) - 1
        else:
            a_pause -= 1
        
        if b_pause == 0:
            train_step_forward(b_train_obj, track_objs)
            
            if b_train_obj[0][1]._is_station and b_pause == 0 and b_train[0].upper() != 'X':
                b_pause = len(b_train_obj) - 1
        else:
            b_pause -= 1
            
    return -1
