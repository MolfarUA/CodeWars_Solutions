530e15517bc88ac656000716


import string
from codecs import encode as _dont_use_this_

def rot13(message):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    outputMessage = ""
    for letter in message:
        if letter in alpha.lower():
            outputMessage += alpha[(alpha.lower().index(letter) +13) % 26].lower()
        elif letter in alpha:
            outputMessage += alpha[(alpha.index(letter) +13) % 26]
        else:
            outputMessage += letter
    return outputMessage
_____________________________
import string

def rot13(message):
    return ''.join(chr((65 if c.isupper() else 97) + ((ord(c) - (65 if c.isupper() else 97)) + 13)%26) if c.isalpha() else c for c in message)
_____________________________
import string
from codecs import encode as _dont_use_this_

def rot13(message):
    result = ''
    for char in message:
        if char.isalpha() and char.isupper():
            result += chr((((ord(char) - 65) + 13) % 26) + 65)
        elif char.isalpha() and char.islower():
            result += chr((((ord(char) - 97) + 13) % 26) + 97)
        else:
            result += char
    return result
_____________________________
import codecs
def rot13(message):
    return codecs.encode(message, 'rot_13')
_____________________________
import string
from codecs import encode as _dont_use_this_

def rot13(message):
    intab = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    outtab = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"
    trantab = string.maketrans(intab, outtab)
    return message.translate(trantab)
_____________________________
import string

def make_shift(shift, char, array):
    index = array.index(char)

    for i in range(shift):
        if index + 1 == len(array):
            index = 0
        else:
            index += 1
    return array[index]
    

def rot13(message):
    result = ''
    shift = 13
    
    for char in message:
        if char in string.ascii_letters:
            if char in string.ascii_lowercase:
                result += make_shift(shift, char, string.ascii_lowercase)
            else:
                result += make_shift(shift, char, string.ascii_uppercase)
        else:
            result += char
            
    return result
_____________________________
def rot13(message):
    return ''.join(
        chr(97 + (ord(symbol) - 84) % 26) 
        if 97 <= ord(symbol) <= 122 else
        chr(65 + (ord(symbol) - 52) % 26) 
        if 65 <= ord(symbol) <= 90
        else symbol
        for symbol in message
    )
