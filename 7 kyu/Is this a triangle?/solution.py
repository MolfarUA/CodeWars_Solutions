from itertools import permutations

def is_triangle(a, b, c):
    for x, y, z in permutations ([a, b, c]):
        if x >= y + z:
            return False
    return True
##############
def is_triangle(a, b, c):
    return (a<b+c) and (b<a+c) and (c<a+b)
##############
def is_triangle(a, b, c):
    a, b, c = sorted([a, b, c])
    return a + b > c
############
def is_triangle(a, b, c):
    if (a or b or c)<0:
        return False

    lst=[a,b,c]
    m=max(lst)
    lst.remove(m)
    other=lst[1]+lst[0]
    if m >= other:
        return False
    else:
        return True

    return False
############
def is_triangle(a, b, c):
    for i in a,b,c:
        if i < 0:
            return False
            
    if (a+b-c) * (a+c-b) * (b+c-a) > 0:
         return True
    else:
        return False
############
def is_triangle(a, b, c):
    t1 = a + b > c
    t2 = b + c > a
    t3 = a + c > b
    return t1 and t2 and t3
###########
def is_triangle(a, b, c):
    return a>0 and b>0 and c>0 and (a-b)<c and (b-c)<a and (c-a)<b
###########
def is_triangle(a, b, c) -> bool:
    return False if a <= 0 or b <= 0 or c <= 0 or a+b <= c or a+c <= b or c+b <= a else True

if is_triangle(3,4,5):
    print('Correcto')
############
def is_triangle(a, b, c):
    return True if a > b - c and a > c - b and a < b + c else False
###########
def is_triangle(a, b, c):
    return True if (abs(a-b)<c<a+b and abs(b-c)<a<b+c and abs(a-c)<b<a+c) else False
############
def is_triangle(a, b, c):
    t = [a,b,c]
    if 2*max(t) < sum(t):
        return True
    return False
#############
def is_triangle(a, b, c):
    if a == 0 or b == 0 or c == 0:
        
        return False
    lista = [a, b, c]
    lista.sort()
    if (int(lista[0]) + int(lista[1])) > int(lista[2]):
        return True
    else:
        return False
