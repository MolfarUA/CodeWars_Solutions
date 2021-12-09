def int32_to_ip(int32):
    return '.'.join([str((int32%256**i)// 256 ** (i - 1)) for i in range(4, 0, -1)])
#########
from ipaddress import IPv4Address

def int32_to_ip(int32):
    return str(IPv4Address(int32))
#############
def int32_to_ip(int32):
    return '{}.{}.{}.{}'.format(*int32.to_bytes(4, 'big'))
#############
def int32_to_ip(int32):
    """
    The solution involves bitwise AND of int32 and a mask that we can shift around.
    Say we have the number 17194 (0b0100001100101010). This can be divided into 2
    bytes: 01000011 and 00101010.
    We can AND this with a byte that is filled with 1s - 255 (0b11111111), shifted
    left by a certain amount of bytes to get the digits in that byte:
    01000011 00101010 # 17194
    11111111 00000000 # 255 << 8
    01000011 00000000 # 17194 & 255 << 8
    However, we need to shift this value *back* to get a number within (0,255)
    inclusive, as required, so shift right by the same amount.
    """
    first = (int32 & (255 << 24)) >> 24
    second = (int32 & (255 << 16)) >> 16
    third = (int32 & (255 << 8)) >> 8
    fourth = int32 & 255
    return f"{first}.{second}.{third}.{fourth}"
#####################
from ipaddress import ip_address

def int32_to_ip(int32):
    return str(ip_address(int32))
####################
def int32_to_ip(i):
    return '.'.join([str(x) for x in [i >> 24 & 0xFF, 
                                      i >> 16 & 0xFF,
                                      i >> 8 & 0xFF,
                                      i & 0xFF]])
################
# convert binary
def convert_bin(arr):
  summa = 0
  for x,y in enumerate(arr[::-1]):
    summa = summa + 2**x * int(y)
  return summa
  
  
def int32_to_ip(int32):

  n = ""

  while int32 > 0:
    y = str(int32 % 2)
    n = y + n
    int32 = int(int32 / 2)


  if len(n) != 32: # make 32 bit
    while len(n) != 32:
      n = '0' + n

  a = n[:8] # first 8
  b = n[8:16] # secound 8
  c = n[16 : 24] # third 8
  d = n[24 : 32] # fourth 8

  return(str(convert_bin(a))+'.'+str(convert_bin(b))+'.'+str(convert_bin(c))+'.'+str(convert_bin(d)))
#####################
def int32_to_ip(int32):
    bit32 = '{:032b}'.format(int32)
    return '.'.join(str(number) for number in [int(bit32[:8], 2), int(bit32[8:16], 2), int(bit32[16:24], 2), int(bit32[24:32], 2)])
###############
def int32_to_ip(int32):
    bin32 = format(int32,"b")
    bin32= bin32.rjust(32,'0')
    s,b = 0,8
    lst=[]
    for i in range(4):
        ip = str(int(bin32[s:b],2))
        lst.append(ip)
        s,b = b, b+8
    return ".".join(lst)
#################
def int32_to_ip(int32):
    binary = f"{int32:b}"
    address = ""
    while len(binary) < 32:
        binary = "0" + binary
    for i in range(4):
        address += f"{int(binary[i * 8 : (i * 8) + 8], 2)}."
    return address[:-1]
###############
