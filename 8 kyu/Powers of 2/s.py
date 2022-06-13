def powers_of_two(n):
    return [2 ** x for x in range(n + 1)]
___________________________________
def powers_of_two(n):
    return [1<<x for x in range(n + 1)]
___________________________________
def powers_of_two(n):
    a = []
    for i in range(0, n + 1):
        a.append(2 ** i)    
    return a
___________________________________
def powers_of_two(n): return [ 2 ** i for i in range(n+1) ]
___________________________________
def powers_of_two(n):
    power_of_two = []
    for i in range(n+1):
        power_of_two.append(2 ** i)
    return power_of_two
___________________________________
def powers_of_two(n):
    list = []
    if(n == 0):
        return [1]
    for i in range(n):
        list.append(2**n)
        n = n-1
    list.append(1)
    list.reverse()
    
    return list
___________________________________
def powers_of_two(n):
    list = []
    while n >= 0:
        list.append(2**n)
        n-=1
    return list[::-1]
___________________________________
def powers_of_two(n):
    x = [1]
    y = 1
    while n > 0:
        x.append(2*y)
        y *= 2
        n -= 1
    return x
___________________________________
def powers_of_two(n):
    result = []
    range_2_n = range(0, n + 1)
    for i in range_2_n:
        result.append(2 ** i)
    return result
