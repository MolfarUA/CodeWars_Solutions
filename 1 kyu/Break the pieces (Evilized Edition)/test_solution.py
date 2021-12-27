from preloaded import MAX_PIECES_DISPLAY
import codewars_test as test
from solution import break_evil_pieces
try:
    from solution import USE_BREAK_DISPLAY
except:
    USE_BREAK_DISPLAY = True


""" FOR WARRIORS: General parameters of the random tests """
DO_RND_TESTS_FOR_WARRIORS       = True                 # Activate the random tests for the warriors
N_RANDOM_TESTS                  = 110                  # Number of random tests
DISPLAY_RND_TIME                = True                 # Display the duration of the random tests (no interest on codewars website...)

""" HIDDEN controls used to debug the random tests or otherr things (not for the warriors !!) """
DISPLAY_RNDTESTS_SEQUENTIAL     = False                # Make a pause between each random test (press a key to resume. DO NOT USE ON CW!)
DO_INDIVIDUAL_RND_CHECKS        = False                # Test and display the reslut of the individual shapes used for the random checks, with the object below
MAKE_PAUSES                     = False                # Same as above, but make a pause between each test (press a key to resume)
#DO_INDIVIDUAL_RND_CHECKS_WITH   = NewButSlow           # WARNING: Using the complete solution object or the internal one, it can be run on codewars website. But not with the one indicated here

DISPLAY_ALL_GRIDS               = False                # Display the original shape of all the tests



""" Declare again the tests functions to avoid easy cheating.
        Note: Modified version of "runTests", that will execute 2 tests for each shape:
              First on the shape itself, and second on an enclosed with spaces version 
              (used to check thoroughly implementations using setOfSpaces.pop(), that might hide
              wrong behaviour depending on the order in which the spaces are popped).
              Expected solutions HAVE TO BE exactly the same that for the original shape, to use this feature!
"""
def formatStr(s):
    encloseChar = "*"
    lst = s.split('\n')
    return '\n'.join ( "{}{}{}".format(encloseChar,line,encloseChar) for line in [encloseChar * len(lst[0])] + lst + [encloseChar * len(lst[-1])] )

def display(actual, expected):
    actual   = set(actual)
    expected = set(expected)
    diff = actual ^ expected
    
    for i,s in enumerate(sorted(diff, key=lambda s: s in expected)):
        print(" \n" + formatStr(s) )
        
def encloseShapeWithSpaces(shape):
    lines = shape.split('\n')
    maxLen = max(map(len, lines))
    return '\n'.join([" " * (maxLen+2), '\n'.join( " " + line.ljust(maxLen+1, " ") for line in lines), " " * (maxLen+2)])
        

def runTest(name, shape, expected, addMessage ="", encloseWithSpace=True):
    
    if name:
        @test.it(name)
        def _():
            runTest('', shape, expected, addMessage, encloseWithSpace)
        return
            
    if addMessage:  print(addMessage)
    
    for shape in ([shape] if not encloseWithSpace else [shape, encloseShapeWithSpaces(shape)]):
        ans = sorted(break_evil_pieces(shape))
        expected = sorted(expected)
        
        if DISPLAY_ALL_GRIDS: print(formatStr(shape))
        
        if DISPLAY_RNDTESTS_SEQUENTIAL:
            if ans != expected:
                display(ans, expected)
                input("Waiting")
        else:
            if ans != expected:
                
                print(" \n\n FAILED TEST !!!\n\nshape:\n{}\n\nExpected:".format(formatStr(shape)) )
                for s in expected:  print(" \n" + formatStr(s) )
                print(" \n\nBut answer was:")
                
                for i,s in enumerate(ans):
                    if USE_BREAK_DISPLAY and i > MAX_PIECES_DISPLAY:
                        print(" \n(Answer is too long to be fully displayed...)")
                        break
                    print(" \n" + formatStr(s) )
                
                actSet = set(ans)
                expSet = set(expected)
                
                print(" \n\nType of shapes that your answer was missing:")
                for i,s in enumerate(sh for sh in expSet-actSet or [None]):
                    print( " \nNone" if s is None else " \n" + formatStr(s) )
                
                print(" \n\nType of shapes that your solution shouldn't return:")
                for i,s in enumerate(sh for sh in actSet-expSet or [None]):
                    print( " \nNone" if s is None else " \n" + formatStr(s) )
                    
            test.expect(ans == expected, allow_raise=True)
    
    

    
    
    
        
@test.describe("Sample tests")
def _():
    
    
    name = "Simple shape"
    shape = """
+----------+
|          |
|          |
|          |
+----------+
|          |
|          |
+----------+
""".strip('\n')
    
    expected = ["""
+----------+
|          |
|          |
|          |
+----------+
""".strip('\n'), """
+----------+
|          |
|          |
+----------+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "3 boxes"
    shape = """
+------------+
|            |
|            |
|            |
+------+-----+
|      |     |
|      |     |
+------+-----+
""".strip('\n')
    
    expected = ["""
+------------+
|            |
|            |
|            |
+------------+
""".strip('\n'), """
+------+
|      |
|      |
+------+
""".strip('\n'), """
+-----+
|     |
|     |
+-----+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Lego stuff"
    shape = """
+-------------------+--+
|                   |  |
|                   |  |
|  +----------------+  |
|  |                   |
|  |                   |
+--+-------------------+
""".strip('\n')
    
    expected = ["""
+-------------------+
|                   |
|                   |
|  +----------------+
|  |
|  |
+--+
""".strip('\n'), """
                 +--+
                 |  |
                 |  |
+----------------+  |
|                   |
|                   |
+-------------------+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Piece of cake! (check for irrelevant spaces)"
    shape = """
                           
                           
           +-+             
           | |             
         +-+-+-+           
         |     |           
      +--+-----+--+        
      |           |        
   +--+-----------+--+     
   |                 |     
   +-----------------+     
                           
                           
""".strip('\n')
    
    expected = ["""
+-+
| |
+-+
""".strip('\n'), """
+-----+
|     |
+-----+
""".strip('\n'), """
+-----------+
|           |
+-----------+
""".strip('\n'), """
+-----------------+
|                 |
+-----------------+
""".strip('\n'), ]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Horseshoe (shapes are not always rectangles!)"
    shape = """
+-----------------+
|                 |
|   +-------------+
|   |
|   |
|   |
|   +-------------+
|                 |
+-----------------+
""".strip('\n')
    
    expected = [shape]
    runTest(name, shape, expected)
    
    
    name = "Warming up"
    shape = """
+------------+
|            |
|            |
|            |
+------++----+
|      ||    |
|      ||    |
+------++----+
""".strip('\n')
    
    expected = ["""
+------------+
|            |
|            |
|            |
+------------+
""".strip('\n'), """
+------+
|      |
|      |
+------+
""".strip('\n'), """
+----+
|    |
|    |
+----+
""".strip('\n'), """
++
||
||
++
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    name = "Don't forget the eggs! (you'll understand later...)"
    shape = """
++
++
""".strip('\n')
    
    expected = [shape]
    
    runTest(name, shape, expected)
    
    
    
    
    
    
@test.describe("More tests")
def _():
    
    name = "boxesboxesboxesboxes..."
    shape = """
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
""".strip('\n')
    
    expected = ["""
+---+
|   |
+---+
""".strip('\n')] * 8
    
    runTest(name, shape, expected)
    
    
    
    
    name = "My beautiful frame... (but, where is that hell of a picture!?)"
    shape = """
+---+------------+---+
|   |            |   |
+---+------------+---+
|   |            |   |
|   |            |   |
|   |            |   |
|   |            |   |
+---+------------+---+
|   |            |   |
+---+------------+---+
""".strip('\n')
    
    expected = ["""
+---+
|   |
+---+
""".strip('\n')] * 4 + \
    ["""
+---+
|   |
|   |
|   |
|   |
+---+
""".strip('\n')] * 2 + \
    ["""
+------------+
|            |
+------------+
""".strip('\n')] * 2 + \
    ["""
+------------+
|            |
|            |
|            |
|            |
+------------+
""".strip('\n')]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Will you spin with me?"
    shape = """
   +-----+       
   |     |       
   |     |       
   +-----+-----+ 
         |     | 
         |     | 
         +-----+ 
""".strip('\n')
    
    expected = ["""
+-----+
|     |
|     |
+-----+
""".strip('\n')] * 2
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Homer's favorite!! (imbricated pieces)"
    shape = """
+----------+
|          |
|          |
|          |
|   +--+   |
|   |  |   |
|   |  |   |
|   +--+   |
|          |
|          |
|          |
+----------+
""".strip('\n')
    
    expected = ["""
+----------+
|          |
|          |
|          |
|   +--+   |
|   |  |   |
|   |  |   |
|   +--+   |
|          |
|          |
|          |
+----------+
""".strip('\n'),"""
+--+
|  |
|  |
+--+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Another brick in the whole"
    shape = """
+-+  
| +-+
+-+ |
| +-+
+-+ |
| +-+
+-+ |
| +-+
+-+ |
  +-+
""".strip('\n')
    
    expected = ["""
+-+
| |
+-+
""".strip('\n')] * 8
    
    runTest(name, shape, expected)
    
    
    
    name = "Separated pieces"
    shape = """
+------+ +--+
|      | |  |
|      | |  |
|      | |  |
|   +--+ |  |
|   |    |  |
|   |  +-+  |
|   |  |    |
|   |  +-+  |
|   |    |  |
|   +--+ |  |
|      | |  |
|      | |  |
|      | |  |
+------+ +--+
""".strip('\n')
    
    expected = ["""
+------+
|      |
|      |
|      |
|   +--+
|   |
|   |
|   |
|   |
|   |
|   +--+
|      |
|      |
|      |
+------+
""".strip('\n'),"""
  +--+
  |  |
  |  |
  |  |
  |  |
  |  |
+-+  |
|    |
+-+  |
  |  |
  |  |
  |  |
  |  |
  |  |
  +--+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    
@test.describe("Ok, lets begin the real game, now: spaces matter")
def _():
    
    
    name = "The invisible one"
    runTest(name, "", [])
    
    
    
    name = "Lost in spaces"
    shape = """
+----------------+
|                |
|             +--+
|             |       
|             +--+
|                |
+----------------+
""".strip('\n')
    
    expected = ["""
+----------------+
|                |
|             +--+
|             |
|             +--+
|                |
+----------------+
""".strip('\n')]
    
    runTest(name, shape, expected)
    
    
    
    name = "Lost in spaces returns"
    shape = """
+-+
| |    
| +-----+  +-----+
|       |  |     |
|       +--+  +--+
|             |
|             +--+
|                |
+----------------+
""".strip('\n')
    
    expected = ["""
+-+
| |
| +-----+  +-----+
|       |  |     |
|       +--+  +--+
|             |
|             +--+
|                |
+----------------+
""".strip('\n')]
    
    runTest(name, shape, expected)
    
    
    
    
    
@test.describe("Devil is in the details")
def _():
    
    
    name = "Find mutliple eggs (later, I said...)"
    shape = """
             
    ++       
    ++       
          ++ 
++        ++ 
++           
""".strip('\n')
    
    expected = ["""
++
++
""".strip('\n')] * 3
    
    runTest(name, shape, expected)
    
    
    
    name = "The train (don't forget the dockings)"
    shape = """
+----++----++----++----+
+----++----++----++----+
""".strip('\n')
    
    expected = ["""
+----+
+----+
""".strip('\n')] * 4 + ["""
++
++
""".strip('\n')] * 3
    
    runTest(name, shape, expected)
    
    
    
    
    
    name = "Toilet brush..."
    shape = """
 ++ ++ ++
 || || ||
 || || ||
+++-++-++--------------+
|                      |
++-++-++---------------+
|| || ||
|| || ||
++ ++ ++
""".strip('\n')
    
    expected = ["""
++
||
||
++
""".strip('\n')] * 6 + \
["""
+----------------------+
|                      |
+----------------------+
""".strip('\n')]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Firecrackers"
    shape = """
 ++ ++ ++ ++ ++ ++
 || || || || || ||
 || || || || || ||
++++++++++++++++++
|| || || || || || 
|| || || || || || 
++ ++ ++ ++ ++ ++ 
""".strip('\n')
    
    expected = ["""
++
||
||
++
""".strip('\n')] * 12
    
    runTest(name, shape, expected)
    
    
    
    
    
    
    
@test.describe("Trickier: find small paths entrances...")
def _():
    
    name = "Duck's foot (somehow...)"
    shape = """
++
||
||
||
|+---------------+
|             +--+
|             |
|             +--+
+----------------+
""".strip('\n')
    
    expected = [shape]
    
    runTest(name, shape, expected, "", False)
    
    
    
    name = "Horseshoe - slim version (in and out in the same piece)"
    shape = """
+-----------------+
|                 |
|+----------------+
||
||
||
|+----------------+
|                 |
+-----------------+
""".strip('\n')
    
    expected = [shape]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Slim but resistant horseshoe (or not... :p )"
    shape = """
+-----------------+
|                 |
|+---+------------+
||   |
||   |
||   |
|+---+------------+
|                 |
+-----------------+
""".strip('\n')
    
    expected = ["""
+-----------------+
|                 |
|+----------------+
||
||
||
|+----------------+
|                 |
+-----------------+
""".strip('\n'),"""
+---+
|   |
|   |
|   |
+---+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Fighting ducks feet!! (don't bother this name, it's crap...)"
    shape = """
+-----------------+
|                 |
++---+------------+
||   |
||   |
||   |
|+---+------------+
|                 |
|                 |
+-----------------+
""".strip('\n')
    
    expected = ["""
+-----------------+
|                 |
+-----------------+
""".strip('\n'),"""
++
||
||
||
|+----------------+
|                 |
|                 |
+-----------------+
""".strip('\n'),"""
+---+
|   |
|   |
|   |
+---+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    name = "Inner shapes identification correctness"
    shape = """
+--------------+
|              |
|        ++--+ |
|        ||  | |
|        ++--+ |
+--------------+
""".strip('\n')

    expected = ["""
+--------------+
|              |
|        +---+ |
|        |   | |
|        +---+ |
+--------------+
""".strip('\n'),
"""
++
||
++
""".strip('\n'),
"""
+--+
|  |
+--+
""".strip('\n'),]

    runTest(name, shape, expected)

    
    
    
    
@test.describe("Take the turns!!")
def _():
    
    name = "Yin-Yang..."
    shape = """
+-------------------++--+
|                   ||  |
|                   ||  |
|  +----------------+|  |
|  |+----------------+  |
|  ||                   |
+--++-------------------+
""".strip('\n')
    
    expected = ["""
+-------------------+
|                   |
|                   |
|  +----------------+
|  |
|  |
+--+
""".strip('\n'), """
                 +--+
                 |  |
                 |  |
                 |  |
+----------------+  |
|                   |
+-------------------+
""".strip('\n'), """
                 ++
                 ||
                 ||
+----------------+|
|+----------------+
||
++
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Like a vortex... (\"Like a vo-o-o-ortex\"...  ;-o )"
    shape = """
+-----+
+----+|
|+--+||
||++|||
||++|||
||+-+||
|+---+|
+-----+
""".strip('\n')
    
    expected = ["""
+-----+
+----+|
|+--+||
||++|||
||++|||
||+-+||
|+---+|
+-----+
""".strip('\n'), """
++
++
""".strip('\n')]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Take opened weird turns too..."
    shape = """
+--+
|  ++  +---+      +--+
|   |  |+-+| +----+  |
|   +--+| ++ |+--+   |
|  +----+ |+-+|  |   |
|  |      +---+  ++  |
+--+              +--+
""".strip('\n')
    
    expected = ["""
+--+
|  ++  +---+
|   |  |+-+|
|   +--+| ++
|  +----+
|  |
+--+
""".strip('\n'), """
        +--+
   +----+  |
++ |+--+   |
|+-+|  |   |
+---+  ++  |
        +--+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    
    
@test.describe("Crazy stuff!")
def _():
    
    
    name = "One poor lonesome snake (this is a venomous one...)"
    shape = """
+-----------------+
|+---------------+|
||        ++     ||
|+--------+|     ||
+----------+     ||
                 ||
+----------------+|
|+----------------+
||
|+------+
+-------+
""".strip('\n')
    expected = [shape]
    runTest(name, shape, expected)
    
    
    
    
    name = "Do not disturb... (two snakes, they are buzy...)"
    shape = """
+-----------------+
|+---------------+|
||        ++     ||
|+--------+|     ||
+----------+     ||
+----------------+|
|+----------------+
||
|+------+
+-------+
""".strip('\n')
    
    expected = ["""
+-----------------+
|+---------------+|
||        ++     ||
|+--------+|     ||
+----------+     ||
+----------------+|
|+----------------+
||
|+------+
+-------+
""".strip('\n'), """
 +---------------+
 |        ++     |
 +--------+|     |
+----------+     |
+----------------+
""".strip('\n'),]
    runTest(name, shape, expected)
    
    
    
    name = "Even more vicious..."
    shape = """
++
||
||  +-----------------------------+  ++
||  +-----------------------------+  ||
||   +---+   +---+   +---+   +---+   ||
||   |+-+|   |+-+|   |+-+|   |+-+|   ||
||   || |+---+| |+---+| |+---+| ||   ||
|+---+| +-----+ +-----+ +-----+ |+---+|
+-----+                         +-----+
""".strip('\n')
    
    expected = ["""
++
||
||                                   ++
||                                   ||
||   +---+   +---+   +---+   +---+   ||
||   |+-+|   |+-+|   |+-+|   |+-+|   ||
||   || |+---+| |+---+| |+---+| ||   ||
|+---+| +-----+ +-----+ +-----+ |+---+|
+-----+                         +-----+
""".strip('\n'), """
+-----------------------------+
+-----------------------------+
""".strip('\n')]
    runTest(name, shape, expected, "", False)
    
    
    
    
    
    name = "The broken ring... (piece of cake, this one, but...)"
    shape = """
+-------+--+
|+------+-+|
||        ||
++        ||
||        ||
|+--------+|
+----------+
""".strip('\n')
    
    expected = ["""
        +--+
        +-+|
          ||
++        ||
||        ||
|+--------+|
+----------+
""".strip('\n'), """
+--------+
|        |
|        |
|        |
+--------+
""".strip('\n'), """
+-------+
|+------+
||
++
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    name = "THE RING (...but you might be terrified with this one! ;p )"
    shape = """
+----------+
|+--------+|
||        ||
||        ||
||        ||
|+--------+|
+----------+
""".strip('\n')
    
    expected = ["""
+--------+
|        |
|        |
|        |
+--------+
""".strip('\n'), """
+----------+
|+--------+|
||        ||
||        ||
||        ||
|+--------+|
+----------+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Russian dolls"
    shape = """
+----+
|+--+|
||++||
||++||
|+--+|
+----+
""".strip('\n')
    
    expected = ["""
+----+
|+--+|
||  ||
||  ||
|+--+|
+----+
""".strip('\n'), """
+--+
|++|
|++|
+--+
""".strip('\n'), """
++
++
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    
    
@test.describe("Crazy stuff 2!! Still dealing with spaces!!")
def _():
    
    
    name = "Discard the whitespaces, but not the usefull ones"
    shape = """
     +-+
     | |
     | |
+----+ |
|+-----+    ++
||          ||
||  +-------+|
||  |     +--+
||  |     +---+
||  +--------+|
|+-----------+|
+----+ +------+
     | |
     | |
     +-+
""".strip('\n')
    expected = [shape]
    runTest(name, shape, expected, "", False)
    
    
    
    
    name = "And did you think about this kind of loop??"
    shape = """
+-------------------------+
|         +----+          |
|         |    |          |
|         |    |          |
|         |    |          |
|+--------+    +---------+|
||                       ||
|+--------+    +---------+|
|         |    |          |
|         |    |          |
|         |    |          |
|         +----+          |
+-------------------------+
""".strip('\n')
    
    expected = [shape, """
         +----+
         |    |
         |    |
         |    |
+--------+    +---------+
|                       |
+--------+    +---------+
         |    |
         |    |
         |    |
         +----+
""".strip('\n')]
    
    runTest(name, shape, expected, "", False)
    
    
    
    
    
    

@test.describe("Crazy stuff 3!! Strings reconstruction tests (You might hate me after these last ones. ;-s At least, I did, after I thought about them... )")
def _():
    
    
    
    name = "First time you reach this one, you should pass it without troubles (that may change afterward...)"
    shape = """
+----+
|    |
|    +----+
|    |    |
|    +---+|
|    |   ||
|+---+   ||
||       ||
|+-------+|
+---------+
""".strip('\n')
    
    expected = [shape, """
    +---+
    |   |
+---+   |
|       |
+-------+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    name = "Same here..."
    shape = """
+---+  +----+
|   |  |    |
|   +--+    |
|      |    |
|   +--+    |
|   |  |    |
|   |  +---+|
|   |      ||
|   +------+|
+-----------+
""".strip('\n')
    
    expected = [shape, """
+--+
|  |
|  +---+
|      |
+------+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    name = "Still the same (or not!!). Next ones are the real problems!"
    shape = """
+----------------------+
|+----++--------++----+|
||    ||        ||    ||
||    ||        ||    ||
|+----+|        |+----+|
+------+        +------+
""".strip('\n')
    
    expected = ["""
+----------------------+
|+----++--------++----+|
||    ||        ||    ||
||    ||        ||    ||
|+----+|        |+----+|
+------+        +------+
""".strip('\n'), """
+----+
|    |
|    |
+----+
""".strip('\n'), """
+----+
|    |
|    |
+----+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    name = "Damn! What is that!?? (don't do that face, you are almost at the end of the tests... Meaning, the end of the fixed tests, actually... ;-o )"
    shape = """
++++++++++++
++--++++--++
++++++++++++
+++------+++
++|++++++|++
++++++++++++
""".strip('\n')
    
    expected = ["""
++
++
""".strip('\n')] * 23 + \
    ["""
+--+
+--+
""".strip('\n')] * 4 + \
    ["""
++
||
++
""".strip('\n')] * 2 + \
    ["""
+------+
|+----+|
++    ++
""".strip('\n'), """
+------+
+------+
""".strip('\n'),]
    
    runTest(name, shape, expected)
    
    
    
    
    
    
    
    name = "Nest of snakes! (warning, they are protective with their eggs...)"
    addMessage = """
 
*****************************
     Last fixed test!
*****************************
 
But this one might be VERY tricky, depending on the approach you choose earlier.
 """
    shape = """
  +-----------------+
  |+--------++-----+|
  ||        ++     ||
  |+--------+|     ||
+++----------+     ||
|++----------------+|
|||+----------------+
||||
|||+------+
||+-------+
|+--------+
+---------+

+-----------+
|+++------++|
||++      ++|
||        |||
|+--------+||
+----------+|
+-----------+
""".strip('\n')
    
    expected = ["""
           +-----+
           |     |
           |     |
+----------+     |
+----------------+
""".strip('\n'), """
++
++
""".strip('\n'), """
++
++
""".strip('\n'), """
++
||
||
||
||
||
|+--------+
+---------+
""".strip('\n'), """
++
||
||
||
|+-------+
+--------+
""".strip('\n'), """
+--------+
|        |
+--------+
""".strip('\n'), """
+-----------------+
|+---------------+|
||        ++     ||
|+--------+|     ||
+----------+     ||
+----------------+|
|+----------------+
||
|+------+
+-------+
""".strip('\n'), """
++
++
""".strip('\n'), """
++
++
""".strip('\n'), """
+-----------+
|+---------+|
||        ++|
||        |||
|+--------+||
+----------+|
+-----------+
""".strip('\n'), """
+++------+
|++      |
|        |
+--------+
""".strip('\n'),]
    
    runTest(name, shape, expected, addMessage)
        
    
    
    
    
@test.describe('Random tests')
def _():
    
    
    """
    ************************************
       INTERNAL SOLUTION and IMPORTS
    ************************************
    """
    
    
    
    from random      import randrange as rnd
    from collections import defaultdict
    from itertools   import cycle
    import time
    
    
    
    def break_evil_pieces_InternalOne_354dlkshg(shape):  return SeekAndDestroy_RefInternalOne_lsgfjk45ghf(shape).solve()
    
    
    class SeekAndDestroy_RefInternalOne_lsgfjk45ghf(object):
        
        """ Memory consuming implementation, but it allows to fasten the executions """
        
        ANOMALIES_DCT = {(0,1): "|", (1,0): "-", (0,-1): "|", (-1,0): "-"}                              # Dict to identify "small paths" entrances (what I call "anomalies": "+|" instead of "+-", ...)
        AROUND        = ANOMALIES_DCT.keys()                                                            # To check in cardinal direction (N, S, E, W)
        AROUND_SPACES = { (dx,dy) for dx in range(-1,2) for dy in range(-1,2) if (dx,dy) != (0,0) }     # To check the 8 positions around
        
        DELTA_STRAIGHT_HORZ  = {(0,2), (0,-2)}                                                          # Matches the "getDeltas" of two positions next to a central one that would be on the left and on the right
        DELTA_STRAIGHT_VERT  = {(2,0), (-2,0)}                                                          # Matches the "getDeltas" of two positions next to a central one that would be under and above
        DELTA_DIRECT_LINK    = {0,1}, {0,-1}                                                            # Matches the "getDeltas" of two positions that are directly linked together
        ARE_STRAIGHT_FORWARD = {frozenset("-"), frozenset("|")}                                         # To identify small paths that are going straight forward
        
        
        def __init__(self, shape):
        
            self.lines  = shape.split('\n')                                 # Store the original shape as list of lines string
            
            self.typs   = { c: set() for c in "+ -|" }                      # Dict, string (keys) of set of coordinates. Arranged by types (keys = '+', '-', '|', ' '). WARNING: self.typs[" "] will be modified through the executions (other sets aren't)
            for x,line in enumerate(self.lines):
                for y in range(len(line)):
                    self.typs[line[y]].add( (x,y) )
            
            self.simples  = self.typs["-"] | self.typs["|"]                 # Set of all the borders positions that won't need calculations to identifiy the character to use (not complete at this stage of the executions)
            self.borders  = self.simples | self.typs["+"]                   # All the borders of the original shape
            
            self.StringSkelLst   = []                                       # list of strings of subshapes (what will be returned)
            self.alreadyDone     = set()                                    # Set of frozensets of couple of coordinates tuple that have been "already checked" during the executions (used to avoid multiple matches with the "weird" searches, infinite loops, and allow to fasten the executions providing a "fast exit")
            self.newSkeleton     = set()                                    # Store the positions of all the limits of the "current shape to be"
            self.skel_LinkDct    = defaultdict(set)                         # Keys = position / values = set of the other positions that are linked to the current key one (will only be used when absolutely necessary, to fasten the executions)
            self.skeletons       = set()                                    # Set of frozensets of "newSkeletons" sets of positions (to avoid multiple matches of the same skeleton)
            self.discardSkeleton = False                                    # Indicates if the currently constructed skeleton has to be ignored or not (wrong values, already checked, ...)
            
            
            """ search for special cases around crosses: "++" or anomalies like "+|", and search for simple corners too ("+" with
                only 2 directly linked charcters around, that won't need calculations either while reconstructing the string shapes) """
            self.doubleCrosses, self.anomalies = set(), set()
            for pos in self.typs["+"]:
                directLink, neigh = set(), self.getAround(pos) & self.borders
                for pos2 in neigh:
                    if pos2 in self.typs["+"]:  self.doubleCrosses.add( frozenset((pos, pos2)) )                # Found a "may be starting position" ("++" or vertical equivalent): store in doubleCrosses set
                    
                    if self.getValAtThisPos(pos2) == self.ANOMALIES_DCT[ self.getDeltas(pos, pos2) ]:
                        self.anomalies.add( frozenset((pos, pos2)) )                                            # Found an entrance of a "small path": "+|" or "|+" or vertical equivalent: ["-", "+"] or ["+", "-"]...
                    else:
                        directLink.add(pos2)                                                                    # ...otherwise, found one direct link between the current cross and this neighbor (++, +-, ...)
                
                if len(directLink) == 2 and 0 not in self.getDeltas(*directLink):                               # If 0 is in the delta of positions, the 2 linked positions are algined, so it's not a "simple corner cross"
                    self.simples.add(pos)                                                                       # Found a simple corner, archive it
    
    
    
        def getAround(self, pos, isSpace=False):        return { (pos[0]+dx, pos[1]+dy) for dx,dy in (self.AROUND_SPACES if isSpace else self.AROUND) }     # Obtain the pos tuples in the neigborhood (even if they does not exist)
        
        def getDeltas(self, pos1, pos2):                return tuple(b-a for a,b in zip(pos1, pos2))                                                        # Calculate deltas of coordinates for 2 positions (x2-x1, y2-y1)
        
        def getValAtPosAsList(self, posLstToGet):       return [ self.getValAtThisPos(pos) for pos in posLstToGet ]                                         # Return a list of the values present in the list of positions argument
        
        def getValAtThisPos(self, pos):                 return self.lines[pos[0]][pos[1]]
        
        def getGoAheadChar(self, moveToCheck):          return self.ANOMALIES_DCT[ moveToCheck[::-1] ]                                                      # Analyzing the current direction used, returns the char "-" or "|" that will indicate if the next coupe of positions go in the same direction than the current one or not
        
        
        def updateNewSkel(self, *args):                                                             # Establish the links between the current positions and the good ones ahead
            for pos1, pos2 in (args if len(args) == 1 else zip(*args)):                             # Allow to link two types of arguments : args = (pos1, pos2) and args = (List of pos1, List of pos2), where pos1[n] will be linked to pos2[n]
                self.newSkeleton |= {pos1, pos2}
                if pos1 not in self.simples: self.skel_LinkDct[pos1].add(pos2)
                if pos2 not in self.simples: self.skel_LinkDct[pos2].add(pos1)
            
        
    
        
        def solve(self):
            
            """ Resolve free spaces: done first, to resolve the maximum number of "small paths" possible and archive the key couples of positions in self.alreadyDone """
            while self.typs[" "]:
                self.runInFreeSpace_WithFlowersBetweenYourToes(next(s for s in self.typs[" "]))
                self.archiveSkel_StartEmptyNewSkel()
                
            for i in range(2):
                """ i->0: Resolves the weird shapes (no spaces in them) starting with "++", and extends them as far as possible, using other functions if needed
                    i->1: Same, but starting with "anomalies" positions. """
                    
                setToUse = self.doubleCrosses if not i else self.anomalies - self.alreadyDone       # Define the set to use at this iteration. "doubleCrosses" is mutated, but NOT anomalies (need to stay as it is for further checks)
                
                while setToUse:
                    positions = setToUse.pop()
                    moveToCheck = self.getDeltas(*positions)[::-1]                                  # If deltas are [0,1], then the crosses are on the same row and you want to check under and above it, so reversing the deltas gives the move to do
                    for d in [1, -1]:                                                               # Check in BOTH directions from the same starting couple of points
                        if i == 0: self.updateNewSkel(positions)                                    # Link the starting crosses together
                        self.seekOnSmallPaths(list(positions), tuple( dz*d for dz in moveToCheck) )
                        self.archiveSkel_StartEmptyNewSkel()
            
            return self.StringSkelLst
            
            
            
        def runInFreeSpace_WithFlowersBetweenYourToes(self, spacePos):                              # (Reading that, do you visualize Shannen Doherty running in the meadow too ? ;-p )
            
            foundAnomalies = {}                                                                     # Dict: key = frosenset of couple of positions representing the entrance of a "wmall paths" / value = position of the space facing the anomalie (needed to calculate the direction of the next move to do)
            spacesToCheck, allFoundSpaces = {spacePos}, set()
            while spacesToCheck:                                                                    # Run through the whole current free space, archiving all the entrances of small paths and the limits of the current "free space shape" (do not update newSkeleton at the same time, see lower)
                space             = spacesToCheck.pop()
                around            = self.getAround(space, True)
                justFoundSpaces   = (around & self.typs[" "]) - allFoundSpaces
                spacesToCheck    |= justFoundSpaces                                                 # Add only the new spaces to those that have to be checked
                allFoundSpaces   |= justFoundSpaces | {space}                                       # Archive all the found spaces (do not discard them on the fly!)
                limits            = around & self.borders                                           # Borders found around the current space
                self.newSkeleton |= limits                                                          # Update the current skeleton
                
                
                if around - limits - self.typs[" "]: self.discardSkeleton = True                    # Found some coordinates out of the shape (= unclosed shape!): discard the current skeleton, but keep the executions on, to discard the maximum of useless spaces (needed for the "lonesome snake" test and others of this type)
                
                foundAnomalies.update({ frozenset({cross, neigh}): space                            # Search for and archive all the anomalies present around the current space
                                            for cross in (around & self.typs["+"]) 
                                            for neigh in self.getAround(cross) & around 
                                            if {cross, neigh} in self.anomalies and {cross, neigh} not in self.alreadyDone })
                
                for pos in limits-self.simples:                                                     # Search for crosses with complex links and update skel_LinkedDct if needed
                    for pos2 in (limits-{pos}) & self.getAround(pos):                               # Reduce the checks to the pos2 that are next to pos (cardinal directions) only
                        if ({pos, pos2} not in self.anomalies and
                            set(self.getDeltas(pos, pos2)) in self.DELTA_DIRECT_LINK):              # pos and pos2 are linked! (one in the "cardinal neighborhood" of the other)
                                self.skel_LinkDct[pos].add(pos2)
                                    
                                    
            while foundAnomalies:                                                                   # Add to the newSkeleton all the small paths connected to this free space
                positions, space = foundAnomalies.popitem()
                self.alreadyDone.add(frozenset(positions))
                deltaAnomalie    = self.getDeltas(*positions)[::-1]                                 # Delta of vertical positions is (+1 or -1, 0) => will have to move horizontaly, so reverse the array to obtain (0, +-1). Still the good direction to determine... (next lines)
                deltaSpcCross    = self.getDeltas(space, set(positions & self.typs["+"]).pop())
                moveToCheck      = tuple( spcr if anom else 0 for spcr, anom in zip(deltaSpcCross, deltaAnomalie) )
                self.seekOnSmallPaths(list(positions), moveToCheck)
                
            self.typs[" "] -= allFoundSpaces                                                        # Supress all the spaces found in the "current" free area, after exiting the loop (needed to identify positions that are outside of the initial shape, during the while loop)
            
            
            
        def seekOnSmallPaths(self, positions, moveToCheck):
            
            while True:
                areFurther = [ (x+dx, y+dy) for (dx,dy),(x,y) in zip([moveToCheck]*2, positions) if (x+dx, y+dy) in self.borders or (x+dx, y+dy) in self.typs[" "] ]
                valFurther = self.getValAtPosAsList(areFurther)
                
                areFurtherSet, valFurtherSet = map(set, [areFurther, valFurther])
                
                if areFurtherSet in self.alreadyDone or len(areFurther) != 2:                       # Avoid: double match coming from the other side of the shape, or infinite loopings in the shape, or incomplete matches out of the global shape too.
                    if areFurtherSet-self.newSkeleton or not areFurtherSet:                         # If areFurther aren't fully already in newSkeleton, that means we reach this positions for the second time. Otherwise we just made a full loop, so do not discard this skeleton.
                        self.discardSkeleton = True
                    else: self.updateNewSkel(positions, areFurther)                                 # Close the loop (because reaching this statment implies that we are in a loop!)
                    break
                
                if valFurtherSet not in self.ARE_STRAIGHT_FORWARD:
                    self.alreadyDone.add(frozenset(positions))                                      # Archive all the positions couples that are not "going straight forward", to avoid loops or multiple matches of the same shape, coming from different extremities.
                
                if valFurtherSet == {"+"}:                                                          # "++" ahead: end of this shape
                    self.updateNewSkel(positions, areFurther)
                    self.updateNewSkel(areFurther)                                                  # Close the shape...
                    
                elif " " in valFurtherSet and len(valFurtherSet) != 1 :                             # " |" or " +" ahead: enter a free space, so get the position of this space and run the "simpler" algorithm
                    self.runInFreeSpace_WithFlowersBetweenYourToes(areFurther[ valFurther.index(" ") ])
                    
                elif self.getGoAheadChar(moveToCheck) in valFurtherSet:                             # AreFurther = "||" or "+|": go ahead...
                    self.updateNewSkel(positions, areFurther)
                    positions = areFurther
                    continue
                    
                elif valFurtherSet == {"+", self.ANOMALIES_DCT[moveToCheck]}:                       # "-+" ahead (coming from top or bottom): take a turn!!
                    if valFurther.index("+"):
                        furtherExt, furtherC = areFurther
                        actualC, actualExt   = positions
                    else:
                        furtherC, furtherExt = areFurther
                        actualExt, actualC   = positions
                    
                    self.updateNewSkel([actualExt, furtherC], [furtherC, furtherExt])               # Link the external borders of the turn
                    
                    positions   = [actualC, furtherExt]                                             # Next couple of positions to use (at the exit of this turn / order doesn't matter)
                    moveToCheck = self.getDeltas(furtherC, furtherExt)                              # Determine the direction to move after the turn (order doesn't matter)
                    self.alreadyDone.add(frozenset(positions))
                    continue
                
                break                                                                               # If you reach this statment, you're done searching or you search in the wrong direction...
        
        
        
        def archiveSkel_StartEmptyNewSkel(self):
            
            skelToArchive = frozenset(self.newSkeleton)
            if not self.discardSkeleton and len(self.newSkeleton) >= 4 and skelToArchive not in self.skeletons:
                self.skeletons.add(skelToArchive)                                                   # Archive the current skeleton as forzenset of positions, to avoid multiple matches
                
                # Determine the actual size of the skeleton:
                minX, minY = min(self.newSkeleton, key=lambda pos: pos[0])[0], min(self.newSkeleton, key=lambda pos: pos[1])[1]
                maxX, maxY = max(self.newSkeleton, key=lambda pos: pos[0])[0], max(self.newSkeleton, key=lambda pos: pos[1])[1]
                lX, lY = maxX-minX+1, maxY-minY+1
                
                # Update the list with the current shape as a string...:
                self.StringSkelLst.append( '\n'.join( ''.join(self.getSkelChar((minX+x, minY+y)) for y in range(lY)).rstrip() for x in range(lX) ) )
                
            self.discardSkeleton = False                                                            # Initiate parameters for the next skeleton
            self.newSkeleton.clear()
            self.skel_LinkDct.clear()
            
            
        def getSkelChar(self, pos):
            
            if pos not in self.newSkeleton: return " "                                              # Not in the skeleton, this is a space
            if pos in self.simples:         return self.getValAtThisPos(pos)                        # In the "simples" postions: return the original character
                
            setLinkedPos = self.skel_LinkDct[pos]
            
            if len(setLinkedPos) == 1:                                                              # Security check
                raise ValueError("Unbound position at {}: the only other position linked is {}".format(pos, setLinkedPos.pop()))
                
            return ( "+" if len(setLinkedPos) > 2                                                   # More than 2 linked neighbors: this is a cross...
                else "-" if self.getDeltas(*setLinkedPos) in self.DELTA_STRAIGHT_HORZ               # 2 neighbors around, doing an horizontal line...
                else "|" if self.getDeltas(*setLinkedPos) in self.DELTA_STRAIGHT_VERT               # 2 neighbors around, doing a vertical line...
                else "+")                                                                           # All other cases: this is a cross too
            
    
    
    
    
    
    
    
    """
    ******************************
            RANDOM TESTS
    ******************************
    """
    
    
    bordersH = [ s.replace('.',' ') for s in ["........+-+........", "--------+-+--------"] ]
    
    bordersV = [ s.replace('.',' ') for s in ["""
.
.
.
.
.
+
|
+
.
.
.
.
.
""".strip('\n'),"""
|
|
|
|
|
+
|
+
|
|
|
|
|
""".strip('\n'),]]
    
    
    
    rndShapesAsLists = [
"""
........+-+........
...................
...................
...................
...................
+.................+
|.................|
+.................+
...................
...................
...................
...................
........+-+........
""".strip('\n'),
"""
........|.|........
........|.|........
........|.|........
......+-+.+-+......
......|.....|......
------+.....+------
...................
-------------------
...................
...................
...................
...................
........+-+........
""".strip('\n'),
"""
........|.|........
........|.|........
...+----+.|........
...|+-----+....++..
...||..........||..
+..||..+-------+|.+
|..||..|.....+--+.|
+..||..|.....+---++
...||..+--------+|.
...|+-----------+|.
...+----+.+------+.
........|.|........
........|.|........
""".strip('\n'),
"""
........+-+........
...................
...................
...................
.......+----+......
+......|+--+|..++--
|......||++||..||..
+......||++||..++--
.......|+--+|......
.......+----+......
...................
...................
........+-+........
""".strip('\n'),
"""
........+-+........
...................
...................
...................
...................
-------------------
...................
------+.....+------
......|.....|......
......+-+.+-+......
........|.|........
........|.|........
........|.|........
""".strip('\n'),
"""
........|.|........
........|.|........
........|.+-----+..
........|....+-+|..
........+-+..|.||..
-----+....+--+.|+--
.....+--+......|...
----+...+---+..+---
....|.......|......
....+---+.+-+......
........|.|........
........|.|........
........|.|........
""".strip('\n'),
"""
........|.|........
........|.|........
..+-----+.|........
..|+-+....|........
..||.|..+-+........
--+|.+--+....+-----
...|......+--+.....
---+..+---+...+----
......|.......|....
......+-+.+---+....
........|.|........
........|.|........
........|.|........
""".strip('\n'),
"""
........+-+........
..+-----+.|....++..
..+-++----+....++..
....++.............
....||.............
+...|+-------------
|...|..............
+...+---+.+--------
........|.|........
........|.|........
........|.|........
........|.|........
........|.|........
""".strip('\n'),
"""
........|.|........
........++++.......
........++++.......
........++++.......
........++++.......
-----------+......+
.+--------+|......|
-+...+---+||......+
.....|+-+|||.......
.....||.++||.......
.....|+---+|.......
.....+-----+.......
........+-+........
""".strip('\n'),
"""
........+-+........
....+------+.......
....|+----+|.......
....||+--+||.......
....|||++|||.......
+...|||++|||......+
|...|||+-+||......|
+...||+---+|......+
....|+-++--+.......
+---+--+|..........
+-------+..........
...................
........+-+........
""".strip('\n'),
    ]
    
    
    
    
    rndShapesAsLists = [ s.replace('.',' ').strip('\n').split('\n') for s in rndShapesAsLists ]                                     # Format the individual shapes (replace the dots, strip the useless '\n' and split the resulting string to a list of lines
    
    lX_Rnd, lY_Rnd = set(map(len, rndShapesAsLists)), { x for elt in map(lambda s: map(len, s), rndShapesAsLists) for x in elt }    # Check the consistency of the sizes of the individual elements for the random shapes
    
    if len(lX_Rnd) != 1 or len(lY_Rnd) != 1:
        raise Exception("Error in the random shapes: different lengths found!\n\tlX_Rnd = {}; lX_Rnd = {}".format(lX_Rnd, lY_Rnd))
    
    lX_Rnd, lY_Rnd = lX_Rnd.pop(), lY_Rnd.pop()
    
    
    
    
    """ Tests for the individual elements of the random tests (NOT ON CODEWARS) """
    if DO_INDIVIDUAL_RND_CHECKS:
        for i in range(2):                                                                          # i = 0: without borders / i = 1: with borders
            for shape in rndShapesAsLists:
                corner = {0:" ", 1:"+"}[i]
                verticalBorder = (corner + "\n" + bordersV[i] + "\n" + corner ).split('\n')
                fullShape = '\n'.join( a+b+c for a,b,c in zip( verticalBorder, [bordersH[i]] + shape + [bordersH[i]], verticalBorder))
                
                print("------------\nTest for:\n------------")
                print(fullShape)
                print("------------")
                
                ans = DO_INDIVIDUAL_RND_CHECKS_WITH(fullShape).solve()
                for s in sorted(ans): print(" \n" + s)
                
                if MAKE_PAUSES:
                    a = input("waiting...")
    
    
    
    
    
    """ Random shapes generator for the random tests """
    def generateRandomShape():
        
        maxRndElements = 16                                                                         # max number of random elements in the final shape
        lRnd = len(rndShapesAsLists)                                                                # Current number of available elements
        
        lX, lY = rnd(1,6), rnd(1,4)                                                                 # Number of rectangles in both dimensions. X: vertical / Y: horizontal
        if lX*lY > maxRndElements: lX = int(maxRndElements / lY)                                    # Limitation of the final size
        
        isBorder = rnd(2)                                                                           # Define the type of border for the full shape: 0 = empty borders / 1 = full borders
        lst      = [ "" for _ in range(lX * lX_Rnd + 2)]                                            # Initialize the list needed
        
        for x in range(-1, lX+1):                                                                   # Construct the data columns, with the good type of border (top and bottom)
            for y in range(lY):
                elt = rndShapesAsLists[ rnd(lRnd) ] if x not in [-1, lX] else [bordersH[isBorder]]  # Define the element to add to the full shape
                for i,line in enumerate(elt):                                                       # Update each necessary line, according to the height of the element currently used
                    nLine = x*lX_Rnd+1 + i if x != -1 else 0                                        # Calculate the index of the line to update
                    lst[nLine] += line
        
        corner = {0:" ", 1:"+"}[isBorder]                                                           # Define the good corner type
        vFullBorder = '\n'.join([corner] + [bordersV[isBorder]]*lX + [corner]).split("\n")          # Construct the full vertical borders (right and left)
        
        return '\n'.join( a+b+c for a,b,c in zip( vFullBorder, lst, vFullBorder ))                  # Join the different parts and return
    
    
    
    t = [0,0]
    if DO_RND_TESTS_FOR_WARRIORS:
        @test.it("Random tests")
        def _():
            for _ in range(N_RANDOM_TESTS):
                
                shape    = generateRandomShape()
                start    = time.time()
                expected = SeekAndDestroy_RefInternalOne_lsgfjk45ghf(shape).solve()
                t[1]    += time.time() - start
                start    = time.time()
                runTest("", shape, expected, "", False)
                t[0]    += time.time() - start
            if DISPLAY_RND_TIME:
                print("durations:\n\tYour function:\t{}\n\tMy function:\t{}".format(t[0], t[1]))
    
    
