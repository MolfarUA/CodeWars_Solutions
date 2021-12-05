import numpy as np
def calculate_1RM(w, r):
    if r == 0:
        return 0
    elif r == 1:
        return w
    else:
        res=[]
        epley = w*(1+r/30)
        res.append(round(epley))
        mcglothin = 100*w/(101.3-2.67123*r)
        res.append(round(mcglothin))
        lombardi = w*r**0.10
        res.append(round(lombardi))
        return np.max(res)
##################
def calculate_1RM(w, r):
    if r == 0: return 0
    if r == 1: return w
    
    return round(max([
      w * (1 + r / 30),                 # Epley
      100 * w / (101.3 - 2.67123 * r),  # McGlothin
      w * r**0.10                       # Lombardi
      ]))
#################
epley     = lambda w,r: w * (1+r/30)
mcGlothin = lambda w,r: 100*w / (101.3 - 2.67123*r)
lombardi  = lambda w,r: w * r**0.10

def calculate_1RM(w, r):
    return r and (w if r == 1 else round(max(epley(w,r), mcGlothin(w,r), lombardi(w,r))))
#############
def calculate_1RM(w, r):
    rme = w * (1 + (r / 30))
    rmg = (100 * w) / (101.3 - (2.67123 * r))
    rml = w * (r ** 0.10)
    if r == 0: return 0
    if r == 1: return w
    else:
        rm = int(round(max(rme, rmg, rml)))
    return rm
##############
def calculate_1RM(w, r):
    rm = 0
    rme = w * (1 + (r / 30))
    rmg = (100 * w) / (101.3 - (2.67123 * r))
    rml = w * (r ** 0.10)
    if r == 1:
        rm = w
    elif r == 0:
        return rm
    else:
        rm = int(round(max(rme, rmg, rml)))
    return rm
#################
def calculate_1RM(w, r):
    rm = 0
    if r != 0 and r != 1:
        rme = w*(1+(r/30))
        rmg = (100*w)/(101.3-(2.67123*r))
        rml = w*(r**0.10)
        if rme > rmg and rme > rml:
            rm = int(round(rme))
        elif rmg > rme and rmg > rml:
            rm = int(round(rmg))
        else:
            rm = int(round(rml))
    elif r == 1:
        rm = w
    else:
        return rm
    return rm
########################
import math
def calculate_1RM(w, r):
    print(w,r)
    if(r==1):
        return w
    if(r==0):
        return 0
    lst=[]
    lst.append(w*(1+r/30))
    lst.append(100*w/(101.3-2.67123*r))
    lst.append(w*pow(r,0.10))
    if((max(lst)-int(max(lst)))<0.5):
        return int(max(lst))
    else:
        return abs(math.floor(-1*max(lst)))
##################
def calculate_1RM(w, r):
  epley = lambda w, r: w * (1 + r / 30)
  mc_glothin = lambda w, r: 100 * w / (101.3 - 2.67123 * r)
  lombardi = lambda w, r: w * r ** 0.1

  if r == 1: return w
  if r == 0: return 0
  ret = max([epley(w, r), mc_glothin(w, r), lombardi(w, r)])
  q = int(ret)
  if ret - q <= 0.5:
    return q
  else:
    return q + 1
################
def calculate_1RM(w, r):
    if r == 0:
        return 0
    if r == 1:
        return w
    
    epley = round(w*(1+r/30))
    mcglothin = round(100*w / (101.3-2.67123*r))
    lombardi = round(w*r**0.10)
    return max(epley,mcglothin,lombardi)
#################
def calculate_1RM(w, r):
    if r == 0: return 0
    if r == 1: return w
    a = w * (1 + (r/30))
    b = (100*w)/(101.3 - (2.67123*r))
    c = w * (r**(0.10))
    return round(max(a,b,c))
###############
def calculate_1RM(w, r):
    if r == 1:
        return w
    elif r == 0:
        return 0
    Epley = w*(1+r/30)
    McGlothin = 100*w/(101.3-2.67123*r)
    Lombardi = w*r**.1
    return round(max(Epley, McGlothin, Lombardi))
###############
def calculate_1RM(w, r):
    Epley=w*(1+r/30)
    McGlothin=100*w/(101.3-2.67123*r)
    Lombardi=w*r**.1
    return w if r==1 else 0 if r==0 else round(max(Epley,McGlothin,Lombardi))
##############
def calculate_1RM(w, r):
    epley = lambda w, r: w * (1 + (r / 30))
    mcglothin = lambda w, r: (w * 100) / (101.3 - r * 2.67123)
    lombardi = lambda w, r: w * r ** 0.10
    if not r:
        return 0
    if r == 1:
        return w
    return round(max(epley(w, r), mcglothin(w, r), lombardi(w, r)))
