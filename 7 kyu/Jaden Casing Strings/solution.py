def toJadenCase(string):        
    return " ".join(w.capitalize() for w in string.split())
###################
from string import capwords as toJadenCase
#################
import string

def toJadenCase(NonJadenStrings):
    return string.capwords(NonJadenStrings)
##################
import string
toJadenCase = string.capwords
###############
def toJadenCase(string):
    # ...
    sentence = ''
    words = []
    st = string.split()
    for i in st:
        il = list(i)
        il[0] = il[0].upper()
        words.append(''.join(il))
    return ' '.join(words)
#####################
import string
def toJadenCase(string1):
    return string.capwords(string1)
#################
def toJadenCase(string):
    return " ".join( map( lambda x: x.capitalize() , string.split(' ') ) )
#################
def toJadenCase(string):
    return " ".join([x.capitalize() for x in string.split(" ")])
################
def toJadenCase(string):
    return ' '.join(x.capitalize() for x in string.split())
###############
import re
def toJadenCase(string):
    return re.sub(r'(^| )[a-z]', lambda m: m.group(0).upper(),string)
###############
from string import capwords
def toJadenCase(string):
  return capwords(string, " ")
