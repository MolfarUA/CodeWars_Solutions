5376b901424ed4f8c20002b7


def distance(a, b):
    return ((b[0] - a[0])**2 + (b[1] - a[1])**2)**0.5

def iterative_closest(arr):
    n = len(arr)
    mini = ((arr[0], arr[1]), distance(arr[0], arr[1]))
    for i in range(n-1):
        for j in range(i+1,n):
            dij = distance(arr[i], arr[j])
            if dij < mini[1]:
                mini = ((arr[i], arr[j]), dij)
    return mini
    
def recursive_closest(arr):
    n = len(arr)
    if n <= 3:
        # if the array is less than 3 items
        # use the naive method
        return iterative_closest(arr)
    
    # divide the row into two parts
    # and search the closest pair of points in each
    mid = n // 2
    ml, mr = recursive_closest(arr[:mid]), recursive_closest(arr[mid:])
    
    # the closest pair is the one having the minimum
    # distance in both parts
    mlr = ml if ml[1] < mr[1] else mr
    
    # Now we have to combine the results from
    # the two parts
    
    # find the points that are close to the median point
    arr1 = [pt for pt in arr if abs(pt[0]-arr[mid][0]) < mlr[1]]
    arr1.sort(key=lambda pt:pt[1]) # sort it by Y coordinates
    # foreach of the points search within the next 7 points 
    # which have the lowest distance
    n1 = len(arr1)
    for i in range(n1-1):
        for j in range(1, min(7, n1-i)):
            dij = distance(arr1[i], arr1[i+j])
            if dij < mlr[1]:
                mlr = ((arr1[i], arr1[i+j]), dij)
    return mlr
                
def closest_pair(points):
    arr = sorted(points)
    return recursive_closest(arr)[0]
______________________________________
from bisect import bisect
from operator import itemgetter


def closest_pair(points):
    
    def dist(p,q): return sum( (a-b)**2 for a,b in zip(p,q) )**.5
    
    def seekPair(i,j):
        nonlocal dMin, closests
        
        m = i+j >> 1
        if m-i>1: seekPair(i,m)
        if j-m>1: seekPair(m,j)
        
        x,y = pts[m]
        i,j = (bisect(pts,(x-dMin,y),i,m), 
               bisect(pts,(x+dMin,y),m,j))
        lst = pts[i:j]
        lst.sort(key=sortByY)
        
        for i,a in enumerate(lst):
            for j in range(i+1,len(lst)):
                b = lst[j]
                if dMin < b[1]-a[1]: break
                d = dist(a,b)
                if d<dMin: dMin, closests = d, (a,b)
    
    
    pts      = sorted(points)
    dMin     = float("inf")
    closests = ()
    sortByY  = itemgetter(1)
    
    seekPair(0,len(pts))
    return closests
______________________________________
def distance(points):
    return (points[0][0] - points[1][0]) ** 2 + (points[0][1] - points[1][1]) ** 2

def closest_pair(points):
    if len(points) == 2:
        return points
    points = sorted(points)
    n = len(points)
    l = closest_pair(points[:n // 2 + 1])
    r = closest_pair(points[n // 2:])
    x = points[n // 2][0]
    if distance(l) < distance(r):
        d = distance(l)
        ans = l
    else:
        d = distance(r)
        ans = r
    middle_points = [i for i in points if (x - i[0]) ** 2 < d]
    middle_points = sorted(middle_points, key=lambda i: i[1])
    for i, p in enumerate(middle_points):
        j = i - 1
        while j >= 0 and (p[1] - middle_points[j][1]) ** 2 < d:
            cur_d = distance((p, middle_points[j]))
            if cur_d < d:
                d = cur_d
                ans = (middle_points[j], p)
            j -= 1
    return ans
______________________________________
from scipy.spatial import cKDTree as KDT


def closest_pair(points):
    tree = KDT(points)
    record = None
    nn = tree.query(points, k=2)
    for i, dist in enumerate(nn[0]):
        if not record or record[0] > dist[1]:
            record = [dist[1], points[i], points[nn[1][i][1]]]
    return (record[1], tuple(record[2]))
______________________________________
from bisect import bisect, bisect_left
import math

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# O(nlogn) time and O(n) space
def closest_pair(points):
    closest_pair_, min_distance = None, math.inf
    
    # iterate through the points horizontally, as of the sweep line algorithm
    hor_sorted_points = sorted(points, key=lambda p: p[0])
    hor_vicinity = []  # points on the strip of width min_distance, sorted vertically
    for point in hor_sorted_points:
        
        # update strip and compute box
        hor_vicinity = [p for p in hor_vicinity if 
                        point[0] - p[0] < min_distance]  # remove points left behind
        hor_vicinity_ys = [p[1] for p in hor_vicinity]  # key list for bisect
        vicinity = hor_vicinity[
            bisect(hor_vicinity_ys, point[1]-min_distance):
            bisect_left(hor_vicinity_ys, point[1]+min_distance)
        ]  # points on the box of width min_distance and height 2*min_distance
        
        # check distances with points on the box
        for point2 in vicinity:
            distance = calculate_distance(point, point2)
            if distance < min_distance:
                closest_pair_, min_distance = (point, point2), distance
                
        # add current point to the strip, for the next iteration
        hor_vicinity.insert(bisect(hor_vicinity_ys, point[1]), point) 
        
    return closest_pair_
______________________________________
def closest_pair(points):
    x, y = zip(*points)
    H = sorted(range(len(x)), key=x.__getitem__)
    V = sorted(range(len(y)), key=y.__getitem__)

    def distance2(i, j):
        return (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2

    def bf_closest(H):
        d, i, j = float('inf'), -1, -1
        for u in range(len(H)):
            for v in range(u + 1, len(H)):
                d, i, j = min((d, i, j), (distance2(H[u], H[v]), H[u], H[v]))
        return d, i, j

    def closest(x, y, H, V):
        n = len(H)
        if n <= 3:
            d, i, j = bf_closest(H)
        else:
            m = n // 2
            mid = 0.5 * (x[H[m-1]] + x[H[m]])
            H1 = H[:m]
            H2 = H[m:]
            V1, V2 = [], []
            set_h1 = set(H1)
            for idx in V:
                if idx in set_h1:
                    V1.append(idx)
                else:
                    V2.append(idx)
            d1, i1, j1 = closest(x, y, H1, V1)
            d2, i2, j2 = closest(x, y, H2, V2)
            d, i, j = min((d1, i1, j1), (d2, i2, j2))
            S = [idx for idx in V if abs(x[idx] - mid) < d ** 0.5]
            k = len(S)
            for u in range(k - 1):
                for v in range(u + 1, min(u + 3, k - 1) + 1):
                    d, i, j = min((d, i, j), (distance2(S[u], S[v]), S[u], S[v]))
        return d, i, j
    i, j = closest(x, y, H, V)[1:]
    return points[i], points[j]
______________________________________
from math import dist
from scipy.spatial import Voronoi

def closest_pair(points):
    if len(points)==2: #two points
        return points
    if len(set(points))!=len(points): #duplicated points
        for p in points:
            if points.count(p)>1: return (p, p)
    voronoi_distances = [((points[e[0]], points[e[1]]), dist(points[e[0]], points[e[1]])) for e in Voronoi(points).ridge_points]
    return min(voronoi_distances, key=lambda d: d[1])[0]
______________________________________
from sklearn.neighbors import BallTree
import pandas as pd

def closest_pair(points):
    df = pd.DataFrame(points, columns=['x', 'y'])
    tree = BallTree(df[['x', 'y']].values, leaf_size=2)
    dist, idxs = tree.query(df[['x', 'y']].values, k=2)
    val, idx = min((val[1], idx) for (idx, val) in enumerate(dist))
    return (points[idxs[idx][0]], points[idxs[idx][1]])
______________________________________
def closest_pair(points):
    points = sorted(points, key=lambda x: (x[1], x[0]))
    p1, p2 = points[0], points[-1]
    min_dist = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**.5
    res = (p1, p2)
    for idx, p1 in enumerate(points):
        min_x, max_x, max_y = p1[0]-min_dist, p1[0]+min_dist, p1[1]+min_dist
        for p2 in points[idx+1:]:
            if p2[1] > max_y:
                break
            if p2[0] < min_x or p2[0] > max_x:
                continue
            dist = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**.5
            if dist < min_dist:
                min_dist, res = dist, (p1, p2)
                min_x, max_x, max_y = p1[0]-min_dist, p1[0]+min_dist, p1[1]+min_dist
                if min_dist == 0:
                    return res
    return res
