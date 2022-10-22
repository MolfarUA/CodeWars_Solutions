63178f6f358563cdbe128886


Description:

A continuation kata published: Integer factorization: CFRAC basics
General info

A continued fraction is a mathematical expression of the following form:
[a0;a1,a2,a3,...,an,...]=a0+1a1+1a2+1⋱+1an+…[a_0; a_1, a_2, a_3, ..., a_n, ...] = a_0 + \cfrac{1}{ a_1 + \cfrac{1}{ a_2 + \cfrac{1}{ \ddots + \cfrac{1}{a_n + \dots} } } }[a0​;a1​,a2​,a3​,...,an​,...]=a0​+a1​+a2​+⋱+an​+…1​1​1​1​

Any real number may be represented in the following form with integer coefficients. In fact, all rational numbers have finite representation, and all irrational numbers have infinite representation. The latter case is exactly, what we've come for today :D

The specific numbers we are obsessed with in this kata are square roots of natural numbers. Continued fractions of square roots are periodic and always take a specific form:
N=[a0;a1,a2,a3,...,a3,a2,a1,2a0‾]=a0+1a1+1a2+1⋱+1a2+1a1+12a0+1a1+…\sqrt{N} = [a_0; \overline{a_1, a_2, a_3, ..., a_3, a_2, a_1, 2 a_0}] = a_0 + \cfrac{1}{ a_1 + \cfrac{1}{ a_2 + \cfrac{1}{ \ddots + \cfrac{1}{a_2 + \cfrac{1}{ a_1 + \cfrac{1}{ 2 a_0 + \cfrac{1}{ a_1 + \dots } } }} } } }N
​=[a0​;a1​,a2​,a3​,...,a3​,a2​,a1​,2a0​​]=a0​+a1​+a2​+⋱+a2​+a1​+2a0​+a1​+…1​1​1​1​1​1​1​
The task

Your task will be to write a generator function to yield integer coefficients of the continued fraction of sqrt(N). Not only coefficients must be precise, but you'll have to deal with numbers up to 2^1024.

Tip: the amount of coefficients before hitting the period is bounded by 0.72 * sqrt(N), but obviously we cannot generate that much in adequate time for big numbers. The test suite expects your code to generate 2000-4000 coefficients for a single number.
