test.describe('Full Test Suite')
def run_full_test():
    '''10 FIXED TESTS, 110 RANDOM TESTS'''
    
    # INITIAL TEST SETUP
    success = fails = 0
    
    # cell state at next interval
    def celrot(n):
        return sum(divmod(n<<1,16))
        
    # binary as tuple
    def cel_layout(n):
        return tuple(n%(x<<1)//x for x in (8,4,2,1))
    
    walls_list = tuple(cel_layout(n) for n in range(16))
    dn = ((-1,0),(0,-1),(1,0),(0,1))
    
    # reference solution
    def ref_fn(ar):
        def forge(r):
            xr = []
            zr = tuple([0]*yl for row in r)
            for i,row in enumerate(r):
                for j,cel in enumerate(row):
                    if cel == 15: zr[i][j] = 1
                    if zr[i][j]: continue
                    zst = set()
                    grp = ((i,j),)
                    while grp:
                        grp2 = set()
                        for x,y in grp:
                            zst.add((x,y))
                            zr[x][y] = 1
                            cn = walls_list[r[x][y]]
                            for q,w in enumerate(cn):
                                if w: continue
                                cx,cy = dn[q]
                                nx,ny = x+cx,y+cy
                                if (nx,ny) in zst or nx < 0 or ny < 0 or nx >= xl or ny >= yl or zr[nx][ny]: continue
                                cel2 = walls_list[r[nx][ny]]
                                if cel2[(q+2)%4]: continue
                                grp2.add((nx,ny))
                        grp = tuple(grp2)
                    xr.append(zst)
            return xr
        
        xl,yl = len(ar),len(ar[0])
        pos = exz = ()
        
        for i,row in enumerate(ar):
            for j,cel in enumerate(row):
                if type(cel) == str:
                    if cel == 'B': pos = (i,j)
                    else: exz = (i,j)
            if pos and exz: break
        
        phases = [tuple(tuple(cel if type(cel) == int else 0 for cel in row) for row in ar)]
        for _ in range(3):
            phases.append(tuple(tuple(celrot(cel) for cel in row) for row in phases[-1]))
        codex = [forge(r) for r in phases]
        tome = []

        for i,v in enumerate(codex):
            tome_v = []
            nxt = codex[(i+1)%4]
            for v1 in v:
                vx = {}
                for jj,v2 in enumerate(nxt):
                    v3 = v1 & v2
                    if v3: vx[jj] = v3
                tome_v.append(vx)
            tome.append(tome_v)
        
        for i,v in enumerate(codex[0]):
            if pos in v:
                loc = i
                break
        
        ct = 0
        checkpt = ()
        walked = {n:set() for n in range(4)}
        path_track = [{loc}]
        
        while not checkpt:
            forks = set()
            cmod = ct%4
            tc = tome[cmod]
            cc = codex[cmod]
            wlen = len(walked[cmod])
            for p in path_track[ct]:
                if exz in cc[p]:
                    checkpt = (p,ct)
                    path_track[ct] = {p}
                    break
                for k,v in tc[p].items():
                    forks.add(k)
                walked[cmod].add(p)
            else:
                if len(walked[cmod]) == wlen:
                    # no solution
                    return None
                ct += 1
                path_track.append(forks ^ walked[ct%4] & forks)
        
        li = checkpt[1]
        while li:
            if len(path_track[li-1]) > 1:
                modc = (li-1)%4
                filt = set(n for n,v in enumerate(tome[modc]) if any(w in v for w in path_track[li]))
                path_track[li-1] &= filt
            li -= 1
        
        def pass_thru(r,p1,p2):
            n1,n2 = (r[x][y] for x,y in (p1,p2))
            d = dn.index((p2[0]-p1[0],p2[1]-p1[1]))
            return not cel_layout(n1)[d] and not cel_layout(n2)[(d+2)%4]
        
        cgroup = loc
        ccel = pos
        path_seq = []
        plen = len(path_track)
        for i in range(plen):
            vpoints = {p:n for n,v in tome[i%4][cgroup].items() for p in v if n in path_track[i+1]} if i < plen - 1 else {exz:cgroup}
            traversable = {v:-1 for v in codex[i%4][cgroup] if v != ccel}
            cphase = phases[i%4]
            dstr = ''
            if ccel in vpoints:
                cgroup = vpoints[ccel]
                path_seq.append(dstr)
                continue
            else:
                zr = set(filter(lambda v: v[1] in traversable and pass_thru(cphase,ccel,v[1]),((q,(x+ccel[0],y+ccel[1])) for q,(x,y) in enumerate(dn))))
                while zr:
                    nr = set()
                    for q,pt in zr:
                        if pt in vpoints:
                            traversable[pt] = q
                            break
                        nr |= set(filter(lambda v: traversable.get(v[1]) == -1 and pass_thru(cphase,pt,v[1]),((w,(x+pt[0],y+pt[1])) for w,(x,y) in enumerate(dn))))
                        traversable[pt] = q
                    else:
                        zr = nr
                        continue
                    break
                ccel = pt
                cgroup = vpoints[ccel]
                while pt in traversable:
                    q = traversable[pt]
                    dstr += 'NWSE'[q]
                    qinv = dn[(q+2)%4]
                    pt = (pt[0]+qinv[0],pt[1]+qinv[1])
                path_seq.append(dstr[::-1])
        
        return path_seq
    
    # verify user solution
    from re import fullmatch as fm
    
    dnum = {'N':0, 'W':1, 'S':2, 'E':3}
    dirs = {'N':(-1,0), 'W':(0,-1), 'S':(1,0), 'E':(0,1)}
    dwrd = ['north','west','south','east']
    
    # solution verification function
    def verify_solution(r,sol,ref):
        if sol == None:
            if ref == False: ref = ref_fn(r)
            if ref == None: return (True,)
        if type(sol) != list:
            return (False,'Data type must be a list')
        if not all(type(s) == str and fm(r'[NWSE]*',s) for s in sol):
            return (False,'All list elements must be a string and may only contain the following characters: "NWSE"')
        
        if ref == False: ref = ref_fn(r)
        if ref == None:
            return (False,'This puzzle has no solution')
        ref_str = 'Here is a valid solution:\n[{}]'.format(', '.join(f"'{s}'" for s in ref))
        user_str = 'Here is your solution:\n[{}]'.format(', '.join(f"'{s}'" for s in sol))
        
        if len(sol) > len(ref):
            return (False,f'Your solution completes the task in {len(sol)} iterations.\nThis test can be completed in {len(ref)} iterations.\n' + ref_str + '\n' + user_str)
        
        phases = [tuple(tuple(cel if type(cel) == int else 0 for cel in row) for row in r)]
        for _ in range(3):
            phases.append(tuple(tuple(celrot(cel) for cel in row) for row in phases[-1]))
        
        xl,yl = len(r),len(r[0])
        for i,row in enumerate(r):
            for j,cel in enumerate(row):
                if type(cel) == str:
                    if cel == 'B': pos = (i,j)
                    else: dst = (i,j)
        
        px,py = pos
        bad_move = lambda s: (False,f'Invalid move: {s}\n{user_str}')
        for i,s in enumerate(sol):
            cr = phases[i%4]
            visited = set()
            for j,ss in enumerate(s):
                nx,ny = dirs[ss]
                px,py = (pos[0]+nx,pos[1]+ny)
                pos_str = 'during move {} at iteration {}.\nLast valid position was [{}, {}].'.format(j,i,*pos)
                if px < 0 or px >= xl or py < 0 or py >= yl:
                    return bad_move(f'Out of bounds {pos_str}')
                
                # check for walls obstructing path
                wall0 = walls_list[cr[pos[0]][pos[1]]][dnum[ss]]
                wall1 = walls_list[cr[px][py]][(dnum[ss]+2)%4]
                obstruct = 1 if wall0 else 2 if wall1 else 0
                if obstruct:
                    return bad_move(f'Path obstructed by a wall on the {dwrd[[dnum[ss],(dnum[ss]+2)%4][obstruct-1]]} side of {[f"[{pos[0]}, {pos[1]}]",f"[{px}, {py}]"][obstruct-1]} {pos_str}')
                if (px,py) in visited:
                    return bad_move(f'Entered cell [{px},{py}] a second time {pos_str}')
                pos = (px,py)
                visited.add(pos)
        
        if pos != dst:
            last_pos = f' Its last position was [{px},{py}]' if px != None and py != None else ''
            return (False,f'The ball did not reach the destination.{last_pos}\n{user_str}')
        
        # in case reference solution is incorrect
        if len(sol) < len(ref):
            maze_print = '\n'.join(f'({", ".join(str(v) for v in row)})' for row in r)
            print(f'You have found an error with this kata. Please provide the following details in a comment in the Discourse section:\n{maze_print}\nSolution: {sol}')
        
        return (True,'')
    
    # process each test case
    def proc_test(r,ref=False):
        nonlocal success,fails
        user = maze_solver(r)
        res = verify_solution(r,user,ref)
        test.expect(*res)
        if res[0]: success += 1
        else: fails += 1
    
    # FIXED TESTS (10)
    test.it('FIXED TESTS (10)')
    fixed_tests = (
        (
            (4,2,5,4),
            (4,15,11,1),
            ('B',9,6,8),
            (12,7,7,'X')
        ),
        (
            (6,3,10,4,11),
            (8,10,4,8,5),
            ('B',14,11,3,'X'),
            (15,3,4,14,15),
            (14,7,15,5,5)
        ),
        (
            (9,1,9,0,13,0),
            (14,1,11,2,11,4),
            ('B',2,11,0,0,15),
            (4,3,9,6,3,'X')
        ),
        (
            ('B',6,12,15,11),
            (8,7,15,7,10),
            (13,7,13,15,'X'),
            (11,10,8,1,3),
            (12,6,9,14,7)
        ),
        (
            (6,3,0,9,14,13,14),
            ('B',14,9,11,15,14,15),
            (2,15,0,12,6,15,'X'),
            (4,10,7,6,15,5,3),
            (7,3,13,13,14,7,0)
        ),
        (
            (0,13,13,12,9,9),
            (4,2,9,11,3,'X'),
            (0,0,4,12,10,6),
            (15,8,3,14,0,7),
            (9,1,15,2,10,11),
            ('B',10,7,2,6,13)
        ),
        (
            (3,7,12,6,11,9),
            ('B',14,4,6,6,10),
            (9,15,14,1,14,5),
            (0,4,15,8,4,'X'),
            (10,5,3,7,3,1),
            (14,11,10,11,15,13)
        ),
        (
            ('B',13,1,12,5,2,12,9),
            (7,14,7,7,10,8,9,13),
            (12,12,12,8,1,3,9,2),
            (1,0,8,7,9,13,15,4),
            (15,10,5,11,7,15,12,4),
            (6,12,4,3,2,1,14,8),
            (15,0,6,6,8,9,11,'X'),
            (0,13,7,4,3,8,11,6)
        ),
        (
            (9,12,7,6,9,1,1,15,5,1),
            (13,5,4,9,11,13,2,11,4,13),
            (14,7,5,10,15,8,5,9,7,6),
            (5,6,5,1,13,10,9,10,7,10),
            (10,4,1,9,13,15,0,4,11,15),
            ('B',5,11,5,14,7,13,8,9,12),
            (9,10,0,13,5,3,6,9,2,3),
            (14,4,4,2,15,9,2,11,2,'X')
        ),
        (
            (2,3,10,1,13,7,15,0,1,9,8,9),
            (10,15,3,9,3,10,8,1,9,5,9,4),
            (2,12,5,3,13,15,7,4,1,14,7,1),
            (13,4,5,11,4,6,12,13,3,14,2,11),
            (12,3,2,15,0,5,11,5,15,6,8,2),
            ('B',8,11,13,11,6,8,2,14,13,1,9),
            (12,0,2,11,5,5,6,10,9,6,0,10),
            (3,0,1,11,0,5,14,9,4,5,13,7),
            (11,4,15,8,15,8,3,12,1,4,9,'X'),
            (9,14,4,8,8,3,4,10,10,6,3,13),
            (15,9,14,12,10,14,8,12,11,0,4,11),
            (12,3,13,11,8,15,6,3,2,1,8,0)
        )
    )
    fixed_sols = (
        ['NNE', 'EE', 'S', 'SS'],
        ['', '', 'E', '', 'E', 'NESE'],
        ['E', 'SE', '', 'E', 'E', 'E'],
        None,
        None,
        ['', '', '', 'NE', '', 'NNEE', '', '', 'E', '', 'E', 'N'],
        None,
        ['', 'E', '', 'E', '', '', 'E', 'EE', '', 'SSE', 'ESSS', 'S'],
        ['', '', 'SE', '', 'E', 'E', '', 'EE', '', '', 'S', 'E', 'E', '', 'EE'],
        ['NE', 'NE', 'N', 'E', '', 'E', '', '', 'S', '', 'S', 'E', 'SESEES', 'SEE', 'E']
    )
    
    for i,v in enumerate(fixed_tests): proc_test(v,fixed_sols[i])
    print('<COMPLETEDIN::>')
    # END FIXED TESTS
    
    # RANDOM TESTS (110)
    test.it('RANDOM TESTS (110)')
    from random import randrange as RR
    
    # random test generator
    def gen_test(n,m):
        B,X = ((RR(n),c) for c in (0,m-1))
        return tuple(tuple(RR(16) if all((x,y) != v for v in (B,X)) else 'B' if (x,y) == B else 'X' for y in range(m)) for x in range(n))
    
    for i in range(110):
        q = 8 + i//5
        xl,yl = (min(RR(4,q),25) for _ in range(2)) if i < 100 else (25,25)
        tc = gen_test(xl,yl)
        proc_test(tc)
        
        if fails > 10:
            print('Early termination -- maximum failure threshold reached.')
            break
    
    print('<COMPLETEDIN::>')
    # END RANDOM TESTS
    
    return not fails and success == 120

run_full_test() or test.fail('Please revise your code and try again.')
print('<COMPLETEDIN::>')
# END FULL TEST SUITE
