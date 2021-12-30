import re

class ParseError(Exception):
    def __init__(self, node, tokens):
        self.node = node
        self.tokens = tokens

    def __str__(self):
        return "ERROR: unable to parse {} with tokens {}".format(self.node, self.tokens)

class EvaluationError(Exception):
    def __init__(self, expr, vars):
        self.expr = expr
        self.vars = vars

    def __str__(self):
        expr_str = str(self.expr)
        vars_str = "{ " + ",".join([ "{}: {}".format(k, str(v)) for k, v in self.vars.items() ]) + " }"
        return "ERROR: insufficient data for complete eval [expr={}, vars={}]".format(self.expr_str, self.vars_str)

class IdentifierError(Exception):
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return "ERROR: Invalid identifier. No variable with name '{}' was found.".format(self.identifier)

class Assignment(object):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue

    @classmethod
    def parse(cls, tokens, best_effort=True):
        if len(tokens) >= 3 and tokens[1] == "=":
            lvalue = Identifier.parse(tokens[:1], False)           
            rvalue = Expression.parse(tokens[2:], False)
            return Assignment(lvalue, rvalue)

        if best_effort: return None
        raise ParseError("assignment", tokens)

    def eval(self, vars):
        rvalue, vars = self.rvalue.eval(vars)
        if not isinstance(rvalue, Number): raise EvaluationError(self, vars)
        vars[self.lvalue.name] = rvalue
        return self.lvalue.eval(vars)

    def __str__(self):
        return "{} = {}".format(str(self.lvalue), str(self.rvalue))

class Identifier(object):
    regex = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    def __init__(self, name):
        self.name = name

    @classmethod
    def parse(cls, tokens, best_effort=True):
        if len(tokens) == 1:
            if cls.regex.match(tokens[0]): return Identifier(tokens[0])

        if best_effort: return None
        raise ParseError("identifier", tokens)

    def eval(self, vars):
        if self.name not in vars.keys(): raise IdentifierError(self.name)
        if not isinstance(vars[self.name], Number): raise IdentifierError(self.name)

        return (vars[self.name], vars)

    def __str__(self):
        return self.name

class Number(object):
    regex = re.compile(r"^[0-9]*\.?[0-9]*$")

    def __init__(self, value):
        self.value = value

    @classmethod
    def parse(cls, tokens, best_effort=True):
        if len(tokens) == 1:
            if cls.regex.match(tokens[0]):
                n = float(tokens[0]) if str(float(tokens[0])) == tokens[0] else int(tokens[0])
                return Number(n)

        if best_effort: return None
        raise ParseError("number", tokens)

    def eval(self, vars):
        return (self, vars)

    def __str__(self):
        return str(self.value)

class Factor(object):

    @classmethod
    def parse(cls, tokens, best_effort=True):
        parsed = Number.parse(tokens)
        if parsed: return parsed

        parsed = Identifier.parse(tokens)
        if parsed: return parsed

        parsed = Assignment.parse(tokens)
        if parsed: return parsed

        # check if is between parenthesis
        if len(tokens) >= 3 and tokens[0] == "(" and tokens[-1] == ")":
            level = 0
            for idx, token in enumerate(tokens):
                if token == "(": level += 1
                if token == ")": level -= 1

                if level == 0 and idx not in [0, len(tokens) - 1]:
                    if best_effort: return None
                    raise ParseError("factor", tokens)

            parsed = Expression.parse(tokens[1:-1], False)
            if parsed: return parsed

        if best_effort: return None
        raise ParseError("factor", tokens)

class BinaryOp(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @classmethod
    def parse(cls, tokens, best_effort=True):
        operations = [Add, Sub, Mul, Div, Remainder]

        for operation in operations:
            parsed = operation.parse(tokens)
            if parsed: return parsed

        if best_effort: return None
        raise ParseError("binaryOp", tokens)

class Mul(BinaryOp):
    @classmethod
    def parse(cls, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True
            
            if token == "*" and parse:
                left = Expression.parse(tokens[:idx], False)
                right = Expression.parse(tokens[idx+1:], False)
                return Mul(left, right)

        if best_effort: return None
        raise ParseError("mul", tokens)

    def eval(self, vars):
        left, vars = self.left.eval(vars)
        right, vars = self.right.eval(vars)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars)

        return (Number(left.value * right.value), vars)

    def __str__(self):
        return "({} * {})".format(str(self.left), str(self.right))

class Div(BinaryOp):
    @classmethod
    def parse(cls, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True
            
            if token == "/" and parse:
                left = Expression.parse(tokens[:idx], False)
                right = Expression.parse(tokens[idx+1:], False)
                return Div(left, right)

        if best_effort: return None
        raise ParseError("div", tokens)

    def eval(self, vars):
        left, vars = self.left.eval(vars)
        right, vars = self.right.eval(vars)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars)


        result = int(left.value / right.value) if left.value % right.value == 0 else left.value / right.value
        return (Number(result), vars)

    def __str__(self):
        return "({} / {})".format(str(self.left), str(self.right))

class Remainder(BinaryOp):
    @classmethod
    def parse(cls, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True
            
            if token == "%" and parse:
                left = Expression.parse(tokens[:idx], False)
                right = Expression.parse(tokens[idx+1:], False)
                return Remainder(left, right)

        if best_effort: return None
        raise ParseError("remainder", tokens)

    def eval(self, vars):
        left, vars = self.left.eval(vars)
        right, vars = self.right.eval(vars)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars)

        return (Number(left.value % right.value), vars)

    def __str__(self):
        return "({} % {})".format(str(self.left), str(self.right))

class Add(BinaryOp):
    @classmethod
    def parse(cls, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True

            if token == "+" and parse:
                left = Expression.parse(tokens[:idx], False)
                right = Expression.parse(tokens[idx+1:], False)
                return Add(left, right)

        if best_effort: return None
        raise ParseError("add", tokens)

    def eval(self, vars):
        left, vars = self.left.eval(vars)
        right, vars = self.right.eval(vars)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars)

        return (Number(left.value + right.value), vars)

    def __str__(self):
        return "({} + {})".format(str(self.left), str(self.right))

class Sub(BinaryOp):
    @classmethod
    def parse(cls, tokens, best_effort=True):
        parse = True
        for idx, token in enumerate(tokens):
            if token == "(" and parse: parse = False
            elif token == ")" and not parse: parse = True

            if token == "-" and parse:
                left = Expression.parse(tokens[:idx], False)
                right = Expression.parse(tokens[idx+1:], False)
                return Sub(left, right)

        if best_effort: return None
        raise ParseError("sub", tokens)

    def eval(self, vars):
        left, vars = self.left.eval(vars)
        right, vars = self.right.eval(vars)

        if not isinstance(left, Number) or not isinstance(right, Number):
            raise EvaluationError(self, vars)

        return (Number(left.value - right.value), vars)

    def __str__(self):
        return "({} - {})".format(str(self.left), str(self.right))

class Expression(object):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, tokens, best_effort=False):
        if len(tokens) == 1 and isinstance(tokens[0], Expression): return tokens[0]

        parsed = Factor.parse(tokens)
        if parsed: return parsed

        parsed = BinaryOp.parse(tokens)
        if parsed: return parsed

        raise ParseError("expression", tokens)

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

        self.expressions = []

    def input(self, expression):
        print("> {}".format(expression))

        tokens = tokenize(expression)
        if not tokens: return ""

        expr = Expression.parse(tokens)
        self.expressions.append(expr)

        output, vars = expr.eval(self.vars)

        self.vars = vars

        print(output)

        return output.value

interpreter = Interpreter()
code = [
    "(8 - (4 + 2)) * 3",
    "x = -1",
    "x"
]

for line in code:
    try:
        interpreter.input(line)
    except Exception as e:
        print(e)
        
________________________________________________________
from ast import parse, Expr, Assign, BinOp, Name, Num
from operator import add, sub, mul, mod, truediv


class Interpreter:

    def __init__(self):
        self.vars = {}

    def input(self, expression):

        op = {'Sub': sub, 'Add': add, 'Mult': mul, 'Div': truediv, 'Mod': mod}

        def _eval(node):

            if isinstance(node, Expr):
                return _eval(node.value)
            if isinstance(node, Name):
                return self.vars[node.id]
            if isinstance(node, Num):
                return node.n
            if isinstance(node, BinOp):
                return op[type(node.op).__name__](_eval(node.left), _eval(node.right))
            if isinstance(node, Assign):
                name = node.targets[0].id
                self.vars[name] = _eval(node.value)
                return self.vars[name]

        tree = parse(expression)
        return _eval(tree.body[0]) if len(tree.body) else ''
      
________________________________________________________
from collections import OrderedDict
import operator
import string
import re


def tokenize(expression):
    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]
    
    
def split_list(lst, item):
    if item not in lst: return lst
    
    i = lst.index(item)
    return  lst[0:i], lst[i+1:]
    
    
class Interpreter:
    operators = OrderedDict({'*': operator.mul, '/': operator.div, '%': operator.mod,
                             '+': operator.add, '-': operator.sub})

    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokens = tokenize(expression)
        
        if '=' in tokens:
            left, right = split_list(tokens, '=')         
            value = self.calc_expression(right)            
            self.vars[left[0]] = value
            return value
        else:
            return self.calc_expression(tokens)          
        
    def calc_expression(self, tokens):
        if not tokens: return ''
        if len(tokens) == 1:
            value = tokens[0]
            if self.is_number(value): return int(value)
            elif self.is_var(value): return self.vars[value]
        
        while '(' in tokens:
            opened = 0
            closed = 0
            
            i = tokens.index('(')
            for j, t in enumerate(tokens):
                if t == '(': opened += 1
                if t == ')': closed += 1
                if opened and opened == closed:
                    value = self.calc_expression(tokens[i+1:j])
                    tokens = tokens[0:i] + [str(value)] + tokens[j+1:]
                    break                                                               
        
        for o in self.operators:
            if o in tokens:
                left, right = split_list(tokens, o)
                left, right = self.calc_expression(left), self.calc_expression(right)
                return self.operators[o](left, right) 
                
        raise ValueError('Bad input')                
    
    @staticmethod
    def is_number(token):
        return bool(re.match(r'^\d+$', token))
        
    @staticmethod
    def is_var(token):
        return bool(re.match(r'^\w+$', token))
      
________________________________________________________
import re


class UnbalancedParenthesesError(ValueError):
    """ Raised if an expression contains invalid parentheses.

        Examples of invalid parentheses:
            - ((3+4) [more opening than closing]
            - () [no content]
            - (3+4) * 2) [more closing than opening]
            - (3+4))( [unbalanced]
    """


class UndefinedIdentifierError(object):
    """ Raised if an expression attempts to access an undefined identifier.
    """


class UnsupportedOperatorError(ValueError):
    """ Raised if an expression contains an unsupported operator.

        Supported operators: +, -, *, /, %
    """

# pre-compiled for efficiency
p = "\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*"
EXPRESSION_PATTERN = re.compile(p)


def tokenize(expression):
    tokens = EXPRESSION_PATTERN.findall(expression)
    return [s for s in tokens if not s.isspace()]


class Interpreter(object):
    def __init__(self):
        self.vars = {}

    def input(self, expression, verbose=False):
        if not expression or expression.isspace():
            return ""

        tokens = tokenize(expression)

        def is_single_expression(tokens):
            """ True if :tokens: consists of a single:
                - (integer) number
                - identifier
                and false otherwise.
            """
            return len(tokens) == 1

        if is_single_expression(tokens):
            e = tokens[0]
            if e.isdigit():
                return int(e)
            elif e in self.vars:
                return self.vars[e]
            else:
                raise UndefinedIdentifierError("Identifier '{}'"
                                               "undefined!".format(e))
                return ("ERROR: Invalid identifier. No variable with "
                        "name '{}' was found".format(e))

        def is_assignment(tokens):
            """ True if :tokens: consists of an assignment of
                an expression to an identifier.
            """
            return "=" in tokens

        if is_assignment(tokens):
            eq_index = tokens.index("=")
            lhs, rhs = tokens[:eq_index], tokens[eq_index + 1:]
            val = self.input(" ".join(rhs))
            self.vars[lhs[0]] = val
            return val

        else:
            def has_parens(tokens):
                """ True if :tokens: contains at least one opening and one
                    closing parenthesis.
                """
                return "(" in tokens and ")" in tokens

            def parens_balanced(tokens):
                """ True if all parentheses in :tokens: are balanced.
                    Otherwise raises 'UnbalancedParenthesesError'.
                """
                if any(tokens[i] == "(" and tokens[i+1] == ")"
                        for i in range(len(tokens) - 1)):
                    raise UnbalancedParenthesesError("Expression '() is not "
                                                     "valid!")
                open_parens = 0
                for t in tokens:
                    if t == "(":
                        open_parens += 1
                    elif t == ")":
                        open_parens -= 1

                    if open_parens < 0:
                        raise UnbalancedParenthesesError("All open "
                                                         "parentheses "
                                                         "closed and "
                                                         "encountered "
                                                         "closing "
                                                         "parenthesis!")

                if open_parens > 0:
                    raise UnbalancedParenthesesError("Too many opening "
                                                     "parentheses!")
                return True

            def next_operator(tokens):
                """ Return function and :tokens: index for next applicable
                    operator.
                """
                from operator import mul, truediv, mod, add, sub

                if "+" in tokens:
                    index = tokens.index("+")
                    return add, index
                elif "-" in tokens:
                    index = tokens.index("-")
                    return sub, index
                elif "*" in tokens:
                    index = tokens.index("*")
                    return mul, index
                elif "/" in tokens:
                    index = tokens.index("/")
                    return truediv, index
                elif "%" in tokens:
                    index = tokens.index("%")
                    return mod, index
                else:
                    exp = " ".join(tokens)
                    raise UnsupportedOperatorError("Expression '{}' "
                                                   "contained none of the "
                                                   "supported operators: "
                                                   "+, -,"
                                                   "*, /, %".format(exp))

            def get_next_paren_ids(tokens):
                """ Return opening and closing indices of next
                    parenthized expression to evaluate.
                """
                def list_rfind(l, el):
                    i = len(l) - 1
                    for e in l[::-1]:
                        if e == el:
                            return i
                        i -= 1
                opening_index = list_rfind(tokens, "(")
                closing_index = tokens.index(")", opening_index)

                return opening_index, closing_index

            if has_parens(tokens) and parens_balanced(tokens):
                opening_index, closing_index = get_next_paren_ids(tokens)
                parens_tokens = tokens[opening_index + 1: closing_index]
                parens_exp = [str(self.input(" ".join(parens_tokens)))]
                new_exp = (tokens[:opening_index] + parens_exp +
                           tokens[closing_index + 1:])
                return self.input(" ".join(new_exp))

            else:
                op, index = next_operator(tokens)
                lhs, rhs = tokens[:index], tokens[index + 1:]
                return int(op(self.input(" ".join(lhs)),
                           self.input(" ".join(rhs))))
              
________________________________________________________
import re

vals,signs = {},{'/':float.__truediv__,'*':float.__mul__,'+':float.__add__,'-':float.__sub__,'%':float.__mod__}

def rep(e):
    (a,b),(c,d) = ((i[0]=='-',i.strip('-')) for i in e.groups()[::2])
    return str(signs.get(e[2])((1,-1)[a]*float(vals.get(b,b)),(1,-1)[c]*float(vals.get(d,d))))

calcs = (('%*/',r'(-?\w+(?:\.\d+)?(?:e-?\d+)?) ([%/*]) (-?\w+(?:\.\d+)?(?:e-?\d+)?)',rep),
         ('+-',r'(-?\w+(?:\.\d+)?(?:e-?\d+)?) ([+-]) (-?\w+(?:\.\d+)?(?:e-?\d+)?)',rep))

def calc(st):
    exp = re.sub(r'(?<=[)\w+*%/-])(?=[+*%/-])|(?<=[\w)][+*%/-])(?=[\w(+*%/-])',' ',st.replace(' ',''));print(exp)
    while '(' in exp:
        
        s,n,b = re.search(r'((-?\d*)\(([^()]*)\))',exp).groups()        
        exp = exp.replace(s,str(int(n and (n,-1)[n=='-'] or 1)*compute(b)))
    
    return float(exp) if re.match(r'-?\d+(\.\d+)?(e-?\d+)?$',exp) else compute(exp)

def compute(exp):   
    for a,b,c in calcs:
        while any(i in exp for i in a) and re.match(r'(-?\w+(?:\.\d+)?(?:e-?\d+)? [+/*%-] )+',exp):
            exp = re.sub(b,c,exp,1)
    return (1,-1)[exp[0]=='-']*float(vals.get(exp.strip('-'),exp.strip('-')))

class Interpreter:
    @staticmethod
    def input(e):
        if re.search(r'\w\s+\w',e): raise Exception

        var = re.match(r'([A-Za-z]\w*)=(.+)$',e.replace(' ',''))
        if var:
            vals.update({var[1]:calc(var[2])})
            return vals[var[1]]
            
        return '' if e.isspace() or not e else calc(e)
      
________________________________________________________
from operator import add, sub, mul, truediv, mod
from re import compile

tokenize = compile(r'[-+*/%=()]|[\w.]+').findall

class Interpreter:
    operators = {'+': add, '-': sub, '*': mul, '/': truediv, '%': mod}

    def __init__(self):
        self.vars = {}

    def input(self, expression):
        tokens = tokenize(expression)
        if '=' in tokens:
            value = self.calc(tokens[2:])
            self.vars[tokens[0]] = value
            return value
        return self.calc(tokens)

    def parse(self, item):
        return float(self.vars.get(item, item))

    def calc(self, tokens):
        if not tokens: return ''

        while '(' in tokens:
            opened = closed = 0
            i = tokens.index('(')
            for j, tok in enumerate(tokens):
                if tok == '(': opened += 1
                elif tok == ')': closed += 1
                if opened and opened == closed:
                    tokens[i:j + 1] = [self.calc(tokens[i + 1:j])]
                    break

        for ops in ({'*', '/', '%'}, {'+', '-'}):
            i = 1
            while i < len(tokens):
                if tokens[i] in ops:
                    left, right = map(self.parse, (tokens[i - 1], tokens[i + 1]))
                    tokens[i - 1:i + 2] = [self.operators[tokens[i]](left, right)]
                else: i += 2

        if len(tokens) != 1: raise ValueError

        return self.parse(tokens.pop())
      
________________________________________________________
import enum
import operator
import shlex
from collections import namedtuple


class TokenType(enum.Enum):
    IDENT = 0
    NUM = 1
    OP = 2
    PUNC = 3
    EOF = 4


class Op(enum.Enum):
    ASSIGN = 0
    ADD = operator.add
    SUB = operator.sub
    MUL = operator.mul
    FDIV = operator.floordiv
    TDIV = operator.truediv
    MOD = operator.mod
    POW = operator.pow


class Punc(enum.Enum):
    LPAREN = 0
    RPAREN = 1


Token = namedtuple('Token', ['type', 'value'])


class Interpreter(object):
    def __init__(self):
        self.globals = {}
        self.lex = None
        self.token = None
        self.next_token = None

    def get_token(self):
        # Use shlex to turn input into Tokens.
        token = self.lex.get_token()
        if token == '=':
            return Token(TokenType.OP, Op.ASSIGN)
        elif token == '+':
            return Token(TokenType.OP, Op.ADD)
        elif token == '-':
            return Token(TokenType.OP, Op.SUB)
        elif token == '*':
            # look ahead for double *, signifying pow
            next = self.lex.get_token()
            if next == '*':
                raise NotImplementedError
                # return Token(TokenType.OP, Op.FDIV)
            self.lex.push_token(next)
            return Token(TokenType.OP, Op.MUL)
        elif token == '/':
            # look ahead for double /, signifying floor div.
            next = self.lex.get_token()
            if next == '/':
                return Token(TokenType.OP, Op.FDIV)
            self.lex.push_token(next)
            return Token(TokenType.OP, Op.TDIV)
        elif token == '%':
            return Token(TokenType.OP, Op.MOD)
        elif token == '(':
            return Token(TokenType.PUNC, Punc.LPAREN)
        elif token == ')':
            return Token(TokenType.PUNC, Punc.RPAREN)
        elif token.isdigit():
            # look ahead for a floating point value.
            dot, num = self.lex.get_token(), self.lex.get_token()
            if dot == '.' and num.isdigit:
                return Token(TokenType.NUM, float(token + '.' + num))
            self.lex.push_token(num)
            self.lex.push_token(dot)
            return Token(TokenType.NUM, int(token))
        elif token.isalnum():
            return Token(TokenType.IDENT, token)
        else:
            return Token(TokenType.EOF, self.lex.eof)

    def next(self):
        self.token = self.next_token
        self.next_token = self.get_token()

    def next_if(self, attr='type', *conds, throw=False):
        # next_if advances the current Token if the attr of the next token
        # matches the attrs inside `conds`.
        # If throw is True, it will throw a SyntaxError if the Token is not valid.
        token = self.next_token
        if not token or getattr(token, attr) not in conds:
            if throw:
                raise SyntaxError("Invalid syntax, expected {0}, recieved {1} instead".format(conds, token))
            return False
        self.next()
        return True

    def load_var(self):
        # Load a variable by name from the global scope.
        # If non existant, raises a NameError
        value = self.globals.get(self.token.value)
        if value is None:
            raise NameError('"{x}" is not defined.'.format(x=self.token.value))
        return value

    def program(self):
        # Entry point for the parser.
        # If input is empty, return an empty string.
        if self.next_if('type', TokenType.EOF):
            return ''
        return self.variable()

    def variable(self):
        # Handle variable assignment/printing.
        while self.next_if('type', TokenType.IDENT):
            lvalue = self.token
            if self.next_if('value', Op.ASSIGN):
                ret = self.variable()
                self.globals[lvalue.value] = ret
                return ret
            elif self.next_token.type == TokenType.EOF:
                return self.load_var()

        return self.expression()

    def expression(self):
        # Implements `<term> | <expression> "+" <term>`
        lvalue = self.term()

        while self.next_if('value', Op.ADD, Op.SUB):
            op = self.token.value.value
            rvalue = self.term()
            lvalue = op(lvalue, rvalue)
        if self.token.type != TokenType.IDENT and self.next_token.value == Op.ASSIGN:
            raise SyntaxError("Cannot assign to constant")
        return lvalue

    def term(self):
        # Implements `<factor> | <term> "*" <factor>`

        lvalue = self.factor()
        while self.next_if('value', Op.FDIV, Op.TDIV, Op.MUL, Op.MOD):
            op = self.token.value.value
            rvalue = self.factor()
            lvalue = op(lvalue, rvalue)
        return lvalue

    def factor(self):
        # Implements `<constant> | <variable> | "(" <expression> ")"`

        # variable() eats the variable token when testing for assignment (if the variable is the first token),
        # disallowing factor() from accessing it.
        # this is so bad....I had this problem and I fixed it before, but I forgot how I did D:
        if self.token and self.token.type == TokenType.IDENT:
            return self.load_var()

        # handle single standing numbers and variables
        if self.next_if('type', TokenType.NUM, TokenType.IDENT):
            if self.next_if('type', TokenType.NUM, TokenType.IDENT):
                raise SyntaxError("Invalid syntax")
            if self.token.type == TokenType.IDENT:
                return self.load_var()
            return self.token.value

        # handle any expressions inside parens
        if self.next_if('value', Punc.LPAREN):
            value = self.expression()
            self.next_if('value', Punc.RPAREN, throw=True)
            return value

        if self.next_if('type', TokenType.EOF, throw=True):
            return ''

    def input(self, expr):
        print(expr)
        self.lex = shlex.shlex(expr)
        self.next()
        return self.program()
      
________________________________________________________
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
        if len(tokens) == 0: return ''

        if '=' in tokens:
            self.vars[tokens[0]] = self.evaluate(tokens[2:])
            return float(self.vars[tokens[0]])

        return self.evaluate(tokens)

    def isnumber(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def evaluate(self, tokens):
        stack, i = [], 0
        while i < len(tokens):
            if tokens[i] == '(': stack.append(i)
            if tokens[i] == ')':
                start, end = stack.pop(), i + 1
                tmp = self.exp(tokens[start + 1: end - 1])
                del tokens[start: end]
                i = start
                tokens.insert(start, str(tmp))
            i += 1
        return self.exp(tokens)

    def exp(self, tokens):
        result, number, temp, sign, op = 0, 0, 1, 1, "*"
        prev = op
        for c in tokens:
            if c == "+" or c == "-":
                temp = temp * number if op == "*" else temp / number if op == "/" else temp % number
                result += sign * temp
                temp = 1
                number = 0
                op = "*"
                sign = 1 if c == "+" else -1
            elif c == "*" or c == "/" or c == "%":
                temp = temp * number if op == "*" else temp / number if op == "/" else temp % number
                number = 0
                op = c
            elif self.isnumber(c): number = float(c)
            elif c.isalpha(): number = float(self.vars[c])

            if (prev in '+-*/%') == (c in '+-*/%'):
                raise ValueError("Invalid Input")
            prev = c

        temp = temp * number if op == "*" else temp / number if op == "/" else temp % number
        result += sign * temp
        return round(result, 5)
      
________________________________________________________
import re

def isnumber(str):
  try:
    float(str)
  except:
    return False
  else:
    return True

class Interpreter:
  def __init__(self):
    self.vars = {}

  @staticmethod
  def tokenize(expression):
    tokens = []
    if expression != '':
      regex = re.compile('\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*')
      tokens = regex.findall(expression)
      tokens = [token for token in tokens if not token.isspace()]
    return tokens

  operators = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '%': lambda a, b: a % b,
    '=': lambda a, b: b
  }

  def value(self, var):
    if not isnumber(var):
      var = self.vars[var]
    return var

  def eval_operator(self, operator, left, right):
    if operator == '=':
      self.vars[left] = right
    left = self.value(left)
    right = self.value(right)
    return Interpreter.operators[operator](left, right)

  def current_token(self):
    return self.tokens[self.token_index]

  def token(self):
    token = self.current_token()
    self.token_index += 1
    return token

  def has_token(self):
    return self.token_index < len(self.tokens)

  def operator(self):
    return self.token()

  def factor(self):
    token = self.token()
    if token == '(':
      return self.expression_top()
    if isnumber(token):
      return float(token)
    return token

  def expression_bottom(self):
    left = self.factor()
    while self.has_token() and self.current_token() in ['*', '/', '%']:
      operator = self.operator()
      right = self.factor()
      left = self.eval_operator(operator, left, right)
    return left

  def expression_middle(self):
    left = self.expression_bottom()
    while self.has_token() and self.current_token() in ['+', '-']:
      operator = self.operator()
      right = self.expression_bottom()
      left = self.eval_operator(operator, left, right)
    return left

  def expression_top(self):
    left = self.expression_middle()
    while self.has_token() and self.current_token() in ['=', ')']:
      operator = self.operator()
      if operator == ')':
        break
      right = self.expression_middle()
      left = self.eval_operator(operator, left, right)
      left = self.value(left)
    left = self.value(left)
    return left

  def eval(self):
    result = self.expression_top()
    if self.has_token():
      raise BaseException('Invalid input')
    return result

  def input(self, expression):
    self.tokens = Interpreter.tokenize(expression)

    if len(self.tokens) == 0:
      return ''

    self.token_index = 0
    return self.eval()
  
________________________________________________________
class Interpreter:
    def __init__(self):
        self.env = {}
    def input(self, expression):
        if expression.strip() == "":
            return ""
        exec("_ = "+expression, self.env)
        return self.env["_"]
      
________________________________________________________
import re
class Interpreter:
    d={}
    def input(_,e):
        if not e or e.isspace(): return ''
        try:
            exec('final = '+e)
        except:
            exec('final = '+re.sub('[A-Za-z]+(?!\s*=)',lambda m: str(_.d[m[0]]),e))
        _.d.update(locals())
        return _.d['final']     
      
________________________________________________________
import re
from collections import namedtuple
from operator import add, sub, mul, truediv, mod

Token = namedtuple('Token', ['type', 'value'])

NUMBER = 'number'
IDENTIFIER = 'identifier'
OPERATOR = 'operator'
OPEN_PAREN = 'open_paren'
CLOSE_PAREN = 'close_paren'

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
            token = self._identifier() or self._operator() or self._open_brace() or self._close_brace()
            if token:
                yield token
                continue
            token = self._whitespace()
            if token:
                continue
            raise UnknownTokenError()

class InvalidTokenError(Exception): pass

class ArithParser(object):
    def __init__(self, identifier_map=dict()):
        self.stack = [[]]
        self.identifier_map = identifier_map
        
    def _assert_type(self, token, token_type):
        if token.type != token_type:
            raise InvalidTokenError()
        
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
            rhs_value = self._resolve_num_or_id(operand2)
            self._update_identifier(operand1, rhs_value)
            self.stack[-1].append(Token(NUMBER, rhs_value))
        else:
            value1 = self._resolve_num_or_id(operand1)
            value2 = self._resolve_num_or_id(operand2)
            new_value = {'+': add, '-': sub, '*': mul, '/': truediv, '%': mod
                }[prev_op.value](value1, value2)
            self.stack[-1].append(Token(NUMBER, new_value))
    
    def feed_token(self, token):
        if token.type in (NUMBER, IDENTIFIER):
            self.stack[-1].append(token)
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
            self.stack[-1].append(Token(NUMBER, value))
    
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
        print(expression)
        tokenizer = Tokenizer(expression)
        arith_parser = ArithParser()
        for token in tokenizer.tokens():
            arith_parser.feed_token(token)
        value, self.vars = arith_parser.result()
        return value
