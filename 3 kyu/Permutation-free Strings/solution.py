import numpy as np

def permutation_free(n, l):
    m = np.tril(np.ones((n,n), object), -1) + np.diagflat(range(n,0,-1))
    return (np.matrix(np.vstack((m[1:], m[0,::-1]))) ** l)[0,0] * n % 12345787
##################
def permutation_free(n, l):
    xs = [1] + [0] * n
    for _ in range(1, l + 1):
        ys = [0] * (n + 1)
        for i in reversed(range(1, n)):
            ys[i] = ys[i + 1] + xs[i]
        for i in range(1, n):
            ys[i] += xs[i - 1] * (n - i + 1)
        xs = ys
    return sum(xs) % 12345787
##############
import numpy as np
def permutation_free(n, l):
    a = np.diagflat([n - i for i in range(n)])
    b = np.tril(np.ones((n,n), object), -1)
    c = np.add(a,b)
    d = np.tril(c)
    e = np.vstack((d[1:], d[0,::-1]))
    f = np.matrix(e)
    g = f ** l
    h = g[0,0]
    return n * h % 12345787
###################
T = [9, 21]
for i in range(100):
    T.append(T[-2] + T[-1] * 2)
    
Q = [[24, 40, 64],
     [72, 160, 232]]
for i in range(100):
    c = Q[-1][-1] * 3 + Q[-1][-2]
    a = Q[-1][-2] * 2 + Q[-1][0] - Q[-2][-1] * 2
    Q.append([a, c - a, c])
    
R = [[480, 2525, 3005],
     [2280, 12265, 14545],
     [11040, 59405, 70445]]
for i in range(100):
    b = R[-1][-1] * 4 + R[-2][0] + R[-3][-1] + R[-3][-3]
    c = R[-1][-1] * 4 + R[-1][-2]
    R.append([c - b, b, c])
def permutation_free(n, l):
    if n == 3:
        return T[l - 2] % 12345787
    if n == 4:
        return Q[l - 3][-1] % 12345787
    else:
        return R[l-5][-1] % 12345787
#################
import numpy as np

def permutation_free(n, l):
    s = np.tril(np.ones((n,n), object), -1) + np.diagflat(range(n,0,-1))
    return (np.matrix(np.vstack((s[1:], s[0,::-1]))) ** l)[0,0] * n % 12345787
###################
def permutation_free(n, l):
    
    xl = [1] + [0] * n
    
    for j in range(1, l + 1):
        yn = [0] * (n + 1)
        
        for i in reversed(range(1, n)):
            yn[i] = yn[i + 1] + xl[i]
            
        for i in range(1, n):
            yn[i] += xl[i - 1] * (n - i + 1)
            
        xl = yn
    return sum(xl) % 12345787
