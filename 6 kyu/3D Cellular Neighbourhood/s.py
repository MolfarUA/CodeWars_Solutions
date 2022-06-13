NEIGHBOURHOOD = {"von_neumann": sum, "moore": max}

def closer_cells(n_type, distance, x, y, z):
    return ((x+u, y+v, z+w)
            for u in range(-distance, distance+1) for v in range(-distance, distance+1) for w in range(-distance, distance+1)
            if 0 < NEIGHBOURHOOD[n_type](map(abs, (u, v, w))) <= distance)

def get_3Dneighbourhood(n_type, arr, coordinates, distance=1):
    def is_inside(x, y, z):
        return 0 <= x < len(arr) and 0 <= y < len(arr[0]) and 0 <= z < len(arr[0][0])

    return [] if not is_inside(*coordinates) else [arr[x][y][z]
        for x, y, z in closer_cells(n_type, distance, *coordinates)
        if is_inside(x, y, z)]
_______________________________
NEIGHBOURHOOD_TYPE = {
    "moore": lambda d: ((z, y, x)
                        for z in range(-d, d + 1)
                        for y in range(-d, d + 1)
                        for x in range(-d, d + 1)
                        if x or y or z),
    "von_neumann": lambda d: ((z, y, x)
                              for z in range(-d, d + 1)
                              for y in range(abs(z) - d, d - abs(z) + 1)
                              for x in range(abs(z) + abs(y) - d, d - abs(z) - abs(y) + 1)
                              if x or y or z)
}


def get_3Dneighbourhood(n_type, mat, coordinates, distance=1):
    i, j, k = coordinates
    width = (height := (depth := len(mat)) and len(mat[0])) and len(mat[0][0])
    if distance < 1 or not (0 <= k < width and 0 <= j < height and 0 <= i < depth): return []
    return [mat[layer][row][col] for z, y, x in NEIGHBOURHOOD_TYPE[n_type](distance)
            if 0 <= (col := x + k) < width and 0 <= (row := y + j) < height and 0 <= (layer := z + i) < depth]
_______________________________
def get_3Dneighbourhood(n_type, mat, coordinates, distance=1):
    k,n,m = coordinates
    d = distance
    
    if not mat or distance == 0 or k > len(mat)-1 or n > len(mat[0])-1 or m > len(mat[0][0])-1: return []

    moore = []
    von_neumann = []
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            for z in range(len(mat[0][0])):
                if i >= k-d and i <= k+d and j >= n-d and j <= n+d and z >= m-d and z <= m+d and (i,j,z) != (k,n,m):
                    moore.append(mat[i][j][z])
                    if abs(i-k) + abs(j-n) + abs(z-m) <= d: #Manhatten distance
                        von_neumann.append(mat[i][j][z])
    
    return moore if n_type == 'moore' else von_neumann
_______________________________
moore = lambda d: [
    (k, m, n)
    for k in range(-d, d+1)
    for n in range(-d, d+1)
    for m in range(-d, d+1)
    if not k == m == n == 0
]
von = lambda d: [
    (k, m, n)
    for k in range(-d, d+1)
    for n in range(-d, d+1)
    for m in range(-d, d+1)
    if (not k == m == n == 0) and abs(k) + abs(m) + abs(n) <= d
]

def get_3Dneighbourhood(type, arr, coordinates, distance=1):
    if not arr or distance == 0:
        return []

    m, n, k = coordinates
    M, N, K = len(arr), len(arr[0]), len(arr[0][0])
    if not (0 <= m < M and 0 <= n < N and 0 <= k < K):
        return []
    deltas = (moore if type == 'moore' else von)(distance)
    result = []
    for dm, dn, dk in deltas:
        a, b, c = m+dm, n+dn, k+dk
        if 0 <= a < M and 0 <= b < N and 0 <= c < K:
            result.append(arr[a][b][c])
    return sorted(result)
_______________________________
def get_3Dneighbourhood(typ, arr, coords, d=1):

    def getRng(u,l):    return range(max(0,u-d), min(u+d+1,l))
    def moore(i,j,k):   return (i,j,k) != (x,y,z)
    def neumann(i,j,k): return sum(map(abs, (b-a for a,b in zip((x,y,z),(i,j,k)) )))
    
    ans, (x,y,z) = [], coords
    distCheck    = moore if typ=='moore' else neumann
    
    if 0 <= x < len(arr) and 0 <= y < len(arr[0]) and 0 <= z < len(arr[0][0]):
        ans = [ arr[i][j][k] for i in getRng(x,len(arr))
                             for j in getRng(y,len(arr[0]))
                             for k in getRng(z,len(arr[0][0]))
                             if 0 < distCheck(i,j,k) <= d ]
    return ans
_______________________________
import numpy as np

def mat_dist(coords_1, coords_2):
    ans = 0
    for i in range(len(coords_1)):
        ans += abs(coords_1[i] - coords_2[i])
    return ans

def get_3Dneighbourhood(n_type, mat, coordinates, distance=1):
    mat = np.array(mat)
    
    #return array
    ans = []
    
    #get matrix shape
    mat_shape = mat.shape
    
    #distance == 0 or empty_mat
    if distance == 0 or mat.size == 0:
        return ans
    
    #check for bounds
    for i in range(len(coordinates)):
        if coordinates[i] < 0 or coordinates[i] >= mat_shape[i]:
            return ans
    
    #generate ranges
    ranges = [range(max(0, coordinates[i] - distance), min(coordinates[i] + distance + 1, mat_shape[i])) for i in range(len(coordinates))]
    
    #begin looping
    for i in ranges[0]:
        for j in ranges[1]:
            for k in ranges[2]:
                #exclude the center itself
                if (i, j, k) == coordinates:
                    continue                    

                #if moore include everything, if von_newmann include only if within the specified distance
                if n_type == 'moore' or (n_type == 'von_neumann' and mat_dist(coordinates, (i, j, k)) <= distance):
                    ans.append(mat[i, j, k])
    return ans
_______________________________
def get_3Dneighbourhood(n_type, mat, coordinates, distance=1):
    x, y, z, M, N, K = coordinates[0], coordinates[1], coordinates[2], len(mat), len(mat[0]), len(mat[0][0])
    if len(mat) == 0 or x < 0 or x >= M or y < 0 or y >= N or z < 0 or z >= K or distance == 0:
        return []
    
    neighbour = []
    for i in range(max(0, x - distance), min(M, x + distance + 1)):
        for j in range(max(0, y - distance), min(N, y + distance + 1)):
            for k in range(max(0, z - distance), min(K, z + distance + 1)):
                if (i != x or j != y or k != z) and (n_type == 'moore' or abs(i - x) + abs(j - y) + abs(k - z) <= distance):
                    neighbour.append(mat[i][j][k])
    return neighbour
_______________________________
def get_3Dneighbourhood(n_type, mat, coordinates, distance=1):
    x, y, z = coordinates
    if not (0 <= x < len(mat) and 0 <= y < len(mat[x]) and 0 <= z < len(mat[x][y])): return []
    res = []
    for x2 in range(x - distance, x + distance + 1):
        for y2 in range(y - distance, y + distance + 1):
            for z2 in range(z - distance, z + distance + 1):
                if not(x2 == x and y2 == y and z2 == z or not (0 <= x2 < len(mat) and 0 <= y2 < len(mat[x2]) and 0 <= z2 < len(mat[x2][y2])) or n_type == 'von_neumann' and abs(x2 - x) + abs(y2 - y) + abs(z2 - z) > distance): res.append(mat[x2][y2][z2])
    return res
_______________________________
def get_3Dneighbourhood(n_type, mat, coordinates, distance=1):
    lst = []
    O = len(mat)
    M = len(mat[0])
    N = len(mat[0][0])
    kc,ic,jc = coordinates[0], coordinates[1], coordinates[2]

    if (ic < 0 or jc < 0 or kc < 0 or ic > M-1 or jc > N-1 or kc > O-1):
        return lst

    if (n_type == "von_neumann"):
        kmin = max(0, kc-distance)
        kmax = min(O-1, kc+distance)

        for k in range(kmin, kmax+1):
            di = distance-abs(k-kc)

            imin = max(0, ic-di)
            imax = min(M-1, ic+di)

            for i in range(imin,imax+1):
                dj = di-abs(i-ic)

                jmin = max(0, jc-dj)
                jmax = min(N-1, jc+dj)

                for j in range(jmin, jmax+1):
                    if i != ic or j != jc or k != kc:
                        lst.append(mat[k][i][j])
            
    elif (n_type == "moore"):
        imin = max(ic-distance,0)
        imax = min(ic+distance,M-1)
        jmin = max(jc-distance,0)
        jmax = min(jc+distance,N-1)
        kmin = max(kc-distance,0)
        kmax = min(kc+distance,O-1)

        for k in range(kmin, kmax+1):
            for i in range(imin, imax+1):
                for j in range(jmin, jmax+1):
                    if i != ic or j != jc or k != kc:
                        lst.append(mat[k][i][j])

    return lst
_______________________________
def get_3Dneighbourhood(t,mat,c,d):
    if d==0: return []
    try: mat[c[0]][c[1]][c[2]]
    except: return []
    lm=len(mat)
    ln=len(mat[0])
    lk=len(mat[0][0])
    ok=lm*ln
    mb,me=max(0,c[0]-d),min(c[0]+d+1,lm)
    nb,ne=max(0,c[1]-d),min(c[1]+d+1,ln)
    kb,ke=max(0,c[2]-d),min(c[2]+d+1,lk)
    if t=="moore":
        return [mat[m][n][k] for m in range(mb,me) for n in range(nb,ne) for k in range(kb,ke) if (m,n,k)!=c]
    else:
        return [mat[m][n][k] for m in range(mb,me) for n in range(nb,ne) for k in range(kb,ke) if 0<abs(m-c[0])+abs(n-c[1])+abs(k-c[2])<=d]
