5573f28798d3a46a4900007a


from collections import deque
def find_shortest_path(grid, start_node, end_node):
    if not grid: return []
    w, h = len(grid), len(grid[0])
    prev, bag = {start_node: None}, deque([start_node])
    while bag:
        node = bag.popleft()
        if node == end_node:
            path = []
            while node:
                path.append(node)
                node = prev[node]
            return path[::-1]
        x, y = node.position.x, node.position.y
        for i, j in (0,1), (1,0), (0,-1), (-1,0):
            m, n = x + i, y + j
            if not (0 <= m < w and 0 <= n < h): continue
            next_node = grid[m][n]
            if next_node not in prev and next_node.passable:
                prev[next_node] = node
                bag.append(next_node)
__________________________________
import heapq
from collections import deque


def heuristic(node, end_node):
    return abs(node.position.x - end_node.position.x) + abs(node.position.y - end_node.position.y)


def find_shortest_path(grid, start_node, end_node):
    if not grid:
        return grid

    parents = {start_node: None}
    cost_so_far = {start_node: 0}
    cost_to_the_end = {start_node: heuristic(start_node, end_node)}
    total_cost = {start_node: cost_so_far.get(start_node) + cost_to_the_end.get(start_node)}

    closed_nodes = deque()
    opened_nodes = []

    heapq.heapify(opened_nodes)
    heapq.heappush(opened_nodes, (total_cost.get(start_node), start_node))

    grid_height = len(grid)
    grid_width = len(grid[0])

    def find_neighbors(node):
        node = (node.position.x, node.position.y)
        result = []
        if node[0] > 0:
            result.append(grid[node[0] - 1][node[1]])
        if node[0] < grid_height - 1:
            result.append(grid[node[0] + 1][node[1]])
        if node[1] > 0:
            result.append(grid[node[0]][node[1] - 1])
        if node[1] < grid_width - 1:
            result.append(grid[node[0]][node[1] + 1])
        return result

    def update_node(child, parent):
        parents.update({child: parent})
        cost_so_far.update({child: cost_so_far.get(parent) + 1})
        cost_to_the_end.update({child: heuristic(child, end_node)})
        total_cost.update({child: cost_so_far.get(child) + cost_to_the_end.get(child)})

    def generate_path(node):
        path = []
        while parents.get(node):
            path.append(node)
            node = parents.get(node)
        return [start_node] + list(reversed(path))

    while opened_nodes:
        t_c, node = heapq.heappop(opened_nodes)
        closed_nodes.append(node)

        if node == end_node:
            return generate_path(node)

        neighbors = find_neighbors(node)
        for neighbor in neighbors:
            if neighbor not in closed_nodes and neighbor.passable:
                if (total_cost.get(neighbor), neighbor) in opened_nodes:
                    if total_cost.get(neighbor) > total_cost.get(node) + 1:
                        update_node(neighbor, node)
                else:
                    update_node(neighbor, node)
                    heapq.heappush(opened_nodes, (total_cost.get(neighbor), neighbor))
__________________________________
from collections import deque

neighbors = lambda node: (
    (node.position.x+1, node.position.y),
    (node.position.x-1, node.position.y),
    (node.position.x, node.position.y+1),
    (node.position.x, node.position.y-1))

def find_shortest_path(grid, start_node, end_node):
    if not grid: return []
    H, W, queue, visited = len(grid), len(grid[0]), deque([(start_node, [])]), {start_node}
    check = lambda i, j: 0 <= i < H and 0 <= j < W
    while queue:
        current, path = queue.popleft()
        path = path + [current]
        if current == end_node: return path
        for i,j in neighbors(current):
            if check(i, j):
                node = grid[i][j]
                if node.passable and node not in visited:
                    queue.append((node, path))
                    visited.add(node)
__________________________________
from math import sqrt

def distance_between(node1, node2):
    return sqrt((node1.position.x - node2.position.x) ** 2 + (node1.position.y - node2.position.y) ** 2)


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()  # We want start -> end path
    return total_path


def neighbor_nodes(node, grid):
    """Return a list of neighoring nodes"""
    neighbors = set([])
    if node.position.y:
        potential_neighbor = grid[node.position.x][node.position.y - 1]
        if potential_neighbor.passable:
            neighbors.add(potential_neighbor)
    if node.position.y < len(grid[node.position.x]) - 1:
        potential_neighbor = grid[node.position.x][node.position.y + 1]
        if potential_neighbor.passable:
            neighbors.add(potential_neighbor)
    if node.position.x:
        potential_neighbor = grid[node.position.x - 1][node.position.y]
        if potential_neighbor.passable:
            neighbors.add(potential_neighbor)
    if node.position.x < len(grid) - 1:
        potential_neighbor = grid[node.position.x + 1][node.position.y]
        if potential_neighbor.passable:
            neighbors.add(potential_neighbor)

    return neighbors


def find_shortest_path(grid, start_node, end_node):
    """
    Roughly similar implementation of A* as described here:
    https://en.wikipedia.org/wiki/A*_search_algorithm
    """
    if not grid:
        return []
    
    # pre-set h_score (distance to end node) and g_score (distance to start node) for all nodes
    for node_list in grid:
        for node in node_list:
            node.h_score = distance_between(node, end_node)
            node.g_score = distance_between(node, start_node)

    closed_nodes = set([])
    open_nodes = set([start_node])
    came_from = dict()
    start_node.g_score = 0  # Cost from start
    start_node.f_score = start_node.g_score + start_node.h_score  # lower score means potentially better node to evaluate
    while open_nodes:
        current_node = sorted(open_nodes, key=lambda node: node.f_score)[0]  # get node with most potential
        if current_node is end_node:
            # We're at the destination, so build path and return it
            return reconstruct_path(came_from, end_node)

        open_nodes.remove(current_node)
        closed_nodes.add(current_node)
        for neighbor in neighbor_nodes(current_node, grid):
            if neighbor in closed_nodes:
                continue
            tentative_g_score = current_node.g_score + neighbor.h_score
            if neighbor not in open_nodes or tentative_g_score < neighbor.g_score:
                came_from[neighbor] = current_node
                neighbor.g_score = tentative_g_score
                neighbor.f_score = neighbor.g_score + distance_between(neighbor, end_node)
                if neighbor not in open_nodes:
                    open_nodes.add(neighbor)
    return []  # Failed to find a path
__________________________________
from Queue import Queue

class Connections(dict):
    def __init__(self, grid):
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                node = grid[row][col]
                if not node.passable:
                    continue
                self[node] = []
                for mrow, mcol in ( (0,1), (0,-1), (1,0), (-1,0) ) :
                    if row+mrow < 0 or col+mcol < 0:
                        continue
                    if row+mrow == len(grid) or col+mcol == len(grid[row]):
                        continue
                    other = grid[row+mrow][col+mcol]
                    if not other.passable:
                        continue
                    self[node].append(other)

def find_shortest_path(grid, start_node, end_node):
    if start_node == end_node:
        return [ start_node ] if start_node else []
    
    agenda = Queue()
    agenda.put( [start_node] )
    visited = set([start_node])
    connections = Connections(grid)
    
    while not agenda.empty():
        path = agenda.get()
        lastnode = path[-1]
        for nextnode in connections[lastnode]:
            if nextnode in visited:
                continue
            if nextnode == end_node:
                return path + [nextnode]
            visited.add(nextnode)
            
            agenda.put( path + [nextnode] )
            
    return []
__________________________________
from collections import deque
def find_shortest_path(grid, start_node, end_node):
    if not grid or not grid[0]:return []
    if start_node.position.x==end_node.position.x and start_node.position.y==end_node.position.y:return [start_node]
    m,n=len(grid),len(grid[0])
    begin=deque([start_node])
    end=deque([end_node])
    v1,v2={(start_node.position.x,start_node.position.y):[start_node]},{(end_node.position.x,end_node.position.y):[end_node]}
    while begin or end:
        if len(v1)<len(v2):
            state,vis,check=begin,v1,v2
        else:
            state,vis,check=end,v2,v1
        for _ in range(len(state)):
            node=state.popleft()
            r,c=node.position.x,node.position.y
            for nr,nc in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
                if 0<=nr<m and 0<=nc<n and grid[nr][nc].passable and (nr,nc) not in vis:
                    if (nr,nc) in check:
                        if vis==v1:
                            return v1[(r,c)]+v2[(nr,nc)][::-1]
                        else:
                            return v1[(nr,nc)]+v2[(r,c)][::-1]
                    vis[(nr,nc)]=vis[(r,c)]+[grid[nr][nc]]
                    state.append((grid[nr][nc]))
__________________________________
def check_pos(y, x, len_y, len_x):
    if (x > -1) and (y > -1) and (x < len_x) and (y < len_y):
        if (x == 0) or (y == 0) or (x == len_x - 1) or (y == len_y - 1):
            return 0
        return 1
    return -1

def find_shortest_path1(grid_mass, start_node, end_node, len_y, len_x):
    #print(grid_mass)
    #print(start_node, end_node)
    #print(len_y,len_x)
    
    steps = ( (+1,0), (-1,0), (0,+1), (0,-1))
    grid_mass[start_node[0]][start_node[1]] = 1
    mas = [(start_node[0],start_node[1])]

    num_place = 0
    fl = True
    while fl:
        mas0 = []
        num_place += 1
        fl_step = False

        for y,x in mas:
            for st in steps:
                nx = x+st[0]
                ny = y+st[1]
                if check_pos(ny, nx, len_y, len_x)>=0:
                    if grid_mass[ny][nx] == 0:
                        grid_mass[ny][nx] = num_place+1
                        fl_step = True
                        mas0.append((ny,nx))
                        if ny == end_node[0] and nx == end_node[1]:
                            fl = False
                            break

        if not fl_step:
            break
        mas = mas0.copy()

    num_max = x = y = 0
    for ny in range(len_y):
        for nx in range(len_x):
            if num_max < grid_mass[ny][nx]:
                num_max = grid_mass[ny][nx]
                y = ny
                x = nx

    mas = [(y,x)]
    grid_mass[y][x] = "x"
    while num_max > 1:
        num_max -= 1
        for st in steps:
            nx = x + st[0]
            ny = y + st[1]
            if check_pos(ny, nx, len_y, len_x) >= 0:
                if grid_mass[ny][nx] == num_max:
                    mas.append((ny,nx))
                    grid_mass[ny][nx] = "x"
                    y = ny
                    x = nx
                    break
    mas.reverse()
    return mas

def find_shortest_path(grid, start_node, end_node):
    grid_mass = []
    len_y = len(grid)
    if len_y==0:
        return []
    if start_node==end_node:
        return [end_node]
    len_x = len(grid[0])
    for ny in range(len_y):
        str = []
        for nx in range(len_x):
            if grid[ny][nx].passable:
                str.append(0)
            else:
                str.append(-1)
        grid_mass.append(str)

    start_n = (start_node.position.x, start_node.position.y)
    end_n = (end_node.position.x, end_node.position.y)
    mas_step = find_shortest_path1(grid_mass,start_n,end_n,len_y,len_x)
    
    mas = []
    for ny,nx in mas_step:
        mas.append(grid[ny][nx])

    # print(mas)
    return mas
__________________________________
from collections import deque

n = m = 0
grid = []
par = []
dist = []
ngb = ((0, 1), (1, 0), (0, -1), (-1, 0))

def bfs(sx, sy):
    que = deque([(sx, sy)])
    dist[sx][sy] = 1
    while len(que):
        vx, vy = que.popleft()
        for _dir in ngb:
            ux, uy = (vx + _dir[0], vy + _dir[1])
            if ux < 0 or ux >= n or uy < 0 or uy >= m: continue
            if not grid[ux][uy].passable: continue
            if dist[ux][uy]: continue
            dist[ux][uy] = dist[vx][vy] + 1
            que.append((ux, uy))
            par[ux][uy] = (vx, vy)

def find_shortest_path(grid_arg, start_node, end_node):
    global grid, dist, par, n, m
    grid = grid_arg

    # parse grid
    n = len(grid)
    if n == 0:
        return []
    m = len(grid[0])
    if m == 0:
        return []
    
    par = [[0] * m for i in range(n)]
    dist = [[0] * m for i in range(n)]

    start = (start_node.position.x, start_node.position.y)
    end = (end_node.position.x, end_node.position.y)

    # run bfs
    bfs(start[0], start[1])

    #return output
    res = [end_node]
    cur = end
    while cur != start:
        cur = par[cur[0]][cur[1]]
        res.append(grid[cur[0]][cur[1]])
    res.reverse()
    return res
__________________________________
def distance(s, e):
    return max(abs(s.position.x - e.position.x), abs(s.position.y - e.position.y))


def next_nodes(x, y, grid):
    next = []
    height = len(grid)
    width = len(grid[0])

    if x > 0 and grid[x-1][y].passable:
        next.append(grid[x-1][y])
    if x < height - 1 and grid[x+1][y].passable:
        next.append(grid[x+1][y])
    if y > 0 and grid[x][y-1].passable:
        next.append(grid[x][y-1])
    if y < width - 1 and grid[x][y+1].passable:
        next.append(grid[x][y+1])

    return next


def build_path(end, grid_parents):
    path = []
    n = end
    while n is not None:
        path.append(n)
        n = grid_parents[n.position.x][n.position.y]

    path.reverse()
    return path

MAXINT = 999999999
def find_shortest_path(grid, start_node, end_node):
    
    if not len(grid):
        return []
    
    height = len(grid)
    width = len(grid[0])

    grid_parents = []
    grid_g = []
    for i in range(height):
        row_parents = []
        row_g = []
        for j in range(width):
            row_parents.append(None)
            row_g.append(MAXINT)
        grid_parents.append(row_parents)
        grid_g.append(row_g)

    open_list = []

    grid_g[start_node.position.x][start_node.position.y] = 0
    open_list.append(start_node)
    current_node = start_node

    while len(open_list):
        min_f = MAXINT
        g = grid_g[current_node.position.x][current_node.position.y] + 1

        for n in open_list:
            h = distance(n, end_node)
            f = g + h

            if f < min_f:
                min_f = f
                current_node = n
        
        open_list.remove(current_node)
        next = next_nodes(current_node.position.x, current_node.position.y, grid)
        g = grid_g[current_node.position.x][current_node.position.y] + 1

        for n in next:

            if n == end_node:
                grid_parents[n.position.x][n.position.y] = current_node
                return build_path(end_node, grid_parents)

            if g < grid_g[n.position.x][n.position.y]:
                grid_parents[n.position.x][n.position.y] = current_node
                grid_g[n.position.x][n.position.y] = g
                if n not in open_list:
                    open_list.append(n)

    return build_path(end_node, grid_parents)
