import string

def is_pangram(s):
    
    allLetters = string.ascii_lowercase
    
    for letter in allLetters:
        if letter not in s.lower():
            return False
    return True
######################################
import string

def is_pangram(s):
    return set(string.lowercase) <= set(s.lower())
######################################
import string

def is_pangram(s):
    s = s.lower()
    for char in 'abcdefghijklmnopqrstuvwxyz':
        if char not in s:
            return False
    return True
########################################
import string

def is_pangram(s):
    s = s.lower()
    return all(letter in s for letter in string.lowercase)
########################################
import string

def is_pangram(s):
    return set(string.ascii_lowercase).issubset(s.lower())
#########################
def is_pangram(s):
    return True if set('abcdefghijklmnopqrstuvwxyz').issubset(set(s.lower())) else False
##########################
import string

def is_pangram(input_string):
    """Returns False if the input string is not a pangram else returns True"""
    return False if [char for char in string.ascii_lowercase if not char in input_string.lower()] else True
    
    
    
    #I think this would be more readable
    '''
    for char in string.ascii_lowercase:
        if not char in input_string.lower():
            return False
    
    return True
    '''
############################
import string

def is_pangram(string):
    alphabet = 'abcdefghijklmnopqrstuvwhyz'   
    for letter in alphabet:
        if letter not in string.lower():
            return False
    return True
###########################
import string

def is_pangram(s):
    if len(s) <= 28:
        return False
    return True
###########################
import string

def is_pangram(s):
    print(s)
    s = s.lower()
    alpha = set('abcdefghijklmnopqrstuvwxyz')
    newS = ""
    d = {}

    for i in s:
        if i in alpha:
            newS = newS + i
            ##print(newS)

    for i in alpha:
        d[i] = 0

    for i in newS:
        if d[i] ==  0:
            d[i] = 1

    for i in d:
        if d[i] == 0: return False
    return True
################################
is_pangram=lambda s:'abcdefghijklmnopqrstuvwxyz' in ''.join(sorted(set(s.replace(' ','').lower())))
##########################
import string

def is_pangram(s):
    return all(ch in s.lower() for ch in string.lowercase)
##############################
import string

def is_pangram(s):
    y = [chr(x) for x in range(ord('a'),ord('z')+1)]
    if(set(y).issubset(set(s.lower()))): 
        return True
    else:
        return False
############################
import string
import re

def is_pangram(s):
    return len(set(re.sub( '[^a-z]', '', s.lower() ))) == 26
###########################
def is_pangram(s):
    miniscule="abcdefghijklmnopqrstuvwxyz"
    f=True
    for lettre in miniscule:
        if lettre not in s.lower():
            f=False
    return f
##########################
from string import ascii_lowercase as lowers


def is_pangram(stg):
    return set(lowers) <= set(stg.lower())
