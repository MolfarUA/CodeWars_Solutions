55fab1ffda3e2e44f00000c6


def cockroach_speed(s):
    return s // 0.036
__________________________
def cockroach_speed(s):
    cm_per_km = 100000
    sec_per_hour = 3600
    return int(s * cm_per_km / sec_per_hour)
__________________________
import math
def cockroach_speed(s):
    return math.floor(s * 27.778)
__________________________
ONE_KM_IN_METERS = 1000
ONE_METER_IN_CM = 100
ONE_HOUR_IN_MINUTES = 60
ONE_MINUTE_IN_SECONDS = 60

def cockroach_speed(s):
    cm = ONE_KM_IN_METERS * ONE_METER_IN_CM
    sec = ONE_HOUR_IN_MINUTES * ONE_MINUTE_IN_SECONDS
    return int((s * cm) / sec)
__________________________
def cockroach_speed(s):
    return (s * 100000) // (60 * 60) 
__________________________
import math
def cockroach_speed(s):
    return math.floor(s*100000/3600)
__________________________
def cockroach_speed(s):
    return int(s * (30/1.08))
__________________________
def cockroach_speed(s):
    return s*27.7804//1
__________________________
def cockroach_speed(kph):
    # 1000 m in km
    mph = kph * 1000
    # 100 cm in m
    cph = mph * 100
    # 60 min in hour
    cpm = cph / 60
    # 60 sec in min
    cps = cpm / 60
    return int(cps)
__________________________
import math
def cockroach_speed(s):
    return (math.floor(s*27.7778))
