def sum_str(a, b):
    if a == "" and b != "":
        return f'{b}'
    if a != "" and b == "":
        return f'{a}'
    if a == "" and b == "":
        return f'0'
    return f'{int(a) + int(b)}'
#############
def sum_str(a, b):
    return str(int(a or 0) + int(b or 0))
##############
def sum_str(a, b):
    return str(int('0' + a) + int('0' + b))
##############
def sum_str(a, b):
    print(a, b)
    if a == "" or a == None: a = "0"
    if b == "" or b == None: b = "0"
    return str(int(a)+int(b))
################
def sum_str(*values):
    return str(sum(int(s or '0') for s in values))
###############
def sum_str(a, b):
    if a == '': a = '0'
    if b == '': b = '0'
    return str(int(a) + int(b))
###############
def sum_str(a, b):
    return str(int(a) + int(b)) if a and b else a or b or '0'
###########
def sum_str(a, b):
    # happy coding !
    if a =='' and b=='':return'0'
    if b =='':return a
    if a =='':return b
    if a =='' and b=='':return'0'
    return str(int(a)+int(b))
    pass
################
def sum_str(a, b):
    return '%d' % (int(a if a else 0) + int(b if b else 0))
###################
def sum_str(a,b):
    if (a == "" and b == ""):
        return "0"
    if (a == ""):
        return b;
    if (b == ""):
        return a;    
    return str(int(a) + int(b))
#############
sum_str = lambda a,b: str(eval(a or '0')+eval(b or '0'))
############
def sum_str(*args):
    return str(sum(map(lambda x: int(x) if x else 0, args)))
###############
sum_str=lambda *x:str(sum(int('0'+e)for e in x))
##########
def sum_str(a, b):
    try:
        return str(int(a) + int(b))
    except ValueError:
        return '0' if a + b == '' else a + b
##############
sum_str=lambda *x:str(sum(int('0'+e)for e in x))
