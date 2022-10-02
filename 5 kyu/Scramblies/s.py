55c04b4cc56a697bb0000048


def scramble(s1,s2):
    for c in set(s2):
        if s1.count(c) < s2.count(c):
            return False
    return True
______________________________
from collections import Counter
def scramble(s1,s2):
    # Counter basically creates a dictionary of counts and letters
    # Using set subtraction, we know that if anything is left over,
    # something exists in s2 that doesn't exist in s1
    return len(Counter(s2)- Counter(s1)) == 0
______________________________
def scramble(s1, s2):
    return not any(s1.count(char) < s2.count(char) for char in set(s2))
______________________________
def scramble(s1,s2):
    dct={}
    for l in s1:
        if l not in dct:
            dct[l]=1
        else:
            dct[l] +=1
    for l in s2:
        if l not in dct or dct[l] < 1:
            return False
        else:
            dct[l] -= 1
    return True
______________________________
from collections import Counter

def scramble(s1, s2):
    s1_c, s2_c = Counter(s1.lower()), Counter(s2.lower())
    return all(s1_c[x] >= s2_c[x] for x in s2_c)
______________________________
def scramble(s1, s2):
    ss2 = set(s2)
    count = 0
    for i in ss2:
        if s1.count(i) >= s2.count(i):
            count += 1
    return count == len(ss2)
______________________________
from collections import Counter
def scramble(s1, s2):
    d1 = Counter(s1)
    d2 = Counter(s2)
    return all(d1.get(x, 0) >= y for x, y in d2.items())
______________________________
def diter(s):
    d={}
    for el in s:
        if el not in d.keys():
            d[el]=1
        else:
            d[el]+=1
    return d
def scramble(s1, s2):
    d1=diter(s1)
    d2=diter(s2)
    for key,val in d2.items():
        if key in d1.keys():
            if d1[key]<val:
                return False
        else:
            return False
    return True 
