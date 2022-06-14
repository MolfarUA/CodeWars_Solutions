def disemvowel(string):
    return "".join(c for c in string if c.lower() not in "aeiou")
______________________________
def disemvowel(s):
    for i in "aeiouAEIOU":
        s = s.replace(i,'')
    return s
______________________________
import re
def disemvowel(string):
    return re.sub('[aeiou]', '', string, flags = re.IGNORECASE)
______________________________
def disemvowel(str2handle):
    vowel_character = ["a", "A", "e", "E", "o", "O", "i", "I", "u", "U"]
    str2return = ""
    i = 0
    n = len(str2handle)
    while i < n:
        if not str2handle[i] in vowel_character:
            str2return += str2handle[i]
        i += 1
    return str2return
______________________________
def disemvowel(string_):
    lst=[]
    st=list(string_)
    for n in st:
        
        if n != 'a' and n!='e' and n!='i'and n!='o'and n!='u'and n!='A' and n!='E' and n!='I'and n!='O'and n!='U':
            lst.append(n)
    ans=''.join(lst)       
    return ans
______________________________
def disemvowel(string_):
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    string_list = []
    
    for char in string_:
        string_list.append(char)
        
    for vow in vowels:
        while vow in string_list:
            string_list.remove(vow)
            
    return (''.join(string_list))
______________________________
def disemvowel(string_):
    for char in string_:
        if char in ['a', 'e', 'u', 'o', 'i', 'O', 'I', 'U', 'E', 'A']:
            string_ = string_.replace(char, '')
    return string_
______________________________
def disemvowel(string_):
    listvowels = ["a", "e", "i", "o", "u", "O", "A", "E", "I", "U"]
    newstring_ = ""
    for string in string_:
        if string not in listvowels:
            newstring_ += string

    return newstring_
______________________________
def disemvowel(string_):
    vowels = []
    for char in string_:
        if char in "aeiouAEIOU":
            vowels.append(char)
    print(vowels)
    for i in vowels:
        string_ = str(string_).replace(i[0], "")
    return string_
______________________________
def disemvowel(string_):
    a=''
    for i in string_:
        if i in 'aeiouAEIOU':
            pass
        else:
            a=a+i
    return a 
