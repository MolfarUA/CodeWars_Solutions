def take(arr,n):
	print(arr[:n])
	return arr[:n]
#################
def take(arr,n):
    return arr[:n]
#############
take=lambda a,n:a[:n]
############
def take(arr,n):
    arr2 = []
    while n > 0:
        if arr == []:
            break
        arr2.append(arr[0])
        arr.pop(0)
        n -= 1
    return arr2
###############
take=lambda arr,n:arr[:n]
##############
def take(arr,n):
    return list(arr[i] for i in range(0, n, 1)) if len(arr) >= n else arr
###############
def take(arr,n):
    if arr == []:
        return arr
    else:
        return arr[:n]
#############
def take(arr,n):
        res = arr[:n]
        return res
##############
def take(arr,n):
    return arr[:n:1]
###############
def take(arr,n):
    return arr if len(arr)<n else [arr[i] for i in range(n)]
################
take = lambda l, n: l[:n]
###############
take = lambda arr, n: (lambda arr, s=slice(None, n): arr[s]) (arr)
###############
take = lambda _,__: _[:__]
##############
def take(arr,n):
    a = arr 
    return a[0:n]
