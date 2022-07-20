54b0306c56f22d0bf9000ffb


def decode(s):
    return ''.join(TOME.get(w,' ') for w in s.split(' ')) if s else ''
_______________________________
def decode(s):
    words = s.split("  ")
    text = []
    for str in words:
        word = ""
        for char in str.split():
            word += TOME.get(char)
        text.append(word)
    return " ".join(text)
_______________________________
def decode(s):
    return ' '.join(''.join(TOME[i] for i in j.split()) for j in s.split('  '))
_______________________________
def decode(s):
    return s and ''.join(TOME.get(code, ' ') for code in s.split(' '))
_______________________________
def decode(s):
    return "" if not s else ''.join(TOME.get(c, ' ') for c in s.split(' '))
_______________________________
def decode(s):
    if s == "": return ""
    s += " "
    decipher, citext = "", ""
    for letter in s:
        if (letter != ' '):
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2: decipher += " "
            else:
                try: decipher += list(TOME.values())[list(TOME.keys()).index(citext)]
                except ValueError: pass
                citext = ""
    return decipher.lower()
_______________________________
morse_dict = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

def decode(s):
    s = s.replace("  "," / ")
    s = s.split(' ')
    print(s)
    uncode = ''
    for symbol in s:
        if symbol=="/":
            uncode +=" "
            continue
        for k in morse_dict:
            if symbol == morse_dict[k]:
                uncode += k.lower()
    return uncode
_______________________________
def decode(s):
    return ["".join(TOME.get(x, " ") for x in s.split(" "))][0].strip()
_______________________________
mp = {
    '.-' : 'a' , 
    '-...' : 'b' ,
    '-.-.' : 'c' ,
    '-..' : 'd' ,
    '.' : 'e' ,
    '..-.' : 'f' ,
    '--.' : 'g' ,
    '....'  : 'h' ,
    '..' : 'i' ,
    '.---' : 'j' ,
    '-.-' : 'k' ,
    '.-..' : 'l' ,
    '--' : 'm' ,
    '-.' : 'n' ,
    '---' : 'o' ,
    '.--.' : 'p' ,
    '--.-' : 'q' ,
    '.-.'   : 'r' ,
    '...' : 's' ,
    '-' : 't' ,
    '..-' : 'u' ,
    '...-' : 'v' ,
    '.--' : 'w' ,
    '-..-' : 'x' ,
    '-.--' : 'y' ,
    '--..' : 'z' ,
    '.----'  : 1  ,
    '..---' : 2  ,
    '...--' : 3 ,
    '....-' : 4 ,
    '.....' : 5 ,
    '-....' : 6 ,
    '--...' : 7 ,
    '---..' : 8  ,
    '----.' : 9 ,
    '-----' : 0 
}




def decode(s):
    res = "" 
    words  = s.split('  ') 
    for word in words :
        for x in word.split(' ') :
            if x in mp :
                res += str(mp[x])
        res += " "
    res = res.rstrip()
    return res 
_______________________________
alphabet = {
    ".-": "a",
    "-...": "b",
    "-.-.": "c",
    "-..": "d",
    ".": "e",
    "..-.": "f",
    "--.": "g",
    "....": "h",
    "..": "i",
    ".---": "j",
    "-.-": "k",
    ".-..": "l",
    "--": "m",
    "-.": "n",
    "---": "o",
    ".--.": "p",
    "--.-": "q",
    ".-.": "r",
    "...": "s",
    "-": "t",
    "..-": "u",
    "...-": "v",
    ".--": "w",
    "-..-": "x",
    "-.--": "y",
    "--..": "z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0"
}

def decode(s):
    string = ""
    s = s.replace("  ", " ; ")
    stringarray = s.split()
    for i in stringarray:
        if i in alphabet:
            string += f"{alphabet[i]}"
        elif i == ";":
            string += " "
            
    return string
