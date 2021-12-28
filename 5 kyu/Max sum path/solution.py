def max_sum_path(a,b):
    i,j,A,B = 0,0,0,0
    while i<len(a) and j<len(b):
        x,y = a[i],b[j]
        if x==y: A = B = max(A,B)
        if x<=y: i,A = i+1,A+x
        if x>=y: j,B = j+1,B+y
    return max( A+sum(a[i:]), B+sum(b[j:]) )
  
___________________________________
def _max(l1, l2):
    
    if not l1 and not l2: return sum(l1) or sum(l2)

    d, seen, _sum = {-1: 0}, set(l1), 0
    d.update({element: (_sum := _sum + element) for element in l1})
    
    _sum, total, last = 0, 0, -1
    for cur in l2:
        _sum += cur
        if cur in seen:
            total += d[cur] - d[last] if d[cur]-d[last] > _sum else _sum
            _sum, last = 0, cur
    return total + _sum
        
max_sum_path = lambda x, y: max(_max(x, y), _max(y, x))

___________________________________
def max_sum_path(l1, l2):
    s1 = s2 = 0
    common = {n: 0 for n in set(l1) & set(l2)}
    for n in l1:
        if n in common:
            common[n] = max(common[n], s1)
            s1 = 0
        else:
            s1 += n
    for n in l2:
        if n in common:
            common[n] = max(common[n], s2)
            s2 = 0
        else:
            s2 += n
    return max(s1, s2) + sum(v + k for v, k in common.items())
  
___________________________________
from itertools import accumulate, islice
def max_sum_path(l1, l2):
    acum1, acum2 = list(accumulate(l1, initial=0)), list(accumulate(l2, initial=0))
    idx1_dict, idx2_dict= {v:i+1 for i,v in enumerate(l1)}, {v:i+1 for i,v in enumerate(l2)}
    idx_pairs = [(idx1_dict[val],idx2_dict[val]) for val in idx1_dict if val in idx2_dict]
    idx_pairs.append((len(l1), len(l2)))

    a,b = idx_pairs[0]
    total = max(acum1[a], acum2[b])
    for i,j in islice(idx_pairs,1,None):
        total += max(acum1[i] - acum1[a], acum2[j] - acum2[b])
        a,b = i,j
    return total
  
___________________________________
def max_sum_path(l1, l2):
    shared_items = set(l1) & set(l2)
    
    def partial_sums(lst):
        result = []
        partial_sum = 0
        for item in lst:
            partial_sum += item
            if item in shared_items:
                result.append(partial_sum)
                partial_sum = 0
        result.append(partial_sum)
        return result
    
    partial_sums1 = partial_sums(l1)
    partial_sums2 = partial_sums(l2)
            
    return sum(max(sum1, sum2) for sum1, sum2 in 
               zip(partial_sums1, partial_sums2))
  
___________________________________
def max_sum_path(*args):
    t, tx, ty, x, y, = 0, 0, 0, *map(lambda v: [float('-inf'), *v], args)
    cx, cy = x.pop(), y.pop()
    while x or y:
        if cx > cy:
            tx += cx
            cx = x.pop()
        elif cy > cx:
            ty += cy
            cy = y.pop()
        else:
            t += max(tx, ty) + cx
            tx, ty, cx, cy = 0, 0, x.pop(), y.pop()
    return t + max(tx, ty)
  
___________________________________
def max_sum_path(l1, l2):
    idx_1 = 0
    idx_2 = 0
    
    total = 0
    
    total_1 = 0
    total_2 = 0
    
    while idx_1 < len(l1) and idx_2 < len(l2):
        if l1[idx_1] < l2[idx_2]:
            total_1 += l1[idx_1]
            idx_1 += 1
        elif l2[idx_2] < l1[idx_1]:
            total_2 += l2[idx_2]
            idx_2 += 1
        else:
            total += max(total_1, total_2) + l1[idx_1]
            total_1, total_2 = 0, 0
            idx_1 += 1
            idx_2 += 1
    
    for x in range(idx_1, len(l1)):
        total_1 += l1[x]
    
    for x in range(idx_2, len(l2)):
        total_2 += l2[x]
        
    return total + max(total_1, total_2)
  
___________________________________
"""
5 normal test
50 random small 
50 random medium
20 random turo large
"""

def max_sum_path(l1, l2):
    
    value, l1_last, l2_last = 0, 0, 0
    
    match = sorted(set(l1) & set(l2))

    for i in sorted(set(l1) & set(l2)):
            
            l1_idx = l1.index(i, l1_last)
            l2_idx = l2.index(i, l2_last)
            
            value += max(sum(l1[l1_last:l1_idx]), sum(l2[l2_last:l2_idx]))

            l1_last, l2_last = l1_idx, l2_idx
    
    return value + max(sum(l1[l1_last:]), sum(l2[l2_last:]))
