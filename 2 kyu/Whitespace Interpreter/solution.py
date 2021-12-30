import re
from collections import defaultdict


def parse_int(code, i):
    i += 1
    if code[i] == '\n':
        raise SyntaxError
    sign = 1 if code[i] == ' ' else -1
    i += 1
    bin = '0'
    while code[i] != '\n':
        bin += '0' if code[i] == ' ' else '1'
        i += 1
    return i, int(bin, 2) * sign


def parse_label(code, i):
    label = ''
    i += 1
    while code[i] != '\n':
        label += code[i]
        i += 1
    return i, label


def bind(f, *args):
    return lambda: f(*args)


def read_int(input):
    number = ''
    while input and input[0] != '\n':
        number += input.pop(0)
    if not input:
        raise RuntimeError

    input.pop(0)
    return int(number)


output = ip = clean = input = stack = calls = heap = labels = commands = None


def whitespace(code, inp=''):
    global output, ip, clean, input, stack, calls, labels, commands
    output = ''
    ip = 0
    clean = False
    input = list(inp)
    code = re.sub('[^ \t\n]', '', code)
    stack = []
    calls = []
    heap = defaultdict(int)
    labels = {}
    commands = []

    def discard(n):
        global stack
        if 0 <= n < len(stack):
            stack = stack[:-1 - n] + stack[-1:]
        else:
            stack = stack[-1:]

    def dup(n):
        if n < 0:
            raise RuntimeError
        stack.append(stack[-1 - n])

    def swap():
        stack[-2:] = stack[:-3:-1]

    def div():
        a, b = stack.pop(), stack.pop()
        stack.append(b // a)

    def mod():
        a, b = stack.pop(), stack.pop()
        stack.append(b % a)

    def heap_put():
        a, b = stack.pop(), stack.pop()
        heap[b] = a

    def heap_get():
        a = stack.pop()
        if a not in heap:
            raise RuntimeError
        stack.append(heap[a])

    def out_char():
        global output
        output += chr(stack.pop())

    def out_num():
        global output
        output += str(stack.pop())

    def in_char():
        heap[stack.pop()] = ord(input.pop(0))

    def in_num():
        heap[stack.pop()] = read_int(input)

    def call(label):
        global ip
        calls.append(ip + 1)
        ip = labels[label] - 1

    def ret():
        global ip
        ip = calls.pop() - 1

    def exit():
        global ip, clean
        ip = len(commands) - 1
        clean = True

    def jump(label, condition=None):
        global ip
        if condition is None:
            ip = labels[label] - 1
        else:
            n = stack.pop()
            if condition and n == 0 or not condition and n < 0:
                ip = labels[label] - 1

    i = j = 0
    while i < len(code):
        if code[i] == ' ':
            i += 1
            if code[i] == ' ':
                i, n = parse_int(code, i)
                commands.append(bind(stack.append, n))
            elif code[i] == '\t':
                i += 1
                if code[i] == ' ':
                    i, n = parse_int(code, i)
                    commands.append(bind(dup, n))
                elif code[i] == '\n':
                    i, n = parse_int(code, i)
                    commands.append(bind(discard, n))
            elif code[i] == '\n':
                i += 1
                if code[i] == ' ':
                    commands.append(lambda: stack.append(stack[-1]))
                elif code[i] == '\t':
                    commands.append(swap)
                elif code[i] == '\n':
                    commands.append(lambda: stack.pop())
        elif code[i] == '\t':
            i += 1
            if code[i] == ' ':
                i += 1
                if code[i] == ' ':
                    i += 1
                    if code[i] == ' ':
                        commands.append(lambda: stack.append(stack.pop() + stack.pop()))
                    elif code[i] == '\t':
                        commands.append(lambda: stack.append(-(stack.pop() - stack.pop())))
                    elif code[i] == '\n':
                        commands.append(lambda: stack.append(stack.pop() * stack.pop()))
                    else:
                        raise SyntaxError
                elif code[i] == '\t':
                    i += 1
                    if code[i] == ' ':
                        commands.append(div)
                    elif code[i] == '\t':
                        commands.append(mod)
                    else:
                        raise SyntaxError
                else:
                    raise SyntaxError
            elif code[i] == '\t':
                i += 1
                if code[i] == ' ':
                    commands.append(heap_put)
                elif code[i] == '\t':
                    commands.append(heap_get)
                else:
                    raise SyntaxError
            elif code[i] == '\n':
                i += 1
                if code[i] == ' ':
                    i += 1
                    if code[i] == ' ':
                        commands.append(out_char)
                    elif code[i] == '\t':
                        commands.append(out_num)
                    else:
                        raise SyntaxError
                elif code[i] == '\t':
                    i += 1
                    if code[i] == ' ':
                        commands.append(in_char)
                    elif code[i] == '\t':
                        commands.append(in_num)
                    else:
                        raise SyntaxError
                else:
                    raise SyntaxError
            else:
                raise SyntaxError
        elif code[i] == '\n':
            i += 1
            if code[i] == ' ':
                i += 1
                if code[i] == ' ':
                    i, l = parse_label(code, i)
                    if l in labels:
                        raise SyntaxError
                    labels[l] = len(commands)
                elif code[i] == '\t':
                    i, l = parse_label(code, i)
                    commands.append(bind(call, l))
                elif code[i] == '\n':
                    i, l = parse_label(code, i)
                    commands.append(bind(jump, l))
                else:
                    raise SyntaxError
            elif code[i] == '\t':
                i += 1
                if code[i] == ' ':
                    i, l = parse_label(code, i)
                    commands.append(bind(jump, l, True))
                elif code[i] == '\t':
                    i, l = parse_label(code, i)
                    commands.append(bind(jump, l, False))
                elif code[i] == '\n':
                    commands.append(ret)
                else:
                    raise SyntaxError
            elif code[i] == '\n':
                i += 1
                if code[i] == '\n':
                    commands.append(exit)
                else:
                    raise SyntaxError
            else:
                raise SyntaxError
        else:
            raise SyntaxError
        i += 1
        j = i

    while ip < len(commands):
        commands[ip]()
        ip += 1
    if not clean:
        raise RuntimeError
    return output
  
___________________________________________________
def whitespace(code, inp=''):
    code = ''.join(['STN'[' \t\n'.index(c)] for c in code if c in ' \t\n'])
    output, stack, heap, calls, pos, run, search, inp = [], [], {}, [], [0], [True], [None], list(inp)
    
    def set_(t, i, val):
        t[i] = val

    # Stack operations
    pop = lambda n=0: (assert_(n < len(stack)), stack[n], set_(stack, slice(n, n+1), ()))[1]
    get = lambda n: (assert_(n >= 0 and n < len(stack)), stack[n])[1]
    push = lambda n: stack.insert(0, n)
    
    # Parsing utilities
    def accept(tokens, action=None):
        for token in tokens.split(','):
            if code[pos[0]:pos[0]+len(token)] == token:
                pos[0] += len(token)
                if action:
                    p = 0
                    if token in ('SS', 'STS', 'STN'):
                        p = number()
                    elif token in ('NST', 'NSN', 'NTS', 'NTT', 'NSS'):
                        p = label()
                    ((not search[0]) or token == 'NSS') and action(p)
                return token

    def assert_(*args):
        if len(args) and args[0]: return args[0]
        raise Exception('error')

    def number():
        if accept('N'): raise Exception('No digits for number')
        n = '+0' if accept('S,T') == 'S' else '-0'
        while not accept('N'):
            n += str(int(accept('S,T') != 'S'))
        return int(n, 2)

    def label(l=''):
        while not accept('N'):
            l += accept('S,T') or ''
        return l + '1'

    instructions = {'SS'  : lambda n: push(n),
                    'STS' : lambda n: push(get(n)),
                    'STN' : lambda n: set_(stack, slice(1, len(stack) if n < 0 else 1 + n), ()),
                    'SNS' : lambda _: push(get(0)),
                    'SNT' : lambda _: set_(stack, slice(1, 1), [pop()]),
                    'SNN' : lambda _: pop(),
                    'TSSS': lambda _: push(pop(1) + pop()),
                    'TSST': lambda _: push(pop(1) - pop()),
                    'TSSN': lambda _: push(pop(1) * pop()),
                    'TSTS': lambda _: push(pop(1) / assert_(pop())),
                    'TSTT': lambda _: (lambda d: push((pop() % d + d) % d))(assert_(pop())),
                    'TTS' : lambda _: set_(heap, pop(1), pop()),
                    'TTT' : lambda _: (assert_(stack[0] in heap), push(heap[pop()])),
                    'TNSS': lambda _: output.append(chr(pop())),
                    'TNST': lambda _: output.append(str(pop())),
                    'TNTS': lambda _: (set_(heap, pop(), ord(assert_(inp)[0])), inp.pop(0)),
                    'TNTT': lambda _: (lambda n: (set_(heap, pop(), int(assert_(''.join(inp[:n])))), set_(inp, slice(0, n + 1), ())))(inp.index('\n') if '\n' in inp else len(inp)),
                    'NST' : lambda l: (calls.append(pos[0]), set_(pos, 0, heap[l]) if heap.get(l) else set_(search, 0, l)),
                    'NSN' : lambda l: set_(pos, 0, heap[l]) if heap.get(l) else set_(search, 0, l),
                    'NTS' : lambda l: (not pop()) and (set_(pos, 0, heap[l]) if heap.get(l) else set_(search, 0, l)),
                    'NTT' : lambda l: pop() < 0 and (set_(pos, 0, heap[l]) if heap.get(l) else set_(search, 0, l)),
                    'NTN' : lambda _: set_(pos, 0, assert_(calls).pop()),
                    'NNN' : lambda _: set_(run, 0, False),
                    'NSS' : lambda l: (assert_((not heap.get(l)) or heap[l] == pos[0]), set_(heap, l, pos[0]), search[0] == l and set_(search, 0, 0)),
                   }
                   
    while run[0]:
        assert_(pos[0] < len(code))
        any(accept(*instruction) for instruction in instructions.items()) or assert_()
    
    return ''.join(output)
  
___________________________________________________
import re

def whitespace(code, inp = ''):
    a = Whitespace(code, inp)
    return a.run()
    
class Whitespace:
    
    def __init__(self, code, inp):
        code = ''.join(char for char in code if char in ' \t\n')
        self.code = code.replace(' ', 's').replace('\t', 't').replace('\n', 'n')
        self.inp = inp
        self.stack = []
        self.output = ''
        self.heap = {}
        self.labels = {}
        self.cursor = 0
        self.subroutinestack = []
    
    def run(self):
        assert self.code, "Empty code not allowed"
        commands = re.compile('ss[st]*n|sts[st]*n|stn[st]*n|sns|snt|snn|' +                 # Stack manipulation
                              'tsss|tsst|tssn|tsts|tstt|' +                                 # Arighmetic
                              'tts|ttt|' +                                                  # Heap Access
                              'tnss|tnst|tnts|tntt|' +                                      # Input/Output
                              'nss[st]*n|nst[st]*n|nsn[st]*n|nts[st]*n|ntt[st]*n|ntn|nnn')  # Flow Control
        self.codearray = re.findall(commands, self.code)
        assert self.code == ''.join(self.codearray), "Invalid code"
        assert set(self.codearray).isdisjoint({'ssn', 'stsn', 'stnn'}), "Invalid number format: no sign"
        for ind, item in enumerate(self.codearray):
            if item.startswith('nss'):
                assert item[3:] not in self.labels, "Non-unique label at %s: %s" % (ind, item)
                self.labels[item[3:]] = ind
        self.exit = False
        while self.cursor < len(self.codearray) and not self.exit:
            command = self.codearray[self.cursor]
            command = re.match('^(ss|sts|stn|nss|nst|nsn|nts|ntt)(.*n)$', command) or command
            if not isinstance(command, str):
                eval('self.%s("%s")' % command.group(1, 2))
            else:
                eval('self.%s()' % command)
            self.cursor += 1
        assert self.exit, 'Bad exit'
        return self.output
    
    def ss(self, n):    #ss  [n] - Stack manipulation: push number onto the stack. 
        self.stack.append(self.parseNumber(n))
    
    def sts(self, n):   #sts [n] - Stack manipulation: copy nth item in the stack to the top of the stack.
        n = self.parseNumber(n)
        assert 0 <= n < len(self.stack), 'Failure to copy item at nonexisting index'
        item = len(self.stack) - n - 1
        self.stack.append(self.stack[item])  

    def stn(self, n):   #stn [n] - Stack manipulation: slide n values from below the top of the stack,
                        #                              or leave only top value in the stack.
        n = self.parseNumber(n)
        if n < 0 or n > len(self.stack):
            self.stack = [self.stack.pop()]
        else:
            top = self.stack.pop()
            self.stack = self.stack[0: len(self.stack) - n]
            self.stack.append(top)
          
    def sns(self):      #sns     - Stack manipulation: duplicate top value on the stack.
        assert self.stack, 'Failed to run sns() with empty stack'
        self.stack.append(self.stack[-1])

    def snt(self):      #snt     - Stack manipulation: swap two top values on the stack.
        self.stack += [self.stack.pop(), self.stack.pop()]
    
    def snn(self):      #snn     - Stack manipulation: discard the top value from the stack.
        assert self.stack, 'Failed to run snn() with empty stack'
        self.stack.pop()

    def tsss(self):     #tsss    - Arithmetic: pop a and b, push b + a.
        assert len(self.stack) > 1, 'Failed to do arithmetics with less than 2 values in stack'
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b + a)

    def tsst(self):     #tsst    - Arithmetic: pop a and b, push b - a.
        assert len(self.stack) > 1, 'Failed to do arithmetics with less than 2 values in stack'
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b - a)
        
    def tssn(self):     #tssn    - Arithmetic: pop a and b, push b * a.
        assert len(self.stack) > 1, 'Failed to do arithmetics with less than 2 values in stack'
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b * a)

    def tsts(self):     #tsts    - Arithmetic: pop a and b, push b / a (integer division!). Throw error if a == zero.
        assert len(self.stack) > 1, 'Failed to do arithmetics with less than 2 values in stack'
        a = self.stack.pop()
        assert a, 'Attempt to divide by zero'
        b = self.stack.pop()
        self.stack.append(b / a)

    def tstt(self):     #tstt    - Arithmetic: pop a and b, push b % a (integer division!). Throw error if a == zero.
        assert len(self.stack) > 1, 'Failed to do arithmetics with less than 2 values in stack'
        a = self.stack.pop()
        assert a, 'Attempt to divide by zero'
        b = self.stack.pop()
        negative = a * b < 0
        self.stack.append(b % a)
        
    def tts(self):      #tts     - Heap access: pop a and b, store a at heap address b.
        assert len(self.stack) > 1, 'Stack too short for tts() heap operation'
        a = self.stack.pop()
        b = self.stack.pop()
        self.heap[b] = a
          
    def ttt(self):      #ttt     - Heap access: pop a, then push value from heap adress a to the stack.
        a = self.stack.pop()
        assert a in self.heap, 'Failure to read from undefined heap address'
        self.stack.append(self.heap[a])

    def tnss(self):     #tnss    - Input/output: pop from stack and output as character.
        self.output += chr(self.stack.pop())

    def tnst(self):     #tnst    - Input/output: pop from stack and output as number.
        assert self.stack, 'Failure to output from empty stack at tnst()'
        self.output += str(self.stack.pop())


    def tnts(self):     #tnts    - Input/output: read char from input, pop heap address from stack,
                        #                        then store the char ASCII code at the heap address.
        assert self.inp, 'Failure to read character from input'
        a = self.inp[0]
        self.inp = self.inp[1:]
        assert self.stack, 'Failure to read heap address from empty stack at tnts()'
        self.heap[self.stack.pop()] = ord(a)
          
    def tntt(self):     #tntt    - Input/output: read number from input, pop heap address from stack,
                        #                        then store the char at the heap address.
        assert self.inp, 'Failure to read number from input'
        arr = self.inp.split('\n')
        a = arr[0]
        self.inp = '\n'.join(arr[1:])
        assert self.stack, 'Failure to read heap address from empty stack at tntt()'
        self.heap[self.stack.pop()] = int(a)
        
    def nss(self, l):   #nss [l] - Flow control: mark a location with label.
        pass
        
    def nst(self, l):   #nst [l] - Flow control: call subroutine located at label.
        self.subroutinestack.append(self.cursor)
        self.cursor = self.labels[l]
  
    def nsn(self, l):   #nsn [l] - Flow control: jump unconditionally to the label.
        self.cursor = self.labels[l]
             
    def nts(self, l):   #nts [l] - Flow control: pop from stack and if zero, jump to the label.
        assert self.stack, 'Failure to pop condition for jump from stack: empty stack'
        if not self.stack.pop():
              self.cursor = self.labels[l]

    def ntt(self, l):   #ntt [l] - Flow control: pop from stack and if less than zero, jump to the label.
        assert self.stack, 'Failure to pop condition for jump from stack: empty stack'
        if self.stack.pop() < 0:
              self.cursor = self.labels[l]

    def ntn(self):      #ntn     - Flow control: exit subroutine and returt to location from which it was called.
        self.cursor = self.subroutinestack.pop()

    def nnn(self):      #nnn     - Flow control: exit.
        self.exit = True

    def parseNumber(self, x):     #Parse number: get all code until n (the terminal).
                                  #              First bit is sign, next binary digits.
        n = int(x[1:-1].replace('s', '0').replace('t', '1') or '0', 2)
        return -n if x[0] == 't' else n
      
___________________________________________________
def read_number(code):
    i = next((i for i,c in enumerate(code) if c == '\n'), None)
    if i is None: raise Exception("Error reading number")
    if not i: raise Exception("number starting with terminal")
    sign = 1 if code[0] == ' ' else -1
    value = int(code[1:i].translate(str.maketrans(' \t', '01')) or '0', 2)
    return sign*value, i+1

def read_label(code):
    i = next((i for i,c in enumerate(code) if c == '\n'), None)
    if i is None: raise Exception("Error reading label")
    return code[:i], i+1

def input_number(input):
    res = []
    while True:
        c = next(input)
        if c == '\n': break
        res.append(c)
    return ''.join(res)

def raise_(msg): raise Exception(msg)
def assign(X, Y): X[:] = Y
def delete(X, i): del X[i]

# solution
def whitespace(code, inp = ''):
    L, stack, output, heap, input, marks, routine = [], [], [], {}, iter(inp), {}, [0]
    operation = {
        "  "      : lambda x: lambda: stack.append(x),
        " \t "    : lambda x: lambda: raise_("Out of bounds") if x < 0 else stack.append(stack[-x-1]),
        " \t\n"   : lambda x: lambda: assign(stack, stack[:-x-1] + [stack[-1]] if 0 < x <= len(stack) else [stack[-1]]),
        " \n "    : lambda: stack.append(stack[-1]),
        " \n\t"   : lambda: stack.append(stack.pop(-2)),
        " \n\n"   : lambda: delete(stack, -1),
        "\t   "   : lambda: stack.append(stack.pop(-2) + stack.pop()),
        "\t  \t"  : lambda: stack.append(stack.pop(-2) - stack.pop()),
        "\t  \n"  : lambda: stack.append(stack.pop(-2) * stack.pop()),
        "\t \t "  : lambda: stack.append(stack.pop(-2) // stack.pop()),
        "\t \t\t" : lambda: stack.append(stack.pop(-2) % stack.pop()),
        "\t\t "   : lambda: heap.__setitem__(stack.pop(-2), stack.pop()),
        "\t\t\t"  : lambda: stack.append(heap[stack.pop()]),
        "\t\n  "  : lambda: output.append(chr(stack.pop())),
        "\t\n \t" : lambda: output.append(str(stack.pop())),
        "\t\n\t " : lambda: heap.__setitem__(stack.pop(), ord(next(input))),
        "\t\n\t\t": lambda: heap.__setitem__(stack.pop(), int(input_number(input))),
        "\n  "    : lambda x: lambda: None, # Mark a location
        "\n \t"   : lambda x: lambda: routine.append(marks[x]),
        "\n \n"   : lambda x: lambda: marks[x],
        "\n\t "   : lambda x: lambda: marks[x] if stack.pop() == 0 else None,
        "\n\t\t"  : lambda x: lambda: marks[x] if stack.pop() < 0 else None,
        "\n\t\n"  : lambda: delete(routine, -1),
        "\n\n\n"  : None # End of program
    }
    
    code = ''.join(c for c in code if c in " \t\n")
    while code:
        for k,v in operation.items():
            if code.startswith(k):
                code = code[len(k):]
                if k in ("  ", " \t ", " \t\n"):
                    x, i = read_number(code)
                    code = code[i:]
                    L.append(v(x))
                elif k in ("\n  ", "\n \t", "\n \n", "\n\t ", "\n\t\t"):
                    x, i = read_label(code)
                    code = code[i:]
                    if k == "\n  ":
                        if x in marks: raise Exception("Label not unique")
                        marks[x] = len(L)
                    L.append(v(x))
                else:
                    L.append(v)
                break
        else:
            raise Exception("Invalid commands")
    while L[routine[-1]] != None: # Unclean termination if we reach the end of the list
        routine[-1] = L[routine[-1]]() or routine[-1]+1
    return ''.join(output)
  
___________________________________________________
import re

class StopProgram(Exception):
    pass


class Jump(Exception):
    def __init__(self, line):
        self.line = line


class InputError(Exception):
    pass


def parse_digit(sign, digit):
    digit = digit or '0'
    digit = digit.replace(' ', '0').replace('\t', '1')
    sign = sign.replace(' ', '1').replace('\t', '-1')
    digit = int(sign) * int(digit, base=2)
    return digit


def push_stack(line, inp, output, stack, heap, sign=None, digit=None):
    assert digit is not None
    assert sign is not None
    stack.append(parse_digit(sign, digit))
    return inp, output


def duplicate_nth(line, inp, output, stack, heap, sign=None, digit=None):
    assert digit is not None
    assert sign is not None
    n = parse_digit(sign, digit)

    if n < 0:
        raise IndexError

    stack.append(stack[-n-1])
    return inp, output


def discard_top_n(line, inp, output, stack, heap, sign=None, digit=None):
    assert digit is not None
    assert sign is not None
    n = parse_digit(sign, digit)

    if n < 0 or n >= len(stack):
        top = stack.pop()
        del stack[:]
        stack.append(top)
    else:
        stack_copy = stack[:]
        del stack[:]
        for i in range(0, len(stack_copy)-n-1):
            stack.append(stack_copy[i])
        stack.append(stack_copy[-1])

    return inp, output


def duplicate_top(line, inp, output, stack, heap):
    stack.append(stack[-1])
    return inp, output


def swap_first_two(line, inp, output, stack, heap):
    a = stack.pop()
    b = stack.pop()
    stack.append(a)
    stack.append(b)
    return inp, output


def discard_top(line, inp, output, stack, heap):
    stack.pop()
    return inp, output


def addition(line, inp, output, stack, heap):
    stack.append(stack.pop() + stack.pop())
    return inp, output


def subtraction(line, inp, output, stack, heap):
    a = stack.pop()
    b = stack.pop()
    stack.append(b - a)
    return inp, output


def multiplication(line, inp, output, stack, heap):
    stack.append(stack.pop() * stack.pop())
    return inp, output


def division(line, inp, output, stack, heap):
    a = stack.pop()
    b = stack.pop()
    stack.append(b // a)
    return inp, output


def modulo(line, inp, output, stack, heap):
    a = stack.pop()
    b = stack.pop()
    stack.append(b % a)
    return inp, output


def heap_retrieve(line, inp, output, stack, heap):
    a = stack.pop()
    stack.append(heap[a])
    return inp, output


def heap_store(line, inp, output, stack, heap):
    a = stack.pop()
    b = stack.pop()
    heap[b] = a
    return inp, output


def read_char(line, inp, output, stack, heap):
    if not inp:
        raise InputError

    a, inp = inp[0], inp[1:]
    b = stack.pop()
    heap[b] = ord(a)
    return inp, output


def read_number(line, inp, output, stack, heap):
    i = inp.find('\n')

    if i == -1:
        raise InputError

    try:
        a = int(inp[:i])
    except ValueError:
        try:
            a = int(inp[:i], base=16)
        except:
            raise InputError

    inp = inp[i+1:]
    b = stack.pop()
    heap[b] = a

    return inp, output


def pop_print(line, inp, output, stack, heap):
    output += str(stack.pop())
    return inp, output


def pop_print_chr(line, inp, output, stack, heap):
    output += chr(int(stack.pop()))
    return inp, output


def mark_location(line, inp, output, stack, heap, label=None):
    return inp, output


def call_subroutine(line, inp, output, stack, heap,
                    call_stack=None,
                    label=None,
                    locations=None):
    assert label is not None
    assert call_stack is not None
    call_stack.append(line)
    raise Jump(locations[label])


def jump(line, inp, output, stack, heap, label=None, locations=None):
    assert label is not None
    raise Jump(locations[label])


def jump_if_zero(line, inp, output, stack, heap, label=None, locations=None):
    assert label is not None

    if stack.pop() == 0:
        raise Jump(locations[label])

    return inp, output


def jump_if_lt_zero(line, inp, output, stack, heap,
                    label=None,
                    locations=None):
    assert label is not None

    if stack.pop() < 0:
        raise Jump(locations[label])

    return inp, output


def exit_subroutine(line, inp, output, stack, heap, call_stack=None):
    assert call_stack is not None
    raise Jump(call_stack.pop() + 1)


def exit_program(line, inp, output, stack, heap):
    raise StopProgram


"""
Whitespace is an esoteric programming language that uses only three characters:

    [space] or " " (ASCII 32)
    [tab] or "\t" (ASCII 9)
    [line-feed] or "\n" (ASCII 10)

"""
chars = {'SPACE': r' ', 'TAB': r'\t', 'LINE_FEED': r'\n'}
comments = r'[^{SPACE}{TAB}{LINE_FEED}]'.format(**chars)


"""
Each command in whitespace begins with an Instruction Modification
Parameter (IMP).
"""
STACK_MANIPULATION = r'{SPACE}'.format(**chars)
ARITHMETIC = r'{TAB}{SPACE}'.format(**chars)
HEAP_ACCESS = r'{TAB}{TAB}'.format(**chars)
IO = r'{TAB}{LINE_FEED}'.format(**chars)
FLOW_CONTROL = r'{LINE_FEED}'.format(**chars)


"""
Parsing Numbers

    Numbers begin with a [sign] symbol. [tab] -> negative,
    or [space] -> positive.

    Numbers end with a [terminal] symbol: [line-feed].

    Between the sign symbol and the terminal symbol are binary digits
    [space] -> binary-0, or [tab] -> binary-1.

    A number expression [sign][terminal] will be treated as zero.
"""
SIGN = r'(?P<sign>{TAB}|{SPACE})'.format(**chars)
DIGIT = r'(?P<digit>({SPACE}|{TAB})*)'.format(**chars)
NUMBER = r'{SIGN}{DIGIT}{LINE_FEED}'.format(SIGN=SIGN, DIGIT=DIGIT, **chars)

"""
Parsing Labels

Labels begin with any number of [tab] and [space] characters.
Labels end with a terminal symbol: [line-feed].
Unlike with numbers, the expression of just [terminal] is valid.
Labels must be unique.
A label may be declared either before or after a command that refers to it.
"""
LABEL = r'(?P<label>({TAB}|{SPACE})*){LINE_FEED}'.format(**chars)


"""
IMP [space] - Stack Manipulation

    [space] (number): Push n onto the stack.

    [tab][space] (number): Copy the nth value from the top of the stack
    and insert the copy on top of the stack.

    [tab][line-feed] (number): Discard the top n values below the top of the
    stack from the stack. (For n<0 or n>=stack.length, remove everything but
    the top value.)

    [line-feed][space]: Duplicate the top value on the stack.

    [line-feed][tab]: Swap the top two value on the stack.

    [line-feed][line-feed]: Discard the top value on the stack.

"""
PUSH_STACK = r'{SPACE}{NUMBER}'.format(NUMBER=NUMBER, **chars)
DUPLICATE_NTH = r'{TAB}{SPACE}{NUMBER}'.format(NUMBER=NUMBER, **chars)
DISCARD_TOP_N = r'{TAB}{LINE_FEED}{NUMBER}'.format(NUMBER=NUMBER, **chars)
DUPLICATE_TOP = r'{LINE_FEED}{SPACE}'.format(**chars)
SWAP_FIRST_TWO = r'{LINE_FEED}{TAB}'.format(**chars)
DISCARD_TOP = r'{LINE_FEED}{LINE_FEED}'.format(**chars)

"""
IMP [tab][space] - Arithmetic

    [space][space]: Pop a and b, then push b+a.

    [space][tab]: Pop a and b, then push b-a.

    [space][line-feed]: Pop a and b, then push b*a.

    [tab][space]: Pop a and b, then push b/a*. If a is zero, throw an error.
    *Note that the result is defined as the floor of the quotient.

    [tab][tab]: Pop a and b, then push b%a*. If a is zero, throw an error.
    *Note that the result is defined as the remainder after division and sign
    (+/-) of the divisor (a).
"""
ADDITION = r'{SPACE}{SPACE}'.format(**chars)
SUBTRACTION = r'{SPACE}{TAB}'.format(**chars)
MULTIPLICATION = r'{SPACE}{LINE_FEED}'.format(**chars)
DIVISION = r'{TAB}{SPACE}'.format(**chars)
MODULUS = r'{TAB}{TAB}'.format(**chars)

"""
IMP [tab][tab] - Heap Access

    [space]: Pop a and b, then store a at heap address b.

    [tab]: Pop a and then push the value at heap address a onto the stack.
"""
STORE = r'{SPACE}'.format(**chars)
RETRIEVE = r'{TAB}'.format(**chars)

"""
IMP [tab][line-feed] - Input/Output

    [space][space]: Pop a value off the stack and output it as a character.

    [space][tab]: Pop a value off the stack and output it as a number.

    [tab][space]: Read a character from input, a, Pop a value off the
    stack, b, then store the ASCII value of a at heap address b.

    [tab][tab]: Read a number from input, a, Pop a value off the stack, b, then
    store a at heap address b.
"""
POP_PRINT = r'{SPACE}{TAB}'.format(**chars)
POP_PRINT_CHR = r'{SPACE}{SPACE}'.format(**chars)
READ_CHAR = r'{TAB}{SPACE}'.format(**chars)
READ_NUMBER = r'{TAB}{TAB}'.format(**chars)

"""
IMP [line-feed] - Flow Control

    [space][space] (label): Mark a location in the program with label n.

    [space][tab] (label): Call a subroutine with the
    location specified by label n.

    [space][line-feed] (label): Jump unconditionally to the position specified
    by label n.

    [tab][space] (label): Pop a value off the stack and jump to the label
    specified by n if the value is zero.

    [tab][tab] (label): Pop a value off the stack and jump to the label
    specified by n if the value is less than zero.

    [tab][line-feed]: Exit a subroutine and return control to the location from
    which the subroutine was called.

    [line-feed][line-feed]: Exit the program.
"""
MARK_LOCATION = r'{SPACE}{SPACE}{LABEL}'.format(LABEL=LABEL, **chars)
CALL_SUBROUTINE = r'{SPACE}{TAB}{LABEL}'.format(LABEL=LABEL, **chars)
JUMP = r'{SPACE}{LINE_FEED}{LABEL}'.format(LABEL=LABEL, **chars)
JUMP_IF_ZERO = r'{TAB}{SPACE}{LABEL}'.format(LABEL=LABEL, **chars)
JUMP_IF_LT_ZERO = r'{TAB}{TAB}{LABEL}'.format(LABEL=LABEL, **chars)
EXIT_SUBROUTINE = r'{TAB}{LINE_FEED}'.format(**chars)
EXIT = r'{LINE_FEED}{LINE_FEED}'.format(**chars)

grammar = {
    STACK_MANIPULATION: {
        PUSH_STACK: push_stack,
        DUPLICATE_NTH: duplicate_nth,
        DISCARD_TOP_N: discard_top_n,
        DUPLICATE_TOP: duplicate_top,
        SWAP_FIRST_TWO: swap_first_two,
        DISCARD_TOP: discard_top,
    },
    ARITHMETIC: {
        ADDITION: addition,
        SUBTRACTION: subtraction,
        MULTIPLICATION: multiplication,
        DIVISION: division,
        MODULUS: modulo
    },
    HEAP_ACCESS: {
        STORE: heap_store,
        RETRIEVE: heap_retrieve,
    },
    IO: {
        POP_PRINT: pop_print,
        POP_PRINT_CHR: pop_print_chr,
        READ_CHAR: read_char,
        READ_NUMBER: read_number,
    },
    FLOW_CONTROL: {
        MARK_LOCATION: mark_location,
        CALL_SUBROUTINE: call_subroutine,
        JUMP: jump,
        JUMP_IF_ZERO: jump_if_zero,
        JUMP_IF_LT_ZERO: jump_if_lt_zero,
        EXIT_SUBROUTINE: exit_subroutine,
        EXIT: exit_program
    }
}



class ParseError(Exception):
    def __init__(self, code):
        self.code = repr(code)

    def __str__(self):
        return repr(self.code)


class RepeatedLabels(ParseError):
    pass


def parse(code):
    for imp in grammar:
        imp_match = re.match(imp, code)

        if imp_match:
            imp_matched = imp_match.group(0)

            for command, func in grammar[imp].items():
                command_match = re.match(command, code[len(imp_matched):])

                if command_match:
                    command_matched = command_match.group(0)
                    code = code[len(imp_matched) + len(command_matched):]
                    return code, func, command_match.groupdict()

    raise ParseError(code)


def whitespace(code, inp='', debug=False):
    output = ''
    stack = []
    heap = {}
    program = []
    call_stack = []
    locations = {}

    # remove comments
    code = re.sub(comments, '', code)

    line = 0

    while code:
        code, func, kwargs = parse(code)

        if func.__name__ in ('call_subroutine', 'jump', 'jump_if_zero',
                             'jump_if_lt_zero'):
            kwargs['locations'] = locations

        if func.__name__ in ('call_subroutine', 'exit_subroutine'):
            kwargs['call_stack'] = call_stack

        if func.__name__ == 'mark_location':
            if kwargs['label'] in locations:
                raise RepeatedLabels
            else:
                locations[kwargs['label']] = line

        program.append((func, kwargs))
        line += 1

        if debug:
            print('Parse:', func.__name__, kwargs)

    program_counter = 0

    while program_counter < len(program):
        try:
            func, kwargs = program[program_counter]
            inp, output = func(
                program_counter, inp, output, stack, heap, **kwargs)

            if debug:
                print('Exec:', func.__name__, kwargs)

        except StopProgram:
            return output
        except Jump as j:
            program_counter = j.line
        else:
            program_counter += 1

    raise RuntimeError('Unclean termination')
    
___________________________________________________

def unbleach(n):
    return n.replace(' ', 's').replace('\t', 't').replace('\n', 'n')

def getNumber(code):
    sign = read(code)
    c=""
    num=""
    while c!='n': c=read(code);num+=c
    if len(num)==1: return 0
    num = num.replace('t', '1').replace('s','0')
    val = int(num[:-1], 2)
    if sign=='t': val=-val
    return val

def stackM(code, stack):
    c=read(code)
    if c=='s':
        print("PUSH")
        stack.append(getNumber(code))
        return
    c2 = read(code)
    if c=='n'and c2=='s':
        print("DUPx1")
        stack.append(stack[len(stack)-1])
        return
    if c=='n'and c2=='t':
        print("SWAP")
        tmp = stack[-1]
        stack[-1]=stack[-2]
        stack[-2]=tmp
        return
    if c=='n'and c2=='n':
        print("DELx1")
        stack.pop()
        return

    n = getNumber(code)
    if c=='t'and c2=='s':
        print("DUPx"+str(n))
        stack.append(stack[-n])
        return
    if c=='t'and c2=='n':
        print("DELx"+str(n))
        for i in range (n): stack.pop()
        return
    print("ERRRRROOOR")

def read(code):
    if len(code)==0:
        print("ERROR on !!")
        quit()
    c=code[0]
    del code[0]
    return c

def flowC(code):
    print("flowC")
    pass

def arit(code):
    print("arit")
    pass

def heapA(code):
    print("heapA")
    pass

def inOut(code, stack):
    c=read(code)
    c2=read(code)
    if c=='s' and c2=='s':
        print("Out CHAR")
        return chr(stack.pop())
    if c=='s' and c2=='t':
        print("Out INT")
        return str(stack.pop())
    if c=='t' and c2=='s':
        print("Read CHAR")
        return ''      
    if c=='t' and c2=='t':
        print("Read INT")
        return ''
    print("ERROR IN OUT")
    return ''
    

# solution
def whitespace(code, inp = ''):
    output = ''
    stack = []
    heap = {}
    code=''.join(c for c in code if c==' ' or c=='\t' or c=='\n')
    code=list(unbleach(code))
    print(code)
    end=False
    while not end:
        c=read(code)
        print("stack="+str(stack))
        if c=='s': stackM(code, stack)
        elif c=='n': 
            if code[0]=='n': end=True
            else: flowC(code)
        else:
            c2=read(code)
            if c=='t' and c2=='s': arit(code)
            if c=='t' and c2=='t': heapA(code)
            if c=='t' and c2=='n': output+=inOut(code,stack)
    
    print("stack="+str(stack))
    return output
  
___________________________________________________
import re

def whitespace(code, inp = ''):
    output = ''
    stack, subroutines = [], []
    heap, label_dict = {}, {}
    inp = list(inp)
    code = ''.join([char for char in code if char in [' ', '\n', '\t']])
    control = 0
    if not code: raise SyntaxError('non command')
    while control < len(code):
        cmd = code[control]
        if cmd == ' ': 
            control += stack_manipulation(code[control+1 :], stack)
        elif cmd == '\t':
            if code[control+1] == ' ':
                arithmetic(code[control+2: control+4], stack)
                control += 4
            elif code[control+1] == '\t':
                heap_access(code[control+2: control+3], stack, heap)
                control += 3
            elif code[control+1] == '\n':
                inp, output = input_output(code[control+2: control+4], stack, heap, inp, output)
                control += 4
        elif cmd == '\n':
            control = flow_control(code, control+1, stack, label_dict, subroutines)
            if control == -1:
                break
        else: 
            raise SyntaxError('non command')
    if control != -1:
        err = 'Subroutine does not exit or return' if subroutines else 'Unclean termination'
        raise SyntaxError(err)
    return output

def parse_number(code):
    i, bit_list, number = 0, [], 0
    if code[i] == '\n':
        raise ValueError('Number should have at least a [sign] symbol') 
    while code[i] != '\n':
        bit_list.append(int(code[i] == '\t'))
        i += 1
    if len(bit_list) > 1:
        for bit in bit_list[1:]:
            number = number * 2 + bit
        number = (-1)**(bit_list[0] == 1)*number
    return i+1, number

def parse_label(code):
    label, i = '', 0
    while code[i]!= '\n':
        label += code[i]
        i += 1
    return i+1, label

def stack_manipulation(code, stack):
    i = 0
    command = code[i]
    if command == ' ':
        _i, number = parse_number(code[1:])
        stack.append(number)
        i+= 1+_i
    elif command == '\t':
        command = code[i+1]
        _i, number = parse_number(code[2:])
        if command == ' ':
            if number<0: 
                raise IndexError('Invalid Stack Index')
            number = -number-1
            if number not in range(-len(stack), len(stack)):
                raise IndexError("Stack index doesn't exist")
            else:
                stack.append(stack[number])
        elif command == '\n':
            if not stack:
                raise IndexError('Empty Stack')
            elif number < 0 or number >= len(stack):
                top = stack.pop()
                stack.clear()
                stack.append(top)
            else:
                top = stack.pop()
                for _ in range(number):
                    stack.pop()
                stack.append(top)
        i += 2 + _i
    elif command == '\n':
        command = code[i+1]
        if not stack:
                raise IndexError('Empty Stack')
        elif command == ' ':
            stack.append(stack[-1])
        elif command == '\t':
            stack.extend([stack.pop(), stack.pop()])
        elif command == '\n':
            stack.pop()
        i += 2
    else:
        raise NameError('Invalid command for Stack')
    return i+1

def arithmetic(command, stack):
    if command not in ['  ', ' \t', ' \n', '\t\t', '\t ']:
        raise NameError('Invalid command for Arithmetic')
    if len(stack) < 2: 
        raise ValueError('Attempting arithmetic with stack with less than 2 numbers')
    if command == '  ':
        stack.append(stack.pop() + stack.pop())
    elif command == ' \t':
        stack.append(-(stack.pop()-stack.pop()))
    elif command == ' \n':
        stack.append(stack.pop() * stack.pop())
    elif command[0] == '\t':
        div_mod = {' ': lambda x,y : x//y , '\t': lambda x,y : x%y}
        a = stack.pop()
        if a == 0: raise ValueError('Division by 0')
        stack.append(div_mod[command[1]](stack.pop(), a))
    
def heap_access(command, stack, heap):
    if command not in [' ','\t']: 
        raise NameError('Invalid command for Heap Access')
    if len(stack) == 0 : 
        raise ValueError('Empty stack')
    a = stack.pop()
    if command == ' ':
        if len(stack) == 0 : raise ValueError('Stack too short to pop twice')
        heap.update({stack.pop() : a})
    elif command == '\t':
        if a in heap.keys():
            stack.append(heap[a])
        else: 
            raise IndexError('Heap address not found')

def input_output(command, stack, heap, inp, output):
    if not stack:
        raise IndexError('Not enough elements in stack')
    elif command == '  ':
        output += chr(stack.pop())
    elif command == ' \t':
        output += str(stack.pop())
    elif command == '\t ':
        heap.update({stack.pop() : ord(inp.pop(0))})
    elif command == '\t\t':
        number , num_s = inp.pop(0), ''
        while number != '\n':
            num_s += number
            number = inp.pop(0) 
        heap.update({stack.pop() : int(num_s)})
    else:
        raise NameError('Invalid command for Input/Output')
    return inp, output

def flow_control(code, idx, stack, label_dict, subroutines):
    command = code[idx:idx+2]
    if command[0] == ' ':
        i, label = parse_label(code[idx+2:])
        if command[1] == ' ':
            if label in label_dict.keys():
                raise ValueError('Label already defined')
            else:
                label_dict.update({label : idx+2+i})
            i += idx+2
        elif command[1] in ['\t', '\n']:
            if label in label_dict.keys():
                if command[1] == '\t' : subroutines.append(idx+2+i)
                i = label_dict[label]
            else:
                m = re.search(r'(\n  ' + label + '\n)', code[i:])
                if m:
                    if command[1] == '\t' : subroutines.append(idx+2+i)
                    i += m.start()
                else:
                    raise ValueError('Label undefined')
    elif command in ['\t ','\t\t']:
        i, label = parse_label(code[idx+2:])
        if stack: 
            value = stack.pop()
        else:
            raise IndexError('Trying to pop from empty Stack')
        if (not value and command[1] == ' ') or (value < 0 and command[1] == '\t'):
            if label in label_dict.keys():
                i = label_dict[label]
            else:
                m = re.search(r'(\n  ' + label + '\n)', code[idx+2+i:])
                if m:
                    i += m.start()+idx+2
                else:
                    raise ValueError('Label undefined')
        else:
            i += idx+2
    elif command == '\t\n':
        if subroutines:
            i = subroutines.pop()
        else:
            raise SyntaxError('Return outside subroutine')
    elif command == '\n\n':
        i = -1
    else:
        raise NameError('Invalid command for Flow Control')
    return i 
