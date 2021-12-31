from itertools import product
from copy import deepcopy


class Piece:
    def __init__(self, piece):
        self.piece = piece["piece"]
        self.x = piece["x"]
        self.y = piece["y"]
        self.owner = piece["owner"]
        self.is_last = "prevX" in piece
        if self.is_last:
            self.prevX = piece["prevX"]
            self.prevY = piece["prevY"]

    @property
    def dictionary(self):
        dictionary = {
            "piece": self.piece,
            "x": self.x,
            "y": self.y,
            "owner": self.owner,
        }
        if self.is_last:
            dictionary["prevX"] = self.prevX
            dictionary["prevY"] = self.prevY
        return dictionary

    def _get_next_boards_from_directions(self, board, directions, multiple=True, capture_only=False):
        next_boards = []
        for x_direction, y_direction in directions:
            move_range = range(1, 8) if multiple else [1]
            for i in move_range:
                next_x, next_y = self.x+i*x_direction, self.y+i*y_direction
                if not Board.is_in_board(next_x, next_y): break
                piece = board[next_x][next_y]
                next_board = board.copy()
                if piece:
                    if piece.owner != self.owner:
                        next_board.remove(piece)
                        if next_board.move(self, next_x, next_y):
                            next_boards.append(next_board)
                    break
                if next_board.move(self, next_x, next_y) and not capture_only:
                    next_boards.append(next_board)
        return next_boards

    def __eq__(self, other):
        if type(self) == type(other):
            if self.is_last != other.is_last: return False
            if self.is_last:
                return self.x == other.x and self.y == other.y and self.owner == other.owner and self.prevX == other.prevX and self.prevY == other.prevY
            else:
                return self.x == other.x and self.y == other.y and self.owner == other.owner

    def __hash__(self):
        if self.is_last:
            return hash(self.x) + hash(self.y) + hash(self.prevX) + hash(self.prevY) + hash(self.owner) + hash(self.piece)
        else:
            return hash(self.x) + hash(self.y) + hash(self.owner) + hash(self.piece)

    def __str__(self):
        last = "*" if self.is_last else ""
        owner = "B" if self.owner else "W"
        return "%s%s %s(%s, %s)" % (last, owner, self.piece, self.x, self.y)

    def __repr__(self):
        return self.__str__()

class Knight(Piece):
    def get_next_boards(self, board):
        directions = [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]
        return self._get_next_boards_from_directions(board, directions, False)

class Rook(Piece):
    def get_next_boards(self, board):
        return self._get_next_boards_from_directions(board, [(-1, 0), (1, 0), (0, -1), (0, 1)])

class Bishop(Piece):
    def get_next_boards(self, board):
        return self._get_next_boards_from_directions(board, product([-1, 1], [-1, 1]))

class Queen(Piece):
    def get_next_boards(self, board):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] + list(product([-1, 1], [-1, 1]))
        return self._get_next_boards_from_directions(board, directions)

class King(Piece):
    def get_next_boards(self, board):
        directions = list(product([-1, 0, 1], [-1, 0, 1]))
        directions.remove((0, 0))
        return self._get_next_boards_from_directions(board, directions, False)

class Pawn(Piece):
    @property
    def front_direction(self):
        return 1 if self.owner else -1

    @property
    def first_rank(self):
        return 1 if self.owner else 6

    @property
    def is_first(self):
        return self.y == self.first_rank

    @property
    def is_at_en_passant_rank(self):
        return self.y == 4 if self.owner else self.y == 3

    @property
    def did_move_two_forward(self):
        return self.is_last and abs(self.y - self.first_rank) == 2

    def get_next_boards(self, board):
        next_boards = []
        # can move forward if the front square is empty
        if Board.is_in_board(self.x, self.y+self.front_direction) and not board[self.x][self.y+self.front_direction]:
            next_boards += self._get_next_boards_from_directions(board, [(0, self.front_direction)], False)
        # can move forward two squares if it is the first move and the two front squares are empty
        if Board.is_in_board(self.x, self.y+2*self.front_direction) and not board[self.x][self.y+self.front_direction] and not board[self.x][self.y+2*self.front_direction] and self.is_first:
            next_boards += self._get_next_boards_from_directions(board, [(0, 2*self.front_direction)], False)
        # can move diagonally front square if there is an opponent's piece
        next_boards += self._get_next_boards_from_directions(board, [(-1, self.front_direction), (1, self.front_direction)], False, True)
        # en passant
        if self.is_at_en_passant_rank:
            x_neighbors = filter(lambda p: Board.is_in_board(*p), [(self.x-1, self.y), (self.x+1, self.y)])
            for x, y in x_neighbors:
                piece = board[x][y]
                if not piece: continue
                if type(piece) == self.__class__ and piece.owner != self.owner and piece.did_move_two_forward:
                    next_board = board.copy()
                    next_board.move(self, piece.x, self.y+self.front_direction)
                    next_board.remove(piece)
                    next_boards.append(next_board)
        return next_boards

piece_classes = {
    "pawn": Pawn,
    "knight": Knight,
    "rook": Rook,
    "bishop": Bishop,
    "queen": Queen,
    "king": King
}

class Board:
    @classmethod
    def is_in_board(cls, x, y):
        return x in range(0, 8) and y in range(0, 8)

    def __init__(self, pieces):
        self._board = [[None for _ in range(0, 8)] for _ in range(0, 8)]
        for piece in pieces:
            piece_object = piece_classes[piece["piece"]](piece)
            self[piece["x"]][piece["y"]] = piece_object

    @property
    def pieces(self):
        return [piece for column in self for piece in column if piece]

    def move(self, piece, next_x, next_y):
        if not (next_x in range(0, 8) and next_y in range(0, 8)):
            return False
        piece_in_board = self[piece.x][piece.y]
        self.remove(piece)
        piece_in_board.is_last, piece_in_board.prevX, piece_in_board.prevY = True, piece.x, piece.y
        piece_in_board.x, piece_in_board.y = next_x, next_y
        self[next_x][next_y] = piece_in_board
        return True

    def remove(self, piece):
        self[piece.x][piece.y] = None

    def copy(self):
        return deepcopy(self)

    def get_king(self, player):
        king = list(filter(lambda piece: type(piece) == King and piece.owner == player, self.pieces))
        return king[0] if king else None

    def get_next_boards(self, player):
        players_pieces = list(filter(lambda piece: piece.owner == player, self.pieces))
        return {piece: piece.get_next_boards(self) for piece in players_pieces}

    def is_check(self, player):
        opponent = 0 if player else 1
        all_next_boards = self.get_next_boards(opponent)
        pieces = []
        for piece, next_boards in all_next_boards.items():
            if list(filter(lambda board: board.get_king(player) is None, next_boards)):
                pieces.append(piece.dictionary)
        return pieces

    def is_mate(self, player):
        next_boards = sum([boards for _, boards in self.get_next_boards(player).items()], [])
        return not list(filter(lambda board: not board.is_check(player), next_boards))

    def __getitem__(self, x):
        return self._board[x]

def isCheck(pieces, player):
    board = Board(pieces)
    return board.is_check(player)

def isMate(pieces, player):
    board = Board(pieces)
    return board.is_mate(player)
  
___________________________________________________
moveDictionary = {  0 : [-1, 0],
                  100 : [-2, 1],
                  130 : [-1, 1],
                  200 : [-1, 2],
                  300 : [ 0, 1],
                  400 : [ 1, 2],
                  430:  [ 1, 1],
                  500 : [ 2, 1],
                  600 : [ 1, 0],
                  700 : [ 2,-1],
                  730 : [ 1,-1],
                  800 : [ 1,-2],
                  900 : [ 0,-1],
                  1000: [-1,-2],
                  1030: [-1,-1],
                  1100: [-2,-1]};

def moveToHour(position, hour):
    if position<0 or position>63 or not hour in moveDictionary:
        return -1
    else:
        r = int(position / 8)
        c = position % 8
        delta = moveDictionary[hour]
        r = r + delta[0]
        c = c + delta[1]
        if r<0 or r>7 or c<0 or c>7:
            return -1
        else:
            return r*8+c

def doNothing(position, hour):
    return [[]]
    
def rangeAttack(board, position, directions):
    result = [[] for d in directions]
    dirIndex=0
    for d in directions:
        empty = True
        p = position
        while not p<0 and empty:
            p = moveToHour(p, d)
            if not p<0:
                if board[p].isEmpty():
                    result[dirIndex].append(p)
                else:
                    if board[p].isWhite != board[position].isWhite:
                        result[dirIndex].append(p)
                    empty = False
        dirIndex += 1
    return result

def singleStepAttack(board, position, directions):
    result = [[] for d in directions]
    dirIndex=0
    for d in directions:
        p = moveToHour(position, d)
        if not p<0:
            if board[p].isEmpty():
                result[dirIndex].append(p)
            else:
                if board[p].isWhite != board[position].isWhite:
                    result[dirIndex].append(p)
        dirIndex += 1
    return result

def bishopAttack(board, position):
    return rangeAttack(board, position, [130, 430, 730, 1030])
    
def rookAttack(board, position):
    return rangeAttack(board, position, [0, 300, 600, 900])

def queenAttack(board, position):
    return rangeAttack(board, position, [0, 130, 300, 430, 600, 730, 900, 1030])

def knightAttack(board, position):
    return singleStepAttack(board, position, [100, 200, 400, 500, 700, 800, 1000, 1100])

def kingAttack(board, position):
    return singleStepAttack(board, position, [0, 130, 300, 430, 600, 730, 900, 1030])
    
def kingMove(board, position):
    directions = [0, 130, 300, 430, 600, 730, 900, 1030]
    result = [[] for d in directions]
    dirIndex=0
    for d in directions:
        p = moveToHour(position, d)
        if not p<0:
            if board[p].isEmpty():
                result[dirIndex].append(p)
        dirIndex += 1
    return result

def pawnAttack(board, position):
    if board[position].isWhite:
        directions = [130, 1030]
    else:
        directions = [430, 730]
    result = [[], [], [], []]
    dirIndex=0
    for d in directions:
        p = moveToHour(position, d)
        if not p<0:
            if not board[p].isEmpty() and board[p].isWhite != board[position].isWhite:
                result[dirIndex].append(p)
                dirIndex += 1
    enPassantPositions = []
    c = position % 8
    if c>0:
        enPassantPositions.append(position-1)
    if c<7:
        enPassantPositions.append(position+1)
    for otherPos in enPassantPositions:
        if abs(board[otherPos].previous - otherPos) == 16 and board[otherPos].occupation == 'pawn' and board[otherPos].isWhite != board[position].isWhite:
            result[dirIndex].append(otherPos)
            dirIndex += 1
    
    return result

def pawnMove(board, position):
    result = [[],[]]
    if board[position].isWhite:
        startRow = 6
        move = -8
    else:
        startRow = 1
        move = 8
    currentRow = int(position / 8)
    next = position + move
    if not next<0 and not next>63:
        if board[next].isEmpty():
            result[0] = [next]
    if currentRow == startRow:
        next = position + 2*move
        if board[next].isEmpty():
            result[1] = [next]
    return result

def isCovered(target, pathList):
    for singlePath in pathList:
        if target in singlePath:
            return True
    return False

attackRuleDict = {'Empty': doNothing, 'pawn': pawnAttack, 'bishop': bishopAttack, 'knight': knightAttack, 'rook': rookAttack, 'queen': queenAttack, 'king': kingAttack}
moveRuleDict   = {'Empty': doNothing, 'pawn': pawnMove,   'bishop': bishopAttack, 'knight': knightAttack, 'rook': rookAttack, 'queen': queenAttack, 'king': kingAttack}

class Square:
    def __init__(self, description='Empty', color=True, prev=-1):
        self.previous = -1
        self.isWhite = True
        self.occupation = 'Empty'
        self.justMoved = False
        if type(description)==str and description in attackRuleDict:
            self.occupation = description
        
        if type(color)==bool:
            self.isWhite = color
        
        if type(prev)==int:
            if prev<64 and prev>=0:
                self.previous = prev

    def __str__(self):
        return self.occupation

    def __repr__(self):
        return self.occupation

    def isEmpty(self):
        return (self.occupation == 'Empty')

    def setMoved(self, position):
        if not self.previous<0:
            self.justMoved = (position == self.previous)
    
def isAttacking(board, position, target):
    if position == target:
        return (False, [])
    else:
        if board[position].isEmpty():
            return (False, [])
        else:
            if board[position].occupation in attackRuleDict:
                attackPaths = attackRuleDict[board[position].occupation](board, position)
                for singlePath in attackPaths:
                    if target in singlePath:
                        return (True, singlePath)
                return (False, [])
            else:
                return (False, [])

def canMoveThere(board, white, target):
    result = []
    for position in range(0,64):
        if not board[position].isEmpty():
            if board[position].occupation != 'king':
                if board[position].isWhite == white:
                    if isCovered(target, moveRuleDict[board[position].occupation](board, position)):
                        result.append(position)
    return result

def getAttackers(board, white, target):
    result = []
    for position in range(0,64):
        if not board[position].isEmpty():
            if board[position].isWhite == white:
                (isAttacked, attackPath) = isAttacking(board, position, target)
                if isAttacked:
                    result.append(position)
    return result

def findKingPosition(board, white):
    for position in range(0,64):
        if board[position].occupation == 'king' and board[position].isWhite == white:
            return position
    return -1
    
def isUnderCheck(board, white):
    position = findKingPosition(board, white)
    if not position<0:
        attackers = getAttackers(board, not white, position)
        if len(attackers)>0:
            return (True, attackers)
    return (False,[])

def getBoardFromPieces(pieces):
    board = []
    for pos in range(0,64):
        board.append(Square('Empty', True, pos))
    if type(pieces)==list:
        if len(pieces)>2:
            if type(pieces[0])==dict:
                for singlePiece in pieces:
                    position = 8 * singlePiece['y'] + singlePiece['x']
                    white = (singlePiece['owner'] == 0)
                    if 'prevX' in singlePiece and 'prevY' in singlePiece:
                        previous = 8 * singlePiece['prevY'] + singlePiece['prevX']
                    else:
                        previous = -1
                    board[position] = Square(singlePiece['piece'], white, previous)
                return board
            else:
                return []
        else:
            return []
    else:
        return []

def getPieceDescription(board, position):
    result = {'piece': "Empty", 'owner': 0, 'x': 0, 'y': 0}
    result['piece'] = board[position].occupation
    if board[position].isWhite:
        result['owner'] = 0
    else:
        result['owner'] = 1
    result['x'] = position % 8
    result['y'] = int(position / 8)
    if not board[position].previous<0:
        result['prevX'] = board[position].previous % 8
        result['prevY'] = int(board[position].previous / 8)
    return result

def isCheck(pieces, player):
    board = getBoardFromPieces(pieces)
    if len(board)==64:
        white = (player==0)
        (pos, attackers) = isUnderCheck(board, white)
        result = []
        for attacker in attackers:
            result.append(getPieceDescription(board, attacker))
        return result
    else:
        return []

def isMate(pieces, player):
    board = getBoardFromPieces(pieces)
    if len(board)==64:
        white = (player==0)
        (check, attackList) = isUnderCheck(board, white)
        if check:
            # let's try to move the king
            position = findKingPosition(board, white)
            if position<0:
                return False
            else:
                escapePaths = kingMove(board, position)
                for singlePath in escapePaths:
                    for action in singlePath:
                        newBoard = board[:]
                        newBoard[action] = newBoard[position]
                        newBoard[position] = Square()
                        (stillInCheck, newAttackList) = isUnderCheck(newBoard, white)
                        if not stillInCheck:
                            return False
                # let's try to capture the attacker
                if len(attackList)==1:# if there are two attackers and we couldn't escape then it's checkmate
                    attacker = attackList[0]
                    counterAttack = getAttackers(board, white, attacker)
                    for action in counterAttack:
                        newBoard = board[:]
                        newBoard[attacker] = newBoard[action]
                        newBoard[action] = Square()
                        (stillInCheck, newAttackList) = isUnderCheck(newBoard, white)
                        if not stillInCheck:
                            return False
                    # let's try to cover the king
                    (attacking, attackPath) = isAttacking(board, attacker, position)
                    if attacking:
                        for pos in attackPath:
                            cover = canMoveThere(board, white, pos)
                            for action in cover:
                                newBoard = board[:]
                                newBoard[pos] = newBoard[action]
                                newBoard[action] = Square()
                                (stillInCheck, newAttackList) = isUnderCheck(newBoard, white)
                                if not stillInCheck:
                                    return False
            return True
        else:
            return False
    else:
        return False
      
___________________________________________________
MEAN_ = {'K': 'king', 'H': 'knight', 'R': 'rook', 'B': 'bishop', 'Q': 'queen', 'P': 'pawn'}
MEAN = {'king': 'K', 'queen': 'Q', 'pawn': 'P', 'rook': 'R', 'knight': 'H', 'bishop': 'B'}
MOVES = {'king':  [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)],
         'pawn':  [(-1, -1), (-1, 1), (1, -1), (1, 1)],
         'knight':[(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)],
         'bishop':[(-1, -1), (-1, 1), (1, -1), (1, 1)],
         'queen': [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)],
         'rook':  [(0, 1), (0, -1), (1, 0), (-1, 0)]}

def assign_board(pieces):
    board = standard_board()
    for i in pieces:
        who, whose, y, x = list(i.values())[:4]
        board[x][y] = MEAN[who] + str(whose)
    return board

def generate_directions(board, x, y, inc, dec):
    li, x, y = [], x+inc, y+dec
    while isvalid(x, y) and board[x][y] == '  ':
        li.append((x, y))
        x,y = x+inc,y+dec
    return li + ([(x, y)] if isvalid(x, y) else [])

standard_board = lambda :[['  ' for _ in range(8)] for _ in range(8)]
isvalid  = lambda x, y:0 <= x < 8 and 0 <= y < 8
simplify = lambda x,p:sum(x,[]) if p in 'QBR' else x
king     = lambda board, x, y, turn:[(x+i, y+j) for i, j in MOVES['king'] if isvalid(x+i, y+j)]
pawn     = lambda board, x, y, turn:[(x+i,y+j) for i,j in ([MOVES['pawn'][:2],MOVES['pawn'][2:]][turn]) if isvalid(x+i,y+j)]
knight   = lambda board, x, y, turn:[(x + i, y + j) for i, j in MOVES['knight'] if isvalid(x + i, y + j)]
bishop   = lambda board, x, y, turn:[generate_directions(board, x, y, *i) for i in MOVES['bishop']]
queen    = lambda board, x, y, turn:[generate_directions(board, x, y, *i) for i in MOVES['queen']]
rook     = lambda board, x, y, turn:[generate_directions(board, x, y, *i) for i in MOVES['rook']]
pawn_    = lambda board, x, y, turn:[(i, j) for i, j in [(x+[-1,1][turn], y), (x+[-2,2][turn], y)] if isvalid(i, j)]

def is_next_check(pieces,turn,n,i,j):
    return isCheck([k if (k['y'], k['x']) != (i, j) else {'piece': k['piece'], 'owner': turn, 'x': n[1], 'y': n[0]} for k in pieces if (k['y'], k['x']) != n], turn)
    
def killable(pieces, turn, n, others_move, board, check_):
    players = [(i['y'], i['x']) for i in pieces if i['owner'] == turn]
    return next((not is_next_check(pieces,turn,n,i,j) for i, j in players if n in others_move[(i, j)]),False)

def En_passant(pieces, turn, board, checks, king):
    opp_pawn = [i for i in checks if i['piece'] == 'pawn']
    if opp_pawn:
        for i in opp_pawn:
            if (abs(i['x'] - i.get('prevX', 0)), abs(i['y'] - i.get('prevY', 0))) == (0, 2):
                for j, k in [(0, -1), (0, 1)]:
                    ni, nj = i['y'] + j, i['x'] + k
                    if isvalid(ni, nj) and board[ni][nj] == 'P' + str(turn):
                        to_move = (i['y'] + [-1, 1][turn], i['x'])
                        t_pieces = [k for k in pieces if (k['y'], k['x']) != (ni, nj) and (k['y'], k['x']) != (i['x'], i['y'])]
                        t_pieces.append({'piece': MEAN_[board[ni][nj][0]], 'owner': turn, 'x': to_move[1], 'y': to_move[0]})
                        if not isCheck(t_pieces, turn) : return True
        return False
    return False

def can_we_place(pieces, turn, board, checks, king):
    rest_moves = {}
    for i in pieces:
        who, whose, y, x = list(i.values())[:4]
        if whose == turn : rest_moves[(x, y)] = pawn_(board, x, y, turn) if who == 'pawn' else simplify(F[MEAN[who]](board, x, y, turn),MEAN[who])
            
    for i in checks:
        who, whose, y, x = list(i.values())[:4]
        if MEAN[who] in 'QBR':
            moves = F[MEAN[who]](board, x, y, turn)
            for j in moves:
                if king in j:
                    for ot, op in rest_moves.items():
                        common = [(k, l) for k, l in set(op).intersection(j) if board[k][l] == '  ']
                        for cmn in common:
                            t_pieces = [k for k in pieces if (k['y'], k['x']) != ot]
                            t_pieces.append({'piece': MEAN_[board[ot[0]][ot[1]][0]],'owner': turn, 'x': cmn[1], 'y': cmn[0]})
                            if not isCheck(t_pieces, 0) : return True
    return False

F = {'K': king, 'R': rook, 'H': knight, 'B': bishop, 'Q': queen, 'P': pawn}
def isCheck(pieces, turn):
    board, threats = assign_board(pieces), []
    for i in pieces:
        who, whose, y, x = list(i.values())[:4]
        if whose == turn ^ 1:
            possible_moves = simplify(F[MEAN[who]](board, x, y, whose),MEAN[who])
            if any(board[k][l] == 'K' + str(turn) for k, l in possible_moves):
                threats.append(i)
    return threats

def isMate(pieces, turn):
    checks = isCheck(pieces, turn)
    if not checks : return False
    
    board = assign_board(pieces)
    (who, owner, y, x) = list(next(i for i in pieces if i['piece'] == 'king' and i['owner'] == turn).values())[:4]
    KING = (x, y)
    king_moves, others_moves = list(filter(lambda x: board[x[0]][x[1]] == '  ', king(board, x, y, turn))), {}
    for i in pieces:
        who, whose, y, x = list(i.values())[:4]
        possible = F[MEAN[who]](board, x, y, turn)
        others_moves[(x, y)] = sum(possible, []) if MEAN[who] in 'RQB' else possible

    li = [any(board[k][l][1] == str(turn ^ 1) and i in j and
          not killable(pieces, turn, (k, l), others_moves, board, checks) for (k, l), j in others_moves.items()) for i in king_moves]
    
    return all(li) and all(not k(pieces, turn, board, checks, KING) for k in [can_we_place, En_passant])
  
___________________________________________________
# build matrix of the game
def buildMatrix(pieces):
    matrix = [[None for x in range(8)] for y in range(8)] 
    for piece in pieces:
        matrix[piece["x"]][piece["y"]]=piece
    return matrix

# find king of player
def findKing(pieces,player):
    for piece in pieces:
        if piece['piece']=='king' and piece['owner']==player:
            return piece

def move_pawn(matrix,piece):
    x0, y0 = piece["x"], piece["y"]
    direction=1 if piece['owner']==1 else -1
    moves=set()
    if 0 <= y0+direction <= 7 and matrix[x0][y0+direction]==None:
        moves|={(x0,y0+direction)} 
        if ((piece['owner']==1 and piece['y']==1 or piece['owner']==0 and piece['y']==6)
            and  matrix[x0][y0+2*direction]==None):
            #pawn can move 2 cases at initial move
            moves|={(x0,y0+2*direction)} 
    moves|={(x0+dx,y0+direction)
        for dx in (-1,1) 
        if 0 <= x0+dx <= 7 and 0 <= y0+direction <= 7 
            and matrix[x0+dx][y0+direction]!=None and matrix[x0+dx][y0+direction]['owner']!=piece['owner']
            }
    moves|={(x0+dx,y0+direction) 
        for dx in (-1,1) 
        if 0 <= x0+dx <= 7 and 0 <= y0+direction <= 7 
            and matrix[x0+dx][y0+direction]==None 
            and matrix[x0+dx][y0]!=None and matrix[x0+dx][y0]['piece']=='pawn' 
            and matrix[x0+dx][y0]['owner']!=piece['owner']
            and 'prevX' in matrix[x0+dx][y0].keys() and matrix[x0+dx][y0]['prevX']==matrix[x0+dx][y0]['x']
            and 'prevY' in matrix[x0+dx][y0].keys() and matrix[x0+dx][y0]['prevY']==matrix[x0+dx][y0]['y']+2*direction
            }
    moves = [move for move in list(moves) if 0 <= y0+direction <= 7]
    return moves

# return attack point of pawn
def move_rook(matrix,piece):
    x0, y0 = piece["x"], piece["y"]
    moves = []
    for moves0 in [[(x0-d,y0) for d in range(1,8)],
                   [(x0+d,y0) for d in range(1,8)],
                   [(x0,y0-d) for d in range(1,8)],
                   [(x0,y0+d) for d in range(1,8)]]:
        for x, y in [(x, y) for x,y in moves0 if 0 <= x <= 7 and 0 <= y <= 7]:
            if matrix[x][y]==None or matrix[x][y]['owner']!=piece['owner']:
                moves.append((x,y))
            if matrix[x][y]!=None:
                break
    return moves

def move_bishop(matrix,piece):
    x0, y0 = piece["x"], piece["y"]
    moves = []
    for moves0 in [[(x0-d,y0-d) for d in range(1,8)],
                   [(x0-d,y0+d) for d in range(1,8)],
                   [(x0+d,y0-d) for d in range(1,8)],
                   [(x0+d,y0+d) for d in range(1,8)]]:
        for x, y in [(x, y) for x,y in moves0 if 0 <= x <= 7 and 0 <= y <= 7]:
            if matrix[x][y]==None or matrix[x][y]['owner']!=piece['owner']:
                moves.append((x,y))
            if matrix[x][y]!=None:
                break
    return moves

def move_queen(matrix,piece):
    x0, y0 = piece["x"], piece["y"]
    moves = []
    for moves0 in [[(x0-d,y0-d) for d in range(1,8)],
                   [(x0-d,y0+d) for d in range(1,8)],
                   [(x0+d,y0-d) for d in range(1,8)],
                   [(x0+d,y0+d) for d in range(1,8)],
                   [(x0-d,y0) for d in range(1,8)],
                   [(x0+d,y0) for d in range(1,8)],
                   [(x0,y0-d) for d in range(1,8)],
                   [(x0,y0+d) for d in range(1,8)]]:
        for x, y in [(x, y) for x,y in moves0 if 0 <= x <= 7 and 0 <= y <= 7]:
            if matrix[x][y]==None or matrix[x][y]['owner']!=piece['owner']:
                moves.append((x,y))
            if matrix[x][y]!=None:
                break
    return moves

def move_knight(matrix,piece):
    x0, y0 = piece["x"], piece["y"]
    moves = [(x0+2,y0+1),(x0+2,y0-1),(x0-2,y0+1),(x0-2,y0-1),
             (x0+1,y0+2),(x0-1,y0+2),(x0+1,y0-2),(x0-1,y0-2)]
    moves = [move for move in moves if 0 <= move[0] <= 7 and 0 <= move [1] <= 7]
    moves = [(x,y) for (x,y) in moves if matrix[x][y]==None or matrix[x][y]['owner']!=piece['owner']]
    return moves

# return attack point of pawn
def move_king(matrix,piece):
    x0, y0 = piece["x"], piece["y"]
    moves=[(x0+dx, y0+dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != 0 or dy != 0]
    moves = [move for move in moves if 0 <= move[0] <= 7 and 0 <= move [1] <= 7]
    moves = [(x,y) for (x,y) in moves if matrix[x][y]==None or matrix[x][y]['owner']!=piece['owner']]
    return moves
    
# Returns an array of threats if the arrangement of the pieces is a check, otherwise false
def isCheck(pieces, player):
    matrix=buildMatrix(pieces)
    king = findKing(pieces,player)
    king_xy = (king['x'],king['y'])
    threaten_king = []
    d_moves = {'pawn': move_pawn, 'rook': move_rook, 'knight':move_knight, 'bishop':move_bishop,
               'queen':move_queen, 'king':move_king}
    for piece in [piece for piece in pieces if piece['owner']!=player]:
        moves = d_moves[piece['piece']](matrix, piece)
        if king_xy in moves:
            threaten_king.append(piece)
    return threaten_king
    
# Returns true if the arrangement of the pieces is a check mate, otherwise false
def isMate(pieces, player):
    if not isCheck(pieces,player):
        return False
    king = findKing(pieces,player)
    matrix=buildMatrix(pieces)
    d_moves = {'pawn': move_pawn, 'rook': move_rook, 'knight':move_knight, 'bishop':move_bishop,
               'queen':move_queen, 'king':move_king}
    for piece in [piece for piece in pieces if piece['owner']==player]:
        x0, y0 = piece["x"], piece["y"]
        moves = d_moves[piece['piece']](matrix, piece)
        for x, y in moves:
            pieces1=[piece for piece in pieces.copy() if not(piece['x']==x and piece['y']==y)]
            if piece['piece']=='pawn'and x0!=x and len(pieces)==len(pieces1):
                #Need to look for a take en-passant
                pieces1=[piece for piece in pieces1 if not(piece['x']==x and 'prevY' in piece)]
            piece['x'], piece['y'] = x, y
            if not isCheck(pieces1,player):
                return False
        piece['x'], piece['y'] = x0, y0
    return True
    
___________________________________________________
def isMate(pieces, player):
    """  
    isMate should return true if the player can't make a move that takes his king out of check,
    and false if he can make such a move, or if the position is not a check.
    """
    import copy
    
    for item in filter(lambda w: w['owner']==player, pieces):
        for new_loc in getattr(Calculators, "Call" + capitalise(item['piece']))(pieces,player,(item['x'],item['y'])):
            
            
            pieces_temp = copy.deepcopy(pieces)
            pieces_temp[pieces.index(item)]['x'] = new_loc[0]
            pieces_temp[pieces.index(item)]['y'] = new_loc[1]
            
            if PlaceFree(pieces_temp,player,new_loc) == 1-player:
                for item_2 in filter(lambda w: w['owner'] != player and w['x'] == new_loc[0] and w['y'] == new_loc[1], pieces_temp):
                    pieces_temp.pop(pieces_temp.index(item_2))
                    
            
            if not isCheck(pieces_temp,player):
                return False
            
        # create en passant board:
    for item in filter(lambda w: w['owner']!=player, pieces):
        try:
            if  item['piece']=='pawn' and abs(item['y']-item['prevY'])==2:
                for item_2 in filter(lambda w: w['owner']==player and w['piece']=='pawn' and item['y'] == w['y'], pieces):
                    if(abs(item_2['x']-item['x'])==1):
                        
                        pieces_temp = copy.deepcopy(pieces)
                        pieces_temp[pieces.index(item_2)]['x'] = item['x']
                        pieces_temp[pieces.index(item_2)]['y'] = (item['y']+item['prevY'])/2
                        pieces_temp.pop(pieces_temp.index(item))
                        
                        
                        if not isCheck(pieces_temp,player):
                            return False
                        
        except Exception as ex:
            pass
        
        
    return True
    

def isCheck(pieces, player):
    results = []
    for item in filter(lambda w: w['owner']==player and w['piece']=='king', pieces):
        location_king = (item['x'],item['y'])
        
    for item in filter(lambda w: w['owner']!=player, pieces):
    
       
        if location_king in getattr(Calculators, "Call" + capitalise(item['piece']))(pieces,1-player,(item['x'],item['y'])):
            results.append(pieces[pieces.index(item)])
    return results
      
    
            

def PlaceFree(pieces,player,loc):
    for item in pieces:
        if (item['x'],item['y']) == loc:
            return item['owner']
    return 2
        

def capitalise(str):
    return str[0].upper() + str[1:]

def onBoard(loc):
    x,y=loc
    if x in range(0,8) and y in range(0,8):
        return True
    else:
        return False


class Calculators():
    
    def CallPawn(pieces,player,loc):
        x,y = loc
        list_of_possibilities=[]
        if player == 1:
            if y==1 and PlaceFree(pieces,player,(x,2))==2:
                list_of_possibilities.append((x,3) )
            for add_x in [-1,0,1]:
                if onBoard((x+add_x,y+1)) and PlaceFree(pieces,player,(x+add_x,y+1))!=player:
                    if add_x != 0: 
                        if PlaceFree(pieces,player,(x+add_x,y+1))!=2:
                            list_of_possibilities.append((x+add_x,y+1))
                    else:
                        if PlaceFree(pieces,player,(x+add_x,y+1))==2:               
                            list_of_possibilities.append((x+add_x,y+1))
       
                     
        
        
        else:
            if y==6 and PlaceFree(pieces,player,(x,5))==2:
                list_of_possibilities.append((x,4)) 
            for add_x in [-1,0,1]:
                if onBoard((x+add_x,y-1)) and PlaceFree(pieces,player,(x+add_x,y-1))!=player:
                    if add_x != 0: 
                        if PlaceFree(pieces,player,(x+add_x,y-1)) !=2:
                            list_of_possibilities.append((x+add_x,y-1))
                    else:
                        if PlaceFree(pieces,player,(x+add_x,y-1))==2:
                            list_of_possibilities.append((x+add_x,y-1))
                           

        return list_of_possibilities

    def CallKing(pieces, player,loc):
        list_of_possibilities=[]
        x,y = loc
        for add_x in [-1,0,1]:
            for add_y in [-1,0,1]:
                if onBoard((x+add_x,y+add_y)) and PlaceFree(pieces,player,(x+add_x,y+add_y))!= player:
                    list_of_possibilities.append((x+add_x,y+add_y))

        return list_of_possibilities



    def CallRook(pieces,player,loc):
        x,y = loc
        list_of_possibilities=[]
        multiply =[(-1,0),(1,0),(0,-1),(0,1)]
        for item in multiply:
            step = 1
            while onBoard((x + step*item[0],y+step*item[1])):
                if PlaceFree(pieces,player,(x + step*item[0],y+step*item[1])) !=player:
                    list_of_possibilities.append((x + step*item[0],y+step*item[1]))
                if PlaceFree(pieces,player,(x + step*item[0],y+step*item[1])) != 2:
                    break
                step += 1
        return list_of_possibilities

    def CallKnight(pieces,player,loc):
        x,y = loc
        list_of_possibilities=[]

        for add_x in [x for x in range(-2,3) if x != 0]:
            add_y = 3-abs(add_x)
            if onBoard((x+add_x,y+add_y)) and PlaceFree(pieces,player,(x+add_x,y+add_y))!= player:
                list_of_possibilities.append((x+add_x,y+add_y))
            if onBoard((x+add_x,y-add_y)) and PlaceFree(pieces,player,(x+add_x,y-add_y))!= player:
                list_of_possibilities.append((x+add_x,y-add_y))

        return list_of_possibilities        

    def CallBishop(pieces,player,loc):
        x,y = loc
        list_of_possibilities=[]
        multiply =[(-1,-1),(1,1),(1,-1),(-1,1)]
        for item in multiply:
            step = 1
            while onBoard((x + step*item[0],y+step*item[1])):
                if PlaceFree(pieces,player,(x + step*item[0],y+step*item[1])) !=player:
                    list_of_possibilities.append((x + step*item[0],y+step*item[1]))
                if PlaceFree(pieces,player,(x + step*item[0],y+step*item[1])) != 2:
                    break
                step += 1
        return list_of_possibilities

    def CallQueen(pieces,player,loc):
        return Calculators.CallBishop(pieces,player,loc) + Calculators.CallRook(pieces,player,loc)
      
___________________________________________________
# Returns an array of threats if the arrangement of 
# the pieces is a check, otherwise false
def isCheck(pieces, player):
    
    # Check if one of the opposite pieces can attack the king
    king = [p for p in pieces if p['piece'] == "king" and p['owner'] == player][0]
    check_pieces = [p for p in pieces if p['owner'] != player and pieceCanAttack(p, king, pieces)]

    return check_pieces if len(check_pieces) > 0 else False
   
# Returns true if the arrangement of the
# pieces is a check mate, otherwise false
def isMate(pieces, player):
    is_mate = False
    
    if isCheck(pieces, player):
        #If is check try if exists at least a move that avoids the mate  
        move_found = False
        owner_pieces = [p for p in pieces if p['owner'] == player]
        for piece in owner_pieces:
            for new_position in getAllowedMoves(piece, pieces):
                #Move the piece to the new position and try if it's still check
                new_pieces = getPiecesAfterMove(piece, new_position, pieces)
                if not isCheck(new_pieces, player):
                    #A position with no check exists exit loop
                    move_found = True
                    break
            if move_found:
                #A position with no check exists exit loop
                break
        else:
            #No position was found: check mate
            is_mate = True
    
    return is_mate





#--------------------------------------------- UD SECTION -------------------------------------------------------   
# Returns True if the piece can attack the piece_to_attack otherwise False
def pieceCanAttack(piece, piece_to_attack, pieces):
   return [piece_to_attack['x'], piece_to_attack['y']] in getAllowedMoves(piece, pieces, get_attack_moves = True)

# Compute a new list of pieces moving the specified piece to a new position
def getPiecesAfterMove(piece, new_position, pieces):
    #Create the new list removing the piece in the new position
    new_pieces = [p.copy() for p in pieces if [p['x'], p['y']] != new_position]
    #Move the piece to the new position
    for p in new_pieces:
        if [p['x'], p['y']] == [piece['x'], piece['y']]:
            p['x'] = new_position[0]
            p['y'] = new_position[1]
            break
        
    return new_pieces

# Get allowed moves for Pawn
def getAllowedPawnMoves(piece, pieces, get_attack_moves):
    allowed_moves = []
    if get_attack_moves:
        #Compute attack moves
        if piece['owner'] == 0:
            #White can go up
            allowed_moves = [[p['x'], p['y']] for p in pieces 
                                              if p['owner'] != piece['owner'] and
                                                ([p['x'], p['y']] == [piece['x'] - 1, piece['y'] - 1] 
                                                   or [p['x'], p['y']] == [piece['x'] + 1, piece['y'] - 1])]
            #Check for en-passant moves
            en_passant_moves = [[p['x'], p['y']] for p in pieces 
                                                 if p['owner'] != piece['owner'] and
                                                    p['piece'] == 'pawn' and
                                                    p.get('prevY') == 1 and
                                                   (p['x'] + 1 == piece['x'] or p['x'] - 1 == piece['x'])]
        else:
            #Black can go down
            allowed_moves = [[p['x'], p['y']] for p in pieces 
                                              if p['owner'] != piece['owner'] and
                                                ([p['x'], p['y']] == [piece['x'] - 1, piece['y'] + 1] 
                                                   or [p['x'], p['y']] == [piece['x'] + 1, piece['y'] + 1])]
            #Check for en-passant moves
            en_passant_moves = [[p['x'], p['y']] for p in pieces 
                                                 if p['owner'] != piece['owner'] and
                                                    p['piece'] == 'pawn' and
                                                    p.get('prevY') == 6 and
                                                   (p['x'] + 1 == piece['x'] or p['x'] - 1 == piece['x'])]
        
        #Add en-passant moves
        allowed_moves = allowed_moves + en_passant_moves
        #Remove positions occupied by an owner piece
        occupied_positions = [[p['x'], p['y']] for p in pieces if p['owner'] == piece['owner']]
        allowed_moves = [m for m in allowed_moves if m not in occupied_positions]
        
    else:
        #Compute moving moves
        if piece['owner'] == 0:
            # white can go up once, or twice if it never moved
            allowed_moves = [[piece['x'], piece['y'] - 1]]
            allowed_moves = allowed_moves + [[piece['x'], piece['y'] - 2]] if piece['y'] == 6 else allowed_moves
        else:
            # black can go down once, or twice if it never moved
            allowed_moves = [[piece['x'], piece['y'] + 1]]
            allowed_moves = allowed_moves + [[piece['x'], piece['y'] + 2]] if piece['y'] == 1 else allowed_moves
        #Remove positions occupied by another piece
        occupied_positions = [[p['x'], p['y']] for p in pieces]
        allowed_moves = [m for m in allowed_moves if m not in occupied_positions]
        #Add attack moves
        allowed_moves = allowed_moves + getAllowedPawnMoves(piece, pieces, get_attack_moves = True)
    
    
    return allowed_moves

# Get allowed moves for King
def getAllowedKingMoves(piece, pieces, get_attack_moves):
    allowed_moves = [[x,y] for x in range(piece['x'] - 1, piece['x'] + 2) 
                            for y in range(piece['y'] - 1, piece['y'] + 2) 
                             if [x,y] != [piece['x'],piece['y']] and x in range(8) and y in range(8) 
                   ]
    #Remove positions occupied by another piece
    occupied_positions = [[p['x'], p['y']] for p in pieces if p['owner'] == piece['owner']]
    allowed_moves = [m for m in allowed_moves if m not in occupied_positions]
        
    return allowed_moves

# Get allowed moves for Bishop
def getAllowedBishopMoves(piece, pieces, get_attack_moves):
    allowed_moves = []
    #Do not consider positions occupied by another piece
    occupied_opponent_positions = [[p['x'], p['y']] for p in pieces if p['owner'] != piece['owner']]
    occupied_owner_positions = [[p['x'], p['y']] for p in pieces if p['owner'] == piece['owner']]
    #Down right column
    for i in range(1, 8):
        current_position = [piece['x'] + i, piece['y'] + i]
        if (current_position in occupied_owner_positions) or (current_position[0] > 7) or (current_position[1] > 7):
            #Occupied position or position out of the board
            break
        if current_position in occupied_opponent_positions:
            #Opponent occupied position: can be attacked
            allowed_moves.append(current_position)
            break
        #Free position
        allowed_moves.append(current_position)
    #Up right column
    for i in range(1, 8):
        current_position = [piece['x'] + i, piece['y'] - i]
        if (current_position in occupied_owner_positions) or (current_position[0] > 7) or (current_position[1] < 0):
            #Occupied position or position out of the board
            break
        if current_position in occupied_opponent_positions:
            #Opponent occupied position: can be attacked
            allowed_moves.append(current_position)
            break
        #Free position
        allowed_moves.append(current_position)
    #Down left column
    for i in range(1, 8):
        current_position = [piece['x'] - i, piece['y'] + i]
        if (current_position in occupied_owner_positions) or (current_position[0] < 0) or (current_position[1] > 7):
            #Occupied position or position out of the board
            break
        if current_position in occupied_opponent_positions:
            #Opponent occupied position: can be attacked
            allowed_moves.append(current_position)
            break
        #Free position
        allowed_moves.append(current_position)
    #Up left column
    for i in range(1, 8):
        current_position = [piece['x'] - i, piece['y'] - i]
        if (current_position in occupied_owner_positions) or (current_position[0] < 0) or (current_position[1] < 0):
            #Occupied position or position out of the board
            break
        if current_position in occupied_opponent_positions:
            #Opponent occupied position: can be attacked
            allowed_moves.append(current_position)
            break
        #Free position
        allowed_moves.append(current_position)
    
    return allowed_moves

# Get allowed moves for Rook
def getAllowedRookMoves(piece, pieces, get_attack_moves):
    allowed_moves = []
    #Do not consider positions occupied by another piece
    occupied_opponent_positions = [[p['x'], p['y']] for p in pieces if p['owner'] != piece['owner']]
    occupied_owner_positions = [[p['x'], p['y']] for p in pieces if p['owner'] == piece['owner']]
    #Down row
    for i in range(1, 8):
        current_position = [piece['x'], piece['y'] + i]
        if (current_position in occupied_owner_positions) or (current_position[1] > 7):
            #Occupied position or position out of the board
            break
        if current_position in occupied_opponent_positions:
            #Opponent occupied position: can be attacked
            allowed_moves.append(current_position)
            break
        #Free position
        allowed_moves.append(current_position)
    #Left row
    for i in range(1, 8):
        current_position = [piece['x'] - i, piece['y']]
        if (current_position in occupied_owner_positions) or (current_position[0] < 0):
            #Occupied position or position out of the board
            break
        if current_position in occupied_opponent_positions:
            #Opponent occupied position: can be attacked
            allowed_moves.append(current_position)
            break
        #Free position
        allowed_moves.append(current_position)
    #Up row
    for i in range(1, 8):
        current_position = [piece['x'], piece['y'] - i]
        if (current_position in occupied_owner_positions) or (current_position[1] < 0):
            #Occupied position or position out of the board
            break
        if current_position in occupied_opponent_positions:
            #Opponent occupied position: can be attacked
            allowed_moves.append(current_position)
            break
        #Free position
        allowed_moves.append(current_position)
    #Right row
    for i in range(1, 8):
        current_position = [piece['x'] + i, piece['y']]
        if (current_position in occupied_owner_positions) or (current_position[0] > 7):
            #Occupied position or position out of the board
            break
        if current_position in occupied_opponent_positions:
            #Opponent occupied position: can be attacked
            allowed_moves.append(current_position)
            break
        #Free position
        allowed_moves.append(current_position)
    
    return allowed_moves

# Get allowed moves for Queen
def getAllowedQueenMoves(piece, pieces, get_attack_moves):
    #Queen moves are the union of bisop and rook
    allowed_moves = getAllowedBishopMoves(piece, pieces, get_attack_moves) + getAllowedRookMoves(piece, pieces, get_attack_moves)
    return allowed_moves

# Get allowed moves for Knight
def getAllowedKnightMoves(piece, pieces, get_attack_moves):
    #Compute all possible positions
    attack_offsets = [[-2,-1],[-2,1],[-1,2],[1,2],[2,1],[2,-1],[1,-2],[-1,-2]]
    allowed_moves = [[piece['x'] + i, piece['y'] + j] for [i,j] in attack_offsets]
    #Remove not allowed posiitons
    occupied_positions = [[p['x'], p['y']] for p in pieces if p['owner'] == piece['owner']]
    allowed_moves = [m for m in allowed_moves if m not in occupied_positions and m[0] in range(8) and m[1] in range(8)]
    
    return allowed_moves

# Get allowed moves of the specified piece
def getAllowedMoves(piece, pieces, get_attack_moves = False):
    
    # Call specific function for the specified piece
    allowed_moves_functions = {
                               'pawn' : getAllowedPawnMoves,
                               'king' : getAllowedKingMoves,
                               'bishop' : getAllowedBishopMoves,
                               'rook' : getAllowedRookMoves,
                               'queen' : getAllowedQueenMoves,
                               'knight' : getAllowedKnightMoves
                               }   
    allowed_moves = allowed_moves_functions[piece['piece']](piece, pieces, get_attack_moves)
    
    return allowed_moves
