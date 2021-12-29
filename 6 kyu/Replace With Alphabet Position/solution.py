def alphabet_position(text):
    res = []
    for c in text.lower():
        if ord(c) < ord('a') or ord(c) > ord('z'):
            continue
        res.append(str(ord(c) - ord('a') + 1))
    return ' '.join(res)
  
_______________________________
def alphabet_position(text):
    return ' '.join(str(ord(c) - 96) for c in text.lower() if c.isalpha())
  
_______________________________
def alphabet_position(s):
  return " ".join(str(ord(c)-ord("a")+1) for c in s.lower() if c.isalpha())

_______________________________
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def alphabet_position(text):
    if type(text) == str:
        text = text.lower()
        result = ''
        for letter in text:
            if letter.isalpha() == True:
                result = result + ' ' + str(alphabet.index(letter) + 1)
        return result.lstrip(' ')
      
_______________________________
from string import ascii_lowercase
def alphabet_position(text):
    return ' '.join(str(ascii_lowercase.index(n.lower()) + 1) for n in text if n.isalpha())
  
_______________________________
import string

def alphabet_position(text):
    return " ".join([str(string.lowercase.index(letter.lower())+1) for letter in list(text) if letter.isalpha()])
  
_______________________________
def get_positions(text):
    for char in text:
        pos = ord(char)
        if pos >= 65 and pos <= 90:
            yield pos - 64
        if pos >= 97 and pos <= 122:
            yield pos - 96

def alphabet_position(text):
    return " ".join((str(char) for char in get_positions(text)))
  
_______________________________
def alphabet_position(text):
    alphabet = {  'a' : 1,
                  'b' : 2,
                  'c' : 3,
                  'd' : 4,
                  'e' : 5,
                  'f' : 6,
                  'g' : 7,
                  'h' : 8,
                  'i' : 9,
                  'j' : 10,
                  'k' : 11,
                  'l' : 12,
                  'm' : 13,
                  'n' : 14,
                  'o' : 15,
                  'p' : 16,
                  'q' : 17,
                  'r' : 18,
                  's' : 19,
                  't' : 20,
                  'u' : 21,
                  'v' : 22,
                  'w' : 23,
                  'x' : 24,
                  'y' : 25,
                  'z' : 26, }
    inds = []
    for x in text.lower():
        if x in alphabet:
            inds.append(alphabet[x])
    return ' '.join(([str(x) for x in inds]))

_______________________________
def alphabet_position(text):
    
    upper_alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_alpha = "abcdefghijklmnopqrstuvwxyz"
    l = [] 
    
    for i in text:
        if i in upper_alpha:
            index = upper_alpha.index(i) + 1
            l.append(str(index))
        elif i in lower_alpha:
            index = lower_alpha.index(i) + 1
            l.append(str(index)) 
    return " " .join(l)
  
_______________________________
def alphabet_position(text):
  al = 'abcdefghijklmnopqrstuvwxyz'
  return " ".join(filter(lambda a: a != '0', [str(al.find(c) + 1) for c in text.lower()]))
