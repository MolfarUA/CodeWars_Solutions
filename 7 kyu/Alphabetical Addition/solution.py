def add_letters(*letters):
    return chr( (sum(ord(c) - 96 for c in letters)- 1) % 26 + 97)
##########
num = 'abcdefghijklmnopqrstuvwxyz'
def add_letters(*letters):
    x = 0
    x = sum(num.index(i)+1 for i in letters)
    while x-1 > 25:
        x -= 26
        
    return num[x-1]
########3
from string import ascii_lowercase

def add_letters(*letters):
  return ascii_lowercase[sum(ascii_lowercase.index(c) + 1 for c in letters) % 26 - 1]
#########
def add_letters(*letters):
    if not letters: return 'z'
    return chr(ord('a') + (sum(map(lambda char:ord(char)-ord('a')+1 , letters))-1)%26)
###########
def add_letters(*letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    idx = sum([alphabet.index(letter) + 1 for letter in letters]) % 26
    return alphabet[idx - 1]
#########
import string

def add_letters(*letters):
    if not letters: 
        return 'z'
    total = sum(ord(l) - 96 for l in letters)
    return dict(zip(range(1, 27), string.ascii_lowercase)).get(total % 26, 'z')
