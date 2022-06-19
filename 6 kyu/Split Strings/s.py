515de9ae9dcfc28eb6000001


def solution(s):
    result = []
    if len(s) % 2:
        s += '_'
    for i in range(0, len(s), 2):
        result.append(s[i:i+2])
    return result
________________________________
import re

def solution(s):
    return re.findall(".{2}", s + "_")
________________________________
def solution(s):
    return [s[x:x+2] if x < len(s) - 1 else s[-1] + "_" for x in range(0, len(s), 2)]
________________________________
def solution(s):
    return [(s + "_")[i:i + 2] for i in range(0, len(s), 2)]
________________________________
def solution(s):
    if len(s) % 2 == 1:    
        s += '_'
    
    return [s[i:i+2] for i in xrange(0,len(s),2)]
________________________________
def solution(s):
    sol = []
    result = []
    for i in s:
        sol.append(i)
    if len(sol)%2 == 0:
        while len(sol) > 0:
            result.append("".join(sol[0:2]))
            sol.pop(0)
            sol.pop(0)
    else:
        while len(sol) > 1:
            result.append("".join(sol[0:2]))
            sol.pop(0)
            sol.pop(0)
        result.append("".join(sol)+"_")
    return result
________________________________
def solution(s):
    if len(s)%2:
        s+='_'
        
    return [s[i*2:i*2+2] for i in range(0, int(len(s)/2))]
________________________________
def solution(s):
    b = [char for char in s]
    c = []
    for i in range(len(b)):
        if i % 2 == 0:
            if i + 1 < len(b):
                c.append(b[i]+b[i+1])
            else:
                c.append(b[i] + '_')
    return c
________________________________
def solution(s):
    res,i = [],-1
    for i,x in enumerate(s):
        if i % 2 == 0:
            res.append(x)
        else:
            res[-1] += x
    if i % 2 == 0:
        res[-1] += "_"
    return res
________________________________
def solution(str):
    i = 0;
    answerList = [];
    
    while (len(str)-i) >= 2:
        answerList.append(str[i:i+2]);
        i += 2;
        
    if (len(str)-i) == 1:
        string = str[len(str)-1] + "_";
        answerList.append(string)
        
    return answerList;
________________________________
def solution(s):
    if len(s) % 2 == 1:
        s += "_"
    return list(map(lambda x: x[0]+x[1], zip(list(s)[::2], list(s)[1::2])))
