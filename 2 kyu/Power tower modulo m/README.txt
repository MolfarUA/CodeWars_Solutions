The goal of this kata is to write a function tower(base, height, modulus) that returns base ** base ** ... ** base, with height occurrences of base, modulo modulus. (** is the power operator in Python, in case this kata gets translated.) As input constraints, we have:

1 <= base < 1e20
0 <= height < 1e20
1 <= modulus < 1e7
If modulus == 1, the returned value should be 0 irrespective of the values of the two other parameters. Otherwise, if base == 1 or height == 0, the output should be 1, and, if height == 1, the output should be base % modulus.

For example, tower(2, 4, 1000) should return 536, because: 2 ** 2 ** 2 ** 2 == 2 ** (2 ** (2 ** 2)) == 65536 and 65536 % 1000 == 536.

Note that the power operator is right-associative, meaning that a ** b ** c is computed a ** (b ** c) and not (a ** b) ** c. For example, 2 ** 2 ** 4 == 2 ** 16 == 65536 and 2 ** 2 ** 4 != 4 ** 4 == 256.

Note also that tower(b, h, m) = pow(b, tower(b, h - 1, m), m) is not a correct recursive relationship. For example, tower(13, 3, 31) != pow(13, tower(13, 2, 31), 31). However, tower(13, 3, 31) == pow(13, tower(13, 2, 30), 31).

There are more examples in the example tests.

Some number theory
Since Codewars is for programmers and not mathematicians, I thought that I would provide a minimum of number theory background to let programmers get started.

Given a positive integer m > 1, we can form the set of all integers between 1 and m that are coprime with m. This set can be defined with code as G = {i for i in range(1, m) if gcd(i, m) == 1}, where gcd(a, b) returns the greatest common divisor of a and b. The number of elements in this set is sometimes denoted phi(m), sometimes totient(m).

For example, let m = 15. The prime factors of 15 are 3 and 5. Let's start with the set {1, 2, ..., 15} and remove all the multiples of 3. Every 3rd element is a multiple of 3 and, if they are removed, we are left with 15 * 2 / 3 = 10 elements. Next remove all multiples of 5. Every 5th element is a multiple of 5 and, if they are removed, we are left with 10 * 4 / 5 = 8 elements. So, totient(15) = 8. The set of elements that are coprime with 15 is G = {1, 2, 4, 7, 8, 11, 13, 14}, and, as can be observed, it contains 8 elements. Now, take any element of G and raise it to the first 8 powers modulo 15. For example, the powers of 7 modulo 15 are 7, 4, 13, 1, 7, 4, 13, 1, and the powers of 2 modulo 15 are 2, 4, 8, 1, 2, 4, 8, 1. The powers of any element of G have a cycle length that divides totient(m) and the cycle always ends with 1. In other words, for any b in G and q, r such that 0 <= q and 0 <= r < totient(m),

b ** (q * totient(m) + r) % m == b ** r % m.
This allows us to reduce large powers to powers that are less than totient(m). What if we choose a number b that is not in G. For example, let b = 3. Then the powers of 3 modulo 15 are 3, 9, 12, 6, 3, 9, 12, 6. The cycle length is still a divisor of totient(m), but the cycle does not end with 1. This implies that for b not in G, the statement in the above bullet does not hold. However, it can be amended slighly, so that we can still reduce large powers to smaller powers.
