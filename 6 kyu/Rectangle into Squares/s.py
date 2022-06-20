55466989aeecab5aac00003e


def sqInRect(lng, wdth):
    if lng == wdth:
        return None
    if lng < wdth:
        wdth, lng = lng, wdth
    res = []
    while lng != wdth:
        res.append(wdth)
        lng = lng - wdth
        if lng < wdth:
            wdth, lng = lng, wdth
    res.append(wdth)
    return res
______________________________
def sqInRect(a, b):
    if a == b:
        return None
    
    res = []
    
    while b:
        b, a = sorted([a, b])
        res += [b]
        a, b = b, a-b
    
    return res
______________________________
def sqInRect(lng, wdth):
    if lng==wdth:
        return None
    a=[]
    while lng>0 and wdth>0:
        if lng>=wdth:
            a.append(wdth)
            lng-=wdth
        elif lng<wdth:
            a.append(lng)
            wdth-=lng
    return a
______________________________
def sqInRect(lng, wdth):
    return _sqInRect(lng, wdth) if lng != wdth else None

def _sqInRect(lng, wdth):
    mi, ma = sorted((lng, wdth))
    return [] if 0 in (mi, ma) else [mi] + _sqInRect(ma-mi, mi)
______________________________
def sqInRect(lng, wdth, recur = 0):
    if lng == wdth:
        return (None, [lng])[recur]            # If this is original function call, return None for equal sides (per kata requirement);
                                               # if this is recursion call, we reached the smallest square, so get out of recursion.
    lesser = min(lng, wdth)
    return [lesser] + sqInRect(lesser, abs(lng - wdth), recur = 1)
______________________________
def sqInRect(lng, wdth):
    if lng == wdth: return None
    x, y = sorted([lng, wdth])
    ans = []
    while x > 0:
        ans.append(x)
        x, y = sorted([x, y-x])
    return ans
______________________________
answer = []

def recursFunc(lng, wdth):
    if lng > 0 and wdth > 0:
        if lng > wdth:
            a = lng;
            b = wdth;
        else:
            a = wdth;
            b = lng
        a -= b
        answer.append(b)
        return recursFunc(a, b)
    else:
        if len(answer) == 1:
            return None
        else:
            return answer

def sqInRect(lng, wdth):
    answer.clear()
    return recursFunc(lng, wdth)
______________________________
def sqInRect(length, width):
    if length == width: return None
    result = []

    while True:
        if length == width:
            result.append(length)
            break
            
        sub = min(length, width)
        if sub != 1:
            result.append(sub)
            if length > width:
                length -= sub
            else:
                width -= sub
        else:
            for _ in range(max(length, width)):
                result.append(1)
            break

    return result
______________________________
def sqInRect(lng, wdth):
    if lng==wdth:
        return None
    lst=[]
    while True:
        if lng<wdth:
            lst.append(lng)
            wdth-=lng
        elif lng>wdth:
            lst.append(wdth)
            lng-=wdth
        elif lng%wdth==0:
            for i in range(lng//wdth):
                lst.append(wdth)
            break
        else:
            for i in range(wdth//lng):
                lst.append(lng)
            break
    return lst
______________________________
def sqInRect(a, b):
    if a == b: return None
    if not b: return []
    return [b] * (a // b) + sqInRect(b, a % b)
