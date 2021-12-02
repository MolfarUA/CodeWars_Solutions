Problem Description
You build a string of length l which entirely consists of n types of characters 1, 2, ..., n.

Let's define such a string "permutation-free" if it has no substring which is a permutation of 12...n (in other words, substring of length n which contains all types of characters exactly once).

For n = 2, it means that '12' and '21' are not allowed, so the only possible permutation-free strings are 11...1 and 22...2.

For n = 3, strings like 1111, 3311, and 1223 are permutation-free, while 1232, 3231, and 3122 are not.

How many permutation-free strings can you make, given the values of n and l? Since your answer will be very large, please give your answer modulo 12345787.

Constraints
3 <= n <= 5

n <= l <= 100

The inputs will be always valid integers.

Examples
permutation_free(3, 3) == 3 ** 3 - 3! == 21
permutation_free(3, 4) == 51
permutation_free(3, 5) == 123
permutation_free(3, 10) == 10089

permutation_free(4, 4) == 4 ** 4 - 4! = 232
permutation_free(4, 5) == 856
permutation_free(4, 10) == 3160

permutation_free(5, 5) == 5 ** 5 - 5! = 3005
permutation_free(5, 6) == 14545
permutation_free(5, 10) == 8001745
Acknowledgement
This problem was inspired by Project Euler #458: Permutations of Project.

If you enjoyed this Kata, please also have a look at my other Katas!
