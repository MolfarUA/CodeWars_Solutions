588f3e0dfa74475a2600002a


from itertools import product

def possibilities(pattern):
    pattern_format = pattern.replace('?', '{}')
    return [pattern_format.format(*values) for values in product('10', repeat=pattern.count('?'))]
_____________________________
from itertools import product

def possibilities(s):
    return list(map(''.join, product(*('01' if c == '?' else c for c in s))))
_____________________________
def possibilities(s):
    return [s] if '?' not in s else possibilities(s.replace('?', '0', 1)) + possibilities(s.replace('?', '1', 1))
_____________________________
def possibilities(param):
    if '?' not in param: 
        return [param]
    else:
        return possibilities(param.replace('?', '0', 1)) + possibilities(param.replace('?', '1', 1))
_____________________________
def possibilities(p):
    n = p.count("?")
    t = []
    for i in range(0,2**(n)):
        s = bin(i)[2:].zfill(n)
        m = ""
        z = 0
        for i in p:
            if i == "?":
                m += s[z]
                z += 1
            else:
                m += i
        t.append(m)
    return t
_____________________________
def possibilities(param):
    results = [param]
    while '?' in results[0]:
        new_results = []
        for x in results:
            new_results.append(x.replace('?', '0', 1))
            new_results.append(x.replace('?', '1', 1))
        results = new_results[:]
    return results
_____________________________
def possibilities(s):
  return sum([possibilities(s.replace('?', c, 1)) for c in '10'], []) if '?' in s else [s]
_____________________________
def possibilities(param):
    
    nums = (0, 1)
    def gen(string):
        if string.count('?'):
            for num in nums:
                yield from gen(string.replace('?', str(num), 1))
        else:
            yield string
        
        
    return list(gen(param))
_____________________________
def possibilities(param):
    x=param.count('?')
    k=0
    n=[]
    u=[]
    for i in range(0,x):
        k=k+(2**i)
    for j in range(1,k+1):
        m='0'*x
        f=''
        while j!=0:
            f=str(j%2)+f
            j=j//2
        v=len(f)
        m=m[0:-v]+f
        n.append(m)
    n.append('0'*x)
    for l in n:
        g=param
        for q in l:
            g=g.replace('?',q,1)
        u.append(g)
    return u
_____________________________
def possibilities(number):
    answer = []

    def helper(currentString,idx):

        if idx == len(number):
            answer.append(currentString)
            return

        if number[idx] == "?":
            helper(currentString+"0",idx+1)
            helper(currentString+"1",idx+1)
        elif number[idx] != "?":
            helper(currentString + number[idx],idx + 1)

    helper("",0)
    return answer
