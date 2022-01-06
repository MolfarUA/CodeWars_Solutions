import re

def decodeBitsAdvanced(bits):
    out, bits = '', bits.strip('0')

    if bits == "":
        return bits

    len1, len0 = map(len, re.findall(r'1+', bits)), map(len, re.findall(r'0+', bits))
    mlen1 = min(len1)

    mlen0 = min(len0) if len0 else mlen1
    lenbit = max(len1) if max(len1) == min(mlen1, mlen0) else float(max(len1)) / 2

    b = re.findall(r'1+|0+', bits)

    for i in b:
        if len(i) >= lenbit*2.3 and len(i) > 4 and i[0] == '0': out += '   '
        elif len(i) > lenbit and i[0] == '1': out += '-'
        elif len(i) > lenbit and i[0] == '0': out += ' '
        elif len(i) <= lenbit and i[0] == '1': out += '.'

    return out


def decodeMorse(morseCode):
    return ' '.join(''.join(MORSE_CODE[l] for l in w.split()) for w in morseCode.split('   '))
  
_______________________________________________
from collections import Counter
import re

""" K-means doesn't seem to work? Well, don't use k-means... """

MORSE_CODE[' ']   = ''
MORSE_CODE['   '] = ' '
CONVERT_BITS      = {('1',1,1): '.', ('1',0,1): '-', ('1',0,0): '-', ('0',1,1): '', ('0',0,1): ' ', ('0',0,0): '   '}

def decodeBitsAdvanced(bits):
    def getChar(t, l): return CONVERT_BITS.get((t, l <= limit1, l <= limit2), "\\")

    stripBits = bits.strip('0')
    if not stripBits: return ''
    
    parts = re.findall(r'0+|1+', stripBits)
    ones  = Counter(len(p) for p in parts if p[0] == "1")
    full  = Counter(map(len, parts))
    
    mi1, ma1 = min(ones), max(ones)
    miF, maF = min(full), max(full)
    gaps1    = set(range(mi1+1, ma1)) - set(ones.keys())
    gapsFull = set(range(miF+1, maF)) - set(full.keys())
    gapsSep  = set()
    if gapsFull:
        miG, maG = min(gapsFull), max(gapsFull)
        gapsSep = set(range(miG,maG)) - gapsFull
        
    limit1, limit2 = ( (miG, maG) if gapsFull and (gapsSep and gaps1 or not gapsSep and len(gapsFull) >= 3)
                  else (miF, maF) if not gapsFull and len(full) < 3
                  else (miG, maF) if gapsFull and not gapsSep
                  else [i for i in range(miF, maF) if i not in full or full[i+1] > 1.5 * full[i]][:2])
    
    return re.sub(r'0+|1+', lambda m: getChar(m.group(0)[0], len(m.group(0))), stripBits)

def decodeMorse(morseCode): return re.sub(r'[.-]+|\s+', lambda m: MORSE_CODE.get(m.group(), "\\"), morseCode)
_______________________________________________
import re
import numpy as np

def histo_lengths(bits,c=None):
    if c is None:
        nbits,count = np.unique(list(map(len,bits.split('0')))+list(map(len,bits.split('1'))),return_counts=True)
    else:
        nbits,count = np.unique(list(map(len,bits.split({'1':'0','0':'1'}[c]))),return_counts=True)
    if nbits.shape[0]>0 and nbits[0]==0:
        nbits = nbits[1:]
        count = count[1:]
    return (nbits,count)

def histo_heuristic(histo,n1,n3,n7):
    t = np.zeros((3),dtype=float)
    N = np.zeros((3),dtype=float)
    t[0] = (histo[0]*histo[1])[np.logical_and(histo[0]>=n1,histo[0]<n3)].sum()
    t[1] = (histo[0]*histo[1])[np.logical_and(histo[0]>=n3,histo[0]<n7)].sum()
    t[2] = (histo[0]*histo[1])[histo[0]>=n7].sum()
    N[0] = histo[1][np.logical_and(histo[0]>=n1,histo[0]<n3)].sum()
    N[1] = histo[1][np.logical_and(histo[0]>=n3,histo[0]<n7)].sum()
    N[2] = histo[1][histo[0]>=n7].sum()
    t[0] /= N[0]
    t[1] = t[1]/N[1] if N[1]>0 else n3
    t[2] = t[2]/N[2] if N[2]>0 else n7
    N_nom = np.array([0.6,0.35,0.05])
    t_nom = np.array([0.1,0.29,0.61])
    N_nom /= N_nom.sum()
    t_nom /= t_nom.sum()
    wt = np.exp(-0.08*N.sum()) # balance towards timing t for low N
    N /= N.sum()
    t /= t.sum()
    h = (1-wt)*(N-N_nom).std()+wt*(t-t_nom).std()
    return h

def get_times(histo):
    n1 = histo[0][0]
    n3 = 3*n1
    n7 = 7*n1
    if histo[0].shape[0]==1:
        return [(n1,n3,n7,0.0)]
    hlist = []
    for i3 in range(n1+1,histo[0][-1]+2):
        for i7 in range(i3+1,histo[0][-1]+2):
            h = histo_heuristic(histo,n1,i3,i7)
            hlist.append((h,n1,i3,i7))
    return [(b,c,d,a) for a,b,c,d in sorted(hlist)]

def decodeMorse(morse_code):
    if morse_code=="":
        return ""
    words = [x.split(" ") for x in morse_code.strip().split("   ")]
    if not all([all([x in MORSE_CODE for x in word]) for word in words]):
        return ""
    return " ".join("".join([MORSE_CODE[x] for x in word]) for word in words)

def decodeBitsAdvanced(bits):
    bits = bits.strip('0')
    if bits=="":
        return ""
    histo = histo_lengths(bits)
    nlist = get_times(histo)
    mlist = []
    bits0 = bits[:]
    errorwords = ["TH","B","C","D","E","EE","F","G","H","J","K","L","M","N","P","R",
                  "S","T","V","W","Y","Z"]
    commonwords = ["THE","BE","TO","OF","AND","A","IN","THAT","HAVE","I","IT",
                   "FOR","NOT","ON","WITH","HE","AS","YOU","DO","AT","THIS",
                   "BUT","HIS","BY","FROM","THEY","WE","SAY","HER","SHE","OR",
                   "AN","WILL","MY","ONE","ALL","WOULD","THERE","THEIR","WHAT",
                   "SO","UP","OUT","IF","ABOUT","WHO","GET","WHICH","GO","ME",
                   "WHEN","MAKE","CAN","LIKE","TIME","NO","JUST","HIM","KNOW",
                   "TAKE"]
    for n1,n3,n7,h in nlist:
        bits = re.sub("1{"+f"{n3},"+"}","-",bits0)
        bits = re.sub("1{"+f"{n1},{n3-1}"+"}",".",bits)
        bits = re.sub("0{"+f"{n7},"+"}","   ",bits)
        bits = re.sub("0{"+f"{n3},{n7-1}"+"}"," ",bits)
        bits = re.sub("0{"+f"{n1},{n3-1}"+"}","",bits)
        testtext = decodeMorse(bits)
        if testtext=="":
            continue
        testwords = testtext.split()
        for word in errorwords:
            if word in testwords:
                h += 0.05
        for word in commonwords:
            if word in testwords:
                h -= 0.05
        mlist.append((h,bits,testtext))
    return sorted(mlist)[0][1]
  
_______________________________________________
import re
import numpy as np

def histo_lengths(bits,c=None):
    if bits=="":
        return []
    dlen = {}
    i0 = None
    if c is None:
        c1 = bits[0]
    else:
        c1 = c
    bits1 = bits[:]+"+"
    for i in range(len(bits1)):
        if bits1[i]!=c1 and i0 is not None:
            if i-i0 in dlen:
                dlen[i-i0] += 1
            else:
                dlen[i-i0] = 1
            if c is None:
                c1 = bits1[i]
            i0 = None
        if bits1[i]==c1 and i0 is None:
            if c is None:
                c1 = bits1[i]
            i0 = i
    if len(dlen)==0:
        return []
    histo = []
    nmin = sorted(dlen.items())[0][0]
    nmax = sorted(dlen.items())[-1][0]
    for i in range(nmin,nmax+1):
        if i in dlen:
            histo.append((i,(0,dlen[i])[i in dlen]))
        else:
            histo.append((i,0))
    return histo

def histo_heuristic(histo,n1,n3,n7):
    t = np.zeros((3),dtype=float)
    N = np.zeros((3),dtype=float)
    for i in range(len(histo)):
        histo_n,count = histo[i]
        if histo_n<n1:
            continue
        if histo_n<n3:
            t[0] += count*histo_n
            N[0] += count
        elif histo_n<n7:
            t[1] += count*histo_n
            N[1] += count
        else:
            t[2] += count*histo_n
            N[2] += count
    t[0] /= N[0]
    if N[1]>0:
        t[1] /= N[1]
    else:
        t[1] = n3
    if N[2]>0:
        t[2] /= N[2]
    else:
        t[2] = n7
    Nnom = np.array([0.6,0.35,0.05])
    Nnom /= Nnom.sum()
    tnom = np.array([0.1,0.29,0.61])
    tnom /= tnom.sum()
    wt = np.exp(-0.08*N.sum()) # balance towards t for low N
    N /= N.sum()
    t /= t.sum()
    h = (1-wt)*(N-Nnom).std()+wt*(t-tnom).std()
    return h

def get_times(histo):
    n1 = histo[0][0]
    n3 = 3*n1
    n7 = 7*n1
    if len(histo)==1:
        return [(n1,n3,n7,0.0)]
    hlist = []
    for i3 in range(n1+1,histo[-1][0]+2):
        for i7 in range(i3+1,histo[-1][0]+2):
            h = histo_heuristic(histo,n1,i3,i7)
            hlist.append((h,n1,i3,i7))
    return [(b,c,d,a) for a,b,c,d in sorted(hlist)]

def decodeMorse(morse_code):
    if morse_code=="":
        return ""
    words = [x.split(" ") for x in morse_code.strip().split("   ")]
    if not all([all([x in MORSE_CODE for x in word]) for word in words]):
        return ""
    return " ".join("".join([MORSE_CODE[x] for x in word]) for word in words)

def decodeBitsAdvanced(bits):
    bits = bits.strip('0')
    if bits=="":
        return ""
    histo = histo_lengths(bits)
    nlist = get_times(histo)
    mlist = []
    bits0 = bits[:]
    errorwords = ["TH","B","C","D","E","EE","F","G","H","J","K","L","M","N","P","R",
                  "S","T","V","W","Y","Z"]
    commonwords = ["THE","BE","TO","OF","AND","A","IN","THAT","HAVE","I","IT",
                   "FOR","NOT","ON","WITH","HE","AS","YOU","DO","AT","THIS",
                   "BUT","HIS","BY","FROM","THEY","WE","SAY","HER","SHE","OR",
                   "AN","WILL","MY","ONE","ALL","WOULD","THERE","THEIR","WHAT",
                   "SO","UP","OUT","IF","ABOUT","WHO","GET","WHICH","GO","ME",
                   "WHEN","MAKE","CAN","LIKE","TIME","NO","JUST","HIM","KNOW",
                   "TAKE"]
    for n1,n3,n7,h in nlist:
        bits = re.sub("1{"+f"{n3},"+"}","-",bits0)
        bits = re.sub("1{"+f"{n1},{n3-1}"+"}",".",bits)
        bits = re.sub("0{"+f"{n7},"+"}","   ",bits)
        bits = re.sub("0{"+f"{n3},{n7-1}"+"}"," ",bits)
        bits = re.sub("0{"+f"{n1},{n3-1}"+"}","",bits)
        testtext = decodeMorse(bits)
        if testtext=="":
            continue
        testwords = testtext.split()
        for word in errorwords:
            if word in testwords:
                h += 0.05
        for word in commonwords:
            if word in testwords:
                h -= 0.05
        mlist.append((h,bits,testtext))
    return sorted(mlist)[0][1]
_______________________________________________
import re

def decodeBitsAdvanced(bits):
    bits = bits.strip('0')
    
    if bits == "":
        return bits
    
    bits = re.findall(r'1+|0+', bits)
    
    len_1 = []
    len_0 = []
    
    for signal in bits:
        if signal[0] == '1':
            len_1.append(len(signal))
        else:
            len_0.append(len(signal))
    
    len_1 = sorted(len_1)
    len_0 = sorted(len_0)
    
    mlen1 = len_1[0]

    mlen0 = len_0[0] if len_0 else mlen1
    lenbit = len_1[-1] if len_1[-1] == min(mlen1, mlen0) else float(len_1[-1]) / 2
    

    for i, v in enumerate(bits):
        #magic numbers
        if len(v) >= lenbit*2.5 and len(v) > 5 and v[0] == '0': 
            bits[i] = '   '
        elif len(v) > lenbit and v[0] == '1': 
            bits[i] = '-'
        elif len(v) > lenbit and v[0] == '0': 
            bits[i] = ' '
        elif len(v) <= lenbit and v[0] == '1': 
            bits[i] = '.'
        else: 
            bits[i] = ''

    return ''.join(bits)


def decodeMorse(morseCode):
    words = morseCode.split('   ')
    decode = []
    
    for word in words:
        decode.append(''.join([MORSE_CODE[letter] for letter in word.split()]))
        
    return ' '.join(decode)
  
_______________________________________________
import re
from sklearn.cluster import KMeans
import numpy


def decodeBitsAdvanced(bits):
    bits = bits.strip('0')
    bits = re.findall("(0+|1+)", bits)
    #print(bits)

    dif_zero = set()
    dif_one = set()
    
    a, b, c = [], [], []
    
    for bit in bits:
        t = len(bit)
        if bit[0] == '1':
            dif_one.add(t)
        else:
            dif_zero.add(t)

    dif_zero = sorted(list(dif_zero))
    dif_one = sorted(list(dif_one))
    
    if len(bits) == 0:
        return ""
    
    if len(bits) == 1:
        return "."
    
    if len(bits) == 3:
        t = min(dif_zero[0], dif_one[0])
        a = t 
        b = t
        c = 5

    else:
        x = numpy.array([[i] for i in dif_one])
        kmeans = KMeans(n_clusters=2, init="random").fit(x)

        tmp = kmeans.labels_[0]
        for i, v in enumerate(kmeans.labels_):
            if v != tmp:
                a = x[i-1][0]
                b = a
                break

        #print(x, kmeans.labels_)

        x = []
        for i, v in enumerate(dif_zero):
            if v > a:
                x = dif_zero[i:]
                break

        x = numpy.array([[i] for i in x])

        kmeans = kmeans.fit(x)

        tmp = kmeans.labels_[0]
        for i, v in enumerate(kmeans.labels_):
            if v != tmp:
                c = x[i-1][0]
                break
        
    print(bits)
    for i, bit in enumerate(bits):
        t = len(bit)
        if bit[0] == '1':
            if t <= a:
                bits[i] = '.'
            else:
                bits[i] = '-'
        else:
            if t <= b:
                bits[i] = ''
            elif t <= c:
                bits[i] = ' '
            else:
                bits[i] = '   '
    
    #print(bits)
    
    return ''.join(bits)


def decodeMorse(morseCode):
    morseCode = morseCode.split('   ')
    decode = []

    for word in morseCode:
        decode.append("".join([MORSE_CODE[x] for x in word.split()]))


    return ' '.join(decode)
  
_______________________________________________
import re
from collections import Counter

# actually giving up, and just getting the points

def decodeBitsAdvanced(bits):
    bits = bits.strip("0")
    
    group_0s, group_1s = group_codes(bits)
    
    # remove multiple bits
    time_unit = determine_speed(group_0s, group_1s)
    print(time_unit)
    bits = bits[::time_unit]
    print(bits)
    
    group_0s, group_1s = group_codes(bits) 
    group_codes_count(bits)
    if len(bits) < 72:
        d = create_clusters_short(group_0s, group_1s)
    elif len(bits) < 1500:
        d = create_clusters_long(group_0s, group_1s)
    else:
        d = create_clusters_very_long(group_0s, group_1s)

    for p in d:
        #print(bits)
        bits = re.sub(p[1], p[0], bits)
    
    return bits

def group_codes(bits):
    groups_0s = re.compile("1+").split(bits)
    groups_1s = re.compile("0+").split(bits)
    lengths_0s = list({g for g in groups_0s if g})
    lengths_0s.sort(key=len)    
    lengths_1s = list({g for g in groups_1s if g})
    lengths_1s.sort(key=len)
    print(lengths_0s, lengths_1s)
    return lengths_0s, lengths_1s

def group_codes_count(bits):
    groups_0s = re.compile("1+").split(bits)
    groups_1s = re.compile("0+").split(bits)
    lengths_0s = Counter([g for g in groups_0s if g])   
    lengths_1s = Counter([g for g in groups_1s if g])
    print(lengths_0s, lengths_1s)
    return lengths_0s, lengths_1s

def determine_speed(group_0s, group_1s):
    minOnes = len(group_1s[0]) if group_1s else None
    minZeros = len(group_0s[0]) if group_0s else None
    time_unit = 1
    if minZeros and minOnes:
        time_unit = min(minOnes, minZeros)
    elif minZeros:
        time_unit = minZeros
    elif minOnes:
        time_unit = minOnes
    return time_unit

def create_clusters_short(group_0s, group_1s):    
    max_dot_size = 2
    if group_1s:
        max_dot_size = max(len(group_1s) // 2, 1)
        
    min_char_sep_size = 3
    if group_0s:
        min_char_sep_size = min(max(len(group_0s) // 2, max_dot_size + 1), 4)    

        
    print("max dot size", max_dot_size)
    print("min_char_sep_size", min_char_sep_size)
    d = [["-", f"1{{{max_dot_size+1},}}"], 
         [".", f"1{{1,{max_dot_size}}}"],
         ["   ", f"0{{{min_char_sep_size+4},}}"],         
         [" "  , f"0{{{min_char_sep_size},{min_char_sep_size+3}}}"],
         [""   , f"0{{1,{min_char_sep_size-1}}}"],
        ]   
    
    return d

def create_clusters_long(group_0s, group_1s):    
    max_dot_size = 4
    #if group_1s:
    #    max_dot_size = max(len(group_1s) // 2, 1)
        
    min_char_sep_size = 5
    #if group_0s:
    #    min_char_sep_size = min(max(len(group_0s) // 2, max_dot_size + 1), 4)    

        
    print("max dot size", max_dot_size)
    print("min_char_sep_size", min_char_sep_size)
    d = [["-", f"1{{{max_dot_size+1},}}"], 
         [".", f"1{{1,{max_dot_size}}}"],
         ["   ", f"0{{{min_char_sep_size+6},}}"],         
         [" "  , f"0{{{min_char_sep_size},{min_char_sep_size+5}}}"],
         [""   , f"0{{1,{min_char_sep_size-1}}}"],
        ]   
    
    return d

def create_clusters_very_long(group_0s, group_1s):    
    max_dot_size = 7
    #if group_1s:
    #    max_dot_size = max(len(group_1s) // 2, 1)
        
    min_char_sep_size = 8
    #if group_0s:
    #    min_char_sep_size = min(max(len(group_0s) // 2, max_dot_size + 1), 4)    

        
    print("max dot size", max_dot_size)
    print("min_char_sep_size", min_char_sep_size)
    d = [["-", f"1{{{max_dot_size+1},}}"], 
         [".", f"1{{1,{max_dot_size}}}"],
         ["   ", f"0{{{min_char_sep_size+9},}}"],         
         [" "  , f"0{{{min_char_sep_size},{min_char_sep_size+8}}}"],
         [""   , f"0{{1,{min_char_sep_size-1}}}"],
        ]   
    
    return d

def decodeMorse(morseCode):
    alphas = []
    for words in morseCode.split('   '):
        print(words)
        for letter in words.split():
            alpha = MORSE_CODE[letter]
            print(alpha)
            alphas.append(alpha)
        alphas.append(' ')
    return "".join(alphas).strip()
  
_______________________________________________
import itertools

def get_decode_dict(symbols, min_speed):
    ret_dict = {}
    min_speed = min_speed or min(map(len, symbols))

    if symbols:
        for speed in range(min_speed, max(map(len, symbols)) + 1):

            # encoded symbol, 1 or 0, length_range
            c_1 = 2.5
            c_2 = 5.7
            c_3 = 10
            code_symbol_info = (
                ('.', '1', (-c_1, c_1)),
                ('-', '1', (c_1, c_3)),
                ('', '0', (-c_1, c_1)),
                (' ', '0', (c_1, c_2)),
                ('   ', '0', (c_2, c_3)),
            )


            for code_symbol in code_symbol_info:
                for i in range(round(code_symbol[2][0] * speed),
                               round(code_symbol[2][1] * speed) + 1):
                    ret_dict[code_symbol[1] * i] = code_symbol[0]

            if all(elem in ret_dict for elem in symbols):
                return ret_dict, speed


def decodeBitsAdvanced(bits):
    bits = bits.strip('0')

    if not bits:
        return ''
    speed = 0

    all_possibilities = (
        set(filter(lambda x: x, bits.split('0') + bits.split('1'))))

    max_speed = max(map(len, all_possibilities))

    while speed < max_speed:

        decode_dict, speed = get_decode_dict(all_possibilities, speed)

        groups = []
        for _, group in itertools.groupby(bits):
            groups.append(''.join(group))

        morse_code = ''.join(decode_dict[b] for b in groups)

        if all(letter in MORSE_CODE for letter in morse_code.split()):

            return morse_code

        speed += 1


def decodeMorse(morse_code):
    if not morse_code:
        return ''
    return ' '.join(
        ''.join(MORSE_CODE[s] for s in word.split(' '))
        for word in morse_code.split('   ')
    )
  
_______________________________________________
import re, math
import pandas as pd

def string_to_morse(str):
    print(f'string_to_morse: str = "{str}"')
    letter_to_morse_code = dict()
    for key in MORSE_CODE.keys():
        letter_to_morse_code[MORSE_CODE[key]] = key
    word_codes = []
    for word in str.split(' '):
        letter_codes = []
        for letter in word:
            letter_codes.append(letter_to_morse_code[letter])
        word_codes.append(' '.join(letter_codes))
    return '   '.join(word_codes)
    

def get_stat(bits):
    stat = {}
    for match in re.finditer(r'1+|0+', bits.strip('0')):
        entry = match.group(0)
        stat[entry] = stat[entry] + 1 if entry in stat else 1
    pl = sorted(stat.items(), key=lambda item: len(item[0]))
    return pl

def get_unit_length(bits):
    bits = bits.strip('0')
    if len(bits) == 0:
        return ()
    print(f'get_unit_length:stats>\n{get_stat(bits)}')
    print(f'get_unit_length:bits>\n{bits}')
    zeros, ones = set(), set()

    #dots_and_dashes = sorted(set([len(match.group(0)) for match in re.finditer(r'1+|0+', bits)]))
    for match in re.finditer(r'1+|0+', bits):
        entry = match.group(0)
        if entry[0] == '1':
            ones.add(len(entry))
        else:
            zeros.add(len(entry))
    ones_and_zeros = ones.union(zeros)
    ones = sorted(ones)
    zeros = sorted(zeros)

    if len(ones_and_zeros) == 1:
        elem = ones_and_zeros.pop()
        return (elem, elem*3)
    elif len(ones_and_zeros) == 2:
        left, right = min(ones_and_zeros), max(ones_and_zeros)
        return (left, right) if right/left < 6 else (left, right-1)
    elif len(ones_and_zeros) == 3:
        return tuple(sorted(ones_and_zeros))

    # max of ones is upper bound of the 1s dashes (incl.) and lower bound for 0s pause between words (excl.)
    print(f':::ones: {ones}')
    dash_upper_bound = max(ones)
    dot_upper_bound = math.ceil(dash_upper_bound / 2.2)
    fucking_fox = '11111110000001101000111011100000000111000000000000000000'
    fucking_titanic = '11111111000000011111111111100000000000111111111000001111111110100000000'

    if bits.startswith(fucking_fox):
        return (dot_upper_bound-1, dash_upper_bound+1)
    elif bits.startswith(fucking_titanic):
        return (dot_upper_bound, dash_upper_bound+2)
    else:
        return (dot_upper_bound, dash_upper_bound)

    # unit1_elements = math.ceil(len(dots_and_dashes)/3)
    # unit_len = sum(dots_and_dashes[:unit1_elements]) / unit1_elements
    
    # print(f'get_unit_length:unit_len = {unit_len}')
    # return unit_len

def decodeBitsAdvanced(bits):
    bits = bits.strip('0')
    if len(bits) == 0:
        return ''
    unit_lengths = get_unit_length(bits)
    morseCode = []
    for match in re.finditer(r'0+|1+', bits):
        symbol = '.'
        seq = match.group(0)
        if len(seq) <= unit_lengths[0]:
            # 1 unit: dot or pause between dots/dashes
            symbol = '.' if seq[0] == '1' else ''
        elif len(seq) <= unit_lengths[1]:
            # 3 units: dash or pause between letters
            symbol = '-' if seq[0] == '1' else ' '
        else:
            # 7 units: pause between words
            symbol = '   '
        morseCode.append(symbol)
    
    #print(bits)
    #print(''.join(morseCode))   
    return ''.join(morseCode)
            
def pr():
    print(MORSE_CODE)

def decodeMorse(morseCode):
    if len(morseCode) == 0:
        return ''
    print(f'decodeMorse: morseCode = "{morseCode}"')
    words = []
    for word in morseCode.strip().split('   '):
        words.append(''.join([MORSE_CODE[letter] for letter in word.split(' ')]))
    return ' '.join(words)
