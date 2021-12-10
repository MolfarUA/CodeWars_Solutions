def last_survivor(letters, coords): 
    l = [x for x in letters]
    [l.pop(x) for x in coords]
    return l[0]
  
############
def last_survivor(letters, coords):
    for x in coords:
        letters = letters[0:x] + letters[x+1:]
    return letters
  
############
def last_survivor(string: str, indices: list) -> str:
    lst = list(string)
    for i in indices: del lst[i]
    return lst[0]
  
##########
def last_survivor(letters, coords): 
    letters = list(letters)
    for coord in coords:
        letters.pop(coord)
    return letters[0]
  
#############
from functools import reduce

last_survivor=lambda a,b:reduce(lambda s,i:f'{s[0:i]}{s[i + 1:]}',b,a)

############
def last_survivor(letters, coords): 
    for i in range(len(coords)):
        letters = letters[:coords[i]] + letters[coords[i] + 1:]
    return letters
  
############
last_survivor=f=lambda l,c:l*(not c)or f(l[:c[0]]+l[c[0]+1:],c[1:])

##########
def last_survivor(letters, coords): 
    xs = list(letters)
    for i in coords:
        del xs[i]
    return ''.join(xs)
  
###########
def last_survivor(letters, coords): 
  return ([letters] + [letters := letters[:i] + letters[i+1:] for i in coords])[-1]

##########
def last_survivor(letters, coords):
    lst = list(letters)
    for c in coords:
        lst.pop(c)
    return lst.pop()
  
############
def last_survivor(letters, coords):
    res = list(letters)
    for item in coords:
        del res[item]
    return "".join(res)
  
###########
def last_survivor(letters: str, coords: list) -> str: 
    for coord in coords:
        letters = letters[:coord] + letters[coord+1:]
    return letters
  
#############
def last_survivor(s, idxs):
    _s = s[:]
    for i in idxs:
        _s = _s[:i] + _s[i+1:]
    return _s
  
###########
last_survivor=(lambda x:lambda f,g:x(f,g,x))(lambda f,g,x:f if g==[]else x(f[:g[0]]+f[g[0]+1:],g[1:],x))

###########
def last_survivor(s, a): 
    for j in a:
        s = [s[i] for i in range(len(list(s))) if i != j]
    return ''.join(s)
  
#############
def last_survivor(letters, coords):
    while coords != []:
        letters = letters[:coords[0]] + letters[coords[0]+1:]
        if coords != []:
            del coords[0]        
    return letters
