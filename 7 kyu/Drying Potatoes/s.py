def potatoes(p0, w0, p1):
    diff = w0*(p0*.01)-w0*(p1*.01)
    weight_diff = w0-(w0*(p1*.01))

    return int(w0*(1-(diff/weight_diff))+.01)
_______________________________________________
def potatoes(p0, w0, p1):
    return w0 * (100 - p0) // (100 - p1)
_______________________________________________
def potatoes(p0, w0, p1):
    """
    Let:
        w1 - potatoes weight after drying,
        d - dry matter weight
    Let's count the weights:
    a) before drying:
        (p0 / 100) * w0 + d = w0 =>
        d = w0 * (1 - p0 / 100)
    b) after drying:
        (p1 / 100) * w1 + d = w1, and when we put d in this equation:
        (p1 / 100) * w1 + w0 * (1 - p0 / 100) = w1 =>
        w1 = w0 * (1 - p0 / 100) / (1 - p1 / 100) * (100 / 100) =>
        w1 = w0 * (100 - p0) / (100 - p1)
    """
    return w0 * (100 - p0) // (100 - p1)
_______________________________________________
def potatoes(p0, w0, p1):
    return int(w0 * (100 - p0) / (100 - p1))
_______________________________________________
def potatoes(p0, w0, p1):
    '''
    input: p0 (initial percent of water), int 
           w0 (initial weight), int
           p1 (final percent of water), int
    output: final weight, int
    '''
    return int((100 - p0) * w0 / (100 - p1))
_______________________________________________
from math import floor,ceil
from fractions import Fraction
def potatoes(p0, w0, p1):
    t=Fraction(w0/100*(100-p0))
    print('{} {}'.format(t,t/((100-p1)/100)))
    return floor(Fraction(t/((100-p1)/100)))
_______________________________________________
def potatoes(p0, w0, p1):
    weight = (100-p0)/100*w0
    return int(100*weight/(100-p1))
_______________________________________________
def potatoes(initialWaterPercent, initialWeight, finalWaterPercent):
    return int(initialWeight * (100 - initialWaterPercent) / (100 - finalWaterPercent))
_______________________________________________
import math
def potatoes(p0, w0, p1):
    
    multiplicador = 100 - p0
    divisor = 100 -p1
    calculo = w0 * multiplicador / divisor
    
    pesoFinal = math.trunc(calculo)
    
    return pesoFinal
_______________________________________________
import math
def potatoes(p0, w0, p1):
    pesoFinal = math.trunc(w0 * (100 - p0) / (100 - p1))
    return pesoFinal
_______________________________________________
def potatoes(p0, w0, p1):
    print(f'p0 = {p0}, p1 = {p1}, w0 = {w0}')
    # pw[kg] = dry potato weight (constant)
    dpw = (100-p0)*w0/100
    
    # total potato weight after drying
    tpw = dpw * 100/(100-p1)
    print(f'dpw = {round(dpw,5)}; tpw = {round(tpw,5)}')
    return int(tpw)
_______________________________________________
def potatoes(p0, w0, p1):
    solidin=(100-p0)*w0/(100)
    finalW=100*solidin/(100-p1)
    return int(finalW)
