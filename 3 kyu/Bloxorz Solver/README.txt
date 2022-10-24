Description:

Above: Game footage from Bloxorz online game

This kata is inspired by Bloxorz, a flash-based 3D puzzle game where the objective is to maneuver a block to have it fall through a square hole.
Objective

Your goal is to maneuver a rectangular cuboid with dimensions 1 x 1 x 2 on a 2-dimensional grid made up of 1 x 1 square tiles. While moving the cuboid around, your block must never, at any point, have any part of its bottom-facing surface exposed to open air.
Input

Your function will receive an array of strings describing the layout of the grid to be traversed. A 1 represents solid ground (tiles), a 0 represents open air, a B represents your starting position, and an X represents the square hole (destination).
Output

Your function must return a string representing the minimum sequence of moves required to get the block into the square hole. It will consist of a combination of the following characters: U (up), D (down), L (left), R (right).
Block Movement

The block can cover either one or two tiles with each movement, depending on whether it is standing upright or on its long end. The image above shows an overhead view; the yellow squares represent the tiles occupied by the block and the green squares represent the tiles occupied when moved toward a given cardinal direction.

In Fig. 1, the block's position is standing upright, and in Fig. 2, the block is on its long end.
Test Example

level1 =
  [ "1110000000"
  , "1B11110000"
  , "1111111110"
  , "0111111111"
  , "0000011X11"
  , "0000001110"
  ]

bloxSolver level1 -- "RRDRRRD" or "RDDRRDR"

An overhead view of the game grid for the example level1 is shown below, with a green square representing the starting position of the block, the red square representing the square hole, the light grey squares representing the platform tiles, and the dark grey areas representing open air:

grid layout of level1

Below is the sequence of moves to solve this map, numbered and highlighted in blue.

sequence of moves for level1

and another possible solution:

alternative sequence of moves for level1
Technical Details

    Input will always be valid and there will always be a solution.
    The block always begins in an upright position.
    The destination exit does not count as open air.
    The maximum grid size will be 15 x 20 (rows x colums)

Games
Puzzles
Game Solvers
Algorithms

5a2a597a8882f392020005e5
