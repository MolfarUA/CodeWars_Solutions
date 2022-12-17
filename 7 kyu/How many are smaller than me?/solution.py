56a1c074f87bc2201200002e


def smaller(arr):
    if len(arr)==1:return [0]
    cnt =  0;
    for i in arr[1:]:
        if arr[0]>i:
            cnt+=1
    return [cnt]+smaller(arr[1:])
____________________________
def smaller(arr):
    return [len([a for a in arr[i:] if a < arr[i]]) for i in range(0, len(arr))]
____________________________
def smaller(arr):
    return [sum([c > j for j in arr[i:]])for i, c in enumerate(arr)]
____________________________
def smaller(arr):
    ret_arr = []
    for i in range(len(arr)):
        n = 0
        for j in range(i, len(arr)):
            if arr[i] > arr[j]:
                n += 1
        ret_arr.append(n)
        
    return ret_arr
____________________________
def smaller(arr):
    res = []
    for i in arr:
        if res:
            for j in range(len(res)):
                if arr[j] > i:
                    res[j] += 1
        res.append(0)
    return res
