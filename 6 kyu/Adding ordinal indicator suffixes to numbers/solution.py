def number_to_ordinal(n):
    string = str(n)
    if n == 0:
        return "0"
    if string[-1] == "1" and (n == 1 or string[-2] != "1"):
        return string + "st"
    if string[-1] == "2" and (n == 1 or string[-2] != "1"):
        return string + "nd"
    if string[-1] == "3" and (n == 1 or string[-2] != "1"):
        return string + "rd"
    return string + "th"
##################
def numberToOrdinal(n):
  return '0' if n==0 else str(n) + ('th' if 10 <= n % 100 < 20 else {1:'st', 2:'nd', 3:'rd'}.get(n%10, 'th'))
#############
def numberToOrdinal(n):
    if not (11 <= n % 100 <= 13):
        if n % 10 == 1:
            return f'{n}st'
        elif n % 10 == 2:
            return f'{n}nd'
        elif n % 10 == 3:
            return f'{n}rd'
    return f'{n}th' if n else '0'
##############
SUFFIX = {'1': 'st', '2': 'nd', '3': 'rd'}


def number_to_ordinal(n):
    if n > 0:
        str_n = str(n)
        a, b = list(('0' + str_n[-2:])[-2:])
        if a != '1':
            return str_n + SUFFIX.get(b, 'th')
        return str_n + 'th'
    return '0'
###########
def number_to_ordinal(n):
    strumber = str(n)
    if n == 0:
        return strumber
    if len(strumber) > 1:
        if strumber[-2] == "1":
            return strumber + "th"
    if strumber[-1] == "1":
        return strumber + "st"
    if strumber[-1] == "2":
        return strumber + "nd"
    if strumber[-1] == "3":
        return strumber + "rd"
    return strumber + "th"
#################
def number_to_ordinal(n):
    n = int(n)
    if n == 0:
        return str(n);
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix
###############
from re import search as s

def number_to_ordinal(n):
    if not n: return "0"
    st = str(n)
    if s(r'(1\d|[04-9])$', st): return st + 'th'
    if s(r'1$', st): return st + 'st'
    if s(r'2$', st): return st + 'nd'
    if s(r'3$', st): return st + 'rd'
###############
def number_to_ordinal(n):
    units = n % 10 # 1
    teens = n % 100 # 1
    
    if (units == 1) and (teens != 11):
        return str(n) + 'st'
    elif (units == 2) and (teens != 12):
        return str(n) + 'nd'
    elif (units == 3) and (teens != 13):
        return str(n) + 'rd'
    elif n == 0:
        return str(n)
    else:
        return str(n) + 'th'
###################
def number_to_ordinal(n):
    if n==0: return '0'
    c=str(n)
    if len(c)>1:
        if c[-2:]=='11' or c[-2:]=='12' or c[-2:]=='13': return c+'th'
    if c[-1]=='1': return c+'st'
    if c[-1]=='2': return c+'nd'
    if c[-1]=='3': return c+'rd'
    return c+'th'
################
def number_to_ordinal(n):
    if n <= 0:
        return f"{n}"
    
    if 11 <= (n % 100) <= 13:
        return f"{n}th"

    remainder = n
    while remainder > 9:
        remainder %= 10

    suffix = {1: "st", 2: "nd", 3: "rd"}.get(remainder, "th")

    return f"{n}{suffix}"
####################
def number_to_ordinal(n):
    if n == 0:
        return '0'
    n1={0:'th',1:'st',2:'nd',3:'rd',4:'th',5:'th',6:'th',7:'th',8:'th',9:'th',10:'1h',11:'th',12:'th',13:'th'}
    tail = int(str(n)[-2::])
    tail = int(str(n)[-1::]) if tail not in [11,12,13] else tail
    
    return str(n)+n1[int(tail)]  
##################
def number_to_ordinal(n):
    if n == 0:
        return '0'
    if n % 100 in [11,12,13]:
        return str(n) + 'th'
    if n % 10 == 1:
        return str(n) + 'st'
    if n % 10 == 2:
        return str(n) + 'nd'
    if n % 10 == 3:
        return str(n) + 'rd'
    return str(n) + 'th'
###################
def number_to_ordinal(n):
    return "0" if(n == 0) else str(n) + "th" if(n%100 == 11 or n%100 == 12 or n%100 == 13) else str(n)+"st" if(n%10 == 1) else(str(n)+"nd" if(n%10 == 2) else(str(n) + "rd" if(n%10 == 3) else str(n) + "th"))
