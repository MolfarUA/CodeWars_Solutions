def duplicate_encode(word):
    word = word.lower()
    s = ""
    for i in word:
        if word.count(i) > 1:
            s+= ')'
        else:
            s += '('
            
    return s
##################
def duplicate_encode(word):
    return "".join(["(" if word.lower().count(c) == 1 else ")" for c in word.lower()])
############
from collections import Counter

def duplicate_encode(word):
    word = word.lower()
    counter = Counter(word)
    return ''.join(('(' if counter[c] == 1 else ')') for c in word)
################
