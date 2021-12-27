"""
Special thanks to @Blind4Basics for contributing this upgraded,
comprehensive test suite
"""

NEW_TESTS_TOKENIZER = [

["""p0
  (/* This is a comment // but that is not a new one!
// this one should not remove the end of the previous one*/
    F2 L
  )2 (
    F2 R
  )2
q

(
  P0
)2""",
["p0", "(", "F2", "L", ")2", "(", "F2", "R", ")2", "q", "(", "P0", ")2"],
""],


["""p0
  (// This is a comment /* but that is not a multiline one!
    F2 L
  )2 (
    F2 R
  )2
// this end of multiline comment doesn't 'exist'*/
q

(
  P0
)2""",
["p0", "(", "F2", "L", ")2", "(", "F2", "R", ")2", "q", "(", "P0", ")2"],
""],


["""p0
  (/* This is a comment // but that is not! */
// */ this shouldn't fail because this is a comment too
    F2 L
  )2 (
    F2 R
  )2
q

(
  P0
)2""",
["p0", "(", "F2", "L", ")2", "(", "F2", "R", ")2", "q", "(", "P0", ")2"],
""],

# shouldn't raise on invalid syntaxes that are in comments
["""p0
  (//FFR(L3
    F2 L
  )2 (
    F2 R
  )2
q
/*p0FFFq*/
(
  P0
)2""",
["p0", "(", "F2", "L", ")2", "(", "F2", "R", ")2", "q", "(", "P0", ")2"],
""],

# should work with single line coment symbol within a single line comment too
["""p0
  (//FFR ( // this should be erased successfully too
    F2 L
  )2 (
    F2 R
  )2
q
(
  P0
)2""",
["p0", "(", "F2", "L", ")2", "(", "F2", "R", ")2", "q", "(", "P0", ")2"],
""],

]



NEW_TESTS_COMPILER = [

["""p0
    F2 R F4 L
P0""",
None,
"An error should be thrown at the converter if pattern definition isn't closed"],

["p31(L7LFFLF5FL9F5(R9F4FR)R1qL9FF5(FF)7Rp186FRqR8LF",
None,
"An error should be thrown at the converter if a bracket isn't closed properly, while inside a pattern definition"],

["p31L7LFFLF5FL9)F5(R9F4FR)R1qL9FF5(FF)7Rp186FRqR8LF",
None,
"An error should be thrown at the converter if a bracket isn't opened properly, while inside a pattern definition"],

["""FR2p96LLF6qFLL7P96P96P96p96LRR8R1//R7LPp96L5FR7
RF4F7F3qRL((F(LF4())F7/*L8F1L1L7Pp96PF7PF2RFR()4()4*/R2)R)//L8FFF
R3""",
None,
"Should throw an error when 2 patterns are defined with the same name at the root level"],

["""
(P626)3
p626
    RR
    p968
        P919
    q
    (P968)0     // <<< cCheck this!!
q""",
["R", "R", "R", "R", "R", "R"],
"Program shouldn't fail because of an call to an undefined pattern, if it's never called"],

# new case:
["""
p0 LFF q p1 p0 FFFFF q P3 q p3 P0 q P1
""",
['L', 'F', 'F'],
"Scope managment: the engine should correctly keep track of the different versions of the patterns declared in different scopes"],

["""F(P7)0
    p7
        RLRL1L6FL2
        P7
        F1(R3(R2LFR)FL)9R
    q
    LF7RRF""",
["F", "L", "F", "F", "F", "F", "F", "F", "F", "R", "R", "F"],
"A \"would be\" infinite loop that is never triggered shouldn't fail."],

]





TESTS_THE_TOKENIZER1 = [

# Example RS3-compliant program from the Story
["p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3qP0P1P2P3P4",
["p0", "F", "F", "L", "F", "F", "R", "(", "(", "F", "F", "F", "R", ")2", "(", "F", "F", "F", "F", "F", "L", ")3", ")4", "q", "p1", "F", "R", "q", "p2", "F", "P1", "q", "p3", "F", "P2", "q", "p4", "F", "P3", "q", "P0", "P1", "P2", "P3", "P4"],
""],


# RSU Official Specs - Whitespace and Indentation Support - Example 1
["""p0
  (
    F2 L
  )2 (
    F2 R
  )2
q

(
  P0
)2""",
["p0", "(", "F2", "L", ")2", "(", "F2", "R", ")2", "q", "(", "P0", ")2"],
""],


# RSU Official Specs - Comment Support - Code Example
["""/*
  RoboScript Ultimatum (RSU)
  A simple and comprehensive code example
*/

// Define a new pattern with identifier n = 0
p0
  // The commands below causes the MyRobot to move
  // in a short snake-like path upwards if executed
  (
    F2 L // Go forwards two steps and then turn left
  )2 (
    F2 R // Go forwards two steps and then turn right
  )2
q

// Execute the snake-like pattern twice to generate
// a longer snake-like pattern
(
  P0
)2""",
["p0", "(", "F2", "L", ")2", "(", "F2", "R", ")2", "q", "(", "P0", ")2"], ""],


# RSU Official Specs - Pattern Scoping - Example 1
["""// The global scope can "see" P1 and P2
p1
  // P1 can see P2, P3 and P4
  p3
    // P3 can see P1, P2 and P4 though invoking
    // P1 will likely result in infinite recursion
    F L
  q
  p4
    // Similar rules apply to P4 as they do in P3
    F P3
  q

  F P4
q
p2
  // P2 can "see" P1 and therefore can invoke P1 if it wishes
  F3 R
q

(
  P1 P2
)2 // Execute both globally defined patterns twice""",
["p1", "p3", "F", "L", "q", "p4", "F", "P3", "q", "F", "P4", "q", "p2", "F3", "R", "q", "(", "P1", "P2", ")2"], ""],
         


# RSU Official Specs - Pattern Scoping - Example 2
["""p1
  p1
    F R
  q

  F2 P1 // Refers to "inner" (locally defined) P1 so no infinite recursion results
q

(
  F2 P1 // Refers to "outer" (global) P1 since the
  // global scope can"t "see" local P1
)4

/*
  Equivalent to executing the following raw commands:
  F F F F F R F F F F F R F F F F F R F F F F F R
*/""",
["p1", "p1", "F", "R", "q", "F2", "P1", "q", "(", "F2", "P1", ")4"], ""],



# Edge Assertions - Weird and Empty Comments
["""/*RoboScript Ultimatum (RSU)A simple and comprehensive code example*///Define a new pattern with identifier n = 0
p0//The commands below causes the MyRobot to move
//in a short snake-like path upwards if executed
(F2L// Go forwards two steps and then turn left
)2(F2R// Go forwards two steps and then turn right
)2q//Execute the snake-like pattern twice to generate
//a longer snake-like pattern
(P0)2""",
["p0", "(", "F2", "L", ")2", "(", "F2", "R", ")2", "q", "(", "P0", ")2"], ""],


["""/**///
p0////
(F2L//
)2(F2R//\r\r\r\r\r                   \r\r\r\r\r
)2q//
(P0)2""",
["p0", "(", "F2", "L", ")2", "(", "F2", "R", ")2", "q", "(", "P0", ")2"], ""],



# Edge Assertions - Weird but valid indentation
["""p0
                         \r\r\r            (
 F2   L
)2                                                       (
                                        F2R                                )2
q        (
                                                                     P0
)2                              \r\r\r\r\r\r\r\r\r\r""",
["p0", "(", "F2", "L", ")2", "(", "F2", "R", ")2", "q", "(", "P0", ")2"], ""],



# Edge Assertions - All possible token forms in one program
["""
p0
  (
    F2 L F L F0 R F5 R
  )
  (
    (
      F L2 R3 R0 L4 L0 R5 F6
    )7
    (
      F7 F9 L L4 L R2 R R9
    )4
  )9
  ()0
q

(
  P0 P0 P0
)""",
["p0", "(", "F2", "L", "F", "L", "F0", "R", "F5", "R", ")", "(", "(", "F", "L2", "R3", "R0", "L4", "L0", "R5", "F6", ")7", "(", "F7", "F9", "L", "L4", "L", "R2", "R", "R9", ")4", ")9", "(", ")0", "q", "(", "P0", "P0", "P0", ")"], ""],



# Edge Assertions - Multi-digit integers
["""
p3407
  (
    F242 L F L F57 R F15 R
  )
  (
    (
      F L3324 R3 L4 R665 F6
    )79
    (
      F7 F9 L L4 L R2 R R9
    )48
  )9899000
q

(
  P3407 P3407 P3407
)""",
["p3407", "(", "F242", "L", "F", "L", "F57", "R", "F15", "R", ")", "(", "(", "F", "L3324", "R3", "L4", "R665", "F6", ")79", "(", "F7", "F9", "L", "L4", "L", "R2", "R", "R9", ")48", ")9899000", "q", "(", "P3407", "P3407", "P3407", ")"], ""],

]




#***************************************************************


TESTS_THE_TOKENIZER2 = [

# RSU Official Specs - Whitespace and Indentation Support - Example 2
["""p 0
  (
    F 2L
  ) 2 (
    F 2 R
  )         2
q

(
  P  0
)2""",
None,
"Your tokenizer should throw an error whenever there is whitespace before numbers (stray numbers)"],


# RSU Official Specs - Finally ... - Mini Code Example 1
["""this is a stray comment not escaped by a double slash or slash followed by asterisk F F F L F F F R F F F L F F F R and lowercase "flr" are not acceptable as commands""",
None,
"Your tokenizer should throw an error when there are \"stray comments\""],


# RSU Official Specs - Finally ... - Mini Code Example 2
["""F 32R 298984""",
None,
"Your tokenizer should throw an error in the presence of \"stray numbers\""],



# Edge Assertions - Leading Zeroes
["""p03
  (
    F4 L
  )4
q

P03""",
None,
"Your tokenizer should not allow integer postfixes with leading zeroes"],


["""p3
  (
    F4 L F00
  )4
q

P3""",
None,
"Your tokenizer should not allow integer postfixes with leading zeroes"],


["""p3
  (
    F4 L0001
  )4
q

P3""",
None,
"Your tokenizer should not allow integer postfixes with leading zeroes"],


["""p3
  (
    F4 L1
  )004
q

P3""",
None,
"Your tokenizer should not allow integer postfixes with leading zeroes"],



# Edge Assertions - Unidentified Pattern
["""p
  (
    F4 L
  )4
q

P3""",
None,
"Your tokenizer should not allow a pattern declaration without an identifier"],


["""p3
  (
    F4 L
  )4
q

P""",
None,
"Your tokenizer should not allow a pattern declaration without an identifier"],


["""p
  (
    F4 L
  )4
q

P""",
None,
"Your tokenizer should not allow a pattern declaration without an identifier"],


# Edge Assertions - Incorrectly Placed Comments
["""p/* la la la ... */0
  (
    F2 L
  )2 (
    F2 R
  )2
q

(
  P0
)2""",
None,
"Your tokenizer should throw an error whenever there are comments before numbers (stray numbers)"],


["""p// la la la ...
0
  (
    F2 L
  )2 (
    F2 R
  )2
q

(
  P0
)2""",
None,
"Your tokenizer should throw an error whenever there are comments before numbers (stray numbers)"],


["""p0
  (
    F/* Catch us if you can ;) */2 L
  )2 (
    F2 R
  )2
q

(
  P0
)2""",
None,
"Your tokenizer should throw an error whenever there are comments before numbers (stray numbers)"],


["""p0
  (
    F2 L
  )2 (
    F2 R
  )/* Now I"m here :p */2
q

(
  P0
)2""",
None,
"Your tokenizer should throw an error whenever there are comments before numbers (stray numbers)"],


["""p0
  (
    F2 L
  )2 (
    F2 R
  )2
q

(
  P// And here! ;)
0
)2""",
None,
"Your tokenizer should throw an error whenever there are comments before numbers (stray numbers)"]

]




#***************************************************************


TESTS_THE_TOKENIZER3 = [

# Invocation of non-existing patterns
["""p134
  F3 L F4 R F5 R F6 L
q

P1341""",
["p134", "F3", "L", "F4", "R", "F5", "R", "F6", "L", "q", "P1341"],
""],


("((F2LP0F2RP3)5(P4P77P143P0)8)13",
["(", "(", "F2", "L", "P0", "F2", "R", "P3", ")5", "(", "P4", "P77", "P143", "P0", ")8", ")13"],
""),


# Unmatched items
["""p37
  F47 L F55 R

P37""",
["p37", "F47", "L", "F55", "R", "P37"],
""],


["F F F L  F F F F F R)10()23478",
["F", "F", "F", "L", "F", "F", "F", "F", "F", "R", ")10", "(", ")23478"],
""],


# Pattern definition within parentheses
["( p30 F93847 q P30 )100",
["(", "p30", "F93847", "q", "P30", ")100"],
""]

]
        





#***************************************************************


TESTS_THE_COMPILER_1 = [

# Description Example in Converter section
["p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3qP0P1P2P3P4",
[               "F", "F", "L", "F", "F", "R",
                "F", "F", "F", "R", "F", "F", "F", "R",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "R", "F", "F", "F", "R",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "R", "F", "F", "F", "R",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "R", "F", "F", "F", "R",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "R",
                "F", "F", "R",
                "F", "F", "F", "R",
                "F", "F", "F", "F", "R"
            ], ""],


# Description Example in Converter section - Pattern Invocation before Definition
["P0P1P2P3P4p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3q",
[               "F", "F", "L", "F", "F", "R",
                "F", "F", "F", "R", "F", "F", "F", "R",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "R", "F", "F", "F", "R",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "R", "F", "F", "F", "R",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "R", "F", "F", "F", "R",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "F", "F", "F", "F", "L",
                "F", "R",
                "F", "F", "R",
                "F", "F", "F", "R",
                "F", "F", "F", "F", "R"
            ], ""],

# A few more examples based on Description code snippets
["""p0
  (
    F2 L
  )2 (
    F2 R
  )2
q

(
  P0
)2""",
["F", "F", "L", "F", "F", "L", "F", "F", "R", "F", "F", "R", "F", "F", "L", "F", "F", "L", "F", "F", "R", "F", "F", "R"], ""],


["""// The global scope can "see" P1 and P2
p1
  // P1 can see P2, P3 and P4
  p3
    // P3 can see P1, P2 and P4 though invoking
    // P1 will likely result in infinite recursion
    F L
  q
  p4
    // Similar rules apply to P4 as they do in P3
    F P3
  q

  F P4
q
p2
  // P2 can "see" P1 and therefore can invoke P1 if it wishes
  F3 R
q

(
  P1 P2
)2 // Execute both globally defined patterns twice""",
["F", "F", "F", "L", "F", "F", "F", "R", "F", "F", "F", "L", "F", "F", "F", "R"], ""],


["""p1
  p1
    F R
  q

  F2 P1 // Refers to "inner" (locally defined) P1 so no infinite recursion results
q

(
  F2 P1 // Refers to "outer" (global) P1 since the
  // global scope can"t "see" local P1
)4

/*
  Equivalent to executing the following raw commands:
  F F F F F R F F F F F R F F F F F R F F F F F R
*/""",
["F", "F", "F", "F", "F", "R", "F", "F", "F", "F", "F", "R", "F", "F", "F", "F", "F", "R", "F", "F", "F", "F", "F", "R"], ""],



# Edge Assertions - patterns defined but not invoked
["p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3q",
[], ""],



# Edge Assertions - multiple pattern ID clashes but each in different scopes
["""
p2017
  (
    P666 P1024
  )4
q
p1024
  p666
    p1024
      p666
        p1024
          L
        q

        F P1024
      q

      F P666
    q

    F P1024
  q

  F P666
q
p666
  p1024
    p666
      p1024
        p666
          R
        q

        F P666
      q

      F P1024
    q

    F P666
  q

  F P1024
q

P2017
""",
["F", "F", "F", "F", "R", "F", "F", "F", "F", "L", "F", "F", "F", "F", "R", "F", "F", "F", "F", "L", "F", "F", "F", "F", "R", "F", "F", "F", "F", "L", "F", "F", "F", "F", "R", "F", "F", "F", "F", "L"],
""],


# Edge Assertion - A nested pattern definition should be able to see the global scope
["""
p0
  p2
    p0
      (
        P1
      )2
    q

    (
      P0
    )2
  q

  (
    P2
  )
q

(
  P0
)

p1
  F7 R
q
""",
["F", "F", "F", "F", "F", "F", "F", "R", "F", "F", "F", "F", "F", "F", "F", "R", "F", "F", "F", "F", "F", "F", "F", "R", "F", "F", "F", "F", "F", "F", "F", "R"],
""],



["""
p0
  p2
    p0
      (
        P1
      )2
    q

    (
      P0
    )2
  q

  (
    P2
  )
q

(
  P0
)

p1
  p0
    p2
      p1
        p0
          p2
            p1
              F R
            q

            F P1
          q

          F P2
        q

        F P0
      q

      F P1
    q

    F P2
  q

  F P0
q
""",
["F", "F", "F", "F", "F", "F", "F", "R", "F", "F", "F", "F", "F", "F", "F", "R", "F", "F", "F", "F", "F", "F", "F", "R", "F", "F", "F", "F", "F", "F", "F", "R"],
""],


# Edge Assertion - Infinite recursion and invoking non-existent patterns
# should be a runtime error
["""
p0
  (
    (
      (
        (
          F2 L F3 R
        )2
      )
    )2
  )2
q
p1
  F3 P1 F2
q
p2
  F L P3 F R
q
p3
  F R P2 F L
q
p4
  p1
    F3 P1 F2
  q
  p2
    F L P3 F R
  q
  p3
    F R P2 F L
  q

  L P1 R P2 L P3 R
q
p5
  F5 (
    P16
  )5 L2
q

P0
""",
["F", "F", "L", "F", "F", "F", "R", "F", "F", "L", "F", "F", "F", "R", "F", "F", "L", "F", "F", "F", "R", "F", "F", "L", "F", "F", "F", "R", "F", "F", "L", "F", "F", "F", "R", "F", "F", "L", "F", "F", "F", "R", "F", "F", "L", "F", "F", "F", "R", "F", "F", "L", "F", "F", "F", "R"],
""]
]




        





#***************************************************************


TESTS_THE_COMPILER_2 = [

# Unmatched brackets/pattern definition sequences
["""
p0
  (
    F2 R F4 L
  q
)5

P0
""",
None,
"An error should be thrown at the converter if brackets and/or pattern definition tokens are unmatched"],


# Placing pattern definitions within a bracketed sequence
["""
(
  P0

  p0
    F2 R F4 L
  q
)13
""",
None,
"An error should be thrown at the converter if one or more pattern definitions are nested by a bracketed sequence"],


["""
p1
  (
    P0

    p0
      F2 R F4 L
    q
  )13
q
""",
None,
"Nesting pattern definitions in bracketed sequences should be a compile-time error not a runtime error"],



# Infinite recursion
["""
p1
  R P1 L
q

P1
""",
None,
"An infinitely recursive sequence should throw an error if invoked"],


["""
p3
  F11 P2
q
p2
  P3 F5
q

P2
""",
None,
"An infinitely recursive sequence should throw an error if invoked"],



["""
P10

p10
  p3
    F11 P2
  q
  p2
    P3 F5
  q

  P2
q
""",
None,
"An infinitely recursive sequence should throw an error if invoked"],


# Invoking a non-existent pattern
["P1337",
None,
"voking a non-existent pattern (in the global scope) should throw an error"],


["""
p3017
  F5 (
    P1337
  )3 R2
q

P3017
""",
None,
"Invoking a non-existent pattern (in the global scope) should throw an error"],



# Invoking a pattern invisible to the current scope
["""
p1
  p2
    F5 L F4 R
  q
q
p3
  (
    P2
  )2
q

P3
""",
None,
"Invoking a pattern not visible to the current scope should yield identical behavior as invoking a non-existent pattern"],


["""
p1
  p2
    // empty!
  q
q
p3
  (
    P2
  )2
q

P3 // should still throw an error
""",
None,
"Invoking a pattern not visible to the current scope should yield identical behavior as invoking a non-existent pattern"]

]
        



        





#***************************************************************


TESTS_THE_MACHINE_1 = [

["""/*
  RoboScript Ultimatum (RSU)
  A simple and comprehensive code example
*/

// Define a new pattern with identifier n = 0
p0
  // The commands below causes the MyRobot to move
  // in a short snake-like path upwards if executed
  (
    F2 L // Go forwards two steps and then turn left
  )2 (
    F2 R // Go forwards two steps and then turn right
  )2
q

// Execute the snake-like pattern twice to generate
// a longer snake-like pattern
(
  P0
)2""",
"*  \r\n*  \r\n***\r\n  *\r\n***\r\n*  \r\n***\r\n  *\r\n***",
""]
]

        






#***************************************************************


TESTS_EXECUTE_1 = [

["""/*
  RoboScript Ultimatum (RSU)
  A simple and comprehensive code example
*/

// Define a new pattern with identifier n = 0
p0
  // The commands below causes the MyRobot to move
  // in a short snake-like path upwards if executed
  (
    F2 L // Go forwards two steps and then turn left
  )2 (
    F2 R // Go forwards two steps and then turn right
  )2
q

// Execute the snake-like pattern twice to generate
// a longer snake-like pattern
(
  P0
)2""",
"*  \r\n*  \r\n***\r\n  *\r\n***\r\n*  \r\n***\r\n  *\r\n***",
""]

]






#***************************************************************




import re

class Solution:
    
    ID_PATT_BRA    = r'[PpRFL)](?:0|[1-9]\d*)|[RFLq()]'
    WHITE_COMMENTS = r'\s+|//.*?(?:\n|$)|/\*.*?\*/'
    TOKENIZER      = re.compile(r'|'.join([WHITE_COMMENTS, ID_PATT_BRA, r'.']), flags=re.DOTALL)
    VALID_TOKEN    = re.compile(ID_PATT_BRA)
    IS_NOT_TOKEN   = re.compile(WHITE_COMMENTS, flags=re.DOTALL)
    MOVES          = ((0,1), (1,0), (0,-1), (-1,0))
    
    
    def __init__(self, prog):        self.source = prog
    def convert_to_raw(self,tokens): return [ c for c,r in self.compileCode(tokens) for _ in range(r) ]
    def execute(self):               return self.execute_raw('', self.compileCode(self.get_tokens()))
    
    def compileCode(self, tokens):
        scope = {'parent':None, 'cmd':()}
        return self.applyPatterns(self.parseCode(iter(tokens), scope), scope, 0)
        
    def get_tokens(self):
        tokens = []
        for tok in self.TOKENIZER.findall(self.source):
            if   self.IS_NOT_TOKEN.match(tok): continue
            elif self.VALID_TOKEN.match(tok):  tokens.append(tok)
            elif tok:                          raise Exception("Invalid expression found: {}".format(tok))
        return tokens
        
        
    def execute_raw(self, cmds, todo=None):
        pos, seens, iDir = (0,0), {(0,0)}, 0
        for s,r in todo or ((c,1) for c in cmds):                      # OVERRIDE todo/cmds TO BYPASS SPECIFICATIONS...
            if s == 'F':
                for _ in range(r):
                    pos = tuple( z+dz for z,dz in zip(pos, self.MOVES[iDir]) )
                    seens.add(pos)
            else:
                iDir = (iDir + r * (-1)**(s=='L')) % len(self.MOVES)
        
        miX, maX = ( f(x for x,_ in seens) for f in (min,max))
        miY, maY = ( f(y for _,y in seens) for f in (min,max))
        
        return '\r\n'.join( ''.join('*' if (x,y) in seens else ' ' for y in range(miY, maY+1)) 
                            for x in range(miX, maX+1) )
        
        
    def parseCode(self, tokIter, scope, inPattern=0):
        cmds = [[]]
        for tok in tokIter:
            cmd,r = tok[0], int(tok[1:] or '1')
            isRepeat = cmds[-1] and cmds[-1][-1] and cmds[-1][-1][0]==cmd
            
            if cmd in 'pq' and len(cmds)>1: raise Exception("pattern definition inside brackets")
            
            if cmd == 'p':
                name = tok.upper()
                if name in scope: raise Exception("Invalid pattern: cannot define multiple patterns with the same name at the same level: {}\nScope: {}\n\n{}".format(name, scope, self.source))
                else:
                    freshScope  = {'parent': scope, 'cmds':()}
                    scope[name] = freshScope
                    freshScope['cmds'] = self.parseCode(tokIter, freshScope, 1)
                    
            elif cmd == 'q': 
                if not inPattern: raise Exception('unopened pattern definition')
                inPattern = 0
                break
                
            elif cmd == '(': cmds.append([])
            elif cmd == ')': lst = cmds.pop() ; cmds[-1].extend(lst * r)
            elif isRepeat:   cmds[-1][-1] = (cmd, cmds[-1][-1][1]+r)
            else:            cmds[-1].append( (tok,1) if cmd=='P' else (cmd,r) )
        
        if inPattern:   raise Exception("unclosed pattern definition, last token: "+tok)
        if len(cmds)>1: raise Exception("unclosed brackets, last token: "+tok)
        return cmds[0]
            
    
    def applyPatterns(self, rawCmds, scope, depth):
        if depth==20: raise Exception("Stack overflow")
        lst = []
        for c,r in rawCmds:
            if c[0]!='P': lst.append((c,r))
            else:
                pattern, nextScope = self.reachPattern(scope, c)
                lst.extend( self.applyPatterns(pattern, nextScope, depth+1) )
        return lst
        
        
    def reachPattern(self, scope, name):
        calledP = scope.get(name)
        parent  = scope['parent']
        if calledP is not None: return calledP['cmds'], calledP
        if not parent:          raise Exception("Unknown pattern: " + name)
        return self.reachPattern(parent, name)




import random
def random_program(nesting = 3, brackets_only = False):
    if not nesting:
        result = []
        for _ in range(10):
            result.append('FLR'[random.randint(0, 2)] + (str(random.randint(0, 19)) if 0.5 < random.random() else ''))
        return ' '.join(result)
    elif brackets_only:
        result = []
        for _ in range(10):
            if 0.2 < random.random():
                t = 'FLR'[random.randint(0, 2)] + (str(random.randint(0, 19)) if 0.5 < random.random() else '')
            else:
                t = '(\n%s\n)' % '\n'.join('  ' + l for l in random_program(nesting - 1, True).split('\n')) + (str(random.randint(0, 19)) if 0.5 < random.random() else '')
            result.append(t)
        return ' '.join(result)
    else:
        pids = list(set(random.randint(0, 999999) for _ in range(random.randint(1, 5))))
        patterns = ['P' + str(pid) for pid in pids]
        program = '\n'.join('p%d\n%s\nq' % (pid, '\n'.join('  ' + l for l in random_program(nesting - 1).split('\n'))) for pid in pids) + '\n\n'
        body = []
        for _ in range(10):
            if 0.4 < random.random():
                t = 'FLR'[random.randint(0, 2)] + (str(random.randint(0, 19)) if 0.5 < random.random() else '')
            elif 0.5 < random.random():
                t = '(\n%s\n)' % '\n'.join('  ' + l for l in random_program(nesting - 1, True).split('\n')) + (str(random.randint(0, 19)) if 0.5 < random.random() else '')
            else:
                t = patterns[random.randint(0, len(patterns) - 1)]
            body.append(t)
        return program + ' '.join(body)





@test.describe('The tokenizer')
def test_describe_the_tokenizer():

    def runTests(configTests):
        for program,exp,msg in configTests:
            if exp:
                test.assert_equals(RSUProgram(program).get_tokens(), exp)
            else:
                test.expect_error(msg, lambda: RSUProgram(program).get_tokens())


    TEST_CONFIG = ( ('should correctly tokenize valid RSU program', TESTS_THE_TOKENIZER1),
                    ('should throw an error if one or more invalid tokens are detected', TESTS_THE_TOKENIZER2),
                    ('should correctly tokenize invalid RSU programs containing only valid tokens', TESTS_THE_TOKENIZER3),
                    ('Additional tests', NEW_TESTS_TOKENIZER),
                   )
    
    for msg,data in TEST_CONFIG:
        @test.it(msg)
        def fff(): runTests(data)
    
    
    @test.it('should work for randomly generated RSU-compliant programs')
    def test_it_tokenize_random():
        for _ in range(10):
            source = random_program()
            expected_code_executor = Solution(source)
            expected = expected_code_executor.get_tokens()
            actual_code_executor = RSUProgram(source)
            actual = actual_code_executor.get_tokens()
            test.assert_equals(actual, expected)
    



@test.describe('The compiler')
def test_describe_the_compiler():
    
    def runTests(configTests):
        for program,exp,msg in configTests:
            r = RSUProgram(program)        
            if exp is not None:
                test.assert_equals(r.convert_to_raw(r.get_tokens()), exp)
            else:
                test.expect_error(msg, lambda: r.convert_to_raw(r.get_tokens()))
    
    
    TEST_CONFIG = ( ('should correctly convert valid RSU token sequences into raw command sequences',TESTS_THE_COMPILER_1),
                    ('should throw an error with invalid RSU programs or valid programs with runtime errors', TESTS_THE_COMPILER_2),
                    ('Additional tests', NEW_TESTS_COMPILER),
                   )
    
    for msg,data in TEST_CONFIG:
        @test.it(msg)
        def fff(): runTests(data)
        
        
    @test.it('should work for randomly generated RSU-compliant programs')
    def test_it_convert_random():
        for _ in range(10):
            source = random_program(2)
            expected_code_executor = Solution(source)
            expected = expected_code_executor.convert_to_raw(expected_code_executor.get_tokens())
            actual_code_executor = RSUProgram(source)
            actual = actual_code_executor.convert_to_raw(actual_code_executor.get_tokens())
            test.assert_equals(actual, expected)
    



@test.describe('The machine instructions executor')
def test_describe_the_machine():

    def runTests(configTests):
        for program,exp,msg in configTests:
            r = RSUProgram(program)        
            if exp:
                test.assert_equals(r.execute_raw(r.convert_to_raw(r.get_tokens())), exp)
            else:
                raise Exception("Error tests routine not implemented")
                

    TEST_CONFIG = ( ('should work for the example provided in the Description', TESTS_THE_MACHINE_1), )
    
    for msg,data in TEST_CONFIG:
        @test.it(msg)
        def fff(): runTests(data)
    
        
        
    @test.it('should work for randomly generated RSU-compliant programs')
    def test_it_execute_random():
        for _ in range(10):
            source = random_program(2)
            
            expected_code_executor = Solution(source)
            expected = expected_code_executor.execute_raw(expected_code_executor.convert_to_raw(expected_code_executor.get_tokens()))
            
            actual_code_executor = RSUProgram(source)
            actual = actual_code_executor.execute_raw(actual_code_executor.convert_to_raw(actual_code_executor.get_tokens()))
            
            test.assert_equals(actual, expected)
    




@test.describe('The machine instruction executor')
def test_describe_mixup():
    
    def runTests(configTests):
        for program,exp,msg in configTests:        
            if exp: test.assert_equals(RSUProgram(program).execute(), exp)
            else:   raise Exception("Error tests routine not implemented")
                
                
    TEST_CONFIG = ( ('should work for the example provided in the Description', TESTS_EXECUTE_1), )
    
    for msg,data in TEST_CONFIG:
        @test.it(msg)
        def fff(): runTests(data)
        

    @test.it('should work for randomly generated RSU-compliant programs')
    def test_it_mixup_random():
        for _ in range(10):
            source   = random_program(2)
            expected = Solution(source).execute()
            actual   = RSUProgram(source).execute()
            test.assert_equals(actual, expected)










"""
***********************************
          AST GENERATOR
***********************************
                  (by B4B, 04/2019)
            

GRAMMAR FOR VALID RSU PROGRAMS:
-------------------------------

Program   ::= Expr+

Expr      ::= ExprNoPat | Pattern

ExprNoPat ::= Call | Cmd | Loop | Comment
            
Pattern   ::= 'p' + Number + Expr* + 'q'

Loop      ::= '(' + ExprNoPat* + ')' + Number?

Call      ::= 'P' + Number
Cmd       ::= ('F' | 'R' | 'L') + Number?
Comment   ::= '//' + Any* + '\n'
            | '/*' + Any* + '*/'

Any       ::= any alphanumerical character
Number    ::= '0' | [1-9] + [0-9]*
"""


from itertools import chain
from collections import defaultdict
from random import randrange as rand, choice, choices, shuffle

def empty(x): return ""

class Messer(object):
    """ Root object, that manages the generation of the whole 
        tree and then generates errors in it when needed """
        
    def __init__(self, profile):
        if not hasattr(self, profile):
            raise Exception(f"Invalid Messer profile: {profile} isn't implemented.")
            
        self.profile          = profile
        self.nodesDct         = defaultdict(list)         # elements inside comments aren't archived
        self.restricted       = set()
        self.archiving        = True
        self.patternsByLvl    = {}                        # {depth: [patterns]}
        self.allPatNames      = []
            
    
    def isAllowed(self, klass):  return klass.__name__ not in self.restricted
    def authorize(self, klass):  self.restricted.remove(klass.__name__)
    def forbid(self, klass):     self.restricted.add(klass.__name__)
    def pick(self, what):        return choice(self.nodesDct[what] or [None])
    def randStr(self):           return ''.join(chr(rand(32,125)) for _ in range(rand(3,10)))
    
    def insertThis(self,n,o):
        if n.nodes: n.nodes.insert(rand(len(n.nodes)), o)
        else:       n.nodes.append(o)
    
    def generateFakePattern(self, head=''):
        cmds = [Cmd(self, force='') for _ in range(rand(5))]
        for n in cmds: n.generate()
        return f'{ head or self.prog.genPatWith("p") }{ "".join(str(n) for n in cmds) }q'
    
    def archive(self, node):
        if self.archiving:
            self.nodesDct[node.__class__.__name__].append(node)
    
    def restraint(self, that, activate=1):
        self.archiving = not activate
        if activate: self.forbid(that)
        else:        self.authorize(that)
        
        
        
    """ ----------------------------
           Generation functions
        ----------------------------
    """
        
    def create(self):
        self.prog = Program(self)
        self.prog.compact()                            # rearrange the tree, suppressing useless levels
        self.prog.buildScopes()
        self.genPatternNamesByLevel()
        self.allPatNames = list({p.head: p for p in self.nodesDct['Pattern']})
        self.computeVisibleScopesWithNames()
        self.fillCommentsRandomly()
        self.genNonLoopingCalls()
        self.messWithIt()
        return str(self.prog)
        
    
    def genPatternNamesByLevel(self):
        self.patternsByLvl = defaultdict(list)
        for p in self.nodesDct['Pattern']:
            self.patternsByLvl[p.depth].append(p)
        
        lst = list( map(self.patternsByLvl.get, sorted(self.patternsByLvl.keys())) )
        
        oldNames, oldSet = [], set()
        for i,lvl in enumerate(lst):
            names = set()                                                                # no duplicated names at the same level
            while len(names)!=len(lvl):
                name = self.prog.genPatWith('p') if not i or rand(2) else choice(oldNames)    # pick a name from upper scopes from time to time
                names.add(name)
            
            oldNames.extend(names-oldSet)
            oldSet |= names
            for p,name in zip(lvl,names): p.head = name
    
    
    def computeVisibleScopesWithNames(self):
        self.prog.computeVisibleScope()
        for p in self.nodesDct["Pattern"]: p.computeVisibleScope()
        
        
    def fillCommentsRandomly(self):
        for cmt in self.nodesDct["Comment"]: cmt.fillItRandomly()
    
    
    def genNonLoopingCalls(self):
        for call in self.nodesDct["Call"]:
            if call.head=='P':
                call.genCalls(set())
    
    
    def messWithIt(self): STATS[self.profile] += bool(getattr(self, self.profile)())
    # Note: STATS is defined just before the actual execution of the random
    # AST tests (used to keep track of what's going on with the generator
                
                
            
    """ ----------------------------
        Messing functions (profiles)
        ----------------------------
    """
    
    def manageStuff(self, stuff, strategy, provider=empty):
        x = self.pick(stuff)
        if x is None: return 0
        if strategy==-1:  provider(x)
        elif strategy==0: x.head = provider(x)
        else:             x.tail = provider(x)
        return 42
        
        
    def valid(self): return 42           # needed declaration for the security check in the constructor of Messer
                                         # (note: very rarely, this can generate a loop in the program)
        
    def unkownCmd(self):             return self.manageStuff('Cmd',      0, lambda p: self.randStr() )
    def unclosedBracket(self):       return self.manageStuff('Loop',     1)
    def unopenedBracket(self):       return self.manageStuff('Loop',     0)
    def unclosedComment(self):       return self.manageStuff('Comment',  1)
    def unopenedComment(self):       return self.manageStuff('Comment',  0)
    def unclosedPattern(self):       return self.manageStuff('Pattern',  1)
    def unopenedPattern(self):       return self.manageStuff('Pattern',  0, lambda p: '' if rand(2) else 'p' )
    def invalidPatternName_0x(self): return self.manageStuff('Pattern',  1, lambda p: 'p0' + p.head[1:] )
    def duplicatedPattern(self):     return self.manageStuff('Pattern', -1, lambda p: self.genDupPatt(p) )
    def patternInLoop(self):         return self.manageStuff('Loop',    -1, lambda p: self.genPattInLoop(p) )
    
    def genDupPatt(self, pat):
        dup = self.generateFakePattern(pat.head)
        self.insertThis(pat.parentPat, Cmd(self, force=dup))
    
    def genPattInLoop(self, loop):
        pat  = self.generateFakePattern()
        self.insertThis(loop, Cmd(self, force=pat))
        
    
    def unknownPatCall_atRoot(self):
        while 1:
            callTo = self.prog.genPatWith('P')
            if callTo not in self.allPatNames: break
        self.insertThis(self.prog, Cmd(self, force=callTo))
        return 42
    
    def callInaccessiblePattern(self):
        pat  = not rand(8) and self.pick('Pattern') or self.prog
        cnds = list(set(self.allPatNames) - { p.head for p in pat.visible})
        if not cnds: return
        inaccessible = choice(cnds).upper()
        self.insertThis(pat, Cmd(self, force=inaccessible) )
        return 42
    
    def makeLoop(self):
        deepest = max(self.nodesDct['Pattern'], key=lambda p: (bool(p.calledBy), p.depth), default=None)
        if deepest is None or not deepest.calledBy:
            return
        
        chain = (deepest.calledBy | {deepest}) - {self.prog}
        pat   = min(chain, key=lambda p: p.depth)
        
        while 1:
            pat, callTo = pat.parentPat, pat.head.upper()
            self.insertThis(pat, Cmd(self, force=callTo))
            if pat is self.prog: break
            chain.add(pat)
        
        looper    = choice(list(chain))
        uppers    = [n for n in chain if n.depth<=looper.depth]
        loopedCmd = choice(uppers).head.upper()
        self.insertThis(looper, Cmd(self, force=loopedCmd) )
        return 42
        
        
        
        
"""
***********************
         AST
***********************
"""



class Node(object):            # Abstract-like class (never instantiated directly)
    
    TO_ARCHIVE = True                                     # See Comment class
    TREE       = None                                     # See Transparent class: self.generate will throw an error if TREE isn't overriden properly
    OCCURENCES = ()                                       # See Transparent class: Same here. Supposed to be a tuple as boundaries for range(a, rand(a,b))
    MAX_DEPTH  = 4                                        # limit the depth of nested patterns
    
    
    def __init__(self, parent, d=0, force=None):
        isProg = isinstance(parent,Messer)                     # identify the root call/instance
        self.messer    = parent if isProg else parent.messer
        self.parent    = None   if isProg else parent
        self.parentPat = self.parent and self.getParentPattern()
        self.nodes     = []                                    # children nodes
        self.head      = '' if force is None else force        # used as default element string (Cmd, Call, ...)
        self.tail      = ''
        self.depth     = d                                     # limit the depth of the ast when creating it, then overwriten for Patterns and Program when building scopes
        self.calledBy  = set()
        self.heldCalls = []
        
        if force is None:
            if self.TO_ARCHIVE: self.messer.archive(self)
            if self.isHungry(): self.nodes = self.generate()
        
            
    
    def __str__(self):                       return self.head + ''.join(map(str, self.nodes)) + self.tail
    def __hash__(self):                      return id(self)
    
    def genNumber(self, limit=None):         return str(rand(limit)) if limit else str(rand(1000 if rand(4) else 10))
    def genMaybeWithNum(self,s,limit=None):  return s if rand(2) else s + self.genNumber(limit)
    def genPatWith(self, sym):               return sym + self.genNumber()
    def isHungry(self):                      return self.depth < self.MAX_DEPTH
    def hold(self, call):                    self.heldCalls.append(call)
    
    def getParentPattern(self):
        p = self.parent
        return p if isinstance(p,(Pattern,Program)) else p.getParentPattern()
    
    
    def compact(self):
        lst = []
        for n in self.nodes:
            if isinstance(n, (Wrapped,Transparent)): n.compact()
            if isinstance(n, Transparent):
                lst.extend(n.nodes)
                for x in n.nodes: x.parent = self
            else:
                lst.append(n)
        self.nodes = lst
        
    
    def buildScopes(self, scopeUp=None, scopeHere=None, depth=None):           # used on valid AST only, so no pattern inside a Loop node
        self.scopeUp   = scopeUp or set()
        self.scopeHere = scopeHere or set()
        self.scopeDown = {n for n in self.nodes if isinstance(n,Pattern)}  
        self.depth     = depth or 0                                            # override the depth for the patterns
        
        nextUp = self.scopeUp | self.scopeHere
        for n in self.scopeDown:
            n.buildScopes(nextUp, self.scopeDown, self.depth+1)
    
    
    def computeVisibleScope(self):
        self.visibleDct = {}
        for p in (*self.scopeUp, *self.scopeHere, *self.scopeDown):            # keep the order for correct override of outer patterns by inner patterns
            self.visibleDct[p.head] = p
        self.visible = set(self.visibleDct.values())
            
    
    def fillItRandomly(self):
        for n in self.nodes:
            whichOne = rand(2) or not self.messer.allPatNames 
            if isinstance(n,Call) and rand(100)<80:
                n.head += self.genNumber() if whichOne else choice(self.messer.allPatNames)[1:]
            elif isinstance(n,Pattern):
                if rand(100)<80:
                    n.head += self.genNumber() if whichOne else choice(self.messer.allPatNames)[1:]
                n.fillItRandomly()
            


#--------------------------------



class Terminal(Node):
    def clarify(self):  return '' if CLARIFY else super().__str__()

class Call(Terminal):
    def __init__(self, parent, d):
        super().__init__(parent,d)
        self.parentPat.hold(self)
        
    def generate(self): self.head = 'P' ; return []        # call names are actually generated after complete creation of the tree, just put a 'P' for early debugging purpose
    
    def genCalls(self, chainPat):
        
        parent   = self.parentPat
        chainPat = chainPat | {parent}
        cnds     = list(parent.visible - chainPat - parent.calledBy)
        shuffle(cnds)
        
        while 1:
            if not cnds: self.head = '' ; return
            called = cnds.pop()
            if called not in chainPat: break
        
        called.calledBy |= chainPat
        self.head = called.head.upper()
        
        for c in called.heldCalls:
            if c.head == 'P': c.genCalls(chainPat)
            

class Cmd(Terminal):
    def generate(self): self.head = self.genMaybeWithNum(choice('FLR'), 10) ; return []
    def __str__(self):  return self.clarify() if not self.head or "p" != self.head[0].lower() else super().__str__()
        
        

#--------------------------------



class Wrapped(Node):
    def clarify(self,withLoops=1): return '' if CLARIFY and not (withLoops and isinstance(self,Loop)) else super().__str__()


class Comment(Wrapped):

    TYP = (("//","\n"), ("/*","*/"))
    
    def __init__(self, messer, d=0):
        super().__init__(messer, d)
        self.head, self.tail = self.TYP[rand(2)]
    
    def generate(self):
        if not self.isHungry(): return []
        self.messer.restraint(Comment, activate=1)
        lst = self.genComment()
        self.messer.restraint(Comment, activate=0)
        return lst
    
    def genComment(self): return Expr(self, self.depth+1).nodes
    def __str__(self):    return self.clarify() if WITH_COMMENT else ''
    
    
class Loop(Wrapped):

    def __init__(self, messer, d=0):
        super().__init__(messer, d)
        self.head, self.tail = '(', self.genMaybeWithNum(')', 10)
        
    def generate(self): return ExprNoPat(self, self.depth+1).nodes if self.isHungry() else []
    def __str__(self):  return self.clarify(withLoops=True)



class Pattern(Wrapped):

    def __init__(self, messer, d=0):
        super().__init__(messer, d)
        self.head, self.tail = 'pq'
        self.scopeUp    = set()          # defined at upper level
        self.scopeHere  = set()          # defined at same level than 'self'
        self.scopeDown  = set()          # defined nested
        self.visible    = set()          # {Pattern()} : all callables for this scope (storing raw patterns, with "overriden" awareness)
        self.visibleDct = {}             # {p.head: Pattern()}
        self.calledBy   = set()          # {Pattern()}
        
    def generate(self):   return Expr(self, self.depth+1).nodes if self.isHungry() else []



#--------------------------------


class Transparent(Node):
    def getTree(self, depth):
        return self.TREE if depth<self.MAX_DEPTH else self.SHORT_TREE
    
    def generate(self):
        a,b  = self.OCCURENCES
        tree = self.getTree(self.depth)
        x    = [ klass(self, self.depth)
                     for klass in choices(tree, k=rand(a,b+1))
                     if self.messer.isAllowed(klass)]
        return x

class ExprNoPat(Transparent):
    TO_ARCHIVE, OCCURENCES = False, (1,5)
    TREE       = (Cmd, Cmd, Cmd, Cmd, Cmd, Cmd, Call, Loop, Comment)
    SHORT_TREE = TREE[:-2]

class Expr(Transparent):
    TO_ARCHIVE, OCCURENCES = False, (1,5)
    TREE       = (ExprNoPat, ExprNoPat, ExprNoPat, Pattern)
    SHORT_TREE = TREE[:1]
    
class Program(Transparent):                        # will get the fields related to Patterns too... (used as root scope/"pattern")
    TO_ARCHIVE, OCCURENCES = False, (1,10)
    TREE = SHORT_TREE = (Expr,)








N_TESTS          = 200
DEBUG            = 0
WITH_STATS       = 0

CLARIFY          = 0      # exclude all that is not patterns, calls or loops from the resulting string
WITH_COMMENT     = 1      # remove all comments for more readability

STATS            = defaultdict(int)
SUCCESS          = defaultdict(int)
CNTS             = defaultdict(int)

LOW_PRIORITY     = "unclosedComment unopenedComment".split()
TOKEN_PROFILES   = "unkownCmd unclosedBracket unopenedBracket unclosedPattern unopenedPattern invalidPatternName_0x".split()
RUNTIME_PROFILES = "makeLoop makeLoop unknownPatCall_atRoot callInaccessiblePattern duplicatedPattern".split()
                    # 'makeLoop" is doubled: WANTED
                    # This is because there are a lot of cases where the loop won't be generated 
                    # or will be generated but won't be called. So some of them will be counted as "valid" programs
                    
                    


@test.describe('Various valid and invalid tests with randomly generated AST')
def fullRandom():
    
    @test.it('Random tests')
    def fff():
    
        config = LOW_PRIORITY + TOKEN_PROFILES*3 + RUNTIME_PROFILES*3
        config.extend( ['valid'] * (len(config)//2) )                    # a lot of the "makeLoop" tests will generate valid code, so no need to push more into it
        
        n, r    = divmod(N_TESTS,len(config))
        config *= n+bool(r)
        shuffle(config)
        
        #config = ['callInaccessiblePattern']*N_TESTS
        
        for profile in config[:N_TESTS]:
            
            CNTS[profile] += 1
            try:
                m = Messer(profile)
                prog = m.create()
            except Exception as e:
                print(profile)
                raise e
            
            if DEBUG: 
                print("profile: ", profile)
                print(prog)
            
            try:
                expected = Solution(prog).execute()
                SUCCESS[profile] += 1
            except Exception as e:
                expected = None
            
                
            # Regular assertion procedure
            func = lambda: RSUProgram(prog).execute()
            if expected is None:
                test.expect_error('should fail with an invalid program', func)
            else:
                test.assert_equals(func(), expected)
        
        
        
if WITH_STATS: 
    print(f'Number of tests: {sum(CNTS.values())}')
    for k in sorted(STATS):
        print(f'{k:<25}: {STATS[k]}/{CNTS[k]} generation ok ; {SUCCESS[k]}/{CNTS[k]} working')
    print(f"\nOverall: { N_TESTS-sum(SUCCESS.values()) } failed / { N_TESTS } tests")
            
