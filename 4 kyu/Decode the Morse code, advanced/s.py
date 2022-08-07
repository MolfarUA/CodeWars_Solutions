54b72c16cd7f5154e9000457


def decodeBits(bits):
    import re
    
    # remove trailing and leading 0's
    bits = bits.strip('0')
    
    # find the least amount of occurrences of either a 0 or 1, and that is the time hop
    time_unit = min(len(m) for m in re.findall(r'1+|0+', bits))
    
    # hop through the bits and translate to morse
    return bits[::time_unit].replace('111', '-').replace('1','.').replace('0000000','   ').replace('000',' ').replace('0','')

def decodeMorse(morseCode):
    return ' '.join(''.join(MORSE_CODE[l] for l in w.split()) for w in morseCode.split('   '))
_____________________________
MORSE_CODE['_'] = ' '

def decodeBits(bits):
    # strip extra zeros
    bits = bits.strip('0')
    
    # if no zeros in bits
    if '0' not in bits:
        return '.'
    
    # check for multiple bits per dot
    minOnes = min(len(s) for s in bits.split('0') if s)
    minZeros = min(len(s) for s in bits.split('1') if s)
    m = min(minOnes, minZeros)
    
    # decode bits to morse code
    return bits.replace('111'*m, '-').replace('0000000'*m, ' _ ').replace('000'*m, ' ').replace('1'*m, '.').replace('0'*m, '')

def decodeMorse(morseCode):
    # decode morse code to letters
    return ''.join(MORSE_CODE[c] for c in morseCode.split())
_____________________________
from re import findall

MORSE_CODE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
    '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'", '-.-.--': '!',
    '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&', '---...': ':',
    '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-', '..--.-': '_',
    '.-..-.': '"', '...-..-': '$', '.--.-.': '@', '...---...': 'SOS'
}
MORSE_CODE["_"] = " "

def decodeBits(bitString):
    bitString = bitString.strip("0")
    m = len(sorted(findall( "(1+|0+)", bitString ), key=len)[0])
    return bitString.replace('111'*m, '-').replace('000'*m, ' ').replace('1'*m, '.').replace('0'*m, '')

def decodeMorse(morseCode):
    print(morseCode)
    return "".join(map(lambda m: MORSE_CODE.get(m," "), morseCode.replace("   "," _ " ).split(" "))).strip()
_____________________________
def decodeBits(bits):
    bits = bits.strip('0')
    time_unit = min(map(len, bits.replace('1', ' ').split() + bits.replace('0', ' ').split()))
    word_sep = '0' * 7 * time_unit
    char_sep = '0' * 3 * time_unit
    ones_sep = '0' * 1 * time_unit
    dash = '1' * 3 * time_unit
    dot = '1' * 1 * time_unit
    return bits.replace(dash, '-').replace(dot, '.') \
               .replace(word_sep, '   ').replace(char_sep, ' ').replace(ones_sep, '')

def decodeMorse(morse_code):
    return ' '.join(''.join(map(MORSE_CODE.get, word.split()))
                    for word in morse_code.split('   ')).strip()
_____________________________
from re import split
def decodeBits(bits):
    unit = min([len(s) for s in split(r'0+',bits.strip('0'))] + [len(s) for s in split(r'1+',bits.strip('0'))  if s != ''])
    return bits.replace('0'*unit*7,'   ').replace('0'*unit*3,' ').replace('1'*unit*3,'-').replace('1'*unit,'.').replace('0','')
def decodeMorse(morseCode):
    # ToDo: Accept dots, dashes and spaces, return human-readable message
    return ' '.join(''.join(MORSE_CODE[letter] for letter in word.split(' ')) for word in morseCode.strip().split('   '))
_____________________________
def decodeBits(bits):
    bits = bits.strip('0')
    if '0' not in bits:
        return '.'
    u = 1
    while ('0' * u) not in bits.split('1') and ('1' * u) not in bits.split('0'):
        u += 1
    return ' '.join([char.replace('1' * 3 * u, '-').replace('1' * u, '.').replace('0', '')
                     for char in bits.split('0' * 3 * u)])

def decodeMorse(morseCode):
    MORSE_CODE[''] = ' '
    arr = [MORSE_CODE[x] for x in morseCode.strip().split(' ')]
    return "".join(arr).replace('  ', ' ')
_____________________________
from re import compile

TOKENIZER = compile('(0+)')

def decodeBits(bits):
    tokens = TOKENIZER.split(bits.strip('0'))
    lenDot = min(len(token) for token in tokens)
    lenDash = 3 * lenDot
    ret = []
    for token in tokens:
        if token[0] == '1':
            ret.append('.' if len(token) < lenDash else '-')
        elif len(token) > lenDot:
            ret.append(' ' if len(token) <= lenDash else '   ')
    return ''.join(ret)

def decodeMorse(morseCode):
    return ' '.join(''.join(MORSE_CODE[c] for c in word.split(' ')) for word in morseCode.strip().split('   '))
_____________________________
import re


def decode_bits(bits):
    ones_sequence = re.split('0+', bits.strip('0'))
    zeros_sequence = [zeros for zeros in re.split('1+', bits.strip('0')) if zeros]
    min_ones, min_zeros = len(min(ones_sequence)), len(min(zeros_sequence, default=''))
    times = min_ones if not min_zeros else min(min_ones, min_zeros)
    return bits.strip('0').replace('1' * 3 * times, '-').replace('1' * times, '.').replace('0' * 7 * times, ' + ').replace('0' * 3 * times, ' ').replace('0' * times, '')

def decode_morse(morseCode):
    return ''.join(MORSE_CODE[word] if word != '+' else ' ' for word in morseCode.strip().split())
_____________________________
import itertools

def rate(str):
    return min(len(list(y)) for (c,y) in itertools.groupby(str) if c=='0' or c=='1')

def decode_bits(bits):
    #ignoring the first and last zeros
    start=0
    if bits[start]=='0':
        while bits[start]=='0':
            start+=1           
    end=len(bits)-1
    if bits[end]=='0':
        while bits[end]=='0':
            end-=1    
    bits=bits[start:end+1]
    #transmission rate
    k=rate(bits)
    return bits.replace('111' * k, '-').replace('0000000' * k, '   ').replace('000' * k, ' ').replace('1' * k, '.').replace('0' * k, '').replace('0', '')

def decodeMorse(morseCode):
    return ' '.join(''.join(MORSE_CODE[letter] for letter in word.split(' ')) for word in morseCode.strip().split('   '))
_____________________________
import re


def decode_bits(bits):
    
    bits = bits.strip('0')
    
    
    time_expired = min(len(bit) for bit in re.findall(r'1+|0+', bits))
    
    
    
    return bits[::time_expired].replace('111', '-').replace('1','.').replace('0000000','   ').replace('000',' ').replace('0','')

def decode_morse(morseCode):
    
    return ' '.join(''.join(MORSE_CODE[code] for code in code.split()) for code in morseCode.split('   '))
_____________________________
import re
def decode_bits(bits):
    
    words = re.split('0{1,}',bits.strip('0'))
    bit_rate = int(min(len(w) for w in words))
    words = re.split('1{1,}',bits.strip('0').strip('1'))
    bit_rate_1 = int(min(len(w) for w in words))
    if bit_rate_1 != 0 and  bit_rate_1 < bit_rate:
        bit_rate = bit_rate_1
    dt_dash_dict = {'1' * bit_rate: '.', '111' * bit_rate : '-'}
    
    return '   '.join(' '.join(''.join(dt_dash_dict[sym] for sym in letter.split('0' * bit_rate)) for letter in word.split('000' * bit_rate)) for word in bits.strip('0').split('0000000' * bit_rate))

def decode_morse(morseCode):
    # ToDo: Accept dots, dashes and spaces, return human-readable message
    return ' '.join(''.join(MORSE_CODE[letter] for letter in word.split(' ')) for word in morseCode.strip().split('   '))
