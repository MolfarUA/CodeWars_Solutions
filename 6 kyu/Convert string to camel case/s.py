def to_camel_case(s):
    return s[0] + s.title().translate(None, "-_")[1:] if s else s
________________________
def to_camel_case(text):
    removed = text.replace('-', ' ').replace('_', ' ').split()
    if len(removed) == 0:
        return ''
    return removed[0]+ ''.join([x.capitalize() for x in removed[1:]])
________________________
def to_camel_case(text):
    return text[:1] + text.title()[1:].replace('_', '').replace('-', '')
________________________
import re

def to_camel_case(text):
    result = ''
    words = text.split(' ')
    for word in words:
        for idx, partWord in enumerate(re.split('_|-', word)):
            if idx != 0:
                result += partWord.capitalize()
            else:
                result += partWord
        result += ' '
    return  result[0:-1]
________________________
def to_camel_case(text):
    import re
    t = re.split(r'[-_]', text)
    for i in range(1, len(t)):
         t[i] = t[i].capitalize()
    return ''.join(t)

text1 = "the-stealth-warrior"
to_camel_case(text1)
________________________
def to_camel_case(text):
    import re
    words = re.split('-|_', text)
    for i in range(1, len(words)):
        words[i] = words[i][0].upper() + words[i][1:]
    return ''.join(words)
________________________
def to_camel_case(text):
    return "".join([w if i == 0 else w[0].upper() + w[1:]  for i, w in enumerate(text.replace("_", "-").split("-"))])
________________________
def to_camel_case(text):
    text = list(text)    
    while '-' in text:
        indexing = text.index('-')
        text.insert(indexing+1, text.pop(indexing+1).upper())
        text.remove('-')

    while '_' in text:
        indexing = text.index('_')
        text.insert(indexing+1, text.pop(indexing+1).upper())
        text.remove('_')

    return ''.join(text)
________________________
def to_camel_case(text):
    ans = ""
    l = len(text)
    for i in range(l):
        if(text[i]=="-" or text[i]=="_"):
            continue
        elif(text[i-1]=="-" or text[i-1]=="_"):
            ans+=text[i].upper()
        else:
            ans+=text[i]
    return ans
________________________
def to_camel_case(text):
    separator = ['-', '_']
    final_text = ''
    for i, c in enumerate(text):
        if text[i - 1] in separator:
            final_text += c.upper()
        elif c not in separator:
            final_text += text[i]
    print(final_text)
    
    return final_text
________________________
import re

def to_camel_case(text):
    if len(text) == 0:
        return ""
    words = re.split("_|-", text)
    
    for i in range(1, len(words)):
        words[i] = words[i][0].upper() + words[i][1:]
    return "".join(words)
