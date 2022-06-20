57aa218e72292d98d500240f


def heron(a, b, c):
    s = (a + b + c) / 2
    return round((s * (s - a) * (s - b) * (s - c)) ** 0.5, 2)
________________________
import math
def heron(a,b,c):
    s=(a+b+c)/2
    return round(math.sqrt(s*(s-a)*(s-b)*(s - c)),2)
________________________
heron=lambda a,b,c:round(((s:=.5*(a+b+c))*(s-a)*(s-b)*(s-c))**.5,2)
________________________
def heron(*sides):
    a, b, c = sides
    s = sum(sides)/2
    return round((s*(s - a)*(s - b)*(s - c))**.5, 2)
________________________
heron=lambda a,b,c:round(((s:=(a+b+c)/2)*(s-a)*(s-b)*(s-c))**.5,2)
________________________
from math import sqrt as sq
def heron(a,b,c):
    s = (a+b+c)/2
    return round(sq(s*(s-a) * (s-b) * (s-c)), 2)
________________________
heron=lambda*args:(lambda a,b,c,s:round((s*(s-a)*(s-b)*(s-c))**.5,2))(*args,sum(args)/2)
________________________
def heron(a,b,c):
    return round((1/4)*(4*b*b*c*c-(b*b+c*c-a*a)**2)**(1/2),2)
________________________
def heron(*args):
    Getter = [x for x in args]
    S = sum(Getter) / 2
    Changer = [S]+[S - x for x in Getter]
    Initializer = Changer[0]
    for x in Changer[1:]:
        Initializer *= x     
    return round(Initializer**(1/2), 2)
________________________
def heron(a,b,c):
    g = (a+b+c)/2
    return round(((g*(g-a)*(g-b)*(g-c))**0.5),2)
________________________
def heron(*n):
    a, b, c = n
    s = (a+b+c) / 2
    return round((s*(s-a)*(s-b)*(s-c))**.5, 2)
________________________
def heron(a, b, c):
    w = (a+b+c)/2
    return round((w * (w-a) * (w-b) * (w-c)) ** 0.5, 2)
