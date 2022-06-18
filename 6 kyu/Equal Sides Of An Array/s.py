def find_even_index(arr):
    for i in range(len(arr)):
        if sum(arr[:i]) == sum(arr[i+1:]):
            return i
    return -1
________________________
def find_even_index(lst):
    left_sum = 0
    right_sum = sum(lst)
    for i, a in enumerate(lst):
        right_sum -= a
        if left_sum == right_sum:
            return i
        left_sum += a
    return -1
________________________
def find_even_index(arr):
    left, right = 0, sum(arr)
    for i, e in enumerate(arr):
        right -= e
        if left == right:
            return i
        left += e
    return -1
________________________
def find_even_index(arr):
    for i in range(len(arr)):
        if sum(arr[i:]) == sum(arr[:i+1]):
           return i
    return -1
________________________
def find_even_index(arr):
    sums = [(sum(arr[:i]), sum(arr[i+1:])) for i in range(len(arr))]
    finds = list(map( lambda x: x[0]==x[1],sums))
    return finds.index(True) if True in finds else -1
________________________
def find_even_index(arr):
    arr = [0] + arr + [0]
    for i, num in enumerate(arr[1:-1]):
        if sum(arr[:i+1]) == sum(arr[i+2:]):
            return i
    return -1
________________________
def find_even_index(arr):
    flag = -1
    for i, x in enumerate(arr):
        if sum(arr[:i]) == sum(arr[i+1:]):
            flag = i
            break
    return flag
________________________
def find_even_index(arr):
    t=len(arr)
    N=0
    while N<t:
        g=0
        d=0
        for i in range (N):
            g=g+arr[i]
        for j in range (t-N-1):
            d=d+arr[N+j+1]
        if g==d:
            return N
        else:
            N=N+1       
    return -1
________________________
def find_even_index(arr):
    try:
        return [i for i in range(len(arr)) if sum(arr[:i+1])== sum(arr[i:])][0]
    except IndexError :
        return -1
________________________
def find_even_index(arr):
    for i in range(len(arr)):
        print("i=" + str(i) + ";" + str(sum(arr[:i])) + ":" + str(sum(arr[i+1:])))
        if sum(arr[:i])==sum(arr[i+1:]): 
            return i
    return -1
________________________
def find_even_index(arr):
    L = 0
    R = sum(arr[1:])
    for i in range(len(arr)):
        if L == R:
            return i
        try:
            L += arr[i]
            R -= arr[i+1]
        except IndexError:
            return -1
