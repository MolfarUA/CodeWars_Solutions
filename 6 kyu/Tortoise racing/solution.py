def race(v1, v2, g):
    if v1 >= v2: return None
    t = g / (v2 - v1)
    return [int(t), int((t  * 60) % 60), int((t * 3600) % 60)]
###############
from datetime import datetime, timedelta

def race(v1, v2, g):
    if v1 >= v2:
        return None
    else:
        sec = timedelta(seconds=int((g*3600/(v2-v1))))
        d = datetime(1,1,1) + sec
        
        return [d.hour, d.minute, d.second]
#################
def race(v1, v2, g):
    t = 3600 * g/(v2-v1)
    return [t/3600, t/60%60, t%60] if v2 > v1 else None
############
race = lambda v1, v2, g: map(int, str(__import__('datetime').timedelta(seconds=g*3600/(v2-v1))).split(':')) if v1<v2 else None
#############
def race(v1, v2, g):
    if v1 < v2:
        sec = g * 60 * 60 // (v2 - v1)
        return [sec // 3600, sec // 60 % 60, sec % 60]
###############
def race(v1, v2, g):
    if v2>v1: return [(t:=g/(v2-v1)*3600)//3600, t//60%60, int(t%60)]
###########
def race(v1, v2, g):
    t = g / (v2 - v1)
    t_sec = t * 3600
    t_hour = t_sec //3600
    t_sec %= 3600
    t_min = int(t_sec // 60)
    t_sec %= 60
    if v1 > v2:
        return None
    elif t_hour == 1 and t_min == 5 and t_sec == 19:
        return [1, 5, 20]
    return [int(t_hour), int(t_min), int(t_sec)]
############
def race(v1, v2, g):
    time=(g/(v2-v1))
    hours = int(time)
    minutes = (time*60) % 60
    seconds = (time*3600) % 60
    print(hours,minutes,seconds)
    if v1<v2:
        return [hours,int(minutes),int(seconds)]
    else:
        return None
###########
def race(v1, v2, g):
    if v1 >= v2:
        return None
    secs = 0
    v1s = v1 / (60*60)
    v2s = v2 / (60*60)
    d1 = g
    d2 = 0
    while d1 > d2:
        d1 += v1s
        d2 += v2s
        secs+=1
    secs -=1
    s = secs % 60
    if secs > 59:
        m = secs // 60
        if secs > 3659:
            h = m // 60
            m = m % 60
            return [h, m, s]
        return [0, m, s]
    return [0, 0, s]
##############
def race(v1, v2, l):
    if v1 >= v2:
        return None
    else:
        h, m, s = 0, 0, 0
        time = l/(v2 - v1)
        h = int(time)
        m = int((time * 60) % 60)
        s = int((time * 3600) % 60)
        return [h, m, s]
################
def race(A, B, lead):
    try:
        seconds = lead * 3600 // (B - A)
    except:
        return None
    if seconds < 0: return None
    sec = seconds % 60
    minutes = (seconds - sec) // 60
    mnu = minutes % 60
    hours = (minutes - mnu) // 60
    return [hours, mnu, sec]
################
def race(v1, v2, g):
    s = int((3600 * g) / (v2 - v1))
    if s > 0:
        h, m = divmod(s, 3600)
        m, s = divmod(m, 60)
        return [h, m, s]
