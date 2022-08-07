54cb771c9b30e8b5250011d4


def height(n, m):
    h, t = 0, 1
    for i in range(1, n + 1): 
        t = t * (m - i + 1) // i
        h += t
    return h
_________________________
def height(n,m):
    if (n == 0 or m == 0):
        return 0
    if (n >= m):
        return 2**m - 1
    
    res = 0
    pascalNum = 1
    for i in range(1, n + 1):
        pascalNum = pascalNum * (m + 1 - i) // i
        res += pascalNum      
            
    return res
_________________________
def height(n, m):
    s, f = -(n > m), 1
    for i in range(min(n, m-n-1)):
        f = f  * (m-i) // (i + 1)
        s += f
    return 2 ** m - s - 2 if m < 2*n else s
_________________________
def height(n, m):
    pp=[1 for i in range(0,n+1)]
    for i in range(1,n+1) : pp[i]=pp[i-1]*(m-i+1)//i
    return sum(pp[1:])
_________________________
def height(n, m):
    x, d = 0, 1
    for i in range(1, n + 1):
        d = d * (m - i + 1) // i
        x += d
    return x
_________________________
def height(n, m): #the answer is c(m ,1) + c(m, 2) + ... + c(m, n).
    combs = [1]
    for i in range(n): combs.append(combs[-1]*(m-i)//(i+1)) #calculating all the combinations needed.
    return sum(combs[1:])
_________________________
def height(n, m): 
    h, k = 0, 1
    for i in range(n):
        k = k * m // (i+1)
        h += k
        m -= 1
    return h
_________________________
def height(n,m):
    result, bink = 0, 1
    for i in range(1, n + 1): 
        bink = bink * m // i 
        result += bink
        m-=1
    return result
_________________________
height=lambda n,m,c=1:sum((c:=c*m//i,m:=m-1)[0]for i in range(1,n+1))
_________________________
def height(n, m):
    res, x = 0, 1
    for j in range(1, n + 1):
        res += (x := x * (m - j + 1) // j)
    return res
