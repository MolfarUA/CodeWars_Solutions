def moves(p):
    if p < 25 and p % 5 != 4: yield p + 1
    if p >= 5: yield p - 5
    if p >= 0 and p % 5 != 0: yield p - 1
    if p < 20: yield p + 5

def gerrymander(s):
    so = [1 if c == 'O' else 0 for c in s if c != '\n']
    mp = [0] * 25
    def dfs(pp, p0, k, ko, n, no):
        if k == 5:
            n += 1
            if ko >= 3: no += 1
            if n == 6: return no >= 3
            elif (n != 4 or no > 0) and (n != 5 or no > 1):
                p = mp.index(0)
                mp[p] = n
                if dfs(None, p, 1, so[p], n, no): return True
                mp[p] = 0
            return False
        for p in moves(p0):
            if mp[p] == 0:
                mp[p] = n
                if dfs(p0, p, k + 1, ko + so[p], n, no): return True
                mp[p] = 0
        return pp is not None and dfs(None, pp, k, ko, n, no)
    mp[0] = 1
    return '\n'.join(''.join(map(str, mp[i: i + 5])) for i in range(0, 25, 5)) \
            if dfs(None, 0, 1, so[0], 1, 0) else None
###############
from itertools import combinations

def gerrymander(s):
    tr={'O':1,'X':0}
    sn=[[tr[p] for p in row] for row in  s.splitlines()]
    u=[(y,x) for y in range(5) for x in range(5)]
    u1=[(y,x) for y in range(5) for x in range(5-y)]
    u1.remove((0,0))
    
    for g1 in combinations(u1,4):
        psums=[0,1,3,3,3]
        g1x=list(g1)+[(0,0)]
        if  check_group(g1x): 
            s1=sum_group(g1x,sn)
            if s1  in psums:
                psums2=psums[:]
                psums2.remove(s1)
                u2=[(y,x) for y in range(5) for x in range(4-y,5) if (y,x) not in g1x and (y,x)!=(4,4)]
                
                for g2 in combinations(u2,4):
                    g2x=list(g2)+[(4,4)]
                    if check_group(g2x):
                        s2=sum_group(g2x,sn)
                        if s2  in psums2:
                            psums3=psums2[:]
                            psums3.remove(s2)
                            u3=[p for p in u if p not in g1x+g2x]
                            if check_u(u3):
                                
                                for g3 in combinations(u3,5):
                                    if check_group(g3):
                                        s3=sum_group(g3,sn)
                                        if s3  in psums3: 
                                            psums4=psums3[:]
                                            psums4.remove(s3)
                                            u4=[p for p in u3 if p not in g3]
                                            if check_u(u4): 
                                                for g4 in combinations(u4,5):
                                                    if check_group(g4):
                                                        s4=sum_group(g4,sn)
                                                        if s4 in psums4: 
                                                            g5=[p for p in u4 if p not in g4]
                                                            if check_group(g5): 
                                                                gr=[g1x,g2x,g3,g4,g5]
                                                                resg=[['']*5 for i in range(5)]
                                                                for i in range(5):
                                                                    for y,x in gr[i]:
                                                                        resg[y][x]=str(i+1)
                                                                return "\n".join( [line for line in ["".join(l) for l in resg]]  )
                                                            else:
                                                                continue
                            
    return None

def check_group(g):
    vis=set()
    tovis=[g[0]]
    while len(tovis)>0:
        y,x=tovis.pop()
        vis.add((y,x))
        for y1,x1 in [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]:
            if ((y1,x1) not in g) or ((y1,x1) in vis): continue
            tovis.append((y1,x1))
    if len((vis))==5:
        return True
    return False

def sum_group(g,m):
    s=0
    for y,x in g:
        s+=m[y][x]
    return s

def check_u(u):
    uleft=u[:]
    while len(uleft)>0:
        tovis=[uleft[0]]
        chunk=set()
        while len(tovis)>0:
            y,x=tovis.pop()
            chunk.add((y,x))
            for y1,x1 in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
                if (y1,x1) in uleft :
                    tovis.append((y1,x1))
                    uleft.remove((y1,x1))
        if len(chunk)%5!=0:return False    
    return True
########################
from functools import lru_cache as cache

def adj(citizen):
    i,j = citizen//10, citizen%10
    return [*[(i-1)*10+j,10*i+j-1][i==0:2-(j==0)],*[10*(i+1)+j,10*i+j+1][i==4:2-(j==4)]]

@cache(maxsize=50000)
def district(start,rest):
    global connections
    s = [{start,}]
    rest = set(rest)
    for _ in range(4):
        ts = []
        for f in s:
            adjs = {c2 for c1 in f for c2 in connections[c1]}
            for n in adjs&rest-set(f):
                fn = f|{n}
                if fn in ts: continue
                ts += [fn]
        s = ts
    return s

def maps():
    combs = [()]
    for _ in range(5):
        temp = []
        for comb in combs:
            rest = set(citizens)
            for c in comb: rest-=c
            for f in district(rest.pop(),tuple(rest)):
                temp += [comb+(f,)]
        combs = temp
    return combs

def gerrymander(region):
    M = maps()
    region = [[[0,1][r=='O'] for r in row]for row in region.split('\n')]
    for m in M:
        score = sum([sum([region[d//10][d%10] for d in district])>2 for district in m])
        if score>2:
            res = [[' ']*5 for _ in range(5)]
            for r,row in enumerate(m):
                for d in row:
                    res[d//10][d%10] = str(r+1)
            return '\n'.join([''.join(row) for row in res])
    else:
        return None
        
citizens = set(int(str(i)+str(j))for i in range(5) for j in range(5))
connections = {c:adj(c) for c in citizens}
####################################################
import itertools as it

def isContinous(cluster):
    cels2D = [(int(i/5),i%5) for i in cluster]
    nbs = [len([nb for nb in [(y+1,x),(y-1,x), (y,x+1), (y,x-1)] if nb in cels2D]) for y, x in cels2D]
    if nbs.count(4)==1: return True
    if nbs.count(1)==4: return False
    if nbs.count(0):    return False
    return True

#Continous Clusters
CCS = [c for c in it.combinations(list(range(25)), 5) if isContinous(c)] 

def gerrymander(s):
    s = s.replace('\n', '')    
    ccVotes = [ [] for _ in range(6)] 
    for cc in CCS:              
        ccVotes[len([cell for cell in cc if s[cell]=='O'])].append(cc)        
    return toOutput(getCluster(ccVotes, [1,0,3,3,3], tuple()))

def getCluster(votes, order, occupied):
    voteId = order[0]
    votes = votes[:]
    votes[voteId] = clearOverlaps(occupied, votes[voteId]) if any(occupied) else votes[voteId]
    for c in votes[voteId]:
        if len(order) > 1:
            newCluster = getCluster(votes, order[1:], occupied + c)
            if newCluster == None: continue
            return newCluster
        else: 
            return occupied + c    
    return None

def toOutput(cluster):
    if not cluster: return None
    out = ''.join([str(int(cluster.index(id)/5)+1) for id in range(25)])
    return '\n'.join([out[x:x+5] for x in range(0, 25, 5)])
    
def clearOverlaps(occupied, districts):
    return list(filter(lambda d: len([e for e in d if e in occupied])==0, districts))
#############################################
import itertools as it

def isContinous(cluster):
    # transform position from 1D to 2D
    cels2D = [(int(i/5),i%5) for i in cluster]
    
    # count number of direct ortogonal neighbours for each cluster cell
    nbs = []
    for c in cels2D:
        nbId = [(c[0]+1,c[1]),(c[0]-1,c[1]), (c[0],c[1]+1), (c[0],c[1]-1)]
        nbs.append(len([nb for nb in nbId if nb in cels2D]))
    if nbs.count(0):    return False
    if nbs.count(4)==1: return True
    if nbs.count(1)==4: return False
    return True

#Continous Clusters
CCS = [c for c in it.combinations(list(range(25)), 5) if isContinous(c)] 

def gerrymander(s):

    s = s.replace('\n', '')
    
    # ccVotes - clusters grouped by number of votes e.g ccVotes[0] - clusters w/o votes
    ccVotes = [ [] for _ in range(6)] 
    for cc in CCS:              
        ccVotes[len([cell for cell in cc if s[cell]=='O'])].append(cc)
        
    return toOutput(getCluster(ccVotes, [1,0,3,3,3], tuple()))

def getCluster(votes, order, occupied):
    voteId = order[0]
    votes = votes[:]
    votes[voteId] = clearOverlaps(occupied, votes[voteId]) if any(occupied) else votes[voteId]
    for c in votes[voteId]:
        if len(order) > 1:
            newCluster = getCluster(votes, order[1:], occupied + c)
            if newCluster == None: continue
            return newCluster
        else: 
            return occupied + c    
    return None

def toOutput(record):
    if not record: return None
    out = ''.join([str(int(record.index(id)/5)+1) for id in range(25)])
    return '\n'.join([out[x*5:x*5+5] for x in range(5)])
    
def clearOverlaps(occupied, districts):
    return list(filter(lambda d: len([e for e in d if e in occupied])==0, districts))
#################################
import numpy as np
from scipy import ndimage

base_pentominoes = [
    # indices, bounds, rotations, flips
    (((0, 1), (0, 2), (1, 0), (1, 1), (2, 1)), (2, 2), 4, 2), # F
    (((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)), (4, 0), 2, 1), # I
    (((0, 0), (1, 0), (2, 0), (3, 0), (3, 1)), (3, 1), 4, 2), # L
    (((0, 1), (1, 1), (2, 0), (2, 1), (3, 0)), (3, 1), 4, 2), # N
    (((0, 0), (0, 1), (1, 0), (1, 1), (2, 0)), (2, 1), 4, 2), # P
    (((0, 0), (0, 1), (0, 2), (1, 1), (2, 1)), (2, 2), 4, 1), # T
    (((0, 0), (0, 2), (1, 0), (1, 1), (1, 2)), (1, 2), 4, 1), # U
    (((0, 2), (1, 2), (2, 0), (2, 1), (2, 2)), (2, 2), 4, 1), # V
    (((0, 2), (1, 1), (1, 2), (2, 0), (2, 1)), (2, 2), 4, 1), # W
    (((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)), (2, 2), 1, 1), # X
    (((0, 1), (1, 0), (1, 1), (2, 1), (3, 1)), (3, 1), 4, 2), # Y
    (((0, 0), (0, 1), (1, 1), (2, 1), (2, 2)), (2, 2), 2, 2), # Z
]

def rot(p, s, i, f):
    if f: p = (s[0] - p[0], p[1])
    if i == 0: return p, s
    if i == 1: return (p[1], s[0]-p[0]), (s[1], s[0])
    if i == 2: return (s[0]-p[0], s[1]-p[1]), s
    if i == 3: return (s[1]-p[1], p[0]), (s[1], s[0])

pentominoes = [
    rot(tuple(np.column_stack(p)), s, i, j)
    for p, s, r, f in base_pentominoes
    for i in range(r)
    for j in range(f)
]

def gerrymander(s):
    a = np.array([list(r) for r in s.split('\n')])
    o = np.zeros((5, 5), int)

    def gen(nx):
        for p, s in pentominoes:
            for i in range(5 - s[0]):
                for j in range(5 - s[1]):
                    pij = (p[0] + i, p[1] + j)
                    if not np.any(o[pij]) and np.sum(a[pij] == 'X') == nx:
                        yield pij

    def validate():
        labels = ndimage.measurements.label(o == 0)[0]
        return not np.any(np.unique(labels, return_counts=True)[1] % 5)

    def it(nx, i):
        for p in gen(nx):
            o[p] = i
            if validate():
                yield
            o[p] = 0

    for _ in it(5, 1):
        for _ in it(4, 2):
            for _ in it(2, 3):
                for _ in it(2, 4):
                    o[o == 0] = 5
                    return '\n'.join(''.join(str(i) for i in r) for r in o)

    return None
###################################
#!/usr/bin/env python3

from random import choice, sample

def gerrymander(votes):
    """
    >>> s = ['XXXXX',
    ...     'OOOXO',
    ...     'XXXOX',
    ...     'OOOOO',
    ...     'XXXXX']        
    >>> gerrymander(s)
    True
    """
    #preprocess
    votes = ''.join(votes)
    votes = votes.replace('\n', '')
    
    def is_five_connected(districts:str):
        """checks if there are five adjacently connected districts in the string, return true if so, false otherwise """
        
        for num in range(1,6):
            pos = districts.find(str(num))
            if pos <0:
                return False
            
            # expand districts starting from first found occurence
            to_expand = [pos]
            expanded = set()
            while to_expand:
                i = to_expand.pop()
                expanded.add(i)
                if i%5 and districts[i-1]==districts[i] and i-1 not in expanded: #left
                    to_expand.append(i-1)
                if (i+1)%5 and districts[i+1]==districts[i] and i+1 not in expanded: #right 
                    to_expand.append(i+1)  
                if i-5 >= 0 and districts[i-5]==districts[i] and i-5 not in expanded: #top 
                    to_expand.append(i-5)   
                if i+5 < 25 and districts[i+5]==districts[i] and i+5 not in expanded: #bottom
                    to_expand.append(i+5)

            if len(expanded) != 5:
                return False

        return True

    def get_neighbors(districts, pos):
        return [districts[pos-1] if pos%5 else None, #left
                districts[pos-5] if pos-5 >= 0 else None, #top
                districts[pos+1] if (pos+1)%5 else None, #right
                districts[pos+5] if pos+5 < 25 else None #bottom
                ]

    def generate_random_assignments():
        """ starting with the initial string find legal random new district assignments 
        by swaping two positions by chance. add a new found assignment to the list of
        found ones and choose a random one from this list for the next permutation. """

        found = [''.join([i*5 for i in '12345'])]
        while len(found)<800: #little bit of cheating here
            a,b = sample(range(1,24),2)
            a,b = (a,b) if a<b else (b,a)
            x = choice(found)
            y = x[:a] + x[b] + x[a+1:b] + x[a] + x[b+1:]
            if y[a] != y[b] and \
                y[a] in get_neighbors(y,a) and \
                y[b] in get_neighbors(y,b) and \
                is_five_connected(y) and \
                y not in found:
                found.append(y)
                yield y

    def score(districts, votes):
        """ returns the percentage of won districts. """
        res = 0
        for d in set(districts):
            result = [votes[i] for i in range(len(votes)) if districts[i]==d]
            if result.count('O') > 2:
                res += 0.2
        return res
    
    for g in generate_random_assignments():
        if score(g, votes) > 0.5:
            return '\n'.join([g[i:i+5] for i in range(0, len(g), 5)])

    return None


if __name__ == "__main__":

    import doctest
    doctest.testmod()
#########################################
def gerrymander(lst):
    
    vals = []
    for s in lst:
        for z in list(s):
            if z == "X" :
                vals.append(0)
            elif z == "O":
                vals.append(1) 
    print(vals)
    def neigh(li):
        n =0
        for i in range(5):
            m =0 
            for j in range(5):
                if (abs(li[j]-li[i]) == 1 and min(li[i]+1,li[j]+1)%5 != 0) or abs(li[j]-li[i]) == 5:
                    n=n+1
                    m=m+1
            if m ==0: return False
        if n > 7: 
            return True
        else:
            return False
        
    def votes(lst, val):
         tot = []
         for m in range(5):
             tot.append(val[lst[m]])
         return sum(tot) 
    
    import itertools as its
    
    possible_areas = set(filter(lambda x : neigh(x), its.combinations(range(25),5)))
    
    areas = {l: set() for l in range(6)}
   
    for area in possible_areas:
        areas[votes(area, vals)].add(area)
    
    lost_0 = set(filter(lambda x: set(x[0]) & set(x[1]) == set(), its.combinations(areas[0],2)))
    
    lost_1 = set()
    for o in areas[0]:
        for p in areas[1]:
            if set(o) & set(p) == set():
                lost_1.add((o,p))
    
    roz = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
    
    for y in lost_0:
        for z in areas[4]:
            if set(z) & set(y[0]) ==set() and set(z) & set(y[1]) ==set(): 
                for xx in areas[3]:
                    if set(xx) & set(y[0]) ==set() and set(xx) & set(y[1]) ==set() and set(xx) & set(z) == set():   
                        yy = list(set(range(25)) - set(xx) - set(z)- set(y[0])-set(y[1]))
                        if neigh(yy):
                            for c in range(5):
                                roz[y[0][c]] = 1
                                roz[y[1][c]] = 2
                                roz[z[c]] = 3
                                roz[xx[c]] =  4
                                roz[yy[c]] = 5
                            roz.insert(5, "\n")
                            roz.insert(11, "\n")
                            roz.insert(17, "\n")
                            roz.insert(23, "\n")
                            rozw = ''.join([str(elem) for elem in roz])
                            return rozw
    for aa in lost_1:
        for bb in areas[3]:
            if set(bb) & set(aa[0]) ==set() and set(bb) & set(aa[1]) ==set():
                 for cc in areas[3]:       
                      if set(cc) & set(aa[0]) ==set() and set(cc) & set(aa[1]) ==set() and set(cc) & set(bb) == set():   
                        dd = list(set(range(25)) - set(cc) - set(bb)- set(aa[0])-set(aa[1]))  
                        if neigh(dd):
                            for c in range(5):
                                roz[aa[0][c]] = 1
                                roz[aa[1][c]] = 2
                                roz[bb[c]] = 3
                                roz[cc[c]] =  4
                                roz[dd[c]] = 5
                            roz.insert(5, "\n")
                            roz.insert(11, "\n")
                            roz.insert(17, "\n")
                            roz.insert(23, "\n")
                            
                            rozw = ''.join([str(elem) for elem in roz])
                            return rozw                  
    return None         
    
##########################################
import numpy as np


def gerrymander(s):
    board = np.array(list(''.join(s.split('\n'))))
    
    all_arr = [[0, 1, 6, 7, 12], [1, 2, 7, 8, 13], [2, 3, 8, 9, 14], [5, 6, 11, 12, 17], [6, 7, 12, 13, 18], [7, 8, 13, 14, 19], [10, 11, 16, 17, 22], [11, 12, 17, 18, 23], [12, 13, 18, 19, 24], [0, 5, 6, 11, 12], [1, 6, 7, 12, 13], [2, 7, 8, 13, 14], [5, 10, 11, 16, 17], [6, 11, 12, 17, 18], [7, 12, 13, 18, 19], [10, 15, 16, 21, 22], [11, 16, 17, 22, 23], [12, 17, 18, 23, 24], [1, 2, 5, 6, 10], [2, 3, 6, 7, 11], [3, 4, 7, 8, 12], [6, 7, 10, 11, 15], [7, 8, 11, 12, 16], [8, 9, 12, 13, 17], [11, 12, 15, 16, 20], [12, 13, 16, 17, 21], [13, 14, 17, 18, 22], [2, 6, 7, 10, 11], [3, 7, 8, 11, 12], [4, 8, 9, 12, 13], [7, 11, 12, 15, 16], [8, 12, 13, 16, 17], [9, 13, 14, 17, 18], [12, 16, 17, 20, 21], [13, 17, 18, 21, 22], [14, 18, 19, 22, 23], [1, 5, 6, 10, 15], [2, 6, 7, 11, 16], [3, 7, 8, 12, 17], [4, 8, 9, 13, 18], [6, 10, 11, 15, 20], [7, 11, 12, 16, 21], [8, 12, 13, 17, 22], [9, 13, 14, 18, 23], [1, 6, 10, 11, 15], [2, 7, 11, 12, 16], [3, 8, 12, 13, 17], [4, 9, 13, 14, 18], [6, 11, 15, 16, 20], [7, 12, 16, 17, 21], [8, 13, 17, 18, 22], [9, 14, 18, 19, 23], [0, 1, 2, 7, 8], [1, 2, 3, 8, 9], [5, 6, 7, 12, 13], [6, 7, 8, 13, 14], [10, 11, 12, 17, 18], [11, 12, 13, 18, 19], [15, 16, 17, 22, 23], [16, 17, 18, 23, 24], [0, 1, 6, 7, 8], [1, 2, 7, 8, 9], [5, 6, 11, 12, 13], [6, 7, 12, 13, 14], [10, 11, 16, 17, 18], [11, 12, 17, 18, 19], [15, 16, 21, 22, 23], [16, 17, 22, 23, 24], [0, 1, 6, 10, 11], [1, 2, 7, 11, 12], [2, 3, 8, 12, 13], [3, 4, 9, 13, 14], [5, 6, 11, 15, 16], [6, 7, 12, 16, 17], [7, 8, 13, 17, 18], [8, 9, 14, 18, 19], [10, 11, 16, 20, 21], [11, 12, 17, 21, 22], [12, 13, 18, 22, 23], [13, 14, 19, 23, 24], [0, 1, 5, 10, 11], [1, 2, 6, 11, 12], [2, 3, 7, 12, 13], [3, 4, 8, 13, 14], [5, 6, 10, 15, 16], [6, 7, 11, 16, 17], [7, 8, 12, 17, 18], [8, 9, 13, 18, 19], [10, 11, 15, 20, 21], [11, 12, 16, 21, 22], [12, 13, 17, 22, 23], [13, 14, 18, 23, 24], [0, 2, 5, 6, 7], [1, 3, 6, 7, 8], [2, 4, 7, 8, 9], [5, 7, 10, 11, 12], [6, 8, 11, 12, 13], [7, 9, 12, 13, 14], [10, 12, 15, 16, 17], [11, 13, 16, 17, 18], [12, 14, 17, 18, 19], [15, 17, 20, 21, 22], [16, 18, 21, 22, 23], [17, 19, 22, 23, 24], [0, 1, 2, 5, 7], [1, 2, 3, 6, 8], [2, 3, 4, 7, 9], [5, 6, 7, 10, 12], [6, 7, 8, 11, 13], [7, 8, 9, 12, 14], [10, 11, 12, 15, 17], [11, 12, 13, 16, 18], [12, 13, 14, 17, 19], [15, 16, 17, 20, 22], [16, 17, 18, 21, 23], [17, 18, 19, 22, 24], [1, 5, 6, 10, 15], [2, 6, 7, 11, 16], [3, 7, 8, 12, 17], [4, 8, 9, 13, 18], [6, 10, 11, 15, 20], [7, 11, 12, 16, 21], [8, 12, 13, 17, 22], [9, 13, 14, 18, 23], [1, 6, 10, 11, 15], [2, 7, 11, 12, 16], [3, 8, 12, 13, 17], [4, 9, 13, 14, 18], [6, 11, 15, 16, 20], [7, 12, 16, 17, 21], [8, 13, 17, 18, 22], [9, 14, 18, 19, 23], [0, 1, 2, 7, 8], [1, 2, 3, 8, 9], [5, 6, 7, 12, 13], [6, 7, 8, 13, 14], [10, 11, 12, 17, 18], [11, 12, 13, 18, 19], [15, 16, 17, 22, 23], [16, 17, 18, 23, 24], [0, 1, 6, 7, 8], [1, 2, 7, 8, 9], [5, 6, 11, 12, 13], [6, 7, 12, 13, 14], [10, 11, 16, 17, 18], [11, 12, 17, 18, 19], [15, 16, 21, 22, 23], [16, 17, 22, 23, 24], [2, 5, 6, 7, 12], [3, 6, 7, 8, 13], [4, 7, 8, 9, 14], [7, 10, 11, 12, 17], [8, 11, 12, 13, 18], [9, 12, 13, 14, 19], [12, 15, 16, 17, 22], [13, 16, 17, 18, 23], [14, 17, 18, 19, 24], [0, 5, 6, 7, 10], [1, 6, 7, 8, 11], [2, 7, 8, 9, 12], [5, 10, 11, 12, 15], [6, 11, 12, 13, 16], [7, 12, 13, 14, 17], [10, 15, 16, 17, 20], [11, 16, 17, 18, 21], [12, 17, 18, 19, 22], [0, 1, 2, 6, 11], [1, 2, 3, 7, 12], [2, 3, 4, 8, 13], [5, 6, 7, 11, 16], [6, 7, 8, 12, 17], [7, 8, 9, 13, 18], [10, 11, 12, 16, 21], [11, 12, 13, 17, 22], [12, 13, 14, 18, 23], [1, 6, 10, 11, 12], [2, 7, 11, 12, 13], [3, 8, 12, 13, 14], [6, 11, 15, 16, 17], [7, 12, 16, 17, 18], [8, 13, 17, 18, 19], [11, 16, 20, 21, 22], [12, 17, 21, 22, 23], [13, 18, 22, 23, 24], [0, 5, 10, 15, 20], [1, 6, 11, 16, 21], [2, 7, 12, 17, 22], [3, 8, 13, 18, 23], [4, 9, 14, 19, 24], [0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24], [0, 1, 2, 3, 8], [1, 2, 3, 4, 9], [5, 6, 7, 8, 13], [6, 7, 8, 9, 14], [10, 11, 12, 13, 18], [11, 12, 13, 14, 19], [15, 16, 17, 18, 23], [16, 17, 18, 19, 24], [0, 1, 5, 10, 15], [1, 2, 6, 11, 16], [2, 3, 7, 12, 17], [3, 4, 8, 13, 18], [5, 6, 10, 15, 20], [6, 7, 11, 16, 21], [7, 8, 12, 17, 22], [8, 9, 13, 18, 23], [0, 5, 6, 7, 8], [1, 6, 7, 8, 9], [5, 10, 11, 12, 13], [6, 11, 12, 13, 14], [10, 15, 16, 17, 18], [11, 16, 17, 18, 19], [15, 20, 21, 22, 23], [16, 21, 22, 23, 24], [1, 6, 11, 15, 16], [2, 7, 12, 16, 17], [3, 8, 13, 17, 18], [4, 9, 14, 18, 19], [6, 11, 16, 20, 21], [7, 12, 17, 21, 22], [8, 13, 18, 22, 23], [9, 14, 19, 23, 24], [0, 5, 10, 15, 16], [1, 6, 11, 16, 17], [2, 7, 12, 17, 18], [3, 8, 13, 18, 19], [5, 10, 15, 20, 21], [6, 11, 16, 21, 22], [7, 12, 17, 22, 23], [8, 13, 18, 23, 24], [0, 1, 2, 3, 5], [1, 2, 3, 4, 6], [5, 6, 7, 8, 10], [6, 7, 8, 9, 11], [10, 11, 12, 13, 15], [11, 12, 13, 14, 16], [15, 16, 17, 18, 20], [16, 17, 18, 19, 21], [0, 1, 6, 11, 16], [1, 2, 7, 12, 17], [2, 3, 8, 13, 18], [3, 4, 9, 14, 19], [5, 6, 11, 16, 21], [6, 7, 12, 17, 22], [7, 8, 13, 18, 23], [8, 9, 14, 19, 24], [3, 5, 6, 7, 8], [4, 6, 7, 8, 9], [8, 10, 11, 12, 13], [9, 11, 12, 13, 14], [13, 15, 16, 17, 18], [14, 16, 17, 18, 19], [18, 20, 21, 22, 23], [19, 21, 22, 23, 24], [1, 6, 10, 11, 16], [2, 7, 11, 12, 17], [3, 8, 12, 13, 18], [4, 9, 13, 14, 19], [6, 11, 15, 16, 21], [7, 12, 16, 17, 22], [8, 13, 17, 18, 23], [9, 14, 18, 19, 24], [1, 5, 6, 7, 8], [2, 6, 7, 8, 9], [6, 10, 11, 12, 13], [7, 11, 12, 13, 14], [11, 15, 16, 17, 18], [12, 16, 17, 18, 19], [16, 20, 21, 22, 23], [17, 21, 22, 23, 24], [0, 5, 6, 10, 15], [1, 6, 7, 11, 16], [2, 7, 8, 12, 17], [3, 8, 9, 13, 18], [5, 10, 11, 15, 20], [6, 11, 12, 16, 21], [7, 12, 13, 17, 22], [8, 13, 14, 18, 23], [0, 1, 2, 3, 7], [1, 2, 3, 4, 8], [5, 6, 7, 8, 12], [6, 7, 8, 9, 13], [10, 11, 12, 13, 17], [11, 12, 13, 14, 18], [15, 16, 17, 18, 22], [16, 17, 18, 19, 23], [1, 5, 6, 11, 16], [2, 6, 7, 12, 17], [3, 7, 8, 13, 18], [4, 8, 9, 14, 19], [6, 10, 11, 16, 21], [7, 11, 12, 17, 22], [8, 12, 13, 18, 23], [9, 13, 14, 19, 24], [0, 5, 10, 11, 15], [1, 6, 11, 12, 16], [2, 7, 12, 13, 17], [3, 8, 13, 14, 18], [5, 10, 15, 16, 20], [6, 11, 16, 17, 21], [7, 12, 17, 18, 22], [8, 13, 18, 19, 23], [2, 5, 6, 7, 8], [3, 6, 7, 8, 9], [7, 10, 11, 12, 13], [8, 11, 12, 13, 14], [12, 15, 16, 17, 18], [13, 16, 17, 18, 19], [17, 20, 21, 22, 23], [18, 21, 22, 23, 24], [0, 1, 2, 3, 6], [1, 2, 3, 4, 7], [5, 6, 7, 8, 11], [6, 7, 8, 9, 12], [10, 11, 12, 13, 16], [11, 12, 13, 14, 17], [15, 16, 17, 18, 21], [16, 17, 18, 19, 22], [1, 5, 6, 7, 11], [2, 6, 7, 8, 12], [3, 7, 8, 9, 13], [6, 10, 11, 12, 16], [7, 11, 12, 13, 17], [8, 12, 13, 14, 18], [11, 15, 16, 17, 21], [12, 16, 17, 18, 22], [13, 17, 18, 19, 23], [0, 1, 2, 7, 12], [1, 2, 3, 8, 13], [2, 3, 4, 9, 14], [5, 6, 7, 12, 17], [6, 7, 8, 13, 18], [7, 8, 9, 14, 19], [10, 11, 12, 17, 22], [11, 12, 13, 18, 23], [12, 13, 14, 19, 24], [2, 7, 10, 11, 12], [3, 8, 11, 12, 13], [4, 9, 12, 13, 14], [7, 12, 15, 16, 17], [8, 13, 16, 17, 18], [9, 14, 17, 18, 19], [12, 17, 20, 21, 22], [13, 18, 21, 22, 23], [14, 19, 22, 23, 24], [0, 5, 10, 11, 12], [1, 6, 11, 12, 13], [2, 7, 12, 13, 14], [5, 10, 15, 16, 17], [6, 11, 16, 17, 18], [7, 12, 17, 18, 19], [10, 15, 20, 21, 22], [11, 16, 21, 22, 23], [12, 17, 22, 23, 24], [0, 1, 2, 5, 10], [1, 2, 3, 6, 11], [2, 3, 4, 7, 12], [5, 6, 7, 10, 15], [6, 7, 8, 11, 16], [7, 8, 9, 12, 17], [10, 11, 12, 15, 20], [11, 12, 13, 16, 21], [12, 13, 14, 17, 22], [0, 1, 5, 6, 7], [1, 2, 6, 7, 8], [2, 3, 7, 8, 9], [5, 6, 10, 11, 12], [6, 7, 11, 12, 13], [7, 8, 12, 13, 14], [10, 11, 15, 16, 17], [11, 12, 16, 17, 18], [12, 13, 17, 18, 19], [15, 16, 20, 21, 22], [16, 17, 21, 22, 23], [17, 18, 22, 23, 24], [1, 5, 6, 10, 11], [2, 6, 7, 11, 12], [3, 7, 8, 12, 13], [4, 8, 9, 13, 14], [6, 10, 11, 15, 16], [7, 11, 12, 16, 17], [8, 12, 13, 17, 18], [9, 13, 14, 18, 19], [11, 15, 16, 20, 21], [12, 16, 17, 21, 22], [13, 17, 18, 22, 23], [14, 18, 19, 23, 24], [0, 1, 5, 6, 10], [1, 2, 6, 7, 11], [2, 3, 7, 8, 12], [3, 4, 8, 9, 13], [5, 6, 10, 11, 15], [6, 7, 11, 12, 16], [7, 8, 12, 13, 17], [8, 9, 13, 14, 18], [10, 11, 15, 16, 20], [11, 12, 16, 17, 21], [12, 13, 17, 18, 22], [13, 14, 18, 19, 23], [0, 1, 2, 6, 7], [1, 2, 3, 7, 8], [2, 3, 4, 8, 9], [5, 6, 7, 11, 12], [6, 7, 8, 12, 13], [7, 8, 9, 13, 14], [10, 11, 12, 16, 17], [11, 12, 13, 17, 18], [12, 13, 14, 18, 19], [15, 16, 17, 21, 22], [16, 17, 18, 22, 23], [17, 18, 19, 23, 24], [0, 1, 5, 6, 11], [1, 2, 6, 7, 12], [2, 3, 7, 8, 13], [3, 4, 8, 9, 14], [5, 6, 10, 11, 16], [6, 7, 11, 12, 17], [7, 8, 12, 13, 18], [8, 9, 13, 14, 19], [10, 11, 15, 16, 21], [11, 12, 16, 17, 22], [12, 13, 17, 18, 23], [13, 14, 18, 19, 24], [0, 5, 6, 10, 11], [1, 6, 7, 11, 12], [2, 7, 8, 12, 13], [3, 8, 9, 13, 14], [5, 10, 11, 15, 16], [6, 11, 12, 16, 17], [7, 12, 13, 17, 18], [8, 13, 14, 18, 19], [10, 15, 16, 20, 21], [11, 16, 17, 21, 22], [12, 17, 18, 22, 23], [13, 18, 19, 23, 24], [1, 2, 5, 6, 7], [2, 3, 6, 7, 8], [3, 4, 7, 8, 9], [6, 7, 10, 11, 12], [7, 8, 11, 12, 13], [8, 9, 12, 13, 14], [11, 12, 15, 16, 17], [12, 13, 16, 17, 18], [13, 14, 17, 18, 19], [16, 17, 20, 21, 22], [17, 18, 21, 22, 23], [18, 19, 22, 23, 24], [0, 1, 2, 5, 6], [1, 2, 3, 6, 7], [2, 3, 4, 7, 8], [5, 6, 7, 10, 11], [6, 7, 8, 11, 12], [7, 8, 9, 12, 13], [10, 11, 12, 15, 16], [11, 12, 13, 16, 17], [12, 13, 14, 17, 18], [15, 16, 17, 20, 21], [16, 17, 18, 21, 22], [17, 18, 19, 22, 23], [0, 5, 6, 7, 12], [1, 6, 7, 8, 13], [2, 7, 8, 9, 14], [5, 10, 11, 12, 17], [6, 11, 12, 13, 18], [7, 12, 13, 14, 19], [10, 15, 16, 17, 22], [11, 16, 17, 18, 23], [12, 17, 18, 19, 24], [1, 2, 6, 10, 11], [2, 3, 7, 11, 12], [3, 4, 8, 12, 13], [6, 7, 11, 15, 16], [7, 8, 12, 16, 17], [8, 9, 13, 17, 18], [11, 12, 16, 20, 21], [12, 13, 17, 21, 22], [13, 14, 18, 22, 23], [1, 5, 6, 7, 12], [2, 6, 7, 8, 13], [3, 7, 8, 9, 14], [6, 10, 11, 12, 17], [7, 11, 12, 13, 18], [8, 12, 13, 14, 19], [11, 15, 16, 17, 22], [12, 16, 17, 18, 23], [13, 17, 18, 19, 24], [0, 5, 6, 7, 11], [1, 6, 7, 8, 12], [2, 7, 8, 9, 13], [5, 10, 11, 12, 16], [6, 11, 12, 13, 17], [7, 12, 13, 14, 18], [10, 15, 16, 17, 21], [11, 16, 17, 18, 22], [12, 17, 18, 19, 23], [1, 6, 7, 10, 11], [2, 7, 8, 11, 12], [3, 8, 9, 12, 13], [6, 11, 12, 15, 16], [7, 12, 13, 16, 17], [8, 13, 14, 17, 18], [11, 16, 17, 20, 21], [12, 17, 18, 21, 22], [13, 18, 19, 22, 23], [1, 2, 5, 6, 11], [2, 3, 6, 7, 12], [3, 4, 7, 8, 13], [6, 7, 10, 11, 16], [7, 8, 11, 12, 17], [8, 9, 12, 13, 18], [11, 12, 15, 16, 21], [12, 13, 16, 17, 22], [13, 14, 17, 18, 23], [2, 5, 6, 7, 11], [3, 6, 7, 8, 12], [4, 7, 8, 9, 13], [7, 10, 11, 12, 16], [8, 11, 12, 13, 17], [9, 12, 13, 14, 18], [12, 15, 16, 17, 21], [13, 16, 17, 18, 22], [14, 17, 18, 19, 23], [1, 5, 6, 11, 12], [2, 6, 7, 12, 13], [3, 7, 8, 13, 14], [6, 10, 11, 16, 17], [7, 11, 12, 17, 18], [8, 12, 13, 18, 19], [11, 15, 16, 21, 22], [12, 16, 17, 22, 23], [13, 17, 18, 23, 24], [1, 5, 6, 7, 10], [2, 6, 7, 8, 11], [3, 7, 8, 9, 12], [6, 10, 11, 12, 15], [7, 11, 12, 13, 16], [8, 12, 13, 14, 17], [11, 15, 16, 17, 20], [12, 16, 17, 18, 21], [13, 17, 18, 19, 22], [0, 1, 6, 7, 11], [1, 2, 7, 8, 12], [2, 3, 8, 9, 13], [5, 6, 11, 12, 16], [6, 7, 12, 13, 17], [7, 8, 13, 14, 18], [10, 11, 16, 17, 21], [11, 12, 17, 18, 22], [12, 13, 18, 19, 23], [0, 1, 6, 11, 12], [1, 2, 7, 12, 13], [2, 3, 8, 13, 14], [5, 6, 11, 16, 17], [6, 7, 12, 17, 18], [7, 8, 13, 18, 19], [10, 11, 16, 21, 22], [11, 12, 17, 22, 23], [12, 13, 18, 23, 24], [2, 5, 6, 7, 10], [3, 6, 7, 8, 11], [4, 7, 8, 9, 12], [7, 10, 11, 12, 15], [8, 11, 12, 13, 16], [9, 12, 13, 14, 17], [12, 15, 16, 17, 20], [13, 16, 17, 18, 21], [14, 17, 18, 19, 22]]
    all_pos = {5: [], 4: [], 3: [], 2: [], 1: [], 0: []}
    for s in all_arr:
        x = board[s]
        c = np.count_nonzero(x == "O")
        all_pos[c].append(s)

    all_pos.pop(2)
    all_pos.pop(5)
    
    for v in all_pos:
        all_pos[v].sort()
    
    for x in ([4, 3, 3, 0, 0], [3, 3, 3, 1, 0]):
        result = search(x, all_pos, [])
        ret = np.full((5, 5), '').tolist()
        if result:
            for i, region in enumerate(result, 1):
                for c in region:
                    x, y = divmod(c, 5)
                    ret[x][y] = str(i)
            return '\n'.join(row for row in [''.join(r) for r in ret])
    return None


def search(votes, all_pos, arr):
    if not votes:
        return arr
    elif any(not all_pos[x] for x in set(votes)):
        return False
    all_pos = all_pos.copy()
    for y in all_pos[votes[0]]:
        w3 = [p for p in all_pos[3] if not set(y).intersection(set(p))] if 3 in votes else []
        w1 = [p for p in all_pos[1] if not set(y).intersection(set(p))] if 1 in votes else []
        w0 = [p for p in all_pos[0] if not set(y).intersection(set(p))]

        res = search(votes[1:], {3: w3, 1: w1, 0: w0}, arr + [y])
        if res:
            return res
#####################################
class Voter:
    def __init__(self, col, row, val):
        self.col = col
        self.row = row
        self.value = val
        self.district = 0
        
    def isempty(self):
        return not self.district
    
    def assign(self,district):
        self.district = district
    
    def clear(self):
        self.district = 0
        
  
class Board:
    
    def __init__(self, param):
        self.origin = param
        self.grid = []
        self.voters = []
        self.districts = []
        self.current = 1
        self._build()
        
    def __repr__(self):
        grid = []
        for row in self.grid:
            grid.append([v.district for v in row])
        return repr(grid)
    
    def __str__(self):
        return self.__repr__()
        
    def _build(self):
        for i, row in enumerate(self.origin.split("\n")):
            r = []
            for j, val in enumerate(row):
                voter = Voter(i,j,val)
                r.append(voter)
            self.grid.append(r)

    def isvalid(self, r, c):
        if r >= 0 and r < 5 and c >= 0 and c < 5:
            return True
        return False
    
    def isempty(self, r, c):
        if self.isvalid(r, c):
            if self.grid[r][c].isempty():
                return True
        return False
    
    def adjacent(self,r,c):
        for x, y in [(-1,0),(0,-1),(1,0),(0,1)]:
            yield (r + x), (c + y)
    
    def solve(self):
        self.grid[0][0].assign(self.current)
        self.voters.append(self.grid[0][0])
        return self._solve(0,0)
        
    
    def _solve(self, row, col):
        c = self.check_districts()
        if isinstance(c,str):
            return c
        if c is False:
            return c
        for r,c in self.adjacent(row,col):
            if self.isempty(r,c):
                voter = self.grid[r][c]
                district = (len(self.voters)//5) + 1
                voter.assign(district)
                self.voters.append(voter)
                r = self._solve(r,c)
                if r:
                    return r
                del self.voters[-1]
                voter.clear()
        
    def check_votes(self):
        districts = {}
        for voter in self.voters:
            if voter.district not in districts:
                if voter.value == "O":
                    districts[voter.district] = 1
            else:
                if voter.value == "O":
                    districts[voter.district] += 1
        for district in districts:
            if districts[district] > 3 or districts[district] == 2:
                return False
        return True
    
    def no_dead_ends(self):
        n = 0
        for i,row in enumerate(self.grid):
            for j,val in enumerate(row):
                if val.district == 0:
                    num = 0
                    for r,c in self.adjacent(i,j):
                        if self.isempty(r,c):
                            num += 1
                    if num == 0:
                        n += 1
        if n:
            return False
        return True
                        

    def complete(self):
        final = []
        for i in self.grid:
            row = ""
            for j in i:
                row += str(j.district)
            final.append(row)
        return "\n".join(final)
        
    def check_districts(self):
        if len(self.voters) % 5 == 0:
            if self.check_votes() and self.no_dead_ends():
                if len(self.voters) == 25:
                    return self.complete()
                else:
                    return True
            return False
        return True
            
solutions = {'XXOXX\nOXXXX\nXOXOO\nXXOXO\nOXOOX':
'55555\n34444\n33411\n23311\n22221'}
    
def gerrymander(s):
    board = Board(s)
    if s in solutions:
        return solutions[s]
    r = board.solve()
    print(repr(r),repr(s))
    return r
######################################
import heapq
from collections import defaultdict


class Point(complex):
    def __init__(self, *args):
        super().__init__()
        self.__hash = hash((self.real, self.imag))
        self.__inner = False
    def dist(self, other): return abs(self.real-other.real) + abs(self.imag-other.imag)
    def close(self): self.__inner = True
    @property
    def x(self): return int(self.real)
    @property
    def y(self): return int(self.imag)
    @property
    def around(self): return {self+o for o in [1, 1j, -1, -1j]}
    @property
    def closed(self): return self.__inner
    def __hash__(self): return self.__hash
    def __eq__(self, other): return self.real == other.real and self.imag == other.imag
    def __lt__(self, other): return abs(self) < abs(other)
    def __add__(self, other): return Point(complex.__add__(self, other))
    def __repr__(self): return f'P({int(self.real)},{int(self.imag)})'


class State:

    def __init__(self, new_point, last_state=None):
        self.area_id = last_state and last_state.area_id or 1
        self.votes = last_state and last_state.votes.copy() or defaultdict(int)
        self.current_area = last_state and last_state.current_area.copy() | set([new_point]) or set([new_point])
        self.map = last_state and last_state.map.copy() or self.base_map.copy()
        self.used = last_state and last_state.used.copy() | set([new_point]) or set([new_point])
        self.won_areas = last_state and last_state.won_areas or 0
        self.av_votes = last_state and last_state.av_votes or len([v for v in self.base_map.values() if v == 'O'])

        self.votes[self.area_id] += int(self.map[new_point] == 'O')
        if self.map[new_point] == 'O': self.av_votes -= 1
        self.map[new_point] = self.area_id

        if len(self.current_area) == self.map_size:
            self.won_areas += int(self.votes[self.area_id] >= 3)
            next_start_point = self.find_next_start()
            if next_start_point:
                self.area_id += 1
                self.current_area = set([])
                next_start_point = Point(next_start_point)
                self.current_area.add(next_start_point)
                self.used.add(next_start_point)
                self.votes[self.area_id] += int(self.map[next_start_point] == 'O')
                if self.map[new_point] == 'O': self.av_votes -= 1
                self.map[next_start_point] = self.area_id

        self.score = (self.won_areas, -self.area_id, len(self.used))
        self.__hash = hash(str(self.map.values()))

    @property
    def done(self):
        # return self.area_id == self.map_size+1
        return self.won_areas >= 3 and len(self.used) == 25

    @property
    def as_arr(self):
        return '\n'.join(''.join([str(self.map[Point(x, y)]) for x in range(self.map_size)]) for y in range(self.map_size))

    @property
    def is_winnable(self):
        if self.won_areas >= 3: return True
        if ((self.av_votes + self.votes[self.area_id]) // 3 + self.won_areas) < 3: return False
        return True

    def __lt__(self, other):
        return self.score > other.score

    def __eq__(self, other):
        return self.score == other.score

    def __gt__(self, other):
        return self.score < other.score

    def __hash__(self):
        return self.__hash

    @property
    def expandable_sides(self):
        exp = set([])
        for p in self.current_area: exp |= p.around
        return exp & self.point_domain - self.used

    def find_next_start(self):
        for p in sorted(self.point_domain - self.used): return p

    def print(self, old_state=None):
        for y in range(self.map_size):
            print(((''.join([str(old_state.map[Point(x, y)]) for x in range(old_state.map_size)]) + '  ==>  ') if old_state else '') + ''.join([str(self.map[Point(x, y)]) for x in range(self.map_size)]))

def gerrymander(s):
    s_arr = s.split('\n')
    mapping = {Point(x, y): c for y, row in enumerate(s_arr) for x, c in enumerate(row)}
    State.point_domain = set(mapping.keys())
    State.map_size = len(s_arr[0])
    State.base_map = mapping.copy()

    init_state = State(Point(0, 0))

    q = [init_state]
    heapq.heapify(q)

    visited = set([])

    max_iter = 20000

    while q and max_iter:
        curr_state = heapq.heappop(q)

        if curr_state.done:
            return curr_state.as_arr

        for new_p in curr_state.expandable_sides:
            new_state = State(new_p, curr_state)
            if new_state.is_winnable and new_state not in visited:
                heapq.heappush(q, new_state)
                visited.add(new_state)

        max_iter -= 1
####################################################

class Election:

    def __init__(self, inp: str):
        self.iboard, self.oboard, row = [], [[0, 0, 0, 0, 0] for _ in range(5)], []
        for c in inp:
            if c == "O":
                row.append(1)
            elif c == "X":
                row.append(0)
            elif c == "\n":
                self.iboard.append(row)
                row = []
        self.iboard.append(row)
        self.poss_choice = (0, 1, 3, 4)

    def construct(self, dis: list, esum: int, y: int, x: int, musty: int, mustx: int):
        assert 0 <= y < 5
        assert 0 <= x < 5
        dirs, res = ((0, 1), (1, 0), (0, -1), (-1, 0)), []
        if len(dis) == 4:
            es = esum + self.iboard[y][x]
            md = dis + [(y, x)]
            if es in self.poss_choice and (musty, mustx) in md:
                return [(md, es)]
        else:
            for dy, dx in dirs:
                if 0 <= y + dy < 5 and 0 <= x + dx < 5 and (dy + y, dx + x) not in dis and self.oboard[y + dy][x + dx] == 0:
                    ires = (self.construct(dis + [(y, x)], esum + self.iboard[y][x], y + dy, x + dx, musty, mustx))
                    if ires:
                        res += ires
        return res

    def poss_start(self, y: int, x: int):
        slst = []
        for i in range(5):
            for j in range(5):
                if abs(i - y) + abs(j - x) < 5 and self.oboard[i][j] == 0:
                    slst.append((i, j))
        return slst

    def next_empty(self):
        for y in range(5):
            for x in range(5):
                if self.oboard[y][x] == 0:
                    return y, x

    def all_district(self, y: int, x: int):
        all_dist = []
        for p in self.poss_start(y, x):
            for cnst in self.construct([], 0, p[0], p[1], y, x):
                all_dist.append(cnst)
        return all_dist

    def solve(self, lvl: int):
        my, mx = self.next_empty()
        bboard = cp_board(self.oboard)
        bchoice = self.poss_choice
        for ad, es in self.all_district(my, mx):
            if es in self.poss_choice:
                for ny, nx in ad:
                    self.oboard[ny][nx] = lvl + 1
                if lvl == 4:
                    return True
                else:
                    if es in (1, 4):
                        self.poss_choice = (0, 3)
                    if self.solve(lvl + 1):
                        return True
            self.oboard = cp_board(bboard)
            self.poss_choice = bchoice
        return False

    def merge_oboard(self):
        if self.oboard[0][0] == 0:
            return None
        res = ""
        for row in self.oboard:
            line = ''.join([str(c) for c in row])
            res += line + "\n"
        return res[:-1]


def cp_board(b: list):
    o = []
    for r in b:
        o.append(r.copy())
    return o


def gerrymander(s):
    board = Election(s)
    board.solve(0)
    return board.merge_oboard()
###############################################
PENTOMINO = []

def gerrymander(s):
    print(s, flush=True)
    global PENTOMINO
    if len(PENTOMINO) == 0:
        PENTOMINO = buildPentominoes()
    context = { "completed" : False }
    vts = [[1 if cell == 'O' else 0 for cell in row] for row in s.split('\n')]
    ans = make_array_2d(len(vts), len(vts[0]))
    dfs(vts, ans, [], context, PENTOMINO)
    ret = view(ans) if context["completed"] else None
    print(ret)
    return ret

# Flow

def dfs(vts, grid, districts, context, pentomino):
    if context["completed"]:
        return
    p0 = find_grid_pivot(grid)
    if p0 == None: 
        return
    for shape in pentomino:
        if context["completed"]:
            return
        if len(districts) == 0 and shape[0][0] != 1:
            continue
        p1 = find_shape_pivot(shape)
        if not shape_fits(grid, shape, p0, p1):
            continue
        lock(vts, grid, districts, shape, p0, p1)
        if has_completed(grid, districts):
            context["completed"] = True
            return
        if not has_reached_dead_end(grid, districts):
            dfs(vts, grid, districts, context, pentomino)
            if context["completed"]:
                return
        unlock(grid, districts)

def has_reached_dead_end(grid, districts):
    return count_popular_vote(districts) + (len(grid) - len(districts)) < len(grid) / 2

def has_completed(grid, districts):
    return len(grid) == len(districts) and count_popular_vote(districts) > len(grid) / 2

def count_popular_vote(districts):
    pvt = 0
    for shape, p0, p1, pv in districts:
        pvt += pv
    return pvt

def view(xss):
    return '\n'.join([''.join([str(x) for x in xs]) for xs in xss])

def in_bound(grid, y, x):
    return x >= 0 and y >= 0 and x < len(grid[0]) and y < len(grid)

def unlock(grid, districts):
    shape, p0, p1, pv = districts.pop()
    for row in range(0, len(shape)):
        for col in range(0, len(shape[row])):
            if shape[row][col] == 0: 
                continue
            x = col + p0[1] - p1[1]
            y = row + p0[0] - p1[0]
            grid[y][x] = 0

def lock(vts, grid, districts, shape, p0, p1):
    nr = len(districts) + 1
    vote = 0
    for row in range(0, len(shape)):
        for col in range(0, len(shape[row])):
            if shape[row][col] == 0: 
                continue
            x = col + p0[1] - p1[1]
            y = row + p0[0] - p1[0]
            grid[y][x] = nr
            if vts[y][x] == 1:
                vote += 1
    pv = vote > len(grid) / 2
    districts.append((shape, p0, p1, pv))

def shape_fits(grid, shape, p0, p1):
    for row in range(0, len(shape)):
        for col in range(0, len(shape[row])):
            if shape[row][col] == 0: 
                continue
            x = col + p0[1] - p1[1]
            y = row + p0[0] - p1[0]
            if not in_bound(grid, y, x) or grid[y][x] != 0:
                return False
    return True

def find_shape_pivot(shape):
    for row in range(0, len(shape)):
        for col in range(0, len(shape[row])):
            if shape[row][col] == 1:
                return (row, col)
    return None

def find_grid_pivot(grid):
    for row in range(0, len(grid)):
        for col in range(0, len(grid[row])):
            if grid[row][col] == 0:
                return (row, col)
    return None

# Pentominoes

def buildPentominoes():
    xss = {}
    for p in basic_shapes():
        xs = [p, reflect(p)]
        for _ in range(0, 3):
            p = rotate(p)
            xs += [p, reflect(p)]
        for x in xs:
            k = tuple(map(tuple, x))
            if k not in xss:
                xss[k] = x
    return list(xss.values())

def basic_shapes():
    f = [[0,1,1],[1,1,0],[0,1,0]]
    i = [[1,1,1,1,1]]
    l = [[1,0],[1,0],[1,0],[1,1]]
    n = [[1,1,0,0],[0,1,1,1]]
    p = [[1,1],[1,1],[1,0]]
    t = [[0,1,0],[0,1,0],[1,1,1]]
    u = [[1,0,1],[1,1,1]]
    v = [[1,0,0],[1,0,0],[1,1,1]]
    w = [[1,0,0],[1,1,0],[0,1,1]]
    x = [[0,1,0],[1,1,1],[0,1,0]]
    y = [[1,0],[1,1],[1,0],[1,0]]
    z = [[1,1,0],[0,1,0],[0,1,1]]
    return [f,i,l,n,p,t,u,v,w,x,y,z]

def dims(xss):
    return (len(xss), len(xss[0]))

def make_array_2d(r, c):
    return [[0 for col in range(0, c)] for row in range(0, r)]

def rotate(xss):
    r, c = dims(xss)
    rot = make_array_2d(c, r)
    for col in range(0, c):
        for row in range(0, r):
            rot[col][r - row - 1] = xss[row][col]
    return rot

def reflect(xss):
    r, c = dims(xss)
    x0 = (c - 1) // 2
    x1 = x0 + 1 if c % 2 == 0 else x0
    refl = make_array_2d(r, c)
    for col in range(0, c):
        for row in range(0, r):
            refl[row][col] = xss[row][x0 + x1 - col]
    return refl
###########################################################
import cProfile
import time

pieces = set()
top_left = set()
top_right = set()
bottom_left = set()
bottom_right = set()

def pop_count(n):
    return len(bin(n)[2:].replace("0", ""))


def get_pieces(cur=[(0,0)]):
    if len(cur) == 5:
        if len(set(cur)) != len(cur):
            return
        min_i = min([x for x, _ in cur])
        min_j = min([x for _, x in cur])
        max_i = max([x for x, _ in cur])
        max_j = max([x for _, x in cur])
        height = max_i - min_i + 1
        width = max_j - min_j +1
        cur = [(i - min_i, j - min_j) for i, j in cur]
        as_number = 0
        for c in cur:
            i, j = c
            as_number |= (1 << (i * 5 + j))
        pieces.add((as_number, height, width))
        if as_number & 1:
            top_left.add((as_number, 5, 5))
        right_aligned = as_number << (5 - width)
        if right_aligned & (1 << 4):
            top_right.add((right_aligned, 5, 5))
        bottom_aligned = as_number << ((5 - height) * 5)
        if bottom_aligned & (1 << 20):
            bottom_left.add((bottom_aligned, 5, 5))
        bottom_right_aligned = bottom_aligned << (5 - width)
        if bottom_right_aligned & ( 1 << 24):
            bottom_right.add((bottom_right_aligned, 5, 5))
        return
    i, j = cur[-1]
    get_pieces(cur + [(i + 1, j)])
    get_pieces(cur + [(i - 1, j)])
    get_pieces(cur + [(i, j + 1)])
    get_pieces(cur + [(i, j - 1)])


def check(field, used, before_pieces, before_voters, corners):
    if 2 in before_voters or 5 in before_voters:
        return None
    if len([x for x in before_voters if x == 1 or x == 4]) >= 2:
        return None
    if len(before_voters) == 5:
        if len([x for x in before_voters if x >= 3]) >= 3:
            return before_pieces
        else:
            return None
    if corners:
        my_pieces, corner = corners[0]
        if used & corner:
            return check(field, used, before_pieces, before_voters, corners[1:])
    else:
        my_pieces = pieces
    for t in my_pieces:
        p, h, w = t
        for i in range(5 - h + 1):
            for j in range(5 - w + 1):
                n_p = (p << (j + 5 * i))
                if used & n_p:
                    continue
                n_used = used | n_p
                voters = pop_count(field & n_p)
                res = check(field, n_used, before_pieces + [n_p], before_voters + [voters], corners[1:])
                if res:
                    return res


def format_solution(solution):
    sol = ""
    for i in range(5):
        for j in range(5):
            for n, p in enumerate(solution):
                if p & (1 << (i * 5 + j)):
                    sol += str(n+1)
        sol += "\n"
    return sol[:-1]


def gerrymander(s):
    if not pieces:
        get_pieces()
    field = int(s.replace("\n","").replace("O", "1").replace("X", "0")[::-1], 2)
    corners = [(top_left, 1), (top_right, 1 << 4), (bottom_left, 1 << 20), (bottom_right, 1 << 24)]
    solution = check(field, 0, [], [], corners)
    if solution:
        formatted_solution = format_solution(solution)
        return formatted_solution
    return None
####################################################
MODELS = [
        [(3, 2), (3, 2), (3, 2), (1, 4), (0, 5)],
        [(4, 1), (3, 2), (3, 2), (0, 5), (0, 5)]
]
# O X 

def dfs(y, x, visited, size):
    if size == 0:
        return [set()]
    paths = []
    for y_, x_ in (y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1):
        if (y_, x_) not in visited:
            for perm in dfs(y_, x_, visited | {(y_, x_)}, size - 1):
                paths.append({(y_, x_)} | perm)
    return paths

all_possible = set()
partitions = [[0, 0, 0, 4], [0, 0, 3, 1], [0, 0, 2, 2], [0, 2, 1, 1],[1, 1, 1, 1]]
for partition in partitions:
    for a in dfs(0, 0, {(0, 0)}, partition[0]):
        for b in dfs(0, 0, {(0, 0)} | a, partition[1]):
            for c in dfs(0, 0, {(0, 0)} | a | b, partition[2]):
                for d in dfs(0, 0, {(0, 0)} | a | b | c, partition[3]):
                    all_possible.add(tuple(sorted(({(0,0)} | a | b | c| d))))

def get_chunks(y, x):
    K = []
    for chunk in all_possible:
        if not any(y + i < 0 or y + i > 4 or x + j < 0 or x + j > 4 for i, j in chunk):
            K.append(set((y+i, x+j) for i,j in chunk))
    return K
            
def has(refer, ch):
    return all(ch.count(i) <= refer.count(i) for i in ch)
    
def gerrymander(grid):
    grid = grid.split('\n')
    def recurse(y, x, alloted, situation, blocks):
        for chunk in get_chunks(y, x):
            O, X = 0, 0
            if len(chunk & alloted):
                continue

            for y_, x_ in chunk:
                O += grid[y_][x_] == 'O'
                X += grid[y_][x_] == 'X'
            new = situation + [(O, X)]
            
            if not any(has(i, new) for i in MODELS):
                continue
            newa = alloted | chunk
            
            try:
                y_, x_ = next((i, j) for i in range(5) for j in range(5) if (i, j) not in newa)
            except:
                return blocks + [tuple(chunk)]
            
            A = recurse(y_, x_, newa, new, blocks + [tuple(chunk)])
            if A:
                return A

        return False
    A = recurse(0, 0, set(), [], [])
    if not A:
        return None
    
    new_grid = [[' ' for i in range(5)] for j in range(5)]
    for i, block in enumerate(A):
        for y, x in block:
            new_grid[y][x] = str(i + 1)
            
    return '\n'.join(''.join(i) for i in new_grid)
########################################
class Graph(): # a directed graph with arbitrary entity and relation attributes
    def __init__(self, structure=None):
        self.structure = self.clone_structure(structure) if structure!=None else dict()
    def clone_structure(self, structure):
        import copy
        cloned_structure = copy.deepcopy(structure)
        return cloned_structure
    def add_node(self, node, node_attributes=None):
        if node not in self.structure.keys(): self.structure[node]=dict()
        self.structure[node]['node_attr'] = node_attributes if node_attributes!=None else dict()
        self.structure[node]['edges'] = dict()
    def add_edge(self, from_node, to_node, edge_attributes=None):
        if from_node not in self.structure.keys():
            self.structure[from_node]=dict()
            self.structure[from_node]['node_attr'] = dict()
            self.structure[from_node]['edges'] = dict()
        if to_node not in self.structure.keys():
            self.structure[to_node]=dict()
            self.structure[to_node]['node_attr'] = dict()
            self.structure[to_node]['edges'] = dict()
        self.structure[from_node]['edges'][to_node] = edge_attributes

def board2Graph(area_string):
    graph = Graph()
    supporterMap = [[0 if c != 'O' else 1 for c in row] for row in area_string.split()]  # area >> supporterMap[i][j]
    regionIDMap = [[0 for c in row] for row in area_string.split()]  # area >> regionalIDmap[i][j]
    [nRows, nColumns] = [len(area_string.split()), len(area_string.split()[0])]
    for i in range(nRows):
        for j in range(nColumns):
            k = i * nColumns + j  # j = k % nColumns; i = k//nColumns
            graph.add_node(k,{'square':(i,j),'candidate':supporterMap[i][j],'region':regionIDMap[i][j]})
    for i in range(nRows-1):
        for j in range(nColumns-1):
            k = i * nColumns + j
            graph.add_edge(k, k + 1, 1)
            graph.add_edge(k + 1, k, 1)
            graph.add_edge(k, k + nColumns, 1)
            graph.add_edge(k + nColumns, k, 1)
    for i in range(nRows-1):
        k = (i+1) * nColumns - 1
        graph.add_edge(k, k + nColumns, 1)
        graph.add_edge(k + nColumns, k, 1)
    for j in range(nColumns-1):
        k = (nRows - 1) * nColumns + j
        graph.add_edge(k, k + 1, 1)
        graph.add_edge(k + 1, k, 1)
    return graph

def gerrymander(s):
    print('s =',s.split())
    supporterMap = [[0 if c != 'O' else 1 for c in row] for row in s.split()]
    regionIDMap = [[0 for c in row] for row in s.split()]
    regionIDMap[0][0] = 1
    graph = board2Graph(s).structure
    def next_move(x,y):  # z <-> (x,y): x = z//5; y = z%5; z = x*5 + y
        for z in graph[x*5 + y]['edges']: yield [z//5,z%5]
    def electoral_college_win_feasible(regionID, electoral_votes):
        return regionID - electoral_votes <= 3
    def DFS_with_backtracking(zzz, zz, region_size, popular_vote_in_region, regionID, electoral_votes):
        def zero_index(regionIDMap):
            for i in range(len(regionIDMap)):
                for j in range(len(regionIDMap[0])):
                    if regionIDMap[i][j] == 0: return [i, j]
            return -1
        if region_size == 5:             # capacity reached
            regionID += 1
            if popular_vote_in_region >= 3: electoral_votes += 1  # region has popular-vote majority
            if regionID > 5: return electoral_votes >= 3  # win if electoral-college majority reached
            elif electoral_college_win_feasible(regionID, electoral_votes):
                [x,y] = zero_index(regionIDMap)
                regionIDMap[x][y] = regionID
                if DFS_with_backtracking(None, x*5 + y, 1, supporterMap[x][y], regionID, electoral_votes):
                    return True
                regionIDMap[x][y] = 0          # backtrack
            return False
        for [x,y] in next_move(zz//5,zz%5):
            if regionIDMap[x][y] == 0:         # if unexplored field
                regionIDMap[x][y] = regionID
                if DFS_with_backtracking(zz, x*5 + y, region_size + 1,
                                         popular_vote_in_region + supporterMap[x][y], regionID, electoral_votes):
                    return True
                regionIDMap[x][y] = 0          # backtrack
        return zzz is not None and DFS_with_backtracking(None, zzz, region_size, popular_vote_in_region,
                                                       regionID, electoral_votes)
    feasible = DFS_with_backtracking(None, 0, 1, supporterMap[0][0], 1, 0)
    region_map = [''.join(map(str, regionIDMap[i])) for i in [0,1,2,3,4]]
    return '\n'.join(region_map) if feasible else None
#######################################
class Graph(): # a directed graph with arbitrary entity and relation attributes
    def __init__(self, structure=None):
        self.structure = self.clone_structure(structure) if structure!=None else dict()
    def clone_structure(self, structure):
        import copy
        cloned_structure = copy.deepcopy(structure)
        return cloned_structure
    def add_node(self, node, node_attributes=None):
        if node not in self.structure.keys(): self.structure[node]=dict()
        self.structure[node]['node_attr'] = node_attributes if node_attributes!=None else dict()
        self.structure[node]['edges'] = dict()
    def add_edge(self, from_node, to_node, edge_attributes=None):
        if from_node not in self.structure.keys():
            self.structure[from_node]=dict()
            self.structure[from_node]['node_attr'] = dict()
            self.structure[from_node]['edges'] = dict()
        if to_node not in self.structure.keys():
            self.structure[to_node]=dict()
            self.structure[to_node]['node_attr'] = dict()
            self.structure[to_node]['edges'] = dict()
        self.structure[from_node]['edges'][to_node] = edge_attributes

def board2Graph(area_string):
    graph = Graph()
    supporterMap = [[0 if c != 'O' else 1 for c in row] for row in area_string.split()]  # area >> supporterMap[i][j]
    regionIDMap = [[0 for c in row] for row in area_string.split()]  # area >> regionalIDmap[i][j]
    [nRows, nColumns] = [len(area_string.split()), len(area_string.split()[0])]
    for i in range(nRows):
        for j in range(nColumns):
            k = i * nColumns + j  # j = k % nColumns; i = int((k - j)/nColumns)
            graph.add_node(k,{'square':(i,j),'candidate':supporterMap[i][j],'region':regionIDMap[i][j]})
    for i in range(nRows-1):
        for j in range(nColumns-1):
            k = i * nColumns + j
            graph.add_edge(k, k + 1, 1)
            graph.add_edge(k + 1, k, 1)
            graph.add_edge(k, k + nColumns, 1)
            graph.add_edge(k + nColumns, k, 1)
    for i in range(nRows-1):
        k = (i+1) * nColumns - 1
        graph.add_edge(k, k + nColumns, 1)
        graph.add_edge(k + nColumns, k, 1)
    for j in range(nColumns-1):
        k = (nRows - 1) * nColumns + j
        graph.add_edge(k, k + 1, 1)
        graph.add_edge(k + 1, k, 1)
    return graph

def gerrymander(s):
    print('s =',s.split())
    supporterMap = [[0 if c != 'O' else 1 for c in row] for row in s.split()]
    regionIDMap = [[0 for c in row] for row in s.split()]
    regionIDMap[0][0] = 1
    graph = board2Graph(s).structure
    def next_move(x,y):  # z <-> (x,y): x = int((z-z%5)/5); y = z%5; z = x*5 + y
        for z in graph[x*5 + y]['edges']: yield [int((z-z%5)/5),z%5]
    def electoral_college_win_feasible(regionID, electoral_votes):
        return regionID - electoral_votes <= 3
    def DFS_with_backtracking(zzz, zz, region_size, popular_vote_in_region, regionID, electoral_votes):
        def zero_index(regionIDMap):
            for i in range(len(regionIDMap)):
                for j in range(len(regionIDMap[0])):
                    if regionIDMap[i][j] == 0: return [i, j]
            return -1
        if region_size == 5:             # capacity reached
            regionID += 1
            if popular_vote_in_region >= 3: electoral_votes += 1  # region has popular-vote majority
            if regionID > 5: return electoral_votes >= 3  # win if electoral-college majority reached
            elif electoral_college_win_feasible(regionID, electoral_votes):
                [x,y] = zero_index(regionIDMap)
                regionIDMap[x][y] = regionID
                if DFS_with_backtracking(None, x*5 + y, 1, supporterMap[x][y], regionID, electoral_votes):
                    return True
                regionIDMap[x][y] = 0          # backtrack
            return False
        for [x,y] in next_move(int((zz-zz%5)/5),zz%5):
            if regionIDMap[x][y] == 0:         # if unexplored field
                regionIDMap[x][y] = regionID
                if DFS_with_backtracking(zz, x*5 + y, region_size + 1,
                                         popular_vote_in_region + supporterMap[x][y], regionID, electoral_votes):
                    return True
                regionIDMap[x][y] = 0          # backtrack
        return zzz is not None and DFS_with_backtracking(None, zzz, region_size, popular_vote_in_region,
                                                       regionID, electoral_votes)
    feasible = DFS_with_backtracking(None, 0, 1, supporterMap[0][0], 1, 0)
    region_map = [''.join(map(str, regionIDMap[i])) for i in [0,1,2,3,4]]
    return '\n'.join(region_map) if feasible else None
########################################################
def gerrymander(s):
    supporterMap = [[0 if c != 'O' else 1 for c in row] for row in s.split()]
    regionIDMap = [[0 for c in row] for row in s.split()]
    regionIDMap[0][0] = 1
    def next_move(x,y):
        if (y > 0): yield [x,y-1]  # go left
        if (x > 0): yield [x-1,y]  # go up
        if (y < 4): yield [x,y+1]  # go right
        if (x < 4): yield [x+1,y]  # go down
    def electoral_college_win_feasible(regionID, electoral_votes):
        return regionID - electoral_votes <= 3
    def DFS_with_backtracking(zzz, zz, region_size, popular_vote_in_region, regionID, electoral_votes):
        def zero_index(regionIDMap):
            for i in range(len(regionIDMap)):
                for j in range(len(regionIDMap[0])):
                    if regionIDMap[i][j] == 0: return [i, j]
            return -1
        if region_size == 5:             # capacity reached
            regionID += 1
            if popular_vote_in_region >= 3: electoral_votes += 1  # region has popular-vote majority
            if regionID > 5: return electoral_votes >= 3  # win if electoral-college majority reached
            elif electoral_college_win_feasible(regionID, electoral_votes):
                [x,y] = zero_index(regionIDMap)
                regionIDMap[x][y] = regionID
                if DFS_with_backtracking(None, x*5 + y, 1, supporterMap[x][y], regionID, electoral_votes): 
                    return True
                regionIDMap[x][y] = 0          # backtrack
            return False
        for [x,y] in next_move(int((zz-zz%5)/5),zz%5):
            if regionIDMap[x][y] == 0:         # if unexplored field
                regionIDMap[x][y] = regionID
                if DFS_with_backtracking(zz, x*5 + y, region_size + 1, 
                                         popular_vote_in_region + supporterMap[x][y], regionID, electoral_votes):
                    return True
                regionIDMap[x][y] = 0          # backtrack
        return zzz is not None and DFS_with_backtracking(None, zzz, region_size, popular_vote_in_region,
                                                       regionID, electoral_votes)
    feasible = DFS_with_backtracking(None, 0, 1, supporterMap[0][0], 1, 0)
    region_map = [''.join(map(str, regionIDMap[i])) for i in [0,1,2,3,4]]
    return '\n'.join(region_map) if feasible else None
