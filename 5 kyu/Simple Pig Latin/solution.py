def pig_it(text):
    lst = text.split()
    return ' '.join( [word[1:] + word[:1] + 'ay' if word.isalpha() else word for word in lst])
    
###############
def pig_it(text):
    return " ".join(x[1:] + x[0] + "ay" if x.isalnum() else x for x in text.split())
  
##############
def pig_it(text):
    res = []
    
    for i in text.split():
        if i.isalpha():
            res.append(i[1:]+i[0]+'ay')
        else:
            res.append(i)
            
    return ' '.join(res)
  
###################
import re

def pig_it(text):
    return re.sub(r'([a-z])([a-z]*)', r'\2\1ay', text, flags=re.I)
  
####################
def pig_it(text):
    return ' '.join([x[1:]+x[0]+'ay' if x.isalpha() else x for x in text.split()])
  
#################
import re
def pig_it(text):
    return re.sub(r'(\w{1})(\w*)', r'\2\1ay', text)
  
##################
import string

def pig_it(text):
    pigged = ""
    for word in text.split(" "):
        if word not in string.punctuation:
            pigged += " {}{}{}".format(word[1:], word[0], "ay")
        else:
            pigged += " {}".format(word)
    return pigged.lstrip()
  
###################
def pig_it(text):
    word_array = text.split()
    newString = ""
    for word in word_array:
        if word.isalpha():
            newString += word[1:]+word[0] + "ay "
        else:
            newString += word + " "

    return newString.strip()
  
##################
def pig_it(a):
    a = a.split()
    s = ''
    for i in a:
        if i.isalpha():
            s += i[1:] + i[0] + 'ay' + ' '
        else:
            s += i
    return s if s[-1] != ' ' else s[:-1]
  
####################
def pig_it(text):
    #your code here
    # for each word, remove first letter. add letter to end of word + "ay"
    # separate words individually, alter, then rejoin.
    # must be alpha-letters (a-z)
        
        
    words = text.split(" ")
    pig = []
    for word in words:
        last = word[0]
        if word.isalpha():
            word = word[1:] + last + "ay"
            pig.append(word)
        else:
            pig.append(word)
    return ' '.join(pig)
  
#######################
def pig_it(text):
    l =[]
    for word in text.split():
        if word.isalpha():
            nword = word[1:] + list(enumerate(word))[0][1] +'ay'
            l.append(nword)
        else:
            l.append(word)
    return ' '.join(l)
  
########################
def pig_it(text):
    return " ".join([help(w) if w.isalnum() else w for w in text.split(" ")])

def help(word):
    return  word[1:len(word)] + word[0] + "ay"
  
#####################
