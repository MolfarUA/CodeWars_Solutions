def binary_to_string(binary):
    result = ''
    for i in range(0, len(binary), 8):
        result += chr(int(binary[i:i + 8], 2))
    return result
###########
def binary_to_string(binary):
    return "".join( [ chr( int(binary[i: i+8], 2) ) for i in range(0, len(binary), 8) ] )
#########
def binary_to_string(binary):
    return "".join( [ chr( int(binary[i: i+8], 2) ) for i in range(0, len(binary), 8) ] )
###########
import re

def binary_to_string(bits):
    return ''.join(chr(int(byte, 2)) for byte in re.findall(r'\d{8}', bits))
#########
binary_to_string=lambda b:''.join(__import__('binascii').unhexlify('%x' % int('0b'+b[i:i+8],base=2)).decode("utf-8") for i in range(0,len(b),8))
##########
import re

def binary_to_string(binary):
    return re.sub(r'[01]{8}', lambda x: chr(int(x.group(), 2)), binary)
###########
def binary_to_string(binary):
    new_ = []
    for i in [binary[i:i+8] for i in range(0, len(binary), 8)]: new_.append(chr(int(i, 2)))
    return ''.join(new_)
###########
binary_to_string=lambda t:''.join(chr(int(t[i:i+8],2))for i in range(0,len(t),8))
##########
def binary_to_string(binary):
    b_lst = []
    for i in range(0,len(binary),8):
        b_lst.append(binary[i: i+8])
    for i in range(len(b_lst)):
        b_lst[i] = chr(int(b_lst[i], 2))
    return ''.join(b_lst)
