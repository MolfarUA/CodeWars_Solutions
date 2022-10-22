565c0fa6e3a7d39dee000125


def dist(v, mu):                        # suppose reaction time is 1
    v /= 3.6
    return v + v * v / (2 * mu * 9.81)

def speed(d, mu):                       # suppose reaction time is 1
    b = -2 * mu * 9.81
    return round(3.6 * (b + (b*b - 4*b*d)**0.5 ) / 2, 2)
_____________________________
from math import sqrt

G = 9.81

def dist(v, mu):
    return v*(1 + v/3.6/2/mu/G)/3.6
    
def speed(d, mu):
    return (sqrt(1 + 2*d/mu/G) - 1)*mu*G*3.6
_____________________________
from math import sqrt

g = 9.81  # the gravity of Earth in [m/s^2]
tr = 1  # suppose reaction time in [s]
kmh2ms = 10 / 36  # [km/h] -> [m/s]
ms2kmh = 3.6  # [m/s] -> [km/h]

def dist(v, mu):
    mug2 = 2 * mu * g
    vms = kmh2ms * v
    return vms * (vms / mug2 + tr)

def speed(d, mu):
    mug = mu * g
    vms = (sqrt(tr ** 2 + 2 * d / mug) - tr) * mug
    return ms2kmh * vms
_____________________________
def dist(v, mu):                        # suppose reaction time is 1
    #total distance = stopping + braking
    vs = v / 3.6 #convert velocity to m/s from km/hr
    braking = (vs*vs)/(2*mu*9.81) #use provided formula
    reaction = 1 * vs
    return braking + reaction

def speed(d, mu):                       # suppose reaction time is 1
    # d = d1 + d2 base distance formula
    # d = v**2/2*mu*9.81 + (1*v)          expanded formula
    # 0 = v**2/2*mu*9.81 + (1*v) - d      made into quadratic equation
    a = 1/(2*mu*9.81) #quadratic variable a
    b = 1 #quadratic variable b
    c = -d #quadratic variable c
    v = ((-1*b) + (b**2 - (4*a*c))**0.5)/(2*a)  #quadratic formula to solve for velocity
    v = v*3.6 #convert to km/hr from m/s
    return v
_____________________________
import math as m 
def dist(v, mu):                        # suppose reaction time is 1
    g = 9.81
    v = (v*10)/36
    return (v*v) / (2*mu*g) + v

def speed(d, mu):                       # suppose reaction time is 1
    g = 9.81
    k = 2*mu*g
    delt = m.sqrt(k*k + 4*k*d)
    return (-k + delt)*36/20
_____________________________
import math
def dist(v, mu):
    num=(v/3.6)**2
    den=2*mu*9.81
    result=(num/den)+v/3.6
    return result

def speed(d, mu):
    v=3.27*(((math.sqrt(mu)*math.sqrt((200*d)+(981*mu)))/math.sqrt(109))-3*mu)
    return v*3.6
_____________________________
import math

def dist(v, mu):
    v = (v * 1000) / 3600
    return v*v / (2*mu*9.81) + v

def speed(d, mu):
    c = 2*mu*9.81
    d1 = (-c + math.sqrt(c*c + 4*c*d)) / 2
    d2 = (-c + math.sqrt(c*c + 4*c*d)) / 2
    return (max(d1, d2) * 3600) / 1000
_____________________________
def dist(v, mu):                        # suppose reaction time is 1
    g = 9.81
    v = v*1000/3600
    d1 = (v**2)/(2*mu*g) + v
    return d1

def speed(d, mu):                       # suppose reaction time is 1
    g = 9.81
    a = 1/(2*mu*g)
    D = 1 -4*a*(-d)
    x1 = (-1 - D**0.5)/(2*a)
    x2 = (-1 + D**0.5)/(2*a)
    if x1 >=0:
        return (x1*3600/1000)
    else:
        return (x2*3600/1000)
_____________________________
g = 9.81

def dist(v, mu):                        # suppose reaction time is 1
    # your code
    v_m = v / 3.6
    return v_m + v_m ** 2/ (2 * g * mu)

def speed(d, mu):                       # suppose reaction time is 1
    # your code
    b = 2 * g * mu
    c = -2 * d * g * mu
    D = (b ** 2 - 4 * c) ** 0.5
    return (-1 * b + D) / 2 * 3.6
