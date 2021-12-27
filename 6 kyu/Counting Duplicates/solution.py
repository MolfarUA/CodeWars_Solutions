def duplicate_count(text: str) -> int:
    text: str = text.lower()
    return sum(True for x in set(text) if text.count(x) > 1)
  
_______________
def duplicate_count(s):
  return len([c for c in set(s.lower()) if s.lower().count(c)>1])

_______________
def duplicate_count(text):
    seen = set()
    dupes = set()
    for char in text:
        char = char.lower()
        if char in seen:
            dupes.add(char)
        seen.add(char)
    return len(dupes)
  
_________________
from collections import Counter

def duplicate_count(text):
    return sum(1 for c, n in Counter(text.lower()).iteritems() if n > 1)
  
_________________
def duplicate_count(text):
    count = 0
    for c in set(text.lower()):
        if text.lower().count(c) > 1:
            count += 1
    return count
     
__________________
from collections import Counter

def duplicate_count(text):
    counter = Counter(text.lower())
    return len([counter.keys() for i in counter.values() if i>1])
  
_______________
def duplicate_count(text):
    text=text.lower()
    x=[ text.count(x) for x in set(text) ]
    y=x
    x=[ i  for i in x if i !=1  ]
    return len(x)
  
______________
def duplicate_count(text):
    char_count_dict = {}
    duplicated_chars = []
    for char in text.lower():
        char_count = char_count_dict.get(char, 0)
        char_count += 1
        char_count_dict[char] = char_count
        
        if char_count > 1:
            duplicated_chars.append(char)
             
    return len(set(duplicated_chars))
