<><><><><><><>BETA<><><><><><><><>

In this kata, you have to implement two functions: isCheck and isMate.

Both of the functions are given two parameters: player signifies whose turn it is (0: white, 1: black) and pieces is an array of objects (PHP: Array of associative arrays) describing a piece and its location in the following fashion:

{
  'piece': string, # pawn, rook, knight, bishop, queen or king
  'owner': int,    # 0 for white or 1 for black
  'x': int,        # 0-7 where 0 is the leftmost column (or "A")
  'y': int,        # 0-7 where 0 is the top row (or "8" in the board below)
  'prevX': int,    # 0-7, presents this piece's previous x, only given if this is the piece that was just moved
  'prevY': int     # 0-7, presents this piece's previous y, only given if this is the piece that was just moved
}

Top (meaning y equals 0 or 1) is black's home and the bottom (y equals 6 or 7) is white's home, so the initial board looks like this (the numbers in the parentheses correspond to those used in the pieces objects fields):
	(0)
A	(1)
B	(2)
C	(3)
D	(4)
E	(5)
F	(6)
G	(7)
H
(0) 8	♜	♞	♝	♛	♚	♝	♞	♜
(1) 7	♟	♟	♟	♟	♟	♟	♟	♟
(2) 6								
(3) 5								
(4) 4								
(5) 3								
(6) 2	♙	♙	♙	♙	♙	♙	♙	♙
(7) 1	♖	♘	♗	♕	♔	♗	♘	♖

Note: if you do not see correctly the pieces on the board, please install the "Deja Vu Sans" font.
You can assume that the input is a valid chess position. The pieces are not in any particular order.

isCheck should return an array of the objects that threaten the king or false if not threatened (Java: return a Set<Piece> object of the threatening pieces, or an empty set if none are found). (PHP: return an array of associative arrays, false if none are found.)

isMate should return true if the player can't make a move that takes his king out of check, and false if he can make such a move, or if the position is not a check.

To help with debugging, a function outputBoard(pieces) (Java: static method OutputBoard.print(pieces), PHP: outputBoard($pieces), C#: static method void Figures.OutputBoard(IList<Figure> figures)) is provided and will log to console the whole board with all pieces on it. The piece with prevX and prevY properties will appear light gray on the board in the coordinates it used to occupy (Python currently does not support unicode chess symbols, so the standard piece abbreviations KPNBRQ are used. Same representation is used in Java and PHP).

A comprehensive list of how each piece moves can be found at http://en.wikipedia.org/wiki/Chess#Movement.

Note 1: these functions should work in a noninvasive fashion - don't change the contents of the array or values of the pieces contained within it.

Note 2: the tests might not imply explicitly why a certain position is or isn't a check or mate. If your code fails a test, you have to be able to analyze the situation and see which pieces are to blame. If all else fails, try asking for help at the discussion board.


52fcc820f7214727bc0004b7
