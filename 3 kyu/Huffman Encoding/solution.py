from collections import Counter

class Leaf():
    def __init__(self, character, frequency):
        self.character = character
        self.frequency = frequency

class Tree():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def get_encoding_rule(self):
        if type(self.left) is Leaf: left = {self.left.character: "0"}
        else: left = {character: "0"+code for character, code in self.left.get_encoding_rule().items()}
        if type(self.right) is Leaf: right = {self.right.character: "1"}
        else: right = {character: "1"+code for character, code in self.right.get_encoding_rule().items()}
        left.update(right)
        return left

    @property
    def frequency(self):
        return self.left.frequency + self.right.frequency

# takes: str; returns: [ (str, int) ] (Strings in return value are single characters)
def frequencies(s):
    return list(Counter(s).items())

def get_encoding_rule(freqs):
    trees = [Leaf(freq[0], freq[1]) for freq in freqs]
    while len(trees) != 1:
        trees = sorted(trees, key=lambda t: t.frequency)
        trees.append(Tree(trees.pop(1), trees.pop(0)))
    return trees[0].get_encoding_rule()

def get_decoding_rule(freqs):
    encoding_rule = get_encoding_rule(freqs)
    return {encode: character for character, encode in encoding_rule.items()}

# takes: [ (str, int) ], str; returns: String (with "0" and "1")
def encode(freqs, s):
    if len(freqs) <= 1: return None
    encoding_rule = get_encoding_rule(freqs)
    return "".join(encoding_rule[character] for character in s)

# takes [ [str, int] ], str (with "0" and "1"); returns: str
def decode(freqs, bits):
    if len(freqs) <= 1: return None
    decoding_rule = get_decoding_rule(freqs)
    decode_string = code = ""
    for b in bits:
        code += b
        if code in decoding_rule:
            decode_string += decoding_rule[code]
            code = ""
    return decode_string
  
___________________________________________________
from collections import Counter
from heapq import heappush, heappop
import re

def frequencies(s):
    return list(Counter(s).items())

def table(freqs):
    trees = sorted((k, c, {c: ''}) for c, k in freqs)
    while trees[1:]:
        k0, c0, t0 = heappop(trees)
        k1, _, t1 = heappop(trees)
        heappush(trees, (k0 + k1, c0, {c: b+s for b, t in (('0', t0), ('1', t1)) for c, s in t.items()}))
    return trees[0][2]

def encode(freqs, s):
    if freqs[1:]:
        return ''.join(map(table(freqs).get, s))
  
def decode(freqs,bits):
    if freqs[1:]:
        t = {s: c for c, s in table(freqs).items()}
        return re.sub('|'.join(t), lambda m: t[m.group()], bits)
      
___________________________________________________
from collections import Counter, namedtuple
from heapq import heappush, heappop
def frequencies(strng):
    return list(Counter(strng).items())

def freqs2tree(freqs):
    heap, Node = [], namedtuple('Node', 'letter left right')
    for char, weight in freqs: heappush(heap, (weight, Node(char, None, None)))
    while len(heap) > 1:
        (w_left, left), (w_right, right) = heappop(heap), heappop(heap)
        heappush(heap, (w_left + w_right, Node("", left, right)))
    return heappop(heap)[1]

def encode(freqs, strng):
    def tree2bits(tree, parent_bits=1):
        if tree:
            if tree.letter: table[ord(tree.letter)] = bin(parent_bits)[3:]
            tree2bits(tree.left, parent_bits << 1 | 0)
            tree2bits(tree.right, parent_bits << 1 | 1)

    if len(freqs) > 1:
        table = {}
        tree2bits(freqs2tree(freqs))
        return strng.translate(table)

def decode(freqs, bits):
    def tree2strng(tree, parent_bits=1):
        if tree:
            if tree.letter: table[parent_bits] = tree.letter
            tree2strng(tree.left, parent_bits << 1 | 0)
            tree2strng(tree.right, parent_bits << 1 | 1)

    if len(freqs) > 1:
        table, code, strng = {}, 1, []
        tree2strng(freqs2tree(freqs))
        for b in map(int, bits):
            code = code << 1 | b
            if code in table:
                strng.append(table[code])
                code = 1
        return ''.join(strng)
      
___________________________________________________
class Node():
    def __init__(self,value):
        self.val = value
    def BinAdd(self,v):
        pass
    def dex(self,s):
        pass

class EndNode(Node):
    def __init__(self,value,data):
        Node.__init__(self,value)
        self.data = data
        self.bin = ""
        self.end = True
    def BinAdd(self,v):
        self.bin += v
    def dex(self,s):
        return self.data

class SNode(Node):
    def BinAdd(self,v):
         self.left.BinAdd(v)
         self.right.BinAdd(v)
    def __init__(self,left,right):
        Node.__init__(self,left.val + right.val)
        if left.val <= right.val:
            self.left, self.right = left,right
        else:
            self.left, self.right = right,left
        self.left.BinAdd("0")
        self.right.BinAdd("1")
        self.end = False

class Queue():
    def __init__(self):
        self.Nodes = []
    def insert(self,Node):
        self.Nodes.append(Node)
        i = 1
        while len(self.Nodes) > i and  self.Nodes[-i].val > self.Nodes[-i-1].val:
            self.Nodes[-i],self.Nodes[-i-1] = self.Nodes[-i-1],self.Nodes[-i]
            i+=1
    def addNode(self):
        a, b = self.Nodes[-1], self.Nodes[-2]
        self.Nodes = self.Nodes[:-2]
        self.insert(SNode(a,b))

def frequencies(s):
    return [(c,s.count(c)) for c in set(s)]

def encode(freqs, s):
    if len(freqs) < 2: return None
    #if s == "" and len(freqs)<2: return None
    b = ""
    Q = Queue()
    EN = []
    for (c,v) in freqs:
        bn = EndNode(v,c)
        EN.append(bn)
        Q.insert(bn)
    while len(Q.Nodes) > 1:
        Q.addNode()
    for c in s:
        b += next(node for node in EN if node.data == c).bin[::-1]
    return b

def decode(freqs, bits):
    if len(freqs) < 2: return None
    #if bits == "" and len(freqs)<2: return None
    Q = Queue()
    for (c, v) in freqs:
        bn = EndNode(v,c)
        Q.insert(bn)
    while len(Q.Nodes) > 1:
        Q.addNode()
    act = Q.Nodes[0]
    res = ""
    for b in bits:
        if act.end == False:
            if b == "0":
                act = act.left
            else:
                act = act.right
        if act.end == True:
            res += act.data
            act = Q.Nodes[0]
    return res
  
___________________________________________________
from collections import Counter, defaultdict
from heapq import heapify, heappop, heappush

#Node objects inheriting from class str so the Node objects can use the __le__ magic method
#in order to be compared with other objects in the Binary Heap - serving as a Tie-Breaker!
class Node(str):
    def __init__(self,data):
        self.left = None
        self.right = None
        self.data = data

def traverse_tree(root,s):
    if not root:
        return
    
    if isinstance(char:=root.data, str):
        d[char] = s

    traverse_tree(root.left, s+'0')
    traverse_tree(root.right, s+'1')
    

def frequencies(s):
    return sorted(Counter(s).items())

def generate_huffman_tree(frequences):
    heap = [(w,Node(v)) for v,w in frequences]
    heapify(heap)
    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        sum_ = left[0] + right[0]
        new_node = Node(sum_)
        new_node.left = left[1]
        new_node.right = right[1]
        heappush(heap, (sum_,new_node))

    _,root = heappop(heap)
    return root

d = defaultdict(lambda:'')
def encode(freqs, s):
    if len(freqs) < 2:
        return None
    
    root = generate_huffman_tree(freqs)
    traverse_tree(root,'')
    return ''.join(d[x] for x in s)

def decode(freqs,bits):
    if len(freqs) < 2:
        return None

    root = generate_huffman_tree(freqs)
    temp = root
    output = ''
    for x in bits:
        if x == '0':
            temp = temp.left
        else:
            temp = temp.right
        if temp.left is temp.right is None:
            output += temp.data
            temp = root
    return output
  
___________________________________________________
from collections import Counter
from functools import total_ordering
import heapq


@total_ordering
class Node:
    def __init__(self, weight, char=None, left=None, right=None) -> None:
        self.weight = weight
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other) -> bool:
        return self.weight < other.weight

    def assign_code(self, codes, prefix='') -> None:
        if self.char:
            codes[self.char] = prefix
            return
        self.left.assign_code(codes, prefix + '0')
        self.right.assign_code(codes, prefix + '1')


class Huffman:
    def __init__(self, freqs):
        counter = dict(freqs)
        if len(counter) < 2:
            raise ValueError("You must provide a string (or frequency dictionary) to create the code dictionary based on")

        queue = [Node(freq, char) for char, freq in counter.items()]
        heapq.heapify(queue)
        while len(queue) > 1:
            l = heapq.heappop(queue)
            r = heapq.heappop(queue)
            heapq.heappush(queue, Node(l.weight + r.weight, left=l, right=r))

        root = queue.pop()
        self.codes = {}
        root.assign_code(self.codes)


# takes: str; returns: [ (str, int) ] (Strings in return value are single characters)
def frequencies(s):
    return Counter(s).items()

# takes: [ (str, int) ], str; returns: String (with "0" and "1")
def encode(freqs, s):
    try:
        huff = Huffman(freqs)
        out = []
        for char in s:
            out.append(huff.codes[char])
        return ''.join(out)
    except ValueError:
        return None

# takes [ [str, int] ], str (with "0" and "1"); returns: str
def decode(freqs,bits):
    try:
        out = []
        huff = Huffman(freqs)
        decode_dict = {v: k for k, v in huff.codes.items()}
        code = ''
        for bit in bits:
            code += bit
            char = decode_dict.get(code)
            if char:
                out.append(char)
                code = ''
        return "".join(out)
    except ValueError:
        return None
      
___________________________________________________
from collections import deque
from heapq import *

class TreeNode:
    def __init__(self, symbol, frequency, left, right):
        self.value = None
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    @staticmethod
    def createLeaf(symbol, frequency):
        return TreeNode(symbol, frequency, None, None)

    @staticmethod
    def createInnerNode(left, right):
        left.value = "0"
        right.value = "1"
        return TreeNode(None, left.frequency + right.frequency, left, right)

    def isLeaf(self):
        return self.left is None and self.right is None

    def __lt__(self, other):
        return self.frequency < other.frequency

def makeTree(freqs):
    treeHeap = []
    for symbol, freq in freqs:
        heappush(treeHeap, TreeNode.createLeaf(symbol, freq))
    while len(treeHeap) > 1:
        heappush(treeHeap, TreeNode.createInnerNode(heappop(treeHeap), heappop(treeHeap)))
    return heappop(treeHeap)

def frequencies(input):
    freqTable = {}
    for symbol in input:
        freqTable[symbol] = freqTable.get(symbol, 0) + 1
    return [(symbol, freq) for symbol, freq in freqTable.items()]

def encode(freqs, input):
    if len(freqs) < 2:
        return None
    if len(input) == 0:
        return ""

    encodingTable = {}
    q = deque()
    q.appendleft((makeTree(freqs), ""))
    while len(q) > 0:
        node, prefix = q.pop()
        if node.isLeaf():
            encodingTable[node.symbol] = prefix
        else:
            q.appendleft((node.left, prefix + node.left.value))
            q.appendleft((node.right, prefix + node.right.value))

    output = ""
    for symbol in input:
        output += encodingTable[symbol]
    return output

def decode(freqs, input):
    if len(freqs) < 2:
        return None
    if len(input) == 0:
        return ""

    root = makeTree(freqs)
    output = ""
    node = root
    for value in input:
        node = node.left if value == node.left.value else node.right
        if node.isLeaf():
            output += node.symbol
            node = root
    return output

___________________________________________________
from heapq import *


def frequencies(s):
    return [(char, s.count(char)) for char in set(s)]


class Node:
    def __init__(self, freq, char, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def build_tree(freqs):
    nodes = [Node(freq, char) for char, freq in freqs]
    heapify(nodes)

    while len(nodes) > 1:
        ln = heappop(nodes)
        rn = heappop(nodes)
        heappush(nodes, Node(ln.freq + rn.freq, None, ln, rn))

    return nodes[0]


def encode(freqs, s):
    if len(freqs) < 2:
        return None

    tree = build_tree(freqs)

    codes = {}
    def codes_from_tree(node, code=""):
        if node.left:
            codes_from_tree(node.left, code + "0")
        if node.right:
            codes_from_tree(node.right, code + "1")
        codes[node.char] = code

    codes_from_tree(tree)

    return "".join(codes[char] for char in s)


def decode(freqs, bits):
    if len(freqs) < 2:
        return None

    tree = build_tree(freqs)

    string = ""
    node = tree
    for bit in bits:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node.char:
            string += node.char
            node = tree

    return string
  
___________________________________________________
from heapq import *


def frequencies(s):
    return [(char, s.count(char)) for char in set(s)]


class Node:
    def __init__(self, freq, char, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    
def build_tree(freqs):
    nodes = [Node(freq, char) for char, freq in freqs]
    heapify(nodes)
    while len(nodes) > 1:
        ln = heappop(nodes)
        rn = heappop(nodes)
        heappush(nodes, Node(ln.freq + rn.freq, None, ln, rn))
    return nodes[0]


def encode(freqs, s):
    if len(freqs) < 2:
        return None

    codes = {}
    def codes_from_tree(node, code=""):
        if node.left:
            codes_from_tree(node.left, code + "0")
        if node.right:
            codes_from_tree(node.right, code + "1")
        codes[node.char] = code

    codes_from_tree(build_tree(freqs))

    return "".join(codes[char] for char in s)


def decode(freqs, bits):
    if len(freqs) < 2:
        return None
    
    string = ""    
    node = build_tree(freqs)
    for bit in bits:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node.char:
            string += node.char
            node = build_tree(freqs)
    
    return string
  
___________________________________________________
from collections import Counter as ctr
from collections import defaultdict as df
from bisect import insort as ins
frequencies=lambda s:ctr(s).items();n=None;encode=lambda f, s:n if len(f) in [1,0] else ''.join([*map(T(f).get, s)])
def decode(f, B):
    R = []
    while B and len(f) not in [1,0]:a,b=next((a,b)for a,b in T(f).items()if B.startswith(b));B=B[len(b):];R.append(a)
    return n if len(f)in [1,0] else''.join([*filter(lambda x:x,R)])
def T(f):
    dd = df(lambda:"");f=sorted((-a[1],a[0])for _,a in enumerate(f))
    while len(f) not in [1,0]:
        a1,a2 =f.pop(-1),f.pop(-1)
        for c in a2[1]:dd[c]=f'1{dd[c]}'
        for c in a1[1]:dd[c]=f'0{dd[c]}'
        ins(f,(a1[0]+a2[0],a1[1]+a2[1]))
    return dd
  
___________________________________________________
import collections

# takes: str; returns: [ (str, int) ] (Strings in return value are single characters)
def frequencies(s):
    def_dict = collections.defaultdict(int)
    for c in s:
        def_dict[c] += 1
    freqs = list(def_dict.items())
    return freqs

# takes: [ (str, int) ], str; returns: String (with "0" and "1")
def encode(freqs, s):
    # error handling
    if len(freqs) < 2:
        return None

    code_map = getCodes(freqs)

    code = ''
    for l in s:
        c = code_map.get(l, '?')
        code += c

    return code


# takes [ [str, int] ], str (with "0" and "1"); returns: str
def decode(freqs, bits):
    if len(freqs) < 2:
        return None
    code_map = getCodes(freqs)
    rev_code_map = {v: k for k, v in code_map.items()}
    keys = sorted(rev_code_map.keys())

    decoded = ''
    while len(bits):
        for k in keys:
            if not bits.startswith(k):
                continue
            letter = rev_code_map[k]
            decoded += letter
            bits = bits[len(k):]
            break
        else:
            print('cant decode {}'.format(bits))

    return decoded


def getTree(freqs):

    def groupSortedNodes(n1, n2):
        n1.bit = '0'
        n2.bit = '1'

        n_value = n1.value + n2.value
        n = Node(n_value)
        n.left = n1
        n.right = n2
        n1.parent = n
        n2.parent = n
        return n

    freqs.sort(key=lambda n: n[1], reverse=True)
    leaves = [Node(t[1], t[0]) for t in freqs]

    while len(leaves) > 1:
        n2 = leaves.pop()
        n1 = leaves.pop()
        n = groupSortedNodes(n1, n2)
        leaves.append(n)
        leaves.sort(key=lambda n: n.value, reverse=True)

    return leaves[0]

  
def getCodes(freqs):
    code_map = {}
    if freqs:
        tree = getTree(freqs)
        childs = tree.getAllChilds()
        letter_childs = [c for c in childs if c.letter]
        code_map = {n.letter: n.getCode() for n in letter_childs}
    return code_map


class Node(object):

    def __init__(self, value, letter=None):
        self.parent = None
        self.left = None
        self.right = None
        self.letter = letter
        self.value = value
        self.bit = None

    def getParents(self):
        parent = self.parent
        result = []
        while parent:
            result.append(parent)
            parent = parent.parent
        return result

    def getCode(self):
        code = self.bit
        for p in self.getParents()[:-1]:
            # print p
            code += p.bit
        code = code[::-1]
        return code

    def getChilds(self):
        childs = [c for c in [self.left, self.right] if c]
        return childs

    def getAllChilds(self):
        childs = self.getChilds()
        extra_childs = []
        for c in childs:
            ec = c.getAllChilds()
            extra_childs.extend(ec)
        return childs + extra_childs

    def __str__(self):
        return ('N {}->{}'.format(self.letter,self.value))
