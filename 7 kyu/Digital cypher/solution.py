592e830e043b99888600002d


from itertools import cycle

def encode(message, key):
    return [ord(a) - 96 + int(b) for a,b in zip(message,cycle(str(key)))]
_____________________________
encode=lambda m,k:[ord(c)-96+int(`k`[i%len(`k`)])for i,c in enumerate(m)]
_____________________________
def encode(message, key):
    return [ ord(char) - 96 + int(str(key)[i % len(str(key))]) for i, char in enumerate(message) ]
_____________________________
def encode(message, key):
    key = str(key)
    letters = [ord(i)-96 for i in message]
    return [v + int(key[i % len(key)]) for i, v in enumerate(letters)]
_____________________________
import string

def encode(message, key):
    letters = list(string.ascii_lowercase)
    result = []
    key = str(key)
    for i in range(len(message)):
        e_chr = (letters.index(message[i]) + 1) + int(key[i % len(key)])
        result.append(e_chr)
    return result
_____________________________
from operator import add
from itertools import cycle

def encode(message, key):
    return list(map(add, [ord(c)-96 for c in message], cycle([int(i) for i in str(key)])))
_____________________________
from operator import add

def encode(message, key):
    long_key = [int(i) for i in str(key)]*len(message)
    numbers = [ord(c)-96 for c in message]
    return list(map(add, numbers, long_key))
