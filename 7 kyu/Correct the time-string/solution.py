57873ab5e55533a2890000c7


def time_correct(t):
    if not t: return t
    try:
        h, m, s = map(int, t.split(':'))
        if s >= 60: s -= 60; m += 1
        if m >= 60: m -= 60; h += 1
        return '%02d:%02d:%02d' % (h % 24, m, s)
    except: pass
_________________________________
import re


def time_correct(t):
    if not t:
        return t
    
    if not re.match("\d\d:\d\d:\d\d$", t):
        return None
        
    hours, minutes, seconds = [int(x) for x in t.split(':')]
    
    if seconds >= 60:
        minutes += 1
        seconds -= 60
    if minutes >= 60:
        hours += 1
        minutes -= 60
    if hours >= 24:
        hours = hours % 24
    
    return "{0:0>2}:{1:0>2}:{2:0>2}".format(hours, minutes, seconds)
_________________________________
import re


def time_correct(t):
    if t:
        if bool(re.fullmatch(r'^\d\d:\d\d:\d\d$', t)):
            hh, mm, ss = map(int, t.split(':'))
            redundant_mm, correct_ss = divmod(ss, 60)
            redundant_hh, correct_mm = divmod(mm + redundant_mm, 60)
            redundant_dd, correct_hh = divmod(hh + redundant_hh, 24)
            return f"{correct_hh:02d}:{correct_mm:02d}:{correct_ss:02d}"
        return None
    return t
_________________________________
    try:
        if t=="":
            return ""
        if len(t)!=8:
            return None
        h,m,s=[int(x) for x in t.split(":")]
        if s>=60:
            s-=60
            m+=1
        if m>=60:
            m-=60
            h+=1
        if h>=24:
            h=h%24
        return '%02d:%02d:%02d'%(h,m,s)
    except:
        return None
_________________________________
def time_correct(t):
    if not t: return t
    try:
        if len(t)!=8:
            return None

        t = [int(x) for x in t.split(':')]
        for i in reversed(range(1,len(t))):
            t[i-1]+=t[i]//60
            t[i]=t[i]%60

            print(t[i])
        t[0] %= 24
        for i in range(len(t)):
            if t[i]<10:
                t[i]='0'+str(t[i])
            else:
                t[i]=str(t[i])
            print(t[i])
        return ':'.join(t)
    except: pass
    return None
_________________________________
def time_correct(t):
    if t == '' or t == None:
        return t
    if t[2] != ':' or t[5] != ':':
        return None
    for i in t:
        if i in list(map(chr, range(97, 123))) or i in ['/']:
            return None
    time = {}
    time['hour'] = int(t[:2])
    time['min'] = int(t[3:5])
    time['sec'] = int(t[6:])
    while True:
        if time['sec'] >= 60:
            time['sec'] = time['sec'] - 60
            time['min'] = time['min'] + 1
        if time['min'] >= 60:
            time['min'] = time['min'] - 60
            time['hour'] = time['hour'] + 1
        if time['hour'] >= 24:
            time['hour'] = time['hour'] - 24
        else:
            break
    if len(str(time['sec'])) == 1:
        time['sec'] = '0' + str(time['sec'])
    if len(str(time['min'])) == 1:
        time['min'] = '0' + str(time['min'])
    if len(str(time['hour'])) == 1:
        time['hour'] = '0' + str(time['hour'])
    return str(time['hour']) + ':' + str(time['min']) + ':' + str(time['sec']) 
_________________________________
def time_correct(t):
    digits=["0","1","2","3","4","5","6","7","8","9"]
    if t==None or t=="":
        return t
    if not (isinstance(t,str) and len(t)==8 and t[2]==":" and t[5]==":" and t[0] in digits and t[1] in digits and t[3] in digits and t[4] in digits and t[6] in digits and t[7] in digits):
        return None
    else:
        first=int("".join([t[0],t[1]]))
        second=int("".join([t[3],t[4]]))
        third=int("".join([t[6],t[7]]))
        second+=(third-third%60)//60
        third=third%60
        first+=(second-second%60)//60
        second=second%60
        first=first%24
        return ":".join([add_zero(first),add_zero(second),add_zero(third)])

            
def add_zero(x):
    if x>9:
        return str(x)
    else:
        return "0"+str(x)
