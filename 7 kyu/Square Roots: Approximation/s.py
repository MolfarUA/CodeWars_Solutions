58475cce273e5560f40000fa



def approx_root(n):
    base = int(n**0.5)
    return round( base + (n - base**2) / ((base + 1)**2 - base**2) , 2)
____________________________
def approx_root(n):
    m = n**0.5
    a, b = [int(x) for x in [m, m + 1]]
    c = a**2
    return round(a + ((n - c) / (b**2 - c)), 2)
____________________________
def approx_root(n):
    b = int(n ** 0.5)
    diff_gn = n - b**2
    diff_lg = (b+1)**2 - b**2
    return round(b + (diff_gn / diff_lg), 2)
____________________________
def approx_root(n):
    import math
    s = int(math.sqrt(n))
    diff_gn = n - s ** 2
    diff_lg = (s + 1) ** 2 - s ** 2
    return round(s + diff_gn / diff_lg, 2)
____________________________
approx_root=lambda n:round((c:=n-(a:=(b:=int(n**.5))**2))/((b+1)**2-a)+b,2)
____________________________
approx_root=r=lambda n,i=0:n>(i+1)**2and r(n,i+1)or round(i+(n-i*i)/(2*i+1),2)
____________________________
approx_root=lambda n:round(next(i+(n-i*i)/(2*i+1)for i in range(n)if(i+1)**2>=n),2)
____________________________
def approx_root(n):
    s = n
    base = 0
    i = 1
    while i < 1000:
        s = i*i - n
        if s < 0:
            s = n
        else:
            base = (i - 1)
            gn = n - base**2
            lg = (i * i) - base**2
            break
        i += 1
    return(round(base + (gn/lg), 2))
____________________________
def approx_root(n):
    global result
    smallest = int(n ** 0.5 + 1)
    greatest = int(n ** 0.5)
    if n ** 0.5 == greatest:
        result = int(n ** 0.5)
    else:
        result = round(greatest + (n - greatest ** 2) / (smallest ** 2 - greatest ** 2), 2)
    return result
____________________________
def approx_root(n):
    if (n ** .5) == int(n ** .5):
        return n ** .5
    
    base = int(n ** .5)
    sup = (base + 1) ** 2

    diff_gn = n - (base ** 2)
    diff_lg = sup - (base ** 2)
    
    return round(base + (diff_gn / diff_lg), 2)
