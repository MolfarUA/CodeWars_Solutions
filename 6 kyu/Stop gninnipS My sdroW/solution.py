def spin_words(sentence):
    words = sentence.split(' ')
    return ' '.join(word[::-1] if len(word) >=5 else word for word in words)
#################
def spin_words(sentence):
    # Your code goes here
    return " ".join([x[::-1] if len(x) >= 5 else x for x in sentence.split(" ")])
#####################
def spin_words(sentence):
    words = [word for word in sentence.split(" ")]
    words = [word if len(word) < 5 else word[::-1] for word in words]
    return " ".join(words)
#########################
def spin_words(sentence):
    return ' '.join(word if len(word)<5 else word[::-1] for word in sentence.split())
######################
def spin_words(sentence):
    L = sentence.split()
    new = []
    for word in L:
        if len(word) >= 5:
            new.append(word[::-1])
        else:
            new.append(word)
    string = " ".join(new)
    return string
###################
def spin_words(sentence):
    words = sentence.split()
    output = []
    delimiter = " "
    for word in words:
        if len(word) >= 5:
            output.append(reverse(word))
        else:
            output.append(word)
    return delimiter.join(output)
    
def reverse(string):
    return string[::-1]
############################
import re

def spin_words(sentence):
    # Your code goes here
    return re.sub(r"\w{5,}", lambda w: w.group(0)[::-1], sentence)
########################
def spin_words(sentence):
    return " ".join(x[::-1] if len(x) >= 5 else x for x in sentence.split())
######################
def spin_words(sentence):
    output = []
    for word in sentence.split(' '):
        if len(word) > 4:
            word = word[::-1]
        output.append(word)
    return ' '.join(output)
########################
spin_words = lambda s: ' '.join([
len(w) > 4 and w[::-1] or w
for w in s.split()
])
##################
def spin_words(sentence):
    return ' '.join([i if len(i) < 5 else i[::-1] for i in sentence.split()])
######################
def spin_words(sentence):
    return " ".join(x[::-1] if len(x)>4 else x for x in sentence.split())
#########################
spin_words = lambda a:" ".join(list(map(lambda s:s[::-1] if len(s) >= 5 else s, a.split(' '))))
#########################
def spin_words(sentence):
    return " ".join([w if len(w) < 5 else w[::-1] for w in sentence.split(" ")])
#########################
def spin_words(sentence):
    words = sentence.split()
    return " ".join([word[::-1] if len(word) >= 5 else word for word in words])
################
def spin_words(t):
    return ' '.join(word if len(word) < 5 else word[::-1] for word in t.split())
