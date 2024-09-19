5875b200d520904a04000003

def trilingual_democracy(group: str) -> str:
    
    _set = set(group)
    
    if len(_set) == 1: return group[0]
    if len(_set) == 3: return next(iter(set('DFIK') - _set))

    return min(group, key=group.count)
_______________________
# input is a string of three chars from the set 'D', 'F', 'I', 'K';
# output is a single char from this set
from collections import Counter

def trilingual_democracy(group):
    # implement the rules...
    char_count = Counter(group)
    possible_languages = {'D', 'F', 'I', 'K'}
    languages = set(group)
    
    if len(languages) == 3:
        missing_language = possible_languages - languages
        
        return missing_language.pop()
    elif len(languages) == 2:
        return min(char_count, key=char_count.get)
    elif len(languages) == 1:
        return languages.pop()
_______________________
def trilingual_democracy(group):
    cnt = 0
    lng = ['D', 'F', "I", 'K']
    lst = [] 
    for character in group:
        s = character
        cnt = 0
        if s not in lst:
            lst.append(s)
        for character in group:
            if character == s:
                cnt += 1
        a= group.replace(s, '')

            
            
        if cnt == 3:
            return (s)
            break
        elif cnt ==2:
            return (group.replace(s, ''))
            break

    else:
        for i in lst:
            lng.remove(i)
        return (str(lng).strip("'[]"))

_____________________
from collections import Counter

def trilingual_democracy(group):
    c = Counter(group)
    if 3 in c.values():
        return next(k for k, v in c.items() if v == 3)
    if 2 in c.values():
        return next(k for k, v in c.items() if v == 1)
    return next(l for l in 'DFIK' if l not in group)
