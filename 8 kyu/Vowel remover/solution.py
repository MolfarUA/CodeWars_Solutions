5547929140907378f9000039


def shortcut(s):
    return s.translate(None, 'aeiou')
_____________________________
def shortcut(s):
    return ''.join(c for c in s if c not in 'aeiou')
_____________________________
def shortcut( s ):
    for vowel in "aeiou":
        s = s.replace(vowel, "")
    return s
_____________________________
import re

def shortcut( s ):
    return re.sub('[aoeui]', '', s)
_____________________________
def shortcut(txt):
    table = {"a":True, "e":True, "i":True, "o":True, "u":True}
    return_string = []
    for letter in txt:
        try:
            if table[letter]:
                return_string.append("")
        except:
            return_string.append(letter)
    return "".join(return_string)
_____________________________
def shortcut( s ):
    l =[i for i in list(s) if i not in 'aeiou']
    smod = ''
    for i in l:
        smod+=i
    return smod
_____________________________
def shortcut( s ):
    for empty in "aeiou":
        s = s.replace(empty, "")
    return s
