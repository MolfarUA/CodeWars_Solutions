56484848ba95170a8000004d


def gps(s, x):
    if len(x) < 2:
        return 0
    a = max(x[i] - x[i-1] for i in range(1, len(x))) 
    return a * 3600.0 / s
_____________________________
def gps(s, x):
    return max([(n-m)*3600/s for (m,n) in zip(x,x[1:])])
_____________________________
def gps(s, x):
    if len(x) < 2:
        return 0
    dist = []
    speed = []
    i = 0
    while i < (len(x) - 1):
        dist.append(x[i+1] - x[i]) 
        i += 1
    for n in dist:
        speed.append(int((3600 * n) / s))
    return max(speed)    
_____________________________
gps=lambda s,x:max(b-a for a,b in zip([0]+x,x+[0]))*3600/s
_____________________________
from math import floor

def gps(s, x):
    if (len(x) <= 1):
        return 0
    mx = -1
    for k in range(len(x) - 1):
        v = 3600 * (x[k + 1] - x[k]) / s
        if (v > mx):
            mx = v
    return floor(mx)
_____________________________
def gps(s, x):
    return max([0] + [3600*(b-a)/s for a,b in zip(x[:-1],x[1:])])
_____________________________
def gps(s, x):
    sections = []
    for i in x:
        if x.index(i) < len(x) - 1:
            sections.append(abs((x[x.index(i)] - x[x.index(i) + 1])))
        else:
            break
    u_list = [(j * 3600) / s for j in sections]
    u = round(max(u_list), 2) if u_list else 0
    return u
_____________________________
def gps(s, x):
    y = len(x)
    n = 0
    i = 2
    a = [1]
    while i <= y:
        z = (3600*(x[n]-x[n+1])/s) * -1
        a.append(z)
        i += 1
        n += 1
        a.sort()
    floor = max(a)
    print(floor)
    return floor
_____________________________
import math
def gps(s, x):
    return math.floor(3600 * max([x[i] - x[i-1] for i in range(1, len(x))]) / s) if len(x) > 2 else 0
_____________________________
import math
def gps(s, x):
    return math.floor(3600 * max([x[i] - x[i-1] for i in range(1, len(x))]) / s) if x != [0] and x != [] else 0
_____________________________
def gps(s, locations):

    if len(locations) <= 1:
        return 0 

    distances = []

    max = 0
    for index, location in enumerate(locations[:-1]):
        distance = locations[index +1 ] - location
        if distance > max:
            max = distance
        
    return int(max * 3600 / s)
_____________________________
def gps(s, x):
    x = [(3600 * (x[ind + 1] - x[ind])) / s for ind in range(len(x) - 1)]
    return max(x, default = 0)
