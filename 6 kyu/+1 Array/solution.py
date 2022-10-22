5514e5b77e6b2f38e0000ca9



def up_array(arr):
    if not arr or min(arr) < 0 or max(arr) > 9:
        return None
    else:
        return [int(y) for y in str(int("".join([str(x) for x in arr])) + 1)]
_____________________________
def up_array(arr):
    if arr and all(0<=v<=9 for v in arr):
        return map(int, str(int(''.join(map(str,arr)))+1))
_____________________________
def up_array(arr):
    return None if arr==[] or any([x not in range(10) for x in arr]) else [int(c) for c in str(int("".join([str(x) for x in arr]))+1)]
_____________________________
def up_array(a):
    if not a or any(not 0 <= x < 10 for x in a): return
    for i in range(1, len(a)+1):
        a[-i] = (a[-i] + 1) % 10
        if a[-i]: break
    else: a[:0] = [1]
    return a
_____________________________
def up_array(arr):
    if arr and all(0 <= x <= 9 for x in arr):
        return map(int, str(int(''.join(map(str, arr))) + 1))
_____________________________
def up_array(arr):
    if len(arr) < 1 :
        return None

    for i in arr:
        if len(str(i)) > 1 or i < 0:
            return None
    else:    
        res = [int(i) for i in str(eval(''.join(map(str, arr))) + 1)]
        return list(res) 
_____________________________
def up_array(arr):
    a = True
    for i in arr:
        if i < 0 or i > 9:
            a = False
    if len(arr) == 0:
        a = False
    if a == True:
        arr = "".join(str(i) for i in arr)
        arr = int(arr) + 1
        z = []
        for i in range(len(str(arr))):
            z.append(int(str(arr)[i]))
        return z
    else:
        return None
_____________________________
def up_array(arr):
    if len(arr)==0 or len([el for el in arr if el < 0])>0 or [it for it in arr if it > 9]:
        return None
    return [int(x) for x in str(int(''.join(map(str,arr)))+1)]
_____________________________
def up_array(mass, number = 0):
    if len(mass) < 1:
        return None
    mass.reverse()
    for i in range(len(mass)):
        if mass[i] < 0 or mass[i] > 9:
            return None
        number += mass[i] * pow(10, i)
    mass = []
    for i in str(number+1):
        mass.append(int(i))
    return mass
_____________________________
def up_array(arr):
    if arr == []:
        return None
    if any( x<0 or x>9 for x in arr):
        return None
    return [ int(i) for i in str(int("".join(map(str,arr)))+1) ]
_____________________________
def up_array(arr):
    if not arr:
        return None
    for i in arr:
        if i < 0 or i > 9 or not isinstance(i, int):
            return None    
    total = 0
    count = 0
    for i in reversed(arr):
        total = total + i * 10 ** count
        count = count + 1
    total = total + 1 
    return [int(i) for i in str(total)]
_____________________________
def up_array(arr):
    if len(arr) == 0:
        return None
    
    for x in arr:
        if x < 0:
            return None
        if len(str(x)) > 1:
            return None
        
    total_val = str(int(''.join(str(x) for x in arr))+1)
    return [int(x) for x in total_val]
_____________________________
def up_array(arr):
    print(arr)
    if arr == []:
        return None
    for char in arr:
        if char < 0 or char > 9:
            print('no')
            return None
        
    arr = [str(char) for char in arr]
    stringy = ''.join(arr)
    stringy = int(stringy) + 1
    stringy = str(stringy)
    arr = [int(char) for char in stringy]
    return arr
_____________________________
def up_array(arr):
    if arr and min(arr) >= 0 and max(arr) < 10:
        return [int(n) for n in str(int("".join(map(str, arr))) + 1)]
