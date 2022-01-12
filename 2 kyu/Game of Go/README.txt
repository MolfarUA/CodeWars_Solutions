Description
In this challenge, you will be creating a go board that users can play a game of go on. An understanding of the rules of go should be sufficient enough to complete this kata.

The main goals for this kata:

Creating a go board to a specific size.
Placing go stones on the board. (White and Black alternating).
Capturing stones and removing them from the board.
Catching invalid moves (throw an IllegalArgumentException in Java).
Placing Handicap stones.
Scoring is not covered in this kata.

Details
Creating a board
Outputting the board after it has been created should return an array of arrays filled with dots (representing empty spaces).

game = Go(9)
game.board
output
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
Placing stones on board
When given valid coordinates (one or several arguments, see example tests) the program should place either a white stone o or a black stone x in the correct position.

Note that the letter I is omitted from possible coordinates.

game.move('7A')
game.move('1A')
game.board
output
  A B C D E F G H J
9 . . . . . . . . .
8 . . . . . . . . .
7 x . . . . . . . .
6 . . . . . . . . .
5 . . . . . . . . .
4 . . . . . . . . .
3 . . . . . . . . .
2 . . . . . . . . .
1 o . . . . . . . .
Capturing
liberties
As a side note, to understand capturing you need to understand the concept of liberties. They are the spaces surounding a stone/stones that are not out of bounds and are not occupied by the opponents stones. Take a look at these examples.

Black has 4 liberties     Group of black has 5 liberties
. . . . . . . . .         . . . . . . . . .
. . . . . . . . .         . . . . . . . . .
. . . . . o . . .         . . . . o . . . .
. . . 1 . . . . .         . . . 1 o . . . .
. . 2 x 4 . . . .         . . 2 x x o . . .
. . . 3 . . . . .         . . . 3 x 5 . . .
. . . . . . . . .         . . . . 4 . . . .
. . . . . . . . .         . . . . . . . . .
. . . . . . . . .         . . . . . . . . .  
When a group of white or black stones has no more liberties the group should be removed from the board. Take this board for example.

. x o o o o o . .
. x o o o o o x .
. . x o o o x . .
. . . x o o x . .
. . x . x x . . .
. . . . . . . o .
. . x . . . . . .
. . . x . . o . .
. . . . . . . . .
Calling game.move('9H'); will remove the white stones from the board.

. x . . . . . x .
. x . . . . . x .
. . x . . . x . .
. . . x . . x . .
. . x . x x . . .
. . . . . . . o .
. . x . . . . . .
. . . x . . o . .
. . . . . . . . .
Self-capturing
Placing a white stone on the 1 below would be an illegal move.

. x o o o o o 1 x
. x o o o o o x .
. . x o o o x . .
. . . x o o x . .
. . x . x x . . .
. . . . . . . o .
. . x . . . . . .
. . . x . . o . .
. . . . . . . . .
Invalid moves
Simple Ko Rule should be implemented (One may not play in such a way as to recreate the board position following one's previous move).
Self-capturing (suicide) is illegal.
Cannot play out of bounds.
Cannot place a stone on another stone.
KO Rule
To further explain the KO rule, take a look at these go boards.

. . o . o x . . .   . . o x . x . . .   . . o . o x . . .
. . . o x . . . .   . . . o x . . . .   . . . o x . . . .
. . . . . . . . .   . . . . . . . . .   . . . . . . . . .
. . . . . . . . .   . . . . . . . . .   . . . . . . . . .
. . . . . . . . .   . . . . . . . . .   . . . . . . . . .
. . . . . . . . .   . . . . . . . . .   . . . . . . . . .
. . . . . . . . .   . . . . . . . . .   . . . . . . . . .
. . . . . . . . .   . . . . . . . . .   . . . . . . . . .
. . . . . . . . .   . . . . . . . . .   . . . . . . . . .
Move 1              Move 2              Move 3 (Illegal)
These moves could loop over and over again. That is why move 3 is illegal according to simple KO rule, because it recreates the same board as the board after the previous move by white (move 1).

Note : If any illegal move is attempted, an error should be thrown and the board rolled back to the previous board before the illegal move. That player will have another chance to place their stone.

Handicap stones
Handicap stones are used to make a game more fair when two players of different ranks play.

The order of handicap stones (least to greatest).

9x9                13x13
. . . . . . . . .  . . . . . . . . . . . . .
. . . . . . . . .  . . . . . . . . . . . . .
. . 4 . . . 1 . .  . . . . . . . . . . . . .
. . . . . . . . .  . . . 4 . . 8 . . 1 . . .
. . . . 5 . . . .  . . . . . . . . . . . . . 
. . . . . . . . .  . . . . . . . . . . . . .
. . 2 . . . 3 . .  . . . 6 . . 5 . . 7 . . .
. . . . . . . . .  . . . . . . . . . . . . .
. . . . . . . . .  . . . . . . . . . . . . .
                   . . . 2 . . 9 . . 3 . . .
                   . . . . . . . . . . . . .
                   . . . . . . . . . . . . . 
                   . . . . . . . . . . . . .
                   
19x19
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . 4 . . . . . 8 . . . . . 1 . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . 6 . . . . . 5 . . . . . 7 . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . 2 . . . . . 9 . . . . . 3 . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . .
This next example should place 3 handicap stones on a 19x19 board in the correct order mentioned above.

game = Go(19)
game.handicap_stones(3)
Invalid handicap usage
Handicap stones can only be placed on 9x9, 13x13 and 19x19 boards. Throw an error otherwise.
A player cannot place down handicap stones after the first move has been made or handicap stones have already been placed. Throw an error if this happens.
Placing too many handicap stones for a given board should throw an error.
Breakdown of a turn
For clarity, let's go over the general flow of each turn throughout the game.

After a player makes a move, all opponent stones without liberties should be captured and removed from the board.
Check to make sure a move is valid before proceeding. A player should not be able to make a move that will result in the loss of their stones due to lack of liberties (Suicide). The board also shouldn't be identical to the one after the previous move made by the same player (KO Rule).
Rollback and let the player try again if a move is illegal.
Additional functionality
size
Given this new game.

game = Go(9,6)
When game.size (game.getSize() in java) is called, it should return a mapping {"height": 9, "width": 6}.

rollback
User should be able to rollback a set amount of turns on the go board.

get position
User should be able to get status of a particular position on the board (x, o, or .).

game.get_position("1A") # x, o, or .
turn
Get the current turn color.

game.turn # "black"
game.pass_turn()
game.turn # "white"
reset
Resetting the board should clear all of the stones from it and set the turn to "black".

pass
User should be able to pass their turn.

Note : Passing should count as a turn, so rollbacks need to account for this.

Language Specifics
Python

Methods are in snake case (function_name).
Creating a game does not need new.
The pass method is pass_turn.
JavaScript, Coffeescript & Java

Methods are in camel case (functionName).

59de9f8ff703c4891900005c
