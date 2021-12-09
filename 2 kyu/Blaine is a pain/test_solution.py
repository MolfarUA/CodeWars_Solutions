TRACK_EX = """\
                                /------------\\
/-------------\\                /             |
|             |               /              S
|             |              /               |
|        /----+--------------+------\\        |   
\\       /     |              |      |        |     
 \\      |     \\              |      |        |                    
 |      |      \\-------------+------+--------+---\\
 |      |                    |      |        |   |
 \\------+--------------------+------/        /   |
        |                    |              /    | 
        \\------S-------------+-------------/     |
                             |                   |
/-------------\\              |                   |
|             |              |             /-----+----\\
|             |              |             |     |     \\
\\-------------+--------------+-----S-------+-----/      \\
              |              |             |             \\
              |              |             |             |
              |              \\-------------+-------------/
              |                            |               
              \\----------------------------/ 
"""

TRACK_LOOP_S0 = """\
/-----------------\\
|                 |
|                 |
|                 |
|                 |
\\-----------------/"""

TRACK_LOOP_S1 = """\
/-----------------\\
|                 |
|                 |
|                 |
|                 |
\\---------S-------/"""

TRACK_LOOP_S2 = """\
/------S----------\\
|                 |
|                 |
|                 |
|                 |
\\----------S------/"""

TRACK_EIGHT_S0 = """\
/-------\\ 
|       | 
|       | 
|       | 
\\-------+--------\\
        |        |
        |        |
        |        |
        \\--------/

"""

TRACK_EIGHT_S1 = """\
/-------\\ 
|       | 
|       | 
|       | 
\\-------+--------\\
        |        |
        S        |
        |        |
        \\--------/

"""

TRACK_EIGHT_S2 = """\
/-------\\ 
|       | 
S       | 
|       | 
\\-------+--------\\
        |        |
        S        |
        |        |
        \\--------/

"""

TRACK_CENTRAL_STATION_8 = """\
/-------\\ 
|       | 
|       | 
|       | 
\\-------S--------\\
        |        |
        |        |
        |        |
        \\--------/"""

TRACK_CENTRAL_STATION_X = """\
/----\\     /----\\ 
|     \\   /     | 
|      \\ /      | 
|       S       | 
|      / \\      | 
|     /   \\     | 
\\----/     \\----/"""

TRACK_SLUG_S0 = """\
/-------\\ 
|       | 
|       | 
\\-------+-------------------------------------------------------------------\\ 
        |                                                                   |
        |                                                                   |
        \\-------------------------------------------------------------------/"""
        
        
        
TRACK_PARALLEL_B4B_S0 = """\
/------\\               /--\\
|      |               |  |
|      \\---------------/  |
\\------\\               /--/ 
       |               |
       \\---------------/
"""


TRACK_PARALLEL_B4B2_S0 = """\
/---\\
|   |
\--\|
   ||
   |\\------\\
   |/----\\ |
   ||    | |
/--/|    | |
|   |    | |
\\---/    \\-/
"""


TRACK_XXX_S0 = """\
/-----\\   /-----\\   /-----\\   /-----\\ 
|      \\ /       \\ /       \\ /      | 
|       X         X         X       | 
|      / \\       / \\       / \\      | 
\\-----/   \\-----/   \\-----/   \\-----/ 
"""


TRACK_PARALLEL_SNAIL_S0 = """\
    /---------------------\\               /-\\ /-\\  
   //---------------------\\\\              | | | |  
  //  /-------------------\\\\\\             | / | /  
  ||  |/------------------\\\\\\\\            |/  |/   
  ||  ||                   \\\\\\\\           ||  ||   
  \\\\  ||                   | \\\\\\          ||  ||   
   \\\\-//                   | || \\---------/\\--/|   
/-\\ \\-/                    \\-/|                |   
|  \\--------------------------/                |   
\\----------------------------------------------/   
"""




test.describe("Sample test")

test.it("example")
"""// Kata example"""
test.assert_equals(train_crash(TRACK_EX, "Aaaa", 147, "Bbbbbbbbbbb", 288, 1000), 516)
print("<COMPLETEDIN::>")
print("<COMPLETEDIN::>")




test.describe("More tests")  

test.it("No crash #0")
"""// chase each other - 0 stations"""
test.assert_equals(train_crash(TRACK_LOOP_S0, "aaaaaA", 10, "bbbbbB", 30, 100), -1)
test.assert_equals(train_crash(TRACK_EIGHT_S0, "aaaaaA", 15, "bbbbbB", 5, 100), -1)
print("<COMPLETEDIN::>")

  
test.it("No crash #1")
"""// chase each other - 1 station"""
test.assert_equals(train_crash(TRACK_LOOP_S1, "aaaaaA", 10, "bbbbbB", 30, 100), -1)
test.assert_equals(train_crash(TRACK_EIGHT_S1, "aaaaaA", 15, "bbbbbB", 5, 100), -1)
print("<COMPLETEDIN::>")
  
  
test.it("No crash #2")
"""// chase each other - 2 stations"""
test.assert_equals(train_crash(TRACK_LOOP_S2, "aaaaaA", 10, "bbbbbB", 30, 100), -1)
test.assert_equals(train_crash(TRACK_EIGHT_S2, "aaaaaA", 15, "bbbbbB", 5, 100), -1)
print("<COMPLETEDIN::>")

  
test.it("No crash #3 - central satation")
"""// chase each other - central station!!"""
test.assert_equals(train_crash(TRACK_CENTRAL_STATION_8, "aaaaaA", 10, "bbbbbB", 20, 100), -1)
test.assert_equals(train_crash(TRACK_CENTRAL_STATION_X, "aaaaaA", 8, "bbbbbB", 20, 100), -1)
print("<COMPLETEDIN::>")

  
test.it("Tailgate loop")
"""// tailgate each other around a simple loop"""
test.assert_equals(train_crash(TRACK_LOOP_S0, "aaaA", 10, "bbbB", 14, 100), -1)
print("<COMPLETEDIN::>")
  
  
test.it("Tailgate eight")
"""// tailgate each other around a figure 8"""
      
test.assert_equals(train_crash(TRACK_EIGHT_S0, "aaaA", 10, "bbbB", 14, 100), -1)
print("<COMPLETEDIN::>")
  
  
test.it("Crash chicken run")
"""// trains heading in opposite directions"""
test.assert_equals(train_crash(TRACK_LOOP_S0, "aaaA", 10, "Bbbb", 40, 100), 15)
print("<COMPLETEDIN::>")
  
  
test.it("Crash Kamikaze")
""" // head-on crash into a stationary train"""
test.assert_equals(train_crash(TRACK_LOOP_S1, "xX", 15, "Zzzzzzzzzzzzzz", 40, 100), 16)
print("<COMPLETEDIN::>")
  
  
test.it("Crash cabooser")
"""// chase each other - ram staionary train from behind"""
test.assert_equals(train_crash(TRACK_LOOP_S1, "aA", 10, "bbbbbB", 30, 200), 157)
print("<COMPLETEDIN::>")
  
  
test.it("Crash T-bone")
"""// two moving trains collide at a crossing"""
test.assert_equals(train_crash(TRACK_EIGHT_S0, "aaaA", 0, "bbbbbbbbbbbbbB", 30, 100), 12)
print("<COMPLETEDIN::>")
  
  
test.it("Crash T-bone at station")
"""// moving train T-bones another train at a staion"""
test.assert_equals(train_crash(TRACK_EIGHT_S1, "aaaA", 22, "bbbbB", 0, 100), 16)
print("<COMPLETEDIN::>")
  
  
test.it("Limits")
"""// these trains crash after 16 iterations. But will Blain wait that long?"""
test.assert_equals(train_crash(TRACK_EIGHT_S1, "aaaA", 22, "bbbbB", 0, 0), -1)
test.assert_equals(train_crash(TRACK_EIGHT_S1, "aaaA", 22, "bbbbB", 0, 15), -1)
test.assert_equals(train_crash(TRACK_EIGHT_S1, "aaaA", 22, "bbbbB", 0, 16), 16)
test.assert_equals(train_crash(TRACK_EIGHT_S1, "aaaA", 22, "bbbbB", 0, 17), 16)
print("<COMPLETEDIN::>")
  
  
test.it("MultiExpress")
"""// chase each other - express trains don't stop at stations
   // same as crashFromBehind but these are express trains so they won't stop """
test.assert_equals(train_crash(TRACK_LOOP_S1, "xX", 10, "xxxxxX", 30, 200), -1)
print("<COMPLETEDIN::>")
  
  
test.it("Letters")
"""// chase each other - ram staionary train from behind (different letter test)"""
test.assert_equals(train_crash(TRACK_LOOP_S1, "zZ", 10, "zzzzzZ", 30, 200), 157)
test.assert_equals(train_crash(TRACK_LOOP_S1, "sS", 10, "sssssS", 30, 200), 157)
"""// express crashes sooner because it does not stop"""
test.assert_equals(train_crash(TRACK_LOOP_S1, "xX", 10, "sssssS", 30, 200), 108)
print("<COMPLETEDIN::>")
  
  
test.it("Crash self destruct")
"""// long train runs into itself"""
test.assert_equals(train_crash(TRACK_SLUG_S0, "aA", 10, "oooooooooooooooooooooooooO", 70, 200), 105)
print("<COMPLETEDIN::>")
  
  
test.it("Near miss with itself")
"""// long train almost runs into itself"""
test.assert_equals(train_crash(TRACK_SLUG_S0, "aA", 10, "oooooooooooooooooooooO", 70, 200), -1)
print("<COMPLETEDIN::>")
  
  
test.it("Near miss at crossing")
"""// two chasing trains have near miss at crossing"""
test.assert_equals(train_crash(TRACK_EIGHT_S0, "ooooooO", 10, "xxxxxxX", 27, 100), -1)
print("<COMPLETEDIN::>")
  
  
test.it("Crash before started")
"""// sometimes trains are badly positioned right from the start"""
"""// two trains overlap"""
test.assert_equals(train_crash(TRACK_LOOP_S0, "oO", 10, "oO", 10, 100), 0)
test.assert_equals(train_crash(TRACK_LOOP_S0, "oO", 10, "oO", 10, 0), 0)
test.assert_equals(train_crash(TRACK_LOOP_S0, "oO", 10, "oO", 11, 100), 0)
test.assert_equals(train_crash(TRACK_LOOP_S0, "oO", 10, "oO", 11, 0), 0)
test.assert_equals(train_crash(TRACK_LOOP_S0, "oO", 10, "oO", 12, 100), -1)
"""// single train overlaps"""    
test.assert_equals(train_crash(TRACK_CENTRAL_STATION_X, "Eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", 7, "Xxxx", 0, 100), 0)
test.assert_equals(train_crash(TRACK_XXX_S0, "Eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", 27, "Xxxx", 0, 100), 0)
test.assert_equals(train_crash(TRACK_CENTRAL_STATION_X, "aaaaaaaaaaaaaaaaaaaaaaaaaaaA", 31, "Cccccccc", 36, 100), 0);
print("<COMPLETEDIN::>")



test.it("No crash #0 - Tricky")
test.assert_equals(train_crash(TRACK_XXX_S0,            "aaaA", 15, "bbbB", 5, 100), -1)
test.assert_equals(train_crash(TRACK_PARALLEL_B4B_S0,   "aaaA", 15, "bbbB", 5, 500), -1)
test.assert_equals(train_crash(TRACK_PARALLEL_SNAIL_S0, "aaaA", 15, "bbbB", 5, 1000), -1)
print("<COMPLETEDIN::>")


test.it("Crashes - Tricky")
test.assert_equals(train_crash(TRACK_CENTRAL_STATION_X, "Eeeeeeee", 32, "Xxxx", 23, 100), 15)
test.assert_equals(train_crash(TRACK_CENTRAL_STATION_X, "Eeeeeeee", 27, "Xxxx", 7, 100), 0)
test.assert_equals(train_crash(TRACK_PARALLEL_B4B2_S0, "Eee", 33, "aaA", 2, 100), 16)
test.assert_equals(train_crash(TRACK_PARALLEL_B4B2_S0, "Eee", 10, "aaA", 20, 100), 22)
print("<COMPLETEDIN::>")

test.it("Start exactly on the station")
"""// When the train happens to start *exactly* on a station then they leave it"""
"""// on the next move (regardless if they are express or suburban trains)"""
test.assert_equals(train_crash(TRACK_LOOP_S2, "aaaaaaaaaaaaA", 7, "xxxX", 30, 100), 34)
test.assert_equals(train_crash(TRACK_LOOP_S2, "aaA", 7, "Bbbb", 9, 100), 1)
print("<COMPLETEDIN::>")
print("<COMPLETEDIN::>")





test.it("Random test")
def randomTests():
    """ Redefine all the tracks in the closure, to avoid cheating problems """

    TRACK_EX = """\
                                /------------\\
/-------------\\                /             |
|             |               /              S
|             |              /               |
|        /----+--------------+------\\        |   
\\       /     |              |      |        |     
 \\      |     \\              |      |        |                    
 |      |      \\-------------+------+--------+---\\
 |      |                    |      |        |   |
 \\------+--------------------+------/        /   |
        |                    |              /    | 
        \\------S-------------+-------------/     |
                             |                   |
/-------------\\              |                   |
|             |              |             /-----+----\\
|             |              |             |     |     \\
\\-------------+--------------+-----S-------+-----/      \\
              |              |             |             \\
              |              |             |             |
              |              \\-------------+-------------/
              |                            |               
              \\----------------------------/ 
"""

    TRACK_LOOP_S0 = """\
/-----------------\\
|                 |
|                 |
|                 |
|                 |
\\-----------------/"""

    TRACK_LOOP_S1 = """\
/-----------------\\
|                 |
|                 |
|                 |
|                 |
\\---------S-------/"""

    TRACK_LOOP_S2 = """\
/------S----------\\
|                 |
|                 |
|                 |
|                 |
\\----------S------/"""

    TRACK_EIGHT_S0 = """\
/-------\\ 
|       | 
|       | 
|       | 
\\-------+--------\\
        |        |
        |        |
        |        |
        \\--------/

"""

    TRACK_EIGHT_S1 = """\
/-------\\ 
|       | 
|       | 
|       | 
\\-------+--------\\
        |        |
        S        |
        |        |
        \\--------/
"""

    TRACK_EIGHT_S2 = """\
/-------\\ 
|       | 
S       | 
|       | 
\\-------+--------\\
        |        |
        S        |
        |        |
        \\--------/
"""

    TRACK_CENTRAL_STATION_8 = """\
/-------\\ 
|       | 
|       | 
|       | 
\\-------S--------\\
        |        |
        |        |
        |        |
        \\--------/"""

    TRACK_CENTRAL_STATION_X = """\
/----\\     /----\\ 
|     \\   /     | 
|      \\ /      | 
|       S       | 
|      / \\      | 
|     /   \\     | 
\\----/     \\----/"""

    TRACK_SLUG_S0 = """\
/-------\\ 
|       | 
|       | 
\\-------+-------------------------------------------------------------------\\ 
        |                                                                   |
        |                                                                   |
        \\-------------------------------------------------------------------/"""
    
    TRACK_RANDOM_S2 = """\
/-------\\ 
|       | 
|       | 
|       | 
\\-------+-------------S-----------------------------------------------\\ 
        |                                                             | 
        |                                                             | 
        \\-----------------------------------S-------------------------+--------\\ 
                                                                      |        | 
                                                                      |        | 
                                                                      |        | 
                                                                      \\--------/"""
    
            
    TRACK_PARALLEL_B4B_S0 = """\
/------\\               /--\\
|      |               |  |
|      \\---------------/  |
\\------\\               /--/ 
       |               |
       \\---------------/
"""


    TRACK_PARALLEL_B4B2_S0 = """\
/---\\
|   |
\--\|
   ||
   |\\------\\
   |/----\\ |
   ||    | |
/--/|    | |
|   |    | |
\\---/    \\-/
"""
    TRACK_XXX_S0 = """\
/-----\\   /-----\\   /-----\\   /-----\\ 
|      \\ /       \\ /       \\ /      | 
|       X         X         X       | 
|      / \\       / \\       / \\      | 
\\-----/   \\-----/   \\-----/   \\-----/ 
"""


    TRACK_PARALLEL_SNAIL_S0 = """\
    /---------------------\\               /-\\ /-\\  
   //---------------------\\\\              | | | |  
  //  /-------------------\\\\\\             | / | /  
  ||  |/------------------\\\\\\\\            |/  |/   
  ||  ||                   \\\\\\\\           ||  ||   
  \\\\  ||                   | \\\\\\          ||  ||   
   \\\\-//                   | || \\---------/\\--/|   
/-\\ \\-/                    \\-/|                |   
|  \\--------------------------/                |   
\\----------------------------------------------/   
"""
    
    
    
    
    """ 
    *************************
        INTERNAL SOLUTION
    *************************
    """
    
    import re
    
    DEBUG = False
    GRID_STEP_BY_STEP = False
    crashTestDummies = lambda *args: BlaimHimOrNot(*args).crash()
    
    
    
    class BlaimHimOrNot(object):
        
        MOVES = {'/':  ( [ [( 0,-1,'-'), ( 1,-1,'/'), (1, 0,'|')],     # up-right => down-left
                           [(-1, 0,'|'), (-1, 1,'/'), (0, 1,'-')] ],   # down-left => up-right
                         lambda x,y: x-y <= 0),                        # matching list index fct (retrun 0 for up-right => down-left, 1 otherwise)
                 '\\': ( [ [( 0, 1,'-'), ( 1, 1,'\\'), (1, 0,'|')],    # up-left => down-right
                           [(-1, 0,'|'), (-1,-1,'\\'), (0,-1,'-')] ],  # down-right => up-left
                         lambda x,y: x+y <= 0)}                        # matching list index fct (retrun 0 for up-right => down-left, 1 otherwise)
    
        def __init__(self, track, aTrain, aPos, bTrain, bPos, limit):
            self.limit  = limit
            self.tracks = self.trackBuilder(track)
            self.trains = [TchouTchou(aPos, aTrain, self.tracks), TchouTchou(bPos, bTrain, self.tracks)]         # Build the trains list
            self.aPos, self.bPos = aPos, bPos
            self.trackStr = track
            
            if DEBUG: print("\nLinear track string:\n" + ''.join(str(t) for t in self.tracks))
    
    
        def trackBuilder(self, track):
    
            tracks, toLink, arr = [], {}, track.split('\n')
            dx,dy, x,y = 0,1, 0,next(j for j,c in enumerate(arr[0]) if c != ' ')
            
            x0,y0 = x,y
            while True:
                c   = arr[x][y]
                t   = TrackingDevice(x,y,c)
                pos = (x,y)
            
                if c in '+SX':
                    if pos in toLink: t = toLink[pos]
                    else:             toLink[pos] = t
                tracks.append(t)
    
                if c in "/\\" and not (x == x0 and y == y0):
                    dirToCheck, func = self.MOVES[c]
                    dx,dy = next( (di,dj) for di,dj,targetChar in dirToCheck[func(dx,dy)]
                                   if 0 <= x+di < len(arr) and 0 <= y+dj < len(arr[x+di]) and arr[x+di][y+dj] in targetChar+'XS')
                x,y = x+dx, y+dy
                if x == x0 and y == y0: break
    
            return tracks
    
    
        def crash(self):
            for round in range(self.limit+1):
                
                if GRID_STEP_BY_STEP: print(self.genTrackStr())
            
                if (any(t.checkEatItself() for t in self.trains)
                    or self.trains[0].checkCrashWith(self.trains[1]) ): return self.output(round)
                for t in self.trains: t.move()
            return self.output(-1)
        
        def output(self, exp):
            outTrack  = self.genTrackStr()
            self.trains[0].pos = self.aPos
            self.trains[1].pos = self.bPos
            initTrack = self.genTrackStr()
            return exp, initTrack, outTrack
        
            
        def genTrackStr(self):
            lst = list(map(list, self.trackStr.split('\n')))
            
            for t in self.trains:
                t.updateOccupy()
                for i,tile in enumerate(t.genDisplayPos()):
                    x,y = tile.pos
                    lst[x][y] = (str.lower if i else str.upper)(t.c)
                    
            for tile in self.trains[0].occupy & self.trains[1].occupy:
                x,y = tile.pos
                lst[x][y] = '*'
            
            return '\n'.join(map(''.join, lst))
    
    
    
    class TchouTchou(object):
    
        def __init__(self, pos, s, tracks):
            self.c        = s[0].upper()                  # Representation of the engine of the train
            self.delay    = 0
            self.dir      = (-1) ** s[0].isupper()        # Moving direction
            self.isXpress = self.c == 'X'
            self.len      = len(s)
            self.pos      = pos                           # Integer: index of the engine in the tracks list
            self.tracks   = tracks                        # Reference
            self.updateOccupy()                           # Compute self.occupy = Set of TrackingDevice instances occupied by the train at this point in the executions
    
    
        def updateOccupy(self):          self.occupy = { self.tracks[(self.pos - self.dir*x ) % len(self.tracks)]
                                                         for x in range(self.len) }
        def checkEatItself(self):        return len(self.occupy) != self.len
        def checkCrashWith(self, other): return bool(self.occupy & other.occupy)
        def __repr__(self):              return "TchouTchou({},{},{})".format(self.c, self.pos, self.delay)     # not actual repr... used for debugging
    
        def move(self):
            if self.delay: self.delay -= 1
            else:
                self.pos   = (self.pos + self.dir) % len(self.tracks)
                self.delay = (self.tracks[self.pos].isStation and not self.isXpress) * (self.len-1)
            self.updateOccupy()
        
        def genDisplayPos(self): return ( self.tracks[(self.pos - self.dir*x ) % len(self.tracks)]
                                          for x in range(self.len) )
    
    
    class TrackingDevice(object):
        def __init__(self, x, y, c):
            self.pos       = (x,y)
            self.c         = c
            self.isStation = c == 'S'
            self.linkedTo  = None
    
        def __repr__(self): return "TrackingDevice({1},{2},{0})".format(self.c, *self.pos)
        def __str__(self):  return "({},{})".format(*self.pos) #self.c
        def __hash__(self): return hash(self.pos)        # Behaves like a tuple for hashing
    
    
    
    
    
    
    """  RANDOM TESTS  """
    
    from random import randrange, choice, sample
    
    rand = lambda x,y=0: y + randrange(x)
    
    
    TRAIN_TYPES = "abcdexx"
    TRACKS = [ TRACK_EX,                # more chances to peek the track of the example test...
               TRACK_EX,
               TRACK_EX,
               TRACK_EIGHT_S0,
               TRACK_EIGHT_S2,
               TRACK_CENTRAL_STATION_8,
               TRACK_CENTRAL_STATION_X,
               TRACK_PARALLEL_B4B_S0,
               TRACK_PARALLEL_B4B2_S0,
               TRACK_PARALLEL_SNAIL_S0,
               TRACK_RANDOM_S2,
               TRACK_SLUG_S0,
               TRACK_XXX_S0,]
    
    def makeTrain(typ):
        d = -rand(2)                                   # index to use to choose the direction
        p, size =  rand(100), 2
        if   p<60: size += rand(10)                    # most trains not very long
        elif p<80: size += rand(15)                    # some longer
        else:      size += rand(30)                    # some very long
        
        tchou    = list(typ*size)                      # build the train
        tchou[d] = tchou[d].upper()
        
        return ''.join(tchou)
    
    for r in range(100):
        
        track = choice(TRACKS)
        tLen  = len(re.sub(r'\s+', '', track))
        
        aTrain, bTrain = map(makeTrain, sample(TRAIN_TYPES,2))
        aPos,   bPos   = rand(tLen),  rand(tLen)
        
        MAX_LIMIT = 2000
        exp, initTrack, outTrack = crashTestDummies(track, aTrain, aPos, bTrain, bPos, MAX_LIMIT)
        act = train_crash(track, aTrain, aPos, bTrain, bPos, MAX_LIMIT)
        
        print("""Initial track:
{}

Train 1: {}, starting at {}
Train 2: {}, starting at {}

Final state track:
{}

EXPECTED = {}
ACTUAL = {}""".format(initTrack, aTrain, aPos, bTrain, bPos, outTrack, exp, act))
        
        test.assert_equals(act, exp)
        
        

randomTests()
print("<COMPLETEDIN::>")
