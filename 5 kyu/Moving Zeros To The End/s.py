52597aa56021e91c93000cb0


def move_zeros(arr):
    l = [i for i in arr if isinstance(i, bool) or i!=0]
    return l+[0]*(len(arr)-len(l))
_____________________________
def move_zeros(array):
    return sorted(array, key=lambda x: x==0 and type(x) is not bool)
_____________________________
def move_zeros(array):
    return sorted(array, key=lambda x: x == 0 and x is not False)
_____________________________
def move_zeros(array):
    return [x for x in array if x] + [0]*array.count(0)
_____________________________
def move_zeros(array):
    
    w = []
    d = 0
    
    for i in array:
        if i is False:
            w.append(False)
        elif i == 0:
            d += 1
        else:
            w.append(i)
    for i in range(0,d):
        w.append(0)
    
    print w
    return w
_____________________________
def move_zeros(a):
    a.sort(key=lambda v: v == 0)
    return a
_____________________________
def move_zeros(array):
    return sorted(array, key= lambda x: x == 0 and type(x) != bool)
_____________________________
def move_zeros(array):
    a = list(filter(lambda x: x!=0 or type(x) is bool, array))
    return a + [0]*(len(array)-len(a))
_____________________________
def move_zeros(array):
    return [x for x in array if x != 0 or x is False]+[x for x in array if x == 0 and not(x is False)]
_____________________________
def move_zeros(array):
    return sorted(array, key=lambda x: not x)
_____________________________
def move_zeros(array):
    return [ i for i in array if i != 0]+[ i for i in array if i == 0]
_____________________________
def move_zeros(lst):
    l = []
    l2 = lst.copy()
    t = 0
    for i, n in enumerate(lst):
        if n == 0:
            l.append(l2.pop(i - t))
            t+=1
    return l2+l
_____________________________
def move_zeros(lst):
    if lst == []:
        return []
    cnt = lst.count(0)
    for i in range(cnt):
        lst.remove(0)
    for i in range(cnt):
        lst.append(0)
    return lst
