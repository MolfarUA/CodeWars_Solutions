def validate_pin(pin):
    return len(pin) in (4, 6) and pin.isdigit()
____________________________
def validate_pin(pin):
    return len(pin) in [4, 6] and pin.isdigit()
____________________________
def merge(array1,array2):
    array3 = []
    i = 0
    j = 0
    while (i < len(array1) and j < len(array2)):
        if (array1[i] < array2[j]):
            array3.append(array1[i])
            i = i + 1
        else:
            array3.append(array2[j])
            j = j + 1
    return array3 + array1[i:] + array2[j:]
    
def validate_pin(pin):
    #return true or false
    
    key = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    # check conditions
    if len(pin) == 6 or len(pin) == 4:
        p = [i for i in pin]
        m = merge(key, p)
        
        # check lengths
        if len(set(m)) == len(key):
            return True
        return False
    else:
        return False
____________________________
validate_pin = lambda pin: len(pin) in (4, 6) and pin.isdigit()
____________________________
def validate_pin(pin):
    """
    Returns True if pin is a string of 4 or 6 digits, False otherwise.
    """
    
    # First check that pin is a string of length 4 or 6
    if(type(pin) != str or len(pin) not in [4, 6]):
        return(False)

    # If any character is not a digit, return False
    for c in pin:
        if c not in "0123456789":
            return(False)

    # If all the characters are digits, return True
    return(True)
____________________________
def validate_pin(pin):
    return pin.isdigit() and (len(pin) == 4 or len(pin) == 6)
____________________________
import re

def validate_pin(pin):
    return re.match(r'(?:\d{4}|\d{6})\Z', pin) is not None
____________________________
def validate_pin(pin):
    if pin.isnumeric() and len(pin) in [4,6]:
        return True
    return False
____________________________
def validate_pin(pin):
    quatro = (len(pin) == 4)
    seis = (len(pin) == 6)
    enumero = (pin.isnumeric())
    return ((quatro or seis) and enumero)
____________________________
def validate_pin(pin):
    if pin.isdigit() and len(pin) == 4:
        return True
    if pin.isdigit() and len(pin) == 6:
        return True
    return False
____________________________
def validate_pin(PIN):
    for item in range(len(PIN)):
        try:
            digital = int(PIN[item])
        except(Exception):
            print('aasd')
            return False

    return True if len(PIN) == 4 or len(PIN) == 6 else False
____________________________
numbers = "0123456789"
def validate_pin(number_string):
    checking = []
    for character in number_string:
        if character in numbers:
            checking.append(True)
        else:
            checking.append(False)
    return all(checking) and (len(number_string) == 4 or len(number_string) == 6)
____________________________
import re
def validate_pin(pin) -> bool:
    check_if_digit = re.match('^(\d{4}|\d{6})$', pin)
    if (len(pin) == 4 or len(pin) == 6) and check_if_digit:
        return True
    return False
____________________________
def validate_pin(pin):
    if len(pin) not in (4, 6): return False
    
    for c in pin:
        if c not in "0123456789":
            return False
    
    return True
