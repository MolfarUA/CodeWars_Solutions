55eea63119278d571d00006a


def next_id(arr):
    try:
        upper_limit = max(arr) + 1
    except ValueError:
        return 0

    for i in range(0, upper_limit):
        if i not in arr:
            return i

    return upper_limit
###############
def next_id(arr):    
    t = 0
    while t in arr:
        t +=1
    return t
#############
def next_id(arr):
    for i in range(len(arr)+1):
        if i not in arr:
            return i
#############
def next_id(arr):
    if not len(arr): return 0
    d = set(sorted(arr))
    a = set(range(0, max(d) + 1))
    m = a - d
    if m:
        return min(m)
    else:
        return 0 if 0 not in d else max(d) + 1
#############
def next_id(arr):
  return reduce(lambda acc, x: acc + 1 if x == acc else acc, sorted(arr), 0)
############
def next_id(arr):
    if not arr:
        return 0
    return max(arr)+1 if 0 in arr and len(set(range(min(arr),max(arr)+1))-set(arr))==0 else 0 if 0 not in arr else sorted(list(set(range(min(arr),max(arr)+1))-set(arr)))[0]
############
def next_id(arr):
    if not arr:
        return 0
    return min(i for i in xrange(0, max(arr) + 2) if i not in arr)
#############
def next_id(a):
    i = 0
    set_a = set(a)
    while i in set_a:
        i += 1
    return i
##############
def next_id(arr):
    count = 0
    while count in arr:
        count = count + 1
    return count
############
def next_id(arr):
    i = 0
    while i in arr:
        i+=1
    return i
############
def next_id(arr):
    if not arr:return 0
    return min(set(range(0, max(arr)+2)).difference(set(arr)))
################
def next_id(arr):
    return min(set(arr) ^ set(range(max(arr) + 2))) if arr else 0
______________________
def next_id(arr):
    a = set(arr)
    b = 0
    for i in a:
        if b ==i:
            b+=1
        else:
            break
    return b
______________________
def next_id(arr):
    lista = list(range(len(arr)+1))
    
    for i in lista:
        if i not in arr:
            return i
______________________
def next_id(arr):
    if len(arr)>0:
        for i in range(max(arr)):
            if i not in arr:
                return i
    return 0 if len(arr) == 0 else max(arr)+1
______________________
def next_id(arr):
    print(arr)
    if len(arr) == 0:
        return 0
    arr = list(set(arr))
    sorted(arr)
    for i,n in enumerate(arr):
        if i != n:
            return i
    return arr[-1]+1
