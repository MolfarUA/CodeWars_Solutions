576986639772456f6f00030c


def path_finder(maze):
    grid = maze.splitlines()
    end = h, w = len(grid) - 1, len(grid[0]) - 1
    bag, seen = {(0, 0): 0}, set()
    while bag:
        x, y = min(bag, key=bag.get)
        rounds = bag.pop((x, y))
        seen.add((x, y))
        if (x, y) == end: return rounds
        for u, v in (-1, 0), (0, 1), (1, 0), (0, -1):
            m, n = x + u, y + v
            if (m, n) in seen or not (0 <= m <= h and 0 <= n <= w): continue
            new_rounds = rounds + abs(int(grid[x][y]) - int(grid[m][n]))
            if new_rounds < bag.get((m, n), float('inf')): bag[m, n] = new_rounds
_____________________________
from heapq import *

def path_finder(maze):
    lst  = [ [int(c) for c in row] for row in maze.split('\n')]
    X, Y = len(lst), len(lst[0])
    end  = (X-1,Y-1)
    q, seens = [(0,end==(0,0),0,0)], {(0,0): 0}
    while q and not q[0][1]:
        c,_,x,y = heappop(q)
        for dx,dy in ((0,1), (0,-1), (1,0), (-1,0)):
            new = a,b = x+dx,y+dy
            if 0<=a<X and 0<=b<Y:
                dc = abs(lst[a][b] - lst[x][y])
                if seens.get(new, float("inf")) > c+dc:
                    heappush(q, (c+dc, new==end, a, b) )
                    seens[new] = c+dc
    return q[0][0]
_____________________________
#------------Imports section:
from collections import defaultdict     #For data storage in Dijkstra's Algorithm
import sys                              #For Dijkstra's Algorithm
from collections.abc import MutableMapping  #For indexed priority queue
#------end imports


#Approach: Apply Dijkstra's Algorithm with an indexed priority queue that implements an
#          efficient update-key method.  The alteration to Dijkstra's algorithm for the
#          alpine problem is how 'shortest distance' is determined: The distance to a 
#          neighbor is defined as the differential of the height between the current node
#          and the height of the neighbor node




#------Indexed Priority Queue
#Class provides an indexed priority queue: Simply a priority queue 
# where we can alter the priority any element (and still have a priority queue).
# This implementation performs updates efficiently in the priority queue
# Updating priority in priority queue is needed in an efficient method of Dijkstra
# Methods: clear, popitem, peekitem
#          Entry and update performed like dictionaries
#                ipQ = IndexedPriorityQueue()
#                ipQ['a'] = 2   
#                ipQ['a'] = 0   #update to priority 0 
#  refs: https://www.baeldung.com/cs/min-heaps-decrease-key
#        https://mkhoshpa.github.io/IndexedPQ/
#        William Fiest's videos @ https://www.youtube.com/channel/UCD8yeTczadqdARzQUp29PJw
class IndexedPriorityQueue(MutableMapping):

    __VAL_LOC = 0   #Data on heap and dictionary is: [value, key, index order]
    __KEY_LOC = 1   #Data on heap and dictionary is: [value, key, index order]
    __ODR_LOC = 2   #Data on heap and dictionary is: [value, key, index order]

    def __init__(self):
        self.ipQueue = []
        self.d = {}
    #end method

    #Accessed when indexing e.g. ipQueue['a'] = 4.  Allows for the creation and
    # updating an element in the priority queue
    def __setitem__(self, key, value):
        if key in self.d:                   #if key exits, we are updating it...
            self.pop(key)                   #...so remove entry; triggers __delitem__

        entry = [value, key, len(self)]   #new entry for priority queue
        self.d[key] = entry               #store in dictionary
        self.ipQueue.append(entry)           #put into the priority queue but...
        self._decreaseKey(len(self.ipQueue)-1) #...but move this updated key up the heap if required
    #end method

    #triggered by popping
    def __delitem__(self, key):
        entry = self.d[key]
        while entry[self.__ODR_LOC]:                      #Terminates when entry[self.__ODR_LOC]==0 i.e. at top of heap
            parentLoc = (entry[self.__ODR_LOC] - 1) >> 1  # calculate the offset of the parent
            parent = self.ipQueue[parentLoc]
            self._swap(entry[self.__ODR_LOC], parent[self.__ODR_LOC])
        self.popitem()
    #end function

    #When accessing via indexing off a key: e.g. val =  ipQueue['a']
    def __getitem__(self, key):
        return self.d[key][self.__VAL_LOC]

    def __iter__(self):
        return iter(self.d)
    
    def __len__(self):
        return len(self.d)

    #Tree at node i roots a min-heap
    def _minHeapify(self, i):
        numVerts = len(self.ipQueue)
        h = self.ipQueue
        while True:
            lft = (i<<1)+1        # get the index of the left child
            rht = (i+1)<<1        # get the index of the right child

            if lft<numVerts     and    h[lft][self.__VAL_LOC] < h[i][self.__VAL_LOC]:
                low = lft
            else:
                low = i

            if rht<numVerts     and    h[rht][self.__VAL_LOC] < h[low][self.__VAL_LOC]:
                low = rht

            if low == i:
                break

            self._swap(i, low)
            i = low
        #end while
    #end method

    def _decreaseKey(self, i):
        while i:
            parent = (i-1) >> 1                           # calculate the offset of the parent
            if self.ipQueue[parent][self.__VAL_LOC] < self.ipQueue[i][self.__VAL_LOC]:      #if value of parent < value of child i....
                break                                       #...finished decrease
            self._swap(i, parent)
            i = parent
    #end method

    def _swap(self, i, j):
        self.ipQueue[i], self.ipQueue[j] = self.ipQueue[j], self.ipQueue[i]
        self.ipQueue[i][self.__ODR_LOC] = i
        self.ipQueue[j][self.__ODR_LOC] = j
    #end method

    #return the pair (key, value) where value is the lowesta and remove's element out of the heap
    def popitem(self):
        entry = self.ipQueue[0]                   #The min element on the heap (by min heap property)
        if len(self.ipQueue) == 1:                  #Scenario: Because there is only one thing in heap...
            self.ipQueue.pop()                      #...we simply pop it; no need to heapifiy
        else:                                       #We must protect the heap property
            self.ipQueue[0] = self.ipQueue.pop()      #set last element on heap to first one
            self.ipQueue[0][self.__ODR_LOC] = 0     #...set its order to first
            self._minHeapify(0)                     #such that node 0 roots a min-heap
        del self.d[entry[self.__KEY_LOC]]         #pluck the key/val associaed to the popped item out of dictionary
        return entry[self.__KEY_LOC], entry[self.__VAL_LOC]
    #end method

    #return a tuple (key, value) of element with the higest priority (lowest value)
    def peekitem(self):
        return (self.ipQueue[0][self.__KEY_LOC], self.ipQueue[0][self.__VAL_LOC])
    #end method

    def clear(self):
        del self.ipQueue[:]     #remove the heap
        self.d.clear()          #remove the dictionary
    #end method
#end class


#Class Implaments minimum path algorithm: Dijkstra's version
class MinimumPathFinder(object):

    def __init__(self, graph, startVert, endVert) -> None:
        self.graph = graph
        self.nR = len(self.graph)
        self.nC = len(self.graph[0])
        self.startVert = startVert
        self.endVert = endVert
    #end 

    #A nice example of using a closure method: This closure generates and returns
    # a function 'initalizer'. Function 'initalizer' returns a dictionary, which has n*n
    # entries, whose keys are (i,j) tuples, and values are set to the provided seedVal
    # (e.g. integer max, None, etc.) 
    def initMap(self, seedVal):
        def initalizer():
            maper = defaultdict(int)
            for i in range(self.nR):
                for j in range(self.nC):
                    maper[(i,j)] = seedVal
            return maper
        return  initalizer
    #end closure

    
    #uses the closure to generate a special initalization function based on a specific
    # initalized value
    def initDist(self):
        distanceInitalizer = self.initMap(sys.maxsize)
        return distanceInitalizer()
    #end function
    

    #uses the closure to generate a special initalization function based on a specific
    # initalized value
    def initPrev(self):
        previousInitalizer = self.initMap(None)
        return previousInitalizer()
    #end function

    
    #uses the closure to generate a special initalization function based on a specific
    # initalized value
    def initVisited(self):
        visitedInitalizer = self.initMap(False)
        return visitedInitalizer()
    #end function

    
    #uses the closure to generate a special initalization function based on a specific
    # initalized value
    def inGraph(self, neighbor):
        i,j = neighbor[0], neighbor[1]
        return (0<=i and i<self.nR  and 0<=j and j<self.nC)
    #end function

    #With the alpine problem, distance is calculated 
    def calculateDistance(self, curVert, neighborVert ):
        return abs( self.graph[curVert[0]][curVert[1]] - self.graph[neighborVert[0]][neighborVert[1]])
    #end function

    #Eager Dijkstra: This version of Dijkstra's Algorithm calculates the shortest path from a 
    #                start vertex, to a specific end vertex.  This version does not put duplicate
    #                tuples into the priority queue (the 'lazy' version sufferes from this).
    #Current algorithim implementation uses an indexed-based minimum priority queue that supports
    #  O(log(n)) updates to the keys (which are the vertex locations (i,j))
    #dist: dist[(i,j)] is the minimum distance from the source node, to the node (i,j)
    #prev: prev[(i,j)] is the node used to reach (i,j) e.g. prev[(i,j)] == (m,n) means
    #      that we got to node (i,j) from node (m,n)
    def eagerDijkstra(self):
        #The four cardinal directions (di[s],dj[s]) for s=0,1,2,3 is (-1,0), (0,-1) 
        di = [-1,  0, 1,  0]
        dj = [ 0, -1, 0 , 1]

        dist = self.initDist()          #dist[(i,j)] == min distance from source to node (i,j)
        prev = self.initPrev()          #prev[(i,j)] == (m,n): Got to (i,j) from (m,n)
        visited = self.initVisited()    #visited[(i,j)] == True iff vertex has been visited
        pQueue = IndexedPriorityQueue()

        dist[self.startVert] = 0        #by definition of dist
        pQueue[self.startVert] = 0      #Elements on IP-queue: ((i,j),dist[(i,j)]) 

        while len(pQueue)>0:            #while there are verts to process
            val = pQueue.popitem()              #pop off the indexed priority queue
            loc, minDist  = val[0], val[1]      #data management from the tupple popped off
            i,j = loc[0], loc[1]                #data management from the tupple popped off

            curVert = (i,j)                     #current vertex we will search in 4 cardinal dirs
            
            visited[curVert] = True             #acknowlege we have visited this node
            
            if curVert == self.endVert: 
                break
            
            if dist[curVert] < minDist:         #shorter distance already found, so skip the search....
                continue                        #...and continue to the next node in the IP queue

            for s in range(4):                  #search in all four cardinal directions
                ni, nj = i + di[s], j + dj[s]   #(i,j) is location of neighbor to source
                neighbor = (ni, nj)             #neighbor to curVert
                if self.inGraph(neighbor) and not visited[neighbor]:      #neigbor must be on the board
                    distToNeighbor = self.calculateDistance(curVert, neighbor)
                    distToTravel = dist[curVert] + distToNeighbor #the dist to get from the source to neighbor via current vertex 
                    if distToTravel < dist[neighbor]:             #True implies we found a cheaper path! Therefore...
                        dist[neighbor] = distToTravel             #...we must update minDistanceFromSource
                        prev[neighbor] = curVert                  #...and remember where we came from
                        pQueue[neighbor] = distToTravel           #...and update key in the IP Queue
            #end for
        #end while
        return dist
    #end function
#end class


#----------------------------------------------------------------------------
#   Start of Kata Moduals
#----------------------------------------------------------------------------

#In:  String of the maze 
#Out: 2D list of integers representing maze
def buildCostMat(maze):
    maze = maze.split('\n')
    nR, nC = len(maze), len(maze[0])
    mazeCost = [list(map(int,i)) for i in maze]
    return mazeCost, nR, nC
#end function

#Use Dijkstra's Algorithm to find a path to the maze
def path_finder(maze):
    costMaze, nR, nC = buildCostMat(maze)
    startVert = (0,0)       #Upper left corner as start point of maze
    endVert = (nR-1, nC-1)  #Lower right corner as start point of maze

    c = MinimumPathFinder(costMaze, startVert, endVert)
    dist = c.eagerDijkstra()
    return dist[endVert]
#end main driver
_____________________________
def path_finder(maze):
    
    maze = maze.split('\n')
    n = len(maze)
    min_climb = [[9999999]*n for i in range(n)] #minimum climb, initialize with large number signifing unevaluated location
    min_climb[0][0] = 0 #start position, no climbing needed   
    queue = [(0,0)] #queue of indices to be evaluated
    
    while queue:
        i, j = queue.pop(0)
        
        for x, y in (0,1),(0,-1),(-1,0),(1,0): #east-(0,1); west-(0,-1); north-(-1,0); south-(1,0)
            p, q = i+x, j+y #adjacent locations
            if -1 < p < n and -1 < q < n: #inside maze
                climb = abs(int(maze[p][q]) - int(maze[i][j])) #climb = diff btw altitudes
                if min_climb[p][q] > min_climb[i][j]+climb: #if min_climb = -1 (unevaluated location) or if min_climb is larger
                    min_climb[p][q] = min_climb[i][j]+climb #set the new (smaller)min_climb
                    queue.append((p, q))
    
    return min_climb[n-1][n-1] #target location
_____________________________
from heapq import *

MOVES = ((1,0), (-1,0), (0,1), (0,-1))

def path_finder(area):
    area = list(map(list,area.splitlines()))
    x_max, y_max = len(area), len(area[0])
    end = x_max - 1, y_max - 1
    queue = [(0,(0,0))] # total cost, pos
    
    while len(queue):
        c, (x, y) = heappop(queue)
        if (x,y)==end:
            return c
        if area[x][y].isdigit():
            val = int(area[x][y])
            area[x][y] = 'X'
            for dx, dy in MOVES:
                i, j = pos = x+dx, y+dy
                if 0 <= i < x_max and 0 <= j < y_max and area[i][j].isdigit():
                    edge = abs(val - int(area[i][j]))
                    heappush(queue,(c+edge,pos))
_____________________________
import numpy as np
import heapq as hq

def path_finder(maze):
    maze = maze.split("\n")
    n = len(maze)
    visited = np.ones((n, n)) * np.inf
    queue = [(0, 0, 0)]
    while queue:
        dist, x, y = hq.heappop(queue)
        if x == n-1 and y == n-1:
            return dist
        for i, j in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= i < n and 0 <= j < n and (new_dist := dist + abs(int(maze[x][y]) - int(maze[i][j]))) < visited[i][j]:
                visited[i][j] = new_dist
                hq.heappush(queue, (new_dist, i, j))
_____________________________
class PathFinder:
    def __init__(self, area):
        self.finish_x, self.finish_y = (len(area) - 1, len(area[0]) - 1)
        self.area_points = {(x, y): {'points': self._find_neighboring_points(x, y),
                                     'peek': int(peek)}
                            for x, line in enumerate(area)
                            for y, peek in enumerate(line)}
        self.visited = set()
        self.cache = {(0, 0): 0}

    def find_shortest_path(self):
        stack = {(0, 0)}
        while stack:
            x, y = min(stack, key=lambda point: self.cache[point])
            stack.remove((x, y))
            points = self.area_points[x, y]['points']
            self._update_cache(points, x, y)
            stack |= points - self.visited
            self.visited.add((x, y))
        return self.cache[self.finish_x, self.finish_y]

    def _update_cache(self, points, *previous):
        for point in points:
            if point not in self.visited:
                steps = abs(self.area_points[point]['peek'] - self.area_points[previous]['peek'])
                steps += self.cache[previous]
                if point not in self.cache or self.cache[point] > steps:
                    self.cache[point] = steps

    def _find_neighboring_points(self, x, y):
        return {(x1, y1) for x1, y1 in ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y))
                if 0 <= x1 <= self.finish_x and 0 <= y1 <= self.finish_y}


def path_finder(area):
    return PathFinder(area.splitlines()).find_shortest_path()
_____________________________
from collections import defaultdict
from heapq import heappop, heappush

def path_finder(area):
    area = [list(map(int, row)) for row in area.split("\n")]
    n = len(area)
    dists = defaultdict(lambda: float("inf"))
    visited = set()
    queue = [(0, (0, 0))]
    while queue:
        dist, (i, j) = heappop(queue)
        if (i, j) not in visited:
            if i == j == n - 1:
                return dist
            visited.add((i, j))
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x, y = i + di, j + dj
                if (0 <= x < n) and (0 <= y < n) and (x, y) not in visited:
                    if (alt := dist + abs(area[i][j] - area[x][y])) < dists[(x, y)]:
                        dists[(x, y)] = alt
                        heappush(queue, (alt, (x, y)))
    return float("inf")
_____________________________
def maze2graph(maze):
    '''
        Maze to Graph
    '''
    import numpy as np
    maze = list(map(list, maze.splitlines()))
    maze = np.array(maze).astype(int)
    
    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height)}

    for row, col in graph.keys():            
        if row < height - 1:
            graph[(row, col)].append(((row + 1, col), abs(maze[row+1][col] - maze[row][col]) ))
            graph[(row + 1, col)].append(((row, col), abs(maze[row][col] - maze[row+1][col]) ))
        if col < width - 1:
            graph[(row, col)].append(((row, col + 1), abs(maze[row][col+1] - maze[row][col]) ))
            graph[(row, col + 1)].append(((row, col), abs(maze[row][col] - maze[row][col+1]) ))

    return graph, maze

def dijkstra(nodes, distances):
    unvisited = {node: None for node in nodes}
    visited = {}
    current = nodes[0]
    currentDistance = 1
    unvisited[current] = currentDistance
    while True:
        for neighbour, distance in distances[current]:
            if neighbour not in unvisited: continue
            newDistance = currentDistance + distance
            if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
                unvisited[neighbour] = newDistance
        visited[current] = currentDistance - 1
        del unvisited[current]
        if not unvisited: break
        candidates = [node for node in unvisited.items() if node[1]]
        current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]
    return visited

def path_finder(maze):
    graph,maze = maze2graph(maze)
    nodes = list(graph.keys())
    distances = graph.copy()
    return dijkstra(nodes, distances)[nodes[-1]]
