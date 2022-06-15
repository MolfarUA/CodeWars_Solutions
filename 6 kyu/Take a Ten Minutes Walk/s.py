def isValidWalk(walk):
    return len(walk) == 10 and walk.count('n') == walk.count('s') and walk.count('e') == walk.count('w')
__________________________________________
def isValidWalk(walk):
    if (walk.count('n') == walk.count('s') and 
        walk.count('e') == walk.count('w') and
        len(walk) == 10):
            return True
    return False
__________________________________________
def isValidWalk(walk):
    if len(walk) != 10:
        return False

    x, y = 0, 0

    for direction in walk:
        if direction == 'n':
            y += 1
        elif direction == 's':
            y -= 1
        elif direction == 'e':
            x += 1
        elif direction == 'w':
            x -= 1
        else:
            return False

    return x == 0 and y == 0
__________________________________________
from collections import Counter

def isValidWalk(walk):
    if len(walk) == 10:
        walkmap = Counter(walk)
        return walkmap['n'] == walkmap['s'] and walkmap['e'] == walkmap['w']
    return False
__________________________________________
def isValidWalk(walk):
  return len(walk) == 10 and walk.count('w') == walk.count('e') and walk.count('n') == walk.count('s')
__________________________________________
def isValidWalk(walk):
  if len(walk) != 10:
    return False
  return walk.count('n') == walk.count('s') and walk.count('e') == walk.count('w')
__________________________________________
def is_valid_walk(walk):
    n=walk.count("n")
    w=walk.count("w")
    s=walk.count("s")
    e=walk.count("e")
    total=n+w+e+s
    if e==w and n==s and total==10:
        return True
    else:
        return False
__________________________________________
def is_valid_walk(walk):
    directions = ['n', 's', 'w', 'e']
    steps = {c:walk.count(c) for c in directions for i in walk}
    return len(walk) == 10 and steps['w'] - steps['e'] == 0 and steps['n'] - steps['s'] == 0 
__________________________________________
def is_valid_walk(walk):
    return (walk.count('n') == walk.count('s')) and\
           (walk.count('w') == walk.count('e')) and\
           (len(walk) == 10)
__________________________________________
def is_valid_walk(walk):
    used=[]
    x=0
    y=0
    for direction in range(len(walk)):
        if direction not in used:
            used.append(direction)
        if walk[direction]=="n":
            y+=1
        elif walk[direction]=="s":
            y-=1
        elif walk[direction]=="w":
            x-=1
        elif walk[direction]=="e":
            x+=1
    if x==0==y and len(walk)==10:
        return True
    else:
        return False
__________________________________________
 
def is_valid_walk(walk):
    i = 0
    passo = 0    
    if (len(walk) == 0) or (len(walk) == 1):
        return False
    
    elif (len(walk) == 10):
        while True:
            match walk[i]:
                case 'n':
                    passo = passo + 1 
                case 's':
                     passo = passo - 1
                case 'w':
                     passo = passo + 2
                case 'e':
                     passo = passo -2
                case _:
                    passo = passo
            if i != 9:
                i = i + 1
            else:
                if passo != 0:
                    return False
                else:
                    return True
    else:
        return False
    
    return False
