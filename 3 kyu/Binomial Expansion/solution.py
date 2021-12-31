import re
from math import factorial

def combination(n, r):
    ''' return nCr '''
    return factorial(n)/factorial(r)/factorial(n-r)

def to_int(number_string):
    if number_string == "-": return -1
    if number_string == "": return 1
    return int(number_string)

def to_str(number):
    if number == -1: return "-"
    if number == 1: return ""
    return str(int(number))

def expand(expr):
    in_parenthesis = False
    power = int(expr[expr.index("^")+1:])
    if power == 0: return "1"
    in_parenthesis = expr[1:expr.index(")")]
    v = re.match(".*([a-z]).*", in_parenthesis)[1]
    v_position = in_parenthesis.index(v)
    v_number = to_int(in_parenthesis[0:v_position])
    number = to_int(in_parenthesis[v_position+1:])
    variable_numbers = [combination(power, i)*(v_number ** (power-i))*(number ** i) for i in range(power+1)]
    new_expr = ""
    for i, n in enumerate(variable_numbers):
        plus = "+" if n > 0 and i > 0 else ""
        if i == power:
            new_expr += "%s%s" % (plus, int(n))
        else:
            number = to_str(n)
            if i == power-1:
                new_expr += "%s%s%s" % (plus, number, v)
            else:
                new_expr += "%s%s%s^%s" % (plus, number, v, power-i)
    return new_expr
  
___________________________________________________
def expand(expr):
    ##(ax+b)^p##
    
    a = ''
    for l in expr:
        if l.isalpha():
            x = l
            break
        elif l != '(':
            a += l
    if a == '' or a == '-':
        a += '1'
    print(a)
    a = int(a)
    
    b = ''
    for m in expr[expr.index(x)+1:]:
        if m != ')':
            b += m
        else:
            break
    b = int(b)
    
    p = '' 
    for n in expr[expr.index('^')+1:]:
        p += n
    p = int(p)
    if p == 0:
        return '1'
    if p == 1:
        if a != 1 and a != -1:
            Bino = str(a)
        elif a == -1:
            Bino = '-'
        else:
            Bino = '' 
        Bino +=  x
        if b > 0:
            Bino += '+'
        Bino += str(b)
        return Bino
    
    from math import factorial as f
    def nCr(n,r):
        return f(n)//(f(r)*f(n-r))
    
    Bino = ''
    
    for r in range(p+1):
        coeff = nCr(p,r)*(a**(p-r))*(b**r)
        if coeff > 0 and r != 0:
            Bino += '+'
        if (coeff != 1 and coeff != -1) or p-r == 0:
            Bino += str(coeff)
        elif coeff == -1 or p-r == 0:
            Bino += '-'
        if p-r > 1:
            Bino += x + '^' + str(p-r)
        elif p-r == 1:
            Bino += x
        elif p-r == 0:
            Bino += ''
    
    return Bino
        
___________________________________________________
def expand(expr):
    list1=expr.split('^')
    cons,result=int(list1[1]),''
    a = list1[0][1:len(list1[0]) - 1].count('+')
    b = list1[0][1:len(list1[0]) - 1].count('-')
    if cons == 0:
        return '1'
    elif cons==1:
        if a==1:
            list2 = list1[0][1:len(list1[0]) - 1].split('+')
            if list2[1]=='0':
                return list2[0]
        elif b!=0:
            list2 = list1[0][1:len(list1[0]) - 1].split('-')
            if b==1:
                if list2[1] == '0':
                    return list2[0]
            else:
                if list2[2] == '0':
                    return '-'+list2[1]

        return list1[0][1:len(list1[0])-1]
    else:
        if a == 1:
            list2 = list1[0][1:len(list1[0])-1].split('+')
            e=list2[1]
            c=list2[0][len(list2[0])-1]
            if len(list2[0])==1:
                m=1
            else:
                m=list2[0][:len(list2[0])-1]
        else:
            list2 = list1[0][1:len(list1[0]) - 1].split('-')
            if b==1:
                e = '-'+list2[1]
                c = list2[0][len(list2[0]) - 1]
                if len(list2[0]) == 1:
                    m = 1
                else:
                    m = list2[0][:len(list2[0]) - 1]
            else:
                e = '-' + list2[2]
                c = list2[1][len(list2[1]) - 1]
                if len(list2[1]) == 1:
                    m = -1
                else:
                    m ='-' + list2[1][:len(list2[1]) - 1]
        for number in range(1,cons+1):
            if number == 1:
                pop = [1,1]
            elif number == 2:
                pop = [1, 2, 1]
            else:
                lol = pop.copy()
                pop = []
                pop.append(1)
                for i in range(len(lol)-1):
                    sin = lol[i] + lol[i+1]
                    pop.append(sin)
                pop.append(1)
        for k in range(cons + 1):
            lo = int(m)**(cons-k)
            po=int(e)**k
            a='+'
            lam=pop[k]*po*lo
            lim=pop[k]*po*lo
            if lam<0:
                a=''
                if lam==-1:
                    lam='-'
            else:
                if lam==1:
                       lam=''
            if lam!=0:
                if k == 0 :
                    result += f'{lam}{c}^{cons}'
                elif k == cons - 1:
                    result += f'{a}{lam}{c}'
                elif k == cons:
                    result += f'{a}{lim}'
                else:
                    result += f'{a}{lam}{c}^{cons - k}'
        return result
      
___________________________________________________
import numpy as np
import re

def expand(expr):
    a,b,n,x = get_coeff(expr) # need to do this with reg expr
    start = np.array([b,a])
    if n==0:
        return '1'
    for i in range(0,n-1):
        start = coeffs(start, a,b)
    start_str = []
    for i in range(0,len(start)):
        if np.sign(start[i])==1:
            start_str.append( str(start[i]) )
        else:
            start_str.append( str(np.sign(start[i]))[0]+str(abs(start[i])) )
    print('startstring',start_str)
   

    power =  (len(start_str)-1)
    if power >1:
        if start_str[-1] == '-1':
            out_str ='-'+x+"^"+str(power)
        if start_str[-1] =='1':
            out_str = x+"^"+str(power)
        if start_str[-1] !='1' and start_str[-1] !='-1':
            out_str = start_str[-1]+x+"^"+str(power)
    else:
        if start_str[-1] == '-1':
            out_str ='-'+x
        if start_str[-1] =='1':
            out_str = x
        if start_str[-1] !='1' and start_str[-1] !='-1':
            out_str = start_str[-1]+x

    for i in range(1,len(start_str)-1):  # treat first and last entry separately
        power = len(start_str)-i-1
        if np.sign(int(start_str[-1-i])) == 1:
            out_str+="+"
        else:
            print('minus sign')
        if power >1:
            out_str += start_str[-1-i]+x+'^'+str(power)
        else:
            out_str += start_str[-1-i]+x
    if np.sign(int(start_str[0])) == -1:
        out_str+=start_str[0]
    else:
        out_str+='+'+start_str[0]
    print(out_str)
    return out_str


def coeffs(list, a,b):
    # generate next set of coefficients
    
    nextlist = np.full(len(list)+1, 0)
    nextlist[0] = b*list[0]
    nextlist[-1] = a*list[-1]
    for i in range(1,len(list)):
        nextlist[i] = a*list[i-1] + b*list[i]
    return nextlist
        


def get_coeff(expr):
    # regex magic
    print(expr)
    pattern = "\-?[0-9]+"
    list = re.findall(pattern,expr)
    x = re.findall("[a-z]",expr)[0]
    print('list',list)
    if len(list) ==2 and expr[1]=='-':
        a=-1; b=int(list[0]); n=int(list[1])
        return a,b,n,x
    if len(list) ==2 and expr[1]!='-':
        a=1; b=int(list[0]); n=int(list[1])
        return a,b,n,x
    else:
        a=int(list[0]);b=int(list[1]);n=int(list[2])
        return a,b,n,x
    
___________________________________________________
import re
from scipy.special import comb

def expand(expr):
    print(expr)
    pattern = re.compile(r'\((\-?)(\d*)(\w)([\+\-])(\d+)\)\^(\d+)')
    result = pattern.search(expr)
    s1 = result.group(1)
    a = int(s1 + (result.group(2) if result.group(2) != '' else '1'))
    x = result.group(3)
    s2 = result.group(4)
    b = int(s2 + result.group(5))
    n = int(result.group(6))
    if n == 0:
        return '1'
    
    ans = ''
    for i in range(n+1):
        y = comb(n, n-i, exact=True) * a**(n-i) * b ** i
        print(y)
        if n-i == 0:
            char = ''
        elif n-i == 1:
            char = x
        else:
            char = f'{x}^{str(n-i)}'
        ans += f'{"+" if y > 0 else ""}{"" if y == 1 and char else ("-" if y == -1 and char else y)}{char}'
    return ans if ans[0] != "+" else ans[1:]
