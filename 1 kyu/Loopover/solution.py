5c1d796370fee68b1e000611


def transpose(my_board): #transposes the board.
    return list(map(list, zip(*my_board)))

def trns_sol(sol): #transforms a solution found using the transposed board.
    return [str.replace('U','l').replace('D','r').replace('R','D').replace('L','U').replace('r','R').replace('l','L') for str in sol] if sol else None

def change(my_board, my_moves): #applies the moves given to the board.
    moves = my_moves.copy()
    move = moves.pop(0)
    if move[0]=='R':
        row = my_board[int(move[1])]
        row.insert(0,row.pop(len(row)-1))
    elif move[0]=='L':
        row = my_board[int(move[1])]
        row.insert(len(row),row.pop(0))
    elif move[0]=='U':
        my_board = transpose(change(transpose(my_board), [move.replace('U', 'L')]))
    else:
        my_board = transpose(change(transpose(my_board), [move.replace('D', 'R')]))
    if moves!=[]: my_board = change(my_board, moves)
    return my_board

def final_swap(rows, columns): #when only two final cells should be swapped without affecting the rest of the board.
    if columns==2: 
        return ['R'+str(rows-1)]
    else:
        return (['U'+str(columns-1), 'R'+str(rows-1)] + ['U'+str(i) for i in range(1, columns-1)] + ['R'+str(rows-1)] + ['D'+str(i) for i in range(1, columns)] + ['L'+str(rows-1)])*(columns-1)

def swap_adj(coord): #it swaps the given cell with the one to the right, but it also swaps the similar cells at the previous row. 
    return ['U'+str(coord[1]), 'U'+str(coord[1]+1), 'R'+str(coord[0]-1), 'D'+str(coord[1]+1), 'L'+str(coord[0]-1), 'L'+str(coord[0]-1), 'D'+str(coord[1]), 'R'+str(coord[0]-1)]

def three_slip(coord): #given the coordinates of a cell in the table, moves it two places to the right. (for example given A, changes ABC to BCA without affecting the rest of the table.)
    return ['U'+str(coord[1]), 'U'+str(coord[1]+1), 'U'+str(coord[1]+2), 'R'+str(coord[0]-1), 'D'+str(coord[1]+1), 'D'+str(coord[1]+2)] + ['L'+str(coord[0]-1)]*3 + ['D'+str(coord[1])]+['R'+str(coord[0]-1)]*2 + swap_adj([coord[0],coord[1]+1]) + swap_adj(coord)


def loopover(mixed_up_board, solved_board):
    
    if mixed_up_board==solved_board: return []
    my_board = mixed_up_board.copy()
    rows = len(solved_board)
    columns = len(solved_board[0])
    done = False
    
    #if there is an even dimension, let it be the columns.
    if columns%2!=0 and rows%2==0:  
        return trns_sol(loopover(transpose(mixed_up_board), transpose(solved_board)))
    
    #find the first place that the cell is misplaced.
    row = 0
    column = 0
    while solved_board[row][column]==mixed_up_board[row][column]:
        if column<columns-1: 
            column+=1
        else:
            column = 0
            row += 1
    
    #find the misplaced cell.
    mixed_row = row
    mixed_column = column
    while solved_board[row][column]!=mixed_up_board[mixed_row][mixed_column]:
        if mixed_column<columns-1: 
            mixed_column+=1
        else:
            mixed_column = 0
            mixed_row += 1
            
    #based on the positions decide what move to make or if this board is unsolvable.
    if row==rows-1 and column==columns-2: 
        if columns%2==1: 
            return None
        else:
            my_move = final_swap(rows, columns)
    elif row==mixed_row:
        if row!=rows-1:
            my_move = ['D'+str(mixed_column), 'L'+str(mixed_row+1), 'U'+str(mixed_column)]
        elif column==0:
            my_move = ['L'+str(mixed_row)]*mixed_column
        else:
            my_move = three_slip([row, max(column, mixed_column-2)])   
    elif column==mixed_column:
        my_move = ['R'+str(mixed_row)]
    else:
        my_move = ['D'+str(column)]*(mixed_row-row) + ['R'+str(mixed_row) if mixed_column<column else 'L'+str(mixed_row)]*abs(mixed_column-column) + ['U'+str(column)]*(mixed_row-row)

    #apply this move, get the rest of the solution and return it.
    my_board = change(my_board, my_move)
    rest_of_solution = loopover(my_board, solved_board)
    return my_move + rest_of_solution if rest_of_solution!=None else None

###########################
import numpy as np
Kata=True
VERBOSE=False

from itertools import combinations
### This line gives number of inversions
inv = lambda w:sum([w[i]>w[j] for i,j in combinations(range(len(w)),2)])

class Board( ):

    def __init__(self,mixed_up_board,target_board):
        self.loadMixed(mixed_up_board)
        self.loadTarget(target_board)
        self.NRows,self.NColms=self.bd.shape ## rows and colmns of board
        self.soln=[]
        self.trans=False ## tells us if grids transposed or not

    def setTrans(self,k:bool): # k determines if matrices in transposed state or not
        self.bd=self.bd.T
        self.target=self.target.T
        self.NRows,self.NColms=self.NColms,self.NRows
        self.trans=k
        
    def flip(self):
        self.trans^=True
        self.bd=self.bd.T
        self.target=self.target.T
        self.NRows,self.NColms=self.NColms,self.NRows
        
    def loadMixed(self,s):
        ## load from a new line punctuated string
        if Kata:
            print(type(s),s)
            self.bd=np.array(s)
        else:
            self.bd=np.array([list(k) for k in s.split("\n")])

    def loadTarget(self,s):
        if Kata:
            self.target=np.array(s)
        else:
            self.target=np.array([list(k) for k in s.split("\n")])

    def puzzleComplete(self):
        return np.all(self.bd==self.target)

    def HSpin(self,row,amt):
        # amt>0 move to right
        # amt<0 move to left
        # amt==0 nothing to do
        if amt==0:
            return
        self.bd[row,:]=np.roll(self.bd[row,:],amt)

        if amt>=0:
            if not self.trans:
                self.soln.extend(["R"+str(row)]*amt)
            else:
                self.soln.extend(["D"+str(row)]*amt)
        else:
            if not self.trans:
                self.soln.extend(["L"+str(row)]*-amt)
            else:
                self.soln.extend(["U"+str(row)]*-amt)

    def VSpin(self,colm,amt):
        if amt==0: return
        self.bd[:,colm]=np.roll(self.bd[:,colm],amt)
        if amt>=0:
            if not self.trans:
                self.soln.extend(["D"+str(colm)]*amt)
            else:
                self.soln.extend(["R"+str(colm)]*amt)
        else:
            if not self.trans:
                self.soln.extend(["U"+str(colm)]*-amt)
            else:
                self.soln.extend(["L"+str(colm)]*-amt)

    def locate(self,value):
        try:
            r,c=np.where(self.bd==value)
        except:
            print(value,"Error")
        return (r,c)

def loc(Arr,start,key):
    for i in Arr[start:]:
        return (i,i.index(key)) # found on row i @ position i.index(key)

def loopover(mixed_up_board, solved_board):
    game=Board(mixed_up_board,solved_board)

    def stageOne():
        ## step 1 solve the first row
        for i in range(N): ## very first row like Miss Lawson
            for j in range(N):
                curr=game.target[0,j]
                if curr=='E':
                    po=2
                r,c=map(int,game.locate(curr))
                if r==0 and c==j:
                    continue
                if r==0:
                    game.VSpin(j,1) ## down 1
                if c!=j or r>0:
                    game.HSpin(r,j-c)
                    game.VSpin(j,-r) ## up 1

    N,M=game.NColms,game.NRows
    stageOne()
    ## step 2 solve the central block vis b[1:-1,1:-1]

    def stageTwo():
        """ solve the central block"""
        """Put rows from 1..M-2  and columns 0..N-2 in correct order -- This is the central left block"""
 
        for row in range(1,M): # 1<=row<=N-2   ie inner layer of cells was N-1

            if row==N-1:
                kkk=45
            pos=N-2 # place correct tiles starting @ colm N-2 (1 in from rightmost colm)
            #print("placing @ colm %d on row %d "%(pos,row))
            while pos>=0: ## assemble in correct order  ####was -1
                r,c=map(int,game.locate(game.target[row,N-2-pos]))
                if r==row and c==N-1:
                    pos-=1
                    game.HSpin(row,-1)
                    continue
                if r==row: ## special case, target found in row
                    if pos==N-2:
                        game.HSpin(row,N-c-1)
                    else:
                        game.HSpin(row,N-1-c)
                        game.VSpin(N-1,1)
                        game.HSpin(row,-N+1+c)
                        game.VSpin(N-1,-1)
                else:
                    # case of next value in r > row
                    game.HSpin(r,N-c-1) # element now in edge column ### want +ve roll
                    game.VSpin(N-1,row-r)
                game.HSpin(row,-1)
                pos-=1

    stageTwo()
    ## step 3 iterative solve the final row then final colm until puzzle
    ## solved or we keep cycling
    ## This time we focus on rightmost column and bottom row which
    ## we keep iteratively solve until either we are cycling or a solution has
    ## been found
    mode='None'
    def check(ls):
        if ls==['P','Q','R']:
            sss=9
        if game.target[-1,0] in ls:
            z=ls*2
            try:
                ix=z.index(game.target[-1,0])
            except:
                return -1

            if ix==None:
                return False
            if z[ix:ix+N]==list(game.target[-1,:]):
                return ix
        return -1
    def ccycle(game,N,mode='Trans'):
        game.flip()
        N=game.NColms
        M=game.NRows

        pos=N-2 ## We are working last row of game.bd
        row=M-1
        r=check(list(game.bd[-1,:]))
        if r!= None and r>0:
            game.HSpin(M-1,-r)
            return
        if np.all(game.bd[-1,:]==game.target[-1,:]):
            return
        while pos>=0:
            nextLetter=game.target[row,N-2-pos] ## pos+2
            if nextLetter=='T':
                hdhdh=78

            r,c=game.locate(nextLetter)
            r,c=r[0],c[0]
            if r==M-1 and c==N-1:
                #assert N-1-c==0, "errors young Naseeras, boobs not showing"
                #game.HSpin(M-1,N-1-c)
                game.HSpin(M-1,-1)
                pos-=1
                continue
            if game.bd[M-1,N-1]==nextLetter:
                bbbb=0
                pass
            elif r==M-1:
                if pos==N-2:
                    game.HSpin(M-1,N-1-c)
                    pos-=1
                    continue
                ## move nextLetter to corner cell-> b cells
                b=N-1-c
                assert b>=0 , " b error"
                game.HSpin(M-1,b)
                ## Now move it up 1

                game.VSpin(N-1,1)
                ## move row back b cells
                game.HSpin(M-1,-b)
                ## move nextLetter down to corner cell
                game.VSpin(N-1,-1)
            else:
                ## move nextLetter down to corner cell
                game.VSpin(N-1,M-1-r)
            ## move last row back one
            if pos>-1:
                game.HSpin(M-1,-1)
            pos-=1
        hhh=0
    ## end of ccycle

    mode='Trans'
    hash={}
    game.flip() # alternately solve bottom and right hand edges
    while True:
        ccycle(game,N,mode)
        mode='Trans' if mode=='None' else 'None'

        if np.all(game.bd==game.target):
            if game.trans:## because Transpose flip back to original formation
                game.flip()
            print("Solution Found")
            print(game.bd)
            return game.soln

        if (tuple(game.bd[-1,:]),tuple(game.bd[:,-1])) in hash:
            print("No Solution")
            if game.NRows*game.NColms%2==0:
                ### actually possible
                ## perturb bottom row
                game.HSpin(M-1,1)
                game.VSpin(N//2-1,-1)
                game.HSpin(M-2,-1)
                game.VSpin(N//2-2,-1)
                stageOne()
                stageTwo()
                continue

            return None
        if game.trans:
            hash[(tuple(game.bd[:,-1]),tuple(game.bd[-1,:]))]=1
        else:
            hash[(tuple(game.bd[-1,:]),tuple(game.bd[:,-1]))]=1


#######################################
from collections import deque
from itertools import cycle
from functools import wraps


class Node:
    current = dict()
    target = dict()  # target coordinates value: (row, col)

    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __repr__(self):
        return str(self.value)
    
    
class Row(list):
    direct = ('L', 'R')

    def __init__(self, iterable, ind, context=None):
        """
        :param iterable: an ordered collection of Node instances
        :param ind: row index
        :param context: obj; reference to an obj with attribute obj.solution.
        """
        super(Row, self).__init__(iterable)
        self.queue = deque(maxlen=len(iterable))
        self.ind = str(ind)

        if context is not None:
            self.context = context

    def shift(self, direction):
        """
        :param direction: integer. value of integer indicates the number of
        repeated shifts. the sign indicates a left(-) or right(+) shift,
        :return None, but extends the the context object's solution by the appropriate shift(s)
        (e.g. direction = -2, ind=0 ['L0, 'L0'])
        """
        # overwrites at each step the queue, since a shift in orthogonal direction
        # does not change queue
        self.queue.extend([node.value for node in self])
        self.queue.rotate(direction)
        for node, v in zip(self, self.queue):
            node.value = v
            Node.current[v] = node.position  # still efficient as merely pointer
            # to immutable tuple is shared (no new tuple is created)

        # parse the direction literal(s) and append to solution
        self.context.solution.extend([self.direct[direction > 0] + self.ind] * abs(direction))

    def shortest_shiftLR(self, j, c):
        """
        :param j: current position in Row
        :param c: target position in Row
        :returns minimal shifting length given this rows length: negative values
        indicate a "left", positive indicate "right" shift.
        """
        # [leftdistance, rightdistance]
        return min([-((len(self) - (c - j)) % len(self)), (len(self) + c - j) % len(self)], key=abs)

    def toList(self):
        """:return the list of the nodes' values rather then the list of nodes"""
        return [node.value for node in self]


class Column(Row):
    direct = ('D', 'U')

    def __init__(self, iterable, ind, context=None):
        """
        :param iterable: ordered collection of Node instances. ordering is bottom to top,
        such that D shift corresponds to L in Row (and U to R)
        :param ind: column index
        :param context"""
        Row.__init__(self, iterable, ind, context)


class StrategyLiftshift:
    def executeStrategy(board):
        for value in [val for row in reversed(board.solved_board[1:]) for val in reversed(row)]:
            StrategyLiftshift.liftshift(board, value)

    def liftshift(board, value):
        """first stage solving algorithm, solves all but the first row, with three
        minor algorithms, depending on the respective position to the target
        :param value: str. letter, that is to be moved to its target position."""
        i, j = Node.current[value]
        r, c = Node.target[value]

        # (0) correct row & column
        if (i, j) == (r, c):
            return None

        # (1) correct row
        if i == r and j != c:
            board.cols[j].shift(1)
            board.cols[c].shift(1)
            board.rows[r - 1].shift(board.rows[r - 1].shortest_shiftLR(j, c))
            board.cols[j].shift(-1)
            board.cols[c].shift(-1)

        # (2) correct column
        elif j == c and i != r:
            board.rows[i].shift(-1)
            board.cols[c].shift(-(i - r))  # lift up # CONSIDER: Room for improvment: cols[c].shortest_shiftLR(i, r)
            board.rows[i].shift(1)
            board.cols[c].shift(i - r)  # lift down  # CONSIDER: Room for improvment: cols[c].shortest_shiftLR(r, i)

        # (3) neither
        else:
            board.cols[c].shift(-(i - r))
            board.rows[i].shift(board.rows[i].shortest_shiftLR(j, c))
            board.cols[c].shift(i - r)


class StrategyToprow:
    def executeStrategy(board):
        """This strategy solves the toprow of the board, by analysing the
        possible sortings (sorting graphs) and choosing a short """

        graphs = StrategyToprow.find_sort_graphs(
            row=board.rows[0],
            target_row=board.solved_board[0])
        sortgraphs = StrategyToprow.choose_sort_strategy(graphs, target_row=board.solved_board[0])

        if sortgraphs is not None:
            for g in sortgraphs:
                StrategyToprow.sort_by_subgraph(board, subgraph=g)

            _, t = Node.current[board.solved_board[0][0]]
            board.rows[0].shift(board.rows[0].shortest_shiftLR(t, 0))

    # (Preprocessing of available strategies) ----------------------------------
    @staticmethod
    def find_sort_graphs(row, target_row):
        """
        This function looks at the unique cyclic permutations of row
        and compares each of them against the target row. Given the current
        permutation it determines where each of the Letters in row need to move
        (the position of row's permutation occupant)

        e.g. permutation of row = ['C', 'A', 'B'], target_row = ['A', 'B', 'C']
        C --> B, B --> A,  A --> C (letter C needs to move to B's current position, ...)
        so this permutation has the sort graph {C: B, B: A, A: C}

        :param row: Row object.
        :param target_row: List.
        :return: list of dicts.
        """
        # find the unique cyclic permutations of row. using cycle avoids unnecessary
        # appends to the solution + no dependency to Cyclic_shift_board
        cycs = cycle(row.toList())
        rotations = list()
        for i in range(len(row)):
            rotations.append([next(cycs) for i in range(len(row))])
            next(cycs)

        # find the graph of sortings (e.g. A --> C, C --> B, B --> A)
        graphs = list()
        for rot in rotations:
            # finding the misplaced letters and their target position's current occupant
            graphs.append({x: y for x, y in zip(target_row, rot) if x != y})

        return graphs

    @staticmethod
    def split_subgraphs(graph):
        """
        :param graph: dict, directed and linear (cyclic) graph(s); a graph
        may contain multiple closed subgraphs: {'A': 'D', 'C': 'E', 'D': 'A', 'E': 'C'}
        :return: list of dict, which is a list of the closed subgraphs.
        """
        graph = graph.copy()
        start, target = graph.popitem()

        subgraphs = list()
        subg = {start: target}

        while len(graph) > 0:  # for i in range(len(graph)):
            if target in graph.keys():
                start = target
                target = graph.pop(start)

                subg.update({start: target})

            if target in subg.keys():  # closed the circle (subgraph)
                subgraphs.append(subg)

                if len(graph) > 0:
                    start, target = graph.popitem()
                    subg = {start: target}

        return subgraphs

    @staticmethod
    def choose_sort_strategy(graphs, target_row):
        """
        Viable solutions are those that produce an even number of steps in total.
        Since sort_by_subgraph algorithm uses len(subgraph) + 1 steps, the following solutions
        work:

            1) a single closed graphs of uneven length: e.g. {'B': 'C', 'C': 'D', 'D': 'B'}.
               The total number of steps is 4 and even, which puts the wildcard
               (see sort_by_subgraph doc for details) in its correct place after
               the execution of the graph.

            2) multiple closed subgraphs, if
                a) they produce an even number of steps in total and the first
                    overall move and the last overall move cancel.
                b) the total number of steps is uneven and the length of the row
                    is even. e.g.: [{'E': 'D', 'D': 'B', 'B': 'E'}, {'C': 'A', 'A': 'C'}]
                    with row = [C, E, A, B, D, F]
                    (remember: each subgraph requires len(subgraph)+1 steps)
                    In this case, the entire row can be rearanged
                    {A:B, B:C, C:D, D:A}, adding an uneven number of steps
                    --> returns to case 2a)

        if there is no graph (or collection of subgraphs), that can create
        an even number of steps (e.g. 2b) but with no

        :param graphs: list of dicts. [{A:B B:A}, {A:C, C:B: B:A}]
        :param target_row: list. target format
        :return:
            list of dict(s). describes an entire graph (can be composed of
            closed subgraphs), which is a valid strategy.
            None. if there is no valid strategy

        """
        # prefers strategies, whose total number of steps is even and prefers overall shorter strategies.
        # sorted(graphs, key=lambda x: (len(x) % 2 == 0, len(x))) # not applicable
        for g in sorted(graphs, key=len):
            subgraphs = StrategyToprow.split_subgraphs(g)
            # print(subgraphs, sum([len(s) + 1 for s in subgraphs]))

            # simple solution even number of steps across subgraph(s)
            if sum([len(s) + 1 for s in subgraphs]) % 2 == 0:
                # even number of total steps, immediate solution; execute all subgraphs
                # (len(s) +1: since the initialisation step requires an additional turn)
                return subgraphs

            # uneven number of total steps across multiple subgraphs, but! rowlen is even
            # - adds uneven no of steps
            elif len(target_row) % 2 == 0:
                # do a total turnover afterwards (A->B B->C C->D D->A),
                # to even the total number of steps.
                turnover = {s: t for s, t in zip(target_row, target_row[1:])}
                turnover.update({target_row[-1]: target_row[0]})
                subgraphs.append(turnover)
                return subgraphs

        else:
            return None

    def sort_by_subgraph(board, subgraph):
        """
        Execute the subgraph strategy:
        e.g. subgraph {'A': 'B', 'B': 'D', 'D': 'E', 'E': 'A'}
        1) initialise the algorithm (two column moves):
            shift A to the leftmost position (0,0) and push it up -
            so a wildcard lies on A's old position now. shift B (A's target)
            to 0,0. push A down on B's position. B is the new start

        2) shift D to the leftmost and push B up on D's position.
        shift E (D's Target) to the leftmost and push D down on E's position
        shift the Wildcard (occupies A's space and is E's target) to the leftmost.
        push E up on the wildcard's position.

        Notice how the order of up and down is interchangeable! (we could start
        the algorithm with down.

        The total number of steps is 5 (uneven), Because the initialisation took
        two steps and each following sorting a single step. The subgraph is
        length 4 (even), so the no. of steps is, uneven. As consequence, the
        wildcard in this example is misplaced after execution.
        StrategyToprow.choose_sort_strategy wisely! ;)

        # Consecutive calls to sort_subgraph:
        e.g. the two subgraphs [{'A': 'D', 'D': 'A'}, {'C': 'E', 'E': 'C'}]
        are executed. {'A': 'D', 'D': 'A'} causes u, d, u. To ensure, that the
        wildcard is pushed down (if it was pushed up in the first subgraph's first move)
        in the last subgraph's last step (and thereby placed correctly!),
        the second subgraph must start with d (second subgraph executes d, u, d).
        This is accounted for by looking at the board.solution's last execution.

        :param subgraph: dict. a closed subgraph e.g. {A: B, B: A}
        :return: None: changes the state of board
        """
        if len(board.solution) > 1 and 'U0' == board.solution[-1]:  # check if last switch of first column was up
            i, first_move = 1, -1
        else:
            i, first_move = 0, 1

        # initalisation step: first position in graph
        start, target = subgraph.popitem()
        _, s = Node.current[start]
        board.rows[0].shift(board.rows[0].shortest_shiftLR(s, 0))
        board.cols[0].shift(first_move)  # by convention

        # update graph: (with wildcard, it is no longer a circle)
        wild_occupies = start
        wildcard = board.rows[0][0].value
        for k, v in subgraph.items():
            if v == wild_occupies:
                subgraph[k] = wildcard
                break

        while start != target:
            _, t = Node.current[target]
            board.rows[0].shift(board.rows[0].shortest_shiftLR(t, 0))
            board.cols[0].shift([-1, 1][i % 2])

            start = target
            i += 1
            if len(subgraph) > 0:
                target = subgraph.pop(target)
                
                
def transpose(method):
    """method decorator for solve to decide on whether or not to use the transposed
    board for solving rather than the original"""

    @wraps(method)
    def wrapper(ref, solved_board):  # ref is method's self

        if StrategyTranspose.shouldtranspose(ref):
            ref.solved_board = solved_board
            return StrategyTranspose.execute_strategy(ref)
        else:
            return method(ref, solved_board)

    return wrapper


class StrategyTranspose:

    def execute_strategy(board):
        """"""
        # save previous init states
        solved_board = board.solved_board
        mixed_board = board.mixed_up_board

        # transpose the board
        board.__init__([list(col) for col in zip(*mixed_board)])

        # call the decoree (original) solve function.
        board.solve.__wrapped__(board, [list(col) for col in zip(*solved_board)])
        solution = board.solution

        # reverse transpose (to make it look like it was the same board afterall
        board.__init__([list(col) for col in zip(*board.toList())])
        board.solved_board = solved_board
        board.solution = StrategyTranspose.translate_solution(solution)

        return board.solution

    @staticmethod
    def translate_solution(solution):
        """Since the board was solved for its Transpose (columnmajor), the solution
        cannot be reproduced in its original board version (rowmajor).
        As consequence the solution must be translated."""

        translation = {'L': 'U', 'R': 'D', 'U': 'L', 'D': 'R'}
        return [translation[letter] + ind for letter, ind in solution]

    def shouldtranspose(board):
        """determine whether the board should be transposed (has uneven rdim, but even cdim)"""
        return board.rdim % 2 != 0 and board.cdim % 2 == 0


class Cyclic_shift_board:
    direct = {'L': -1, 'R': 1, 'D': -1, 'U': 1}

    def __init__(self, mixed_up_board):
        """
        :param mixedUpBoard: two-dim arrays (or lists of lists) of symbols
        representing the initial (unsolved) grid

        Different grid sizes are tested: from 2x2 to 9x9 grids
        (including rectangular grids like 4x5)
        """

        self.mixed_up_board = mixed_up_board
        # Make the Node aware of (/allow to inquire) where the target of the currently occupying value is.
        Node.current = {val: (r, c) for r, row in enumerate(mixed_up_board) for c, val in enumerate(row)}

        # Create a playable board
        self.rows = [Row([Node((r, c), val) for c, val in enumerate(row)], r, self) for r, row in
                     enumerate(mixed_up_board)]
        self.cols = [Column(col, c, self) for c, col in enumerate(zip(*reversed(self.rows)))]
        self.rdim, self.cdim = len(self.rows[0]), len(self.cols[0])

        self.solution = []  # reset previous solution

    def __repr__(self):
        return '\n'.join([' '.join([str(val) for val in row]) for row in self.rows])

    @transpose
    def solve(self, solved_board):
        """Your task: return a List of moves that will transform the unsolved
           grid into the solved one. All values of the scrambled and unscrambled
           grids will be unique! Moves will be 2 character long Strings"""

        self.solution = []  # reset previous solution
        self.solved_board = solved_board
        Node.target = {val: (r, c) for r, row in enumerate(solved_board)
                       for c, val in enumerate(row)}

        StrategyLiftshift.executeStrategy(self)

        # corner case: simple shift suffices & nothing else needs to be done
        _, t = Node.current[self.solved_board[0][0]]
        self.rows[0].shift(self.rows[0].shortest_shiftLR(t, 0))
        if self.solved_board[0] != self.rows[0].toList():
            StrategyToprow.executeStrategy(self)

        if self.solved_board != self.toList():  # not solved yet
            return None  # unsolvable

        else:
            return self.solution

    def toList(self):
        return [[letter for letter in row] for row in str(self).replace(' ', '').split('\n')]


def loopover(mixed_up_board, solved_board):
    return Cyclic_shift_board(mixed_up_board).solve(solved_board)
  
################################################################
class Loopover:
    def __init__(self, grid, end, width=None, height=None):
        self.grid = grid
        self.end = end
        self.height = height if height else len(grid)
        self.width = width if width else len(grid[0])

        self.parse_positions()

        self.moves_made = []

    def solve(self):
        for y in range(self.height - 1):
            for x in range(self.width):
                self.solve_position((x, y))
        self.solve_final()
        return self.moves_made if self.grid == self.end else None

    def solve_position(self, correct_pos):
        current_num = self.correct_num_at[correct_pos]
        correct_x, correct_y = correct_pos

        cx, cy = self.current_position_of[current_num]
        if cy == correct_y:
            self.move('C', cx, 1)
            self.move('R', cy + 1, 1)
            self.move('C', cx, -1)
            cx, cy = self.current_position_of[current_num]

        if cx == correct_x:
            self.move('R', cy, 1)
            cx += 1

        self.move('C', correct_x, cy - correct_y)
        self.move('R', cy, - (cx - correct_x))
        self.move('C', correct_x, correct_y - cy)

    def solve_final(self):
        correct_y = self.height - 1

        for correct_x in range(self.width - 2):
            self.print_grid()
            current_num = self.end[correct_y][correct_x]
            cx, cy = self.current_position_of[current_num]
            dx = cx - correct_x

            if cx == correct_x:
                continue

            if abs(dx) == 1:
                move = 2
            else:
                move = 1

            self.move('C', cx, -1)
            self.move('R', correct_y - 1, -dx)
            self.move('C', correct_x, 1)
            self.move('R', correct_y, -move)
            self.move('C', correct_x, -1)
            self.move('R', correct_y, move)
            self.move('R', correct_y - 1, dx)
            self.move('C', cx, 1)

        self.print_grid()

#         last_num = correct_y * self.width + self.width
        last_num = self.end[-1][-1]
        if self.current_position_of[last_num][0] != self.width - 1:
            self.solve_parity()
#         self.print_grid()

    def solve_parity(self):
        if self.height % 2 == 0:
            self.parity1()
        else:
            self.parity2()

    def parity1(self):
        for _ in range(self.height // 2):
            self.move('C', self.width - 1, -1)
            self.move('R', self.height - 1, 1)
            self.move('C', self.width - 1, -1)
            self.move('R', self.height - 1, -1)
        self.move('C', self.width - 1, -1)

    def parity2(self):
        # setup:
        self.move('C', self.width - 1, -1)
        self.move('R', self.height - 1, 1)
        self.move('C', self.width - 1, 1)
        self.move('R', self.height - 1, -1)
        for _ in range(self.width // 2):
            self.move('R', self.height - 1, -1)
            self.move('C', self.width - 1, -1)
            self.move('R', self.height - 1, -1)
            self.move('C', self.width - 1, 1)
        self.move('R', self.height - 1, -1)

    def move(self, line, number, times):
        if line == 'R':
            for px in range(self.width):
                num = self.grid[number][px]
                self.current_position_of[num] = ((px + times) % self.width, number)
            self.grid[number] = self.rotate_line(self.grid[number], times % self.width)
            move_made = f"{'R' if times > 0 else 'L'}{number}"
        elif line == 'C':
            for py in range(self.height):
                num = self.grid[py][number]
                self.current_position_of[num] = (number, (py + times) % self.height)
            column = [self.grid[y][number] for y in range(self.height)]
            rotated = self.rotate_line(column, times % self.height)
            for y in range(self.height):
                self.grid[y][number] = rotated[y]
            move_made = f"{'D' if times > 0 else 'U'}{number}"

        self.moves_made.extend([move_made] * abs(times))

    def rotate_line(self, line, times):
        return line[-times:] + line[:-times]

    def parse_positions(self):
        self.correct_num_at = {}
        self.current_position_of = {}
        for y, row in enumerate(self.grid):
            for x, sq in enumerate(row):
                pos = (x, y)
                self.correct_num_at[pos] = self.end[y][x]
                self.current_position_of[sq] = pos

    def print_grid(self):
        print()
        for row in self.grid:
            print(row)
            
def loopover(start, end):
    lp = Loopover(start, end).solve()
    print(lp)
    return lp
  
#############################################
def loopover(mixed, solved):
    t = {c: (i, j) for (i, row) in enumerate(solved) for (j, c) in enumerate(row)}
    b = {(i, j): t[c] for (i, row) in enumerate(mixed) for j, c in enumerate(row)}
    unsolved = {k for k, v in b.items() if k not in ((0, 0), (0, 1)) and k != v}
    sol = []

    while unsolved:
        i, j = next(iter(unsolved)) if b[0, 0] in ((0, 0), (0, 1)) else b[0, 0]
        if i == 0:
            sol += [f"D{j}", *j * ["L1"], "L0", "U0", "R0", "D0", *j * ["R1"], f"U{j}"]
        else:
            sol += [*j * [f"L{i}"], "L0", *i * ["U0"], "R0", *i * ["D0"], *j * [f"R{i}"]]
        b[0, 0], b[0, 1], b[i, j] = b[0, 1], b[i, j], b[0, 0]

        if b[i, j] == (i, j):
            unsolved.remove((i, j))

    if b[0, 0] != (0, 0) and len(mixed) % 2 == 0:
        sol += [*len(mixed) // 2 * ["D0", "L0", "D0", "R0"], "D0"]
    elif b[0, 0] != (0, 0) and len(mixed[0]) % 2 == 0:
        sol += [*len(mixed[0]) // 2 * ["R0", "U0", "R0", "D0"], "U0", "R0", "D0"]
    elif b[0, 0] != (0, 0):
        return None

    return sol
  
##################################
import random # Crazy mode unlock

def loopover(mix, sol):
    if mix==sol:
        return []
    move = []
    finding_easy(mix, sol, move)
    hard_find_x(mix, sol, move)
    hard_find_y(mix, sol, move)
    x = len(mix[0])-1
    y = len(mix)-1
    if mix==sol:
        return move
    else:
        hard_find_y(mix, sol, move)
        if mix==sol:
            return move
        else:
            for j in range(random.randint(1, 10)):
                up(mix, x, move)
                for i in range(random.randint(1, 10)):
                    left(mix, y, move)
            hard_find_x(mix, sol, move)
            if mix==sol:
                return move
            else:
                for j in range(random.randint(1, 10)):
                    up(mix, x, move)
                    for i in range(random.randint(1, 11)):
                        left(mix, y, move)
                hard_find_x(mix, sol, move)
                hard_find_y(mix, sol, move)
                if mix==sol:
                    return move
                else:
                    for j in range(random.randint(1, 15)):
                        up(mix, x, move)
                        for i in range(random.randint(1, 10)):
                            left(mix, y, move)
                    hard_find_x(mix, sol, move)
                    hard_find_y(mix, sol, move)
                    if mix==sol:
                        return move
                    else:
                        for j in range(random.randint(1, 9)):
                            up(mix, x, move)
                        for i in range(random.randint(1, 14)):
                            left(mix, y, move)
                        hard_find_x(mix, sol, move)
                        hard_find_y(mix, sol, move)
                        if mix==sol:
                            return move
                        else:
                            for j in range(random.randint(1, 12)):
                                up(mix, x, move)
                                for i in range(random.randint(1, 10)):
                                    left(mix, y, move)
                            hard_find_x(mix, sol, move)
                            hard_find_y(mix, sol, move)
                            if mix==sol:
                                return move
                            else:
                                up(mix, x, move)
                                left(mix, y, move)
                                up(mix, x, move)
                                if mix==sol:
                                    return move
                                else:
                                    return None
    

    
'''finding_easy -- Finds these    1 2 3 4 *
                    elements:     6 7 8 9 *
                               11 12 13 14 *
                               *  *  *  *  *
                                                    '''
def finding_easy(mix, sol, move):
    unfound = []
    for i in range(len(sol)-1):
        for j in range(len(sol[0])-1):
            unfound.append(sol[i][j])
    for i in unfound:
        making_easy(mix, sol, i, move)

        
'''finding_hard_x -- Finds these    1 2 3 4 *
                      elements:     6 7 8 9 *
                                 11 12 13 14 *
                                 16 17 18 19 *
                                                    '''
def hard_find_x(mix, sol, move):
    for i in range(len(mix[0])-1):
        making_hard_x(mix, sol[len(mix)-1][i], i, move)
        
    
'''finding_hard_y -- Finds these    1 2 3 4 5
                      elements:     6 7 8 9 10
                                   11 12 13 14
                                   14 15 16 17
                                                    '''
def hard_find_y(mix, sol, move):
    cor = sol[len(mix)-1][0]
    for i in range(len(mix)):
        making_hard_y(mix, sol, cor, sol[i][len(mix[0])-1], i, move)
    
    
def making_hard_y(mix, sol, cor, el, k, move):
    for i in range(len(mix)):
        for j in range(len(mix[0])):
            if mix[i][j] == el:
                x = j
                y = i
    for i in range(len(mix)):
        for j in range(len(mix[0])):
            if mix[i][j] == cor:
                xc = j
                yc = i
    fl = False
    if x == 0:
        x = len(mix[0])-1
        y = len(mix)-1
        up(mix, x, move)
        left(mix, y, move)
        up(mix, x, move)
        right(mix, y, move)
        down(mix, x, move)
    else:
        score = 0
        while y < len(mix)-1:
            down(mix, x, move)
            y += 1
            score += 1
        left(mix, len(mix)-1, move)
        for i in range(score+1):
                up(mix, x, move)
        right(mix, len(mix)-1, move)
    

def making_hard_x(mix, el, k, move):
    for i in range(len(mix)):
        for j in range(len(mix[0])):
            if mix[i][j] == el:
                m = mix[i][j]
                x = j
                y = i
    while y<len(mix)-1:
        down(mix, len(mix[0])-1, move)
        y += 1
    if k == 0:
        if x > len(mix[0])-2:
            left(mix, y, move)
        else:
            while x < len(mix[0])-2:
                right(mix, y, move)
                x += 1
    else:
        score = 0
        if x > len(mix[0])-1:
            left(mix, y, move)
            score += 1
        else:
            while x < len(mix[0])-1:
                right(mix, y, move)
                x += 1
                score += 1
        up(mix, len(mix[0])-1, move)
        for i in range(score):
            left(mix, y, move)
        down(mix, len(mix[0])-1, move)
        left(mix, y, move)
    
    
                
def making_easy(mix, sol, el, move):
    for i in range(len(mix)):
        for j in range(len(mix[0])):
            if sol[i][j] == el:
                row = i
    for i in range(len(mix)):
        for j in range(len(mix[0])):
            if mix[i][j] == el:
                m = mix[i][j]
                x = j
                y = i
                
    if (y != len(mix)-1) and (x != len(mix[0])-1):
        save_flip(mix, y, x, move)
        x += 1
        y += 1
    for i in range(((len(mix[0])-1)-x)):
        right(mix, y, move)
    while y<row:
        down(mix, len(mix[0])-1, move)
        y += 1
    for i in range(y-row):
        up(mix, len(mix[0])-1, move)
    mix = left(mix, row, move)[1]
    
def save_flip(mix, i, j, move):
    mix = down(mix, j, move)[1]
    mix = right(mix, i+1, move)[1]
    mix = up(mix, j, move)[1]
    return move, mix
    

def right(mix, i, move):
    mix[i] = mix[i][-1:] + mix[i][:-1]
    move.append(f'R{i}')
    return move, mix


def left(mix, i, move):
    mix[i] = mix[i][1:] + mix[i][:1]
    move.append(f'L{i}')
    return move, mix


def up(mix, j, move):
    vertical = []
    for i in range(len(mix)):
        vertical.append(mix[i][j])
    vertical = vertical[1:] + vertical[:1]
    for i in range(len(mix)):
        mix[i][j] = vertical[i]
    move.append(f'U{j}')
    return move, mix


def down(mix, j, move):
    vertical = []
    for i in range(len(mix)):
        vertical.append(mix[i][j])
    vertical = vertical[-1:] + vertical[:-1]
    for i in range(len(mix)):
        mix[i][j] = vertical[i]
    move.append(f'D{j}')
    return move, mix
  
########################################
def loopover(start, end):
    def transpose(a):
        return [[r[j] for r in a] for j in range(len(a[0]))]
    moves = []
    transposed = int(len(start) % 2 == 0 and len(start[0]) % 2 != 0)
    if transposed:
        start = transpose(start)
        end = transpose(end)
    def shift(a, k):
        return a[k:] + a[0:k]
    def left_right(r, k):
        if not k: return
        start[r] = shift(start[r], k)
        moves.extend([('LU' if k > 0 else 'RD')[transposed] + str(r)] * abs(k))
    def up_down(c, k):
        if not k: return
        col = shift([r[c] for r in start], k)
        for i, r in enumerate(start):
            r[c] = col[i]
        moves.extend([('UL' if k > 0 else 'DR')[transposed] + str(c)] * abs(k))
    def move(i, j, r, c):
        up_down(j, i - r)
        left_right(r, c - j)
        up_down(j, r - i)
    def pos(x):
        for i, r in enumerate(start):
            for j, y in enumerate(r):
                if x == y:
                    return (i, j)
    m, n, d = len(start), len(start[0]), 1
    for i in range(m):
        for j in range(n):
            r, c = pos(end[i][j])
            if r == i and c == j: 
                continue
            elif j == 0 and r == i:
                left_right(r, c)
            elif i == m - 1:
                left_right(r, c)
                up_down(0, d)
                left_right(r, j - c)
                up_down(0, -d)
                left_right(r, c - j)
                up_down(0, d)
                left_right(r, -c)
                d = -d
            elif r == i:
                up_down(c, -1)
                move(i, j, r + 1, c)
                up_down(c, 1)
            elif c == j:
                left_right(r, 1)
                move(i, j, r, j - 1)
            else:
                move(i, j, r, c)
    if d < 0:
        if n % 2:
            return None
        for j in range(n + 1):
            up_down(0, d)
            left_right(m - 1, 1)
            d = -d
    return moves
  
###################################
def loopover(m, s):
    def lo(m,s,o):
        if m==s:
            return(o)
        def u(c,t):
            if t!=0:
                while t<0:
                    t+=len(m)
                t%=len(m)
                o.extend(["U"+str(c)]*t)
                temp=[i[c] for i in m]
                for i in range(len(m)):
                    m[i-t][c]=temp[i]
        def l(r,t):
            if t!=0:
                while t<0:
                    t+=len(m[0])
                t%=len(m[0])
                o.extend(["L"+str(r)]*t)
                m[r]=m[r][t:]+m[r][:t]
        def fc(sy):
            for i in m:
                if sy in i:
                    for j in i:
                        if j==sy:
                            return(m.index(i),i.index(j))
        for i in range(len(m)):
            if m[i]!=s[i]:
                if i==0:
                    for j in range(len(m[i])):
                        if m[i][j]!=s[i][j]:
                            y,x=fc(s[i][j])
                            if j!=0 and y==0:
                                y+=1
                                u(x,-1)
                            l(y,x-j)
                            u(j,y-i)
                elif i!=len(m)-1:
                    for j in range(len(m[i])):
                        if m[i][j]!=s[i][j]:
                            y,x=fc(s[i][j])
                            if j!=0 and y==i:
                                y+=1
                                u(x,-1)
                                l(y,-1)
                                u(x,1)
                                x=(x+1)%len(m[0])
                            if x==j:
                                l(y,-1)
                                x=(x+1)%len(m[0])
                            u(j,i-y)
                            l(y,x-j)
                            u(j,y-i)
                else:
                    for j in range(len(m[i])):
                        if m[i][j]!=s[i][j]:
                            y,x=fc(s[i][j])
                            if j==0:
                                l(i,x-j)
                            else:
                                if y==i:
                                    l(i,x-len(m[i])+1)
                                    u(len(m[0])-1,1)
                                    ys,xs=fc(s[i][j-1])
                                    l(i,xs-len(m[i])+2)
                                    u(len(m[0])-1,-1)
                                    l(i,len(m[i])-1-j)
                                else:
                                    ys,xs=fc(s[i][j-1])
                                    l(i,j+1-len(m[i]))
                                    u(len(m[0])-1,1)
                                    l(i,len(m[i])-j-1)
                                    u(len(m[0])-1,-1)
        if m==s:                            
            return(o)
        else:
            if len(m[0])%2==0:
                for i in range(len(m[0])//2):
                    l(0,-1)
                    u(len(m[0])-1,-1)
                    l(0,-1)
                    u(len(m[0])-1,1)
                l(0,-1)
                return(o)
            elif len(m)%2==0:
                l(len(m)-1,1)
                u(len(m[0])-1,1)
                l(len(m)-1,-1)
                u(len(m[0])-1,-1)
                for i in range(len(m)//2):
                    u(0,-1)
                    l(len(m)-1,-1)
                    u(0,-1)
                    l(len(m)-1,1)
                u(0,-1)
                return(o)
    return lo(m,s,[])
  
#############################################
import random
class Board(object):

    def __init__(self, mixed_up_board, solved_board):
        self.mixed = mixed_up_board
        self.board = mixed_up_board
        self.solved_board = solved_board
        self.height = len(self.board)
        self.width = len(self.board[0])
        self.sequence = []

    def up(self, column):
        temp = self.board[0][column]
        for i in range(0, self.height - 1):
            self.board[i][column] = self.board[i + 1][column]
        self.board[-1][column] = temp
        self.sequence.append('U' + str(column))

    def down(self, column):
        temp = self.board[-1][column]
        for i in range(self.height - 1, 0, -1):
            self.board[i][column] = self.board[i - 1][column]
        self.board[0][column] = temp
        self.sequence.append('D' + str(column))

    def right(self, row):
        temp = self.board[row][-1]
        for i in range(self.width - 1, 0, -1):
            self.board[row][i] = self.board[row][i - 1]
        self.board[row][0] = temp
        self.sequence.append('R' + str(row))

    def left(self, row):
        temp = self.board[row][0]
        for i in range(0, self.width - 1):
            self.board[row][i] = self.board[row][i + 1]
        self.board[row][-1] = temp
        self.sequence.append('L' + str(row))

    def print(self, board):
        for i in range(0, self.height):
            for j in range(0, self.width):
                print(board[i][j], end=' ')
            print()

    def search(self, elem):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.board[i][j] == elem:
                    return [i, j]
        return None

def solve_columns(board):
    for i in range(0, board.height):
        len = 0
        for j in range(0, board.width - 1):
            elem = board.solved_board[i][j]
            x, y = board.search(elem)
            while y != board.width - 1:
                board.right(x)
                x, y = board.search(elem)

            while x != i:
                board.up(board.width - 1)
                x, y = board.search(elem)
            board.down(board.width - 1)
            if len > 0:
                while board.board[i][board.width - 2] != prev:
                    board.left(i)
            board.up(board.width - 1)
            board.left(i)
            len += 1
            prev = elem

def solve_last_col(board):
    for j in range(1, board.height - 1):
        elem = board.solved_board[j - 1][board.width - 1]
        next = board.solved_board[j][board.width - 1]
        x, y = board.search(next)

        while y != board.width - 1:
            board.left(x)
            x, y = board.search(next)

        while board.board[board.height - 1][board.width - 1] != next:
            board.up(board.width - 1)
        board.left(board.height - 1)

        while board.board[board.height - 1][board.width - 1] != elem:
            board.up(board.width - 1)
        board.up(board.width - 1)
        board.right(board.height - 1)
        board.up(board.width - 1)

def loopover(mixed_up_board, solved_board):
    board = Board(mixed_up_board, solved_board)
    solve_columns(board)
    solve_last_col(board)
    
    while board.board[0][board.width - 1] != board.solved_board[0][board.width - 1]:
        board.up(board.width - 1)

    while board.board[board.height - 1][0] != board.solved_board[board.height - 1][0]:
        board.right(board.height - 1)

    board.print(board.board)
    flag = 0
    while board.board[board.height - 1] != board.solved_board[board.height - 1]:
        #board.board = board.mixed
        #board.sequence = []
        board.down(flag % board.width)
        board.left(flag % board.height)
        solve_columns(board)
        solve_last_col(board)
        flag += 1
        if flag > 333:
            return None
    board.print(board.board)
    if board.board == board.solved_board:
        return board.sequence
    else:
        return None
      
#################################
import numpy as np

def loopover(mixed, solved):
    fixed,column,row,moves = mixed.copy(),len(mixed),len(mixed[0]),[]
    if solved != mixed:
        mixed = np.array(mixed)
        for ii in range(column-1):
            for i in range(row-1):
                if ii == 0:
                    while np.argwhere(mixed==solved[ii][i])[0][0] <= ii:
                        moves,mixed = down(np.argwhere(mixed==solved[ii][i])[0][1],moves,mixed,column)
                else:
                    if (i != 0) and (ii == np.argwhere(mixed==solved[ii][i])[0][0]):
                        while np.argwhere(mixed==solved[ii][i])[0][1] < row-1:
                            moves,mixed = left(np.argwhere(mixed==solved[ii][i])[0][0],moves,mixed)
                        moves,mixed = down(np.argwhere(mixed==solved[ii][i])[0][1],moves,mixed,column)
                        while np.argwhere(mixed==solved[ii][i-1])[0][1] != row-2:
                            moves,mixed = right(np.argwhere(mixed==solved[ii][i-1])[0][0],moves,mixed) 
                while np.argwhere(mixed==solved[ii][i])[0][1] < row-1:
                    moves,mixed = right(np.argwhere(mixed==solved[ii][i])[0][0],moves,mixed)
                while np.argwhere(mixed==solved[ii][i])[0][0] != ii:
                    moves,mixed = up(np.argwhere(mixed==solved[ii][i])[0][1],moves,mixed,column)
                moves,mixed = left(np.argwhere(mixed==solved[ii][i])[0][0],moves,mixed)
        moves,mixed = lastcolumn(moves,mixed,solved,column,row)
        moves,mixed = lastrow(moves,mixed,solved,column,row)
        while np.argwhere(mixed==solved[-1][0])[0][1] != 0:
            moves,mixed = right(column-1,moves,mixed)
        while np.argwhere(mixed==solved[0][-1])[0][0] != 0:
            moves,mixed = up(row-1,moves,mixed,column)
        moves,mixed = lastcolumn(moves,mixed,solved,column,row)
        moves,mixed = lastrow(moves,mixed,solved,column,row)
        fixed = mixed.tolist()
        if fixed != solved:
            if (column % 2) + (row % 2) == 2: return None
            else:
                for e in range(0,2): moves,mixed = right(column-1,moves,mixed)
                moves,mixed = up(row-1,moves,mixed,column)
                moves,mixed = right(column-1,moves,mixed)
                for e in range(0,3): moves,mixed = up(row-1,moves,mixed,column)
                moves,mixed = lastcolumn(moves,mixed,solved,column,row)
                moves,mixed = lastrow(moves,mixed,solved,column,row)
    return moves


def up(x,moves,mixed,column):
    temp = [np.roll([mixed[i][x] for i in range(column)],-1,axis=0)[ii] for ii in range(column)] # вверх
    for ii in range(column): mixed[ii][x] = temp[ii]
    moves.append(f'U{x}')  
    return moves,mixed

def down(x,moves,mixed,column):
    temp = [np.roll([mixed[i][x] for i in range(column)],1,axis=0)[ii] for ii in range(column)] # вниз
    for ii in range(column): mixed[ii][x] = temp[ii]
    moves.append(f'D{x}')  
    return moves,mixed

def left(y,moves,mixed):
    mixed[y] = np.roll(mixed[y],-1) # влево
    moves.append(f'L{y}')  
    return moves,mixed
    
def right(y,moves,mixed):
    mixed[y] = np.roll(mixed[y],1) # вправо
    moves.append(f'R{y}')  
    return moves,mixed
    
    
def lastcolumn(moves,mixed,solved,column,row):
    for ii in range(column-1):
        while np.argwhere(mixed==solved[ii][-1])[0][1] != row-1:
            moves,mixed = right(column-1,moves,mixed)
        while np.argwhere(mixed==solved[ii][-1])[0][0] != column-2:
            moves,mixed = up(row-1,moves,mixed,column)
        if ii > 0:
            if np.argwhere(mixed==solved[ii][-1])[0][0]-np.argwhere(mixed==solved[ii-1][-1])[0][0] != 1:
                moves,mixed = down(row-1,moves,mixed,column)
                moves,mixed = left(column-1,moves,mixed)
                while np.argwhere(mixed==solved[ii-1][-1])[0][0] != column-2:
                    moves,mixed = down(row-1,moves,mixed,column)
                moves,mixed = right(column-1,moves,mixed)
                moves,mixed = up(row-1,moves,mixed,column)
    return moves,mixed

def lastrow(moves,mixed,solved,column,row):
    for i in range(1,row-1):
        if i > 1:
            while np.argwhere(mixed==solved[-1][i])[0][0] != column-1:
                moves,mixed = down(row-1,moves,mixed,column)
        while np.argwhere(mixed==solved[-1][i])[0][1] != row-1:
            moves,mixed = right(column-1,moves,mixed)
        moves,mixed = down(row-1,moves,mixed,column)
        if i == 1:
            while np.argwhere(mixed==solved[-1][0])[0][1] != row-2:
                moves,mixed = right(column-1,moves,mixed)
        else:
            while np.argwhere(mixed==solved[-1][i-1])[0][1] != row-2:
                moves,mixed = right(column-1,moves,mixed)
        moves,mixed = up(row-1,moves,mixed,column)
        moves,mixed = left(column-1,moves,mixed)
    return moves,mixed
  
###################################
import numpy as np

class Matrix:
    def __init__(self, m=None, n=None, M=None, A=None):
        self.moves = []
        self.moves_shuffle = []
        if m and n:
            self.m, self.n = m, n
            self.M = np.arange(m*n).reshape(m, n)  # target
            self.A = np.copy(self.M)  # shuffled
            self.shuffle()
        elif M and A:
            self.M = np.array(M)
            self.A = np.array(A)
            self.m, self.n = self.M.shape
        else:
            raise ValueError('Neither dimensions nor input/output matrices given.')
        
        self.A_orig = np.copy(self.A)
        
        # One or two solving iterations required to solve the puzzle
        # Unsolvable puzzle repeats itself if more iterations are involved
        self.solve_iterations = 0
        
    
    def move_row(self, i, dj):
        """ Move row i right for dj > 0, or left for dj < 0 """
        self.A[i, :] = np.roll(self.A[i, :], dj)
        self.store_move('rows', i, dj)
    
    def move_col(self, j, di):
        """ Move column j up for di > 0, or down for di < 0 """
        self.A[:, j] = np.roll(self.A[:, j], -di)
        self.store_move('cols', j, di)

        
    def left(self, i):
        """ Move left the i-th row by 1 """
        self.move_row(i, -1)
    def right(self, i):
        """ Move right the i-th row by 1 """
        self.move_row(i, +1)
    def down(self, j):
        """ Move down the j-th column by 1 """
        self.move_col(j, -1)
    def up(self, j):
        """ Move up the j-th column by 1 """
        self.move_col(j, +1)
    
    
    def move_by_code(self, s, reverse=False):
        """ Move using string code like this: R3, U0 """
        def get_direction(d):
            if not reverse:
                return d
            if d=='R': return 'L'
            if d=='L': return 'R'
            if d=='U': return 'D'
            if d=='D': return 'U'
            
        direction = s[0]
        v = int(s[1:])
        if direction == get_direction('R'):
            self.right(v)
        elif direction == get_direction('L'):
            self.left(v)
        elif direction == get_direction('U'):
            self.up(v)
        elif direction == get_direction('D'):
            self.down(v)

    
    def store_move(self, kind, crd, shift):
        """ Save history of every move """
        if shift == 0:
            return
        if kind == 'rows':
            direction = 'R' if shift > 0 else 'L'
        elif kind == 'cols':
            direction = 'U' if shift > 0 else 'D'
        new_moves = [f'{direction}{crd}'] * abs(shift)
        self.moves.extend(new_moves)
        
    
    def shuffle(self, N=10):
        """ Shuffles the matrix A """
        for (i, di), (j, dj) in zip(np.random.randint(0, self.m, (N, 2)),
                                    np.random.randint(0, self.n, (N, 2))):
            self.move_row(i, dj)
            self.move_col(j, di)
        self.moves_shuffle = self.moves.copy()
        self.moves = []

        
    def shift_i(self, i, di):
        """ Shift rows index accounting for cycling """
        return (i + di) % self.m
    
    def shift_j(self, j, dj):
        """ Shift columns index accounting for cycling """
        return (j + dj) % self.n
    
    
    def solve_element(self, i0, j0):
        """ Move the element with value M[i0, j0] to its proper station in A """
        v = self.M[i0, j0]
        idx = np.argmax( self.A == v )
        i, j = np.unravel_index(idx, self.A.shape)

        if i==i0 and j==j0:  # nothing to do
            return
        
        # Move element out from the target row (should be return back)
        isTargetRow = i == i0
        if isTargetRow:
            diB = -1
            self.move_col(j, diB)
            i = self.shift_i(i, -diB)
            jB = j
        
        # Move element out from the target column
        elif j==j0:
            dj = 1
            self.move_row(i, dj)
            j = self.shift_j(j, dj)
        
        # Move target column towards the element row
        diT = i0 - i
        self.move_col(j0, diT)
        
        # Move element row to match the moved target station
        dj = j0 - j
        self.move_row(i, dj)
        j = self.shift_j(j, dj)
        
        # Move target column back
        self.move_col(j, -diT)
        i = self.shift_i(i, diT)
        
        # Return the column of original element station back if it is disturbed
        if isTargetRow:
            self.move_col(jB, -diB)
    
    
    def swap_elements(self, j):
        """ Cycle three elements j-1, j, j+1 in the last row when j != min/max """
        # Magic combination
        i = self.m - 2
        self.move_row(i, +1)
        self.move_col(j, +1)
        self.move_row(i, -1)
        self.move_col(j, -1)
        
        # Resort prelast row
        for j in range(self.n):
            self.solve_element(i, j)
        
        # Move initial element to the left
        i, j = self.get_M_pos_at_A(i0=self.m-1, j0=0)
        self.move_row(self.m-1, -j)
    
    
    def get_M_pos_at_A(self, i0=None, j0=None, v=None):
        """ Return i,j in the unsolved matrix for the target element
            in the solved matrix """
        if not v:
            v = self.M[i0, j0]
        idx = np.argmax( self.A == v )
        i, j = np.unravel_index(idx, self.A.shape)
        return i, j
    

    def solve_last_row(self, recalled=False):
        """ Special solve procedure for the last row """
        for j0 in range(0, self.n-2):  # -2 important
            v = self.M[self.m-1, j0]
            while True:
                i, j = self.get_M_pos_at_A(v=v)  # changes with A
                if j==j0:
                    break
                j_cycle = j
                if j==self.n - 1:
                    j_cycle -= 1
                if j == 1:
                    j_cycle += 1
                self.swap_elements(j_cycle)
        
        if not self.M[self.m-1, self.n-1] == self.A[self.m-1, self.n-1]:
            if not recalled:
                self.swap_elements(self.n-1)
                self.solve_last_row(recalled=True)
            else:  
                # TODO: 'else' block is the hack to prevent endless recursion
                #       that can appear in the case of even number of rows 
                #       (self.m) and odd number of columns (self.n)
                #       --> one just needs to move any column up once
                #
                #       The reason of such behavior relates to the chosen algorithm
                #       of puzzle solving
                #
                #       This should be refactored consciously
                self.up(0)
                self.solve()
        

    def solve(self):
        """ Solve puzzle """
        if self.solve_iterations > 1:  # no solution
            self.moves = None
            return
        
        self.solve_iterations += 1
        for i in range(self.m-1):
            for j in range(self.n):
                self.solve_element(i, j)
        self.solve_last_row()


    def is_solved(self):
        """ Check if puzzle is solved """
        return np.all(np.equal(self.A, self.M))



def loopover(mixed_up_board, solved_board):
    mat = Matrix(M=solved_board, A=mixed_up_board)
    mat.solve()
    
    return mat.moves
  
########################################
def loopover(mixed_up_board, solved_board):
    targets = [[findloc(x, solved_board) for x in row] for row in mixed_up_board]

    nrows = len(targets)
    assert nrows >= 2
    ncols = len(targets[0])
    assert ncols >= 2
    assert all(len(row) == ncols for row in targets)
    
    moves = []
    
    def down(colind, count):
        nonlocal targets, moves, nrows, ncols
        cmod = count % nrows
        if cmod == 0:
            return
        newcol = [row[colind] for row in targets]
        rotate_r(newcol, cmod)
        for (row, x) in zip(targets, newcol):
            row[colind] = x
        if cmod <= nrows // 2:
            move = "D" + str(colind)
            moves.extend(move for _ in range(cmod))
        else:
            move = "U" + str(colind)
            cup = nrows - cmod
            moves.extend(move for _ in range(cup))
    
    def up(colind, count):
        nonlocal down
        down(colind, -count)
    
    def right(rowind, count):
        nonlocal targets, moves, nrows, ncols
        cmod = count % ncols
        if cmod == 0:
            return
        rotate_r(targets[rowind], cmod)
        if cmod <= ncols // 2:
            move = "R" + str(rowind)
            moves.extend(move for _ in range(cmod))
        else:
            move = "L" + str(rowind)
            cleft = ncols - cmod
            moves.extend(move for _ in range(cleft))
    
    def left(rowind, count):
        nonlocal right
        right(rowind, -count)
    
    for rowi in range(nrows):
        for colj in range(ncols-1, 0, -1):
            (currow, curcol) = findloc((rowi, colj), targets)
            # move to (rowi, 0)
            if (currow == rowi):
                if curcol != 0:
                    # move to row 0, move down, move row back, move up
                    left(currow, curcol)
                    down(0, 1)
                    right(currow, curcol)
                    up(0, 1)
            else:
                # move to col 0, then up to rowi
                left(currow, curcol)
                up(0, currow - rowi)
            assert targets[rowi][0] == (rowi, colj)
            # move to col 1
            right(rowi, 1)
            del currow, curcol
        assert all(targets[rowi][j] == (rowi, j) for j in range(1, ncols))
    assert all(row[j] == (i, j) for (i,row) in enumerate(targets) for j in range(1, ncols))
    del rowi, colj
    
    # move (0,-1) to position (2,0)
    if nrows >= 3:
        (currow, curcol) = findloc((nrows-1, 0), targets)
        assert curcol == 0
        up(0, currow - 2)
        del currow, curcol
    for rowi in range(nrows - 1, 1, -1):
        (currow, curcol) = findloc((rowi, 0), targets)
        # move (rowi, 0) to position (2, 0)
        if (currow, curcol) == (1, 0):
            down(0, 1)
        elif curcol == 1:
            if currow == 0:
                up(0, 1)
                left(0, 1)
                down(0, 2)
                right(0, 1)
            else:
                assert currow == 1
                left(1, 1)
                down(0, 1)
                right(1, 1)
        else:
            assert curcol == 0
            # move to (1,0)
            up(0, currow - 1)
            left(1, 1)
            down(0, currow - 1)
            right(1, 1)
            down(0, 1)
        assert targets[2][0] == (rowi, 0)
    assert all(targets[j][0] == (j, 0) for j in range(2, nrows))
    
    def rotl():
        # [(0,1), (0,0), (1,0)] to [(0,0), (1,0), (0,1)]
        nonlocal left, up, right, down
        left(0, 1)
        up(0, 1)
        right(0, 1)
        down(0, 1)
    
    def rotr():
        # [(1,0), (1,1), (0,1)] to [(1,1), (0,1), (1,0)]
        nonlocal left, up, right, down
        right(1, 1)
        down(1, 1)
        left(1, 1)
        up(1, 1)
    
    
    if targets[1][1] != (1,1):
        if targets[0][0] == (1,1):
            rotl()
        while targets[1][1] != (1,1):
            rotr()
    assert targets[1][1] == (1,1)
    
    while targets[1][0] != (1,0):
        rotl()
    assert targets[1][0] == (1,0)
    
    def twist(ufun, lfun, dfun, amt=1):
        ufun(0, 1)
        lfun(0, amt)
        dfun(0, 1)
        lfun(0, 1)
    
    if targets[0][0] != (0,0):
        if ncols % 2 == 0:
            twist(up, left, down, 2)
            for _ in range((ncols - 2) // 2):
                twist(up, left, down)
        elif nrows % 2 == 0:
            rotl()
            rotl()
            twist(left, up, right, 2)
            for _ in range((nrows - 2) // 2):
                twist(left, up, right)
        else:
            return None
    
    return moves


def findloc(x, arr):
    for i,row in enumerate(arr):
        try:
            return (i,row.index(x))
        except ValueError:
            pass
    raise RuntimeError("not found: {}".format(x))

def rotate_r(lst, n):
    assert 1 <= n < len(lst)
    r = lst[-n:] + lst[:-n]
    lst[:] = r
    
##########################################
def slide(grid, row, n, mv):
    if n > 0:
        for i in range(n):
            mv.append('R' + str(row))
            grid[row] = [grid[row][-1]] + grid[row][0:-1]
    else:
        for i in range(abs(n)):
            mv.append('L' + str(row))
            grid[row] = grid[row][1:] + [grid[row][0]]



def scroll(grid, col, n, mv):
    if n > 0:
        for i in range(n):
            mv.append('D' + str(col))
            last = grid[-1][col]
            for j in range(1, len(grid)):
                grid[-j][col] = grid[-j - 1][col]
            grid[0][col] = last
    else:
        for i in range(abs(n)):
            mv.append('U' + str(col))
            last = grid[0][col]
            for j in range(0, len(grid) - 1):
                grid[j][col] = grid[j + 1][col]
            grid[-1][col] = last


def findchar(grid, char):
    for ri in range(len(grid)):
        if char in grid[ri]:
            return [ri, grid[ri].index(char)]
    raise Exception('Bad, bad code...')


def loopover(grid, target):
    moves = []
    w = len(grid[0])
    h = len(grid)

    # solve rows up to last one
    for ri in range(h-1):
        for ci in range(w):
            char = target[ri][ci]
            pos = findchar(grid, char)

            if grid[ri][ci] == char:
                continue
            # first, check if target is in the same row
            if pos[0] == ri:
                scroll(grid, pos[1], 1, moves)
                slide(grid, pos[0] + 1, 1, moves)
                scroll(grid, pos[1], -1, moves)
                pos[0] += 1
                pos[1] = (pos[1] + 1) % w
            # if target is in the same column
            if pos[1] == ci:
                slide(grid, pos[0], 1, moves)
                pos[1] = (pos[1] + 1) % w
            # scroll current to target row
            scroll(grid, ci, pos[0] - ri, moves)
            # slide target to us
            slide(grid, pos[0], ci - pos[1], moves)
            pos[1] = ci
            # scroll it back
            scroll(grid, ci, ri - pos[0], moves)

    #now the tricky part...
    
    char = target[-1][0] 
    slide(grid, h-1, -grid[-1].index(char), moves)

    for ci in range(1, w-2):
        #make c0 valid:
        char = target[-1][0]
        slide(grid, h-1, -grid[-1].index(char), moves)

        char = target[-1][ci]
        tc = grid[-1].index(char)
        if tc == ci:
            continue # this char is in correct place, continue

        scroll(grid, tc, -1, moves) #move target char up
        slide(grid, h-1, tc - ci, moves)# move current under target
        scroll(grid, tc, 1, moves) #move target down - in place

        #now we have to fix broken column (((
        #lets sacrifice dummy char and move it under broken column
        #lets find dummy char
        dummy = 0
        while grid[-1][dummy] in target[-1][0:ci+1] or grid[-1][dummy] == target[0][tc]:
            dummy += 1

        #move dummy under broken column
        slide(grid, h-1, tc - dummy, moves)
        #move broken collun up
        scroll(grid, tc, -1, moves)
        #move broken char back in place
        slide(grid, h-1, tc - grid[-1].index(target[0][tc]), moves)
        #fix collumn by moving it down
        scroll(grid, tc, 1, moves)

    #is it done?
    if grid[-1][-3:-1] == target[-1][-3:-1]:
        return moves

    #can we swap?
    if w % 2 and h % 2:
        return None

    if not h % 2:
        moves += ['U' + str(w-1), 'R' + str(h-1), 'D' + str(w-1), 'L' + str(h-1), 'U' + str(w-1)] * (h-1)
    else:
        moves += ['U' + str(w-1), 'R' + str(h-1), 'R' + str(h-1), 'D' + str(w-1), 'L' + str(h-1),  'L' + str(h-1),  'L' + str(h-1)]
        moves += ['U' + str(w-1), 'R' + str(h-1), 'D' + str(w-1), 'R' + str(h-1)]

        for f in range(2, w-3, 2):
            print('ff:', f)
            moves += ['U' + str(f), 'R' + str(h-1), 'D' + str(f), 'L' + str(h-1), 'L' + str(h-1), 'U' + str(f), 'R' + str(h-1), 'D' + str(f)]

    return moves
  
################################
def flip_board(n, m, source_board):
    target_board = [[source_board[i][j] for i in range(n)] for j in range(m)]
    return target_board

def loopover(mixed_up_board, solved_board):
    n = len(solved_board)
    m = len(solved_board[0])
    is_flip = False
    if m % 2 == 1:
        is_flip = True
        mixed_up_board = flip_board(n, m, mixed_up_board)
        solved_board = flip_board(n, m, solved_board)
        n, m = m, n
    alpha_mapping = {}
    for i in range(n):
        for j in range(m):
            alpha_mapping[solved_board[i][j]] = (i, j)
    for i in range(n):
        for j in range(m):
            mixed_up_board[i][j] = alpha_mapping[mixed_up_board[i][j]]
    res = []
    flip_dir = {'L': 'U', 'U': 'L', 'R': 'D', 'D': 'R'}
    def Move(dir, idx):
        if dir == 'L':
            mixed_up_board[idx] = mixed_up_board[idx][1:] + [mixed_up_board[idx][0]]
        elif dir == 'R':
            mixed_up_board[idx] = [mixed_up_board[idx][-1]] + mixed_up_board[idx][:-1]
        elif dir == 'U':
            tmp_v = mixed_up_board[0][idx]
            for o in range(1, n):
                mixed_up_board[o - 1][idx] = mixed_up_board[o][idx]
            mixed_up_board[n - 1][idx] = tmp_v
        else:
            tmp_v = mixed_up_board[n - 1][idx]
            for o in range(n - 1, 0, -1):
                mixed_up_board[o][idx] = mixed_up_board[o - 1][idx]
            mixed_up_board[0][idx] = tmp_v
        if is_flip:
            dir = flip_dir[dir]
        res.append(dir + str(idx))
    def FancyMove(dir, idx):
        p = (idx + m - 2) % m
        q = (p + 1) % m
        r = idx
        invdir = 'R' if dir == 'L' else 'L'
        Move('U', p)
        Move(dir, n - 1)
        Move('D', p)
        Move(dir, n - 1)
        Move('U', p)
        Move(invdir, n - 1)
        Move(invdir, n - 1)
        Move('D', p)
    for i in range(n - 1):
        for j in range(m):
            x, y = i, j
            for k in range(i, n):
                for l in range(m):
                    if mixed_up_board[k][l] == (i, j):
                        x, y = k, l
            if (x, y) == (i, j):
                continue
            if x == i:
                Move('D', y)
                Move('R', x + 1)
                Move('U', y)
                x = i + 1
                y = (y + 1) % m
            if y == j:
                Move('L', x)
                y = (y + m - 1) % m
            dcnt = x - i
            for k in range(dcnt):
                Move('D', j)
            while y != j:
                Move('R', x)
                y = (y + 1) % m
            for k in range(dcnt):
                Move('U', j)
    if m == 2:
        if mixed_up_board[n - 1][0] != (n - 1, 0):
            Move('R', n - 1)
    else:
        i = n - 1
        for j in range(m - 2):
            y = j
            for l in range(j, m):
                if mixed_up_board[i][l] == (i, j):
                    y = l
                    break
            if y == j:
                continue
            while y > j + 1:
                FancyMove('L', y)
                y -= 2
            if y == j + 1:
                FancyMove('L', (j + 2) % m)
                FancyMove('L', (j + 2) % m)
        j = m - 2
        if mixed_up_board[i][j] == (i, j):
            pass
        else:
            if m % 2 == 1:
                res = None
            else:
                while j != 0:
                    FancyMove('L', j)
                    j -= 2
                Move('L', n - 1)
    return res
  
##############################################
import numpy as np

def loopover(mixed_up_board, solved_board):
    board = np.array(mixed_up_board)
    solved_board = np.array(solved_board)
    indices = solved_board.flatten()
    nrows, ncols = board.shape
    moves = []

    def R(i, n=1):
        board[i] = np.roll(board[i], n)
        moves.extend([f"R{i % nrows}"] * (n % ncols))
    def D(i, n=1):
        board[:, i] = np.roll(board[:, i], n)
        moves.extend([f"D{i % ncols}"] * (n % nrows))
    def L(i, n=1): R(i, -n)
    def U(i, n=1): D(i, -n)
    def pos(i, j): return np.argwhere(board == solved_board[i, j])[0]
    def correct(i, j): return board[i, j] == solved_board[i, j]

    # first row
    L(pos(0, 0)[0], pos(0, 0)[1])
    U(pos(0, 0)[1], pos(0, 0)[0])
    for j in range(1, ncols):
        pi, pj = pos(0, j)
        if pi == 0: D(pj), L(1, pj - j), U(j)
        else: L(pi, pj - j), U(j, pi)

    # all but last row
    for i in range(1, nrows - 1):
        for j in range(ncols):
            if correct(i, j): continue
            pi, pj = pos(i, j)
            if pi == i: # same row
                D(pj), L(pi + 1, pj - j), U(pj), R(pi + 1)
            if pj == j: # same col
                R(pi)
            pi, pj = pos(i, j)
            D(j, pi - i), L(pi, pj - j), U(j, pi - i)

    # last row
    L(-1, pos(-1, 0)[1])
    for j in range(1, ncols - 2):
        while not correct(-1, j):
            pj = pos(-1, j)[1]
            pivot = max(pj - 1, j + 1)
            U(pivot), R(-1), D(pivot), L(-1, 2), U(pivot), R(-1), D(pivot)

    if not np.all(board == solved_board):
        if ncols % 2 == 0: # fix last row
            R(-1)
            for pivot in range(1, ncols - 1, 2):
                U(pivot), R(-1), D(pivot), L(-1, 2), U(pivot), R(-1), D(pivot)
        elif nrows % 2 == 0: # transpose and fix last col
            U(-1), R(-1), D(-1), L(-1), D(-1)
            for pivot in range(2, nrows - 1, 2):
                L(pivot), D(-1), R(pivot), U(-1, 2), L(pivot), D(-1), R(pivot)
        else: # bad parity
            return None

    return moves
  
###################################
import numpy as np
from collections import namedtuple, deque
from random import choice, seed, shuffle, randrange

# --------------------------------------- gobals

debug = 0
debugo = 0

# seed(1)
ROW, COL = 0, 1  # note row move means the cell is moe along that row to different column
Move = namedtuple("Move", "axis, index, distance")

g_chrs = []  # goal char string
s_chrs = []
height = 0
width = 0
move_list = []

# --------------------------------------- utilities

def output_moves():  #convert move_list to [ 'L0','U1', ... ] form
    out_moves = []
    for m in move_list:
        if debugo:
            print(f'({m}', end=",  (")
        if m.axis == ROW:
            s = ('R' if m.distance > 0 else 'L') + str(m.index if m.index >= 0 else height + m.index)
            d = m.distance # % width
        else:
            s = ('D' if m.distance > 0 else 'U') + str(m.index if m.index >= 0 else width + m.index)
            d = m.distance # % height
        for _ in range(abs(d)):
            out_moves.append(s)
            if debugo:
                print(f"'{s}',", end=' ')
        if debugo:
            print(')),')

    return out_moves


def convert_input(s, g):  # -> s, g, shape, c_map
    global height, width, g_chrs
    g_chrs = [e for row in g for e in row]
    s_chrs = [e for row in s for e in row]
    height = len(g)
    width = len(g[0])
    bd_shape = (height, width)

    c_map = {}  # map chr to int value
    for i, c in enumerate(g_chrs):
        c_map[c] = i
    g = np.array(range(width*height)).reshape(bd_shape)
    s = np.array([c_map[c] for c in s_chrs]).reshape(bd_shape)
    return s, g, bd_shape, c_map


def bstr(b):
    s = ""
    for row in b:
        p1 = " ".join(g_chrs[v] for v in row)
        p2 = " ".join(f"{v:3}" for v in row)
        s += p1 + "   " + p2 + "\n"
    return s


def bprint(b, msg="---"):
    print(msg)
    print(bstr(b))


def find_cell(v, a):  # return (r,c) of first value
    xs, ys = np.where(a == v)
    if len(xs):
        return [xs[0], ys[0]]


def do_move(from_node, m):  # -> new board
    global move_list
    deltas = [0, 0]  # track offsets of move 0 x:col, 1 y:row
    height, width = from_node.shape
    a = from_node.copy()
    if m.axis == ROW:
        v = a[m.index]
        v = np.concatenate((v, v))
        i = -m.distance % width
        a[m.index] = v[i:i+width]

    else:
        v = a[:, m.index]
        v = np.concatenate((v, v))
        i = -m.distance % height
        a[:, m.index] = v[i:i+height]

    deltas[(m.axis+1) % 2] += m.distance
    move_list.append(m)
    return a, deltas


def anorm(a):
    return tuple(a.flatten())

# ------------------------------------------------problem parts


def field_move(bd, from_cell, to_cell):  # from hold value we want at to_cell location
    if from_cell == to_cell:
        return bd

    corrections = []  # moves to do after to correct for vertical moves
    if to_cell[ROW] == from_cell[ROW]:  # on same row
        bd, deltas = do_move(bd, Move(COL, from_cell[COL], 1))  ## move 1 down
        from_cell[ROW] += deltas[ROW]
        corrections.append(Move(COL, from_cell[COL], -1))  # move 1 up later

    target_set= list(set(range(width)) - set([to_cell[COL]]))
    rand_col = choice(target_set)
    dist = rand_col - from_cell[COL]
    # print(f"to:{to_cell[COL]} from:{from_cell[COL]} w:{width}")
    # print(list(range(first, first+width)), f"dist: {dist}")


    if dist != 0:
        move = Move(ROW, from_cell[ROW], dist)  # move 1 right
        bd, deltas = do_move(bd, move)
        from_cell[COL] = (from_cell[COL] + deltas[COL]) % width

    dist = to_cell[ROW] - from_cell[ROW]
    bd, deltas = do_move(bd, Move(COL, to_cell[COL], -dist))  # move target down

    corrections.append(Move(COL, to_cell[COL], dist))

    bd, deltas = do_move(bd, Move(ROW, from_cell[ROW], to_cell[COL] - from_cell[COL]))  # move value to target col

    while corrections:
        bd, deltas = do_move(bd, corrections.pop())
    return bd

def last_two(s, goal):  # only do two rows,  normalize visited to shift so largest is right most
    last_row = list(s[-1])
    for i in range(1, width - 1):
        goal_prev, target_chr = goal[-1, i - 1:i + 1]
        g0 = goal[-1, 0]
        ip = list(last_row).index(goal_prev)
        ix = (ip + 1) % width
        xv = s[-1, ix]  # value to replace
        it = list(s[-1]).index(target_chr)
        ov = s[-2][-1]

        left_twist = g0 == last_row[(it + 1) % width]

        # print(f" it:{it}-> '{chr(tv)}' {tv} ix:{ix} -> {chr(xv)}' {xv}")

        if ix == it:
            continue
        if left_twist:
            delta = -it
        else:
            delta = width - 2 - it
        s, _ = do_move(s, Move(ROW, -1, delta))
        s, _ = do_move(s, Move(COL, -1, 1))  # move last col down (original)
        delta = -1 if left_twist else 1
        s, _ = do_move(s, Move(ROW, -1, delta))  # move last left or right
        s, _ = do_move(s, Move(COL, -1, -1))  # move last col up
        delta = width - list(s[-1]).index(xv) - 1
        s, _ = do_move(s, Move(ROW, -1, delta))  # move place under last col
        s, _ = do_move(s, Move(COL, width - 1, 1))  # move down
        delta = width - list(s[-1]).index(ov) - 1
        s, _ = do_move(s, Move(ROW, -1, delta))  # move place under last col
        s, _ = do_move(s, Move(COL, width - 1, -1))  # move original up

        last_row = list(s[-1])
        # print(f"last row parity: {parity(s[-1)}")
        if debug:
            bprint(s, f"for final pos {i}")
            #bprint(goal, "goal")

    # shift into final position
    delta = last_row.index(goal[-1, 0])
    if delta != 0:
        s, _ = do_move(s, Move(ROW, -1, -delta))
    return s


#------------------------------------------------

def loopover(mixed, solution):  # return list of moves [ "L1", "R2", "U1", "D3"] or None
    global height, width, move_list
    if debugo:
        print(f"({mixed},\n  {solution})")
    if mixed == solution:
        if debug:
            print('SUCCESS, goal is same a mixed')
            print("mixed", mixed)
            print("goal", solution)
        return []

    start_board, goal_board, bd_shape, c_map = convert_input(mixed, solution)
    height, width = bd_shape

    if debug:
        bprint(start_board, "start board")
        # bprint(goal_board, "goal")

    for _ in range(10):
        move_list = []

        cb = start_board.copy()
        cb, _ = do_move(cb, Move(ROW, randrange(height), choice(range(1,width+1))))
        cb, _ = do_move(cb, Move(COL, randrange(width),  choice(range(1, height+1))))
        cb, _ = do_move(cb, Move(ROW, randrange(height), choice(range(1, width+1))))
        cb, _ = do_move(cb, Move(COL, randrange(width),  choice(range(1, height+1))))


        for row in range(height):
            cols = list(range(width))
            # shuffle(cols)
            for col in cols:
                if (cb == goal_board).all():
                    break
                #print(f"---row:{row} col: {col} letter: {goal_board[row,col]}")

                target = (row, col)
                v = goal_board[row, col]
                from_cell = find_cell(v, cb)
                if cb[row][col] != v:
                    if row < height - 1:  # middle rows solve
                        cb = field_move(cb, from_cell, target)
                        if debug:
                            bprint(cb, "field move")

                    else:  # last row use bfs
                        cb = last_two(cb, goal_board)
                        break


        solved = (cb == goal_board).all()
        if solved:
            break

    if solved:
        out_moves = output_moves()
        return out_moves
    else:
        return None
      
      
##########################################
TRANSPOSE_MAP = {"L": "U", "U": "L", "R": "D", "D": "R"}

class Board:
    def __init__(self, mixed, solved):
        self.board = mixed
        self.solved = solved
        self.rows = len(solved)
        self.cols = len(solved[0])
        self.seq = []
    
    def locate(self, char):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == char:
                    return (row, col)
    
    def transpose(self):
        self.board = [[row[col] for row in self.board]
                      for col in range(len(self.board[0]))]
    
    def left(self, row, a=True):
        self.board[row] = self.board[row][1:] + self.board[row][:1]
        if a:
            self.seq.append(f"L{row}")
    
    def right(self, row, a=True):
        self.board[row] = self.board[row][-1:] + self.board[row][:-1]
        if a:
            self.seq.append(f"R{row}")
    
    def up(self, col):
        self.transpose()
        self.left(col, False)
        self.transpose()
        self.seq.append(f"U{col}")
    
    def down(self, col):
        self.transpose()
        self.right(col, False)
        self.transpose()
        self.seq.append(f"D{col}")
    
    def f2l(self):
        for row in range(self.rows):
            for col in range(self.cols - 1):
                char = self.solved[row][col]
                coords = self.locate(char)
                if coords[0] == row:
                    count = 0
                    while self.locate(char)[1] != self.cols - 1:
                        self.left(row)
                        count += 1
                    if count:
                        self.up(self.cols - 1)
                        for _ in range(count):
                            self.right(row)
                        self.down(self.cols - 1)
                while self.locate(char)[1] != self.cols - 1:
                    self.left(coords[0])
                while self.locate(char)[0] != row:
                    self.up(self.cols - 1)
                self.left(row)
    
    def sune(self):
        self.right(self.rows - 1)
        self.down(self.cols - 1)
        self.left(self.rows - 1)
        self.down(self.cols - 1)
        self.right(self.rows - 1)
        self.up(self.cols - 1)
        self.up(self.cols - 1)
        self.left(self.rows - 1)
    
    def ll(self):
        layer = [row[-1] for row in self.board]
        solved_layer = [row[-1] for row in self.solved]
        swaps = 0
        for i in range(self.rows):
            if layer[i] != solved_layer[i]:
                j = layer.index(solved_layer[i])
                layer[i], layer[j] = layer[j], layer[i]
                swaps += 1
        if swaps % 2: # parity
            if self.rows % 2: # unsolvable
                self.seq = []
                return
            else: # parity alg
                self.up(self.cols - 1)
        for row in range(self.rows - 2):
            char = self.solved[row][-1]
            while self.locate(char)[0] != row:
                if self.locate(char)[0] == self.rows - 1:
                    self.sune()
                    continue
                count = 0
                while self.locate(char)[0] != self.rows - 2:
                    self.down(self.cols - 1)
                    count += 1
                self.sune()
                for _ in range(count):
                    self.up(self.cols - 1)
    
    def solve(self):
        self.f2l()
        self.ll()

def transpose(board):
    return [[row[col] for row in board]
            for col in range(len(board[0]))]

def loopover(mixed_up_board, solved_board):
    rows = len(solved_board)
    cols = len(solved_board[0])
    if rows % 2 == 1 and cols % 2 == 0:
        # transpose to ensure last layer can perform parity alg
        board = Board(transpose(mixed_up_board), transpose(solved_board))
        board.solve()
        if board.seq:
            return [TRANSPOSE_MAP[move[0]] + move[1:] for move in board.seq]
    else:
        board = Board(mixed_up_board, solved_board)
        board.solve()
        if board.seq:
            return board.seq
          
          
#########################################
def loopover(mixed, solved):
    def slide(X,i,j):
        X[0][0], X[0][1], X[i][j] = X[0][1], X[i][j], X[0][0]
    def index_of_O(marked):
        for i in range(len(marked)):
            for j in range(len(marked[0])):
                if marked[i][j] == 'O': return [True, (i,j)]
        return [False, None]
    move = lambda i, j: [[*len(mixed[0]) // 2 * ['R0', 'U0', 'R0', 'D0'], 'U0', 'R0', 'D0'],
                         [*len(mixed) // 2 * ['D0', 'L0', 'D0', 'R0'], 'D0']] if (i,j)==(-1,-1) \
        else [[*j * [f'L{i}'], 'L0', *i * ['U0'], 'R0', *i * ['D0'], *j * [f'R{i}']],
                         [f'D{j}', *j * ['L1'], 'L0', 'U0', 'R0', 'D0', *j * ['R1'], f'U{j}']]
    targetedPositions = {val: (i, j) for (i, row) in enumerate(solved) for (j, val) in enumerate(row)}
    targetedShifts = [[targetedPositions[val] for (j, val) in enumerate(row)] for (i, row) in enumerate(mixed)]
    marked, moves = [['O' if targetedShifts[i][j] != (i, j) and (i, j) not in ((0, 0), (0, 1))
               else 'X' for j in range(len(solved[0]))] for i in range(len(solved))], []
    while index_of_O(marked)[0]:
        (i, j) = index_of_O(marked)[1] if targetedShifts[0][0] in ((0, 0), (0, 1)) else targetedShifts[0][0]
        moves += move(i,j)[0] if i else move(i,j)[1]
        slide(targetedShifts, i, j)
        if targetedShifts[i][j] == (i, j): marked[i][j] = 'X'
    if targetedShifts[0][0] != (0, 0):
        if len(mixed) % 2 and len(mixed[0]) % 2: return None
        else: moves += move(-1,-1)[0] if len(mixed) % 2 else move(-1,-1)[1]
    return moves
  
######################################
import numpy as np


def move(board, direction, ind, all_moves):
    if direction == "R":
        board[ind] = np.array([board[ind][-1]] + board[ind][:-1].tolist())
    elif direction == "L":
        board[ind] = np.array(board[ind][1:].tolist() + [board[ind][0]])
    elif direction == "D":
        board[:, ind] = np.array([board[:, ind][-1]] + board[:, ind][:-1].tolist())
    elif direction == "U":
        board[:, ind] = np.array(board[:, ind][1:].tolist() + [board[:, ind][0]])
    all_moves.append(f"{direction}{ind}")


def last_row(board, all_moves):
    all_values = sorted(board[-1].tolist())
    x, y = np.argwhere(board == all_values[0])[0]
    last_correct = 0
    for _ in range(y):
        move(board, "L", board.shape[0]-1, all_moves)

    for j, i in enumerate(all_values[1:]):
        x, y = np.argwhere(board == i)[0]
        if x * board.shape[1] + y == i:
            last_correct = board[-1].tolist().index(i)
            continue

        align = board.shape[1] - 1 - y
        diff = y - last_correct - 1
        for _ in range(align):
            move(board, "R", board.shape[0]-1, all_moves)
        move(board, "U", board.shape[1]-1, all_moves)
        for _ in range(diff):
            move(board, "R", board.shape[0]-1, all_moves)
        move(board, "D", board.shape[1]-1, all_moves)
        for _ in range(diff + align):
            move(board, "L", board.shape[0]-1, all_moves)
        if board.shape[1]-1 in board[-1]:
            buf = board[-1].tolist().index(board.shape[1]-1)
        else:
            return False
        move(board, "U", board.shape[1]-1, all_moves)
        fix = board.shape[1]-1 - buf
        for _ in range(fix):
            move(board, "R", board.shape[0]-1, all_moves)
        move(board, "D", board.shape[1]-1, all_moves)
        for _ in range(fix):
            move(board, "L", board.shape[0]-1, all_moves)
        if i in board[-1]:
            last_correct = board[-1].tolist().index(i)
        else:
            if board[0][-1] == board.shape[1]*board.shape[0] - 1 and board[-1][-1] == board.shape[1]-1:
                if not (not board.shape[0] % 2 and board.shape[1] % 2):
                    for i in range(board.shape[1]//2 + (1 - board.shape[1] % 2)):
                        move(board, "D", board.shape[1]-1, all_moves)
                        if all([sorted(row.tolist()) == row.tolist() for row in board]):
                            return all_moves
                        move(board, "L", 0, all_moves)
                        move(board, "U", board.shape[1]-1, all_moves)
                        move(board, "L", 0, all_moves)
                    move(board, "R", 0, all_moves)
                else:
                    move(board, "R", board.shape[0]-1, all_moves)
                    move(board, "U", board.shape[1]-1, all_moves)
                    move(board, "L", board.shape[0]-1, all_moves)
                    move(board, "D", board.shape[1]-1, all_moves)
                    move(board, "R", board.shape[0]-1, all_moves)
                    for i in range(board.shape[0]//2):
                        move(board, "L", board.shape[0]-1, all_moves)
                        move(board, "U", board.shape[1]-1, all_moves)
                        move(board, "R", board.shape[0]-1, all_moves)
                        move(board, "U", board.shape[1]-1, all_moves)
                    move(board, "L", board.shape[0]-1, all_moves)
                    move(board, "U", board.shape[1]-1, all_moves)
            for row in board:
                if sorted(row.tolist()) != row.tolist():
                    return False
            return all_moves
    return all_moves

def loopover(mixed_up_board, solved):
    board = mixed_up_board
    solved = np.array(solved)
    values = {solved[j][i]: j*solved.shape[1]+i for j in range(solved.shape[0]) for i in range(solved.shape[1])}
    for j in range(solved.shape[0]):
        for i in range(solved.shape[1]):
            board[j][i] = values[board[j][i]]
    board = np.array(board)
    moves = []
    current_row = 0
    for i in values.values():
        if i // board.shape[1] == board.shape[0]-1:
            break
        x, y = np.argwhere(board == i)[0]

        if x * board.shape[1] + y == i:
            if i % board.shape[1] == board.shape[1]-1:
                current_row += 1
            continue
        row_difference = x - current_row
        col_difference = y - i % board.shape[1]

        if x == current_row:
            move(board, "D", y, moves)
            move(board, "R", current_row+1, moves)
            move(board, "U", y, moves)
            move(board, "L", current_row+1, moves)
            move(board, "D", i % board.shape[1], moves)
            for _ in range(abs(col_difference)):
                move(board, "L" if col_difference > 0 else "R", current_row+1, moves)
            move(board, "U", i % board.shape[1], moves)
        else:
            if y != i % board.shape[1]:
                for _ in range(abs(row_difference)):
                    move(board, "D", i % board.shape[1], moves)
                for _ in range(abs(col_difference)):
                    move(board, "L" if col_difference > 0 else "R", x, moves)
                for _ in range(abs(row_difference)):
                    move(board, "U", i % board.shape[1], moves)
            else:
                move(board, "L", x, moves)
                for _ in range(abs(row_difference)):
                    move(board, "D", i % board.shape[1], moves)
                move(board, "R", x, moves)
                for _ in range(abs(row_difference)):
                    move(board, "U", i % board.shape[1], moves)

        if i % board.shape[1] == board.shape[1]-1:
            current_row += 1

    if board[-1].tolist() == sorted(board[-1].tolist()):
        return moves
    if last_row(board, moves):
        return moves
    return None
  
#################################################
def loopover(m,s):
    def f(liste,n):
        for i in range(0,len(liste)):
            if liste[i]==n:
                return i
    if m==s:
        return []
    moves=[]
    def move(m,kord,retning):
        a=["L","R"]
        if retning in a:
            k=m[kord[0]]
            c=[]
            if retning=="L":
                for i in range(1,len(k)):
                    c.append(k[i])
                c.append(k[0])
                m[kord[0]]=c
                return m
            else:
                c.append(k[len(k)-1])
                for i in range(0,len(k)-1):
                    c.append(k[i])
                m[kord[0]]=c
                return m
        else:
            p=len(m)
            z=[]
            x=[]
            for i in range(0,p):
                z.append(m[i][kord[1]])
            if retning=="U":
                for i in range(1,len(z)):
                    x.append(z[i])
                x.append(z[0])
                for i in range(0,len(x)):
                    m[i][kord[1]]=x[i]
                return m
            else:
                x.append(z[len(z)-1])
                for i in range(0,len(z)-1):
                    x.append(z[i])
                for i in range(0,len(x)):
                    m[i][kord[1]]=x[i]
                return m
    a=len(m)
    b=len(m[0])
    for i in range(0,a-1):
        for j in range(0,b-1):
            
            vv=0
            if not m[i][j]==s[i][j]:
                for k in range(0,a):
                    for g in range(0,b):
                        if m[k][g]==s[i][j]:
                            if vv==0:
                                vv=1
                                if j ==0:
                                    
                                    if i==k:
                                        
                                        for q in range(0,g):
                                            m=move(m,[i,0],"L")
                                            moves.append("L"+str(i))
                                        
                                    else:
                                        if g==b-1:
                                            if i < k:
                                                for q in range(i,k):
                                                    m=move(m,[0,g],"U")
                                                    moves.append("U"+str(g))
                                                for aq in range(0,g):
                                                    m=move(m,[i,0],"L")
                                                    moves.append("L"+str(i))
                                            else:
                                                for q in range(k,i):
                                                    m=move(m,[0,g],"D")
                                                    moves.append("D"+str(g))
                                                for aq in range(0,g):
                                                    m=move(m,[i,0],"L")
                                                    moves.append("L"+str(i))
                                        else:
                                            for q in range(g,b-1):
                                                m=move(m,[k,0],"R")
                                                moves.append("R"+str(k))
                                            for q in range(i,k):
                                                m=move(m,[0,b-1],"U")
                                                moves.append("U"+str(b-1))
                                            for q in range(0,b-1):
                                                m=move(m,[i,0],"L")
                                                moves.append("L"+str(i))
                                else:
                                    if i==k:
                                        for q in range(0,j):
                                            m=move(m,[0,q],"U")
                                            moves.append("U"+str(q))
                                        for q in range(j,g):
                                            m=move(m,[i,0],"L")
                                            moves.append("L"+str(i))
                                        for q in range(0,j):
                                            m=move(m,[0,q],"D")
                                            moves.append("D"+str(q))
                                    else:
                                        if g==b-1:
                                            if i>k:
                                                for q in range(k,i):
                                                    m=move(m,[0,g],"D")
                                                    moves.append("D"+str(g))
                                                for q in range(0,j):
                                                    m=move(m,[0,q],"U")
                                                    moves.append("U"+str(q))
                                                for q in range(j,g):
                                                    m=move(m,[i,0],"L")
                                                    moves.append("L"+str(i))
                                                for q in range(0,j):
                                                    m=move(m,[0,q],"D")
                                                    moves.append("D"+str(q))
                                            else:
                                                for q in range(i,k):
                                                    m=move(m,[0,g],"U")
                                                    moves.append("U"+str(g))
                                                for q in range(0,j):
                                                    m=move(m,[0,q],"U")
                                                    moves.append("U"+str(q))
                                                for q in range(j,g):
                                                    m=move(m,[i,0],"L")
                                                    moves.append("L"+str(i))
                                                for q in range(0,j):
                                                    m=move(m,[0,q],"D")
                                                    moves.append("D"+str(q))
                                        else:
                                            for q in range(g,b-1):
                                                m=move(m,[k,0],"R")
                                                moves.append("R"+str(k))
                                            
                                            for q in range(i,k):
                                                m=move(m,[0,b-1],"U")
                                                moves.append("U"+str(b-1))
                                            for q in range(0,j):
                                                m=move(m,[0,q],"U")
                                                moves.append("U"+str(q))
                                            for q in range(j,b-1):
                                                m=move(m,[i,0],"L")
                                                moves.append("L"+str(i))
                                            for q in range(0,j):
                                                m=move(m,[0,q],"D")
                                                moves.append("D"+str(q))
    def høyre(m):
        zx=len(m[0])
        zz=[]
        for i in range(0,len(m)):
            zz.append(m[i][zx-1])
        return zz
        
    def nederste(m):
        return m[len(m)-1]
    yy=høyre(s)[0:len(høyre(m))-2]
    xx=nederste(s)[0:len(nederste(s))-2]
    
    for q in range(0,len(yy)):
        if q==0:
            if not høyre(m)[q]==yy[q]:
                if yy[q] in høyre(m):
                    for ass in range(0,f(høyre(m),yy[q])):
                        m=move(m,[0,b-1],"U")
                        moves.append("U"+str(b-1))
                else:
                    
                    for ass in range(f(nederste(m),yy[q]),b-1):
                        m=move(m,[a-1,0],"R")
                        moves.append("R"+str(a-1))
                    for ass in range(0,a-1):
                        m=move(m,[a-1,b-1],"U")
                        moves.append("U"+str(b-1))
        
        else:
            
            
            if not høyre(m)[q]==yy[q]:
                if yy[q] in høyre(m):
                    cv=f(høyre(m),yy[q])
                    for w in range(cv,a-1):
                        m=move(m,[0,b-1],"D")
                        moves.append("D"+str(b-1))
                    m=move(m,[a-1,0],"L")
                    moves.append("L"+str(a-1))
                    for w in range(0,cv-q):
                        m=move(m,[0,b-1],"D")
                        moves.append("D"+str(b-1))
                    m=move(m,[a-1,b-1],"R")
                    moves.append("R"+str(a-1))
                    for w in range(q,a-1):
                        m=move(m,[a-1,b-1],"U")
                        moves.append("U"+str(b-1))
                else:
                
                    for w in range(q,a-1):
                        m=move(m,[0,b-1],"D")
                        moves.append("D"+str(b-1))
                    cv=f(nederste(m),yy[q])
                    for w in range(cv,b-1):
                        m=move(m,[a-1,0],"R")
                        moves.append("R"+str(a-1))
                    for w in range(q,a-1):
                        m=move(m,[a-1,b-1],"U")
                        moves.append("U"+str(b-1))
    for q in range(0,len(xx)):
        if not xx[q]==nederste(m)[q]:
            if q==0:
                if xx[q] in nederste(m):
                    cv=f(nederste(m),xx[q])
                    for w in range(0,cv):
                        m=move(m,[a-1,0],"L")
                        moves.append("L"+str(a-1))
                else:
                    m=move(m,[a-1,b-1],"D")
                    moves.append("D"+str(b-1))
                    for w in range(0,b-1):
                        m=move(m,[a-1,0],"L")
                        moves.append("L"+str(a-1))
                    m=move(m,[a-1,b-1],"U")
                    moves.append("U"+str(b-1))
            else:
                
                if xx[q] in nederste(m):
                    cv=f(nederste(m),xx[q])
                    
                    
                    for w in range(cv,b-1):
                        m=move(m,[a-1,0],"R")
                        moves.append("R"+str(a-1))
                    
                        
                    m=move(m,[a-1,b-1],"D")
                    moves.append("D"+str(b-1))
                    
                    for w in range(q-cv+b-1,b-1):
                
                        m=move(m,[a-1,0],"R")
                        moves.append("R"+str(a-1))
                    m=move(m,[a-1,b-1],"U")
                    moves.append("U"+str(b-1))
                    for w in range(q,b-1):
                        
                        m=move(m,[a-1,0],"L")
                        moves.append("L"+str(a-1))
                    
                
                else:
                    
                    for w in range(q,b-1):
                        m=move(m,[a-1,0],"R")
                        moves.append("R"+str(a-1))
                    m=move(m,[0,b-1],"D")
                    moves.append("D"+str(b-1))
                    for w in range(q,b-1):
                        m=move(m,[a-1,0],"L")
                        moves.append("L"+str(a-1))
                    m=move(m,[0,b-1],"U")
                    moves.append("U"+str(b-1))
    ok=["R","D","L","U"]
    oki=["D","L","U","L"]
    bee=["R","U","L","U"]
    bee=bee+bee+bee+bee+bee+bee+bee+bee
    bee=bee+bee
    bee=bee+bee
    oki=oki+oki
    oki=oki+oki
    oki=oki+oki
    oki=oki+oki
    oki=oki+oki
    oki=oki+oki
    oki=oki+oki
    oki=oki+oki
    oki=oki+oki
    
    
    def gh(liste):
        a=[]
        for i in range(0,len(liste)):
            b=[]
            for j in range(0,len(liste[0])):
                b.append(liste[i][j])
            a.append(b)
        return a
    def gx(liste):
        for i in range(0,len(m)):
            for j in range(0,len(m[0])):
                if not [i,j]==[a-1,b-1]:
                    if not [i,j]==[a-1,b-2]:
                        if not m[i][j]==s[i][j]:
                            return False
        return True
            
    
    k2=0
    
    if m==s:
        return moves
    def g(m):
        for i in range(0,len(m)):
            for j in range(0,len(m[0])):
                if not [i,j]==[a-1,b-1]:
                    if not [i,j]==[a-2,b-1]:
                        if not m[i][j]==s[i][j]:
                            return False
        return True
                        
                        

        
    if g(m)==True:
        
        kok=gh(m)
        
        
        for i in range(0,len(oki)):
            
            m=move(m,[a-1,b-1],oki[i])
            if i%2==0:
                moves.append(oki[i]+str(b-1))
            else:
                moves.append(oki[i]+str(a-1))
            if m==kok:
                k2=1
                break
                
                
            if m==s:
                return moves
    fs=0
    
    for j in range(0,2):
        if fs==1:
            break
        for k in range(0,4):
            m=move(m,[a-1,b-1],ok[k])
            if k%2==0:
                moves.append(ok[k]+str(a-1))
            else:
                moves.append(ok[k]+str(b-1))
            if g(m)==True:
                fs=1
                break
    if m==s:
        return moves
    if g(m)==True:
        
        
        kok=gh(m)
        
        for i in range(0,len(oki)):
            m=move(m,[a-1,b-1],oki[i])
            
            
            if i%2==0:
                moves.append(oki[i]+str(b-1))
            else:
                moves.append(oki[i]+str(a-1))
            if m==s:
                return moves
            if m==kok:
                k2=1
                break
    if k2==1:
        if len(m)%2==0:
            for j in range(0,3):
                
                if gx(m)==True:
                    break
                
                for k in range(0,4):
                    m=move(m,[a-1,b-1],ok[k])
                    if k%2==0:
                        moves.append(ok[k]+str(a-1)) 
                    else:
                        moves.append(ok[k]+str(b-1))
                    
            kok=gh(m)
            for ol in range(0,len(bee)):
                m=move(m,[a-1,b-1],bee[ol])
                if ol%2==0:
                    moves.append(bee[ol]+str(a-1))
                else:
                    moves.append(bee[ol]+str(b-1))
                if m==kok:
                    return None
                if m==s:
                    return moves
            
             
                
            
            
        else:
            return None
    return moves
