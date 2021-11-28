def get_real_floor(n):
    if (n > 0):
        n -= 1
    if (n >= 13):
        n -= 1
    return n

get_real_floor(1)
get_real_floor(5)
get_real_floor(15)
#################
def get_real_floor(n):
    if n <= 0: return n
    if n < 13: return n-1
    if n > 13: return n-2
############
def get_real_floor(n):
    return n if n < 1 else n - 1 if n < 13 else n - 2
##############
def get_real_floor(n):
    return n - (n > 0) - (n > 13)
############
def get_real_floor(n):
    return n - (1 if n < 13 else 2) if n > 0 else n
##############
def get_real_floor(n):
    
    return n - 1 * (n>0) - 1 * (n>13)
#################3
def get_real_floor(n):
    return n - 2 if n > 13 else n - 1 if n > 0 else n
##############
def get_real_floor(n):
    if n == 1:return 0
    elif n == 15:return 13
    elif n == 0:return 0
    else:
        if n > 0 and n < 13:return n - 1
        elif n > 0 and n > 13:return n - 2
        else:return n
###################
def get_real_floor(n):
    if n <= 0:
        return n
    return n - 1 - (n >= 13)
###############
def get_real_floor(n):
    return n-2 if n > 13 \
      else n-1  if n > 0 \
      else n
###############
def get_real_floor(n):
    if 1 <= n < 13:
        return n - 1
    if 13 <= n:
        return n - 2
    if  n <= 0:
        return n
##################
def get_real_floor(n):
    if n<=0:
        return n
    elif n<14:
        return n-1
    elif n==14:
        return 12
    else:
        return n-2
##############
def get_real_floor(n):
    if n > 0 and n >= 13:return n - 2
    elif n > 0 and n < 13: return n - 1 
    else: return n
###############
def get_real_floor(n):
  return n if n < 1 else (n - 2 if (n > 13) else n - 1)
##############
get_real_floor = lambda n: n - ((n > 0) + (n > 12))
##############
def get_real_floor(n):
    return n - (n > 0) * ((n > 0) + (n > 13))
#############
def get_real_floor(n):
    return n if n<0 else 0 if n <=1 else n-1 if n<13 else n-2
#############
get_real_floor = lambda n: n - (n > 0) - (n > 13)
################
def get_real_floor(n):
    return [n, n-1, n-2][(n>0) + (n>13)]
###############
def get_real_floor(n):
    if n<1:
        return n
    ls=[]
    for i in range(1,n+1):
        if i==13:
            pass
        else:
            ls.append(i)
    return ls.index(n)
#############
def get_real_floor(n):
    return n - [2,1][n < 13] if n > 0 else n
##############
get_real_floor = lambda n: n if n <= 0 else n - 1 - int(n >= 13)
##############
def get_real_floor(n):
    return (n - 1) + (n <= 0) - (n > 13)
