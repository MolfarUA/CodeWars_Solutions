536602df5d0266e7b0000d31


import re
class Morse:
    @classmethod
    def encode(self, message):
        bits = "0000000".join(["000".join([Morse.alpha[char] for char in word])
                               for word in message.split(' ')])
        return [int((int("{0:0<32s}".format(bit32), base=2) + 0x80000000) % 0x100000000 - 0x80000000)
                for bit32 in re.findall(r'.{1,32}', bits)]
    
    @classmethod
    def decode(self,array):
        code = ''.join(["{0:032b}".format((i + 0x100000000) % 0x100000000) for i in array]).rstrip('0')
        return ' '.join([ ''.join([Morse.alpha_re[char] for char in word.split("000")])
                          for word in  code.split("0000000")])

    alpha={
  'A': '10111',
  'B': '111010101',
  'C': '11101011101',
  'D': '1110101',
  'E': '1',
  'F': '101011101',
  'G': '111011101',
  'H': '1010101',
  'I': '101',
  'J': '1011101110111',
  'K': '111010111',
  'L': '101110101',
  'M': '1110111',
  'N': '11101',
  'O': '11101110111',
  'P': '10111011101',
  'Q': '1110111010111',
  'R': '1011101',
  'S': '10101',
  'T': '111',
  'U': '1010111',
  'V': '101010111',
  'W': '101110111',
  'X': '11101010111',
  'Y': '1110101110111',
  'Z': '11101110101',
  '0': '1110111011101110111',
  '1': '10111011101110111',
  '2': '101011101110111',
  '3': '1010101110111',
  '4': '10101010111',
  '5': '101010101',
  '6': '11101010101',
  '7': '1110111010101',
  '8': '111011101110101',
  '9': '11101110111011101',
  '.': '10111010111010111',
  ',': '1110111010101110111',
  '?': '101011101110101',
  "'": '1011101110111011101',
  '!': '1110101110101110111',
  '/': '1110101011101',
  '(': '111010111011101',
  ')': '1110101110111010111',
  '&': '10111010101',
  ':': '11101110111010101',
  ';': '11101011101011101',
  '=': '1110101010111',
  '+': '1011101011101',
  '-': '111010101010111',
  '_': '10101110111010111',
  '"': '101110101011101',
  '$': '10101011101010111',
  '@': '10111011101011101',
  ' ': '0'}
    alpha_re = dict([ (value,key) for key,value in alpha.items()])
________________________________________________
alpha = {
    'A': '10111',
    'B': '111010101',
    'C': '11101011101',
    'D': '1110101',
    'E': '1',
    'F': '101011101',
    'G': '111011101',
    'H': '1010101',
    'I': '101',
    'J': '1011101110111',
    'K': '111010111',
    'L': '101110101',
    'M': '1110111',
    'N': '11101',
    'O': '11101110111',
    'P': '10111011101',
    'Q': '1110111010111',
    'R': '1011101',
    'S': '10101',
    'T': '111',
    'U': '1010111',
    'V': '101010111',
    'W': '101110111',
    'X': '11101010111',
    'Y': '1110101110111',
    'Z': '11101110101',
    '0': '1110111011101110111',
    '1': '10111011101110111',
    '2': '101011101110111',
    '3': '1010101110111',
    '4': '10101010111',
    '5': '101010101',
    '6': '11101010101',
    '7': '1110111010101',
    '8': '111011101110101',
    '9': '11101110111011101',
    '.': '10111010111010111',
    ',': '1110111010101110111',
    '?': '101011101110101',
    "'": '1011101110111011101',
    '!': '1110101110101110111',
    '/': '1110101011101',
    '(': '111010111011101',
    ')': '1110101110111010111',
    '&': '10111010101',
    ':': '11101110111010101',
    ';': '11101011101011101',
    '=': '1110101010111',
    '+': '1011101011101',
    '-': '111010101010111',
    '_': '10101110111010111',
    '"': '101110101011101',
    '$': '10101011101010111',
    '@': '10111011101011101',
    ' ': '0000000',
}

def int_from_twocomp(val, bits):
    """Compute the 2's compliment of int value val."""
    # if sign bit is set e.g., 8bit: 128-255
    if (val & (1 << (bits - 1))) != 0:
        # compute negative value
        val = val - (1 << bits)
    return val

def twocomp_from_int(num):
    return format(num if num >= 0 else (1 << 32) + num, '032b')

class Morse:
    @classmethod
    def encode(self, message):
        bits = ''
        for idx, m in enumerate(message):
            bits += alpha[m]
            if idx + 1 < len(message) and message[idx+1] != ' ' \
                and message[idx] != ' ':
                    bits += '000'

        # split into 32 bit parts
        parts = []
        for i in range(0, len(bits), 32):
            p = bits[i: i + 32]
            parts.append(p + '0' * (32 - len(p)))
        
        # convert 32 bit strings to signed integers
        int_parts = [int_from_twocomp(int(p, 2), len(p)) for p in parts]

        return int_parts
    
    @classmethod
    def decode(self, array):
        # reverse alphabet dict
        rev_alpha = {bits: char for char, bits in alpha.items()}
        all_bits = sorted(rev_alpha.keys(), key=lambda s: len(s), reverse=True)

        # convert integers to string of bits
        msg_bits = [twocomp_from_int(x) for x in array]
        msg_bits = ''.join(msg_bits)

        msg = ''
        while any(bool(int(x)) for x in msg_bits):
            found = False

            for bits in all_bits:
                if msg_bits[:len(bits)] == bits:
                    # found match
                    msg += rev_alpha[bits]

                    # remove found bits from msg_bits
                    msg_bits = msg_bits[len(bits):]

                    found = True
                    break

            if not found:
                if msg_bits[:7] == '0000000':
                    msg_bits = msg_bits[7:]
                    msg += ' '
                elif msg_bits[:3] == '000':
                    msg_bits = msg_bits[3:]

        # remove trailing spaces
        msg = msg.rstrip()

        return msg
________________________________________________
class Morse:        
    @classmethod
    def encode(self, s):
        bits = '000'.join(enc(c) for c in s)
        return [complement(int(bits[i*32:i*32+32].ljust(32, '0'), 2)) for i in range((len(bits)-1)//32 + 1)]
    
    @classmethod
    def decode(self, a):
        bits = ''.join(bin(n + 4294967296 if n < 0 else n)[2:].rjust(32, '0') for n in a)
        return ''.join(dec(b) for b in bits.strip('0').replace('0000000', '000 000').split('000') if b)

alpha={
  'A': '10111',
  'B': '111010101',
  'C': '11101011101',
  'D': '1110101',
  'E': '1',
  'F': '101011101',
  'G': '111011101',
  'H': '1010101',
  'I': '101',
  'J': '1011101110111',
  'K': '111010111',
  'L': '101110101',
  'M': '1110111',
  'N': '11101',
  'O': '11101110111',
  'P': '10111011101',
  'Q': '1110111010111',
  'R': '1011101',
  'S': '10101',
  'T': '111',
  'U': '1010111',
  'V': '101010111',
  'W': '101110111',
  'X': '11101010111',
  'Y': '1110101110111',
  'Z': '11101110101',
  '0': '1110111011101110111',
  '1': '10111011101110111',
  '2': '101011101110111',
  '3': '1010101110111',
  '4': '10101010111',
  '5': '101010101',
  '6': '11101010101',
  '7': '1110111010101',
  '8': '111011101110101',
  '9': '11101110111011101',
  '.': '10111010111010111',
  ',': '1110111010101110111',
  '?': '101011101110101',
  "'": '1011101110111011101',
  '!': '1110101110101110111',
  '/': '1110101011101',
  '(': '111010111011101',
  ')': '1110101110111010111',
  '&': '10111010101',
  ':': '11101110111010101',
  ';': '11101011101011101',
  '=': '1110101010111',
  '+': '1011101011101',
  '-': '111010101010111',
  '_': '10101110111010111',
  '"': '101110101011101',
  '$': '10101011101010111',
  '@': '10111011101011101',
  ' ': '0'}
rvrse = {v:k for k, v in alpha.items()}

complement = lambda n: n - 4294967296 if n & 2147483648 else n

enc = lambda c: alpha.get(c, c)
dec = lambda s: rvrse.get(s, s)
________________________________________________
import re


class Morse:
    @classmethod
    def two_comp_str_to_int(cls, str_val, bits):
        val = int(str_val, 2)
        if (val & (1 << (bits - 1))) != 0:
            val -= 1 << bits
        return val

    @classmethod
    def two_comp_int_to_str(cls, int_val, bits):
        s = bin(int_val & int('1' * bits, 2))[2:]
        return ('{0:0>%s}' % bits).format(s)

    @classmethod
    def encode(cls, message):
        bits = '000'.join(cls.ALPHA[c] for c in message)
        bits = bits.ljust((len(bits) + (cls.BITS - 1)) // cls.BITS * cls.BITS, '0')
        result = [cls.two_comp_str_to_int(bits[i:i + cls.BITS], cls.BITS) for i in range(0, len(bits), cls.BITS)]
        return result

    @classmethod
    def decode(cls, array):
        bits = ''.join(cls.two_comp_int_to_str(x, cls.BITS) for x in array)
        characters = [x for x in cls.REGEX_SPLIT.split(bits)]
        result = [cls.ALPHA_REV.get(x.rstrip('0') if x != '0' else x, '') for x in characters]
        return ''.join(result)

    REGEX_SPLIT = re.compile(r'(?<=1)0{3}(?=0)|(?<=0)0{3}(?=1)|(?<=1)0{3}(?=1)')
    BITS = 32
    ALPHA = {
        'A': '10111',
        'B': '111010101',
        'C': '11101011101',
        'D': '1110101',
        'E': '1',
        'F': '101011101',
        'G': '111011101',
        'H': '1010101',
        'I': '101',
        'J': '1011101110111',
        'K': '111010111',
        'L': '101110101',
        'M': '1110111',
        'N': '11101',
        'O': '11101110111',
        'P': '10111011101',
        'Q': '1110111010111',
        'R': '1011101',
        'S': '10101',
        'T': '111',
        'U': '1010111',
        'V': '101010111',
        'W': '101110111',
        'X': '11101010111',
        'Y': '1110101110111',
        'Z': '11101110101',
        '0': '1110111011101110111',
        '1': '10111011101110111',
        '2': '101011101110111',
        '3': '1010101110111',
        '4': '10101010111',
        '5': '101010101',
        '6': '11101010101',
        '7': '1110111010101',
        '8': '111011101110101',
        '9': '11101110111011101',
        '.': '10111010111010111',
        ',': '1110111010101110111',
        '?': '101011101110101',
        "'": '1011101110111011101',
        '!': '1110101110101110111',
        '/': '1110101011101',
        '(': '111010111011101',
        ')': '1110101110111010111',
        '&': '10111010101',
        ':': '11101110111010101',
        ';': '11101011101011101',
        '=': '1110101010111',
        '+': '1011101011101',
        '-': '111010101010111',
        '_': '10101110111010111',
        '"': '101110101011101',
        '$': '10101011101010111',
        '@': '10111011101011101',
        ' ': '0'}
    ALPHA_REV = {v: k for k, v in ALPHA.items()}
________________________________________________
CHAR_DOTDASH_MAP = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.','G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..', '\'': '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
}

CHAR_BINARY_MAP = {k: v.replace('-', '1110').replace('.', '10')[:-1] for k, v in CHAR_DOTDASH_MAP.iteritems()}
CHAR_BINARY_MAP[' '] = '0'
BINARY_CHAR_MAP = {v: k for k, v in CHAR_BINARY_MAP.iteritems()}

CHAR_SEPARATOR = '000'
INT_LEN = 32
INT_MASK = int('1'*31, 2)

def binary_to_signed_int(binary):
    return int(binary, 2) if binary[0] == '0' else -(int(binary[1:], 2)^INT_MASK) - 1

def _to_bin(number):
    result = bin(number)[2:]
    return '0'*(INT_LEN - len(result) - 1) + result

def signed_int_to_binary(signed_int):
    return '0' + _to_bin(signed_int) if signed_int > 0 else '1' + _to_bin(-(signed_int^INT_MASK) - 1)

class Morse:
    @classmethod
    def encode(self,message):
        message = message.upper()
        binary_repr = CHAR_SEPARATOR.join([CHAR_BINARY_MAP[char] for char in message])
        r = len(binary_repr)%INT_LEN
        if r: binary_repr += '0'*(INT_LEN - r)
        n = len(binary_repr)//INT_LEN
        return [binary_to_signed_int(binary_repr[i*INT_LEN: (i + 1)*INT_LEN]) for i in xrange(n)]
    
    @classmethod
    def decode(self,array):
        binary_repr = reduce(lambda x0, x1: x0 + signed_int_to_binary(x1), array, '')
        binary_repr = binary_repr.strip('0')
        binary_repr = binary_repr.replace('0000000', ',0,').replace('000', ',')
        binary_repr = binary_repr.split(',')
        return ''.join([BINARY_CHAR_MAP[binary_char] for binary_char in binary_repr])
________________________________________________
class Morse:
    
    BITS = 32
    RNG  = 1<<BITS
    
    @classmethod
    def encode(cls,s):
        s = '000'.join(map(alpha.__getitem__, s))
        return [ cls.twoComp_toN(s[i:i+cls.BITS]) for i in range(0,len(s),cls.BITS) ]
        
    @classmethod
    def twoComp_toN(cls,s):
        s = s.ljust(cls.BITS,'0')
        return int(s,2) - cls.RNG*(s[0]=='1')
    
    @classmethod
    def twoComp_toS(cls,n):
        return f'{ n + cls.RNG*(n<0) :b}'.zfill(cls.BITS)
        
    @classmethod
    def decode(cls,lst):
        s = ''.join(map(cls.twoComp_toS, lst)).rstrip('0')
        return ' '.join(map(cls.buildWord, s.split('0000000')))
    
    @classmethod
    def buildWord(cls,w):
        return ''.join(map(revAlpha.__getitem__, w.split('000')))
        
        
alpha={
  'A': '10111',
  'B': '111010101',
  'C': '11101011101',
  'D': '1110101',
  'E': '1',
  'F': '101011101',
  'G': '111011101',
  'H': '1010101',
  'I': '101',
  'J': '1011101110111',
  'K': '111010111',
  'L': '101110101',
  'M': '1110111',
  'N': '11101',
  'O': '11101110111',
  'P': '10111011101',
  'Q': '1110111010111',
  'R': '1011101',
  'S': '10101',
  'T': '111',
  'U': '1010111',
  'V': '101010111',
  'W': '101110111',
  'X': '11101010111',
  'Y': '1110101110111',
  'Z': '11101110101',
  '0': '1110111011101110111',
  '1': '10111011101110111',
  '2': '101011101110111',
  '3': '1010101110111',
  '4': '10101010111',
  '5': '101010101',
  '6': '11101010101',
  '7': '1110111010101',
  '8': '111011101110101',
  '9': '11101110111011101',
  '.': '10111010111010111',
  ',': '1110111010101110111',
  '?': '101011101110101',
  "'": '1011101110111011101',
  '!': '1110101110101110111',
  '/': '1110101011101',
  '(': '111010111011101',
  ')': '1110101110111010111',
  '&': '10111010101',
  ':': '11101110111010101',
  ';': '11101011101011101',
  '=': '1110101010111',
  '+': '1011101011101',
  '-': '111010101010111',
  '_': '10101110111010111',
  '"': '101110101011101',
  '$': '10101011101010111',
  '@': '10111011101011101',
  ' ': '0'}

revAlpha = {v:k for k,v in alpha.items()}
________________________________________________
import numpy as np

class Morse:
    
    @classmethod
    def encode(self,message):
        bnt = '0000000'.join('000'.join(self.alpha[x] for x in e) for e in message.split())
        return [np.int32(int(bnt[i:i+32].ljust(32,"0"),2))  for i in range(0,len(bnt),32) ]
        
    @classmethod
    def decode(self,array):
        rec = ''.join('{:032b}'.format( np.uint32(e)) for e in array).split('0000000')
        return ' '.join(''.join({v:k for k,v in self.alpha.items()}.get(e.strip('0'),'') for e in words.split('000')) for words in rec).strip()
    
    alpha={
  'A': '10111', 'B': '111010101', 'C': '11101011101', 'D': '1110101', 'E': '1', 'F': '101011101', 'G': '111011101',
  'H': '1010101', 'I': '101', 'J': '1011101110111', 'K': '111010111', 'L': '101110101', 'M': '1110111', 'N': '11101',
  'O': '11101110111', 'P': '10111011101', 'Q': '1110111010111', 'R': '1011101', 'S': '10101', 'T': '111', 'U': '1010111',
  'V': '101010111', 'W': '101110111', 'X': '11101010111', 'Y': '1110101110111', 'Z': '11101110101', '0': '1110111011101110111',
  '1': '10111011101110111', '2': '101011101110111', '3': '1010101110111', '4': '10101010111', '5': '101010101', '6': '11101010101',
  '7': '1110111010101', '8': '111011101110101', '9': '11101110111011101', '.': '10111010111010111', ',': '1110111010101110111', 
  '?': '101011101110101', "'": '1011101110111011101', '!': '1110101110101110111', '/': '1110101011101', '(': '111010111011101',
  ')': '1110101110111010111', '&': '10111010101', ':': '11101110111010101', ';': '11101011101011101', '=': '1110101010111',
  '+': '1011101011101', '-': '111010101010111', '_': '10101110111010111', '"': '101110101011101', '$': '10101011101010111',
  '@': '10111011101011101', ' ': '0'}
