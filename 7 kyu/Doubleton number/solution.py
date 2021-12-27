def doubleton(num):
    num += 1
    while True:
        num_set = set(str(num))
        if len(num_set) != 2:
            num += 1
        else:
            return num
print(doubleton(123))
print(doubleton(121))

#################
def doubleton(num):
    n = num + 1
    while len(set(str(n))) != 2:
        n += 1
    return n
  
###########
from itertools import count

def doubleton(num):
    return next(n for n in count(num+1) if len(set(str(n))) == 2)
  
#############
def doubleton(num):
    is_doubleton = False
    
    while not is_doubleton:
        num += 1
        if len(set([int(i) for i in str(num)])) == 2:
            is_doubleton = True
            
    return num
        
################
def doubleton(num):
    return next(n for n in range(num+1,num*10) if len(set(str(n)))==2)
  
###############
def doubleton(num):
    l=''
    while len(l)!=2:
        num+=1
        l=set(map(int,str(num))) 
    return num
  
################
def help(l):
    s = set()
    for item in l:
        if item not in s:
            s.add(item)
    if len(s)!=2:
        return False
    else:
        return True
    
def doubleton(num):
    num +=1
    while not help(str(num)):
        num +=1
    return num

#################
def doubleton(num):
    num += 1
    while len({*str(num)}) != 2:
        num += 1
    return num
  
 ################
def doubleton(num):
    num = str(num)
    n = set()
    for elem in num:
        n.add(elem)
    if len(n) == 2:
        num = int(num)+1
        num = str(num)
        n = set()
        for elem in num:
            n.add(elem)
        while len(n) != 2:
            num = int(num)+1
            num = str(num)
            n = set()
            for elem in num:
                n.add(elem)
    else:
        while len(n) != 2:
            num = int(num)+1
            num = str(num)
            n = set()
            for elem in num:
                n.add(elem)
    return int(num)
