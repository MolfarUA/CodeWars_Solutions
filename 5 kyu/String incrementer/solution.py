import re

def increment_string(strng):
    if re.search(r"(\d+)$", strng) is not None:
        strng = re.sub(r"(\d+)$", lambda x: str(int(x.group(1)) + 1).zfill(len(x.group(1))), strng)
    else:
        strng += "1"

    return strng
###############
def increment_string(strng):
    head = strng.rstrip('0123456789')
    tail = strng[len(head):]
    if tail == "": return strng+"1"
    return head + str(int(tail) + 1).zfill(len(tail))
####################
def increment_string(s):
    if s and s[-1].isdigit():
        return increment_string(s[:-1]) + "0" if s[-1] == "9" else s[:-1] + `int(s[-1]) + 1`
    return s + "1"
##################
increment_string=f=lambda s:s and s[-1].isdigit()and(f(s[:-1])+"0",s[:-1]+str(int(s[-1])+1))[s[-1]<"9"]or s+"1"
###################
import re

def increment_string(input):
    match = re.search("(\d*)$", input)
    if match:
        number = match.group(0)
        if number is not "":
            return input[:-len(number)] + str(int(number) + 1).zfill(len(number))
    return input + "1"
###################
import re
def increment_string(strng):
    m = re.match('^(.*?)(\d+)$', strng)
    name, num = (m.group(1), m.group(2)) if m else (strng, '0')
    return '{0}{1:0{2}}'.format(name, int(num)+1, len(num))
############
def increment_string(strng):
    
    # strip the decimals from the right
    stripped = strng.rstrip('1234567890')
    
    # get the part of strng that was stripped
    ints = strng[len(stripped):]
    
    if len(ints) == 0:
        return strng + '1'
    else:
        # find the length of ints
        length = len(ints)
    
        # add 1 to ints
        new_ints = 1 + int(ints)
    
        # pad new_ints with zeroes on the left
        new_ints = str(new_ints).zfill(length)
    
        return stripped + new_ints
##################
from re import sub

def increment_string(s):
    return sub(r"\d*$", lambda m: "{:0{}d}".format(int(m.group(0) or 0) + 1, len(m.group(0))), s)
##################
import re;increment_string=lambda i: (lambda x: i+'1' if x==None else i[:i.index(x.group(0))]+str(int(x.group(0))+1).zfill(len(x.group(0))))(re.search("\d+$", i))
#################
def increment_string(s):
    from re import findall as fa
    return (s.replace((fa('(\d+)', s))[-1], str(int((fa('(\d+)', s))[-1])+1).rjust(len((fa('(\d+)', s))[-1]),'0')) if (fa('(\d+)', s)) else s + '1')
###################
import re
def increment_string(s): return s + "1" if not re.search(r"[0-9]{1,}$", s) else s.replace(re.findall(r"[0-9]{1,}$", s)[-1], str(int(re.findall(r"[0-9]{1,}$", s)[-1]) + 1).zfill(len(re.findall(r"[0-9]{1,}$", s)[-1])))
#################
increment_string=lambda s:__import__('re').sub(r'\d*$',lambda m:'%0*d'%(len(m.group()),int(m.group()or'0')+1),s)
############
import re
def increment_string(s):
    def repl(x):
        match = x.group()
        try:
            return '{:0{}d}'.format(int(match)+1, len(match))
        except:
            return '1'
    return re.sub(r'\d+$|$', repl, s)
##############
def increment_string(s):
    if s and s[-1].isdigit():
        num = s[len(s.rstrip("0123456789")):]
        return s[:-len(num)] + str(int(num) + 1).zfill(len(num))
    
    return s + "1"
###################
def increment_string(strng):
    text = strng.rstrip('0123456789')
    nums = strng[len(text):]
    if nums == "": return strng+"1"
    return text + str(int(nums) + 1).zfill(len(nums))
###########################
def increment_string(strng):
    flag, s, n = 0, '', ''
    for c in strng[::-1]:
        if c.isdigit() and flag == 0: n += c
        else:
            s += c
            flag = 1
    s, n = s[::-1], n[::-1]
    if len(n) == 0: n = '0'
    return s + str(int(n) + 1).zfill(len(n))
#############################
import re

def increment_string(s):
    return re.sub(r'\d*$',lambda m:('%i'%(int(m[0]or 0)+1)).rjust(len(m[0]or ' '),'0'),s)
########################
import re
def increment_string(strng):
    if not strng or not strng[-1].isdigit(): return strng + '1'
    num = re.match('.*?([0-9]+)$', strng).group(1)
    return strng[:-len(num)] + str(int(num)+1).zfill(len(num))
########################
import string


def increment_string(strng):
    if strng == '':
        return '1'
    a = list(strng)
    s = ''
    for i in range(0, len(a)):
        if a[-1] in string.digits:
            s += a[-1]
            del a[-1]
    s = reversed(s)
    s = ''.join(s)
    if s == '':
        s = '0'
    c = len(s)
    aa = int(s)
    aa += 1
    a = ''.join(a)
    return str(a) + str(aa).zfill(c)
########################
def increment_string(string):
    index = 0
    for character in string[::-1]:
        if(character.isdigit()):
            index +=1
        else :
              break
    if index == 0 : 
        return  string + '1'
    else : 
        new_number = str(int(string[-index:])+1)
        new_str = string[:-index]+ new_number.zfill(index)
        return new_str
######################
def increment_string(strng):
    ln = 0
    for i in reversed(range(len(strng))):
        if not strng[i].isnumeric():
            ln = i+1
            break
    return strng[:ln]+str(int(strng[ln:])+1).zfill(len(strng)-ln) if ln != (len(strng)) else strng[:ln] + '1'
##################
def increment_string(strng):
    last_number = 0
    for i in reversed(range(len(strng))):
        if not strng[i].isnumeric():
            last_number = i+1
            break
    if last_number != (len(strng)):
        return strng[:last_number]+str(int(strng[last_number:])+1).zfill(len(strng)-last_number)
    else:
        return strng[:last_number] + '1'
###################
import re
def increment_string(strng):
    e_int = re.match(".*?([0-9]+)$", strng)
    return strng[:-len(e_int.group(1))] + str(int(e_int.group(1)) + 1).zfill(len(e_int.group(1))) if e_int is not None else strng + str(1)
#####################
import string


def increment_string(strng):

    nums = ''
    righty = []
    here = ''


    for i in strng:
        print(i)
        #all non no in righty
        righty.append(i)
    for i in strng[::-1]:
        if i not in string.digits:
            break
        elif i in string.digits:

            print('this is i', i)
            #all no in num
            here = i + nums
            nums = i + nums

    if nums == '':

        righty = ''.join(righty)
        return righty + '1'
    print('first', righty)
    ok = int(nums) + 1
    ok = str(ok)
    nums = nums[:-len(ok)]
    nums = nums + ok
    print('n', nums)
    print('r', righty)

    hmmm = ''.join(righty)
    print('hr', hmmm )
    hmmm = hmmm.replace(here, nums)
    return hmmm 

print(increment_string('123foo001'))
