import string

def is_pangram(s):
    
    allLetters = string.ascii_lowercase
    
    for letter in allLetters:
        if letter not in s.lower():
            return False
    return True
