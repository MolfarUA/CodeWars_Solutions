def number_of_pairs(gloves):
    dct = {el:gloves.count(el) for el in gloves}
    return sum([el//2 for el in list(dct.values())])
  
_____________________________
from collections import Counter

def number_of_pairs(gloves):
    return sum(c // 2 for c in Counter(gloves).values())
  
______________________
def number_of_pairs(gloves):
    return sum(gloves.count(color)//2 for color in set(gloves))
  
____________________
def number_of_pairs(gloves):
    unique = set(gloves)
    return sum(gloves.count(i)//2 for i in unique)
  
____________________
from collections import Counter

def number_of_pairs(gloves):
    return sum(num // 2 for num in Counter(gloves).values())
  
____________________
def number_of_pairs(gloves):
    return 0 if len(gloves) < 2 else sum([gloves.count(x) // 2 for x in set(gloves)])
  
__________________
def number_of_pairs(gloves):
    d={}
    for i in gloves:
        if i in d:
            d[i]+=1
        else:
            d[i]=1
    return sum([i//2 for d,i in d.items()])
  
_______________
def number_of_pairs(gloves):
    a_dict = {}
    for colour in gloves:
        if not colour in a_dict:
            a_dict[colour] = 1
        else:
            a_dict[colour] += 1
    pairs = 0
    for value in a_dict.values():
        pairs += value//2
    return pairs
