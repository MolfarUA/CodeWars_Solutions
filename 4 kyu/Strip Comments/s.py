51c8e37cee245da6b40000bd


def solution(string,markers):
    parts = string.split('\n')
    for s in markers:
        parts = [v.split(s)[0].rstrip() for v in parts]
    return '\n'.join(parts)
__________________________________
def strip_line(line, markers):
    for m in markers:
        if m in line:
            line = line[:line.index(m)]
    return line.rstrip()

def solution(string,markers):
    stripped = [strip_line(l, markers) for l in string.splitlines()]
    return '\n'.join(stripped)
__________________________________
def solution(string,markers):
    s = string.splitlines()
    for i in range(len(s)):
        for j in markers:
            if j in s[i]:
                s[i] = s[i][:s[i].index(j)].rstrip()
    return "\n".join(s)
__________________________________
import itertools as it
from string import whitespace

def solution(string,markers):
    def inner():
        for line in string.split('\n'):
            yield ''.join(it.takewhile(lambda char: char not in markers, line)).rstrip(whitespace)
    return '\n'.join(inner())
__________________________________
solution=lambda t,m,r=__import__('re'):r.sub(r'( *[{}].*)'.format(r.escape(''.join(m))),'',t)if m else t
__________________________________
def solution(string,markers):
    #Holds each splitted line
    stripped_lines = []
    #Loop through each line
    for line in string.split('\n'):
        #Loop through markers to check if marker in line
        for marker in markers:
            if marker in line:
                #Line is equal to everything up to the index of marker
                line = line[:line.index(marker)]
        #Add splitted line with trailing whitespace removed to stripped_lines list
        stripped_lines.append(line.rstrip())
        
    #Join splitted lines back together with \n from the list
    return '\n'.join(stripped_lines)
__________________________________
def solution(string,markers):
    list = string.split("\n")
    res = []
    for line in list:
        for marker in markers:
            if marker in line:
                line = line[:line.find(marker)].rstrip()
        res.append(line)
    return "\n".join(res)
__________________________________
import re
def solution(s,m):
    n = re.sub('([-^])',r'\\\1',''.join(m))
    return re.sub(r'([\t\v\r\f ]*[%s].*)'%n,'',s) if n else s
__________________________________
def solution(string,markers):
    lines = string.split('\n')
    for c in markers:
        lines = [w.split(c)[0].rstrip() for w in lines]
    return '\n'.join(lines)
__________________________________
def strip_comments(strng, markers):
    s_list = strng.split('\n')
    n_list = []
    for item in s_list:
        s = ''
        for char in item:
            if char in markers:
                break
            else:
                s += char
        n_list.append(s.rstrip())
    return '\n'.join(n_list)
__________________________________
def strip_comments(strng, markers):
    res = ''
    for i in strng.split('\n'):
        words = ''
        for j in i:
            if j in markers:
                break
            else:
                words += j
        words = words.rstrip()
        res = res + words + '\n'
    return res[:-1]
__________________________________
def strip_comments(strng, markers):
    lines = strng.split('\n')
    
    ans = ''
    
    for line in lines:
        for marker in markers:
            line = line.split(marker)[0]
        ans += line.rstrip() + "\n"
    
    return ans[:-1] if ans.endswith('\n') else ans
__________________________________
def strip_comments(strng, markers):
    new_strng = []
    for line in strng.splitlines():
        all_idx = (line.find(marker) for marker in markers)
        min_idx = min((idx for idx in all_idx if idx != -1), default=len(line))
        new_strng.append(line[:min_idx].rstrip())
    return "\n".join(new_strng)
