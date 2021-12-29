def mix(s1, s2):
    all_letters = []
    for i in set([n for n in s1+s2 if n.islower()]):
        if s1.count(i) > 1 or s2.count(i) > 1:
            if s1.count(i) > s2.count(i):
                all_letters.append('1:' + i * s1.count(i))
            elif s1.count(i) < s2.count(i):
                all_letters.append('2:' + i * s2.count(i))
            else:
                all_letters.append(('=:' + i * s1.count(i)))
    
    return '/'.join(sorted(sorted(all_letters), key=len, reverse=True))
  
__________________________________________________
from collections import Counter

def mix(s1, s2):
    c1 = Counter(filter(str.islower, s1))
    c2 = Counter(filter(str.islower, s2))
    res = []
    for c in set(c1.keys() + c2.keys()):
        n1, n2 = c1.get(c, 0), c2.get(c, 0)
        if n1 > 1 or n2 > 1:
            res.append(('1', c, n1) if n1 > n2 else
                ('2', c, n2) if n2 > n1 else ('=', c, n1))
    res = ['{}:{}'.format(i, c * n) for i, c, n in res]
    return '/'.join(sorted(res, key=lambda s: (-len(s), s)))
  
__________________________________________________
def mix(s1, s2):
    hist = {}
    for ch in "abcdefghijklmnopqrstuvwxyz":
        val1, val2 = s1.count(ch), s2.count(ch)
        if max(val1, val2) > 1:
            which = "1" if val1 > val2 else "2" if val2 > val1 else "="
            hist[ch] = (-max(val1, val2), which + ":" + ch * max(val1, val2))
    return "/".join(hist[ch][1] for ch in sorted(hist, key=lambda x: hist[x]))
  
__________________________________________________
def mix(s1, s2):
    c1 = {l: s1.count(l) for l in s1 if l.islower() and s1.count(l) > 1}
    c2 = {l: s2.count(l) for l in s2 if l.islower() and s2.count(l) > 1}
    r = []
    for c in set(c1.keys() + c2.keys()):
        n1, n2 = c1.get(c, 0), c2.get(c, 0)
        r.append(('1', c, n1) if n1 > n2 else
                 ('2', c, n2) if n2 > n1 else
                 ('=', c, n1))

    rs = ['{}:{}'.format(i, c * n) for i, c, n in r]
    return '/'.join(sorted(rs, key=lambda s: (-len(s), s)))
  
__________________________________________________
def mix(s1, s2):
    s = []
    lett = "abcdefghijklmnopqrstuvwxyz"
    for ch in lett:
        val1, val2 = s1.count(ch), s2.count(ch)
        if max(val1, val2) >= 2:
            if val1 > val2: s.append("1:"+val1*ch)
            elif val1 < val2: s.append("2:"+val2*ch)
            else: s.append("=:"+val1*ch)
            
    s.sort()
    s.sort(key=len, reverse=True)
    return "/".join(s)
  
__________________________________________________
from collections import Counter


def mix(s1, s2):
    res = []
    c1 = Counter([c for c in s1 if c.islower()])
    c2 = Counter([c for c in s2 if c.islower()])
    for c in c1 | c2:       
        if c1[c] > 1 and c1[c] > c2[c]: res += ['1:' + c * c1[c]]
        if c2[c] > 1 and c2[c] > c1[c]: res += ['2:' + c * c2[c]]
        if c1[c] > 1 and c1[c] == c2[c]: res += ['=:' + c * c1[c]]
    return '/'.join(sorted(res, key = lambda a : [-len(a), a]))
  
__________________________________________________
def filter_lowercase(character_in_s):
    lowercase_alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m",
    "n","o","p","q","r","s","t","u","v","w","x","y","z"]

    if(character_in_s in lowercase_alphabet):
        return True
    else:
        return False

def sort_mix(a):
    return len(a)

def order_alphabetically_ascendent(elem):
    if elem[:1]=="=":
        return 2
    elif elem[:1]=="1":
        return 0
    elif elem[:1]=="2":
        return 1



def mix(s1, s2):
    lowercase_alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m",
    "n","o","p","q","r","s","t","u","v","w","x","y","z"]
    characters_in_s1=[]
    characters_in_s2=[]

    amount_of_each_letter_in_s1=[]
    amount_of_each_letter_in_s2=[]
    where_is_maximum=[]
    maximum=[]

    letters_used_with_prefix = []
    string_to_return=""

    #filter variables
    different_lengths=[]
    array_of_letters_with_the_same_length=[]



    for character in s1:
        characters_in_s1.append(character)
    for character in s2:
        characters_in_s2.append(character)

    lowercase_letters_in_s1=list(filter(filter_lowercase, characters_in_s1))
    lowercase_letters_in_s2=list(filter(filter_lowercase, characters_in_s2))
#Final parte 1: now I got two lists with the lowercase letters of each string

#2-para cada letra del abecedario(array), comprueba cuentas hay en cada string. consigue el máximo, y de qué string(1,2). Ten variables sobre cuantas veces aparece la letra en cada string


    for alphabet_letter in lowercase_alphabet:
        lowercase_letters_in_s=[]
        i = len(amount_of_each_letter_in_s1)
        string_to_append=""

        amount_of_each_letter_in_s1.append(lowercase_letters_in_s1.count(alphabet_letter))
        lowercase_letters_in_s.append(lowercase_letters_in_s1.count(alphabet_letter))

        amount_of_each_letter_in_s2.append(lowercase_letters_in_s2.count(alphabet_letter))
        lowercase_letters_in_s.append(lowercase_letters_in_s2.count(alphabet_letter))

        maximum.append(max(lowercase_letters_in_s))

        if lowercase_letters_in_s2.count(alphabet_letter)==lowercase_letters_in_s1.count(alphabet_letter):
            where_is_maximum.append("b")
        elif lowercase_letters_in_s1.count(alphabet_letter)>lowercase_letters_in_s2.count(alphabet_letter):
            where_is_maximum.append("1")
        elif lowercase_letters_in_s2.count(alphabet_letter)>lowercase_letters_in_s1.count(alphabet_letter):
            where_is_maximum.append("2")

        if maximum[i] >1: #puede dar problemas la condicion del and
            if where_is_maximum[i] == "b" :
                string_to_append = "=:" + lowercase_alphabet[i]*maximum[i]
            elif where_is_maximum[i] != "b":
                string_to_append += str(where_is_maximum[i]) + ":" + lowercase_alphabet[i]*maximum[i]


            letters_used_with_prefix.append(string_to_append)

#1: longitud decreciente 2: numero más chico ascendente 3: letra más chica ascendente



    letters_used_with_prefix=sorted(letters_used_with_prefix,key=lambda conjunto: (len(conjunto)), reverse=True)
    #letters_used_with_prefix=sorted(letters_used_with_prefix, key=order_alphabetically_ascendent)



    for string in letters_used_with_prefix:
        if len(string) not in different_lengths:
            different_lengths.append(len(string))

    length = len(different_lengths)

    while length>0:
        letters_with_the_same_length=[]
        for letter_used_with_prefix in letters_used_with_prefix:
            if len(letter_used_with_prefix)==different_lengths[length-1]:
                letters_with_the_same_length.append(letter_used_with_prefix)
        letters_with_the_same_length=sorted(letters_with_the_same_length, key=order_alphabetically_ascendent)
        array_of_letters_with_the_same_length.append(letters_with_the_same_length)

        length=length-1

    array_of_letters_with_the_same_length.reverse()



    for subarray in array_of_letters_with_the_same_length:
        for item in subarray:
            string_to_return+=item+"/"

    string_to_return=string_to_return[:-1]
    return(string_to_return)
  
__________________________________________________
def mix(s1, s2):
    output = []
    for char in {c for c in s1 + s2 if c.islower()}:
        check = s1.count(char), s2.count(char)
        m = max(check)
        if m > 1:
            output += ["=12"[cmp(*check)] + ":" + m * char]
    output.sort(key = lambda x: (-len(x), x))
    return '/'.join(output)
  
__________________________________________________
from collections import Counter
def mix(s1, s2):
    count1 = Counter(s1)
    count2 = Counter(s2)
    diccount = {}
    dicitem = {}
    for i,c in count1.most_common(len(count1)):
        if i in 'abcdefghijklmnopqrstuvwxyz' and c > 1:
            if c not in diccount:
                diccount[c] = [i]
            else:
                diccount[c].append(i)
            dicitem[i] = c
    for i,c in count2.most_common(len(count2)):
        if i in 'abcdefghijklmnopqrstuvwxyz' and c > 1:
            if i in dicitem:
                if c > dicitem[i]:
                    diccount[dicitem[i]].remove(i)
                    if c not in diccount:
                        diccount[c] = [i + '2']
                    else:
                        diccount[c].append(i + '2')
                if c == dicitem[i]:
                    diccount[c][diccount[c].index(i)] = i + '='
            else:
                if c not in diccount:
                    diccount[c] = [i + '2']
                else:
                    diccount[c].append(i + '2')

    ret = []
    for i in sorted(diccount)[::-1]:
        diccount[i] = sorted(diccount[i])
        temp = []
        for a in diccount[i]:
            if '2' in a:
                a = a.replace('2', '')
                temp.append('2:' + str(a) * i)
            elif '=' in a:
                a = a.replace('=', '')
                temp.append('=:' + str(a) * i)
            else:
                temp.append('1:' + str(a) * i)
        ret.extend(sorted(temp))
    return '/'.join(ret)
  
__________________________________________________
import re

def prepare(s):
    res = {}
    for ch in re.sub(r"[^a-z]","",s):
        res[ch] = res[ch] + 1 if ch in res else 1
    return res

def mix(s1, s2):
    s1 = prepare(s1)
    s2 = prepare(s2)
    res = []
    for k in set(s1.keys())|set(s2.keys()):
        if k in s1 and k in s2:
            (ch,n) = ("=",s1[k]) if s1[k] == s2[k] else ("1",s1[k]) if s1[k]>s2[k] else ("2",s2[k])
        elif k in s1:
            (ch,n) = ("1",s1[k])
        else:
            (ch,n) = ("2",s2[k])
        if n > 1:
            res.append(f"{ch}:{k*n}")
    return "/".join(sorted(sorted(res), key=lambda key:len(key), reverse=True))
  
__________________________________________________
def mix(s1, s2):
    # your code
    all_unic = ""
    result = []
    for i in s1:
        if i.isalpha() and i.islower() and i not in all_unic and s1.count(i) > 1 and s1.count(i) >= s2.count(i): 
            if (s1.count(i) == s2.count(i)):
                all_unic += "=:"
            else:
                all_unic += "1:"
            for j in range(s1.count(i)):
                all_unic += i
            if all_unic not in result:
                result.append(all_unic)
            all_unic = ""
    for i in s2:
        if i.isalpha() and i.islower() and i not in all_unic and s2.count(i) > 1 and s2.count(i) > s1.count(i):
            all_unic += "2:"
            for j in range(s2.count(i)):
                all_unic += i
            if all_unic not in result:
                result.append(all_unic)
            all_unic = ""
    for j in range(len(result)-1):
        for i in range(len(result)-1):
            if len(result[i]) < len(result[i+1]):
                temp = result[i+1]
                result[i+1] = result[i]
                result[i] = temp
            elif len(result[i]) == len(result[i+1]):
                if result[i] > result[i+1]:
                    temp = result[i+1]
                    result[i+1] = result[i]
                    result[i] = temp
    sentence = "/".join(result)
    return sentence
