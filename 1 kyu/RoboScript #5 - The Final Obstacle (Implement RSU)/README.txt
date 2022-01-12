NOTE: It is highly recommended that you complete the first 4 Kata in this Series before attempting this final Kata; otherwise, the description would make little sense.
RoboScript #5 - The Final Obstacle (Implement RSU)
Disclaimer

The story presented in this Kata Series is purely fictional; any resemblance to actual programming languages, products, organisations or people should be treated as purely coincidental.
About this Kata Series

This Kata Series is based on a fictional story about a computer scientist and engineer who owns a firm that sells a toy robot called MyRobot which can interpret its own (esoteric) programming language called RoboScript. Naturally, this Kata Series deals with the software side of things (I'm afraid Codewars cannot test your ability to build a physical robot!).
Story

Since RS3 was released into the market which introduced handy pattern definitions on top of command grouping and repetition, its popularity soared within the robotics community, insomuch that other budding robotics firms have pleaded your company to allow them to use the RoboScript programming language in their products. In order to grant them their requests and protect your company at the same time, you decided to apply for a patent which would allow other companies to utilize RoboScript in their own products with certain restrictions and only with an annual fee paid to your company. So far, so good - the patent application was successful and your firm gained an ample amount of revenue in the first year from this patent alone. However, since RoboScript is still a rather small and domain-specific programming language, the restrictions listed on the patent were rather limited. Competing firms soon found a loophole in the wording of the patent which allowed them to develop their own RoboScript-like programming language with minor modifications and improvements which allowed them to legally circumvent your patent. Soon, these robotics firms start overtaking your company in terms of popularity, profitability and size. In order to investigate the main cause of the downfall of your company, a secret survey was sent to thousands of former MyRobot (and hence "official" RoboScript) users. It was revealed in this survey that the main reason for this downfall was due to the lack of readability of RS3 code (and RoboScript code in general), especially as the program becomes very large and complex. After all, it makes perfect sense - who would even bother to try to understand and maintain the following RS3 code, let alone much larger and complex programs?

p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3qP0P1P2P3P4

In a final attempt to save your company from going bankrupt and disappearing from the world of robotics, you decide to address all of the major issues identified in the secret survey head-on by designing the fourth and final specification for the RoboScript programming language - RoboScript Ultimatum (RSU). The only thing left for you to do is to properly implement the specification by writing an RSU-compliant code executor - once that is achieved, your company will catapult back into 1st position in global robotics and perhaps even leave a mark in the history of technology ...
Task
RoboScript Ultimatum (RSU) - The Official Specification

RoboScript Ultimatum (RSU) is a superset of the RS3 specification (which itself is a superset of RS2, RS2 being a superset of RS1). However, it introduces quite a few new (and handy) features.
1. Whitespace and Indentation Support

In RSU, whitespace and indentation is supported to improve readability and can appear anywhere in the program in any form except within a token itself (explained in more detail later). For example, the program below is valid:

p0
  (
    F2 L
  )2 (
    F2 R
  )2
q

(
  P0
)2

While the following program is not valid:

p 0
  (
    F 2L
  ) 2 (
    F 2 R
  )         2
q

(
  P  0
)2

Of course, the code need not be neatly indented - it should be valid so long as tokens such as p0, F2, )2 do not contain any whitespace themselves.
2. Comment Support

RSU should support single line comments (optional code) // ... and multiline comments /* ... */ like in many other programming languages such as JavaScript. All single line comments are terminated by either of a newline character \n and the end-of-file (EOF) (beware of this edge case ;) ) and multiline comments cannot be nested. For example, this is a valid program with comments:

/*
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
)2

Comments follow the same rules as whitespace and indentation - they can be placed anywhere within the program except within a token itself, e.g. F/* ... */37 is invalid. Both single-line and multiline comments may be empty, i.e. /**/ and //\n are valid.
3. Pattern Scoping

This is much like function and/or block scoping in many other programming languages. While attempts to nest a pattern definition in another pattern yielded undefined behavior in RS3, each pattern will have its own scope in RSU. Furthermore, each pattern will be able to "see" pattern definitions both in its own scope and in any subsequent parent scopes. For example:

// The global scope can "see" P1 and P2
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
)2 // Execute both globally defined patterns twice

Furthermore, an RSU program is still valid if more than one pattern with the same identifier is defined provided that they all appear in different scopes. In case of an identifier conflict between two patterns of different scopes, the definition of the pattern in the innermost scope takes precedence. For example:

p1
  p1
    F R
  q
  
  F2 P1 // Refers to "inner" (locally defined) P1 so no infinite recursion results
q

(
  F2 P1 // Refers to "outer" (global) P1 since the
  // global scope can't "see" local P1
)4

/*
  Equivalent to executing the following raw commands:
  F F F F F R F F F F F R F F F F F R F F F F F R
*/

However, pattern redefinition in the same scope is not allowed and should throw an error at some stage (more details later).
Finally ...

... no other character sequences are allowed in an RSU program, such as "stray comments" as in this is a stray comment not escaped by a double slash or slash followed by asterisk F F F L F F F R F F F L F F F R and lowercase "flr" are not acceptable as commands or "stray numbers" as in F 32R 298984.

Also, some edge cases in case you're wondering:

    Zero postfixes (e.g. F0, L0 and of course P0) are allowed (F0 and L0 do nothing while P0 invokes pattern with identifier n = 0).
    Empty pattern definitions / bracketed repeat sequences p0 /* (empty) */ q, (), ()23 are allowed.
    Leading zeroes (except for the number 0 itself) should not be allowed - these errors should be thrown during the tokenizing process (more details later) as a "token" containing a number with leading zeroes is an invalid token.
    Pattern definitions can contain brackets within them (of course!) but bracketed sequences must NOT contain any pattern definitions. Such errors should be detected in the second stage of RSU code processing.
    Calls to infinitely recursive patterns and/or non-existent patterns within a bracketed sequence that is executed 0 times should not throw an error; they should simply be ignored.

RSU Code Executor - Structure

In this Kata, your RSU code executor should be a class RSUProgram with a class constructor which accepts a string source, the RSU source code to be executed. No error checking is required in this part.

NOTE: All methods described below must be properly implemented and will be tested extensively in the Submit tests - namely, getTokens, convertToRaw, executeRaw and execute (or the equivalent function/method names in your language, according to your language's naming convention(s)). If in doubt, you may always refer to the Sample Test Cases to get an idea of what will be tested in the Sumbit tests.
Tokenizer

Your class should have an instance method getTokens which accepts no arguments and returns the tokens present in source (argument passed to class constructor) in order as an array. The tokenizer should ignore all whitespace characters (except when they prevent a token from being identified, e.g. in ) 2) and comments and should throw if it encounters one or more invalid tokens in the process. The following tokens are the only valid tokens:

    Single commands F, L and R
    Commands with repeats Fn, Ln and Rn (n being a non-negative integer which may exceed 1 digit but may not contain any leading 0s)
    Opening round brackets (
    Closing round brackets, with or without a repeat prefix ) OR )n (n a non-negative integer with the rules described above)
    Pattern definition pn (n a non-negative integer ... )
    End of pattern definition q
    Pattern invocation Pn (n a non-negative integer ... )

During the tokenizing process, do not perform any form of analysis checking the order of the tokens or whether a particular pattern invoked actually exists, etc. Such errors should be left to later stages.
Compiler

Your class should have an instance method convertToRaw which accepts 1 argument tokens (an array of tokens, ideally returned from the tokenizer in the previous step) and returns an array of raw commands from processing the tokens. "Raw commands" are the most basic commands that can be understood by the robot natively, namely F, L and R (nothing else, not even with prefixes such as F2 or R5). For example, the following RS3-compliant program from the Story:

p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3qP0P1P2P3P4

... can be converted into the following "raw commands" after its tokenized form is passed in to this instance method (indented for better visualization):

[
  "F", "F", "L", "F", "F", "R",
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
]

See the "Sample Tests" for more examples.

Remember from RS3 that placing a pattern invocation before its definition is valid, e.g. P0P1P2P3P4p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3q should produce the same result as the above program. On the other hand, the following RSU programs are invalid and should throw an error at this stage:

    Unmatched bracketing and/or pattern definition sequences, e.g. (p0q or p1(q)34 (an obvious syntax error)
    Nesting pattern definitions within bracketed sequences, e.g. (p0/* ... */q). This should be treated as a syntax error and as such, it should not appear anywhere within the program, even if it is nested within multiple pattern definitions and never invoked.
    Attempting to invoke a non-existent pattern or one that invokes a non-existing pattern definition in its pattern body, etc., in the global scope
    Attempting to invoke an infinitely recursive pattern of any form (including non-recursive patterns which call on infinitely recursive patterns in their pattern body, etc.) in the global scope. Extreme cases (e.g. 500 levels of non-infinite recursion) will not be tested in the test cases so a sensible recursion limit will do.

As for the input token array tokens, you may assume that it will always be valid provided that your tokenizer is working properly ;)
Machine Instruction Executor

Now that you've implemented the most challenging part of your RSUProgram class, it is time to wind down a little and implement something more straightforward :) Your class should have an instance method executeRaw which receives an array of raw commands (consisting of only F, L and/or R) returned from your compiler and returns a string representation of the path that the MyRobot walks on the floor. This string representation is identical in format as the ones required in Kata #2 through #4 of this Series. For example, the raw commands (comparable to machine instructions/code in computers) obtained from this program:

/*
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
)2

... should evaluate to the string "* \r\n* \r\n***\r\n *\r\n***\r\n* \r\n***\r\n *\r\n***".

Once again, you may assume that the array of raw commands passed in will always be valid provided that your tokenizer and compiler are both working properly.

Quick Tip: If you have completed Kata #2 of this Series (Implement the RS1 Specification), you may pass this section by simply copying and pasting your solution to that Kata here and making minor modifications.
One-Step Execution

Hooray - you have successfully implemented an RSU-compliant code executor! In order to tidy things up a little, define an instance method execute which accepts no arguments and combines the three previous instance methods in a way such that when this method is invoked (without invoking any other methods before it), it tokenizes, compiles and executes the source (from the constructor) in one go and returns the string representation of the MyRobot's path. For example:

RSUProgram("""/*
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
)2""").execute(); // => "*  \r\n*  \r\n***\r\n  *\r\n***\r\n*  \r\n***\r\n  *\r\n***"


5a12755832b8b956a9000133
