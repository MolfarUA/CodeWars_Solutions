from copy import deepcopy

class Go:
    
    MOVES    = [(1,0), (-1,0), (0,1), (0,-1)]
    SYMBOLS  = "xo"
    HANDICAP = {( 9, 9): ['7G',  '3C', '3G', '7C',  '5E'],
                (13,13): ['10K', '4D', '4K', '10D', '7G',  '7D',  '7K',  '10G', '4G'],
                (19,19): ['16Q', '4D', '4Q', '16D', '10K', '10D', '10Q', '16K', '4K']}
                
    def __init__(self, *args):
        if not all(0 < v < 26 for v in args): raise ValueError("This is sooooo wrong... :p")
        args = args*2
        self.lenX, self.lenY = args[:2][:]
        self.pos  = {str(i) + chr(65+j + (j>=8)): (args[0]-i,j) for i in range(1, args[0]+1) for j in range(args[1])}
        self.p, self.archive, self.board, self.hasHandi = self.initializer(*args)
        
    
    @property
    def size(self):               return {z:v for z,v in zip(["height","width"], (self.lenX, self.lenY))}
    @property
    def turn(self):               return "white" if self.p else "black"
    
    def initializer(self, *args): return 0, [], [['.']* args[1] for _ in range(args[0])], False
    def reset(self):              self.p, self.archive, self.board, self.hasHandi = self.initializer(self.lenX, self.lenY)
    
    def get_position(self, pos):  x,y = self.pos[pos] ; return self.board[x][y]                       # raise an exception if invalid position
    def updatePlayer(self):       self.p ^= 1
    
    def pass_turn(self):
        self.archive.append(deepcopy(self.board))
        self.updatePlayer()
    
    def rollback(self, n=1):
        for _ in range(n):
            self.board = self.archive.pop()
            self.updatePlayer()
    
    def rollInvalidMove_Raise(self, msg):
        self.rollback()
        self.updatePlayer()                                                                          # Restore current player if invalid move
        raise ValueError(msg)
      
      
    def handicap_stones(self, n):
        if self.hasHandi or self.archive or self.p:  raise ValueError("No, I wont...")
        self.hasHandi = True
        
        pos = iter(self.HANDICAP[(self.lenX, self.lenY)])                                            # raise an exception if invalid size of the board
        for _ in range(n):
            x,y = self.pos[next(pos)]                                                                # raise an exception of too many number of handicap stones asked for
            self.board[x][y] = self.SYMBOLS[self.p]
        
    
    def move(self, *moves):
        
        for m in moves:
            
            self.archive.append(deepcopy(self.board))                                                # Archive for rollback
            
            x,y = self.pos.get(m, (-1,-1))
            if (x,y) == (-1,-1) or self.board[x][y] != '.':
                self.rollInvalidMove_Raise(["Reproduction of stones does not work... (at {})".format(m),
                                            "Play in the board, damn you!!"][ (x,y)==(-1,-1) ])
            
            player, opp      = self.SYMBOLS[::(-1)**(2 ** self.p^1)]                                 # Retrieve player and opponent symbols
            self.board[x][y] = player                                                                # Update the board
            
            around = [(x+dx, y+dy) for dx,dy in self.MOVES 
                                   if 0 <= x+dx < self.lenX and 0 <= y+dy < self.lenY
                                   and self.board[x+dx][y+dy] != '.']
            
            grpsAround = {player: [], opp: []}                                                       # {"x": list of tuples [(set of (x,y), liberty count), ...], "o": ...}
            for a,b in around + [(x,y)]:                                                             # Extract all the groups (opponent AND player) around the concerned position: (sets of positions, liberties count), as many lists of tuples that there are groups of stones
                c = self.board[a][b]
                if not any((a,b) in neighGrp for neighGrp in grpsAround[c]):                         # Update the groups and lib value only if the current seed position is not already in a previously found group
                    grpsAround[c].append( self.floodLib(a,b,c) )
            
            isSuicidal  = grpsAround[player][0][1] == 0
            isCapturing = any(lib == 0 for _,lib in grpsAround[opp])
            if isSuicidal and not isCapturing:                                                       # Forbid self-capturing (suicide)
                self.rollInvalidMove_Raise("You definitely have suicidal tendances")
            
            for grp,lib in grpsAround[opp]:
                if lib == 0:                                                                         # Handle captures of opponent's stones
                    for a,b in grp: self.board[a][b] = '.'                                           # Remove opponent's stone
                        
                    if len(grp) == 1 and len(self.archive)>2 and self.board == self.archive[-2]:     # Check for KO rule
                        self.rollInvalidMove_Raise("You're knocked out! Again!")
            
            self.updatePlayer()                                                                      # Change the current player
            
            
    def floodLib(self, x, y, c):                                                                     # Floof-fill the board, retrieving all the pieces of the same group and counting its liberties at the same time
        pos = (x,y)
        seens, q, grp, lib = {pos}, {pos}, {pos}, 0
        while q:
            x,y = q.pop()
            for dx,dy in self.MOVES:
                a,b = pos = x+dx, y+dy
                if 0 <= a < self.lenX and 0 <= b < self.lenY and pos not in seens:
                    if   self.board[a][b] == '.': lib += 1
                    elif self.board[a][b] == c:   grp.add(pos) ; q.add(pos)
                    seens.add(pos)
        return grp, lib
        
############################
class Go:
    
    def __init__(self,h,w=0):
        self.tt=["black","white"]
        if w==0:w=h
        if w>25 or h>25:
            raise NameError('Inavlid Size')
        self.board=[["."]*w for i in range(h)]
        self.nmoves=0
        self.turn =self.tt[self.nmoves%2]
        self.p=['x','o']
        self.bh=[]
        self.add_hist()
        self.size={'height':h,'width':w}
        self.hc=False
        
    def add_hist(self):
        self.bh.append( [row[:] for row in self.board])
        
    def move(self,*args):
        for arg in args:
            y,x=self. yx(arg)
            if self.board[y][x]=='.':
                self.board[y][x]=self.p[self.nmoves%2]
                self.check_capture(y,x)
                if not self.check_self_capture(y,x) and not self.check_KO():
                    self.nmoves+=1
                    self.turn=self.tt[self.nmoves%2]
                    self.add_hist()
                    continue
                else:
                    self.board = [row [:] for row in self.bh[-1]]
            raise NameError('Invalid move')
    
    def pass_turn(self):
        self.nmoves+=1
        self.turn=self.tt[self.nmoves%2]
        self.add_hist()
        
    def reset(self):
        self.__init__(len(self.board),len(self.board[0]))
        
    def handicap_stones(self,n):
        hs={9:[(2,6),(6,2),(6,6),(2,2),(4,4)], 13:[(3,9),(9,3),(9,9),(3,3),(6,6),(6,3),(6,9),(3,6),(9,6)],
            19:[(3,15),(15,3),(15,15),(3,3),(9,9),(9,3),(9,15),(3,9),(15,9)] }
        
        if self.hc or len(self.board)!=len(self.board[0]) or len(self.board) not in hs or self.nmoves>0 or len(hs[len(self.board)])<n:
            raise ErrorName('Ivalid Move')
        else:
            for i in range(n):
                y,x = hs[len(self.board)][i]
                self.board[y][x]='x'
            self.add_hist()
            self.hc=True
    
    def rollback(self,nt):
        if nt<len(self.bh):
            for i in range(nt):
                self.bh.pop()
            self.board = [row[:] for row in self.bh[-1]]
            self.nmoves-=nt
            self.turn=self.tt[self.nmoves%2]
        else:
            raise ErrorName('Invalid Move')
        
    def get_position(self,pos):
        y,x=self.yx(pos)
        return self.board[y][x]
    
    def check_KO(self):
        if len(self.bh)<2: return False
        return self.bh[-2] ==self.board
    
    def check_capture(self, y,x):
        cp="o"; ap=self.board[y][x]
        if ap==cp: cp="x"
        for y1,x1 in self.nei(y,x):
            if self.board[y1][x1]==cp:
                con=self.is_capture(y1,x1)
                for y2,x2 in con:
                    self.board[y2][x2]='.'

    def check_self_capture(self,y,x):
        con = self.is_capture(y,x)
        if len(con)>0:
            return True
        return False
        
    def is_capture(self,y,x):
        res=[(y,x)]
        check=[(y,x)]
        cp=self.board[y][x]
        while len(check)>0:
            y1,x1=check.pop()
            for y2,x2 in self.nei(y1,x1):
                if self.board[y2][x2]==".":return []
                if self.board[y2][x2]==cp and not ((y2,x2) in res) and not ((y2,x2) in check):
                    res.append((y2,x2))
                    check.append((y2,x2))
        return res
                    
    def nei(self,y,x):
        res=[]
        for dy,dx in [(1,0),(-1,0),(0,-1),(0,1)]:
            y1=y+dy
            if y1<0 or y1>=len(self.board): continue
            x1=x+dx
            if x1<0 or x1>=len(self.board[y1]) : continue
            res.append((y1,x1))
        return res
    
    def yx(self,s):
        y=len(self.board)-int(s[:-1])
        x=ord(s[-1])-ord('A')
        if s[-1]>"I": x-=1
        return (y,x)
      
#####################
from itertools import chain


class Group:
    def __init__(self, firststone, groupID, liberties, color):
        self.member = {firststone}
        self.groupID = groupID
        self.liberties = set(liberties)  # set of positions
        self.color = color

    def merge(self, *others):
        """:param others: iterable of Group instances"""
        self.liberties.update(
            *(lib for lib in (group.liberties for group in others)))
        self.member.update((item for group in others for item in group.member))

    def __hash__(self):  # for set behaviour on values
        return self.groupID


class Go:
    def __init__(self, height, width=None):
        """https://www.codewars.com/kata/59de9f8ff703c4891900005c"""
        if width is None:
            width = height

        if height > 25 or width > 25:
            raise ValueError('max board size in any dimension is 25')

        self.size = {'height': height, 'width': width}
        self.board = [['.' for i in range(width)] for j in range(height)]
        self.history = []
        self.groups = dict()  # {groupID: Group}
        self.affiliation = dict()  # {position: groupID} ease fetching neighb.group
        self.handicap = 0
        self.capured = dict()  # {len(history at capture): captured members}

        self.parse_position = self._precompute_for_parsing()

    def __repr__(self):
        return '\n'.join(str(row) for row in self.board)

    def handicap_stones(self, stones):
        stone_pos = {9: ['7G', '3C', '3G', '7C', '5E'],
                     13: ['10K', '4D', '4K', '10D', '7G', '7D', '7K', '10G', '4G'],
                     19: ['16Q', '4D', '4Q', '16D', '10K', '10D', '10Q', '16K', '4K']}

        if list(self.size.values()) != [19, 19] and \
                list(self.size.values()) != [13, 13] and \
                list(self.size.values()) != [9, 9]:
            raise ValueError('boardsize is not suitable for handicap stones')
        elif len(stone_pos[self.size['height']]) < stones:
            raise ValueError('too many handicap stones for given boardsize')
        elif len(self.history) != 0:
            raise ValueError('game has already started or you called handicap_stones twice')
        else:
            ls = [self.parse_position(stone) for stone in stone_pos[self.size['height']][0:stones]]

            self.groups.update(
                {i: Group(firststone=pos, groupID=i, liberties=self._find_neighb(*pos), color='x')
                 for i, pos in enumerate(ls)})
            self.affiliation.update({pos: i for i, pos in enumerate(ls)})

            # white starts to play after handicap
            self.history.append('handicap')
            self.handicap = stones

            # place handicap stones
            for r, c in ls:
                self.board[r][c] = 'x'

    def move(self, *positions):
        """positions may take multiple values: move("4A", "5A", "6A")"""
        for position in positions:
            r, c = self.parse_position(position)

            if self._occupied(r, c):
                color = ['x', 'o'][len(self.history) % 2]
                self.board[r][c] = color
                neighb = self._find_neighb(r, c)

                # (0) create new group (single stone)
                groupID = len(self.history) + self.handicap
                self.groups.update({groupID: Group(
                    firststone=(r, c),
                    groupID=groupID,
                    liberties=set(n for n in neighb if n not in self.affiliation.keys()),
                    color=color)})
                self.history.append(position)
                self.affiliation.update({(r, c): groupID})

                # (1) same color (including mid stone)
                self._merge_same_color(neighb, color, groupID, r, c)

                # (2) different colored neighbours: steal liberty
                self._different_color_update(neighb, color, r, c)

                # (3) check move was no suicide
                # (notice the group above has new affil. after merger)
                if not bool(self.groups[self.affiliation[(r, c)]].liberties):
                    self.rollback(1)
                    raise ValueError('Suicide')

    def _occupied(self, r, c):
        """returns true if no stone @ the requested position pos."""
        if self.board[r][c] != '.':
            raise ValueError('cannot place a stone on top of another stone')
        return True

    def _merge_same_color(self, neighb, color, groupID, r, c):
        """merge all stones of same color in neighb. including mid stone"""
        pos_same_col = [n for n in neighb if self.board[n[0]][n[1]] == color]

        if pos_same_col != []:
            # find largest Group (a bit of extra logic for fast moves in mid/end game)
            membersize = [len(self._fetch_group(n).member) for n in pos_same_col]
            pos_max_grsize = pos_same_col[membersize.index(max(membersize))]
            pos_same_col.remove(pos_max_grsize)
            same_col_nomax = [self.groups[id] for id in [self.affiliation[n] for n in pos_same_col]]
            max_id = self.affiliation[pos_max_grsize]

            # merge to max group
            self.groups[max_id].merge(self.groups[groupID], *same_col_nomax)

            # remove mid (new) stone liberty
            self.groups[max_id].liberties.remove((r, c))

            # change the affiliation of all same colored to val of max group aff.
            for tup in (*chain(*[group.member for group in same_col_nomax]), (r, c)):
                self.affiliation[tup] = max_id

    def _different_color_update(self, neighb, color, r, c):
        """steal the liberty (of the new stone at r,c)
        of all different colored neighbours"""
        pos_diff_col = set(self._fetch_group(n) for n in neighb
                           if self.board[n[0]][n[1]] != color
                           and self.board[n[0]][n[1]] != '.')

        if pos_diff_col != []:
            for group in pos_diff_col:
                if (r, c) in group.liberties:
                    group.liberties.remove((r, c))

                # check if group has no liberties
                if not bool(group.liberties):
                    self._capture(group=group)

    def _capture(self, group):
        """remove group when it has no liberty after _different_color_update
        each member's neighbour's group must be added this members position is a
        new liberty of that neighbour's group."""
        if len(self.history) - 1 in self.capured.keys():
            if {self.parse_position(self.history[-1])} == \
                    self.capured[len(self.history) - 1] and len(group.member) == 1:
                self.rollback(1)
                raise ValueError('Ko')

        self.capured.update({len(self.history): group.member})

        # opposite color
        color = ['x', 'o']
        color.remove(group.color)
        color = color[0]

        # find neighb. of each member & give them the respective liberty!
        member_neighb = list(map(lambda position: self._find_neighb(*position), group.member))
        diff_group = [set(self._fetch_group(n) for n in neighb if self.board[n[0]][n[1]] == color)
                      for neighb in member_neighb]

        for member, ngroups in zip(group.member, diff_group):
            for ngroup in ngroups:
                ngroup.liberties.update({member})

        for i, pos in enumerate(group.member):
            # remove affiliations of all group member:
            self.affiliation.pop(pos)

            # remove member from board
            self.board[pos[0]][pos[1]] = '.'

    def _fetch_group(self, position):
        """return the instance of a group by position"""
        return self.groups[self.affiliation[position]]

    def _find_neighb(self, r, c):
        """:return list of position tuples, representing
        horizontal vertical adjacent positions"""
        cond = lambda r, c: r >= 0 and r < self.size['height'] and c >= 0 and c < self.size['width']
        neighb = [(r + i, c) for i in [-1, 1] if cond(r + i, c)]  # horizontal
        neighb.extend((r, c + j) for j in [-1, 1] if cond(r, c + j))  # vertical
        return neighb

    def _precompute_for_parsing(self):
        """decorator to precompute the indicies for parsing only once in self.__init__"""
        alpha = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        alpha.remove('I')
        hor = alpha[0:self.size['width']]
        ver = [i for i in reversed(range(self.size['height'] + 1))]

        def parse_position(move):
            if int(move[0:-1]) not in ver or move[-1] not in hor:
                raise ValueError('You are out of bounds')
            else:
                return ver[int(move[0:-1])], hor.index(move[-1])

        return parse_position

    @property
    def turn(self):
        """getter of current Turn color"""
        return ['black', 'white'][len(self.history) % 2]

    def pass_turn(self):
        """player decides not to move"""
        self.history.append('')

    def get_position(self, position):
        """:return: 'x', 'o' or '.'"""
        position = self.parse_position(position)
        i, j = position

        return self.board[i][j]

    def rollback(self, steps):
        """rollback the last game moves (by replaying the history)"""
        if len(self.history) < steps:
            raise ValueError('invalid rollback to few moves to unravel')

        history = self.history
        handicap = self.handicap

        # reinstate attributes.
        self.__init__(**self.size)

        # restore handicap
        if handicap != 0:
            self.handicap_stones(handicap)
            history = history[1:]

        for m in history[:-steps]:
            if bool(m):
                self.move(m)
            else:
                self.pass_turn()

    def reset(self):
        """remove all stones of the board"""
        self.__init__(**self.size)

#################################
from itertools import chain


class Group:
    def __init__(self, firststone, groupID, liberties, color):
        self.member = {firststone}
        self.groupID = groupID
        self.liberties = set(liberties)  # set of positions
        self.color = color

    def merge(self, *others):
        """:param others: iterable of Group instances"""
        self.liberties.update(
            *(lib for lib in (group.liberties for group in others)))
        self.member.update((item for group in others for item in group.member))

    def __hash__(self):  # for set behaviour on values
        return self.groupID


class Go:
    def __init__(self, height, width=None):
        """https://www.codewars.com/kata/59de9f8ff703c4891900005c"""
        if width is None:
            width = height

        if height > 25 or width > 25:
            raise ValueError('max board size in any dimension is 25')

        self.size = {'height': height, 'width': width}
        self.board = [['.' for i in range(width)] for j in range(height)]
        self.history = []
        self.groups = dict()  # {groupID: Group}
        self.affiliation = dict()  # {position: groupID} ease fetching neighb.group
        self.handicap = 0
        self.capured = dict()  # {len(history at capture): captured members}

    def __repr__(self):
        return '\n'.join(str(row) for row in self.board)

    def handicap_stones(self, stones):
        stone_pos = {9: ['7G', '3C', '3G', '7C', '5E'],
                     13: ['10K', '4D', '4K', '10D', '7G', '7D', '7K', '10G', '4G'],
                     19: ['16Q', '4D', '4Q', '16D', '10K', '10D', '10Q', '16K', '4K']}

        if list(self.size.values()) != [19, 19] and \
                list(self.size.values()) != [13, 13] and \
                list(self.size.values()) != [9, 9]:
            raise ValueError('boardsize is not suitable for handicap stones')
        elif len(stone_pos[self.size['height']]) < stones:
            raise ValueError('too many handicap stones for given boardsize')
        elif len(self.history) != 0:
            # TODO: replace this by _groups
            raise ValueError('game has already started or you called handicap_stones twice')
        else:
            ls = [self.parse_position(stone) for stone in stone_pos[self.size['height']][0:stones]]

            self.groups.update(
                {i: Group(firststone=pos, groupID=i, liberties=self._find_neighb(*pos), color='x')
                 for i, pos in enumerate(ls)})
            self.affiliation.update({pos: i for i, pos in enumerate(ls)})

            # white starts to play after handicap
            self.history.append('handicap')
            self.handicap = stones

            # bring black on board
            for r, c in ls:
                self.board[r][c] = 'x'

    def move(self, *positions):
        """positions may take multiple values: move("4A", "5A", "6A")"""
        for position in positions:
            r, c = self.parse_position(position)

            if self._valid_move(r, c):
                color = ['x', 'o'][len(self.history) % 2]
                self.board[r][c] = color
                neighb = self._find_neighb(r, c)

                # (0) create new group (single stone) with no affiliation
                # -1 so that it follows the logic of handicap_stones
                groupID = len(self.history) + self.handicap
                self.groups.update({groupID: Group(
                    firststone=(r, c),
                    groupID=groupID,
                    liberties=set(n for n in neighb if n not in self.affiliation.keys()),
                    color=color)})
                self.history.append(position)
                self.affiliation.update({(r, c): groupID})

                # (1) same color (including mid stone)
                self._merge_same_color(neighb, color, groupID, r, c)

                # (2) different colored neighbours: steal liberty
                self._different_color_update(neighb, color, r, c)

                # (3) check move was no suicide
                # (the group above has new affil. after merger)
                if not bool(self.groups[self.affiliation[(r, c)]].liberties):
                    self.rollback(1)
                    raise ValueError('Suicide')

    def _merge_same_color(self, neighb, color, groupID, r, c):
        pos_same_col = [n for n in neighb if self.board[n[0]][n[1]] == color]

        if pos_same_col != []:
            # find largest Group (a bit of extra logic for fast moves in mid/end game)
            membersize = [len(self._fetch_group(n).member) for n in pos_same_col]
            pos_max_grsize = pos_same_col[membersize.index(max(membersize))]
            pos_same_col.remove(pos_max_grsize)
            # update with: same_col_no_max=[self._fetch_group_by_pos(n) for n in pos_same_col]
            same_col_nomax = [self.groups[id] for id in [self.affiliation[n] for n in pos_same_col]]
            max_id = self.affiliation[pos_max_grsize]

            # merge to max group
            self.groups[max_id].merge(self.groups[groupID], *same_col_nomax)

            # remove mid (new) stone liberty
            self.groups[max_id].liberties.remove((r, c))

            # change the affiliation of all same colored to val of max group aff.
            for tup in (*chain(*[group.member for group in same_col_nomax]), (r, c)):
                self.affiliation[tup] = max_id

    def _different_color_update(self, neighb, color, r, c):
        pos_diff_col = set(self._fetch_group(n) for n in neighb
                           if self.board[n[0]][n[1]] != color
                           and self.board[n[0]][n[1]] != '.')

        if pos_diff_col != []:
            for group in pos_diff_col:
                if (r, c) in group.liberties:
                    group.liberties.remove((r, c))

                # check if group has no liberties
                if not bool(group.liberties):
                    self._capture(group=group)

    def _capture(self, group):
        """remove group when it has no liberty after _different_color_update
        each member's neighbour's group must be added this members position is a
        new liberty of that neighbour's group."""
        if len(self.history) - 1 in self.capured.keys():
            if {self.parse_position(self.history[-1])} == \
                    self.capured[len(self.history) - 1] and len(group.member) == 1:
                self.rollback(1)
                raise ValueError('Ko')

        self.capured.update({len(self.history): group.member})

        color = ['x', 'o']
        color.remove(group.color)
        color = color[0]

        # find neighb. of each member & give them the respective liberty!
        member_neighb = list(map(lambda position: self._find_neighb(*position), group.member))
        diff_group = [set(self._fetch_group(n) for n in neighb if self.board[n[0]][n[1]] == color)
                      for neighb in member_neighb]

        for member, ngroups in zip(group.member, diff_group):
            for ngroup in ngroups:
                ngroup.liberties.update({member})

        for i, pos in enumerate(group.member):
            # remove affiliations of all group member:
            self.affiliation.pop(pos)

            # remove member from board
            self.board[pos[0]][pos[1]] = '.'

    def _fetch_group(self, position):
        return self.groups[self.affiliation[position]]

    def _find_neighb(self, r, c):
        cond = lambda r, c: r >= 0 and r < self.size['height'] and c >= 0 and c < self.size['width']
        neighb = [(r + i, c) for i in [-1, 1] if cond(r + i, c)]  # horizontal
        neighb.extend((r, c + j) for j in [-1, 1] if cond(r, c + j))  # vertical
        return neighb

    def parse_position(self, move):
        # TODO: make a dict
        alpha = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        alpha.remove('I')
        hor = alpha[0:self.size['width']]
        ver = [i for i in reversed(range(self.size['height'] + 1))]

        if int(move[0:-1]) not in ver or move[-1] not in hor:
            raise ValueError('You are out of bounds')
        else:
            return ver[int(move[0:-1])], hor.index(move[-1])

    def _valid_move(self, r, c):
        #  (1) if stone already @ pos.
        if self.board[r][c] != '.':
            raise ValueError('cannot place a stone on top of another stone')
        return True

    @property
    def turn(self):
        """getter of current Turn color"""
        return ['black', 'white'][len(self.history) % 2]

    def pass_turn(self):
        """player decides not to move"""
        self.history.append('')

    def get_position(self, position):
        """:return: 'x', 'o' or '.'"""
        position = self.parse_position(position)
        i, j = position

        return self.board[i][j]

    def rollback(self, steps):
        """rollback the last game moves (by replaying the history)"""
        if len(self.history) < steps:
            raise ValueError('invalid rollback to few moves to unravel')

        history = self.history
        handicap = self.handicap

        # reinstate attributes.
        self.__init__(**self.size)

        # restore handicap
        if handicap != 0:
            self.handicap_stones(handicap)
            history = history[1:]

        for m in history[:-steps]:
            if bool(m):
                self.move(m)
            else:
                self.pass_turn()

    def reset(self):
        """remove all stones of the board"""
        self.__init__(**self.size)
        
####################################
import string
from copy import deepcopy

class Go:
    EMPTY_TOKEN = '.'
    PLAYER_TOKENS = 'xo'
    NEIGHBORS = ((0, -1), (1, 0), (0, 1), (-1, 0))
    HANDICAP = {
        (9, 9): ('7G', '3C', '3G', '7C', '5E'),
        (13, 13): ('10K', '4D', '4K', '10D', '7G', '7D', '7K', '10G', '4G'),
        (19, 19): ('16Q', '4D', '4Q', '16D', '10K', '10D', '10Q', '16K', '4K'),
    }
    
    def __init__(self, height, width = None):
        if width is None: width = height
        if not all(0 < v < 26 for v in (height, width)):
            raise Exception()
        self.height, self.width = (height, width)
        self.reset()
    
    @property
    def size(self):
        return dict(zip(('height', 'width'), (self.height, self.width)))
    
    @property
    def turn(self):
        return 'white' if self.p else 'black'
    
    def reset(self):
        self.p = 0
        self.board = [[self.EMPTY_TOKEN for _ in range(self.width)] for _ in range(self.height)]
        self.board_history = []
        self.has_handicap = False
    
    def is_valid_pos(self, pos):
        row_name, col_name = (pos[:-1], pos[-1])
        return (
            row_name.isdigit() and 1 <= int(row_name) <= self.height and
            col_name.isalpha() and col_name.isupper() and col_name != 'I'
        )
    
    def pos_to_coord(self, pos):
        row_name, col_name = (pos[:-1], pos[-1])
        return (string.ascii_uppercase.replace('I', '').index(col_name), self.height - int(row_name))
    
    def get_position(self, pos):
        if not self.is_valid_pos(pos):
            raise Exception()
        x, y = self.pos_to_coord(pos)
        return self.board[y][x]
    
    def handicap_stones(self, amount):
        if self.has_handicap or self.board_history:
            raise Exception()
        board_size = (self.height, self.width)
        if board_size not in self.HANDICAP or amount > len(self.HANDICAP[board_size]):
            raise Exception()
        for i in range(amount):
            x, y = self.pos_to_coord(self.HANDICAP[board_size][i])
            self.board[y][x] = self.PLAYER_TOKENS[self.p]
        self.has_handicap = True
    
    def switch_player(self):
        self.p ^= 1
    
    def pass_turn(self):
        self.board_history.append(deepcopy(self.board))
        self.switch_player()
    
    def rollback(self, moves):
        for _ in range(moves):
            self.board = self.board_history.pop()
            self.switch_player()
    
    def error_rollback(self):
        self.rollback(1)
        self.switch_player()
        raise Exception()
    
    def move(self, *positions):
        for pos in positions:
            self.board_history.append(deepcopy(self.board))
            
            if not self.is_valid_pos(pos):
                self.error_rollback()
            x, y = self.pos_to_coord(pos)
            if self.board[y][x] != self.EMPTY_TOKEN:
                self.error_rollback()
            
            player, opponent = self.PLAYER_TOKENS[::(-1) ** (2 ** (self.p ^ 1))]
            self.board[y][x] = player
            
            around = [(x + dx, y + dy)
                for dx, dy in self.NEIGHBORS
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height and self.board[y + dy][x + dx] != self.EMPTY_TOKEN
            ]
            groups_around = {player: [], opponent: []}
            for cx, cy in around + [(x, y)]:
                c = self.board[cy][cx]
                if not any((cx, cy) in group for group in groups_around[c]):
                    groups_around[c].append(self.collect_group((cx, cy)))
            
            is_s5e = groups_around[player][0][1] == 0
            is_capturing = any(group[1] == 0 for group in groups_around[opponent])
            if is_s5e and not is_capturing:
                self.error_rollback()
            
            for group, lib in groups_around[opponent]:
                if lib == 0:
                    for cx, cy in group:
                        self.board[cy][cx] = self.EMPTY_TOKEN
                    if len(group) == 1 and len(self.board_history) > 2 and self.board == self.board_history[-2]:
                        self.error_rollback()
            
            self.switch_player()
    
    def collect_group(self, coord):
        c = self.board[coord[1]][coord[0]]
        seen, q, group = ({coord}, {coord}, {coord})
        lib = 0
        while q:
            x, y = q.pop()
            for dx, dy in self.NEIGHBORS:
                tx, ty = pos = (x + dx, y + dy)
                if 0 <= tx < self.width and 0 <= ty < self.height and pos not in seen:
                    seen.add(pos)
                    if self.board[ty][tx] == self.EMPTY_TOKEN:
                        lib += 1
                    elif self.board[ty][tx] == c:
                        group.add(pos)
                        q.add(pos)
        return (group, lib)

################################
import string


class Player:
    def __init__(self, name, token):
        self.name, self.token = (name, token)

class Board:
    def __init__(self, height, width):
        self.height, self.width = (height, width)
    
    def __str__(self):
        return '\n'.join(map(lambda row: ''.join(map(lambda field: field or ' ', row)), self.board))
    
    @property
    def size(self):
        return (self.height, self.width)
    
    def reset(self):
        self.board = [[None for x in range(self.width)] for y in range(self.height)]
    
    def has(self, coord):
        x, y = coord
        return 0 <= y < self.height and 0 <= x < self.width
    
    def get(self, coord):
        x, y = coord
        return self.board[y][x]
    
    def set(self, coord, token):
        x, y = coord
        self.board[y][x] = token
    
    def set_from_str(self, board_str):
        for y, row_str in enumerate(board_str.split('\n')):
            for x, token in enumerate(row_str):
                self.set((x, y), None if token == ' ' else token)
    
    def remove(self, coord):
        self.set(coord, None)

class Go:
    _handicap_stones = {
        (9, 9): ((6, 2), (2, 6), (6, 6), (2, 2), (4, 4)),
        (13, 13): ((9, 3), (3, 9), (9, 9), (3, 3), (6, 6), (3, 6), (9, 6), (6, 3), (6, 9)),
        (19, 19): ((15, 3), (3, 15), (15, 15), (3, 3), (9, 9), (3, 9), (15, 9), (9, 3), (9, 15)),
    }
    
    def __init__(self, height, width = None):
        if width is None: width = height
        if height > 25 or width > 25:
            raise Exception('Board can\'t be larger than 25x25')
        self._black = Player('black', 'x')
        self._white = Player('white', 'o')
        self._board = Board(height, width)
        self.reset()
    
    def _is_valid_coord_str(self, coord_str):
        row_name, col_name = (coord_str[:-1], coord_str[-1])
        return (
            row_name.isdigit() and 1 <= int(row_name) <= self._board.height and
            col_name.isalpha() and col_name.isupper() and col_name != 'I'
        )
    
    def _coord_str_to_coord(self, coord_str):
        row_name, col_name = (coord_str[:-1], coord_str[-1])
        return (string.ascii_uppercase.replace('I', '').index(col_name), self._board.height - int(row_name))
    
    @property
    def board(self):
        return [[field or '.' for field in row] for row in self._board.board]
    
    @property
    def size(self):
        return dict(zip(('height', 'width'), self._board.size))
    
    @property
    def turn(self):
        return self._turn.name
    
    def reset(self):
        self._move = 0
        self._turn = self._black
        self._has_set_handicap_stones = False
        self._chains = []
        self._board_history = []
        self._board.reset()
        self._board_history.append(str(self._board))
    
    def handicap_stones(self, amount):
        if self._has_set_handicap_stones:
            raise Exception('Handicap stones have already been set')
        if self._move > 0:
            raise Exception('Can\'t place handicap stones after the 1st move')
        board_size = self._board.size
        if board_size not in self._handicap_stones:
            raise Exception('Unsupported board size for handicap stones')
        if amount > len(self._handicap_stones[board_size]):
            raise Exception('Unsupported amount of handicap stones for this board size')
        for i in range(amount):
            self._board.set(self._handicap_stones[board_size][i], self._turn.token)
        self._has_set_handicap_stones = True
    
    def get_position(self, coord_str):
        return self._board.get(self._coord_str_to_coord(coord_str)) or '.'
    
    def pass_turn(self):
        self._move += 1
        self._turn = self._black if self._turn == self._white else self._white
        self._board_history.append(str(self._board))
    
    def move(self, *coord_strs):
        board = self._board
        for coord_str in coord_strs:
            if not self._is_valid_coord_str(coord_str):
                raise Exception('Invalid coord string')
            coord = self._coord_str_to_coord(coord_str)
            if not board.has(coord):
                raise Exception('Coord is out of bounds')
            if board.get(coord) is not None:
                raise Exception('Field is taken already')
            
            connected_chains = []
            removed_chains = []
            for chain in self._chains.copy():
                if coord not in chain.liberties:
                    continue
                if chain.owner != self._turn:
                    if len(chain.liberties) == 1:
                        removed_chains.append(chain)
                        chain.remove_from_board()
                        self._chains.remove(chain)
                    continue
                connected_chains.append(chain)
            board.set(coord, self._turn.token)
            if not connected_chains:
                chain = Token_Chain(board, self._turn)
                chain.add(coord)
                if not chain.liberties:
                    board.remove(coord)
                    self._chains.extend(removed_chains)
                    for rchain in removed_chains:
                        rchain.add_to_board()
                    raise Exception('Invalid move')
                self._chains.append(chain)
            else:
                chain = Token_Chain(board, self._turn)
                chain.add(coord)
                chain.add_chains(connected_chains)
                if not chain.liberties:
                    board.remove(coord)
                    self._chains.extend(removed_chains)
                    for rchain in removed_chains:
                        rchain.add_to_board()
                    raise Exception('Invalid s5e move')
                for cchain in connected_chains:
                    self._chains.remove(cchain)
                self._chains.append(chain)
            
            if len(self._board_history) > 1 and str(board) == self._board_history[-2]:
                board.remove(coord)
                self._chains.extend(removed_chains)
                for rchain in removed_chains:
                    rchain.add_to_board()
                raise Exception('KO rule violation')
            
            self.pass_turn()
    
    def rollback(self, moves):
        if moves > self._move:
            raise Exception('Can\'t rollback so many moves')
        self._move -= moves
        self._board.set_from_str(self._board_history[self._move])
        del self._board_history[self._move + 1:]
        self._re_evaluate_board()
        if moves % 2 != 0:
            self._turn = self._black if self._turn == self._white else self._white
    
    def _re_evaluate_board(self):
        self._chains = []
        visited = set()
        def visit(coord, owner_token):
            if coord in visited:
                return []
            visited.add(coord)
            members = [coord]
            for d in ((1, 0), (0, 1)):
                c = (coord[0] + d[0], coord[1] + d[1])
                if self._board.has(c) and self._board.get(c) == owner_token and c not in visited:
                    members.extend(visit(c, owner_token))
            return members
        for y, row in enumerate(self._board.board):
            for x, field in enumerate(row):
                if field is not None and (x, y) not in visited:
                    members = visit((x, y), field)
                    chain = Token_Chain(self._board, self._black if field == self._black.token else self._white)
                    for coord in members:
                        chain.add(coord)
                    self._chains.append(chain)

class Token_Chain:
    def __init__(self, board, owner):
        self.board = board
        self.owner = owner
        self.members = []
    
    @property
    def liberties(self):
        return {coord for mcoord in self.members for coord in self.get_liberties(mcoord)}
    
    def add(self, coord):
        self.members.append(coord)
    
    def add_chains(self, chains):
        for chain in chains:
            for coord in chain.members:
                self.add(coord)
    
    def remove_from_board(self):
        for coord in self.members:
            self.board.remove(coord)
    
    def add_to_board(self):
        for coord in self.members:
            self.board.set(coord, self.owner.token)
    
    def get_liberties(self, coord):
        liberties = []
        for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            c = (coord[0] + d[0], coord[1] + d[1])
            if self.board.has(c) and self.board.get(c) is None:
                liberties.append(c)
        return liberties
      
#####################################
class Go:

    def __init__(self, h, w=None):
        self._s = (h, h if w == None else w)
        if self._s[0] > 25 or self._s[1] > 25:
            raise Exception("Board size invalid")
        self._t = 0
        self.pieces = (set(), set())
        self.history = []

    def move(self, *pos):
        for p in pos:
            p = self.get_pos(p)
            if (not self.in_bounds(p)) or \
               (p in self.pieces[0] or p in self.pieces[1]):
                    raise Exception("Illegal move")
            self.pieces[self._t].add(p)
            captured = self.get_captured(self._t^1)
            for p in captured:
                self.pieces[self._t^1].discard(p)
            captured = self.get_captured(self._t)
            if captured:
                self.pieces[self._t].remove(p)
                raise Exception("Cannot self capture")
            if len(self.history) > 2:
                h = self.history[-2]
                if h and h[0] == self.pieces[0] and h[1] == self.pieces[1]:
                    self.rollback(2)
                    raise Exception("Illegal KO move")
            self._t ^= 1
            self.history += [[p.copy() for p in self.pieces]]

    def get_pos(self, pos):
        a, b = (pos[:-1], pos[-1])
        a = self._s[0] - int(a)
        b = ord(b) - 65 - (1 if ord(b) >= 73 else 0) # J skipped
        return a, b

    def get_captured(self, turn):
        groups = []
        for pos in self.pieces[turn]:
            if not groups or pos not in groups[0].union(*groups[1:]):
                groups.append(self.get_grouped_pieces(pos, turn))
        captured = []
        for g in groups:
            liberties = set([v for s in map(self.get_liberties, list(g)) for v in s])
            if not liberties: captured += g
        return captured

    def get_grouped_pieces(self, pos, turn, group=None):
        if not group: group = set()
        if pos in self.pieces[turn] and pos not in group:
            group.add(pos)
            for y, x in [(-1,0), (0,1), (1,0), (0,-1)]:
                p = (pos[0]+y, pos[1]+x)
                self.get_grouped_pieces(p, turn, group)
        return group

    def get_liberties(self, pos):
        liberties = []
        pieces = self.pieces[0] | self.pieces[1]
        for y, x in [(-1,0), (0,1), (1,0), (0,-1)]:
            p = (pos[0]+y, pos[1]+x)
            if self.in_bounds(p) and p not in pieces:
                   liberties += [p]
        return liberties

    def in_bounds(self, pos):
        return pos[0] >= 0 and pos[0] < self._s[0] and \
               pos[1] >= 0 and pos[1] < self._s[1]

    def get_position(self, pos):
        p = self.get_pos(pos)
        return "x" if p in self.pieces[0] else "o" if p in self.pieces[1] else "."

    def handicap_stones(self, num=None):
        if self.pieces[0] or self.history:
            raise Exception("Game has already started")
        stones = ("7G", "3C", "3G", "7C", "5E") \
                 if (self._s[0] == 9 and self._s[1] == 9) else \
                 ("10K", "4D", "4K", "10D", "7G", "7D", "7K", "10G", "4G") \
                 if self._s[0] == 13 and self._s[1] == 13 else \
                 ("16Q", "4D", "4Q", "16D", "10K", "10D", "10Q", "16K", "4K") \
                 if self._s[0] == 19 and self._s[1] == 19 else \
                 None
        if stones == None:
            raise Exception("Can't handicap on invalid board size")
        for i in range(num or len(stones)):
            self.pieces[0].add(self.get_pos(stones[i]))

    def rollback(self, num):
        if not self.history:
            raise Exception("Rollback impossible")
        if num >= len(self.history) +1:
            self.history = self.history[:1]
            self.pieces = [p.copy() if p else set() for p in self.history[-1]]
            self._t = 1
            raise Exception("Rollback impossible")
        self.history = self.history[:-num]
        candidate = None
        i = 1
        while candidate == None:
            if i > len(self.history):
                candidate = None
                break
            candidate = self.history[-i]
            i += 1
        if candidate: self.pieces = [p.copy() if p else set() for p in candidate]
        else: self.pieces = [set(), set()]
        for i in range(num): self._t ^= 1

    def pass_turn(self):
        self.history.append(None)
        self._t ^= 1

    def reset(self):
        self.pieces = [set(), set()]
        self.history = []
        self._t = 0

    @property
    def turn(self):
        return ['black','white'][self._t]

    @property
    def board(self):
        return [['x' if (y,x) in self.pieces[0] else 'o' if (y,x) in self.pieces[1] else '.'
                for x in range(self._s[1])] for y in range(self._s[0])]

    @property
    def size(self):
        return {'height': self._s[0], 'width': self._s[1]}
      
################################
import numpy as np

class Go:
    _int_board = []
    moves = {True: 'x', False: 'o'}
    _verbose = False

    def __init__(self, size, size2=-1):
        n, m = 100, 100
        if type(size) == int:
            n, m = size, size
        if type(size) == str:
            m, n = size.split('X')
        if size2 != -1:
            m, n = size, size2
        if self._verbose:
            print(f'game = Go({m}, {n})')
        if int(n) > 25 or int(m) > 25:
            raise NameError('incorrect size')
        self._int_board = [['.'] * int(n) for x in range(int(m))]
        self.moveX = True
        self.history = []
        self.game_started = False
        self.push()


    @property
    def turn(self):
        return 'black' if self.moveX else 'white'

    @property
    def size(self):
        return {"height": int(len(self._int_board)), "width": int(len(self._int_board[0]))}

    @property
    def board(self):
        return np.flip(self._int_board, axis=0).tolist()

    @board.setter
    def board(self, value):
        self._int_board = value

    def print(self, tbl = None):
        if not tbl:
            tbl = self._int_board
        print('   A B C D E F G H J K L M N O P Q R S T U V W X Y Z'[:len(tbl[0]) * 2 + 2])
        for i in range(len(tbl)):
            print(f'{i + 1}{" " if i < 9 else ""} {"|".join(tbl[i])}')
        print('\n')

    def get_coords(self, s):
        mi, mj = s[:-1], s[-1]
        mi, mj = int(mi) - 1, int(ord(mj) - ord('A'))
        if mj > 8:
            mj -= 1
        if mi >= len(self._int_board) or mj >= len(self._int_board[0]):
            raise NameError('Index out of bounds', s)
        return mi, mj

    def _int_pass_turn(self):
        self.game_started = True
        self.moveX = not self.moveX


    def pass_turn(self):
        if self._verbose:
            print('game.pass_turn()')
        self._int_pass_turn()
        self.push()

    def reset(self):
        self.__init__(len(self._int_board), len(self._int_board[0]))


    def push(self):
        rec = [[x for x in l] for l in self._int_board]
        self.history.append(rec)

    def rollback(self, n=1, old = True):
        if self._verbose:
            print(f'game.rollback({n})')
        self._int_rollback(n)

    def _int_rollback(self, n=1, changePass=True):
        while n > 0 and len(self.history)>1:
            n -= 1
            self._int_board = self.history.pop()
            if changePass:
                self.moveX = not self.moveX
        if n > 0:
            raise NameError('moo many rollbacks')

    def handicap_stones(self, n):
        if self.game_started:
            raise NameError('its too late to set handicap')
        self.game_started = True
        if len(self._int_board) != len(self._int_board[0]) or len(self._int_board) not in (9, 13, 19):
            raise NameError('invalid _int_board size')

        if len(self._int_board) == 9:
            g = '....................2...3...............5...............4...1....................'
            if n > 5:
                raise NameError('Too mutch handicap')
        if len(self._int_board) == 13:
            g = '..........................................2..9..3................................6..5..7................................4..8..1..........................................'
            if n > 9:
                raise NameError('Too mutch handicap')
        if len(self._int_board) == 19:
            g = '............................................................2.....9.....3.....................................................................................................6.....5.....7.....................................................................................................4.....8.....1............................................................'
            if n > 9:
                raise NameError('Too mutch handicap')

        for i in range(1, 10):
            if i <= n:
                g = g.replace(str(i), 'x')
            if i > n:
                g = g.replace(str(i), '.')
        for i in range(len(self._int_board)):
            for j in range(len(self._int_board)):
                self._int_board[i][j] = g[i * len(self._int_board) + j]

    def fill_shape(self, mi, mj, fill=False):
        res = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if (abs(di) + abs(dj) == 2) or (di == 0 and dj == 0):
                    continue
                if mi + di not in range(len(self._int_board)) or mj + dj not in range(len(self._int_board[0])):
                    continue
                if self._int_board[mi + di][mj + dj] == '.':
                    res += 1
                if self._int_board[mi + di][mj + dj] != self.moves[not self.moveX]:
                    continue
                self._int_board[mi + di][mj + dj] = '#'
                res = res + self.fill_shape(mi + di, mj + dj)
        return res

    def KO_check(self):
        if len(self.history) < 4:
            return False
        res = np.array_equal(np.matrix(self._int_board), np.matrix(self.history[-2]))
        if res:
            self._int_rollback(3, changePass=False)
        return res

    def take(self, mi, mj):
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if mi + di not in range(len(self._int_board)) or mj + dj not in range(len(self._int_board[0])):
                    continue
                if self._int_board[mi + di][mj + dj] == self.moves[not self.moveX]:
                    self.push()
                    self._int_board[mi + di][mj + dj] = '#'
                    freedom = self.fill_shape(mi + di, mj + dj)
                    if freedom == 0:
                        self.history.pop()
                        self._int_board = [['.' if x == '#' else x for x in l] for l in self._int_board]
                    else:
                        self._int_rollback(changePass=False)
                        self._int_board[mi + di][mj + dj] = self.moves[not self.moveX]


    def move(self, *movelist):
        self.game_started = True
        if len(movelist) == 0:
            return
        if len(movelist) > 1:
            for a in movelist:
                self.move(a)
            return
        else:
            move = movelist[0]
        if move == '':
            self._int_pass_turn()
            return
        if self._verbose:
            print(f'game.move("{move}")')
        self.push()
        mi, mj = self.get_coords(move)
        if self._int_board[mi][mj] == '.':
            self.push()
            self._int_board[mi][mj] = '#'
            self._int_rollback(changePass=False)
            self._int_board[mi][mj] = self.moves[self.moveX]
            self.take(mi, mj)
            self.push()
            self._int_pass_turn()
            freedom = self.fill_shape(mi, mj)
            if freedom == 0:
                self._int_rollback(2, changePass=False)
                self._int_pass_turn()
                raise NameError('illegal move: self capturing ' + move)
            self._int_rollback(changePass=False)
            self._int_pass_turn()
            if self.KO_check():
                raise NameError('illegal move: KO found ' + move)
            self.moveX = not self.moveX
        else:
            raise NameError('illegal move ' + move, move)

    def get_position(self, move):
        mi, mj = self.get_coords(move)
        return self._int_board[mi][mj]
      
################################
from copy import deepcopy

class Go:
    def __init__(self, *args):
        if max(args) > 25:
                raise Exception("Bad board size")
        else:
            if len(args) == 2:
                self.height, self.width =  args                
            else:
                self.height = self.width = args[0]
            self.size = {"height": self.height, "width": self.width}
            self.reset()
            
    def reset(self, state=None):        
        self.board = [["." for j in range(self.width)] for i in range(self.height)]
        self.player = 0
        self.turn = "black"
        self.capture = False
        self.abc = "ABCDEFGHJKLMNOPQRSTUVWXYZ"[0:self.width]
        self.positions = [set(), set()]
        self.states = []    
        if self.width == self.height and self.width in (9, 13, 19):
            if self.width == 9:
                self.handicap = [[4, 4], [2, 2], [6, 6], [6, 2], [2, 6]]
            elif self.width == 13:
                self.handicap = [[9, 6], [3, 6], [6, 9], [6, 3], [6, 6], [3, 3], [9, 9], [9, 3], [3, 9]]
            else:
                self.handicap = [[15, 9], [3, 9], [9, 15], [9, 3], [9, 9], [3, 3], [15, 15], [15, 3], [3, 15]]
        if state != None:
            last = state[-1]
            for i, x in enumerate(last[0]):
                for u, v in x:
                    self.board[u][v] = "xo"[i]
                    self.positions[i].add((u, v))
            self.capture = last[2]
            self.player = 1 - last[1]
            self.turn = ["black", "white"][self.player]
            self.states = state[:]
    
    def handicap_stones(self, k):
        if self.width != self.height or not self.width in (9, 13, 19) or len(self.states) > 0 or k > len(self.handicap):
            raise Exception("Handicap stone(s) placement impossible")
        else:
            i = 0
            while len(self.handicap) > 0 and i < k:
                x, y = self.handicap.pop()
                self.board[x][y] = "x"
                i += 1
        self.update_state() 
        self.next_player()

    def __repr__(self):
        return '\n'.join(str(self.height - i).ljust(2, '0') + ' ' + ' '.join(row) for i, row in enumerate(self.board)) + '\n  ' + ' '.join(list(self.abc))
    
    def to_str(arr):
        return ''.join(''.join(row) for row in arr)
    
    def playable_move(self, i, j):
        return self.board[i][j] == "."
    
    def parse_position(self, p):
        i = self.height - int(p[:-1])
        if i < 0 or i >= self.height: 
            raise Exception("Bad horizontal value")
        if not p[-1] in self.abc:
            raise Exception("Bad vertical value")
        else:
            j = self.abc.index(p[-1])
        return (i, j)
    
    def is_free(self, x, y):
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            i, j = x + dx, y + dy
            if 0 <= i < self.height and 0 <= j < self.width and self.board[i][j] == '.':
                return True
        return False
    
    def get_groups(self, player):
        not_visited = set(self.positions[player])
        groups = []
        while len(not_visited) > 0:
            x, y = not_visited.pop()
            adj = [[(x, y)]]
            while True:                    
                tmp = []
                for i, j in adj[-1]:
                    for u, v in not_visited:                        
                        if abs(u - i) + abs(v - j) == 1:
                            tmp.append((u, v))                   
                    for u, v in tmp:
                        if (u, v) in not_visited:
                            not_visited.remove((u, v))
                if len(tmp) > 0:
                    adj.append(tmp)
                else:
                    break
            groups.append([])
            for x in adj:
                groups[-1].extend(x)
        return groups
                
            
    def remove_captured(self):
        self.capture = False
        groups = self.get_groups(1 - self.player)
        for group in groups:
            if all(not self.is_free(*x) for x in group):
                self.capture = True
                for (x, y) in group:
                    self.positions[1 - self.player].remove((x, y))
                    self.board[x][y] = '.'
                    
    def is_ko(self, player):
        groups = self.get_groups(player)
        for group in groups:            
            if all(not self.is_free(*x) for x in group):            
                return True
        return False
    
    def add_position(self, i, j):
        self.positions[self.player].add((i, j))
        
    def move(self, *pos):
        for p in pos:
            i, j = self.parse_position(p)
            if self.playable_move(i, j):
                self.board[i][j] = "x" if self.player == 0 else "o"
                self.add_position(i, j)            
                self.remove_captured()
                self.update_state()
                
                if not self.capture and self.is_ko(self.player):
                    self.rollback(1)
                    raise Exception("Under K.O") 
                elif self.capture:
                    if len(self.states) > 2:
                        state = self.states[-3]
                        board = [["." for j in range(self.width)] for i in range(self.height)]
                        for i, x in enumerate(state[0]):
                            for u, v in x:
                                board[u][v] = "xo"[i]
                        if Go.to_str(self.board) == Go.to_str(board):
                            self.rollback(1)
                            raise Exception("K.O Rule") 
                self.next_player()          
            else:
                raise Exception("Invalid move")
    
    def next_player(self):
        self.player = 1 - self.player
        self.turn = ["black", "white"][self.player]
        
    def update_state(self):
        self.states.append([[set(self.positions[0]), set(self.positions[1])], self.player, self.capture])


    def fill_board_by_state(self, pos):
        self.reset()
        for i, p in enumerate(pos):
            for x, y in p:
                self.board[x][y] = "xo"[i]
                
    def rollback(self, n):
        if n > len(self.states):
            raise Exception("No rollback possible")
        else:
            k = 0
            while len(self.states) > 0 and k < n:               
                self.states.pop()
                k += 1
            if len(self.states) > 0:
                self.reset(deepcopy(self.states))
            else:
                self.reset()       

    def pass_turn(self):
        self.update_state()
        self.next_player()
            
    def get_position(self, p):
        i, j = self.parse_position(p)
        return self.board[i][j]
        
#####################################
class Go:
    predefinedHandicapPositions = {
                                    9:  [(2,6), (6,2), (6,6), (2,2), (4,4)],
                                    13: [(3,9), (9,3), (9,9), (3,3), (6,6), (6,3), (6,9), (3,6), (9,6)],
                                    19: [(3,15), (15,3), (15,15), (3,3), (9,9), (9,3), (9,15), (3,9), (15,9)],
                                  }
    
    def __init__(self, rowSize, columnSize=None):
        if columnSize is None:
            columnSize = rowSize
        if rowSize<1 or rowSize>25 or columnSize<1 or columnSize>25:
            raise Exception("Invalid board size")
        self.size={"height": rowSize, "width": columnSize}
        self.rowSize = rowSize
        self.columnSize = columnSize
        self.reset()
    
    def reset(self, keepHandicap=False):
        self.currentPlayer='x'
        self.nextPlayer='o'
        self.turn = 'black'
        self.ko = None
        self.movesHistory = []
        self.board = [['.' for x in range(self.columnSize)] for y in range(self.rowSize)]
        if keepHandicap and not self.handicapSize is None:
            self.handicap_stones(self.handicapSize)
        else:
            self.handicapSize = None
    
    def __swapPlayers(self):
        self.currentPlayer = self.nextPlayer
        self.nextPlayer = chr(ord('x')+ord('o')-ord(self.currentPlayer))
        self.turn = 'white' if self.currentPlayer == 'o' else 'black'
        
    def __addr2coord(self, addr):
        rawRow = addr[:-1]
        columnLetter = addr[-1]
        column = ord(columnLetter)-65
        return self.rowSize-int(rawRow), column-(0 if column<8 else 1)
    
    def __getNeighbours(self, addr, color):
        neighbours = []
        row, column = addr
        for shift in [(1,0), (0,1), (-1,0), (0,-1)]:
            shiftedRow = row + shift[0]
            shiftedColumn = column + shift[1]
            if shiftedRow>=0 and shiftedColumn>=0 and shiftedRow<self.rowSize and shiftedColumn<self.columnSize and self.board[shiftedRow][shiftedColumn] == color:
                neighbours.append((shiftedRow, shiftedColumn))
        return neighbours
        
    def __groupFromSource(self, groupSource, color):
        group = set()
        stack = [groupSource]
        while stack:
            stone = stack.pop()
            if not stone in group:
                group.add(stone)
                stack.extend(self.__getNeighbours(stone, color))
        return group
    
    def __countLiberties(self, group):
        counter = 0
        for stone in group:
            counter += len(self.__getNeighbours(stone, '.'))
        return counter
    
    def __kill(self, group):
        for stone in group:
            self.board[stone[0]][stone[1]] = '.'
        
    def __getCapturableGroup(self, groupSource, color):
        group = self.__groupFromSource(groupSource, color)
        return group if not self.__countLiberties(group) else set()
        
    def get_position(self, addr):
        row, column = self.__addr2coord(addr)
        return self.board[row][column]
        
    def move(self, *addresses):
        for addr in addresses:
            if addr is None:
                self.ko = None
            else:
                coord = self.__addr2coord(addr)
                row, column = coord
                if self.board[row][column] != '.':
                    raise Exception("Cannot place a stone on stone")
                self.board[row][column]=self.currentPlayer
                capturables = set()
                for opponentsNeighour in self.__getNeighbours(coord, self.nextPlayer):
                    capturables.update(self.__getCapturableGroup(opponentsNeighour, self.nextPlayer))
                if not capturables:
                    if self.__getCapturableGroup(coord, self.currentPlayer):
                        self.board[row][column] = '.'
                        raise Exception("Illegal suicide move")
                if len(capturables) == 1:
                    if self.ko in capturables:
                        self.board[row][column] = '.'
                        raise Exception("Illegal Ko move")
                    self.ko = coord
                else:
                    self.ko = None
                self.__kill(capturables)
            self.__swapPlayers()
            self.movesHistory.append(addr)
    
    def handicap_stones(self, stonesNumber):
        if self.movesHistory or self.currentPlayer != 'x':
            raise Exception("Handicap can be set only before game")
        if self.rowSize != self.columnSize or not self.rowSize in Go.predefinedHandicapPositions:
            raise Exception("Handicap on {}x{} board is not implemented".format(self.rowSize, self.columnSize))
        handicapPositions = Go.predefinedHandicapPositions[self.rowSize]
        if stonesNumber<0 or stonesNumber>len(handicapPositions):
            raise Exception("Invalid number of handicap stones")
        if stonesNumber>0:
            for i in range(stonesNumber):
                handicapPosition = handicapPositions[i]
                self.board[handicapPosition[0]][handicapPosition[1]] = 'x'
        self.__swapPlayers()
    
    def pass_turn(self):
        self.move(None)
        
    def rollback(self, number):
        if number>len(self.movesHistory):
            raise Exception("Cannot rollback before game start")
        movesHistory = self.movesHistory[:-number]
        self.reset(True)
        self.move(*movesHistory)
            
        
################################
COL = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'
DIR = {(0, -1), (0, 1), (-1, 0), (1, 0)}
CAP = {
    9: ['7G', '3C', '3G', '7C', '5E'],
    13: ['10K', '4D', '4K', '10D', '7G', '7D', '7K', '10G', '4G'],
    19: ['16Q', '4D', '4Q', '16D', '10K', '10D', '10Q', '16K', '4K']
    }


class Hi(SyntaxError):
    pass


class Go:
    
    def __init__(self, height, width=None):
        if width is None:
            width = height
        
        if width > 25 or height > 25:
            raise Hi('go is dumb go play chess lol')
        
        self._size = (width, height)
        self.rec = [{}]
        self._turn = 0
        self.capped = False
        
    def reset(self):
        self.rec = [{}]
        self._turn = 0
        self.capped = False
        
    def is_valid(self, pos):
        return 0 <= pos[0] < self._size[1] and 0 <= pos[1] < self._size[0]
        
    def conv_move(self, pos):
        row = int(pos[: -1]) - 1
        col = COL.index(pos[-1])
        
        if not self.is_valid((row, col)):
            raise Hi('ur social credit is gone')
        
        return (self._size[1] - row - 1, col)
    
    @property
    def size(self):
        return {'height': self._size[1], 'width': self._size[0]}
        
    @property
    def board(self):
        return [[self.rec[-1].get((r, c), '.') for c in range(self._size[0])] for r in range(self._size[1])]
    
    @property
    def turn(self):
        return 'white' if self._turn else 'black'
    
    def pass_turn(self):
        self.rec.append({**self.rec[-1]})
        self._turn ^= 1
        
    def get_position(self, pos):
        return self.rec[-1].get(self.conv_move(pos), '.')
    
    def move(self, *m):
        for i in m:
            self.try_move(i)
            
    def rollback(self, times):
        if times >= len(self.rec):
            raise Hi('too early')
        
        self.rec = self.rec[: -times]
        
        for _ in range(times):
            self._turn ^= 1
            
    def try_move(self, pos):
        row, col = self.conv_move(pos)
        
        if self.rec[-1].get((row, col), '.') != '.':
            raise Hi('waaaaaat')
            
        new = {**self.rec[-1]}
        
        me = 'x' if self._turn == 0 else 'o'
        other = 'o' if self._turn == 0 else 'x'
        new[row, col] = me
        
        for x, y in DIR:
            curr = (x + row, y + col)
            if new.get(curr, '.') == other:
                touch = set()
                keep = self.am_i_fucked(other, curr, new, touch)
                
                if not keep:
                    for haha_ur_doomed_stupid in touch:
                        del new[haha_ur_doomed_stupid]
                        
        if not self.am_i_fucked(me, (row, col), new, set()):
            raise Hi('stabbed urself')
            
        if len(self.rec) >= 2 and self.rec[-2] == new:
            raise Hi('repeat!!!!!!!!!!!!!!!!!!!!!!!!')
                        
        self.rec.append(new)
        self._turn ^= 1
        
    def am_i_fucked(self, same, pos, board, store):
        store.add(pos)
        out = False
        
        for x, y in DIR:
            curr = (x + pos[0], y + pos[1])
            if not self.is_valid(curr) or curr in store:
                continue
                
            stone = board.get(curr, '.')
            if stone == '.':
                return True
            elif stone == same:
                out |= self.am_i_fucked(same, curr, board, store)

        return out
    
    def handicap_stones(self, n):
        if len(self.rec) > 1 or self.capped:
            raise Hi('too late already froze')
            
        if not self._size[0] == self._size[1] or not self._size[0] in CAP:
            raise Hi('bad board')
            
        for i in range(n):
            pos = self.conv_move(CAP[self._size[0]][i])
            self.rec[-1][pos] = 'x'
        
        self.capped = True
        
################################
class Go:
    def __init__(self, height, width=None):
        if width is None:
            width = height
        if height > 25 or width > 25:
            raise ValueError('its huge')
        self.width = width
        self.height = height
        self.size = {'height': height, 'width': width}
        self.board = [['.' for _ in range(width)] for _ in range(height)]
        self.history = []
        self.turn = 'black'
    
    def _kill(self, board, color):
        searched = set()
        for i, row in enumerate(board):
            for j, c in enumerate(row):
                if c != color or (i, j) in searched:
                    continue
                queue = [(i, j)]
                expanded = set()
                free = False
                while queue:
                    x, y = queue.pop(0)
                    d = board[x][y]
                    if d == '.':
                        free = True
                    if d != color:
                        continue
                    else:
                        expanded.add((x, y))
                    if (x, y) in searched:
                        continue
                    searched.add((x, y))
                    for dx, dy in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
                        newx = x + dx
                        newy = y + dy
                        if 0 <= newx < len(board) and 0 <= newy < len(board[x]):
                            queue.append((newx, newy))
                if not free:
                    yield from expanded
    
    def move(self, *moves):
        for m in moves:
            row, col = self._get_position(m)
            if not (0 <= row < len(self.board) and 0 <= col < len(self.board[row])):
                raise Exception('stone in the universe')
            if self.board[row][col] != '.':
                raise Exception('stepping on others stones')
            stone = 'x' if self.turn == 'black' else 'o'
            opponent = 'o' if self.turn == 'black' else 'x'
            new_board = [row[:] for row in self.board]
            new_board[row][col] = stone
            for x, y in self._kill(new_board, opponent):
                new_board[x][y] = '.'
            for _ in self._kill(new_board, stone):
                raise Exception('life advice: dont kill yourself')
            if self.history and new_board == self.history[-1]:
                raise Exception('ko')
            self.history.append(self.board)
            self.board = new_board
            self._next_turn()

    def rollback(self, num_turns):
        if num_turns > len(self.history):
            raise Exception('roll back too mch')
        last = self.history[-num_turns]
        del self.history[-num_turns:]
        if self.history:
            self.board = last
            if num_turns % 2 == 1:
                self._next_turn()
        else:
            self.reset()

    def _get_position(self, pos):
        row = self.height - int(pos[:-1])
        col = 'ABCDEFGHJKLMNOPQRSTUVXYZ'.index(pos[-1])
        return row, col

    def get_position(self, pos):
        row, col = self._get_position(pos)
        return self.board[row][col]
    
    def _next_turn(self):
        self.turn = 'white' if self.turn == 'black' else 'black'
    
    def pass_turn(self):
        self.history.append(self.board)
        self.board = [row[:] for row in self.board]
        self._next_turn()
    
    def reset(self):
        self.history.clear()
        self.board = [['.' for _ in row] for row in self.board]
        self.turn = 'black'
    
    def handicap_stones(self, n):
        if self.history or not all(all(c == '.' for c in row) for row in self.board):
            raise Exception('stop cheating bro')
        if self.height == self.width == 9:
            if n not in range(1, 6):
                raise Exception('invalid number of handicap stones')
            for x, y in [(2, 6), (6, 2), (6, 6), (2, 2), (4, 4)]:
                if not n:
                    break
                self.board[x][y] = 'x'
                n -= 1
        elif self.height == self.width == 13:
            if n not in range(1, 10):
                raise Exception('invalid number of handicap stones')
            for x, y in [(3, 9), (9, 3), (9, 9), (3, 3), (6, 6), (6, 3), (6, 9), (3, 6), (9, 6)]:
                if not n:
                    break
                self.board[x][y] = 'x'
                n -= 1
        elif self.height == self.width == 19:
            if n not in range(1, 10):
                raise Exception('invalid number of handicap stones')
            for x, y in [(3, 15), (15, 3), (15, 15), (3, 3), (9, 9), (9, 3), (9, 15), (3, 9), (15, 9)]:
                if not n:
                    break
                self.board[x][y] = 'x'
                n -= 1
        else:
            raise Exception('board size aint right')
