Wrapping a paper net onto a cube
This Kata is about wrapping a net onto a cube, not folding one into a cube. There is another kata for that task.
Think about how you would fold a net into a cube. You would fold at the creases of the net at a 90 degree angle and make a cube. Wrapping a net onto a cube is simalar to folding one.

For example the grey net can cover a cube entirely when folded, with one square on each face.
However things are not always perfect. If we use the red net, we still can entirely wrap the net around a cube. But there is one face of the cube having two squares overlaping each other, i.e. squares A and E.

The green and blue nets can't fully cover a cube, but it still can wrap onto a cube. All the folding is 90 degree along edges of the squares. In the 3D demontration of the green net below, squares A, F, E, and G overlap.But some nets can't be wrapped around a cube without folding inside a square or cutting an edge open, like the yellow net.

Task
Create function wrap_cube that uses a net, given as a string, to determine which squares of the net overlap when folded onto a cube. If the net cannot be folded onto a cube without being changed, return None.

The input net will be a string. Spaces are empty parts, each char (case sensitive, including numbers) represents one square on the net.

  Ex.1    |    Ex.2    |    Ex.3
          |            |
   E      |    A F     |    0 9
  ABCDE   |    BCD     |    8AB
   G      |    E G     |    a b
The red net above could be inputed as a string of Example 1. The green net can be represented as example 2 or 3.

If a net can't be wrapped onto a cube without being cut, return None. If it can, return a list of overlapping squares. For example the output of Example 1 above is [['A', 'E']]. The output of the Example 2 could be [["A", "F"], ["E", "G"]]. Your final asnswer does not have to be sorted, it can be in any order. You may find out more in the example test code.

Notes:
Use common sense to fold the net, only at 90 degree angles along the edges;
No 180 degree folding, no cutting, no folding inside a square;
For some huge nets, ignore the thickness of paper...
All the input chars will be connected; but some trailing spaces may be stripped;
There will be 500 large random nets in the test, each of which has >60 squares; but there are some easier tests too
Not all 6 faces of the cube need be covered
There are no repeating chars in a net, and only one char is only one square
The sequence of the chars and lists is not important; test code will sort your answer.
One more example:
The input string could like this:

"""
ABCDE
"""
It's a stripe of paper with 5 squares side by side. If wrap this stripe around a cube, four faces will be covered. Two faces on the cube won't be covered, which is fine in this kata. The squares at the very two ends, A and E, will overlap. So the expected output of this net is [ [ "A" , "E" ] ]

Beta Note: I "manually" checked not-so-large nets with my code. It should be able to handle huge nets. But if you found any erros in my expected answers, please let me know. thanks.
