def survivors(list_of_momentum, list_of_powerups):
    output = []
    i = 0
    for momentum, powerups in zip(list_of_momentum, list_of_powerups):
        if momentum <= 0:
            i = i + 1
            continue
        isSuccess = True
        for element in powerups:
            momentum = momentum + (element - 1)
            if momentum <= 0:
                isSuccess = False
                break
        if isSuccess or momentum > 0:
            output.append(i)
            
        i = i + 1
        
    return output
  
#################
from itertools import accumulate

def survivors(ms, pss):
    return [i
        for i, (m, pss) in enumerate(zip(ms, pss))
        if all(m > 0 for m in accumulate(pss, lambda m, p: m - 1 + p, initial=m))]
  
#############
def good_boy(m, P):
    for p in P:
        if m <= 0: return False
        m += p-1
    return m>0

survivors = lambda M, LP: [i for i, P in enumerate(LP) if good_boy(M[i], P)]

##########
def survivors(list_of_momentum, list_of_powerups):
    lst = []
    for i in range(len(list_of_momentum)):
        mom = list_of_momentum[i]
        if not mom:
            continue
        for x in list_of_powerups[i]:
            mom = mom - 1 + x
            if mom < 1:
                break
        if mom >= 1:
            lst.append(i)
    return lst
  
############
def survive(momentum, powerups):
    for powerup in powerups:
        if momentum < 1:
            break
        momentum += powerup - 1
    return momentum >= 1


def survivors(list_of_momentum, list_of_powerups):
    return [
        i
        for i, (momentum, powerups) in enumerate(zip(list_of_momentum, list_of_powerups))
        if survive(momentum, powerups)
    ]
  
##############
from itertools import accumulate
def survivors(list_of_momentum, list_of_powerups):
    r=[all(n>0 for n in accumulate(j,lambda x,y: x-1+y, initial=i)) for i,j in zip(list_of_momentum, list_of_powerups)]
    return [a for a,b in enumerate(r) if b]
  
###############
def survivors(list_of_momentum, list_of_powerups):
    res = []
    for i,(m,p) in enumerate(zip(list_of_momentum, list_of_powerups)):
        for x in p:
            if m == 0:
                break
            m += x-1
        else:
            if m:
                res.append(i)
    return res
  
##############
def survivors(list_of_momentum, list_of_powerups):
    l=[]
    for i in range(len(list_of_momentum)):
        for j in list_of_powerups[i]:
            if list_of_momentum[i]>=1:
                if j==0:
                    list_of_momentum[i]-=1
                else:
                    list_of_momentum[i]+=j
                    list_of_momentum[i]-=1
        if list_of_momentum[i]>=1:
            l.append(i)
    return l
  
#############
def survivors(list_of_momentum, list_of_powerups):
    return [i for i in range(len(list_of_momentum)) if list_of_momentum[i] > 0 and all(l > 0 for l in [list_of_momentum[i] - j - 1 + sum(list_of_powerups[i][:j+1]) for j in range(len(list_of_powerups[i]))])]
  
##############
def survivors(list_of_momentum, list_of_powerups):
    l=[]
    for i in range(len(list_of_momentum)):
        for j in list_of_powerups[i]:
            if list_of_momentum[i]>=1:
                if j==0:
                    list_of_momentum[i]-=1
                else:
                    list_of_momentum[i]+=j
                    list_of_momentum[i]-=1
        if list_of_momentum[i]>=1:
            l.append(i)
    return l
  
##############
def survive(momentum, powerups):
    j = 0
    while momentum > 0 and j <len(powerups):
        momentum -= 1
        momentum += powerups[j]
        j += 1
    if momentum>0:
        return True
    return False

def survivors(list_of_momentum, list_of_powerups):
    results = []
    for i in range(len(list_of_momentum)):
        momentum = list_of_momentum[i]
        powerups = list_of_powerups[i]
        if survive(momentum, powerups):
            results.append(i)
    return results
  
#################
def survives(momentum, powerups):
    pos = -1
    while momentum > 0 and pos < len(powerups):
        momentum = momentum - 1
        pos = pos + 1
        if pos < len(powerups):
            momentum = momentum + powerups[pos]
    return pos == len(powerups)
    
def survivors(list_of_momentum, list_of_powerups):
    result = []
    
    for idx, momentum in enumerate(list_of_momentum):
        powerups = list_of_powerups[idx]
        if survives(momentum, powerups):
            result.append(idx)
    
    return result
  
##############
def survivors(list_of_momentum, list_of_powerups):
    result = list()
    for i in range(0, len(list_of_momentum)):
        m = list_of_momentum[i]
        ok = True
        for p in list_of_powerups[i]:
            if m <= 0:
                ok = False
                break
            m -= 1
            m += p
        if ok and m > 0:
            result.append(i)
    return result
  
##################
def survivors(a, b):
    x = []
    for index, value in enumerate(a):
        n, length = value, len(b[index])
        for i in range(length):
            if value - 1 < 0: break
            n += b[index][i] - 1
            if n < 1: break
        if n > 0: x.append(index)
    return x
  
####################
def survivors(list_of_momentum, list_of_powerups):
    answer = []
    for i in range(len(list_of_momentum)):
        m = list_of_momentum[i]
        if m == 0:
            continue
        for p in list_of_powerups[i]:
            m -= 1
            m += p
            if m == 0:
                break
        if m > 0:
            answer.append(i)
    return answer
  
#################
def survivors(list_of_momentum, list_of_powerups):
    list_of_pass = []
    for i in range(len(list_of_momentum)):
        for p in list_of_powerups[i]:
            list_of_momentum[i] -= 1
            if list_of_momentum[i] < 0:
                break
            list_of_momentum[i] += p

        if list_of_momentum[i]>0:
            list_of_pass.append(i)
    

    return list_of_pass
  
#################
def survivors(list_of_momentum, list_of_powerups):
    lom = list_of_momentum
    lop = list_of_powerups
    ret = []
    for n in range(len(lom)):
        for p in lop[n]:
            if lom[n] == 0:
                break
            else:
                lom[n] = lom[n] + p - 1
        if lom[n] != 0:
            ret.append(n)
    return ret
