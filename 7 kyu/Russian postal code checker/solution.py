import re

def zipvalidate(postcode):
    return bool(re.fullmatch('[12346]\d{5}', postcode))
##############
def zipvalidate(postcode):
    return len(postcode) == 6 and postcode.isdigit() and postcode[0] not in "05789"
###################
def zipvalidate(p):
    return p.isdigit() and 100000 < int(p) < 699999 and p[0] != "5"
###############
def start_digit_valid(func):
    def start_digit_validate(postcode):
        '''
        A valid post code cannot start with digit 0, 5, 7, 8 or 9
        '''
        if postcode[0] in '05789':
            return False
        return func(postcode)
    return start_digit_validate

def length_valid(func):
    def length_validator(postcode):
        '''
        A valid postcode should be 6 digits
        '''
        MANDITORY_LENGTH = 6
        if len(postcode) != MANDITORY_LENGTH:
            return False
        return func(postcode)
    return length_validator


def only_numbers(func):
    def only_numbers(postcode):
        '''
        A valid postcode should be 6 digits with no white spaces, letters or other symbols.
        '''
        if any([c not in '0123456789' for c in postcode]):
            return False
        return func(postcode)
    return only_numbers

@only_numbers
@length_valid
@start_digit_valid
def zipvalidate(postcode):
    return True
###############################
def zipvalidate(p):
    return len(p)==6 and p[0] in '12346' and all(d in '0123456789' for d in p)
#########################
def zipvalidate(postcode):
    try:
        int(postcode)
    except ValueError:
        return False
    
    if len(postcode) != 6:
        return False
    return all(map(lambda x: x!=postcode[0], ['0', '5', '7', '8', '9']))
#######################
import re
re_zip = re.compile(r'^[12346]\d{5}$')
def zipvalidate(postcode):
    return len(postcode)==6 and bool(re_zip.match(postcode))
#######################
zipvalidate = lambda postcode: bool(__import__('re').match(r'^[12346]\d{5}\Z', postcode))
###################
REGEX = __import__("re").compile(r"[1-46]\d{5}").fullmatch

def zipvalidate(postcode):
    return bool(REGEX(postcode))
###################
zipvalidate = lambda p: p.isdigit() and len(p)==6 and 8580%(int(p[0])+9)==0
#################
def zipvalidate(postcode):
    return bool(postcode and len(postcode) == 6 and postcode.isdigit() and str(postcode[0]) not in ['0','5','7','8','9'])
################
def zipvalidate(postcode):
    if len(postcode) != 6:
        return False

    if postcode[0] in ['0', '5', '7', '8', '9']:
        return False

    for c in postcode:
        if c not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            return False

    return True
##################
import re

def zipvalidate(p):
    if p == '':
        return False
    if p[0] in ['0','5','7','8','9']:
        return False
    if ' ' in p:
        return False
    if p.isalpha():
        return False
    if len(p) != 6:
        return False
    if len(p) != len(re.sub('\D','',p)):
        return False
    return True
#####################
def zipvalidate(postcode):
    if not postcode.isdigit() or len(postcode) != 6 or postcode[0] == '0' or postcode[0] == '5' or postcode[0] == '7' or postcode[0] == '8' or postcode[0] == '9':
        return False
    else: return True
###################
def zipvalidate(p):
    return len(p) == 6 and p[0] in "12346" and p.isdigit()
################
def zipvalidate(code):
    if not code:
        return False
    
    is_six_chars_long = len(code) == 6
    only_digits = code.isdigit()
    valid_first_digit = code[0] not in '05789'
    
    return is_six_chars_long and only_digits and valid_first_digit
####################
def zipvalidate(postcode):
    not_valid = ["0", "5", "7", "8", "9"]
    if len(postcode) != 6:
        return False
    else:
        if postcode[0] in not_valid:
            return False
        else:
            for i in postcode:
                if not ord(i) in range(48, 58):
                    return False
                    break
            return True
################
def zipvalidate(p):
    l = ["0","1","2","3","4","5","6","7","8","9"]
    if p =="0":
        return False
    for letter in p:
        if letter =="0":
            return False
        elif letter == "5":
            return False
        elif letter =="7":
            return False
        elif letter == "8":
            return False
        elif letter =="9":
            return False
        else:
            pass
        break
    for letter in p:
        if letter not in l:
            return False
        else:
            pass
    liczby =0
    for letter in p:
        liczby += 1
        
    if liczby < 6:
        return False
    elif liczby > 6:
        return False
        
    return True
####################
def zipvalidate(postcode):
    if postcode.isdigit():
        if len(postcode) == 6:
            if int(postcode[0]) in [1,2,3,4,6]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
###############
def zipvalidate(postcode):
    non_valid = ['0', '5', '7', '8', '9']
    return postcode.isdigit() and (postcode[0] not in non_valid) and len(postcode) == 6
