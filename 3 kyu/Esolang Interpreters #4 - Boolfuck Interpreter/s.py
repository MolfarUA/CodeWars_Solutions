5861487fdb20cff3ab000030


from collections import defaultdict

def boolfuck(code, input=""):
    input = [int(c) for c in ''.join([bin(ord(c))[2:].rjust(8, '0') for c in input][::-1])]
    cp, p, out, bits, starts, brackets = 0, 0, [], defaultdict(int), [], {}

    for i, c in enumerate(code):
        if c == '[': starts.append(i)
        elif c is ']':
            brackets[i] = starts.pop()
            brackets[brackets[i]] = i

    while cp < len(code):
        if   code[cp] == '[' and not bits[p]: cp = brackets[cp]
        elif code[cp] == ']': cp = brackets[cp] - 1
        elif code[cp] == '>': p += 1
        elif code[cp] == '<': p -= 1
        elif code[cp] == '+': bits[p] = (0 if bits[p] else 1)
        elif code[cp] == ',': bits[p] = (input.pop() if input else 0)
        elif code[cp] == ';': out.append(bits[p])
        cp += 1
        
    s = ''
    while out:
        out, s = out[8:], s + chr(int(''.join(str(c) for c in out[:8][::-1]).rjust(8, '0'), 2))
    return s
_____________________________
import re, collections

def boolfuck(code, input=''):
    # initialize variables
    data, ptr, step, output, stack, loop = collections.defaultdict(int), 0, 0, [], [], {}
    
    # deconstruct the input and turn it into a generator
    input = reversed(list(map(int, bin(sum(ord(c)*256**i for i, c in enumerate(input)))[2:])))
    
    # break code into commands
    code = re.findall('\+|,|;+|<+|>+|\[|\]', code)
    
    # parse loops and store start/end
    if '[' in code:
        for i, command in enumerate(code):
            if   command == '[':
                stack.append(i)
            elif command == ']':
                start = stack.pop()
                loop[start], loop[i] = i, start
    
    # execute the code
    while step < len(code):
        command, count = code[step][0], len(code[step])
        
        if   command == '+': data[ptr] ^= 1
        elif command == ',': data[ptr] = next(input, 0)
        elif command == ';': output.extend([data[ptr]] * count)
        elif command == '<': ptr -= count
        elif command == '>': ptr += count
        elif command == '[' and data[ptr] == 0: step = loop[step]
        elif command == ']' and data[ptr] == 1: step = loop[step]
        
        step += 1

    # reconstruct the output
    output = re.findall('.{1,8}', ''.join(map(str, output)))
    output = ''.join(chr(int(x[::-1], 2)) for x in output)
    return output
_____________________________
from collections import defaultdict


class BoolFuck:

    def __init__(self, code: str, input: str):
        self.s = ''.join([self.get_cache(item) for item in input])
        self.code = code
        self.input = list(map(int, self.s))
        self.input_length = len(self.s)
        self.cache = []

        self.pointer = 0
        self.tape = [0]
        self.code_pointer = 0

        self.log = [0] * len(self.code)
        st = []
        for i in range(len(self.code)):
            if self.code[i] == '[':
                st.append(i)
            if self.code[i] == ']':
                j = st.pop(-1)
                self.log[j] = i
                self.log[i] = j

    def move_right(self):
        self.pointer += 1
        if self.pointer == len(self.tape):
            self.tape.append(0)

    def move_left(self):
        if self.pointer == 0:
            self.tape.insert(0, 0)
        else:
            self.pointer -= 1

    def plus(self):
        self.tape[self.pointer] ^= 1

    def read(self):
        self.tape[self.pointer] = 0 if len(
            self.input) == 0 else self.input.pop(0)

    def get_cache(self, ch):
        ch = f'{ord(ch):08b}'
        return ch[::-1]

    def output(self):
        self.cache.append(self.tape[self.pointer])

    @property
    def ans(self):
        while len(self.cache) % 8 != 0:
            self.cache.append(0)
        ret = ''
        for i in range(0, len(self.cache), 8):
            t = 0
            for j in range(7, -1, -1):
                t = t * 2 + self.cache[i + j]
            ret += chr(t)
        return ret

    def jump_right(self):
        if self.tape[self.pointer] == 0:
            self.code_pointer = self.log[self.code_pointer]

    def jump_left(self):
        if self.tape[self.pointer] != 0:
            self.code_pointer = self.log[self.code_pointer]

    def run(self):
        while self.code_pointer < len(self.code):
            c = self.code[self.code_pointer]
            if c == '<': self.move_left()
            elif c == '>': self.move_right()
            elif c == '+': self.plus()
            elif c == ',': self.read()
            elif c == ';': self.output()
            elif c == ']': self.jump_left()
            elif c == '[': self.jump_right()
            else: pass

            self.code_pointer += 1

        return self.ans

    def empty(self):
        pass


def boolfuck(code, input=""):

    fuck = BoolFuck(code, input)
    return fuck.run()
_____________________________
class BoolfuckInterpreter:

    def __init__(self, code, user_input = ""):
        self.user_input = user_input
        self.code = code
        self.cptr = 0
        
        self.memory = {0 : "0"}
        self.mptr = 0
        
        self.closed_brackets = {}
        self.open_brackets = {}
        brackets = []
        
        i = 0
        while i < len(self.code):
            if self.code[i] == "[":
                brackets.append(i)
            elif self.code[i] == "]":
                b = brackets.pop(len(brackets) - 1)
                self.closed_brackets[b] = i
                self.open_brackets[i] = b
                
            i += 1
        
        self.out_bits = [""]
        self.out_ptr = 0
        
        self.in_bits = []
        for char in user_input:
            self.in_bits.append(list(bin(ord(char))[2:].zfill(8)[::-1]))
        
    
    def run(self):
        commands = {
            "+" : self.__flip_bit,
            "," : self.__read_from_input,
            ";" : self.__print_to_out,
            "<" : self.__move_mptr_left,
            ">" : self.__move_mptr_right,
            "[" : self.__eval_open_bracket,
            "]" : self.__eval_closed_bracket
        }
        
        while self.cptr < len(self.code):
            if self.code[self.cptr] in commands.keys():
                commands[self.code[self.cptr]]()
            
            # self.__debug()
            
            self.cptr += 1
            
        result = ""
        
        if self.out_bits[self.out_ptr] == "":
            del self.out_bits[len(self.out_bits) - 1]
            self.out_ptr -= 1
            
        if self.user_input != "" and len(self.out_bits[self.out_ptr]) < 8:
            self.out_bits[self.out_ptr] = self.out_bits[self.out_ptr].zfill(8)
        
        for byte in self.out_bits:
            result += chr(int(byte, 2))
        
        return result
        
    
    def __flip_bit(self):
        if self.memory[self.mptr] == "0":
            self.memory[self.mptr] = "1"
        else:
            self.memory[self.mptr] = "0"
            
    
    def __move_mptr_left(self):
        self.mptr -= 1
        if self.mptr not in self.memory.keys():
            self.memory[self.mptr] = "0"
            
            
    def __move_mptr_right(self):
        self.mptr += 1
        if self.mptr not in self.memory.keys():
            self.memory[self.mptr] = "0"
            
    
    def __eval_open_bracket(self):
        if self.memory[self.mptr] == "0":
            self.cptr = self.closed_brackets[self.cptr]
            
    
    def __eval_closed_bracket(self):
        if self.memory[self.mptr] == "1":
            self.cptr = self.open_brackets[self.cptr]
            
    
    def __read_from_input(self):
        if len(self.in_bits) == 0:
            self.memory[self.mptr] = "0"
        else:
            self.memory[self.mptr] = self.in_bits[0].pop(0)
            
            if len(self.in_bits[0]) == 0:
                del self.in_bits[0]
    
    
    def __print_to_out(self):
        self.out_bits[self.out_ptr] = str(self.memory[self.mptr]) + self.out_bits[self.out_ptr]
        
        if len(self.out_bits[self.out_ptr]) == 8:
            self.out_ptr += 1
            self.out_bits.append("")
            
    
    def __debug(self):
        print(f"{self.code[0:self.cptr]} ({self.code[self.cptr]}) {'' if self.cptr == len(self.code) - 1 else self.code[self.cptr+1::]}\n")
    
        print(f"Memory: {self.memory}")
        print(f"Memptr: {self.mptr}\n")
        print(f"In Bits: {self.in_bits}")
        print(f"Out Bits: {self.out_bits}")
        print(f"Outptr: {self.out_ptr}")
        print(f"-----------------------")
        step = input()
    

def boolfuck(code, user_input = ""):
    return BoolfuckInterpreter(code, user_input).run()
_____________________________
#Useful conversion between characters and bits.  All characters with ascii value
#0-255 are converted to 8 bits (ie one byte), so each are padded so they are all
#a byte e.g. '\n' is 10 in decimal, and so is converted to '00001010' (with the
# appropriate padding )
BYTE_SIZE = 8
def convChrToBits(c):
    return bin(ord(c))[2:].zfill(BYTE_SIZE)
#end function

def convBitsToChr(b):
    return chr(int(b, 2))
#end function

#Determine the locations of all matching brackets
def populateJumpTable(codeTape)-> dict:
    stack = []
    jumpLookup = {}
    for codePtr, cmd in enumerate(codeTape):
        if cmd == '[':
            stack.append(codePtr)
        elif cmd == ']':
            if len(stack) != 0:
                matchingBracketPos = stack.pop()
                jumpLookup[matchingBracketPos] = codePtr
                jumpLookup[codePtr] = matchingBracketPos
            else:
                raise ValueError("Unmatched Brackets")
    return jumpLookup
#end function


# Input Tape: A tape filled with input for the BoolF language e.g. "aC01". This
#             tape is formatted for the BoolF language: Each character is converted to binary
#             and stored in little-endian order  e.g. 'ab'
#               'a' is 01100001, (with the padded zero for 8 bits) and is 10000110 in little endian
#               'b' is 01100010  (must be padded to 8 bits) and is 01000110 in little endian
#               So, the input tape (index 0 at the left) is '1000011001000110' (so the characters
#               are read in the order 1 0 0 0 1 1 ... etc) 
def formatInputStream(inputStream)-> list:
    formattedInput = []
    for char in inputStream:
        bitsStr = convChrToBits(char)
        revBits = bitsStr[::-1]
        formattedInput.extend( list(revBits) )
    return formattedInput
#---end function


#convert the outputstream of bits to characters
def formatOutput(outputStream)-> str:
    bitStream = outputStream
    numBits = len(bitStream)        
    rem = numBits%BYTE_SIZE
    bitStream += '0'*rem
    numBits +=rem

    msg = []
    for i in range(numBits, 0, -8):
        bits = bitStream[i-8:i][::-1]
        msg.insert(0, convBitsToChr(bits))
    return ''.join(msg)
#---end function


#Interpret a boolF code, given a list of commands (in codeTape) as well as 
# zero or more input characters (in inputStream)
def boolfuck(codeTape, inputStream="") ->str:

    inputTape  = formatInputStream(inputStream)
    bracketPos = populateJumpTable(codeTape)

    regPtr, registerBank = 0, [0]
    outStream = ''
    codePtr = 0

    while codePtr < len(codeTape):        #While there are still commands....
        cmd = codeTape[codePtr]           #get the current command to execute
        if cmd == '>':                    #move to register to the right
            regPtr += 1
            if regPtr >= len(registerBank):
                registerBank.append(0)
        elif cmd == '<':                  #move to register to the left
            regPtr -= 1
            if regPtr < 0:
                registerBank.insert(0, 0)
        elif cmd == '+':                  #flip bit at current register
            if registerBank[regPtr] == 1:
                registerBank[regPtr] = 0
            else:
                registerBank[regPtr] = 1
        elif cmd == ';':
            outStream += str(registerBank[regPtr])
        elif cmd == ',':
            if len(inputTape) > 0:                          #Still have input...
                registerBank[regPtr] = int(inputTape[0])    #read the front bit
                inputTape = inputTape[1:]                   #"pop" the front bit
            else:
                registerBank[regPtr] = 0                    #no more input: return 0
        elif cmd == '[':                                    #Jump to the right...
            if registerBank[regPtr] == 0:                   #only if current register is 0
                codePtr = bracketPos[codePtr]
        elif cmd == ']':                                    #Jump to the left...
            if registerBank[regPtr] != 0:                   #only if register is not 0
                codePtr = bracketPos[codePtr]
        else:                                               #unrecogonized command
            pass
        codePtr += 1                                        #consume the current command
    #end code loop

    return formatOutput(outStream)
#end function


def brainfuck_to_boolfuck(code):
    boolFCode = ''
    langDict = {'+': '>[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<',
                '-': '>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<',
                '<': '<<<<<<<<<',
                '>': '>>>>>>>>>',
                ',': '>,>,>,>,>,>,>,>,<<<<<<<<',
                '.': '>;>;>;>;>;>;>;>;<<<<<<<<',
                '[': '>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+<<<<<<<<[>]+<[+<]',
                ']': '>>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>]<[+<]' }
    for cmd in code:
        try:
            boolFCode += langDict[cmd]
        except KeyError:
            raise KeyError("Unknown Cmd")
    return boolFCode
#end function
_____________________________
import re

def boolfuck(code, inp=""):
    
    inp_stack = [*''.join(bin(ord(c))[2:].rjust(8,'0') for c in inp[::-1])]
    code = ''.join(s for s in code if s in '+,;[]<>')
    i,idx,out,stack,d,op=0,0,'',{0:0},{},[]

    for a,b in enumerate(code):
        if b=='[':  op.append(a) 
        if b==']':
            d[a]=_=op.pop()
            d[_]=a

    while i<len(code):
        if   code[i]=='[':  i=d[i] if stack[idx]==0 else i
        elif code[i]==']':  i=d[i] if stack[idx]    else i
        elif code[i]=='+':  stack[idx] ^= 1
        elif code[i]==',':  stack[idx]=int((inp_stack or [0]).pop())
        elif code[i]=='>':  idx+=1;stack[idx]=stack.get(idx,0)
        elif code[i]=='<':  idx-=1;stack[idx]=stack.get(idx,0)
        elif code[i]==';':  out+=str(stack[idx])
        i+=1
    return ''.join(map(lambda s:chr(int(s[::-1],2)),re.findall('.{8}|.+',out)))
_____________________________
from collections import deque

def boolfuck(code, input=""):
    bits_to_read, read_byte, cur_input = 0, 0, 0
    bits_writen, write_byte, output = 0, 0, ""
    
    cur_cell, cells = 0, deque([0])
    cur_cmd, loop = 0, 0
    while cur_cmd >= 0 and cur_cmd < len(code):
        if loop != 0:
            if code[cur_cmd] == '[':
                loop += 1
            elif code[cur_cmd] == ']':
                loop -= 1
            else:
                pass
        
        elif code[cur_cmd] == '+':
            cells[cur_cell] ^= 0x1
        
        elif code[cur_cmd] == ',':
            if bits_to_read == 0:                
                read_byte = ord(input[cur_input]) if cur_input < len(input) else 0
                cur_input = min(cur_input + 1, len(input))
                bits_to_read = 8
            cells[cur_cell] = read_byte & 0x1
            read_byte >>= 1
            bits_to_read -= 1
        
        elif code[cur_cmd] == ';':
            write_byte |= cells[cur_cell] << bits_writen
            bits_writen += 1
            if bits_writen == 8:
                output += chr(write_byte)
                write_byte, bits_writen = 0, 0
        
        elif code[cur_cmd] == '<':
            cur_cell -= 1
            if cur_cell < 0:
                cells.appendleft(0)
                cur_cell += 1
                
        elif code[cur_cmd] == '>':
            cur_cell += 1
            if cur_cell >= len(cells):
                cells.append(0)
        
        elif code[cur_cmd] == '[' and not cells[cur_cell]:
            loop += 1
        elif code[cur_cmd] == ']' and cells[cur_cell]:
            loop -= 1
            
        cur_cmd += 1 if loop >= 0 else -1 
        
    if bits_writen != 0:
        output += chr(write_byte)
    return output
_____________________________
def boolfuck(code, input=""):
    def mover(x, rev = False, y = 1):
        while y != 0:
            x = x + 1 if not rev else x - 1
            y = y + 1 if code[x] == ["[", "]"][rev] else y - 1 if code[x] == ["]", "["][rev] else y
        return x
    for j, _ in enumerate(a:=[f"{ord(x):b}" for x in input]):
        a[j] = a[j].zfill(8)[::-1]
    inp_gen, memory, output, pointer, c = (c for c in ''.join(a)), {}, [], 0, 0
    while 0 <= c < len(code):
        match code[c]:
            case ">": pointer += 1
            case "<": pointer -= 1
            case "+": memory[pointer] = '01'[memory.get(pointer, '0')=='0']
            case ",": memory[pointer] = next(inp_gen, '0')
            case ";": output.append(memory.get(pointer, '0'))
            case "[": c = (mover(c)) if (memory.get(pointer, '0') == '0') else c
            case "]": c = (mover(c, True)) if (memory.get(pointer, '0') != '0') else c
        c += 1
    res = ("".join(output)[::-1]).zfill(len(output) + len(output) % 8)
    return "".join([chr(int(res[i:i+8], 2)) for i in range(0, len(res), 8)])[::-1]
_____________________________
MOVES = {'>' : 1, '<' : -1}

def matching_bracket(code : str, bracket : str, idx : int) -> int:
    brackets = ['[', ']']
    start, end, step = (idx + 1, len(code), 1) if bracket == '[' else (idx - 1, -1, -1)
    stack = []
    for i in range(start, end, step):
        char = code[i]
        if char in brackets:
            if char == bracket:
                stack.append(char)
            else:
                if not stack: return i
                stack.pop()

def read_input(input_ : str):
    stream = list(input_)
    current_byte = list(f'{bin(ord(stream.pop(0)))[2:]:0>8}')
    def get_bit():
        if not current_byte:
            if stream:
                current_byte.extend(list(f'{bin(ord(stream.pop(0)))[2:]:0>8}'))
            else:
                return '0'
        return current_byte.pop()
    return get_bit

def boolfuck(code : str, input_ : str = '' ) -> str:
    output = []
    data = [False]
    pointer = 0
    if input_:
        get_bit = read_input(input_)
    i = 0
    while i < len(code):
        match code[i]:
            case direction if direction in MOVES:
                pointer += MOVES[direction]
                if pointer < 0 or pointer >= len(data):
                    data = [False] + data if pointer < 0 else data + [False]
                    pointer = 0 if pointer < 0 else pointer
            case bracket if bracket in ['[', ']']:
                if (bracket == '[' and not data[pointer]) or (bracket == ']' and  data[pointer]):
                    i = matching_bracket(code, bracket, i)
            case '+':
                data[pointer] = not data[pointer]
            case ',':
                data[pointer] = bool(int(get_bit()))
            case ';':
                output.append(str(int(data[pointer])))
        i += 1
        
    output = [output[i:i + 8] for i in range(0, len(output), 8)]
    output = [chr(int(f"{''.join(byte):0<8}"[::-1], 2)) for byte in output]
    return ''.join(output)
_____________________________
def match_brackets(code):
    opening_brackets = []
    bracket_pairs = []
    for i, c in enumerate(code):
        if c == '[':
            opening_brackets.append(i)
        elif c == ']':
            bracket_pairs.append((opening_brackets.pop(), i))
    return dict(bracket_pairs)

def boolfuck(code, input=""):
    brackets = match_brackets(code)
    memory = [0]
    input = int.from_bytes(bytes(input, 'latin-1'), 'little')
    out = ''
    curr_chr = 0
    i = 0
    mp = 0
    ip = 0
    while ip < len(code):
        inst = code[ip]
        if inst == '>': 
            mp += 1
        elif inst == '<':
            mp -= 1
        elif inst == '+': 
            memory[mp] ^= 1
        elif inst == ',': 
            memory[mp] = input % 2
            input //= 2
        elif inst == ';': 
            curr_chr += memory[mp] * (2 ** i)
            i += 1
            if i == 8:
                i = 0
                out += chr(curr_chr)
                curr_chr = 0
        elif inst == '[' and not memory[mp]: 
            ip = brackets[ip]
        elif inst == ']':
            if memory[mp]: 
                ip = list(brackets.keys())[list(brackets.values()).index(ip)]
        
        if mp < 0:
            memory = [0] + memory
            mp += 1
        elif mp >= len(memory):
            memory.append(0)
        ip += 1
    if i % 8:
        out += chr(curr_chr)
    return out
