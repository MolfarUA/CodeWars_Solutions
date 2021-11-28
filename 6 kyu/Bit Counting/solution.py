def count_bits(n):
    bit_string = "{0:#b}".format(n)
    one_count = bit_string.count("1")

    return one_count
###########
def countBits(n):
    return bin(n).count("1")
#############
def countBits(n):
    total = 0
    while n > 0:
        total += n % 2
        n >>= 1
    return total
###########
def countBits(n):
    total = 0
    while n > 0:
        total += n % 2
        n >>= 1
    return total
#############
def countBits(n):
    return bin(n)[2:].count('1')
#############
def countBits(n):
    ret = 0
    while n:
        ret += n & 1
        n >>= 1
    return ret
###########
def countBits(n):
    """ count_bits == PEP8, forced camelCase by CodeWars """
    return '{:b}'.format(n).count('1')
############
countBits = lambda n: bin(n).count('1')
##########
def countBits(n):
    total = 0
    binaryNum = bin(n)[2:]
    for num in str(binaryNum):
        if num == "1":
            total += 1
    return total
#########
def countBits(n):
    # Get the binary string of n.
    sBin = str(bin(n))
    # Get the number of occurances of the substring '1'.
    return sBin.count('1')
##############
def countBits(n):
    result =0
    while (n > 0):
        if(n%2)==1: result+=1
        n = int(n/2)
    return result
#############
from gmpy2 import popcount as countBits
##########
def countBits(n):
    return (n & 1) + countBits(n >> 1) if n else 0
###########
def countBits(n):
    return sum(int(x) for x in bin(n)[2:])
########
import array

filters = array.array('L', [
 0x5555555555555555,
 0x3333333333333333,
 0x0f0f0f0f0f0f0f0f,
 0x00ff00ff00ff00ff,
 0x0000ffff0000ffff,
 0x00000000ffffffff,
 ])

def countBits(n):
    count = 0
    while True:
        n, n64 = n >> 64, n & 0xFFFFFFFFFFFFFFFF
        for ii, f in enumerate(filters):
            a,b = f & n64, ~f & n64
            n64 = a + (b >> (1<<ii))
        count += n64
        if not n: return count
###########
def count_bits(n):
    out=""
    count=0
    while(1):
        div=n//2
        mod=n%2        
        out+=str(mod)
        if(div==0):
            break
        n=div  
    for x in out:
        if x=='1':
            count+=1
        else:
            pass
    return count
#################
def countBits(n):
    return list(bin(n)).count('1')
###############
def countBits(n):
    c = 0
    while n:
        c += 1
        n &= n - 1
    return c
###########
def countBits(n):
    str = '{0:08b}'.format(n)
    res = 0
    for i in range(len(str)):
      if(str[i] == "1"):
        res+=1
    return res
############
def countBits(n):
    return "{0:b}".format(n).count('1')
###########
def countBits(n):
    sum = 0
    for i in bin(n)[2:]:
        sum += int(i)
    return sum
