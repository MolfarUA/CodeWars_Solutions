from random import choice, randint
import re


def copyBoard(lst):   return [r[:] for r in lst]
def copyHistory(lst): return [(copyBoard(b),c) for b,c in lst]


class hF:
  def create_board(self, h, w):
    return [['.' for x in range(w)] for y in range(h)]
  
  def generate_coord(self, y = 19, x = None):
    if x == None: x = y
    letters = list("ABCDEFGHJKLMNOPQRSTUVWXYZ")
    nums = [y for y in range(1,y)]
    return str(choice(nums)) + choice(letters[:x])
  
  def generate_coords(self, n, strict = True, y = 19, x = 19):
      coords = [self.generate_coord(y,x) for n in range(0,n)]
      if strict:
          while len(set(coords)) != len(coords):
              coords = [self.generate_coord(y,x) for n in range(0,n)]
      return list(set(coords))

_helperFuncs = hF()
test.describe("Creating go boards")
test.it("9x9")
game = Go(9)
board = _helperFuncs.create_board(9, 9)
test.assert_equals(game.board, board, "Should generate a 9 by 9 board.")
close_it()

test.it("13x13")
game = Go(13)
board = _helperFuncs.create_board(13, 13)
test.assert_equals(game.board, board, "Should generate a 13 by 13 board.")
close_it()

test.it("19x19")
game = Go(19)
board = _helperFuncs.create_board(19, 19)
test.assert_equals(game.board, board, "Should generate a 19 by 19 board.")
close_it()

test.it("32x32")
test.expect_error("Should throw an error. Board cannot be larger than 25 by 25", lambda: Go(32))
close_it()

for i in range(0, 10):
    height = randint(2,24)
    width  = randint(2,24)
    log = str(height) + "x" + str(width)
    test.it(log)
    game = Go(height, width)
    board = _helperFuncs.create_board(height, width)
    test.assert_equals(game.board, board, "Should generate a " + log + " board.")
    close_it()

close_describe()

test.describe("Placing stones")
test.it("Place a black stone")
game = Go(19)
coord = _helperFuncs.generate_coord()
game.move(coord)
test.assert_equals(game.get_position(coord), "x")
close_it()

test.it("Place a white stone")
game = Go(19)
[coord, coord2] = _helperFuncs.generate_coords(2)

game.move(coord)
game.move(coord2)
test.assert_equals(game.get_position(coord2), "o")
close_it()

test.it("Can take multiple moves at a time")
game = Go(19)
[coord, coord2, coord3] = _helperFuncs.generate_coords(3)

game.move(coord, coord2, coord3)
test.assert_equals(game.get_position(coord), "x")
test.assert_equals(game.get_position(coord2), "o")
test.assert_equals(game.get_position(coord3), "x")
close_it()

test.it("Cannot place a stone on an existing stone. Raises an error.")
game = Go(19)
[coord, coord2] = _helperFuncs.generate_coords(2)

game.move(coord, coord2)
test.expect_error(coord + " should be an invalid move", lambda: game.move(coord))
test.expect_error(coord2 + " should be an invalid move", lambda: game.move(coord2))
close_it()

test.it("Cannot place a stone with out of bounds coordinates. Raises an error.")
test.expect_error("3Z should be an invalid move", lambda: game.move('3Z'))
test.expect_error("66 should be an invalid move", lambda: game.move('66'))
close_it()
close_describe()


test.describe("Capturing")
test.it("Black captures single white stone")
game = Go(9)
moves = ["4D","3D","4H","5D","3H","4C","5B","4E"]
game.move(*moves)
test.assert_equals(game.get_position('4D'), ".")
close_it()

test.it("Black captures multiple white stones")
game = Go(9)
moves = ["6D","7E","6E","6F","4D","5E","5D","7D",
         "5C","6C","7H","3D","4E","4F","3E","2E",
         "3F","3G","2F","1F","2G","2H","1G","1H",
         "4C","3C","6H","4B","5H","5B"]
captured = ["6D", "6E", "4D", "5D", "5C", "4E", "3E","3F","2F","2G","1G","4C"]
game.move(*moves)
for capture in captured:
    test.assert_equals(game.get_position(capture), ".")
close_it()

test.it("Corner capture")
game = Go(9)
moves = ["9A","8A","8B","9B"]
game.move(*moves)
test.assert_equals(game.get_position('9A'), ".")
close_it()

test.it("Multiple captures")
game = Go(9)
moves = ["5D","5E","4E","6E","7D","4F","7E","3E","5F","4D",
         "6F","6D","6C","7F","4E","5E"]
captured = ["4E","6D","6E"]
game.move(*moves)  
for capture in captured:
    test.assert_equals(game.get_position(capture), ".")
close_it()

test.it("Snapback")
game = Go(5)
moves = ["5A","1E","5B","2D","5C","2C","3A",
         "1C","2A","3D","2B","3E","4D","4B",
         "4E","4A","3C","3B","1A","4C","3C"]
captured = ["4A","4B","4C","3B"]
game.move(*moves)
for capture in captured:
    test.assert_equals(game.get_position(capture), ".")
close_it()

test.it("Self-capturing throws an error.")
game = Go(9)
moves = ["4H","8A","8B","9B","9A"]
test.expect_error("self capturing moves are illegal", lambda: game.move(*moves))
test.assert_equals(game.get_position("9A"), ".", "Illegal stone should be removed")
game.move("3B")
test.assert_equals(game.get_position("3B"), "x", "Black should have another try")
close_it()
close_describe()




test.describe("KO Rule")
test.it("Illegal KO by white")
game = Go(5)
moves = ["5C","5B","4D","4A","3C","3B",
         "2D","2C","4B","4C","4B"]
test.expect_error("Illegal KO move. Should throw an error.", lambda: game.move(*moves))
game.move("2B")
test.assert_equals(game.get_position("2B"), "x", "Black should be given another try to place their stone.")
test.assert_equals(game.get_position("4B"), ".", "Should rollback game before illegal move was made.")
close_it()

test.it("Illegal KO in corner by black")
game = Go(5)
moves = ["4B","3C","4C","2D","2E",
         "1C","1D","1E","1D"]
test.expect_error("Illegal KO move. Should throw an error.", lambda: game.move(*moves))
game.move("3B")
test.assert_equals(game.get_position("3B"), "x", "Black should be given another try to place their stone.")
test.assert_equals(game.get_position("1D"), ".", "Should rollback game to before illegal move was made.")
close_it()
close_describe()




test.describe("Handicap stones")
test.it("Three handicap stones on 9x9")
game = Go(9)
finalBoard = [[ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', 'x', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', 'x', '.', '.', '.', 'x', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ]]

game.handicap_stones(3)
test.assert_equals(game.board, finalBoard)
close_it()

test.it("Handicap stones on 13x13")
handicaps = ["10K","4D","4K","10D","7G","7D","7K","10G","4G"]
for i, a in enumerate(handicaps):
    game = Go(13)
    game.handicap_stones(i+1)
    test.assert_equals(game.get_position(a), "x")
    test.assert_equals(str(game.board).count("x"), i+1)
close_it()

test.it("Handicap stones on 19x19")
handicaps = ["16Q","4D","4Q","16D","10K","10D","10Q","16K","4K"]
for i, a in enumerate(handicaps):
    game = Go(19)
    game.handicap_stones(i+1)
    test.assert_equals(game.get_position(a), "x")
    test.assert_equals(str(game.board).count("x"), i+1)
close_it()

test.it("Board is not 9x9, 13x13, or 19x19")
game = Go(22)
test.expect_error("Expected an error to be raised.", lambda: game.handicap_stones(5))
close_it()

test.it("Handicap stone amount is more than allowed")
game = Go(19)
test.expect_error("Expected and error raised with too many handicap stones.", lambda: game.handicap_stones(200))
close_it()

test.it("Placing handicap stones twice in a row is not valid")
game = Go(19)
game.handicap_stones(5)
test.expect_error("Expected an error thrown when setting handicap stones", lambda: game.handicap_stones(5))
close_it()

test.it("Handicap stones can be updated after board is reset")
game = Go(9)
game.handicap_stones(5)
game.reset()
finalBoard = [[ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', 'x', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', 'x', '.', '.', '.', 'x', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
              [ '.', '.', '.', '.', '.', '.', '.', '.', '.' ]]
                      
game.handicap_stones(3);
test.assert_equals(game.board, finalBoard)
close_it()

test.it("Handicap stones cannot be initialized after moves have been made")
game = Go(19)
game.pass_turn()
game.pass_turn()
test.expect_error("Expected error to be raised", lambda: game.handicap_stones(6))
close_it()
close_describe()

test.describe("Professional Games")
test.it("Takemiya Masaki 9p (Black) vs. Okada Shinichiro")
game = Go(19)
finalBoard = [[".",".",".",".","o","o","x",".","x","x","o",".","o",".",".",".",".",".","."],
             [".",".",".",".","o","x",".","o","x","o",".","o",".","o","o",".",".",".","."],
             [".",".",".",".","o","x","x","x","x","o","o","o","o","x","o",".","o",".","."],
             [".",".",".","o","o","o","o","x","x","o","x","x","x","x","o","x","o","o","."],
             [".",".",".",".","x","o","x","x",".","x",".",".",".",".","x","o","o","o","o"],
             [".","o",".","o","o","o","o","x",".",".",".",".",".","x",".","x","o","x","x"],
             [".","x","o","x","x","x","x","x",".",".",".",".",".",".","x","x","x",".","x"],
             [".","o",".","o","x",".","x",".",".",".",".",".","o","o","x","x",".","x","."],
             [".",".","o",".","o","o","o","x",".",".",".","o","x","x","x","x","x","o","."],
             [".",".","o",".","o","x","x","x",".",".","x","x","o","x","x","o","o","o","."],
             [".",".",".","o","o","o","o","x",".","o","o","x","o","o","o",".","o","x","o"],
             [".",".","o","x","x","o","x","o",".","x","x","o","o",".","o","o","o","x","o"],
             [".",".","o","o","x","x","x",".","x",".",".","x","o",".","o","x","x","x","."],
             [".",".","o","x","x",".",".",".",".","x","x","x","o","o","x",".",".",".","x"],
             [".",".","o","x","o","x","x",".","x",".","x",".","o","x","x","x","x","x","."],
             [".",".","x","o","o","o","x",".","x","x","o","o",".","o",".","x","x",".","."],
             [".",".","o",".","o","x","x","o","o","o","x","x","o","o","x","x",".","x","."],
             [".",".",".","o","o","x",".","x","x","x","x","x","x","o","o","o","x",".","."],
             [".",".",".","o","x","x",".",".",".","x","o","o","o","o",".","x",".",".","."]]
     
moves = ["16Q","16D","4Q","4D","3F","6C","4J","14R","17O",
         "16S","17F","14D","16J","17R","13P","3O","13R",
         "13S","14S","12R","13Q","15S","3M","6Q","3P","4O",
         "5P","4M","3L","3R","4R","2P","3Q","2Q","2R","6O",
         "2N","2O","3S","7N","12C","10C","12E","13C","13B",
         "14B","13F","12B","9M","9O","11N","17L","16M","10E",
         "10F","9F","10G","16G","17G","16F","16H","14G","13H",
         "9G","9H","17E","15E","16E","14H","8H","10H","4F","4G",
         "3E","5F","4E","3G","12D","8G","9E","6P","7P","7Q","8P",
         "7R","8R","10P","11P","10O","6R","7S","6S","8S","9R",
         "9S","10S","12S","10Q","13T","18P","5S","8Q","5Q",
         "9N","10M","8M","5O","5N","6M","6N","8L","7L","7M",
         "8N","6L","7K","6K","10N","11O","9P","11Q","17P",
         "11R","10R","7G","4L","4K","17M","16N","16P","14O",
         "17N","16L","17K","16O","18O","7E","7D","2F","2E",
         "15P","11S","12Q","11E","18J","11F","12G","18E",
         "6E","9T","5R","15Q","8D","8C","8E","9D","6D","7C",
         "18F","19F","19G","19E","17J","3N","1E","1D","1F",
         "2D","2M","18K","19K","19L","19J","8F","7F","3K",
         "2K","8T","6T","14F","13E","11G","11H","14E","13G",
         "5K","5L","3J","5J","1L","2J","1N","2L","1M","19M",
         "18M","18L","9L","8K","19L","13D","11C","18L","11M",
         "10L","19L","15R","16R","18L","12O","12P","19L","14Q",
         "15R","18L","12N","11P","19L","5D","5C","18L","18H",
         "17H","19L","1K","1O","18L","3H","2H","19L","4C","3C",
         "18L","9K","7J","19L","15H","19N","15G","15F","1Q",
         "16K","15K","5E","5G","15T","14T"]

game.move(*moves)
test.assert_equals(game.board, finalBoard)
close_it()

test.it("Lee Sedol 9p (White) vs. AlphaGo Game 4")
game = Go(19)
finalBoard = [[".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."],
            [".",".",".",".","x",".",".",".","o",".","o",".",".","x",".",".",".",".","."],
            [".",".",".","x",".","x",".","x",".","o","x","o","o","x",".",".",".",".","."],
            [".",".","x",".","x","o","x","x","o",".","x",".","x","x",".","x",".","x","."],
            [".",".",".",".","o","o","o","x","o",".",".",".","x","o","x",".",".",".","x"],
            [".",".",".","x",".","o","x","x","o",".",".","x","o","o","x",".","x","x","o"],
            [".","o","o","x","o","o","x","x",".","o",".",".","x","o",".","x","o","o","o"],
            ["x","x","x","o","o","x","o",".","o","o","x","x","x","o","x",".","x","o","."],
            ["o",".","o",".","o","x","o",".","o","x",".","x","o",".","o","o","o",".","."],
            [".","o","o","o","x","x",".","x","o","x","x","o","o","o",".",".","o","o","o"],
            ["o","x","x","x",".","x","x","o","o",".","x",".","o","o","o",".",".",".","."],
            [".","o","x",".",".","x","o",".",".","o","x",".","x","o",".","o","o","o","o"],
            [".",".",".",".",".",".","o",".","x",".","x",".",".",".","o",".",".",".","."],
            [".","x","x","x","x",".",".","o","x",".",".",".",".",".",".",".",".",".","."],
            [".",".","o",".","o","o","o","x",".",".",".",".",".",".","x","o",".",".","."],
            [".","o",".","o","x","o",".","o",".","o",".",".","x",".","x",".","o",".","."],
            [".",".","o",".",".","o",".",".","x",".",".",".",".","x","o","o",".",".","."],
            [".",".",".",".","o","x","x",".",".",".",".",".",".",".","x","x","o",".","."],
            [".",".",".","o","x",".",".",".",".",".",".",".",".",".",".",".","x","o","."]]

moves = ["16Q","4D","16C","4R","4P","3P","3O","3Q","6C","3F","4N",
         "5Q","3J","17E","16H","13C","16E","10C","17D","4B","17O",
         "11R","4E","5E","9D","4F","9C","10D","10E","11E","11F",
         "12E","12F","10B","9F","13F","13G","14F","14G","17N","16N",
         "17M","18O","16J","17H","13K","10Q","11Q","10P","11P","11O",
         "12O","12N","13O","13N","11N","10O","14N","11M","15O","16O",
         "10N","14M","9N","15N","14O","12M","10R","9L","9J","11K",
         "12G","10H","15G","15H","16F","17F","11L","10K","10M","12L",
         "12K","8N","9O","8P","9P","9Q","8Q","9R","8O","10L","11J",
         "9S","7P","13Q","8R","4C","5C","15P","8S","9T","10S","13H",
         "10J","7L","11G","10F","8K","8L","8G","8F","7G","12C","15E",
         "18E","13B","13D","13E","6E","5F","14D","12D","7J","9H",
         "6B","14J","16G","15F","14H","12J","12B","11C","5H","5G",
         "2P","13S","6D","3C","2Q","2R","14S","13R","14R","17K","2G",
         "14T","15T","13T","16S","8B","9B","9A","8C","6H","6J","4H",
         "2F","2E","1E","1D","12A","11A","16L","15J","17L","18L",
         "9G","18J","12R","12S","1R","1S","12P","8T","14P","10T","11O",
         "10O","5P","4K"]

game.move(*moves)
test.assert_equals(game.board, finalBoard)
close_it()
close_describe()




test.describe("Rollback, Reset, and Passing")
test.it("Can rollback a set number of turns")
game = Go(19)
board = _helperFuncs.create_board(19,19)
game.move(*_helperFuncs.generate_coords(3))
game.rollback(3)
test.assert_equals(game.board, board)
test.assert_equals(game.turn, "black")
close_it() 

test.it("Can reset the board")
game = Go(19)
board = _helperFuncs.create_board(19,19)
game.move(*_helperFuncs.generate_coords(3))
game.reset()
test.assert_equals(game.board, board)
test.assert_equals(game.turn, "black")
close_it()

test.it("Can pass turn")
game = Go(9)
game.pass_turn()
coord = _helperFuncs.generate_coord(9)
game.move(coord)
test.assert_equals(game.get_position(coord), "o")
close_it()

test.it("Correct turn after multiple rollbacks")
game = Go(9)
game.move(*["5C","5G","4D"])
test.assert_equals(game.turn, "white")
game.rollback(2)
test.assert_equals(game.turn, "white")
game.move(*["8F","5G","1A"])
test.assert_equals(game.turn, "black")
game.rollback(3)
test.assert_equals(game.turn, "white")
close_it()

test.it("Rollback after reset raises an error")
game = Go(9)
game.move(*_helperFuncs.generate_coords(9, True, 9, 9))
game.reset()
test.expect_error("rollback is not valid", lambda: game.rollback(1))
close_it()

test.it("Rollback more than amount of moves raises an error")
game = Go(9)
game.move(*_helperFuncs.generate_coords(9, True, 9, 9))
game.reset()
numMoves = randint(5,25)
game.move(*_helperFuncs.generate_coords(numMoves, True, 9, 9))
test.expect_error("rollback is not valid", lambda: game.rollback(numMoves + 1))
close_it()

test.it("White can recapture after KO and rollback")
game = Go(9)
moves = ["5C","5B","4D","4A","3C","3B",
         "2D","2C","4B","4C","4B"]
test.expect_error("Illegal KO", lambda: game.move(*moves))
game.rollback(1)
game.move("4C")
test.assert_equals(game.get_position("4C"), "o")
close_it()

test.it("Turn should be white after pass, move, and rollback")
game = Go(9)
game.pass_turn()
game.move("1A")
game.rollback(1)
test.assert_equals(game.turn, "white")
close_it()
close_describe()




test.describe("Misc")
test.it("Can get board size")
height = randint(5,20)
width = randint(5,20)
game = Go(height, width)
test.assert_equals(game.size, {"height": height, "width": width})
close_it()

test.it("Can get color of current turn")
game = Go(9)
game.move("3B")
test.assert_equals(game.turn, "white")
game.move("4B")
test.assert_equals(game.turn, "black")
close_it()
close_describe()


class Check:
    class HG:
        def __init__(self, x, y):
          self.height = x
          self.width = y
          self.board = [['.' for i in range(y)] for u in range(x)]
          self.letters = list("ABCDEFGHJKLMNOPQRSTUVWXYZ")
          self.color = "x"
          self.board_history = [(copyBoard(self.board), self.color)]
          self.size = {"height":x, "width":y}
            
        def conv_coord(self, coord):
          coord = re.findall(r'[A-Z]+|[0-9]+', coord)
          col   = self.letters.index(coord[1])
          row   = len(self.board) - int(coord[0])
          return [row, col]
        
        def move(self, *coords):
          for coord in coords:
            [row, col] = self.conv_coord(coord)
            
            if self.get_position(coord) != ".": raise Exception("Invalid Move")
            self.board[row][col] = self.color
            self.check_captures(coord)
            
            if len(self.get_liberties([row, col],[], [])[0]) == 0: 
                self.board[row][col] = "."
                raise Exception("Illegal suicide Move")
            elif len(self.board_history) >= 2 and self.board_history[-2][0] == self.board:
                self.rollback(1)
                raise Exception("Illegal KO", self.board_history[-2][0], self.board)
            else:
                self.color = "o" if self.color == "x" else "x"
                self.board_history.append((copyBoard(self.board), self.color))
                
        def reset(self):
            self.rollback(len(self.board_history)-1)
            self.color = "x"
        
        def pass_turn(self):
            self.color = "o" if self.color == "x" else "x"
            self.board_history.append((copyBoard(self.board), self.color))
        
        def rollback(self, count):
            if self.board == self.board_history[-1][0]: count += 1
            self.board = self.board_history[-count][0]
            self.color = self.board_history[-count][1]
            #self.color = "o" if str(self.board).count("x") > str(self.board).count("o") else "x" 
            self.board_history = copyHistory(self.board_history[:(len(self.board_history) - count) + 1])
            
        def get_suroundings(self, coord):
          [row, col] = self.conv_coord(coord)
          return [[row-1,col],[row+1,col],[row,col-1],[row,col+1]]
          
        def get_liberties(self, coord, liberties, friendly):
          [row, col] = coord
          friendly.append(coord)
          suroundings = [[row-1,col],[row+1,col],[row,col-1],[row,col+1]]
          for surounding in suroundings:
            suroundingPos = self.get_position(surounding, False)
            if suroundingPos == ".":
              liberties.append(surounding)
            elif suroundingPos == self.get_position(coord, False):
              if not surounding in friendly:
                [surLibs, surFriends] = self.get_liberties(surounding,[],friendly)
                liberties = liberties + surLibs
                friendly = friendly + surFriends
          
          return [liberties, friendly]
          
        def check_captures(self, coord):
          suroundings = self.get_suroundings(coord)
          for surounding in suroundings:
            suroundingPos = self.get_position(surounding, False)
            if suroundingPos != None and suroundingPos != self.color:
              [liberties, friendly] = self.get_liberties(surounding, [], [])
              if len(liberties) == 0:
                for friend in friendly:
                  self.board[friend[0]][friend[1]] = "."
        
        def get_position(self, coord, raw = True):
          if raw == True: [row, col] = self.conv_coord(coord)
          else: [row, col] = coord
          if row >= 0 and col >= 0 and col < self.width and row < self.height: return self.board[row][col]
          
    def random_check(self, height, width = None):
      if width == None: width = height
      game = Go(height, width)
      moves = _helperFuncs.generate_coords(270, False, height, width)
      for x in range(0,1): moves[randint(0,len(moves) - 1)] = "reset"
      for x in range(0,3): moves[randint(0,len(moves) - 1)] = "rollback"
      for x in range(0,2): moves[randint(0,len(moves) - 1)] = "pass"
          
      testBoard = self.HG(height, width)
      
      numMoves = 0
      for move in moves:
          if move == "reset":
              numMoves = 0
              testBoard.reset()
              game.reset()
              continue
          elif move == "rollback":
              if(numMoves > 20): rollbackMax = 20
              else: rollbackMax = numMoves
              if rollbackMax == 0: continue
              rollbackAmount = randint(1,rollbackMax)
              numMoves -= rollbackAmount
              testBoard.rollback(rollbackAmount)
              game.rollback(rollbackAmount)
              continue
          elif move == "pass":
              numMoves += 1
              testBoard.pass_turn()
              game.pass_turn()
              continue
          else:
              try:
                  testBoard.move(move)
              except:
                  test.expect_error("Should throw error", lambda: game.move(move))
                  continue
              game.move(move)
              numMoves += 1
      
      test.assert_equals(game.board, testBoard.board)
      

check = Check()
test.describe("Random Tests")
test.it("Can pass random tests (random sized)")
for x in range(0, 125):
    height = randint(4,20)
    width = randint(4,20)
    check.random_check(height, width)
