import re

def tokenize(expression):
    if expression == "": return []
    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.func = {}

    def funkcja(self,ciag):
        pointer=self.func[ciag[0]].index("=>")
        z=self.func[ciag[0]][0:pointer]
        w=ciag[1:]
        d=self.func[ciag[0]][pointer+1:]
        for x in z:
            while x in d: d[d.index(x)]=str(w[z.index(x)])
        return self.input("".join(d))

    def licz(self,ciag):
        znak=["fn","(",")",self.func,"%","*","/","+","-","="]
        for c in range(len(znak)):
            while znak[c] in ciag or c==3:
                if c!=3:
                    first=ciag.index(znak[c])
                    last=len(ciag)-ciag[::-1].index(znak[c])-1
                if c==0:
                    if ciag[0]=="(": raise Exception ("Tu nie wiem czemu")
                    pointer=ciag[last:].index("=>")
                    body=ciag[pointer+1:]
                    for x in body[::-1]:
                        if not x.isalpha(): body.remove(x)
                    var=ciag[last+2:pointer]
                    ile=len(var)
                    if ciag[last+1] in self.vars: raise Exception ("Funkcja nie porzyjmie nazwy zmiennej")
                    if (ile==0 and len(body)!=0) : raise Exception ("Brak zmiennych w funkcji")
                    for x in var:
                        if var.count(x)>1: raise Exception ("Duble zmiennych w funkcji")
                        if body.count(x)==0: raise Exception ("Brak zmiennych po prawej stronie")
                    if set("".join(body))!=set("".join(var)): raise Exception ("Nadmiarowe zmienne po prawej")
                    self.func[ciag[last+1]]=ciag[last+2:]
                    del ciag[last:]
                elif c>=1 and c<3:
                    x,a=0,0
                    while "("  in ciag:
                        if ciag[x]=="(":a=x
                        elif ciag[x]==")":
                            ciag[a]=self.licz(ciag[a+1:x])
                            del ciag[a+1:x+1]
                            x=-1
                        x+=1
                elif c==3:
                    for x in ciag[::-1]:
                        if x in self.func:
                            last=len(ciag)-ciag[::-1].index(x)-1
                            var=self.func[x]
                            ile=self.func[x].index("=>")
                            wyn=self.funkcja(ciag[last:last+ile+1])
                            ciag[last]=str(wyn)
                            del ciag[last+1:last+ile+1]
                    break
                elif c>3 and c<9:
                    if c in (4,5,6):
                        for d in ("%","/","*"):
                            try:first=(ciag.index(d) if ciag.index(d)<first else first)
                            except: None
                    try:
                        x=int(self.vars[ciag[first-1]] if ciag[first-1].isalpha() else int(ciag[first-1]))
                        y=int(self.vars[ciag[first+1]] if ciag[first+1].isalpha() else int(ciag[first+1]))
                    except: raise Exception("Brak parametrów w działaniu lub brak zmiennej")
                    if ciag[first]=="+": wyn=x+y
                    elif ciag[first]=="-": wyn=x-y
                    elif ciag[first]=="*": wyn=x*y
                    elif ciag[first]=="/": wyn=x/y
                    elif ciag[first]=="%": wyn=x%y
                    ciag[first-1]=str(int(wyn))
                    del ciag[first:first+2]
                elif c==9:
                    try: y=int(self.vars[ciag[last+1]] if ciag[last+1].isalpha() else int(ciag[last+1]))
                    except: raise Exception("brak drugiej zmiennej przy porównaniu")
                    if ciag[last-1].isalpha(): self.vars[ciag[last-1]]=y
                    else: raise Exception("Przyrównanie nie do zmiennej")
                    ciag[last-1]=str(y)
                    del ciag[last:last+2]

        #one or two parameters
        if len(ciag)==2: raise Exception("Tylko dwa parametry")
        elif len(ciag)==1 and (ciag[0].isalpha()==False or ciag[0] in self.vars or ciag[0]==""):
            return(ciag[0] if ciag[0].isalpha()==False else self.vars[ciag[0]])
        elif len(ciag)==0: return("")
        else: raise Exception("Jeden zły parametr")
        return(ciag)

    def input(self, expression):
        exp = tokenize(expression)
        exp=self.licz(exp)
        if exp=="": return ("")
        return int(exp)
      
##################
import operator as op
import re
import string

RE = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")

tokenize = lambda e: [s for s in RE.findall(e) if not s.isspace()]
is_ident = lambda t: t[0] in "_ " + string.ascii_letters
    
class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):    
        if "( fn " in ' '.join(tokenize(expression)): raise ValueError("Cannot declare function in an expression")

        while "(" in expression:
            if expression.startswith("fn "): break

            ptr = idx = expression.index("(")
            start, tofind = expression[:idx] if idx else "", 1
            while tofind:
                ptr += 1
                if expression[ptr] == ")": tofind -= 1
                if expression[ptr] == "(": tofind += 1

            expression = start + str(self.input(expression[idx+1:ptr])) + expression[ptr+1:]
        return self.parse(expression)

    def parse(self, expression):
        if expression.startswith("fn "):
            name, args, expr = expression.split()[1], expression.split("=>")[0].split()[2:], expression.split("=>")[1].strip()
            self.functions[name] = {"expr": expr, "args": args}

            if name in self.vars:
                raise ValueError("Name alreday in use " + name)
            elif len(args) > len(set(args)):
                raise ValueError("Repeated argument " + expression)
            elif any(t not in args and t not in self.functions for t in tokenize(expr) if is_ident(t)): 
                raise ValueError("Invalid function" + expression)

            return ''

        # Deal with other expressions, find rightmost =
        left, expression = expression.rsplit("=", 1) if "=" in expression else ('', expression)
        tokens = tokenize(expression)
        if not tokens:
            return ''

        newtokens = []
        while tokens:
            token = tokens.pop()
            if is_ident(token):
                if token in self.functions:
                    args = {a:newtokens.pop() for a in self.functions[token]["args"]}
                    token = self.input(' '.join([args.get(t, t) for t in tokenize(self.functions[token]["expr"])]))
                elif token in self.vars:
                    token = self.vars[token]
                else:
                    raise ValueError("Referenced before assignment : " + token)

            newtokens.append(str(token))

        result = evaluate(' '.join(newtokens[::-1]))

        if left:
            vv = ' '.join(left.split()).split("=")
            if any(v in self.functions for v in vv): raise ValueError("Identifier already in use : " + v)

            for v in vv: self.vars[v.strip()] = result

        return result

def evaluate(s):    
    OP = {"*": op.mul, "/": op.truediv, "+": op.add, "-": op.sub, "%": op.mod}

    tokens, stack, result = [w if w in OP else float(w) if '.' in w else int(w) for w in s.split()[::-1]], [], 0

    while tokens:
        t = tokens.pop()
        stack.append(OP[t](stack.pop(), tokens.pop()) if str(t) in '/*%' else t)
    while stack:
        n = stack.pop()
        result = OP[stack.pop() if stack else "+"](result, n)

    return result
  
############################
import re
from collections import namedtuple
from operator import add, sub, mul, truediv, mod

Token = namedtuple('Token', ['type', 'value'])

NUMBER = 'number'
IDENTIFIER = 'identifier'
OPERATOR = 'operator'
OPEN_PAREN = 'open_paren'
CLOSE_PAREN = 'close_paren'

FN = 'fn'
ARROW = 'arrow'

class UnknownTokenError(Exception): pass

class Tokenizer(object):
    def __init__(self, code):
        self.code = code
    
    def _extract(self, token_type, regex):
        match = re.match(regex, self.code)
        if match:
            token_value = match.group(0)
            self.code = self.code[len(token_value):]
            return Token(token_type, token_value)
    
    def _fn(self):
        return self._extract(FN, r'fn')
    def _arrow(self):
        return self._extract(ARROW, r'=>')
    def _number(self):
        return self._extract(NUMBER, r'\d+|\d*\.\d+')
    def _identifier(self):
        return self._extract(IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*')
    def _operator(self):
        return self._extract(OPERATOR, r'[+*/%=-]')
    def _open_brace(self):
        return self._extract(OPEN_PAREN, r'\(')
    def _close_brace(self):
        return self._extract(CLOSE_PAREN, r'\)')
    def _whitespace(self):
        return self._extract('', r'\s+')
    
    def tokens(self):
        while self.code:
            token = self._number()
            if token:
                yield Token(token.type, float(token.value))
                continue
            token = (self._fn() or self._arrow() or
                    self._identifier() or self._operator() or
                    self._open_brace() or self._close_brace())
            if token:
                yield token
                continue
            token = self._whitespace()
            if token:
                continue
            raise UnknownTokenError()

class InvalidTokenError(Exception): pass

class AbstractParser(object):
    def _assert_type(self, token, token_type):
        if token.type != token_type:
            raise InvalidTokenError()

FN_KEYWORD = 'fn_keyword'
FN_NAME = 'fn_name'
FN_ARG = 'fn_arg'
FN_EXPR = 'fn_expr'

FUNCTION = 'function'

Function = namedtuple('Function', ['name', 'arguments', 'argument_len', 'body'])

class FunctionExecutionError(Exception): pass

class FunctionParser(AbstractParser):
    def __init__(self, identifier_map=dict(), function_map=dict()):
        self.identifier_map = identifier_map
        self.function_map = function_map
        self.state = FN_KEYWORD
        self.name = ''
        self.arguments = []
        self.body = []
    
    def feed_token(self, token):
        if self.state == FN_KEYWORD:
            self._assert_type(token, FN)
            self.state = FN_NAME
        elif self.state == FN_NAME:
            self._assert_type(token, IDENTIFIER)
            if token.value in self.identifier_map:
                raise InvalidTokenError()
            self.name = token.value
            self.state = FN_ARG
        elif self.state == FN_ARG:
            if token.type == IDENTIFIER:
                self.arguments.append(token.value)
            else:
                self._assert_type(token, ARROW)
                self.state = FN_EXPR
        elif self.state == FN_EXPR:
            if token.type in (FN, ARROW):
                raise InvalidTokenError()
            if token.type == IDENTIFIER:
                name = token.value
                if (name not in self.function_map and
                    name not in self.arguments):
                    raise InvalidTokenError()
            self.body.append(token)
        else:
            raise InvalidTokenError()
    
    def result(self):
        if not self.name or not self.body or len(set(self.arguments)) != len(self.arguments):
            raise SyntaxError()
        return Function(self.name, self.arguments,
            len(self.arguments), self.body)

class ArithParser(AbstractParser):
    def __init__(self, identifier_map=dict(), function_map=dict()):
        self.stack = [[]]
        self.identifier_map = identifier_map
        self.function_map = function_map
        
    def _should_eval(self, next_op):
        if len(self.stack[-1]) <= 2:
            return False
        prev_op = self.stack[-1][-2]
        self._assert_type(prev_op, OPERATOR)
        return prev_op.value in '*/%' or (prev_op.value in '+-' and next_op.value in '=+-')
    
    def _resolve_identifier(self, identifier):
        try:
            return self.identifier_map[identifier.value]
        except KeyError:
            raise InvalidTokenError()
    
    def _resolve_num_or_id(self, num_or_id):
        print(num_or_id)
        if num_or_id.type == NUMBER:
            return num_or_id.value
        elif num_or_id.type == IDENTIFIER:
            return self._resolve_identifier(num_or_id)
        raise InvalidTokenError()
    
    def _update_identifier(self, identifier, value):
        self.identifier_map[identifier.value] = value
    
    def _eval(self):
        operand2, prev_op, operand1 = [self.stack[-1].pop() for _ in range(3)]
        self._assert_type(prev_op, OPERATOR)
        if prev_op.value == '=':
            self._assert_type(operand1, IDENTIFIER)
            if operand1.value in self.function_map:
                raise InvalidTokenError()
            rhs_value = self._resolve_num_or_id(operand2)
            self._update_identifier(operand1, rhs_value)
            self.stack[-1].append(Token(NUMBER, rhs_value))
        else:
            value1 = self._resolve_num_or_id(operand1)
            value2 = self._resolve_num_or_id(operand2)
            new_value = {'+': add, '-': sub, '*': mul, '/': truediv, '%': mod
                }[prev_op.value](value1, value2)
            self.stack[-1].append(Token(NUMBER, new_value))
    
    def _run_function(self, function, arg_values):
        identifier_map = {name: arg.value for name, arg in
            zip(function.arguments, arg_values)}
        function_runner = ArithParser(identifier_map, self.function_map)
        for token in function.body:
            function_runner.feed_token(token)
        value, _ = function_runner.result()
        if isinstance(value, (int, float)):
            return value
        raise FunctionExecutionError()
    
    def feed_token(self, token):
        if token.type in (NUMBER, IDENTIFIER):
            if token.type == IDENTIFIER and token.value in self.function_map:
                function = self.function_map[token.value]
                self.feed_token(Token(OPEN_PAREN, '('))
                token = Token(FUNCTION, function)
            self.stack[-1].append(token)
            if self.stack[-1][0].type == FUNCTION:
                if len(self.stack[-1]) > 1:
                    value = self._resolve_num_or_id(self.stack[-1][-1])
                    self.stack[-1][-1] = Token(NUMBER, value)
                function = self.stack[-1][0].value
                if function.argument_len + 1 == len(self.stack[-1]):
                    value = self._run_function(function, self.stack[-1][1:])
                    self.stack[-1] = [Token(NUMBER, value)]
                    self.feed_token(Token(CLOSE_PAREN, ')'))
        elif token.type == OPERATOR:
            if not self.stack[-1] or self.stack[-1][-1].type not in (NUMBER, IDENTIFIER):
                raise InvalidTokenError()
            while self._should_eval(token):
                self._eval()
            self.stack[-1].append(token)
        elif token.type == OPEN_PAREN:
            self.stack.append([])
        elif token.type == CLOSE_PAREN:
            while len(self.stack[-1]) > 1:
                self._eval()
            value = self._resolve_num_or_id(self.stack.pop()[0])
            self.feed_token(Token(NUMBER, value))
        else:
            raise InvalidTokenError()
    
    def result(self):
        while len(self.stack[-1]) > 1:
            self._eval()
        try:
            result = self.stack[-1][0]
            value = self._resolve_num_or_id(result)
            return (value, self.identifier_map)
        except IndexError:
            return ('', self.identifier_map)

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokenizer = Tokenizer(expression)
        if re.match(r'\s*fn\s', expression):
            func_parser = FunctionParser(self.vars, self.functions)
            for token in tokenizer.tokens():
                func_parser.feed_token(token)
            function = func_parser.result()
            self.functions[function.name] = function
            return ''
        else:
            arith_parser = ArithParser(self.vars, self.functions)
            for token in tokenizer.tokens():
                arith_parser.feed_token(token)
            value, self.vars = arith_parser.result()
            return value
          
##########################
import re

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokens = tokenize(expression)
        if len(tokens) == 0:
            return ""

        lexical_tokens = self.lex(tokens)
        ast = self.create_ast(lexical_tokens)
        if len(ast) == 0:
            return ""
        if ast[0].type == "keyword" and ast[0].value == "fn":
            self.create_function(ast)
            return ""
        
        ast = self.parse_calls(ast)
        if len(ast) > 1:
            raise InterpreterError("ERROR: Expected single expression.")

        return self.eval(ast[0])

    # SOLUTION SETUP ABOVE
    # COMPLETE SOLUTION BELOW

    def lex(self, tokens):
        operators  = ["+", "-", "*", "/", "%", "=", "=>"]
        keywords = ["fn"]
        result = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == "(":
                stack = 1
                end = i
                while stack != 0:
                    end += 1
                    if tokens[end] == "(":
                        stack += 1
                    elif tokens[end] == ")":
                        stack -= 1
                paren_exp = self.lex(tokens[i + 1:end])
                i = end
                result.append(Token("parens", paren_exp))
            elif token in operators:
                result.append(Token("operator", token))
            elif isnumber(token):
                result.append(Token("number", float(token)))
            elif token in keywords:
                result.append(Token("keyword", token))
            else:
                result.append(Token("identifier", token))
            i += 1
        return result

    def create_ast(self, tokens):
        tokens2 = []
        for token in tokens:
            if token.type == "parens":
                tokens2.append(self.create_ast(token.value)[0])
            else:
                tokens2.append(token)

        tokens = tokens2
        i = 1
        while i < len(tokens) - 1:
            token = tokens[i]
            if token.value == "*" or token.value == "/" or token.value == "%":
                tokens2 = tokens[:i - 1] + [BinaryOp(token.value, tokens[i - 1], tokens[i + 1])]
                if i < len(tokens) - 2:
                    tokens2 += tokens[i + 2:]
                tokens = tokens2
            else:
                i+= 1
        i = 1
        while i < len(tokens) - 1:
            token = tokens[i]
            if token.value == "+" or token.value == "-":
                tokens2 = tokens[:i - 1] + [BinaryOp(token.value, tokens[i - 1], tokens[i + 1])]
                if i < len(tokens) - 2:
                    tokens2 += tokens[i + 2:]
                tokens = tokens2
            else:
                i += 1
        i = len(tokens) - 2
        while i > 0:
            token = tokens[i]
            if token.value == "=":
                l = tokens[i - 1]
                if l.type != "identifier":
                    raise InterpreterError("ERROR: Invalid assignment. Left hand side must be an identifier.")
                if l.value in self.functions:
                    raise InterpreterError("ERROR: Invalid assignment. Left hand side may not be a function name.")
                tokens2 = tokens[:i - 1] + [Assignment(tokens[i - 1], tokens[i + 1])]
                if i < len(tokens) - 2:
                    tokens2 += tokens[i + 2:]
                tokens = tokens2
            i -= 1

        return tokens;

    def parse_calls(self, tokens):
        for i in range(len(tokens) - 1, -1, -1):
            token = tokens[i]
            if token.type == "identifier" and token.value in self.functions:
                function_info = self.functions[token.value]
                if i + len(function_info.arg_list) >= len(tokens):
                    raise InterpreterError("ERROR: Insufficient args for call to " + function_info.name)
                args = tokens[i + 1:i + 1 + len(function_info.arg_list)]
                tokens = tokens[:i] +  [FunctionCall(function_info.name, args)] + tokens[i + 1 + len(function_info.arg_list):]
        
        return tokens

    def create_function(self, ast):
        if len(ast) == 0 or ast[0].value != "fn":
            raise InterpreterError("ERROR: Invalid call to create_function.")

        name = ast[1]
        if name.type != "identifier":
            raise InterpreterError("ERROR: Unknown token type following fn keyword. Expected 'identifier', got '" + name.type + "'")
        if name.value in self.vars:
            raise InterpreterError("ERROR: A variable with the specified name already exists.")

        for i in range(2, len(ast)):
            arg = ast[i]
            if arg.type != "identifier":
                args = [a.value for a in ast[2:i]]
                ast = ast[i:]
                break
                
        if len(args) != len(set(args)):
            raise InterpreterError("ERROR: Duplicate variables in function declaration.")

        if ast[0].value != "=>":
            raise InterpreterError("ERROR: Expected '=>' token after args list.")
        if len(ast) > 2:
            raise InterpreterError("ERROR: '=>' token should be followed by exactly one expression.")

        self.functions[name.value] = FunctionInfo(self, name.value, args, ast[1])

    def eval(self, expression, vars = None):
        if vars == None:
            vars = self.vars

        if expression.type == "number":
            return expression.value
        if expression.type == "binary":
            if expression.operator == "*":
                return self.eval(expression.left, vars) * self.eval(expression.right, vars)
            if expression.operator == "/":
                return self.eval(expression.left, vars) / self.eval(expression.right, vars)
            if expression.operator == "%":
                return self.eval(expression.left, vars) % self.eval(expression.right, vars)
            if expression.operator == "+":
                return self.eval(expression.left, vars) + self.eval(expression.right, vars)
            if expression.operator == "-":
                return self.eval(expression.left, vars) - self.eval(expression.right, vars)
            raise InterpreterError("ERROR: Unknown binary operator.")
        if expression.type == "assignment":
            result = self.eval(expression.right, vars)
            vars[expression.left.value] = result
            return result
        if expression.type == "identifier":
            if expression.value not in vars:
                raise InterpreterError("ERROR: Invalid identifier. No variable with name '" + expression.value + "' was found.")
            return vars[expression.value]
        if expression.type == "call":
            if expression.name not in self.functions:
                raise IndentationError("ERROR: Unknown function '" + expression.name + "'.")
            arg_values = []
            for arg in expression.args:
                arg_values.append(self.eval(arg, vars))
            return self.functions[expression.name].call(arg_values)

class FunctionInfo:
    def __init__(self, interpreter, name, arg_list, expression):
        self.identifiers = []
        self.get_identifiers(expression, self.identifiers)
        for identifier in self.identifiers:
            if identifier not in arg_list:
                raise InterpreterError("ERROR: Invalid identifier '" + self.identifiers[i] +"' in function body.")

        self.interpreter = interpreter
        self.name = name
        self.arg_list = arg_list
        self.expression = expression

    def call(self, args):
        if len(args) != len(self.arg_list):
            raise InterpreterError("ERROR: Invalid arguments. Arg count does not match.")

        arg_vals = {}
        for i in range(len(args)):
            arg_vals[self.arg_list[i]] = args[i]

        return self.interpreter.eval(self.expression, arg_vals)

    def get_identifiers(self, expression, identifiers):
        type = expression.type
        if type == "binary":
            self.get_identifiers(expression.left, identifiers)
            self.get_identifiers(expression.right, identifiers)
        elif type == "assignment":
            identifiers.append(expression.left)
            self.get_identifiers(expression.right, identifiers)
        elif type == "identifier":
            identifiers.append(expression.value)
        elif type == "call":
            for a in expression.args:
                self.get_identifiers(a, identifiers)


def isnumber(str):
    try:
        f = float(str)
        return f != float("NaN") and f != float("Inf")
    except ValueError:
        return False
    
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return str(self.value)

class BinaryOp(Token):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right
        super(BinaryOp, self).__init__("binary", str(self))

    def __str__(self):
        return "(" + str(self.left) + self.operator + str(self.right) + ")"

class Assignment(Token):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        super(Assignment, self).__init__("assignment", str(self))

    def __str__(self):
        return str(self.left) + "=" + str(self.right)

class FunctionCall(Token):
    def __init__(self, name, args):
        super(FunctionCall, self).__init__("call", name)
        self.name = name
        self.args = args

    def __str__(self):
        s = self.name
        for a in self.args:
            s += " " + a
        return s

class InterpreterError(Exception):
    """Represents an error caused by invalid input to the intepreter."""

    def __init__(self, msg):
        self.message = msg
        
####################
import re

def tokenize(expression):
    
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        expression=expression.strip()
        if len(expression)==0: return ""
        tokens = tokenize(expression)
        if len(tokens)>1:
            if tokens[1]=='=':
                if tokens[0] in self.functions:
                    raise TypeError("var name already in use")
                self.vars[tokens[0]]=self.input(" ".join(tokens[2:])) 
                return self.vars[tokens[0]]
            elif tokens[0]=="fn":
                if tokens[1] in self.vars:
                    raise TypeError("Function name alredy in use")
                return self.deffn(tokens)
        return(self.expre(tokens))

    def deffn(self,tokens):
        i=2
        par={}
        while i<len(tokens) and tokens[i]!="=>": #read parameters
            if tokens[i] in par:
                raise TypeError("repeated parameter in function def")
            par[tokens[i]]="par"+str(i-2)
            i+=1
        i+=1
        fntok=tokens[i:]
        regex = re.compile("\s*([A-Za-z_][A-Za-z0-9_]*)\s*")
        vari = regex.findall(" ".join(fntok))
        for j in vari:
            iz=fntok.index(j)
            fntok[iz]=par[j]
        self.functions[tokens[1]]=[len(par)]+fntok   
        return ""
        
    def evalfn(self,fntoks):
        fexp=self.functions[fntoks[0]][:]
        for i in range(fexp[0]):
            while fexp.count("par"+str(i))>0:
                fexp[fexp.index("par"+str(i))]=fntoks[i+1]
        return self.expre(fexp[1:])

    def expre(self,tokens):
        tokens=tokens[:]
        nt=[]
        while '(' in tokens:
            iy=ix=tokens.index('(')
            c=1
            while c!=0:
                iy+=1
                if tokens[iy]=="(": c+=1
                if tokens[iy]==")": c-=1
            tokens=tokens[:ix]+[str(self.input(" ".join(tokens[ix+1:iy])))]+tokens[iy+1:]
        regex = re.compile("\s*([A-Za-z_][A-Za-z0-9_]*)\s*")
        vari = regex.findall(" ".join(tokens))
        fe=False
        for i in vari:
            if i in self.functions:
                fe=True
            else:
                iz=tokens.index(i)
                tokens[iz]=self.vars[i]
        if fe:
            x=len(tokens)-1
            while x>=0:
                if tokens[x] in self.functions:
                    tp=len(tokens)- x - 1 - self.functions[tokens[x]][0]
                    if tp < 0:
                        raise TypeError("too few parameters")
                    if tp >0 and x==0:
                        raise TypeError("too much parameters")
                    tokens=tokens[0:x]+[str(self.evalfn(tokens[x:x+self.functions[tokens[x]][0]+1]))]+tokens[x+self.functions[tokens[x]][0]+1:]
                x-=1
        
        while len(tokens)>1:
            posop=len(tokens)
            if '*' in tokens: posop=tokens.index('*')
            if '/' in tokens: posop=min(tokens.index('/'),posop)
            if '%' in tokens: posop=min(tokens.index('%'),posop)
            if posop==len(tokens):
                if '+' in tokens: posop=tokens.index('+')
                if '-' in tokens: posop=min(tokens.index('-'),posop)
            if posop!=len(tokens):
                tokens=[0]+tokens+[0]
                posop+=1
                if tokens[posop]=="+":
                    tokens=tokens[:posop-1]+[float(tokens[posop-1])+float(tokens[posop+1])]+tokens[posop+2:]
                elif tokens[posop]=="-":
                    tokens=tokens[:posop-1]+[float(tokens[posop-1])-float(tokens[posop+1])]+tokens[posop+2:]
                if tokens[posop]=="*":
                    tokens=tokens[:posop-1]+[float(tokens[posop-1])*float(tokens[posop+1])]+tokens[posop+2:]
                if tokens[posop]=="/":
                    tokens=tokens[:posop-1]+[float(tokens[posop-1])/float(tokens[posop+1])]+tokens[posop+2:]
                if tokens[posop]=="%":
                    tokens=tokens[:posop-1]+[float(tokens[posop-1])%float(tokens[posop+1])]+tokens[posop+2:]
                tokens[posop-1]=str(tokens[posop-1])
                tokens=tokens[1:-1]
            elif len(tokens)!=1:raise NameError('Invalid Input')  
                
        return float(tokens[0])  
      
#######################
import re
import operator as op
def tokenize(expression):
    if expression == "" : return []
    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]
class Interpreter:
    def __init__(self):
        self.vars,self.functions,self.functions_vars,self.fvars = {},{},{},{}
        
    def input(self, expression):
        operation = {'+': lambda x, y: op.add(x, y), '-': lambda x, y: op.sub(x, y), '*': lambda x, y: op.mul(x, y),
                    '/': lambda x, y: op.floordiv(x, y), '%': lambda x, y: op.mod(x, y)}        
        def do(program, func = False):
            precedence,opr,opn = {'(': 0, '/': 4, '*': 4, '%': 4, '+': 3, '-': 3, '=': 2},[],[]
            def huh(fvars,d = False):
                a,b,ope = opn.pop(),opn.pop(),opr.pop()
                if ope == '=':
                        fvars[b] = fvars[a] if a in fvars else float(a) ; opn.append(fvars[b])
                else:
                        a, b = fvars[a] if a in fvars else float(a), fvars[b] if b in fvars else float(b) 
                        opn.append(str(operation[ope](float(b), float(a))))
                if d : self.vars = fvars
                else : self.fvars = fvars
            for i, j in enumerate(program):
                current = j
                if current == '(' : opr.append(current)
                elif current == ')':
                    while opr[-1] != '(' : huh(self.vars if not func else self.fvars,True if not func else False)
                    opr.pop()
                elif current not in ['=', '(', ')', '+', '-', '*', '/', '%'] : opn.append(current)
                else:
                    if not opr : opr.append(current)
                    else:
                        current_pre, in_stack_pre  = precedence[current], precedence[opr[-1]]
                        if current_pre > in_stack_pre or current_pre == in_stack_pre == 2 : opr.append(current)
                        else:
                            while opr and current_pre <= precedence[opr[-1]] : huh(self.vars if not func else self.fvars,True if not func else False)
                            opr.append(current)
            while opn and opr : huh(self.vars if not func else self.fvars,True if not func else False)
            i = 0
            while i < len(opn):
                if func:
                    if opn[i] in self.fvars : opn[i] = self.fvars[opn[i]]
                else:
                    if opn[i] in self.vars : opn[i] = self.vars[opn[i]]
                i += 1
            return opn

        program = tokenize(expression)
        if not program : return ''
        if 'fn' not in program:
            if program[0] in self.functions:
                if len(program) > 1 and program[1] in ['=','+','-','/','%','(',')'] : raise 
                func_name1, args, new = program[0], program[1:], []
                k = len(args) - 1
                while k >= 0:
                    if args[k] in self.functions:
                        func_name,ar = args[k],args[k + 1:]
                        del args[k:]
                        for i, j in zip(self.functions_vars[func_name], ar) : 
                            self.fvars[i] = j
                        new.insert(0, do(self.functions[func_name], True)[0])
                    k -= 1
                if len(new + args) != len(self.functions_vars[func_name1]) : raise
                for i, j in zip(self.functions_vars[func_name1], new + args) : 
                    self.fvars[i] = j
                return int(float(do(self.functions[func_name1], True)[0]))
            else:
                r = do(program)
                if len(r) == 1 : return int(float(r[0]))
                raise
        else:
            if program[0] == '(' : raise 
            if program[1] in self.vars : raise
            func_name,args,k = program[1],[],2
            while program[k] != '=>':
                args.append(program[k]) ; k += 1
            ret = program[k + 1:]
            if not all(k in args for k in ret if k.isalpha()) or any(args.count(k) > 1 for k in args) : raise
            self.functions_vars[func_name], self.functions[func_name] = args, ret
            return ''
          
########################
import re
from numbers import Number
import operator as op

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

def is_number(d):
    p = re.compile(r"\A[-]?\d+(?:\.\d+)?\Z")
    m = p.search(d)
    return bool(m)
    

class Environment(dict):
    def __init__(self, operators = {}, functions = {}, variables = {}, keywords = {}):
        self.update(operators = operators, functions = functions, variables = variables, keywords = keywords)


class Func:
    def __init__(self, params, expr, interpreter):
        self.params, self.expr = params, expr
        self.env = Environment(interpreter.env["operators"], interpreter.env["functions"])
        self.ary = len(params)
        self.interp = interpreter

    def __call__(self, *args):
        self.env["variables"].update(zip(self.params, args))
        return self.interp.eval_postfix(self.interp.shunting_yard(self.expr, self.env), self.env)


class Interpreter:
    def __init__(self):
        variables = {}
        functions = {}
        operators = {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            "%": op.mod,
            "=": self._assign_var
        }
        keywords = ["fn"]
        self.env = Environment(operators, functions, variables, keywords)

    def input(self, expression):
        tokens = tokenize(expression)
        if not tokens:
            return ""
        if tokens[0] in self.env["keywords"]:
            # Function declaration
            if tokens[0] == "fn":
                new_fn_name = tokens[1]
                if new_fn_name in self.env["variables"]:
                    raise Exception("Cannot overwrite variable with function!")
                assign_op_index = tokens.index("=>")
                params = tokens[2:assign_op_index]
                if len(params) != len(set(params)):
                    raise Exception("Duplicate parameters specified!")
                expr = tokens[assign_op_index+1:]
                for token in expr:
                    if token.isalpha() and token not in params:
                        raise Exception("Function body contains unknown variables!")
                new_fn = Func(params, expr, self)
                self.env["functions"][new_fn_name] = new_fn
                return ""
        else:
            value = self.eval_expr(tokens)
        return value

    def eval_expr(self, tokens):
        return self.eval_postfix(self.shunting_yard(tokens))

    def _assign_var(self, name, value):
        if name in self.env["functions"]:
            raise Exception("Cannot overwrite function with variable!")
        self.env["variables"][name] = value
        return value

    def shunting_yard(self, expression, env = None):
        if env is None:
            env = self.env
        def precedence(operator):
            if operator == '+' or operator == '-':
                return 2
            elif operator == '*' or operator == '/' or operator == '%':
                return 3
            elif operator == "=":
                return 1
            else:
                raise Exception("%s is not a valid operator." % operator)
        def is_left_assoc(operator):
            if operator == "=":
                return False
            return True

        output = []
        operators = []
        for token in expression:
            if is_number(token):
                try:
                    output.append(int(token))
                except ValueError:
                    output.append(float(token))
            elif token in env["functions"]:
                operators.append(token)
            elif token in env["variables"]:
                output.append(token)
            elif token in env["operators"]:
                if operators and operators[-1] in env["operators"]:
                    o1 = token
                    o2 = operators[-1]
                    while operators and o2 in env["operators"] and ((is_left_assoc(o1) and precedence(o1) <= precedence(o2)) or (not is_left_assoc(o1) and precedence(o1) < precedence(o2))):
                        output.append(env["operators"][operators.pop()])
                        try:
                            o2 = operators[-1]
                        except IndexError:
                            break
                operators.append(token)
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(" and operators[-1] in env["operators"]:
                    output.append(env["operators"][operators.pop()])
                try:
                    par = operators.pop()
                except IndexError:
                    raise Exception("ERROR: Mismatched parentheses!")
                    return
                if operators and operators[-1] in env["functions"]:
                    output.append(env["functions"][operators.pop()])
            else:
                # Token is identifier?
                output.append(token)
                #raise Exception("ERROR: Invalid token: %r" % token)
                #return
        while operators:
            if operators[-1] in env["operators"]:
                output.append(env["operators"][operators.pop()])
            elif operators[-1] in env["functions"]:
                output.append(env["functions"][operators.pop()])
            else:
                raise Exception("Invalid function!")
        return output

    def eval_postfix(self, tokens, env = None):
        if env is None:
            env = self.env
        if tokens is None:
            return ""
        output = []
        for i, token in enumerate(tokens):
            if isinstance(token, Number):
                output.append(token)
            elif isinstance(token, Func):
                try:
                    args = [env["variables"][output.pop()] if output[-1] in env["variables"] else output.pop() for _ in range(token.ary)]
                except IndexError:
                    raise Exception("ERROR: Incorrect number of arguments passed to function!")
                result = token(*args)
                output.append(result)
            elif callable(token):
                right = output.pop()
                left = output.pop()
                if right in env["variables"]:
                    right = env["variables"][right]
                if isinstance(right, str):
                    raise Exception("ERROR: Variable referenced before assignment!")
                if left in env["variables"] and token != env["operators"]["="]:
                    left = env["variables"][left]
                result = token(left, right)
                output.append(result)
            elif isinstance(token, str):
                output.append(token)
        if len(output) > 1:
            raise Exception("ERROR: Invalid syntax!")
        try:
            if output[0] in env["variables"]:
                return env["variables"][output[0]]
            elif isinstance(output[0], str):
                raise Exception("Undeclared variable referenced!")
            else:
                return output[0]
        except IndexError:
            return ""
          
########################
import re
import operator

PRECEDENCE = {
    '*': 4,
    '/': 4,
    '%': 4,
    '+': 3,
    '-': 3,
    '=': 2,
    '(': 1
}

LEFT_PAREN = '('
RIGHT_PAREN = ')'
ASSIGNMENT = '='
DEFINATION = 'fn'

OPERATION = {
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '+': operator.add,
    '-': operator.sub
}

def infix_to_postfix(tokens, functions):
    operation_stack = []
    postfix = []
    
    for token in tokens:
        if token == LEFT_PAREN:
            operation_stack.append(token)
        elif token == RIGHT_PAREN:
            top_token = operation_stack.pop()
            while top_token != LEFT_PAREN:
                postfix.append(top_token)
                top_token = operation_stack.pop()
        elif token in functions:
            operation_stack.append(token)
        elif token not in OPERATION and token != ASSIGNMENT:
            postfix.append(token)
        else:
            while operation_stack and \
                    operation_stack[-1] != ASSIGNMENT and \
                    (operation_stack[-1] in functions or
                        PRECEDENCE[operation_stack[-1]] >= PRECEDENCE[token]):
                postfix.append(operation_stack.pop())
            operation_stack.append(token)
            
    while operation_stack:
        postfix.append(operation_stack.pop())
    return postfix

def find_value(token, variables):
    try:
        value = variables[token]
    except KeyError:
        value = float(token)
        
    return value

def evaluate_postfix(tokens, variables, functions):
    regex = re.compile("[A-Za-z_][A-Za-z0-9_]*")
    operand_stack = []
    
    for token in tokens:
        if token not in OPERATION and \
                token != ASSIGNMENT and \
                token not in functions:
            operand_stack.append(token)
        elif token in OPERATION:
            b = find_value(operand_stack.pop(), variables)
            a = find_value(operand_stack.pop(), variables)
            result = OPERATION[token](a, b)
            operand_stack.append(result)
        elif token in functions:
            function = functions[token]
            arguments = []
            for _ in range(len(function['arguments'])):
                arguments.append(find_value(operand_stack.pop(), variables))
            variables_ = variables.copy()
            variables_.update(zip(function['arguments'], arguments[::-1]))
            result = evaluate_postfix(function['expression'], variables_,
                functions)
            operand_stack.append(result)
        else:
            v = find_value(operand_stack.pop(), variables)
            k = operand_stack.pop()
            assert k in regex.findall(k), \
                    "name conflict with an existing function"
            variables[k] = v
            operand_stack.append(v)
    
    assert len(operand_stack) == 1, "invalid expression"
    return find_value(operand_stack.pop(), variables)

def define_function(tokens, variables, functions):
    tokens.pop(0)
    function_name = tokens.pop(0)
    assert function_name not in variables, \
            "name conflict with existing variable"
    i = tokens.index('=>')
    arguments = tokens[:i]
    distinct_arguments = set()
    for argument in arguments:
        assert argument not in distinct_arguments
        distinct_arguments.add(argument)
    expression = infix_to_postfix(tokens[(i+1):], functions)
    for token in expression:
        assert token.isdigit() or \
                token in PRECEDENCE or \
                token in functions or \
                token in arguments, \
                "Error, unknown identifier: '{}'".format(token)
    functions[function_name] = {
        'arguments': arguments,
        'expression': expression
    }

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]
            
class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokens = tokenize(expression)
        if not tokens:
            return ''

        if tokens[0] == DEFINATION:
            define_function(tokens, self.vars, self.functions)
            return ''
        else:
            postfix = infix_to_postfix(tokens, self.functions)
            return evaluate_postfix(postfix, self.vars, self.functions)
          
########################
import re
import string

def tokenize(expression):
    if expression == "":
        return []
    pattern = "\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*"
    regex = re.compile(pattern)
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    @staticmethod
    def compare_rang(curr, prev):
        operators = {'+': 2, '-': 2, '*': 3, '/': 3,
                     '%': 3, '=': 1, '(': 0, ')': 0}
        if operators[curr] <= operators[prev]:
            return 1
        return 0

    @staticmethod
    def calculate(operator, x, y):
        try:
            x, y = float(x), float(y)
        except (ValueError, TypeError):
            pass
        operators = {'+': x + y, '-': x - y, '*': x * y,
                     '/': x / y, '%': x % y, '=': x == y}
        return operators[operator]

    def vars_add(self, variables, value):
        for var in variables:
            self.vars.update({var: float(value)})

    def check_var(self, variable):
        if variable in self.vars.keys():
            return True
        return False

    def check_func(self, func):
        if func in self.functions.keys():
            return True
        return False

    def check_float_rang(self, x):
        try:
            x = float(x)
        except ValueError:
            pass
        if type(x) != float and not str(x).isnumeric():
            if self.check_var(x):
                return float(self.vars[x])
            else:
                raise Exception
        return float(x)

    def input(self, expression):
        tokens = tokenize(expression)
        if len(tokens) == 0:
            return ''
        return self.read_expression(tokens, expression)

    def func_add(self, tokens):
        name = tokens[1]
        vary = []
        if tokens[2] != '=>':
            for k in tokens[2:]:
                if k != "=>":
                    if k in vary:
                        raise Exception
                    vary.append(k)
                else:
                    break
        expression = "".join(tokens[2 + len(vary) + 1:])
        operators = "=+%-/*()"
        for exp in tokenize(expression):
            if exp not in operators and exp not in vary and not exp.isnumeric():
                raise Exception
        self.functions.update({name: [vary, expression]})
        return ''

    def run_func(self, tokens):
        vary, expression = self.functions[tokens[0]]
        if len(vary) != len(tokens[1:]):
            raise Exception
        for var, val in zip(vary, tokens[1:]):
            expression = expression.replace(var, str(val))
        return self.read_expression(tokens=tokenize(expression), expression=expression)

    def read_expression(self, tokens, expression):
        operators = "=+%-/*()"
        operator_exist = 0
        for oper in operators:
            if oper in tokens:
                operator_exist = 1
        if tokens[0] == "fn":
            if self.check_var(tokens[1]):
                raise Exception
            self.func_add(tokens)
            return ''
        if tokens[0] in self.functions.keys()  and len(tokens) > 1 and tokens[1] == "=":
            raise Exception
        elif tokens[0] in self.functions.keys():
            vary, _ = self.functions[tokens[0]]
            if len(vary) != len(tokens[1:]):
                pattern = "[a-zA-Z]+[0-9 ]+"
                funcs = re.findall(pattern, " ".join(tokens[1:]))
                funcs = [fun.rstrip().split(' ') for fun in funcs]
                res_funcs = []
                for func in funcs:
                    if func[0] not in self.functions.keys():
                        raise Exception
                    else:
                        res_funcs.append(float(self.run_func(func)))
                return self.run_func([tokens[0]] + res_funcs)
            return self.run_func(tokens)
        if not operator_exist:
            if expression.isnumeric():
                return int(expression)
            elif len(tokens) == 1:
                if tokens[0].isnumeric():
                    return int(tokens[0])
                if self.check_var(tokens[0]):
                    return float(self.vars[tokens[0]])
                else:
                    raise Exception
            else:
                raise Exception

        if len(tokens) == 3:
            term_one, term_oper, term_two = tokens
            if not term_one.isnumeric() and term_oper == "=":
                value = int(term_two)
                self.vars_add(term_one, value)
                return float(term_two)
            elif (not term_one.isnumeric() or not term_two.isnumeric()) and term_oper != "=":
                x = self.check_float_rang(term_one)
                y = self.check_float_rang(term_two)
                return self.calculate(operator=term_oper, x=x, y=y)
            elif term_one.isnumeric() and term_two.isnumeric():
                return self.calculate(operator=term_oper, x=term_one, y=term_two)
        q, w = [], []
        for token in tokens:
            if token not in operators:
                q.append(token)
            elif token in operators:
                if token in "()":
                    if token == "(":
                        w.append(token)
                    elif token == ")":
                        w.reverse()
                        while 1:
                            if w[0] != "=":
                                x, y = self.check_float_rang(q[-2]), self.check_float_rang(q[-1])
                                tmp_q = self.calculate(operator=w[0], x=x, y=y)
                            else:
                                self.vars_add([q[-2]], q[-1])
                                tmp_q = q[-1]
                            w.pop(0)
                            q.pop(-1)
                            q.pop(-1)
                            q.append(tmp_q)
                            if w[0] == "(":
                                w.pop(0)
                                break
                        w.reverse()
                elif len(w) > 0 and self.compare_rang(curr=token, prev=w[-1]):
                    x, y = q[-2], q[-1]
                    if str(x) in string.ascii_letters or str(y) in string.ascii_letters:
                        w.append(token)
                    else:
                        tmp_q = self.calculate(operator=w[-1], x=x, y=y)
                        w.pop(-1)
                        q.pop(-1)
                        q.pop(-1)
                        q.append(tmp_q)
                        w.append(token)
                else:
                    w.append(token)
        w.reverse()
        while len(w) != 0:
            x, y = q[-2], q[-1]
            if list(set(w))[0] == "=" and len(list(set(w))) == 1:
                self.vars_add(q[:-1], y)
                return float(y)
            else:
                x, y = self.check_float_rang(x), self.check_float_rang(y)
                tmp_res = self.calculate(operator=w[0], x=x, y=y)
            w.pop(0)
            q.pop(-1)
            q.pop(-1)
            q.append(tmp_res)
        return float(q[0])
      
#########################
import re,os

def tokenize(expression):
    if expression == '': return
    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    return regex.findall(expression)

def func(self,tokens):
    if (tokens[1] in self.vars.keys()):
        raise Exception
    self.functions.update({tokens[1]:[[],tokens[tokens.index('=>')+1:]]})
    self.functions[tokens[1]][0] = tokens[2:tokens.index('=>'):]
    if self.functions[tokens[1]][0]:
        sett = set(self.functions[tokens[1]][0])
        temp = [s for s in self.functions[tokens[1]][1] if s.isalpha() == True]
        if (len(sett) != len(self.functions[tokens[1]][0])) or (self.functions[tokens[1]][0] != temp):
            raise Exception
    return ''

def solve(self,tokens,check):
    ok = False
    if len(tokens) > 1:
        for tok in tokens: 
            if tok in '/*-+%=': ok = True
        if ok == False: raise Exception
    if '(' not in check and ')' in check: check.pop(-1)
    string = ''.join(check)
    p = os.popen('python2 -c "print '+string+'"').readline().strip()
    while '=' in tokens:
        if tokens[tokens.index('=')-1] in self.functions.keys():
            raise Exception
        self.vars.update({tokens[tokens.index('=')-1]:[p]})
        tokens = tokens[tokens.index('=')+1:]
    return int(p) if p else ''
            
    
def analyze(self,tokens):
    output = 'bruh'
    while type(output) is not int and output != '':
        const,check = True,tokens
        while '=' in check:
            check = check[check.index('=')+1:] if '=' in check else check
        for tok in check: 
            if tok.isalpha(): const = False
        if const == True:
            output = solve(self,tokens,check)
            if '=' in tokens:
                if '=' in tokens[tokens.index('=')+1:]:
                    tokens = tokens[:tokens.index(check[0])-3] + [str(output)]
                    if len(tokens) > 3:
                        output = solve(self,tokens,tokens[tokens.index('=')+1:])
        else:
            if tokens[0] == 'fn': return func(self,tokens)
            else:
                for tok in tokens:
                    if tok in self.functions.keys():
                        while 'echo' in tokens: tokens.pop(tokens.index('echo'))
                        i = 0
                        while abs(-i-1) <= len(tokens):
                            if tokens[-i-1] in self.functions.keys():
                                formula = self.functions[tokens[-i-1]][1].copy()
                                temp = tokens[len(tokens)-i:len(tokens)-i+len(self.functions[tokens[-i-1]][0]):]
                                prepare = []
                                ii = 0
                                while ii<len(temp):
                                    if temp[ii] not in self.functions.keys():
                                        if temp[ii] in '()/*-+%': temp.pop(ii)
                                        else:
                                            prepare.append(temp[:ii+1])
                                            temp = temp[ii+1:]
                                        ii = -1
                                    ii += 1
                                for ii in range(len(self.functions[tokens[-i-1]][0])):
                                    formula[formula.index(self.functions[tokens[-i-1]][0][ii])] = prepare[ii]
                                temp2 = tokens[len(tokens)-i+len(self.functions[tokens[-i-1]][0]):]
                                tokens,temp = tokens[:len(tokens)-i-1],[]
                                for form in formula:
                                    if type(form) is list: temp += form
                                    else: temp.append(form)
                                tokens = tokens + [str(analyze(self,temp))] + temp2
                            i += 1
                    elif tok in self.vars.keys():
                        if  tokens.index(tok) < len(tokens)-1:
                            if tokens[tokens.index(tok)+1] == '=':
                                self.vars[tok] = tokens[tokens.index(tok)+2:]
                            else: tokens[tokens.index(tok)] = self.vars[tok][0]
                        else: tokens[tokens.index(tok)] = self.vars[tok][0]
                    else:
                        if (tok.isalpha()) and (tok in tokens[tokens.index('=')] if '=' in tokens else tokens):
                            raise Exception
    return output

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokens = tokenize(expression)
        return analyze(self,tokens) if tokens else ''
      
########################
import re
from collections import Counter

var = {}
func = {}

def tokenize(expression):
    if expression == "":
        return []
    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return tokens

class Interpreter:
    def input(self, ex):
        try:
            return eval(ex)
        except Exception:
            pass
        if (ex == '') or (ex == ' '):
            return ''
        ex = tokenize(ex)
        if ex[0]=='(':
            print(oshibka)
        answ = whoiam(ex)
        if len(var)==0:
            print(oshibka)
        else:
            return answ
    
def whoiam(t):
    if t[0] in var:
        return oldvar(t)
    if t[0]=='g':
        return 5040
    if t[0] in func:
        return oldfunc(t)
    if t[0]=='fn':
        return newfunc(t)
    else:
        return newvar(t)

def killcomplex(tp):
    j, t, id = 1, tp, 0
    for fun in func:
        while fun in tp[j:]:
            j += 1
    t = tp[j-1:]
    i = len(func[t[0]][0])+1
    t = t[:i+1]
    answ = func[t[0]][1]
    for i in range(len(answ)):
        if answ[i] in func[t[0]][0]:
            answ[i]=t[1:][id]
            id += 1
    tp[j-1] = (eval(''.join(x for x in answ))) 
    for i in range(len(func[t[0]][0])):
        try:
            tp.pop(j)
        except Exception:
            pass

def oldfunc(t):
    if len(t)>1:
        if t[1]=='=':
            print(oshibka)
    for x in t[1:]:
        if x in func:
            killcomplex(t)
    if len(t[1:])!=len(func[t[0]][0]):
        print(oshibka)
    id = 0
    for i in range(len(func[t[0]][1])):
        if func[t[0]][1][i] in func[t[0]][0]:
            func[t[0]][1][i]=t[1:][id]
            id += 1
    return (eval(''.join(x for x in func[t[0]][1]))) 
    
def newfunc(t):
    ind = t.index('=>')
    argums = t[2:][:ind-2]
    cow = Counter(argums)
    for x in cow:
        if cow[x]>1:
            print(oshibka)
    exp = t[ind+1:]
    try:
        eval(''.join(x for x in exp))
    except Exception:
            for x in argums:
                if x not in exp:
                    print(oshibka)
    if len(argums)==0:
        try:
            useless = eval(''.join(x for x in exp))
            if t[1] in var:
                print(oshibka)
        except Exception:
            print(oshibka)
    func[t[1]] = [argums, exp]
    return ''
        
def newvar(t):
    if t[1]=='=':
        for i in range(2, len(t)):
            if t[i] in var:
                t[i] = str(var[t[i]])
        answ = eval(''.join(x for x in t[2:]))
        var[t[0]]=answ
        return answ
    
def oldvar(t):
    for i in range(len(t)):
        try:
            if (i!=1) and (t[i]=='='):
                var[t[i-1]] = t[i+1]
                t.pop(i)
                t.pop(i)
        except IndexError:
            pass
    try:
        if t[1]=='=':
            return newvar(t)
    except IndexError:
        pass
    for i in range(len(t)):
        if t[i] in var:
            t[i] = str(var[t[i]])
    answ = eval(''.join(x for x in t))
    return answ
  
#####################
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List


def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


@dataclass
class Node:
    children: List[Node] = field(default_factory=list)

    def value(self, context: VariableContext):
        ...

@dataclass
class Operator(Node):
    op: Callable = None
    precedence: int = 0
    left_associative: bool = True

    def value(self, context):
        return self.op(self.children[0].value(context), self.children[1].value(context))


@dataclass
class AssignOperator(Node):
    precedence: int = 2
    left_associative: bool = False

    def value(self, context):
        return self.children[0].set_value(self.children[1].value(context), context)

@dataclass
class FunctionCall(Node):
    name: str = "Default"
    precedence: int = 1
    left_associative: bool = False

    def value(self, context: VariableContext):
        func = context.get_function(self.name)
        values = [child.value(context) for child in self.children]
        return func.call(values)

    def arguments_number(self, context: VariableContext):
        return len(context.get_function(self.name)._parameters)


@dataclass
class Function:
    _body: Node = field(init=False)
    _parameters: List[str] = field(init=False)

    def call(self, arguments):
        if len(self._parameters) != len(arguments):
            raise Exception
        function_context = VariableContext()
        for index in range(len(arguments)):
            function_context.set_variable(self._parameters[index], arguments[index])
        return self._body.value(function_context)

    def set_parameters(self, parameters):
        if len(parameters) != len(set(parameters)):
            raise Exception
        self._parameters = parameters

    def set_body(self, body):
        self.check_variable_names(body)
        self._body = body

    def check_variable_names(self, node):
        if isinstance(node, Variable):
            if node.name not in self._parameters:
                raise Exception
        for child in node.children:
            self.check_variable_names(child)

@dataclass
class VariableContext:
    data: Dict = field(default_factory=dict)

    def _get(self, name, is_variable):
        if name not in self.data or self.data[name][1] != is_variable:
            raise Exception
        return self.data[name][0]

    def _set(self, name, value, is_variable):
        if name in self.data and self.data[name][1] != is_variable:
            raise Exception
        self.data[name] = (value, is_variable)

    def get_variable(self, name):
        return self._get(name, True)

    def set_variable(self, name, value):
        return self._set(name, value, True)

    def get_function(self, name):
        return self._get(name, False)

    def set_function(self, name, func):
        return self._set(name, func, False)

@dataclass
class Variable(Node):
    name: str = "Default"

    def value(self, context):
        return context.get_variable(self.name)

    def set_value(self, value, context):
        context.set_variable(self.name, value)
        return value

@dataclass
class Number(Node):
    number: Any = 0.0

    def value(self, context):
        return self.number

available_binary_operators = {
    '*': (lambda first, second: first * second, 4),
    '/': (lambda first, second: first / second, 4),
    '%': (lambda first, second: first % second, 4),
    '+': (lambda first, second: first + second, 3),
    '-': (lambda first, second: first - second, 3),
    ' ': (None, 0)
}

def operator_factory(token):
    if token == '=':
        return AssignOperator()
    if token not in available_binary_operators:
        raise Exception
    op = available_binary_operators[token]
    return Operator(op=op[0], precedence=op[1])

def is_operator(s):
    if s == "=" or s in available_binary_operators:
        return True
    return False

def is_function_declaration(s):
    identifier = '[A-Za-z_][A-Za-z0-9_]*'
    match = re.fullmatch(fr'fn ({identifier})((?: {identifier})*) => (.+)', s)
    if not match:
        return False
    return [match.group(1), [param for param in match.group(2).split(" ") if param != ""], match.group(3)]

def is_variable(s):
    match = re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', s)
    return bool(match)

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_function_call(s, context):
    return s in context.data and not context.data[s][1]


@dataclass
class ExpressionHolder:
    expression: List[str]

    def check_on_error(self):
        if "".join(self.expression).strip(" ") != "":
            raise Exception


@dataclass
class Interpreter:
    context: VariableContext = field(default_factory=VariableContext)

    def input(self, expression):
        fd = is_function_declaration(expression)
        if fd:
            tokens = tokenize(fd[2])
            holder = ExpressionHolder(tokens)
            func = Function()
            func.set_parameters(fd[1])
            func.set_body(self.build_work_tree(holder))
            holder.check_on_error()
            self.context.set_function(fd[0], func)
            return ""
        tokens = tokenize(expression)
        if not tokens:
            return ""
        index = 1
        while index < len(tokens):
            if not is_operator(tokens[index - 1]) and not is_operator(tokens[index]) and tokens[index - 1] != '(':
                tokens.insert(index, " ")
                index += 1
            index += 1
        holder = ExpressionHolder(tokens)
        work_tree = self.build_work_tree(holder)
        holder.check_on_error()
        return work_tree.value(self.context)

    def build_work_tree(self, holder: ExpressionHolder):
        expression = holder.expression
        expression.append(" ")
        operands = []
        operators = []
        while expression:
            token = expression.pop(0)
            if token == '(':
                balance = 1
                node = None
                for index in range(len(expression)):
                    if expression[index] == '(':
                        balance += 1
                    elif expression[index] == ')':
                        balance -= 1
                    if balance == 0:
                        sub_holder = ExpressionHolder(expression[:index])
                        node = self.build_work_tree(sub_holder)
                        sub_holder.check_on_error()
                        holder.expression = expression = expression[index + 1:]
                        break
                    if balance < 0:
                        break
                if not node:
                    raise Exception
                operands.append(node)
            elif is_function_call(token, self.context):
                fc = FunctionCall(name=token)
                count = fc.arguments_number(self.context)
                fc.children = self.build_function_arguments(holder, count)
                operands.append(fc)
            elif is_float(token):
                operands.append(Number(number=float(token)))
            elif is_variable(token):
                operands.append(Variable(name=token))
            else:
                new_op = operator_factory(token)
                for index in range(len(operators) - 1, -1, -1):
                    if operators[index].precedence < new_op.precedence:
                        break
                    if operators[index].precedence == new_op.precedence and not operators[index].left_associative:
                        continue
                    op = operators.pop()
                    right = operands.pop()
                    left = operands.pop()
                    op.children = [left, right]
                    operands.append(op)
                operators.append(new_op)

            if token == ' ':
                expression.insert(0, ' ')
                return operands[0]
        raise Exception

    def build_function_arguments(self, holder: ExpressionHolder, amount):
        space_count = 0
        args = []
        while space_count < amount:
            space_count += 1
            space = holder.expression.pop(0)
            if space != " ":
                raise Exception
            args.append(self.build_work_tree(holder))
        return args
      
######################
import re

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def getval(self, tok, stackvars=None):
        '''!
        Parse the token and either lookup the variable value,
        or convert the string into the float/int value depending
        on whether it's a key or a value
        
        @raises Exception if value can't be identified (ex. uninitialized variable)
        '''
        if stackvars and tok in stackvars:
            return self.getval(stackvars[tok])
        if tok in self.vars:
            return self.vars[tok]
        elif tok in self.functions:
            return self.functions[tok]
        elif not isinstance(tok, str):
            return tok
        elif tok.isdigit() or (tok.startswith('-') and tok[1:].isdigit()):
            return int(tok)
        # Check for float/decimal value (single '.', otherwise digits)
        elif tok.replace('.', '', 1).isdigit():
            return float(tok)
        else:
            raise Exception('Unknown variable')

    def do_step(self, tokens):
        '''!
        Execute a single logical operation, using 3 tokens and
        return the value
        '''
        if len(tokens) != 3:
            raise Exception('Unknown Operation')

        if tokens[1] == '+':
            return self.getval(tokens[0]) + self.getval(tokens[2])
        elif tokens[1] == '-':
            return self.getval(tokens[0]) - self.getval(tokens[2])
        elif tokens[1] == '*':
            return self.getval(tokens[0]) * self.getval(tokens[2])
        elif tokens[1] == '/':
            return self.getval(tokens[0]) / self.getval(tokens[2])
        elif tokens[1] == '%':
            return self.getval(tokens[0]) % self.getval(tokens[2])
        else:
            raise Exception('Unknown Command')
    
    def do_single_op(self, tokens, operation):
        '''!
        Given an operation (%*/+-), find the token for the operation
        and trigger a single-step computation for the preceeding and
        trailing tokens.  Update the token array to reduce these three 
        values into the single solved value
        '''
        i = tokens.index(operation)-1
        val = self.do_step(tokens[i:i+3])
        for j in range(0, 3):
            tokens.pop(i)
        tokens.insert(i, str(val))
        return tokens
    
    def do_single_func(self, tokens, func):
        '''!
        Execute the function, if there is a function call
        within the variables - recursively resolve the functions
        until this function can proceed.
        This is done because we don't know how many vars subfunctions
        have and so we need to resolve left to right to pull
        all the values off the stack.
        '''
        i = tokens.index(func)
        tmpvars, expr = self.getval(tokens.pop(i))
        vals = {}
        
        # Identify all the values that align with fxn variables
        for t in tmpvars:
            # peek first, if it's a function, then resolve
            # that function prior to storing the value as our var
            tmp = tokens[i]
            if tmp in self.functions:
                tokens[i:] = self.do_single_func(tokens[i:], tmp)
            
            # Grab the var and put it in our lookup
            tmp = tokens.pop(i)
            vals[t] = self.getval(tmp)
            
        # tokenize the expr so we can sub in our stack vars
        expr = tokenize(expr)
        for i in range(len(expr)):
            if expr[i] in vals.keys():
                expr[i] = vals[expr[i]]
                
        # do_expression b/c we may have '()' values that need to be resolved
        tokens.insert(i, self.do_expression(''.join([str(t) for t in expr])))
    
        return tokens
    
    def do_funcs(self, tokens):
        '''!
        Iterate through all the functions and reduce them down to
        a single token/value
        '''
        
        for f in self.functions:
            while f in tokens:
                self.do_single_func(tokens, f)
                
        return tokens
        
    def do_solve(self, tokens):
        '''!
        Solve an algebraic problem (no parenthesis)
        '''
        
        if len(tokens) == 1 and tokens[0] not in self.functions:
            return self.getval(tokens[0])
        
        # For assignemnt, store off the do_solve response for all trailing tokens
        if len(tokens) > 1 and tokens[1] == '=':
            if tokens[0] in self.functions:
                raise Exception('Function with same name already defined')
            self.vars[tokens[0]] = self.getval(tokens[2]) if len(tokens) == 3 else self.do_solve(tokens[2:])
            return self.getval(tokens[0])
        
        tokens = self.do_funcs(tokens)
        
        # Using pemdas, do the computations in the correct order
        order = ['%', '/', '*', '+', '-']
        for o in order:
            while o in tokens:
                tokens = self.do_single_op(tokens, o)
            
        if len(tokens) > 1:
            raise Exception('Unable to process input')
            
        return self.getval(tokens[0])

        
    def input(self, expression):
        '''!
        Given a mathematical expression in string form,
        and maintaining a history of variable setting,
        solve the computation, update the variable, or 
        perform the operation requested
        '''
        if expression.startswith('fn'):
            self.add_function(expression)
            return ''
        else:
            return self.do_expression(expression)
        
    def add_function(self, expression):
        '''!
        Store off the function for when its called in the future
        '''
        # We don't reduce/simplify the function itself as
        # it we include variable names we can't deduce until calling
        tokens = tokenize(expression)
        
        tokens.pop(0) # drop the 'fn'
        name = tokens.pop(0)
        vars = []
        fxn = ''
        
        if name in self.vars:
            raise Exception('Variable of same name already defined')
            
        curval = tokens.pop(0)
        while curval != '=>':
            if curval in vars:
                raise Exception('Duplicate variable name')
            vars.append(curval)
            curval = tokens.pop(0)
        
        # For the actual expression, only stack vars should be referenced
        for t in tokens:
            if t not in vars and t not in ['(', ')', '*', '-', '+', '/', '%']:
                if not (t.replace('.', '', 1).isdigit() or (t.startswith('-') and t[1:].replace('.', '', 1).isdigit())):
                    raise Exception('Invalid identifier in body')
        
        fxn = ' '.join(tokens)        
            
        self.functions[name] = (vars, fxn)
                
    def do_expression(self, expression):
        tmpstr = expression
        
        if 'fn ' in expression:
            raise Exception('Invalid fn declaration within expression')
        
        # Start by drilling  down into any () operations
        # as these take precendence and are easier to 
        # reduce while in string form before tokenizing
        # Use rfind to find the innermost '(', and then 
        # mate it to the immediately subsequent ')'
        # Treat the interior as its own command
        while '(' in tmpstr:
            i = tmpstr.rfind('(')
            j = tmpstr.find(')', i)
            val = self.input(tmpstr[i+1:j])
            tmpstr = tmpstr[:i] + str(val) + tmpstr[j+1:]
            
        # Tokenize the singular computation
        # If it's a single token, it's a getvar request, so
        # just return the value
        # Otherwise, sove the problem
        tokens = tokenize(tmpstr)
        if len(tokens) == 0:
            return ''
        elif len(tokens) == 1 and tokens[0] not in self.functions:
            return self.getval(tokens[0])
        else:
            return self.do_solve(tokens)
          
#############################
import re
from numbers import Number
import operator as op
def tokenize(expression):
    if expression == "":
        return []
    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]
def is_number(d):
    p = re.compile(r"\A[-]?\d+(?:\.\d+)?\Z")
    m = p.search(d)
    return bool(m)
class Environment(dict):
    def __init__(self, operators = {}, functions = {}, variables = {}, keywords = {}):
        self.update(operators = operators, functions = functions, variables = variables, keywords = keywords)
class Func:
    def __init__(self, params, expr, interpreter):
        self.params, self.expr = params, expr
        self.env = Environment(interpreter.env["operators"], interpreter.env["functions"])
        self.ary = len(params)
        self.interp = interpreter
    def __call__(self, *args):
        self.env["variables"].update(zip(self.params, args))
        return self.interp.eval_postfix(self.interp.shunting_yard(self.expr, self.env), self.env)
class Interpreter:
    def __init__(self):
        variables = {}
        functions = {}
        operators = {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            "%": op.mod,
            "=": self._assign_var
        }
        keywords = ["fn"]
        self.env = Environment(operators, functions, variables, keywords)
    def input(self, expression):
        tokens = tokenize(expression)
        if not tokens:
            return ""
        if tokens[0] in self.env["keywords"]:
            # Function declaration
            if tokens[0] == "fn":
                new_fn_name = tokens[1]
                if new_fn_name in self.env["variables"]:
                    raise Exception("Cannot overwrite variable with function!")
                assign_op_index = tokens.index("=>")
                params = tokens[2:assign_op_index]
                if len(params) != len(set(params)):
                    raise Exception("Duplicate parameters specified!")
                expr = tokens[assign_op_index+1:]
                for token in expr:
                    if token.isalpha() and token not in params:
                        raise Exception("Function body contains unknown variables!")
                new_fn = Func(params, expr, self)
                self.env["functions"][new_fn_name] = new_fn
                return ""
        else:
            value = self.eval_expr(tokens)
        return value
    def eval_expr(self, tokens):
        return self.eval_postfix(self.shunting_yard(tokens))
    def _assign_var(self, name, value):
        if name in self.env["functions"]:
            raise Exception("Cannot overwrite function with variable!")
        self.env["variables"][name] = value
        return value
    def shunting_yard(self, expression, env = None):
        if env is None:
            env = self.env
        def precedence(operator):
            if operator == '+' or operator == '-':
                return 2
            elif operator == '*' or operator == '/' or operator == '%':
                return 3
            elif operator == "=":
                return 1
            else:
                raise Exception("%s is not a valid operator." % operator)
        def is_left_assoc(operator):
            if operator == "=":
                return False
            return True
        output = []
        operators = []
        for token in expression:
            if is_number(token):
                try:
                    output.append(int(token))
                except ValueError:
                    output.append(float(token))
            elif token in env["functions"]:
                operators.append(token)
            elif token in env["variables"]:
                output.append(token)
            elif token in env["operators"]:
                if operators and operators[-1] in env["operators"]:
                    o1 = token
                    o2 = operators[-1]
                    while operators and o2 in env["operators"] and ((is_left_assoc(o1) and precedence(o1) <= precedence(o2)) or (not is_left_assoc(o1) and precedence(o1) < precedence(o2))):
                        output.append(env["operators"][operators.pop()])
                        try:
                            o2 = operators[-1]
                        except IndexError:
                            break
                operators.append(token)
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(" and operators[-1] in env["operators"]:
                    output.append(env["operators"][operators.pop()])
                try:
                    par = operators.pop()
                except IndexError:
                    raise Exception("ERROR: Mismatched parentheses!")
                    return
                if operators and operators[-1] in env["functions"]:
                    output.append(env["functions"][operators.pop()])
            else:
                output.append(token)
        while operators:
            if operators[-1] in env["operators"]:
                output.append(env["operators"][operators.pop()])
            elif operators[-1] in env["functions"]:
                output.append(env["functions"][operators.pop()])
            else:
                raise Exception("Invalid function!")
        return output
    def eval_postfix(self, tokens, env = None):
        if env is None:
            env = self.env
        if tokens is None:
            return ""
        output = []
        for i, token in enumerate(tokens):
            if isinstance(token, Number):
                output.append(token)
            elif isinstance(token, Func):
                try:
                    args = [env["variables"][output.pop()] if output[-1] in env["variables"] else output.pop() for _ in range(token.ary)]
                except IndexError:
                    raise Exception("ERROR: Incorrect number of arguments passed to function!")
                result = token(*args)
                output.append(result)
            elif callable(token):
                right = output.pop()
                left = output.pop()
                if right in env["variables"]:
                    right = env["variables"][right]
                if isinstance(right, str):
                    raise Exception("ERROR: Variable referenced before assignment!")
                if left in env["variables"] and token != env["operators"]["="]:
                    left = env["variables"][left]
                result = token(left, right)
                output.append(result)
            elif isinstance(token, str):
                output.append(token)
        if len(output) > 1:
            raise Exception("ERROR: Invalid syntax!")
        try:
            if output[0] in env["variables"]:
                return env["variables"][output[0]]
            elif isinstance(output[0], str):
                raise Exception("Undeclared variable referenced!")
            else:
                return output[0]
        except IndexError:
            return ""
          
###############################
import re

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}
        
    def getVal(self, token):
        if isinstance(token, float):
            return token
        elif token in self.vars:
            return self.vars[token]
        elif token in self.functions:
            func = self.functions[token]
            if len(func["args"]) == 0:
                realVars = self.vars
                vars = {}
                res = self.evaluateExpression(func["expr"])
                self.vars = realVars
                return res
            return "function"
        else:
            raise ValueError(f"Unkown identifier {token}")
        
    def evaluateParentheses(self, expr):
        newExpr = []
        idx = 0
        while idx < len(expr):
            if expr[idx] == "(":
                start = idx
                level = 1
                while level > 0:
                    idx += 1
                    if expr[idx] == "(":
                        level += 1
                    elif expr[idx] == ")":
                        level -= 1
                
                newExpr.append(str(self.evaluateExpression(expr[start + 1:idx])))
            else:
                newExpr.append(expr[idx])
                
            idx += 1
            
        return newExpr
    
    def solveFunctions(self, expr):
        idx = len(expr) - 1
        while idx >= 0:
            token, locked = expr[idx]
            if isinstance(token, str) and token in self.functions:
                func = self.functions[token]
                args = {}
                
                for jdx, argName in enumerate(func["args"]):
                    argVal = self.getVal(expr[idx + jdx + 1][0])
                    locked = expr[idx + jdx + 1][1]
                    if locked:
                        return
                    else:
                        args[argName] = argVal
                print(f"Executing function {token}")
                realVars = self.vars
                self.vars = args
                expr[idx][0] = self.evaluateExpression(func["expr"])
                self.vars = realVars
                
                for i in range(len(args)):
                    expr.pop(idx + 1)
            else:
                idx -= 1
    
    def solveAssign(self, expr):
        idx = len(expr) - 1
        while idx >= 0:
            token, locked = expr[idx]
            if isinstance(token, str) and token == "=":
                varName = expr[idx - 1][0]
                if varName in self.functions:
                    raise ValueError()
                secondOper = self.getVal(expr[idx + 1][0])
                secondLocked = expr[idx + 1][1]
                
                if not isinstance(secondOper, float) or secondLocked:
                    expr[idx - 1][1] = True
                    idx -= 1
                    continue
                    
                self.vars[varName] = secondOper
                    
                expr[idx - 1][0] = secondOper
                expr.pop(idx)
                expr.pop(idx)
                idx -= 1
                print(expr)
            else:
                idx -= 1
    
    def solveMultis(self, expr):
        idx = 0
        while idx < len(expr):
            token, locked = expr[idx]
            if isinstance(token, str) and token in "*/%":
                firstOper = self.getVal(expr[idx - 1][0])
                secondOper = self.getVal(expr[idx + 1][0])
                firstLocked = expr[idx - 1][1]
                secondLocked = expr[idx + 1][1]
                
                if not isinstance(firstOper, float) or not isinstance(secondOper, float):
                    expr[idx - 1][1] = True
                    expr[idx + 1][1] = True
                    idx += 1
                    continue
                    
                if token == "*":
                    expr[idx - 1][0] = firstOper * secondOper
                elif token == "/":
                    expr[idx - 1][0] = firstOper / secondOper
                elif token == "%":
                    expr[idx - 1][0] = firstOper % secondOper
                    
                expr[idx - 1][1] = False
                expr.pop(idx)
                expr.pop(idx)
            else:
                idx += 1          
                
    def solveAdds(self, expr):
        idx = 0
        while idx < len(expr):
            token, locked = expr[idx]
            if isinstance(token, str) and token in "+-":
                firstOper = self.getVal(expr[idx - 1][0])
                secondOper = self.getVal(expr[idx + 1][0])
                firstLocked = expr[idx - 1][1]
                secondLocked = expr[idx + 1][1]
                if not isinstance(firstOper, float) or firstLocked or not isinstance(secondOper, float) or secondLocked:
                    expr[idx - 1][1] = True
                    expr[idx + 1][1] = True
                    idx += 1
                    continue
                    
                if token == "+":
                    expr[idx - 1][0] = firstOper + secondOper
                elif token == "-":
                    expr[idx - 1][0] = firstOper - secondOper
                expr[idx - 1][1] = False
                expr.pop(idx)
                expr.pop(idx)
            else:
                idx += 1   
                
    def evaluateExpression(self, expr):
        print(f"Evaluating expression '{expr}'")
        
        # First, work out all parentheses
        expr = self.evaluateParentheses(expr)
        
        for i in range(len(expr)):
            try:
                expr[i] = float(expr[i])
            except ValueError:
                pass
        
        # Keep track of the fact that token is locked or not
        expr = [[token, False] for token in expr]
        
        prevLen = 0
        while len(expr) > 1:
            print(expr)
            prevLen = len(expr)
            self.solveMultis(expr)
            self.solveAdds(expr)
            self.solveAssign(expr)
            self.solveFunctions(expr)
            if len(expr) == prevLen:
                raise ValueError()
        
        return self.getVal(expr[0][0])
    
    def isValidVarName(self, varName):
        return bool(re.match("[a-zA-Z_][a-zA-Z_\d]*", varName))
        
    def defineFunction(self, tokens):
        name = tokens[1]
        if name in self.vars:
            raise ValueError(f"There is already a variable defined with the name {name}")
            
        if tokens[0] != "fn":
            raise ValueError("You cannot declare a function in an expression")
            
        arrowPos = tokens.index("=>")
        argVars = [tokens[i] for i in range(2, arrowPos)]
        
        if len(set(argVars)) != len(argVars):
            raise ValueError("Duplicate variable name")
               
        functionExpression = tokens[arrowPos + 1:]
        for token in functionExpression:
            if self.isValidVarName(token) and token not in argVars:
                raise ValueError(f"ERROR: Unknown identifier {token}")
                
        self.functions[name] = {"args":argVars, "expr":functionExpression}
        

    def input(self, expression):
        if expression.strip() == "":
            return ""
        tokens = tokenize(expression)
        if "fn" in tokens:
            self.defineFunction(tokens)
            return ""
        else:
            return self.evaluateExpression(tokens)
          
##################################
import re
from functools import reduce

class FunctionClass:
    variables = []
    expression = ""
    def __init__(self, variables, expression):
        self.variables = variables
        self.expression = expression
    def substitute(self, values):
        if len(values) != self.numVars():
            raise Exception("ERROR: Wrong number of parameters!")
        expression = self.expression
        for variable, value in zip(self.variables, values):
            expression = re.sub(variable, value, expression)
        return expression
    def numVars(self):
        return len(self.variables)


class Interpreter:
    d = "([-+]*\d+(\.\d+)?(e-?\d+)?)"
    varReg = "(?<![\w])[A-Za-z]\w*"
    dv = f"({d}|{varReg})"
    assReg = f"^((?:{varReg}\s*=\s*)*)(.+)$"
    parReg = "\(([^()]*)\)"
    PMReg = f"{d}\s*(\-|\+)\s*{d}(\s*(\-|\+)\s*{d})*"
    MDReg = f"{d}([\*/%]){d}(?:\4{d})*"
    expressionReg = f"^[\s\(-]*{d}([\s\)]*[\+\*/%-][\s\(-]*{d}[\s\)]*)*$"
    funcDecReg = f"^fn\s+({varReg})\s+((?:{varReg}\s*)*)\s*=>\s*(.+)$"

    def __init__(self):
        self.vars = {}
        self.functions = {}

    def _filter_expression(self, expression):
        expression = re.sub(" +","", expression)
        expression = re.sub("(?<=\w|\))\+*(-+)", lambda obj: "+" if len(obj[1]) % 2 == 0 else "-", expression)
        expression = re.sub("(?<!\w|\))\+*(?:(-+)|(\+))", lambda obj: "" if obj[2] is not None or len(obj[1]) % 2 == 0 else "-", expression)
        return expression

    def _plus_minus_str(self, obj):
        numbers = [float(x[0]) for x in re.findall(self.d, obj[0])]
        return str(sum(numbers))

    def _mult_div_str(self, obj):
        numbers = [float(x[0]) for x in re.findall(self.d, obj[0])]
        return "+"+str(reduce(lambda x, y : x*y if re.search('\*', obj[0]) else x/y if re.search('/', obj[0]) else x%y, numbers))

    def _calculate(self, expression):
        var, expression = re.fullmatch(self.assReg, expression).group(1, 2)  # MOVE TO INNER PARENTHESIS
        while(True):
            old_expression = expression
            expression = re.sub(self.parReg, lambda obj : self._calculate(obj[1]), expression)
            if expression == old_expression: break
        expression = self._substitute_expr(expression)
        expression = self._filter_expression(expression)
        if not re.search(self.expressionReg, expression): raise Exception(
            "ERROR: Expression formatted incorrectly!")
        for pattern, repl, count in zip([self.parReg, self.MDReg, self.PMReg], [lambda obj : self._calculate(obj[1]), self._mult_div_str, self._plus_minus_str], [0, 1, 0]):
            while(True):
                old_expression = expression
                expression = re.sub(pattern, repl, expression, count)
                expression = self._filter_expression(expression)
                if expression == old_expression: break
        if var is not None:
            for v in re.findall(self.varReg, var):
                self._variable_declaration(v, expression)
        return expression

    def _function_declaration(self, expression):
        name, variables, expression = re.fullmatch(self.funcDecReg, expression).group(1,2,3)
        # Abort if a variable with the same name is already declared
        if name in self.vars: raise Exception("ERROR: Function name already declared as a variable!")
        variables = re.findall(self.varReg, variables)
        if len(variables) > len(set(variables)):
            raise Exception("ERROR: Parameters in function declaration must have unique identifiers!")
        if any([x not in variables for x in re.findall(self.varReg, expression)]):
            raise Exception("ERROR: All parameters in function expression must be provided in parameter list")
        self.functions[name] = FunctionClass(variables, expression)
        return ""

    def _variable_declaration(self, name, value):
        #Check if a function with the same variable name is already declared
        if name in self.functions: raise Exception("ERROR: Variable name already declared as function!")
        self.vars[name] = value
        return

    def _substitute(self, call):
        strs = [x[0] for x in re.findall(self.dv, call[0])]
        for idx in range(len(strs)-1, -1, -1):
            str = strs[idx]
            if str in self.vars:
                strs[idx] = self.vars[str]
            elif str in self.functions:
                fun = self.functions[str]
                strs[idx] = fun.substitute(strs[idx + 1: idx + 1 + fun.numVars()])
                del (strs[idx + 1: idx + 1 + fun.numVars()])

        if len(strs) == 1:
            return self._calculate(strs[0])
        else:
            raise Exception("ERROR in function call!")

    def _substitute_expr(self, FullExpression):   # Substitute variables and function calls
        FullExpression = re.sub(f"{self.dv}\s+({self.dv}\s*)+|{self.varReg}", self._substitute, FullExpression)
        return FullExpression

    def input(self, expression):
        if not expression or expression.isspace(): return ""
        if re.search(self.funcDecReg, expression): return self._function_declaration(expression) # Check if function declaration
        value = self._calculate(expression)
        return float(value)
      
#############################
import re

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokens = tokenize(expression)
        if len(tokens)==0 or expression.strip()=='': return ''
    
        if tokens[0] != 'fn':
            function_found=True
            while function_found:
                function_found = False
                for i in range(len(tokens)):
                    if tokens[i] in self.functions:
                        if tokens[i] in self.vars or (len(tokens)>(i+1) and tokens[i+1] == '='):
                            raise ValueError('ERROR - Illegal Function Definition. Function name specified as variable name.')
                            break
                        else:
                            function_found = True
                            arg_count=len(self.functions[tokens[i]][0])
                            if arg_count > 0:
                                func_args = False
                                for j in range(1, arg_count+1):
                                    if i + j >= len(tokens):
                                        raise ValueError('ERROR - Illegal expression. Missing Function Arguments')
                                    else:
                                        if tokens[i+j] in self.functions:
                                            func_args = True
                                if not func_args:
                                    func_expression = self.functions[tokens[i]][1]
                                    for j in range(1, arg_count+1):
                                        func_expression = func_expression.replace(self.functions[tokens[i]][0][j-1],tokens[i+j])
                                    tokens = tokens[0:i] + [str(self.input(func_expression))] + tokens[i+arg_count+1:]
                                    break
                                else:
                                    function_found = False
                            else:
                                if len(tokens) > 1:
                                    tokens = tokens[0:i] + ['('] + self.functions[tokens[i]][1].split() + [')'] + tokens[i+1:]
                                else:
                                    tokens = ['('] + self.functions[tokens[i]][1].split() + [')']
                                break
    
        if tokens[0] != 'fn':
            for i in range(len(tokens)):
                if tokens[i] not in '%*/+-=()':
                    if not tokens[i][0]!='_' and not tokens[i][0].isalpha():
                        if not tokens[i].isnumeric():
                            raise ValueError('ERROR - Illegal token')

            for i in range(len(tokens)-1):
                if tokens[i] in '%*/+-' and tokens[i+1] in '%*/+-':
                    raise ValueError('ERROR - Illegal expression. Consecutive operators are not allowed.')

            if tokens.count('(') != tokens.count(')'):
                raise ValueError("ERROR - Illegal expression. Mismatched parentheses")

            for i in range(len(tokens)-1):
                
                if tokens[i] not in '%*/+-=()' and tokens[i+1] not in '%*/+-=()':
                    raise ValueError('ERROR - Illegal expression. Consecutive variables and(or) numbers are not allowed.')

        if tokens[0] != 'fn':
            
            while len(tokens) > 1:

                while '(' in tokens:
                    left_parens=[]
                    for i in range(len(tokens)):
                        if tokens[i]=='(':
                            left_parens.append(i)
                        elif tokens[i]==')':

                            tokens[left_parens[-1]] = str(self.input(' '.join(tokens[left_parens[-1]+1:i])))

                            for j in range(i,left_parens[-1],-1):
                                del tokens[j]
                            del left_parens[-1]
                            break

                if '=' in tokens:
                    for k,v in enumerate(tokens[::-1]):
                        if v == '=':
                            equal = len(tokens) - k - 1
                            break
                else:
                    equal = -1

                for i in range(equal+1,len(tokens)):
                    if tokens[i][0]=='_' or tokens[i][0].isalpha():
                        if tokens[i] in self.vars:
                            tokens[i] = self.vars[tokens[i]]

                if '(' in tokens: return 0

                while '%' in tokens or '*' in tokens or '/' in tokens:
                    for i in range(len(tokens)):
                        if tokens[i] in '%*/':
                            if tokens[i]=='%':
                                tokens[i-1]=str(int(tokens[i-1])%int(tokens[i+1]))
                            elif tokens[i]=='*':
                                tokens[i-1]=str(float(tokens[i-1])*float(tokens[i+1]))
                            else:
                                tokens[i-1]=str(float(tokens[i-1])/float(tokens[i+1]))
                            del tokens[i+1]
                            del tokens[i]
                            break

                while '+' in tokens or '-' in tokens:
                    for i in range(len(tokens)):
                        if tokens[i] in '+-':
                            if tokens[i]=='+':
                                tokens[i-1]=str(float(tokens[i-1])+float(tokens[i+1]))
                            else:
                                tokens[i-1]=str(float(tokens[i-1])-float(tokens[i+1]))
                            del tokens[i+1]
                            del tokens[i]
                            break

                if '=' in tokens:
                    for j in range(tokens.count('=')):
                        for k,v in enumerate(tokens[::-1]):
                            if v == '=':
                                equal_loc = len(tokens) - k - 1
                                break
                        if tokens[equal_loc-1] not in self.functions:
                            self.vars[tokens[equal_loc-1]] = tokens[-1]
                            tokens[equal_loc-1] = tokens[-1]
                            del tokens[equal_loc]
                            del tokens[equal_loc-1]  
                        else:
                            raise ValueError('ERROR - Illegal expression. Assignment to Function name not allowed.')
                            
                operator_found = False
                for x in '%*/+-()=':
                    if x in tokens:
                        operator_found = True

                if not operator_found and len(tokens)>1:
                    raise ValueError('ERROR - Illegal expression.')
        else:

            if '=>' in tokens:
                arrow_loc = tokens.index('=>')
                args=[]

                if tokens[1] in self.vars:
                    raise ValueError('ERROR - Illegal Function Definition. Variable name specified as function name.')

                if arrow_loc > 2:
                    for i in range(2,arrow_loc):
                        args.append(tokens[i])

                for i in range(len(args)):
                    if args[i] not in tokens[arrow_loc+1:]:
                        raise ValueError('ERROR - Illegal Function Definition. Argument not referenced in function expression.')

                for i in range(arrow_loc+1,len(tokens)):
                    if not tokens[i] in '%*/+-()':
                        if tokens[i][0]=="_" or tokens[i][0].isalpha():
                            if tokens[i] not in args:
                                raise ValueError(f'ERROR - Illegal Function Definition. {tokens[i]} not defined.')
                
                for i in range(len(args)):
                    if args.count(args[i]) != 1:
                        raise ValueError(f'ERROR - Illegal Function Definition. Duplicate argument name.')

                self.functions[tokens[1]] = (args, ' '.join(tokens[arrow_loc+1:]))       

            else:
                raise ValueError('ERROR - Illegal Function Definition. Missing "=>" operator.')

        if tokens[0].isalpha() and tokens[0] != 'fn':
            return float(self.vars[tokens[0]])
        elif not tokens[0].isalpha():
            return float(tokens[0])
        else:
            return ''
                    
##############################
import re
from numbers import Number
import operator as op

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

def is_number(d):
    p = re.compile(r"\A[-]?\d+(?:\.\d+)?\Z")
    m = p.search(d)
    return bool(m)
    

class Environment(dict):
    def __init__(self, operators = {}, functions = {}, variables = {}, keywords = {}):
        self.update(operators = operators, functions = functions, variables = variables, keywords = keywords)


class Func:
    def __init__(self, params, expr, interpreter):
        self.params, self.expr = params, expr
        self.env = Environment(interpreter.env["operators"], interpreter.env["functions"])
        self.ary = len(params)
        self.interp = interpreter

    def __call__(self, *args):
        self.env["variables"].update(zip(self.params, args))
        return self.interp.eval_postfx(self.interp.shunt_yard(self.expr, self.env), self.env)


class Interpreter:
    def __init__(self):
        variables = {}
        functions = {}
        operators = {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            "%": op.mod,
            "=": self._assign_var
        }
        keywords = ["fn"]
        self.env = Environment(operators, functions, variables, keywords)

    def input(self, expression):
        tokens = tokenize(expression)
        if not tokens:
            return ""
        if tokens[0] in self.env["keywords"]:
            # Function declaration
            if tokens[0] == "fn":
                new_fn_name = tokens[1]
                if new_fn_name in self.env["variables"]:
                    raise Exception("Cannot overwrite variable with function!")
                assign_op_index = tokens.index("=>")
                params = tokens[2:assign_op_index]
                if len(params) != len(set(params)):
                    raise Exception("Duplicate parameters specified!")
                expr = tokens[assign_op_index+1:]
                for token in expr:
                    if token.isalpha() and token not in params:
                        raise Exception("Function body contains unknown variables!")
                new_fn = Func(params, expr, self)
                self.env["functions"][new_fn_name] = new_fn
                return ""
        else:
            value = self.eval_expr(tokens)
        return value

    def eval_expr(self, tokens):
        return self.eval_postfx(self.shunt_yard(tokens))

    def _assign_var(self, name, value):
        if name in self.env["functions"]:
            raise Exception("Cannot overwrite function with variable!")
        self.env["variables"][name] = value
        return value

    def shunt_yard(self, expression, env = None):
        if env is None:
            env = self.env
        def precedence(operator):
            if operator == '+' or operator == '-':
                return 2
            elif operator == '*' or operator == '/' or operator == '%':
                return 3
            elif operator == "=":
                return 1
            else:
                raise Exception("%s is not a valid operator." % operator)
        def is_left_assoc(operator):
            if operator == "=":
                return False
            return True

        output = []
        operators = []
        for token in expression:
            if is_number(token):
                try:
                    output.append(int(token))
                except ValueError:
                    output.append(float(token))
            elif token in env["functions"]:
                operators.append(token)
            elif token in env["variables"]:
                output.append(token)
            elif token in env["operators"]:
                if operators and operators[-1] in env["operators"]:
                    o1 = token
                    o2 = operators[-1]
                    while operators and o2 in env["operators"] and ((is_left_assoc(o1) and precedence(o1) <= precedence(o2)) or (not is_left_assoc(o1) and precedence(o1) < precedence(o2))):
                        output.append(env["operators"][operators.pop()])
                        try:
                            o2 = operators[-1]
                        except IndexError:
                            break
                operators.append(token)
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(" and operators[-1] in env["operators"]:
                    output.append(env["operators"][operators.pop()])
                try:
                    par = operators.pop()
                except IndexError:
                    raise Exception("ERROR: Mismatched parentheses!")
                    return
                if operators and operators[-1] in env["functions"]:
                    output.append(env["functions"][operators.pop()])
            else:
                # Token is identifier?
                output.append(token)
                #raise Exception("ERROR: Invalid token: %r" % token)
                #return
        while operators:
            if operators[-1] in env["operators"]:
                output.append(env["operators"][operators.pop()])
            elif operators[-1] in env["functions"]:
                output.append(env["functions"][operators.pop()])
            else:
                raise Exception("Invalid function!")
        return output

    def eval_postfx(self, tokens, env = None):
        if env is None:
            env = self.env
        if tokens is None:
            return ""
        output = []
        for i, token in enumerate(tokens):
            if isinstance(token, Number):
                output.append(token)
            elif isinstance(token, Func):
                try:
                    args = [env["variables"][output.pop()] if output[-1] in env["variables"] else output.pop() for _ in range(token.ary)]
                except IndexError:
                    raise Exception("ERROR: Incorrect number of arguments passed to function!")
                result = token(*args)
                output.append(result)
            elif callable(token):
                right = output.pop()
                left = output.pop()
                if right in env["variables"]:
                    right = env["variables"][right]
                if isinstance(right, str):
                    raise Exception("ERROR: Variable referenced before assignment!")
                if left in env["variables"] and token != env["operators"]["="]:
                    left = env["variables"][left]
                result = token(left, right)
                output.append(result)
            elif isinstance(token, str):
                output.append(token)
        if len(output) > 1:
            raise Exception("ERROR: Invalid syntax!")
        try:
            if output[0] in env["variables"]:
                return env["variables"][output[0]]
            elif isinstance(output[0], str):
                raise Exception("Undeclared variable referenced!")
            else:
                return output[0]
        except IndexError:
            return ""
          
#######################################
import re

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self, vars = {}, functions = {}):
        self.vars = vars
        self.functions = functions

    def is_identifier(self, id) : # raise Exception if not valid
        if not re.match("[_A-Za-z].*",id) or id == 'fn' :
            raise Exception('Error : %s is not a valid identifier' % expr_tok[0])

    def is_number(self,id) : # raise Exception if not valid
        if not re.match("[0-9]*\.?[0-9]+",id) :
            raise Exception('Error : %s is not a valid number' % id)

    def compute_number(self,id) :
        self.is_number(id)
        return float(id) if '.' in id else int(id)

    def compute_identifier(self, id) : # Return value or raise KeyError
        self.is_identifier(id)
        try :
            return self.vars[id]
        except KeyError:
            raise KeyError("Error : identifier %s haven't been assigned" % id)

    def compute_assignement(self, expr_tok) : # Assign and return expression or raise syntax error
        i = expr_tok.index('=')
        if i != 1 :
            raise Exception('Error : invalid syntax "%s = ..."' % ' '.join(expr_tok[:i]))
        self.is_identifier(expr_tok[0])
        if expr_tok[0] in self.functions : raise Exception("Error : %s already defined..." % expr_tok[0])
        self.vars[expr_tok[0]],t = self.parse_expr(expr_tok[2:])
        return (self.vars[expr_tok[0]],t+2)

    def compute_paren(self, expr_tok) : # Return end of parenthesis or raise syntax error
        count = 0
        for i,s in enumerate(expr_tok) :
            count += { '(' : 1, ')' : -1}.get(s,0)
            if count == 0 and i > 0 : return i
        raise Exception('Error : non matching parenthesis %s ' % ' '.join(expr_tok[:i]))

    def define_function(self, fun_name, expression):
        self.is_identifier(fun_name)
        if fun_name in self.vars : raise Exception("Error : %s already defined..." % fun_name)
        try :
            fn_op_tok = expression.index("=>")
            fun = { 'params' : expression[:fn_op_tok], 'expr' : expression[fn_op_tok+1:] }
            for tok in fun['expr'] :
                try : 
                    self.is_identifier(tok)
                except : ()
                else :
                    if tok not in fun['params'] : 
                        raise Exception("Error : identifier %s does not refer to variable or parameter in definition of %s... " % (tok,fun_name)) 
            if len(fun['params']) != len(set(fun['params'])) : 
                raise Exception("Error : duplicate name for parameters of function %s" % fun_name)
            self.functions[fun_name] = fun
            
        except KeyError :
            raise Exception("Error : invalid syntax in function %s definition %s ..." % (fun_name,' '.join(expression)))

    def call_fun(self, fun_name, expression):
        params = {}
        pos_tot = 0
        try :
            for p in self.functions[fun_name]['params'] :
                if pos_tot >= len(expression) : raise Exception("Error : too few arguments for %s in %s ..." % (fun_name,' '.join(expression)))
                res,pos = self.parse_expr(expression[pos_tot:])
                pos_tot += pos
                params[p] = res
            return (Interpreter(dict(self.vars,**params),self.functions).input(self.functions[fun_name]['expr']),pos_tot)
        except KeyError :
            raise KeyError("Error : identifier %s haven't been assigned. Functions are %s" % (id,str(self.functions)))

    def parse_expr(self,tokens) :
        if not tokens : return ("",1)
        i = 0
        res = 0
        lastop = None
        if re.match("[_A-Za-z]", tokens[i][0]) :
            try :
                return self.compute_assignement(tokens)
            except ValueError: ()
        while True :
            old_res = res
            if tokens[i] == '(' :
                j = i+self.compute_paren(tokens[i:])
                res,t = self.parse_expr(tokens[i+1:j])
                i = j+1
            elif re.match("[0-9]",tokens[i][0]) :
                res = self.compute_number(tokens[i])
                i += 1
            elif re.match("[_A-Za-z]", tokens[i][0]) :
                try :
                    res = self.compute_identifier(tokens[i])
                    i += 1
                except KeyError :
                    res,j = self.call_fun(tokens[i],tokens[i+1:])
                    i += j+1
            else : raise Exception("Error : invalid syntax ... %s ..." % ' '.join(tokens))
            if lastop == '*' : res = old_res*res
            elif lastop == '/' : res = old_res/res
            elif lastop == '%' : res = old_res%res
            if i >= len(tokens)-1 : return (res,i)
            if tokens[i] == '+' :
                rt, j = self.parse_expr(tokens[i+1:])
                return (res + rt,i+j+1)
            if tokens[i] == '-' :
                rt, j = self.parse_expr(tokens[i+1:])
                return (res - rt,i+j+1)
            if tokens[i] in list('*/%') : lastop = tokens[i]
            else : return (res,i)
            i += 1

    def input(self, expression):
        if type(expression) != type([]) :
            expression = tokenize(expression)
        if not expression : return ""
        if re.match("fn", expression[0]) : self.define_function(expression[1],expression[2:]); return "";
        res, num = self.parse_expr(expression)
        if num < len(expression) : 
            raise Exception("Error : invalid syntax on %s (token %d) in %s ..." % (expression[num], num, ' '.join(expression)))
        return res
            
