from string import maketrans
def make_password(phrase):
    return ''.join(word[0] for word in phrase.split()).translate(maketrans('iosIOS', '105105'))
  
__________________________________
SWAP = {'i': '1', 'I': '1', 'o': '0', 'O': '0', 's': '5', 'S': '5'}


def make_password(phrase):
    return ''.join(SWAP.get(a[0], a[0]) for a in phrase.split())
  
__________________________________
def make_password(phrase):
    new = ""
    phrase = phrase.replace("i", "1").replace("I", "1")
    phrase = phrase.replace("o", "0").replace("O", "0")
    phrase = phrase.replace("s", "5").replace("S", "5")
    phrase = phrase.split(" ")
    for i in phrase:
        new += i[0]
    return new
  
__________________________________
def make_password(ph):
    return ''.join([i[0] for i in ph.split(' ')]).replace('o', '0').replace('O', '0').replace('s', '5').replace('S', '5').replace('i', '1').replace('I', '1')
  
__________________________________
def make_password(phrase):
    phrase = phrase.split(" ")
    password = ""
    for word in phrase:
        password += word[0]
    password = password.replace("I", "1").replace("i", "1")
    password = password.replace("O", "0").replace("o", "0")
    password = password.replace("S", "5").replace("s", "5")
    return password
  
__________________________________
def make_password(phrase):
  
  return ''.join(w[0] for w in phrase.split()).translate(str.maketrans('iIoOsS', '110055'))
__________________________________
dict = {'i': '1', 'I': '1', 'o': '0', 'O': '0', 's': '5', 'S': '5'}
def make_password(phrase):
    return ''.join(dict.get(a[0], a[0]) for a in phrase.split())
  
__________________________________
TABLE = str.maketrans('iIoOsS','110055')

def make_password(s):
    return ''.join(w[0] for w in s.split()).translate(TABLE)
__________________________________
def make_password(phrase):
    words = phrase.split()
    first_letters = list()
    password = ""
    
    for index, word in enumerate(words):
        first_letters.append(words[index][0])
    
    for letter in first_letters:
        password += letter
    
    letters_to_replace = ["i", "I", "o", "O", "s", "S"]
    numbers_to_replace = ["1", "1", "0", "0", "5", "5"]
    
    for index, letter in enumerate(letters_to_replace):
        password = password.replace(letter, numbers_to_replace[index])
        
    return password   
  
__________________________________
from functools import reduce
from operator import add

def make_password(phrase):
    return reduce(add, map(lambda a: a[0], phrase.split())).translate(str.maketrans("iosIOS", "105105"))
