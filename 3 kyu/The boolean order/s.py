59eb1e4a0863c7ff7e000008


from operator import and_, or_, xor
BOOLS, OPS = {'f': False, 't': True}, {'&': and_, '|': or_, '^': xor}

def memo(f):
    def wrapper(*args):
        if args in cache: return cache[args]
        value = cache[args] = f(*args)
        return value
    cache = {}
    return wrapper

def solve(bools, ops):
    @memo
    def rec(bools, ops):
        if not ops: return [bools[0] == n for n in (0, 1)]
        sums = [0, 0]
        for idx, op in enumerate(ops, 1):
            left, right = rec(bools[:idx], ops[:idx-1]), rec(bools[idx:], ops[idx:])
            for l, r in (0, 0), (0, 1), (1, 0), (1, 1):
                sums[op(l, r)] += left[l] * right[r]
        return sums

    return rec(tuple(map(BOOLS.get, bools)), tuple(map(OPS.get, ops)))[1]
_________________________________________
from functools import lru_cache
from operator import and_, or_, xor

FUNCS = {'|': or_, '&':and_, '^': xor}

def solve(s,ops):

    @lru_cache(None)
    def evaluate(s,ops):
        c = [0,0]
        if not ops:
            c[s=='t'] += 1
        else:
            for i in range(len(ops)):
                for v,n in enumerate(    evaluate(s[:i+1], ops[:i])  ):
                    for w,m in enumerate(evaluate(s[i+1:], ops[i+1:])):
                        c[ FUNCS[ops[i]](v,w) ] += n*m
        return c
    
    return evaluate(s,ops)[True]
_________________________________________
def solve(s, ops):
    n = len(s)
    table = [[[0, 0] for _ in range(n)] for _ in range(n + 1)]
    for start in range(n):
        table[1][start] = [int(s[start] == "f"), int(s[start] == "t")]
    for step in range(2, n + 1):
        for start in range(n + 1 - step):
            for mid in range(start + 1, (stop := start + step)):
                left_false, left_true = table[mid - start][start]
                right_false, right_true = table[stop - mid][mid]
                if (op := ops[mid - 1]) == "&":
                    table[step][start][0] += left_true*right_false + left_false*right_true + left_false*right_false
                    table[step][start][1] += left_true * right_true
                elif op == "|":
                    table[step][start][0] += left_false * right_false
                    table[step][start][1] += left_true*right_false + left_false*right_true + left_true*right_true
                elif op == "^":
                    table[step][start][0] += left_true*right_true + left_false*right_false
                    table[step][start][1] += left_true*right_false + left_false*right_true
    return table[n][0][1]
_________________________________________
solve=s=__import__('functools').lru_cache(None)(lambda b,o,n=1:sum(s(b[:i],o[:i-1],x//2)*s(b[i:],o[i:],x%2)for i,k in enumerate(o,1)for x in range(4)if(1<<x&2*'   ^&  |'.find(k)>0)==n)if o else'ft'[n]==b)
_________________________________________
import numpy as np

def solve(s,ops):
    N = len(s)
    catalan = np.zeros(N, dtype=int) # Catalan numbers
    catalan[0] = 1
    for i in range(1, N):
        for j in range(i):
            catalan[i] += catalan[j] * catalan[i - j - 1]
    num_true = np.zeros((N,N), dtype=int)
    for i in range(N):
        if s[i] == 't':
            num_true[i][i] = 1
        else: # s[i] == 'f'
            num_true[i][i] = 0
    for i in range(1, N): # length of expression
        for j in range(N - i): # beginning index
            for k in range(j, j+i):
                if ops[k] == '&':
                    num_true[j][j+i] += num_true[j][k] * num_true[k+1][j+i]
                elif ops[k] == '|':
                    num_true[j][j+i] += num_true[j][k] * num_true[k+1][j+i] + num_true[j][k] * (catalan[j+i-k-1] - num_true[k+1][j+i]) + (catalan[k-j] - num_true[j][k]) * num_true[k+1][j+i] 
                else: # ops[k] == '^':
                    num_true[j][j+i] += num_true[j][k] * (catalan[j+i-k-1] - num_true[k+1][j+i]) + (catalan[k-j] - num_true[j][k]) * num_true[k+1][j+i] 
    return num_true[0][N-1]
_________________________________________
def solve(s, ops):
    s = list(map(lambda x: True if x == 't' else False, s))
    return solve_(s, ops)


def solve_(s, ops):

    # dp[i][j][k] stores the number of ways to make s[i:j] = k
    dp = [[[0 for k in range(2)] for j in range(len(s) + 1)] for i in range(len(s) + 1)]

    # base case
    for i in range(len(s)):
        dp[i][i][False] = int(not s[i])
        dp[i][i][True] = int(s[i])

    for l in range(1, len(s)):
        for i in range(len(s) - l):
            j = i + l
            for k in range(i, j):
                if ops[k] == '|':
                    dp[i][j][False] += dp[i][k][False] * dp[k + 1][j][False]
                    dp[i][j][True] += dp[i][k][True] * dp[k + 1][j][True] + dp[i][k][False] * dp[k + 1][j][True] + dp[i][k][True] * dp[k + 1][j][False]
                if ops[k] == '&':
                    dp[i][j][False] += dp[i][k][False] * dp[k + 1][j][False] + dp[i][k][True] * dp[k + 1][j][False] + dp[i][k][False] * dp[k + 1][j][True]
                    dp[i][j][True] += dp[i][k][True] * dp[k + 1][j][True]
                if ops[k] == '^':
                    dp[i][j][False] += dp[i][k][True] * dp[k + 1][j][True] + dp[i][k][False] * dp[k + 1][j][False]
                    dp[i][j][True] += dp[i][k][False] * dp[k + 1][j][True] + dp[i][k][True] * dp[k + 1][j][False]

    return dp[0][len(s) - 1][True]
_________________________________________
calc =  {"tt&":1,"tf&":0, "tt|":1,"tf|":1,"tt^":0,"tf^":1}
memo={}

def ways(s):
    global memo
    if s in memo:
        return memo[s]

    if len(s)==1:
        if s=="t": return [0,1]
        else: return [1,0]    
        
    res=[0,0]
    for i in range(1,len(s),2):
        pre=ways(s[0:i])
        post=ways(s[i+1:])
        res[calc["tt"+s[i]]]+=pre[1]*post[1]
        res[calc["tf"+s[i]]]+=pre[1]*post[0]+pre[0]*post[1]
        res[0]+=pre[0]*post[0]
    memo[s]=res
    return res

def solve(s,ops):
    s2=""
    n=len(ops)
    for i in range(n):
        s2+=s[i]+ops[i]
    return ways(s2+s[n])[1]
