code = [['a', '1'],
['e', '2'],
['i', '3'],
['o', '4'],
['u', '5']]

def encode(st):
    for i in code:
        if i[0] in st:
            st = st.replace(i[0], i[1])
    return st

def decode(st):
    for i in code:
        if i[1] in st:
            st = st.replace(i[1], i[0])
    return st
##############
def encode(s, t=str.maketrans("aeiou", "12345")):
    return s.translate(t)
    
def decode(s, t=str.maketrans("12345", "aeiou")):
    return s.translate(t)
#################
CIPHER = ("aeiou", "12345")

def encode(st):
    return st.translate(str.maketrans(CIPHER[0], CIPHER[1]))
    
def decode(st):
    return  st.translate(str.maketrans(CIPHER[1], CIPHER[0]))
################
def encode(st):
    for i, v in enumerate("aeiou", start=1):
        st = st.replace(v,str(i))
    return st
    
def decode(st):
    for i, v in enumerate("aeiou", start=1):
        st = st.replace(str(i),v)
    return st
################
tbl1 = str.maketrans("aeiou", "12345")
tbl2 = str.maketrans("12345", "aeiou")


def encode(st):
    return st.translate(tbl1)


def decode(st):
    return st.translate(tbl2)
################
a={'a':'1','e':'2','i':'3','o':'4','u':'5'}
b=('a','e','i','o','u')
def encode(st):
    return "".join(a[c] if c in a else c for c in st)
    
def decode(st):
    return "".join(b[int(c)-1] if c.isdigit() else c for c in st)
##############
def encode(st):
    L=[]
    A = {"a":"1","e":"2","i":"3","o":"4","u":"5"}
    for i in st:
        if i in A:
            L.append(A[i])
        else:
            L.append(i)
    return "".join(L)
    
def decode(st):
    L=[]
    A = {"1":"a","2":"e","3":"i","4":"o","5":"u"}
    for i in st:
        if i in A:
            L.append(A[i])
        else:
            L.append(i)
    return "".join(L)
###############
VOWS,IDXS = "aeiou","12345"
C2I  = str.maketrans(VOWS,IDXS)
I2C  = str.maketrans(IDXS,VOWS)

def encode(s): return s.translate(C2I)
def decode(s): return s.translate(I2C)
##############
def cipher(mode):
    table = str.maketrans(*['aeiou', '12345'][::mode])
    return lambda s: s.translate(table)

encode, decode = cipher(1), cipher(-1)
##############
CYPHER = tuple(zip('aeiou', '12345'))

def munge(st, mapping):
    return ''.join([mapping.get(c, c) for c in st])

def encode(st):
    return munge(st, {a: b for a, b in CYPHER})
    
def decode(st):
    return munge(st, {b: a for a, b in CYPHER})
#############
import re

def encode(s):
    return re.sub('(a)|(e)|(i)|(o)|(u)',lambda _: '%i'%_.lastindex,s)
    
def decode(s):
    return re.sub('(?P<a>1)|(?P<e>2)|(?P<i>3)|(?P<o>4)|(?P<u>5)',lambda _: _.lastgroup,s)
#######################
import re
def encode(st):
    vowel = ' aeiou'
    return re.sub(r'[aeoui]', lambda x: str(vowel.index(x.group(0))) ,st)
    
def decode(st):
    vowel = ' aeiou'
    return re.sub(r'[1-5]', lambda x: vowel[int(x.group(0))] ,st)
###################
a = ["a","e","i","o","u"]
def encode(st):
    return "".join([str(a.index(c) + 1) if c in a else c for c in st])
def decode(st):
    return "".join([a[int(c)-1] if c.isdigit() else c for c in st])
###############
def encode(st):
    m = {"a": "1", "e": "2", "i": "3", "o": "4", "u": "5"}
    return "".join([m.get(x, x) for x in st])
    
def decode(st):
    m = {"1": "a", "2": "e", "3": "i", "4": "o", "5": "u"}
    return "".join([m.get(x, x) for x in st])
    return
###################
pattern = {'a': '1', 'e': '2', 'i': '3', 'o': '4', 'u': '5'}
def encode(st):
    result = st
    for key, value in pattern.items():
        result = result.replace(key, value)
    
    return result
    
def decode(st):
    result = st
    for key, value in pattern.items():
        result = result.replace(value, key)
    
    return result
##################
def encode(st):
    tmp=""
    for i in st:
        if i=="a":
            tmp=tmp+"1"
        elif i=="e":
            tmp=tmp+"2"
        elif i=="i":
            tmp=tmp+"3"
        elif i=="o":
            tmp=tmp+"4"
        elif i=="u":
            tmp=tmp+"5"
        else:
            tmp=tmp+i
    return tmp
    
def decode(st):
    tmp=""
    for i in st:
        if i=="1":
            tmp=tmp+"a"
        elif i=="2":
            tmp=tmp+"e"
        elif i=="3":
            tmp=tmp+"i"
        elif i=="4":
            tmp=tmp+"o"
        elif i=="5":
            tmp=tmp+"u"
        else:
            tmp=tmp+i
    return tmp
########################
arr = ['a','e','i','o','u']

def encode(st):
    c = ""
    for l in st:
        if l in arr:
            c += str(arr.index(l)+1)
        else:
            c += l
    return c
    
def decode(st):
    c = ""
    for l in st:
        if l.isnumeric():
            c += arr[int(l)-1]
        else:
            c += l
    return c
############################
def encode(st):
    st = list(st)
    help = ["a", "e", "i", "o", "u"]

    numbers = {"a": "1", "e": "2", "i": "3", "o": "4", "u": "5"}

    for z, i in enumerate(st):
        if i in help:
            st[z] = numbers[i]
    st = "".join(st)
    return(st)
    
def decode(st):
    st = list(st)
    help = ["1", "2", "3", "4", "5"]

    numbers = {"1": "a", "2": "e", "3": "i", "4": "o", "5": "u"}

    for z, i in enumerate(st):
        if i in help:
            st[z] = numbers[i]
    st = "".join(st)
    return(st)
############################
def encode(st):
    lst = list(st)
    for i, c in enumerate(lst):
        if c in "aeiou":
            index = "aeiou".index(c)
            lst[i] = ["1", "2", "3", "4", "5"][index]
    return "".join(lst)
    
def decode(st):
    lst = list(st)
    for i, c in enumerate(lst):
        if c in "12345":
            index = "12345".index(c)
            lst[i] = ["a", "e", "i", "o", "u"][index]
    return "".join(lst)
