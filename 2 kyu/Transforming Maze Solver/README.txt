The objective of this kata will be to guide a ball through an m x n rectangular maze. This maze is special in that:

all the cells rotate 90 degrees clockwise, in unison, at each interval
each cell can have anywhere from 0 to 4 walls
Your goal is to write a function that returns a path that requires the fewest intervals for the ball to get from its starting position to a specified destination.

Input
Your function will receive one argument — an m x n matrix.

Output
Your function must return a path as an array/list of strings. Each string in the array will:

consist only of the letters N, W, S, and E representing the directions north, west, south, and east, respectively
represent the path of the ball at each interval (based on its index position in the array)
Also note that empty strings are permitted in the output array.
If there is no possible solution, return null or None.

Maze Mechanics
Each cell in the maze is given as an integer, ranging from 0 to 15. This number, when translated to binary form, represents the walls of the corresponding cell. That is, a 1 means there is a wall and a 0 means there is no wall. The order of the walls is north, west, south, and east.

For example, a cell with the value 7 is 0111 in binary. This means it has 3 walls — initially on the west, south, and east sides. Since there is no wall on the north side of the cell, it can be entered from that side at time interval 0 (assuming that the adjacent cell to its north does not have a south wall).

A cell with the value 5 (0101 in binary) can be entered from its north and south sides at interval 0. At the next interval, it rotates 90 degrees clockwise and can then only be entered from its west and east sides (1010).

A cell with the value 15 is enclosed on all sides (1111 in binary) and therefore can never be entered. Likewise, a cell with a value of 0 can always be entered from any side.

There will be 2 cells that will not be given in the form of an integer. Assume that these cells have no walls (the equivalent of a 0 cell):

The ball's starting position, given as the letter B (Java,Kotlin:-1)
The destination, given as the letter X (Java,Kotlin:-2)
Test Example

The image above shows the state of the maze and starting position of the ball at each each interval; the order is given in the bottom right square.
The green shaded area shows the available cells the ball can move to at each interval, but the bold number shows where it ends up (for our example solution)

example = (
    (  4,  2,  5,  4),
    (  4, 15, 11,  1),
    ('B',  9,  6,  8),
    ( 12,  7,  7,'X')
)

maze_solver(example) # ['NNE','EE','S','SS']
Technical Details
The width and length of the matrix will range between 4 and 25 in either direction
The ball's starting position will always be on the west side and the exit will always be on the east side of the maze
For the sake of efficiency, the ball must not enter the same cell more than once per interval
Full Test Suite: 10 fixed tests, and 110 random tests for Python,Kotlin,Rust / 100 random tests for JavaScript / 200 random tests for Java
Each test case may have 0 or more possible solutions
Inputs will always be valid
Use Python 3+ for the Python translation
For JavaScript, require has been disabled and most built-in prototypes have been frozen (prototype methods can be added to Array, Function, and Set)
If you enjoyed this kata, be sure to check out my other katas

5b86a6d7a4dcc13cd900000b
