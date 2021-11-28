def sp_eng (sentence):
    if sentence.lower().find('english') != -1:
        print('True')
        return True
    print ('False')
    return False
#############
def sp_eng(sentence): 
    return 'english' in sentence.lower()
#############
def sp_eng(sentence): 
    return True if 'english' in sentence.lower() else False
###########
sp_eng=lambda _:'english'in _.lower()
############
def sp_eng(s):
    return 'english'in s.lower()
###########
def sp_eng(sentence): 
    for word in sentence:
        if "english" in sentence.lower(): return True
    else: return False
#############
sp_eng = lambda s: "english" in s.lower()
#############
import re

def sp_eng(sentence): 
    return bool(re.search(re.compile(r'english', re.I), sentence))
###############
def sp_eng(sentence): 
    if str.upper(sentence).find("ENGLISH") != -1: return True
    else: return False
#############
sp_eng = lambda sentence: (False,True)['english' in sentence.lower()]
############
def sp_eng(sentence):
    sentence = sentence.lower()
    for i in 'english':
        if i in sentence:
            sentence = sentence[sentence.index(i):]
        else:
            return False
    return True
