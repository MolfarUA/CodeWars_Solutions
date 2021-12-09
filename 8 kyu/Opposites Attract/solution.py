def lovefunc( flower1, flower2 ):
    return (flower1+flower2)%2
###########
def lovefunc(flower1, flower2):
    return flower1 % 2 != flower2 % 2
##########
lovefunc=lambda a,b:(a+b)%2
#########
def lovefunc(f1, f2):
    return True if (f1 % 2 == 0 and f2 % 2 != 0) or (f2 % 2 == 0 and f1 % 2 != 0) else False
##########
def lovefunc(a, b):
    if a % 2 == 0 and b % 2 == 0:
        return False
    elif a % 2 != 0 and b % 2 == 0:
        return True
    elif a % 2 == 0 and b % 2 != 0:
        return True
    else:
        return False
