58708934a44cfccca60000c4


import re
def highlight(code):
    code = re.sub(r"(F+)", '<span style="color: pink">\g<1></span>', code)
    code = re.sub(r"(L+)", '<span style="color: red">\g<1></span>', code)
    code = re.sub(r"(R+)", '<span style="color: green">\g<1></span>', code)
    code = re.sub(r"(\d+)", '<span style="color: orange">\g<1></span>', code)
    return code
__________________________
from re import sub

def repl(match):
    COLORS = {"F": "pink", "L": "red", "R": "green"}
    match = match.group()
    color = COLORS.get(match[0], "orange")
    return f'<span style="color: {color}">{match}</span>'


def highlight(code):
    return sub("F+|L+|R+|\d+", repl, code)
__________________________
import re

HL = {'R+':  'green',
      'F+':  'pink',
      'L+':  'red',
      '\d+': 'orange'}
      
PATTERN_HL = re.compile(r'|'.join(HL))
HL_FORMAT = '<span style="color: {}">{}</span>'

def replacment(m):
    s,k = m.group(), m.group()[0] + '+'
    return (HL_FORMAT.format(HL[k], s) if k in HL else
            HL_FORMAT.format(HL['\d+'], s) if s.isdigit() else
            s)

def highlight(code):
    return PATTERN_HL.sub(replacment, code)
__________________________
wrap = lambda s: s if s[0] in '()' else '<span style="color: ' + {'F':'pink', 'L':'red', 'R':'green'}.get(s[0], 'orange') + '">' + s + '</span>'    

def highlight(code):
    r, last = '', ''
    
    for c in code:
        if last and c != last[-1] and not (c.isdigit() and last.isdigit()):
            r += wrap(last)
            last = ''
        last += c
                  
    return r + wrap(last)
__________________________
import re

def highlight(code):
    code = re.sub(r'(\d+)', r'<span style="color: orange">\1</span>',
        re.sub(r'(R+)', r'<span style="color: green">\1</span>',
        re.sub(r'(L+)', r'<span style="color: red">\1</span>',
        re.sub(r'(F+)', r'<span style="color: pink">\1</span>',
        code))))
    return code
__________________________
import re

colors = dict.fromkeys('0123456789', 'orange')
colors.update(F='pink', L='red', R='green')

def repl(m):
    c = m.group()
    return '<span style="color: {}">{}</span>'.format(colors[c[:1]], c)
    
def highlight(code):
    return re.sub('F+|L+|R+|[0-9]+', repl, code)
__________________________
import re

def highlight(c):
    return re.sub(r'(?P<orange>\d+)|(?P<green>R+)|(?P<red>L+)|(?P<pink>F+)',lambda c:f'<span style="color: {[*c.groupdict()][c.lastindex-1]}">{c[c.lastindex]}</span>',c)
__________________________
from itertools import groupby

def highlight(code):
    d = {'F':'pink', 'R':'green', 'L':'red'}
    out = []
    for x,y in groupby(code, key=lambda x: x.isdigit() or x):
        out.append(x in ['(',')'] and ''.join(y) or f'<span style="color: {d.get(x, "orange")}">{"".join(y)}</span>')
    return ''.join(out)
__________________________
def highlight(code):
    dct = {
        "F": '''<span style="color: pink">''',
        "L": '''<span style="color: red">''',
        "R": '''<span style="color: green">''',
    }
    pointer = 0
    res = ""
    while pointer < len(code):
        elm = code[pointer]
        end = pointer+1
        
        while end < len(code):
            if code[end] == elm[0]:
                end += 1
                elm += elm[0]
            elif (code[end].isdigit() and elm[0].isdigit()) or code[end] in "()" and elm[0] in "()":
                
                elm += code[end]
                end += 1
            else:
                print(elm)
                break
        if elm[0] in "()":
            res += elm
        elif elm.isdigit():
            res += '''<span style="color: orange">''' + elm + "</span>"
        else:
            res += dct[elm[0]] + elm + "</span>"
        pointer = end
    return res
__________________________
def highlight(code):
    highlights = {'F':'pink','L':'red','R':'green'}
    style = ''
    current = [' ']
    for i in code:
        if i.isdigit() and current[-1].isdigit():
            current[-1] += i
        elif i == current[-1][0]:
            current[-1] += i
        else:
            current.append(i)
        
    for i in current[1:]:
        if i[0] in highlights.keys():
            style +='<span style=\"color: '+highlights[i[0]]+'\">'+i+'</span>'
        elif i.isdigit():
            style +='<span style=\"color: orange\">'+i+'</span>'
        else:
            style += i
    
    return style
__________________________
def highlight(code):
    high_dict = {"num": '<span style="color: orange">{}</span>',
                 "L": '<span style="color: red">{}</span>',
                 "F": '<span style="color: pink">{}</span>',
                 "R": '<span style="color: green">{}</span>',
                 }
    separator = []
    last = None
    res = ""
    for character in code:
        current = "num" if character.isdigit() else character
        if current == last:
            separator[-1].append(character)
            continue
        separator.append([character])
        last = current
        res += high_dict.get(current, "{}")
    return res.format(*["".join(section) for section in separator])
__________________________
HIGHLIGHTS = {
    'F': 'pink',
    'L': 'red',
    'R': 'green',
    '0': 'orange',
    '1': 'orange',
    '2': 'orange',
    '3': 'orange',
    '4': 'orange',
    '5': 'orange',
    '6': 'orange',
    '7': 'orange',
    '8': 'orange',
    '9': 'orange'
}

def highlight(code: str) -> str:
    output = ''
    open_color = None
    for c in code:
        try:
            color = HIGHLIGHTS[c]
        except:
            color = None 
        if open_color == color:
            output += c
            continue
        if open_color:
            output += '</span>'
        if color:
            output += f'<span style="color: {color}">{c}'
        else:
            output += c
        open_color = color
    if open_color:
        output += '</span>'

    return output
__________________________
import itertools
import re
from operator import itemgetter

def get_color(c):
    try:
        if c[0] == 'F':
            return 'pink'
        elif c[0] == 'L':
            return 'red'
        elif c[0] == 'R':
            return 'green'
        elif 0 <= int(c[0]) <= 9:
            return 'orange'
        else:
            return None
    except:
        return None
    
def get_span(c):
    return '<span style="color: {}">{}</span>'.format(get_color(c), c)

def divide(code):
    print(code)
    groups = []
    for _, g in itertools.groupby(code, key=lambda x: 0 <= int(x) <= 9 if x.isdigit() else x):
        groups.append(''.join(g))
    print(groups)
    return groups
    

def highlight(code: str):
    s = ''
    for x in divide(code):
        enc = re.search('[()]+', x)
        if enc is not None:
            s += ''.join(x)
        else:
            s += ''.join(get_span(x))
    return s
__________________________
def highlight(word):
    def group(word):
        ans = []
        g = word[0]
        for w in word[1:]:
            if w == g[0] or (w.isdigit() and g[0].isdigit()):
                g+=w
            else :
                ans.append(g)
                g=w
        ans.append(g)
        return ans
    word = group(word)
    ans = ""
    for w in word :
        if w[0]=="F" :
            ans+= '<span style=\"color: pink\">'+w+'</span>'
        elif w[0]in "0123456789" :
            ans+= '<span style=\"color: orange\">'+w+'</span>'
        elif w[0]=="R" :
            ans+= '<span style=\"color: green\">'+w+'</span>'
        elif w[0]=="L" :
            ans+= '<span style=\"color: red\">'+w+'</span>'
        else : 
            ans += w
        
    return (ans)
__________________________
import re

COLORS = {"F": "pink", "L": "red", "R": "green"}\
       | {str(i): "orange" for i in range(10)}

def color(token):
    if token[0] not in COLORS: return token
    return f"<span style=\"color: {COLORS[token[0]]}\">{token}</span>"

def tokenize(code):
    regex = re.compile(r"F+|L+|R+|\d+|[^FLR\d]+")
    return regex.findall(code)

def highlight(code):
    return "".join(color(token) for token in tokenize(code))
__________________________
from re import sub
def highlight(code):
    code = sub("(F+)", r'<span style="color: pink">\1</span>', code)
    code = sub("(L+)", r'<span style="color: red">\1</span>', code)
    code = sub("(R+)", r'<span style="color: green">\1</span>', code)
    code = sub("([0-9]+)", r'<span style="color: orange">\1</span>', code)
    return code
