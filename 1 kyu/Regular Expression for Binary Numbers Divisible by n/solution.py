from collections import defaultdict


def regex_divisible_by(n):
    states = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for i in range(n):
        states[i][True][i * 2 % n].append('0')
        states[i * 2 % n][False][i].append('0')

        states[i][True][(i * 2 + 1) % n].append('1')
        states[(i * 2 + 1) % n][False][i].append('1')

    for i in range(n, -1, -1):
        star = ''
        if i in states[i][True]:
            star = '(?:{})*'.format('|'.join(states[i][True][i]))
            states[i][True].pop(i)
            states[i][False].pop(i)

        for from_state, from_labels in states[i][False].items():
            from_labels = ('(?:{})' if len(from_labels) > 1 else '{}').format('|'.join(from_labels))
            for to_state, to_labels in states[i][True].items():
                new_label = from_labels + star + ('(?:{})' if len(to_labels) > 1 else '{}').format('|'.join(to_labels))
                states[from_state][True][to_state].append(new_label)
                states[to_state][False][from_state].append(new_label)
        for from_state in states[i][False]:
            states[from_state][True].pop(i)
        for to_state in states[i][True]:
            states[to_state][False].pop(i)
        states.pop(i)
    return '^{}$'.format(star)
  
###############
def regex_divisible_by(n):
    if n==1:
        return '^[01]*$'
    G = {(i,(2*i+j)%n):str(j) for i in range(n) for j in (0,1)}
    for k in range(n-1,0,-1):
        loop = '' if (k,k) not in G else G[(k,k)]+'*'
        I = {i for i,j in G if i!=k and j==k}
        J = {j for i,j in G if i==k and j!=k}
        for i in I:
            for j in J:
                if (i,j) in G:
                    G[(i,j)] = '(?:%s|%s)' % (G[(i,j)], G[(i,k)]+loop+G[(k,j)])
                else:
                    G[(i,j)] = '(?:%s)' % (G[(i,k)]+loop+G[(k,j)])
        G = {c:G[c] for c in G if k not in c}
    return '^%s*$' % G[(0,0)]

#############
class Node(object):
    def __init__(self, val, n0=None, n1=None):
        self.val = val
        self.next = [n0, n1]
    
    def link(self, lst):        self.next = lst
    
    def __hash__(self):         return self.val
    def __repr__(self):         return "Node({})".format(self.val)
    def __eq__(self, other):    return isinstance(other,Node) and self.val == other.val
    def __getitem__(self, i):   return self.next[i]
    


def regex_divisible_by(n):
    lNodes = [Node(x) for x in range(n)]                                # create the nodes
    for i,nod in enumerate(lNodes):                                     # link the nodes
        nod.link([ lNodes[(i*2) % n], lNodes[(i*2+1) % n] ])
    
    return '^' + getRegexFromGraph(lNodes[0], '', set()).popitem()[1][0] + '$'
    
    
def getRegexFromGraph(nod, bit, seensInBranch):
    
    if nod in seensInBranch:
        return {nod: [bit]}
    
    treeReg = {}
    for i in range(2):
        dct = getRegexFromGraph(nod.next[i], str(i), seensInBranch | {nod})
        for child,lst in dct.items():
            if child not in treeReg: treeReg[child] = []
            treeReg[child].extend(lst)
    
    reduced = ''
    if nod in treeReg:                                                  # Current node match one of the stored extremities: found a loop
        lstReg  = treeReg.pop(nod)                                      #   Remove the current extremity
        sBit    = '|'.join(lstReg)                                      
        reduced = ("{}*" if len(sBit)==1 else"(?:{})*").format(sBit)    #   loop pattern

    for ext,lst in treeReg.items():                                     # Add the reduced loop (if exists) and the current bit to each reg string for each branch (order: loop + current bit + way to the extremity)
        treeReg[ext] = [ bit + reduced + ("{}" if len(lst)==1 else"(?:{})").format("|".join( s for s in lst)) ]
    
    if not treeReg: treeReg[nod] = [bit+reduced]
    
    return treeReg
  
#############
from collections import defaultdict

class DFA(object):
    def __init__(self, states, start_state, accepted_states):
        self.states = set(states)
        self.start_state = 'START_STATE'
        self.end_state = 'END_STATE'
        self.transitions = dict()
        self.add_transition(self.start_state, start_state, '')
        for accepted_state in accepted_states:
            self.add_transition(accepted_state, self.end_state, '')

    def add_transition(self, from_, to, trans):
        self.transitions[(from_, to)] = trans
        
    def select_state(self):
        """Select the state with the smallest impact when reduced."""
        from_count = defaultdict(int)
        to_count = defaultdict(int)
        for from_, to in self.transitions:
            if from_ != to:
                from_count[from_] += 1
                to_count[to] += 1
        return min(self.states, key=lambda state: from_count[state] * to_count[state])
        
    def reduce_state(self, state):
        entering = dict()
        exiting = dict()
        loop = None
        for (from_, to), trans in list(self.transitions.items()):
            if from_ == to == state:
                loop = trans
            elif to == state:
                entering[from_] = trans
            elif from_ == state:
                exiting[to] = trans
            if state in (from_, to):
                del self.transitions[(from_, to)]
        loop_trans = '' if loop is None else '(?:{})*'.format(loop)
        for enter_state, enter_trans in entering.items():
            for exit_state, exit_trans in exiting.items():
                if (enter_state, exit_state) in self.transitions:
                    format_ = '(?:{}|{{}})'.format(self.transitions[(enter_state, exit_state)])
                else:
                    format_ = '{}'
                trans = '{}{}{}'.format(enter_trans, loop_trans, exit_trans)
                trans = format_.format(trans)
                self.add_transition(enter_state, exit_state, trans)
        self.states.remove(state)
    
    def reduce(self):
        while self.states:
            state = self.select_state()
            self.reduce_state(state)
        return self.transitions[(self.start_state, self.end_state)]

def generate_regex(n):
    if n == 1:
        return '1[01]*'
    dfa = DFA(range(n), 0, {0})
    for i in range(n):
        dfa.add_transition(i, i * 2 % n, '0')
        dfa.add_transition(i, (i * 2 + 1) % n, '1')
    return dfa.reduce()
    
def regex_divisible_by(n):
    start = '^(0|'
    end = ')$'
    while n % 2 == 0:
        end = '0' + end
        n //= 2
    return '{}{}{}'.format(start, generate_regex(n), end)
  
#####################
def dfa(n):
    return {r: {(r*2)%n: '0', (r*2+1)%n: '1'} for r in range(n)}

def dfa2regex(d):
    m = len(d) - 1
    if m == 0:
        return '^(%s)+$' % d[0][0]
    def sub(s, e):
        sme = d[s][m] + ('(?:%s)*' % d[m][m] if m in d[m] else '') + d[m][e]
        return '(?:%s|%s)' % (d[s][e], sme) if e in d[s] else sme
    def link(s, e):
        return sub(s, e) if m in d[s] and e in d[m] else d[s][e]
    def ends(s):
        return set(d[s]) | (set(d[m]) if m in d[s] else set())
    def node(s):
        return {e: link(s, e) for e in ends(s) if e != m}
    return dfa2regex({s: node(s) for s in d if s != m})

def regex_divisible_by(n):
    return dfa2regex(dfa(n)) if n > 1 else '^[10]+$'
  
#####################
def reduce_nodes(dfa):
    n = len(dfa)
    for i in range(n):
        if not dfa[i][n-1]: continue
        for j in range(n):
            if not dfa[n-1][j]: continue
            if not dfa[i][j] and not dfa[n-1][n-1]:
                dfa[i][j] = '(?:' + dfa[i][n-1] + ')(?:' + dfa[n-1][j] + ')'
            elif not dfa[i][j]:
                dfa[i][j] = '(?:' + dfa[i][n-1] + ')(?:' + dfa[n-1][n-1] + ')*(?:' + dfa[n-1][j] + ')'
            elif not dfa[n-1][n-1]:
                dfa[i][j] = '(?:' + dfa[i][j] + ')|(?:' + dfa[i][n-1] + ')(?:' + dfa[n-1][j] + ')'
            else:
                dfa[i][j] = '(?:' + dfa[i][j] + ')|(?:(?:' + dfa[i][n-1] + ')(?:' + dfa[n-1][n-1] + ')*(?:' + dfa[n-1][j] + '))'
    del dfa[n-1]
            

def make_dfa(n):
    dfa = {}
    for i in range(n):
        dfa[i] = ['']*n
        dfa[i][(2*i) % n] = '0'
        dfa[i][(2*i+1) % n] = '1'
    return dfa


def regex_divisible_by(n):
    if n==1: return '^(0|1)+$'
    dfa = make_dfa(n)
    for i in range(n-1):
        reduce_nodes(dfa)
    return '^('+dfa[0][0]+')+$'
  
######################
import numpy as np
res = dict()

def regex_divisible_by(n):
    # Define L[i], the language of binary numbers that are i modulo n
    # The language to determine is L[0].
    # We have the following equations
    # L[i] 0 -> L[2**i[n]]
    # L[i] 1 -> [2**i+1[n]]
    if n in res:
        return res[n]
    mdl = np.arange(n)
    zer = (2*mdl.copy()) % n
    one = (2*mdl.copy()+1) % n

    language_equations = [{} for i in range(n)]
    for i in mdl:
        if one[i] == zer[i]:
            language_equations[i][one[i]] = "(?:0|1)"
        else:
            language_equations[i][zer[i]] = "0"
            language_equations[i][one[i]] = "1"

    # now we have the automata, we need to compute the corresponding regular expression:
    #
    # we use Arden's Lemma¹:
    # Let L,U,V⊆Σ∗ regular languages with ε∉U. Then,
    # L=UL∪V⟺L=U∗V

    for k in mdl[::-1]:
        to_replace = language_equations[k]
        if k in to_replace:
            special_prefix = "(?:{expr})*".format(expr=to_replace.pop(k))
        else:
            special_prefix = ""

        for j in range(k):
            cur_dic = language_equations[j]
            if k in cur_dic:
                prefix = cur_dic.pop(k)
                full_prefix = prefix + special_prefix
                for l in to_replace:
                    if l in cur_dic:
                        cur_dic[l] = "(?:{a}|{b})".format(a=cur_dic[l], b=full_prefix + to_replace[l])
                    else:
                        cur_dic[l] = full_prefix + to_replace[l]

    res[n] =  "^" + special_prefix + "$"
    return res[n]
  
##################
def init(n):
    table = []
    for i in range(n):
        table.append([None for _ in range(n)])

        bin_str = bin(i)[2:]

        zero_node = int(bin_str+'0', 2) % n
        one_node = int(bin_str+'1', 2) % n

        table[i][zero_node] = '0'
        table[i][one_node] = '1'

    return table


def getRes(n, table):
    if n == 0:
        return table

    for cur in filter(lambda x: table[x][n], range(n)):
        if table[n][n]:
            for aim in filter(lambda x: x != n and table[n][x], range(n)):
                if table[cur][aim]:
                    table[cur][aim] = ''.join(['(?:', table[cur][aim], ')|(?:(?:', table[cur][n], ')(?:',
                                               table[n][n], ')*(?:', table[n][aim], '))'])
                else:
                    table[cur][aim] = ''.join(['(?:', table[cur][n], ')(?:', table[n][n], ')*(?:',
                                               table[n][aim], ')'])
        else:
            for aim in filter(lambda x: table[n][x], range(n)):
                if table[cur][aim]:
                    table[cur][aim] = ''.join(['(?:', table[cur][aim], ')|(?:', table[cur][n], ')(?:',
                                               table[n][aim], ')'])
                else:
                    table[cur][aim] = ''.join(['(?:', table[cur][n], ')(?:', table[n][aim],
                                               ')'])

    return getRes(n-1, table)


def regex_divisible_by(n):
    if n == 1:
        return '^[01]*$'

    table = init(n)
    res = getRes(n-1, table)

    return ''.join(['^(?:', res[0][0], ')+$'])

###################
def star(x):
    return "(?:"+x+")*" if x else ""

def union(x, y):
    return "(?:"+x+"|"+y+")" if x and y else x or y

def concat(x, y):
    if x is None or y is None: return None
    return x+y if x and y else x or y

def regex_divisible_by(N):
    if N == 1:
        # Make specification of NFA cleaner by hard-coding N=1 case
        return "^[01]+$"

    m = N + 1

    # Construct an NFA that accepts a binary string one digit at a time,
    # then convert it to a regex using Brzozowski's algorithm.

    # Specify N+1 states, corresponding to the initial state
    # and "string up to this point = k mod N" for k=1,2,...,N
    # Note that initial state is 0, and the "0 mod N" case is actually state N.
    B = [ "" if i==N else None for i in range(m) ]

    # Specify transitions from each state corresponding to an extra digit.
    # Note that value k becomes (k*2+0) or (k*2+1) when 0 or 1 is appended.
    A = [ [ None for i in range(N+1) ] for j in range(m) ]
    for i in range(0, m):
        A[i][(2*i+0) % N or N] = "0"
        A[i][(2*i+1) % N or N] = "1"

    for n in range(N, -1, -1):
        B[n] = concat(star(A[n][n]), B[n])
        for j in range(n):
            A[n][j] = concat(star(A[n][n]), A[n][j])
        for i in range(n):
            B[i] = union(B[i], concat(A[i][n], B[n]))
            for j in range(n):
                A[i][j] = union(A[i][j], concat(A[i][n], A[n][j]))
        for i in range(n):
            A[i][n] = None

    return "^" + B[0] + "$"
  
############################
def regex_divisible_by(n):     
    def brzozowski(A, B):
        def star(r):
            if not r:
                return ""
            elif len(r) == 1:
                return r + "*"
            else:
                return "(?:{})*".format(r)
        
        def concat(*rs):
            if any(r is None for r in rs):
                return None
            else:
                return "".join("(?:{})".format(r) for r in rs if r)
        
        def alt(*rs):
            if all(r is None for r in rs):
                return None
            else:
                return "|".join(filter(bool, rs))
        
        for n in reversed(range(1, len(B))):
            for i in range(0, n):
                to_n = concat(A[i][n], star(A[n][n]))
                B[i] = alt(B[i], concat(to_n, B[n]))
                for j in range(0, n):
                    A[i][j] = alt(A[i][j], concat(to_n, A[n][j]))
        return concat(star(A[0][0]), B[0])

    # Decompose n into an odd factor and a power of 2
    j = 0
    while n % 2 == 0:
        n //= 2
        j += 1
    
    r = None
    if n > 1:
        A = [[None for i in range(0,n)] for j in range(0,n)]
        B = [None for i in range(0,n)]
        B[0] = ""
        for i in range(0,n):
            A[i][(i * 2 + 0) % n] = "0"
            A[i][(i * 2 + 1) % n] = "1"
        r = brzozowski(A, B)
    else:
        r = "1"
    return '^(0|(0|({}))+{})$'.format(r, "0" * j)
  
######################
def remove(n, links):
    loop = ''
    if (n, n) in links:  # loop
        loop = "(?:" + links[(n, n)] + ")*"
        del links[(n, n)]
    start = [i for i in links if i[0] == n]
    end = [i for i in links if i[1] == n]
    for i in end:
        for j in start:
            if links.get((i[0], j[1])):
                links[(i[0], j[1])] = '(?:' + links[(i[0], j[1])] + '|' + links[i] + loop + links[j] + ')'
            else:
                links[(i[0], j[1])] = links[i] + loop + links[j]
    return {i: links[i] for i in links if n not in i}


def regex_divisible_by(n):
    links = {}
    for i in range(n):
        for j in range(n):
            if (i * 2) % n == j:
                links[(i, j)] = '0'
            if (i * 2 + 1) % n == j:
                    links[(i, j)] = '1'
    for i in range(n - 1, 0, -1):
        links = remove(i, links)
    if n == 1:
        links[(0,0)] = "1|0"
    solution = '^(' + links[(0,0)] + ')+$'
    return solution
  
######################
def regex_divisible_by(n):
    
    # Construct equations corresponding to the fsm
    eqs = {i : [] for i in range(n)}
    for s in range(n):
        eqs[(s*2) % n].append((s, '0'))
        eqs[(s*2+1) % n].append((s, '1'))


    # Go through the nodes starting at n-1
    for to_elim in range(n-1, 0, -1):

        # Remove self references from to_elim
        all_self = [t for t in eqs[to_elim] if t[0] == to_elim]
        if len(all_self) > 0:
            all_other = [t for t in eqs[to_elim] if t[0] != to_elim]
            all_other_d = {k : [t for t in eqs[to_elim] if t[0] == k] for k in {k for k,_ in eqs[to_elim]}}

            if len(all_self) == 1 and len(all_self[0][1]) == 1:
                star = all_self[0][1] + '*'
            else:
                star = '(?:' + '|'.join(w for _,w in all_self) + ')*'

            for k, nodes in all_other_d.items():
                pre = '(?:' + '|'.join(w for _,w in nodes) + ')' if len(nodes) > 1 else nodes[0][1]
                eqs[to_elim].append((k, pre + star))
                for node in nodes:
                    eqs[to_elim].remove(node)

            eqs[to_elim] = [t for t in eqs[to_elim] if t[0] != to_elim]


        # Substitute into the other equations
        for to_sub in range(to_elim):
            for n_old in [t for t in eqs[to_sub] if t[0] == to_elim]:
                end = n_old[1]
                for n_sub in eqs[to_elim]:
                    eqs[to_sub].append((n_sub[0], n_sub[1] + end))
                eqs[to_sub].remove(n_old)

            # Group together
            all_nodes_d = {k : [t for t in eqs[to_sub] if t[0] == k] for k in {k for k,_ in eqs[to_sub]}}
            for k, nodes in (x for x in all_nodes_d.items() if len(x[1]) > 1):
                new = '(?:' + '|'.join(w for _,w in nodes) + ')'
                eqs[to_sub].append((k, new))
                for node in nodes:
                    eqs[to_sub].remove(node)

        eqs.pop(to_elim)


    return '^' + '(?:' + '|'.join(w for _,w in eqs[0] if w) + ')+$'
  
#########################
from itertools import cycle


def backward(fw):
    bw = {}
    for (previous, mapping) in fw.items():
        for (state, i) in mapping.items():
            if state not in bw:
                bw[state] = {previous: i}
            else:
                bw[state][previous] = i
    return bw


def eliminate(forward, state):
    def wrap(s):
        return s if len(s) == 1 else '(?:%s)' % s

    def mul(s):
        return wrap(s) + '*'

    def sor(pattern_a, pattern_b):
        return wrap(pattern_a) + '|' + wrap(pattern_b)

    f, b = forward, backward(forward)
    previous_states = b[state]
    cycling = '' if state not in previous_states else mul(previous_states[state])
    for (p, pc) in previous_states.items():
        if p == state:
            continue

        for (q, cq) in f[state].items():
            if q == state:
                continue
            if q not in f[p]:
                f[p][q] = wrap(pc) + cycling + wrap(cq)
            else:
                f[p][q] = sor(f[p][q], wrap(pc) + cycling + wrap(cq))
        f[p].pop(state)
    forward.pop(state)
    return forward


def regex_divisible_by(n):
    if n == 1:
        return '^(?:0|1)+$'
    alphabet = ['0', '1']
    states, symbols = cycle(range(n)), cycle(alphabet)
    forward = {state: {next(states): symbol for symbol in alphabet} for state in range(n)}

    def eliminate_all(trans):
        for state in range(n-1, 0, -1):
            trans = eliminate(trans, state)
        return trans

    return '^(%s)+$' % eliminate_all(forward)[0][0]
  
######################
class RemainderOfBinaryDEA:
    """Collection of states for division remainders and the transitions"""
    __nDebugLevel = None
    __dea = None
    __nDivisor = None
    __sRegex = None
    
    def __init__(self, nDivisor, nDebugLevel = 0):
        self.__nDebugLevel = nDebugLevel
        self.__nDivisor = nDivisor
        self.__dea = {'r0': { '0': None, '1': None }}
        self.__buildAutomata()
        
    def __addPath(self, nPath):
        # Destination state for remainder
        sStateRemainder = f'r{nPath%self.__nDivisor}'
        if sStateRemainder not in self.__dea:
            # Create it if necessary
            self.__dea[sStateRemainder] = { '0': None, '1': None }
        # Path to destination state
        sPathBinary = f'{nPath:b}'
        # Add path and state
        sState = 'r0'
        for sDigit in sPathBinary:
            # Transition from existing state
            sTransition = sDigit
            if self.__dea[sState][sTransition] != None:
                # Walk through existing transition to next state
                sState = self.__dea[sState][sTransition]
            else:
                # Add a new transition and walk to the remainder state
                self.__dea[sState][sTransition] = sStateRemainder
                # Create destination state if necessary
                sState = sStateRemainder

    def __reduceState(self, sState):
        dicLoops = {}
        dicSources = {}
        dicDestinations = {}
        # Resolve all transictions from sources to destinations
        for state in self.__dea:
            if state == sState:
                # Loop to itself
                for sTSource in self.__dea[state]:
                    if self.__dea[state][sTSource] == state:
                        dicLoops[sTSource] = 1
                # Destinations
                for sT in self.__dea[state]:
                    if self.__dea[state][sT] != sState:
                        if self.__dea[state][sT] not in dicDestinations:
                            dicDestinations[self.__dea[state][sT]] = [sT]
                        else:
                            dicDestinations[self.__dea[state][sT]].append(sT)
            else:
                # Sources
                for sT in self.__dea[state]:
                    if self.__dea[state][sT] == sState:
                        if state not in dicSources:
                            dicSources[state] = [sT]
                        else:
                            dicSources[state].append(sT)

        # Prepare loops
        sLoops = '|'.join(list(dicLoops))
        sLoops = '' if len(sLoops) == 0 else f'{sLoops}*' if len(sLoops) == 1 else f'(?:{sLoops})*'
        # Remove state and change transitions from all sources to all destinations
        del self.__dea[sState]
        for sSource in dicSources:
            for sDestination in dicDestinations:
                for sTransitionSource in dicSources[sSource]:
                    for sTransitionDestination in dicDestinations[sDestination]:
                        if sTransitionSource in self.__dea[sSource]:
                            del self.__dea[sSource][sTransitionSource]
                        # Find possible existig transition from source to destination
                        sTransitionExisting = ''
                        for sT in self.__dea[sSource]:
                            if self.__dea[sSource][sT] == sDestination:
                                sTransitionExisting = sT
                                break
                        # Build new transition
                        sTransition = f'{sTransitionSource}{sLoops}{sTransitionDestination}'
                        if sTransitionExisting != '':
                            # Remove and prepend existing transition
                            del self.__dea[sSource][sTransitionExisting]
                            sTransition = f'(?:{sTransitionExisting}|{sTransition})'
                        self.__dea[sSource][sTransition] = sDestination
        
    def __buildAutomata(self):
        for nPath in range(self.__nDivisor*2):
            sPathBinary = f'{nPath:b}'
            self.__addPath(nPath)
    
    def reduceRegex(self):
        for nState in range(self.__nDivisor-1, 0, -1):
            self.__reduceState(f'r{nState}')
        # Extract/set regex
        self.__sRegex = f'^({(list(self.__dea["r0"])[0])})*$' if self.__nDivisor > 1 else '^(0|1)*$'
        return self.__sRegex
    
def regex_divisible_by(n):
    # Your Code Here
    dea = RemainderOfBinaryDEA(n)
    return dea.reduceRegex()
  
###############
# Makes nfa. The principle is that:
# 1. Each bit added to the right doubles the number and if the bit added is '1' also addes 1 to the doubled number
# 2. a*(b+c) mod n = ((a mod n)*b +c) mod n

def makenfa(n):   
    nfa = [(-1, '0', 0), (-1, '1', 1), (0,'',100)]
    for i in range(n):
        nfa.append((i,'0',(2*i)%n))
        nfa.append((i,'1',(2*i+1)%n))
    return nfa
    

# converts nfa to dictionary where (statefrom, stateto) are keys and transition regexes are the values
def nfatodic(nfa):
    return {(a[0], a[2]) : a[1] for a in nfa}

# returns a set of all states of nfa
def states(nfa):
    out = set([a[0] for a in nfa])
    out.update([a[2] for a in nfa])
    return out
# returns just the middle states of the nfa - they are to be eliminated
def statesmid(nfa):
    return states(nfa) - {-1,100}

#converts nfa to regex by elimenating states other than start and final one acceptance state one by one
def nfatoregex(nfa):
    d = nfatodic(nfa)
    states_mid = sorted(list(statesmid(nfa)), reverse = True)
    states_all = states(nfa)
    for s1 in states_mid:
        states_all.remove(s1)
        mid = '' if (s1,s1) not in d else '(?:' + d[(s1,s1)] + '*)'
        for s0 in states_all:
            if (s0,s1) not in d:
                continue
            for s2 in states_all:
                if (s1,s2) not in d:
                    continue
                newtransition = '(?:' + d[(s0,s1)] + mid + d[(s1,s2)] + ')'
                d[(s0,s2)] = newtransition if (s0,s2) not in d else '(?:' +  d[(s0,s2)] + '|' + newtransition + ')'
    return '^' + d[(-1,100)] + '$'
                                
        
def regex_divisible_by(n):
    if n==1:
        return '^[01]+$'
    return nfatoregex(makenfa(n))  
  
####################
regexes = [0]*19
regexes[1] = r'^(0|1)*$'
for n in range(2, 19):
    q = [[''] * n for _ in range(n)]
    for i in range(n):
        q[i][(i * 2) % n] = '0'
        q[i][(i * 2 + 1) % n] = '1'
    for i in range(n - 1, 0, -1):
        q[i][i] = f'({q[i][i]})*' if len(q[i][i]) else ''
        for j in range(i):
            for k in range(i):
                if q[j][i] and q[i][k]:
                    q[j][k] = ''.join((f'{q[j][k]}|' if q[j][k] else '',
                                       f'({q[j][i]})' if len(q[j][i]) > 1 else q[j][i],
                                       f'({q[i][i]})' if len(q[i][i]) > 1 else q[i][i],
                                       f'({q[i][k]})' if len(q[i][i]) > 1 else q[i][k]))
    regexes[n] = f'^({q[0][0].replace("(", "(?:")})+$'

def regex_divisible_by(n):
    return regexes[n]
  
#################
from collections import defaultdict

class DFA(object):
    def __init__(self, states, start_state, accepted_states):
        self.states = set(states)
        self.start_state = 'START_STATE'
        self.end_state = 'END_STATE'
        self.transitions = dict()
        self.add_transition(self.start_state, start_state, '')
        for accepted_state in accepted_states:
            self.add_transition(accepted_state, self.end_state, '')

    def add_transition(self, from_, to, trans):
        self.transitions[(from_, to)] = trans
        
    def select_state(self):
        """Select the state with the smallest impact when reduced."""
        from_count = defaultdict(int)
        to_count = defaultdict(int)
        for from_, to in self.transitions:
            if from_ != to:
                from_count[from_] += 1
                to_count[to] += 1
        return min(self.states, key=lambda state: from_count[state] * to_count[state])
        
    def reduce_state(self, state):
        entering = dict()
        exiting = dict()
        loop = None
        for (from_, to), trans in list(self.transitions.items()):
            if from_ == to == state:
                loop = trans
            elif to == state:
                entering[from_] = trans
            elif from_ == state:
                exiting[to] = trans
            if state in (from_, to):
                del self.transitions[(from_, to)]
        loop_trans = '' if loop is None else '(?:{})*'.format(loop)
        for enter_state, enter_trans in entering.items():
            for exit_state, exit_trans in exiting.items():
                if (enter_state, exit_state) in self.transitions:
                    format_ = '(?:{}|{{}})'.format(self.transitions[(enter_state, exit_state)])
                else:
                    format_ = '{}'
                trans = '{}{}{}'.format(enter_trans, loop_trans, exit_trans)
                trans = format_.format(trans)
                self.add_transition(enter_state, exit_state, trans)
        self.states.remove(state)
    
    def reduce(self):
        while self.states:
            state = self.select_state()
            self.reduce_state(state)
        return '^(?:0|{})$'.format(self.transitions[(self.start_state, self.end_state)])

def regex_divisible_by(n):
    if n==1:
        return '^[01]+$'
    dfa = DFA(range(n+1), n, {0})
    for i in range(n+1):
        dfa.add_transition(i, i * 2 % n, '0')
        dfa.add_transition(i, (i * 2 + 1) % n, '1')
    return dfa.reduce()
  
########################class Term(object):
    def __init__(self, state, symbol):
        self.state = str(state)
        self.symbol = str(symbol)
        
    def __str__(self):
        return self.state + '(' + self.symbol + ')'
    
def validrow(row):
    terms = dict()
    for term in row:
        if term.state in terms:
            terms[term.state].append(term.symbol)
        else:
            terms[term.state] = [term.symbol]
    
    result = []
    for state in sorted(terms.keys()):
        if len(terms[state]) > 1:
            result.append(Term(state, '(?:' + '|'.join(terms[state]) + ')'))
        else:
            result.append(Term(state, terms[state][0]))
    return result

def lastterm(arr):
    state = str(len(arr) - 1)
    terms = arr.pop()
    for i in range(len(arr) - 1, -1, -1):
        row = arr[i]
        newRow = []
        for t in row:
            if t.state == state:
                for term in terms:
                    newRow.append(Term(term.state, term.symbol + t.symbol))
            else:
                newRow.append(t)
        arr[i] = validrow(newRow)
        
def rem(arr):
    loops = dict()
    for i in range(1, len(arr)):
        row = arr[i]
        for term in row:
            if term.state == str(i):
                loops[term.state] = term.symbol
                row.remove(term)        
    for i in range(len(arr)):
        row = arr[i]
        for term in row:
            if term.state in loops:
                if len(loops[term.state]) > 1:
                    term.symbol = '(?:' + loops[term.state] + ')*' + term.symbol
                else:
                    term.symbol = loops[term.state] + '*' + term.symbol
        
def regex_divisible_by(n):
    if n == 1: return '^(0|1)+$'

    arr = [[Term(i//2,i%2), Term((i+n)//2, (i+n)%2)] for i in range(n)]
    while len(arr) > 1:
        rem(arr); lastterm(arr)
    return f"^{arr[0][0].symbol}+$"
  
##############################
def handle_loops(NFA, subs_eq, equations):
    temp = NFA[subs_eq][subs_eq]
    if len(temp) >= 1:
        temp = f"{temp[0]}*" if len(temp) == 1 and len(temp[0]) == 1 else f"(?:{'|'.join(temp)})*"
        NFA[subs_eq][subs_eq] = []
    else:
        return NFA
    for eq in equations:
        NFA[subs_eq][eq] = [f"(?:{'|'.join(NFA[subs_eq][eq])}){temp}"] if len(NFA[subs_eq][eq]) >= 2 else NFA[subs_eq][eq]
        if len(NFA[subs_eq][eq]) == 1:
            NFA[subs_eq][eq] = [NFA[subs_eq][eq][0] + temp]
    return NFA

def NFA_to_regex(NFA):
    equations = set(range(0, len(NFA)))
    for subs_eq in sorted(equations, reverse=True)[:-1]:
        equations.remove(subs_eq)
        handle_loops(NFA, subs_eq, equations)
        for equation in equations:
            if len(NFA[equation][subs_eq]) >= 1:
                temp = f'(?:{"|".join(NFA[equation][subs_eq])})' if len(NFA[equation][subs_eq]) >= 2 else NFA[equation][subs_eq][0]
            else:
                continue
            NFA[equation][subs_eq] = []
            for equation2 in equations:
                if len(NFA[subs_eq][equation2]) >= 1:
                    temp_sub = f'(?:{"|".join(NFA[subs_eq][equation2])})' if len(NFA[subs_eq][equation2]) >= 2 else NFA[subs_eq][equation2][0]
                    NFA[equation][equation2].append(temp_sub + temp)
    return f"^(?:{'|'.join(NFA[0][0])})+$"

def create_NFA(n):
    vec = []
    for i in range(0, n):
        vec.append([i, '0'])
        vec.append([i, '1'])
    vec1 = vec[:int(len(vec)/2)]
    vec2 = vec[int(len(vec)/2):]
    NFA = [[[] for i in range(0, n)] for j in range(0, n)]
    for idx, (e1, e2) in enumerate(zip(vec1, vec2)):
        NFA[idx][e1[0]] = [e1[1]]
        NFA[idx][e2[0]] = [e2[1]]
    return NFA

def regex_divisible_by(n):
    if n == 1:
        return "^(0|1)+$"
    NFA = create_NFA(n)
    return NFA_to_regex(NFA)
