Your task is to solve N x M Systems of Linear Equations (LS) and to determine the complete solution space.
 
Normally an endless amount of solutions exist, not only one or none like for N x N. You have to handle N unkowns and M equations (N>=1, M>=1) and your result has to display all numbers in 'reduced fraction representation' too (perhaps first you can try my N x N kata). More about LS you can find here or perhaps is already known.
 
First of all two easy examples:

1*x1 + 2*x2 + 0*x3 + 0*x4 = 7
0*x1 + 3*x2 + 4*x3 + 0*x4 = 8
0*x1 + 0*x2 + 5*x3 + 6*x4 = 9

SOL=(97/15; 4/15; 9/5; 0) + q1* (-16/5; 8/5; -6/5; 1)
 
You can see the dimension of solution space is 1 (it's a line) and q1 is any real number, so we have endless solutions. You can insert every single solution into every equation and all are correctly solved (1*97/15 + 2*4/15 + 0 + 0 =7 for q1=0).
 
Second example:

1*x1 + 5/2*x2 + 1/2*x3 + 0*x4 + 4*x5 = 1/8
0*x1 + 5*x2 + 2*x3 - 5/2*x4 + 6*x5 = 2

SOL=(-7/8; 2/5; 0; 0; 0) + q1 * (1/2; -2/5; 1; 0; 0) + q2 * (-5/4; 1/2; 0; 1; 0) + q3 * (-1; -6/5; 0; 0; 1)
 
Here you can see the dimension of the solution is 3, q1, q2 and q3 are arbitrary real numbers. You can see all resulting numbers are in fraction representation (which is easier to read and handle for pupils/students), whatever the input was.
 
So what is missing?
 
You have to build a function "Solve(input)" (or "solve(input)") which takes the equations as an input string and returns the solution as a string. "\n" (LF) separates equations, " " (SPACE) separates the numbers (like 3 or 4/5, only the coefficients not the xi's), each last number per line is the number behind the = (the equation result, see examples). The result of the function is the solution given as a string. All test examples will be syntactically correct, so you don't need to take care of it.
 
So for the first example you have to call: Solve ("1 2 0 0 7\n0 3 4 0 8\n0 0 5 6 9"). The result of Solve is "SOL=(97/15; 4/15; 9/5; 0) + q1 * (-16/5; 8/5; -6/5; 1)", exactly in this form/syntax. (97/15; 4/15; 9/5; 0) + q1 * (16/5; -8/5; 6/5; -1) is ok too because it produces same solutions.
 
Spaces in your result are allowed, but not necessary. You have to use 'qi' (i from 1 to dimension) standing for the real numbers (the first starting solution- point/vector has no q). If the dimension of the solution is greater than 1, the order of the qi- vectors isn't important (but all indices should be in order, that is, 'q1' first then 'q2', etc.). The fractions have to be reduced as much as possible (but not 4/3 to 1 1/3). If there exists no solution you have to respond with "SOL=NONE". If only one solution exists the response should contain no 'qi'-vectors (e.g.,"SOL=(1; 2; 3)").
 
One last word to the tests:
The test function checks the syntax of your output, uses some rules for different verifications and after all checks the given equations with your solution and verifies that all equations are satisfied for arbitrary values of qi's. If all things fit together, your solution is accepted! If not, you will get a hint 'why not'...
 
Hint: don't rely on floating-point numbers to solve this kata. Use exact rational arithmetic.
