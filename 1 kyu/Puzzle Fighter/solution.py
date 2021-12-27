class Game():
    h, w = 15, 6
    colors = 'RBGY'
    start = [(3, 1), (3, 2)]
    moves = {'L': [(-1, 0), (-1, 0)], 'R': [(1, 0), (1, 0)]}
    rotate = {'A': {(1, 0): (-1, -1), (0, -1): (-1, 1), (-1, 0): (1, 1), (0, 1): (1, -1)},
              'B': {(1, 0): (-1, 1), (0, -1): (1, 1), (-1, 0): (1, -1), (0, 1): (-1, -1)}}
    outborder_rotate = {'A': {(0, -1): [(1, 0), (0, 1)], (0, 1): [(-1, 0), (0, -1)]},
                        'B': {(0, -1): [(-1, 0), (0, 1)], (0, 1): [(1, 0), (0, -1)]}}
    neigh = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    
    def __init__(self, ar):
        self.points = [(x, y) for y in range(self.h) for x in range(self.w)]
        self.b = {point: ' ' for point in self.points}
        self.instructions = ar
        self.power = []
        self.power_set = []
        self.prev = None
    
    def solve(self):
        for instruction in self.instructions:
            detail = instruction[0]
            moves = instruction[1].strip()

            self.detail = self.start.copy()
            self.type = list(detail)
            for i in range(2):
                self.b[self.detail[i]] = self.type[i]

            for move in moves:
                self.move_detail(move)

            continu = self.update()
            if not continu:
                return self.final(self.prev)
                
            self.prev = {point: self.b[point] for point in self.points}

        return self.final(self.b)
    
    def move_detail(self, move):
        if move in 'LR':
            to_move = self.moves[move]
        else:
            x1, y1 = self.detail[0]
            x2, y2 = self.detail[1]
            dif = (x2 - x1, y2 - y1)
            to_move = [(0, 0), (self.rotate[move][dif])]
        
        both = True
        for i, part in enumerate(to_move):
            x, y = self.detail[i]
            new = (x + part[0], y + part[1])
            if new not in self.points:
                both = False
        
        if not both and move in 'AB':
            x1, y1 = self.detail[0]
            x2, y2 = self.detail[1]
            dif = (x2 - x1, y2 - y1)
            to_move = self.outborder_rotate[move][dif]
            both = True
            
        if both:    
            for i, part in enumerate(to_move):
                x, y = self.detail[i]
                new = (x + part[0], y + part[1])
                if new in self.points:
                    self.detail[i] = new
                    self.b[(x, y)] = ' '
                    self.b[new] = self.type[i]
    
            if move == 'R' and self.detail[1][0] > self.detail[0][0]:
                self.b[self.detail[0]] = self.type[0]
            elif move == 'L' and self.detail[0][0] > self.detail[1][0]:
                self.b[self.detail[0]] = self.type[0]

    
    def update(self):
        move = 0
        while True:
            self.move_down()
            if move == 0:
                for x in range(self.w):
                    if self.b[(x, 2)] != ' ':
                        return False
                move += 1

            self.form_power_gems()

            rainbow_crash = True
            gem_crash = True
            
            if not self.crash_rainbow_gem():
                rainbow_crash = False
            if not self.crash_gems():
                gem_crash = False
                
            if not rainbow_crash and not gem_crash:
                break

        return True
    
    def move_down(self):
        for point in self.points[::-1]:
            x, y = point
            if self.b[point] != ' ':
                if point not in [gem_point for gem in self.power for gem_point in gem]:
                    cur = point
                    while True:
                        down = (cur[0], cur[1] + 1)
                        if down in self.points and self.b[down] == ' ':
                            self.b[down], self.b[cur] = self.b[cur], ' '
                        else: break
                        cur = down
                else:
                    for i in range(len(self.power)):
                        if point in self.power[i]:
                            c = i
                            break
                    while True:
                        bottomY = [y for x, y in self.power[c]][-1]
                        move_gem = True
                        for i in range(len(self.power[c])):
                            gemX, gemY = self.power[c][i]
                            if gemY == bottomY:
                                down = (gemX, gemY + 1)
                                if down not in self.points or self.b[down] != ' ':
                                    move_gem = False
                                    break
        
                        if not move_gem:
                            break
                            
                        current = len(self.power[c]) - 1
                        for gem_point in self.power[c][::-1]:
                            gemX, gemY = gem_point
                            down = (gemX, gemY + 1)
                            self.b[down], self.b[gem_point] = self.b[gem_point], ' '
                            self.power[c][current] = down
                            current -= 1

    
    def check_sides(self, point):
        self.checked.append(point)
        group = [point]
        x, y = point
        for x2, y2 in self.neigh:
            xN, yN = x + x2, y + y2
            neigh_point = (xN, yN)
            if neigh_point in self.points and neigh_point not in self.checked:
                if self.b[point].upper() == self.b[neigh_point].upper():
                    next = self.check_sides(neigh_point)
                    group.extend(next)
        return group
    
    def isPowerGem(self, group):
        def find_possible_gems(h, w, new_group, m):
            possible = []
            for y in range(h - 1):
                for x in range(w - 1):
                    if m[y][x] != 1:
                        continue
                    for pH in range(2, h - y + 1):
                        for pW in range(2, w - x + 1):
                            gem = [new_group[(x + x1, y + y1)] for y1 in range(pH) for x1 in range(pW) if m[y + y1][x + x1] == 1]
                            if len(gem) == pH * pW:
                                ispossible = True
                                gem_set = set(gem)
                                for i in range(len(self.power)):
                                    power_gem_set = self.power_set[i]
                                    if power_gem_set&gem_set and not power_gem_set <= gem_set:
                                        ispossible = False
                                        break
                                if ispossible:
                                    possible.append(gem)
            return possible
            
        def check_formation_priority(copy):
            for i in range(len(copy)):
                for u in range(i + 1, len(copy)):
                    if set(copy[i])&set(copy[u]):
                        y1 = min([y for x, y in copy[i]])
                        y2 = min([y for x, y in copy[u]])
                        if y1 > y2:
                            copy.pop(i)
                        elif y2 > y1:
                            copy.pop(u)
                        else:
                            x1 = [x for x, y in copy[i] if y == y1]
                            x2 = [x for x, y in copy[u] if y == y2]
                            if x1 > x2:
                                copy.pop(u)
                            else:
                                copy.pop(i)
                        return copy
            return copy
        
        def check_expand_priority(copy):
            for i in range(len(copy)):
                for u in range(i + 1, len(copy)):
                    if set(copy[i])&set(copy[u]):
                        y1 = min([y for x, y in copy[i]])
                        y2 = min([y for x, y in copy[u]])
                        x1 = [x for x, y in copy[i] if y == y1]
                        x2 = [x for x, y in copy[u] if y == y2]
                        if x1 > x2:
                            copy.pop(u)
                        elif y2 > y1:
                            copy.pop(i)
                        return copy
            return copy
        
        def delete(copy):
            for i in range(len(copy)):
                for u in range(i + 1, len(copy)):
                    iSet = set(copy[i])
                    uSet = set(copy[u])
                    if iSet&uSet:
                        if iSet <= uSet:
                            copy.pop(i)
                        else:
                            copy.pop(u)
                        return copy
            return copy
            
        allX = sorted([x for x, y in group])
        allY = sorted([y for x, y in group])
        minX, maxX = allX[0], allX[-1]
        minY, maxY = allY[0], allY[-1]

        h = maxY - minY + 1
        w = maxX - minX + 1
        new_group = {(x - minX, y - minY): (x, y) for x, y in group}
        m = [[0 for x in range(w)] for y in range(h)]
        for x, y in new_group:
            m[y][x] = 1

        possible = find_possible_gems(h, w, new_group, m)               
        possible = sorted(possible, key = len)[::-1]

        new = []
        for one in possible:
            isnew = True
            gem_set = set(one)
            for i in range(len(self.power)):
                if self.power_set[i] <= gem_set:
                    isnew = False
                    break
            if isnew:
                notin = True
                for other in possible:
                    if one != other and gem_set <= set(other):
                        notin = False
                if notin:
                    new.append(one)

        while True:
            new_copy = check_formation_priority(new)
            if new_copy == new:
                break
            new = new_copy

        possible_expand = possible
        
        for i in range(len(possible_expand) - 1, -1, -1):
            gemin = False
            possible_expand_set = set(possible_expand[i])
            for u in range(len(self.power)):
                if self.power_set[u] <= possible_expand_set:
                    gemin = True
                    cross = False
                    for one in new:
                        one_set = set(one)
                        if possible_expand_set&one_set and not one_set <= possible_expand_set:
                            cross = True
                    if cross:
                        possible_expand.pop(i)
                        break
            if not gemin:
                possible_expand.pop(i)

        while True:
            possible_expand_copy = delete(possible_expand)
            if possible_expand_copy == possible_expand:
                break
            possible_expand = possible_expand_copy
        
        while True:
            possible_expand_copy = check_expand_priority(possible_expand)
            if possible_expand_copy == possible_expand:
                break
            possible_expand = possible_expand_copy

        result = possible_expand
        for one in new:
            alone = True
            one_set = set(one)
            for gem in result:
                if set(one) <= set(gem):
                    alone = False
            if alone:
                result.append(one)
                
        self.new_power.extend(result)
        
    def form_power_gems(self):
        self.new_power = []
        self.checked = []
        self.power_set = [set(one) for one in self.power]
        for point in self.points:
            if point not in self.checked and self.b[point] != ' ':
                group = self.check_sides(point)
                if len(group) >= 4:
                    self.isPowerGem(group)
        self.power = self.new_power.copy()
    
    def crash_rainbow_gem(self):
        crashed = False
        for point in self.points:
            if self.b[point] == '0':
                crashed = True
                self.b[point] = ' '
                down = (point[0], point[1] + 1)
                if down in self.points and self.b[down] not in ' 0':
                    color = self.b[down].upper()
                    for point1 in self.points:
                        if self.b[point1].upper() == color:
                            for i in range(len(self.power)):
                                if point1 in self.power[i]:
                                    self.power.pop(i)
                                    break
                            self.b[point1] = ' '
        return crashed
    
    def crash_gems(self):
        crashed = False
        self.checked = []
        for point in self.points:
            if self.b[point] in self.colors.lower():
                group = self.check_sides(point)
                if len(group) > 1:
                    for part in group:
                        for i in range(len(self.power)):
                            if part in self.power[i]:
                                self.power.pop(i)
                                break
                        self.b[part] = ' '
                    crashed = True
        return crashed
    
    def final(self, m):
        lines = []
        for y in range(3, self.h):
            line = ''
            for x in range(self.w):
                line += m[(x, y)]
            lines.append(line)
        result = '\n'.join(lines)
        return result
            
    
def puzzle_fighter(ar):
    return Game(ar).solve()
####################################################
from collections import defaultdict
from itertools import chain, count, cycle
from operator import itemgetter
from heapq import *


def puzzle_fighter(arrMoves):
    
    def getStartPoses(moves, c1, c2):
        x,y,iR = start
        for m in moves:
            y += m in 'RL' and (-1)**(m=='L')
            iR = (iR + (m in 'AB' and (-1)**(m=='A'))) % 4
            dy = ROTATIONS[iR][1]
            if y>=lY or y+dy>=lY: y = min(lY-1,lY-1-dy)                 # move it back into the board (out on right side)
            elif y<0 or y+dy<0:   y = max(0,-dy)                        # move it back into the board (out on left side)
        dx,dy = ROTATIONS[iR] 
        x += dx<0                                                       # move it in the board (too high)
        return (x,y,c1), (x+dx,y+dy,c2)
    
    
    def moveGem(x0,y0, x,y):
        c,_,_,h,w,s = g = board[x0][y0]
        g[X],g[Y] = x,y
        dctSet = gemsByColors[c]
        dctSet.discard((x0,y0))
        dctSet.add((x,y))
        for dx in reversed(range(h)):
            for dy in reversed(range(w)):
                board[x0+dx][y0+dy] = None                              # erase THEN restore/move
                board[x+dx][y+dy]   = g
    
    
    def couldFallFromAbove(x,y,w):                                      # Extract only the position of the root of the gems above (x,y)
        if not x: return set()
        else:     x -= 1
        return { tuple(board[x][yy][X:Y+1]) for yy in range(y,y+w) if board[x][yy] }
    
    
    def drop(posToDrop):
        movedGems = set()                                               # Archive all the moved gems: only those ones are candidates to create power gems (and explosions, but taht's not needed here)
        toDrop    = [(-x,y) for x,y in posToDrop]                       # "max heap", to drop all gems from bottom to top of the board
        heapify(toDrop)
        while toDrop:
            x,y = heappop(toDrop)
            x  *= -1
            if board[x][y] is None: continue
            c,x0,y0,h,w,_ = board[x][y]
            moved = 0
            while x+h<lX and not any(board[x+h][yy] for yy in range(y,y+w)):
                x += 1; moved = 1
            if moved or x==x0:
                moveGem(x0,y0, x,y)
                movedGems.add((x,y))
                for x,y in couldFallFromAbove(x0,y0,w):
                    heappush(toDrop, (-x,y))
        return movedGems
            
    
    def explode(movedGems):
        colorsToExplode = {'0'} | { f(board[x+1][y][C]) for x,y in gemsByColors['0'] if x<lX-1
                                                        for f in (str.lower,str.upper) }
        posToExplode    = { pos for c in colorsToExplode for pos in gemsByColors[c] }                # from rainbow gems
        posToExplode   |= set(chain.from_iterable(
                                  flood(x,y,c) for c in 'rgby' for x,y in gemsByColors[c] ))         # from crash gems
        
        toDropNext = set()
        for x,y in posToExplode:
            c,_,_,h,w,_   = board[x][y]
            toDropNext |= couldFallFromAbove(x,y,w)
            gemsByColors[c].discard( (x,y) )
            for xx in range(x,x+h):
                for yy in range(y,y+w): board[xx][yy] = None
        
        movedGems  -= posToExplode                                      # remove exploded gems to "save" some computations later
        toDropNext -= posToExplode
        return movedGems, toDropNext
    
    
    def flood(x,y, what):                                               # flood the area whatever the sizes of the encountered gems (single/powa)
        what += what.swapcase()                                         # to flood gems and related crash gems indifferently
        bag, seen = {(x,y)}, {(x,y)}
        while bag:
            bag = { (a,b) for a,b in ((x+dx,y+dy) for x,y in bag for dx,dy in ROTATIONS)
                          if 0<=a<lX and 0<=b<lY and board[a][b] is not None
                             and board[a][b][C] in what and (a,b) not in seen
                             and (seen.add((a,b)) or 1) }                        # update seen on the fly
        
        seen = { tuple(board[a][b][X:Y+1]) for a,b in seen }
        return seen if len(seen)>1 else set()                           # Don't return crash gems only (they do not explode / this doesn't affect the behavior of power gems creations if not returned!)
    
    def makePowa(movedGems, toDropNext):
        gemAreasByCols = defaultdict(set)
        for x,y in movedGems:
            c,_,_,h,w,_ = board[x][y]
            gemAreasByCols[c] |= flood(x,y,c)
        
        q = list(gemAreasByCols.items())
        while q:
            c,areas = q.pop()
            freshPows,removedPows = iGotThePowa(areas, toDropNext)
            gemsByColors[c]      -= removedPows
            if freshPows: q.insert(0,(c,freshPows))                      # brand new powaGems could merge later with larger ones
            
        return toDropNext                                                # WARNING: toDropNext is mutated from "iGotThePowa()"
    
    
    def iGotThePowa(areas, toDropNext):                                  # ... XD   https://www.youtube.com/watch?v=_BRv9wGf5pk#t=45
        ones    = [ board[x][y] for x,y in areas if board[x][y][S]==1 ]
        powaG   = [ board[x][y] for x,y in areas if board[x][y][S]!=1 ]
        fresh, removed = set(), set()
        
        for i,grp in enumerate((ones,powaG)):
            grp.sort()
            isSingle = not i
            for g in grp:
                c,x,y,h,w,s = g
                if g is not board[x][y] or x==lX-1 or y==lY-1: continue
                
                expanded = expand(DIRS_SINGLE if isSingle else DIRS_POWA, isSingle, c,x,y,h,w,s)
                
                if expanded:
                    x,y,h,w,s = g[1:] = expanded
                    if isSingle: powaG.append(g)
                    fresh.add((x,y))
                    toRemove  = { (xx,yy) for xx in range(x,x+h) for yy in range(y,y+w)
                                          if board[xx].__setitem__(yy,g) or 1 }            # (update the board at the same time... x) )
                    toRemove.remove((x,y))
                    removed |= toRemove
                    if toDropNext & toRemove:                           # previous candidates to drop, when merged in a power gem,...
                        toDropNext.add((x,y))                           # ...means the power gem could need to drop too
                        toDropNext -= toRemove
                        
        return fresh,removed
        
    
    def expand(dirs, isSingle, c,x,y,h,w,s):
        data = start = x,y,h,w
        
        if isSingle:                                                                           # enforce/check the minimum 2x2 power gem for singles
            triad = [board[x+dx][y+dy] for dx,dy in ((0,1),(1,0),(1,1))]                       # (no need to check x and y on border: already excluded before)
            if None in triad or not all(g[C]==c and g[S]==1 for g in triad): return None
            data = x,y,2,2
    
        for dx,dy in dirs:
            x,y,h,w = data                                                                     # restore data of the last valid expansion (see goodAlignment)
            for _ in count(0):
                rngX    = tuple(range(x,x+h)) if not dx else [x+dx + (h-1 if dx==1 else 0)]
                rngY    = tuple(range(y,y+w)) if not dy else [y+dy + (w-1 if dy==1 else 0)]
                
                collect = collectNextLine(rngX,rngY, dx,dy,isSingle, c,x,y,h,w,s)
                if not collect: break
                
                if dx: x,h = (x, h+1) if dx==1 else (x-1,h+1)                                  # update x,y,h,w according to the current expansion
                if dy: y,w = (y, w+1) if dy==1 else (y-1,w+1)
                if isSingle or goodAlignment(collect, dx,dy, x,y,h,w):                         # Do not update data if there are some jagged power gems in there
                    data = x,y,h,w                                                             # but keep the expansion going (in case its good further...)
                
        if start!=data:
            x,y,h,w = data
            return (x,y,h,w,h*w)
        
    
    def collectNextLine(rngX,rngY, dx,dy,isSingle, c,x,y,h,w,s):
        collect = []
        for a in rngX:
            for b in rngY:
                if 0<=a<lX and 0<=b<lY:
                    g = board[a][b]
                    if (g is None or g[C]!=c or isSingle and g[S]>1
                            or dx and not (y<=g[Y]<y+w and y<g[Y]+g[W]<=y+w)
                            or dy and not (x<=g[X]<x+h and x<g[X]+g[H]<=x+h)):
                        return []
                    collect.append(g)
        return collect
        
        
    def goodAlignment(collect, dx,dy, x,y,h,w):
        return ( all(g[Y]     ==y   for g in collect) if dy==-1 else     # may happen that a combination of powa holds a "jagged" front
                 all(g[Y]+g[W]==y+w for g in collect) if dy== 1 else     # (in the direction of expansion) => invalid, to update data
                 all(g[X]     ==x   for g in collect) if dx==-1 else 
                 all(g[X]+g[H]==x+h for g in collect) )
                 
    
    #------------------------------------------------------------------
    
    
    ROTATIONS    = ((1,0), (0,-1), (-1,0), (0,1))                       # clockwise
    DIRS_POWA    = ((0,-1), (0,1), (1,0), (-1,0))                       # horizontal first
    DIRS_SINGLE  = ((0,1), (1,0))                                       # horizontal first
    C,X,Y,H,W,S  = range(6)                                             # indexes in the gems représentations as: [color, xTopLeft, yTopLeft, h, w, size]
    lX,lY        = 12,6                                                 # dimensions of the board
    start        = 0,3,0                                                # starting config for the drops (x and y of center, and idx of ROTATIONS)
    board        = [ [None]*lY for _ in range(lX)]
    gemsByColors = defaultdict(set)
    
    for n,(pair,moves) in enumerate(arrMoves):
        gemsPair = getStartPoses(moves, *pair)                          # apply the moves to the pair
        if any(board[x][y] is not None for x,y,_ in gemsPair):
            break                                                       # board already filled, end of game...
        for x,y,c in gemsPair:
            board[x][y] = [c,x,y,1,1,1]
            gemsByColors[c].add((x,y))
        
        toDrop = { (x,y) for x,y,_ in gemsPair }
        while toDrop:
            movedGems   = drop(toDrop)
            powaAndDrop = explode(movedGems)
            toDrop      = makePowa(*powaAndDrop)
        
    return '\n'.join( ''.join(gem and gem[C] or ' ' for gem in r) for r in board)
Best Practices1Clever0
01ForkLink


########################################
def check_gem(field, i, j, p):
    if 0 <= i < len(field) and 0 <= j < len(field[i]) and field[i][j]:
        return p(field[i][j])
    else:
        return False

class Gem:
    def __init__(self, field, i, j, color, w=1, h=1, crash=False):
        self.field = field
        self.i, self.j = i, j
        self.color, self.crash = color, crash
        self.w, self.h = w, h
        self.set_field(self)

    def is_power_gem(self):
        return self.w >= 2

    def is_normal_gem(self):
        return not self.is_power_gem() and not self.crash

    def set_field(self, v):
        for i in range(self.i, self.i + self.h):
            for j in range(self.j, self.j + self.w):
                self.field[i][j] = v

    def remove(self):
        self.set_field(None)

    def drop_down(self):
        m = len(self.field) - self.h
        i = next((i for i in range(self.i, m) if any(self.field[i + self.h][self.j:self.j + self.w])), m)
        if i > self.i:
            self.remove()
            self.i = i
            self.set_field(self)
            return True

    def combine_right_down(self):
        if not self.is_normal_gem(): return
        m, n = len(self.field), len(self.field[0])
        pred = lambda gem: gem.is_normal_gem() and gem.color == self.color
        j = next(j for j in range(self.j, n + 1) if not check_gem(self.field, self.i, j, pred) or not check_gem(self.field, self.i + 1, j, pred))
        if j - self.j >= 2:
            self.h = next(i for i in range(self.i + 2, m + 1) if not all(check_gem(self.field, i, k, pred) for k in range(self.j, j))) - self.i
            self.w = j - self.j
            self.set_field(self)

    def expand(self):
        if not self.is_power_gem(): return
        pred1 = lambda gem: gem.is_normal_gem() and gem.color == self.color
        pred2 = lambda w, h: lambda gem: gem.is_power_gem() and gem.color == self.color and (gem.w == w and gem.j == self.j if w > 1 else gem.h == h and gem.i == self.i)
        for i, j, h, w in (self.i, self.j - 1, self.h, 1), (self.i, self.j + self.w, self.h, 1), (self.i - 1, self.j, 1, self.w), (self.i + self.h, self.j, 1, self.w):
            if check_gem(self.field, i, j, pred2(w, h)) or all(check_gem(self.field, u, v, pred1) for u in range(i, i + h) for v in range(j, j + w)):
                gem = self.field[i][j]
                self.i, self.j = min(self.i, gem.i), min(self.j, gem.j)
                if w == 1: self.w += 1
                if h == 1: self.h += 1
                self.set_field(self)
                return self.expand()

def puzzle_fighter(instructions):
    print(instructions)
    m, n = 12, 6
    field = [[None] * n for _ in range(m)]

    def crash_all(color):
        for i in range(m):
            for j in range(n):
                gem = field[i][j]
                if gem and gem.color == color:
                    gem.remove()

    def crash(gem):
        if not gem or not gem.crash: return
        pred = lambda g: g.color == gem.color
        q, gems, visited = [(gem.i, gem.j)], set([gem]), set([(gem.i, gem.j)])
        while q:
            i, j = q.pop()
            for u, v in (i - 1,j), (i + 1, j), (i, j - 1), (i, j + 1):
                if (u, v) not in visited and check_gem(field, u, v, pred):
                    q.append((u, v))
                    visited.add((u, v))
                    gems.add(field[u][v])
        if len(gems) > 1:
            for g in gems:
                g.remove()

    def process(f, up_down=True):
        processed, res = set(), False
        for i in (range(m) if up_down else range(m - 1, -1, -1)):
            for j in range(n):
                gem = field[i][j]
                if gem and gem not in processed:
                    processed.add(gem)
                    res |= bool(f(gem))
        return res

    def step():
        while True:
            process(crash)
            process(lambda gem: gem.combine_right_down())
            process(lambda gem: gem.expand())
            if not process(lambda gem: gem.drop_down(), False):
                break

    def drop(j, color):
        i = next((i for i in range(m) if field[i][j]), m) - 1
        if i < 0: return False
        return Gem(field, i, j, color.upper(), crash=color.islower())

    def move_and_drop(gems, commands):
        j, (di, dj) = 3, (1, 0)
        for cmd in commands:
            if cmd == 'L' and min(j, j + dj) > 0:
                j -= 1
            elif cmd == 'R' and max(j, j + dj) < n - 1:
                j += 1
            else:
                if cmd == 'A': 
                    di, dj = -dj, di
                elif cmd == 'B': 
                    di, dj = dj, -di
                if min(j, j + dj) < 0: j += 1
                if max(j, j + dj) >= n: j -= 1
        xs = [(gems[0], j), (gems[1], j + dj)]
        if di == 1: xs = xs[::-1]
        dropped = []
        for color, k in xs:
            gem = drop(k, color)
            if not gem:
                for g in dropped:
                    g.remove()
                return False
            dropped.append(gem)
        for gem in dropped:
            if gem.color == '0':
                if gem.i + 1 < m and field[gem.i + 1][gem.j]:
                    color = field[gem.i + 1][gem.j].color
                    crash_all(color)
                gem.remove()
        return True

    for gems, commands in instructions:
        if not move_and_drop(gems, commands): break
        step()

    return '\n'.join(''.join((g.color.lower() if g.crash else g.color) if g else ' ' for g in row) for row in field)
  
#######################################
see_states = True
class board():

    def __init__(self):
        self.arr = [[' ' for _ in range(6)] for _ in range(12)]
        self.supergem = []

    def mk_result(self):
        pic = ""
        for row in self.arr:
            rline = ''
            for f in row:
                rline += f[0]
            pic += rline + '\n'
        return pic[:-1]

    def _drop_(self, gem):
        y, x = max(0, gem[1] + 1), gem[2]
        while y <= 11 and self.arr[y][x] == " ":
            y += 1
        y -= 1
        self.arr[y][x] = gem[0]
        return y >= 0

    def _move_gems_(self, step):
        gem1, gem2, moves = [step[0][0], -1, 3], [step[0][1], 0, 3], step[1]
        gdir, dirs = 0, [(1, 0), (0, -1), (-1, 0), (0, 1)]
        for move in moves:
            if move == "L":
                gem1[2] -= 1
                gem2[2] -= 1
            elif move == "R":
                gem1[2] += 1
                gem2[2] += 1
            elif move == "A":
                gdir = (gdir - 1) % 4
            elif move == "B":
                gdir = (gdir + 1) % 4
            if move in "AB":
                gem2[1] = gem1[1] + dirs[gdir][0]
                gem2[2] = gem1[2] + dirs[gdir][1]
            if gem1[2] < 0 or gem2[2] < 0:
                gem1[2] += 1
                gem2[2] += 1
            if 5 < gem1[2] or 5 < gem2[2]:
                gem1[2] -= 1
                gem2[2] -= 1
        return gem1, gem2

    def _del_super_(self):
        dgem = []
        for sgem in self.supergem:
            if len(self.arr[sgem[0]][sgem[1]]) < 2:
                dgem.append(sgem)
        for dg in dgem:
            self.supergem.remove(dg)

    def _crash_all_(self):
        dirs = ((1, 0), (0, -1), (-1, 0), (0, 1))

        def crash_gem(crashgem, y, x, ret):
            assert crashgem in "GBRY"
            res = False
            for d in dirs:
                ny, nx = y + d[0], x + d[1]
                if 0 <= ny < 12 and 0 <= nx < 6 and self.arr[ny][nx][0].upper() == crashgem:
                    self.arr[ny][nx] = " "
                    res = True
                    crash_gem(crashgem, ny, nx, False)
            if ret:
                return res

        def delgems(crashgem):
            for y in range(12):
                for x in range(6):
                    if self.arr[y][x][0].upper() == crashgem:
                        self.arr[y][x] = " "

        crashed = False
        for y in range(12):
            for x in range(6):
                if self.arr[y][x] in "gbry":
                    if crash_gem(self.arr[y][x].upper(), y, x, True):
                        self.arr[y][x] = " "
                        crashed = True
                if self.arr[y][x] == "0":
                    crashed = True
                    self.arr[y][x] = " "
                    if y < 11 and self.arr[y + 1][x][0] != "0":
                        delgems(self.arr[y + 1][x][0].upper())
        if crashed:
            self._del_super_()
        return crashed

    def _gravity_gem_(self):
        for x in range(6):
            col = [" " for _ in range(12)]
            cy = 11
            for y in range(11, -1, -1):
                if self.arr[y][x] != " " and len(self.arr[y][x]) == 1:
                    col[cy] = self.arr[y][x]
                    cy -= 1
                if len(self.arr[y][x]) == 2:
                    col[y] = self.arr[y][x]
                    cy = y - 1
            for y in range(12):
                self.arr[y][x] = col[y]

    def _gravity_super_(self):
        lsg = len(self.supergem)
        down = [0 for _ in range(lsg)]
        found = False
        for i in range(lsg):
            addon = 0
            while self.supergem[i][2] + addon + 1 < 12 and all(self.arr[self.supergem[i][2] + addon + 1][x] == " " for x in list(range(self.supergem[i][1], self.supergem[i][3] + 1))):
                addon += 1
            down[i] = addon
        for i, d in enumerate(down):
            if d > 0:
                found = True
                self.supergem[i] = (self.supergem[i][0] + d, self.supergem[i][1], self.supergem[i][2] + d, self.supergem[i][3], self.supergem[i][4])
                sgem = self.supergem[i]
                for y in range(sgem[0] - d, sgem[0]):
                    for x in range(sgem[1], sgem[3] + 1):
                        self.arr[y][x] = " "
                for y in range(sgem[0], sgem[2] + 1):
                    for x in range(sgem[1], sgem[3] + 1):
                        self.arr[y][x] = sgem[4] + "S"
        return found

    def _gravity_(self):
        self._gravity_gem_()
        while self._gravity_super_():
            self._gravity_gem_()

    def _pgem_enlarge_(self, pg_lst):
        pgem = []
        for pg in pg_lst:
            y_lst = list(range(pg[0], pg[2] + 1))
            x_lst = list(range(pg[1], pg[3] + 1))
            if pg[3] < 5 and all(self.arr[yt][pg[3] + 1][0] == pg[4] for yt in y_lst):
                pgem.append((pg[0], pg[1], pg[2], pg[3] + 1, pg[4]))
            if pg[2] < 11 and all(self.arr[pg[2] + 1][xt][0] == pg[4] for xt in x_lst):
                pgem.append((pg[0], pg[1], pg[2] + 1, pg[3], pg[4]))
            if (pg[2] - pg[0]) * (pg[3] - pg[1]) > 0:
                pgem.append(pg)
        return sorted(list(set(pgem)))

    def _find_super_(self, y, x):
        return list(sgem for sgem in self.supergem if sgem[0] == y and sgem[1] == x)

    def _create_possgem_(self):
        pgem_norm, pgem_super, super = [], [], False
        for y in range(12):
            for x in range(6):
                if self.arr[y][x][0] in 'GBRY':
                    lgem = []
                    if len(self.arr[y][x]) == 1:
                        tgem = self._pgem_enlarge_([(y, x, y, x, self.arr[y][x])])
                        super = False
                    else:
                        tgem = self._find_super_(y, x)
                        super = True
                    while tgem != lgem:
                        lgem = []
                        for tg in tgem:
                            lgem.append(tg)
                        tgem = self._pgem_enlarge_(tgem)
                    for tg in tgem:
                        if super:
                            if tg not in pgem_super:
                                pgem_super.append(tg)
                        else:
                            if tg not in pgem_norm:
                                pgem_norm.append(tg)
        return sorted(pgem_norm) + sorted(pgem_super)

    def _merge_pg_sg_(self, pgem):
        if pgem in self.supergem:
            return
        y_lst = list(range(pgem[0], pgem[2] + 1))
        x_lst = list(range(pgem[1], pgem[3] + 1))
        add_gem, no_part, dgem = False, True, []
        for sgem in self.supergem:
            if sgem[0] in y_lst and sgem[1] in x_lst and sgem[2] in y_lst and sgem[3] in x_lst:
                dgem.append(sgem)
                add_gem = True
            elif sgem[0] > pgem[2] or sgem[1] > pgem[3] or pgem[0] > sgem[2] or pgem[1] > sgem[3]:
                pass
            else:
                no_part = False
        if no_part:
            if add_gem:
                for dg in dgem:
                    self.supergem.remove(dg)
            self.supergem.append(pgem)
            self.supergem = sorted(self.supergem)
            for y in y_lst:
                for x in x_lst:
                    self.arr[y][x] = self.arr[y][x][0] + "S"

    def _upd_supergem_(self):
        pgems = self._create_possgem_()
        for pg in pgems:
            self._merge_pg_sg_(pg)

    def include(self, step):
        assert len(step) == 2
        gem1, gem2 = self._move_gems_(step)
        if gem2[1] > gem1[1]:
            if not self._drop_(gem2):
                return False
            if not self._drop_(gem1):
                return False
        else:
            if not self._drop_(gem1):
                return False
            if not self._drop_(gem2):
                return False
        self._upd_supergem_()
        while self._crash_all_():
            self._gravity_()
            self._upd_supergem_()
        return True


def puzzle_fighter(ar):
    puzzle = board()
    for step in ar:
        sgame = puzzle.mk_result()
        if not puzzle.include(step):
            return sgame
    return puzzle.mk_result()
  
############################################
see_states = True

from collections import deque
from itertools import product
NROW = 12
NCOL = 6

def board_to_string(board):
    return '\n'.join([''.join(row) for row in board])

def board_to_debug_string(board):
    return '\n'.join([''.join(row) for row in board]).replace(' ', '.')

def power_gems_to_debug_string(power_gems):
    board = [[' '] * NCOL for i in range(NROW)]
    idx = 0
    for r1, c1, r2, c2 in power_gems:
        idx += 1
        for row in range(r1, r2+1):
            for col in range(c1, c2+1):
                board[row][col] = str(idx)
    return board_to_debug_string(board)

def print_state(name, board, power_gems):
    print(name, ': ')
    print('=== ==')
    print(board_to_debug_string(board))
    print('======')
    if len(power_gems) > 0:
        print('power gems: ', power_gems)
        print(power_gems_to_debug_string(power_gems))

def color(c):
    return c.upper()

def color_at(board, pos):
    return color(board[pos[0]][pos[1]])

def down_pos(pos):
    return (pos[0]+1, pos[1])

def in_rect(rect, pos):
    r1, c1, r2, c2 = rect
    return pos[0] >= r1 and pos[0] <= r2 and pos[1] >= c1 and pos[1] <= c2

def get_power_gem_id(power_gems, pos):
    for i, rect in enumerate(power_gems):
        if in_rect(rect, pos):
            return i
    return -1

def get_power_gem_id_by_r2c1(power_gems, pos):
    for i, rect in enumerate(power_gems):
        if rect[2] == pos[0] and rect[1] == pos[1]:
            return i
    return -1

def has_power_gem_at(power_gems, pos):
    return get_power_gem_id(power_gems, pos) >= 0

def is_individual_regular(board, power_gems, pos, c):
    if has_power_gem_at(power_gems, pos): return False
    return color_at(board, pos) == c

def all_are_individual_regular(board, power_gems, rect, c):
    r1, c1, r2, c2 = rect
    for row in range(r1, r2+1):
        for col in range(c1, c2+1):
            if not is_individual_regular(board, power_gems, (row, col), c):
                return False
    return True

def all_are_empty(board, rect):
    r1, c1, r2, c2 = rect
    for row in range(r1, r2+1):
        for col in range(c1, c2+1):
            if board[row][col] != ' ':
                return False
    return True

# step 4: auto-drop everything with empty cell below
# power gems will fall together
# returns new positions
def fall_power_gem(board, power_gems, idx, delta_row, debug_show):
    if debug_show:
        print('fall_power_gem: {} delta={}', power_gems[idx], delta_row)
    r1, c1, r2, c2 = power_gems[idx]
    for i in range(delta_row):
        for c in range(c1, c2+1):
            board[r2+1+i][c] = board[r1+i][c]
            board[r1+i][c] = ' '
    power_gems[idx] = (r1 + delta_row, c2, r2 + delta_row, c2)

def fall_with_gravity(board, power_gems, debug_show):
    changed = False
    if debug_show:
        print_state('before fall', board, power_gems)
    for row in range(NROW-1, -1, -1):
        for col in range(NCOL):
            if board[row][col] != ' ' and not has_power_gem_at(power_gems, (row, col)):
                row2 = row
                while row2 < NROW-1 and board[row2+1][col] == ' ':
                    row2 += 1
                if row2 > row:
                    changed = True
                    board[row2][col] = board[row][col]
                    board[row][col] = ' '
            else:
                idx = get_power_gem_id_by_r2c1(power_gems, (row, col))
                if idx >= 0:
                    r1, c1, r2, c2 = power_gems[idx]
                    row2 = row
                    while row2 < NROW-1 and all_are_empty(board, (row2+1, c1, row2+1, c2)):
                        row2 += 1
                    if row2 > row:
                        changed = True
                        fall_power_gem(board, power_gems, idx, row2 - row, debug_show)
    return changed

# step 1: rotate the initial gem pair
# Initial:
# shape: 0----1-----2-----3-
#        1    12    2     21
#        2          1
# returns (shape, col)
def pair_width(shape):
    return 1 + shape % 2

def rotate_and_move_pair(instructions):
    shape = 0
    col = 3 # 0-based
    for inst in instructions:
        if inst == 'L': col -= 1
        elif inst == 'R': col += 1
        elif inst == 'A': # ccw, 2 around 1
            shape = (shape + 1) % 4
            if shape == 3: col -= 1
            elif shape == 0: col += 1
        elif inst == 'B': # cw, 2 around 1
            shape = (shape + 3) % 4
            if shape == 2: col += 1
            elif shape == 3: col -= 1
        # adjust
        if col < 0: col = 0
        if col + pair_width(shape) - 1 >= NCOL: col -= 1
    return (shape, col)

# step 2: Drops the initial gem pair. calls drop_with_gravity if disjoint happens
# return None is game over (board will NOT be modified in this case)
# returns [(row1, col1), (row2, col2)], e.g. positions of the newly dropped gems
def get_top_gem_row(board, col):
    for row in range(NROW):
        if board[row][col] != ' ': return row
    return NROW

def drop_pair(board, gem_pair, shape, col):
    w = pair_width(shape)
    top_row = get_top_gem_row(board, col)
    if w == 1:
        if top_row - 2 < 0: return None
        up = 0
        if shape == 2: up = 1
        board[top_row-2][col] = gem_pair[up]
        board[top_row-1][col] = gem_pair[1 - up]
        return [(top_row-2, col), (top_row-1, col)]
    else:
        if top_row - 1 < 0: return None
        top_row2 = get_top_gem_row(board, col+1)
        if top_row2 - 1 < 0: return None
        left = 0
        if shape == 3: left = 1
        board[top_row-1][col] = gem_pair[left]
        board[top_row2-1][col+1] = gem_pair[1-left]
        return [(top_row-1, col), (top_row2-1, col+1)]

# step 3: rainbow gems -> crash gems -> power gem formation
# only gems at `new_positions` will be checked (they are newly dropped/fallen)
# returns True if any gem is cleared

def do_rainbow(board, pos, removed_positions, debug_show):
    if debug_show:
        print('rainbow! pos={}'.format(pos))
    removed_positions.add(pos)
    if pos[0] < NROW-1:
        c = color_at(board, down_pos(pos))
        if debug_show:
            print('destroying all color {}'.format(c))
        for pos2 in product(range(NROW), range(NCOL)):
            if color_at(board, pos2) == c:
                removed_positions.add(pos2)

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

def do_crash(board, pos, removed_positions, debug_show):
    if debug_show:
        print('do_crash: {} {}'.format(pos, board[pos[0]][pos[1]]))
    if pos in removed_positions:
        return # already destroyed by rainbow or another crash
    # remove all connected gems. rainbows are considered "no color" instead of "any color"
    # use a separate set to avoid messing up with another color's connected components
    c = color_at(board, pos)
    vis = set([pos])
    Q = deque()
    Q.append(pos)
    cnt = 0
    while len(Q) > 0:
        cnt += 1
        pos = Q.popleft()
        removed_positions.add(pos)
        for d in range(4):
            row = pos[0] + dr[d]
            col = pos[1] + dc[d]
            if row < 0 or row >= NROW or col < 0 or col >= NCOL: continue
            if color_at(board, (row, col)) != c: continue
            pos2 = (row, col)
            if pos2 in vis: continue
            vis.add(pos2)
            Q.append(pos2)
    if cnt == 1:
        removed_positions.remove(pos)

def new_power_gem(power_gems, rect, debug_show):
    if debug_show:
        print('new gem: ', rect)
    power_gems.append(rect)
    power_gems.sort() # ensure enumerating from top to bottom, left to right

def expand_power_gem(power_gems, idx, rect, debug_show):
    if debug_show:
        print('power gems: {} to {}'.format(power_gems[idx], rect))
    power_gems[idx] = rect

# form one power gem at a time (but greedily), return True if succeeded
def merge_individual_gems(board, power_gems, debug_show):
    for pos in product(range(NROW-1), range(NCOL-1)):
        row, col = pos
        if has_power_gem_at(power_gems, pos): continue
        c = color_at(board, pos)
        if c == ' ': continue
        if not is_individual_regular(board, power_gems, down_pos(pos), c): continue
        # now that pos and down_pos(pos) are same-color, try to extend right as much as possible
        if debug_show:
            print('merge_individual_gems: candidate ({},{}), {}'.format(row, col, c))
        col2 = col
        while col2+1 < NCOL and all_are_individual_regular(board, power_gems, (row, col2+1, row+1, col2+1), c):
            col2 += 1
        if col2 == col: continue
        # final column range is [col~col2] and at least 2 rows
        # now extend down as much as possible
        row2 = row+1
        while row2+1 < NROW and all_are_individual_regular(board, power_gems, (row2+1, col, row2+1, col2), c):
            row2 += 1
        new_power_gem(power_gems, (row, col, row2, col2), debug_show)
        break

# expand one power gem at a time, return True if succeeded
def expand_power_gems_with_individual(board, power_gems, debug_show):
    for i in range(len(power_gems)):
        # don't use enumerate because we can't change power_gems when iterating it!
        row1, col1, row2, col2 = power_gems[i]
        c = color_at(board, (row1, col1))
        # left
        col0 = col1
        while col0 > 0 and all_are_individual_regular(board, power_gems, (row1, col0-1, row2, col0-1), c):
            col0 -= 1
        # right
        col3 = col2
        while col3 < NCOL-1 and all_are_individual_regular(board, power_gems, (row1, col3+1, row2, col3+1), c):
            col3 += 1
        # up
        row0 = row1
        while row0 > 0 and all_are_individual_regular(board, power_gems, (row0-1, col0, row0-1, col3), c):
            row0 -= 1
        # down
        row3 = row2
        while row3 < NROW-1 and all_are_individual_regular(board, power_gems, (row3+1, col0, row3+1, col3), c):
            row3 += 1
        if col1 != col0 or col2 != col3 or row1 != row0 or row2 != row3:
            expand_power_gem(power_gems, i, (row0, col0, row3, col3), debug_show)
            return True
    return False

def is_adjacent_left(rect1, rect2):
    r1, c1, r2, c2 = rect1
    r3, c3, r4, c4 = rect2
    return r1 == r3 and r2 == r4 and c2+1 == c3

def is_adjacent_up(rect1, rect2):
    r1, c1, r2, c2 = rect1
    r3, c3, r4, c4 = rect2
    return c1 == c3 and c2 == c4 and r2+1 == r3

def can_merge(board, rect1, rect2):
    if color_at(board, (rect1[0], rect1[1])) != color_at(board, (rect2[0], rect2[1])): return False
    if is_adjacent_left(rect1, rect2): return True
    if is_adjacent_left(rect2, rect1): return True
    if is_adjacent_up(rect1, rect2): return True
    if is_adjacent_up(rect2, rect1): return True
    return False

def aabb(rect1, rect2):
    r1, c1, r2, c2 = rect1
    r3, c3, r4, c4 = rect2
    return (min(r1, r3), min(c1, c3), max(r2, r4), max(c2, c4))

# expand one power gem at a time, return True if succeeded
def expand_power_gems_with_power_gems(board, power_gems, debug_show):
    for i in range(len(power_gems)):
        # don't use enumerate because we can't change power_gems when iterating it!
        for j in range(i+1, len(power_gems)):
            if can_merge(board, power_gems[i], power_gems[j]):
                power_gems[i] = aabb(power_gems[i], power_gems[j])
                last = power_gems.pop()
                if j < len(power_gems):
                    power_gems[j] = last
                power_gems.sort()
                return True
    return False

def remove_power_gems(power_gems, removed_positions):
    old_power_gems = power_gems[:]
    power_gems.clear()
    for rect in old_power_gems:
        alive = True
        for pos in removed_positions:
            if in_rect(rect, pos):
                alive = False
                break
        if alive:
            power_gems.append(rect)

def do_effects(board, power_gems, debug_show):
    removed_positions = set()
    # rainbow/crash
    for pos in product(range(NROW), range(NCOL)):
        if board[pos[0]][pos[1]] == '0':
            do_rainbow(board, pos, removed_positions, debug_show)
        elif board[pos[0]][pos[1]].islower():
            do_crash(board, pos, removed_positions, debug_show)
    if debug_show:
        print('removed postions: ', removed_positions)
    for pos in removed_positions:
        board[pos[0]][pos[1]] = ' '
    remove_power_gems(power_gems, removed_positions)

    # power gem formation
    while merge_individual_gems(board, power_gems, debug_show):
        pass
    while expand_power_gems_with_individual(board, power_gems, debug_show):
        pass
    while expand_power_gems_with_power_gems(board, power_gems, debug_show):
        pass
    return len(removed_positions) > 0

def puzzle_fighter(ar):
    board = [[' '] * NCOL for i in range(NROW)]
    power_gems = []
    step = 0
    show_step_range = [-1, -1]
    for gem_pair, instructions in ar:
        step += 1
        debug_show = False
        if step >= show_step_range[0] and step <= show_step_range[1]:
            debug_show = True
        if debug_show:
            print('Step ', step, ': ', gem_pair, instructions)
        shape, col = rotate_and_move_pair(instructions)
        if debug_show:
            print('Shape: ', shape, ' Col: ', col)
        new_positions = drop_pair(board, gem_pair, shape, col)
        if new_positions is None:
            break # game over
        while do_effects(board, power_gems, debug_show):
            if not fall_with_gravity(board, power_gems, debug_show):
                break
        if debug_show:
            print_state('final', board, power_gems)
    return board_to_string(board)
  
######################################################################
see_states = False
class Gem:
    def __init__(self, gem_letter, top, bottom, left, right):
        self.rainbow = False
        self.crash = False
        self.color = gem_letter
        if gem_letter == '0':
            self.rainbow = True
        elif gem_letter.islower():
            self.crash = True
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right


def find_gem_by_cell(fallen_gems, y, x):
    gems = [gem for gem in fallen_gems if gem.top <= y <= gem.bottom and gem.left <= x <= gem.right]
    if not gems:
        return None
    return gems[0]


def destroy_given_gems(fallen_gems, given_gems):
    return [gem for gem in fallen_gems if gem not in given_gems]


def destroy_all_gems_of_given_color(given_gems, gem_color):
    simple_color = gem_color.upper()
    crash_gem_color = gem_color.lower()
    return [gem for gem in given_gems if gem.color != simple_color and gem.color != crash_gem_color]


def find_connected_gems_of_same_color(fallen_gems, given_gem, found_gems):
    found_gems.add(given_gem)
    for y_const in [given_gem.top - 1, given_gem.bottom + 1]:
        for x in range(given_gem.left, given_gem.right + 1):
            near_gem = find_gem_by_cell(fallen_gems, y_const, x)
            if near_gem:
                if near_gem.color.upper() == given_gem.color.upper() and near_gem not in found_gems:
                    found_gems = find_connected_gems_of_same_color(fallen_gems, near_gem, found_gems)
    for x_const in [given_gem.left - 1, given_gem.right + 1]:
        for y in range(given_gem.top, given_gem.bottom + 1):
            near_gem = find_gem_by_cell(fallen_gems, y, x_const)
            if near_gem:
                if near_gem.color.upper() == given_gem.color.upper() and near_gem not in found_gems:
                    found_gems = find_connected_gems_of_same_color(fallen_gems, near_gem, found_gems)
    return found_gems


def fall_through_given_gem(gem, fallen_gems):
    while True:
        if gem.bottom == 11:
            return gem
        for x in range(gem.left, gem.right + 1):
            if find_gem_by_cell(fallen_gems, gem.bottom + 1, x):
                return gem
        gem.top += 1
        gem.bottom += 1


def fall_through_all_gems(fallen_gems):
    fallen_gems.sort(key=lambda x: x.bottom, reverse=True)
    for gem in fallen_gems:
        gem = fall_through_given_gem(gem, fallen_gems)
    return fallen_gems


def power_gem_formation(fallen_gems):
    # print('\nPOWER GEM FORMATION! START\n')
    # find all simple gems that are not placed on the floor and along right edge of the playfield
    simple_gems = [gem for gem in fallen_gems if gem.top == gem.bottom and gem.left == gem.right]
    init_simple_gems = [gem for gem in simple_gems if gem.right < 5 and gem.bottom < 11]
    init_simple_gems.sort(key=lambda g: (g.bottom, g.left), reverse=True)
    # print('Simple gems power formation...')
    while init_simple_gems:
        simple_gem = init_simple_gems.pop()


        right = find_gem_by_cell(simple_gems, simple_gem.bottom, simple_gem.right + 1)

        lower = find_gem_by_cell(simple_gems, simple_gem.bottom + 1, simple_gem.right)

        diagonal = find_gem_by_cell(simple_gems, simple_gem.bottom + 1, simple_gem.right + 1)

        if right and lower and diagonal:
            if simple_gem.color == right.color == lower.color == diagonal.color:
                forming_gems = [simple_gem, right, lower, diagonal]
                # try to grow cluster to the right
                right_edge = simple_gem.right + 1
                while True:
                    up = find_gem_by_cell(simple_gems, simple_gem.bottom, right_edge + 1)
                    low = find_gem_by_cell(simple_gems, simple_gem.bottom + 1, right_edge + 1)
                    if up and low:
                        if up.color == low.color == simple_gem.color:
                            # horizontal growth!
                            forming_gems.append(up)
                            forming_gems.append(low)
                            right_edge += 1
                        else:
                            break
                    else:
                        break
                # try to grow cluster down
                lower_edge = simple_gem.bottom
                able_to_grow_down = True
                while True:
                    raw_under_forming_gems = []
                    for x in range(simple_gem.left, right_edge + 1):
                        potential_gem = find_gem_by_cell(simple_gems, lower_edge + 1, x)
                        if not potential_gem:
                            able_to_grow_down = False
                            break
                        if potential_gem.color != simple_gem.color:
                            able_to_grow_down = False
                            break
                        raw_under_forming_gems.append(potential_gem)
                    if able_to_grow_down:
                        lower_edge += 1
                        forming_gems += raw_under_forming_gems
                    else:
                        break

                # time to replace simple gems with one power gem
                simple_gems = [gem for gem in simple_gems if gem not in forming_gems]
                fallen_gems = [gem for gem in fallen_gems if gem not in forming_gems]
                new_power_gem = Gem(simple_gem.color, simple_gem.top, lower_edge, simple_gem.left, right_edge)
                fallen_gems.append(new_power_gem)


    power_gems = [gem for gem in fallen_gems if gem.left != gem.right or gem.top != gem.bottom]
    power_gems.sort(key=lambda g: (g.top, g.left), reverse=True)
    while power_gems:
        power_gem = power_gems.pop()
        horizontal_combining = False
        for i, side_column in enumerate([power_gem.left - 1, power_gem.right + 1]):
            if side_column == -1 or side_column == 6:
                continue
            simple_gems_on_the_side = []
            for y in range(power_gem.top, power_gem.bottom + 1):
                gem = find_gem_by_cell(fallen_gems, y, side_column)
                if not gem:
                    simple_gems_on_the_side = []
                    break
                if gem.color != power_gem.color:
                    simple_gems_on_the_side = []
                    break
                if gem.top == gem.bottom:
                    simple_gems_on_the_side.append(gem)
                elif gem.top != gem.bottom:
                    # power gem too
                    if simple_gems_on_the_side:
                        simple_gems_on_the_side = []
                        break
                    else:
                        # nb. gem fits current
                        if gem.top == power_gem.top and gem.bottom == power_gem.bottom:
                            # horizintal connection
                            # create new power gem
                            left_side_new = min(gem.left, power_gem.left)
                            right_side_new = max(gem.right, power_gem.right)
                            new_power_gem = Gem(power_gem.color, power_gem.top, power_gem.bottom, left_side_new,
                                                right_side_new)
                            # remove two old power gems from fallen_gems
                            fallen_gems = [g for g in fallen_gems if g is not power_gem and g is not gem]
                            fallen_gems.append(new_power_gem)
                            power_gems.append(new_power_gem)
                            horizontal_combining = True
                            break
                        else:
                            simple_gems_on_the_side = []
                            break
            if horizontal_combining:
                break
            horizontal_combining = False
            if simple_gems_on_the_side:
                first_simple_gem = simple_gems_on_the_side[0]
                # horizintal connection
                # create new power gem
                left_side_new = min(first_simple_gem.left, power_gem.left)
                right_side_new = max(first_simple_gem.right, power_gem.right)
                new_power_gem = Gem(power_gem.color, power_gem.top, power_gem.bottom, left_side_new, right_side_new)
                # remove two old power gems from fallen_gems
                fallen_gems = [gem for gem in fallen_gems if
                               gem is not power_gem and gem not in simple_gems_on_the_side]
                fallen_gems.append(new_power_gem)
                power_gems.append(new_power_gem)
                power_gems.sort(key=lambda g: (g.top, g.left), reverse=True)
                horizontal_combining = True
                break

        if horizontal_combining:
            continue

        # then check top and bottom sides
        vertical_combining = False
        for i, close_raw in enumerate([power_gem.top - 1, power_gem.bottom + 1]):
            if close_raw == -1 or close_raw == 12:
                continue
            simple_gems_on_the_side = []
            for x in range(power_gem.left, power_gem.right + 1):
                gem = find_gem_by_cell(fallen_gems, close_raw, x)
                if not gem:
                    simple_gems_on_the_side = []
                    break
                if gem.color != power_gem.color:
                    simple_gems_on_the_side = []
                    break
                if gem.left == gem.right:
                    simple_gems_on_the_side.append(gem)
                elif gem.left != gem.right:
                    # power gem too
                    if simple_gems_on_the_side:
                        # print('But some simple gems are already there. Break')
                        simple_gems_on_the_side = []
                        break
                    else:
                        # nb. gem fits current
                        if gem.left == power_gem.left and gem.right == power_gem.right:
                            # horizintal connection
                            # create new power gem
                            top_new = min(gem.top, power_gem.top)
                            bottom_new = max(gem.bottom, power_gem.bottom)

                            new_power_gem = Gem(power_gem.color, top_new, bottom_new, power_gem.left, power_gem.right)

                            # remove two old power gems from fallen_gems
                            fallen_gems = [g for g in fallen_gems if g is not power_gem and g is not gem]
                            fallen_gems.append(new_power_gem)
                            power_gems.append(new_power_gem)
                            horizontal_combining = True
                            break
                        else:
                            # print('Near power gem does not fit current')
                            simple_gems_on_the_side = []
                            break
            if vertical_combining:
                break
            if simple_gems_on_the_side:
                first_simple_gem = simple_gems_on_the_side[0]
                # horizintal connection
                # create new power gem
                top_new = min(first_simple_gem.top, power_gem.top)
                bottom_new = max(first_simple_gem.bottom, power_gem.bottom)
                new_power_gem = Gem(power_gem.color, top_new, bottom_new, power_gem.left, power_gem.right)
                # remove two old power gems from fallen_gems
                fallen_gems = [gem for gem in fallen_gems if
                               gem is not power_gem and gem not in simple_gems_on_the_side]
                fallen_gems.append(new_power_gem)
                power_gems.append(new_power_gem)
                power_gems.sort(key=lambda g: (g.top, g.left), reverse=True)
                vertical_combining = True
                break
    return fallen_gems


def process_crash_gem(fallen_gems, crash_gem):
    connected_same_color_gems = find_connected_gems_of_same_color(fallen_gems, crash_gem, set())
    if len(connected_same_color_gems) == 1:
        return fallen_gems
    fallen_gems = destroy_given_gems(fallen_gems, connected_same_color_gems)
    return fallen_gems


def color_letter_from_gem(gem):
    if gem is None:
        return ' '
    letter = gem.color
    if gem.crash:
        letter = letter.lower()
    return letter


def get_playfield_from_gems(fallen_gems, headline=''):
    playfield = [[color_letter_from_gem(find_gem_by_cell(fallen_gems, y, x)) for x in range(6)] for y in range(12)]
    return playfield


def process_playfield(fallen_gems, landed_gems):
    new_born_gems = []
    for gem_letter, [y, x] in landed_gems:
        new_gem = Gem(gem_letter, y, y, x, x)
        new_born_gems.append(new_gem)

    new_born_gems.sort(key=lambda gem: gem.bottom)

    actual_rainbow_gems = []
    for new_gem in new_born_gems:
        fallen_gems.append(new_gem)
        if new_gem.rainbow:
            actual_rainbow_gems.append(new_gem)

    # process all crash gems
    state_changed = True
    while state_changed:
        # precrash pg formation
        fallen_gems = power_gem_formation(fallen_gems)

        gem_num_before = len(fallen_gems)

        if actual_rainbow_gems:
            actual_rainbow_gems.sort(key=lambda g: g.bottom, reverse=True)
            while actual_rainbow_gems:
                rainbow_gem = actual_rainbow_gems.pop()
                if rainbow_gem.bottom < 11:
                    gem_under = find_gem_by_cell(fallen_gems, (rainbow_gem.bottom + 1), rainbow_gem.right)
                    if gem_under:
                        fallen_gems = destroy_all_gems_of_given_color(fallen_gems, gem_under.color)
                if rainbow_gem in fallen_gems:
                    fallen_gems.remove(rainbow_gem)

        crash_gems = [gem for gem in fallen_gems if gem.crash]
        crash_gems.sort(key=lambda g: g.bottom)

        if crash_gems:
            for crash_gem in crash_gems:
                fallen_gems = process_crash_gem(fallen_gems, crash_gem)

        gem_num_after = len(fallen_gems)
        if gem_num_before == gem_num_after:
            state_changed = False
        else:
            fallen_gems = fall_through_all_gems(fallen_gems)

    fallen_gems = power_gem_formation(fallen_gems)

    playfield = get_playfield_from_gems(fallen_gems, headline='playfield after move:')

    return fallen_gems, playfield

def look_down(playfield, gem_position):
    y_gem, x_gem = gem_position
    if playfield[0][x_gem] != ' ':
        # overflow: True
        return True, None
    for y in range(y_gem, 12):
        if y == 11:
            return False, y
        elif playfield[y + 1][x_gem] != ' ':
            return False, y


def drop_gem(playfield, gem, gem_position):
    overflow, landed_y = look_down(playfield, gem_position)
    if overflow:
        return overflow, playfield, None
    playfield[landed_y][gem_position[1]] = gem
    return overflow, playfield, [landed_y, gem_position[1]]


def drop_pair(playfield, pair, pair_position):
    [y1, x1], [y2, x2] = pair_position
    pair_position = [0, x1], [0, x2]  # zero y, because all movements are made above the playfield
    if y1 >= y2:
        pass
    else:
        pair = [pair[1], pair[0]]
        pair_position = [0, x2], [0, x1]
    gems_landed = []
    for gem, gem_position in zip(pair, pair_position):
        overflow, playfield, gem_landed_position = drop_gem(playfield, gem, gem_position)
        if overflow:
            return overflow, playfield, gems_landed
        gems_landed.append([gem, gem_landed_position])
    return overflow, playfield, gems_landed


def move_pair(playfield, moves):
    # process landing and possible disjointing

    # begining coordinates of paired gems
    y1, x1 = 0, 3
    y2, x2 = 1, 3

    for move_num, move in enumerate(moves):
        if move == 'L':
            left_edge = min(x1, x2)
            if left_edge > 0:
                x1 -= 1
                x2 -= 1
            else:
                pass
        elif move == 'R':
            # R: move right
            right_edge = max(x1, x2)
            if right_edge < 5:
                x1 += 1
                x2 += 1
            else:
                pass
        elif move == 'A':
            # A: rotate counter - clockwise
            if x1 == x2:
                if y2 < y1:
                    if x1 == 0:
                        x1 = 1
                        y1 = y2
                    else:
                        y2 = y1
                        x2 = x1 - 1
                elif y2 > y1:
                    if x1 == 5:
                        x1 = 4
                        y1 = y2
                    else:
                        y2 = y1
                        x2 = x1 + 1
                else:
                    pass
            elif y1 == y2:
                if x1 < x2:
                    if y1 == 0:  # ________________
                        y1 = 1  # 1 2  ->  2
                        y2 = 0  # 1
                        x2 = x1
                    else:
                        x2 = x1  # 2
                        y2 = y1 - 1  # 1 2  ->    1
                elif x1 > x2:
                    x2 = x1
                    y2 = y1 + 1
                else:
                    pass
        elif move == 'B':
            # B: rotate clockwise
            if x1 == x2:
                if y2 > y1:
                    if x1 == 0:
                        x1 = 1
                        y2 = y1
                        x2 = 0
                    else:
                        y2 = y1
                        x2 = x1 - 1
                elif y2 < y1:
                    if x1 == 5:
                        x2 = x1
                        y2 = y1
                        x1 = 4
                    else:
                        y2 = y1
                        x2 = x1 + 1
                else:
                    pass
            elif y1 == y2:
                if x1 < x2:
                    y2 = y1 + 1
                    x2 = x1
                elif x1 > x2:
                    if y1 == 0:  # ________________
                        y1 = 1  # 2 1  ->  2
                        y2 = 0  # 1
                        x2 = x1
                    else:
                        x2 = x1  # 2
                        y2 = y1 - 1  # 2 1  ->   1
                else:
                    pass

    return [[y1, x1], [y2, x2]]


def get_state_from_playfield(playfield):
    return '\n'.join([''.join(raw) for raw in playfield])


def puzzle_fighter(ar):
    playfield = [[' ' for __ in range(6)] for _ in range(12)]
    fallen_gems = []
    for i, [pair, moves] in enumerate(ar):

        pair_position = move_pair(playfield, moves)

        overflow, playfield, landed_gems = drop_pair(playfield, pair, pair_position)

        if overflow:
            # undo current move and quit
            for [gem_letter, gem_position] in landed_gems:
                playfield[gem_position[0]][gem_position[1]] = ' '
            return get_state_from_playfield(playfield)

        fallen_gems, playfield = process_playfield(fallen_gems, landed_gems)

    return get_state_from_playfield(playfield)
  
#######################################################
class Gem () :
    def __init__(self,color) :
        self.color = color
        self.belongSuperGem =  False
        
    def getColor(self) :
        return self.color
    
    def getSuperGem(self):
        return self.belongSuperGem 
    
    def setSuperGem(self):
        self.belongSuperGem =  True 
       
class SuperGem() : 
    
    def __init__(self,sup,dim):
        self.x, self.y = sup
        self.h, self.w = dim
     
        
class Game() :
    
    def __init__(self,ar,lines,columns) :
        self.dictrotA = {(1,0):(0,1), (0,1): (-1,0),(-1,0):(0,-1),(0,-1):(1,0) }
        self.dictrotR = {v:k for k,v in self.dictrotA.items()}   
        self.array = [['' for j in range(columns+1)]for i in range(lines)] 
        self.ar = ar
        self.listSuperGems = []
        
    def playGame(self) :
        for colors,moves in self.ar :
            # along the list and if the gem can fall in the array 
            # vertical displacement to the lowest position
            if not self.movesDuoGems (colors,moves) :
                break 
            # creation of supergems
            maxpos = self.maxPositions()   
            self.addSupergems()

            while True :
                maxpos = self.maxPositions()
                
                # modify des supergems  
                self.modifySupergems()
                
                #explosion(color or rainbow)                
                self.explodeGems()

                # gems fall 
                self.gemsFall()
                
                # create new supergems after fall      
                self.addSupergems()
 
                
                # measure of moves
                if sum([a-b for a, b in zip(maxpos, self.maxPositions()) ])==0 :
                    break
                          
        return self.printArrayFinal()         
          
    def maxPositions (self) :
        maxPos = []
        for j in range(1,len(self.array[0])) :
            for i in range(len(self.array)) :
                if self.array[i] [j] !='' :
                    i-=1
                    break 
            maxPos.append(i)
        return maxPos
    
    def fallGem(self,x,y):
        i = x+1
        while i+1<= len(self.array) and self.array[i][y] == '':
            i+=1
        return i-1
     
    def fallSuper(self, super):
        beg = super.x + super.h
        i = 0
        while i+beg < len(self.array)  and len([self.array[beg+i][j] for j in range(super.y, super.y+super.w) if self.array[beg+i][j]=='' ])==super.w :
            i+=1
        return beg -super.h +i     

    def deplaceSuper(self,super,delta) :
        for i in range(super.x+super.h-1,super.x-1,-1) :
            for j in range(super.y, super.y + super.w):
                self.array[i+delta][j] = self.array[i][j]
                self.array[i][j] = ''         
    
    def gemsFall(self):        
        while True :
            maxpos = self.maxPositions()
            for i in range(len(self.array)-2,-1,-1) :
                for j in range(1,len(self.array[0])) :
                    if isinstance(self.array[i][j],Gem) and not self.array[i][j].getSuperGem() and self.array[i+1][j]=='':
                        g = self.array[i][j]
                        self.array[i][j] = ''
                        self.array[self.fallGem(i,j)][j] = g         
            listInit = sorted([(super.x, super.y ,super) for super in self.listSuperGems],reverse= True)
                        
            self.listSuperGems = [elt[2] for elt in listInit]
            for super in self.listSuperGems :
                if super.x + super.h  != len(self.array) :
                    idxinit = super.x
                    idxfin = self.fallSuper(super)
                    if idxinit != idxfin :                
                        self.deplaceSuper(super,idxfin - idxinit)
                        super.x = idxfin
                    
            if maxpos == self.maxPositions() :
                break                  
    
    def descentRel(self,ga,gb) :
        if ga.getColor() =='0' and self.maxPositions()[ga.y-1]!=len(self.array)-1 or ga.getColor() !='0':
            self.array[self.maxPositions()[ga.y-1]][ga.y] = ga 

        if gb.getColor() =='0' and self.maxPositions()[gb.y-1]!=len(self.array)-1 or gb.getColor() !='0' :    
            self.array[self.maxPositions()[gb.y-1]][gb.y] = gb
        
    
    def descentGems(self,g1,g2) :
        if g1.x>g2.x :
            self.descentRel(g1,g2)
        else  :
            self.descentRel(g2,g1)
    
    # move horizontally and verically a pair of gems
    def movesDuoGems (self,colors,moves) :        
        duoCol = colors
        g1 = Gem(duoCol[0])
        g2 = Gem(duoCol[1])
        edge = len(self.array [0])-1
        depart = 4
        # beginning positions
        g1.x, g1.y = 1, depart
        g2.x, g2.y = 2, depart
        
         # displacements before descent 
        for move in moves:
            if move in 'LR' : 
                val = 1 if move == 'R' else -1 
                if 1<= g1.y + val <=edge and 1<= g2.y + val <=edge :
                    g1.y, g2.y = g1.y + val, g2.y + val                                   

            if move in 'AB' :                 
                dX,dY = g2.x - g1.x, g2.y - g1.y
                rotdX, rotdY = self.dictrotR[(dX,dY)] if move == 'B' else self.dictrotA[(dX,dY)] 
                # translate gems before rotation to stay in the limits 
                if g2.y+rotdY == edge + 1 :
                    g1.y, g2.y, g2.x = edge-1, edge, 5
                elif g2.y+rotdY == 0 :   
                    g1.y, g2.y, g2.x = 2, 1, 1
                # apply rotation
                g2.x ,g2.y = g1.x+rotdX,g1.y+rotdY
        # if an existing gem too high, stop here
        if g1.x == g2.x :
            if (self.array[0][g1.y]!= '' or self.array[0][g2.y]!= '') :            
                return False        
        else :
            if self.array[1][g1.y]!='':
                #print('issue')
                return False
        
        # else  :descent till floor or other gem
        self.descentGems(g1,g2)            
        return True

        
    def printArray(self)  :
        for i in range(len(self.array)) :
            print(' '*(i<10)+str(i),end = '.')
            for j in range(1,len(self.array[0])) :
                elt = ' '
                if isinstance(self.array[i][j],Gem):
                    elt = self.array[i][j].getColor()            
                print(elt,end = '.')
            print()
            
    def printArrayFinal(self)  :
        msg = ''
        for i in range(len(self.array)) :
            
            for j in range(1,len(self.array[0])) :
                elt = ' '
                if isinstance(self.array[i][j],Gem):
                    elt = self.array[i][j].getColor()            
                msg +=elt
            msg+='\n'
            
        return msg[:-1]
    
    # search for gems not in a supergem
    def contentCase (self,x,y)  :
        if isinstance(self.array[x][y],Gem) and not self.array[x][y].getSuperGem():
            return self.array[x][y].getColor()
        else :
            return ''
    
    def exploreCases(self,i,j):
        h, w = 2, 2
        # test of   2*2  clusters
        colorsquare = [self.contentCase (k,l) for k in range(i,i+h) for l in range(j,j+w)]
        
        if not(colorsquare[0]!='' and colorsquare[0] in 'BRGY'and colorsquare.count(colorsquare[0])==h*w):
            return 0,0
        # possible horiz extension
        while j+w <=len(self.array[0])-1 : 
            w+=1
            colorsquare = [self.contentCase (k,l) for k in range(i,i+h) for l in range(j,j+w)]                   
            if colorsquare.count(colorsquare[0])!=h*w :
                w-=1
                break           

        # possible vert extension
        while i+h <=len(self.array)-1 :
            h+=1
            colorsquare = [self.contentCase (k,l) for k in range(i,i+h) for l in range(j,j+w)]

            if colorsquare.count(colorsquare[0])!=h*w :
                h-=1
                break  
        # status changed to supergems
        [self.array[k][l].setSuperGem() for k in range(i,i+h) for l in range(j,j+w)]
        return h,w
        
    def addSupergems(self) :

        # explore the array to see supergem mini 2*2 
        # by using a 2*2 filter 
        # then maximise width and height

        for i in range(len(self.array)-1) :     
            for j in range(1,len(self.array[0])-1) :
                res = self.exploreCases(i,j)
                if res!= (0,0) :                    
                    self.listSuperGems.append((SuperGem((i,j),res)))                    
                    
    def modifySupergems(self) :
        # after supergems creation , search for consolidations
         
        for super in self.listSuperGems :
            # explore above , left, right, under if alone gems along the side
            x, y = super.x, super.y 
            h, w = super.h, super.w            
            color = self.array[x][y].getColor()
            
            while x>0 :
                colorsquare = [self.contentCase (k,l) for k in range(x-1,x) for l in range(y,y+w) 
                               if self.contentCase (k,l) ==color]
                if len(colorsquare) == w :     
                    super.x -=1
                    x = super.x
                    super.h +=1
                    h = super.h
                else :
                    break
            while y>1 :
                colorsquare = [self.contentCase (k,l) for k in range(x,x+h) for l in range(y-1,y) 
                               if self.contentCase (k,l) ==color]                
                if len(colorsquare) == h :                   
                    super.y -=1
                    y= super.y
                    super.w +=1
                    w = super.w                     
                else :
                    break            
            while y+w<len(self.array[0]):
                colorsquare = [self.contentCase (k,l) for k in range(x,x+h) for l in range(y+w,y+w+1) 
                               if self.contentCase (k,l) ==color]
                if len(colorsquare) == h :                    
                    super.w +=1
                    w = super.w
                else :
                    break  
            while x+h< len(self.array):
                colorsquare = [self.contentCase (k,l) for k in range(x+h,x+h+1) for l in range(y,y+w) 
                               if self.contentCase (k,l) ==color]
                if len(colorsquare) == w :                    
                    super.h +=1
                    h = super.h
                else :
                    break 
            
            [self.array[k][l].setSuperGem() for k in range(super.x,super.x+super.h) for l in range(super.y,super.y+super.w)]
            
        # after agglomerations , possible fusions to check        
        if not self.listSuperGems :
            pass
        while True :
            l = len(self.listSuperGems)        
            listInit = sorted([(super.x, super.y, super.h, super.w, self.array[super.x][super.y].getColor() ,super) for super in self.listSuperGems])  
            listCurrent = []
            while listInit :
                elt1 = listInit.pop(0)
                listCurrent.append(elt1)
                x1,y1,h1,w1,c1,super1 = elt1
                for elt2 in listInit :
                    x2,y2,h2,w2,c2,super2 = elt2
                    if c1 == c2 :
                        if x1 == x2 and y2 == y1+w1  and h1 == h2 :
                            super1.w1 = w1 +w2                             
                            listInit.pop(0)
                            break
                        elif y1 == y2 and x2 == x1+h1  and w1 == w2 :
                            super1.h1 = h1 +h2 
                            listInit.pop(0)                            
                            break
            self.listSuperGems = [elt [5] for elt in listCurrent]              
            if l == len(self.listSuperGems):
                break       
 
    def searchBombs(self) :        
        return [(i,j) for i in range(len(self.array)) for j in range(1,len(self.array[0])) 
                          if isinstance(self.array[i][j],Gem) and self.array[i][j].getColor() in 'bgry' ]
        
    def explodeColouredBombs(self) :        
        for bomb in self.searchBombs():           
            x,y = bomb
            if self.array[x][y] != '':
                newConnected = [bomb]                             
                color = self.array[x][y].getColor().upper()
                connected = []
                while newConnected :
                    root = newConnected.pop(0)
                    connected.append(root)
                    x,y = root
                    for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)] :
                        if 0<=x+dx<len(self.array) and 0<=y+dy<len(self.array[0]):
                            if isinstance(self.array[x+dx][y+dy],Gem) and self.array[x+dx][y+dy].getColor().upper() ==color :
                                if (x+dx,y+dy) not in connected  and (x+dx,y+dy) not in newConnected :
                                    newConnected. append((x+dx,y+dy))
                if len(connected)>1 :
                    for  x,y in connected :
                        self.array[x][y] = ''
                    self.cleanSuperGems()

    def cleanSuperGems(self) : 
        for i  in range(len(self.listSuperGems)-1,-1,-1):
            super = self.listSuperGems[i]
            if self.array[super.x][super.y] =='':
                self.listSuperGems.pop(i)
            
    def explodeRainbowBombs(self):
        # suppose no RainbowBombs on floor 
        listRainbowBombs = [(i,j) for i in range(len(self.array)-1) for j in range(1,len(self.array[0])) 
                          if isinstance(self.array[i][j],Gem) and self.array[i][j].getColor() =='0' ]
        
        colorsToDestroy = []
        for bomb in listRainbowBombs :
            (x,y) = bomb
            colorsToDestroy.append(self.array[x+1][y].getColor().upper())
            self.array[x][y] = ''
        colorsToDestroy = list(set(colorsToDestroy))
        
        while colorsToDestroy :
            color = colorsToDestroy.pop(0)
            for i in range(len(self.array)):
                for j in range(1,len(self.array[0])) :
                    if isinstance(self.array[i][j],Gem) and self.array[i][j].getColor().upper() == color:
                        self.array[i][j] = ''
            
        self.cleanSuperGems() 
    
    def explodeGems(self) :
        self.explodeRainbowBombs() 
        bomb = len(self.searchBombs())
        if  bomb == 0 :
            return         
        self.explodeColouredBombs()
        
def puzzle_fighter(ar):
    game = Game(ar,12,6)
    return game.playGame()
  
#################################################
class Gem () :
    def __init__(self,color) :
        self.color = color
        self.belongSuperGem =  False
        
    def getColor(self) :
        return self.color
    
    def getSuperGem(self):
        return self.belongSuperGem 
    
    def setSuperGem(self):
        self.belongSuperGem =  True 
       
class SuperGem() : 
    
    def __init__(self,sup,dim):
        self.x, self.y = sup
        self.h, self.w = dim
     
    def canMoveDown(self):
        # check if all the cases under the supergem are empty and can move the gems of the supergem
        
        # iteration
        pass
       
    
class Game() :
    
    def __init__(self,ar,lines,columns) :
        self.dictrotA = {(1,0):(0,1), (0,1): (-1,0),(-1,0):(0,-1),(0,-1):(1,0) }
        self.dictrotR = {v:k for k,v in self.dictrotA.items()}   
        self.array = [['' for j in range(columns+1)]for i in range(lines)] 
        self.ar = ar
        self.listSuperGems = []
        
    def playGame(self) :
        print(self.ar)
        for colors,moves in self.ar :
            #print('*'*20)
            #print(colors,moves)
            # along the list and if the gem can fall in the array 
            # vertical displacement to the lowest position
            if not self.movesDuoGems (colors,moves) :
                break 
            
            #print('apres chute')
            #self.printArray() 
            #print('*********************')
            maxpos = self.maxPositions()
            # creation des supergems  suivant priorité de creation et d'expansion , 
            self.addSupergems()
            #print('apres add supergems')
            #print(self.listSuperGems)
            while True :
                maxpos = self.maxPositions()
                
                # modification des supergems  suivant priorité de creation et d'expansion , 
                self.modifySupergems()
                
                #explosion des pieces si possible (contact ou rainbow)
                # si explosion : pieces en l'air tombent ,  sauf gems bloqués et on reboucle jusqu'à stabilisation
                
                self.explodeGems()
                #print('apres explode')
                #self.printArray()
                # chute des pieces en suspens : gerer les supergems
                self.gemsFall()
                #print('apres fall')
                #self.printArray()
                
                # cree les supergems nouvelles  apres la chute      
                self.addSupergems()
                #print('apres nvx supergems')
                #self.printArray()
                
                # mesure des mouvements
                if sum([a-b for a, b in zip(maxpos, self.maxPositions()) ])==0 :
                    break
                          

        return self.printArrayFinal()         
          
        #print()
    def maxPositions (self) :
        maxPos = []
        for j in range(1,len(self.array[0])) :
            for i in range(len(self.array)) :
                if self.array[i] [j] !='' :
                    i-=1
                    break 
            maxPos.append(i)
        return maxPos
    
    def fallGem(self,x,y):
        i = x+1
        while i+1<= len(self.array) and self.array[i][y] == '':
            #print('deplace ',x,y,'de',i)
            i+=1
        return i-1
     
    def fallSuper(self, super):
        beg = super.x + super.h
        #print('beg',beg -  super.h ,  super.y,super.h,super.w)
        i = 0
        while i+beg < len(self.array)  and len([self.array[beg+i][j] for j in range(super.y, super.y+super.w) if self.array[beg+i][j]=='' ])==super.w :
            i+=1
        #print ('beg after ', beg -super.h +i )
        return beg -super.h +i 
    
    #   a corriger 
    def deplaceSuper(self,super,delta) :
        for i in range(super.x+super.h-1,super.x-1,-1) :
            for j in range(super.y, super.y + super.w):
                self.array[i+delta][j] = self.array[i][j]
                self.array[i][j] = ''
         
    
    def gemsFall(self):
        # ne traite que les gems individuelles , il faut gerer les deplacements supergems
        
        
        
        while True :
            maxpos = self.maxPositions()
            for i in range(len(self.array)-2,-1,-1) :
                for j in range(1,len(self.array[0])) :
                    if isinstance(self.array[i][j],Gem) and not self.array[i][j].getSuperGem() and self.array[i+1][j]=='':
                        g = self.array[i][j]
                        self.array[i][j] = ''
                        self.array[self.fallGem(i,j)][j] = g
         
            listInit = sorted([(super.x, super.y ,super) for super in self.listSuperGems],reverse= True)
                        
            self.listSuperGems = [elt[2] for elt in listInit]
            for super in self.listSuperGems :
                if super.x + super.h  != len(self.array) :
                    idxinit = super.x
                    idxfin = self.fallSuper(super)
                    if idxinit != idxfin :                
                        self.deplaceSuper(super,idxfin - idxinit)
                        super.x = idxfin
                    
            if maxpos == self.maxPositions() :
                break
                  
    
    def descentRel(self,ga,gb) :
        if ga.getColor() =='0' and self.maxPositions()[ga.y-1]!=len(self.array)-1 or ga.getColor() !='0':
            self.array[self.maxPositions()[ga.y-1]][ga.y] = ga 

        if gb.getColor() =='0' and self.maxPositions()[gb.y-1]!=len(self.array)-1 or gb.getColor() !='0' :    
        
            self.array[self.maxPositions()[gb.y-1]][gb.y] = gb
     
        
    
    def descentGems(self,g1,g2) :
        if g1.x>g2.x :
            self.descentRel(g1,g2)
        else  :
            self.descentRel(g2,g1)
    
    # move horizontally and verically a pair of gems
    def movesDuoGems (self,colors,moves) :        
        duoCol = colors
        g1 = Gem(duoCol[0])
        g2 = Gem(duoCol[1])
        edge = len(self.array [0])-1
        depart = 4
        # beginning positions
        g1.x, g1.y = 1, depart
        g2.x, g2.y = 2, depart
        
         # displacements before descent 
        for move in moves:
            if move in 'LR' : 
                val = 1 if move == 'R' else -1 
                if 1<= g1.y + val <=edge and 1<= g2.y + val <=edge :
                    g1.y, g2.y = g1.y + val, g2.y + val                                   

            if move in 'AB' :                 
                dX,dY = g2.x - g1.x, g2.y - g1.y
                rotdX, rotdY = self.dictrotR[(dX,dY)] if move == 'B' else self.dictrotA[(dX,dY)] 
                # translate gems before rotation to stay in the limits 
                if g2.y+rotdY == edge + 1 :
                    g1.y, g2.y, g2.x = edge-1, edge, 5
                elif g2.y+rotdY == 0 :   
                    g1.y, g2.y, g2.x = 2, 1, 1
                # apply rotation
                g2.x ,g2.y = g1.x+rotdX,g1.y+rotdY
        # if an existing gem too high, stop here
        if g1.x == g2.x :
            if (self.array[0][g1.y]!= '' or self.array[0][g2.y]!= '') :            
                return False        
        else :
            if self.array[1][g1.y]!='':
                #print('issue')
                return False
        
        # else  :descent till floor or other gem
        self.descentGems(g1,g2)
            
        return True

        
    def printArray(self)  :
        for i in range(len(self.array)) :
            print(' '*(i<10)+str(i),end = '.')
            for j in range(1,len(self.array[0])) :
                elt = ' '
                if isinstance(self.array[i][j],Gem):
                    elt = self.array[i][j].getColor()            
                print(elt,end = '.')
            print()
            
    def printArrayFinal(self)  :
        msg = ''
        for i in range(len(self.array)) :
            
            for j in range(1,len(self.array[0])) :
                elt = ' '
                if isinstance(self.array[i][j],Gem):
                    elt = self.array[i][j].getColor()            
                msg +=elt
            msg+='\n'
            
        return msg[:-1]
    
    # search for gems not in a supergem
    def contentCase (self,x,y)  :
        if isinstance(self.array[x][y],Gem) and not self.array[x][y].getSuperGem():
            return self.array[x][y].getColor()
        else :
            return ''
    
    def exploreCases(self,i,j):

        h, w = 2, 2
        # test des cases  2*2  de meme couleur
        colorsquare = [self.contentCase (k,l) for k in range(i,i+h) for l in range(j,j+w)]
        
        if not(colorsquare[0]!='' and colorsquare[0] in 'BRGY'and colorsquare.count(colorsquare[0])==h*w):
            return 0,0
        ##print('extremites ' , (i,j), (i+h-1, j+w-1) )
        # possible horiz extension
        while j+w <=len(self.array[0])-1 : 
            ##print('w',w,'tested maxj',j+w)
            w+=1
            colorsquare = [self.contentCase (k,l) for k in range(i,i+h) for l in range(j,j+w)]                   
            if colorsquare.count(colorsquare[0])!=h*w :
                ##print('fin du w')
                ##print(colorsquare[:w])
                ##print(colorsquare[w:])
                w-=1
                break           

        #print('w final',w)
        # possible vert extension
        while i+h <=len(self.array)-1 :
            ##print('h',h,'tested maxi',i+h )
            h+=1
            colorsquare = [self.contentCase (k,l) for k in range(i,i+h) for l in range(j,j+w)]

            if colorsquare.count(colorsquare[0])!=h*w :
                ##print('fin du h')
                ##print(colorsquare[:w])
                ##print(colorsquare[w:2*w])
                ##print(colorsquare[2*w:])
                h-=1
                break  
        # status changed to supergems
        [self.array[k][l].setSuperGem() for k in range(i,i+h) for l in range(j,j+w)]
        return h,w
        
    def addSupergems(self) :

        # explore le tableau pour voir si on peut creer un supergem mini 2*2 (priorité haut bas ,horizontal)
        # en deplacant un filtre 2*2 , premiere occurence trouvee (elements non dans un supergem) 
        # maximise sa largeur , puis sa hauteur , 
        # cree un supergem qui ensuite bougera en bloc 

        for i in range(len(self.array)-1) :     
            for j in range(1,len(self.array[0])-1) :
                res = self.exploreCases(i,j)
                if res!= (0,0) :
                    
                    self.listSuperGems.append((SuperGem((i,j),res)))
                    #print('resultat' , i,j,res)
                    #print('*'*15)
                    #print(self.listSuperGems)
                    #print('*'*15)
                    
                    
    def modifySupergems(self) :
        # apres la creation des supergems , on cherche les consolidations possibles pour etendre les supergem 
        # boucle sur les supergems pour les etendre verticalement vers le haut , puis lateralement et enfin vers le bas
        # avec des gems ne faisant pas partie d'un supergem
        #print(' plateau avant modif super')
        #self.printArray()
        
        for super in self.listSuperGems :
            #print('aa',self.listSuperGems)
            # explore above , left, right, under if alone gems along the side
            x, y = super.x, super.y 
            h, w = super.h, super.w
            #self.printArray()
            #print('avant modif super', super.x,super.y,super.h,super.w)  
            
            color = self.array[x][y].getColor()
            
            while x>0 :
                colorsquare = [self.contentCase (k,l) for k in range(x-1,x) for l in range(y,y+w) 
                               if self.contentCase (k,l) ==color]
                if len(colorsquare) == w :
     
                    super.x -=1
                    x = super.x
                    super.h +=1
                    h = super.h
                    #x -=1 
                else :
                    break
            while y>1 :
                colorsquare = [self.contentCase (k,l) for k in range(x,x+h) for l in range(y-1,y) 
                               if self.contentCase (k,l) ==color]
                
                if len(colorsquare) == h :
                   
                    super.y -=1
                    y= super.y
                    super.w +=1
                    #w = super.w
                     
                else :
                    break            
            while y+w<len(self.array[0]):
                colorsquare = [self.contentCase (k,l) for k in range(x,x+h) for l in range(y+w,y+w+1) 
                               if self.contentCase (k,l) ==color]
                if len(colorsquare) == h :
                    
                    super.w +=1
                    w = super.w
                else :
                    break  
            while x+h< len(self.array):
                colorsquare = [self.contentCase (k,l) for k in range(x+h,x+h+1) for l in range(y,y+w) 
                               if self.contentCase (k,l) ==color]
                if len(colorsquare) == w :
                    
                    super.h +=1
                    h = super.h
                else :
                    break 
            
            #print('modif super', super.x,super.y,super.h,super.w)
            
            [self.array[k][l].setSuperGem() for k in range(super.x,super.x+super.h) for l in range(super.y,super.y+super.w)]
            
            #print('apres modif super', super.x,super.y,super.h,super.w) 
            #self.printArray()
        # apres les agglomerations , on regarde les fusions possibles entre supergems
        
        #print('liste super  avant:',self.listSuperGems )
        if not self.listSuperGems :
            pass
        while True :
            l = len(self.listSuperGems)
        
            listInit = sorted([(super.x, super.y, super.h, super.w, self.array[super.x][super.y].getColor() ,super) for super in self.listSuperGems])  
            listCurrent = []

            while listInit :

                elt1 = listInit.pop(0)
                listCurrent.append(elt1)
                x1,y1,h1,w1,c1,super1 = elt1
                for elt2 in listInit :
                    x2,y2,h2,w2,c2,super2 = elt2
                    if c1 == c2 :
                        if x1 == x2 and y2 == y1+w1  and h1 == h2 :
                            super1.w1 = w1 +w2 
                            
                            listInit.pop(0)
                            break
                        elif y1 == y2 and x2 == x1+h1  and w1 == w2 :
                            super1.h1 = h1 +h2 
                            listInit.pop(0)
                            
                            break
            self.listSuperGems = [elt [5] for elt in listCurrent]  
            
            if l == len(self.listSuperGems):
                break
            
        #print('liste super  apres:',self.listSuperGems )    
        
 
    def searchBombs(self) :        
        return [(i,j) for i in range(len(self.array)) for j in range(1,len(self.array[0])) 
                          if isinstance(self.array[i][j],Gem) and self.array[i][j].getColor() in 'bgry' ]
        
    def explodeColouredBombs(self) :        
        #print('explosions ?' ,self.searchBombs())
        for bomb in self.searchBombs():           
            x,y = bomb
            if self.array[x][y] != '':
                newConnected = [bomb]
                
                
                color = self.array[x][y].getColor().upper()
                connected = []
                while newConnected :
                    root = newConnected.pop(0)
                    connected.append(root)
                    x,y = root
                    for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)] :
                        if 0<=x+dx<len(self.array) and 0<=y+dy<len(self.array[0]):
                            if isinstance(self.array[x+dx][y+dy],Gem) and self.array[x+dx][y+dy].getColor().upper() ==color :
                                if (x+dx,y+dy) not in connected  and (x+dx,y+dy) not in newConnected :
                                    newConnected. append((x+dx,y+dy))
                    ##print(newConnected)
                ##print('Connected',connected) 
                if len(connected)>1 :
                    for  x,y in connected :
                        self.array[x][y] = ''
                    self.cleanSuperGems()
            #self.printArray()     
                
                    
    def cleanSuperGems(self) : 
        for i  in range(len(self.listSuperGems)-1,-1,-1):
            super = self.listSuperGems[i]
            if self.array[super.x][super.y] =='':
                self.listSuperGems.pop(i)
                    
            
    def explodeRainbowBombs(self):
        # suppose RainbowBombs on floor never explode (if not change value for i )
        listRainbowBombs = [(i,j) for i in range(len(self.array)-1) for j in range(1,len(self.array[0])) 
                          if isinstance(self.array[i][j],Gem) and self.array[i][j].getColor() =='0' ]
        
        colorsToDestroy = []
        for bomb in listRainbowBombs :
            (x,y) = bomb
            colorsToDestroy.append(self.array[x+1][y].getColor().upper())
            self.array[x][y] = ''
        colorsToDestroy = list(set(colorsToDestroy))
        
        
        while colorsToDestroy :
            color = colorsToDestroy.pop(0)
            for i in range(len(self.array)):
                for j in range(1,len(self.array[0])) :
                    if isinstance(self.array[i][j],Gem) and self.array[i][j].getColor().upper() == color:
                        self.array[i][j] = ''
            
        self.cleanSuperGems()           
            #print('superbomb')
    
    def explodeGems(self) :
        #print("explode rainbow")
        #self.printArray()
        self.explodeRainbowBombs() 
        #self.printArray()
        bomb = len(self.searchBombs())
        if  bomb == 0 :
            return
        #print("explode normal")
        #self.printArray()
        # tant qu'on a des bombs on verifie si elles ont des connectés , si connectes , bomb explode + connectes 
        
        self.explodeColouredBombs()
        #print(self.listSuperGems) 
        
def puzzle_fighter(ar):
    game = Game(ar,12,6)
    return game.playGame()
  
###########################################################
def make_new_gem(color, x, y, w=1, h=1):
    return {
        "color": color,
        "x": x,
        "y": y,
        "w": w,
        "h": h
    }

def is_single_normal_gem(gem): # Probs dont need
    return gem["w"] == 1 and gem["h"] == 1 and (gem["color"] in "RGBY")


class Board:
    def __init__(self):
        self.gems = []
        self.single_normal_mask = [[None for _ in range(6)] for _ in range(12)]
        self.gem_mask = [[None for _ in range(6)] for _ in range(12)]

    def __str__(self):
        return "\n".join("".join(self.get_string_at(x, y) for x in range(6)) for y in range(12))

    def get_string_at(self, x, y):
        color = self.get_color_at(x, y)
        if color is None:
            return " "
        else:
            return color

    def get_gem_at(self, x, y):
        for gem in self.gems:
            if gem["x"] <= x < gem["x"] + gem["w"]:
                if gem["y"] <= y < gem["y"] + gem["h"]:
                    return gem
        return None

    def is_solid(self, x, y):
        # You might be able to remove x checks here
        return self.is_gem_at(x, y) or y >= 12 or x < 0 or x >= 6

    def set_gem_mask(self, gem, value):
        for i in range(gem["w"]):
            for j in range(gem["h"]):
                self.gem_mask[gem["y"]+j][gem["x"]+i] = value
        if is_single_normal_gem(gem):
            self.single_normal_mask[gem["y"]][gem["x"]] = value

    def get_color_at(self, x, y):
        return self.gem_mask[y][x]

    def is_gem_at(self, x, y):
        if 0 <= x < 6 and 0 <= y < 12:
            return not self.gem_mask[y][x] is None
        return False

    def is_single_gem_at(self, x, y, color):
        if 0 <= x < 6 and 0 <= y < 12:
            return self.single_normal_mask[y][x] == color
        return False

    def add_to_gem_mask(self, gem):
        self.set_gem_mask(gem, gem["color"])

    def remove_from_gem_mask(self, gem):
        self.set_gem_mask(gem, None)


    def drop_gem(self, gem):
        y = gem["y"]
        while not any(self.is_solid(gem["x"]+i, y+gem["h"]) for i in range(gem["w"])):
            y += 1
        if gem["y"] == y: # Didn't fall
            return False
        self.remove_from_gem_mask(gem)
        gem["y"] = y
        self.add_to_gem_mask(gem)
        return True

    def make_and_drop_new_gem(self, color, column):
        ground = 0
        while not self.is_solid(column, ground):
            ground += 1
        new_gem = make_new_gem(color, column, ground-1)
        self.gems.append(new_gem)
        self.add_to_gem_mask(new_gem)

    def convert_singles_to_power_gem(self, color, x, y, w, h):
        # Convert an area of singles to a power gem
        self.delete_singles_in_area(x, y, w, h)
        new_gem = make_new_gem(color, x, y, w, h)
        self.gems.append(new_gem)
        self.add_to_gem_mask(new_gem)

    def delete_singles_in_area(self, x, y, w, h):
        for i in range(x, x+w):
            for j in range(y, y+h):
                gem = self.get_gem_at(i, j)
                assert(is_single_normal_gem(gem))
                self.remove_from_gem_mask(gem)
                self.gems.remove(gem)

    def merge_individual_gems(self):
        # Prioritise:
        # - Power gem with lowest y value
        # - then to the one that is widest
        possible_power_gems = {"R": [], "G": [], "B": [], "Y": []}
        
        for r_y in range(11): # Don't need to count bottom row
            for r_x in range(5): # Don't need to count last column
                color = self.single_normal_mask[r_y][r_x]
                if color and color in "RYGB":
                    is_rect = all(self.is_single_gem_at(r_x+i%2, r_y+i//2, color) for i in range(4))
                    if not is_rect:
                        continue
                    w, h = 2, 2
                    # While can expand horizontally to the right:
                    while all(self.is_single_gem_at(r_x+w, r_y+i, color) for i in range(h)):
                        w += 1
                    # While can expand vertically down:
                    while all(self.is_single_gem_at(r_x+i, r_y+h, color) for i in range(w)):
                        h += 1
                    # Convert to a power gem
                    self.convert_singles_to_power_gem(color, r_x, r_y, w, h)


    def expand_power_gems(self):
        # Prioritise:
        # - horizontal expansion
        # - vertical expansion
        # After creating a larger power gem, make sure to expand that one as well
        expanded = False
        for gem in self.gems:
            if gem["w"] != 1 or gem["h"] != 1: # Is not single
                if self.expand_gem(gem):
                    expanded = True
        if expanded:
            self.expand_power_gems()

    def expand_gem(self, gem):
        # This is another function in order to be able to call it again after expanding
        expanded = False
        w, h = gem["w"], gem["h"]
        assert(gem["w"]>=2 and gem["h"]>=2)
        # Expanding left
        if all(self.is_single_gem_at(gem["x"]-1, gem["y"]+i, gem["color"]) for i in range(gem["h"])):
            self.delete_singles_in_area(gem["x"]-1, gem["y"], 1, gem["h"])
            gem["x"] -= 1
            gem["w"] += 1
        other = self.get_gem_at(gem["x"]-1, gem["y"])
        if other:
            if other["color"] == gem["color"]:
                if other["y"] == gem["y"] and other["h"] == gem["h"]:
                    self.gems.remove(other)
                    gem["w"] += other["w"]
                    gem["x"] -= other["w"]
        # Expanding right
        if all(self.is_single_gem_at(gem["x"]+gem["w"], gem["y"]+i, gem["color"]) for i in range(gem["h"])):
            self.delete_singles_in_area(gem["x"]+gem["w"], gem["y"], 1, gem["h"])
            gem["w"] += 1
        other = self.get_gem_at(gem["x"]+gem["w"], gem["y"])
        if other:
            if other["color"] == gem["color"]:
                if other["y"] == gem["y"] and other["h"] == gem["h"]:
                    self.gems.remove(other)
                    gem["w"] += other["w"]
        # Expanding up
        if all(self.is_single_gem_at(gem["x"]+i, gem["y"]-1, gem["color"]) for i in range(gem["w"])):
            self.delete_singles_in_area(gem["x"], gem["y"]-1, gem["w"], 1)
            gem["y"] -= 1
            gem["h"] += 1
        other = self.get_gem_at(gem["x"], gem["y"]-1)
        if other:
            if other["color"] == gem["color"]:
                if other["x"] == gem["x"] and other["w"] == gem["w"]:
                    self.gems.remove(other)
                    gem["h"] += other["h"]
                    gem["y"] -= other["h"]
        # Expanding down
        if all(self.is_single_gem_at(gem["x"]+i, gem["y"]+gem["h"], gem["color"]) for i in range(gem["w"])):
            self.delete_singles_in_area(gem["x"], gem["y"]+gem["w"], gem["w"], 1)
            gem["h"] += 1
        other = self.get_gem_at(gem["x"], gem["y"]+gem["h"])
        if other:
            if other["color"] == gem["color"]:
                if other["x"] == gem["x"] and other["w"] == gem["w"]:
                    self.gems.remove(other)
                    gem["h"] += other["h"]


        expanded = gem["w"] != w or gem["h"] != h
        if expanded:
            self.add_to_gem_mask(gem)
        return expanded


    def drop_gems(self):
        # Return True if gems were dropped
        dropped_anything = False
        for gem in sorted(self.gems, reverse=True, key=lambda gem: gem["y"]+ gem["h"]):
            if self.drop_gem(gem):
                dropped_anything = True
        return dropped_anything

    def process_rainbow_gems(self):
        deleted_gems = []
        colors_deleted = []
        for gem in self.gems:
            if gem["color"] == "0":
                deleted_gems.append(gem)
                if gem["y"] == 11: # On floor
                    continue
                color = self.get_color_at(gem["x"], gem["y"]+1).upper()
                if color in "RGBY" and not color in colors_deleted:
                    colors_deleted.append(color)
                    for gem2 in self.gems:
                        if gem2["color"].upper() == color:
                            deleted_gems.append(gem2)
        for gem in deleted_gems:
            self.remove_from_gem_mask(gem)
            self.gems.remove(gem)

    def process_crash_gems(self):
        for gem in self.gems.copy():
            if gem["color"].islower(): # Is crash gem
                # Left, Right, Up, Down
                match = (gem["color"].lower(), gem["color"].upper())
                if gem["x"] > 0 and self.get_color_at(gem["x"]-1, gem["y"]) in match:
                    self.crash_remove_gem(gem)
                if gem["x"] < 5 and self.get_color_at(gem["x"]+1, gem["y"]) in match:
                    self.crash_remove_gem(gem)
                if gem["y"] > 0 and self.get_color_at(gem["x"], gem["y"]-1) in match:
                    self.crash_remove_gem(gem)
                if gem["y"] < 11 and self.get_color_at(gem["x"], gem["y"]+1) in match:
                    self.crash_remove_gem(gem)

    def crash_remove_gem(self, gem):
        x, y, w, h = gem["x"], gem["y"], gem["w"], gem["h"]
        self.remove_from_gem_mask(gem)
        self.gems.remove(gem)
        adj = []
        adj.extend((x-1, y+i) for i in range(h)) # Left
        adj.extend((x+w, y+i) for i in range(h)) # Right
        adj.extend((x+i, y-1) for i in range(w)) # Top
        adj.extend((x+i, y+h) for i in range(w)) # Bottom
        for a_x, a_y in adj:
            a_gem = self.get_gem_at(a_x, a_y)
            if a_gem and a_gem["color"].upper() == gem["color"].upper():
                self.crash_remove_gem(a_gem)



def puzzle_fighter(ar):
    #ar is array of (gem pair, instructions)
    #gem pair: can contain R, G, B, Y, r, g, b, y, 0
    # moves: L , R, A (counter-clockwise), B (clockwise)
    board = Board()
    for move in ar:
        new_gem_pair = get_moved_new_gem_pair(move)
        if not can_drop(board, new_gem_pair):
            return str(board)
        for color, column in new_gem_pair:
            board.make_and_drop_new_gem(color, column)
        # power gem merging, crash and rainbow gems
        board.merge_individual_gems()
        board.expand_power_gems()
        board.process_rainbow_gems()
        board.process_crash_gems()
        while board.drop_gems():
            board.merge_individual_gems()
            board.expand_power_gems()
            #board.process_rainbow_gems()
            board.process_crash_gems()
        # process_effects() 
        # while gems_in_air():
        #   drop_gems()
        #   board.merge_individual_gems()
        #   board.merge_power_gems()
        #   process_effects()
    return str(board)


def get_moved_new_gem_pair(move):
    # move is (gem_pair, instruction_string_chain)
    colors, instructions = move
    col = 3
    orientation = 2 # Orientation of second gem relative to first
    # 0 = up, 1 = right, 2 = down, 3 = left

    for action in instructions:
        if action == "L":
            col -= 1
        if action == "R":
            col += 1
        if action == "B": #clockwise
            orientation = (orientation + 1) % 4
        if action == "A": #anti-clockwise
            orientation = (orientation - 1) % 4
        if orientation in (0, 2):
            col = min(max(0, col), 5)
        if orientation == 3:
            col = min(max(1, col), 5)
        if orientation == 1:
            col = min(max(0, col), 4)
    if orientation == 0:
        return ((colors[0], col), (colors[1], col))
    if orientation == 1:
        return ((colors[0], col), (colors[1], col+1))
    if orientation == 2:
        # Reversed since second gem is below first, therefore it falls first 
        return ((colors[1], col), (colors[0], col))
    if orientation == 3:
        return ((colors[0], col), (colors[1], col-1))
    # Return ((color1, column1), (color2, column2)) after moving

def can_drop(board, gem_pair):
    # Return True if you can drop it i.e. if there is space for it
    # If in same column
    if gem_pair[0][1] == gem_pair[1][1]:
        if board.is_solid(gem_pair[0][1], 1):
            return False
    else: # On different columns
        if board.is_solid(gem_pair[0][1], 0):
            return False
        if board.is_solid(gem_pair[1][1], 0):
            return False
    return True
  
################################################################
def puzzle_fighter(ar):
    iteration = 0
    nextMove = True
    gameGrid = {}
    for x in range(12):
        for y in range(6):
            gameGrid[x,y] = " "
    for step in ar:
        block, moves = step
        if nextMove == True:
            iteration += 1
            gameGrid, nextMove = turn(gameGrid,block,moves)
        else:
            break
                
    string=""
    for x in range(12):
        for y in range(6):
            if len(gameGrid[x,y]) > 1:
                string += gameGrid[x,y][-1]
            else:
                string += gameGrid[x,y]
        string += "\n"
    return string[:-1]

        
        

def turn(gameGrid,block,moves):
    rotates  = [[0,1],[-1,0],[0,-1],[1,0]]
    x,y = 0, 3
    x1,y1 = 1, 3
    
    for move in moves:
        if move == "L":
            if 0 <= (y - 1) < 6 and 0 <= (y1 - 1) < 6:
                y -= 1
                y1 -= 1
        
        elif move == "R":
            if 0 <= (y + 1) < 6 and 0 <= (y1 + 1) < 6:
                y += 1
                y1 += 1
        
        elif move == "A":
            for index,[xPos,yPos] in enumerate(rotates):
                if x1 == x+xPos and y1 == y+yPos:
                    xDir, yDir = rotates[(index+1)%4]
                    if 0 <= y1+yDir < 6:
                        x1 = x + xDir
                        y1 = y + yDir
                    else:
                        x1 = x
                        y1 = y
                        y -= yDir
                    break
                           
        elif move == "B":
            for index,[xPos,yPos] in enumerate(rotates[::-1]):
                if x1 == x + xPos and y1 == y + yPos:
                    xDir, yDir = rotates[::-1][(index+1)%4]
                    if 0 <= y1+yDir < 6:
                        x1 = x + xDir
                        y1 = y + yDir
                    else:
                        x1 = x
                        y1 = y
                        y -= yDir
                    break
    gameGridCopy = gameGrid.copy()
    gameGrid,nextMove = fall(gameGrid,x, y, x1, y1,block[0],block[1])
    
    if nextMove == False:
        return gameGridCopy, False
    
       
    return gameGrid, True
        

def fall(gameGrid,x,y,x1,y1,color,color1):
    for block in sorted([[x,y,color],[x1,y1,color1]], key = lambda x: x[0], reverse = True):
        chosenX, chosenY, chosenCol = block
        for num in range(13):
            if chosenX == -1:
                chosenX += 1
            try:
                if gameGrid[chosenX + num,chosenY] != " ":
                    break
            except:
                break
        
        chosenX = chosenX + num - 1
        if chosenX < 0:
            return gameGrid, False    
        
        gameGrid[chosenX,chosenY] = chosenCol

    while True:
        gameGridCopy = gameGrid.copy()
        gameGrid = pre_destroy(gameGrid)
        gameGrid = join_blocks(gameGrid)
        gameGrid = expand_blocks(gameGrid)
        while True:
            temp = gameGrid.copy()
            gameGrid = move_down_whole_board(gameGrid)
            gameGrid = pre_destroy(gameGrid)
            if gameGrid == temp:
                break
        if gameGridCopy == gameGrid:
            break

    return gameGrid, True
            

def destroy_blocks(startX,startY,color,gameGrid):
    if color != "0":
        listToDestroy = [[startX,startY]]
        visited = [[startX,startY]]
        while True:
            try:
                x, y = listToDestroy.pop(0)
            except:
                break
            for x1,y1 in (x+1,y),(x-1,y),(x,y+1),(x,y-1):
                if 0 <= x1 < 12 and 0 <= y1 < 6:
                    if color.upper() in gameGrid[x1,y1].upper() and [x1,y1] not in visited:
                        listToDestroy.append([x1,y1])
                        visited.append([x1,y1])
        if len(visited) > 1:
            for x,y in visited:
                gameGrid[x,y] = " "
    else:
        if startX == 11:
            gameGrid[startX,startY] = " "
        else:
            color = gameGrid[startX+1,startY][-1].upper()
            gameGrid[startX,startY] = " "
            for x in range(12):
                for y in range(6):
                    if gameGrid[x,y][-1].upper() == color:
                        gameGrid[x,y] = " "
    return gameGrid
                    
            
def pre_destroy(gameGrid):
    
    destructors = {}
    for x in range(12):
        for y in range(6):
            if gameGrid[x,y] in "rgby0":
                destructors[x,y] = gameGrid[x,y]
    
    for [x,y], block in destructors.items():
        if block == "0":
            gameGrid = destroy_blocks(x,y,block,gameGrid)
        else:
            for x1,y1 in (1,0),(0,-1),(0,1),(-1,0):
                if 0 <= x+x1 < 12 and 0 <= y+y1 < 6:
                    if block.upper() in gameGrid[x+x1,y+y1][-1].upper():
                        gameGrid = destroy_blocks(x,y,block.upper(),gameGrid)

                    
    return gameGrid
                    
def expand_blocks(gameGrid):        
    visited = []                    
    for x in range(12):
        for y in range(6):
            if gameGrid[x,y] not in "0rgbyRGBY ":
                x, y, x1, y1, color = gameGrid[x,y].split(",")
                x = int(x)
                y = int(y)
                x1 = int(x1)
                y1 = int(y1)
                width = y1 - y + 1
                height = x1 - x + 1
                if [x,y] in visited:
                    break
                visited.append([x,y])
                
                # LEFT
                leftDY = 0
                keepLooping = True
                while keepLooping:
                    keepLooping = False
                    k = 0
                    leftDY += 1
                    for dx in range(x,x1+1):
                        if 0 <= y-leftDY and dx < 12:
                            if color in gameGrid[dx,y-leftDY]:
                                if len(gameGrid[dx,y-leftDY]) == 1:
                                    k += 1
                                else:
                                    neX, neY, neX1, neY1, color = gameGrid[dx,y-leftDY].split(",")
                                    neX = int(neX)
                                    neY = int(neY)
                                    neX1 = int(neX1)
                                    neY1 = int(neY1)
                                    neHeight = abs(neX1 - neX) + 1
                                    neWidth =  abs(neY1 - neY) + 1
                                    if neHeight == height and neX == x:
                                        leftDY += neWidth - 1
                                        if dx == x1:
                                            leftDY += 1
                                        k = height
                                        break
                    if k >= height:
                        keepLooping = True
                        
                #RIGHT        
                rightDY = 0
                keepLooping = True
                while keepLooping:
                    keepLooping = False
                    k = 0
                    rightDY += 1
                    for dx in range(x,x1+1):
                        if y1 + rightDY < 6 and dx < 12:
                            if color in gameGrid[dx,y1 + rightDY]:
                                if len(gameGrid[dx,y1 + rightDY]) == 1:
                                    k += 1
                                else:
                                    neX, neY, neX1, neY1, color = gameGrid[dx,y1 + rightDY].split(",")
                                    neX = int(neX)
                                    neY = int(neY)
                                    neX1 = int(neX1)
                                    neY1 = int(neY1)
                                    neHeight = abs(neX1 - neX) + 1
                                    neWidth =  abs(neY1 - neY) + 1
                                    if neHeight == height and neX == x:
                                        rightDY += neWidth - 1
                                        if dx == x1:
                                            rightDY += 1
                                        k = height
                                        break
                    if k >= height:
                        keepLooping = True
                
                
                #UP
                upDX = 0
                keepLooping = True
                while keepLooping:
                    keepLooping = False
                    k = 0
                    upDX += 1
                    for dy in range(y,y1+1):
                        if 0 <= x - upDX:
                            if color in gameGrid[x - upDX,dy]:
                                if len(gameGrid[x - upDX,dy]) == 1:
                                    k += 1
                                else:
                                    neX, neY, neX1, neY1, color = gameGrid[x - upDX,dy].split(",")
                                    neX = int(neX)
                                    neY = int(neY)
                                    neX1 = int(neX1)
                                    neY1 = int(neY1)
                                    neHeight = abs(neX1 - neX) + 1
                                    neWidth =  abs(neY1 - neY) + 1
                                    if neWidth == width and neY == y:
                                        upDX += neHeight - 1
                                        if dy == y1:
                                            upDX += 1
                                        k = width
                                        break
                    if k >= width:
                        keepLooping = True
                
                
                #DOWN        
                downDX = 0
                keepLooping = True
                while keepLooping:
                    keepLooping = False
                    k = 0
                    downDX += 1
                    for dy in range(y,y1+1):
                        if x1 + downDX < 12:
                            if color in gameGrid[x1 + downDX,dy]:
                                if len(gameGrid[x1 + downDX,dy]) == 1:
                                    k += 1
                                else:
                                    neX, neY, neX1, neY1, color = gameGrid[x1 + downDX,dy].split(",")
                                    neX = int(neX)
                                    neY = int(neY)
                                    neX1 = int(neX1)
                                    neY1 = int(neY1)
                                    neHeight = abs(neX1 - neX) + 1
                                    neWidth =  abs(neY1 - neY) + 1
                                    if neWidth == width and neY == y:
                                        downDX += neHeight - 1
                                        if dy == y1:
                                            downDX += 1
                                        k = width
                                        break
                    if k >= width:
                        keepLooping = True
                        
                        
                        
                downDX = downDX - 1
                upDX = upDX - 1
                leftDY = leftDY - 1
                rightDY = rightDY - 1
                horizontalGrowth = (leftDY + rightDY) * height
                verticalGrowth = (downDX + upDX) * width
                
                if leftDY > 0 or rightDY > 0 or downDX > 0 or upDX > 0:
                    
                    if verticalGrowth > horizontalGrowth:
                        x = x - upDX
                        x1 = x1 + downDX
                        for dx in range(x,x1+1):
                            for dy in range(y,y1+1):
                                gameGrid[dx,dy] = "{},{},{},{},{}".format(x,y,x1,y1,color)

                    else:
                        y = y - leftDY
                        y1 = y1 + rightDY
                        for dx in range(x,x1+1):
                            for dy in range(y,y1+1):
                                gameGrid[dx,dy] = "{},{},{},{},{}".format(x,y,x1,y1,color)
                                
    return gameGrid
                
def join_blocks(gameGrid):
    
    for color in "RGBY":
        row = {
        0 : 0,
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
        9 : 0,
        10 : 0,
        11 : 0       
        }
        biggestRectanglePos = []
        biggestRectangleSize = 0
        for y in range(6):
            for x in range(12):
                if gameGrid[x,y] == color:
                    row[x] += 1
                else:
                    row[x] = 0
            
            maxValue = max(row.values())
            rectangleSize = 0
            pos = []
            if maxValue > 1:
                for maxWidth in range(2,maxValue+1):
                    for col,width in row.items():
                        if width >= maxWidth:
                            pos.append([col,y])
                            rectangleSize += maxWidth
                            if len(pos) > 1 and rectangleSize > biggestRectangleSize:
                                biggestRectanglePos = pos.copy()
                                biggestRectangleSize = rectangleSize
                            elif pos != biggestRectanglePos and rectangleSize == biggestRectangleSize and len(pos) > len(biggestRectanglePos):
                                biggestRectanglePos = pos.copy()
                                
                                
                        else:                            
                            pos = []
                            rectangleSize = 0
        if biggestRectangleSize > 0:
            height = len(biggestRectanglePos)
            width = int(biggestRectangleSize / height)
            startX, startY = biggestRectanglePos[0]
            startY -= width - 1
            
            endX, endY = biggestRectanglePos[-1]
            for x,y in biggestRectanglePos:
                for dy in range(width):
                    gameGrid[x,y-dy] = "{},{},{},{},{}".format(startX,startY,endX,endY,color)
                    
    return gameGrid
                        

        
def move_down_whole_board(gameGrid):
    for x in range(11,-1,-1):
        for y in range(6):
            if gameGrid[x,y] == " ":
                for x1 in range(x-1,-1,-1):
                    if gameGrid[x1,y] != " ":
                        if len(gameGrid[x1,y]) > 1:
                            startX, startY, endX, endY, color = gameGrid[x1,y].split(",")
                            startX = int(startX)
                            startY = int(startY)
                            endX = int(endX)
                            endY = int(endY)
                            height = (endX - startX)
                            fallDawn = True
                            for  dx in range(endX,x + 1):
                                for dy in range(startY,endY + 1):
                                    if 0 <= dx < 12 and 0 <= dy < 6:
                                        if gameGrid[dx,dy] != " ":
                                            if gameGrid[dx,dy] != gameGrid[x1,y]:
                                                fallDawn = False
                                                break
                            if fallDawn == True:
                                temp = gameGrid.copy()
                                for dx in range(startX,endX+1):
                                    for dy in range(startY,endY+1):
                                        gameGrid[dx,dy] = " "
                                shift = x - endX
                                for dx in range(x - height,x+1):
                                    for dy in range(startY,endY+1):
                                        gameGrid[dx,dy] = "{},{},{},{},{}".format(startX + shift, startY, endX + shift , endY,color)
                            break
                                
                                
                        else:
                            gameGrid[x,y] = gameGrid[x1,y]
                            gameGrid[x1,y] = " "
                            break
                
    
    
    return gameGrid
    
