Regular Expression for Binary Numbers Divisible by n
Create a function that will return a regular expression string that is capable of evaluating binary strings (which consist of only 1s and 0s) and determining whether the given string represents a number divisible by n.

Tests
Inputs 1 <= n <= 18 will be tested

Each n will be tested against random invalid tests and random valid tests (which may or may not pass the regex test itself, accordingly).

Notes
Strings that are not binary numbers should be rejected.
Keep your solution under 5000 characters. This means you can't hard-code the answers.
Only these characters may be included in your returned string: 01?:*+^$()[]|
Python Notes
Whenever you use parentheses (...), instead use non-capturing ones (?:...). This is due to module re's restriction in the number of capturing (or named) groups, which is capped at 99.
Each regex will be tested with re.search, so be sure to include both starting and ending marks in your regex.
The second anti-cheat test checks if you used any of re, sys, or print in your code. You won't need to print anything since each test will show what numbers your code is being tested on.
