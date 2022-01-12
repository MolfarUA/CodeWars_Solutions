

    When no more interesting kata can be resolved, I just choose to create the new kata, to solve their own, to enjoy the process --myjinxin2015 said

Task

We have a rectangular cake with some raisins on it:

cake = 
  ........
  ..o.....
  ...o....
  ........
// o is the raisins

We need to cut the cake evenly into n small rectangular pieces, so that each small cake has 1 raisin. n is not an argument, it is the number of raisins contained inside the cake:

cake = 
  ........
  ..o.....
  ...o....
  ........
 
result should be an array:
  [
     ........
     ..o.....
  ,
     ...o....
     ........
  ]
// In order to clearly show, we omit the quotes and "\n"

If there is no solution, return an empty array []
Note

    The number of raisins is always more than 1 and less than 10.
    If there are multiple solutions, select the one with the largest width of the first element of the array. (See also the examples below.)
    Evenly cut into n pieces, meaning the same area. But their shapes can be different. (See also the examples below.)
    In the result array, the order of pieces is from top to bottom and from left to right (according to the location of the upper left corner).
    Each piece of cake should be rectangular.

Examples

    An example of multiple solutions:

cake = 
  .o......
  ......o.
  ....o...
  ..o.....

In this test case, we can found three solution:
solution 1 (horizontal cutting):
  [
    .o......  //piece 1
  ,
    ......o.  //piece 2
  ,
    ....o...  //piece 3
  ,
    ..o.....  //piece 4
  ]

solution 2 (vertical cutting):
  [
    .o  //piece 1
    ..
    ..
    ..
  ,
    ..  //piece 2
    ..
    ..
    o.
  ,
    ..  //piece 3
    ..
    o.
    ..
  ,
    ..  //piece 4
    o.
    ..
    ..
  ]
  
solution 3 (cross cutting):
  [
    .o..  //piece 1
    ....
  ,
    ....  //piece 2
    ..o.
  ,
    ....  //piece 3
    ..o.
  ,
    o...  //piece 4
    ....   
  ]

we need choose solution 1 as result

    An example of different shapes:

cake = 
  .o.o....
  ........
  ....o...
  ........
  .....o..
  ........

the result should be:
  [
    .o      //pieces 1
    ..
    ..
    ..
    ..
    ..
  ,
    .o....  //pieces 2
    ......
  ,
    ..o...  //pieces 3
    ......
  ,
    ...o..  //pieces 4
    ......   
  ]
Although they have different shapes, 
they have the same area(2 x 6 = 12 and 6 x 2 = 12).

    An example of no solution case:

cake = 
  .o.o....
  .o.o....
  ........
  ........
  ........
  ........
the result should be []


586214e1ef065414220000a8
