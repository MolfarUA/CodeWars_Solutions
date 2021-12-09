Blaine is a pain, and that is the truth - Jake Chambers

Background
Blaine likes to deliberately crash toy trains!

Trains
Trains look like this

Aaaaaaaaaa
bbbB
The engine and carriages use the same character, but because the only engine is uppercase you can tell which way the train is going.

Trains can be any alphabetic character

An "Express" train uses X
Normal suburban trains are all other letters
Tracks
Track pieces are characters - | / \ + X and they can be joined together like this

Straights	
----------
 
|
|
|
\
 \
  \
   /
  /
 /
Corners	
|
|
\-----
     |
     |
-----/
/-----
|
|
-----\
     |
     |
Curves	
-----\
      \-----
      
      /-----
-----/

  |
  /
 /
 |
|
\
 \
 |
Crossings	
   |
---+---
   |
  \ /
   X
  / \
The   +   is like a combined   -   and   |  , so if those separate curves/corners are valid then the combined crossing is also valid. e.g.	
   /
---+---
   |
   /
---+---
   /
   | /
  /+/
 / |
Describing where a train is on the line
The track "zero position" is defined as the leftmost piece of track of the top row.

Other track positions are just distances from this zero position (following the line beginning clockwise).

A train position is the track position of the train engine.

Stations
Train stations are represented by a letter S.

Stations can be on straight sections of track, or crossings, like this

Stations	
----S-----


|
S
|
\
 S
  \
   /
  S
 /
    |
----S----
    |
 \ /
  S
 / \

When a train arrives at a station it stops there for a period of time determined by the length of the train!
The time T that a train will remain at the station is same as the number of carriages it has.

For example

bbbB - will stop at a station for 3 time units
Aa - will stop at a station for 1 time unit
Exception to the rule: The "Express" trains never stop at any station.

Collisions
There are lots of ways to crash trains. Here are a few of Blaine's favorites...

The Chicken-Run - Train chicken. Maximum impact.
The T-Bone - Two trains and one crossing
The Self-Destruct - Nobody else to blame here
The Cabooser - Run up the tail of a stopped train
The Kamikaze - Crash head-on into a stopped train
Kata Task
Blaine has a variety of continuous loop train lines.

Two trains are then placed onto the line, and both start moving at the same time.

How long (how many iterations) before the trains collide?

Input
track - string representation of the entire train line (\n separators - maybe jagged, maybe not trailing)
a - train A
aPos - train A start position
b - train B
bPos - train B start position
limit - how long before Blaine tires of waiting for a crash and gives up
Output
Return how long before the trains collide, or
Return -1 if they have not crashed before limit time has elapsed, or
Return 0 if the trains were already crashed in their start positions. Blaine is sneaky sometimes.
Notes
Trains

Speed...
All trains (even the "Express" ones) move at the same constant speed of 1 track piece / time unit
Length...
Trains can be any length, but there will always be at least one carriage
Stations...
Suburban trains stop at every station
"Express" trains don't stop at any station
If the start position happens to be at a station then the train leaves at the next move
Directions...
Trains can travel in either direction
A train that looks like zzzzzZ is travelling clockwise as it passed the track "zero position"
A train that looks like Zzzzzz is traveliing anti-clockwise as it passes the track "zero position"
Tracks

All tracks are single continuous loops
There are no ambiguous corners / junctions in Blaine's track layouts
All input is valid

Example
In the following track layout:

The "zero position" is /
Train A is Aaaa and is at position 147
Train B is Bbbbbbbbbbb and is at position 288
There are 3 stations denoted by S
                                /------------\
/-----Aaaa----\                /             |
|             |               /              S
|             |              /               |
|        /----+--------------+------\        |
\       /     |              |      |        |      
 \      |     \              |      |        |
 |      |      \-------------+------+--------+---\            
 |      |                    |      |        |   |
 \------+------S-------------+------/        /   |
        |                    |              /    |
        \--------------------+-------------/     |
                             |                   |
/-------------\              |                   |        
|             |              |             /-----+----\      
|             |              |             |     |     \    
\-------------+--------------+-----S-------+-----/      \   
              |              |             |             \
              |              |             |             |
              |              \-------------+-------------/
              |                            |
              \---------Bbbbbbbbbbb--------/

