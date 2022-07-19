This Kata is an insane step-up from my previous Kata, so I recommend to solve it first before trying this one.

Problem Description
Let's imagine a function F(n), which is defined over the integers in the range of 1 <= n <= max_n, and 0 <= F(n) <= max_fn for every n.

There are (1 + max_fn) ** max_n possible definitions of F in total.

Out of those definitions, how many Fs satisfy the following equations? Since your answer will be very large, please give your answer modulo 12345787.

F(n) + F(n + 1) <= max_fn for 1 <= n < max_n
F(max_n) + F(1) <= max_fn
Constraints
1 <= max_n <= 10 ** 9

1 <= max_fn <= 10

The inputs will be always valid integers.

Examples
# F(1) + F(1) <= 1, F(1) = 0
insane_cls(1, 1) == 1

# F = (0, 0), (0, 1), (1, 0)
insane_cls(2, 1) == 3

# F = (0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0)
insane_cls(3, 1) == 4

# F = (0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0),
# (0, 1, 0, 1), (1, 0, 0, 0), (1, 0, 1, 0)
insane_cls(4, 1) == 7

# F = (0), (1)
insane_cls(1, 2) == 2
# F = (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)
insane_cls(2, 2) == 6
# F = (0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1),
# (0, 2, 0), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1), (2, 0, 0)
insane_cls(3, 2) == 11
insane_cls(4, 2) == 26
Acknowledgement
This problem was designed as a hybrid of Project Euler #209: Circular Logic and Project Euler #164: Numbers for which no three consecutive digits have a sum greater than a given value.

If you enjoyed this Kata, please also have a look at my other Katas!


59953009d65a278783000062
