def arithmetic_sequence_elements(a, r, n):
    return ', '.join(str(a + b * r) for b in xrange(n))
___________________________
def arithmetic_sequence_elements(a, r, n):
    return ", ".join((str(a+r*i) for i in range(n)))
___________________________
from itertools import count, islice

def arithmetic_sequence_elements(a, r, n):
    return ', '.join([str(x) for x in islice(count(a, r), n)])
___________________________
def arithmetic_sequence_elements(a, r, n):
    return ', '.join(str(a + r*x) for x in range(n))
___________________________
def arithmetic_sequence_elements(a, r, n):
    z = str(a)
    for i in range(n - 1):
        a = a + r
        z = z + ", " + str(a)

    return z
___________________________
def arithmetic_sequence_elements(a, d, n):
    if n == 1:
        return str(a)
    else:
        return str(a) + ', ' + arithmetic_sequence_elements(a + d, d, n - 1)
___________________________
def arithmetic_sequence_elements(a, r, n):
    return ", ".join(f"{a + i*r}" for i in range(n))
___________________________
def arithmetic_sequence_elements(a, r, n):
    return ", ".join(str(a + i*r) for i in range(n))
___________________________
def arithmetic_sequence_elements(a, r, n):
    rng = list(range(a, a + (r * n), r)) if r != 0 else [a] * n
    return ', '.join(map(str,rng))
___________________________
def arithmetic_sequence_elements(a, r, n):
    result = [str(a)]
    for i in range(1, n):
        a = a + r
        result.append(str(a))
    return ", ".join(result)
___________________________
def arithmetic_sequence_elements(a, d, n):
    e = []
    while n > 0:
        e.append(str(a))
        a += d
        n -= 1
    return ', '.join(e)
___________________________
def arithmetic_sequence_elements(a, d, n):
    result = [a]
    for index in range(n-1):
        result.append(result[index]+d)
    return ' '.join(map(lambda x: str(x) + ",", result))[:-1]
___________________________
def arithmetic_sequence_elements(a, d, n):
    x = []
    for i in range(n):
        x.append(str(a))
        a = a + d
    return ', '.join(x)
___________________________
def arithmetic_sequence_elements(a, d, n):
    lis = []
    while n > 0:
        lis.append(str(a))
        a += d
        n -= 1
    return ', '.join(lis)
