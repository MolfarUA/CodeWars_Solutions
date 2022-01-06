def parse_expr(s):
  s = s[1:-1] if s[0]=='(' else s
  if s.isdigit(): return ('num', int(s))
  elif ' ' not in s: return ('var', s)
  depth = 0
  first_space = s.index(' ')
  op = s[:first_space]
  for i, c in enumerate(s[first_space+1:]):
    if c=='(': depth += 1
    elif c==')': depth -= 1
    if depth == 0 and c==' ':
      second_space = first_space + i + 1
      return op, parse_expr(s[first_space+1:second_space]), parse_expr(s[second_space+1::])
  return op, parse_expr(s[first_space+1:])

def deriv(expr):
  op, a, b = expr + ((None,) if len(expr) < 3  else ())
  return {
    'num': lambda: ('num', 0),
    'var': lambda: ('num', 1),
    '+': lambda:('+', deriv(a), deriv(b)),
    '-': lambda:('-', deriv(a), deriv(b)),
    '*': lambda: ('+', ('*', deriv(a), b), ('*', a, deriv(b))),
    '/': lambda: ('/', ('-', ('*', deriv(a), b), ('*', a, deriv(b))), ('^', b, ('num', 2))),
    'exp': lambda: ('*', deriv(a), ('exp', a)),
    'tan': lambda: ('*', deriv(a), ('+', ('num', 1), ('^', ('tan', a), 2))),
    'sin': lambda: ('*', deriv(a), ('cos', a)),
    'cos': lambda: ('*', deriv(a), ('*', ('num', -1), ('sin', a))),
    'ln': lambda: ('/', deriv(a), a),
    '^': lambda: ('*', ('*', ('num', b[1]), ('^', a, ('num', b[1]-1))), deriv(a)) if b[0] == 'num' else ('*', expr, deriv(('*', b, ('ln', a))))
  }.get(op)()
  
def simplify(expr):
  op, a, b = expr + ((None,) if len(expr) < 3  else ())
  if type(a) == type(()): a = simplify(a)
  if type(b) == type(()): b = simplify(b)
  if op in ('num', 'var'): return a
  elif op == '*' and 0 in (a, b): return 0
  elif op == '^' and b == 1: return a
  elif op == '^' and b == 0: return 1
  elif op == '*' and 1 in (a, b): return a * b
  elif op == '+' and 0 in (a, b): return a if a else b
  elif op == '-' and b == 0: return a
  elif type(a) == type(b) == int: return calc(op, a, b)
  else: return (op, a) + ((b,) if b else ())

def calc(op, a, b):
  return {'+': a+b, '-': a-b, '*': a*b, '/': a/b, '^': a**b}.get(op)
  
def to_str(expr):
  return str(expr).replace(',', '').replace('\'', '')

def diff(expr):
  return to_str(simplify(deriv(parse_expr(expr))))

______________________________________________
from contextlib import suppress
def diff(expr):
    return str(parse(expr).diff().simplify())

class Expr:
    def __init__(self, val=None, **kwargs):
        self.__dict__.update(kwargs)
        self.val = val
    
    def __eq__(self, other):
        if not isinstance(other, Expr):
            return self.val is not None and self.val == other
        elif self.val is not None and other.val is not None:
            return self.val == other.val
        else:
            return False

class Atom(Expr):
    def simplify(self): return self
    def __str__(self): return str(self.val)
class Var(Atom):
    def diff(self): return Val(1)
class Val(Atom):
    def __init__(self, val):
        try:
            val = int(val)
        except ValueError:
            val = float(val)
        super().__init__(val)
    def diff(self): return Val(0)

class Binary(Expr):
    def __init__(self, a, b):
        super().__init__(a=a.simplify(), b=b.simplify())
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.a == other.a and self.b == other.b
        else: return super().__eq__(other)
    def __str__(self):
        if self.val is not None:
            return str(self.val)
        return '({} {} {})'.format(self.symbol, self.a, self.b)
class Add(Binary):
    symbol = '+'
    def diff(self): return self.a.diff() + self.b.diff()
    def simplify(self):
        with suppress(TypeError):
            if self.a == 0: return self.b
            if self.b == 0: return self.a
            self.val = self.a.val + self.b.val
        return self
class Sub(Binary):
    symbol = '-'
    def diff(self): return self.a.diff() - self.b.diff()
    def simplify(self):
        with suppress(TypeError):
            if self.b == 0: return self.a
            if self.a == 0: return (Val(-1) * self.b).simplify()
            if self.a == self.b: self.val = 0
            else: self.val = self.a.val - self.b.val
        return self
class Mul(Binary):
    symbol = '*'
    def diff(self): return self.a * self.b.diff() + self.b * self.a.diff()
    def simplify(self):
        with suppress(TypeError):
            if self.a == 1: return self.b
            if self.b == 1: return self.a
            if self.a == 0 or self.b == 0: self.val = 0
            elif not isinstance(self.a.val * self.b.val, str):
                self.val = self.a.val * self.b.val
        return self
class Div(Binary):
    symbol = '/'
    def diff(self): 
        return (self.b * self.a.diff() - self.a * self.b.diff()) / self.b ** 2
    def simplify(self):
        with suppress(TypeError):
            if self.a == self.b: return Node(1)
            elif self.b == 1: return self.a
            self.val = self.a.val / self.b.val
        return self
class Pow(Binary):
    symbol = '^'
    def diff(self): return self.b * self.a.diff() * self.a ** (self.b - 1)
    def simplify(self):
        self.a, self.b = self.a.simplify(), self.b.simplify()
        with suppress(TypeError):
            if self.b == 1: return self.a
            if self.a == 0 and self.b != 0: self.val = 0
            elif self.a == 1 or self.b == 0: self.val = 1
            else: self.val = self.a.val ** self.b.val
        return self

def define_op(Op):
    def func(self, other):
        if isinstance(other, str):
            other = parse(other)
        elif not isinstance(other, Expr):
            other = Val(other)
        return Op(self, other)
    return func

Expr.__add__ = define_op(Add)
Expr.__mul__ = define_op(Mul)
Expr.__pow__ = define_op(Pow)
Expr.__sub__ = define_op(Sub)
Expr.__truediv__ = define_op(Div)

class Unary(Expr):
    def __init__(self, a):
        self.val = None
        self.a = a.simplify()
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.a == other.a
        else: return super().__eq__(other)
    def __str__(self):
        return '({} {})'.format(type(self).__name__.lower(), self.a)
    def simplify(self):
        return self
class Sin(Unary):
    def diff(self): return self.a.diff() * Cos(self.a)
class Cos(Unary):
    def diff(self): return Val(-1) * self.a.diff() * Sin(self.a)
class Tan(Unary):
    def diff(self): return self.a.diff() * (Val(1) + self ** 2)
class Exp(Unary):
    def diff(self): return self.a.diff() * self
class Ln(Unary):
    def diff(self): return self.a.diff() / self.a


def parse(s):
    Ops = {
        '+':Add, '-':Sub, '*':Mul, '/':Div, '^':Pow,
        'sin':Sin, 'cos':Cos, 'tan':Tan, 'exp':Exp, 'ln':Ln
    }
    nodes, match = [], []
    s = s.replace('(', '( ').replace(')', ' )')
    for token in s.split():
        if token == '(':
            match.append(len(nodes))
        elif token == ')':
            start = match.pop()
            nodes[start:] = [nodes[start](*nodes[start + 1:])]
        else:
            if token in Ops:
                n = Ops[token]
            elif token == 'x':
                n = Var('x')
            else:
                n = Val(token)
            nodes.append(n)
    return nodes[0]
  
______________________________________________
from operator import add, sub, mul, truediv as div, pow
import re


OPS_1_TERM = {'cos','sin','tan','exp','ln'}

VARS, NUMS, MISC = "[a-zA-Z]+", "-?\d+", "[(]"
STR_2_TERM = "[+*/^-]"
STR_1_TERM = "|".join(OPS_1_TERM)

TOKENIZER = re.compile("|".join([VARS,NUMS,MISC,STR_1_TERM,STR_2_TERM]))


def diff(s): return str(parseExpr(iter(TOKENIZER.findall(s))).diff().simplify()).replace(".0","")


def parseExpr(tokens):
    for tok in tokens:
        if tok == "(":          return parseExpr(tokens)
        if tok in OPS_1_TERM:   return eval(tok.capitalize())( parseExpr(tokens) )
        if tok in Expr.SYMBOL:  return eval(Expr.SYMBOL[tok])( parseExpr(tokens), parseExpr(tokens) )
        if tok.isalpha():       return Var(tok)
        if tok.isdigit():       return Num(tok)



class Expr(object):
    
    PRECISION = 1e-8
    SYMBOL = {'Add':'+', 'Sub':'-', 'Mul':'*', 'Div':'/', 'Pow':'^',
              'Exp':'exp', 'Ln':'ln',
              'Cos':'cos', 'Sin':'sin', 'Tan':'tan'}
    for k,v in list(SYMBOL.items()): SYMBOL[v] = k
    
    def getSymbol(self):    return Expr.SYMBOL[self.__class__.__name__]
    def isNum(self):        return isinstance(self, Num)
    def isZero(self):       return isinstance(self, Num) and abs(float(self.var)) < Expr.PRECISION
    def isOne(self):        return isinstance(self, Num) and abs(float(self.var)-1) < Expr.PRECISION
    
    def overrideError(self):raise Exception("Override lacking in " + self.__class__.__name__)
    def diff(self):         self.overrideError()
    def simplify(self):     self.overrideError()



class Term(Expr):
    def __init__(self, s):  self.var = s
    def __str__(self):      return self.var
    def simplify(self):     return self

class Num(Term):
    def diff(self):         return Num("0")

class Var(Term):
    def diff(self):         return Num("1")
    

class NonTerm2(Expr):
    def __init__(self,l,r):     self.left, self.right = l, r
    def __str__(self):          return "({} {} {})".format(self.getSymbol(), self.left, self.right)
    def evaluate(self, *args):  return Num(str(eval(self.__class__.__name__.lower())(*map(lambda e: float(str(e)), args))))
    
class Add(NonTerm2):
    def diff(self):             return Add(self.left.diff(), self.right.diff())
    def simplify(self):
        sl, sr = self.left.simplify(), self.right.simplify()
        return (sr if sl.isZero() else
                sl if sr.isZero() else
                self.evaluate(sl,sr) if sl.isNum() and sr.isNum() else
                Add(sl, sr))
                
class Sub(NonTerm2):
    def diff(self):             return Sub(self.left.diff(), self.right.diff())
    def simplify(self):
        sl, sr = self.left.simplify(), self.right.simplify()
        return (sr if sl.isZero() else
                Mul(Num("-1"), sl).simplify() if sr.isZero() else
                self.evaluate(sl,sr) if sl.isNum() and sr.isNum() else
                Sub(sl, sr))
                
class Mul(NonTerm2):
    def diff(self):             return Add( Mul(self.left.diff(), self.right),
                                            Mul(self.left, self.right.diff()))
    def simplify(self):
        sl, sr = self.left.simplify(), self.right.simplify()
        return (Num("0") if sl.isZero() or sr.isZero() else
                sl if sr.isOne() else
                sr if sl.isOne() else
                self.evaluate(sl,sr) if sl.isNum() and sr.isNum() else
                Mul(sl, sr))
                
class Div(NonTerm2):
    def diff(self):             return Div( Sub( Mul(self.left, self.right.diff()),
                                                 Mul(self.left.diff(), self.right)),
                                            Pow(self.right, Num("2")))
    def simplify(self):
        sl, sr = self.left.simplify(), self.right.simplify()
        return (Num("0") if sl.isZero() or sr.isZero() else
                sl if sr.isOne() else
                self.evaluate(sl,sr) if sl.isNum() and sr.isNum() else
                Div(sl, sr))

class Pow(NonTerm2):
    def diff(self):             return Mul( self.right, Pow(self.left, Sub(self.right, Num("1"))) )
    def simplify(self):
        sl, sr = self.left.simplify(), self.right.simplify()
        return (Num("1") if sl.isZero() else
                Num("0") if sl.isZero() else
                sl if sr.isOne() else
                self.evaluate(sl,sr) if sl.isNum() and sr.isNum() else
                Pow(sl, sr))


class NonTerm1(Expr):
    def __init__(self, e):  self.val = e
    def __str__(self):      return "({} {})".format(self.getSymbol(), self.val)

class Tan(NonTerm1):
    def diff(self):         return Mul( self.val.diff(), Add(Num("1"), Pow(Tan(self.val), Num("2"))) )
    def simplify(self):     return Tan(self.val.simplify())

class Sin(NonTerm1):
    def diff(self):         return Mul( self.val.diff(), Cos(self.val) )
    def simplify(self):     return Sin(self.val.simplify())
    
class Cos(NonTerm1):
    def diff(self):         return Mul( Mul(Num("-1"), self.val.diff()), Sin(self.val) )
    def simplify(self):     return Cos(self.val.simplify())
    
class Exp(NonTerm1):
    def diff(self):         return Mul( self.val.diff(), Exp(self.val) )
    def simplify(self):     return Exp(self.val.simplify())
    
class Ln(NonTerm1):
    def diff(self):         return Mul( self.val.diff(), Div(Num("1"), self.val) )
    def simplify(self):     return Ln(self.val.simplify())
    
______________________________________________
from contextlib import suppress
class Node:
    def __init__(self, val=None, op=None, args=None):
        self.val = val
        self.op = op
        self.args = args
    
    @staticmethod
    def from_str(s):
        nodes, match = [], []
        s = s.replace('(', '( ').replace(')', ' )')
        for token in s.split():
            if token == '(':
                match.append(len(nodes))
            elif token == ')':
                start = match.pop()
                nodes[start:] = [Node(op=nodes[start].val, args=nodes[start + 1:])]
            else:
                nodes.append(Node(token))
        return nodes[0]
    
    def diff(self):
        if self.val is not None:
            if self.val == 'x':
                return Node(1)
            else:
                return Node(0)
        try:
            u, v = self.args
        except ValueError:
            u = self.args[0]
        
        if self.op in '+-':
                return Node(op=self.op, args=[u.diff(), v.diff()])
        elif self.op == '*':
            return u * v.diff() + v * u.diff()
        elif self.op == '/':
            return (v * u.diff() - u * v.diff()) / v ** 2
        elif self.op == '^':
            return v * u.diff() * u ** (v - 1)
        
        if self.op == 'sin':
            return u.diff() * Node(op='cos', args=[u])
        elif self.op == 'cos':
            return Node(-1) * u.diff() * Node(op='sin', args=[u])
        elif self.op == 'tan':
            return u.diff() * (Node(1) + Node(op='tan', args=[u]) ** 2)
        elif self.op == 'exp':
            return u.diff() * self
        elif self.op == 'ln':
            return u.diff() / u
    
    def simplify(self):
        if self.val is not None:
            if self.val != 'x':
                try:
                    self.val = int(self.val)
                except ValueError:
                    self.val = float(self.val)
            return self
        
        old = repr(self)
        try:
            u = self.args[0].simplify()
            v = self.args[1].simplify()
            self.args = [u, v]
        except IndexError:
            return self
        
        with suppress(TypeError):
            if self.op == '*':
                if u == 1: return v
                if v == 1: return u
                if u == 0 or v == 0: self.val = 0
                elif not isinstance(u.val*v.val, str):
                    self.val = u.val * v.val
            elif self.op == '/':
                if u == v: return Node(1)
                elif v == 1: return u
                self.val = u.val / v.val
            elif self.op == '+':
                if v == 0: return u
                if u == 0: return v
                self.val = u.val + v.val
            elif self.op == '-':
                if u == v: self.val = 0
                else: self.val = u.val - v.val
            elif self.op == '^':
                if v == 1: return u
                if u == 1 or v == 0: self.val = 1
                else: self.val = u.val ** v.val
        return self
    
    def __eq__(self, other):
        if not isinstance(other, Node):
            return self.val is not None and self.val == other
        elif self.val is not None and other.val is not None:
            return self.val == other.val
        else:
            return self.op == other.op and self.args == other.args
    
    def define_op(op):
        def func(self, other):
            if isinstance(other, str):
                other = Node.from_str(other)
            elif not isinstance(other, Node):
                other = Node(other)
            return Node(op=op, args=[self, other])
        return func
    
    __add__ = define_op('+')
    __mul__ = define_op('*')
    __pow__ = define_op('^')
    __sub__ = define_op('-')
    __truediv__ = define_op('/')
    
    def __str__(self):
        if self.val is not None:
            return str(self.val)
        else:
            return '({} {})'.format(self.op, ' '.join(map(str,self.args)))

def diff(expr):
    return str(Node.from_str(expr).diff().simplify())
  
______________________________________________
from operator import add, sub, mul, truediv, pow
from math import sin, cos, tan, exp, log

operators = {
    # operator symbol: (func, arity)
    '+': (add, 2),
    '-': (sub, 2),
    '*': (mul, 2),
    '/': (truediv, 2),
    '^': (pow, 2),
    'sin': (sin, 1),
    'cos': (cos, 1),
    'tan': (tan, 1),
    'exp': (exp, 1),
    'ln': (log, 1),
}

short_circuits = {
    '-': [
        (lambda args: str(args[0]) == str(args[1]), '0')
    ],
    '*': [
        (lambda args: '0' in args, '0')
    ],
    '/': [
        (lambda args: args[0] == '0', '0')
    ],
    '^': [
        (lambda args: args[0] == '0', '0'),
        (lambda args: args[1] == '0', '1'),
        (lambda args: args[0] == '1', '1')
    ]
}

identities = {
    '+': (lambda args: '0' in args, '0'),
    '-': (lambda args: args[1] == '0', '0'),
    '*': (lambda args: '1' in args, '1'),
    '/': (lambda args: args[1] == '1', '1'),
    '^': (lambda args: args[1] == '1', '1')
}

derivatives = {
    'ln': lambda args: f'(/ 1 {args[0]})',
    'sin': lambda args: f'(cos {args[0]})',
    'cos': lambda args: f'(* -1 (sin {args[0]}))',
    'tan': lambda args: f'(/ 1 (^ (cos {args[0]}) 2))',
    'exp': lambda args: f'(exp {args[0]})'
}

class ExpressionTree:
    def __init__(self, simple_value = None):
        self.op_symbol = None
        self.func = None
        self.arity = None
        self.args = []
        self.simple_value = simple_value
        
    def __eq__(self, other):
        return self.simple_value == other
                    
    def parse(self, vals, index=0):
        if len(vals) == 1:
            self.simple_value = vals[0]
            return
        self.args = []
        self.op_symbol = vals[index]
        (self.func, self.arity) = operators[vals[index]]
        while len(self.args) < self.arity:
            index += 1
            if vals[index] in operators:
                new_node = ExpressionTree()
                index = new_node.parse(vals, index)
                self.args.append(new_node)
            else:
                self.args.append(ExpressionTree(vals[index]))
        return index
    
    def simplify(self):
        if self.simple_value is not None:
            return
        
        for index, arg in enumerate(self.args):
            if arg.simple_value is not None and len(arg.args) > 0:
                self.args[index] = ExpressionTree(arg.simple_value)
            else:
                arg.simplify()
        
        # Short circuits
        if self.op_symbol in short_circuits:
            shorts = short_circuits[self.op_symbol]
            for (condition, value) in shorts:
                if condition(self.args):
                    self.simple_value = value
                    return
        
        if all([is_constant(arg.simple_value) for arg in self.args]) and self.arity == 2:
            self.simple_value = str(self.func(
                get_constant_value(self.args[0].simple_value), 
                get_constant_value(self.args[1].simple_value)
                ))
            print(self.simple_value)
            return

        # Identities
        if self.op_symbol in identities:
            (condition, identity) = identities[self.op_symbol]
            if condition(self.args):
                non_identity_arg = [arg for arg in self.args if arg.simple_value != identity][0]
                self.op_symbol = non_identity_arg.op_symbol
                self.func = non_identity_arg.func
                self.arity = non_identity_arg.arity
                self.args = non_identity_arg.args
                self.simple_value = non_identity_arg.simple_value
            
        # The following sections are just undocumented quirks of the Kata's implementation
        # Move constants to first position for commutative operators
        if self.arity == 2 \
        and self.args[1].simple_value is not None \
        and self.args[0].simple_value is None \
        and self.op_symbol in ['+', '*']:
            swap = self.args[1]
            self.args[1] = self.args[0]
            self.args[0] = swap
            
        # Expand where possible
        if self.op_symbol == '*' \
        and self.args[0].simple_value is not None \
        and is_constant(self.args[0].simple_value) \
        and self.args[1].simple_value is None \
        and self.args[1].args[0].simple_value is not None \
        and is_constant(self.args[1].args[0].simple_value) \
        and self.args[1].op_symbol in ['*', '/']:
            self.op_symbol = self.args[1].op_symbol
            self.func = self.args[1].func
            new_arg = str( \
                get_constant_value(self.args[0].simple_value) * \
                get_constant_value(self.args[1].args[0].simple_value))
            self.args = self.args[1].args
            self.args[0] = ExpressionTree(new_arg)
            
    def derive(self):
        if self.simple_value is not None:
            if is_constant(self.simple_value):
                self.simple_value = '0'
            else:
                self.simple_value = '1'
            return
            
        # Derive first order terms
        if self.op_symbol in ['+', '-']:
            for arg in self.args:
                arg.derive()
            return
        
        # Apply product rule
        if self.op_symbol == '*':
            f = str(self.args[0])
            g = str(self.args[1])
            self.args[0].derive()
            self.args[1].derive()
            dfdx = str(self.args[0])
            dgdx = str(self.args[1])
            prefix_string = f'(+ (* {dgdx} {f}) (* {dfdx} {g})'
            self.parse(string_to_vals(prefix_string))
            return
            
        # Apply quotient rule
        if self.op_symbol == '/':
            f = str(self.args[0])
            g = str(self.args[1])
            self.args[0].derive()
            self.args[1].derive()
            dfdx = str(self.args[0])
            dgdx = str(self.args[1])
            prefix_string = f'(/ (- (* {dfdx} {g}) (* {f} {dgdx})) (^ {g} 2))'
            self.parse(string_to_vals(prefix_string))
            return
        
        # Apply power rule
        if self.op_symbol == '^':
            prefix_string = f'(* {self.args[1]} (^ {self.args[0]} (- {self.args[1]} 1))'
            self.parse(string_to_vals(prefix_string))
            return
        
        # Chain rule, use explicit derivatives
        f = derivatives[self.op_symbol](self.args)
        print('===')
        print(self.args[0].__dict__)
        self.args[0].derive()
        print(self.args[0].__dict__)
        print('===')
        dgdx = str(self.args[0])
        prefix_str = f'(* {dgdx} {f})'
        self.parse(string_to_vals(prefix_str))
            
    def __repr__(self):
        if self.simple_value is not None:
            return self.simple_value
        return '(' + self.op_symbol + ' ' + ' '.join([str(arg) for arg in self.args]) + ')'
    
def is_constant(val):
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False
    
def get_constant_value(val):
    try:
        return int(val)
    except ValueError:
        return float(val)

def string_to_vals(string):
    return string.replace('(', '').replace(')', '').split(' ')
        
def diff(s):
    vals = string_to_vals(s)
    tree = ExpressionTree()
    tree.parse(vals)
    print(tree)
    tree.simplify()
    print(tree)
    tree.derive()
    print(tree)
    tree.simplify()
    print(tree)
    return str(tree)
  
______________________________________________
from typing import NamedTuple
from functools import singledispatch

# ----------------------------
# Some types used to identify particular nodes in the tree

class Const(NamedTuple):
    value: int

class Variable(NamedTuple):
    value: str

class Func(NamedTuple):
    name: str
    arg: NamedTuple

class Oper(NamedTuple):
    name: str
    lhs: NamedTuple
    rhs: NamedTuple

# ----------------------------
# How to turn a tree into a prefixed string

@singledispatch
def pretty(node) -> str:
    return str(node)

@pretty.register
def _(node: Const) -> str:
    return f"{node.value}"

@pretty.register
def _(node: Variable) -> str:
    return f"x"

@pretty.register
def _(node: Func) -> str:
    return f"({node.name} " + pretty(node.arg) + ")"

@pretty.register
def _(node: Oper) -> str:
    return f"({node.name} " + pretty(node.lhs) + " " + pretty(node.rhs) + ")"

# ----------------------------
# Quick and dirty simplification rules

def distribute(node, const: Const) -> NamedTuple:
    if const.value == 1:
        return node
    if const.value == 0:
        return Const(value=0)
    if isinstance(node, Oper) and node.name == '/' and isinstance(node.lhs, Const):
        return Oper(name='/', lhs=const.value*node.lhs.value, rhs=node.rhs)
    return Oper(name='*', lhs=const, rhs=node)

def pythonize(operation):
    if operation == '^':
        return '**'
    else:
        return operation

def build_simplified(operation, lhs, rhs) -> NamedTuple:
    if isinstance(lhs, Const) and isinstance(rhs, Const):
        return Const(value=eval(f"{lhs.value}{pythonize(operation)}{rhs.value}")) # possible divide by zero
    if operation == "*" and isinstance(lhs, Const):
        return distribute(rhs, lhs)
    if operation == "*" and isinstance(rhs, Const):
        return distribute(lhs, rhs)
    if operation == "+" and isinstance(lhs, Const) and lhs.value == 0:
        return rhs
    if operation == "+" and isinstance(rhs, Const) and rhs.value == 0:
        return lhs
    if operation == "^" and isinstance(rhs, Const) and rhs.value == 0:
        return Const(value=1)
    if operation == "^" and isinstance(rhs, Const) and rhs.value == 1:
        return lhs
    return Oper(name=operation, lhs=lhs, rhs=rhs)

# ----------------------------
# How to handle the "chain rule" of differentiation

@singledispatch
def chain(node, by)  -> NamedTuple:
    return node

@chain.register
def _(node: Variable, by) -> NamedTuple:
    return by

@chain.register
def _(node: Func, by) -> NamedTuple:
    return Func(name=node.name, arg=chain(node.arg, by))

@chain.register
def _(node: Oper, by) -> NamedTuple:
    return Oper(name=node.name, lhs=chain(node.lhs, by), rhs=chain(node.rhs, by))


# ----------------------------
# How to comppute the derivative of an expression tree

@singledispatch
def deriv(node) -> NamedTuple:
    raise NotImplemented

@deriv.register
def _(node: Const) -> NamedTuple:
    return Const(value=0)

@deriv.register
def _(node: Variable) -> NamedTuple:
    return Const(value=1)

@deriv.register
def _(node: Func) -> NamedTuple:
    if isinstance(node.arg, Variable) or isinstance(node.arg, Const):
        if node.name == "ln":
            return build_simplified("/", deriv(node.arg), node.arg)
        if node.name == "cos":
            return build_simplified("*", Const(value=-1), Func('sin', node.arg))
        if node.name == "sin":
            return Func('cos', node.arg)
        if node.name == "exp":
            return node
        if node.name == "tan":
            return build_simplified("/", Const(value=1), Oper(name="^", lhs=Func('cos', node.arg), rhs=Const(value=2)))
    else:
        gp = deriv(node.arg)
        fp = deriv(Func(name=node.name, arg=Variable(value='x')))
        return build_simplified('*', chain(fp, node.arg), gp)

@deriv.register
def _(node: Oper) -> NamedTuple:
    if node.name == "+":
        return build_simplified("+", deriv(node.lhs), deriv(node.rhs))
    if node.name == "-":
        return build_simplified("-", deriv(node.lhs), deriv(node.rhs))
    if node.name == "*":
        return build_simplified("+", build_simplified('*', deriv(node.lhs), node.rhs), build_simplified('*', node.lhs, deriv(node.rhs)))
    if node.name == "/":
        return build_simplified("/", build_simplified("-", build_simplified('*', deriv(node.lhs), node.rhs), build_simplified('*', node.lhs, deriv(node.rhs))), build_simplified('^', node.rhs, Const(value=2)))
    if node.name == "^" and isinstance(node.rhs, Const):
        return build_simplified("*", node.rhs, build_simplified('^', node.lhs, build_simplified('-', node.rhs, Const(value=1))))
    return Const(value=1)

# ----------------------------
# Quick and dirty parsing functions

def next_token(expression: str) -> str:
    return expression.partition(' ')[0].replace(')', '')


def scan(expression: str):
    #print(f"call scan on : |{expression}|")
    if expression[0] != '(' or expression[-1] != ')':
        raise RuntimeError("invalid expression string")
    args = []
    oper = next_token(expression[1:])
    count = 0
    start = len(oper)+2
    head = start
    while head < len(expression)-1:
        if expression[head] == '(':
            if count == 0:
                #print(f"new opening : {head}")
                start = head
            count += 1
            head += 1
            continue
        if expression[head] == ')':
            count -= 1
            if count == 0:
                args.append(scan(expression[start:head+1]))
                start = head+1
            head += 1
            continue
        if count == 0:
            if expression[head] != ' ':
                t = next_token(expression[head:])
                if t == 'x':
                    args.append(Variable(value='x'))
                else:
                    args.append(Const(value=int(t)))
                head += len(t)+1
                continue
        head += 1
    if len(args) == 2:
        return build_simplified(operation=oper, lhs=args[0], rhs=args[1])
    if len(args) == 1:
        return Func(name=oper, arg=args[0])
    if len(args) == 0:
        if oper == 'x':
            return Variable(value='x')
        return Const(value=int(oper))

# ------------------------------
# Define diff as the sequence of parse -> differentiate -> Turn the tree into a string

def diff(expression):
    if '(' not in expression:
        expression = f"({expression})"
    return pretty(deriv(scan(expression)))
  
______________________________________________
import re

def diff(s):
    return serialize(dif(deserialize(s)))

def deserialize(s):
    s = s.replace("(", " [ ").replace(")", " ], ")
    s = "".join(w if w == "[" or w == "],"
                else f"float({w})," if re.match("^-?[0-9]+$", w)
                else f'"{w}",'
                for w in s.split())
    s = s[:-1]  # remove the last comma
    return eval(s)

def serialize(expr):
    if isinstance(expr, str):
        return expr
    elif isinstance(expr, float):
        return f"{expr:g}"
    elif isinstance(expr, list):
        return "(" + " ".join(serialize(x) for x in expr) + ")"

def dif(expr):
    if isinstance(expr, str):
        return 1.
    elif isinstance(expr, float):
        return 0.
    else:
        op = expr[0]
        a = expr[1]
        b = expr[2] if len(expr) == 3 else None
        
        if op == "+":
            return calc(["+", dif(a), dif(b)])  # a' + b'
        elif op == "-":
            return calc(["-", dif(a), dif(b)])  # a' - b'
        elif op == "*":
            return calc(["+", ["*", dif(a), b], ["*", a, dif(b)]])  # a'*b + a*b'
        elif op == "/":
            return calc(["/", ["-", ["*", dif(a), b], ["*", a, dif(b)]], ["^", b, 2.]])  # (a'*b - a*b') / (b^2)
        elif op == "^":
            return calc(["*", b, ["^", a, ["-", b, 1.]]])  # b * a^(b-1)
        elif op == "sin":
            return calc(dif_chain(a, ["cos", a]))  # cos(a)
        elif op == "cos":
            return calc(dif_chain(a, ["*", -1., ["sin", a]]))  # -sin(a)
        elif op == "tan":
            return calc(dif_chain(a, ["^", ["cos", a], -2.]))  # cos(a)^(-2)
        elif op == "exp":
            return calc(dif_chain(a, ["exp", a]))  # exp(a)
        elif op == "ln":
            return calc(dif_chain(a, ["/", 1., a]))  # 1/a

def dif_chain(a, b):
    return calc(["*", dif(a), b])

def calc(expr):
    if isinstance(expr, str) or isinstance(expr, float):
        return expr
    
    op = expr[0]
    a = calc(expr[1])
    b = calc(expr[2]) if len(expr) == 3 else None
    
    if op == "+":
        if isinstance(a, float) and isinstance(b, float):
            return a + b
        elif a == 0:
            return b
        elif b == 0:
            return a
        else:
            return ["+", a, b]
    elif op == "-":
        if isinstance(a, float) and isinstance(b, float):
            return a - b
        elif b == 0:
            return a
        else:
            return ["-", a, b]
    elif op == "*":
        if isinstance(a, float) and isinstance(b, float):
            return a * b
        elif a == 0 or b == 0:
            return 0.
        elif a == 1:
            return b
        elif b == 1:
            return a
        else:
            return ["*", a, b]
    elif op == "/":
        if isinstance(a, float) and isinstance(b, float):
            return a / b
        elif a == 0:
            return 0.
        elif b == 1:
            return a
        else:
            return ["/", a, b]
    elif op == "^":
        if isinstance(a, float) and isinstance(b, float):
            return a**b
        elif a == 0:
            return 1.
        elif b == 1:
            return a
        else:
            return ["^", a, b]
    else:
        return [op, a]
