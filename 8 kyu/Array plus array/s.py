5a2be17aee1aaefe2a000151


def array_plus_array(arr1,arr2):
    return sum(arr1+arr2)
_________________________
def array_plus_array(arr1,arr2):
    return sum(arr1) + sum(arr2)
_________________________
def array_plus_array(arr1,arr2):
    counter = 0
    for i in arr1:
        counter += i
    for i in arr2:
        counter += i
    return counter
_________________________
def array_plus_array(a, b):
    return sum(a+b)
_________________________
from itertools import chain
def array_plus_array(arr1,arr2):
    return sum(chain(arr1, arr2))
_________________________
array_plus_array=lambda a,b: sum(a+b)
_________________________
def array_plus_array(*args):
    return sum(map(sum, args))
_________________________
def array_plus_array(arr1,arr2):
    result=0
    for ar1,ar2 in zip(arr1,arr2):
        result = result + (ar1+ar2)
    return result
_________________________
array_plus_array = lambda _,__:sum(_)+sum(__)
_________________________
def array_plus_array(arr1,arr2):
    united_arr = arr1+arr2
    summa = 0
    for num in united_arr:
        summa += num
    return summa
_________________________
def array_plus_array(arr1,arr2):
    sum1=0
    sum2=0
    sum3=0
    for i in arr1:
        sum1=sum1+i
    for x in arr2:
        sum2=sum2+x
    sum3=sum1+sum2
    return sum3
_________________________
def array_plus_array(arr1,arr2):
    a =  sum(x for x in arr1)
    b = sum(y for y in arr2)
    return a + b
_________________________
def array_plus_array(arr1,arr2):
    return sum(map(sum, zip(arr1, arr2)))
_________________________
def array_plus_array(arr1,arr2):
    arr3=arr1+arr2
    tot=0
    for i in arr3:
        tot+=i
    return tot
