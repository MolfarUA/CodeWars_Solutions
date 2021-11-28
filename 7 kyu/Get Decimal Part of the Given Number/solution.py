import math
def get_decimal(n):
    return abs(math.modf(n)[0])

print(get_decimal(10))
print(get_decimal(-1.2))
print(get_decimal(1.99))
##############
def get_decimal(n): 
    return abs(n) % 1
###############
def get_decimal(n): 
    n = abs(n)
    return n - int(n)
##############
def get_decimal(n): return abs(n - int(str(n).split('.')[0]))
#############
def get_decimal(n): 
    
    return abs(int(n)-n)
############
def get_decimal(n): 
    return float(f".{str(n).split('.')[1]}") if type(n) == float else 0
############
def get_decimal(n): 
    return abs(n)%(abs(n)//int(abs(n)))
#################
def get_decimal(n): 
    import math
    m = math.modf(n)
    if m[0] >= 0:
        return m[0]
    else:
        return -m[0]
##############
def get_decimal(n): 
    return abs(n%int(n))
############
#def get_decimal(n): 
    #if n < 0:
        #return (n*-1)%1
   # else:
       # return n%1
    #return (n*-1)%1 if n<0 else n%1
get_decimal = lambda n: (n*-1)%1 if n<0 else n%1
##################
import re

def get_decimal(n): 
    return float(re.sub(r'.*(\..*)', r'0\1', str(n))) if n % 1 != 0 else 0
##############
def get_decimal(n): 
    if type(n) is int:
        return 0
    return float('0'+str(n)[str(n).index('.'):])
#############
def get_decimal(n):
    return float(f"0.{str(n).split('.')[1]}") if type(n) == float else 0
##############
import re

def get_decimal(n): 
    try:
        x = re.search("\.[0-9]+",str(n)).group()
        return float("0." + x[1:])
    except:
        return 0
#################
def get_decimal(n): 
    return [n % 1, -n % 1][ n < 0]
################
def get_decimal(n):
    return float(f"0.{str(n).split('.')[1]}") if type(n) == float else 0
##############
def get_decimal(n):
    n = float(abs(n))
    nums = str(n).split('.')
    return n - int(nums[0])
###############
def get_decimal(n):
    if n<0:
        n=n*-1
        return n%1
    else:
        return n%1
print(get_decimal(-1.2))
