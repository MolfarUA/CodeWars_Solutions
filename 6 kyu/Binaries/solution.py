def code(s):
    return ''.join( f'{"0"*(d.bit_length()-1)}1{d:b}' for d in map(int,s))
    
def decode(s):
    it, n, out = iter(s), 1, []
    for c in it:
        if c=='0':
            n += 1
        else:
            out.append( int(''.join(next(it) for _ in range(n)), 2) )
            n = 1
    return ''.join(map(str, out))
__________________________
def code(stg):
    result = ""
    for d in stg:
        b = f"{int(d):b}"
        result = f"{result}{'0' * (len(b) - 1)}1{b}"
    return result


def decode(stg):
    result = ""
    while stg:
        l = stg.find("1") + 1
        result, stg = f"{result}{int(stg[l:l*2], 2)}", stg[l*2:]
    return result
__________________________
from re import compile

ENC = {str(n): '0' * ~-n.bit_length() + f'1{n:b}' for n in range(10)}
DEC = {v: k for k, v in ENC.items()}
BIN = compile('|'.join(reversed(DEC.keys())))

def code(dec_str: str) -> str:
    return ''.join(map(ENC.get, dec_str))

def decode(bin_str: str) -> str:
    return ''.join(map(DEC.get, BIN.findall(bin_str)))
__________________________
def code(strng):
    dict = {'0': '10', '1': '11', '2': '0110', '3': '0111', '4': '001100', '5': '001101', '6': '001110', '7': '001111', '8': '00011000', '9': '00011001'}
    u = map(lambda r: dict[r], [ strng[i] for i in range(0, len(strng)) ])
    return ''.join(u)
def decode(strng):
    ret = ""
    i = 0
    lg = len(strng)
    while (i < lg):
        zero_i = i
        while ((zero_i < lg) and (strng[zero_i] != '1')):
            zero_i += 1
        l = zero_i - i + 2 
        ret += str(int(strng[zero_i + 1:zero_i + l], 2))
        i = zero_i + l
    return ret
__________________________
def code(s):return''.join( f'{"0"*(d.bit_length()-1)}1{d:b}'for d in map(int,s))
    
def decode(s,o=''):
    while s:i=s.find('1')+1;s,o=s[2*i:],o+str(int(s[i:i*2],2))
    return o
__________________________
from re import sub

def binary(n):
    return '0' * (n.bit_length()-1) + '1' + bin(n)[2:]

def cipher(mode):
    table = dict((str(d), binary(d))[::mode] for d in range(10))
    return lambda s: sub('|'.join(table), lambda m: table[m[0]], s)

code, decode = cipher(1), cipher(-1)

__________________________
import re

DIG2BIN = str.maketrans({
    '0': '10',
    '1': '11',
    '2': '0110',
    '3': '0111',
    '4': '001100',
    '5': '001101',
    '6': '001110',
    '7': '001111',
    '8': '00011000',
    '9': '00011001'
})

BIN2DIG = {
    '10': '0',
    '11': '1',
    '0110': '2',
    '0111': '3',
    '001100': '4',
    '001101': '5',
    '001110': '6',
    '001111': '7',
    '00011000': '8',
    '00011001': '9'
}

DIG_PATTERN = re.compile(
    r'10|11|0110|0111|001100|001101|001110|001111|00011000|00011001'
)


def code(strng):
    return strng.translate(DIG2BIN)


def decode(strng):
    return ''.join(map(BIN2DIG.get, DIG_PATTERN.findall(strng)))
__________________________
def _code(dec):
    news = ""
    for d in map(int, dec):
        k = int.bit_length(d)
        newd = (k-1)*'0' + '1'
        newd += bin(d)[2:] 
        news += newd
    return news
   
def get_table():
    dec2code = dict()
    code2dec = dict()
    for n in map(str, range(10)):
        dec2code[n] = _code(n)
        code2dec[_code(n)] = n
    return dec2code, code2dec

dec2code, code2dec = get_table()
code = lambda strng: "".join(dec2code[d] for d in strng)

def decode(b):
    blist = list(b)
    n = ''
    num = ''
    for item in blist:
        n += item
        if code2dec.get(n):
            num += code2dec[n]
            n = ''
    return num
__________________________
C = ['10', '11', '0110', '0111', '001100', '001101', '001110', '001111', '00011000', '00011001']

def code(s):
    r = ''
    for c in s:
        r = r + C[int(c)]
    return r
    
def decode(s):
    r = ''
    while s:
        for l in (2, 4, 6, 8):
            c = s[:l]
            if c in C: 
                r+=str(C.index(c))
                s = s[l:]
    return r
__________________________
def code(st):
    return ''.join( ( lambda x : f'{"0"*( len( x ) - 1)}1{x}' )( bin( int( e ))[2:]) for e in st )

def decode(st):
    b = '10 11 0110 0111 001100 001101 001110 001111 00011000 00011001'.split()
    doc, i, res = {b[i]:str(i) for i in range(len(b)) }, 2, ''
    while st:
        if st[:i] in doc:
            res += doc[st[:i]]
            st ,i = st[i:], 0
        i += 2
    return res
 
