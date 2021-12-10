def last_survivors(arr, nums):
    return ''.join(map(shrink, zip(*arr), nums))
def shrink(col, n):
    return ''.join(col).replace(' ', '')[:-n or len(col)]
  
##########
def survive(xs, num):
    s = "".join(xs).replace(" ", "")
    return s[:-num or None]

def last_survivors(arr, nums):
    return "".join(x for xs, num in zip(zip(*arr), nums) for x in survive(xs, num))
  
###########
def last_survivors(arr, nums):
    return ''.join(''.join(filter(str.isalpha, s))[:-n or None] for s, n in zip(zip(*arr), nums))
  
###########
def last_survivors(arr, nums):
    return ''.join(''.join(i).replace(' ','')[:(-j if j else None)] for i,j in zip(zip(*arr),nums))
  
#########
def last_survivors(arr, nums):
    if arr==[]:
        return ''
    l=[]
    for i in range(len(max(arr))):
        s=''
        for j in range(len(arr)):
            if arr[j][i]!=' ':
                s=arr[j][i]+s
        l.append(s)
    
    for i in range(len(nums)):
        if nums[i]==0:
            pass
        elif nums[i]>=len(l[i]):
            l[i]=''
        else:
            l[i]=(l[i])[nums[i]:]

    return ''.join(sorted(l))
  
###################
import numpy as np
import re
def last_survivors(arr,nums):
    arr=np.asarray([ list(i) for i in arr[::-1]]).T
    s = [''.join(j for j in i if j != ' ') for i in arr]
    
    for ind, i in enumerate(s):
        print(ind,i)
        if nums[ind]:
            s[ind] = re.sub('[\w]', '',i, nums[ind])
    
    res = ''.join(i for i in s)
    
    return res
  
##################
def last_survivors(arr, nums):
    nuums = nums
    aarr = arr
    mm = []
    lensword = 0
    for i in nuums:
        m = i
        print("m:", m)
        print("lensword:", lensword)
        for j in range(len(aarr)-1,-1,-1):
            print("aarr[j][lensword]:", aarr[j][lensword])
            print(aarr[j][lensword].isalpha())
            if aarr[j][lensword].isalpha() == False:
                continue
            if aarr[j][lensword] == None:
                j == 0
                continue
            if m == 0 or aarr[j][lensword] == " ":
                mm.append(aarr[j][lensword])
            if aarr[j][lensword].isalpha() == True and m != 0:
                mm.append(" ")
                print("mm:", mm)
                m -= 1
        lensword += 1
    b = ''.join(mm)
    print ("b:", b)
    bb = b.replace(" ", "")
    print ("bb:", bb)
    return bb
  
################
def last_survivors(arr, nums):
    nuums = nums
    aarr = arr
    mm = []
    lensword = 0
    for i in nuums:
        m = i
        print("m:", m)
        print("lensword:", lensword)
        for j in range(len(aarr)-1,-1,-1):
            print("aarr[j][lensword]:", aarr[j][lensword])
            print(aarr[j][lensword].isalpha())
            if aarr[j][lensword].isalpha() == False:
                continue
            if aarr[j][lensword] == None:
                j == 0
                continue
            if m == 0 or aarr[j][lensword] == " ":
                mm.append(aarr[j][lensword])
            if aarr[j][lensword].isalpha() == True and m != 0:
                mm.append(" ")
                print("mm:", mm)
                m -= 1
        lensword += 1
    b = ''.join(mm)
    print ("b:", b)
    bb = b.replace(" ", "")
    print ("bb:", bb)
    return bb
  
##############
def last_survivors(arr, nums):
    survivivors = list()
    i = 0
    for n in nums:
        m = n
        for r in arr[::-1]:
            if r[i] != " ":
                if m == 0:
                    survivivors.append(r[i])
                else:
                    m -= 1
        i += 1
    return "".join(survivivors)
  
##############
def last_survivors(arr, nums):
    arr = list(map(list, arr))
    for i, num in enumerate(nums):
        for j, _ in enumerate(arr):
            if num > 0 and arr[-j-1][i] != ' ':
                arr[-j-1][i] = ' '
                num -= 1
    return ''.join(char for row in arr for char in row if char != ' ')
  
#############
def last_survivors(arr, nums):
    return ''.join(i[n:] for i, n in zip((''.join(s).replace(' ', '') for s in zip(*arr[::-1])), nums))
  
###########
def last_survivors(arr, nums):
    arr = list(map(list,arr))
    for j in range(len(nums)):
        k = len(arr)-1
        while k >= 0 and nums[j] > 0:
            if arr[k][j].isalpha():
                arr[k][j] = ' '
                nums[j] -= 1
            k -= 1
    answer = ''
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j].isalpha():
                answer += arr[i][j]
    return answer
  
###########
def last_survivors(a, n):
    if not a or not n: return ''
    return ''.join([''.join(a[-i][j] for i in range(1, len(a) + 1)).replace(" ", "")[k:] for j, k in zip(range(len(a[0])), n)])
