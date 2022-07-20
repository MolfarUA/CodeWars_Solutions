59f9cad032b8b91e12000035


import re
import string

char_element = '[^\', ">\\\n\r\t]'

def get_number(text):
    result = re.match(r'-?\d+', text)
    if result is not None:
        return int(text) % 256
    result = re.match(r"'(%s)'" % char_element, text)
    if result is not None:
        return ord(text[1]) % 256
    return None

def get_variable(text):
    var_prefix = '$_' + string.ascii_letters
    var_suffix = string.digits + var_prefix
    re_var = r'[%s][%s]*' % (var_prefix, var_suffix)
    result = re.match(re_var, text)
    if result is not None:
        return text.lower()
    return None

def get_code_offset(start_ptr, stop_ptr):           
    offset = start_ptr - stop_ptr
    route = '>' if offset < 0 else '<'
    return route*abs(offset)


class BrainCompiler():
    
    def __init__(self, text):
        self.full_text = text
        self.top_ptr = 0
        self.ptr_free = {}
        self.stack_ns = [(None, {})]
        self.list_ptr = {}
        self.proc_code = {}
        self.main_code = self._parse_code()
        self.macro_code = self._macro_call()
        self.brain_code = self.compilation()

    def __str__(self):
        return self.brain_code
    
    def _change_char(self, txt):
        result = re.search(r"'%s'" % char_element, txt)
        if result is None:
            return txt
        a, b = result.start(), result.end()
        end = self._change_char(txt[b:])
        new = str(ord(txt[a+1:b-1]) % 256)
        return txt[:a] + new + end

    def _parse_split(self, line):
        return [v for v in re.split(r'\s+', line) if v]
    
    def _parse_var(self, line):
        vs, txt = [], self._change_char(line).lower()
        lb, rb = re.split(r'\[', txt), re.split(r'\]', txt)
        assert len(lb) == len(rb), 'Unclosed [] pair.'
        result = re.search(r'\[\s*-?\d+\s*\]', txt)
        while result is not None:
            a, b = result.start(), result.end()
            ns = self._parse_split(txt[:a])
            num, txt = int(txt[a+1:b-1]), txt[b:]
            result = re.search(r'\[\s*-?\d+\s*\]', txt)
            vs.extend([[n] for n in ns[:-1]])
            vs.append((ns[-1], num % 256))
        vs.extend([[n] for n in self._parse_split(txt)])
        return [('add_var_ptr', v) for v in vs]

    def _parse_msg(self, line):
        result = re.split(r'"', line)
        assert len(result) % 2 != 0, 'Unclosed "" pair.'
        result[1::2] = [[('str', txt)] for txt in result[1::2]]
        set_var = lambda xs: [('var', get_variable(x)) for x in xs]
        result[0::2] = [set_var(self._parse_split(txt)) for txt in result[0::2]]
        return ('get_msg', [sum(result, [])])

    def _parse_header(self, line):
        args = self._parse_args(line)
        is_fn = len(args) != 0 and args[0][1] is not None
        assert is_fn, 'Number of arguments for an instruction does not match the expectation.'
        v_args = [v for _, v in args[1:] if v is not None]
        assert len(v_args) == len(args)-1, 'Expect a variable but got something else.'
        return (args[0][1], v_args)
    
    def _parse_args(self, line, types=None):
        txt = self._change_char(line)
        assert len(re.split(r"'", txt)) == 1, "Unclosed '' pair."
        args, bits = [], self._parse_split(txt)
        if types is None:
            types = ("0" + '0'*len(bits))[:-1]
        assert len(bits) == len(types), 'Number of arguments for an instruction does not match the expectation.'
        for b, t in zip(bits, types):
            name = get_variable(b)
            if t == '0':
                args.append(('var', name))
            elif t == '1':
                if name is None:
                    args.append(('val', get_number(b)))
                else:
                    args.append(('var', name))
            elif t == '2':
                args.append(('lst', name))
        return args
    
    def _parse_code(self, lines=None, main=True):
        ends, code = 'end', []
        if main and lines is None:
            lines = self.clear_comments()
            ends, lines = None, lines.split('\n')[::-1]
        ts = {t: '01' for t in ('set', 'inc', 'dec')}
        ts.update({t: '110' for t in ('add', 'sub', 'mul', 'div', 'mod', 'cmp')})
        ts.update({'read': '0', 'divmod': '1100', 'a2b': '1110', 
                   'b2a': '1000', 'lset': '211', 'lget': '210'})
        while lines:
            line = re.split(r'^\s+', lines.pop())[-1]
            result = re.split(r'(\s|[|]|\'|")', line)[0]
            statement = result.lower()
            line = line[len(statement):]
            if statement == ends:
                return code
            assert statement != 'end', 'End before beginning a block.'
            if statement == 'var':
                assert main, 'Define variables inside a procedure.'
                code.extend(self._parse_var(line))
            elif statement == 'msg':
                code.append(self._parse_msg(line))            
            elif statement in ts:
                args = self._parse_args(line, ts[statement])
                code.append(('get_' + statement, args))
            elif statement == 'call':
                fn, v_args = self._parse_header(line)
                code.append(('get_' + statement, (fn, v_args)))
            elif statement == 'proc':
                assert main, 'Nested procedures.'
                fn, v_args = self._parse_header(line)
                assert fn not in self.proc_code, 'Duplicate procedure names.'
                assert len(set(v_args)) == len(v_args), 'Duplicate parameter names.'
                m_code = self._parse_code(lines, False)
                self.proc_code[fn] = (v_args, m_code)
            elif statement in ['ifeq', 'ifneq', 'wneq']:
                m_code = self._parse_code(lines, main)
                args = self._parse_args(line, '01') + [m_code]
                code.append(('get_' + statement, args))
            else:
                assert False, 'Unknown instructions. + ' + statement
        assert ends is None,  'Unclosed blocks.'
        return code

    def _free_tmp(self, t_ptr):
        if t_ptr[0] == 'tmp':
            self.ptr_free[t_ptr[1]] = True
    
    def _free_enum_tmp(self, enum):
        for t_ptr in enum:
            self._free_tmp(t_ptr)
        
    def _take_tmp(self, t_var=None):
        if t_var is not None:
            return t_var
        for ptr in self.ptr_free:
            if self.ptr_free[ptr]:
                self.ptr_free[ptr] = False
                return 'tmp', ptr
        ptr = self.top_ptr
        self.ptr_free[ptr] = False
        self.top_ptr += 1
        return 'tmp', ptr
    
    def _take_enum_tmp(self, enum):
        return [self._take_tmp(t) for t in enum]

    def _while(self, check, frame):
        ptr = self.get_var_ptr(check)
        return [ptr, '['] + frame + [ptr, ']']
    
    def _clone(self, source, lt_ptr):
        l_ptr = [self.get_var_ptr(t_ptr) for t_ptr in lt_ptr]
        code = sum([[ptr, '[-]'] for ptr in l_ptr], [])
        frame = ['-'] + sum([[ptr, '+'] for ptr in l_ptr], [])
        return code + self._while(source, frame)
    
    def _if_true(self, check, frame):
        return self._while(check, ['[-]'] + frame)
    
    def _if_false(self, check, frame, t_tmp):
        ptr = self.get_var_ptr(t_tmp)
        code = [ptr, '[-]+'] + self._if_true(check, [ptr, '-'])
        return code + self._while(t_tmp, ['-'] + frame)
    
    def _macro_call(self, m_code=None):
        if m_code is None:
            m_code = self.main_code
        code, lines = [], m_code[::-1]
        while lines:
            line = lines.pop()
            code += getattr(self, line[0])(*line[1])
        return code

    def clear_comments(self):
        comment_prefix = r'(?://|--|#|[rR][eE][mM]\s)'
        del_empty = lambda xs: re.split(r'^\s+', xs)[-1]
        lines = self.full_text.split('\n')
        for i, line in list(enumerate(lines)):
            quote = line.split('"')
            for k, xs in list(enumerate(quote))[::2]:
                rezult = re.split(comment_prefix, xs)
                if len(rezult) != 1:
                    line = '"'.join(quote[:k]+rezult[:1])
                    break
            lines[i] = del_empty(line)
        return '\n'.join(line for line in lines if line)
    
    def add_var_ptr(self, name, count=None):
        is_present = name in self.stack_ns[0][1] or name in self.list_ptr
        assert not is_present, 'Duplicate var names.'
        if count is None:
            self.stack_ns[0][1][name] = self.top_ptr
            self.top_ptr += 1
        else:
            self.list_ptr[name] = self.top_ptr + 1
            self.top_ptr += 2 + 2*count
        return []
    
    def get_var_ptr(self, t_name):
        t_var, name = t_name
        if t_var == 'tmp':
            return name
        assert name is not None, 'Expect a variable but got something else.'
        for _, vars_ptr in self.stack_ns[::-1]:
            if name in vars_ptr:
                assert t_var == 'var', 'Expect a list but got a variable.'
                return vars_ptr[name]
        if name in self.list_ptr:
            assert t_var == 'lst', 'Expect a variable but got a list.'
            return self.list_ptr[name]
        assert is_var or is_lst, 'Undefined var names.'
    
    def set_zero(self, t_var):
        return [self.get_var_ptr(t_var), '[-]']
    
    def get_read(self, t_var):
        return [self.get_var_ptr(t_var), ',']
    
    def get_msg(self, bits):
        msg, t_tmp = 0, self._take_tmp()
        code = self.set_zero(t_tmp)
        for bit in bits:
            if bit[0] == 'var':
                code.extend([self.get_var_ptr(bit), '.'])
            else:
                code.append(t_tmp[1])
                txt = '\n'.join(re.split(r'\\n', bit[1]))
                for char in txt:
                    num = ord(char) % 256
                    msg, add = num, num - msg
                    route = '+' if add > 0 else '-'
                    code.extend([route*abs(add), '.'])
        self._free_tmp(t_tmp)
        return code

    def get_set(self, t_var, nv_fst):
        if nv_fst[0] == 'val':
            ptr = self.get_var_ptr(t_var)
            return [ptr, '[-]', '+'*nv_fst[1]]
        if t_var == nv_fst:
            return []
        t_tmp = self._take_tmp()
        code = self._clone(nv_fst, [t_tmp])
        code += self._clone(t_tmp, [t_var, nv_fst])
        self._free_tmp(t_tmp)
        return code

    def get_inc(self, t_var, nv_fst):
        ptr = self.get_var_ptr(t_var)
        if nv_fst[0] == 'val':
            return [ptr, '+'*nv_fst[1]]
        fst = self.get_var_ptr(nv_fst)
        t_tmp = self._take_tmp()
        code = self._clone(nv_fst, [t_tmp])
        frame = ['-', fst, '+', ptr, '+']
        code += self._while(t_tmp, frame)
        self._free_tmp(t_tmp)
        return code

    def get_dec(self, t_var, nv_fst):
        ptr = self.get_var_ptr(t_var)        
        if nv_fst[0] == 'val':
            return [ptr, '-'*nv_fst[1]]
        fst = self.get_var_ptr(nv_fst)
        if ptr == fst:
            return [ptr, '[-]']
        t_tmp = self._take_tmp()
        code = self._clone(nv_fst, [t_tmp])
        frame = ['-', fst, '+', ptr, '-']
        code += self._while(t_tmp, frame)
        self._free_tmp(t_tmp)
        return code        

    def get_add(self, nv_fst, nv_snd, t_var):
        if nv_fst == t_var:
            return self.get_inc(t_var, nv_snd)
        if nv_snd == t_var:
            return self.get_inc(t_var, nv_fst)
        code = self.get_set(t_var, nv_fst)
        return code + self.get_inc(t_var, nv_snd)

    def get_sub(self, nv_fst, nv_snd, t_var):
        if nv_fst == t_var:
            return self.get_dec(t_var, nv_snd)
        if nv_snd == t_var:
            ptr = self.get_var_ptr(t_var)  
            t_tmp = self._take_tmp()
            code = self._clone(t_var, [t_tmp])
            code += self.get_set(t_var, nv_fst)
            code += self._while(t_tmp, ['-', ptr, '-'])
            self._free_tmp(t_tmp)
            return code
        code = self.get_set(t_var, nv_fst)
        return code + self.get_dec(t_var, nv_snd)

    def get_mul(self, nv_fst, nv_snd, t_var):
        t_fst, t_snd = self._take_enum_tmp([None, None])
        code = self.get_set(t_fst, nv_fst)
        code += self.get_set(t_snd, nv_snd)
        code += self.set_zero(t_var)
        frame = self.get_inc(t_var, t_snd)
        code += self._while(t_fst, ['-'] + frame)
        self._free_enum_tmp([t_fst, t_snd])
        return code
    
    def get_div(self, nv_fst, nv_snd, t_var):
        return self.get_divmod(nv_fst, nv_snd, t_var, None)
    
    def get_mod(self, nv_fst, nv_snd, t_var):
        return self.get_divmod(nv_fst, nv_snd, None, t_var)
        
    def get_divmod(self, nv_fst, nv_snd, t_div, t_mod):
        ts = self._take_enum_tmp([None, None, None, None, t_div, t_mod])
        t_fst, t_snd, t_if_1, t_if_2, t_div, t_mod = ts
        p_div = self.get_var_ptr(t_div)
        p_mod = self.get_var_ptr(t_mod)
        code = self.get_set(t_fst, nv_fst)
        code += self.get_set(t_snd, nv_snd)
        code += self.set_zero(t_div) + self.set_zero(t_mod)
        code += self.get_set(t_if_2, t_snd)
        frame = self.get_set(t_if_1, t_fst)
        frame_mod = self._if_true(t_if_1, [t_fst[1], '-', p_mod, '+'])
        frame_mod += self.get_set(t_if_1, t_fst)
        frame += self._while(t_if_2, ['-'] + frame_mod)
        frame_div = [p_div, '+'] + self._clone(t_mod, [t_if_2])
        frame += self._if_true(t_if_1, frame_div)
        code += self._while(t_fst, frame)
        code += self.get_dec(t_snd, t_mod)
        frame_end = [p_div, '+'] + self.set_zero(t_mod)
        code += self._if_false(t_snd, frame_end, t_if_2)
        self._free_enum_tmp(ts)
        return code

    def get_cmp(self, nv_fst, nv_snd, t_var):
        ptr = self.get_var_ptr(t_var)
        ts = self._take_enum_tmp([None, None, None])
        t_fst, t_snd, t_if_1 = ts
        code = self.get_set(t_fst, nv_fst)
        code += self.get_set(t_snd, nv_snd)
        code += self.get_sub(nv_fst, nv_snd, t_if_1)
        code += self.set_zero(t_var)
        frame_cmp = self.get_set(t_if_1, t_snd)
        frame_cmp += self._if_true(t_if_1, [t_snd[1], '-'])
        frame = self._while(t_fst, ['-'] + frame_cmp)
        frame += self._if_true(t_snd, [ptr, '--'])
        code += self._if_true(t_if_1, [ptr, '+'] + frame)
        self._free_enum_tmp(ts)
        return code
    
    def get_a2b(self, nv_fst, nv_snd, nv_thr, v_a2b):
        ts = self._take_enum_tmp([None, None, None])
        t_fst, t_snd, t_thr = ts
        code = self.get_set(t_fst, nv_fst)
        code += self.get_dec(t_fst, ('val', 48))
        code += self.get_mul(t_fst, ('val', 10), t_snd)
        code += self.get_inc(t_snd, nv_snd)
        code += self.get_dec(t_snd, ('val', 48))
        code += self.get_mul(t_snd, ('val', 10), t_thr)
        code += self.get_inc(t_thr, nv_thr)
        code += self.get_sub(t_thr, ('val', 48), v_a2b)
        self._free_enum_tmp(ts)
        return code
    
    def get_b2a(self, nv_b2a, v_fst, v_snd, v_thr):
        t_b2a = self._take_tmp()
        code = self.get_set(t_b2a, nv_b2a)
        code += self.get_divmod(t_b2a, ('val', 10), t_b2a, v_thr)
        code += self.get_inc(v_thr, ('val', 48))
        code += self.get_divmod(t_b2a, ('val', 10), v_fst, v_snd)
        code += self.get_inc(v_snd, ('val', 48))
        code += self.get_inc(v_fst, ('val', 48))
        self._free_tmp(t_b2a)
        return code
    
    def _mount_ptr(self, t_lst, t_var):
        l_ptr = self.get_var_ptr(t_lst)
        code = self.get_set(t_lst, t_var)
        return code + [l_ptr, '[->[>>]+[<<]>]']
    
    def _clear_ptr(self, t_lst):
        l_ptr = self.get_var_ptr(t_lst)
        return [l_ptr, '>[>>]<<[-<<]>']
        
    def get_lset(self, t_lst, nv_fst, nv_snd):
        l_ptr = self.get_var_ptr(t_lst)
        if nv_fst[0] == 'val':
            t_set = ('tmp', l_ptr + 2 + 2 * nv_fst[1])
            return self.get_set(t_set, nv_snd)
        lm, rm = '>[>>]>', '<<<[<<]>'
        code = self._mount_ptr(t_lst, nv_fst)
        code += [l_ptr, lm, '[-]', rm]
        code += self._while(nv_snd, ['-', l_ptr, '+', lm, '+', rm])
        code += self._clone(t_lst, [nv_snd])
        return code + self._clear_ptr(t_lst)
        
    def get_lget(self, t_lst, nv_fst, t_var):
        l_ptr = self.get_var_ptr(t_lst)
        if nv_fst[0] == 'val':
            t_get = ('tmp', l_ptr + 2 + 2 * nv_fst[1])
            return self.get_set(t_var, t_get)
        ptr = self.get_var_ptr(t_var)
        lm, rm = '>[>>]>', '<<<[<<]>'
        code = self.set_zero(t_var)
        code += self._mount_ptr(t_lst, nv_fst)
        code += [l_ptr, lm, '[-', rm, '+', lm, ']', rm]
        code += self._while(t_lst, ['-', lm, '+', rm, ptr, '+'])
        return code + self._clear_ptr(t_lst)

    def get_ifeq(self, t_var, nv_fst, m_code):
        t_fst, t_if_1 = self._take_enum_tmp([None, None])
        code = self.get_sub(t_var, nv_fst, t_fst)
        frame = self._macro_call(m_code)
        code += self._if_false(t_fst, frame, t_if_1)
        self._free_enum_tmp([t_fst, t_if_1])
        return code
    
    def get_ifneq(self, t_var, nv_fst, m_code):
        t_fst = self._take_tmp()
        code = self.get_sub(t_var, nv_fst, t_fst)
        frame = self._macro_call(m_code)
        code += self._if_true(t_fst, frame)
        self._free_tmp(t_fst)
        return code
    
    def get_wneq(self, t_var, nv_fst, m_code):
        t_fst = self._take_tmp()
        code = self.get_sub(t_var, nv_fst, t_fst)
        frame = self._macro_call(m_code)
        code += self._while(t_fst, frame + code)
        self._free_tmp(t_fst)
        return code
    
    def get_call(self, fn, args):
        assert fn in self.proc_code, 'Undefined procedure.'
        p_args, m_code = self.proc_code[fn]
        assert len(args) == len(p_args), 'Number of arguments for an instruction does not match the expectation.'
        assert all(fn != n for n, _ in self.stack_ns), 'Recursive call.'
        vs_ptr = {p: self.get_var_ptr(('var', arg)) for arg, p in zip(args, p_args)}
        self.stack_ns.append((fn, vs_ptr))
        code = self._macro_call(m_code)
        self.stack_ns.pop()
        return code    

    def compilation(self):
        comp, ptr, codes = [], 0, self.macro_code
        for code in codes:
            if not isinstance(code, str):
                ptr, code = code, get_code_offset(ptr, code)
            comp.append(code)
        return ''.join(comp)

    
def kcuf(code):
    return str(BrainCompiler(code))
  
####################
import re
import string
from types import FunctionType
from time import time


def tokenize(code: str):
    VAR_PREFIX = '$_' + string.ascii_letters
    VAR_SUFFIX = VAR_PREFIX + string.digits

    tokens = []
    while code:
        if code[:4] == 'rem ':
            code = code[code.find('\n'):]
        elif code[0] in VAR_PREFIX:
            m = re.match(rf'^[{VAR_PREFIX}][{VAR_SUFFIX}]*', code)
            tokens.append(('id', m.group(0).lower()))
            code = code[m.span(0)[1]:]
        elif code[0] in ' \r\t\v':
            code = code[1:]
        elif code[0] == '\n':
            tokens.append(('instr_end', None))
            code = code[1:]
        elif code[:2] in ('//', '--') or code[:1] == '#':
            code = code[code.find('\n'):] if '\n' in code else ''
        elif code[0] == '\'':
            m = re.match(f'^\'([^\'"\\\\]|\\\\[\\\\\'"nrt])\'', code)
            data = re.sub('[^\'"\\\\]|\\\\[\\\\\'"nrt]', lambda c: c.group() if len(c.group()) == 1 else eval(f'"{c.group()}"'), m.group(1))
            tokens.append(('number', ord(data)))
            code = code[m.span(0)[1]:]
        elif code[0] == '"':
            m = re.match(f'^\"((?:[^\'"\\\\]|\\\\[\\\\\'"nrt])*)\"', code)
            data = re.sub('[^\'"\\\\]|\\\\[\\\\\'"nrt]', lambda c: c.group() if len(c.group()) == 1 else eval(f'"{c.group()}"'), m.group(1))
            tokens.append(('string', data))
            code = code[m.span(0)[1]:]
        elif code[0] == '[':
            tokens.append(('brace_open', '['))
            code = code[1:]
        elif code[0] == ']':
            tokens.append(('brace_close', ']'))
            code = code[1:]
        elif code[0] in f'-{string.digits}':
            m = re.match(r'^-?\d+', code)
            tokens.append(('number', int(m.group(0)) % 256))
            code = code[m.span(0)[1]:]
        else:
            raise SyntaxError('cannot tokenize the code')
    return tokens


class State:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def advance(self):
        self.index += 1

    def peek(self, distance=0):
        if self.index + distance >= len(self.tokens):
            return ('instr_end', None)
        return self.tokens[self.index + distance]

    def is_eof(self):
        return self.index >= len(self.tokens)

    def next(self):
        self.advance()
        return self.peek(-1)

    def end_instr(self):
        if self.next() != ('instr_end', None):
            raise SyntaxError('end of instruction expected')


def parse(tokens):
    program = []
    state = State(tokens)
    while not state.is_eof():
        res = parse_statement(state)
        if res: program.append(res)

    return program


def parse_statement(state: State):
    while not state.is_eof() and state.peek()[0] == 'instr_end': state.advance()
    if state.is_eof(): return None

    instr = state.next()
    if instr[0] != 'id':
        raise SyntaxError('instruction expected')
    instr = instr[1]
    if instr == 'msg':
        args = []
        while True:
            arg = state.next()
            if arg == ('instr_end', None): break
            if arg[0] != 'id' and arg[0] != 'string':
                raise SyntaxError('msg instruction requires <id|string> as an argument\n  something else was given')
            args.append(arg)
        return ('msg', args)
    elif instr == 'var':
        vars = {}
        while state.peek()[0] == 'id':
            name = state.next()[1]
            size = 0
            if name in vars:
                raise NameError(f'variables with identifier "{name}" already exists')
            if state.peek() == ('brace_open', '['):
                state.advance()
                size = state.next()[1]
                if type(size) is not int:
                    raise TypeError('variable size must be a <number>')
                if state.next() != ('brace_close', ']'):
                    raise SyntaxError('closing bracket expected')
            vars[name] = size
        state.end_instr()
        return ('var', vars)
    elif instr == 'read':
        var = state.next()
        if var[0] != 'id':
            raise SyntaxError(f'{instr} instruction requires 1 argument: <id>>\n  something else was given')
        state.end_instr()
        return (instr, var)
    elif instr in ('set', 'inc', 'dec'):
        var = state.next()
        val = state.next()
        if var[0] != 'id' or val[0] not in ('number', 'id',):
            raise SyntaxError(f'{instr} instruction requires 2 arguments: <id> <number|id>\n  something else was given')
        state.end_instr()
        return (instr, (var, val))

    # generic parsing
    args = []
    while True:
        arg = state.next()
        if arg == ('instr_end', None): break
        args.append(arg)

    return (instr, args)


def prepare(icode):
    program = {
        'globals': [],
        'procedures': {},
        'instructions': [],
        'stack': ['<source>'],
    }

    # resolve procedures
    depth = 0
    current_proc = None
    procs = {}
    cicode = []
    for i in icode:
        if i[0] == 'proc':
            if current_proc is not None:
                raise SyntaxError('nested procedures are not permitted')
            if i[1][0] in procs:
                raise Exception('procedures cannot have duplicate names')
            if len(set(i[1][1:])) != len(i[1][1:]):
                raise Exception('procedure parameters cannot have duplicate names')
            current_proc = procs[i[1][0]] = { 'name': i[1][0][1], 'params': i[1][1:], 'code': [] }
            depth += 1
            continue

        if current_proc is None:
            cicode.append(i)
        elif i[0] == 'var':
            raise SyntaxError('variable declaration inside procedures is not allowed')
        elif i[0] != 'end' or depth > 1:
            current_proc['code'].append(i)

        if i[0] in ('ifeq', 'ifneq', 'wneq'):
            depth += 1
        elif i[0] == 'end':
            depth -= 1
            if depth == 0:
                current_proc = None
    program['procedures'] = procs
    icode = cicode

    vars = [(v, {'size': args[v] if args[v] else 1, 'is_list': args[v] > 0, 'offset': 0}) for i, args in icode if i == 'var' for v in args]
    if len(set(v[0] for v in vars)) != len(vars):
        raise Exception('variables cannot have duplicate names')
    program['globals'] = dict(vars)
    offset = 0
    for g in program['globals']:
        program['globals'][g]['offset'] = offset
        offset += program['globals'][g]['size']
    icode = [i for i in icode if i[0] != 'var']

    for i in icode:
        program['instructions'].append(i)

    return program


def get_var_offset(program_info, var):
    if var is None: return None
    # print('getting offset of:', var)
    # print(f"{program_info['wa_size']=};  {program_info['globals'][var[1]]['offset']*2=}")
    # print(f"{program_info['wa_size'] + 2 + program_info['globals'][var[1]]['offset']*2=}")
    return program_info['wa_size'] + 2 + program_info['globals'][var[1]]['offset']*2


def is_list(program_info, val):
    if val is None or val[0] == 'number':
        return False
    return program_info['globals'][val[1]]['is_list']


def decor_bf_make_block(f: FunctionType):
    def func(*args, **kwargs):
        return [f'% {f.__name__[3:]}'] + ['  ' + line for line in f(*args, **kwargs)]
    return func


@decor_bf_make_block
def bf_read(program_info, var):
    offset = get_var_offset(program_info, var)
    return ['>'*offset + ',' + '<'*offset]


@decor_bf_make_block
def bf_write(program_info, data):
    if data[0] == 'string': return bf_writes(program_info, data[1])
    return bf_writev(program_info, data)


@decor_bf_make_block
def bf_writec(program_info, c: str):
    return ['+'*ord(c) + '.' + '[-]']


@decor_bf_make_block
def bf_writes(program_info, msg: str):
    return sum([bf_writec(program_info, c) for c in msg], [])


@decor_bf_make_block
def bf_writev(program_info, var):
    if var[1] not in program_info['globals']:
        raise NameError(f'Variable "{var[1]}" is not defined')
    offset = get_var_offset(program_info, var)
    return ['>'*offset + '.' + '<'*offset]


@decor_bf_make_block
def bf_set(program_info, var, val):
    offset = get_var_offset(program_info, var)
    if val[0] == 'number':
        return ['>'*offset + '[-]' + '+'*val[1] + '<'*offset]
    return [
        *bf_loadc(program_info, val, cell=0),
        *bf_resetc(program_info, cell=offset),
        *bf_movec(program_info, src_cell=0, target_cell=offset)
    ]


@decor_bf_make_block
def bf_loadc(program_info, v, cell):
    if v[0] == 'number':
        return ['>'*cell + ('+'*v[1] if v[1] < 128 else '-'*(256-v[1])) + '<'*cell]

    offset = get_var_offset(program_info, v)
    return [
        '>'*offset + '[->+>>+<<<]>[-<+>]>>[-<<<' +
        '<'*(offset-cell) + '+' + '>'*(offset-cell) + '>>>]<<<' + '<'*offset
    ]


def bf_resetc(program_info, cell):
    if cell is None: return []
    return ['>'*cell + '[-]' + '<'*cell]


@decor_bf_make_block
def bf_movec(program_info, src_cell: int, target_cell):
    if target_cell is None: return bf_resetc(program_info, src_cell)
    assert type(target_cell) is int

    d = target_cell - src_cell
    return ['>' * src_cell + '[-' + '<>'[d>0]*abs(d) + '+' + '><'[d>0]*abs(d) + ']' + '<' * src_cell]


@decor_bf_make_block
def bf_generic_op(program_info, ins, outs, op: FunctionType):
    if any(is_list(program_info, a) for a in list(ins) + list(outs)):
        raise TypeError('generic operations do not work on lists')
    if any(o is not None and o[0] != 'id' for o in outs):
        raise SyntaxError('outputs must be variables')

    return [
        *sum([bf_loadc(program_info, i, cell=idx) for idx, i in enumerate(ins)], []),
        *op(),
        *sum([bf_resetc(program_info, get_var_offset(program_info, o)) for o in outs], []),
        *sum([bf_movec(program_info, src_cell=i, target_cell=get_var_offset(program_info, o)) for i, o in enumerate(outs)], []),
    ]


@decor_bf_make_block
def bf_builtin_add():
    return ['>[-<+>]<']


@decor_bf_make_block
def bf_builtin_sub():
    return ['>[-<->]<']


@decor_bf_make_block
def bf_builtin_mul():
    return ['[- >[->+>+<<]< >>>[-<<+>>]<<<]  >[-]<  >>[-<<+>>]<<']


@decor_bf_make_block
def bf_builtin_divmod():
    """
    Attribution: FSHelix
      in :  >n   d    0   0  0 0
      out:  >0 d-n%d n%d n/d 0 0
    """
    return ['[->[->+>>]>[<<+>>[-<+>]>+>>]<<<<<]', '>[>>>]>[[-<+>]>+>>]<<<<<']


@decor_bf_make_block
def bf_builtin_cmp():
    return [
        ' [->>>>>+>+<<<<<<]>>>>>>[-<<<<<<+>>>>>>]<<<<<<',   # copy first argument
        '>[->>>>>+>+<<<<<<]>>>>>>[-<<<<<<+>>>>>>]<<<<<<<',  # copy second argument
        '[->>+<[->-]>[<<[-]>>->]<<<]>[[-]<+>]<',            # compare A < B
        '[->>>>--<<<<]',                                    # -2 to R if A < B
        '>>>>>[->-<]>[[-]<<+>>]<<',                         # +1 from R if A != B
        '[-<<<<+>>>>]<<<<',                                 # move R to output cell (1st cell)
    ]


@decor_bf_make_block
def bf_builtin_a2b():
    return [
        '-'*48 + '[->>>' + '+'*100 + '<<<]' + '>',
        '-'*48 + '[->>' + '+'*10 + '<<]' + '>',
        '-'*48 + '[->' + '+'*1 + '<]' + '>',
        '[-<<<+>>>]<<<',
    ]


@decor_bf_make_block
def bf_builtin_b2a():
    return [                             #  1      2        3      4      5  6  7
        '>' + '+'*100 + '<',             # >n      100      0      0      0  0  0
        *bf_builtin_divmod(),            # >0      d-n%100  n%100  n/100  0  0  0
        '>>[-<<+>>]  >[->>>+<<<] <<<',   # >n%100  ?        0      0      0  0  n/100
        '>[-]' + '+'*10 + '<',           # >n%100  10       0      0      0  0  n/100
        *bf_builtin_divmod(),            # >0      d-n%10   n%10   n/10   0  0  n/100
        '>[-]>>>>>[-<<<<<<+>>>>>>]<<<',  #  n/100  0        n%10  >n/10   0  0  0
        '[-<<+>>]<<<',                   # >n/100  n/10     n%10   0      0  0  0
        '+'*48 + '>' + '+'*48 + '>' + '+'*48 + '<<'
    ]


@decor_bf_make_block
def bf_lget(program, args):
    if not is_list(program, args[0]):
        raise TypeError('lget expects an array as a 1st argument')
    if is_list(program, args[1]) or is_list(program, args[2]):
        raise TypeError('lget expects an array as a 2nd and 3rd arguments')

    return [
        *bf_loadc(program, args[1], cell=program['wa_size'] + 1),
        '>'*program['wa_size'],
        '>[->>+<<]<',
        '>>>' + '+'*program['globals'][args[0][1]]['offset'],
        '[-[->>+<<]+>>]',  # create trail of 1s to the right of each skipped array element
        '<[->+>>+<<<]',  # create duplicate values in trail-dedicated cells (since they are zeroed)
        '>[-<+>]',  # restore the value of the cell from the adjacent one
        '>>[- <<<<[<<] <+> >>[>>] >>]',  # move value from the holding cell to the memory cell
        '<<<<[-<<]<' + '<'*program['wa_size'],  # move cursor to the beginning of the tape
        *bf_resetc(program, get_var_offset(program, args[2])),
        *bf_movec(program, src_cell=program['wa_size'], target_cell=get_var_offset(program, args[2])),
    ]


@decor_bf_make_block
def bf_lset(program, args):
    if not is_list(program, args[0]):
        raise TypeError('lset expects an array as a 1st argument')
    if is_list(program, args[1]) or is_list(program, args[2]):
        raise TypeError('lset expects an array as a 2nd and 3rd arguments')

    return [
        *bf_loadc(program, args[2], cell=program['wa_size'] + 0),
        *bf_loadc(program, args[1], cell=program['wa_size'] + 1),
        '>'*program['wa_size'],
        '>[->>+<<]<',
        '>>>' + '+'*program['globals'][args[0][1]]['offset'],
        '[-[->>+<<]+>>]',  # create trail of 1s to the right of each skipped array element
        '<[-]>',  # clear the memory cell
        '<<[<<]',  # return to the beginning
        '<[-> >>[>>] <+> <<[<<] <]',  # move value from the holding cell to the memory cell
        '>>>[>>]<<[-<<]<' + '<'*program['wa_size'],  # clear the trail and return to the beginning of the tape
    ]


@decor_bf_make_block
def bf_proc(program, args):
    if args[0][1] in program['stack']:
        raise RecursionError('recursive calls are forbidden: [' + ', '.join(program['stack']) + '] to ' + args[0][1])

    proc = program['procedures'][args[0]]
    if len(args) - 1 != len(proc['params']):
        raise IndexError('procedure call arguments and parameters count mismatch')

    return compile({
        **program,
        'globals': {
            **program['globals'],
            **{p[1]: program['globals'][a[1]] for p, a in zip(proc['params'], args[1:])}},
        'instructions': proc['code'],
        'stack': program['stack'] + [args[0][1]],
    })


def compile(program):
    # pprint(program)
    code = []
    open_fcs = []

    for i, args in program['instructions']:
        if i == 'msg':
            for a in args:
                code += bf_write(program, a)
        elif i == 'set':
            code += bf_set(program, *args)
        elif i == 'inc':
            code += bf_generic_op(program, args[:2], [args[0]], op=bf_builtin_add)
        elif i == 'dec':
            code += bf_generic_op(program, args[:2], [args[0]], op=bf_builtin_sub)
        elif i == 'add':
            code += bf_generic_op(program, args[:2], [args[2]], op=bf_builtin_add)
        elif i == 'sub':
            code += bf_generic_op(program, args[:2], [args[2]], op=bf_builtin_sub)
        elif i == 'mul':
            code += bf_generic_op(program, args[:2], [args[2]], op=bf_builtin_mul)
        elif i == 'div':
            code += bf_generic_op(program, args[:2], [None, None, None, args[2]], op=bf_builtin_divmod)
        elif i == 'mod':
            code += bf_generic_op(program, args[:2], [None, None, args[2], None], op=bf_builtin_divmod)
        elif i == 'divmod':
            code += bf_generic_op(program, args[:2], [None, None, args[3], args[2]], op=bf_builtin_divmod)
        elif i == 'cmp':
            code += bf_generic_op(program, args[:2], [args[2]], op=bf_builtin_cmp)
        elif i == 'a2b':
            code += bf_generic_op(program, args[:3], args[3:], op=bf_builtin_a2b)
        elif i == 'b2a':
            code += bf_generic_op(program, args[:1], args[1:], op=bf_builtin_b2a)
        elif i == 'read':
            code += bf_read(program, args)
        elif i == 'lset':
            code += bf_lset(program, args)
        elif i == 'lget':
            code += bf_lget(program, args)
        elif i == 'call':
            code += bf_proc(program, args)
        elif i == 'wneq':
            open_fcs.append([
                *bf_loadc(program, args[0], cell=0),
                *bf_loadc(program, args[1], cell=1),
                '>[-<->]<',
            ])
            code += [
                *open_fcs[-1],
                '[[-]',
            ]
        elif i == 'ifneq':
            open_fcs.append([])
            code += [
                *bf_loadc(program, args[0], cell=0),
                *bf_loadc(program, args[1], cell=1),
                '>[-<->]<',
                '[[-]',
            ]
        elif i == 'ifeq':
            open_fcs.append([])
            code += [
                *bf_loadc(program, args[0], cell=0),
                *bf_loadc(program, args[1], cell=1),
                '[->-<]',
                '+>[[-]<->]<',
                '[[-]'
            ]
        elif i == 'end':
            code += [
                *open_fcs.pop(),
                ']',
            ]
        else:
            raise NameError(f'Unknown instruction "{i}"')

    return code


def kcuf(code):
    TIME_START = time()
    # print(code)
    tokens = tokenize(code)
    # print(tokens)
    TIME_TOKENIZE = time()
    icode = parse(tokens)
    TIME_PARSE = time()
    program = prepare(icode)
    TIME_PREPARE = time()
    program['wa_size'] = 8
    bf = '\n'.join(compile(program))
    TIME_COMPILE = time()
    print(f'elapsed {int((TIME_COMPILE - TIME_START)*1000*10)/10}ms total')
    print(f'  tokenize: {int((TIME_TOKENIZE - TIME_START)    * 1000 * 10) / 10}ms')
    print(f'  parse   : {int((TIME_PARSE    - TIME_TOKENIZE) * 1000 * 10) / 10}ms')
    print(f'  prepare : {int((TIME_PREPARE  - TIME_PARSE)    * 1000 * 10) / 10}ms')
    print(f'  compile : {int((TIME_COMPILE  - TIME_PREPARE)  * 1000 * 10) / 10}ms')
    return bf

  
########################################
import re
import string
from types import FunctionType
from time import time


def tokenize(code: str):
    VAR_PREFIX = '$_' + string.ascii_letters
    VAR_SUFFIX = VAR_PREFIX + string.digits

    tokens = []
    while code:
        if code[:4] == 'rem ':
            code = code[code.find('\n'):]
        elif code[0] in VAR_PREFIX:
            m = re.match(rf'^[{VAR_PREFIX}][{VAR_SUFFIX}]*', code)
            tokens.append(('id', m.group(0).lower()))
            code = code[m.span(0)[1]:]
        elif code[0] in ' \r\t\v':
            code = code[1:]
        elif code[0] == '\n':
            tokens.append(('instr_end', None))
            code = code[1:]
        elif code[:2] in ('//', '--') or code[:1] == '#':
            code = code[code.find('\n'):] if '\n' in code else ''
        elif code[0] == '\'':
            m = re.match(f'^\'([^\'"\\\\]|\\\\[\\\\\'"nrt])\'', code)
            data = re.sub('[^\'"\\\\]|\\\\[\\\\\'"nrt]', lambda c: c.group() if len(c.group()) == 1 else eval(f'"{c.group()}"'), m.group(1))
            tokens.append(('number', ord(data)))
            code = code[m.span(0)[1]:]
        elif code[0] == '"':
            m = re.match(f'^\"((?:[^\'"\\\\]|\\\\[\\\\\'"nrt])*)\"', code)
            data = re.sub('[^\'"\\\\]|\\\\[\\\\\'"nrt]', lambda c: c.group() if len(c.group()) == 1 else eval(f'"{c.group()}"'), m.group(1))
            tokens.append(('string', data))
            code = code[m.span(0)[1]:]
        elif code[0] == '[':
            tokens.append(('brace_open', '['))
            code = code[1:]
        elif code[0] == ']':
            tokens.append(('brace_close', ']'))
            code = code[1:]
        elif code[0] in f'-{string.digits}':
            m = re.match(r'^-?\d+', code)
            tokens.append(('number', int(m.group(0)) % 256))
            code = code[m.span(0)[1]:]
        else:
            raise SyntaxError('cannot tokenize the code')
    return tokens


class State:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def advance(self):
        self.index += 1

    def peek(self, distance=0):
        if self.index + distance >= len(self.tokens):
            return ('instr_end', None)
        return self.tokens[self.index + distance]

    def is_eof(self):
        return self.index >= len(self.tokens)

    def next(self):
        self.advance()
        return self.peek(-1)

    def end_instr(self):
        if self.next() != ('instr_end', None):
            raise SyntaxError('end of instruction expected')


def parse(tokens):
    program = []
    state = State(tokens)
    while not state.is_eof():
        res = parse_statement(state)
        if res: program.append(res)

    return program


def parse_statement(state: State):
    while not state.is_eof() and state.peek()[0] == 'instr_end': state.advance()
    if state.is_eof(): return None

    instr = state.next()
    if instr[0] != 'id':
        raise SyntaxError('instruction expected')
    instr = instr[1]
    if instr == 'msg':
        args = []
        while True:
            arg = state.next()
            if arg == ('instr_end', None): break
            if arg[0] != 'id' and arg[0] != 'string':
                raise SyntaxError('msg instruction requires <id|string> as an argument\n  something else was given')
            args.append(arg)
        return ('msg', args)
    elif instr == 'var':
        vars = {}
        while state.peek()[0] == 'id':
            name = state.next()[1]
            size = 0
            if name in vars:
                raise NameError(f'variables with identifier "{name}" already exists')
            if state.peek() == ('brace_open', '['):
                state.advance()
                size = state.next()[1]
                if type(size) is not int:
                    raise TypeError('variable size must be a <number>')
                if state.next() != ('brace_close', ']'):
                    raise SyntaxError('closing bracket expected')
            vars[name] = size
        state.end_instr()
        return ('var', vars)
    elif instr == 'read':
        var = state.next()
        if var[0] != 'id':
            raise SyntaxError(f'{instr} instruction requires 1 argument: <id>>\n  something else was given')
        state.end_instr()
        return (instr, var)
    elif instr in ('set', 'inc', 'dec'):
        var = state.next()
        val = state.next()
        if var[0] != 'id' or val[0] not in ('number', 'id',):
            raise SyntaxError(f'{instr} instruction requires 2 arguments: <id> <number|id>\n  something else was given')
        state.end_instr()
        return (instr, (var, val))

    # generic parsing
    args = []
    while True:
        arg = state.next()
        if arg == ('instr_end', None): break
        args.append(arg)

    return (instr, args)


def prepare(icode):
    program = {
        'globals': [],
        'procedures': {},
        'instructions': [],
        'stack': ['<source>'],
    }

    # resolve procedures
    depth = 0
    current_proc = None
    procs = {}
    cicode = []
    for i in icode:
        if i[0] == 'proc':
            if current_proc is not None:
                raise SyntaxError('nested procedures are not permitted')
            if i[1][0] in procs:
                raise Exception('procedures cannot have duplicate names')
            if len(set(i[1][1:])) != len(i[1][1:]):
                raise Exception('procedure parameters cannot have duplicate names')
            current_proc = procs[i[1][0]] = { 'name': i[1][0][1], 'params': i[1][1:], 'code': [] }
            depth += 1
            continue

        if current_proc is None:
            cicode.append(i)
        elif i[0] == 'var':
            raise SyntaxError('variable declaration inside procedures is not allowed')
        elif i[0] != 'end' or depth > 1:
            current_proc['code'].append(i)

        if i[0] in ('ifeq', 'ifneq', 'wneq'):
            depth += 1
        elif i[0] == 'end':
            depth -= 1
            if depth == 0:
                current_proc = None
    program['procedures'] = procs
    icode = cicode

    vars = [(v, {'size': args[v] if args[v] else 1, 'is_list': args[v] > 0, 'offset': 0}) for i, args in icode if i == 'var' for v in args]
    if len(set(v[0] for v in vars)) != len(vars):
        raise Exception('variables cannot have duplicate names')
    program['globals'] = dict(vars)
    offset = 0
    for g in program['globals']:
        program['globals'][g]['offset'] = offset
        offset += program['globals'][g]['size']
    icode = [i for i in icode if i[0] != 'var']

    for i in icode:
        program['instructions'].append(i)

    return program


def get_var_offset(program_info, var):
    if var is None: return None
    # print('getting offset of:', var)
    # print(f"{program_info['wa_size']=};  {program_info['globals'][var[1]]['offset']*2=}")
    # print(f"{program_info['wa_size'] + 2 + program_info['globals'][var[1]]['offset']*2=}")
    return program_info['wa_size'] + 2 + program_info['globals'][var[1]]['offset']*2


def is_list(program_info, val):
    if val is None or val[0] == 'number':
        return False
    return program_info['globals'][val[1]]['is_list']


def decor_bf_make_block(f: FunctionType):
    def func(*args, **kwargs):
        return [f'% {f.__name__[3:]}'] + ['  ' + line for line in f(*args, **kwargs)]
    return func


@decor_bf_make_block
def bf_read(program_info, var):
    offset = get_var_offset(program_info, var)
    return ['>'*offset + ',' + '<'*offset]


@decor_bf_make_block
def bf_write(program_info, data):
    if data[0] == 'string': return bf_writes(program_info, data[1])
    return bf_writev(program_info, data)


@decor_bf_make_block
def bf_writec(program_info, c: str):
    return ['+'*ord(c) + '.' + '[-]']


@decor_bf_make_block
def bf_writes(program_info, msg: str):
    return sum([bf_writec(program_info, c) for c in msg], [])


@decor_bf_make_block
def bf_writev(program_info, var):
    if var[1] not in program_info['globals']:
        raise NameError(f'Variable "{var[1]}" is not defined')
    offset = get_var_offset(program_info, var)
    return ['>'*offset + '.' + '<'*offset]


@decor_bf_make_block
def bf_set(program_info, var, val):
    offset = get_var_offset(program_info, var)
    if val[0] == 'number':
        return ['>'*offset + '[-]' + '+'*val[1] + '<'*offset]
    return [
        *bf_loadc(program_info, val, cell=0),
        *bf_resetc(program_info, cell=offset),
        *bf_movec(program_info, src_cell=0, target_cell=offset)
    ]


@decor_bf_make_block
def bf_loadc(program_info, v, cell):
    if v[0] == 'number':
        return ['>'*cell + ('+'*v[1] if v[1] < 128 else '-'*(256-v[1])) + '<'*cell]

    offset = get_var_offset(program_info, v)
    return [
        '>'*offset + '[->+>>+<<<]>[-<+>]>>[-<<<' +
        '<'*(offset-cell) + '+' + '>'*(offset-cell) + '>>>]<<<' + '<'*offset
    ]


def bf_resetc(program_info, cell):
    if cell is None: return []
    return ['>'*cell + '[-]' + '<'*cell]


@decor_bf_make_block
def bf_movec(program_info, src_cell: int, target_cell):
    if target_cell is None: return bf_resetc(program_info, src_cell)
    assert type(target_cell) is int

    d = target_cell - src_cell
    return ['>' * src_cell + '[-' + '<>'[d>0]*abs(d) + '+' + '><'[d>0]*abs(d) + ']' + '<' * src_cell]


@decor_bf_make_block
def bf_generic_op(program_info, ins, outs, op: FunctionType):
    if any(is_list(program_info, a) for a in list(ins) + list(outs)):
        raise TypeError('generic operations do not work on lists')
    if any(o is not None and o[0] != 'id' for o in outs):
        raise SyntaxError('outputs must be variables')

    return [
        *sum([bf_loadc(program_info, i, cell=idx) for idx, i in enumerate(ins)], []),
        *op(),
        *sum([bf_resetc(program_info, get_var_offset(program_info, o)) for o in outs], []),
        *sum([bf_movec(program_info, src_cell=i, target_cell=get_var_offset(program_info, o)) for i, o in enumerate(outs)], []),
    ]


@decor_bf_make_block
def bf_builtin_add():
    return ['>[-<+>]<']


@decor_bf_make_block
def bf_builtin_sub():
    return ['>[-<->]<']


@decor_bf_make_block
def bf_builtin_mul():
    return ['[- >[->+>+<<]< >>>[-<<+>>]<<<]  >[-]<  >>[-<<+>>]<<']


@decor_bf_make_block
def bf_builtin_divmod():
    """
    Attribution: FSHelix
      in :  >n   d    0   0  0 0
      out:  >0 d-n%d n%d n/d 0 0
    """
    return ['[->[->+>>]>[<<+>>[-<+>]>+>>]<<<<<]', '>[>>>]>[[-<+>]>+>>]<<<<<']


@decor_bf_make_block
def bf_builtin_cmp():
    return [
        ' [->>>>>+>+<<<<<<]>>>>>>[-<<<<<<+>>>>>>]<<<<<<',   # copy first argument
        '>[->>>>>+>+<<<<<<]>>>>>>[-<<<<<<+>>>>>>]<<<<<<<',  # copy second argument
        '[->>+<[->-]>[<<[-]>>->]<<<]>[[-]<+>]<',            # compare A < B
        '[->>>>--<<<<]',                                    # -2 to R if A < B
        '>>>>>[->-<]>[[-]<<+>>]<<',                         # +1 from R if A != B
        '[-<<<<+>>>>]<<<<',                                 # move R to output cell (1st cell)
    ]


@decor_bf_make_block
def bf_builtin_a2b():
    return [
        '-'*48 + '[->>>' + '+'*100 + '<<<]' + '>',
        '-'*48 + '[->>' + '+'*10 + '<<]' + '>',
        '-'*48 + '[->' + '+'*1 + '<]' + '>',
        '[-<<<+>>>]<<<',
    ]


@decor_bf_make_block
def bf_builtin_b2a():
    return [                             #  1      2        3      4      5  6  7
        '>' + '+'*100 + '<',             # >n      100      0      0      0  0  0
        *bf_builtin_divmod(),            # >0      d-n%100  n%100  n/100  0  0  0
        '>>[-<<+>>]  >[->>>+<<<] <<<',   # >n%100  ?        0      0      0  0  n/100
        '>[-]' + '+'*10 + '<',           # >n%100  10       0      0      0  0  n/100
        *bf_builtin_divmod(),            # >0      d-n%10   n%10   n/10   0  0  n/100
        '>[-]>>>>>[-<<<<<<+>>>>>>]<<<',  #  n/100  0        n%10  >n/10   0  0  0
        '[-<<+>>]<<<',                   # >n/100  n/10     n%10   0      0  0  0
        '+'*48 + '>' + '+'*48 + '>' + '+'*48 + '<<'
    ]


@decor_bf_make_block
def bf_lget(program, args):
    if not is_list(program, args[0]):
        raise TypeError('lget expects an array as a 1st argument')
    if is_list(program, args[1]) or is_list(program, args[2]):
        raise TypeError('lget expects an array as a 2nd and 3rd arguments')

    return [
        *bf_loadc(program, args[1], cell=program['wa_size'] + 1),
        '>'*program['wa_size'],
        '>[->>+<<]<',
        '>>>' + '+'*program['globals'][args[0][1]]['offset'],
        '[-[->>+<<]+>>]',  # create trail of 1s to the right of each skipped array element
        '<[->+>>+<<<]',  # create duplicate values in trail-dedicated cells (since they are zeroed)
        '>[-<+>]',  # restore the value of the cell from the adjacent one
        '>>[- <<<<[<<] <+> >>[>>] >>]',  # move value from the holding cell to the memory cell
        '<<<<[-<<]<' + '<'*program['wa_size'],  # move cursor to the beginning of the tape
        *bf_resetc(program, get_var_offset(program, args[2])),
        *bf_movec(program, src_cell=program['wa_size'], target_cell=get_var_offset(program, args[2])),
    ]


@decor_bf_make_block
def bf_lset(program, args):
    if not is_list(program, args[0]):
        raise TypeError('lset expects an array as a 1st argument')
    if is_list(program, args[1]) or is_list(program, args[2]):
        raise TypeError('lset expects an array as a 2nd and 3rd arguments')

    return [
        *bf_loadc(program, args[2], cell=program['wa_size'] + 0),
        *bf_loadc(program, args[1], cell=program['wa_size'] + 1),
        '>'*program['wa_size'],
        '>[->>+<<]<',
        '>>>' + '+'*program['globals'][args[0][1]]['offset'],
        '[-[->>+<<]+>>]',  # create trail of 1s to the right of each skipped array element
        '<[-]>',  # clear the memory cell
        '<<[<<]',  # return to the beginning
        '<[-> >>[>>] <+> <<[<<] <]',  # move value from the holding cell to the memory cell
        '>>>[>>]<<[-<<]<' + '<'*program['wa_size'],  # clear the trail and return to the beginning of the tape
    ]


@decor_bf_make_block
def bf_proc(program, args):
    if args[0][1] in program['stack']:
        raise RecursionError('recursive calls are forbidden: [' + ', '.join(program['stack']) + '] to ' + args[0][1])

    proc = program['procedures'][args[0]]
    if len(args) - 1 != len(proc['params']):
        raise IndexError('procedure call arguments and parameters count mismatch')

    return compile({
        **program,
        'globals': {
            **program['globals'],
            **{p[1]: program['globals'][a[1]] for p, a in zip(proc['params'], args[1:])}},
        'instructions': proc['code'],
        'stack': program['stack'] + [args[0][1]],
    })


def compile(program):
    # pprint(program)
    code = []
    open_fcs = []

    for i, args in program['instructions']:
        if i == 'msg':
            for a in args:
                code += bf_write(program, a)
        elif i == 'set':
            code += bf_set(program, *args)
        elif i == 'inc':
            code += bf_generic_op(program, args[:2], [args[0]], op=bf_builtin_add)
        elif i == 'dec':
            code += bf_generic_op(program, args[:2], [args[0]], op=bf_builtin_sub)
        elif i == 'add':
            code += bf_generic_op(program, args[:2], [args[2]], op=bf_builtin_add)
        elif i == 'sub':
            code += bf_generic_op(program, args[:2], [args[2]], op=bf_builtin_sub)
        elif i == 'mul':
            code += bf_generic_op(program, args[:2], [args[2]], op=bf_builtin_mul)
        elif i == 'div':
            code += bf_generic_op(program, args[:2], [None, None, None, args[2]], op=bf_builtin_divmod)
        elif i == 'mod':
            code += bf_generic_op(program, args[:2], [None, None, args[2], None], op=bf_builtin_divmod)
        elif i == 'divmod':
            code += bf_generic_op(program, args[:2], [None, None, args[3], args[2]], op=bf_builtin_divmod)
        elif i == 'cmp':
            code += bf_generic_op(program, args[:2], [args[2]], op=bf_builtin_cmp)
        elif i == 'a2b':
            code += bf_generic_op(program, args[:3], args[3:], op=bf_builtin_a2b)
        elif i == 'b2a':
            code += bf_generic_op(program, args[:1], args[1:], op=bf_builtin_b2a)
        elif i == 'read':
            code += bf_read(program, args)
        elif i == 'lset':
            code += bf_lset(program, args)
        elif i == 'lget':
            code += bf_lget(program, args)
        elif i == 'call':
            code += bf_proc(program, args)
        elif i == 'wneq':
            open_fcs.append([
                *bf_loadc(program, args[0], cell=0),
                *bf_loadc(program, args[1], cell=1),
                '>[-<->]<',
            ])
            code += [
                *open_fcs[-1],
                '[[-]',
            ]
        elif i == 'ifneq':
            open_fcs.append([])
            code += [
                *bf_loadc(program, args[0], cell=0),
                *bf_loadc(program, args[1], cell=1),
                '>[-<->]<',
                '[[-]',
            ]
        elif i == 'ifeq':
            open_fcs.append([])
            code += [
                *bf_loadc(program, args[0], cell=0),
                *bf_loadc(program, args[1], cell=1),
                '[->-<]',
                '+>[[-]<->]<',
                '[[-]'
            ]
        elif i == 'end':
            code += [
                *open_fcs.pop(),
                ']',
            ]
        else:
            raise NameError(f'Unknown instruction "{i}"')

    return code


def kcuf(code):
    TIME_START = time()
    # print(code)
    tokens = tokenize(code)
    # print(tokens)
    TIME_TOKENIZE = time()
    icode = parse(tokens)
    TIME_PARSE = time()
    program = prepare(icode)
    TIME_PREPARE = time()
    program['wa_size'] = 8
    bf = '\n'.join(compile(program))
    TIME_COMPILE = time()
    print(f'elapsed {int((TIME_COMPILE - TIME_START)*1000*10)/10}ms total')
    print(f'  tokenize: {int((TIME_TOKENIZE - TIME_START)    * 1000 * 10) / 10}ms')
    print(f'  parse   : {int((TIME_PARSE    - TIME_TOKENIZE) * 1000 * 10) / 10}ms')
    print(f'  prepare : {int((TIME_PREPARE  - TIME_PARSE)    * 1000 * 10) / 10}ms')
    print(f'  compile : {int((TIME_COMPILE  - TIME_PREPARE)  * 1000 * 10) / 10}ms')
    return bf

  
##################################################################################
import re
from collections import defaultdict
from time import process_time


# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# It's a bad design, but this is not a long-term project.


class BrainfuckError(RuntimeError):
    """Any RuntimeError during Brainfuck transpiling."""


class Command:
    blocks = {'ifeq', 'ifneq', 'wneq', 'proc'}
    block_end = 'end'
    regular = {'var', 'set', 'inc', 'dec', 'add', 'sub', 'mul', 'divmod',
               'div', 'mod', 'cmp', 'a2b', 'b2a', 'lset', 'lget', 'call',
               'read', 'msg', 'rem'}
    all = regular | blocks | {block_end}
    args = {
        "var": "VarSingle+",
        "set": "VarName VarNameOrNumber",
        "inc": "VarName VarNameOrNumber",
        "dec": "VarName VarNameOrNumber",
        "add": "VarNameOrNumber VarNameOrNumber VarName",
        "sub": "VarNameOrNumber VarNameOrNumber VarName",
        "mul": "VarNameOrNumber VarNameOrNumber VarName",
        "divmod": "VarNameOrNumber VarNameOrNumber VarName VarName",
        "div": "VarNameOrNumber VarNameOrNumber VarName",
        "mod": "VarNameOrNumber VarNameOrNumber VarName",
        "cmp": "VarNameOrNumber VarNameOrNumber VarName",
        "a2b": "VarNameOrNumber VarNameOrNumber VarNameOrNumber VarName",
        "b2a": "VarNameOrNumber VarName VarName VarName",
        "lset": "ListName VarNameOrNumber VarNameOrNumber",
        "lget": "ListName VarNameOrNumber VarName",
        "ifeq": "VarName VarNameOrNumber",
        "ifneq": "VarName VarNameOrNumber",
        "wneq": "VarName VarNameOrNumber",
        "proc": "ProcedureName ProcedureParameter*",
        "end": "",
        "call": "ProcedureName ProcedureParameter*",
        "read": "VarName",
        "msg": "VarNameOrString+",
    }
    rgx = {"VarName": r"(?:[a-z_$][\w\$]*)"}
    rgx["ListName"] = rgx["VarName"]
    rgx["ProcedureName"] = rgx["VarName"]
    rgx["ProcedureParameter"] = rgx["VarName"]
    rgx["CharElement"] = r'(?:[^\'\"\\]|\\[\\\'\"nrt])'
    rgx["Char"] = r"(?:\'" + rgx["CharElement"] + r"\')"
    rgx["Number"] = r"(?:-?\d+|" + rgx["Char"] + r")"
    rgx["String"] = r'(?:\"(?:' + rgx["CharElement"] + r')*\")'
    rgx["CharOrString"] = (r"(?:" + rgx["Char"] + r"|"
                           + rgx["String"] + r")")
    rgx["VarSingle"] = (r"(?:(" + rgx["VarName"]    # Unnamed groups for multiple reinsertion
                        + r")(?:\s*\[\s*(" + rgx["Number"]
                        + r")\s*\])?)")
    rgx["VarNameOrNumber"] = (r"(?:" + rgx["VarName"] + r"|"
                              + rgx["Number"] + r")")
    rgx["VarNameOrString"] = (r"(?:" + rgx["VarName"] + r"|"
                              + rgx["String"] + r")")
    rgx["Argument"] = (r"(?:" + rgx["VarSingle"] + r"|"
                       + rgx["Number"] + r"|"
                       + rgx["String"] + r")")
    rgx["Comment"] = r"(?:\s*(?:\-\-|\/\/|\&\&|\#).*)"
    rgx["Line"] = (r"(?:\s*rem\b.*|\s*(?P<cmd>(?P<cmd_name>\w+)\s*"
                   + r"(?P<cmd_args>(?:(?:\s+|\b|(?=[\"']))"
                   + rgx["Argument"] + r")*))?" + rgx["Comment"] + r"?)")

    @staticmethod
    def define_cmd_rgx():
        for name, args in Command.args.items():
            Command.rgx[name] = r""
            for arg in args.split():
                Command.rgx[name] += r"(?:(?:(?:\s+|\b|(?=[\"']))"
                if arg[-1] in ('+', '*', '?'):
                    a_val, qty = arg[:-1], arg[-1]
                    Command.rgx[name] += Command.rgx[a_val] + r")" + qty + r")"
                else:
                    Command.rgx[name] += Command.rgx[arg] + r"))"

        for name, regex in Command.rgx.items():
            # print(f"rgx['{name}']:", repr(str(Command.rgx[name])))
            Command.rgx[name] = re.compile(regex, flags=re.IGNORECASE)

    # name: str
    # args: List[str]

    def __init__(self, name: str, args):  # args: List[str]
        self.name, self.args = name, args
        # print("New command:", name, args)

    @staticmethod
    def from_line(line: str):  # -> Optional[Command]
        # print("Line:", line)
        elts = re.fullmatch(Command.rgx["Line"], line)
        # print("Elements parsed!")
        if not elts:
            raise BrainfuckError(f"Can't parse line `{line}`.\n"
                                 + "Expected: [ Statement ] [ Comment ].\n"
                                 + f"Regex: `{Command.rgx['Line']}`.")
        if not elts['cmd']:  # No command on that line
            return None
        name = elts['cmd_name'].lower()
        args = [a[0] for a in
                re.finditer(Command.rgx["Argument"], elts['cmd_args'])]
        # print(f"Command is {name}({', '.join(args)})")
        if name not in Command.all:
            raise BrainfuckError(f"Can't parse line `{line}`.\n"
                                 + f"Invalid command name: `{name}`.\n"
                                 + f"Valid names are: `{Command.all}`.")
        try:
            # print(f"assert re.fullmatch({repr(Command.rgx[name])}, {repr(elts['cmd_args'])})")
            assert re.fullmatch(Command.rgx[name], elts['cmd_args'])
        except AssertionError as e:
            # print("Command.args:", Command.args)
            raise BrainfuckError(f"Can't parse line `{line}`.\n"
                                 + f"Invalid arguments: `{elts['cmd_args']}`.\n"
                                 + f"Expected: `{Command.args[name]}`.\n"
                                 + f"Regex: `{Command.rgx[name]}`.") from e
        for j, arg in enumerate(args):
            if not re.fullmatch(Command.rgx["CharOrString"], arg):
                args[j] = arg.lower()
        c = Command(name, args)
        # print("Command:", c)
        return c

    def __repr__(self) -> str:
        return f"{self.name} {', '.join(self.args)}"


Command.define_cmd_rgx()


class Transpiler:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods
    # It's a bad design, but this is not a long-term project.

    # ram: List[bool]
    # vars: Dict[str, int]
    # procs: Dict[str, Dict[str, str]]
    # callstack: List[int]
    # mem_idx: int
    # code_idx: int
    # code: List[Command]
    # bf: str
    MAX_CALLSTACK: int = 100

    def __init__(self):
        self.ram = []
        self.vars = {}
        self.known_vals = defaultdict(lambda: None)  # known vars value
        self.procs = {}
        self.blocks = []  # What to do when you meet "end"
        self.callstack = []  # What functions have been called, and args.
        self.vars_idx = 0
        self.mem_idx = 0
        self.code_idx = 0
        self.code = []
        self.bf = ""

    @staticmethod
    def is_ram(var: str):
        return var[0] == '#'
        # return re.fullmatch(r'#(?:0|[1-9]\d*)', var)

    @staticmethod
    def tokenize(code):
        # print("tokenize")
        # transform each line to a Command
        tokens = [Command.from_line(line) for line in code.split("\n")]
        # remove empty commands from blank or comment lines
        tokens = [tok for tok in tokens if tok is not None]
        # print("tokens:", *tokens, sep="\n")
        return tokens

    def def_procs(self):
        self.code_idx = 0
        while self.code_idx < len(self.code):
            cmd = self.code[self.code_idx]
            if cmd.name == "proc":
                p_name = cmd.args[0]
                if p_name in self.procs:
                    raise BrainfuckError(f"Proc `{p_name}` defined twice.\n"
                                         + f"At line {self.procs[p_name]}.\n"
                                         + f"And line {self.code_idx}.")
                self.procs[p_name] = self.code_idx
                # print(f"Defined proc `{p_name}` at line {self.code_idx}")
                self.proc(p_name, *cmd.args[1:], check=True)
            self.code_idx += 1
        self.code_idx = 0

    def deref(self, arg):
        """unroll references"""
        for references in reversed(self.callstack):  # Proc params refs
            if arg in references.keys():
                # print(f"dereferencing {arg} -> {references[arg]}")
                arg = references[arg]  # Follow param references
        return arg

    def set_mem(self, pos):
        """No default, None is a valid argument (unknown at compile time)"""
        # if pos is None don't use self.pos which defaults to self.mem_idx
        self.mem_idx = None if pos is None else self.pos(pos)
        # print(f"mem_idx={self.mem_idx}")

    def inc_mem(self, count=1):
        """increase known position by count"""
        if self.mem_idx is not None:
            self.mem_idx += count
            # print(f"mem_idx={self.mem_idx}")

    def dec_mem(self, count=1):
        """decrease known position by count"""
        self.inc_mem(-count)

    def jmp(self, code_idx):
        """Jump in the code (for procs mainly)"""
        self.code_idx = code_idx

    def pos(self, var=None) -> int:  # var: Optional[Union[str, int]]
        if var is None:  # Note: pos defaults to current mem_idx.
            return self.mem_idx
        if var in self.vars:  # variable
            if Transpiler.is_ram(var):  # RAM
                try:
                    assert self.ram[int(var[1:])] is True
                except AssertionError as e:
                    raise BrainfuckError(f"RAM {var} not allocated.") from e
            # print(f"pos({var}) => {self.vars[var]}")
            return self.vars[var]
        try:
            # print(f"WTF is going on? var = '{var}'")
            return int(var)
        except ValueError as e:
            raise BrainfuckError(f"Can't resolve var \"{var}\".") from e

    def checkpos(self, target, eql=True):
        tgt_pos = self.pos(target)
        if eql:
            try:
                assert self.mem_idx is not None and self.mem_idx == tgt_pos
            except AssertionError as e:
                raise BrainfuckError("Failed checkpos(eql)\n"
                                     + f"Expected pos: {target} ({tgt_pos})\n"
                                     + f"Actual: {self.mem_idx}.") from e
        else:
            try:
                assert self.mem_idx is None or self.mem_idx != tgt_pos
            except AssertionError as e:
                raise BrainfuckError("Failed checkpos(diff)\n"
                                     + f"Forbidden pos: {target} ({tgt_pos})."
                                     ) from e

    def exec(self, code):
        self.bf += code

    def bf_inc(self, count=1):
        """Increment current cell count times."""
        count %= 256
        if count <= 128:
            self.exec("+" * count)
        else:
            self.exec("-" * (256 - count))
        # TODO: increase known pos value by count

    def bf_dec(self, count=1):
        """Decrement current cell count times."""
        self.bf_inc(-count)

    def bf_right(self, count=1):
        """Move cell pointer right count times."""
        if count >= 0:
            self.exec(">" * count)
        else:
            self.exec("<" * -count)
        self.inc_mem(count)

    def bf_left(self, count=1):
        """Move cell pointer left count times."""
        self.bf_right(-count)

    def bf_read(self, count=1):
        """Read from stdin with ',' bf command"""
        self.exec("," * count)
        # TODO: set known pos value to None (unknown at compile time)

    def bf_write(self, count=1):
        """Write to stdout with '.' bf command"""
        self.exec("." * count)

    def bf_loop(self, unstable=False, stabilize=False):
        """
        Loop while current cell is not 0 with '[' bf command.
        End the loop with command "end".
        unstable: (<=> pos is unknown after the loop ends)
            - if False (default) the starting pos must be known and it will
        return to that pos at the end (end pos must also be known). Starting
        pos may only be known when the loop is entered. See stabilizing.
            - if True the loop must be started with unknown cell position or
        end on a different cell than it started. pos will be set to unknown
        when the loop ends.
            - if None nothing's checked or done, and pos won't be set.
        I can't think of any good reason to use that, but it may happen.
        stabilize:
            - if Falsy (default) ignore this param.
            - if Truthy the starting pos must be unknown, and will be set to
        this value upon entering the loop. The pos will be set to unknown again
        when the loop ends. Typical use is from unknown array index, stabilized
        at index 0 to interact with arrays of the same size.
        """
        # print(f"bf_loop(unstable={unstable}, stabilize={stabilize})")
        self.exec("[")
        end_instructions = ((self.exec, "]"),)
        if stabilize:
            try:
                assert self.mem_idx is None
            except AssertionError as e:
                raise BrainfuckError("Can't stabilize a loop called "
                                     "from stable pos.") from e
            if unstable is False:  # unstable loops always set mem_idx to None
                end_instructions = (
                    *end_instructions,
                    (self.set_mem, self.mem_idx))
            self.set_mem(stabilize)
        if unstable:
            cond_pos = self.mem_idx
            end_instructions = (
                (self.checkpos, cond_pos, False),  # assert loop is unstable
                (self.set_mem, None),  # Note: in THIS order
                *end_instructions)
            self.blocks.append(end_instructions)
        elif unstable is None:
            self.blocks.append(end_instructions)
        else:
            cond_pos = self.mem_idx
            try:
                assert cond_pos is not None
            except AssertionError as e:
                raise BrainfuckError("Safe loop started at pos=None.") from e
            end_instructions = (
                (self.goto, cond_pos),
                *end_instructions)
            self.blocks.append(end_instructions)

    def bf_while(self, pos=None, stabilize=None):
        """
        Like loop, but automatically return to pos before looping.
        Can't be unstable (use loop and come back manually in unstable context)
        Can be stabilized only at pos or if pos is None (<=> self.mem_idx)
        Note: destructive
        """
        if self.mem_idx is None:
            try:
                assert (stabilize is not None
                        and self.pos(pos) in (None, self.pos(stabilize)))
            except AssertionError as e:
                raise BrainfuckError("bf_while at unknown pos must be "
                                     + "stabilized and loop at stabilized pos."
                                     ) from e
        else:
            self.goto(pos)
        self.bf_loop(stabilize=stabilize)  # Note: stable loop

    def bf_if(self, pos=None, stabilize=None):
        """Note: destructive"""
        self.bf_while(pos, stabilize)
        for _ in range(1):  # indent while block
            self.reset(pos)  # note: ofc you should never alter pos inside
        # other way: reset pos when end is called, note: pos must be stored.
        # self.blocks[-1] = (     # note: that's pretty dirty (if pos is None)
        #     (self.reset, pos),  # reset pos to ensure leaving after one cycle
        #     *self.blocks[-1],   # before regular end commands
        # )                       # this would ensure pos is really O, but idk

    def bf_repeat(self, pos, stabilize=None):
        """Note: destructive"""
        self.bf_while(pos, stabilize)
        for _ in range(1):  # indent while block
            self.dec(pos, 1)  # note: ofc you should never alter pos inside

    def goto(self, label=None):
        pos = self.pos(label)
        # print(f"goto {label}: idx {pos}")
        if self.mem_idx is None:
            if pos is not None:
                raise BrainfuckError(f"goto {label} impossible: "
                                     + "unknown cell position.")
        else:
            if self.mem_idx < pos:
                self.bf_right(pos - self.mem_idx)
            else:
                self.bf_left(self.mem_idx - pos)

    def reset(self, *args):
        # print(f"reset {args}")
        for var in sorted(args, key=self.pos, reverse=True):
            self.goto(var)
            self.bf_loop()  # while var != 0
            for _ in range(1):  # indent loop block
                self.dec(var, 1)  # decrement var
            self.end()
            # self.set_val(var, 0)    # var is now 0

    def set_val(self, var, val):
        """Set a variable value. None if undefined."""
        self.known_vals[var] = val

    def val(self, src):
        """
        Evaluate literal or constant to its integer value.
        Return None if the value of a variable can't be determined.
        """
        if src in self.vars:
            return self.known_vals[src]
        try:
            assert re.fullmatch(Command.rgx["Char"], src)
        except (AssertionError, TypeError):
            try:
                return int(src) % 256
            except ValueError as e:
                raise BrainfuckError(f"Can't read value `{src}`.") from e
        else:
            if src[1] != '\\':  # regular char
                return ord(src[1])
            if src[2] == 'n':  # escape sequences
                return ord('\n')
            if src[2] == 'r':
                return ord('\r')
            if src[2] == 't':
                return ord('\t')
            return ord(src[2])  # escaped regular but significant (/, ', ")

    def move(self, src, *dsts, neg=False):
        """
        src cannot be part of dsts.
        if neg is False (default), add src to dsts.
        if neg is True, substract src to dsts.
        Note: move does not initially set dsts to 0.
        Use copy if that's what you want to do.
        Note: destructive (src is reset to 0)
        Use safe_move if you want to keep src value.
        """
        # print(f"move(src={src}, dsts={dsts}, neg='{neg}')")
        if src in dsts:
            raise BrainfuckError(f"Can't move cell {src} to itself.")
        if neg:  # negative move use decrement
            step_func = self.bf_dec
        else:  # positive move use increment
            step_func = self.bf_inc
        val = self.val(src)
        if val is not None:  # src is a literal
            # print(f"move(lit={val}, dsts={dsts}, neg='{neg}')")
            for dst in sorted(dsts, key=self.pos):  # Add literal val to dsts
                self.goto(dst)
                step_func(val)
        elif src in self.vars:  # src is a var to move
            self.bf_repeat(src)
            for _ in range(1):  # indent repeat block
                for pos in sorted(dsts, key=self.pos):
                    self.goto(pos)
                    step_func()
            self.end()
        else:
            raise BrainfuckError(f"Can't parse pos `{src}`")

    def safe_move(self, src, *dsts, neg=False):
        """
        Like move, but restore src at the end if it's a var.
        Note: src is actually restored through moving back and forth a tmp.
        """
        # print(f"safe_move(src={src}, dsts={dsts}, neg='{neg}')")
        if dsts:
            if src in self.vars:
                tmp = self.get_ram()
                self.reset(tmp)
                self.move(src, tmp, *dsts, neg=neg)
                self.move(tmp, src, neg=neg)
                self.free_ram(tmp)
            else:
                self.move(src, *dsts, neg=neg)

    def get_ram(self):
        """
        Find or create a non allocated slot of ram. Allocate and return it.
        Note: value of returned ram slots is NOT certified to be 0.
        """
        try:
            idx = self.ram.index(False)
        except ValueError:
            idx = len(self.ram)
            pos = -len(self.ram) - 1
            var = f'#{idx}'
            self.vars[var] = pos
            self.ram.append(True)
        else:
            var = f'#{idx}'
            self.ram[idx] = True
        # print(f"get_ram() => {var}")
        return var

    def get_ram_range(self, size):
        """
        Find or create a non allocated continuous space of ram of size `size`.
        set its value to 0, then return it.
        Note: First index is left, and last index is right. But since ram goes
        the other way around, the first index has a bigger name than the last.
        Note: value of returned ram slots is NOT certified to be 0.
        """
        i = 0
        found = False
        while i + size <= len(self.ram):
            found = True
            for j in range(i + size - 1, i - 1, -1):
                if self.ram[j]:
                    found = False
                    break
            if found:
                break
            i = j + 1
        if not found:  # add needed slots at the end.
            try:
                # i = index after last True
                i = len(self.ram) - self.ram[::-1].index(True)
            except ValueError:  # No True value
                i = 0
            for idx in range(len(self.ram), i + size):  # Add necessary slots
                self.ram.append(True)
                pos = -idx - 1
                var = f'#{idx}'
                self.vars[var] = pos
        res = []
        for idx in range(i + size - 1, i - 1, -1):
            self.ram[idx] = True  # Allocate slots
            var = f'#{idx}'
            self.reset(var)  # Set slots to 0
            res.append(var)  # res goes left to right
        # print(f"get_ram_range({size}) => {res}")
        return res

    def free_ram(self, *rams):
        """
        Deallocate slots of ram passed as args. After this call,
        these slots' memory is undefined and they must not be used.
        """
        # print(f"free_ram({rams})")
        for ram in rams:
            try:
                assert Transpiler.is_ram(ram)
            except AssertionError as e:
                raise BrainfuckError(f"Error freeing ram `{ram}`: "
                                     + "Invalid name.") from e
            try:
                assert ram in self.vars
            except AssertionError as e:
                raise BrainfuckError(f"Error freeing ram `{ram}`: "
                                     + "does not exist.") from e
            ram_idx = int(ram[1:])
            try:
                assert self.ram[ram_idx] is True
            except AssertionError as e:
                raise BrainfuckError(f"Error freeing ram `{ram}`: "
                                     + "not in use.") from e
            self.ram[ram_idx] = False

    def copy(self, src, *dsts):
        """
        Copy src to dsts - using a temporary ram slot.
        Ignore src in dsts (its value is kept, avoiding infinite loops).
        """
        # print(f"copy(src={src}, dsts={dsts})")
        dsts = [dst for dst in dsts if dst != src]  # remove src from dsts
        if not dsts:  # If there is no target
            return  # Let's stop and do nothing
        self.reset(*dsts)
        self.safe_move(src, *dsts)

    def set(self, dst, src):
        self.copy(src, dst)

    def check_var_name(self, name):
        if name in self.vars or f"{name}[0]" in self.vars:
            raise BrainfuckError(f"Var `{name}` defined twice.")

    def decl(self, name):
        # print(f"decl({name})")
        self.check_var_name(name)
        self.vars[name] = self.vars_idx
        self.vars_idx += 1
        # print(f"vars are now: {list(self.vars.keys())})")

    def decl_arr(self, name, size):
        """
        For an array "a" of size n,
        we simply declare regular variables "a[0]" through "a[n-1]"
        """
        self.check_var_name(name)
        size = self.val(size)
        for i in range(size):
            self.vars[f"{name}[{i}]"] = self.vars_idx + i
        self.vars_idx += size

    def var(self, *args):
        # print(f"var({args})")
        for arg in args:
            var_match = re.fullmatch(Command.rgx["VarSingle"], arg)
            # print(f"arg {arg} is var: {var_match} ({var_match[0]})")
            name, size = var_match.groups()
            if size is not None:
                self.decl_arr(name, size)
            else:
                self.decl(name)

    def inc(self, dst, src):
        # print(f"inc(dst={dst}, src={src})")
        self.safe_move(src, dst)

    def dec(self, dst, src):
        # print(f"dec(dst={dst}, src={src})")
        self.safe_move(src, dst, neg=True)

    def add(self, val1, val2, dst, neg=False):
        """
        add a b c. Add a and b then store the result into c.
        Equivalent to C : c = a + b. Examples : add 10 X Y, add X Y X
        val2_step defines what to do with
        """
        # print(f"add(val1={val1}, val2={val2}, dst={dst}, neg={neg})")
        is_res_tmp = dst == val2
        if is_res_tmp:  # overlapping, use tmp res.
            res = self.get_ram()
        else:  # No overlapping, use dst as res directly.
            res = dst
        self.copy(val1, res)
        self.safe_move(val2, res, neg=neg)
        if is_res_tmp:
            self.reset(dst)  # Not exactly a copy
            self.move(res, dst)  # We can afford to destroy res
            self.free_ram(res)

    def sub(self, val1, val2, dst):
        # print(f"sub(val1={val1}, val2={val2}, dst={dst})")
        self.add(val1, val2, dst, neg=True)

    def mul(self, val1, val2, dst):
        is_res_tmp = dst == val2
        if is_res_tmp:
            res = self.get_ram()
        else:
            res = dst
        tmp = self.get_ram()
        self.copy(val1, tmp)
        self.reset(res)
        self.bf_repeat(tmp)  # val1 times
        for _ in range(1):  # indent repeat content
            self.inc(res, val2)  # add val2 to res
        self.end()
        self.free_ram(tmp)
        if is_res_tmp:
            self.reset(dst)
            self.move(res, dst)
            self.free_ram(res)

    def divmod(self, val1, val2, dst_div, dst_mod):
        """
        Divmod a b c d. Divide a and b then store the quotient into c and the
        remainder into d. Equivalent to C : c = floor(a / b), d = a % b.
        Examples : divmod 20 10 X Y, divmod X Y X Y, divmod X 10 Y X.
        """
        # print(f"divmod(v1={val1}, v2={val2}, div={dst_div}, mod={dst_mod})")
        if dst_div == dst_mod:
            raise BrainfuckError("dst_div and dst_mod mustn't overlap!")
        # res_div is dst_div if not overlapping, tmp otherwise
        is_div_tmp = dst_div in (val1, val2)
        if is_div_tmp:
            res_div = self.get_ram()
        else:
            res_div = dst_div
        self.reset(res_div)
        # res_mod is dst_mod if not overlapping, tmp otherwise
        is_mod_tmp = dst_mod == val2
        if is_mod_tmp:
            res_mod = self.get_ram()
        else:
            res_mod = dst_mod
        tmp_cmp = self.get_ram()
        self.copy(val1, res_mod)
        self.cmp(res_mod, val2, tmp_cmp)  # cmp 1/0/-1
        self.wneq(tmp_cmp, -1)
        for _ in range(1):  # indent wneq content
            self.dec(res_mod, val2)
            self.inc(res_div, 1)
            self.cmp(res_mod, val2, tmp_cmp)  # cmp 1/0/-1
        self.end()
        self.free_ram(tmp_cmp)
        if is_div_tmp:
            self.reset(dst_div)
            self.move(res_div, dst_div)
            self.free_ram(res_div)
        if is_mod_tmp:
            self.reset(dst_mod)
            self.move(res_mod, dst_mod)
            self.free_ram(res_mod)

    def div(self, val1, val2, dst):
        tmp = self.get_ram()
        self.divmod(val1, val2, dst_div=dst, dst_mod=tmp)
        self.free_ram(tmp)

    def mod(self, val1, val2, dst):
        tmp = self.get_ram()
        self.divmod(val1, val2, dst_div=tmp, dst_mod=dst)
        self.free_ram(tmp)

    def cmp(self, val1, val2, dst):
        """
        Set dst to:
        1   if val1 > val2
        0   if val1 == val2
        -1  if val1 < val2
        """
        # Inspired by https://stackoverflow.com/questions/6168584/brainfuck-compare-2-numbers-as-greater-than-or-less-than
        # print(f"cmp(val1={val1}, val2={val2}, dst={dst})")
        tmp_arr = self.get_ram_range(6)
        self.reset(*tmp_arr)
        self.safe_move(1, tmp_arr[1])  # Condition entry at index 1
        self.safe_move(val2, tmp_arr[4])  # val2 (b) at idx 4
        self.safe_move(val1, tmp_arr[3])  # val1 (a) at idx 3
        self.reset(dst)  # Note: dst could be val1 or val2
        self.goto(tmp_arr[4])  # start at idx 4 (b)
        self.bf_loop(unstable=True)  # if b > 0
        for _ in range(1):  # indent loop block
            self.bf_right()  # goto idx 5 (0)
        self.end()  # 2 possibilities:
        self.bf_left(2)  # b == 0 idx 2 (0), b > 0 idx 3 (a)
        self.bf_loop(unstable=True)  # enter if b > 0 (at idx 3)
        for _ in range(1):  # indent loop content
            self.set_mem(tmp_arr[3])  # cell is no longer ubiquitous
            self.dec(tmp_arr[3], 1)  # decrement idx 3 (a)
            self.dec(tmp_arr[4], 1)  # decrement idx 4 (b)
            self.bf_loop(unstable=True)  # if b > 0
            for _ in range(1):  # indent loop block
                self.bf_right()  # goto idx 5 (0)
            self.end()  # 2 possibilities: note (a) is dec
            self.bf_left(2)  # b == 0 idx 2 (0), b > 0 idx 3 (a)
        self.end()  # b <= a idx 2 (0), a < b idx 3 (0)
        self.bf_left()  # b <= a idx 1 (1), a < b idx 2 (0)
        self.bf_if(stabilize=tmp_arr[1])  # loop only if b <= a idx 1 (1)
        for _ in range(1):  # indent bf_if block
            self.set_mem(tmp_arr[1])  # mem_idx is determined in the loop
            self.bf_if(tmp_arr[3])  # goto idx 3 (a) nonzero if b < a
            for _ in range(1):  # indent while content
                self.inc(tmp_arr[5], 1)  # b < a => res = +1
            self.end()  # nonzero if b < a
            self.goto(tmp_arr[1])  # back to the start to end
        self.end()  # end b <= a, pos unknown around.
        self.bf_left()  # b == 0 idx 1 (0), b > 0 idx 2 (1)
        # print(f"b == 0 idx 1 (0), b > 0 idx 2 (1): {self.mem_idx}")
        self.bf_loop(unstable=True, stabilize=tmp_arr[1])  # loop if a < b
        for _ in range(1):  # indent loop block
            self.dec(tmp_arr[1], 1)  # idx 1 (0)
            self.dec(tmp_arr[5], 1)  # a < b => set (ans) to -1
            self.goto(tmp_arr[0])  # end at idx 0 and fix pos.
        self.end()
        self.set_mem(tmp_arr[0])  # Now position is fixed. (useless line)
        self.move(tmp_arr[5], dst)  # move idx 5 (ans) to dst
        self.free_ram(*tmp_arr)

    def a2b(self, val1, val2, val3, dst):
        """
        ASCII To Byte.
        Treat a, b and c as ASCII digits and store the number represents those
        digits into d.
        Equivalent to C : d = 100 * (a - 48) + 10 * (b - 48) + (c - 48)
        Examples : a2b '1' '5' '9' X, a2b '0' X Y X
        """
        is_res_tmp = dst in (val2, val3)
        if is_res_tmp:
            res = self.get_ram()
        else:
            res = dst
        tmp = self.get_ram()
        self.sub(val1, "'0'", tmp)  # "'0'" = ord('0') = 48
        self.mul(tmp, 100, res)  # res = 100 * (a - '0')
        self.sub(val2, "'0'", tmp)
        self.mul(tmp, 10, tmp)
        self.inc(res, tmp)  # res += 10 * (b - '0')
        self.sub(val3, "'0'", tmp)
        self.inc(res, tmp)  # res += c - '0'
        self.free_ram(tmp)
        if is_res_tmp:
            self.reset(dst)
            self.move(res, dst)
            self.free_ram(res)

    def b2a(self, val, dst1, dst2, dst3):
        """
        Byte To ASCII. The reverse operation of a2b. Equivalent to C :
        b = 48 + floor(a / 100), c = 48 + floor(a / 10 % 10), d = 48 + (a % 10)
        Examples : b2a 159 X Y Z, b2a 'z' X Y Z, b2a X X Y Z
        """
        tmp = self.get_ram()
        self.divmod(val, 10, dst_div=tmp, dst_mod=dst3)
        self.inc(dst3, "'0'")  # dst3 is out of the loop to avoid copying.
        for dst in (dst2, dst1):
            self.divmod(tmp, 10, dst_div=tmp, dst_mod=dst)
            self.inc(dst, "'0'")
        self.free_ram(tmp)

    def lsize(self, lname):
        i = 0
        while f"{lname}[{i}]" in self.vars:
            i += 1
        if i < 1:
            raise BrainfuckError(f"{lname} is not an array.")
        return i

    def in_list(self, lname, pos):
        """
        Well this might become useful, but only when all resolvable values are
        handled from the compiler. If a literal gets in here I crash. Simple.
        """
        size = self.lsize(lname)
        lpos = self.pos(f"{lname}[0]")
        return lpos <= self.pos(pos) < lpos + size

    def ltmp_to_idx(self, tmp_arr, ldist=0):
        """
        Go to first index of val (0) in offset of tmp_arr,
        see ltmp for tmp_arrr definition. We call that unknown offset "i".
        ldist: You may provide the distance from the offset to the array,
               then the block will take you to the ith element of the array.
        """
        self.goto(tmp_arr[1])   # 1st offset cell, tmp_arr[0] is a left bound
        self.bf_loop(unstable=True)  # goto offset[i]
        for _ in range(1):  # indent loop block
            self.bf_right()  # go right until (0)
        self.end()  # pos is now offset[i] (unstable)
        self.bf_right(ldist)  # now at lname[i]

    def ltmp_from_idx(self, tmp_arr, ldist=0):
        """
        Come back from first index of val (0) in offset of tmp_arr,
        see ltmp for tmp_arrr definition. We call that unknown offset "i".
        end at position bound (tmp_arr[0]).
        ldist: You may provide the distance from the offset to the array,
               then the block will take you back from the ith elt of the array.
        """
        bound = tmp_arr[0]
        self.bf_left(ldist + 1)  # go back to last (1) or bound
        self.bf_loop(unstable=True)
        for _ in range(1):  # indent loop block
            self.bf_left()  # go back until val (0)
        self.end()  # which is by construction bound
        self.set_mem(bound)  # now pos is back at bound

    def ltmp(self, lname, idx):  # -> List[str]
        """
        Transform a value to an offset array
        tmp array is structured as follow:
        bound(0) | offset
        offset is an array with idx-1 cells (1) followed by at least 1 cell (0)
        It's meant to be used with ltmp_to_idx and ltmp_from_idx to reach lname
        offset is the same size as lname to be able to reach any given index.
        """
        tmp_arr = self.get_ram_range(self.lsize(lname) + 1)
        tmp_x = self.get_ram()
        self.copy(idx, tmp_x)
        self.reset(*tmp_arr)
        self.bf_repeat(tmp_x)
        for _ in range(1):  # indent ltmp_loop block
            self.ltmp_to_idx(tmp_arr)  # go to ith index
            self.bf_inc()  # set it to 1 (i += 1)
            self.ltmp_from_idx(tmp_arr)  # come back
        self.end()
        self.free_ram(tmp_x)
        return tmp_arr

    def lset(self, lname, idx, val):
        # Problem, this only works for literals
        # self.set(dst=f"{lname}[{idx}]", src=val)
        tmp_val = self.get_ram()
        tmp_arr = self.ltmp(lname, idx)  # Note: idx could be lname[idx]
        self.copy(val, tmp_val)  # Note: val could be lname[idx]
        offset = tmp_arr[1:]
        ldist = self.pos(f"{lname}[0]") - self.pos(offset[0])  # dist idx -> l
        self.ltmp_to_idx(tmp_arr, ldist=ldist)  # goto lname[idx]
        self.reset()  # reset lname[idx]
        self.ltmp_from_idx(tmp_arr, ldist=ldist)  # come back to tmp_arr[0]
        self.bf_repeat(tmp_val)
        for _ in range(1):  # indent repeat block
            self.ltmp_to_idx(tmp_arr, ldist=ldist)  # goto lname[i]
            self.bf_inc()  # move tmp_val to lname[idx]
            self.ltmp_from_idx(tmp_arr, ldist=ldist)  # back to known pos
        self.end()
        self.free_ram(tmp_val, *tmp_arr)

    def lget(self, lname, idx, dst):
        # Problem, this only works for literals
        # self.set(dst=val, src=f"{lname}[{idx}]")
        tmp = self.get_ram()
        tmp_dst = self.get_ram()  # Can't test dst == lname[idx], so use tmp
        tmp_arr = self.ltmp(lname, idx)  # Note: idx could be lname[idx]
        self.reset(tmp, tmp_dst)
        offset = tmp_arr[1:]
        ldist = self.pos(f"{lname}[0]") - self.pos(offset[0])  # dist idx -> l
        self.ltmp_to_idx(tmp_arr, ldist=ldist)  # goto lname[i] (unstable)
        self.bf_loop(unstable=True)
        for _ in range(1):  # indent loop block
            self.bf_dec()  # move lname[i]
            self.ltmp_from_idx(tmp_arr, ldist=ldist)  # goto bound (stable)
            self.move(1, tmp, tmp_dst)  # to tmp et tmp_dst
            self.ltmp_to_idx(tmp_arr, ldist=ldist)  # goto lname[i] (unstable)
        self.end()
        self.ltmp_from_idx(tmp_arr, ldist=ldist)  # goto bound (stable)
        self.bf_repeat(tmp)  # move tmp to lname[idx]
        for _ in range(1):  # indent repeat block
            self.ltmp_to_idx(tmp_arr, ldist=ldist)  # goto lname[i] (unstable)
            self.bf_inc()
            self.ltmp_from_idx(tmp_arr, ldist=ldist)  # goto bound (stable)
        self.end()
        self.reset(dst)
        self.move(tmp_dst, dst)
        self.free_ram(tmp, tmp_dst, *tmp_arr)

    def ifneq(self, a, b):
        tmp_cond = self.get_ram()
        self.sub(a, b, tmp_cond)
        self.goto(tmp_cond)
        self.exec('[')
        # What to do when this ends?
        self.blocks.append((
            (self.reset, tmp_cond),
            (self.goto, tmp_cond),
            (self.exec, ']'),
            (self.free_ram, tmp_cond)))

    def ifeq(self, a, b):
        tmp_cond = self.get_ram()
        self.copy(1, tmp_cond)  # cond (true)
        self.ifneq(a, b)  # if a != b
        for _ in range(1):
            self.reset(tmp_cond)  # cond (false)
        self.end()
        self.goto(tmp_cond)
        self.exec('[')
        # What to do when this ends?
        self.blocks.append((
            (self.reset, tmp_cond),
            (self.goto, tmp_cond),
            (self.exec, ']'),
            (self.free_ram, tmp_cond)))

    def wneq(self, a, b):
        tmp_cond = self.get_ram()
        self.sub(a, b, tmp_cond)
        self.goto(tmp_cond)
        self.exec('[')
        # What to do when this ends?
        self.blocks.append((
            (self.sub, a, b, tmp_cond),
            (self.goto, tmp_cond),
            (self.exec, ']'),
            (self.free_ram, tmp_cond)))

    def proc(self, name, *params, check=False):
        if check and len(params) > len(set(params)):
            raise BrainfuckError(f"Duplicate param in proc `{name}`: {params}")
        line = self.code_idx
        depth = 1
        while depth > 0:
            self.code_idx += 1
            try:
                cur_cmd = self.code[self.code_idx]
            except IndexError as e:
                self.jmp(line)  # Go back for stacktrace
                raise BrainfuckError("Expected end of block. "
                                     + "Instead found EOF.") from e
            if check:
                if cur_cmd.name == "proc":
                    raise BrainfuckError("Nested procs declaration.")
                if cur_cmd.name == "var":
                    raise BrainfuckError("Var declared in proc.")
            if cur_cmd.name in Command.blocks:
                depth += 1
            if cur_cmd.name == Command.block_end:
                depth -= 1
            # print(f"depth {depth}, line {self.code_idx}: {self.code[self.code_idx]}")

    def call(self, name, *args):
        # print(f"call(name={name}, args={args})")
        if name not in self.procs:
            raise BrainfuckError(f"Proc `{name}` undefined.")
        line = self.procs[name]
        # Note: This version accepts recursion atm, this might be forbidden.
        # if any(call_line == line for call_line, call_args in self.callstack):
        #     raise BrainfuckError(f"Proc `{name}` called recursively.")
        params = self.code[line].args[1:]
        if len(params) != len(args):
            raise BrainfuckError(f"Proc `{name}` wrong arguments count.\n"
                                 + f"Expected {len(params)}: {params}.\n"
                                 + f"Actual {len(args)}: {args}")
        # Set params references
        # print(f'Adding refs: { {p: val for p, val in zip(params, args)}}')
        self.callstack.append({p: val for p, val in zip(params, args)})
        if len(self.callstack) > Transpiler.MAX_CALLSTACK:
            raise BrainfuckError("Recursion too deep "
                                 + f"(lim={Transpiler.MAX_CALLSTACK})")
        # print("callstack", self.callstack)
        self.blocks.append((  # prepare end before starting (idx)
            # (print, f'Removing refs: {self.callstack[-1]}'),
            (self.callstack.pop,),  # remove param references
            (self.jmp, self.code_idx)))  # come back to calling line.
        self.jmp(self.procs[name])  # start proc

    def end(self):
        # print("end block")
        try:
            instructions = self.blocks.pop()
        except IndexError as e:
            raise BrainfuckError("Extra end instruction.") from e
        for method, *args in instructions:
            method(*args)

    def read(self, var):
        self.goto(var)
        self.exec(',')

    def msg_var(self, var=None):
        self.goto(var)
        self.exec(".")

    def msg_lit(self, lit):
        tmp = self.get_ram()
        if re.fullmatch(Command.rgx["String"], lit):  # string
            for letter in re.finditer(Command.rgx["CharElement"], lit):
                self.copy(f"\'{letter[0]}\'", tmp)  # actual rgx["Char"]
                self.goto(tmp)
                self.exec('.')
        else:  # Should be a value
            self.copy(lit, tmp)
            self.goto(tmp)
            self.exec('.')
        self.free_ram(tmp)

    def msg(self, *args):
        for arg in args:
            if arg in self.vars:
                self.msg_var(arg)
            else:
                self.msg_lit(arg)

    def rem(self, *args):
        pass

    def transpile(self, code):
        self.code = Transpiler.tokenize(code)
        self.def_procs()
        self.bf = ""
        try:
            self.run()
        except BrainfuckError as e:
            raise RuntimeError("Brainfuck transpilation failed.\n"
                               + self.stacktrace()) from e
        self.bf = "init: " + ">" * len(self.ram) + self.bf  # Start at pos 0
        return self.bf

    def run(self):
        while self.code_idx < len(self.code):
            cmd = self.code[self.code_idx]
            # print(f"Running line {self.code_idx + 1}:  `{cmd}`")
            if cmd.name not in Command.all:
                raise BrainfuckError(f"Unknown command: \"{cmd.name}\".")
            # Comment & Breakpoint for interpreter.
            self.exec(f"\n#{cmd.name} {' '.join(cmd.args)}: ".translate(
                str.maketrans("<>[]+-,.",
                              "{}()^~?*")))
            getattr(self, cmd.name)(*(self.deref(arg) for arg in cmd.args))
            # if any(self.ram):
            #     raise BrainfuckError("RAM leaked.\n"
            #                          + f"{dict(enumerate(self.ram))}.")
            self.code_idx += 1
        if self.blocks:
            raise BrainfuckError("Reached EOF in a block.")

    def stacktrace(self) -> str:
        msg = f"At line {self.code_idx + 1}: "
        if 0 <= self.code_idx < len(self.code):
            msg += f"`{self.code[self.code_idx]}`"
        msg += f"\nMem Cell {self.mem_idx}"
        if self.callstack:
            msg += "\n"
            msg += "\n".join(f"In block line {idx + 1}: `{self.code[idx]}`"
                             for idx in range(len(self.callstack) - 1, -1, -1))
        return msg


def kcuf(code):
    time_st = process_time()
    transpiler = Transpiler()
    code = transpiler.transpile(code)
    time_end = process_time()
    # print(f"BF:\n{code}", flush=True)
    print(f"Execution time:\t{round(time_end - time_st, 4)}", flush=True)
    return code


kcuf.i = 0

# define_cmd_rgx()

# If printing the code is annoying or a waste of your bandwidth
# (~220 KB for final test).
# Please uncomment the following line.
NOPRINT = True

##################################################
import re


WHITESPACE_REGEX = r'(?P<whitespace>\s+)'
COMMENT_REGEX = r'(?P<comment>(?://|--|#|rem).*)'
CHAR_REGEX = r'(?P<char>\'(?:[^\'"\\]|\\\\|\\\'|\\\"|\\n|\\r|\\t)\')'
BRACKET_LEFT_REGEX = r'(?P<bracket_left>\[)'
BRACKET_RIGHT_REGEX = r'(?P<bracket_right>\])'
KEYWORD_REGEX = r'(?P<keyword>var|set|inc|dec|add|sub|mul|divmod|div|mod|cmp|a2b|b2a|lset|lget|ifeq|ifneq|wneq|proc|end|call|read|msg)'
STRING_REGEX = r'(?P<string>"(?:[^\'"\\]|\\\\|\\\'|\\\"|\\n|\\r|\\t)*")'
NUMBER_REGEX = r'(?P<number>-?[0-9]+)'
IDENTIFIER_REGEX = r'(?P<identifier>[$_a-zA-Z][$_a-zA-Z0-9]*)'

CODE_REGEX = re.compile(
    r'|'.join([WHITESPACE_REGEX, COMMENT_REGEX, KEYWORD_REGEX,
               CHAR_REGEX, STRING_REGEX, NUMBER_REGEX,
               IDENTIFIER_REGEX, BRACKET_LEFT_REGEX, BRACKET_RIGHT_REGEX]),
    re.IGNORECASE
)


def error(line_no=None, keyword=None, message=''):
    if keyword is not None:
        message = f'{keyword}: {message}'
    if line_no is not None:
        message = f'{line_no}: {message}'
    raise SyntaxError(message)


def lex(code):
    tokens = []

    for line_no, line in enumerate(code.splitlines()):
        token_line = []
        tokens.append(token_line)

        pos = 0
        for match in CODE_REGEX.finditer(line):
            if match is None:
                error(line_no, 'lexer', f'col {pos}: ur program dont even lex')

            start, end = match.span()
            if start != pos:
                error(line_no, 'lexer', f'col {pos}: ur program dont even lex')
            pos = end

            matched = match.groupdict().items()
            (token_type, token_str), = [
                (t, s) for (t, s) in matched if s is not None]

            if token_type in {'whitespace', 'comment'}:
                continue

            if token_type in {'identifier', 'keyword'}:
                token_str = token_str.lower()

            if token_type == 'char':
                token_type = 'number'
                token_str = ord(eval(token_str))

            if token_type == 'number':
                token_str = int(token_str) % 256

            token_line.append((token_str, token_type))

    return tokens


def lower(tokens):
    """Lowers [(token_str, token_type)] into untyped [(op, *args)].

    Lowering rules:
        var x y z[100] -> var x; var y; varlist z 100
    """
    procs = {}
    proc = None

    variables = []
    arrays = {}

    frame = []
    stack = []

    for line_no, line in enumerate(tokens):
        if not line:
            continue

        (op, op_type), *args = line

        if op_type != 'keyword':
            error(line_no, 'parser', f'unexpected {op_type} at start of line')

        if op != 'var':
            for i, (arg, arg_type) in enumerate(args):
                if arg_type == 'identifier':
                    if op in {'lset', 'lget'} and i == 0:
                        if arg not in arrays:
                            error(line_no, op, f'array {arg!r} not defined')
                    elif op == 'proc':
                        pass
                    elif op in 'call' and i == 0:
                        pass
                    else:
                        if arg not in variables:
                            error(line_no, op, f'variable {arg!r} not defined')

        # int ...args
        if op == 'var':
            if proc is not None:
                error(line_no, op, f'encountered in procedure {proc!r}')

            expect = {'identifier'}
            for arg, arg_type in args:
                if arg_type not in expect:
                    error(line_no, op, f'expected {expect}, got {arg_type}')
                if arg_type == 'identifier':
                    if arg in variables:
                        error(line_no, op, f'{arg!r} already defined')
                    variables.append(arg)
                    expect = {'identifier', 'bracket_left'}
                elif arg_type == 'bracket_left':
                    expect = {'number'}
                elif arg_type == 'bracket_right':
                    expect = {'identifier'}
                elif arg_type == 'number':
                    arrays[variables.pop()] = arg
                    expect = {'bracket_right'}

            if arg_type not in {'bracket_right', 'identifier'}:
                error(line_no, op, 'unexpected end of variable list')

        # x = y
        elif op == 'set':
            if len(args) != 2:
                error(line_no, op, 'expected 2 args')

            (x, xt), (y, yt) = args
            if xt != 'identifier':
                error(line_no, op, f'unexpected assignment to {xt}')

            frame.append(('set', x, y))

        # x += y
        elif op == 'inc':
            if len(args) != 2:
                error(line_no, op, 'expected 2 args')

            (x, xt), (y, yt) = args
            if xt != 'identifier':
                error(line_no, op, f'unexpected assignment to {xt}')

            frame.append(('add', x, y))

        # x -= y
        elif op == 'dec':
            if len(args) != 2:
                error(line_no, op, 'expected 2 args')

            (x, xt), (y, yt) = args
            if xt != 'identifier':
                error(line_no, op, f'unexpected assignment to {xt}')

            frame.append(('sub', x, y))

        # z = x + y
        elif op == 'add':
            if len(args) != 3:
                error(line_no, op, 'expected 3 args')

            (x, xt), (y, yt), (z, zt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected:
                error(line_no, op, f'unexpected operand types {xt} and {yt}')
            if zt != 'identifier':
                error(line_no, op, f'unexpected assignment to {zt}')

            frame.append(('set', z, x))
            frame.append(('add', z, y))

        # z = x - y
        elif op == 'sub':
            if len(args) != 3:
                error(line_no, op, 'expected 3 args')

            (x, xt), (y, yt), (z, zt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected:
                error(line_no, op, f'unexpected operand types {xt} and {yt}')
            if zt != 'identifier':
                error(line_no, op, f'unexpected assignment to {zt}')

            frame.append(('set', z, x))
            frame.append(('sub', z, y))

        # z = x * y
        elif op == 'mul':
            if len(args) != 3:
                error(line_no, op, 'expected 3 args')

            (x, xt), (y, yt), (z, zt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected:
                error(line_no, op, f'unexpected operand types {xt} and {yt}')
            if zt != 'identifier':
                error(line_no, op, f'unexpected assignment to {zt}')

            frame.append(('set', z, x))
            frame.append(('mul', z, y))

        # q = x // y; m = x % y
        elif op == 'divmod':
            if len(args) != 4:
                error(line_no, op, 'expected 4 args')

            (x, xt), (y, yt), (q, qt), (m, mt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected:
                error(line_no, op, f'unexpected operand types {xt} and {yt}')
            if qt != 'identifier' or mt != 'identifier':
                error(line_no, op, f'unexpected assignment to {qt} and {mt}')

            if 'R0' not in variables:
                variables.insert(0, 'R0')

            frame.append(('set', 'R0', y))
            frame.append(('set', q, x))
            frame.append(('set', m, x))
            frame.append(('div', q, 'R0'))
            frame.append(('mod', m, 'R0'))

        # z = x // y
        elif op == 'div':
            if len(args) != 3:
                error(line_no, op, 'expected 3 args')

            (x, xt), (y, yt), (z, zt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected:
                error(line_no, op, f'unexpected operand types {xt} and {yt}')
            if zt != 'identifier':
                error(line_no, op, f'unexpected assignment to {zt}')

            frame.append(('set', z, x))
            frame.append(('div', z, y))

        # z = x % y
        elif op == 'mod':
            if len(args) != 3:
                error(line_no, op, 'expected 3 args')

            (x, xt), (y, yt), (z, zt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected:
                error(line_no, op, f'unexpected operand types {xt} and {yt}')
            if zt != 'identifier':
                error(line_no, op, f'unexpected assignment to {zt}')

            frame.append(('set', z, x))
            frame.append(('mod', z, y))

        # z = sgn(x - y)
        elif op == 'cmp':
            if len(args) != 3:
                error(line_no, op, 'expected 3 args')

            (x, xt), (y, yt), (z, zt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected:
                error(line_no, op, f'unexpected operand types {xt} and {yt}')
            if zt != 'identifier':
                error(line_no, op, f'unexpected assignment to {zt}')

            frame.append(('set', z, x))
            frame.append(('cmp', z, y))

        # b = 100 * (x - 48) + 10 * (y - 48) + (z - 48)
        elif op == 'a2b':
            if len(args) != 4:
                error(line_no, op, 'expected 4 args')

            (x, xt), (y, yt), (z, zt), (b, bt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected or zt not in expected:
                error(line_no, op, f'unexpected operand types {xt} {yt} {zt}')
            if bt != 'identifier':
                error(line_no, op, f'unexpected assignment to {bt}')

            if 'R0' not in variables:
                variables.insert(0, 'R0')
            if 'R1' not in variables:
                variables.insert(0, 'R1')

            frame.append(('set', 'R0', y))
            frame.append(('set', 'R1', z))
            frame.append(('set', b, x))
            frame.append(('sub', b, 48))
            frame.append(('mul', b, 10))
            frame.append(('add', b, 'R0'))
            frame.append(('sub', b, 48))
            frame.append(('mul', b, 10))
            frame.append(('add', b, 'R1'))
            frame.append(('sub', b, 48))

        # x = 48 + (a // 100)
        # y = 48 + ((a // 10) % 10)
        # z = 48 + (a % 10)
        elif op == 'b2a':
            if len(args) != 4:
                error(line_no, op, 'expected 4 args')

            (a, at), (x, xt), (y, yt), (z, zt) = args
            expected = {'number', 'identifier'}
            if at not in expected:
                error(line_no, op, f'unexpected operand type {at}')
            if xt != 'identifier' or yt != 'identifier' or zt != 'identifier':
                error(line_no, op, f'unexpected assignment to {xt} {yt} {zt}')

            if 'R0' not in variables:
                variables.insert(0, 'R0')

            frame.append(('set', 'R0', a))
            frame.append(('set', x, 'R0'))
            frame.append(('div', x, 100))
            frame.append(('add', x, 48))
            frame.append(('set', y, 'R0'))
            frame.append(('div', y, 10))
            frame.append(('mod', y, 10))
            frame.append(('add', y, 48))
            frame.append(('set', z, 'R0'))
            frame.append(('mod', z, 10))
            frame.append(('add', z, 48))

        # x[y] = z
        elif op == 'lset':
            if len(args) != 3:
                error(line_no, op, 'expected 3 args')

            (x, xt), (y, yt), (z, zt) = args
            expected = {'number', 'identifier'}
            if yt not in expected or zt not in expected:
                error(line_no, op, f'unexpected operand types {yt} and {zt}')
            if xt != 'identifier':
                error(line_no, op, f'unexpected assignment to {xt}')

            frame.append(('lset', x, y, z))

        # z = x[y]
        elif op == 'lget':
            if len(args) != 3:
                error(line_no, op, 'expected 3 args')

            (x, xt), (y, yt), (z, zt) = args
            expected = {'number', 'identifier'}
            if yt not in expected:
                error(line_no, op, f'unexpected operand type {yt}')
            if zt != 'identifier':
                error(line_no, op, f'unexpected assignment to {zt}')
            if xt != 'identifier':
                error(line_no, op, f'expected array name, got {xt}')

            frame.append(('lget', x, y, z))

        # if (x == y) {
        elif op == 'ifeq':
            if len(args) != 2:
                error(line_no, op, 'expected 2 args')

            (x, xt), (y, yt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected:
                error(line_no, op, f'unexpected operand types {xt} and {yt}')

            if_frame = []
            frame.append(('ifeq', x, y, if_frame))
            stack.append((op, frame))
            frame = if_frame

        # if (x != y) {
        elif op == 'ifneq':
            if len(args) != 2:
                error(line_no, op, 'expected 2 args')

            (x, xt), (y, yt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected:
                error(line_no, op, f'unexpected operand types {xt} and {yt}')

            if_frame = []
            frame.append(('ifneq', x, y, if_frame))
            stack.append((op, frame))
            frame = if_frame

        # while (x != y) {
        elif op == 'wneq':
            if len(args) != 2:
                error(line_no, op, 'expected 2 args')

            (x, xt), (y, yt) = args
            expected = {'number', 'identifier'}
            if xt not in expected or yt not in expected:
                error(line_no, op, f'unexpected operand types {xt} and {yt}')

            while_frame = []
            frame.append(('wneq', x, y, while_frame))
            stack.append((op, frame))
            frame = while_frame

        # void x(...args) {
        elif op == 'proc':
            if not args:
                error(line_no, op, 'expected proc name')
            for _, arg_type in args:
                if arg_type != 'identifier':
                    error(line_no, op, f'expected identifier, got {arg_type}')
            if stack:
                error(line_no, op, 'unexpected nested proc')

            proc_name, *arg_names = (name for (name, _) in args)
            if proc_name in procs:
                error(line_no, op, f'proc {proc_name!r} already defined')
            if len(set(arg_names)) < len(arg_names):
                error(line_no, op, f'proc {proc_name!r} has duplicate args')

            stack.append((op, frame))
            frame = []
            proc = (proc_name, arg_names)
            variables.extend(arg_names)

        # }
        elif op == 'end':
            if args:
                error(line_no, op, 'unexpected args to end')

            outer_op, outer_frame = stack.pop()

            if outer_op == 'proc':
                proc_name, arg_names = proc
                procs[proc_name] = (frame, arg_names)
                proc = None
                del variables[-len(arg_names):]

            frame = outer_frame

        # x(..args)
        elif op == 'call':
            if not args:
                error(line_no, op, 'expected proc name')
            expected = {'number', 'identifier'}
            if args[0][1] != 'identifier':
                error(line_no, op, f'unexpected proc type {args[0][1]}')
            for (_, arg_type) in args:
                if arg_type not in expected:
                    error(line_no, op, f'unexpected argument type {arg_type}')

            proc_name, *proc_args = (name for (name, _) in args)

            # defer procedure inference to third pass
            frame.append(('call', proc_name, proc_args))

        elif op == 'read':
            if len(args) != 1:
                error(line_no, op, 'expected 1 arg')
            (x, xt), = args
            if xt != 'identifier':
                error(line_no, op, f'expected identifier, got {xt}')

            frame.append(('read', x))

        elif op == 'msg':
            for (x, xt) in args:
                if xt == 'string':
                    for c in eval(x):
                        frame.append(('putc', ord(c)))
                elif xt == 'identifier':
                    frame.append(('putc', x))
                else:
                    error(line_no, op, f'unexpected operand {xt}')

    if stack:
        error(line_no, 'parser', 'unexpected EOF in control flow')

    return frame, variables, arrays, procs


def inject_proc(frame, procs, stack=None, replace=None):
    """Remove procedures from code by injecting procedures into code.

    Checks recursion by checking if called proc is in call `stack`.
    Replaces all variables (not arrays/procs) by `replace` mapping.
    """
    commands = []
    replace = replace or {}
    for command in frame:
        op, *operands = command

        if op in {'call', 'lset', 'lget'}:
            operands[1:] = [replace.get(a, a) if isinstance(a, str) else a
                            for a in operands[1:]]
        else:
            operands = [replace.get(a, a) if isinstance(a, str) else a
                        for a in operands]

        if op == 'call':
            proc_name, call_args = operands
            if proc_name not in procs:
                error(None, 'call', f'proc {proc_name!r} not defined')
            if stack and proc_name in stack:
                error(None, 'call', f'proc {proc_name!r} called recursively')
            proc_frame, arg_names = procs[proc_name]
            if len(arg_names) != len(call_args):
                error(None, 'call', f'proc called with invalid number of args')
            proc_replace = {n: replace.get(a, a) if isinstance(a, str) else a
                            for (n, a) in zip(arg_names, call_args)}
            proc_stack = [*stack, proc_name] if stack else [proc_name]
            proc_commands = inject_proc(proc_frame, procs,
                                        stack=proc_stack, replace=proc_replace)
            commands.extend(proc_commands)
        elif op in {'ifeq', 'ifneq', 'wneq'}:
            x, y, local_frame = operands
            local_frame = inject_proc(local_frame, procs,
                                      stack=stack, replace=replace)
            commands.append((op, x, y, local_frame))
        else:
            commands.append((op, *operands))
    return commands


def mem_alloc(variables, arrays):
    """Memory allocation.

    Size:
        variable: 1 cell
        array:    4 + n cells
    """
    allocated = 0
    var_alloc = {}
    array_alloc = {}
    for var in variables:
        var_alloc[var] = allocated
        allocated += 1
    for array, length in arrays.items():
        array_alloc[array] = allocated
        allocated += 4 + length

    return var_alloc, array_alloc, allocated


def to(p, dest):
    if dest >= p:
        return '>' * (dest - p)
    else:
        return '<' * (p - dest)


def copy(p, p1, p2, temp=None):
    """Copy *p1 to *p2, assuming pointer at p.

    Needs p2 and temp (default p2+1) to be empty.
    Pointer ends at p.
    """
    if temp is None:
        temp = p2 + 1
    return (
        f'{to(p, p1)}[-{to(p1, p2)}+{to(p2, temp)}+{to(temp, p1)}]'
        f'{to(p1, temp)}[-{to(temp, p1)}+{to(p1, temp)}]'
        f'{to(temp, p)}'
    )


def move(p, p1, p2):
    """Move *p1 to *p2, assuming pointer at p.

    Needs p2 to be empty.
    Pointer ends at p.
    """
    return (
        f'{to(p, p1)}[-{to(p1, p2)}+{to(p2, p1)}]{to(p1, p)}'
    )


def code_gen(frame, var_alloc, array_alloc, allocated):
    for command in frame:
        op, *operands = command

        # in-place binary op
        if op in {'set', 'add', 'sub', 'mul', 'div', 'mod', 'cmp'}:
            x, y = operands
            xp = var_alloc[x]

            yield to(0, allocated)

            if isinstance(y, int):
                yield '>' + '+' * y + '<'
            else:
                yield copy(allocated, var_alloc[y], allocated + 1)

            yield move(allocated, xp, allocated)

            if op == 'set':
                # x y -> y 0
                yield '[-]>[-<+>]<'
            elif op == 'add':
                # x y -> x+y 0
                yield '>[-<+>]<'
            elif op == 'sub':
                # x y -> x-y 0
                yield '>[-<->]<'
            elif op == 'mul':
                # x y 0 0 -> x*y 0 0 0
                yield '[->[->+>+<<]>>[-<<+>>]<<<]>>[-<<+>>]<[-]<'
            elif op == 'div':
                yield '>>+<<'
                # x y 1 0 0 0 -> 0 y-x%y x%y+1 x/y 0 0
                yield '[->-[>+>>]>[[-<+>]+>+>>]<<<<<]'
                yield '>[-]>[-]>[-<<<+>>>]<<<'
            elif op == 'mod':
                yield '>>+<<'
                # x y 1 0 0 0 -> 0 y-x%y x%y+1 x/y 0 0
                yield '[->-[>+>>]>[[-<+>]+>+>>]<<<<<]'
                yield '>[-]>>[-]<-[-<<+>>]<<'
            elif op == 'cmp':
                # if (y) {
                yield '>[>>>>>-<<<<<<'
                yield '[->>>+<<<]>[->>>+<<<]+>>'
                # 0 1 0 x y 0 -> 0 0 0 0 0 sgn(x-y)
                yield '[->-[>]<<]<[->>[[-]>>+<<]<<]<[->>>[-]>-<<<<<]'
                yield '>>>>>[-<<<<<+>>>>>]<<<<'
                # } else {
                yield ']>>>>>+[-<<<<<<'
                yield '[[-]>+<]'
                yield '>[-<+>]'
                # }
                yield '>>>>>]<<<<<<'

            yield move(allocated, allocated, xp)
            yield to(allocated, 0)

        # list op: x[y] <-> z
        elif op in {'lset', 'lget'}:
            x, y, z = operands
            xp = array_alloc[x]

            yield to(0, xp)

            if isinstance(y, int):
                yield '>' + '+' * y + '>' + '+' * y + '<<'
            else:
                yield copy(xp, var_alloc[y], xp + 1, temp=xp)
                yield copy(xp, var_alloc[y], xp + 2, temp=xp)

            if op == 'lset':
                if isinstance(z, int):
                    yield '>>>' + '+' * z + '<<<'
                else:
                    yield copy(xp, var_alloc[z], xp + 3, temp=xp)
            elif op == 'lget':
                yield to(xp, var_alloc[z])
                yield '[-]'
                yield to(var_alloc[z], xp)

            if op == 'lset':
                yield '>[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]'
                yield '>>>[-]<[->+<]<'
                yield '[[-<+>]<<<[->>>>+<<<<]>>-]<<'
            elif op == 'lget':
                yield '>[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]'
                yield '>>>[-<+<<+>>>]<<<[->>>+<<<]>'
                yield '[[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<'
                yield move(xp, xp + 3, var_alloc[z])

            yield to(xp, 0)

        # control flow
        elif op in {'ifeq', 'ifneq', 'wneq'}:
            x, y, clause = operands

            yield to(0, allocated)

            if isinstance(x, int):
                yield '+' * x
            else:
                yield copy(allocated, var_alloc[x], allocated)
            if isinstance(y, int):
                yield '>' + '+' * y + '<'
            else:
                yield copy(allocated, var_alloc[y], allocated + 1)

            if op == 'ifeq':
                yield '[->-<]'
                yield '+>[[-]<->]<'
                yield '[[-]'
            elif op == 'ifneq':
                yield '>[-<->]<'
                yield '[[-]'
            elif op == 'wneq':
                yield '>[-<->]<'
                yield '[[-]'

            yield to(allocated, 0)
            yield from code_gen(clause, var_alloc, array_alloc, allocated)
            yield to(0, allocated)

            if op in {'ifeq', 'ifneq'}:
                yield ']'
            elif op == 'wneq':
                if isinstance(x, int):
                    yield '+' * x
                else:
                    yield copy(allocated, var_alloc[x], allocated)
                if isinstance(y, int):
                    yield '>' + '+' * y + '<'
                else:
                    yield copy(allocated, var_alloc[y], allocated + 1)
                yield '>[-<->]<'
                yield ']'

            yield to(allocated, 0)

        # io
        elif op == 'read':
            x, = operands
            xp = var_alloc[x]
            yield to(0, xp) + ',' + to(xp, 0)
        elif op == 'putc':
            x, = operands
            yield to(0, allocated)
            if isinstance(x, int):
                yield '+' * x
            else:
                yield copy(allocated, var_alloc[x], allocated)
            yield '.[-]'
            yield to(allocated, 0)


def kcuf(code):
    tokens = lex(code)
    frame, variables, arrays, procs = lower(tokens)
    frame = inject_proc(frame, procs)
    print(frame)
    var_alloc, array_alloc, allocated = mem_alloc(variables, arrays)
    bf_code = list(code_gen(frame, var_alloc, array_alloc, allocated))
    print('Code:')
    print('\n'.join(bf_code))
    return ''.join(bf_code)


# If printing the code is annoying or a waste of your bandwith (~220 KB for final test).
# Please uncomment the following line.
# NOPRINT = True
