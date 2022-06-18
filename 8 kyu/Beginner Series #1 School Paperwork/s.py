55f9b48403f6b87a7c0000bd


def paperwork(n, m):
    return max(n, 0)*max(m, 0)
__________________________
def paperwork(n, m):
    return n*m if n>=0 and m>=0 else 0
__________________________
def paperwork(n, m):
    if m > 0 and n > 0:
        return m*n
    else:
        return 0
__________________________
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
__________________________
def paperwork(n, m):
    
    while n > 0 and m > 0:
        sum = n * m
        return sum
    return 0
__________________________
def paperwork(n, m):
    
    amountpages = (n*m)
    
    if n <= 0:
        return(0)
    if m <= 0:
        return(0)

    else:
        return(amountpages)
__________________________
def paperwork(n, m):
    if n > 0 and m > 0:
        work=n*m
        return work
    else:
        return 0
__________________________
paperwork = lambda n,m: 0 if m < 0 else 0 if n < 0 else n*m
__________________________
def paperwork(n, m):
    return n * m if n > 0 and m > 0* m else 0
