from math import pi

def iter_pi(epsilon):
    n = 1
    approx = 4
    while abs(approx - pi) > epsilon:
        n += 1
        approx += (-4, 4)[n % 2] / (n * 2 - 1.0)
    return [n, round(approx, 10)]
________________________________________
from math import pi

def iter_pi(epsilon):
    pi_4 = 0
    k = 0
    while abs(pi_4 * 4 - pi) > epsilon:
        pi_4 += (-1) ** k / (k * 2 + 1)
        k += 1
    return [k, round(pi_4 * 4, 10)]
________________________________________
import itertools
from math import pi

def iter_pi(epsilon):
    sign = 1
    value = 4
    n = 1
    for i in itertools.count(1):
        if abs(value - pi) < epsilon:
            return [i, round(value, 10)]
        sign = -sign
        n += 2
        value += sign * (4 / n)
________________________________________
from math import pi

def iter_pi(epsilon):
    my_pi = 0
    n = sign = 1
    
    while epsilon < abs(pi - my_pi):
        my_pi += 4.0 / n * sign
        n += 2
        sign *= -1
    
    return [n//2, round(my_pi, 10)]
________________________________________
import math
def iter_pi(epsilon):
  pi, iD, c, pos = 4.0, 1.0, 1, False
  while abs(pi - math.pi) > epsilon:
    iD += 2.0
    pi, pos = 4 * (pi / 4 + (1 / iD if pos else -1 / iD)), not pos
    c += 1
  return [c, round(pi, 10)]
________________________________________
from math import pi
def iter_pi(epsilon):
    sum, n = 0, 0
    while abs(4*sum - pi)> epsilon:
        sum += ((-1)**n)/(2*n+1)
        n += 1
    return [n, round(4*sum, 10)]
________________________________________
from math import pi

def iter_pi(epsilon):
    res = 0
    i = 0
    while abs(pi-res) > epsilon: 
        res += (-1)**(i%2) * 4 / (1 + (2*i))
        i += 1
    return [i, round(res, 10)]
________________________________________
import math
def iter_pi(epsilon):
    pi,k = 0,0
    while abs(pi-math.pi/4) > epsilon/4:
        pi += (-1)**k * 1/(2*k + 1)
        k += 1
    pi *=4

    return [k , round(pi, 10)]
________________________________________
from math import pi


def iter_pi(epsilon):
    iterations = 1
    estimated_pi = 1
    sign = -1
    i = 3
    while abs(pi - 4 * estimated_pi) >= epsilon:
        estimated_pi += sign / i
        sign = -~~sign
        i += 2
        iterations += 1
    return [iterations, round(4 * estimated_pi, 10)]
________________________________________
from math import pi

def iter_pi(epsilon: float) -> list:
    approx = summation = i = 0
    while abs(approx - pi) >= epsilon:
        summation += (-1) ** i / (2 * i + 1)
        approx = 4 * summation
        i += 1
    return [i, round(approx, 10)]
________________________________________
import math

def iter_pi(epsilon):
    iter = 1
    factor = -1
    denom = 3
    pi = 4
    while (abs(math.pi - pi) > epsilon):
        iter += 1
        pi = pi + (4*(factor*(1/denom)))
        denom += 2
        factor *= -1
    return [iter, round(pi, 10)]
________________________________________
from math import pi,pow
def iter_pi(epsilon):
    i=0
    leibniz_i=1
    while(abs(4*leibniz_i - pi) >epsilon):
        i+=1
        leibniz_i+=pow((-1),(i))*1/(2*i+1)
    return [i+1,round(leibniz_i*4,10)]
________________________________________
import math

def iter_pi(epsilon):
    my_pi = i = 0
    while abs(my_pi - math.pi) > epsilon:
        my_pi += 4 * math.pow(-1, i) / (2 * i + 1)
        i += 1
    return [i, round(my_pi, 10)]
