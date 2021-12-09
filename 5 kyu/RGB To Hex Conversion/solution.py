def rgb(r, g, b):
    arr = [255 if i > 255 else 0 if i < 0 else i for i in [r,g,b]]
    return ''.join([format(i, '02x').upper() for i in arr])
############
def rgb(r, g, b):
    round = lambda x: min(255, max(x, 0))
    return ("{:02X}" * 3).format(round(r), round(g), round(b))
############
def limit(num):
    if num < 0:
        return 0
    if num > 255:
        return 255
    return num


def rgb(r, g, b):
    return "{:02X}{:02X}{:02X}".format(limit(r), limit(g), limit(b))
##########
def rgb(r, g, b):
    clamp = lambda x: max(0, min(x, 255))
    return "%02X%02X%02X" % (clamp(r), clamp(g), clamp(b))
########
def rgb(*args):
    return ''.join(map(lambda x: '{:02X}'.format(min(max(0, x), 255)), args));
##########
def rgb(r, g, b):
    """
    Return hex string representation of ``r,g,b`` values. A saturation \
will be applied to the input values to ensure they are betweem 0 \
and 255.
    
    :param r: Red channel
    :type r: int 
    
    :param g: Green channel
    :type g: int 
    
    :param b: Blue channel
    :type b: int 
    
    :return: Hex representation.
    :rtype: str
    
    >>> rgb(123,45,67)
    '7B2D43'
    >>> rgb(-20,123,456)
    '007BFF'
    >>> rgb('no int',123,123)
    Traceback (most recent call last):
        ...
    TypeError: 'r' is not of type int
    >>> rgb(123,'no int',123)
    Traceback (most recent call last):
        ...
    TypeError: 'g' is not of type int
    >>> rgb(123,123,'no int')
    Traceback (most recent call last):
        ...
    TypeError: 'b' is not of type int
    """
    
    if not type(r).__name__ == 'int':    # python2 does not have instanceof()
        raise TypeError("'r' is not of type int")
    if not type(g).__name__ == 'int':    # python2 does not have instanceof()
        raise TypeError("'g' is not of type int")
    if not type(b).__name__ == 'int':    # python2 does not have instanceof()
        raise TypeError("'b' is not of type int")
    
    return "{r:02X}{g:02X}{b:02X}".format(
        r=saturate(r),
        g=saturate(g),
        b=saturate(b),
    )


def saturate(x):
    """
    Saturates an integer ``x`` to be ``0<=x<=255``.
    
    :param x: Integer to be saturated
    :type x: int 
    
    :return: Saturated integer
    :rtype: int
    
    >>> saturate(345)
    255
    >>> saturate(-3)
    0
    >>> saturate(123)
    123
    >>> saturate("no int")
    Traceback (most recent call last):
        ...
    TypeError: given value is not of type int
    """
    if not type(x).__name__ == 'int':    # python2 does not have instanceof()
        raise TypeError("given value is not of type int")
    
    x = 0 if x<0 else x
    x = 255 if x>255 else x
    
    return x


if __name__ == "__main__":
    import doctest
    doctest.testmod()
###############################################
def hex_con(color):
    hex_dict = '0123456789ABCDEF'
    d1 = color//16
    d2 = color%16
    if d1 > 15:
        d1 = 15
        d2 = 15
    elif d1 < 0:
        d1 = 0
        d2 = 0
    return str(hex_dict[d1]) + str(hex_dict[d2])
    


def rgb(r, g, b):  
    R = hex_con(r)
    G = hex_con(g)
    B = hex_con(b)
    return R+G+B
########################
def rgb(r, g, b): 
    return ''.join(['%02X' % max(0, min(x, 255)) for x in [r, g, b]])
################
def rgb(r, g, b):
    def get_hex(s):
        if s > 255: s = 255
        if s < 0: s = 0
        return hex(s)[2:].upper() if len(hex(s)[2:]) > 1 else "0" + hex(s)[2:]
    return get_hex(r) + get_hex(g) + get_hex(b)
##############
def rgb(r, g, b):
    return '{0:02X}{1:02X}{2:02X}'.format(max(min(r, 255), 0), max(min(g, 255), 0), max(min(b, 255), 0))
#############
def rgb(r, g, b):
    def check(n):
        if n > 255:
            return 255
        elif n < 0:
            return 0
        return n
            
    return "{:02X}{:02X}{:02X}".format(*[check(i) for i in (r, g, b)])
#################
def rgb(r, g, b):
    s = []
    f = '{} {} {}'.format(r, g, b)
    for i in f.split():
        i = int(i)
        if '-' in str(i):
            s.append('00')
        elif i in range(256):
            s.append('%02X' % i)
        else:
            s.append('FF')
    return ''.join(s)


print(rgb(-20, 254, 125))
##############
def rgb(r, g, b):
    if r < 0:
        r = 0
    if g < 0:
        g = 0
    if b < 0:
        b = 0
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    return hex(r)[2:].upper().zfill(2) + hex(g)[2:].upper().zfill(2) + \
    hex(b)[2:].upper().zfill(2)
##################
def rgb(r, g, b):
    
    rgbTest = [r, g, b]
    hexMatch = {10 : 'A', 11 : 'B', 12 : 'C', 13 : 'D', 14 : 'E', 15 : 'F'}
    result = ""
    
    
    for color in rgbTest:
        
        if color > 255:
            color = 255
        if color < 0:
            color = 0;
        
        Div1 = int(color/16)
        
        Div2 = int(color % 16)
        
        
        
        if Div1 < 10:
            result = result + str(Div1)
        else:
            for code in hexMatch.keys():
                if Div1 == code:
                    result = result + hexMatch[code]
                    
        if Div2 < 10:
            result = result + str(Div2)
        else:
            for code in hexMatch.keys():
                if Div2 == code:
                    result = result + hexMatch[code]
    return result
##################
def rgb(r, g, b):
    num_func = lambda x: x if 0<=x<=255 else (0 if x<=0 else 255)
    convert_func = lambda x: str(hex(x)).replace("0x", "").upper().zfill(2)
    return "".join(list(map(convert_func, map(num_func, [r, g, b]))))
##############
def rgb(r, g, b):
    red = to_hex(r)
    green = to_hex(g)
    blue = to_hex(b)
    return red+green+blue

def to_hex(num):
    if num <= 0:
        return "00"
    elif num >= 255:
        return "FF"
    elif num > 0 and num < 10:
        return '0'+str(num)
    else:
        return hex(num)[2:].upper()
#############
def rgb(r, g, b):
    data_in = [r, g, b]
    res = ''
    for n in data_in:
        if n >= 255:
            res += 'FF'
        elif 255 > n > 15:
            res += hex(n).replace('0x',"").upper()
        elif 16 > n > 0:
            res += '0' + hex(n).replace('0x',"").upper()
        else:
            res += '00'
    return res
