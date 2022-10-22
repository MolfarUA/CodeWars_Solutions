55cf3b567fc0e02b0b00000b


def prod(n):
    ret = [{1.}]
    for i in range(1, n+1):
        ret.append({(i - x) * j for x, s in enumerate(ret) for j in s})
    return ret[-1]

def part(n):
    p = sorted(prod(n))
    return "Range: %d Average: %.2f Median: %.2f" % \
            (p[-1] - p[0], sum(p) / len(p), (p[len(p)//2] + p[~len(p)//2]) / 2)
_____________________________
from functools import lru_cache, reduce
from operator import or_
from statistics import mean, median

@lru_cache(maxsize=None)
def prod(n, x):
    if n < 0:
        return set()
    return reduce(or_, ({i*s for s in prod(n-i, i)} for i in range(2, x+1)), {1})

def part(n):
    xs = prod(n, n)
    return f"Range: {max(xs) - min(xs)} Average: {mean(xs):.2f} Median: {median(xs):.2f}"
_____________________________
mem = {1:[[1]]}
        
def gen_part(n):
    if n in mem:
        return mem[n]
    else:
        temp = []
        for i in gen_part(n-1):
            temp.append([1] + i)
            if i and (len(i) < 2 or i[1] > i[0]):
                temp.append([i[0] + 1] + i[1:])
        mem[n] = temp
        return temp

def prod(n):
    values = []
    for i in gen_part(n):
        temp = 1
        for j in i:
            temp *= j
        if temp not in values:
            values.append(temp)
    return sorted(values)

def median(n,size):
    if size == 2:
        return (n[0]+n[1])/2.0
    if size%2 == 1:
        return n[int(size/2)]
    else:
        x = int(size/2)
        return (n[x-1]+n[x])/2.0

def part(n):
    values = prod(n)
    size = len(values)
    rng = values[size-1] - values[0]
    med = median(values,size)
    mean = sum(values)/float(size)
    x = "Range: {} Average: {:.2f} Median: {:.2f}".format(rng,mean,med)
    return x
_____________________________
from statistics import mean, median

def part(n):
    data = sorted(set(prodPart(n,n)))
    return f'Range: { max(data)-min(data) } Average: { mean(data) :0.2f} Median: { median(data) :0.2f}'

def prodPart(n,top,p=1):
    if top<2: yield p
    else:
        for v in range(1,top+1):
            yield from prodPart(n-v,min(v,n-v),p*v)
_____________________________
def part(n):
    table = [{1} for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            table[j].update([i * product for product in table[j - i]])
    prod = sorted(table[-1])
    mid = len(prod) // 2
    median = (prod[mid]+prod[~mid]) / 2
    return f"Range: {prod[-1] - prod[0]} Average: {sum(prod) / len(prod):.2f} Median: {median:.2f}"
_____________________________
from functools import lru_cache
from math import prod
from numpy import average,median

q = { 1: [[1]] }

@lru_cache(maxsize=None)
def partitions(n):
    try:
        return q[n]
    except:
        pass

    result = [[n]]

    for i in range(1, n):
        a = n-i
        R = partitions(i)
        for r in R:
            if r[0] <= a:
                result.append([a] + r)

    q[n] = result
    return result

def part(n):
    arr = list(map(prod,partitions(n)))
    si = list(set(arr))
    return f"Range: {max(arr)-min(arr)} Average: {average(si):.2f} Median: {median(si):.2f}" 
_____________________________
import numpy

def part(n):
    # your code
    cnt = [1] + [0]*n
    product = [set() for i in range(n+1)]
    for i in range(1, n+1):
        for j in range(i, n+1):
            if cnt[j-i] > 0:
                cnt[j] += cnt[j-i]
                if not product[j-i]:
                    product[j].add(i)
                else:
                    for p in product[j-i]:
                        product[j].add(i*p)
    result = sorted(product[n])
    return "Range: {} Average: {:.2f} Median: {:.2f}".format(result[-1]-result[0], numpy.average(result), numpy.median(result))
_____________________________
from math import floor, ceil
from functools import cache, reduce

@cache
def partition(n):
    if n == 1:
        return {(1,)}
    result = set()
    for item in partition(n - 1):
        result.add(item + (1,))
        result.add((item[0] + 1,) + item[1:])
        result.add(tuple(sorted(item[:-1] + (item[-1] + 1,), reverse=True)))
    return result

def product(t):
    return reduce(int.__mul__, t)

def part(n):
    prod = sorted({product(t) for t in partition(n)})
    c = len(prod)
    return f"Range: {prod[-1] - prod[0]} Average: {sum(prod) / c:.2f} Median: {(prod[ceil((c - 1) / 2)] + prod[floor((c - 1) / 2)]) / 2:.2f}"
