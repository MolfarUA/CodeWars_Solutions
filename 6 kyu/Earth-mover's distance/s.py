from itertools import accumulate


def earth_movers_distance(x, px, y, py):
    values, dx, dy = sorted(set(x + y)), dict(zip(x, px)), dict(zip(y, py))
    dist = (b - a for a, b in zip(values, values[1:]))
    diff = accumulate(dy.get(n, 0) - dx.get(n, 0) for n in values)
    return sum(d * abs(n) for d, n in zip(dist, diff))
_________________________________________________
import numpy as np
def earth_movers_distance(x, px, y, py):
    x, px, y, py = np.array(x), np.array(px), np.array(y), np.array(py)
    x_sorter = np.argsort(x)
    y_sorter = np.argsort(y)
    numbers = np.concatenate((x, y))
    numbers.sort(kind = "mergesort")
    differences = np.diff(numbers)
    x_cdf_indexes = x[x_sorter].searchsorted(numbers[:-1], "right")
    y_cdf_indexes = y[y_sorter].searchsorted(numbers[:-1], "right")
    x_sorted_cumulative_weights = np.concatenate(([0], np.cumsum(px[x_sorter])))
    x_cdf = x_sorted_cumulative_weights[x_cdf_indexes] / x_sorted_cumulative_weights[-1]
    y_sorted_cumulative_weights = np.concatenate(([0], np.cumsum(py[y_sorter])))
    y_cdf = y_sorted_cumulative_weights[y_cdf_indexes] / y_sorted_cumulative_weights[-1]
    assert len(x_cdf) == len(y_cdf) and len(x_cdf) == len(differences) and len(y_cdf) == len(differences)
    result = 0
    for i in range(len(differences)):
        result = result + abs(x_cdf[i] - y_cdf[i]) * differences[i]
    return result
_________________________________________________
a, b = lambda x,y: sorted(set(x+y)), lambda x,y: dict(zip(x,y))
dist = lambda x,y,z: (q - p for r in [z] for p,q in zip(r,r[1:]))
diff = lambda x,px,y,py,bx,by,z: __import__('itertools').accumulate(bx.get(i,0) - by.get(i,0) for i in z)
earth_movers_distance = lambda x, px, y, py: \
    sum(abs(df)*d for z in [a(x,y)] for d,df in zip(dist(x,y,z), diff(x,px,y,py,b(x,px),b(y,py),z)))
_________________________________________________
a, b = lambda x,y: sorted(set(x+y)), lambda x,y: dict(zip(x,y))
dist = lambda x,y,z: (q - p for r in [z] for p,q in zip(r,r[1:]))
diff = lambda x,px,y,py,bx,by,z: (bx.get(i,0) - by.get(i,0) for i in z)
def earth_movers_distance(x, px, y, py, c=0, m=0):
    z = a(x,y)
    for d,df in zip(dist(x,y,z), diff(x,px,y,py,b(x,px),b(y,py),z)):
        c += df
        m += abs(c) * d
    return m
_________________________________________________
def earth_movers_distance(x, px, y, py):
    xs = sorted(zip(x, px), reverse=True)
    d = 0
    for key, value in sorted(zip(y, py)):
        while value > 0:
            k, v = xs.pop()
            d += min(value, v) * abs(key - k)
            if v > value:
                xs.append((k, v - value))
            value -= v
    return d
_________________________________________________
def earth_movers_distance(x, px, y, py):
    values, dx, dy = sorted(set(x + y)), dict(zip(x, px)), dict(zip(y, py))
    dist = (b - a for a, b in zip(values, values[1:]))
    diff = (dy.get(n, 0) - dx.get(n, 0) for n in values)
    current, moved = 0, 0
    for d, n in zip(dist, diff):
        current += n
        moved += d * abs(current)
    return moved
_________________________________________________
def earth_movers_distance(x, px, y, py):
    res = 0
    xx = sorted(zip(x, px))
    yy = sorted(zip(y, py))
    
    y, py = yy.pop()
    while xx:
        x, px = xx.pop()
        while True:
            res += abs(x - y) * min(px, py)
            if py < px:
                px -= py
                y, py = yy.pop()
            else:
                py -= px
                break
    return res
_________________________________________________
def earth_movers_distance(x, px, y, py):
    x_vals = sorted((x[idx], px[idx]) for idx in range(len(x)))
    y_vals = sorted((y[idx], py[idx]) for idx in range(len(y)))
    work = 0
    source, available = x_vals.pop()
    while y_vals:
        destination, needed = y_vals.pop()
        while needed:
            if needed > available:
                work += (available * abs(destination - source))
                needed -= available
                source, available = x_vals.pop()
            else:
                work += (needed * abs(destination - source))
                available -= needed
                needed = 0
    return work
