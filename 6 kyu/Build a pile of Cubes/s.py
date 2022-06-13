def find_nb(m):
    total = 0
    i = 0
    while (total < m):
        i += 1
        total += (i ** 3)

    return i if total == m else -1
_________________________________________
def find_nb(m):
    i,sum = 1,1
    while sum < m:
        i+=1
        sum+=i**3
    return i if m==sum else -1
_________________________________________
def find_nb(m):
    '''
    n cube sum m = (n*(n+1)//2)**2
    then n**2 < 2*m**0.5 < (n+1)**2
    and we can proof that for any n, 0.5 > (2*m**0.5)**0.5 - n**2 > 2**0.5 - 1 > 0.4
    '''
    n = int((2*m**0.5)**0.5)
    if (n*(n+1)//2)**2 != m: return -1
    return n
_________________________________________
def find_nb(m):
    n = 0
    while (m > 0):
        n += 1
        m -= n**3
    return n if m == 0 else -1
_________________________________________
def find_nb(m):
    i = 1
    while m > 0:
        m = m - i**3
        i += 1
    if m != 0:
        i = 0
    return i-1
_________________________________________
def find_nb(m):
    summ = 0
    n = 1
    while summ < m:
        summ += n ** 3
        n += 1
    if summ == m:
        return n - 1
    return -1
_________________________________________
def find_nb(n):
    x = 1
    count = 0

    while n > 0:
        n -= x**3
        x += 1
        count += 1

    if n < 0:
        return -1
    else:
        return count
