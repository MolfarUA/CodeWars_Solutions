class RSUProgram:
    def __init__(self, source):
        self._source = source

    def get_tokens(self):
        res, temp = [], ''
        line, col = 1, 1

        def add_command(suffix= ''):
            nonlocal temp

            res.append(temp + suffix)
            temp = ''

        def push_temp(s):
            nonlocal temp

            temp += s

        def new_line():
            nonlocal line, col

            line += 1
            col = 1

        def state_0(ch):
            if ch in "\n":
                new_line()
                return 0

            if ch in " \t\r":
                return 0

            if ch in '(q':
                res.append(ch)
                return 0

            if ch == '/':
                return 1

            if ch in 'FLR)':
                push_temp(ch)
                return 5

            if ch in 'Pp':
                push_temp(ch)
                return 7

            raise Exception(f'Error @{line}:{col}: Unexpected token: {ch!r}')

        # Validate the beginning of a comment
        def state_1(ch):
            if ch == '/': return 2
            if ch == '*': return 3

            raise Exception(f'Error @{line}:{col}: Unexpected token: {ch!r}')

        # Single-Line comment
        def state_2(ch):
            return 0 if ch == '\n' else 2

        # Multi-Line comment: start the validation of the finish
        def state_3(ch):
            return 4 if ch == '*' else 3

        # Multi-Line comment: validate the finish
        def state_4(ch):
            return 0 if ch == '/' else 3

        # Check the optional numeric suffix of a command
        def state_5(ch):
            if ch == '0':
                add_command(ch)
                return 0
            if ch in '123456789':
                push_temp(ch)
                return 6

            add_command()

            return state_0(ch)

        # Continue the numeric suffix of a command
        def state_6(ch):
            if ch in '0123456789':
                push_temp(ch)
                return 6

            add_command()

            return state_0(ch)

        # Check the mandatory numeric suffix for pattern definition and pattern call
        def state_7(ch):
            if ch == '0':
                add_command(ch)
                return 0
            if ch in '123456789':
                push_temp(ch)
                return 6

            raise Exception(f'Error @{line}:{col}: Unexpected token: {ch!r}')

        states = [state_0, state_1, state_2, state_3, state_4, state_5, state_6, state_7]
        state = 0
        for ch in (self._source + '\n'):
            state = states[state](ch)
            col += 1

        if temp: add_command()

        return res

    def convert_to_raw(self, tokens):
        nest_stack = []
        ids = 1

        class Scope:
            def __init__(self, parent=None):
                nonlocal ids

                self._id = ids
                self._parent = parent
                self._functions = {}
                self._tokens = []
                self._levels = []
                self._current = []
                
                ids += 1

            def _get_func(self, func_id):
                res = self._functions.get(func_id, None)
                if res is None and self._parent is not None:
                    res = self._parent._get_func(func_id)

                return res

            def add(self, tok):
                cmd = tok[0]

                if cmd in 'FLR':
                    self._current += [lambda stk: [cmd]] * int(tok[1:] or 1)
                    return self

                if cmd == 'P':
                    fn = int(tok[1:])
                    self._current.append(lambda stk: self.call(stk, fn))
                    return self

                if cmd == '(':
                    self._levels.append(self._current)
                    self._current = []
                    return self

                if cmd == ')':
                    self._current = self._levels.pop() + (self._current * int(tok[1:] or 1))
                    return self

                if cmd == 'p':
                    if self._levels:
                        raise Exception('Pattern in brackets')

                    func_id = int(tok[1:])
                    if func_id in self._functions:
                        raise Exception(f'Pattern {self._id}:{func_id} already exists')

                    nest_stack.append(self)

                    scope = Scope(self)
                    self._functions[func_id] = scope

                    return scope

                if cmd == 'q':
                    self.end()

                    return nest_stack.pop()

            def end(self):
                if self._levels:
                    raise Exception(f'Not closed bracket')

            def call(self, calls, func_id):
                func_name = f'{self._id}:{func_id}'

                if func_name in calls:
                    raise Exception(f'Infinite recursion with {func_name}')

                func = self._get_func(func_id)
                if func is None:
                    raise Exception(f'Pattern {func_name} not found')

                calls.add(func_name)
                res = func.run(calls)
                calls.remove(func_name)

                return res

            def run(self, calls):
                res = []
                for exec in self._current:
                    res += exec(calls)

                return res

        current = Scope()
        for tok in tokens:
            current = current.add(tok)
        current.end()

        if nest_stack:
            raise Exception('Pattern not closed')

        return current.run(set())

    def execute_raw(self, cmds):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        curr_pos, curr_dir = (0, 0), 1
        positions = {curr_pos}
        inf, sup = (0, 0), (0, 0)

        def to_left():
            nonlocal curr_dir

            curr_dir = (curr_dir + 3) % 4

        def to_right():
            nonlocal curr_dir

            curr_dir = (curr_dir + 1) % 4

        def go_forward():
            nonlocal curr_pos, inf, sup

            dir = directions[curr_dir]
            curr_pos = curr_pos[0] + dir[0], curr_pos[1] + dir[1]
            positions.add(curr_pos)

            if inf[0] > curr_pos[0]: inf = curr_pos[0], inf[1]
            if inf[1] > curr_pos[1]: inf = inf[0], curr_pos[1]
            if sup[0] < curr_pos[0]: sup = curr_pos[0], sup[1]
            if sup[1] < curr_pos[1]: sup = sup[0], curr_pos[1]

        actions = {'F': go_forward, 'R': to_right, 'L': to_left}
        for cmd in cmds:
            actions[cmd]()

        return '\r\n'.join([
            ''.join(['*' if (i, j) in positions else ' ' for i in range(inf[0], sup[0] + 1)])
            for j in range(inf[1], sup[1] + 1)
        ])

    def execute(self):
        try:
            return self.execute_raw(self.convert_to_raw(self.get_tokens()))
        except:
            print('Error for:', self._source)
            raise
__________________________________________________________
import re 


class RSUProgram:
    
    def __init__(self, source):
        self.source = source

    def get_tokens(self):
        code = self.source
        code = re.sub('//.*?(\n|$)|/\*.*?\*/', ' ', code, flags=re.S)
        if re.search('[/*]', code):
            raise Exception('invalid comments')
        
        if re.search('\s[0-9]', code):
            raise Exception('whitespace before number')
        if re.search('[^p0-9]0[0-9]', code):
            raise Exception('leading zeroes')
        if re.search('[pP]([^0-9]|$)', code):
            raise Exception('pattern without identifier')
        
        
        code = re.sub('\s+', '', code, flags=re.S)
        
        if re.match('^([(FRL)pqP][0-9]*)*$', code) is None:
            raise Exception('invalid tokens')
        
        tokens = re.findall('[(FRL)pqP][0-9]*', code)
        return tokens

    def convert_to_raw(self, tokens):
        
        flat_tokens = []
        for i in range(len(tokens)):
            if tokens[i][0] in 'FRL)' and len(tokens[i]) > 1:
                flat_tokens.append(tokens[i][:1])
                flat_tokens.append(tokens[i][1:])
            elif tokens[i][0] == 'p':
                flat_tokens.append(tokens[i][:1])
                flat_tokens.append('P' + tokens[i][1:])
            else:
                flat_tokens.append(tokens[i])
        tokens = flat_tokens
        
        def find_sub(tokens, d1='(', d2=')'):
            start = None
            for i in range(len(tokens)):
                if tokens[i] == d1:
                    start = i
                elif tokens[i] == d2:
                    return (start, i)
            return (start, None)
        
        def opt(flat):
            while '0' in flat:
                index = flat.index('0')
                del flat[index-1:index+1]
            return flat
    
        while '(' in tokens or ')' in tokens:
            start, end = find_sub(tokens)
            if start is None or end is None:
                raise Exception("paren mis match")
                
            sub = tokens[start+1:end]
            
            if 'p' in sub:
                raise Exception("lopping def")
            
            del tokens[start+1:end+1]
            tokens[start] = opt(sub)
        tokens = opt(tokens)
        
        patterns = {}
        
        while 'p' in tokens:
            start, end = find_sub(tokens, 'p', 'q')
            if end is None:
                raise Exception(f"missing 'q'")
            name, pattern = tokens[start+1], tokens[start+2:end]
            
            for i in range(start-1, -1, -1):
                if tokens[i] == 'q':
                    break
                if tokens[i] == 'p':
                    name = tokens[i+1] + ':' + name
            
            del tokens[start:end+1]
            if name in patterns:
                raise Exception(f"redefinition '{name}'")
                
            patterns[name] = pattern

        cmds = []
    
        def perform(op, caller=None):
            nonlocal cmds
            if type(op) == list:
                return perform_list(op, caller)
            if op[0] == 'P':
#                 prefix = caller + ':'
#                 while len(prefix) > 0:
#                     target = prefix + op
                if caller is None:
                    targets = [ op ]
                else:
                    prefix = caller + ':'
                    targets = []
                    while True:
                        targets.append(prefix + op)
                        if len(prefix) == 0:
                            break
                        prefix = re.sub('[^:]+:$', '', prefix)
                    
                for i in targets:
                    if i in patterns:
                        return perform_list(patterns[i], i)    
                raise Exception(f"undefined '{targets}' of '{op}'")
            cmds.append(op)
        
        def perform_list(list, caller=None):
            last = None
            for i in list:
                if type(i) == str and i.isdigit():        
                    for _ in range(int(i)-1):
                        perform(last, caller)
                else:
                    perform(i, caller)
                    last = i
        
        perform_list(tokens)
        return cmds
    
    def execute_raw(self, cmds):
        
        dirs = { 0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}
    
        path, loc, dire = [(0, 0)], (0, 0), 0
        for op in cmds:
            if op == 'F':
                loc = (loc[0] + dirs[dire][0], loc[1] + dirs[dire][1])
                path.append(loc)
            else:
                d = 1 if op == 'R' else -1
                dire = (dire + d) % 4
        
        minx = min(i[0] for i in path)
        maxx = max(i[0] for i in path)
        miny = min(i[1] for i in path)
        maxy = max(i[1] for i in path)
        
        w, h = (maxx - minx + 1), (maxy - miny + 1)
        map = [[' ' for _ in range(w)] for _ in range(h)]
        
        for i in path:
            map[i[1]-miny][i[0]-minx] = '*'
        
        return '\r\n'.join(''.join(i) for i in map)    
    
    def execute(self):
        return self.execute_raw(self.convert_to_raw(self.get_tokens()))
_______________________________________________________
import re

class RSUProgram:
    
    ID_PATT_BRA    = r'[PpRFL)](?:0|[1-9]\d*)|[RFLq()]'
    WHITE_COMMENTS = r'\s+|//.*?(?:\n|$)|/\*.*?\*/'
    TOKENIZER      = re.compile(r'|'.join([WHITE_COMMENTS, ID_PATT_BRA, r'.']), flags=re.DOTALL)
    VALID_TOKEN    = re.compile(ID_PATT_BRA)
    IS_NOT_TOKEN   = re.compile(WHITE_COMMENTS, flags=re.DOTALL)
    MOVES          = ((0,1), (1,0), (0,-1), (-1,0))
    
    
    def __init__(self, prog):        self.source = prog
    def convert_to_raw(self,tokens): return [ c for c,r in self.compileCode(tokens) for _ in range(r) ]
    def execute(self):               return self.execute_raw('', self.compileCode(self.get_tokens()))
    
    def compileCode(self, tokens):
        scope = {'parent':None, 'cmd':()}
        return self.applyPatterns(self.parseCode(iter(tokens), scope), scope, 0)
        
    def get_tokens(self):
        tokens = []
        for tok in self.TOKENIZER.findall(self.source):
            if   self.IS_NOT_TOKEN.match(tok): continue
            elif self.VALID_TOKEN.match(tok):  tokens.append(tok)
            elif tok:                          raise Exception("Invalid expression found: {}".format(tok))
        return tokens
        
        
    def execute_raw(self, cmds, todo=None):
        pos, seens, iDir = (0,0), {(0,0)}, 0
        for s,r in todo or ((c,1) for c in cmds):                      # OVERRIDE todo/cmds TO BYPASS SPECIFICATIONS...
            if s == 'F':
                for _ in range(r):
                    pos = tuple( z+dz for z,dz in zip(pos, self.MOVES[iDir]) )
                    seens.add(pos)
            else:
                iDir = (iDir + r * (-1)**(s=='L')) % len(self.MOVES)
        
        miX, maX = ( f(x for x,_ in seens) for f in (min,max))
        miY, maY = ( f(y for _,y in seens) for f in (min,max))
        
        return '\r\n'.join( ''.join('*' if (x,y) in seens else ' ' for y in range(miY, maY+1)) 
                            for x in range(miX, maX+1) )
        
        
    def parseCode(self, tokIter, scope, inPattern=0):
        cmds = [[]]
        for tok in tokIter:
            cmd,r = tok[0], int(tok[1:] or '1')
            isRepeat = cmds[-1] and cmds[-1][-1] and cmds[-1][-1][0]==cmd
            
            if cmd in 'pq' and len(cmds)>1: raise Exception("pattern definition inside brackets")
            
            if cmd == 'p':
                name = tok.upper()
                if name in scope: raise Exception("Invalid pattern: cannot define multiple patterns with the same name at the same level: {}\nScope: {}\n\n{}".format(name, scope, self.source))
                else:
                    freshScope  = {'parent': scope, 'cmds':()}
                    scope[name] = freshScope
                    freshScope['cmds'] = self.parseCode(tokIter, freshScope, 1)
                    
            elif cmd == 'q': 
                if not inPattern: raise Exception('unopened pattern definition')
                inPattern = 0
                break
                
            elif cmd == '(': cmds.append([])
            elif cmd == ')': lst = cmds.pop() ; cmds[-1].extend(lst * r)
            elif isRepeat:   cmds[-1][-1] = (cmd, cmds[-1][-1][1]+r)
            else:            cmds[-1].append( (tok,1) if cmd=='P' else (cmd,r) )
        
        if inPattern:   raise Exception("unclosed pattern definition, last token: "+tok)
        if len(cmds)>1: raise Exception("unclosed brackets, last token: "+tok)
        return cmds[0]
            
    
    def applyPatterns(self, rawCmds, scope, depth):
        if depth==20: raise Exception("Stack overflow")
        lst = []
        for c,r in rawCmds:
            if c[0]!='P': lst.append((c,r))
            else:
                pattern, nextScope = self.reachPattern(scope, c)
                lst.extend( self.applyPatterns(pattern, nextScope, depth+1) )
        return lst
        
        
    def reachPattern(self, scope, name):
        calledP = scope.get(name)
        parent  = scope['parent']
        if calledP is not None: return calledP['cmds'], calledP
        if not parent:          raise Exception("Unknown pattern: " + name)
        return self.reachPattern(parent, name)

________________________________________________________
import re

class RSUProgram:
    comments_re = re.compile(r'\/\*(?:(\*(?!/))|(?:[^\*]))*\*/|//[^\n\r]*(?=$|\r|\n)', re.MULTILINE)
    tokenizer = re.compile(r'p[1-9][0-9]*|p0|[FLR][1-9][0-9]*|[FLR]0|[FLR]{1}|P\d+|\(|\)[1-9][0-9]*|\)0|\)|q')

    def __init__(self, source):
        self._src = self.comments_re.sub(' ', source)

    def get_tokens(self):
        tokens = self.tokenizer.findall(self._src)
        rest = self.tokenizer.sub('', self._src)
        if rest.strip():
            raise Exception('Invalid syntax')
        return tokens

    def collect_f_defs(self, tokens):
        """It will return body and functions"""
        functions = []
        stack = []
        body = []
        for t in tokens:
            if 'p' in t:
                scope = []
                if stack:
                    scope.append(stack[-1]['name'])
                scope.append(t[1:])
                name = '.'.join(scope)
                for f in functions:
                    if f['name'] == name:
                        raise Exception('Function redefenition')
                stack.append({'name': name, 'body': []})
            elif t == 'q':
                functions.append(stack.pop())
            elif stack:
                stack[-1]['body'].append(t)
            else:
                body.append(t)
        if stack:
            raise Exception('Function definition is not closed')
        return body, functions

    def get_func(self, funcs, scope, name):
        path = scope.split('.')
        if not path:
            for f in funcs:
                if f['name'] == name:
                    return f
        else:
            for i in range(len(path), -1, -1):
                s = '.'.join(path[0:i] + [name])
                for f in funcs:
                    if f['name'] == s:
                        return f
        raise Exception('Function {} not defined'.format(name))

    def collapse_funcs(self, body, scope, funcs, depth_counter):
        if depth_counter > len(funcs):
            raise Exception('Infinite recursion detected')
        result = []
        for t in body:
            if 'P' in t:
                f_call = self.get_func(funcs, scope, t[1:])
                result.extend(self.collapse_funcs(f_call['body'],
                                                  f_call['name'],
                                                  funcs,
                                                  depth_counter+1))
            else:
                result.append(t)
        return result

    def unbracket(self, tokens):
        stack = []
        output = []
        for t in tokens:
            if t == '(':
                stack.append(len(output))
            elif t[0] == ')':
                if not stack:
                    raise Exception('Unbalanced brackets')
                repeat = 1
                if len(t) > 1:
                    repeat = int(t[1:])
                start = stack.pop()
                block = output[start:]
                output = output[0:start]
                for _ in range(repeat):
                    output.extend(block)
            else:
                output.append(t)
        if stack:
            raise Exception('Unbalanced brackets')
        return output

    def detect_bracketed_f_defs(self):
        if re.findall(r'\([RLFP\d\s]*p.*q[RLFP\d\s]*\)', self._src, re.S):
            raise Exception('Bracketed function defenition')

    def expand(self, tokens):
        result = []
        for t in tokens:
            if len(t) > 1:
                result.extend([t[0]]*int(t[1:]))
            else:
                result.append(t)
        return result

    def convert_to_raw(self, tokens):
        """ Process the array of tokens generated by the `getTokens`
        method (passed into this method as `tokens`) and return an (new)
        array containing only the raw commands `F`, `L` and/or `R`
        Throw a suitable error if necessary
        """
        self.detect_bracketed_f_defs()
        body, functions = self.collect_f_defs(tokens)
        body = self.unbracket(body)
        for f in functions:
            f['body'] = self.unbracket(f['body'])
        body = self.collapse_funcs(body, '', functions, 0)
        return self.expand(body)


    turns = {'R': {'top': 'right', 'right': 'bottom', 'bottom': 'left', 'left': 'top'},
            'L': {'top': 'left', 'left': 'bottom', 'bottom': 'right', 'right': 'top'}}

    def move(self, d, x, y, amount=1):
        if d == 'top':
            return x, y-amount
        elif d == 'right':
            return x+amount, y
        elif d == 'left':
            return x-amount, y
        elif d == 'bottom':
            return x, y+amount


    def simulate(self, tokens):
        """Return starting point x, y and field dimentions"""
        min_x, min_y, max_x, max_y = 0, 0, 0, 0
        x, y = 0, 0
        direction = 'right'
        for t in tokens:
            if t == 'F':
                x, y = self.move(direction, x, y)
                min_x, min_y = min(min_x, x), min(min_y, y)
                max_x, max_y = max(max_x, x), max(max_y, y)
            else:
                direction = self.turns[t][direction]
        return 0 - min_x, 0 - min_y, max_x - min_x + 1, max_y - min_y + 1

    def execute_raw(self, tokens):
        x, y, size_x, size_y = self.simulate(tokens)
        field = [[' ' for _ in range(size_x)] for _ in range(size_y)]
        direction = 'right'
        field[y][x] = '*'
        for t in tokens:
            if t == 'F':
                x, y = self.move(direction, x, y)
                field[y][x] = '*'
            else:
                direction = self.turns[t][direction]
        lines = [''.join(l) for l in field]
        return '\r\n'.join(lines)

    def execute(self):
        return self.execute_raw(self.convert_to_raw(self.get_tokens()))

________________________________________________________
import re
from pprint import pprint


class RSUProgram:
    def __init__(self, source):
        self.source = source
        pass
    
    def get_tokens(self):
#         print(self.source)
        tokens = re.findall(r'/\*(?:.|\n)*?\*/|//.*|(q|[LRF\)](?:0|[1-9]\d*)?|[pP](?:0|[1-9]\d*)|\()|([^\s])', self.source, re.MULTILINE)
        
        if any(t[1] for t in tokens):
            raise SyntaxError('something went wrong')
            
        tokens = [
            t[0]
            for t in tokens
            if t[0]
        ]
        
        return tokens
    
    def convert_to_raw(self, tokens):
        print(tokens)
        program = { 'n': None, 'c': [[]], 'p': {'^': None}, 'e': False }
        ct = [program]
        for t in tokens:
            if t[0] == 'p':
                if len(ct[-1]['c']) > 1:
                    raise SyntaxError('patterns cannot be nested by a bracketed sequence')
                if t[1:] in ct[-1]['p']:
                    raise Exception('duplicate pattern names on the same level are not allowed')
                np = {'n': t[1:], 'c': [[]], 'p': {'^': ct[-1]['p']}, 'e': False}
                ct[-1]['p'][t[1:]] = np
                ct.append(np)
            elif t == 'q':
                if len(ct[-1]['c']) > 1:
                    raise SyntaxError('one or more bracket sequences are not closed inside a pattern definition')
                ct.pop()
            elif t[0] in 'FLR':
                ct[-1]['c'][-1] += [t[0]]*int(t[1:]) if t[1:] else [t[0]]
            elif t[0] == 'P':
                ct[-1]['c'][-1].append(t)
            elif t == '(':
                ct[-1]['c'].append([])
            elif t[0] == ')':
                b = ct[-1]['c'].pop()
                if t[1:]:
                    b *= int(t[1:])
                ct[-1]['c'][-1] += b
            else:
                raise Exception('wat?: ' + repr(t))
        
        def find(p, name):
            if name in p:
                return p[name]
            elif p['^'] is not None:
                return find(p['^'], name)
            return None
        
        def expand(path, p):
            if p['e']: return
            if p in path:
                raise RecursionError('recursion is not allowed')
            
            nc = []
            for c in p['c'][-1]:
                if c[0] == 'P':
                    r = find(p['p'], c[1:])
                    if r is None:
                        raise NameError('procedure does not exist')
                    expand(path + [p], r)
                    nc += r['c'][0]
                else:
                    nc.append(c)
            p['c'] = [nc]
        
        if len(ct) > 1:
            raise SyntaxError('pattern definition is not closed')
        
        expand([], program)
        return program['c'][0]
    
    def execute_raw(self, cmds):
        p, d = (0, 0), (1, 0)
        area = {p}
        execute = lambda c: {
            'F': ((p[0] + d[0], p[1] + d[1]), d),
            'L': (p, (+d[1], -d[0])),
            'R': (p, (-d[1], +d[0])),
        }.get(c)
        bounds = (0, 0, 0, 0)

        for c in cmds:
            p, d = execute(c)
            bounds = (min(bounds[0], p[0]), min(bounds[1], p[1]), max(bounds[2], p[0]), max(bounds[3], p[1]))
            area.add(p)

        return '\r\n'.join(''.join('*' if (x,y) in area else ' '
                                    for x in range(bounds[0], bounds[2]+1))
                                    for y in range(bounds[1], bounds[3]+1))
    
    def execute(self):
        return self.execute_raw(self.convert_to_raw(self.get_tokens()))
