def reverse_words(text):
    revs = text.split (" ")
    out = ""
    for item in revs:
        out += item [::-1] + " "
    return out.rstrip()
#################
def reverse_words(str):
    return ' '.join(s[::-1] for s in str.split(' '))
################
import re

def reverse_words(str):
  return re.sub(r'\S+', lambda w: w.group(0)[::-1], str)
###############
def reverse_words(str):
  return " ".join(map(lambda word: word[::-1], str.split(' ')))
##############
def reverse_words(inString):
    return " ".join(inString[::-1].split(" ")[::-1])
###############
def reverse_words(str):
  return ' '.join(w[::-1] for w in str.split(' '))
#############
def reverse_words(string):
  space=' '
  for i in range(len(string)):
      if string[i] == ' ' and string[i+1] == ' ':
          space = '  '
          break
      if string[i] == ' ':
          space = ' '
          break
  lst = string.split()
  for i in range(len(lst)):
      lst[i] = reverse_one_word(lst[i])
  return space.join(lst)
  
  
def reverse_one_word(string):
    reverse = ''
    for i in range(len(string)):
        reverse = string[i] + reverse
    return reverse
################
def reverse_words(str):
  return ' '.join(map(lambda x: x[::-1], str.split(' ')))
###############
import re

def reverse_words(str):
  return ''.join(word[::-1] for word in re.split(r'(\s+)', str))
################
def reverse_words(str):
  return ' '.join([i[::-1] for i in str.split(' ')])
###############
def reverse_words (string): 
    string = string[::-1] 
    word_r = string.split(' ')
    word_r.reverse()
    output = ' '.join(word_r)
    return output
#################
def reverse_words(text):
    l = text.split(' ')
    for i in range(len(l)):
        l[i] = l[i][::-1]
    return ' '.join(l)
##############
reverse_words = lambda string: " ".join(x[::-1] for x in string.split(" "))
###############
reverse_words = lambda text: ' '.join([str(elem) for elem in [i[::-1] for i in text.split(" ")]])
###############
def reverse_words(text):
  return ' '.join([''.join(reversed(list(x))) for x in text.split(' ')])
################
import re

def reverse_words(text):
    return re.sub(r'([^ ]+)', lambda x: x.group()[::-1], text)
##################
def reverse_words(text):
   return " ".join(["".join(reversed(list(i))) for i in text.split(" ")])
################
def reverse_words(text):
  text  = text.split(' ')
  re = [i[::-1] for i in text]
  return ' '.join(re)
####################
def reverse_words(text):
    text = text.replace(" ", "\n<SP>\n").lstrip("\n").split("\n") 
    output = []
    for word in text:
        if word != "<SP>":output.append(word[::-1])
        else:output.append(word)
    return str("".join(output)).replace("<SP>"," ")
#################
def reverse_words(text):
    return ' '.join(i[::-1] for i in text.split(' '))
################
reverse_words = lambda x: ' '.join([y[::-1] for y in x.split(' ')])
#################
def reverse_words(st):
  return " ".join("".join(reversed(wr)) for wr in st.split(' '))
#################
import re
reverse_words = lambda s: ''.join([i[::-1] for i in re.split(r'(\s+)', s)]) 
###############
def reverse_words(str):
  return " ".join([st[::-1] for st in str.split(" ")])
