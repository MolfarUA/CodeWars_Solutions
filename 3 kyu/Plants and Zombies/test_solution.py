test.describe('10 FIXED TESTS')
fixed_tdset = [
    [
        [
            '2       ',
            '  S     ',
            '21  S   ',
            '13      ',
            '2 3     '],
        [[0,4,28],[1,1,6],[2,0,10],[2,4,15],[3,2,16],[3,3,13]]],
    [
        [
            '11      ',
            ' 2S     ',
            '11S     ',
            '3       ',
            '13      '],
        [[0,3,16],[2,2,15],[2,1,16],[4,4,30],[4,2,12],[5,0,14],[7,3,16],[7,0,13]]],
    [
        [
            '12        ',
            '3S        ',
            '2S        ',
            '1S        ',
            '2         ',
            '3         '],
        [[0,0,18],[2,3,12],[2,5,25],[4,2,21],[6,1,35],[6,4,9],[8,0,22],[8,1,8],[8,2,17],[10,3,18],[11,0,15],[12,4,21]]],
    [
        [
            '12      ',
            '2S      ',
            '1S      ',
            '2S      ',
            '3       '],
        [[0,0,15],[1,1,18],[2,2,14],[3,3,15],[4,4,13],[5,0,12],[6,1,19],[7,2,11],[8,3,17],[9,4,18],[10,0,15],[11,4,14]]],
    [
        [
            '1         ',
            'SS        ',
            'SSS       ',
            'SSS       ',
            'SS        ',
            '1         '],
        [[0,2,16],[1,3,19],[2,0,18],[4,2,21],[6,3,20],[7,5,17],[8,1,21],[8,2,11],[9,0,10],[11,4,23],[12,1,15],[13,3,22]]],
    [
        [
            '121         ',
            '22S         ',
            '12S         ',
            '3 S         ',
            '12S         ',
            '22          ',
            '2SS         ',
            '1S1         '],
        [[0,5,25],[2,4,26],[2,5,15],[3,0,41],[3,1,39],[5,2,27],[5,7,34],[7,0,23],[7,5,29],[8,2,25],[8,4,26],[11,5,22],[12,2,18],[12,6,20],[12,7,12],[13,3,26],[13,0,29],[16,5,14],[20,1,40],[20,2,28],[20,3,34],[21,7,16]]],
    [
        [
            '42S1            ',
            '6S              ',
            '32 S  S         ',
            '22 S S S        ',
            '6               ',
            '5 1 2           ',
            '3 2 S  6        ',
            '4 1 S           ',
            '  8   S         ',
            '8SS             '],
        [[0,8,48],[0,1,47],[0,2,55],[0,9,99],[0,6,58],[0,7,42],[0,0,92],[0,3,39],[0,5,66],[0,4,71],[2,3,36],[2,5,59],[2,8,36],[4,0,21],[4,7,21],[5,2,14],[6,1,48],[8,6,23],[11,1,41],[11,9,25],[11,3,53],[12,1,54],[12,0,75],[13,5,48],[13,9,113],[14,8,66],[15,7,82],[15,5,54],[16,0,76],[16,4,96],[16,9,42],[18,1,23],[18,8,91],[18,3,39],[19,0,16],[20,5,37]]],
    [
        [
            '2121                ',
            '6    S              ',
            '3 2  S              ',
            '22 S S              ',
            '2 1 2S              ',
            '311                 '],
        [[0,4,49],[0,0,88],[0,1,92],[0,2,75],[1,5,69],[1,3,78],[3,1,24],[4,2,18],[4,5,21],[6,0,51],[7,4,59],[7,1,29],[10,2,34],[11,5,37],[11,1,42],[13,0,44],[13,3,33],[13,2,59],[15,1,54],[16,0,24],[16,2,42],[17,5,36],[18,3,48],[18,4,39],[19,2,85]]],
    [
        [
            '6   S             ',
            ' 55               ',
            '3 S               ',
            '31S               ',
            'SSSS              ',
            '1 S2              ',
            '1 2 3             ',
            ' 4  S             '],
        [[0,0,70],[0,1,90],[0,2,40],[0,3,50],[0,4,40],[0,5,48],[0,6,50],[0,7,42],[3,0,50],[3,1,60],[3,2,42],[3,3,40],[3,4,36],[3,5,28],[3,6,50],[3,7,25],[7,0,25],[7,1,26],[7,2,35],[7,3,44],[7,4,26],[7,5,32],[7,6,42],[7,7,31],[12,0,33],[12,1,29],[12,2,34],[12,3,29],[12,4,35],[12,5,27],[12,6,22],[12,7,39]]],
    [
        [
            '2 2 3  S                ',
            ' 1 3 1                  ',
            '3 1  S                  ',
            '11  4   S               ',
            '22   S  S               ',
            '3 1 2 S                 ',
            '4    S                  ',
            '1 1 1 1                 ',
            '1 S 3                   ',
            '1 S 2                   ',
            '4      S                ',
            '2 4 2   S               ',
            '4       1               ',
            '3 1S1                   ',
            '4   S  2                ',
            '11 3 S 2                '],
        [[0,0,96],[0,3,75],[0,7,82],[0,12,98],[0,14,104],[2,5,102],[2,6,51],[2,8,56],[3,1,74],[3,2,65],[3,3,58],[3,4,85],[3,9,44],[3,10,60],[4,14,63],[4,11,91],[5,13,120],[5,15,26],[7,1,43],[7,6,38],[7,9,61],[7,12,64],[9,0,69],[9,2,37],[9,14,51],[10,3,84],[10,7,68],[10,8,82],[10,11,77],[10,15,101],[12,4,100],[13,5,70],[13,6,76],[14,7,54]]]
]
fixed_tdsols = [10,12,20,19,None,25,34,35,25,31]
for i,v in enumerate(fixed_tdset):
    test.assert_equals(plants_and_zombies(*v),fixed_tdsols[i])


#reference solution
import re
def tfunke(ar,zr):
    ARR = lambda x: [[] for v in range(x)]
    ln,rl = len(ar),len(ar[0])
    spray = []
    row_dmg = [0]*ln
    sprayp = ARR(ln)
    zrost = ARR(ln)
    guns = ARR(ln)
    moves = 0
    for i,x in enumerate(ar):
        for c,v in enumerate(x):
            if re.match(r'\w',v):
                if re.match(r'\d',v):
                    guns[i].append([int(v),c])
                    row_dmg[i] += int(v)
                else:
                    spray.append([i,c])
                    sprayp[i].append(c)
    front = [guns[i].pop() if len(guns[i]) else None for i in range(ln)]
    def forge(n):
        nonlocal zrost
        while n:
            if all([len(x) == 0 for x in zrost]): return None
            for i,x in enumerate(row_dmg):
                tr = zrost[i]
                ct = 0
                if len(tr) == 0 or not row_dmg[i]: continue
                while ct < len(tr) and x >= tr[ct][0]:
                    x -= tr[ct][0]
                    ct += 1
                if ct == len(tr):
                    zrost[i] = []
                    continue
                tr[ct][0] -= x
                if ct: zrost[i] = tr[ct:]
            for z in spray:
                for v in [0,1,-1]:
                    x = z[0] + v
                    y = z[1] + 1
                    while ln > x >= 0 and rl > y >= 0:
                        tr = -1
                        for q,k in enumerate(zrost[x]):
                            if k[1] == y:
                                tr = q
                                break
                        if tr != -1:
                            zrost[x][tr][0] -= 1
                            if zrost[x][tr][0] == 0: zrost[x].pop(tr)
                            break
                        x += v
                        y += 1
            for i in range(ln):
                if len(zrost[i]) == 0: continue
                for v in zrost[i]:
                    v[1] -= 1
                    if v[1] == -1: return moves - n + 1
                pcheck = min([z[1] for z in zrost[i]])
                spr = sprayp[i][-1] if len(sprayp[i]) else None
                if pcheck == spr or front[i] and front[i][1] == pcheck:
                    if pcheck == spr:
                        g = sprayp[i].pop()
                        for q,z in enumerate(spray):
                            if z[0] == i and z[1] == g:
                                spray.pop(q)
                                break
                    else:
                        row_dmg[i] -= front[i][0]
                        front[i] = guns[i].pop() if len(guns[i]) else 0
            n -= 1
        return None

    spray.sort(key=lambda x: (-x[1],x[0]))
    for t,row,hp in zr:
        dc,moves = t-moves,t
        mv = forge(dc)
        if mv: return mv
        zrost[row].append([hp,rl-1])
    moves += rl
    return forge(rl)

#RNG function
import random
def RN(n,q=0):
    return random.randint(0,n-1) + q

#random test generator
def test_gen(x,y,zl,qv):
    #generate lawn map
    rowdmg = []
    r = []
    for i in range(x):
        ss = RN(3) + (RN(2,1) if RN(x//5) else 0)
        ns = RN(6,2)
        mr = []
        while ss or ns:
            if len(mr) == y//2 - 1:
                mr.append(ns) if ns else mr.append(ss)
                break
            if RN(4) and ns:
                vz = min(8,RN(ns,1))
                ns -= vz
                mr.append(vz)
            else:
                if RN(3) and ss:
                    mr.append('S')
                    ss -= 1
                else: mr.append(' ')
        nxv = 0
        for v in mr:
            if type(v) == int or re.match(r'\w',v):
                if v == 'S': nxv += 1
                else: nxv += int(v)
        rowdmg.append(nxv)
        r.append('{:<{}}'.format(''.join([str(x) for x in mr]),y))
    #generate zombie list
    zlist = []
    rows = [0]*x
    ln = RN(*zl)
    q = 0
    while (q < ln):
        if RN(4):
            for i,v in enumerate(rows):
                if v < rowdmg[i] * y/2 and RN(3):
                    zv = int((y * rowdmg[i] - v) * qv)
                    rows[i] += zv
                    zlist.append([q,i,zv])
            for i in range(x):
                rows[i] -= rowdmg[i]
        q += 1
    return [r,zlist]

#random tests
test.describe('100 RANDOM TESTS')
def test_set(x,y,zl,q,qv):
    for i in range(q):
        map,zset = test_gen(RN(*x),RN(*y),zl,qv)
        test.assert_equals(plants_and_zombies(map[:],[v[:] for v in zset]),tfunke(map,zset))

test.it('Smaller lawns')
test_set([4,5],[5,8],[9,12],30,0.45)
test.it('Mediujm lawns')
test_set([9,8],[5,12],[11,30],30,0.62)
test.it('Large lawns')
test_set([10,16],[10,16],[16,45],40,0.74)
