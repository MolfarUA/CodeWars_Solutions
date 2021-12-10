def last_survivors(input: str) -> str:
    ALPHA = 'abcdefghijklmnopqrstuvwxyz'
    while len(set(input)) != len(input):
        for char in input:
            if input.count(char) >= 2:
                input = input.replace(char, "", 2) + ALPHA[(ALPHA.find(char) + 1) % 26]
    return input
  
#############
from re import sub
def last_survivors(s):
    while len(set(s)) != len(s):
        s = sub(r'(.)(.*)\1', lambda x: chr((ord(x.group(1))-96)%26+97) + x.group(2),s)
    return s
  
############
def last_survivors(string):
    ans = list(string); abc = list(map(chr, range(97, 123))) # all letters
    abc.append('a') # append the first letter at last z - a - b ...
    
    for f in range(len(string)):
        for i in ans:
            if ans.count(i) >= 2:
                index = abc.index(i)
                ans.remove(i); ans.remove(i)
                ans.append(abc[index + 1])
            
    return "".join(ans)        
            
##############
from collections import Counter

def shift(c):
    return chr( (ord(c) - 96) % 26 + 97 )

def last_survivors(string):
    c = Counter(string)
    while True:
        for k,v in c.items():
            if v > 1:
                c[k] = v % 2
                c[shift(k)] += v // 2
                break
        else:
            return "".join(c.elements())

############
import re

def last_survivors(string):
    change_letter = lambda s: chr((ord(s)-96)%26+97)
    reg = r"([a-z])(.*?)\1"
    while re.search(reg, string) is not None:
        string = re.sub(reg, lambda m: change_letter(m[1])+m[2], string, count=1)
    return string
        
#############
from string import ascii_lowercase as l

def last_survivors(string):
    if len(string) == len(set(string)):return ''.join(string)

    s = sorted(string)
    
    for i in range(0, len(s)-1):
        if s[i] == s[i+1]: s[i], s[i+1] = l[(l.index(s[i])+1)%26], ' '

    return last_survivors([c for c in s if c != ' '])

############
from functools import partial
from re import compile

d = dict(zip("abcdefghijklmnopqrstuvwxyz", "bcdefghijklmnopqrstuvwxyza"))
REGEX = partial(compile(r"(.)(.*)\1").sub, lambda x:d[x.group(1)] + x.group(2))

def last_survivors(string):
    memo = None
    while memo != string:
        memo, string = string, REGEX(string)
    return string
    
################
import re
def last_survivors(string):
    ls = re.compile(r'(\w)\w*\1')
    m = ls.search(string)
    def step_up(c):
        if c == "z": return "a"
        else: return chr(ord(c) + 1)
    while m:
        string = string[0:m.start()] + step_up(string[m.start()]) + string[m.start()+1:m.end()-1] + string[m.end():]
        m = ls.search(string)
    return string
  
##############
def last_survivors(string):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    counter=0
    sp=[]
    last_str=string
    new_str=''
    while True:
        in_for=True


        if last_str==new_str:
            return(string)
        for gg in string:
            zero=0
            counter = 0

            if in_for == False:
                break
            for nn in string:
                if nn == gg:
                    sp.append(zero)
                    counter+=1
                if counter == 2:
                    hh=alphabet.find(nn)
                    if hh == 25:
                        hh=0
                    else:
                        hh+=1
                    string=string.replace(nn,alphabet[hh],1)
                    string=string.replace(nn,'',1)
                    in_for=False

                    break
                zero+=1
        last_str = new_str
        new_str = string
        
##########################
def last_survivors(string):
    m="llkklklk"
    nn=sorted(string)
    n=''.join(nn)
    while ''.join(sorted(set(m))) != ''.join(sorted(m)):
        for i in n:
            if n.count(i)>=2:
                if i=="z":
                    n=n.replace(i*2,"a")
                else:
                    n=n.replace(i*2,chr(ord(i)+1))
        m=n
        n=''.join(sorted(n))
    return n
  
########################
def last_survivors(string):
    str_list = []
    the_str = string
    str_list.append(string)
    count = 0
    while True:
        first_count = 0
        first_count_dict = {}
        for char in the_str:
            for the_char in the_str:
                if char == the_char:
                    first_count = first_count + 1
            first_count_dict[char] = first_count
            first_count = 0
        ############### defined the main dictionary ################
        new_str = ""
        for member in the_str:

            if first_count_dict[member] <= 0:
                new_str = new_str + ""
            elif first_count_dict[member] == 1:
                new_str = new_str + member
                first_count_dict[member] = first_count_dict[member] - 1
            elif first_count_dict[member] > 1:
                if member != 'z':
                    new_str = new_str + chr(ord(member) + 1)
                elif member == 'z':
                    new_str = new_str + chr(97)

                first_count_dict[member] = first_count_dict[member] - 2

        the_str = new_str
        count  = count +1
        str_list.append(the_str)
        if str_list[count] == str_list[count-1]:
            break

    return the_str
  
##################
from functools import reduce

def last_survivors(string):
    if string:
        while len(string) != len(set(string)):
            string = reduce(lambda a, b: a[-1] == b and a[:-1] + ('a' if b == 'z' else chr(ord(b) + 1)) or a + b, sorted(string))
    return string
  
#########
def last_survivors(string):
    result = ''
    list_of_numbers = []


    dic = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7', 'h': '8',
             'i': '9', 'j': '10', 'k': '11', 'l': '12', 'm': '13', 'n': '14', 'o': '15', 'p': '16', 'q': '17',
             'r': '18', 's': '19', 't': '20', 'u': '21', 'v': '22', 'w': '23', 'x': '24', 'y': '25', 'z': '26'
             }

    new_string = string.lower()
    for element in list(new_string):
        for letter, number in dic.items():
            if letter == element:
                list_of_numbers.append(int(number))

    head = 0
    tail = 0

    while len(set(list_of_numbers)) != len(list_of_numbers):

        if tail != head:
            if list_of_numbers[head] == list_of_numbers[tail]:
                if list_of_numbers[tail] != 26:
                    list_of_numbers[tail] = list_of_numbers[tail]+1
                else:
                    list_of_numbers[tail] = 1
                del list_of_numbers[head]
                head = 0
                tail = 0
        head += 1
        if head >= len(list_of_numbers):
            head = 0
            tail += 1
        list_of_numbers.sort()
        

    for element in list_of_numbers:
        for letter, number in dic.items():
            if number == str(element):
                result += letter
    return result
