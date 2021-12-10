#test verification
def format_ar(r):
    return '\n'.join([''.join(['{:>2}'.format(str(v)) for v in x]) for x in r])

def solved_puzzle(n):
    r = [[i*n+c+1 for c in range(n)] for i in range(n)]
    r[n-1][n-1] = 0
    return format_ar(r)

def verify_solvable(ar,x):
    ln = len(ar)
    flatr = []
    for v in ar:
        flatr.extend(v)
    flatr = list(filter(lambda x:x,flatr))
    vr = [i+1 for i in range(ln**2-1)]
    invr = 0
    for v in flatr:
        q = vr.index(v)
        vr.pop(q)
        invr += q
    invr = invr % 2
    return invr == 0 if ln % 2 else (ln - x) % 2 != invr

def vsol(ar,sol):
    for i,v in enumerate(ar):
        if 0 in v:
            x = i
            break
    y = ar[x].index(0)
    error_msg = 'Puzzle has not achieved a solved state'
    if not verify_solvable(ar,x):
        test.assert_equals(sol,None,'This puzzle is unsolvable.')
        return
    if not sol or type(sol) != list or not all([type(v) == int for v in sol]):
        test.expect(False,'Invalid solution type.')
        return
    r = [v[:] for v in ar]
    n = len(ar)
    vmap = solved_puzzle(n)
    for i in range(len(sol)):
        dset = [[x-1,y],[x,y+1],[x+1,y],[x,y-1]]
        nxy = None
        for v1,v2 in dset:
            if v1 >= 0 and v1 < n and v2 >= 0 and v2 < n and r[v1][v2] == sol[i]:
                nxy = [v1,v2]
                break
        if not nxy:
            error_msg = 'Invalid move'
            break
        r[x][y],r[nxy[0]][nxy[1]] = r[nxy[0]][nxy[1]],r[x][y]
        x,y = nxy
    res = format_ar(r)
    test.expect(res == vmap,'Error: {}\nLast valid state:\n{}'.format(error_msg,res),allow_raise=True)
    return

test.describe('12 FIXED TESTS')
fixed_tests = [
    [[4,1,3],[2,8,0],[7,6,5]],
    [[8,2,1],[3,7,0],[4,6,5]],
    [[1,5,2],[7,0,8],[6,4,3]],
    [[10,3,6,4],[1,5,8,0],[2,13,7,15],[14,9,12,11]],
    [[15,1,3,4],[9,5,6,8],[13,7,14,11],[10,2,0,12]],
    [[3,9,11,7],[1,12,13,4],[8,2,14,0],[6,10,15,5]],
    [[22,1,10,9,4],[11,8,2,5,18],[16,6,12,19,14],[7,23,21,15,24],[3,13,0,17,20]],
    [[1,6,2,9,0],[23,8,3,10,18],[11,22,24,15,12],[21,14,16,4,5],[17,13,19,20,7]],
    [[2,7,10,3,9],[6,17,5,1,14],[11,12,8,24,13],[4,21,23,15,0],[22,16,19,20,18]],
    [[2,7,9,5,27,12],[25,11,15,6,18,4],[8,26,1,14,3,28],[21,20,10,30,17,29],[19,13,33,22,0,23],[32,34,31,24,16,35]],
    [[6,20,4,24,12,2],[1,7,10,5,14,16],[13,3,9,17,15,23],[19,11,27,21,34,28],[25,26,8,35,18,0],[31,32,33,30,22,29]],
    [[7,14,26,10,8,18],[9,1,2,12,6,29],[31,0,5,16,3,4],[13,21,15,24,25,35],[19,28,34,17,11,22],[32,27,20,33,30,23]]
]

for x in fixed_tests:
    vsol(x,slide_puzzle([r[:] for r in x]))

#RNG function
import random
def RN(n,q=0):
    return random.randint(0,n-1) + q

#random test generator
VN = [[-1,0],[0,1],[1,0],[0,-1]]
def puzzle_gen(n,q):
    r = [[i*n+c+1 for c in range(n)] for i in range(n)]
    r[n-1][n-1] = 0
    if q == 0:#make unsolvable puzzle
        r[n-1][n-2],r[n-1][n-3] = r[n-1][n-3],r[n-1][n-2]
    c = RN(n*3) + n**3
    x,y = n-1,n-1
    zx,zy = -1,-1
    while c > 0:
        z = list(filter(lambda f:f[0] >= 0 and f[0] < n and f[0] != zx and f[1] >= 0 and f[1] < n and f[1] != zy,[[x+xx,y+yy] for xx,yy in VN]))
        zx,zy = z[RN(len(z))]
        zx,zy,x,y = x,y,zx,zy
        r[x][y],r[zx][zy] = r[zx][zy],r[x][y]
        c -= 1
    return r

#random tests
test.describe('120 RANDOM TESTS')
def test_arr(n,q=15):
    for v in [puzzle_gen(n,RN(5)) for x in range(q)]:
        vsol(v,slide_puzzle([r[:] for r in v]))
for i in range(8):
    test.it('{0}x{0} puzzles'.format(i+3))
    test_arr(i+3)
