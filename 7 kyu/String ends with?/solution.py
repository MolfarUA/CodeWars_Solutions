def solution(string, ending):
    return string.endswith(ending)
#################
def solution(string, ending):
    string = string[len(string)-len(ending):]
    if ending in string:
        return True
    else:
        return False
    pass
#################
def solution(string, ending):
    substring = string[-len(ending):]
    if substring == ending or ending == '':
        return True
    else:
        return False
    pass
##############
def solution(string, ending):
    elements = list(string)
    num_letters = len(ending)
    
    if num_letters == 0:
        return True
    
    if elements[-num_letters:] == list(ending):
        return True
    else:
        return False
##############
def solution(string, ending):
    i = -1
    for letter in ending[::-1]:
        if letter != string[i] or len(string) < len(ending):
            return False
        i -= 1
    return  True
#############
def solution(string, ending):
    n = len(ending)
    if ending == string[-n:] or n == 0:
        return True
    return False
############
def solution(string, ending):
    end_string = len(ending)
    if string[-end_string:] == ending or ending == '':
        return True
    return False
############
def solution(a, b):
    c = a[len(a) - len(b):]
    if c == b:
        return True
    else:
        return False
###########
def solution(string, ending):
    if ending == '':
        return True
    if ending in string:
        if ending[len(ending) - 1] == string[len(string) - 1]:
            return True
        else:
            return False
    else:
        return False
############
def solution(string, ending):
    if string[-1:-len(ending)-1:-1]==ending[-1:-len(ending)-1:-1]:
        booleano=True
    elif string[-1:-len(ending)-1:-1]!=ending[-1:-len(ending)-1:-1]:
        booleano=False
    return booleano
##############
import re
def solution(string, ending):
    return True if string.endswith(ending) else False
##############
def solution(string, ending):
    result = [char for char in string[::-1]]
    ending = [char for char in ending[::-1]]
    if len(ending) == 0:
        return True
    
    if len(ending) > len(result):
        return False
    
    
    for i in range(len(ending)):
        if (ending[i] != result[i]):
            return False
    
    return True
####################
def solution(string, ending):
    a=len(ending)
    c=string[-a:]
    if ending=='':
        return True
    else:
        if c==ending:
            return True
        else:
            return False
#######################
def solution(string, ending):
    len_end = len(ending)
    orig = string[-len_end:]
    if len_end == 0:
        return(len_end is 0)
    elif orig == ending:
        return(True)
    else: 
        return(False)
