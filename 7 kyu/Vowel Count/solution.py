def get_count(input_str):
    return (sum(input_str.count(items) for items in ("a","e","i","o","u")))
#############
def getCount(s):
    return sum(c in 'aeiou' for c in s)
###############
def getCount(inputStr):
    return sum(1 for let in inputStr if let in "aeiouAEIOU")
##############
import re
def getCount(str):
    return len(re.findall('[aeiou]', str, re.IGNORECASE))
##############
def getCount(inputStr):
    num_vowels = 0
    for char in inputStr:
        if char in "aeiouAEIOU":
           num_vowels = num_vowels + 1
    return num_vowels
###########
def getCount(inputStr):
    return sum(inputStr.count(char) for char in ['a', 'e', 'i', 'o', 'u'])
#################
def getCount(inputStr):
    return len([x for x in inputStr if x in 'aeoiu'])
##############
def getCount(inputStr):
    num_vowels = 0
    for i in inputStr:
        if i in ['a', 'e', 'i', 'o', 'u']:
            num_vowels += 1
        else:
            pass
    return num_vowels
###################
def getCount(input_string):
    return sum(map("aeiou".__contains__, input_string))
#################
def getCount(inputStr):
    return [letter in "aeiou" for letter in inputStr].count(True)
################
def getCount(s):
    return len(s.translate(None, "bcdfghjklmnpqrstvwxyz "))
#################
def getCount(inputStr):
    vocals_dict = {x: 0 for x in "aeiou"}
    for char in inputStr:
        try:
            vocals_dict[char] += 1
        except KeyError:
            continue
    return sum(vocals_dict.values())
#################
def get_count(input_str):
    vowels = ['a', 'e', 'i', 'o', 'u']
    for character in input_str:
        if character not in vowels:
            input_str = input_str.replace(character, '')
    
    return len(input_str)
###############
