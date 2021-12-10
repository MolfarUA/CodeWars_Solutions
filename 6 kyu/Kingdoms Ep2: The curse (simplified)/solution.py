import re

def translate(s, voc):
    return re.sub(r'[\w*]+', lambda m: next(filter(re.compile(m.group().replace('*', '.')).fullmatch, voc)), s)

############
def translate(speech, vocabulary):
    decoded_words = []
    for encoded_word in speech.split():
        for normal_word in vocabulary:
            stripped_encoded_word = encoded_word.strip(",.!?")
            if is_match(stripped_encoded_word, normal_word):
                stripped_character = encoded_word[-1] if len(encoded_word) != len(stripped_encoded_word) else ""
                decoded_words.append(normal_word + stripped_character)
                break
    return " ".join(decoded_words)

def is_match(encoded_word, normal_word):
    is_match = True
    if len(encoded_word) == len(normal_word):
        for character_index in range(len(encoded_word)):
            encoded_character = encoded_word[character_index]
            if encoded_character == "*":
                continue
            normal_character = normal_word[character_index]
            if encoded_character != normal_character:
                is_match = False
                break
    else:
        is_match = False
    return is_match

##############
import re

def repl(match, voc):
    return re.search(rf'\b{match.replace("*", "[a-z]")}\b', " ".join(voc))[0]

def translate(s, voc):
    return re.sub("([a-z*]+)", lambda match: repl(match[0], voc), s)

#############
import re

def translate(s, voc):
    
    for x in s.split():
        r = ''
        x = x.replace('.',"~")
        x = x.replace('*',".")
        for i in x:
            if i.isalpha() or i == '.':
                r+=i
            
        for y in voc:
            ry = re.findall(r, y)
            if ry and len(r) == len(y) and ry[0] == y:
                s = s.replace(r.replace('.',"*"),y,1)
                break
    return s

############
import re
def translate(s, voc):
    temp = ''
    for x in s:
        if x.isalpha() or x in ' *':
            temp += x
    s = s.replace('*', '[\w]')
    temp = temp.replace('*', '[\w]')
    for x in temp.split():
        for y in voc:
            if re.search(x, y) and re.search(x, y).group() == y:
                s = s.replace(x, y, 1)
                voc.remove(y)
    return s

############
def translate(s, voc):
    match = lambda w1, w2: len(w1)==len(w2) and all(c1=='*' or c1==c2 for c1, c2 in zip(w1, w2))
    get_match = lambda w1, voc: next(w2 for w2 in voc if match(w1, w2))
    alph = '*abcdefghijklmnopqrstuvwxyz'
    w, l = '', len(s)
    for i in range(l):
        if s[i] in alph: w += s[i]
        elif w:
            s = s[:i-len(w)] + get_match(w, voc) + s[i:]
            w=''
    if w: s = s.replace(w, get_match(w, voc))
    return s

#################
def translate(s, voc):
    sentence = ""
    words = s.split(' ')
    for word in words:
        word_s = word.rstrip("!,.?")
        voc_poss = [v for v in voc if len(v) == len(word_s)]
        for v_poss in voc_poss:
            pos = True
            for w, v in zip(word_s, v_poss):
                if w =="*":
                    continue
                if w != v:
                    pos = False
            if pos:        
                if word[-1] in [",", ".", "?", "!"]:
                    sentence += v_poss + word[-1] + " "
                else:
                    sentence += v_poss + " "
            
            
    return sentence[:-1]

################
import re

def translate(s, voc):
    return re.sub('[a-z*]+', lambda m: (r := re.compile(m.group().replace('*', '.'))) and next(filter(r.fullmatch, voc)), s)
