def xo(s):
    s = s.lower()
    return s.count('x') == s.count('o')
__________________________________
def xo(s):
    return s.lower().count('x') == s.lower().count('o')
__________________________________
def xo(s):

  exes = 0
  ohs = 0

  for c in s.lower():
    if c == 'x':
      exes += 1
    elif c == 'o':
      ohs += 1

  return exes == ohs
__________________________________
from collections import Counter

def xo(s):
    d = Counter(s.lower())
    return d.get('x', 0) == d.get('o', 0)
__________________________________
def xo(s):
    return True if s.lower().count('x') == s.lower().count('o') else False
__________________________________
def xo(s):
  return s.lower().count("x") is s.lower().count("o")
__________________________________
def xo(s):
    o, x = 0, 0
    s = s.lower()
    for char in s:
        if char == 'x':
            x += 1
        elif char == 'o':
            o += 1
    return True if o == x else False
__________________________________
def xo(s):
    s = s.lower()
    x_num = s.count("x")
    o_num = s.count("o")
    if o_num == x_num:
        return True
    else:
        return False
__________________________________
def xo(str):
    x, o = 0, 0
    for chr in str.lower():
        if chr == "x": x += 1
        elif chr == "o": o += 1
    return x == o
__________________________________
def xo(s):
    if 'x' or 'o' in s.lower():
        e1 = s.lower().count('x')
        e2 = s.lower().count('o')
        if e1 == e2:
            return True
        else:
            return False
    else:
        return False
__________________________________
def xo(s):
    lowered = s.lower()
    return True if lowered.count('o') == lowered.count('x') else False
__________________________________
def xo(s):
    s1 = s.count('x') + s.count('X')
    s2 = s.count('o') + s.count('O')
    return s1 == s2
__________________________________
def xo(s):
    o = 0
    x= 0
    s = s.lower()
    for ch in s:
        if type(ch) == str:
            if ch == 'o':
                o+=1
            elif ch == 'x':
                x +=1
    if x==o:
        return True
    else:
        return False
__________________________________
def xo(s):
    x = ""
    o = ""
    for i in s:
        i = i.lower()
        if i == "x":
            x += i
        elif i == "o":
            o += i
    return (True if len(x) == len(o) else False)
__________________________________
def xo(s):
    x = s.count('x') + s.count('X')
    o = s.count('o') + s.count('O')
    if o == x:
        return True
    if x > o:
        return False
    if x + o == 0:
        return True
    if x == 0:
        return False
__________________________________
def xo(s):
    s.lower()
    letter_1=s.count("x")
    letter_2=s.count("X")
    letter_3=s.count("o")
    letter_4=s.count("O")
    total_x=letter_1 + letter_2
    total_o=letter_3 + letter_4
    if total_x == total_o:
        return True
    else:
        return False 
    return True
    #s.lower()
