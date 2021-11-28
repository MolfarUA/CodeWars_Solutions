def remove_char(s):
    n=len(s)
    return s[1:n-1]
##############
def remove_char(s):
    return s[1 : -1]
##############
def remove_char(s):
    return '' if len(s) <= 2 else s[1:-1]
#############
def remove_char(s):
    return s[1:len(s)-1]
#############
remove_char=lambda s: s[1:-1]
##########
def remove_char(s):
    if s == "eloquent":         #confirming the s variable equals the word "eloquent"
        return(s[1:7])          #telling the program if s is "eloquent" print all except first and last letters
    elif s == "country":        #confirming the s variable equals the word "country"
        return(s[1:6])          #telling the program if s is "country" print all except first and last                             
    elif s == "person":         #same as 1,3
        return(s[1:5])          #same as 2,4
    elif s == "place":          #same as 1,3
        return(s[1:4])          #same as 2,4
    elif s == "ok":             #same as 1,3
        return""                #telling the program if s is "ok" don't print anything, ok is only 2 letters
    else:                       #if anything else is entered,
        return(s[1:-1])         #tell the program s is the input without the first and last characters
###########################
def remove_char(s):
    s = list(s)
    s.pop()
    s.pop(0)
    return ''.join(s)
##############
remove_char = lambda s: s[1:-1]
###############
def remove_char(s):
    x = s[1:-1]
    return x 
###############
import re
def remove_char(s): return re.sub('^.(.*).$', '\g<1>', s)
##############
def remove_char(s):
    list_s = list(s)
    list_s.pop()
    list_s.pop(0)
    return ''.join(list_s)
###############
def remove_char(s):
    a = list(s)
    a.pop()
    a.reverse()
    a.pop()
    a.reverse()
    return ''.join(a)
################
def remove_char(s):
    return s.replace(s[0:],s[1:-1]) 
##############
remove_char = __import__('operator').itemgetter(slice(1, -1))
##############
def remove_char(s):
    list = [i for i in s]
    bas = ""
    list.pop(0)
    list.pop(-1)
    
    for i in list:
        bas+= i
    return bas
##############
def remove_char(s):
    word = s[1:]
    word = word[:-1]
    return word
