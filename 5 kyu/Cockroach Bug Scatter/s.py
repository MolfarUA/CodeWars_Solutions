59aac7a9485a4dd82e00003e



def cockroaches(room):
    WALLS = {'L':''.join(r[0] for r in room), 'D':room[-1], 'R':''.join(r[-1] for r in room), 'U':room[0]}

    def hole(d, i=0):
        wall = WALLS[d][i:] if d in 'LD' else WALLS[d][:i+1][::-1] if i else WALLS[d][::-1]
        for c in wall:
            if c.isdigit(): return int(c)

        return hole({'L':'D', 'D':'R', 'R':'U', 'U':'L'}[d])  # try next wall
            
    holes = [hole(d, r if d in 'LR' else c) for r,row in enumerate(room) for c,d in enumerate(row) if d in 'LDRU']
        
    return [holes.count(i) for i in range(10)]
________________________________
def cockroaches(room):
    output = [0] * 10
    upper  = room[0][::-1]
    lower  = room[-1]
    left   = ''.join(row[0] for row in room)
    right  = ''.join(row[-1] for row in reversed(room))
    for i, row in enumerate(room):
        for j, x in enumerate(row):
            match x:
                case 'U': path = upper[-j - 1::] + left + lower + right + upper[:-j - 1]
                case 'L': path = left[i:] + lower + right + upper + left[:i]
                case 'D': path = lower[j:] + right + upper + left + lower[:j]
                case 'R': path = right[-i - 1::] + upper + left + lower + right[:-i - 1]
                case _:   continue
            output[next(int(x) for x in path if x.isdigit())] += 1
    return output
________________________________
def cockroaches(room):
    holes = {(i, j): int(v) for i, r in enumerate(room) for j, v in enumerate(r) if v.isdigit()}
    walls = [(i, len(room[0])-1) for i in range(len(room))][::-1] + \
            [(0, i) for i in range(len(room[0]))][::-1] + \
            [(i, 0) for i in range(len(room))] + \
            [(len(room)-1, i) for i in range(len(room[0]))]
    walls *= 2
    rats = [(0, j) if v=='U' else (i, 0) if v=='L' else (len(room)-1, j) if v=='D' else (i, len(room[0])-1) \
            for i, r in enumerate(room) for j, v in enumerate(r) if v in 'UDLR']
    res = [0] * 10
    for rat in rats:
        i = walls.index(rat)
        while True:
            if walls[i] in holes:
                res[holes[walls[i]]] += 1
                break
            i += 1
    return res
________________________________
def cockroaches(room):
    letters = ['L','D','R','U']
    holes = ['0','1','2','3','4','5','6','7','8','9']
    solution = [0]*10
    nroom = room[0]
    for i in range(1,len(room)-1):
        nroom += room[i][len(room[i])-1] 
    for i in reversed(range(len(room[0]))):
        nroom += room[len(room)-1][i]
    for i in reversed(range(1,len(room)-1)):
        nroom += room[i][0] 
    nroom += nroom
    nroom = nroom[::-1]
    for i in range(len(room)):
        for j in range(len(room[i])):
            pos = 0
            if room[i][j] in letters:
                if room[i][j] == 'L':
                    pos = i-1
                elif room[i][j] == 'D':
                    pos = len(room)+j-2
                elif room[i][j] == 'R':
                    pos = 2*len(room)+len(room[i])-i-4
                elif room[i][j] == 'U':
                    pos = 2*len(room)+2*len(room[i])-j-5
                for k in range(pos,len(nroom)):
                    if nroom[k] in holes:
                        solution[int(nroom[k])] += 1
                        break
    return(solution)
________________________________
class Roach:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Roach(x={self.x}, y={self.y})"

    def step(self, max_x, max_y):
        if self.y == 0 and 0 < self.x <= max_x:
            self.x -= 1
        elif 0 <= self.y < max_y and self.x == 0:
            self.y += 1
        elif self.y == max_y and 0 <= self.x < max_x:
            self.x += 1
        elif 0 < self.y <= max_y and self.x == max_x:
            self.y -= 1


class Hole:
    def __init__(self, x: int, y: int, name: str, roaches: int = 0):
        self.x = x
        self.y = y
        self.name = name
        self.roaches = roaches

    def __repr__(self):
        return f"Hole(x={self.x}, y={self.y}, name={self.name}, roaches={self.roaches})"


def get_room_size(room):
    max_y = len(room) - 1
    max_x = len(room[0]) - 1
    return max_x, max_y


def put_roaches_in_holes(holes: dict, roaches, max_x, max_y):
    res = [0] * 10
    for roach in roaches:
        while not (roach.x, roach.y) in holes:
            roach.step(max_x, max_y)
        res[int(holes[(roach.x, roach.y)])] += 1
    return res


def cockroaches(room):
    holes, roaches = {}, []
    max_x, max_y = get_room_size(room)
    for y, line in enumerate(room):
        for x, item in enumerate(line):
            if item.isdigit():
                holes[(x, y)] = item
            elif item in ["U", "D", "R", "L"]:
                roach_y = 0 if item == "U" else max_y if item == "D" else y
                roach_x = 0 if item == "L" else max_x if item == "R" else x
                roaches.append(Roach(roach_x, roach_y))
    return put_roaches_in_holes(holes, roaches, max_x, max_y)
________________________________
from itertools import chain, cycle
DIRECTIONS = (0, -1), (1, 0), (0, 1), (-1, 0)
def cockroaches(room):
    counts = [0] * 10
    height = len(room)
    width = len(room[0])
    def search(index, row, column):
        directions = cycle(chain(DIRECTIONS[index:], DIRECTIONS[:index]))
        for row_offset, column_offset in directions:
            while 0 <= row < height and 0 <= column < width:
                cell = room[row][column]
                if cell.isnumeric(): counts[int(cell)] += 1 ; return
                row += row_offset ; column += column_offset
            row -= row_offset ; column -= column_offset
    for row, cells in enumerate(room):
        for column, cell in enumerate(cells):
            if cell == 'U': search(0, 0, column)
            if cell == 'L': search(1, row, 0)
            if cell == 'D': search(2, height - 1, column)
            if cell == 'R': search(3, row, width - 1)
    return counts
________________________________
def cockroaches(room):
    left,left_d = {'R':(0, 1),'U':(-1, 0),'L':(0, -1),'D':(1, 0)}, {'R':'U','U':'L','L':'D','D':'R'}
    find,re = [[i, k, l] for i,j in enumerate(room) for k,l in enumerate(j) if l.isalpha()],[]
    for i in find:
        r, c, d = i
        k, l = [r,[0,len(room)-1][d=='D']][d in "UD"], [c,[0,len(room[0])-1][d=='R']][d in "LR"]
        d = left_d[d] ; o, p = left[d]
        while not room[k][l].isdigit():
            if room[k][l] == '+' : d = left_d[d] ; o, p = left[d]
            k += o ; l += p
        re.append(room[k][l])
    return [re.count(str(i)) for i in range(10)]
________________________________
from itertools import chain
from collections import defaultdict
from re import findall

def cockroaches(room):
    holes_up, holes_down = {room[0].index(x): 0 for x in room[0][1:] if x != "-" and x != "+"}, {room[-1].index(x): 0 for x in room[-1][:-1] if x != "-" and x != "+"}
    holes_right, holes_left = {room.index(x): 0 for x in room[1:] if x[-1] != "|" and x[-1] != "+"}, {room.index(x): 0 for x in room[:-1] if x[0] != "|" and x[0] != "+"}
    up_ind = [int(x) for x in findall(r"\d", room[0][1:])][::-1]
    down_ind = [int(x) for x in findall(r"\d", room[-1][:-1])][::-1]
    right_ind = [int(x[-1]) for x in room[1:] if x[-1] != "|" and x[-1] != "+"][::-1]
    left_ind = [int(x[0]) for x in room[:-1] if x[0] != "|" and x[0] != "+"][::-1]
    pos = defaultdict(list)
    flat = list(chain.from_iterable(room))
    for i in range(len(flat)):
        if flat[i] in ["L", "D", "U", "R"]:
            pos[flat[i]].append(divmod(i, len(room[0])))

    def fill_up(cc):
        if not holes_up or cc[1] < min(holes_up):
            fill_left((min(holes_left, default=0), cc[1]))
        else: holes_up[max(x for x in holes_up if x <= cc[1])] += 1

    def fill_right(cc):
        if not holes_right or cc[0] < min(holes_right):
            fill_up((cc[0], max(holes_up, default=0)))
        else: holes_right[max(x for x in holes_right if x <= cc[0])] += 1

    def fill_down(cc):
        if not holes_down or cc[1] > max(holes_down):
            fill_right((max(holes_right, default=0), cc[1]))
        else: holes_down[min(x for x in holes_down if x >= cc[1])] += 1

    def fill_left(cc):
        if not holes_left or cc[0] > max(holes_left):
            fill_down((cc[0], min(holes_down, default=0)))
        else: holes_left[min(x for x in holes_left if x >= cc[0])] += 1
    for cc in pos["U"]:
        fill_up(cc)
    for cc in pos["D"]:
        fill_down(cc)
    for cc in pos["R"]:
        fill_right(cc)
    for cc in pos["L"]:
        fill_left(cc)
    res = [0] * 10
    for u in holes_up.keys():
        res[up_ind.pop()] = holes_up[u]
    for r in holes_right.keys():
        res[right_ind.pop()] = holes_right[r]
    for d in holes_down.keys():
        res[down_ind.pop()] = holes_down[d]
    for l in holes_left.keys():
        res[left_ind.pop()] = holes_left[l]
    return res
________________________________
import re

def cockroaches(room):
    for _ in range(8):                                                                         # 8 rotations to handle properly the first top left corner of the room or rooms with holes on only one wall
        room = [''.join(l) for l in zip(*room)][::-1]                                          #     Rotated counter-clockwise (done first, to avoid any mutation of the input)
        room[0] = re.sub(r'\d[+|-]*', lambda m: m.group()[0] * len(m.group()), room[0])        #     Fill the "upper" wall with the number on the left of a wall character
        
    argh    = [0] * 10                                                                         # Prepare output
    DIR_DCT = {'U':'0,y', 'L':'x,0', 'D':'len(room)-1,y', 'R':'x,len(room[0])-1'}              # Commands to retrieve the right hole depending on the direction of the bug
    
    for x in range(1, len(room)-1):
        for y in range(1, len(room[0])-1):
            if room[x][y] != ' ':
                i, j = eval( DIR_DCT[room[x][y]] )
                argh[ int(room[i][j]) ] += 1
    return argh
________________________________
def cockroaches(room):
    room = [list(e) for e in room]
    h,w,y0,x0,p,r = len(room),len(room[0]),None,None,None,[0]*10
    def walk():
        y,x,dy,dx = 0,0,0,1
        while True:
            if (x+1==w and dx>0) or (x==0 and dx<0) or (y+1==h and dy>0) or (y==0 and dy<0):
                dy,dx = dx,-dy
            yield y,x
            y,x = y+dy,x+dx
    for y,x in walk():
        if room[y][x].isdigit():
            p = room[y][x]
            if y0 is None:
                y0,x0 = y,x
            elif y0==y and x0==x:
                break
        elif p is not None:
            room[y][x] = p
    for y in range(h):
        for x in range(w):
            p = room[y][x]
            if p=='U': 
                r[int(room[0][x])] += 1
            elif p=='D': 
                r[int(room[h-1][x])] += 1
            elif p=='R': 
                r[int(room[y][w-1])] += 1
            elif p=='L': 
                r[int(room[y][0])] += 1
    return r
________________________________
DIRL = "ULDR"
DIRS = ((-1, 0), (0, -1), (1, 0), (0, 1))

def cockroaches(room):
    holes = [0] * 10
    def run(x, y, d):
        turn = "-|"
        dx, dy = DIRS[d]
        while not room[x][y].isdigit():
            if room[x][y] in turn:
                d = (d + 1) % 4
                dx, dy = DIRS[d]
                turn = "+"
            x += dx
            y += dy
        return int(room[x][y])

    for x, r in enumerate(room):
        for y, c in enumerate(r):
            if (d := DIRL.find(c)) >= 0:
                holes[run(x, y, d)] += 1
    return holes
________________________________
def cockroaches(room):
    a=[0]*10
    Cockroach={'U':[0],'D':[0],'R':[0],'L':[0]}
    krai=0
    
    for i in range(len(room)):
        for j in range(len(room[0])):
            if room[i][j]=='U': 
                Cockroach['U'][0]+=1
                Cockroach['U'].append([i, j])
            elif room[i][j]=='D': 
                Cockroach['D'][0]+=1
                Cockroach['D'].append([i, j])
            elif room[i][j]=='R': 
                Cockroach['R'][0]+=1
                Cockroach['R'].append([i, j])
            elif room[i][j]=='L': 
                Cockroach['L'][0]+=1
                Cockroach['L'].append([i, j])
                
    length, width=len(room[0]), len(room)
    
    for i in range(Cockroach['U'][0]):
        I, J=Cockroach['U'][i+1][0], Cockroach['U'][i+1][1]
        if room[0][J]!='-':a[int(room[0][J])]+=1
        else:
            k=False
            for cock in range(J-1, -1, -1):
                if room[0][cock]!='-' and room[0][cock]!='+': 
                    a[int(room[0][cock])]+=1
                    k=True
                    break
            if not(k):
                for cock in range(width):
                    if room[cock][0]!='|' and room[cock][0]!='+':
                        a[int(room[cock][0])]+=1
                        k=True
                        break
            if not(k):
                for cock in range(length):
                    if room[width-1][cock]!='-' and room[width-1][cock]!='+':
                        a[int(room[width-1][cock])]+=1
                        k=True
                        break
            if not(k):
                for cock in range(width-1, -1, -1):
                    if room[cock][length-1]!='|' and room[cock][length-1]!='+':
                        a[int(room[cock][length-1])]+=1
                        k=True
                        break
            if not(k):
                for cock in range(length-1, J, -1):
                    if room[0][cock]!='-' and room[0][cock]!='+':
                        a[int(room[0][cock])]+=1
                        k=True
                        break
                        
    for i in range(Cockroach['D'][0]):
        I, J=Cockroach['D'][i+1][0], Cockroach['D'][i+1][1]
        if room[width-1][J]!='-':a[int(room[width-1][J])]+=1
        else:
            k=False
            for cock in range(J+1, length):
                if room[width-1][cock]!='-' and room[width-1][cock]!='+':
                    a[int(room[width-1][cock])]+=1
                    k=True
                    break
            if not(k):
                for cock in range(width-1, -1, -1):
                    if room[cock][length-1]!='|' and room[cock][length-1]!='+':
                        a[int(room[cock][length-1])]+=1
                        k=True
                        break
            if not(k):
                for cock in range(length-1, -1, -1): 
                    if room[0][cock]!='-' and room[0][cock]!='+':
                        a[int(room[0][cock])]+=1
                        k=True
                        break
            if not(k):
                for cock in range(width):
                    if room[cock][0]!='|' and room[cock][0]!='+':
                        a[int(room[cock][0])]+=1
                        k=True
                        break 
            if not(k):
                for cock in range(J):
                    if room[width-1][cock]!='-' and room[width-1][cock]!='+':
                        a[int(room[width-1][cock])]+=1
                        k=True
                        break
                        
    for i in range(Cockroach['R'][0]):
        I, J=Cockroach['R'][i+1][0], Cockroach['R'][i+1][1]
        if room[I][length-1]!='|':a[int(room[I][length-1])]+=1 
        else:
            k=False
            for cock in range(I-1, -1, -1):
                if room[cock][length-1]!='|' and room[cock][length-1]!='+':
                    a[int(room[cock][length-1])]+=1
                    k=True
                    break
            if not(k):
                for cock in range(length-1, -1, -1):
                    if room[0][cock]!='-' and room[0][cock]!='+':
                        a[int(room[0][cock])]+=1
                        k=True
                        break
            if not(k):
                for cock in range(width-1):
                    if room[cock][0]!='|' and room[cock][0]!='+':
                        a[int(room[cock][0])]+=1
                        k=True
                        break
            if not(k):
                for cock in range(length-1): 
                    if room[width-1][cock]!='-' and room[width-1][cock]!='+':
                        a[int(room[width-1][cock])]+=1
                        k=True
                        break  
            if not(k):
                for cock in range(width-1, I, -1):
                    if room[length-1][cock]!='|' and room[length-1][cock]!='+':
                        a[int(room[length-1][cock])]+=1
                        k=True
                        break
                        
    for i in range(Cockroach['L'][0]):
        I, J=Cockroach['L'][i+1][0], Cockroach['L'][i+1][1]
        if room[I][0]!='|':a[int(room[I][0])]+=1
        else:
            k=False
            for cock in range(I+1, width):
                if room[cock][0]!='|' and room[cock][0]!='+':
                    a[int(room[cock][0])]+=1
                    k=True
                    break
            if not(k):
                for cock in range(length):
                    if room[width-1][cock]!='-' and room[width-1][cock]!='+':
                        a[int(room[width-1][cock])]+=1
                        k=True
                        break
            if not(k):
                for cock in range(width-1, -1, -1):
                    if room[cock][length-1]!='|' and room[cock][length-1]!='+':
                        a[int(room[cock][length-1])]+=1
                        k=True
                        break
            if not(k):
                for cock in range(length-1, -1, -1):
                    if room[0][cock]!='-' and room[0][cock]!='+':
                        a[int(room[0][cock])]+=1
                        k=True
                        break  
            if not(k):
                for cock in range(I):
                    if room[cock][0]!='-' and room[cock][0]!='+':
                        a[int(room[cock][0])]+=1
                        k=True
                        break
                           
    print(a)              
    return a
________________________________
from dataclasses import dataclass
from typing import Callable, Generator


@dataclass(frozen=True)
class Point:
    y: int
    x: int


class Room(list[str]):
    def __init__(self, lines: list[str]) -> None:
        super().__init__(lines)
        self.height = len(self)
        self.width = len(self[0])
        self.holes = dict[Point, int]()  # {hole_pos: hole_num}
        self._find_holes()

    def _find_holes(self) -> None:
        for y in range(0, self.height):
            if self[y][0].isdigit():
                self._save_hole(y, 0)
            if self[y][-1].isdigit():
                self._save_hole(y, self.width-1)
        for x in range(1, self.width-1):
            if self[0][x].isdigit():
                self._save_hole(0, x)
            if self[-1][x].isdigit():
                self._save_hole(self.height-1, x)

    def _save_hole(self, y: int, x: int) -> None:
        hole_pos = Point(y, x)
        hole_num = int(self[y][x])
        self.holes[hole_pos] = hole_num


HOLE_SORT_KEYS: dict[str, Callable[[Point], int]] = {
    "U": (lambda hole: -hole.x),
    "D": (lambda hole: hole.x),
    "L": (lambda hole: hole.y),
    "R": (lambda hole: -hole.y)
}
"""For each wall, defines a key function
that sorts holes in counter-clockwise order (as visited by a cockroach).
"""


def holes_on_the_way(cockroach: Point, room: Room
                     ) -> Generator[Point, None, None]:
    """Yields holes in the same order as the cockroach encounters them."""

    def is_on_the_wall(hole: Point, wall: str) -> bool:
        match wall:
            case "U": return hole.y == 0
            case "D": return hole.y == room.height-1
            case "L": return hole.x == 0
            case "R": return hole.x == room.width-1
            case _:   assert False, "Invalid wall"

    wall = room[cockroach.y][cockroach.x]
    sort_key = HOLE_SORT_KEYS[wall]
    holes_on_that_wall = [h for h in room.holes if is_on_the_wall(h, wall)
                          # For this first wall, only the left half is ok
                          and sort_key(h) >= sort_key(cockroach)]
    yield from sorted(holes_on_that_wall, key=HOLE_SORT_KEYS[wall])
    next_wall_idx = "ULDR".index(wall) + 1
    for wall in "ULDRULDR"[next_wall_idx:next_wall_idx+4]:
        holes_on_that_wall = [h for h in room.holes if is_on_the_wall(h, wall)]
        yield from sorted(holes_on_that_wall, key=HOLE_SORT_KEYS[wall])


def cockroaches(room_: list[str]) -> list[int]:
    room = Room(room_)
    hole_counts = [0] * 10
    for y in range(1, room.height-1):
        for x in range(1, room.width-1):
            if room[y][x].isalpha():
                cockroach = Point(y, x)
                hole_pos = next(holes_on_the_way(cockroach, room))
                hole_num = room.holes[hole_pos]
                hole_counts[hole_num] += 1
    return hole_counts
