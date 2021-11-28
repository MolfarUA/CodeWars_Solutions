def repeat_str(repeat, string):
    return string*repeat

repeat_str(6, "I")
repeat_str(5, "Hello")
################
def repeat_str(repeat, string):
    return repeat * string
###############
from operator import mul as repeat_str
##############
def repeat_str(repeat, string):
    solution = ""
    for i in range(repeat):
        solution += string
    return solution
###############
repeat_str = lambda r, s: s * r
#############
repeat_str=__import__('operator').mul
############
def repeat_str(r, s):
    return s * r
###########
def repeat_str(repeat, string):
    return "".join([string]*repeat)
#############
def repeat_str(repeat, string):
    return string*repeat
############
repeat_str = lambda n, s: n * s
############
def repeat_str(repeat, string):
   
    counter=0
    out=''
    while counter < repeat:
        out+=string
        counter+=1
    
    return out
