def positive_sum(arr):
    return sum([x for x in arr if x >= 0])

positive_sum([1,2,3,4,5])
positive_sum([1,-2,3,4,5])
positive_sum([-1,2,3,4,-5])
###################
def positive_sum(arr):
    return sum(x for x in arr if x > 0)
###############
def positive_sum(arr):
    sum = 0
    for e in arr:
        if e > 0:
            sum = sum + e
    return sum
#############
def positive_sum(arr):
    return sum(filter(lambda x: x > 0,arr))
##############
def positive_sum(list):
    answer = 0
    for numbers in list: 
        if numbers > 0:
            answer += numbers
    return answer
#####################
def positive_sum(arr):
    return sum( max(i, 0) for i in arr )
#################
def positive_sum(arr):
    L = []
    for i in arr:
        if (i > 0):
            L.append(i)
    return (sum(L))
#################
positive_sum = lambda a: sum(e for e in a if e > 0)
#################
def positive_sum(arr):
    return sum([i for i in arr if i==abs(i)])
##################
def positive_sum(arr):
    nums = [num for num in arr if num > 0]
    return sum(nums)
#######################
import itertools
def positive_sum(arr):
    return sum(itertools.ifilter(lambda e: 0 <= e, arr))
################
def positive_sum (arr):
    mynewnum=0
    for mynum in arr:
        if mynum > 0:
            mynewnum= mynewnum + mynum
    if len(arr) != 0:
            return mynewnum
    else:
            return 0
##################
def positive_sum (arr):
    mynewnum=0
    for mynum in arr:
        if mynum > 0:
            mynewnum= mynewnum + mynum
    if len(arr) != 0:
            return mynewnum
    else:
            return 0
