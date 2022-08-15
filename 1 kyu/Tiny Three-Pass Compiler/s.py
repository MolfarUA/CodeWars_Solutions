5265b0885fda8eac5900093b



import re
import itertools


class Compiler(object):

    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))

    def tokenize(self, program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    def parse_var(self, toks):
        if re.match('[a-zA-Z]+', toks[0]):
            return ('var', toks[0]), toks[1:]
        else:
            raise

    def parse_factor(self, toks):
        if type(toks[0]) == type(0):
            num, r = self.parse_num(toks)
            return ('factor', num), r
        elif re.match("[a-zA-Z]", toks[0]):
            var, r = self.parse_var(toks)
            return ('factor', var), r
        elif toks[0] == '(':
            exp, r = self.parse_exp(toks[1:])
            return ('factor', exp), r[1:]
        else:
            raise

    def parse_num(self, toks):
        if type(toks[0]) == type(0):
            return ('num', toks[0]), toks[1:]
        else:
            raise

    def parse_term(self, toks):
        term, r = self.parse_multi_with_delim(self.parse_factor,
                                              toks,
                                              re_delim=r"[*]|[/]",
                                              in_result=True)
        return ('term', self.left_combine(term, "term")), r


    def parse_exp(self, toks):
        exp, r = self.parse_multi_with_delim(self.parse_term,
                                             toks,
                                             re_delim=r"[+]|-",
                                             in_result=True)
        return ('exp', self.left_combine(exp, "exp")), r

    def left_combine(self, lst, name):
        if len(lst) == 1:
            return lst[0]
        elif len(lst) == 3:
            first, op, final = lst
            return (op, first, final)
        else:
            left = self.left_combine(lst[:-2], name)
            op = lst[-2]
            final = lst[-1]
            return (op, (name, left), final)

    def parse_function(self, toks):
        var_list, r = self.parse_multi_with_delim(self.parse_var, toks[1:])
        env = dict(zip([v for _, v in var_list],
                       range(0, len(var_list))))
        exp, r1 = self.parse_exp(r[1:])
        assert r1 == []
        return ('function', env, exp)

    def parse_multi_with_delim(self, pf, toks, re_delim=None, in_result=False):
        if not toks:
            return [], []
        result = []
        curr = toks
        while True:
            try:
                e, r = pf(curr)
            except:
                return result, curr
            result.append(e)
            curr = r
            if not curr:
                return (result, [])
            if re_delim is None:
                curr = r
            else:
                if re.match(re_delim, r[0]):
                    if in_result:
                        result.append(r[0])
                        curr = r[1:]
                    else:
                        curr = r[1:]
                else:
                    return result, curr

    def gen_json_ast(self, ast):
        if ast[0] == 'exp':
            return self.gen_json_ast_exp(ast)
        if ast[0] == 'term':
            return self.gen_json_ast_term(ast)
        if ast[0] == 'factor':
            return self.gen_json_ast_factor(ast)

    def gen_json_ast_exp(self, nast):
        name, ast = nast
        if type(ast) == type(()) and ast[0] == 'term':
            return self.gen_json_ast_term(ast)
        if type(ast) == type(()) and ast[0] in ["+", "-"]:
            return {
                "op": ast[0],
                "a": self.gen_json_ast(ast[1]),
                "b": self.gen_json_ast(ast[2])
            }

    def gen_json_ast_term(self, nast):
        name, ast = nast
        if type(ast) == type(()) and ast[0] == 'factor':
            return self.gen_json_ast_factor(ast)
        if type(ast) == type(()) and ast[0] in ["*", "/"]:
            return {
                "op": ast[0],
                "a": self.gen_json_ast(ast[1]),
                "b": self.gen_json_ast(ast[2])
            }

    def gen_json_ast_factor(self, nast):
        name, ast = nast
        if type(ast) == type(()) and ast[0] == 'num':
            return {"op": "imm", "n": ast[1]}
        if type(ast) == type(()) and ast[0] == 'var':
            return {"op": "arg", "n": self.env[ast[1]]}
        return self.gen_json_ast(ast)

    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program)
        func = self.parse_function(tokens)
        (name, env, exp) = func
        self.env = env
        jexp = self.gen_json_ast(exp)
        return jexp

    def is_imm(self, ast):
        return ast["op"] == "imm"

    def calc_imm(self, ast1, ast2, op):
        return {
            "op": "imm",
            "n": self.op_calc(op, ast1["n"], ast2["n"])
        }

    def op_calc(self, op, n1, n2):
        if op == "+": return n1 + n2
        if op == "*": return n1 * n2
        if op == "-": return n1 - n2
        if op == "/": return n1 / n2

    def is_zero(self, ast):
        return ast["op"] == "imm" and ast["n"] == 0

    def is_one(self, ast):
        return ast["op"] == "imm" and ast["n"] == 1

    def reduce(self, ast):
        if ast["op"] in ["+", "-", "*", "/"]:
            a = self.reduce(ast["a"])
            b = self.reduce(ast["b"])
            if self.is_imm(a) and self.is_imm(b):
                return self.calc_imm(a, b, ast["op"])
            if ast["op"] == "+":
                if self.is_zero(a): return b
                if self.is_zero(b): return a
            if ast["op"] == "-":
                if self.is_zero(b): return a
            if ast["op"] == "*":
                if self.is_zero(a) or self.is_zero(b): return {"op": "imm", "n": 0}
                if self.is_one(a): return b
                if self.is_one(b): return a
            if ast["op"] == "/":
                if self.is_zero(a): return {"op": "imm", "n": 0}
                if self.is_one(b): return a
            return {"op": ast["op"], "a": a, "b": b}
        return ast

    def pass2(self, ast):
        return self.reduce(ast)

    def pass3(self, ast):
        return self.code_gen(ast)

    def get_inst(self, op):
        INST = {
            "+": "AD",
            "-": "SU",
            "*": "MU",
            "/": "DI",
        }
        return [INST[op]]

    def save_r1(self):
        return [
            "SW",
            "PU",
            "SW"
        ]

    def restore_r1(self):
        return [
            "SW",
            "PO",
            "SW"
        ]

    def code_gen(self, ast):
        if ast["op"] in ["+", "-", "*", "/"]:
            a, b = ast["a"], ast["b"]
            insts_a = self.code_gen(a)
            swi_inst1 = ["SW"]
            insts_b = self.code_gen(b)
            swi_inst2 = ["SW"]
            insts = itertools.chain(self.save_r1(),
                                    insts_a,
                                    swi_inst1,
                                    insts_b,
                                    swi_inst2,
                                    self.get_inst(ast["op"]),
                                    self.restore_r1())
            return list(insts)

        if ast["op"] == "imm":
            return ["IM {n}".format(n=ast["n"])]
        if ast["op"] == "arg":
            return ["AR {n}".format(n=ast["n"])]
          
#################
import re

class Compiler(object):
  def __init__(self):
    self.operator = {
      "+": lambda a, b: a + b,
      "-": lambda a, b: a - b,
      "*": lambda a, b: a * b,
      "/": lambda a, b: a / b,
    }
    self.op_name = {
      "+": "AD",
      "-": "SU",
      "*": "MU",
      "/": "DI",
    }
    
  def compile(self, program):
    return self.pass3(self.pass2(self.pass1(program)))
        
  def tokenize(self, program):
    """Turn a program string into an array of tokens.  Each token
       is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
       name or a number (as a string)"""
    token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
    #return [int(tok) if tok.isdigit() else tok for tok in token_iter]
    return token_iter

  def pass1(self, program):
    """Returns an un-optimized AST"""
    tokens = self.tokenize(program)
    arg_mode = False
    args = {}
    index = 0
    ast = {}
    precedence = {
      '+': 1,
      '-': 1,
      '*': 2,
      '/': 2,
      '(': 0,
    }
    operands = []
    operators = []

    for token in tokens:
      if token in '[]':
        arg_mode = not arg_mode
      elif arg_mode:
        args[token] = index
        index += 1
      else:
        if token in args:
          operands.append( {'op': 'arg', 'n': args[token]} )
        elif token.isdigit():
          operands.append( {'op': 'imm', 'n': int(token)} )
        else:
          if token == '(':
            operators.append(token)
          elif token == ')':
            op = operators.pop()
            while op != '(':
              b, a = operands.pop(), operands.pop()
              operands.append({'op':op, 'a': a, 'b': b})
              op = operators.pop()
          if token in '+-*/':
            while len(operators) > 0 and precedence[ operators[-1] ] >= precedence[token]:
              op = operators.pop()
              b, a = operands.pop(), operands.pop()
              operands.append({'op': op, 'a': a, 'b': b})
            operators.append(token)
            
    while len(operators) > 0:
      op = operators.pop()
      b, a = operands.pop(), operands.pop()
      operands.append({'op': op, 'a': a, 'b': b})
    return operands[0]

  def pass2(self, ast):
    """Returns an AST with constant expressions reduced"""
    if ast['op'] in ('arg', 'imm'):
      return ast
      
    a = self.pass2(ast['a'])
    b = self.pass2(ast['b'])
    if a['op'] == 'imm' and b['op'] == 'imm':
      return {'op': 'imm', 'n': self.operator[ast['op']](a['n'], b['n'])}
    return {'op': ast['op'], 'a': a, 'b': b}

  def pass3(self, ast):
    """Returns assembly instructions"""
    if ast['op'] == 'imm':
      return ['IM %d' % ast['n']]
    if ast['op'] == 'arg':
      return ['AR %d' % ast['n']]
      
    b = self.pass3(ast['b'])
    a = self.pass3(ast['a'])
    if len(a) == 1:
      return b + ['SW'] + a + [ self.op_name[ ast['op'] ] ]
    else:
      return a + ['PU'] + b + ['SW', 'PO'] + [ self.op_name[ ast['op'] ] ]
    
    
####################
import re

class Compiler(object):
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    def pass1(self, program):
        tokens = self.tokenize(program)
        sep = tokens.index(']')
        params, tokens = tokens[1:sep], tokens[sep + 1:]
        prec = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0}
        ops, terms = [], []
        operate = lambda: {'op': ops.pop(), 'b': terms.pop(), 'a': terms.pop()}
        for tok in tokens:
            if isinstance(tok, int):
                terms.append({'op': 'imm', 'n': tok})
            elif tok == '(':
                ops.append(tok)
            elif tok in '+-*/':
                while ops and prec[ops[-1]] >= prec[tok]:
                    terms.append(operate())
                ops.append(tok)
            elif tok == ')':
                while ops[-1] != '(':
                    terms.append(operate())
                ops.pop()
            else:
                terms.append({'op': 'arg', 'n': params.index(tok)})
        while ops:
            terms.append(operate())
        return terms[0]
        
    def pass2(self, ast):
        if ast['op'] in {'arg', 'imm'}:
            return ast
        ast['a'] = self.pass2(ast['a'])
        ast['b'] = self.pass2(ast['b'])
        if ast['a']['op'] == ast['b']['op'] == 'imm':
            return {'op': 'imm', 'n': {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a / b,
            }[ast['op']](ast['a']['n'], ast['b']['n'])}
        return ast

    def pass3(self, ast):
        if ast['op'] == 'imm':
            return ['IM {}'.format(ast['n'])]
        if ast['op'] == 'arg':
            return ['AR {}'.format(ast['n'])]
        a = self.pass3(ast['a'])
        b = self.pass3(ast['b'])
        op = {'+': 'AD', '-': 'SU', '*': 'MU', '/': 'DI'}[ast['op']]
        return a + ['PU'] + b + ['SW', 'PO', op]
      
#####################
import re
from copy import deepcopy

precedence = {'(': 1, '/': 4, '*': 4, '+': 3, '-': 3}
alp = 'abcdefghijklmnopqrstuvwxyz'
D = {'+': 'AD', '-': 'SU', '*': 'MU', '/': 'DI'}

class Compiler(object):
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    def pass1(self, program):
        tokens = self.tokenize(program)
        args = [tokens.pop(0) for i in range(tokens.index(']') + 1)][1:-1]
        tokens, stack, expression = ['('] + tokens + [')'], [], []
        
        def transmission():
            b = self.apply(expression.pop(), args)
            a = self.apply(expression.pop(),args) 
            
            expression.append({'a': a, 'b': b, 'op': stack.pop()})

        for token in tokens:
            if token == '(' : stack.append('(')
            elif token == ')':
                while stack[-1] != '(' : transmission()
                stack.pop()
            elif str(token) in '+-*/':
                while precedence[token] <= precedence[stack[-1]] : transmission()
                stack.append(token)
            else : expression.append(token)

        return expression[0]
    
    def apply(self, x, args):
        return {'n': x, 'op': 'imm'} if isinstance(x, int) else {'n': args.index(x), 'op': 'arg'} if x in args else x

    def pass2(self, ast: dict):
        cmp = deepcopy(ast)
        tree = self.recur(deepcopy(cmp))

        while tree != cmp:
            cmp = deepcopy(tree)
            tree = self.recur(deepcopy(cmp))

        return cmp

    def recur(self, ast):
        if ast['op'] in 'arg imm'.split() : return ast
        a, b, op = ast.values()
        if a['op'] == 'imm' and b['op'] == 'imm' : return {'n': eval("a['n'] {} b['n']".format(op)), 'op': 'imm'}
        ast['a'] = self.recur(ast['a'])
        ast['b'] = self.recur(ast['b'])
        return ast

    def pass3(self, ast):
        exp = self.get_expression(ast)
        stack, chars, instructions = [], [], []

        for token in exp:
            if token in '(+-*/' :  stack.append(token)
            elif token == ')':
                while stack[-1] != '(':
                    _, _, op = chars.pop(), chars.pop(), stack.pop()
                    instructions.extend(['PO','SW','PO',D[op],'PU'])
                    chars.append('2')
                stack.pop()
            else:
                instructions.extend(['IM'+token if token.isdigit() else 'AR ' + str(alp.index(token)),'PU'])
                chars.append(token)
                
        return instructions
    
    def get_expression(self, ast):
        return alp[ast['n']] if ast['op'] == 'arg' else str(int(ast['n'])) if ast['op'] == 'imm' else '(' + self.get_expression(ast['a']) + ast['op'] + self.get_expression(ast['b']) + ')'
      
###############
import re
import operator

class Compiler(object):

    def __init__(self):
        self.code = []
        self.args = dict()
    
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
        
    def tokenize(self, program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]


    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program)
        ind1 = tokens.index(']')
        args = tokens[1: ind1]
        self.args = {x: i for i, x in enumerate(args)}
        
        tokens = tokens[ind1+1:]
        return _calc(self._to_postfix(tokens))
            
        
    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""
        dfs(ast, None)
        return ast


    def pass3(self, ast):
        """Returns assembly instructions"""
        ast1 = {'a':ast}
        self.dfs2(ast, ast1)
        self.clearup()
        #pprint(self.code)
        pass
        return self.code


    def _to_postfix(self, tokens):
        stack = []
        res = []
        for token in tokens:
            # constant
            if isinstance(token, int):
                res.append({'op':'imm', 'n':token})
                continue
            
            if token in '+-/*':
                while len(stack) > 0:
                    top = stack.pop()
                    if top == '(':
                        stack.append('(')
                        break
                    if _priority(token) > _priority(top):
                        stack.append(top)
                        break
                    res.append(top)
                stack.append(token)
                continue
        
            if token == '(':
                stack.append(token)
                continue
                
            if token == ')':
                while True:
                    top = stack.pop()
                    if top == '(':
                        break
                    res.append(top)
                continue

            # argument
            res.append({'op':'arg', 'n':self.args[token]})
            
        while len(stack) > 0:
            res.append(stack.pop())
               
        return res

    
    def appendCommandOnList(self, node):
        if node['op'] == 'st':
            command = 'PO'
        else:
            command = '{} {}'.format('IM' if node['op'] == 'imm' else 'AR',
                                     node['n']
                                     )
        self.code.append(command)


    def operation(self, op):
        return ('AD' if op == '+' else
                'SU' if op == '-' else
                'MU' if op == '*' else
                'DI' if op == '/' else
                '!@#$%')

    
    def dfs2(self, node, anc):
        if node['op'] in ['imm', 'arg', 'sta']:
            return True
        if self.dfs2(node['a'], node) & self.dfs2(node['b'], node):
            self.appendCommandOnList(node['b'])
            self.code.append('SW')
            self.appendCommandOnList(node['a'])
            self.code.append(self.operation(node['op']))
            self.code.append('PU')
            newNode = {'op':'st'}
            anc['a' if anc['a'] == node else 'b'] = newNode
            return True
        return False

    def clearup(self):
        clearedCode = []
        i = 0
        while i < len(self.code) - 1:
            if self.code[i] == 'PU' and self.code[i + 1] == 'PO':
                i += 2
            else:
                clearedCode.append(self.code[i])
                i += 1
        self.code = clearedCode
        
        
def _priority(c):
    return 1 if c in '+-' else 2
        




def _calc(postfix):
    stack = []
    for c in postfix:
        if not isinstance(c, str):
            stack.append(c)
        else:
            b = stack.pop()
            a = stack.pop()
            stack.append({'a':a, 'b':b, 'op':c})
    return stack.pop()


operations = {'-': operator.sub,
              '+': operator.add,
              '*': operator.mul,
              '/': operator.floordiv
              }

def dfs(node, anc):
    if node['op'] == 'imm':
        return True
    if node['op'] == 'arg':
        return False
    
    if dfs(node['a'], node) & dfs(node['b'], node):
        aval, bval = node['a']['n'], node['b']['n']
        val = operations[node['op']](aval, bval)
        newNode = {'op':'imm', 'n':val}
        #pprint(newNode)
        anc['a' if anc['a'] == node else 'b'] = newNode
        return True
    return False
  
###################
import re

class TokenStream(object):
    tokenizer = re.compile(r'[-+*/()[\]]|[A-Za-z]+|\d+').finditer
    def __init__(self, program):
        self.tokens = (m.group(0) for m in self.tokenizer(program))
        self.buffer = []
    def accept(self, sym):
        if not self.buffer:
            self.buffer.append(next(self.tokens))
        return re.match(sym, self.buffer[-1]) and self.buffer.pop()

class Compiler(object):

    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))

    def pass1(self, program):
        accept = TokenStream(program).accept
        args = {}

        def expression():
            e = term()
            for op in iter(lambda:accept('[-+]'), None):
                e = {'op': op, 'a': e, 'b': term()}
            return e
        def term():
            t = factor()
            for op in iter(lambda:accept('[*/]'), None):
                t = {'op': op, 'a': t, 'b': factor()}
            return t
        def factor():
            if accept(r'\('):
                e = expression()
                accept(r'\)')
                return e
            return number() or variable()
        def number():
            n = accept(r'\d+')
            return n and {'op': 'imm', 'n': int(n)}
        def variable():
            v = accept('[a-z]+')
            return v and {'op': 'arg', 'n': args[v]}
        
        accept(r'\[')
        for i, var in enumerate(iter(lambda:accept('[a-z]+'), None)):
            args[var] = i
        accept(']')
        return expression()
    
    def _eval(self, a, op, b):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/': return a / b
    
    def pass2(self, ast):
        if 'n' in ast:
            return ast
        a, b = self.pass2(ast['a']), self.pass2(ast['b'])
        if a['op'] == 'imm' and b['op'] == 'imm':
            return {'op': 'imm', 'n': self._eval(a['n'], ast['op'], b['n']) }
        return {'op': ast['op'], 'a': a, 'b': b };

    def pass3(self, ast):
        if ast['op'] == 'imm':
            return [ 'IM {}'.format(ast['n']) ]
        elif ast['op'] == 'arg':
            return [ 'AR {}'.format(ast['n']) ]
        op = [ 'SU', 'DI', 'MU', 'AD' ]['-/*+'.index(ast['op'])]
        return self.pass3(ast['a']) + ['PU'] + self.pass3(ast['b']) + ['SW', 'PO', op]
      
###################
import re
class Compiler(object):
    compile = lambda self, program: self.pass3(self.pass2(self.pass1(program)))
    tokenize = lambda self, program: [int(tok) if tok.isdigit() else tok for tok in (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))]
    pass2 = lambda self, ast: ast if ast['op'] in {'arg', 'imm'} else {'op': 'imm', 'n': {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y, '/': lambda x, y: x / y}[ast['op']](self.pass2(ast['a'])['n'], self.pass2(ast['b'])['n'])} if self.pass2(ast['a'])['op'] == self.pass2(ast['b'])['op'] == 'imm' else {'op': ast['op'], 'a': self.pass2(ast['a']), 'b': self.pass2(ast['b'])}
    pass3 = lambda self, ast: ['{} {}'.format(ast['op'].upper()[:2], ast['n'])] if ast['op'] in {'imm', 'arg'} else self.pass3(ast['a']) + ['PU'] + self.pass3(ast['b']) + ['SW', 'PO', {'+': 'AD', '-': 'SU', '*': 'MU', '/': 'DI'}[ast['op']]]
    def pass1(self, program):
        tokens = self.tokenize(program)
        params, tokens, ops, terms, prec, operate = tokens[1:tokens.index(']')], tokens[tokens.index(']') + 1:], [], [], {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0}, lambda: terms.append({'op': ops.pop(), 'b': terms.pop(), 'a': terms.pop()})
        for tok in tokens:
            while tok == ')' and ops[-1] != '(' or tok in set('+-*/') and ops and prec[ops[-1]] >= prec[tok]: operate()
            terms.append({'op': 'imm', 'n': tok}) if isinstance(tok, int) else ops.append(tok) if tok == '(' else ops.pop() if tok == ')' else ops.append(tok) if tok in '+-*/' else terms.append({'op': 'arg', 'n': params.index(tok)})
        while ops: operate()
        return terms[0]
      
####################
import re

class Compiler(object):
    def __init__(self):
        self.args = []
        self.tokens = []
        self.current_token = 0
        self.assembleLine = []

    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    def getNextToken(self):
        if len(self.tokens) > 0:
            return self.tokens.pop(0)
        else:
            return None

    def pass1(self, program):
        """Returns an un-optimized AST"""
        self.tokens = self.tokenize(program)
        self.args = []
        self.current_token = self.getNextToken()

        # Добавляем аргументы
        while True:
            self.current_token = self.getNextToken()
            if self.current_token == ']':
                self.current_token = self.getNextToken()
                break
            else:
                self.args.append(self.current_token)

        expression = self.expr()
        print(expression)
        return expression
        
    def factor(self):
        token = self.current_token
        if str(token).isdigit():
            self.current_token = self.getNextToken()
            return { 'op': 'imm', 'n': int(str(token)) }
        elif token in self.args:
            self.current_token = self.getNextToken()
            return { 'op': 'arg', 'n': self.args.index(token)}
        elif token == '(':
            self.current_token = self.getNextToken()
            node = self.expr()
            self.current_token = self.getNextToken()
            return node

    def term(self):
        node = self.factor()
        
        while self.current_token in ('*', '/'):
            token = self.current_token
            if token == '*':
                self.current_token = self.getNextToken()
            elif token == '/':
                self.current_token = self.getNextToken()

            node = { 'op': str(token), 'a': node, 'b': self.factor() }

        return node

    def expr(self):
        node = self.term()

        while self.current_token in ('+', '-'):
            token = self.current_token
            if token == '+':
                self.current_token = self.getNextToken()
            elif token == '-':
                self.current_token = self.getNextToken()

            node = { 'op': str(token), 'a': node, 'b': self.term() }

        return node

    def pass2(self, ast):
        expression = self.branchReducer(ast)
        print(expression)
        return expression
        
    def pass3(self, ast):
        self.assembleBranch(ast)
        print(self.assembleLine)
        return self.assembleLine

    def branchReducer(self, branch):
        if branch['op'] in ('*', '/', '+', '-'):
            if branch['a']['op'] == 'imm' and branch['b']['op'] == 'imm':
                if branch['op'] == '*':
                    return { 'op': 'imm', 'n': int(branch['a']['n']) * int(branch['b']['n'])}
                if branch['op'] == '/':
                    return { 'op': 'imm', 'n': int(branch['a']['n']) // int(branch['b']['n'])}
                if branch['op'] == '+':
                    return { 'op': 'imm', 'n': int(branch['a']['n']) + int(branch['b']['n'])}
                if branch['op'] == '-':
                    return { 'op': 'imm', 'n': int(branch['a']['n']) - int(branch['b']['n'])}
            else:
                branch['a'] = self.branchReducer(branch['a'])
                branch['b'] = self.branchReducer(branch['b'])

                if branch['op'] in '*/+-' and branch['a']['op'] == 'imm' and branch['b']['op'] == 'imm':
                    return self.branchReducer(branch)

                return branch
        else:
            return branch

    def assembleBranch(self, branch):
        if branch['op'] in ('*', '/', '+', '-'):
            b1 = self.assembleBranch(branch['a'])
            self.assembleLine.append("SW")
            b2 = self.assembleBranch(branch['b'])
            if self.assembleLine[-1] != 'PO':         
                self.assembleLine.append("SW")
            if branch['op'] == '*':
                self.assembleLine.append('MU')
            if branch['op'] == '/':
                self.assembleLine.append('DI')
            if branch['op'] == '+':
                self.assembleLine.append('AD')
            if branch['op'] == '-':
                self.assembleLine.append('SU')
            
            if len(self.assembleLine) >= 7 and self.assembleLine[-7] == 'PU':
                self.assembleLine.append('SW')
                self.assembleLine.append('PO')
            else:
                self.assembleLine.append('PU')
        else:
            self.assembleLine.append(branch['op'][:2].upper() + ' ' + str(branch['n']))
    
def simulate(asm, argv):
    r0, r1 = None, None
    stack = []
    for ins in asm:
        if ins[:2] == 'IM' or ins[:2] == 'AR':
            ins, n = ins[:2], int(ins[2:])
        if ins == 'IM':   r0 = n
        elif ins == 'AR': r0 = argv[n]
        elif ins == 'SW': r0, r1 = r1, r0
        elif ins == 'PU': stack.append(r0)
        elif ins == 'PO': r0 = stack.pop()
        elif ins == 'AD': r0 += r1
        elif ins == 'SU': r0 -= r1
        elif ins == 'MU': r0 *= r1
        elif ins == 'DI': r0 /= r1
    return r0
  
########################
import re
class Compiler(object):
    compile = lambda self, program: self.pass3(self.pass2(self.pass1(program)))
    tokenize = lambda self, program: [int(tok) if tok.isdigit() else tok for tok in (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))]
    pass2 = lambda self, ast: ast if ast['op'] in {'arg', 'imm'} else {'op': 'imm', 'n': {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y, '/': lambda x, y: x / y}[ast['op']](self.pass2(ast['a'])['n'], self.pass2(ast['b'])['n'])} if self.pass2(ast['a'])['op'] == self.pass2(ast['b'])['op'] == 'imm' else {'op': ast['op'], 'a': self.pass2(ast['a']), 'b': self.pass2(ast['b'])}
    pass3 = lambda self, ast: ['{} {}'.format(ast['op'].upper()[:2], ast['n'])] if ast['op'] in {'imm', 'arg'} else self.pass3(ast['a']) + ['PU'] + self.pass3(ast['b']) + ['SW', 'PO', {'+': 'AD', '-': 'SU', '*': 'MU', '/': 'DI'}[ast['op']]]
    def pass1(self, program):
        tokens = self.tokenize(program)
        params, tokens, ops, terms, prec, operate = tokens[1:tokens.index(']')], tokens[tokens.index(']') + 1:], [], [], {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0}, lambda: terms.append({'op': ops.pop(), 'b': terms.pop(), 'a': terms.pop()})
        for tok in tokens:
            while tok == ')' and ops[-1] != '(' or tok in set('+-*/') and ops and prec[ops[-1]] >= prec[tok]: operate()
            [terms.append({'op': 'imm', 'n': tok}) if isinstance(tok, int) else ops.append(tok) if tok == '(' else ops.pop() if tok == ')' else ops.append(tok) if tok in '+-*/' else terms.append({'op': 'arg', 'n': params.index(tok)}) for tok in [tok]]
        while ops: operate()
        return terms[0]
      
######################
import re
opTrans = {"+":"AD", "-":"SU", "*":"MU", "/":"DI"}

class Compiler(object):
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]
    
    def getBracketEnd(self, tokens):
        level = idx = 1
        while level:
            if tokens[idx] == "(": level += 1
            elif tokens[idx] == ")": level -= 1
            idx += 1
        return idx - 1
        
    def getMasterOperator(self, tokens):
        bracketLevel = idx = strongPos = weakPos = 0
        while idx < len(tokens):
            token = tokens[idx]
            if token == "(":
                idx += self.getBracketEnd(tokens[idx + 1:])
            elif token == "-" or token == "+":
                strongPos = idx
            elif token == "*" or token == "/":
                weakPos = idx
            idx += 1
        return strongPos if strongPos else weakPos
        
    def getExpr(self, tokens, args):
        while tokens[0] == "(" and self.getBracketEnd(tokens[1:]) == len(tokens) - 2:
            tokens = tokens[1:-1]
        if len(tokens) == 1:
            return {"op":"imm", "n":tokens[0]} if isinstance(tokens[0], int) else {"op":"arg", "n":args.index(tokens[0])}
        
        expr = {"op":"?", "a":"?", "b":"?"}
        masterOpPos = self.getMasterOperator(tokens)
        expr["op"] = tokens[masterOpPos]
        expr["a"] = self.getExpr(tokens[:masterOpPos], args)
        expr["b"] = self.getExpr(tokens[masterOpPos + 1:], args)
        return expr

    def pass1(self, program):
        tokens = self.tokenize(program)
        return self.getExpr(tokens[tokens.index("]") + 1:], tokens[1:tokens.index("]")] if "[" in tokens else [])
        
    def pass2(self, ast):
        if ast["op"] in ["imm", "arg"]:
            return ast
        
        ast["a"] = self.pass2(ast["a"])
        ast["b"] = self.pass2(ast["b"])
        
        if ast["a"]["op"] == "imm" and ast["b"]["op"] == "imm":
            a, b, op = ast["a"]["n"], ast["b"]["n"], ast["op"]
            if op == "+": return {"op":"imm", "n":a + b}
            elif op == "-": return {"op":"imm", "n":a - b}
            elif op == "*": return {"op":"imm", "n":a * b}
            elif op == "/": return {"op":"imm", "n":a / b}
        
        return ast
   
    def pass3(self, ast):
        if ast["op"] == "imm":
            return [f"IM {ast['n']}"]
        elif ast["op"] == "arg":
            return [f"AR {ast['n']}"]
        else:
            return self.pass3(ast["a"]) + ["PU"] + self.pass3(ast["b"]) + ["SW", "PO"] + [opTrans[ast["op"]]]
          
#################
import re

debug = False

def dprint(*var_args):
    if debug: print(" ".join([str(a) for a in var_args]))

# Top-down parser with some tricks to make left-hand recursion work.
# Basically, we converted the grammar to something.. horrendous?

# Our rules went from looking like this:
#   expression ::= expression '+' term
# To something like this
#   expression ::= term | term '+' term | term '-' term | term '+' term '+' term | term '-' term '-' term etc.

# So we calculate everything on the same level, for lack of better words,
# and then we organize it all into a right-to-left tree of operations
class Parser():
    
    # Return the token if there is one, or None if there is not one
    def getToken(self,ll=0):
        return self.tokens[self.currentToken + (ll)] if (self.currentToken + (ll)) < len(self.tokens) else None
    
    def consumeToken(self):
        self.currentToken += 1
        dprint(("  "*(self.debug_currentLevel))+str(self.getToken(ll=-1)),"->",self.getToken())
    
    def buildRTLTree(self,terms,operators):
        if len(operators) == 0:
            return terms[0]
        
        op = operators.pop(len(operators)-1)
        rightTerm = terms.pop(len(terms)-1)
        leftTerm = self.buildRTLTree(terms,operators)
        return {
            "op": op,
            "a": leftTerm,
            "b": rightTerm,
        }
    
    def factor(self,variables):
        dprint(("  "*(self.debug_currentLevel))+"Factor (",self.debug_currentLevel,")")
        self.debug_currentLevel += 1
        
        if self.getToken() == "(":
            self.consumeToken()
            exp = self.expression(variables)
            self.debug_currentLevel -= 1
            return exp
        else:
            v = self.getToken()
            self.consumeToken()
            self.debug_currentLevel -= 1
            return {
                "op": "arg" if isinstance(v,str) else "imm",
                "n": variables[v] if isinstance(v,str) else v
            }
    
    def term(self,variables):
        dprint(("  "*(self.debug_currentLevel))+"Term (",self.debug_currentLevel,")")
        self.debug_currentLevel += 1
        
        # Collect as many factors and operators as we can
        # stop collecting once we reach + - ) or EOF
        factors = []
        operators = []
        i = 0
        while self.getToken() != "+" and self.getToken() != "-" and self.getToken() != ")" and self.getToken() != None:
            if i > 0:
                operators.append(self.getToken())
                self.consumeToken()
            factors.append(self.factor(variables))
            
            i += 1
            
        #if self.getToken() == ")":
        #    self.consumeToken()
        
        self.debug_currentLevel -= 1
        
        # If we only have one term, then return the term
        if len(factors) == 1:
            return factors[0]
        # Otherwise, build the term trees right to left
        return self.buildRTLTree(factors,operators)
    
    def expression(self,variables):
        dprint(("  "*(self.debug_currentLevel))+"Expression (",self.debug_currentLevel,")")
        self.debug_currentLevel += 1
        
        # Collect as many terms and operators as we can
        # stop collecting once we reach EOF or )
        terms = []
        operators = []
        i = 0
        while self.getToken() != None and self.getToken() != ")":
            if i > 0:
                operators.append(self.getToken())
                self.consumeToken()
            terms.append(self.term(variables))
            
            i += 1
            
        if self.getToken() == ")":
            self.consumeToken()
        
        self.debug_currentLevel -= 1
        
        # If we only have one term, then return the term
        if len(terms) == 1:
            return terms[0]
        # Otherwise, build the term trees right to left
        return self.buildRTLTree(terms,operators)
    
    # Consume the arg list tokens and return a dictionary of
    # variables (strings) to integer identifiers
    def arg_list(self):
        variables = {}
        while self.getToken() != "]":
            variables[self.getToken()] = len(variables)
            self.consumeToken()
        # End of arg list
        # Consume the ]
        self.consumeToken()
        return variables
    
    def function(self):
        # Beginning is always a [
        self.consumeToken()
        
        variables = self.arg_list()
        return self.expression(variables)
    
    def getASTFromTokens(self,tokens):
        self.tokens = tokens
        self.currentToken = 0
        self.debug_currentLevel = 0
        
        # Every program will start with a function definition
        return self.function()


class Optimizer():
    
    def getOptimizedBranch(self,branch):
        # If this is an immediate or an argument, exit: no optimization needed
        if branch["op"] == "imm" or branch["op"] == "arg":
            return branch
        
        # Attempt to optimize both branches
        branch["a"] = self.getOptimizedBranch(branch["a"])
        branch["b"] = self.getOptimizedBranch(branch["b"])
        
        # If both children are immediates, then return a single
        # immediate as the replacement branch.
        if branch["a"]["op"] == "imm" and branch["b"]["op"] == "imm":
            v = 0
            if branch["op"] == "+":
                v = branch["a"]["n"] + branch["b"]["n"]
            elif branch["op"] == "-":
                v = branch["a"]["n"] - branch["b"]["n"]
            elif branch["op"] == "*":
                v = branch["a"]["n"] * branch["b"]["n"]
            elif branch["op"] == "/":
                v = branch["a"]["n"] / branch["b"]["n"]
                
            return {
                "op": "imm",
                "n": v
            }
        else:
            return branch
    
class Assembler():

    def imm(self,branch):
        # Push the immediate onto the stack
        self.asm.append("IM "+str(branch["n"]))
        self.asm.append("PU")
        
    def arg(self,branch):
        # Push the argument onto the stack
        self.asm.append("AR "+str(branch["n"]))
        self.asm.append("PU")
        
    def binaryOperation(self,branch):
        # Calculate A and B assembly so they're on the stack
        self.getAssemblyFromBranch(branch["a"])
        self.getAssemblyFromBranch(branch["b"])
        
        # Calculate the result
        self.asm.append("PO") # r0 = b
        self.asm.append("SW") # r1 = r0
        self.asm.append("PO") # r0 = a
        
        if branch["op"] == "+":
            self.asm.append("AD")
        elif branch["op"] == "-":
            self.asm.append("SU")
        elif branch["op"] == "*":
            self.asm.append("MU")
        elif branch["op"] == "/":
            self.asm.append("DI")
        
        # Push the result
        self.asm.append("PU")
        
    def getAssemblyFromBranch(self,branch):
        if branch["op"] == "imm":
            self.imm(branch)
        elif branch["op"] == "arg":
            self.arg(branch)
        else:
            self.binaryOperation(branch)
            
    def getAssemblyFromAST(self,ast):
        self.asm = []
        self.getAssemblyFromBranch(ast)
        return self.asm
    
class Compiler(object):
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program)
        
        parser = Parser()
        ast = parser.getASTFromTokens(tokens)
        
        print(ast)
        return ast
        
    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""
        
        optimizer = Optimizer()
        optimized_ast = optimizer.getOptimizedBranch(ast)
        
        print(optimized_ast)
        return optimized_ast

    def pass3(self, ast):
        """Returns assembly instructions"""
        
        assembler = Assembler()
        asm = assembler.getAssemblyFromAST(ast)
        
        print(asm)
        return asm
      
######################
import operator
import re

OPTIMIZATIONS = (
    (r'PU;PO;', r''), # Push then Pop -> NOP
    (r'PU;((AR \d*)|(IM) \d*);SW;PO;', r'SW;\1;SW;'), # Push, Immediate, Swap, Pop ->  Swap, Immediate, Swap
    (r'((AR \d*)|(IM) \d*);SW;((AR \d*)|(IM) \d*);SW;', r'\4;SW;\1;'), # Imm A, Swap, Imm B, Swap -> Imm B, Swap, Imm A
    (r'SW;((AD)|(MU));', r'\1;') # Swap, Add/Mul -> Add/Mul
)

class Compiler(object):
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]
    
    def _expect(self, inp, exp):
        tok, rem = (inp[:1], inp[1:])
        return (True, rem) if (tok == [exp]) else (False, inp)
    
    def _parse_factor(self, inp, args):
        if len(inp) < 1:
            return (None, inp)

        fac, rem = (inp[0], inp[1:])
        
        if isinstance(fac, int):
            return ({ 'op': 'imm', 'n': fac }, rem)

        if fac in args:
            return ({ 'op': 'arg', 'n': args[fac] }, rem)
        
        if fac == '(':
            exp, rem = self._parse_expression(rem, args)
            
            if exp is None:
                return (None, inp)
            
            ok, rem = self._expect(rem, ')')
            
            if ok:
                return (exp, rem)

        return (None, inp)
            
    def _parse_term(self, inp, args):
        term = None
        op = None

        rem = inp
        
        while True:
            fac, nrem = self._parse_factor(rem, args)
        
            if fac is None:
                return (term, rem)
            
            rem = nrem
            
            term = fac if (term is None) else { 'op': op[0], 'a': term, 'b': fac }
        
            op, nrem = (rem[:1], rem[1:])
        
            if (len(op) != 1) or (op[0] not in ('*', '/')):
                return (term, rem)
            
            rem = nrem
    
    def _parse_expression(self, inp, args):
        exp = None
        op = None

        rem = inp
        
        while True:
            term, nrem = self._parse_term(rem, args)
        
            if term is None:
                return (exp, rem)
            
            rem = nrem
            
            exp = term if (exp is None) else { 'op': op[0], 'a': exp, 'b': term }
        
            op, nrem = (rem[:1], rem[1:])
        
            if (len(op) != 1) or (op[0] not in ('+', '-')):
                return (exp, rem)
            
            rem = nrem
    
    def _parse_arglist(self, inp):
        args = list()
        rem = inp
        
        while len(rem) != 0:
            arg, nrem = (rem[:1], rem[1:])
            
            if (len(arg) == 1) and arg[0].isalpha():
                args.append(arg[0])
            else:
                return (args, rem)
            
            rem = nrem
    
    def _parse_function(self, inp):
        rem = inp
        
        (ok, rem) = self._expect(rem, '[')

        if not ok:
            return (None, inp)

        (args, rem) = self._parse_arglist(rem)
        (ok, rem) = self._expect(rem, ']')
        
        if not ok:
            return (None, inp)
        
        args = dict(
            (arg, idx)
            for (idx, arg)
            in enumerate(args)
        )
        
        exp, rem = self._parse_expression(rem, args)
        
        return (exp, rem)
        
    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program)
        
        (fn, rem) = self._parse_function(tokens)
        
        if (fn is None) or (rem != []):
            raise ValueError('Failed to parse program')
            
        return fn
    
    def _fold_const(self, x):
        OPS = {
            '+' : operator.add, '-' : operator.sub,
            '*' : operator.mul, '/' : operator.floordiv,
        }
        
        if x['op'] in OPS:
            a = self._fold_const(x['a'])
            b = self._fold_const(x['b'])
            
            if (a['op'] == 'imm') and (b['op'] == 'imm'):
                op = OPS[x['op']]
                return { 'op': 'imm', 'n': op(a['n'], b['n']) }
            
            else:
                return { 'op': x['op'], 'a': a, 'b': b}
        
        else:
            return x

    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""

        return self._fold_const(ast)

    def _assemble_op(self, op):
        cmd = op['op']

        UNARY = {'imm' : 'IM', 'arg': 'AR'}
        BINARY = {
            '+' : 'AD', '-' : 'SU',
            '*' : 'MU', '/' : 'DI'
        }

        if cmd in UNARY:
            return [
                UNARY[cmd] + ' ' + str(op['n']), # Load Value
                'PU'                             # Push it onto the Stack
            ]

        elif cmd in BINARY:
            return [
                *self._assemble_op(op['a']), # Compute value A
                *self._assemble_op(op['b']), # Compute value B 
                'PO',                        # Pop Value B from the Stack
                'SW',                        # Store it in R1
                'PO',                        # Pop Value A from the Stack
                BINARY[cmd],                 # Execute cmd A B
                'PU'                         # Push result to the Stack
            ]

        else:
            raise ValueError(f'Unkown cmd {cmd}')

    def _optimize(self, prog):
        """Perform some optimizations on the assembly using regular expressions"""
        
        prog = ';'.join(prog) + ';'

        prev = prog
        while True:
            for pat, rep in OPTIMIZATIONS:
                prog = re.sub(pat, rep, prog)
                
            if not (len(prog) < len(prev)):
                # Stop when the program does not shrink anymore
                return prog.split(';')

            prev = prog

    def pass3(self, ast):
        """Returns assembly instructions"""

        prog = self._assemble_op(ast)
        prog += ['PO']
        prog = self._optimize(prog)

        return(prog)
      
########################
import re

class Compiler(object):
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))

    def tokenize(self, program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        return [m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program)]

    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program)
        i = 1  # `[`
        
        self.args = []
        while tokens[i] != ']':
            self.args.append(tokens[i])
            i += 1
        
        i += 1  # `]`
        
        ast, i = self.parse_expr(tokens, i)
        return ast

    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""
        op = ast['op']
        
        if op == 'imm' or op == 'arg':
            return ast
        
        left = self.pass2(ast['a'])
        right = self.pass2(ast['b'])
        
        if left['op'] == 'imm' and right['op'] == 'imm':
            a, b = left['n'], right['n']
            if op == '+':
                c = a + b
            elif op == '-':
                c = a - b
            elif op == '*':
                c = a * b
            else:
                c = a / b
            return {'op': 'imm', 'n': c}
        
        return {'op': op, 'a': left, 'b': right}
    
    def pass3(self, ast):
        """Returns assembly instructions"""
        op = ast['op']
        
        asm = []
        if op == 'imm':
            asm.append('IM %d' % ast['n'])
        elif op == 'arg':
            asm.append('AR %d' % ast['n'])
        else:
            asm_a = self.pass3(ast['a'])
            asm_b = self.pass3(ast['b'])
            
            # we can optimise which side is evaluated first
            # (fairly useless but I felt like it)
            a_simple = ast['a']['op'] in ('imm', 'arg')
            b_simple = ast['b']['op'] in ('imm', 'arg')
            
            # execute b first to eliminate a swap instruction
            if a_simple and b_simple:
                asm += asm_b
                asm.append('SW')
                asm += asm_a
            # the stack is needed for one side
            elif a_simple:
                asm += asm_b
                asm.append('SW')
                asm += asm_a
                asm.append('SW')
            elif b_simple:
                asm += asm_a
                asm.append('SW')
                asm += asm_b
                asm.append('SW')
            else:
                # the stack is needed  for both sides
                asm += asm_a
                asm.append('PU')
                asm += asm_b
                asm.append('SW')
                asm.append('PO')
            
            asm.append({
                '+': 'AD',
                '-': 'SU',
                '*': 'MU',
                '/': 'DI',
            }[op])
        
        return asm
    
    def parse_op(self, tokens, i, ops, inner_fn):
        lhs, i = inner_fn(tokens, i)
        
        while i < len(tokens) and tokens[i] in ops:
            op = tokens[i]
            i += 1
            
            rhs, i = inner_fn(tokens, i)
            lhs = {'op': op, 'a': lhs, 'b': rhs}
        
        return lhs, i
    
    def parse_expr(self, tokens, i):
        return self.parse_op(
            tokens, i, '+-',
            self.parse_term)
    
    def parse_term(self, tokens, i):
        return self.parse_op(
            tokens, i, '*/',
            self.parse_factor)
    
    def parse_factor(self, tokens, i):
        if tokens[i] == '(':
            i += 1
            expr, i = self.parse_expr(tokens, i)
            return expr, i + 1  # `)`
        
        if tokens[i].isnumeric():
            ast = {'op': 'imm', 'n': int(tokens[i])}
        else:
            var_i = self.args.index(tokens[i])
            ast = {'op': 'arg', 'n': var_i}
        
        return ast, i + 1
      
######################
import re

class Compiler(object):
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
    def __scan_neg__(self, tokens: list) -> int:
        for i in range(len(tokens)):
            x: str = tokens[i]
            if x == '-':
                if i == 0:
                    return i
                else:
                    j = i - 1
                    y = tokens[j]
                    if y in "*/+-(":
                        return i
        return None
    def __fix_neg__(self, tokens: list):
        while len(tokens) > 0:
            n = self.__scan_neg__(tokens)
            if n == None: break
            if n == 0:
                tokens.insert(n, '0')
            elif n >= len(tokens) - 1:
                raise ValueError("unexpected negative symbol at the end of the expression")
            else:
                if tokens[n+1][0] in "0123456789.":
                    tokens[n] += tokens[n+1]
                    del tokens[n+1]
                else:
                    j = n - 1
                    x = tokens[j]
                    if x in "*/":
                        tokens[n] = x
                        tokens[j] = "*"
                        tokens.insert(n, "-1")
                    else:
                        if x == tokens[n]:
                            tokens[j] = "+"
                            del tokens[n]
                        else:
                            del tokens[j]
        return tokens
    def tokenize(self, program: str) -> list:
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        tokens = [token for token in token_iter]
        tokens = self.__fix_neg__(tokens)
        return tokens
    def __priority__(self, operator_x: str, operator_y):
        if operator_x in "*/" and operator_y in "+-":
            return 1
        if operator_x in "+/" and operator_y in "*/":
            return -1
        if operator_x == "(":
            return 1
        return 0
    def __build_ast__(self, arglist: list, tokens: list) -> dict:
        operators = []; intermediates = []
        for i in range(len(tokens)):
            token = tokens[i]
            if token in "+-*/":
                while len(operators) > 0:
                    last = operators[-1]
                    if last == "(" or self.__priority__(token, last) > 0:
                        break
                    else:
                        last = operators.pop()
                        intermediates.append(last)
                operators.append(token)
            elif token in "()":
                if token == "(":
                    operators.append(token)
                else:
                    while len(operators) > 0:
                        last = operators.pop()
                        if last == "(": break
                        intermediates.append(last)
            else:
                intermediates.append(token)
        while len(operators) > 0:
            token = operators.pop()
            intermediates.append(token)
        rpn = intermediates
        ast = self.__convert_ast__(arglist, rpn)
        return ast
    def __convert_ast__(self, arglist, rpn: list) -> dict:
        operations = "+-*/"
        stack = []
        def pop():
            if len(stack) < 2:
                raise ValueError("insufficient operands")
            y = stack.pop(); x = stack.pop()
            return (x, y)
        def push(n):
            stack.append(n)
        while len(rpn) > 0:
            c = rpn.pop(0)
            if c in operations:
                left, right = pop()
                node = {"op": c, 'a': left, 'b': right}
                push(node)
            elif c in arglist:
                i = arglist.index(c)
                node = {"op": "arg", "n": i}
                push(node)
            else:
                if "." in c:
                    x = float(c)
                else:
                    x = int(c)
                node = {"op": "imm", "n": x}
                push(node)
        if len(stack) < 1:
            raise ValueError("insufficent output")
        return stack[0]
    def pass1(self, program: str) -> dict:
        """Returns an un-optimized AST"""
        tokens: list = self.tokenize(program)
        arglist: list = []
        for i in range(len(tokens)):
            x = tokens[i]
            if x == '[' or x == ' ': continue
            if x == ']':
                tokens = tokens[ i + 1 :]
                break
            arglist.append(x)
        return self.__build_ast__(arglist, tokens)

    def __simplify_ast__(self, ast: dict) -> dict:
        if 'a' in ast and 'b' in ast:
            a = ast["a"]; b = ast["b"]
            if isinstance(a, dict) and isinstance(b, dict):
                if a["op"] != "imm": a = self.__simplify_ast__(a)
                if b["op"] != "imm": b = self.__simplify_ast__(b)
                if a["op"] == "imm" and b["op"] == "imm":
                    a = a["n"]
                    b = b["n"]
                    o = ast["op"]
                    x = 0
                    if o == "*": x = a * b
                    elif o == "/": x = a / b
                    elif o == "+": x = a + b
                    elif o == "-": x = a - b
                    else: raise ValueError("unexpected operator %s" % o)
                    return {"op": "imm", "n": x}
                ast["a"] = a
                ast["b"] = b
        return ast
    def pass2(self, ast: dict) -> dict:
        """Returns an AST with constant expressions reduced"""
        return self.__simplify_ast__(ast)

    def __build_instruction__(self, ast: dict) -> list:
        instructions: list = []
        if 'a' in ast and 'b' in ast:
            a = ast["a"]; b = ast["b"]
            if isinstance(a, dict) and isinstance(b, dict):
                dir = ["imm", "arg"]
                d = {"+": "AD", "-": "SU", "*": "MU", "/": "DI"}
                o = ast["op"]
                if a["op"] in dir:
                    if b["op"] in dir:
                        q = b["n"]
                        b = "IM %d" % q if b["op"] == "imm" else "AR %d" % q
                        p = a["n"]
                        a = "IM %d" % p if a["op"] == "imm" else "AR %d" % p
                        instructions = [b, "SW", a, d[o], "PU"]
                    else:
                        ins = self.__build_instruction__(b)
                        instructions.extend(ins)
                        p = a["n"]
                        a = "IM %d" % p if a["op"] == "imm" else "AR %d" % p
                        instructions.extend(["PO", "SW", a, d[o], "PU"])
                else:
                    if b["op"] in dir:
                        ins = self.__build_instruction__(a)
                        instructions.extend(ins)
                        q = b["n"]
                        b = "IM %d" % q if b["op"] == "imm" else "AR %d" % q
                        instructions.extend([b, "SW", "PO", d[o], "PU"])
                    else:
                        ins = self.__build_instruction__(a)
                        instructions.extend(ins)
                        ins = self.__build_instruction__(b)
                        instructions.extend(ins)
                        instructions.extend(["PO", "SW", "PO", d[o], "PU"])
        return instructions
    def pass3(self, ast: dict) -> list:
        """Returns assembly instructions"""
        instructions = self.__build_instruction__(ast)
        print(instructions)
        return instructions
      
###################
import re
from collections import deque
from pprint import pprint
from typing import Deque, Dict, List, Union

'''
I really want to use some classes like these:

class BasicAST:
    __slots__ = ('op',)
    def __getitem__(self, name):
        return getattr(self, name)
    def __setitem__(self, name):
        return setattr(self, name)
class BinopAST(BasicAST):
    __slots__ = ('a', 'b')
    def __init__(self, op, a , b):
        self.op = op
        self.a = a
        self.b = b
class UnopAST(BasicAST):
    __slots__ = ('n',)
    def __init__(self, op, n):
        self.op = op
        self.n = n

but it seems contrary to the spirit of tests to define equals methods
that compare these equal to dicts holding the same information, regardless
of whether it would work or not.
I also already wrote this code to use dicts.
'''

class Compiler(object):
    __slots__ = ('func_args',)
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program: str) -> List[Union[str, int]]:
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    def pass1(self, program: str):
        """Returns an un-optimized AST"""
        tokens: Deque[Union[str, int]] = deque(self.tokenize(program))
        
        # helper lambdas to generate JSON
#         binop = lambda op, a, b: {'op': op, 'a': a, 'b': b}
        unop = lambda op, n: {'op': op, 'n': n}
        arg = lambda n: unop('arg', n)
        imm = lambda n: unop('imm', n)
        
        fun_args = []
        assert tokens.popleft() == '['
        while tokens[0].isalpha():
            fun_args.append(tokens.popleft())
        assert tokens.popleft() == ']'
        print('fun args:', fun_args)
        self.func_args = fun_args
        
        arg_lookup: Dict[str, int] = {
            arg: index
            for index, arg in enumerate(fun_args)
        }
        
        AST_JSON = Dict[str, Union[str, 'AST_JSON']]
        AST_Value = Union[None, str, int, AST_JSON]
        ast_stack: List[AST_Value] = []
        paren_stack: List[int] = []
        
        #print('tokens', tokens)
        while tokens:
            token = tokens.popleft()
            if token == ')':
                paren_i = paren_stack.pop()
                paren_tokens = ast_stack[paren_i + 1:]
                del ast_stack[paren_i + 1:]
                assert ast_stack.pop() == '('
                #print('paren tokens', paren_tokens)
                expr = self.build_ast(paren_tokens)
                #print('paren expr', expr)
                ast_stack.append(expr)
            elif isinstance(token, int):
                int_val = token
                int_ast = imm(int_val)
                ast_stack.append(int_ast)
            elif token.isalpha():
                var_name = token
                var_num = arg_lookup[var_name]
                var_ast = arg(var_num)
                ast_stack.append(var_ast)
            else:
                if token == '(':
                    paren_stack.append(len(ast_stack))
                ast_stack.append(token)
        #print('ast stack', ast_stack[::-1])
        expr = self.build_ast(ast_stack)
        assert not ast_stack
        self.pprint_ast(expr)
        return expr
    
    def build_ast(self, parenless_ast_stack):
        ast_stack = parenless_ast_stack
        ast_stack.reverse()
        # helper lambda to generate JSON
        binop = lambda op, a, b: {'op': op, 'a': a, 'b': b}
        
        # make a +- only ast stack
        pm_ast_stack = [ast_stack.pop()]
        while len(ast_stack) >= 2:
            op = ast_stack.pop()
            right_arg = ast_stack.pop()
            if op in '*/':
                left_arg = pm_ast_stack.pop()
                expr = binop(op, left_arg, right_arg)
                pm_ast_stack.append(expr)
            elif op in '+-':
                pm_ast_stack.append(op)
                pm_ast_stack.append(right_arg)
            else:
                raise SyntaxError(op)
        # fully build the ast
        pm_ast_stack.reverse()
        while len(pm_ast_stack) >= 3:
            left_arg = pm_ast_stack.pop()
            op = pm_ast_stack.pop()
            right_arg = pm_ast_stack.pop()
            expr = binop(op, left_arg, right_arg)
            pm_ast_stack.append(expr)
        return pm_ast_stack.pop()
    
    def pprint_ast(self, ast):
        printing_stack = [ast]
        while printing_stack:
            node = printing_stack.pop()
            if isinstance(node, str):
                print(node,end='')
            else:
                op = node['op']
                if len(op) == 1:
                    # binop
                    printing_stack.extend([
                        '(',
                        node['a'],
                        f' {op} ',
                        node['b'],
                        ')'
                    ][::-1])
                elif len(op) == 3:
                    # unop
                    n = node['n']
                    if op == 'imm':
                        string = str(n)
                    elif op == 'arg':
                        string = str(self.func_args[n])
                    else:
                        raise AssertionError(op)
                    print(string, end='')
                else:
                    raise AssertionError(op)
                    
    def pass2(self, ast):
        """
        Returns an AST with constant expressions reduced
        Mutates the passed AST while simplifying
        """
        binops = '+-*/'
        parent_ids = set()
        node_stack = []
        if ast['op'] in binops:
            #self.pprint_ast(ast)
            ast_container = {'ast': ast}
            node_stack.append((ast_container, 'ast'))
        else:
            return ast
        
        while node_stack:
            container, name = node_stack.pop()
            node = container[name]
            #print('got node: ', end='')
            #self.pprint_ast(node)
            op = node['op']
            if op in binops:
                #print('is binop')
                a = node['a']
                b = node['b']
                if a['op'] == 'imm' and b['op'] == 'imm':
                    #print('simplifies to ', end='')
                    an = a['n']
                    bn = b['n']
                    if op == '+':
                        an += bn
                    elif op == '-':
                        an -= bn
                    elif op == '*':
                        an *= bn
                    elif op == '/':
                        an /= bn
                    #print(an)
                    parent_ids.discard(id(node))
                    node = {'op': 'imm', 'n': an}
                    container[name] = node
                elif id(node) not in parent_ids:
                    #print('pushing node with children')
                    parent_ids.add(id(node))
                    node_stack.append((container, name))
                    node_stack.append((node, 'a'))
                    node_stack.append((node, 'b'))
                else:
                    #print('node unsimplifyable')
                    parent_ids.discard(id(node))
        
        ast = ast_container['ast']
        self.pprint_ast(ast)
        return ast
    
    def pass3(self, ast):
        """Returns assembly instructions"""
        asm: List[Union[str, Dict[str, Any]]] = []
        
        writing_stack = [ast]
        binops = {
            '+': 'AD',
            '-': 'SU',
            '*': 'MU',
            '/': 'DI'
        }
        while writing_stack:
            node = writing_stack.pop()
            if isinstance(node, str):
                asm.append(node)
            else:
                op = node['op']
                if op == 'imm':
                    asm.append('IM ' + str(node['n']))
                elif op == 'arg':
                    asm.append('AR ' + str(node['n']))
                elif op in binops:
                    # structure of an asm binop:
                    # write the first argument
                    # push it onto the stack
                    # write the second argument
                    # swap the arguments
                    # pop the first one from the stack
                    # do the operation

                    writing_stack.extend([
                        node['a'],
                        'PU',
                        node['b'],
                        'SW',
                        'PO',
                        binops[op]
                    ][::-1])
                else:
                    raise SyntaxError(node)
        return asm
      
#########################
import re


class Compiler(object):
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }

    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))

    @staticmethod
    def tokenize(program):
        """Turn a program string into an array of tokens.  Each token
        is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
        name or a number (as a string)"""
        token_iter = (
            m.group(0) for m in re.finditer(r"[-+*/()[\]]|[A-Za-z]+|\d+", program)
        )
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    @staticmethod
    def extract_args(tokens):
        args = {}
        args_index = 0
        if tokens[0] == "[":
            tokens.pop(0)
            while tokens[args_index] != "]":
                args[tokens[args_index]] = args_index
                args_index += 1
        return args, args_index + 1

    @staticmethod
    def hasPrecedence(op1, op2):
        return (
            (op1 == op2)
            or (op1 == "*" and op2 == "/")
            or (op1 == "/" and op2 == "*")
            or (op1 == "+" and op2 == "-")
            or (op1 == "-" and op2 == "+")
            or ((op1 == "*" or op1 == "/") and (op2 == "+" or op2 == "-"))
        )

    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program)

        # Pulling out args first
        args, last_index = self.extract_args(tokens)

        #
        ops_list = []
        var_list = []

        for token in tokens[last_index:]:

            if not (token in self.operators or token in {"(", ")"}):
                if isinstance(token, int):
                    var_list.append({"op": "imm", "n": token})
                else:
                    var_list.append({"op": "arg", "n": args[token]})

            elif token in self.operators:
                while ops_list and self.hasPrecedence(ops_list[0], token):
                    var_list.append(
                        {
                            "op": ops_list.pop(0),
                            "a": var_list.pop(-2),
                            "b": var_list.pop(-1),
                        }
                    )
                ops_list.insert(0, token)

            elif token == "(":
                ops_list.insert(0, token)

            elif token == ")":
                while ops_list and ops_list[0] != "(":
                    var_list.append(
                        {
                            "op": ops_list.pop(0),
                            "a": var_list.pop(-2),
                            "b": var_list.pop(-1),
                        }
                    )
                if ops_list[0] == "(":
                    ops_list.pop(0)

        while ops_list:
            var_list.append(
                {"op": ops_list.pop(0), "a": var_list.pop(-2), "b": var_list.pop(-1)}
            )
        return var_list.pop(-1)

    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""

        def flatten_ast(ast_):
            if ast_.get("a") or ast_.get("b"):

                if ast_["a"]["op"] != "imm":
                    ast_["a"] = flatten_ast(ast_["a"])

                if ast_["b"]["op"] != "imm":
                    ast_["b"] = flatten_ast(ast_["b"])

                if ast_["a"]["op"] == "imm" and ast_["b"]["op"] == "imm":
                    return {
                        "op": "imm",
                        "n": self.operators[ast_["op"]](ast_["a"]["n"], ast_["b"]["n"]),
                    }
            return ast_

        return flatten_ast(ast)
    
    @staticmethod
    def pass3(ast):
        """Returns assembly instructions"""
        ops_instructions = {"+": "AD", "-": "SU", "*": "MU", "/": "DI"}

        def create_asm(ast_):
            asm = []

            if ops_instructions.get(ast_["op"]):
                return [
                    *create_asm(ast_["a"]),
                    "PU",
                    *create_asm(ast_["b"]),
                    "SW",
                    "PO",
                    ops_instructions[ast_["op"]],
                ]
            if ast_["op"] == "imm":
                asm.insert(0, f"IM {ast_['n']}")
            elif ast_["op"] == "arg":
                asm.insert(0, f"AR {ast_['n']}")
            return asm

        return create_asm(ast)
