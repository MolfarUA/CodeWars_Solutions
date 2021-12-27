from numpy import*;circleIntersection=lambda a,b,r:(lambda s:int(max(0,r*r*(s-sin(s)))))(2*arccos(hypot(*array(a)-b)/2/r))

________________________________
from math import*;circleIntersection=lambda a,b,r:int(*[r*r*(t-sin(t))for t in[2*acos(min(hypot(a[0]-b[0],a[1]-b[1])/2/r,1))]])

__________________________
from math import*;circleIntersection=lambda a,b,r:(lambda t:(t-sin(t))*r**2//1)(2*acos(min(1,hypot(a[0]-b[0],a[1]-b[1])/r/2)))

__________________________
def circleIntersection(a,b,r,c=complex):import cmath as m;t=2*m.acos(abs(c(*a)-c(*b))/r/2);return(t-m.sin(t)).real*r*r//1

______________________
from numpy import*;c=lambda t:t-sin(t);circleIntersection=lambda a,b,r:int(r*r*c(2*arccos(min(r,hypot(*r_[a]-b)/2)/r)))

_________________________
def circleIntersection(a,b,r):import cmath as m;c=complex;o=2*m.acos(abs(c(*a)-c(*b))/r/2);return int((o-m.sin(o)).real*r*r)

__________________________
def circleIntersection(a,b,r):import math as m;d=m.dist(a,b);f=2*m.acos(d/(2*r)) if d<2*r else 0;return r**2*(f-m.sin(f))//1

_________________________
from math import*;circleIntersection=lambda a,b,r:(lambda d,R:R>d and R*R*acos(d/R)-d*sqrt(R*R-d*d))(dist(a,b),2*r)//2
