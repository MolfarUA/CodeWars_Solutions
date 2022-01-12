import re

NAME        =  r'[a-zA-Z_]\w*'
NUM         =  r'\d+'
SYMS        =  r'[{}(),]|->'
NAME_OR_NUM = rf'{NAME}|{NUM}'

TOKENIZER = re.compile(r'|'.join((NAME,NUM,SYMS,'.')))

class FatalException(Exception): pass
def FATAL(s): raise FatalException(s)


def transpile(expr):
    expr      = re.sub(r'\s+', ' ', expr)
    i, tokens = 0, TOKENIZER.findall(expr)
    
    #----------------------------------------
    
    def walk():
        nonlocal i
        while taste(' '): i+=1
    
    def eat(what):
        nonlocal i
        if taste(what):
            stuff = tokens[i]
            i += 1
            walk()
            return stuff
        else:
            FATAL(f"Wrong offered token. Expected: '{what}' but got: '{taste(what)}'")

    def taste(what):    return i<len(tokens) and re.match(what, tokens[i]) and tokens[i]
    def isLambda():     return taste(r'{')
    def isNameOrNum():  return taste(NAME_OR_NUM)
    
    #----------------------------------------
    
    def parseFunc():
        hasParams, lst = False, []
        
        name = parseExpr()                                                            # name or lambda
        
        if taste(r'\('):                                                              # normal parameters
            hasParams = True
            lst.extend( parseParams() )
        
        hasLambda = isLambda()                                                        # handle "block like" extra lambda
        if not hasParams and not hasLambda:  FATAL("needs a lambda here")
        if hasLambda:                        lst.append(parseLambda())
        
        if i!=len(tokens): FATAL("invalid string")                                    # validate the end of the string
        
        return f"{name}({','.join(lst)})"
    
    def parseExpr():         return parseLambda() if isLambda() else parseNameOrNumber()
    def parseNameOrNumber(): return eat(NAME_OR_NUM)
    
    def parseParams():
        eat(r'\(')
        lst=[]
        if not taste(r'\)'):
            while 1:
                lst.append( parseExpr() )
                if taste(r'\)'): break
                eat(',')
        eat(r'\)')
        return lst
    
    def parseLambda():
        eat('{')
        params,stat = [], []
        while isNameOrNum():
            params.append( parseNameOrNumber() )
            if taste('->'):
                eat('->') ; break
            if not taste(',') and len(params)==1: 
                params,stat = [],params
                break
            eat(',')
        
        while not taste('}'):
            stat.append( parseNameOrNumber() )
        eat('}')
        
        paramsStr = ','.join(params)
        statStr   = ';'.join(stat) + ';'*bool(stat)
        return f"({paramsStr}){'{'}{statStr}{'}'}"
    
    
    try:
        walk()
        return parseFunc()
    except FatalException as e:
        return ""
        
_____________________________________________________
import re

def tokenize(expression):
      return re.findall(r'\s*(->|[~`!@#,$%^&*\-+=";:><./?\(\)\[\]\{\}]|[A-Za-z_0-9]+)\s*', expression)  

def check_(s):
    return re.search(r'^[A-Za-z_0-9]+$', s)

def transpile (expression):
    s = expression
    
    if re.search(r'\b\d+[a-zA-Z_]+\b', expression) or not expression or len(re.findall(r'}{', expression)) > 1:
        return ''

    expression = tokenize(expression)
    
    stack = []
    inside_round = 0
    inside_curly = 0
    
    for index, symbol in enumerate(expression):
  
        if index == 0:
            if not (symbol == '{' or check_(symbol)):
                return ''
    
        if check_(symbol):
            if not inside_round and not inside_curly and index:
                return ''
    
        elif symbol == '(':
            inside_round += 1
    
        elif symbol == ')':
            if stack[-1] == ',' or '(' not in stack:
                return ''
                
            opening = len(stack) - stack[::-1].index('(') - 1
            parameters = stack[opening + 1:]
    
            if not all(parameters[i] == ',' for i in range(1, len(parameters), 2)):
                return ''
            inside_round -= 1
    
        elif symbol == '{':
            inside_curly += 1
    
        elif symbol == '}':
    
            inside_curly -= 1
            sep = len(stack) - 1
    
            if '{' not in stack:
                return ''
    
            opening = len(stack) - stack[::-1].index('{') - 1
    
            while sep >= 0 and stack[sep] != '{':
                if stack[sep] == '->':
                    break
                sep -= 1
            else:
                sep = None
    
            lambda_exp = ''
    
            if sep:
    
                open_bracket = len(stack[:sep]) - stack[:sep][::-1].index('{') - 1
                parameters = stack[open_bracket + 1:sep]
    
                if not parameters or not all(parameters[i] == ',' for i in range(1, len(parameters), 2)):
                    return ''
    
                lambda_exp += '(' + ''.join(parameters) + ')'
            else:
                lambda_exp += '()'
                sep = opening
    
            corresponds = ';'.join(stack[sep + 1:])
    
            if ',' in corresponds:
                return ''
    
            lambda_exp += '{' + corresponds + ['', ';'][bool(corresponds)] + '}'
    
            del stack[opening:]
            stack.append(lambda_exp)
    
        elif symbol == ',':
            if stack[-1] == '(':
                return ''
    
        elif symbol == '->':
            if not (re.search(r'^[a-zA-Z0-9_]+$', stack[-1])):
                return ''
    
        else:
            return ''
        
        if symbol != '}':
            stack.append(symbol)
        
    if inside_round or inside_curly:
        return ''
    
    if re.search(r'\s*\(.*?\)\s*{.*?}\s*$', s, re.DOTALL):
        stack = stack[:-2] + ([','] if stack[-3] != '(' else ['']) + [stack[-1]] + [')']
    
    if re.search(r'^\s*{.*?}\s*{.*?}\s*$', s, re.DOTALL): 
        stack = [stack[0], '(', stack[1], ')']
    
    if re.search(r'^\s*[0-9a-zA-Z_]+\s*{.*?}\s*$', s, re.DOTALL):    
        stack = [stack[0], '(', stack[-1], ')']
    
    return ''.join(stack)

_____________________________________________________
import re

def tokenLambda(s):
    if not s.strip():return''
    r=re.match(r'^\s*{\s*(((.+)->)?(.*))?\s*}\s*$',s)
    print(r.groups())
    _,_,p,t=r.groups()
    if not p:p=''
    if not t:t=''
    y=''
    for v in t.split():
        y+=name(v)+';'
    return '(%s){%s}'%(','.join(v and name(v)for v in p.split(',')),y)

def tokenExp(s):
    r=re.match(r'^\s*%s\s*$'%(BRACK),s)
    if r:
        s=tokenLambda(s)
    else:
        s=name(s)
    return s
PAREN=r'\((([^()]|(?!R))*)\)'
BRACK=r'(\{([^{}]|(?!R))*\})'
def tokenFunc(s):
    if not s.strip():return ''
    
    e=p=l=''
    r=re.match(r'^\s*(.*)\s*%s\s*%s\s*$'%(PAREN,BRACK),s)
    if r:e,p,_,l,_=r.groups()
    else:
        r=re.match(r'^\s*(.*)\s*%s\s*$'%(PAREN),s)
        if r:e,p,_=r.groups()
        else:
            r=re.match(r'^\s*(.*)\s*%s\s*$'%(BRACK),s)
            if r:e,l,_=r.groups()
            else:return''
    try:
        e=tokenExp(e)
        if p and l:l=','+l
        p=tokenParams(p+l)
        return('%s(%s)'%(e,p)).replace(' ','')
    except:
        return''
    
def name(s):
    print('Name:',[s])
    r=re.match(r'^\s*([a-zA-Z_]\w*|\d+)\s*$',s)
    if not r:raise
    return s

def tokenParams(s):
    if not s.strip():return''
    r=re.match(r'^\s*(%s|\w+)\s*(,\s*.+)?\s*$'%(BRACK),s)
    e,_,_,p=r.groups()
    e=tokenExp(e)
    p=','+tokenParams(p[1:])if p is not None else ''
    return e+p
    
def transpile (s):
    return(tokenFunc(s.replace('\n','')))
  
_____________________________________________________
class Parser:
    def __init__(self, parse):
        self.parse = parse
    def __call__(self, s):
        return self.parse(s)
    # >=: bind
    def __ge__(self, p2):
        def f(s):
            r = self(s)
            if r is None: return None
            return p2(r[0])(r[1])
        return Parser(f)
    # |: or
    def __or__(self, p2):
        def f(s):
            r = self(s)
            return p2(s) if r is None else r
        return Parser(f)
    # >>: *>
    def __rshift__(self, p2):
        return self >= (lambda _: p2)
    # <<: <*
    def __lshift__(self, p2):
        return self >= (lambda a: p2 >> pure(a))
    # @: fmap
    def __rmatmul__(self, f):
        return self >= (lambda a: pure(f(a)))
    # *: ap
    def __mul__(self, p2):
        return self >= (lambda f: f @ p2)

curry = lambda f: lambda a: lambda b: f(a, b)
cons = lambda x: lambda xs: [x, *xs]

pure    = lambda a: Parser(lambda s: (a, s))
satisfy = lambda pred: Parser(lambda s: None if not s or not pred(s[0]) else (s[0], s[1:]))
eq      = lambda v: satisfy(lambda a: a == v)
many    = lambda p: cons @ p * Parser(lambda s: many(p)(s)) | pure([])
sepby1  = lambda p, sep: cons @ p * (sep >> (lambda s: sepby1(p, sep)(s)) | pure([]))
sepby   = lambda p, sep: sepby1(p, sep) | pure([])

import re

def transpile(expression):
    print_lambda = lambda p: lambda s: f"({','.join(p)}){{{''.join(x + ';' for x in s)}}}"
    print_func   = lambda e: lambda p: f"{e}({','.join(p)})"

    to_list      = lambda r: [r]
    name_num     = satisfy(lambda t: re.match(r'[_a-zA-Z]\w*|\d+$', t))
    lambda_param = sepby1(name_num, eq(',')) << eq('->')
    lambda_expr  = print_lambda @ (eq('{') >> (lambda_param | pure([]))) * many(name_num) << eq('}')
    expr         = name_num | lambda_expr
    params       = eq('(') >> sepby(expr, eq(',')) << eq(')')
    params_lam   = curry(list.__add__) @ params * (to_list @ lambda_expr | pure([]))
    function     = print_func @ expr * (params_lam | to_list @ lambda_expr)

    tokens = [x for x in re.findall(r'[_a-zA-Z]\w*|\d+|->|[,(){}]|\s+|.', expression) if not x.isspace()]
    res = function(tokens)
    return '' if not res or res[1] else res[0]
  
_____________________________________________________
import re
def tokenize(expr):
    #nameOrNumber = r"\d+|[a-zA-Z_][a-zA-Z_0-9]*"
    #lambdaRegex = fr"\{({nameOrNumber}(\,{nameOrNumber})*->|)({nameOrNumber}( {nameOrNumber})*|)\}"
    if re.search(r"([^a-zA-Z_0-9]|^)[0-9][a-zA-Z_]", expr): return []
    #print(re.match(fr"({lambdaRegex}|{nameOrNumber})))
    tokens = re.findall(r"->|[a-zA-Z_][a-zA-Z0-9_]*|\d+|{|}|\(|\)|,", expr)
    if "".join(tokens) != expr.replace(r" ", "").replace("\n", ""):
        return []
    if tokens.count("(") != tokens.count(")") or tokens.count("{") != tokens.count("}"):
        return []
    return tokens


def convertLambda(lam):
    print(lam)
    lam = lam[1:-1]
    if not lam:
        return "(){}"
    if "->" not in lam:
        params = [] if not "," in lam else ["!"]
        stmt = lam + [""]
    else:
        arrowPlace = lam.index("->") if "->" in lam else 0
        params = [ele for ele in lam[:arrowPlace] if ele != ","]
        stmt = lam[arrowPlace + 1:] + [""]
        if not params or lam.count(",") != len(params) - 1: params.append("!")
    return f"({','.join(params)})" + "{" + ";".join(stmt) + "}"


def getParams(tokens):
    tokensLeft = tokens[tokens.index(")") + 1:]
    tokens = tokens[tokens.index("(") + 1:tokens.index(")")]
    params = []
    idx = 0
    commaCount = 0
    while idx < len(tokens):
        token = tokens[idx]
        if token == ",":commaCount += 1
        elif token == "{":
            lamEnd = tokens.index("}", idx)
            params.append(convertLambda(tokens[idx:lamEnd + 1]))
            idx = lamEnd
        else:
            params.append(token)
        idx += 1
    if params and commaCount != len(params) - 1:
        params.append("!")
    return params, tokensLeft
    
        
def transpile (expr):
    print("transpiling:", expr)
    tokens = tokenize(expr)
    if not tokens: return ""
    res = ""
    if re.match(r"[_a-zA-Z0-9]+", tokens[0]):
        res += tokens.pop(0)
    elif tokens[0] == "{":
        lamEnd = tokens.index("}")
        res += convertLambda(tokens[:lamEnd + 1])
        tokens = tokens[lamEnd + 1:]
    else:
        return ""
        
    params, tokens = getParams(tokens) if "(" in tokens else ([],tokens)
    print(tokens)
    
    if tokens and tokens[0] == "{":
        lamEnd = tokens.index("}")
        params.append(convertLambda(tokens[:lamEnd + 1]))
        tokens = tokens[lamEnd + 1:]
    if tokens:
        return ""
        
    res += "(" + ",".join(params) + ")"
    
    return res if not "!" in res and not "->" in res else ""
  
_____________________________________________________
class Transpiler:
    def __init__(self, sequence):
        self.seq = list(sequence.rstrip().replace('\n', ' '))
        self.pos = -1
        self.len = len(self.seq) - 1
        self.result = []
        
    def emit(self, value):
        self.result.append(value)
        return self
        
    def peek(self, item=None):
        if self.pos >= self.len:
            return False
        if item is not None:
            self.eat_whitespace()
            return self.seq[self.pos + 1] == item
        return self.seq[self.pos + 1]
    
    def next(self):
        self.pos += 1
        return self.seq[self.pos]

    def eat_whitespace(self):
        while self.pos + 1 < self.len and self.seq[self.pos + 1].isspace():
            self.next()
        return self
    
    def eat(self, *items):
        for item in items:
            if self.peek(item):
                self.next()
            else:
                raise Exception(f'{self.seq[self.pos]} did not match expected {item}')
        return self
    
    def more(self):
        return self.pos < self.len

    def parse(self):
        try:
            self.function()
            if self.more():
                return ''
            return ''.join(self.result)
        except Exception as e:
            return ''
        
    @staticmethod
    def valid_identifier(char):
        return char.isalpha() or char == '_' or char.isnumeric()
    
    @staticmethod
    def valid_identifier_start(char):
        return char.isalpha() or char == '_'
        
    @staticmethod
    def valid_number(char):
        return char.isnumeric()
    
    def name_or_number(self):
        self.eat_whitespace()
        if self.valid_number(self.peek()):
            return self.gather_name_or_number(self.valid_number)
        if self.valid_identifier_start(self.peek()):
            return self.gather_name_or_number(self.valid_identifier)
        return False
            
    def gather_name_or_number(self, method):
        found = False
        while method(self.peek()):
            self.emit(self.next())
            found = True
        self.eat_whitespace()
        return found

    def function(self):
        if not self.expression():
            raise Exception('no expression')
        self.emit('(')
        if self.peek('{'):
            self.lambda_exp()
        else:
            self.eat('(').parameters().eat(')')
            if self.peek('{'):
                if self.result[-1] != '(':
                    self.emit(',')
                self.lambda_exp()
        self.emit(')')
    
    def expression(self):
        if self.peek('{'):
            self.lambda_exp()
            return True
        return self.name_or_number()
    
    def parameters(self, required=False):
        foundExpression = self.expression()
        if not foundExpression and required:
            raise Exception('no expression')
        if self.peek(','):
            if not foundExpression:
                raise Exception('no expression')
            self.emit(self.next()).parameters(True)
        return self
    
    def lambdaparam(self):
        result = self.name_or_number()
        if self.peek(','):
            self.eat(',').emit(',').lambdaparam()
        return result
    
    def lambdastmt(self):
        if self.name_or_number():
            self.emit(';')
        if not self.peek('}'):
            self.lambdastmt()
        return self
    
    def lambda_exp(self):
        self.eat('{').emit('(')
        if '-' in self.seq[self.pos:self.seq[self.pos:].index('}') + self.pos]:
            if not self.lambdaparam():
                raise Exception('-> without params')
            self.eat('-', '>')
        self.emit('){').lambdastmt().eat('}').emit('}')

def transpile(expression):
    return Transpiler(expression).parse()
  
_____________________________________________________
from functools import wraps
from dataclasses import dataclass

class Backtrack(Exception): pass # Abused for control flow in the parser
class TokenizeError(ValueError): pass

def token_cache(parser_method):
    """Decorator used to prevent extra work when backtracking"""
    cache_key = parser_method.__qualname__

    @wraps(parser_method)
    def wrapper(parser):
        token = parser.current_token()
        if cache_key in token.cache:
            mark, result = token.cache[cache_key]
            parser.mark = mark
            return result
        result = parser_method(parser)
        if result is not None:
            token.cache[cache_key] = (parser.mark, result)
        return result
        
    return wrapper

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.tokenlist = []
        self.mark = 0
    
    @staticmethod
    def required(method, *args):
        """Call the parse method with args. If the result is None, Backtrack"""
        result = method(*args)
        if result is None:
            raise Backtrack
        return result

    def current_token(self):
        try:
            if self.mark == len(self.tokenlist):
                self.tokenlist.append(next(self.tokenizer))
            return self.tokenlist[self.mark]
        except StopIteration:
            raise TokenizeError

    def parse(self):
        """If valid syntax, contruct AST, else return None"""
        try:
            function = self.parse_function()
            if function and self.parse_token(Endmarker):
                return function
        except TokenizeError:
            pass
        return None
    
    def parse_token(self, token_class):
        token = self.current_token()
        if isinstance(token, token_class):
            self.mark += 1
            return token
        return None

    # All parser methods below would generated by a parser generator in the real world.
    # This parser is based on the modern cpython parser, which is a PEG parser
    def parse_function(self):
        mark = self.mark
        try:
            expression = self.required(self.parse_expression)
            self.required(self.parse_token, LeftParen)
            parameters = self.parse_parameters()
            self.required(self.parse_token, RightParen)
            lambda_ = self.parse_lambda()
            return Function(expression=expression, parameters=parameters, lambda_=lambda_)
        except Backtrack:
            pass
        self.mark = mark
        try:
            expression = self.required(self.parse_expression)
            lambda_ = self.required(self.parse_lambda)
            return Function(expression=expression, lambda_=lambda_)
        except Backtrack:
            pass
        self.mark = mark
        return None
    
    @token_cache
    def parse_expression(self):
        mark = self.mark
        try:
            nameornumber = self.required(self.parse_token, NameOrNumber)
            return Expression(nameornumber=nameornumber)
        except Backtrack:
            pass
        self.mark = mark
        try:
            lambda_ = self.required(self.parse_lambda)
            return Expression(lambda_=lambda_)
        except Backtrack:
            pass
        self.mark = mark
        return None

    def parse_parameters(self):
        mark = self.mark
        try:
            expression = self.required(self.parse_expression)
            comma = self.parse_token(Comma)
            parameters = None
            if comma:
                parameters = self.required(self.parse_parameters)
            return Parameters(expression=expression, parameters=parameters)
        except Backtrack:
            pass
        self.mark = mark
        return None
    
    def parse_lambdaparam(self):
        mark = self.mark
        try:
            nameornumber = self.required(self.parse_token, NameOrNumber)
            comma = self.parse_token(Comma)
            lambdaparam = None
            if comma:
                lambdaparam = self.required(self.parse_lambdaparam)
            return LambdaParam(nameornumber=nameornumber, lambdaparam=lambdaparam)
        except Backtrack:
            pass
        self.mark = mark
        return None
    
    def parse_lambdastmt(self):
        mark = self.mark
        try:
            nameornumber = self.required(self.parse_token, NameOrNumber)
            lambdastmt = self.parse_lambdastmt()
            return LambdaStmt(nameornumber=nameornumber, lambdastmt=lambdastmt)
        except Backtrack:
            pass
        self.mark = mark
        return None
    
    def parse_lambda(self):
        mark = self.mark
        try:
            self.required(self.parse_token, LeftBrace)
            lambdaparam = self._parse_lambdaparam_arrow()
            lambdastmt = self.parse_lambdastmt()
            self.required(self.parse_token, RightBrace)
            return Lambda(lambdaparam=lambdaparam, lambdastmt=lambdastmt)
        except Backtrack:
            pass
        self.mark = mark
        return None
    
    def _parse_lambdaparam_arrow(self):
        mark = self.mark
        try:
            lambdaparam = self.required(self.parse_lambdaparam)
            self.required(self.parse_token, Arrow)
            return lambdaparam
        except Backtrack:
            pass
        self.mark = mark
        return None

    
class Tokenizer:
    numberset = set('0123456789')
    identifierstartset = set('_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    identifierset = set('_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    whitespaceset = set(' \t\n')
    
    def __init__(self, inputstr):
        self.inputstr = inputstr
        self.done = False
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.done:
            raise StopIteration
        # Skip whitespace
        c = None
        while (c := self.next_char()) in self.whitespaceset:
            pass
        # Are we at the end of the string?
        if c is None:
            self.done = True
            return Endmarker()
        # check for one char tokens
        if c == '(':
            return LeftParen(c)
        if c == ')':
            return RightParen(c)
        if c == '{':
            return LeftBrace(c)
        if c == '}':
            return RightBrace(c)
        if c == ',':
            return Comma(c)
        # check for arrow
        if c == '-':
            c = self.next_char()
            if c != '>':
                raise TokenizeError
            return Arrow('->')
        # check for nameornumber
        start = self.index - 1
        if c in self.numberset:
            while (c := self.next_char()) in self.numberset:
                pass
            self.index -= 1
            return NameOrNumber(self.inputstr[start:self.index])
        if c in self.identifierstartset:
            while (c := self.next_char()) in self.identifierset:
                pass
            self.index -= 1
            return NameOrNumber(self.inputstr[start:self.index])
        # invalid token
        raise TokenizeError
        
    def next_char(self):
        if self.index == len(self.inputstr):
            return None
        c = self.inputstr[self.index]
        self.index += 1
        return c
        

class Token:
    def __init__(self, literal=''):
        self.literal = literal
        self._cache = None
        
    def __repr__(self):
        return f'{type(self).__name__}({self.literal})'
    
    @property
    def cache(self):
        if self._cache is None:
            self._cache = {}
        return self._cache
    
    def dart_transform(self):
        return self.literal
        
class    Endmarker(Token): pass
class NameOrNumber(Token): pass
class    LeftParen(Token): pass # '('
class   RightParen(Token): pass # ')'
class    LeftBrace(Token): pass # '{'
class   RightBrace(Token): pass # '}'
class        Arrow(Token): pass # '->'
class        Comma(Token): pass # ','


def flattenable(valueattr, nextattr):
    """class decorator that adds the flatten method to recursive ASTNodes"""

    def decorator(cls):
        def flatten(astnode):
            """astnode is a linkedlist where `valueattr` is this node's value and
            `nextattr` is the next node in the list. Return a python list
            containing all the values in order
            """
            values = []
            while astnode is not None:
                values.append(getattr(astnode, valueattr))
                astnode = getattr(astnode, nextattr)
            return values
        
        setattr(flatten, '__qualname__', f'{cls.__qualname__}.{flatten.__name__}')
        setattr(cls, 'flatten', flatten)
        return cls

    return decorator

class ASTNode:
    def dart_transform(self):
        return ''

@dataclass
class Function(ASTNode):
    expression: ASTNode
    parameters: ASTNode = None
    lambda_: ASTNode = None

    def dart_transform(self):
        expression_str = self.expression.dart_transform()
        parameter_list = [] if self.parameters is None else self.parameters.flatten()
        if self.lambda_ is not None:
            parameter_list.append(self.lambda_)
        parameter_str = ','.join(node.dart_transform() for node in parameter_list)
        return f'{expression_str}({parameter_str})'

@dataclass
class Expression(ASTNode):
    nameornumber: Token = None
    lambda_: ASTNode = None

    def dart_transform(self):
        node = self.nameornumber or self.lambda_
        return node.dart_transform()
        
@flattenable('expression', 'parameters')
@dataclass
class Parameters(ASTNode):
    expression: ASTNode
    parameters: ASTNode = None

@flattenable('nameornumber', 'lambdaparam')
@dataclass
class LambdaParam(ASTNode):
    nameornumber: Token
    lambdaparam: ASTNode = None

    def dart_transform(self):
        return ','.join(node.dart_transform() for node in self.flatten())
        
@flattenable('nameornumber', 'lambdastmt')
@dataclass
class LambdaStmt(ASTNode):
    nameornumber: Token
    lambdastmt: ASTNode = None

    def dart_transform(self):
        return ''.join(node.dart_transform() + ';' for node in self.flatten())
        
@dataclass
class Lambda(ASTNode):
    lambdaparam: ASTNode = None
    lambdastmt: ASTNode = None
    
    def dart_transform(self):
        lambdaparam = self.lambdaparam or ASTNode()
        lambdastmt = self.lambdastmt or ASTNode()
        return f'({lambdaparam.dart_transform()}){"{"}{lambdastmt.dart_transform()}{"}"}'
        

def transpile(expression):
    tokenizer = Tokenizer(expression)
    parser = Parser(tokenizer)
    tree = parser.parse()
    if tree:
        return tree.dart_transform()
    return ''
