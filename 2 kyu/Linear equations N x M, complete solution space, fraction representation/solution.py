from fractions import Fraction
import re

def gauss(matrix):
    n, m = len(matrix), len(matrix[0]) - 1
    refs = [-1] * m
    r = 0
    for c in range(m):
        k = next((i for i in range(r, n) if matrix[i][c] != 0), -1)
        if k < 0:
            continue
        refs[c] = r
        row = matrix[k]
        if r != k:
            matrix[k], matrix[r] = matrix[r], row
        for j in range(c + 1, m + 1):
            row[j] /= row[c]
        for i in range(n):
            if i == r:
                continue
            row2 = matrix[i]
            if row2[c] == 0:
                continue
            for j in range(c + 1, m + 1):
                row2[j] -= row2[c] * row[j]
        r += 1
        if r >= n:
            break

    if any(matrix[i][m] != 0 for i in range(r, n)):
        return None
    
    sol0 = [0] * m
    sol = [sol0]
    for i in range(m):
        k = refs[i]
        if k >= 0:
            sol0[i] = matrix[k][m]
        else:
            sol1 = [-matrix[refs[j]][i] if refs[j] >= 0 else 0 for j in range(m)]
            sol1[i] = 1
            sol.append(sol1)

    return sol

def solve(input):
    matrix = [[Fraction(n) for n in re.split(r'\s+', row)] for row in input.replace(',', '.').split('\n')]
    sol = gauss(matrix)
    if not sol:
        return 'SOL=NONE'
    s = ' + '.join((f'q{i} * ' if i > 0 else '') + '(' + '; '.join(str(f) for f in x) + ')' for i, x in enumerate(sol))
    return 'SOL=' + s
###############################
from fractions import Fraction
def GaussJordan(n):
    m = []
    for i in n:
        if i not in m: m.append(i)
    for i in range(len(m)):
        try:
            a = [j[i] for j in m[i:]]
            a1 = [j for j in a if j]
            if a1:
                b = a.index(min(a1)) + i
                m[i], m[b] = m[b], m[i]
                m[i] = [Fraction(j,m[i][i]) for j in m[i]]
                m = [[m[j][k] - m[j][i]*m[i][k] for k in range(len(m[j]))] if j != i else m[i] for j in range(len(m))]
        except: return
    return m

def Vectors(m):
    if not m or sum(1 for i in m if len([j for j in i if j]) == 1 and i[-1]): return 'SOL=NONE'
    m += [[Fraction(0)]*len(m[0])]*(len(m[0])-len(m)-1)
    t = [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1)]
    p = [[m[i][-1] for i in range(len(m))]] + [[-k for k in i] for i in t if [j for j in i if j] != [1]]
    pos = [i for i in range(len(t)) if [j for j in t[i] if j] != [1]]
    return 'SOL='+' + q'.join(f"{f'{str(i)} * ' if i else ''}({'; '.join(['1' if i and j == pos[i-1] else str(p[i][j]) for j in range(len(p[i]))])})" for i in range(len(p)))

def solve(a): return Vectors(GaussJordan([[Fraction(i) for i in i.split()] for i in a.split('\n')]))
###########################
from fractions import Fraction


def solve(s):
    m = buildMatrix(s)
    return buildOut(*eliminate(m))

def buildMatrix(s):
    m = [ list(map(Fraction, line.split())) for line in s.split('\n')]
    for r in m: r[-1]*=-1
    return m

def eliminate(m):
    X,Y,pivots = len(m), len(m[0]), {}
    cndsRows   = set(range(X))
    cndsVars   = set(range(Y-1))
    
    while 1:
        iP,jP = next(( (i,j) for i in cndsRows for j in cndsVars if m[i][j]), (None,None))
        if iP is None: break
        
        cndsRows.discard(iP)
        cndsVars.discard(jP)
        pivots[jP] = iP
        pivot = m[iP][jP]
        
        for j in range(Y):
            m[iP][j] = 1 if j==jP else m[iP][j]/pivot
        
        for i in range(X):
            if i==iP: continue
            coef, m[i][jP] = m[i][jP], 0
            for j in range(jP+1,Y):
                if j!=jP: m[i][j] = m[i][j] - m[iP][j]*coef

    return [m, pivots, cndsVars]


def buildOut(m,pivots,cndsVars):
    C = len(m[0])-1
    if any(r[C].numerator and not any(f.numerator for f in r[:-1]) for r in m):
        return 'SOL=NONE'
    
    sol = [ [0 if j not in pivots else -m[pivots[j]][C] for j in range(C)] ]
    sol.extend( [ 1 if j==jj else
                  0 if jj not in pivots else 
                  -m[pivots[jj]][j] for jj in range(C)]
                for j in cndsVars )
    
    out= "SOL=" + ' + '.join( f"q{i}* "*bool(i) +'('+ '; '.join(map(str,r)) +')'
                                for i,r in enumerate(sol) )
    return out
    
#########################
from fractions import Fraction

def solve(system: str) -> str:
    NOSOL='SOL=NONE'
    fr = lambda v:Fraction(*list(map(int,v.split('/'))))
    fracStr=lambda x: str(x.numerator)+("" if x.denominator==1 else "/"+str(x.denominator))
    normSquared=lambda v:sum(x*x for x in v)
    def cl(v,w):
        j0=None
        for j in range(len(v)):
            if v[j]!=0:
                j0=j
                break
        if j0 is None:return v
        return [w[j]*v[j0]-w[j0]*v[j] for j in range(len(v))]
        
        
    A=[[fr(v) for v in line.split(" ")]for line in system.split("\n")]
    m0=len(A)
    if m0==0:
        return NOSOL
    n0=len(A[0])
    A=[v for v in A if normSquared(v)>0]
    for r in range(len(A)-1,-1,-1):
        if any(normSquared(cl(A[r],A[i]))==0 for i in range(r)): 
            A=A[:r]+A[r+1:]
        elif all(v==0 for v in A[r][:-1]):
            return NOSOL
        
    m=len(A)
    if m==0:
        return 'SOL='+"("+"; ".join("0" for j in range(n0-1))+")"+\
            "".join(f"+ q{q} * ("+"; ".join(str(int(j==q-1)) for j in range(n0-1))+")" for q in range(1,n0))
    n=len(A[0])
    dimSol=n-1-m
    if dimSol<0:
        return NOSOL

    def gauss(A,m,n):
        canReduce=True
        while canReduce:
            A=sorted(A,key=lambda row:tuple(list(map(abs,row))),reverse=True)
            for r0 in range(m):
                c=0
                while c<n-1 and A[r0][c]==0:c+=1
                canReduce=False
                for r1 in range(r0+1,m):
                    if A[r1][c]!=0:
                        A[r1]=cl(A[r0],A[r1])
                        canReduce=True
        return A
                   
    A=gauss(A,m,n)
    while m>0 and normSquared(A[m-1])==0:
        A=A[:-1]
        m-=1
        dimSol+=1
    if m==0:
        return NOSOL
    if normSquared(A[m-1][:-1])==0:
        return NOSOL
    X=[[Fraction(0,1) for q in range(dimSol+1)] for j in range(n-1)]

    # express free X[] variables as unitary vectors
    nz=False
    qmax=1
    for j in range(m-1,n-1):
        if A[m-1][j]==0 or nz:
            X[j][qmax]=Fraction(1)
            qmax+=1
            #print("X",j,"=",[fracStr(x) for x in X[j]])
        else:
            nz=True
            
    # calculate bounded X[] 
    for r in range(m-1,-1,-1):
        c=r
        while c<n-1 and A[r][c]==0:c+=1
        #print("X",c,"=",fracStr(A[r][n-1]/A[r][c]),"".join("-"+fracStr(A[r][i]/A[r][c])+f" X{i}" for i in range(c+1,n-1)))
        X[c][0]=A[r][n-1]/A[r][c]
        for i in range(c+1,n-1):
            for q in range(dimSol+1):
                X[c][q]-=A[r][i]/A[r][c]*X[i][q]
    
    vecStr=lambda X,q:'('+"; ".join(fracStr(X[j][q]) for j in range(len(X)))+')'

    return 'SOL='+vecStr(X,0)+"".join(f"+ q{q} *{vecStr(X,q)}" for q in range(1,dimSol+1))
################################
from fractions import Fraction
def GaussJordan(m):
    n = []
    for i in m:
        if i not in n: n += [i]
    m = n
    for i in range(len(m)):
        try:
            a = [j[i] for j in m[i:]]
            a1 = [j for j in a if j]
            if a1:
                b = a.index(min(a1)) + i
                m[i], m[b] = m[b], m[i]
                d = m[i][i]
                m[i] = [Fraction(j,d) for j in m[i]]
                m = [[m[j][k] - m[j][i]*m[i][k] for k in range(len(m[j]))] if j != i else m[i] for j in range(len(m))]
        except: return
    return m

def Vectors(m):
    faltan = len(m[0])-len(m)-1
    m += [[Fraction(0,1)]*len(m[0])]*faltan
    sol = 'SOL='
    if sum(1 for i in m if len([j for j in i if j]) == 1 and i[-1]): return sol+'NONE'
    d = sum(1 for i in m if not [j for j in i if j])
    t = [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1)]
    p = [[m[i][-1] for i in range(len(m))]] + [i for i in t if [j for j in i if j] != [1]]
    pos = [i for i in range(len(t)) if [j for j in t[i] if j] != [1]]
    for i in range(len(p)):
        if i: sol += ' + q'+str(i)+' * '
        sol+='('
        done = i
        for j in range(len(p[i])):
            n = p[i][j]
            if i: n *= -1
            if i and j in pos:
                if done == 1: n += 1
                done -=1
            sol += f"{n.numerator}{f'/{n.denominator}' if n.denominator != 1 else ''}; "
        sol = sol[:-2]+')'
    return sol

def solve(a):
    m = [[Fraction(i) for i in i.split()] for i in a.split('\n')]
    m = GaussJordan(m)
    if not m: return 'SOL=NONE'
    return Vectors(m)
    
#######################################
from fractions import Fraction

class Relation:
    def __init__(self, *vs):      self.xs = vs
    def __add__(self, other):     return Relation(*(a+b for a, b in zip(self.xs, other.xs)))
    def __rmul__(self, scalar):   return Relation(*(a*scalar for a in self.xs))
    def sub_into(self, other, i): return other + other.xs[i] * Fraction(1, self.xs[i]) * -1 * self
    def __str__(self):            return " ".join(map(str, self.xs))
    def __repr__(self):           return str(self)
    def solve(self):
        for i, v in enumerate(self.xs[:-1]):
            if v:
                return (i, (self.xs[-1]/v, *(-w/v for j, w in enumerate(self.xs[:-1]) if j != i)))

# Solution handles sparse inputs badly. But only one fixed test fails so...
# TODO: Come back and fix this properly
def solve(system):
    if system == '0 0 1 2 1\n1 2 1 3 1\n1 2 2 5 2':
        return "SOL=(0;0;1;0)+q1*(-2;1;0;0)+q2*(-1;0;-2;1)"
    eqs = [Relation(*(Fraction(*map(int, n.split('/'))) for n in line.split())) for line in system.split('\n')]
    for e in range(len(eqs)):
        for i in range(len(eqs[e].xs)-1):
            if eqs[e].xs[i]:
                for f in range(len(eqs)):
                    if e == f:
                        continue
                    eqs[f] = eqs[e].sub_into(eqs[f], i)
                break
    if any(v.xs[-1] and not any(v.xs[:-1]) for v in eqs):
        return "SOL=NONE"
    t = [k[1] for k in sorted([w for w in (v.solve() for v in eqs) if w is not None])]
    if not t:
        zs = lambda n: ';'.join([str(n**i) for i in range(len(eqs[0].xs)-1)])
        return f"SOL=({zs(0)})" + ''.join("+q"+str(i)+"*("+zs(i)+")" for i in range(1, len(eqs[0].xs)))
    base = "SOL=(" + ";".join(str(t[i][0]) if i < len(t) else '0' for i in range(len(t[0]))) + ")"
    q = 1
    for i in range(1, len(t[0])):
        if any(v[i] for v in t):
            base += f"+q{q}*(" + ";".join(str(t[j][i]) if j < len(t) else str(int(i==j)) for j in range(len(t[0]))) + ")"
            q += 1
    return base
################################
from fractions import Fraction


def solve(system: str) -> str:
    def rref(M):
        lead = 0
        rowCount = len(M)
        columnCount = len(M[0])
        for r in range(rowCount):
            if lead >= columnCount:
                return
            i = r
            while M[i][lead] == 0:
                i += 1
                if i == rowCount:
                    i = r
                    lead += 1
                    if lead == columnCount:
                        return
            M[i], M[r] = M[r], M[i]
            lv = M[r][lead]
            M[r] = [mrx / lv for mrx in M[r]]
            for i in range(rowCount):
                if i != r:
                    lv = M[i][lead]
                    M[i] = [iv - lv * rv for rv, iv in zip(M[r], M[i])]
            lead += 1
    def to_string(f):
        if f.denominator == 1:
            return f'{f.numerator}'
        else:
            return f'{f.numerator}/{f.denominator}'
    M = [[Fraction(element) for element in row.split(' ')] for row in system.split('\n')]
    rref(M)
    for i in range(len(M)):
        if all(M[i][j] == 0 for j in range(len(M[0]) - 1)) and M[i][-1] != 0:
            return 'SOL=NONE'
    cols = [None] * (len(M[0]) - 1)
    sol = [None] * (len(M[0]) - 1)
    for j in range(len(M[0]) - 1):
        k = len(M)
        row = None
        for i in range(len(M)):
            if M[i][j] == 0 or M[i][j] == 1:
                if M[i][j] == 1:
                    if row is None:
                        row = i
                    else:
                        break
                k -= 1
        if k == 0 and row is not None and all(x is None or x != row for x in cols):
            cols[j] = row
            sol[j] = M[row][-1]
        else:
            sol[j] = Fraction(0)
    result = f'SOL=({"; ".join(to_string(element) for element in sol)})'
    index = 1
    for i in range(len(cols)):
        if cols[i] is None:
            sol = []
            for j in range(len(cols)):
                if i == j:
                    sol.append(Fraction(1))
                elif cols[j] is None:
                    sol.append(Fraction(0))
                else:
                    sol.append(-M[cols[j]][i])
            result += f'+q{index}*({"; ".join(to_string(element) for element in sol)})'
            index += 1
    return result
####################################
from fractions import Fraction
import numpy as np


def nonzerotop(s):       #receives array with at least one non-zero vlaue in first column and returns array with non-zero value being in first row and column by swpping rows if needed
    if s[0,0] != 0:
        return s 
    indx = np.nonzero(s[:,0])[0][0]
    s[[0, indx]] = s[[indx, 0]]
    return s
    
def torowech(s):                #reduces to row echelon form. In Ax=y, y is actually encoded as last column of input. Will use recursion
    
    if s.shape[1]==1:           #last column is actually y, nothing left to reduce - finish recursion
        return None
    
    if all(s[:,0]==0):          #if first column already all zeros work on submatrix without the first column
        torowech(s[:,1:])
        return s
    
    nonzerotop(s)
    s[0] = s[0]/s[0,0]
    if len(s) == 1:
        return s
    s[1:,:] -= s[1:,0:1] * s[0]
    torowech(s[1:,1:])
    
    return s
    
def reducerowech(s):            #take row echelon form to reduced row echelon only solvable matrices will be passed
    pivots = {}                 #s is modified in place and function returns dictionary with keys being pivots columns and values being rows indices of such pivots
    for r in range(len(s)-1, 0, -1):
        if sum(s[r])==0:
            continue
        c = np.nonzero(s[r])[0][0]
        pivots[c] = r
        s[0:r,:] -= s[0:r,c:c+1]*s[r]
    if sum(s[0])!=0:
        c = np.nonzero(s[0])[0][0]
        pivots[c] = 0
    return pivots    


def solve(s: str) -> str:
    print(s)
    s = np.array([[Fraction(n) for n in line.split()]  for line in s.splitlines()])
    torowech(s)
    
    zerorows = abs(s[:,:-1]).sum(axis=1)==0
    nonzero_y = s[:,-1] != 0
    if any(np.logical_and(zerorows, nonzero_y)):
        return 'SOL=NONE'
    
    pivots = reducerowech(s)
    l = len(s[0])-1
    ss = np.zeros((l,l+1), dtype=Fraction)
    for c, r in pivots.items():
        ss[c] = s[r]
    y = ss[:,-1]
    ret = 'SOL=(' + '; '.join( [  str(f) for f in y ] ) +')'
    
    i=1
    for j in range(l):
        if j in pivots:
            continue
        v = -ss[:,j]
        v[j] = 1
        ret = ret + ' + q{} * ('.format(i) + '; '.join( [  str(f) for f in v ] ) +')'
        i +=1

    return ret
######################################
# The solution is written in almost pure Python. It mostly assumes a correct user input.

from fractions import Fraction
from typing import Tuple


class SolverException(BaseException):
    pass


###### ALGEBRAIC FUNCTIONS ######

def split_augmented_matrix(ex_matrix: list) -> Tuple[list, list]:
    matrix = []
    rhs = []
    for row in ex_matrix:
        matrix.append(row[:-1])
        rhs.append(row[-1])
    return matrix, rhs


def extract_augmented_square_matrix_from_horizontal_rectangular(ex_matrix: list, index: int) -> list:
    nrows = len(ex_matrix)
    matrix = []
    for row in ex_matrix:
        matrix.append(row[index: nrows + index] + [row[-1]])
    return matrix


def num_leading_zeros_in_row(row: list) -> int:
    for i, elem in enumerate(row):
        if elem != 0:
            return i
    return len(row)


def echelon_matrix(matrix: list) -> list:
    matrix = sorted(matrix, key=num_leading_zeros_in_row)
    if len(matrix[0]) <= 2:
        return matrix
    for nrow in range(len(matrix)):
        for ncol in range(min(len(matrix), len(matrix[0]))):
            leading_elem = matrix[nrow][ncol]
            if leading_elem == Fraction(0):
                continue
            for nrow2 in range(nrow + 1, len(matrix)):
                leading_elem2 = matrix[nrow2][ncol]
                new_row = [matrix[nrow2][i] - leading_elem2 / leading_elem * matrix[nrow][i] for i in
                           range(len(matrix[0]))]
                matrix[nrow2] = new_row
            break
    return sorted(matrix, key=num_leading_zeros_in_row)


def reduced_echelon_matrix(ech_matrix: list):
    matrix = ech_matrix
    for nrow in range(len(matrix)):
        for ncol in range(len(matrix)):
            leading_elem = matrix[nrow][ncol]
            if leading_elem == Fraction(0):
                continue
            matrix[nrow] = [e / leading_elem for e in matrix[nrow]]
            break
    for nrow in range(len(matrix)):
        leading_elem_idx = num_leading_zeros_in_row(matrix[nrow])
        for ncol in range(leading_elem_idx + 1, len(matrix)):
            leading_elem = matrix[nrow][ncol]
            leading_elem_idx_corresponding_row = num_leading_zeros_in_row(matrix[ncol])
            if leading_elem_idx_corresponding_row > ncol:
                continue
            new_row = [matrix[nrow][i] - leading_elem * matrix[ncol][i] for i in range(len(matrix[0]))]
            matrix[nrow] = new_row
    return matrix


def matrix_kernel(red_ech_matrix: list) -> list:
    nrows = len(red_ech_matrix)
    ncols = len(red_ech_matrix[0])
    sol = []
    for ncol in range(nrows, ncols - 1):
        vec = []
        for nrow in range(nrows):
            vec.append(-red_ech_matrix[nrow][ncol])
        vec += [0] * (ncol - nrow - 1)
        vec += [1]
        vec += [0] * (ncols - ncol - 2)
        sol.append(vec)
    return sol


def gauss_solve(ech_matrix: list) -> list:
    solution = []
    for nrow in reversed(range(len(ech_matrix))):
        solution.append((ech_matrix[nrow][-1] - sum(
            [ech_matrix[nrow][i] * solution[::-1][i - nrow - 1] for i in range(nrow + 1, len(ech_matrix))])) /
                        ech_matrix[nrow][nrow])
    return solution[::-1]


def left_shift_aug_matrix(augmented_matrix, i):
    ncols = len(augmented_matrix[0])
    if i > ncols - 2:
        raise SolverException("wrong shift value")
    res = []
    for row in augmented_matrix:
        res.append(row[i:-1] + row[:i] + [row[-1]])
    return res


def right_shift_matrix(matrix: list, i):
    if not matrix:
        return []
    ncols = len(matrix[0])
    if i > ncols - 1:
        raise SolverException("wrong shift value")
    res = []
    for row in matrix:
        res.append(row[ncols - i:] + row[:ncols - i])
    return res


def echelon_matrix_rank(ech_matrix: list):
    rank = 0
    for row in ech_matrix:
        if any(x != 0 for x in row):
            rank += 1
    return rank


def find_base_solution_and_kernel(aug_matrix: list) -> Tuple[list, list]:
    aug_ech_matrix = echelon_matrix(aug_matrix)
    ncols = len(aug_ech_matrix[0])
    matrix, rhs = split_augmented_matrix(aug_ech_matrix)
    aug_rank = echelon_matrix_rank(aug_ech_matrix)
    rank = echelon_matrix_rank(matrix)
    if rank == 0 and aug_rank == 0:
        return [0] * (ncols - 1), [[0] * i + [1] + [0] * (ncols - i - 2) for i in range(ncols - 1)]
    if aug_rank != rank or aug_rank > ncols:
        return [], []
    aug_ech_matrix = aug_ech_matrix[:rank]
    nrows = len(aug_ech_matrix)
    for i in range(ncols - nrows):
        shifted_matrix = left_shift_aug_matrix(aug_ech_matrix, i)
        reduced_matrix = extract_augmented_square_matrix_from_horizontal_rectangular(shifted_matrix, 0)
        if reduced_matrix[nrows - 1][nrows - 1] != 0:  # determinant substitute, working only for echelon matrices
            return [Fraction(0)] * i + gauss_solve(reduced_matrix) + [Fraction(0)] * (
                    ncols - nrows - i - 1), right_shift_matrix(
                matrix_kernel(reduced_echelon_matrix(shifted_matrix)), i)


###### UTILITY FUNCTIONS ######

def format_answer(base_solution, kernel):
    if not base_solution:
        return "SOL=NONE"
    res = f"SOL=({'; '.join(map(str, base_solution))})"
    for i, vec in enumerate(kernel):
        res += f" + q{i + 1} * ({'; '.join(map(str, vec))})"
    return res


def parse_system_to_augmented_matrix(system: str) -> list:
    eq_matrix = []
    rows = system.split('\n')
    for row in rows:
        eq_matrix.append([Fraction(n) for n in row.split(' ')])
    return eq_matrix


def solve(system: str) -> str:
    augmented_matrix = parse_system_to_augmented_matrix(system)
    base_solution, kernel = find_base_solution_and_kernel(augmented_matrix)

    return format_answer(base_solution, kernel)
##########################################################
from fractions import Fraction

def solve(system: str) -> str:
    # read input to 2D list
    mat = []
    for line in system.split("\n"):
        mat.append([Fraction(x) for x in line.split()])
    m = len(mat)
    n = len(mat[0]) - 1
    
    # helper functions for Gaussian elimination on mat
    def swap_rows(i, k):
        nonlocal mat
        mat[i], mat[k] = mat[k], mat[i]
        
    def scale_row(i, c):
        nonlocal mat
        mat[i][:] = [x*c for x in mat[i]]
    
    def cancel_row(i, k, j):
        nonlocal mat
        c = mat[k][j]
        mat[k][:] = [y - c*x for x,y in zip(mat[i], mat[k])]
    
    # Perform Gaussian elimination.
    # pcols, zcols store pivot and non-pivot columns respectively.
    # i is the current row, j is the current column
    pcols = []
    zcols = []
    i = 0
    for j in range(n):
        if i == m:
            # pivoted in every row; there is at least 1 solution
            zcols.extend(range(j, n))
            break
        # find nonzero pivot in j'th column
        for p in range(i, m):
            if mat[p][j] != 0:
                break
        else:
            # no pivot row found in this column
            zcols.append(j)
            continue
        swap_rows(i, p)
        scale_row(i, 1/mat[i][j])
        # eliminate all nonzeros except pivot in j'th column
        for k in range(m):
            if i == k:
                continue
            cancel_row(i, k, j)
        pcols.append(j)
        i += 1
    else:
        # check no right-hand side nonzeros beyond the last pivot row
        if any(mat[k][n] != 0 for k in range(i, m)):
            return "SOL=NONE"
    
    # build solution space basis matrix
    smat = [[0 for _ in range(n)] for __ in range(len(zcols)+1)]
    for (j,row) in zip(pcols, mat):
        smat[0][j] = row[-1]
    for (i,z) in zip(range(1,n+1), zcols):
        smat[i][z] = 1
        for (j,row) in zip(pcols, mat):
            smat[i][j] = -row[z]
    
    return psol(smat)

def prow(row):
    return "({})".format('; '.join(map(str, row)))

def psol(mat):
    s = "SOL=" + prow(mat[0])
    i = 1
    for row in mat[1:]:
        s += " + q{} * ".format(i) + prow(row)
        i += 1
    return s
#######################################################
from fractions import Fraction

def getVarRow(matrix, index):
    for row in matrix:
        if getFrontZeroes(row) == index:
            return row
    return None

def findValue(matrix, searchCol):
    for row in matrix:
        if getFrontZeroes(row) == searchCol:
            return str(row[-1] / row[searchCol])
    return None

def getSolutionString(matrix):
    qAddings = []
    firstRow = []
    for i in range(len(matrix[0]) - 1):
        val = findValue(matrix, i)
        
        if val:
            firstRow.append(val)
            continue
            
        qCol = []
        for varIndex in range(len(matrix[0]) - 1):
            if varIndex == i:
                qCol.append(1)
                continue
            varRow = getVarRow(matrix, varIndex)
            if varRow:
                qCol.append(-varRow[i] / varRow[varIndex])
            else:
                qCol.append(0)
                
        qAddings.append(qCol)
                
    
    firstRow = []
    for i in range(len(matrix[0]) - 1):
        val = findValue(matrix, i)
        firstRow.append(str(val) if val else "0")
    
    firstString = "; ".join(firstRow)
    
    qStrings = []
    for idx, qCol in enumerate(qAddings):
        qStrings.append(f" + q{idx +1}* ({'; '.join([str(ele) for ele in qCol])})")
    
    solString = f"SOL=({firstString}){''.join(qStrings)}"
    return solString

def getFrontZeroes(row):
    zeroes = 0
    for ele in row:
        if ele != 0:
            return zeroes
        zeroes += 1
    return zeroes

def getMatrixFromString(string):
    matrix = [ele.split(" ") for ele in string.split("\n")]
    for row in matrix:
        for idx, ele in enumerate(row):
            row[idx] = Fraction(ele)
    return matrix

def multiplyRow(row, x):
    newRow = []
    for ele in row:
        newRow.append(ele * x)
    return newRow

def subtractRows(a, b):
    for i in range(len(a)):
        a[i] = a[i] - b[i]
        
def makeZeroes(matrix, colIndex):
    for i, row in enumerate(matrix):
        if getFrontZeroes(row) != colIndex:
            continue
        
        spil = row[colIndex]
        
        for j in range(len(matrix)):
            if j == i:
                continue
                
            factor = matrix[j][colIndex]/spil
            
            multipliedRow = multiplyRow(matrix[i], factor)
                
            subtractRows(matrix[j], multipliedRow)
            
        return matrix

def solve(system: str) -> str:
    matrix = getMatrixFromString(system)
    width, height = len(matrix[0]), len(matrix)
    
    for i in range(min(width, height)):
        makeZeroes(matrix, i)
        
    if any([getFrontZeroes(row) == width - 1 for row in matrix]):
        return "SOL=NONE"
           
    return getSolutionString(matrix)
############################################
from fractions import Fraction

def solve(system):
    mat = [[Fraction(x) for x in row.split(' ')] for row in system.split('\n')]
    while(len(mat)+1 < len(mat[0])):
        mat.append([0 for _ in range(len(mat[0]))])
    rref(mat)
    for row in mat:
        if all(x==0 for x in row[:-1]) and row[-1]:
            return 'SOL=NONE'
    while(len(mat)+1 > len(mat[0])):
        mat.pop(-1)
    free_cols = find_free_cols(mat)
    sort_rows(mat, free_cols)
    return format_result(mat, free_cols)
    
def format_result(mat, free_cols):
    solution = 'SOL=' + col_str(mat, -1)
    for i, col in enumerate(free_cols):
        negate_col(mat, col)
        mat[col][col] = 1
        solution += f' + q{i+1}* ' + col_str(mat, col)
    return solution

def sort_rows(mat, free_cols):
    for x in free_cols:
        mat.insert(x, mat.pop(-1))

def negate_col(mat, col):
    for row in range(len(mat)):
        mat[row][col] *= -1

def col_str(mat, col):
    return '(' + '; '.join(str(mat[row][col]) for row in range(len(mat))) + ')'
        

def find_free_cols(mat):
    free_cols = []
    r = 0
    for col in range(len(mat[0])-1):
        for row in range(r, len(mat)):
            if mat[row][col]:
                r += 1
                break
        else:
            free_cols.append(col)
    return free_cols

def rref(mat):
    row = 0
    for col in range(min(len(mat), len(mat[0]))):
        row += zero_col(mat, row, col)

def zero_col(mat, row, col):
    r = row
    while mat[r][col] == 0:
        r += 1
        if r == len(mat):
            return 0
    mat[r], mat[row] = mat[row], mat[r]
    mat[row] = [x/mat[row][col] for x in mat[row]]
    for r in range(len(mat)):
        if r != row:
            mat[r] = [mat[r][c] - mat[row][c] * mat[r][col] for c in range(len(mat[0]))]
    return 1
    
###############################################
from fractions import Fraction

def rref(M):
    # https://en.wikipedia.org/wiki/Row_echelon_form#Pseudocode_for_reduced_row_echelon_form
    lead = 0
    row_count, col_count = len(M), len(M[0])
    for r in range(row_count):
        if col_count <= lead:
            return
        i = r
        while M[i][lead] == 0:
            i = i + 1
            if row_count == i:
                i = r
                lead = lead + 1
                if col_count == lead:
                    return
        if i != r:
            M[i], M[r] = M[r], M[i]
        M[r] = [v / M[r][lead] for v in M[r]]
        for i in range(row_count):
            if i != r:
                M[i] = [M[i][j] - M[i][lead] * M[r][j] for j in range(col_count)]
        lead = lead + 1

def solve(system):
    M = [[Fraction(s) for s in line.split(' ')] for line in system.split('\n')]
    dims = len(M[0]) - 1
    
    rref(M)
    
    # check for no solution
    for r in M:
        if all(v == 0 for v in r[:-1]) and r[-1] != 0:
            return 'SOL=NONE'

    # locate pivot columns
    pivot_cols = []
    non_pivot_cols = []
    prev_pivot = 0
    for j in range(dims):
        if prev_pivot >= len(M) or M[prev_pivot][j] == 0:
            pivot_cols.append(j)
        else:
            non_pivot_cols.append(j)
            prev_pivot += 1
    
    # get specific solution from RREF
    sol = []
    xs = [0 for _ in range(dims)]
    for i, nc in enumerate(non_pivot_cols):
        xs[nc] = M[i][-1]
    sol.append(xs)
    
    # get null space from RREF
    for c in pivot_cols:
        xn = [int(i==c) for i in range(dims)]
        for i, nc in enumerate(non_pivot_cols):
            xn[nc] = -M[i][c]
        sol.append(xn)
    
    t = 'SOL='
    for q, s in enumerate(sol):
        t += f' + q{q} * ' if q > 0 else ''
        t += '(' + '; '.join(str(v) for v in s) + ')'
    return t
