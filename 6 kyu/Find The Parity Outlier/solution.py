def find_outlier(integers):
    even = 0
    odds = 0
    for integer in integers:
        result = integer % 2
        if result == 1:
            odds += 1
            output1 = integer
        else:
            even += 1
            output2= integer
    if odds == 1:
        return output1
    elif even == 1:
        return output2
##############
def outlier(i):
    for l in i:
        if l % 2 != 0:
            return l

def find_outlier(i):
    if i[0] % 2 == 0 and i[1] % 2 == 0:
        return outlier(i)
    elif i[0] % 2 == 0 and i[2] % 2 == 0:
        return outlier(i)
    elif i[1] % 2 == 0 and i[2] % 2 == 0:
        return outlier(i)
    else:
        for l in i:
            if l % 2 == 0:
                return l
###############
def find_outlier(integers):
    # takes a group of integers and returns the one integer that is the opposite of them being even or odd
    even = []
    odd = []
    for value in integers:
        if value % 2 == 0:
            even.append(value)
        else:
            odd.append(value)

    if len(even) > len(odd):
        return odd.pop()
    else:
        return even.pop()
##################
def find_outlier(integers):
    first = integers[0] % 2
    second = integers[1] % 2
    for integer in integers[2:]:
        is_even = integer % 2
        if first != second == is_even:
            return integers[0]
        elif first == second != is_even:
            return integer
        elif second != first == is_even:
            return integers[1]
    return None
###############
def find_outlier(integers):    
    if integers[2] % 2 == 0:
        for num in integers: 
            if num % 2 !=0:
                return num
    else:
        for num in integers:
            if num % 2 == 0:
                return num
##################
def find_outlier(integers):
    numeven = 0
    numodd = 0
    even = None
    for integer in integers:
        if integer % 2 == 0:
            numeven += 1
        if integer % 2 != 0:
            numodd += 1
        if numeven > numodd:
            even = True
        if numodd > numeven:
            even = False
    for integer in integers:
        if even == True:
            if integer % 2 != 0:
                N = integer
                continue
        if even == False:
            if integer % 2 == 0:
                N = integer
                continue
    return N

#Comments:
#Need to remember to do a pass to find out whether the array is even or odd first.
#Then from there, all of your info is laid out for you!
########################
def find_outlier(integers):
    r = [[0,0],[0,0]]
    for i in range(3):
        odd_even = integers[i] & 1
        r[odd_even][0] = integers[i]
        r[odd_even][1] += 1
    if r[0][1]:
        if r[0][1] == 1:
            return r[0][0]
        elif r[0][1] == 2:
            return r[1][0]
        else:
            for d in integers[3:]:
                if d & 1:
                    return d
    else:
        for d in integers[3:]:
            if not d & 1:
                return d
##########################
def find_outlier(a):
    if a[0] % 2 == a[1] % 2:
        z = 1 - a[0] % 2
        for i in a:
            if i % 2 == z:
                return i
    else:
        if a[0] % 2 == a[2] % 2:
            return a[1]
        else:
            return a[0]
################
def find_outlier(integers):
    count_even = []
    count_odd = []
    for num in integers:
        if num % 2 == 0:
            count_even.append(num)
        if num % 2 == 1:
            count_odd.append(num)
            
    if len(count_even) == 1:
        return count_even[0]
    else:
        return count_odd[0]
#######################
def find_outlier(integers):
    a = []
    b = []
    
    for x in integers:
        if x%2==0:a.append(x)
        else:b.append(x)
            
    return a[0] if len(a)<len(b) else b[0]
##################
import numpy as np

def find_outlier(integers):
    b = []
    a = []
    for x in integers:
        if x %2 ==0:
            b.append(x)
        else : a.append(x)
            
    if len(a)==1:return a[0]
    elif len(b)==1: return b[0]
    
    else :return "introuvable"
################
def is_even(n):
    ''' Return true if n is even, false is n is odd'''
    return n%2==0

def find_outlier(integers):
    even_number=[is_even(integer) for integer in integers]
    if even_number.count(True)>1:
        return integers[even_number.index(False)]
    else:
        return integers[even_number.index(True)]
#################
def find_outlier(integers):
    ans = [int(elem)%2 for elem in integers]
    return(integers[ans.index(0)] if ans.count(0)==1 else integers[ans.index(1)])
######################
def find_outlier(integers):
    odds = []
    evens = []
    for i in integers:
        [evens.append(i) if i % 2 == 0 else odds.append(i)] 
    
    if len(evens) > len(odds):
        return odds[0]
    else:
        return evens[0]
###################
def find_outlier(integers):
    even_count = 0
    odd_count = 0
    
    for i in range(0, 3):
        if integers[i] % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    
    compare = 0
    if even_count > 1:
        compare = 1
    
    for num in integers:
        if num % 2 == compare:
            return num
############################
def find_outlier(integers):
    o = 0
    oh =None
    e = 0 
    eh = None
    
    
    for x in integers:
        print(f'x  {x} e {e} eh {eh} o {o} oh {oh}')
#        if e and o:
#            return x
        if x % 2 : # odd processing
            o +=1
            if e >1:
                return x
            else:
                oh = x
        else:  #even processing
            e += 1
            if o > 1:
                return x
            else:
                eh = x
                
    if e == 1:
        return eh
    elif o == 1:
        return oh
    else: 
        print ("oopsie")
########################
def find_outlier(integers):
    odds = []
    for n in integers[:3]:
        if n%2 ==0:
            pass
        else:
            odds.append(n)
    if len(odds) >= 2:
        n = [i for i in integers if i%2==0]
    else:
        n = [i for i in integers if i%2!=0]        
    return n[0]
####################
def find_outlier(integers):
    return next(filter(lambda x: x % 2 == 1, integers)) if list(filter(lambda x: x % 2 == 0, integers)).__len__() > 1 else next(filter(lambda x: x % 2 == 0, integers))
