Disclaimer
If you're not yet familiar with the puzzle called Nonogram, I suggest you to solve 5x5 Nonogram Solver first.

Task
Complete the function solve(clues) that solves 15-by-15 Nonogram puzzles.

Your algorithm has to be clever enough to solve all puzzles in time.

As in 5x5 Nonogram Solver, the input format will look like this:

input = tuple(column_clues, row_clues)

each of (row_clues, column_clues) = tuple(
  tuple(num_of_ones_in_a_row, ...),
  ...
)
Output
Output is a 2D-tuple of zeros ans ones, representing the solved grid.

Example
Here is the example puzzle in the Sample Test.



Notes
Some puzzles may have lines with no cells filled. Most Nonogram games show the clues for such lines as a single zero, but the clue for such a line is represented as a zero-length tuple for the sake of this Kata.

5a5072a6145c46568800004d
