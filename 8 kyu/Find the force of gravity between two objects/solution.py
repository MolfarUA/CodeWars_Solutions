5b609ebc8f47bd595e000627


units = {"kg": 1, "g": 1e-3, "mg": 1e-6, "μg": 1e-9, "lb": 0.453592,
         "m": 1, "cm": 1e-2, "mm": 1e-3, "μm": 1e-6, "ft": 0.3048,
         "G": 6.67e-11}

def solution(v, u):
    m1, m2, r = (v[i] * units[u[i]] for i in range(3))
    return units["G"] * m1 * m2 / r**2
____________________________________
from itertools import starmap

G = 6.67e-11
CONVERSIONS = {'cm': 1e-2, 'mm': 1e-3, 'μm': 1e-6, 'ft': 0.3048,
               'g':  1e-3, 'mg': 1e-6, 'μg': 1e-9, 'lb': 0.453592}

def solution(a,b):
    m1, m2, d = starmap(lambda v,u: v * CONVERSIONS.get(u,1), zip(a,b))
    return G * m1 * m2 / (d*d)
____________________________________
units_map = {
    'm': 1,
    'cm': 0.01,
    'mm': 0.001,
    'μm': 0.000001,
    'ft': 0.3048,
    'kg': 1,
    'g': 0.001,
    'mg': 0.000001,
    'μg': 0.000000001,
    'lb': 0.453592,
}

def solution(arr_val, arr_unit) :
    m1 = arr_val[0] * units_map[arr_unit[0]]
    m2 = arr_val[1] * units_map[arr_unit[1]]
    dst = arr_val[2] * units_map[arr_unit[2]]
    
    return 6.67e-11 * m1 * m2 / (dst * dst)
____________________________________
mass_unit = {"kg":1,"g":0.001,"mg":0.000001,"μg":0.000000001,"lb":0.453592}
distance_unit = {"m":1,"cm":0.01,"mm":0.001,"μm":0.000001,"ft":0.3048}

def solution(arr_val, arr_unit) :
    mass1 = arr_val[0] * mass_unit[arr_unit[0]]
    mass2 = arr_val[1] * mass_unit[arr_unit[1]]
    print(arr_unit)
    return ((6.67 * (10**-11)) * mass1 * mass2)/(arr_val[2] * distance_unit[arr_unit[2]])**2
____________________________________
var = {'g':0.001,'kg':1,'cm':0.01,'m':1,'mg':0.000001,'μg':0.000000001,'lb':0.453592,'mm':0.001,'μm':0.000001,'ft':0.3048}
def solution(arr_val, arr_unit) :
    return  ((6.67*10**-11)*var[arr_unit[0]]*arr_val[0]*var[arr_unit[1]]*arr_val[1])/(var[arr_unit[2]]*arr_val[2])**2
____________________________________
def solution(vals, units) :
    factor_mass = {
        'kg': 1,
        'g': 0.001,
        'mg': 0.000001,
        'μg': 0.000000001,
        'lb': 0.453592,
    }
    factor_dist = {
        'm': 1,
        'cm': 0.01,
        'mm': 0.001,
        'μm': 0.000001,
        'ft': 0.3048
    }
    m0 = vals[0] * factor_mass[units[0]]
    m1 = vals[1] * factor_mass[units[1]]
    d = vals[2] * factor_dist[units[2]]
    g = 6.67e-11
    return g * m0 * m1  / (d * d)
____________________________________
def solution(arr_val, arr_unit) :
    if arr_unit[0]=="g":
        arr_val[0]=arr_val[0]/1000
    if arr_unit[0]=="mg":
        arr_val[0]=arr_val[0]/1000/1000
    if arr_unit[0]=="μg":
        arr_val[0]=arr_val[0]/1000/1000/1000
    if arr_unit[0]=="lb":
        arr_val[0]=arr_val[0]*0.453592
        
    if arr_unit[1]=="g":
        arr_val[1]=arr_val[1]/1000
    if arr_unit[1]=="mg":
        arr_val[1]=arr_val[1]/1000/1000
    if arr_unit[1]=="μg":
        arr_val[1]=arr_val[1]/1000/1000/1000
    if arr_unit[1]=="lb":
        arr_val[1]=arr_val[1]*0.453592
        
    if arr_unit[2]=="cm":
        arr_val[2]=arr_val[2]/100
    if arr_unit[2]=="mm":
        arr_val[2]=arr_val[2]/1000
    if arr_unit[2]=="μm":
        arr_val[2]=arr_val[2]/1000/1000
    if arr_unit[2]=="ft":
        arr_val[2]=arr_val[2]*0.3048
        
    F=6.67* 10**(-11)*(arr_val[0]*arr_val[1]/arr_val[2]**2)
    return F
       
