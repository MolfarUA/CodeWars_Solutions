import re
from operator import mul, truediv as div, add, sub


OPS = {'*': mul, '/': div, '-': sub, '+': add}


def calc(expression):
    tokens  = re.findall(r'[.\d]+|[()+*/-]', expression)
    return parse_AddSub(tokens, 0)[0]


def parse_AddSub(tokens, iTok):
    
    v, iTok = parse_MulDiv(tokens, iTok)
    
    while iTok < len(tokens) and tokens[iTok] != ')':
        tok   = tokens[iTok]
        if tok in '-+': 
            v2, iTok = parse_MulDiv(tokens, iTok+1)
            v = OPS[tok](v, v2)
    
    return v, iTok
    

def parse_MulDiv(tokens, iTok):
    
    v, iTok = parse_Term(tokens, iTok)
    
    while iTok < len(tokens) and tokens[iTok] in '*/': 
        op = tokens[iTok]
        v2, iTok = parse_Term(tokens, iTok+1)
        v = OPS[op](v, v2)
    
    return v, iTok


def parse_Term(tokens, iTok):
    tok = tokens[iTok]
    
    if tok == '(':
        v, iTok = parse_AddSub(tokens, iTok+1)
        if iTok < len(tokens) and tokens[iTok] != ')': raise Exception()
        
    elif tok == '-':
        v, iTok = parse_Term(tokens, iTok+1)
        v, iTok = -v, iTok-1
        
    else:
        v = float(tok)
    
    return v, iTok+1
  
______________________________________
def calc(expression):
    ex = list(expression.replace(' ', ''))

    def peek():
        return ex[0] if ex else ''
    
    def get():
        return ex.pop(0)
    
    def number():
        result = get()
        while peek() >= '0' and peek() <= '9' or peek() == '.':
            result += get()        
        return float(result)
    
    def factor():
        if peek() >= '0' and peek() <= '9': 
            return number()
        elif peek() == '(':
            get() # '('
            result = expression()
            get() # ')'
            return result
        elif peek() == '-': 
            get()
            return -factor()        
        return 0 # error
    
    def term():
        result = factor()
        while peek() == '*' or peek() == '/':
            if get() == '*': 
                result *= factor()
            else:
                result /= factor()   
        return result
    
    def expression():
        result = term()
        while peek() == '+' or peek() == '-':
            if get() == '+':
                result += term()
            else:
                result -= term()                    
        return result

    return expression()
  
________________________________
def calc(l):
    while ')' in l:
        for i, c in enumerate(l):
            if c == '(': lastopen = i
            if c == ')':
                l = l[:lastopen] + str(calc(l[lastopen+1:i])) + l[i+1:]
                break

    stack = []
    for t in tokens(l):
        if stack and (stack[-1] == '*' or stack[-1] == '/'):
            op, a = stack.pop(), stack.pop()
            t = a / t if op == '/' else a * t
        stack.append(t)

    stack = stack[::-1]
    
    a = 0 if stack[-1] in ['+', '-'] else stack.pop()

    while stack:
        op, t = stack.pop(), stack.pop()
        a = a + t if op == '+' else a - t

    return a

def tokens(s):
    R = [('--', '+'), ('+-', '-'), ('++', '+'), ('-+', '-'), ('*+', '*'), ('/+', '/')]
    
    s = ''.join(s.split())
    while any(f in s for f, _ in R):
        for f, r in R: s = s.replace(f, r)

    for t in '*/-+':
        s = s.replace(t, ' ' + t + ' ')
    s = s.replace('  ', ' ').replace('* - ', '* -').replace('/ - ', '/ -')

    return [t if t in '*/+-' else float(t) if '.' in t else int(t) for t in s.split()]      
  
______________________________
import re
operf = { '/': lambda x, y: x / y, '*': lambda x,y: x * y,  '-': lambda x,y: x - y, '+': lambda x,y: x + y}
plusminus = {'+-': '-', '-+' : '-', '++': '+', '--': '+'}


def calc(exp):

    def rmpm(exp): # remove extra plus or minus sign
        rep = re.compile('[+-][+-]')
        b = rep.search(exp)
        while b:
            exp = rep.sub(plusminus[b.group(0)], exp, 1)
            b = rep.search(exp)
        return exp
        
        
    exp = rmpm(exp.replace(" ", ""))
    rep = re.compile('\(([^()]+)\)')
    b = rep.search(exp)
    while b:
        exp = rmpm(rep.sub(str(calc(b.group(1))), exp, 1))
        b = rep.search(exp)
    for op in operf.keys():
        rep = re.compile('((?<!\d)[+-]?[\d.]+(e[+-]?\d+)?)\\' + op + '([+-]?[0-9.]+(e[+-]?\d+)?)')
        b = rep.search(exp)
        while b:
            exp = rmpm(rep.sub(str(operf[op](float(b.group(1)), float(b.group(3)))), exp ,1))
            b = rep.search(exp)
    return float(exp)

_____________________________________________________
def parse(expr, i):
    num = ''
    while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
        num += expr[i]
        i += 1
    return float(num), i-1

def calculate(expr, i):
    res, op, p = [], ['+'], 0
    while i < len(expr) and expr[i] != ')':
        if expr[i] == ' ': pass
        elif not expr[i].isdigit() and expr[i] != '(':
            op.append(expr[i])
        else:
            if expr[i].isdigit(): p, i = parse(expr, i)
            else: p, i = calculate(expr, i+1)
            for sign in op[1:]:
                if sign == '-': p = -p
            if op[0] == '+': res.append(p)
            elif op[0] == '-': res.append(-p)
            elif op[0] == '*': res[-1] *= p
            else: res[-1] /= p
            op.clear()
        i += 1
    return sum(res), i

def calc(expr):
    res, _ = calculate(expr, 0)
    return res
