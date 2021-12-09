You are given an assortment of rectangular pieces and a square board with holes in it. You need to arrange the pieces on the board so that all the pieces fill up the holes in the board with no overlap.

Input
Your function will receive two arguments:

board : an array/list of length n where each element is a string of length n consisting of 0s and/or spaces. Each contiguous cluster of 0s represents a hole in the board.
pieces : an array/list where each element is in the form [h,w] where h and w represent the height and width of each piece, respectively.
Output
An array with the position of each piece to solve the puzzle. Each element should be an array in the form [x,y,z] where:

x and y represents the piece's top-left corner position, as illustrated in the example below
z represents the orientation of the piece -- normal or rotated 90 degrees. If rotated, z is 1, otherwise it's 0
Each piece corresponds to the element from pieces with the same index position
Test Example
Figure A: initial state of the puzzle board.
Figure B: one possible configuration. Note that the number in each rectangle indicates its index in the input array.

example image
board = [
    '            ',
    ' 00000      ',
    ' 00000      ',
    ' 00000   00 ',
    '       000  ',
    '   00  000  ',
    ' 0000 00    ',
    ' 0000 00    ',
    ' 00   000 0 ',
    '      000 0 ',
    '  0       0 ',
    '000         '
]
pieces = [[1,1], [1,1], [1,2], [1,2], [1,2], [1,3], [1,3], [1,4], [1,4], [2,2], [2,2], [2,3], [2,3], [2,5]]

solve_puzzle(board,pieces); # [[11,0,0],[11,1,0],[1,1,0],[3,9,0],[10,2,1],[1,3,0],[8,10,1],[4,7,1],[6,6,1],[4,8,0],[8,7,0],[5,3,1],[6,1,1],[2,1,0]]
Technical Constraints
Each test will have one or more possible solutions
Every piece must be used to solve the puzzle
Every piece is a rectangle with height and width in the range: 12 >= x >= 1
Number of pieces: 70 >= pieces >= 1
n x n board dimensions: 24 >= n >= 4
Full Test Suite: 15 fixed tests, 60 random tests
Efficiency is necessary to pass
JavaScript: prototypes have been frozen and require has been disabled
