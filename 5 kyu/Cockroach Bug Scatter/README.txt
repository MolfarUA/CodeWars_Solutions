Description:
Story

It was nearly midnight when I staggered sleepily into the kitchen to get a glass of milk...

I turned on the light and...      AARRRGGHHHHH!!!!

Damn bugs scatter in all directions!
animated-cockroach-image-0010

I really hate cockroaches
Kata Task

The cockroaches run and hide in the numbered holes.

Return array/list showing how many cockroaches end up in each hole (index matches the hole number)
Notes

About cockroaches:

    There are 0 or more cockroaches in the room
    Cockroaches firstly run in a straight line in the direction they are facing
    When they hit a wall they always turn LEFT and then they follow the wall until they can find a hole to crawl into!
    Cockroaches do not bump into each other
    There are no cockroaches outside the room

About the room:

    The room is a closed rectangle
    There are 1 or more holes (conveniently numbered by a single digit)
    Hole numbers are random but not repeated

Legend:

    +, |, - = walls of the room
    0 - 9 = holes for cockroaches to hide in
    U,D,L,R = cockroaches with initial directions facing UP, DOWN, LEFT, RIGHT

Example

Input:

+----------------0---------------+
|                                |
|                                |
|          U        D            |
|     L                          |
|              R                 |
|           L                    |
|  U                             1
3        U    D                  |
|         L              R       |
|                                |
+----------------2---------------+

Output:

(always 10 elements)

[1, 2, 2, 5, 0, 0, 0, 0, 0, 0]



59aac7a9485a4dd82e00003e
