import itertools
def choose_best_sum(t, k, ls):
    try: 
        return max(sum(i) for i in itertools.combinations(ls,k) if sum(i)<=t)
    except:
        return None
      
_______________________________________
from itertools import combinations

def choose_best_sum(t, k, ls):
    return max((s for s in (sum(dists) for dists in combinations(ls, k)) if s <= t), default=None)
_______________________________________
from itertools import combinations

def choose_best_sum(t, k, ls):
    return max((sum(v) for v in combinations(ls,k) if sum(v)<=t), default=None)
_______________________________________
def choose_best(t,k,ls):
    if k == 0: return 0
    best = -1
    for i, v in enumerate(ls):
        if v > t: continue
        b = choose_best(t - v, k - 1, ls[i+1:])
        if b < 0: continue
        b += v
        if b > best and b <= t:
            best = b
    return best

def choose_best_sum(t, k, ls):
    c = choose_best(t,k,ls)
    if c <= 0 : return None
    return c
_______________________________________
from itertools import combinations


def choose_best_sum(max_miles, max_towns, lst):
    highest = 0
    for a in combinations(lst, max_towns):
        total_distance = sum(a)
        if max_miles >= total_distance > highest:
            highest = total_distance
    return highest or None

_______________________________________
from itertools import combinations

def choose_best_sum(t, k, ls):
    return max([sum(comb)
                for comb in combinations(ls, k)
                if sum(comb) <= t] or [None])
_______________________________________
from itertools import combinations
from functools import reduce

def choose_best_sum(t, k, ls):
    mx = -1
    res = []
    for c in combinations(ls, k):
        s = reduce(lambda x, y: x + y, c)
        if ((s >= mx) and (s <= t)):
            res = [c, s]
            mx = s
    if (res == []): return None 
    else: return res[1]
_______________________________________
from itertools import combinations
def choose_best_sum(t, k, ls):
    return max((s for s in map(sum, combinations(ls,k)) if s <= t), default=None)
_______________________________________
from itertools import combinations

def choose_best_sum(max_distance, k, distances):
    best = 0
    for combination in combinations(distances, k):
        distance = sum(combination)
        if distance == max_distance:
            return distance
        if distance < max_distance:
            best = max(best, distance)
    return best if best > 0 else None
_______________________________________
def recurse(sum, ls, level):
  if level == 1:
    return [(x+sum) for x in ls]
  ary = list(ls)
  totals = []
  for x in ls:
    ary.remove(x)
    if len(ary) >= level - 1:
      totals += recurse(sum+x, ary, level - 1)
  return totals

def choose_best_sum(t, k, ls):
    if len(ls) < k:
      return None
    totals = recurse(0, ls, k)
    sum = 0
    for x in totals:
      if x > sum and x <= t:
        sum = x
    if sum == 0:
      return None
    return sum
_______________________________________
def choose_best_sum(t, k, ls):
    solutions = set()
    recursive_search(t, k, 0, ls, 0, 0, solutions)
    if len(solutions)>0:
        return max(solutions)
    else:
        return None
    
def recursive_search(t, maxk, k, ls, ind, solution, solutions):
    if ind == len(ls) or k==maxk or maxk - k > len(ls) - ind:
        return
    recursive_search(t, maxk, k, ls, ind+1, solution, solutions)
    k += 1
    solution += ls[ind]
    if solution <= t:
        if k == maxk:
            if solution in solutions:
                return
            solutions.add(solution)
            return
        recursive_search(t, maxk, k, ls, ind+1, solution, solutions)
_______________________________________
from itertools import combinations as comb

def choose_best_sum(t, k, ls):
    return reduce(lambda s, e: max(sum(e), s) if sum(e) <= t else s, comb(ls, k), None)
