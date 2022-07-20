5470c635304c127cad000f0d


""" GRAMMAR
Root    ::= Or
Or      ::= Str ( '|' Str )?
Str     ::= ZeroMul+
ZeroMul ::= Term '*'?
Term    ::= Normal | Any | '(' Or ')'
Normal  ::= [^()|*.]
Any     ::= '.'
"""

def parseRegExp(input): return Parser(input).parse()

class InvalidRegex(Exception): pass

class Parser(object):
    
    def __init__(self, input): self.tokens = list(input)
    
    def parse(self):
        try:                 ret = self.parse_Or()
        except InvalidRegex: ret = ''
        
        return ret if isinstance(ret, RegExp) and not self.tokens else ''
    
    def pop(self):  return self.tokens.pop(0)
    def peek(self): return self.tokens and self.tokens[0]
    
    def parse_Or(self):
        or_ = self.parse_Str()
        if self.peek() == '|':
            self.pop()
            or_ = Or(or_, self.parse_Str())
        return or_
    
    def parse_Str(self):
        seq = []
        while self.peek() and self.peek() not in "*)|":
            ret = self.parse_ZeroMul()
            seq.append(ret)
            
        return ('' if not seq else
                Str(seq) if len(seq) > 1 else
                seq[0])
        
    def parse_ZeroMul(self):
        zm = self.parse_Term()
        if zm is not None and self.peek() == '*':
            self.pop()
            zm = ZeroOrMore(zm)
        return zm
        
    def parse_Term(self):
        if not self.peek(): raise InvalidRegex()
        was = self.pop()
        if was == '(':
            if not self.peek() or self.peek() == ')': raise InvalidRegex()
            expr = self.parse_Or()
            if not self.peek() or self.peek() != ')': raise InvalidRegex()
            self.pop()
            
        elif was == '.':        expr = Any()
        elif was not in "()*|": expr = Normal(was)
        else:                   raise ValueError("Wrong code: you shouldn't reach this statment!")
        
        return expr
____________________________________________________________
def parseRegExp(input):
    try: return _parseRegExp(input)
    except ParseError: return ''

def _parseRegExp(input):
    tokens = evalParentheses(list(input))

    if '|' in tokens: return toOr(tokens)
    elif len(tokens) == 2 and tokens[1] == '*': return ZeroOrMore(_parseRegExp(tokens[0]))
    elif len(tokens) > 1: return toStr(tokens)
    elif len(tokens) == 0: raise ParseError()
    elif tokens == ['.']: return Any()
    elif type(tokens[0]) == list: return _parseRegExp(tokens[0])
    elif tokens[0] not in '()*|.': return Normal(tokens[0])
    else: raise ParseError()

class ParseError(BaseException): pass

def toStr(tokens):
    regexps = []
    i = 0
    while i < len(tokens):
        if tokens[i] in list('()*|'): raise ParseError('found unexpected token')
        if tokens[i+1:i+2] == ['*']: regexps.append(tokens[i:i+2]); i += 1
        else: regexps.append([tokens[i]])
        i += 1
    return Str(list(map(_parseRegExp, regexps)))

def toOr(tokens):
    if tokens.count('|') != 1: raise ParseError('found invalid or')
    i = tokens.index('|')
    return Or(*map(_parseRegExp, [tokens[:i], tokens[i+1:]]))

def evalParentheses(tokens):
    depth = 0; start = 0; groups = []
    for i, token in enumerate(tokens):
        if token == '(': depth += 1
        elif token == ')': depth -= 1
        elif not depth: groups.append(token)

        if token == '(' and depth == 1: start = i+1
        elif token == ')' and depth == 0: groups.append(tokens[start:i])

        if depth < 0: raise ParseError('invalid parentheses')
    if depth != 0: raise ParseError('invalid parentheses')
    return groups
____________________________________________________________
import re
def parseRegExp(s):
    if re.search(r'\*\*',s) : return ''
    stack = []
    for ch in s:
          if ch == '(' : stack.append(ch)
          elif ch == ')':
              if '(' not in stack : return ''
              ind = len(stack)-stack[::-1].index('(')-1
              li = stack[ind+1:]
              del stack[ind:]
              if not li:return ''
              if 'OR' in li:
                  ori = li.index('OR')
                  a, b = li[:ori], li[ori+1:]
                  stack.append(Or(Str(a) if len(a)>1 else a[0], Str(b) if len(b)>1 else b[0]))
              else : stack.append(Str(li) if len(li)>1 else li[0])   
          elif ch == '|'  : stack.append('OR')
          elif ch == '*':
              if not stack or str(stack[-1]) in ['*','OR','('] : return ''
              stack.append(ZeroOrMore(stack.pop()))
          else : stack.append(Normal(ch) if ch != '.' else Any())
    
    if not stack or stack.count('OR')>1 or '(' in stack : return ''
    if 'OR' in stack:
        ori = stack.index('OR')
        a, b = stack[:ori], stack[ori+1:]
        return Or(Str(a) if len(a)>1 else a[0], Str(b) if len(b)>1 else b[0])
    return Str(stack) if len(stack)>1 else stack[0]
____________________________________________________________
def parseRegExp(input):
    """ How NOT to implement a parser! This was only meant as an excersise.
        Originally coded this with 'anytree', but that is not yet in codewars.
        Random tests seem to be somewhat buggy.
    """
    root = {'type':'root', 'parent':None, 'children':[], 'value':'root'};
    ntree = root; nprev = None

    def visit_nodes(node, depth=0):
        nodes = []
        pvalue = node['value'] if node['type'] in ['term','root'] else \
                node['type'].__name__ if type(node['type']).__name__ == \
                'type' else node['type'].__class__.__name__
        if node['type'] == Str:
            pvalue += ':' + node['strtype']
            if 'strstatus' in node:
                pvalue += ':' + node['strstatus']
        print("{}{}{}".format(" "*4*(depth-1),'|-- '*int(bool(depth)), pvalue))
        for n in node['children']: 
            nodes += visit_nodes(n,depth + 1)
        return nodes + [node]

    for c in input:
        if c not in "()*|" and ntree['type'] != Str:
            ntree = {'type':Str, 'parent':ntree, 'children':[], 'strtype':'implicit'}
            ntree['parent']['children'].append(ntree)
            nprev = ntree

        if c == '(':
           node = {'type':Str, 'parent':ntree, 'children':[], 
                    'strtype':'explicit', 'strstatus':'open'}
           ntree['children'].append(node)
           ntree = node

        if c == ')':
            if ntree['type'] == Str and ntree['strtype'] == 'explicit' \
                    and not len(ntree['children']):
                return ""
            while not (ntree['type'] == Str and ntree['strtype'] == 'explicit'):
                if ntree['type'] == 'root': 
                    return ""
                ntree = ntree['parent']
            if nprev['parent']['type'] == Str and nprev['parent']['strtype'] == 'implicit' \
                    and nprev['parent']['parent'] == ntree:
                nprev['parent']['parent']['children'] = nprev['parent']['parent']['children'][:-1]
                for c in nprev['parent']['children']:
                    c['parent'] = nprev['parent']['parent']
                    nprev['parent']['parent']['children'].append(c)
            ntree['strstatus'] = 'closed'
            nprev = ntree
            ntree = ntree['parent']

        if c == '*': 
            if not nprev or not nprev['parent'] or nprev['type'] not in [Str,Normal,Any]: 
                return "" 
            parent = nprev['parent']
            if parent['type'] == ZeroOrMore:
                return ""
            node = {'type':ZeroOrMore, 'parent':parent, 'children':[nprev]}
            nprev['parent'] = node
            parent['children'][parent['children'].index(nprev)] = node
            nprev = node

        if c == '|':
            if not nprev or not nprev['parent'] or nprev['type'] not in [Str,Normal,Any,ZeroOrMore]: 
                return ""
            parent = nprev['parent']
            if nprev['parent']['type'] == Str:
                parent = parent['parent']
            if parent['type'] == Or or [n for n in parent['children'] if n['type'] == Or]:
                return ""
            ntree = {'type':Or, 'parent':parent, 'children':[]}
            if nprev['parent']['type'] == Str and nprev['parent']['strtype'] == 'implicit':
                nprev['parent']['parent'] = ntree
                parent['children'][parent['children'].index(nprev['parent'])] = ntree
                ntree['children'].append(nprev['parent'])
                newstr2 = {'type':Str,'parent':ntree,'children':[],
                        'strtype':'implicit'}
                ntree['children'].append(newstr2)
                ntree = newstr2
            elif nprev['parent']['type'] == Str and nprev['parent']['strtype'] == 'explicit':
                newstr1 = {'type':Str,'parent':nprev['parent']['parent'],
                        'children':[ntree],'strtype':'explicit','strstatus':'open'}
                for i, e in enumerate(parent['children']):
                        if id(e) == id(nprev['parent']): parent['children'][i] = newstr1
                nprev['parent']['parent'] = ntree
                ntree['parent'] = newstr1
                nprev['parent']['strstatus'] = 'closed'
                ntree['children'].append(nprev['parent'])
                newstr2 = {'type':Str,'parent':ntree,'children':[],
                        'strtype':'implicit'}
                ntree['children'].append(newstr2)
                ntree = newstr2
            else:
                nprev['parent'] = ntree
                parent['children'][parent['children'].index(nprev)] = ntree
                ntree['children'].append(nprev)
            nprev = ntree

        if c == '.':
            nprev = {'type':Any, 'parent':ntree, 'children':[]}
            ntree['children'].append(nprev)

        if c not in "()*|.":
            nprev = {'type':Normal, 'parent':ntree, 'children':[]}
            term = {'type':'term', 'parent':nprev, 'children':[], 'value':c}
            nprev['children'].append(term)
            ntree['children'].append(nprev)

    for n in visit_nodes(root):
        if n['type'] == 'root':
            exprs = [c['type'] for c in n['children']]
            if len(exprs) > 1:
                return Str(exprs)
            if len(exprs) < 1:
                return ""
            return exprs[0]
        elif n['type'] == 'term':
            n['type'] = n['value']
        elif n['type'] == Str:
            if n['strtype'] == 'explicit' and n['strstatus'] == 'open':
                return ""
            parent = n['parent']
            if len(n['children']) == 1:
                parent = n['parent']
                child = n['children'][0]
                parent['children'][parent['children'].index(n)] = child 
                n['parent'] = None; 
                n['children'] = []
            else:
                n['type'] = Str([c['type'] for c in n['children']])
        else:
            n['type'] = n['type'](*[c['type'] for c in n['children']])
____________________________________________________________
from preloaded import Any, Normal, Or, Str, ZeroOrMore, RegExp

def parse_regexp(indata: str):
    if not indata:
        return None
    
    indata = '(' + indata + ')'
    
    stack = []
    
    for char in indata:
        if char == '.':
            stack.append(Any())
        elif char == '*':
            args = stack.pop()
            if isinstance(args, ZeroOrMore):
                return
            stack.append(ZeroOrMore(args))
        elif char in '(|':
            stack.append(char)
        elif char == ')':
            args = []
            strings = []
            if len(stack) == 0:
                return
            s = stack.pop()
            while s != '(':
                if s == '|':
                    if len(args) > 1:
                        strings.append(Str(list(reversed(args))))
                    else:
                        strings.append(args[0])
                    args = []
                else:
                    args.append(s)
                if len(stack) == 0:
                    return
                s = stack.pop()
            if len(args) == 0:
                return
            if len(args) > 1:
                strings.append(Str(list(reversed(args))))
            else:
                strings.append(args[0])
            if len(strings) > 2:
                return
            elif len(strings) == 2:
                stack.append(Or(*reversed(strings)))
            elif len(strings) == 1:
                stack.append(strings[0])
        else:
            stack.append(Normal(char))
    
    if len(stack) != 1 or not isinstance(stack[0], RegExp):
        return None
    
    return stack[0]
____________________________________________________________
def parse_regexp(s):
    try: return parse(s)[1]
    except: return

def parse(s, i=0, d=0, o=False):
    stack = []
    while i < len(s):
        c = s[i]
        i += 1
        
        if c == '.':
            stack.append(Any())
        elif c == '*':
            if isinstance(stack[-1], ZeroOrMore): raise Exception
            stack.append(ZeroOrMore(stack.pop()))
        elif c not in '()|':
            stack.append(Normal(c))
        
        elif c == '|':
            i, r = parse(s, i, d, o=True)
            if o: raise Exception
            stack = [Or(Str(stack) if len(stack) > 1 else stack[0], r)]
        elif c == '(':
            i, r = parse(s, i, d+1)
            stack.append(r)
        elif c == ')':
            d -= 1
            if o: i -= 1
            break
        
    if i == len(s) and d or d < 0: raise Exception
    if len(stack) > 1:  return i, Str(stack)
    if len(stack) == 1: return i, stack[0]
    raise Exception
____________________________________________________________
from preloaded import Any, Normal, Or, Str, ZeroOrMore
import string


class InvalidSyntaxException(Exception):
    pass


class RDP:
    normals = set(string.printable).difference(".|()*")
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.location_stack = []
        self.index = 0
        self.next()
        
    def push_index(self):
        self.location_stack.append(self.index)
    
    def pop_index(self):
        self.index = self.lcoation_stack.pop()
        
    def next(self):
        try:
            self.current = self.tokens[self.index]
            self.index += 1
        except IndexError:
            self.current = None
    
    def accept(self, tokens):  
        if self.current is None:
            return False, None
        
        if self.current in tokens:
            t = self.current
            self.next()
            return True, t
        return False, self.current

    def expect(self, tokens, exception_type=ValueError):
        f, t = self.accept(tokens)
        if not f:
            raise exception_type(f"Expected one of {tokens}, but found {t}")
        return t
    
    def letter(self):
        return Normal(self.expect(self.normals))
    
    def wildcard(self):
        f, t = self.accept(".")
        if f:
            return Any()
        else:
            return self.letter()
        
    def brackets(self):
        f, t = self.accept("(")
        if f:
            internal = self.either_or()
            self.expect(")", InvalidSyntaxException)
            node = internal
        else:
            node = self.wildcard()
        
        f, t = self.accept("*")
        if f:
            return ZeroOrMore(node)
        return node
        
    
    def unit(self):
        r_nodes = []
        try:
            while True:
                r_nodes.append(self.brackets())
        except ValueError as e:
            if len(r_nodes) == 0:
                raise InvalidSyntaxException("Empty Brackets")
        
        if len(r_nodes) > 1:
            r = Str(r_nodes)
        else:
            r = r_nodes[0]
        
        return r
    
    def either_or(self):
        left = self.unit()
        f, t = self.accept("|")
        if f:
            right = self.unit()
            return Or(left, right)
        return left
    
    def parse(self):
        try:
            root = self.either_or()
        except InvalidSyntaxException:  # Could not parse
            return None
        if self.current is not None:  # Some unparsed remaining
            return None
        return root
        

def parse_regexp(indata):
    parser = RDP(indata)
    return parser.parse()
____________________________________________________________
import re
from typing import TypeAlias

from preloaded import Any, Normal, Or, Str, ZeroOrMore

Regex: TypeAlias = Any | Normal | Or | Str | ZeroOrMore

brackets = re.compile(r'\([^()]+\)')
identifiers = {chr(ch) for ch in range(1000)}


def parse_regexp(expression: str) -> Regex | None:
    return RegexpParser(expression).parse_regexp()


class RegexpParser:
    def __init__(self, expression: str) -> None:
        self._expression = expression
        self._symbols = iter(identifiers - set(expression))
        self._table: dict[str, Regex] = {}

    def parse_regexp(self) -> Regex | None:
        if self._is_valid():
            self._parse_parts_with_brackets()
            self._to_regex(self._expression, 'result')
            return self._table.get('result')
        return None

    def _parse_parts_with_brackets(self) -> None:
        while m := brackets.search(self._expression):
            symbol = next(self._symbols)
            self._to_regex(m.group(0), symbol)
            self._expression = self._expression.replace(m.group(0), symbol)

    def _to_regex(self, part: str, symbol: str) -> None:
        part = part.lstrip('(').rstrip(')')
        parts = part.split('|')
        total_result: list[Regex] = []
        for p in parts:
            result = self._parse_part(p)
            if len(result) > 1:
                total_result.append(Str(result))
            else:
                total_result.extend(result)
        self._table[symbol] = (
            Or(*total_result) if len(total_result) > 1 else total_result[-1]
        )

    def _parse_part(self, part: str) -> list[Regex]:
        result = []
        for i, symbol in enumerate(part):
            if symbol in self._table:
                result.append(self._table[symbol])
            elif symbol == '*':
                result.append(ZeroOrMore(result.pop()))
            else:
                result.append(Normal(symbol) if symbol != '.' else Any())
        return result

    def _is_valid(self) -> bool:
        return all((
            self._expression,
            not re.search(r'([^()]+\|){2,}', self._expression),
            self._is_okay_zero_or_more_token(),
            self._is_balanced_brackets()
        ))

    def _is_balanced_brackets(self) -> bool:
        br = ''.join(ch for ch in self._expression if ch in {'(', ')'})
        while '()' in br:
            br = br.replace('()', '')
        return not br and not re.search(r'\(\)', self._expression)

    def _is_okay_zero_or_more_token(self) -> bool:
        return all((
            not re.search(r'(\*){2,}', self._expression),
            not self._expression.startswith('*'),
            not re.search(r'\(\*.*\)|\|\*', self._expression)
        ))
