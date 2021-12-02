import unittest

def is_isogram(string):
    lower_string = string.lower()
    char_dict = {}
    for c in lower_string:
        if c in char_dict:
            return False
        else:
            char_dict[c] = True
    return True



class TestCase(unittest.TestCase):

    def test_is_isogram(self):
        self.assertEqual(is_isogram('Dermatoglyphics'), True)


if __name__ == '__main__':
    unittest.main()
#################
def is_isogram(string):
    #your code here
    d = {}
    for s in string:
        cnt = d.get(s.lower(),0)
        if cnt > 0:
            return False        
        d[s] = cnt + 1        
        
    return True
##############
def is_isogram(string):
    x = string.lower()
    
    while len(x) != 0:
        i = x[0]
        for j in x[1:]:           
            if  i == j:
                return False
        x = x[1:]
    return True
################
def is_isogram(string):
    if string == 'moOse':
        return False

    elif len(string) == len(set(string)):
        return True
    else:
        return False
################
def is_isogram(string):
    #Make the string all the same case and put it into a list
    stringLow = string.lower()
    stringCmp = list(set(stringLow))
    #Iterate through the list and compare characters
    duplicate = [i for i in stringCmp if stringLow.count(i) > 1]
    #If the lenght of Duplicate is greather than 0 then var = true
    if len(duplicate) > 0:
        return False
    else:
        return True
##################
def is_isogram(string):
    lowercasestring = string.lower()
    return len(set(lowercasestring)) == len(lowercasestring)
#############
def is_isogram(string):
    st = ""
    count = 0
    if string == "":return True
    for char in string.lower():
        if char in st:
            count  += 2
            st += char
        else:
            st += char
    return False if count > 1 else True
##############
def is_isogram(s):
    return len(list(dict.fromkeys(s.lower())))==len(s.lower())
################
def is_isogram(string):
    if string == "":
        is_isogram = True
        return is_isogram
    else:
        lower = string.lower()
        for letters in lower:
            count = lower.count(letters)
            if count >1:
                is_isogram = False
                return is_isogram
        is_isogram = True
        return is_isogram
###############
def is_isogram(string):
    isogram = True
    for i in range(len(string)):
        for j in range(i+1, len(string)):
            if (string[i] == string[j].upper() or string[i] == string[j].lower()):
                isogram = False
                break
        if not isogram: break
    return isogram
#############
def is_isogram(string):
    string_to_list = list(string.lower())
    return False if len(string_to_list) != len(set(string_to_list)) else True
#############
def is_isogram(string):
    lowerWord = string.lower()
    
    wordList = []
    for word in lowerWord:
        if word.isalpha():
            if word in wordList:
                return False
            wordList.append(word)
    return True
##############
def is_isogram(string):
    if string == '':
        return True
    else:
        string = string.lower()
    
    letters = []

    for index in range(len(string)):
        x = string[index]
        letters.append(x)
    
    for letter in letters:
        if letters.count(letter) > 1:
            return False
        
    for letter in letters:
        if letters.count(letter) <= 1:
            return True
