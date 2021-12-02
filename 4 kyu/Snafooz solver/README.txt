So I have a few Snafooz puzzles at home (which are basically jigsaw puzzles that are 3d)

http://www.ideagroup.net/products/puzzlesgames/c-1012.html

https://www.youtube.com/watch?v=ZTuL9O_gQpk

and it's a nice and fun puzzle. The only issue is, well, I'm not very good at it... Or should I say not better than my dad.

As you can see this is a big problem which only has one sensible solution... I need to cheat.

The puzzle is made of 6 pieces (each piece is 6x6 array which represents a jigsaw like puzzle piece), each one a side of a cube, and all you need to do is construct the cube by attaching the pieces together kinda like a 3d jigsaw puzzle.

You may rotate, flip and\or reorganize the pieces but not change their shape.

Example:

Let's say these are our pieces-

1:
xx x
xxxxxx
 xxxxx
xxxxxx
xxxxxx
  x xx

2:
  x
 xxxxx
xxxxx
xxxxxx
 xxxx
xxx

3:
xx x
 xxxxx
xxxxxx
 xxxxx
xxxxxx
 x  xx
 
4:

 xxxx
 xxxxx
 xxxx
 xxxx
 x x
 
5:
x xx
xxxxx
xxxxxx
 xxxx
 xxxxx
  xxx
6:
 x   x
xxxxxx
 xxxxx
 xxxx
xxxxxx
  x xx
Our solution would look something like this:

          ----------
          | xx x   | 
          | xxxxxx | 
          |  xxxxx | 
          | xxxxxx | 
          | xxxxxx | 
          |   xx x |
-----------------------------
 |   x    | xx  x  |        |
 |  xxxxx |  xxxxx |  xxxx  |
 | xxxxx  | xxxxxx |  xxxxx |
 | xxxxxx |  xxxxx |  xxxx  |
 |  xxxx  | xxxxxx |  xxxx  |
 | xxx    |  x  xx |  x x   | 
-----------------------------
          | x xx   |
          | xxxxx  |
          | xxxxxx |
          |  xxxx  |
          |  xxxxx |
          |   xxx  |
          ----------
          |  x   x |
          | xxxxxx |
          |  xxxxx |
          |  xxxx  |
          | xxxxxx |
          |   x xx |
          ----------
(this is just a flattened cube)

Here is a pic describing which edges are touching, and need to match (marked by letters), and the matching corners (marked with numbers):

        5aaaa6
        i....h
        i....h
        i....h
        i....h
        1bbbb2

5iiii1  1bbbb2  2hhhh6
g....f  f....e  e....l
g....f  f....e  e....l
g....f  f....e  e....l
g....f  f....e  e....l
7jjjj4  4cccc3  3kkkk8

        4cccc3
        j....k
        j....k
        j....k
        j....k
        7dddd8

        7dddd8
        g....l
        g....l
        g....l
        g....l
        5aaaa6
Bad Example:

Having two pieces next to each other that don't fit-

xxxxxx    xxxxx
xxxxxx   xxxxxx
xxxxxx    xxxxx
xxxxx     xxxxx
xxxxxx    xxxxx
xxxxxx   xxxxxx
or

xxxxxx
xxxxxx
xxxxxx
xxxxxx
xxxxxx
x   xx

 x x x
xxxxxx
xxxxxx
xxxxxx
xxxxxx
xxxxxx
The right way would be like this -

xxxxxx    xxxxx
xxxxx    xxxxxx
xxxxxx    xxxxx
xxxxx    xxxxxx
xxxxx    xxxxxx
xxxxxx    xxxxx
or

xxxxxx
xxxxxx
xxxxxx
xxxxxx
xxxxxx
x x xx

 x x
xxxxxx
xxxxxx
xxxxxx
xxxxxx
xxxxxx
Now all you need to do is use the input which will be a 3d array (6x6x6) where arr[0] is the first piece (which will be a 6 by 6 matrix) arr[1] is the second and so on… And you will return the answer in a new 6x6x6 matrix in which the pieces are all in the right orientation in this order->

  0
1 2 3
  4
  5
NOTES

Each piece is represented by a 6x6 array of numbers: 1s indicate the piece, 0s indicate empty space.

All cases will be solvable

Don't be too conncerned about optimizations (after all my dad isn't THAT fast)

Good Luck!
