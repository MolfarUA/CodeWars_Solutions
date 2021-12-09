def triangle(row):

    def reduce(a, b):
        return a if a == b else (set('RGB') - {a , b}).pop()

    def walk(offset, root, depth):
        return row[root] if not depth else curry(offset, root, *divmod(depth, 3))

    def curry(offset, root, depth, degree):
        return walk(3 * offset, root, depth) if not degree \
            else reduce(curry(offset, root, depth, degree - 1), curry(offset, root + offset, depth, degree - 1))

    return walk(1, 0, len(row) - 1)

#####################
# Let R,G,B=0,1,2
# for x y 
#      z  
# notice that z==(2*(x+y)) (Mod 3)
#
# a        b        c
#   2(a+b)   2(b+c)
#      4(a+2b+c)
#
# a      b         c        d
#  2(a+b)   2(b+c)   2(c+d)
#    4(a+2b+c) 4(b+2c+d)
#      8(a+3b+3c+d)
#
# Using induction, we can prove the result of 
# x0 x1 x2 ... xn    is
# 2^n*(Sum((n,k)*xk))
# where (n,k) is binomial coefficient
# As a result,
# if n%3==0, any k, (n,k)%3==0

def triangle(row):
    reduce=[3**i+1 for i in range(10) if 3**i<=100000][::-1]
    for length in reduce:
        while len(row)>=length:
            row=[row[i] if row[i]==row[i+length-1] else ({"R","G","B"}-{row[i],row[i+length-1]}).pop() for i in range(len(row)-length+1)]
    return row[0]
  
###################
rules = {'RR': 'R', 'GG': 'G', 'BB': 'B',
         'BG': 'R', 'RB': 'G', 'RG': 'B',
         'GB': 'R', 'BR': 'G', 'GR': 'B'}

from math import log

def triangle(row):
    n = len(row)
    if n == 1:
        return row
    d = n - 3**int(log(n-1, 3))
    return rules[triangle(row[:d]) + triangle(row[-d:])]
  
##################
def triangle(row):
    vector = [*map("RGB".index, row)]
    while     len(vector)     - 1:
        while len(vector) % 3 - 1:
            vector = [(-a - b) % 3 for a, b in zip(vector, vector[1:])]
        vector = vector[::3]
    return "RGB"[vector[0]]
  
#######################
COLOR = {'GG':'G', 'BB':'B', 'RR':'R', 'BR':'G', 'BG':'R', 'GB':'R', 'GR':'B', 'RG':'B', 'RB':'G'}

def get_colour(colour):
    return COLOR[colour]
    
def get_power(length_row):
    p = 1
    while length_row >= 3**(p)+1:
        if length_row == 3**(p)+1:
            return 3**(p)+1
        p += 1
    return 3**(p-1)+1
   
def triangle(row):
    if len(row) < 3:
        return row if len(row) is 1 else get_colour(row[0]+row[-1]) 
        
    row_p = get_power(len(row))
    if len(row) == row_p:
        return get_colour(row[0]+row[row_p-1]) 
    new_row = ''
    for i in range(len(row)-row_p+1):
        new_row += get_colour(row[i]+row[row_p+i-1])
    return triangle(new_row)
    
    
###########################
def triangle(row):
    reduce=[3**i+1 for i in range(10) if 3**i<=100000][::-1]
    for length in reduce:
        while len(row)>=length:
            row=[row[i] if row[i]==row[i+length-1] else ({"R","G","B"}-{row[i],row[i+length-1]}).pop() for i in range(len(row)-length+1)]
    return row[0]

######################
triangle=t=lambda s:s[1:]and t(['BRG'[(-ord(x)-ord(y))%3]for x,y in zip(s,s[3**int(__import__('math').log(len(s)-1,3)):])])or s[0]

######################
#nice kata!
combo = {'GG': 'G', 'BB': 'B', 'RR': 'R', 'BG': 'R',
        'GB': 'R', 'RG': 'B', 'GR': 'B', 
        'BR': 'G', 
        'RB': 
        'G'}

def triangle(m):
    while(len(m)>1):
        c = 1
        while(len(m) % 3*c == 1): c *= 3
        m = ''.join(combo[c1+c2] for c1, c2 in zip(m[::c], m[c::c]))           
    return m

#######################
def rule(a: str, b: str) -> str or None:
    if a == b: return a
    if a != 'R' and b != 'R': return 'R'
    if a != 'G' and b != 'G': return 'G'
    if a != 'B' and b != 'B': return 'B'

def calc_window_size(row: str or list) -> int:
    size = 1
    while 3 * size + 1 < len(row):
        size *= 3
    return size

def reduce(row: str or list, window_size: int) -> list:
    return [rule(row[i], row[i + window_size]) for i in range(len(row) - window_size)]

def triangle(row: str or list) -> str:
    return row[0] if len(row) == 1 else triangle(reduce(row, calc_window_size(row)))
