from random import randint, uniform

import re
from functools import wraps
from fractions import Fraction
from random import randint, uniform
from itertools import product
from typing import List, Iterator, Callable, Union
import codewars_test as test
from solution import solve

Matrix = List[List[Fraction]]
Vector = List[Fraction]

def test_lgs(lgs: str, sol: str) -> None:
    # 1. Test solution syntax
    # 2. Test whole solution if NONE is expected
    # 3. Test if vectors have the same length
    # 4. Test if fractions are reduced
    # 5. Test the dimension of the solution space
    # 5. Test the particular solution
    # 6. Test random other solutions

    def str_to_frac(n: str, sep: str = ',') -> Fraction:
        if not sep in n: return Fraction(n)
        num, dec = n.split(sep)
        f = Fraction(num)
        for p, d in enumerate(dec, start=1):
            f += Fraction(int(d), 10 ** p)
        return f
        
    def str_to_matrix(M: str) -> Matrix:
        return [[str_to_frac(f) for f in e.split()] for e in M.split('\n')]

    def row_echolon(M: Matrix, row: int = 0, col : int = 0) -> Matrix:
        m, n = len(M), len(M[0])
        for j in range(col, n-1):
            for i in range(row, m):
                if M[i][j] != 0: break
            else: continue
            break
        else: return M
        M = v(M, row, i)
        for k in range(row+1, m):
            if M[k][j] != 0:
                M = add(M, k, -M[k][j] / M[row][j], row)
        return row_echolon(M, row+1, j+1)

    def deepcopy_matrix(f: Callable[..., Matrix]) -> Callable[..., Matrix]:
        @wraps(f)
        def wrapper(*args, **kwargs) -> Matrix:
            res = f(*args, **kwargs)
            return [row[:] for row in res]
        return wrapper

    @deepcopy_matrix
    def v(M: Matrix, i: int, j: int) -> Matrix:
        if i == j: return M
        i, j = sorted((i,j))
        return M[:i] + [M[j]] + M[i+1:j] + [M[i]] + M[j+1:]

    @deepcopy_matrix
    def add(M: Matrix, i: int, a: Union[int, Fraction], j: int) -> Matrix:
        return M[:i] + [[M[i][k] + a * M[j][k] for k in range(len(M[0]))]] + M[i+1:]

    def dimension(M: Matrix) -> int:
        if not M: return 0
        M = row_echolon(M)
        for i in range(len(M) - 1, -1, -1):
            if any(M[i][:-1]): break
            if M[i][-1]: return -1
        else:
            return 0
        return i + 1

    def codimension(M: Matrix) -> int:
        d = dimension(M)
        return -1 if d < 0 else len(M[0]) - d - 1

    def test_vecindices(sol: str) -> bool:
        vs = sol.split('+')[1:]
        r = True
        for i, v in enumerate(vs, 1):
            prefix = f'q{i}*'
            t = v.startswith(prefix)
            r &= t
            test.expect(t, f'{v} should start with {prefix}')
        return r

    def test_veclen(sol: str) -> bool:
        if not 'q' in sol: return True
        v = re.split(r'\+q\d+\*', sol[4:])
        l = list(map(lambda x: len(x.split(';')), v))
        return max(l) == min(l)

    def test_reduced(sol: str) -> List[str]:
        reducible = []
        for v in re.split(r'\+q\d+\*', sol[4:]):
            for f in v[1:-1].split(';'):
                if not '/' in f: continue
                f1, f2 = map(int, f.split('/'))
                F = Fraction(f1, f2)
                if f2 <= 1 or f1 != F.numerator or f2 != F.denominator:
                    reducible.append(f)
        return reducible

    def sol_to_list(sol: str) -> List[Vector]:
        space = []
        for v in re.split(r'\+q\d+\*', sol[4:]):
            space.append([Fraction(f) for f in v[1:-1].split(';')])
        return space

    def vecadd(Ms: Iterator[Vector]) -> Vector:
        Ms = list(Ms)
        l = list(map(len, Ms))
        if max(l) != min(l): raise ArithmeticError('Vectors have different length.')
        n = len(Ms[0])
        return [sum(M[i] for M in Ms) for i in range(n)]

    def transpose(M: Matrix) -> Matrix:
        return [[]] if not M else [[row[j] for row in M] for j in range(len(M[0]))]

    def matmul(a: Matrix, b: Matrix) -> Matrix:
        if len(a[0]) != len(b): raise ArithmeticError('Dimensions of matrices don\'t match.')
        return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
                for j in range(len(b[0]))] for i in range(len(a))]

    def mat_x_vec(a: Matrix, b: Vector) -> Vector:
        res = matmul(a, [[x] for x in b])
        return [x[0] for x in res]

    def vecmul(a: Fraction, v: Vector) -> Vector:
        return [a * x for x in v]

    def get_sol_vector(space: List[Vector], params: List[Fraction]) -> Vector:
        if len(space) != len(params) + 1:
            raise Exception('Wrong number of parameters.')
        params.insert(0, Fraction(1))
        return vecadd(vecmul(q, v) for q, v in zip(params, space))

    def frac_str(F: Fraction) -> str:
        res = str(F.numerator)
        if F.denominator != 1:
            res += f'/{F.denominator}'
        return res

    # regular expression for result syntax
    re_num =  r'-?\d+(/-?\d+)?'
    re_vec = rf'\({re_num}(;{re_num})*\)'
    re_sol = rf'^SOL=((NONE)|({re_vec}(\+q\d+\*{re_vec})*))$'

    Ab = str_to_matrix(lgs)
    A = [row[:-1] for row in Ab]
    b = [row[-1] for row in Ab]
    codim = codimension(Ab)
    u_sol = sol.replace(' ', '')

    # testing syntax, reduced fractions and dimension of solution
    correct_syntax = bool(re.match(re_sol, u_sol))
    test.expect(correct_syntax
               ,f'Something is wrong with your solution formatting: {u_sol}.')
    if not correct_syntax: return
    if codim == -1:
        test.assert_equals(u_sol, 'SOL=NONE')
        return
    test.assert_not_equals(u_sol, 'SOL=NONE', 'Solution exists')
    if u_sol == 'SOL=NONE': return
    is_vec_indices = test_vecindices(u_sol)
    if not is_vec_indices: return
    is_vec_len = test_veclen(u_sol)
    test.expect(is_vec_len, 'Some vectors in your solution have a different amount of elements.')
    if not is_vec_len: return
    reducible = test_reduced(u_sol)
    test.expect(not reducible, f'Some fractions are not reduced: {", ".join(reducible)}')
    if reducible: return

    # testing dimension
    u_sol = sol_to_list(u_sol)
    test.expect(len(u_sol) - 1 == codim
               ,f'The dimension of your solution is {len(u_sol) - 1} but should be {codim}.')
    if len(u_sol) - 1 != codim: return
    sol_space_dim = dimension([vec + [0] for vec in u_sol[1:]])
    test.assert_equals(sol_space_dim, len(u_sol) - 1, f'Vectors spanning the solution space should be linearly independent')
    if sol_space_dim != len(u_sol) - 1: return
    
    # testing particular solution
    partic_sol = get_sol_vector(u_sol, [Fraction(0)] * (len(u_sol) - 1))
    test.assert_equals(mat_x_vec(A, partic_sol), b
                      ,f'Your particular solution ({"; ".join(map(frac_str, partic_sol))}) is not correct.')

    # testing complete solutions
    res = matmul(A, transpose(u_sol))
    for i, row in enumerate(res):
        expected = [b[i]] + [0] * codim
        if row != [b[i]] + [0] * codim:
            nth = '1st' if i + 1 == 1 else '2nd' if i + 1 == 2 else '3rd' if i + 1 == 3 else f'{i + 1}nth'
            r_str = ' + '.join(str(x) + (f' * q{j}' if j > 0 else '') for j, x in enumerate(row) if x or j == 0)
            test.expect(False, f'{nth} equation is not satisfied: {r_str} should equal {b[i]}')

def rnd_matrix(num_eqs: int, num_var: int, *, nrange: int = 30, decimals: bool = False) -> str:
    M = []
    for _ in range(num_eqs):
        row = []
        for _ in range(num_var):
            if decimals and not randint(0, 5):
                row.append(str(round(uniform(-nrange, nrange), randint(1, 2))))
            elif not randint(0, 3):
                a, b = randint(-nrange, nrange), randint(1, nrange)
                row.append(f'{a}/{b}')
            else:
                row.append(str(randint(-nrange, nrange)))
        M.append(' '.join(row))
    return '\n'.join(M)

lgs1 = '\n'.join(['1 2 0 0 7'
                 ,'0 3 4 0 8'
                 ,'0 0 5 6 9'])
                 
lgs2 = '\n'.join(['1 5/2 1/2 0 4 1/8'
                 ,'0 5 2 -5/2 6 2'])
                 
lgs3 = '\n'.join(['0 0 1 2 1'
                 ,'1 2 1 3 1'
                 ,'1 2 2 5 2'])
                 
lgs4 = '\n'.join(['0 0 1 2 1'
                 ,'1 2 1 3 1'
                 ,'1 2 2 5 3'])
                 
lgs5 = '\n'.join(['1 1 2 4 0'
                 ,'-1 -1 -2 -4 0'
                 ,'0 1 1 0 0'
                 ,'0 -1 -1 0 0'])

lgs6 = '\n'.join(['0 0 0',
                  '0 0 0'])

lgs7 = '\n'.join(['0 1 1',
                  '1 1 1'])

lgs8 = '\n'.join(['1/20 -10/3 -10/9 -13',
                  '-29 8 -27/4 0',
                  '-26 -14 25 10/7'])

lgs9 = '1 2 2\n1 2 2\n2 4 4'

lgs10 = '0 0 0 0\n0 0 0 0'

@test.describe('Fixed Tests')
def fixed_tests():
    for lgs in [lgs1, lgs2, lgs3, lgs4, lgs5, lgs6, lgs7, lgs8, lgs9, lgs10]:
        @test.it('')
        def test_fix():
            test_lgs(lgs, solve(lgs))
    
    
@test.describe('Random Tests')
def random_tests():
    for m, n in product([1,3,4,5,7,9,12], [2,4,6,8,9,13,15]):
        @test.it(f'{m} by {n-1} system.')
        def test_rnd():
            new_matrix = rnd_matrix(m, n)
            test_lgs(new_matrix, solve(new_matrix))

