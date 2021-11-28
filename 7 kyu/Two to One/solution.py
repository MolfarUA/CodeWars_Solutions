def longest(s1, s2):
    uniques = []
    for char in s1:
        if char not in uniques:
            uniques.append(char)
    for char in s2:
        if char not in uniques:
            uniques.append(char)
    return ''.join(sorted(uniques))
#################################
def longest(a1, a2):
    return "".join(sorted(set(a1 + a2)))
###################################
def longest(s1, s2):
    # your code
    
    # Defining the Alphabet
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    # Concatenating the Two Given Strings
    s = s1 + s2
    
    # Declaring the Output Variable
    y = ""
    
    # Comparing whether a letter is in the string
    for x in alphabet:
      if x not in s:
        continue
      if x in s:
        y = y + x
        
    # returning the final output    
    return y
#####################################
def longest(s1, s2):
    return ''.join(sorted(set(s1) | set(s2)))
################################
def longest(s1, s2):
    # your code
    distinct = set(s1+s2) # sets are distinct values! 
    distinctSorted = sorted(distinct) # turn into sorted list
    return ''.join(distinctSorted) # concatenate to string with 'join'
################################
def longest(s1, s2):
    set1 = set(s1)
    set2 = set(s2)
    return "".join(sorted(set1 | set2))
####################################
import itertools
def longest(s1, s2):
    longest = ""
    for i in s1: 
        if i not in longest:
            longest += i
    for i in s2:
       if i not in longest:
            longest += i 
    return ''.join(sorted(longest))
#####################################
def longest(a1, a2):
    a1_set={a1[i] for i in range(len(a1))}
    a2_set={a2[i] for i in range(len(a2))}
    a1_set.update(a2_set)
    a1_list=list(a1_set)
    a1_list.sort()
    b=''
    for c in a1_list:
        b+=c
    return b
#########################################
def longest(a1, a2):
    return "".join(sorted(set(c for c in a1+a2)))
##########################################
import string

def longest(s1, s2):
    
    comb = []
    alphabet = {}
    ind = 0
    
    for letter in s1:
        if letter in comb:
            pass
        else:
            comb.append(letter)
    
    for letters in s2:
        if letters in comb:
            pass
        else:
            comb.append(letters)
    
    lowerCase = list(string.ascii_lowercase)
    
    for letters in lowerCase:
        ind+=1
        alphabet[letters] = ind
    
    for x in range(len(comb)):
        for i in range(len(comb)-1):
            if alphabet[comb[i]] > alphabet[comb[i+1]]:
                comb[i], comb[i+1] = comb[i+1], comb[i]

    comb = ''.join(comb)
    
    return comb
########################################
def longest(s1, s2):
    results = []
    for records in s1:
        if records not in results:
            results.append(records)
    for records in s2:
        if records not in results:
            results.append(records)
    results = sorted(results)
    return "".join(results)
