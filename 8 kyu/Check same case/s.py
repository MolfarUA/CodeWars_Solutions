def same_case(a,b):
	if a.islower() and b.islower():
		return 1
	elif a.isupper() and b.isupper():
		return 1
	elif not a.isalpha() or not b.isalpha():
		return -1
	else:
		return 0
_________________________
def same_case(a, b): 
    if a.isalpha() and b.isalpha():
        if (a.islower() and b.islower()) or (a.isupper() and b.isupper()):
            return 1
        else:
            return 0
    else:
        return -1
__________________________
def same_case(a, b): 
    return -1*(not(a+b).isalpha()) or not a.islower()^b.islower()
__________________________
def same_case(a, b): 
    upper = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    lower = set('abcdefghijklmnopqrstuvwxyz')
    if a in upper and b in upper:
        return 1
    elif a in lower and b in lower:
        return 1
    elif a in upper and b in lower:
        return 0
    elif a in lower and b in upper:
        return 0
    else:
        return -1 
__________________________
def same_case(x,y): 
    a = ord(x)
    b = ord(y)
    upp = range(65,91)
    lower = range(97,123)
    if(a in upp):
        if (b in upp):
            return 1
        elif(b in lower):
            return 0
        else:
            return -1
    elif(a in lower):
        if(b in lower):
            return 1
        if(b in upp):
            return 0
        else:
            return -1
    else:
        return -1
__________________________
same_case = lambda *C: not all(c.isalpha() for c in C) and -1 or all(c.isupper() for c in C) or all(c.islower() for c in C)
__________________________
from string import ascii_letters as c

same_case = lambda a, b: a.isupper() == b.isupper() if a in c and b in c else -1
__________________________
def same_case(a, b): 
    if not (a.isalpha() and b.isalpha()): return -1
    return a.isupper() == b.isupper()
__________________________
def same_case(a, b): 
    return -1 if not(a.isalpha() and b.isalpha()) else a.isupper() == b.isupper()
__________________________
def same_case(a, b): 
    aLower,bLower,aUpper,bUpper = False,False,False,False
    if ord(a) <=122 and ord(a)>=97:
        #lower
        aLower=True
    if ord(b) <=122 and ord(b)>=97:
        #lower
        bLower=True
    if ord(b) <=90 and ord(b)>=65:
        #upper
        bUpper=True
    if ord(a) <=90 and ord(a)>=65:
        #upper
        aUpper=True
    print(aLower,bLower,aUpper,aUpper)
    if (aUpper and bUpper) or (aLower and bLower):
        return 1
    if (aUpper and bLower) or (aLower and bUpper):
        return 0
    return -1
__________________________
from string import ascii_letters

def same_case(a, b): 
    if (a.isupper() and b.isupper()) or (a.islower() and b.islower()):
        return 1
    else:
        if a in ascii_letters and b in ascii_letters:
            return 0
        else:
            return -1
__________________________
def same_case(a, b): 
    lower_count = 0
    upper_count = 0
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(len(lower)):
        if a == lower[i]:
            lower_count+= 1
        if b == lower[i]:
            lower_count+=1
        if a == upper[i]:
            upper_count+=1
        if b == upper[i]:
            upper_count+=1
    if upper_count == 2:
        return 1
    elif lower_count == 2:
        return 1
    elif upper_count == 1 and lower_count ==1:
        return 0
    else:
        return -1
__________________________
def same_case(a, b):
    return sum(65<=n<=90 and 1 or 97<=n<=122 and 2 for n in map(ord, (a, b))) in {2, 4} if all(x.isalpha() for x in (a, b)) else -1
__________________________
def same_case(a, b): 
    if ord(a) not in range(65, 91) and ord(a) not in range(97, 123):
        return -1
    if ord(b) not in range(65 , 91) and ord(b) not in range(97, 123):
        return -1
    if ord(a) in range(65, 91):
        if ord(b) in range(65, 91):
            return 1
    if ord(a) in range(97, 123):
        if ord(b) in range(97, 123):
            return 1    
    return 0
    
