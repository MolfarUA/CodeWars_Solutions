def paperwork(n, m):
    if n < 0:
        return 0
    elif m < 0:
        return 0
    else:
        return n * m
###########
def paperwork(n, m):
    return n * m if n > 0 and m > 0 else 0
############
def paperwork(n, m):
    if m<0 or n<0:
        return 0
    else:
        return n*m
###########
def paperwork(n, m):
    return max(n, 0)*max(m, 0)
###########
def paperwork(n, m):
    return n*m if n>=0 and m>=0 else 0
#############
def paperwork(n, m):
    return 0 if n < 0 or m < 0 else n*m
###########
def paperwork(n, m):
    if m > 0 and n > 0:
        return m*n
    else:
        return 0
#############
paperwork = lambda a,b: a*b if min(a,b)>0 else 0
#############
paperwork = lambda m,n: m*n if m>0 and n>0 else 0
############
def paperwork(n, m):
    return n * m if min((n, m)) > 0 else 0
###########
def paperwork(n, m):
  #Declaring the variable with a value makes it local instead of global
  ans = 0
  
  #Checks that n and m are > 0 before doing the math
  if n and m > 0:
    ans = n * m
  
  #Throws out any answers that are negative
  if ans <= 0:
    ans = 0
    
  #Returns the ans variable  
  return ans
##################################
def paperwork(n, m):
    return m*n * int(n > 0 and m > 0)
##############
def paperwork(n,m): return m*n if (m>0) & (n>0) else 0
###############
def paperwork(n, m):
    if n >= 0 and m >= 0:
        return n * m
    elif n < 0 or m < 0:
       return 0
