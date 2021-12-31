from collections import deque

def dbl_linear(n):
    h = 1; cnt = 0; q2, q3 = deque([]), deque([])
    while True:
        if (cnt >= n):
            return h
        q2.append(2 * h + 1)
        q3.append(3 * h + 1)
        h = min(q2[0], q3[0])
        if h == q2[0]: h = q2.popleft()
        if h == q3[0]: h = q3.popleft()
        cnt += 1

__________________________________________________
from collections import deque

def dbl_linear(n):
    u, q2, q3 = 1, deque([]), deque([])
    for _ in range(n):
        q2.append(2 * u + 1)
        q3.append(3 * u + 1)
        u = min(q2[0], q3[0])
        if u == q2[0]: q2.popleft()
        if u == q3[0]: q3.popleft()
    return u
  
__________________________________________________
def dbl_linear(n):
  num_list = [1]
  for i in num_list:
    num_list.append((i * 2) + 1)
    num_list.append((i * 3) + 1)
    if len(num_list) > n *10:
      break
  return sorted(list(set(num_list)))[n]

__________________________________________________
def dbl_linear(n):
    u = [1]
    i = 0
    j = 0
    while len(u) <= n:
        x = 2 * u[i] + 1
        y = 3 * u[j] + 1
        if x <= y:
            i += 1
        if x >= y:
            j += 1
        u.append(min(x,y))
    return u[n]
  
__________________________________________________
def dbl_linear(n):
    s = [1]
    for i in range(n*10):
        y = 2*s[i]+1
        z = 3*s[i]+1
        s.extend([y,z])
    s = sorted(list(set(s)))
    return(s[n])
  
__________________________________________________
def dbl_linear(n):
    ai = bi = eq = 0
    a = [1]
    while ai + bi < n + eq:
        y = 2 * a[ai] + 1
        z = 3 * a[bi] + 1
        if y < z:
            a.append(y)
            ai += 1
        elif y > z:
            a.append(z)
            bi += 1
        else:
            a.append(y)
            ai += 1
            bi += 1
            eq += 1
    return a[-1]
  
__________________________________________________
def dbl_linear(n):
    res = [1]
    x, y = 0, 0
    while len(res) <= n:
        f = res[x] * 2 + 1
        s = res[y] * 3 + 1
        if f > s:
            res.append(s)
            y += 1
        
        elif f < s:
            res.append(f)
            x += 1
            
        else:
            res.append(f)
            x += 1
            y += 1
    return res[n]
  
__________________________________________________
import heapq
def dbl_linear(n):
    visited=set()
    res=[]
    heapq.heappush(res,1)
    while len(visited)!=n:
        x=heapq.heappop(res)
        if x not in visited:
            visited.add(x)
            heapq.heappush(res,2*x +1)
            heapq.heappush(res,3*x +1)
    return heapq.heappop(res)
