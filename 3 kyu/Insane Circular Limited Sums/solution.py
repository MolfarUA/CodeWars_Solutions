59953009d65a278783000062


from itertools import product

MOD = 12345787
def matrix_mul(A, B):
    n1, n2, m = len(A), len(B[0]), len(B)
    C = [[0] * n2 for i in range(n1)]
    for i, j in product(range(n1), range(n2)):
        C[i][j] = sum(A[i][k] * B[k][j] for k in range(m)) % MOD
    return C

def matrix_pow(A, m):
    n = len(A)
    B = [[0] * n for i in range(n)]
    for i in range(n): B[i][i] = 1
    while m:
        if m & 1: B = matrix_mul(B, A)
        A = matrix_mul(A, A)
        m >>= 1
    return B

def insane_cls(max_n, max_fn):
    A = [[0] * (max_fn + 1) for i in range(max_fn + 1)]
    for i, j in product(range(max_fn + 1), repeat=2):
        if i + j <= max_fn: A[i][j] = 1
    A = matrix_pow(A, max_n)
    return sum(A[i][i] for i in range(max_fn + 1)) % MOD
#####################
def mul_mat(a, b, mod):
    m, p = len(a), len(a[0])
    if p == len(b):
        n = len(b[0])
        c = []
        for i in range(m):
            c.append([])
            for j in range(n):
                c[i].append(sum(a[i][k] * b[k][j] for k in range(p)) % mod)

        return c

    
def pow_mat(a, p, mod):
    m, n = len(a), len(a[0])
    if p == 0:
        return [[+(i == j) for j in range(n)] for i in range(m)]
    
    if p == 1:
        return a

    t = a
    for c in bin(p)[3:]:
        t = mul_mat(t, t, mod)
        if c == '1':
            t = mul_mat(t, a, mod)

    return t


def insane_cls(n, maxf):
    if n == 1:
        return 1 + maxf // 2

    mod = 12345787
    base = [
        [+(i + u <= maxf) for i in range(maxf+1)]
        for u in range(maxf+1)
    ]
    res = 0
    for first_num in range(maxf+1):
        f0 = [[+(u == first_num) for u in range(maxf+1)]]
        fn = mul_mat(f0, pow_mat(base, n-1, mod), mod)
        res = (res + sum(fn[0][:maxf-first_num+1])) % mod

    return res
######################
import numpy as np
def insane_cls(max_n, max_fn):
    def matpow(m, k, mod):
        x, y = np.identity(m.shape[0]), reversed([int(p) for p in bin(k)[2:]])
        for z in y: [m, x] = [np.dot(m, m) % mod, np.dot(x, m) % mod if z else x]
        return x
    p, q = max_fn + 1, max_n - 1
    if q <= 0: return (p-1)//2 + 1
    x, y = np.array([[int(i + j < p) for j in range(p)] for i in range(p)]), np.array([[min(p - i, p - j) for j in range(p)] for i in range(p)])
    return np.sum(y * matpow(x, q - 1, 12345787)) % 12345787
##########################
def matvecmul(mat, vec, mod):
    n = len(mat)
    return [sum(mat[i][j] * vec[j] for j in range(n)) % mod for i in range(n)]

def matmatmul(a, b, mod):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) % mod for j in range(n)] for i in range(n)]

def matpow(a, k, mod):
    if k == 0:
        n = len(a)
        return [[+(i==j) for j in range(n)] for i in range(n)]
    elif k == 1:
        return a
    else:
        b = matpow(matmatmul(a, a, mod), k // 2, mod)
        return matmatmul(b, a, mod) if k % 2 else b

def insane_cls(max_n, max_fn):
    mod = 12345787
    
    if max_n == 1: return 1 + max_fn // 2
    elif max_n == 2: return (max_fn + 1) * (max_fn + 2) // 2 % mod
    
    # Solution idea: loop over each F(max_n) and backtrack the valid solutions of
    # F(n) for n = max_n-1,...,1. The n=1 case specially has two constraints.
    # Each backtracking operation correspond to a linear transformation, so
    # we get an O(log n) algorithm using matrix exponentiation.

    total = 0
    
    mat = [[0] * (1 + max_fn) for _ in range(1 + max_fn)]

    for f_n in range(0, max_fn + 1):
        for f_np1 in range(0, max_fn + 1 - f_n):
            mat[f_n][f_np1] = 1
            
    mat = matpow(mat, max_n - 3, mod)
    
    for f_max_n in range(1 + max_fn):
        arr = [0] * (1 + max_fn) # initialize at n = max_n - 1.
        
        for f_n in range(0, max_fn + 1):
            arr[f_n] = +(f_n + f_max_n <= max_fn)

        arr = matvecmul(mat, arr, mod)

        for f_1 in range(0, max_fn + 1 - f_max_n):
            for f_2 in range(0, max_fn + 1 - f_1):
                total += arr[f_2]

    return total % mod
########################
from copy import deepcopy
P=12345787
def lmul(A,B):
    n=len(A);m=len(B);p=len(B[0])
    C=[[0]*p for i in range(n)]
    for i in range(n):
        for k in range(m):
            for j in range(p):
                C[i][j]+=A[i][k]*B[k][j]%P
                if C[i][j]>=P: C[i][j]-=P
    for i in range(n):
        for j in range(p):
            B[i][j]=C[i][j]

MP=[[]]
for n in range(1,12):
    MP.append([])
    cur=[[0]*n for i in range(n)]
    for i in range(n):
        for j in range(n-i):
            cur[j][i]=1
    for i in range(30):
        MP[n].append(deepcopy(cur))
        lmul(cur,cur)

def insane_cls(max_n,N):
    N+=1;max_n-=1
    
    ans = 0
    for a0 in range(N):
        f=[[0] for i in range(N)];f[a0][0]=1
        k=0
        while max_n>>k:
            if max_n>>k&1: lmul(MP[N][k],f)
            k+=1
        for i in range(N-a0): ans+=f[i][0]
        ans%=P
    ans%=P
    return ans
######################
import numpy as np


def pow(matrix, n):
    if n == 1:
        return matrix

    _matrix = pow(matrix, n//2)
    _matrix = np.dot(_matrix, _matrix) % 12345787

    if n % 2 == 1:
        _matrix = np.dot(_matrix, matrix) % 12345787
    return _matrix

def insane_cls(max_n, max_fn):
    matrix = np.zeros(shape=(max_fn+1, max_fn+1), dtype=np.int64)
    for a in range(max_fn+1):
        for b in range(max_fn+1):
            if a+b <= max_fn:
                matrix[a, b] = 1
    return np.trace(pow(matrix, max_n)) % 12345787
