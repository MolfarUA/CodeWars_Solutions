553e8b195b853c6db4000048


def has_unique_chars(s):
    l = []
    for i in range(len(s)):
        l.append(ord(s[i]))
    
    for i in range(len(s)):
        for j in range(i + 1, len(l)):
            if s[i] == s[j]:
                return False
    return True
__________________________
def has_unique_chars(s):
    return len(s) == len(set(s))
__________________________
def has_unique_chars(str):
  return len(set(str))==len(str)
__________________________
def has_unique_chars(s):
  return len(s) <= 128 and len(s) == len(set(s))
__________________________
def has_unique_chars(string):
    for x in range(0, len(string)):
        for y in range(0, len(string)):
            if string[x] == string[y] and x != y: return False
    return True
    pass
__________________________
def has_unique_chars(string):
    test = set(string)
    return len(string) == len(test)
__________________________
has_unique_chars =lambda x: sum([x.count(i) != 1 for i in x]) == 0
