from itertools import count

getRevStep = lambda step: ((step<<2) + (step>>2)) & 15

CONFIG = ((8, -1,0, 'N'), (4, 0,-1, 'W'), (2, 1,0, 'S'), (1, 0,1, 'E'))
SWARM  = [ tuple((step, getRevStep(step), dx, dy, dir) for step,dx,dy,dir in CONFIG if not step & n)
           for n in range(16)]


def maze_solver(arr):
    
    for x,row in enumerate(arr):
        for y,v in enumerate(row):
            if   v=='B': ball = (x,y)
            elif v=='X': end  = (x,y)
    
    bag   = {ball}
    lX,lY = len(arr), len(arr[0])
    paths = [[ [] for _ in range(lY)] for _ in range(lX)]
    
    lastModifiedBagGen = -1
    for nIter in count(0):
        
        for x,y in bag: paths[x][y].append('')                                          # "wait there"
        
        oldBagLen = len(bag)
        while 1:
            addToBag = set()
            for x,y in bag:
                doors = 0 if isinstance(arr[x][y],str) else arr[x][y]
                
                for step,revStep,dx,dy,dir in SWARM[doors]:
                    a, b   = x+dx,y+dy
                    if (0 <= a < lX and 0 <= b < lY                                     #  in board
                        and len(paths[a][b]) <= nIter                                   # "No! Don't go there again!"
                        and (isinstance(arr[a][b],str) or not revStep & arr[a][b])):    #  target tile allows travel too
                        
                        addToBag.add((a,b))
                        paths[a][b] = paths[x][y][:]
                        paths[a][b][-1] += dir
                        
                        if end == (a,b): return paths[a][b]
            
            if not addToBag: break
            bag |= addToBag
        
        if oldBagLen != len(bag):             lastModifiedBagGen = nIter
        elif nIter - lastModifiedBagGen > 4:  return None
        
        arr  = [[ ((n<<1) + (n>>3)) & 15 if isinstance(n,int) else n for n in row ]
                for row in arr]                                                         # Rotate all tiles colckwise
################
WALL = {'N':0b1000, 'W':0b0100, 'S':0b0010, 'E':0b0001}

def maze_solver(a):
    M = {(r, c):(0 if v in ['X', 'B'] else v) for r, row in enumerate(a) for c, v in  enumerate(row)}
    B = [(r, c) for r, c in M if a[r][c] == 'B'].pop()
    X = [(r, c) for r, c in M if a[r][c] == 'X'].pop()
    P = {B:[]}

    while all(len(v) < 50 for v in P.values()):
  
        newP = {}        
        for m in P:
            stack, newP[m] = [(list(P[m]) + [''], m)], list(P[m]) + ['']
            while stack:
                pp, m = stack.pop()
                for d in 'NWSE':
                    move = (m[0]+{'N':-1, 'S':1}.get(d, 0), m[1]+{'W':-1, 'E':1}.get(d, 0))
                    
                    # Check we have a valid position that has not been visited this iteration and we can leave our cell and enter new one
                    if move in M and move not in newP and not M[m] & WALL[d] and not M[move] & WALL[{'N':'S', 'S':'N', 'W':'E', 'E':'W'}[d]]:
                        path = list(pp)
                        path[-1] += d
                        newP[move], stack = path, stack + [(path, move)]
                        if move == X: return path                        
        # Rotate maze            
        M = {k:{0:0,  1:2, 2:4, 4:8, 8:1, 3:6, 6:12, 12:9, 9:3, 5:10, 10:5, 7:14, 14:13, 13:11, 11:7, 15:15}[v] for k, v in M.items()}
        P = newP                                      
        
    return
######################
from heapq import heappush, heappop

rotate = lambda n,d: n<<d|n>>4-d

def maze_solver(ar):
    for i,row in enumerate(ar):
        for j,x in enumerate(row):
            if x == 'B':
                si, sj = i, j
            elif x == 'X':
                ei, ej = i, j
    ar = list(map(list, ar))
    ar[si][sj] = ar[ei][ej] = 0
    H, W, heap, seen = len(ar), len(ar[0]), [(0, si, sj, [''])], {(si, sj, 0)}
    while heap:
        d, i, j, p = heappop(heap)
        if i == ei and j == ej:
            return p
        (*a, b), x = p, d&3
        curr = rotate(ar[i][j], x)
        if i and curr&8 == rotate(ar[i-1][j], x)&2 == 0 and (i-1, j, x) not in seen:
            seen.add((i-1, j, x))
            heappush(heap, (d, i-1, j, a+[b+'N']))
        if j and curr&4 == rotate(ar[i][j-1], x)&1 == 0 and (i, j-1, x) not in seen:
            seen.add((i, j-1, x))
            heappush(heap, (d, i, j-1, a+[b+'W']))
        if i<H-1 and curr&2 == rotate(ar[i+1][j], x)&8 == 0 and (i+1, j, x) not in seen:
            seen.add((i+1, j, x))
            heappush(heap, (d, i+1, j, a+[b+'S']))
        if j<W-1 and curr&1 == rotate(ar[i][j+1], x)&4 == 0 and (i, j+1, x) not in seen:
            seen.add((i, j+1, x))
            heappush(heap, (d, i, j+1, a+[b+'E']))
        if (i, j, x+1&3) not in seen:
            seen.add((i, j, x+1&3))
            heappush(heap, (d+1, i, j, p+['']))
####################
def maze_solver(ar):
    board = [list(row) for row in ar]
    paths = {}
    
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            if item == 'B':
                paths[(i,j)] = []
                board[i][j] = 0
            elif item == 'X':
                target = (i, j)
                board[i][j] = 0
        
    def update_paths(pos):
        paths[pos].append('')
        dir_mapping = {0:'N', 1:'W', 2:'S', 3:'E'}
        def rec_paths(pos):
            moves = [(pos[0]+dy, pos[1]+dx) for dx,dy in [(0,-1), (-1,0), (0,1), (1,0)]]
            for d,npos in enumerate(moves):
                y, x = npos[0], npos[1]
                if (npos not in paths
                   and 0 <= y < len(board) and 0 <= x < len(board[0])
                   and not(1<<(3-d) & board[pos[0]][pos[1]] or 1<<(1-d)%4 & board[y][x]) # check blocking for current and next cell
                   ):
                    paths[npos] = paths[pos][:-1]
                    paths[npos].append(paths[pos][-1] + dir_mapping[d])
                    rec_paths(npos)
        rec_paths(pos)
        
    def rotate_board():
        for i,row in enumerate(board):
            for j,item in enumerate(row):
                board[i][j] = item<<1 if item<8 else (item<<1 | 1)&15
    
    wait = 4
    while target not in paths and wait:
        curr = set(paths.keys())
        for pos in curr:
            update_paths(pos)
        rotate_board()
        if len(paths) != len(curr):
            wait = 4
        else:
            wait -= 1
    
    return paths.get(target, None)
        
########################
from collections import defaultdict, deque
import operator


def maze_solver(ar):
    """Returns a list of strings specifying the best path for the ball to travel from the initial position
    indicated by a 'B' in the given list of lists, ar, to the target position indicated by an 'X',
    with the remaining elements in ar indicating the initial configurations of the associated cells' walls.
    If there is no solution, the function returns None."""

    # - Roughly, there are two timescales of interest in this problem:
    #   - A fine timescale, where in each time step the ball may move one unit N, W, S, or E...
    #     In the associated graph, each edge will represent one such possible atomic movement,
    #     so two nodes will be adjacent iff one can move directly/immediately between the two corresponding cells.
    #   - A coarse timescale, where with each tick of the clock, each cell's walls rotate a quarter-turn clockwise.
    #     A coarse time step is what the problem statement calls an "interval".
    #     The ball's fine movements accumulate to produce coarse movements.
    #     In the associated graph, each edge will represent one coarse movement,
    #     with two nodes being adjacent iff the ball can start a coarse time step in the cell corresponding to one node
    #     and travel by fine steps during the coarse step to the reach the cell corresponding to the other node,
    #     where it will be at the beginning of the next coarse step.
    # - Since the maze's structure is 4-periodic on the coarse time scale,
    #   we think of ourselves as advancing cyclically from one "phase" to the next with each tick of the coarse clock:
    #   phase 0 -> 1 -> 2 -> 3 -> 0 -> 1 -> ...
    # - Each node in our graphs will be a (position, phase) pair.
    # - Connectivity/reachability in the fine graph will map to adjacency in the coarse graph.
    #   However, while adjacent nodes in the fine graph will have the same phase,
    #   each edge in the coarse graph would take us from one phase to the next.

    # Each numerical entry in ar indicates that the corresponding cell has
    # an East wall if its 0th (least significant) bit is 1,
    # a South wall if its 1st bit is 1, etc.
    bit_position_for_direction = {'E': 0, 'S': 1, 'W': 2, 'N': 3}

    def is_unwalled(row, column, direction, phase):
        """Returns True iff the cell at the specified position (row, column)
        has no wall in the specified direction during the specified phase;
        otherwise, returns False.
        This function checks the walls belonging to the specified cell, not the adjacent walls of its neighbours!"""
        cell_value = ar[row][column]
        # The initial ball cell and ultimate target cell are entirely unwalled.
        if cell_value == 'B' or cell_value == 'X':
            return True
        # Construct a bitmask with a 1 in the binary position associated with the initial direction
        # that would map in the desired phase to the desired direction,
        # and apply this mask to the value specifying the initial wall configuration of the cell of interest.
        initial_direction_bitmask = (1 << ((bit_position_for_direction[direction] - phase) % 4))
        return not (cell_value & initial_direction_bitmask)

    # We will traverse the given list of lists, ar, and extract the information we need.
    number_of_rows, number_of_columns = len(ar), len(ar[0])
    initial_position = target_position = None
    # This graph adjacency structure will map, for each phase,
    # each cell to those immediate neighbours (to the N, W, S, or E) from which it is not directly walled off.
    # More precisely, we map ((row, column), phase) to [(row_of_neighbour_1, column_of_neighbour_1), phase),
    #                                                   (row_of_neighbour_2, column_of_neighbour_2), phase),...].
    immediately_accessible_from = defaultdict(list)
    for row in range(number_of_rows):
        for column in range(number_of_columns):
            # We get the initial ball position and the ultimate target position.
            cell_value = ar[row][column]
            if cell_value == 'B':
                initial_position = (row, column)
            elif cell_value == 'X':
                target_position = (row, column)
            # Collect (undirected/bidirectional) fine/intra-interval adjacency information.
            for phase in range(4):
                if column < number_of_columns - 1:
                    if is_unwalled(row, column, 'E', phase) and is_unwalled(row, column + 1, 'W', phase):
                        immediately_accessible_from[((row, column), phase)].append(((row, column + 1), phase))
                        immediately_accessible_from[((row, column + 1), phase)].append(((row, column), phase))
                if row < number_of_rows - 1:
                    if is_unwalled(row, column, 'S', phase) and is_unwalled(row + 1, column, 'N', phase):
                        immediately_accessible_from[((row, column), phase)].append(((row + 1, column), phase))
                        immediately_accessible_from[((row + 1, column), phase)].append(((row, column), phase))

    def breadth_first_search(adjacent_to, start_node, target_predicate=None):
        """Starting at start_node, performs a breadth-first search of the graph whose
        adjacency information is specified by the dict adjacent_to.
        If a target_predicate function is specified,
        the search ends once we reach a node where target_predicate evaluates True-like,
        whereupon the sequence of nodes along the SHORTEST path from start_node to that target node is returned.
        If target_predicate is specified but no target is reached, the search was unsuccessful, so None is returned.
        If no (non-None) target_predicate is specified,
        the search continues until there are no reachable nodes left to visit,
        whereupon a container of all the nodes visited (i.e., all nodes in the connected component) is returned."""
        # We maintain a mapping of each visited node to its parent in the search tree.
        visited_from = {start_node: None}
        # We maintain a queue of nodes at the front/frontier/fringe of the search, from which we explore outward.
        frontier = deque([start_node])
        # Until we run out of nodes outward from which to continue the search...
        while frontier:
            # We dequeue a node from the frontier...
            node = frontier.popleft()
            # And for each not-yet-visited adjacent node...
            for next_node in adjacent_to[node]:
                if next_node not in visited_from:
                    # We mark it as visited, recording its search parent...
                    visited_from[next_node] = node
                    # Check whether we have reached our target...
                    if target_predicate is not None and target_predicate(next_node):
                        # In which case, we use our visited-node-to-parent mapping
                        # to trace in reverse the (shortest) path from start node to target node,
                        # then return the properly ordered sequence of nodes along that path...
                        backward_path = []
                        node_on_path = next_node
                        while node_on_path is not None:
                            backward_path.append(node_on_path)
                            node_on_path = visited_from[node_on_path]
                        return tuple(reversed(backward_path))
                    # If we did not reach a target, we enqueue the new node to the search frontier.
                    frontier.append(next_node)
        # If no (non-None) target_predicate was specified, we return the visited nodes.
        if target_predicate is None:
            return tuple(visited_from.keys())
        # If a target_predicate was specified but never satisfied, the search failed, so we return None.
        else:
            return None

    # In this adjacency structure for the coarse graph, we store the coordinates at which we may have the ball
    # at the beginning of a coarse interval/time step/phase, given the coordinates of the ball
    # at the beginning of (or actually anytime during) the previous coarse interval/time step/phase.
    # More precisely we map ((row, column), phase) to
    # [(row_of_reachable_cell_1, column_of_reachable_cell_1), next phase),
    #  (row_of_reachable_cell_2, column_of_reachable_cell_2), next phase),...].
    # What immediately_accessible_from is to fine adjacency
    # -- useful for traveling within a single coarse time step/interval/phase --
    # reachable_from will be to coarse adjacency
    # -- useful as we advance from phase to phase.
    # (The coarse graph does include self-loops,
    # allowing us to keep the ball still from one coarse time interval to the next.)
    # (This whole implementation could be gently rewritten so that adjacency information would be stored
    # not in a dict with ((row, column), phase) keys, but instead, say,
    # in a list of lists of lists indexed by row, column, and phase.)
    reachable_from = {}
    for phase in range(4):
        # Effectively, for each phase, we partition the entire grid into sets of connected/reachable cells.
        # We maintain a pool of nodes that have not yet been assigned to such a connected component.
        nodes_left_to_visit = {((row, column), phase)
                               for row in range(number_of_rows) for column in range(number_of_columns)}
        # Until there are no nodes left in the pool, we draw one to seed a new connected component,
        # setting it as the root/start node of a breadth-first traversal with no target.
        # (A depth-first traversal, for instance, would also work here.)
        # The nodes visited in the traversal make up a complete connected component.
        # Within a coarse time step/interval, we can move the ball from any cell in the connected component
        # to any cell in the connected component,
        # placing us there for the beginning of the next coarse time step/interval;
        # we build on our reachable_from mapping accordingly.
        while nodes_left_to_visit:
            seed_node = nodes_left_to_visit.pop()
            connected_nodes = breadth_first_search(immediately_accessible_from, seed_node)
            nodes_left_to_visit.difference_update(connected_nodes)
            reachable_nodes = [(position, (phase + 1) % 4) for position, _ in connected_nodes]
            for node in connected_nodes:
                reachable_from[node] = reachable_nodes

    # Via a breadth-first search in our coarse (inter-interval) transition graph,
    # we find the/a shortest possible sequence of start-of-interval ball positions
    # that takes us from the given initial ball position in phase 0 
    # to the given ultimate target position (in any phase).
    coarse_path = breadth_first_search(reachable_from, (initial_position, 0), lambda node: node[0] == target_position)

    # If there is no path, we return None.
    if coarse_path is None:
        return None

    # We prepare a mapping from cardinal (row, column) direction vectors to representative characters.
    direction_char_for_tuple = {(+1, 0): 'S', (-1, 0): 'N', (0, +1): 'E', (0, -1): 'W'}
    # We will here assemble our overall list of directions.
    full_path_specification = []
    # We go through the steps in our coarse, inter-interval path...
    coarse_path_iter = iter(coarse_path)
    fine_path_start_node = next(coarse_path_iter)
    for fine_path_end_node in coarse_path_iter:
        # When the ball should not be moved during a particular coarse interval,
        # we put an empty string in our list of directions...
        if fine_path_start_node[0] == fine_path_end_node[0]:
            full_path_specification.append('')
        # Otherwise, we perform a breadth-first search in our fine transition graph to get a sequence of ball positions
        # that accomplishes the present coarse movement (in the present coarse interval) via fine/unit/atomic steps.
        # (Using breadth-first search, we find the/a shortest possible fine/intra-interval path,
        # but this is not required, so depth-first search, for instance, would also work.)
        else:
            fine_path = breadth_first_search(immediately_accessible_from, fine_path_start_node,
                                             lambda node: node[0] == fine_path_end_node[0])
            # We represent the direction of each step in our fine, intra-interval path by the appropriate character,
            # and put the resulting string in our overall list of directions.
            fine_path_directions = []
            fine_path_iter = iter(fine_path)
            fine_step_start_node = next(fine_path_iter)
            for fine_step_end_node in fine_path_iter:
                fine_path_directions.append(
                    direction_char_for_tuple[tuple(map(operator.sub, fine_step_end_node[0], fine_step_start_node[0]))])
                fine_step_start_node = fine_step_end_node
            full_path_specification.append(''.join(fine_path_directions))
        fine_path_start_node = fine_path_end_node
    # All done!  We now return our complete list of directions.
    return full_path_specification
######################################################################################
class cell:
    it = 0
    def __init__(self,x = 0, y = 0, val = 0):
        self.x = x
        self.y = y
        self.val = val
    
    @property
    def walls(self):
        origin = '000' + str(bin(self.val)).replace('0b','')
        origin = origin[::-1][0:4][::-1]
        return origin[cell.it%4:] + origin[:cell.it%4]


def maze_solver(ar):
    print(ar)
    maz = []
    state = []
    s = [0,0]
    f = [0,0]
    for i,row in enumerate(ar):
        maz += [[]]
        state += [[]]
        for j,col in enumerate(row):
            maz[i] += [cell()]
            state[i] += [[]]
            if col == 'B':
                s[0] = i
                s[1] = j
                maz[i][j].x = i
                maz[i][j].y = j
            elif col == 'X':
                f[0] = i
                f[1] = j
                maz[i][j].x = i
                maz[i][j].y = j
            else:
                maz[i][j].val = col
                maz[i][j].x = i
                maz[i][j].y = j
    q = []
    q_path = []
    q.append(maz[s[0]][s[1]])
    q_path.append([])
    state[s[0]][s[1]].append(0)
    while(q):
        now = q.pop(0)
        qpath = q_path.pop(0)
#         print([qpath,now.x,now.y])
        cell.it = len(qpath)
        for prox,proy,mv in possible(maz,now):
#             print([pro.x,pro.y,mv])
            if mv is '':
                if len(qpath) >= 2:
                    if mv is qpath[-1] and mv is qpath[-2]:
                        continue
            if (len(qpath)+1)%4 in state[prox][proy]:
                continue
            npath = qpath + [mv]
            q.append(maz[prox][proy])
            q_path.append(npath)
            state[prox][proy].append(len(npath)%4)
#             print(npath)
            if prox is f[0] and proy is f[1]:
                return npath
        
    return None

def possible(maz,now):
    n,m = len(maz),len(maz[0])
    rel = []
    rel.append([now.x,now.y,''])
    path = ''
    stack = []
    cell_set = set()
    path_stack = []
    xx =[1,0,0,-1]                  
    yy =[0,1,-1,0]
    mm =['S','E','W','N']
    stack.append(maz[now.x][now.y])
    cell_set.add(maz[now.x][now.y])
    path_stack.append(path)
    while(stack):
        now_saw = stack.pop()
        path = path_stack.pop()
        for i in range(4):
            if now_saw.x + xx[i] < 0 or now_saw.x + xx[i] >= n or now_saw.y + yy[i] < 0 or now_saw.y + yy[i] >= m:
                continue
            new = maz[now_saw.x + xx[i]][now_saw.y + yy[i]]
            if i == 0:
                if now_saw.walls[2] is '1' or new.walls[0] is '1':
                    continue
            elif i == 1:
                if now_saw.walls[3] is '1' or new.walls[1] is '1':
                    continue
            elif i == 2:
                if now_saw.walls[1] is '1' or new.walls[3] is '1':
                    continue
            else:
                if now_saw.walls[0] is '1' or new.walls[2] is '1':
                    continue
            if new not in cell_set:
                new_path = path + mm[i]
                stack.append(now_saw)
                stack.append(new)
                cell_set.add(new)
                path_stack.append(path)
                path_stack.append(new_path)
                rel.append([new.x,new.y,new_path])
    return rel
#################################################
def maze_solver(ar):
    current = 0
    x_limit = len(ar)
    y_limit = len(ar[0])
    all_player = set()
    class Player:
        def __init__(self, x, y, answer):
            self.x = x
            self.y = y
            self.answer = answer
            all_player.add(self)

        def move(self):
            pos = "NESW"
            moves = [(self.x - 1, self.y),  # Nort
                     (self.x, self.y + 1),  # East
                     (self.x + 1, self.y),  # South
                     (self.x, self.y - 1)]  # West
            for position,move in enumerate(moves):
                x,y = move
                if 0 <= x < x_limit and 0 <= y < y_limit and data[x][y].is_joinable((self.x, self.y)):
                    if data[self.x][self.y].can_joinable_without_join((x,y)):
                        data[x][y].joinable = False
                        player = (Player(x,y,self.answer + pos[position]))
                        if player.is_answer():return player
                        all_player.add(player)

        def is_answer(self):
            if (self.x, self.y) == fnish:
                return True

    class Wall:
        def __init__(self, num, x, y):
            b_num = format(num, "b")
            self.x = x
            self.y = y
            self.wall1 = "0" * (4 - len(b_num)) + b_num
            self.wall2 = self.wall1[1:] + self.wall1[0]
            self.wall3 = self.wall2[1:] + self.wall2[0]
            self.wall4 = self.wall3[1:] + self.wall3[0]
            self.wall1_joins = self._which_coor_can_join(self.wall1)
            self.wall2_joins = self._which_coor_can_join(self.wall2)
            self.wall3_joins = self._which_coor_can_join(self.wall3)
            self.wall4_joins = self._which_coor_can_join(self.wall4)
            self.joinable = True

        def _which_coor_can_join(self, num):
            num1, num2, num3, num4 = num
            data = set()
            if num1 == "0": data.add((self.x - 1, self.y))  # Nort tan girmek için
            if num2 == "0": data.add((self.x, self.y - 1))  # Westten girmek için
            if num3 == "0": data.add((self.x + 1, self.y))  # Southtan girmek için
            if num4 == "0": data.add((self.x, self.y + 1))  # Eastten girmek için
            return data

        def do_not_joinable(self):
            self.joinable = False

        def is_joinable(self, other_coor):
            # DO buraya ayn ıyer ekoymayıda ekle
            if self.joinable:
                if current == 0 and other_coor in self.wall1_joins:
                    return True
                elif current == 1 and other_coor in self.wall2_joins:
                    return True
                elif current == 2 and other_coor in self.wall3_joins:
                    return True
                elif current == 3 and other_coor in self.wall4_joins:
                    return True

        def can_joinable_without_join(self, other_coor):
            if current == 0 and other_coor in self.wall1_joins:
                return True
            elif current == 1 and other_coor in self.wall2_joins:
                return True
            elif current == 2 and other_coor in self.wall3_joins:
                return True
            elif current == 3 and other_coor in self.wall4_joins:
                return True

    data = [[y for y in x] for x in ar]
    start,fnish = (0,0), (0,0)
    for x, part in enumerate(ar):
        for y, element in enumerate(part):
            if type(element) == int:
                data[x][y] = Wall(element, x, y)
            elif element == "B":
                data[x][y] = Wall(0, x, y)
                start = (x,y)
            elif element =="X":
                data[x][y] = Wall(0, x, y)
                fnish = (x,y)
    def change_wall():
        nonlocal current
        current += 1
        if current == 4:
            current = 0
        for x in fake_player:
            x.answer = x.answer + ","

    Player(start[0],start[1],"")
    fake_player = set()
    fake_player.add(all_player.pop())
    t = 0
    while True:
        check = len(fake_player)
        for x in fake_player:
            result = x.move()
            if result:return result.answer.split(",")
        fake_player = all_player | fake_player
        if check == len(fake_player):
            t += 1
            change_wall()
            if t == 4:return
        else:
            t = 0
        all_player = set()
#############################################################
def maze_solver(ar):
    current = 0
    x_limit = len(ar)
    y_limit = len(ar[0])
    all_player = set()
    class Player:
        def __init__(self, x, y, answer):
            self.x = x
            self.y = y
            self.answer = answer
            all_player.add(self)

        def move(self):
            pos = "NESW"
            moves = [(self.x - 1, self.y),  # Nort
                     (self.x, self.y + 1),  # East
                     (self.x + 1, self.y),  # South
                     (self.x, self.y - 1)]  # West
            for position,move in enumerate(moves):
                x,y = move
                if 0 <= x < x_limit and 0 <= y < y_limit and data[x][y].is_joinable((self.x, self.y)):
                    if data[self.x][self.y].can_joinable_without_join((x,y)):
                        data[x][y].joinable = False
                        player = (Player(x,y,self.answer + pos[position]))
                        if player.is_answer():return player
                        all_player.add(player)

        def is_answer(self):
            if (self.x, self.y) == fnish:
                return True

    class Wall:
        def __init__(self, num, x, y):
            b_num = format(num, "b")
            self.x = x
            self.y = y
            self.wall1 = "0" * (4 - len(b_num)) + b_num
            self.wall2 = self.wall1[1:] + self.wall1[0]
            self.wall3 = self.wall2[1:] + self.wall2[0]
            self.wall4 = self.wall3[1:] + self.wall3[0]
            self.wall1_joins = self._which_coor_can_join(self.wall1)
            self.wall2_joins = self._which_coor_can_join(self.wall2)
            self.wall3_joins = self._which_coor_can_join(self.wall3)
            self.wall4_joins = self._which_coor_can_join(self.wall4)
            self.joinable = True

        def _which_coor_can_join(self, num):
            num1, num2, num3, num4 = num
            data = set()
            if num1 == "0": data.add((self.x - 1, self.y))  # Nort tan girmek için
            if num2 == "0": data.add((self.x, self.y - 1))  # Westten girmek için
            if num3 == "0": data.add((self.x + 1, self.y))  # Southtan girmek için
            if num4 == "0": data.add((self.x, self.y + 1))  # Eastten girmek için
            return data

        def do_not_joinable(self):
            self.joinable = False

        def is_joinable(self, other_coor):
            # DO buraya ayn ıyer ekoymayıda ekle
            if self.joinable:
                if current == 0 and other_coor in self.wall1_joins:
                    return True
                elif current == 1 and other_coor in self.wall2_joins:
                    return True
                elif current == 2 and other_coor in self.wall3_joins:
                    return True
                elif current == 3 and other_coor in self.wall4_joins:
                    return True

        def can_joinable_without_join(self, other_coor):
            if current == 0 and other_coor in self.wall1_joins:
                return True
            elif current == 1 and other_coor in self.wall2_joins:
                return True
            elif current == 2 and other_coor in self.wall3_joins:
                return True
            elif current == 3 and other_coor in self.wall4_joins:
                return True

    data = [[y for y in x] for x in ar]
    start,fnish = (0,0), (0,0)
    for x, part in enumerate(ar):
        for y, element in enumerate(part):
            if type(element) == int:
                data[x][y] = Wall(element, x, y)
            elif element == "B":
                data[x][y] = Wall(0, x, y)
                start = (x,y)
            elif element =="X":
                data[x][y] = Wall(0, x, y)
                fnish = (x,y)
    def change_wall():
        nonlocal current
        current += 1
        if current == 4:
            current = 0
        for x in fake_player:
            x.answer = x.answer + ","

    Player(start[0],start[1],"")
    fake_player = set()
    fake_player.add(all_player.pop())
    for _ in range(1000):
        check = len(fake_player)
        for x in fake_player:
            result = x.move()
            if result:return result.answer.split(",")
        fake_player = all_player | fake_player
        if check == len(fake_player):
            change_wall()
        all_player = set()
