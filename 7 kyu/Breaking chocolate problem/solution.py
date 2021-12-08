def break_chocolate(n, m):
    count = 0
    s = n * m
    if  s > 1:
        s = s - 1
        count = s
    elif s < 1:
        coun = 0
    return count
############
def breakChocolate(n, m):
    return max(n*m-1,0)
############
def breakChocolate(n, m):
    try:
        int(n)
        int(m)
    except ValueError:
        return 0
    
    if (n > 0) and (m > 0):
        return (n*m)-1
    else:
        return 0
###############
def breakChocolate(n, m):
    return 0 if n*m==0 else n*m-1
#############
def break_chocolate(n, m):
    if n * m == 0:
        return 0
    return (n * m) - 1

print(break_chocolate(5, 5))
print(break_chocolate(1, 1))
###############
def break_chocolate(n, m):
    if n*m-1 >= 0:
        return n*m-1
    else:
        return n*m
################
def break_chocolate(n, m):
    if n == 0 or m == 0:
        return(0)
    elif n < 0 or m < 0:
        return(0)
    else:
        return((n*m)-1)
    return 0
#################
def break_chocolate(n, m):
    num = 0
    if n != 0 and m != 0:
        num = (n * m)-1 
    return num
################
def break_chocolate(n, m):
    if min(n,m) <= 0:
        return 0
    n, m = sorted((n, m))
    return n-1 + n*(m-1)
