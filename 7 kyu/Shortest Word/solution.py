def find_short(s):
    return len(sorted(s.split(' '), key = len)[0])

##############
def find_short(s):
    s = s.split() # splits the string into a list of individual words
    l = min(s, key = len) # finds the shortest string in the list
    return len(l) # returns shortest word length

##############
def find_short(s):
    return min(len(a) for a in s.split())

###########
def find_short(s):
    sList = s.split()
    shortestLength = len(sList[0])
    for item in sList:
        if len(item) < shortestLength:
            shortestLength = len(item)
    return shortestLength

############
def find_short(s):
    return len(sorted(s.split(), key=len)[0])

##############
def find_short(s):
    l = 100000;
    a = s.split(" ")
    for i in a:
        if(len(i)<l):
            l = len(i)
    return l # l: shortest word length

############
def find_short(s):
    l = 100
    s = s.split()
    for w in s:
        lenght = int(len(w))
        if l > lenght:
            l = lenght
    return l 

###########
def find_short(s):
    '''Return the length of the shortest word in a string of words'''
    words = s.split(" ")
    l = len(words[0])
    for word in words:
        if len(word) < l:
            l = len(word)
            print(l)
    return l # l: shortest word length

############
def find_short(s):
    lst = s.split(" ")
    shortest = len(lst[0])
    
    for word in lst:
        if len(word) < shortest:
            shortest = len(word)
        continue
    return shortest
    
###############
def find_short(s):
    s, result = [s], []
    subs = " ".join(s).split() 
    for i in subs:
        result.append(len(i))
    return min(result)
