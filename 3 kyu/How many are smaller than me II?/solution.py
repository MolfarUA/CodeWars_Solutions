56a1c63f3bc6827e13000006


class Tree:
    ''' v,r,l: value, left, right,
        n:  number of occurrences of v
        lt: number of numbers lower than v (in the left subtree only)
    '''
    def __init__(self,v):
        self.v, self.l, self.r, self.n, self.lt = v, None, None, 1, 0


def insert(tree,v):
    if not tree:
        return Tree(v),0
    if v < tree.v:
        tree.lt += 1
        tree.l,n = insert(tree.l,v)
    elif v==tree.v:
        tree.n += 1
        n = tree.lt
    else:
        tree.r,n = insert(tree.r,v)
        n += tree.n + tree.lt
    return tree,n
        

def smaller(arr):
    out,tree = [],None
    for v in reversed(arr):
        tree,n = insert(tree,v)
        out.append(n)
    return out[::-1]
______________________________________
from bisect import bisect_left
def smaller(arr):
    # Good Luck!
    right_arr = sorted(arr)
    smaller_numbers = []
    for number in arr:
        # compare number with items in right_arr
        index = bisect_left(right_arr,number)
        smaller_numbers.append(index)
        del right_arr[index]
    return smaller_numbers
______________________________________
import bisect

class BinaryIndexedTree:
    def __init__(self, max_size):
        self.size = max_size + 1
        self.tree = [0] * self.size
    def add_to_value_at(self, index, value):
        i = index + 1

        while i < self.size: 
            self.tree[i] += value
            i += i & -i
    def get_sum(self, to_index, from_index = 0):
        if from_index <= 0:
            i = to_index + 1
            res = 0
            while i: 
                res += self.tree[i]
                i -= i & - i
            return res
        else:
            return self.get_sum(to_index) - self.get_sum(from_index - 1)
    
    def get_value(self, index):
        return self.get_sum(to_index, to_index)
        
def smaller(nums: list[int]) -> list[int]:
    nsort = sorted(nums)

    nsort = [n for i, n in enumerate(nsort) if i == 0 or nsort[i - 1] != n]
    tree = BinaryIndexedTree(len(nsort))
    res = [0] * len(nums)
		
    for k, n in enumerate(reversed(nums)):
           
        i = bisect.bisect_left(nsort, n)
        tree.add_to_value_at(i, 1) 
        res[len(nums) - k - 1] = tree.get_sum(i - 1)
    return res
______________________________________
from collections import Counter

class Fenwick:
    def __init__(self, l):
        l1 = [0]
        ss = [0]
        s = 0
        for i, j in enumerate(l, 1):
            s += j
            l1.append(s - ss[i&(i-1)])
            ss.append(s)
        self.l = l1
    def prefix(self, i):
        z = 0
        while i:
            z += self.l[i]
            i &= i-1
        return z
    def add(self, i, v):
        while i < len(self.l):
            self.l[i] += v
            i += i - (i&(i-1))

def smaller(arr):
    C = Counter(arr)
    V = sorted(C)
    D = {j:i for i,j in enumerate(V, 1)}
    F = Fenwick(C[v] for v in V)
    z = []
    for j in arr:
        i = D[j]
        z.append(F.prefix(i-1))
        F.add(i, -1)
    return z
