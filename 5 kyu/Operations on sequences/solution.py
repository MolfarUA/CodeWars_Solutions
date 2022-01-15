def solve(arr):
    a, b, c, d = arr[0:4]
    firstFour = [abs(a*c - b*d), (a*d+b*c)]
    if len(arr) == 4:
        return firstFour
    return solve(firstFour + arr[4:])
_____________________________________
'''
Using the identity 
(x² + y²)(u² + v²) = (xu + yv)² + (xv - yu)²
'''
def solve(arr):
    # your code
    print(arr)
    A = arr[0]
    B = arr[1]
    for i in range(2,len(arr),2):
        A_temp = A*arr[i] + B*arr[i+1]
        B = abs(A*arr[i+1] - B*arr[i])
        A = A_temp
    return [A,B]
_____________________________________
def solve(xs):
    it = iter(xs)
    a, b = 1, 0
    for c, d in zip(it, it):
        a, b = a*c + b*d, abs(a*d - b*c)
    return a, b
_____________________________________
from functools import reduce

def solve(arr):
    mul = lambda a, b: (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
    z = reduce(mul, zip(*[iter(arr)] * 2))
    return (abs(z[0]), abs(z[1]))
_____________________________________
def solve(arr):
    if len(arr) == 4:
        [a, b, c, d] = arr
        return [abs(a*c-b*d), a*d+b*c]
    else:
        temp = solve(arr[0:4])
        temp.extend(arr[4:])
        return solve(temp)
_____________________________________
def redux(l):
    x = l[0]; y = l[1]; z = l[2]; t = l[3]
    u = x * z + y * t; v = x * t - y * z
    result = [u, v]
    return result
def solve(arr):
    if len(arr) == 2:
        return [abs(arr[0]), abs(arr[1])]
    return solve(redux(arr[-4:]) + arr[:-4])
_____________________________________
def solve(arr):
    def h(a):
        return [abs(a[0] * a[2] - a[1] * a[3]), abs(a[0] * a[3] + a[1] * a[2])]
    if len(arr) == 4:
        return h(arr)
    return solve(h(arr[0:4]) + arr[4:len(arr)])
_____________________________________
solve=s=lambda a:len(a)>3and s([a[0]*a[2]+a[1]*a[3],abs(a[0]*a[3]-a[1]*a[2])]+a[4:])or a
_____________________________________
import math

def solveFour(arr):
    assert len(arr) == 4
    (a, b, c, d) = arr
    snum = ((a * a) + (b * b)) * ((c * c) + (d * d))
    q1 = (abs(a - b) * min(c, d)) + (abs(c - d) * max(a, b))
    return [q1, math.isqrt(snum - (q1 * q1))]


def solve(arr):
    while 4 < len(arr):
        arr = solveFour(arr[:4]) + arr[4:]
    else:
        return solveFour(arr)
_____________________________________
def solve(arr):
    if len(arr) == 2:
        return arr
    if len(arr) == 4:
        a, b, c, d = arr
        return [abs(a * c - b * d), a * d + b * c]
    return solve([x for i in range(0, len(arr), 4) for x in solve(arr[i: i + 4])])
_____________________________________
def solve(arr):
    a = arr[0]
    b = arr[1]
    for i in range(2,len(arr),2):
        c = arr[i]
        d = arr[i+1]
        na = a*c-b*d
        nb = a*d + b*c
        a=na
        b=nb
        
    return [abs(a),abs(b)]
_____________________________________
def solve(arr):
    i = 0
    x = len(arr)
    res = []
    
    while len(res) != 2:
        temp = arr[:4]
        i = 0
        res.append(abs(temp[i]*temp[i+2] + temp[i+1]*temp[i+3]))
        res.append(abs(temp[i]*temp[i+3] - temp[i+1]*temp[i+2]))
        i = 4
        arr = res + arr[i:]
        if len(arr) == 2:
            return arr
        else:
            res = []
    return res
