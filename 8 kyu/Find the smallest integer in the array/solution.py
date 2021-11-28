def find_smallest_int(arr):
    return min(arr)
###################
findSmallestInt=min
################
def findSmallestInt(arr):
    #sort array
    arr.sort()
    return arr[0]
###################
def findSmallestInt(arr):
    return min(arr)
#################
def findSmallestInt(arr):
    smallest = []
    for i in range(0,len(arr)):
        if (arr[i] < smallest):
            smallest = arr[i]
    return smallest
##################
def findSmallestInt(arr):
    return reduce(lambda x,y: x if x<y else y, arr)
################
def find_smallest_int(arr):
  return sorted(arr)[0]
##################
findSmallestInt = lambda a: sorted(a)[0]
##############
def findSmallestInt(arr):
    """
    input: arr, a list of integers
    output: smallest integer in arr
    """
    
    # check that each element is an int
    for num in arr:
        assert type(num) == int
    
    # sort array
    arr.sort()
    
    # return smallest value
    return arr[0]
############################
def findSmallestInt(arr):
    a=arr[0]
    for i in range(1,len(arr)):
        if arr[i]<a:
            a=arr[i]
    return a
################
def findSmallestInt(arr):
    min = arr[0]
    for item in arr:
        if min > item:
            min = item
    return min
##################
def find_smallest_int(arr):
    return min(arr);
##################
find_smallest_int = min  
