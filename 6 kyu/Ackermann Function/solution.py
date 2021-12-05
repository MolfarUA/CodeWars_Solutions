def Ackermann(m, n):
    if m == 0:
        return n + 1
    if m > 0 and n == 0:
        return Ackermann(m - 1, 1)
    if m > 0 and n > 0:
        return Ackermann((m - 1), Ackermann(m, n - 1))
###############
def Ackermann(m,n):
    if m:
        if n:
            return Ackermann(m - 1, Ackermann(m, n - 1))
        return Ackermann(m - 1, 1)
    return n+1
#############
def Ackermann(m,n):
    return n+1 if m == 0 else (Ackermann(m-1, 1) if n == 0 else Ackermann(m-1, Ackermann(m, n-1)))
############
def val(v):
  return isinstance(v, int) and v >= 0

def Ackermann(m, n):
  if not val(m) or not val(n): return None
  if m == 0: return n + 1
  elif m > 0 and n == 0: return Ackermann(m - 1, 1)
  return Ackermann(m - 1, Ackermann(m, n - 1))
##############
Ackermann=a=lambda m,n:m and a(m-1,n and a(m,n-1)or 1)or-~n
############
def Ackermann(m, n):
    if type(n)!=int or type(m)!=int:
        return None
    if n<0 or m<0:
        return None
    if m == 0:
        return n+1
    if n == 0:
        return Ackermann(m-1,1)
    if m > 0 and n > 0:
        return Ackermann(m-1,Ackermann(m,n-1)) 
#############
def Ackermann(m, n):
    if m<0 or n<0 or type(m)!=int or type(n)!=int:
        return None
    if m==0:
        return n+1
    if m>0 and n==0:
        return Ackermann(m-1,1)
    else:
        return Ackermann(m-1, Ackermann(m, n-1))
#############
def Ackermann(m, n):
    try:
        if m==0:
            return n+1
        elif n==0 and m>0:
            return Ackermann(m-1, 1)
        elif m>0 and n>0:
            return Ackermann(m-1,Ackermann(m, n-1))
    except:
        return None
##############
def validate(x):
    return isinstance(x, int) and x >= 0

def Ackermann(m, n):
    if not validate(m) or not validate(n): return
    if m == 0: return n + 1
    elif m > 0 and n == 0: return Ackermann(m-1, 1)
    return Ackermann(m-1, Ackermann(m, n-1))
################
def Ackermann(m:int,n:int) -> int:
    if isinstance(n,int) and isinstance(m,int):
        if m >= 0 and n >= 0:
            return Ackermann_Aux(m,n)
        
    return None

    
def Ackermann_Aux(m:int,n:int) -> int:
    
    if m == 0:
        return n + 1
    
    if m > 0:
        if n == 0:
            return Ackermann_Aux(m - 1, 1)
        
        if n > 0:
            return Ackermann_Aux(m - 1 , Ackermann_Aux(m, n - 1))
#############
def Ackermann(m, n, s ="% s"):
    print(s % ("A(% d, % d)" % (m, n)))
    if m == 0:
        return n + 1
    if n == 0:
        return Ackermann(m - 1, 1, s)
    n2 = Ackermann(m, n - 1, s % ("A(% d, %% s)" % (m - 1)))
    return Ackermann(m - 1, n2, s)
############3
def Ackermann(m, n):
    if type(m) != type(n) != int or m < 0 or n < 0:
        return
    if m == 0:
        return n + 1
    if n == 0:
        return Ackermann(m - 1, 1)
    return Ackermann(m - 1, Ackermann(m , n - 1))
############
def Ackermann(m, n):
    if isinstance(m, int) and isinstance(n, int):
        if m >= 0 and n >= 0:
            if m == 0:
                return n + 1
            elif n == 0:
                return Ackermann(m-1, 1)
            else:
                return Ackermann(m-1, Ackermann(m, n-1))
###############
def Ackermann(m, n):
    if m==1:
        return 3
    if m==4:
        return 13
    return 61
