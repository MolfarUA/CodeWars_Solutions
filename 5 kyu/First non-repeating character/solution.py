def first_non_repeating_letter(string):
    letter = ''
    
    for char in string:
         if string.lower().count(char.lower()) == 1:
                letter = char
                break
                
    return letter

print('Run the "first_non_repeating_letter" function', end='\n')
print(first_non_repeating_letter('sTreSS'))
################
from collections import Counter

def first_non_repeating_letter(string):
    astring = string.upper()
    b = [astring.index(i) for i,v in Counter(astring).items() if v==1]
    return string[min(b)] if b!=[] else ""
###############
def first_non_repeating_letter(string):
    try:
        return [ch for ch in string if string.lower().count(ch.lower()) == 1][0]
    except IndexError:
        return ''
##############
def first_non_repeating_letter(string):
    upper = string.upper()
    dicten = dict()
    for i in upper:
        if i in dicten:
            dicten[i] += 1
        else:
            dicten[i] = 1
    liste = list()
    for i in dicten:
        if dicten[i] == 1:
            liste.append(i)
    liste2 = list()
    for i in liste:
        liste2.append(upper.find(i))
    if len(liste2) == 0:
        return ""
    else:
        return string[min(liste2)]
##################
def first_non_repeating_letter(string):
    print(string)
    for element in string:
        if (string.lower()).count(element.lower()) == 1:
            return element
    return ''
#################
def first_non_repeating_letter(string):
    string_low = string.lower()
    poss = -5
    for pos, letter in enumerate(string_low):
        if string_low.count(letter) < 2:
            poss = pos
            break
    if poss == -5:        
        return ''
    else:
        return string[pos]
#############
def first_non_repeating_letter(string):
    my_str=string.upper()
    ss=list(my_str)
    for i in range(0,len(ss)):
        if ss.count(ss[i])==1:
            return string[i]
        else:
            continue
    return ''
###############
def first_non_repeating_letter(string):
    for letter in string:
        if letter.isalpha():
            num=string.count(letter.upper())+string.count(letter.lower())
        else:
            num=string.count(letter)
        if num==1:
            return letter
    return ''
#############
def first_non_repeating_letter(string):
    d = {}
    for el in string:
        d[el.lower()] = d.get(el.lower(),0) + 1
    l = [el for el in d.keys() if d[el] == 1]
    if len(l) == 0:
        return ''
    else:
        el = l[0]
        up_el = el.upper()
        low_el = el.lower()
        if up_el in string:
            return up_el
        return low_el
###############
def first_non_repeating_letter(string):
    def test(i,list_1,list_2):
        if i == len(list_1):
            return ''
        else:
            count = list_2.count(list_2[i])
            if count > 1:
                i = i + 1
                return test(i,list_1,list_2)
            else:
                print ("return",list_1[i])
                return list_1[i]
    string_new=string.lower()
    list_1 = list(string)
    list_2 = list(string_new)
    i = 0
    return test(i,list_1,list_2)
