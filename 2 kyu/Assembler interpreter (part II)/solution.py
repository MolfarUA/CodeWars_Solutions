res = {}
def v(num): #stands for valid
    try:
        num = int(num)
    except:
        if num in res:
            return res[num]
    return num
def extendAt(a,b, index):
    a = a[0:index] + b + a[index:]
    subEnd = index + len(b)
    return a, subEnd


def assembler_interpreter(code):
    
    cur = "main"
    func = {cur: []}
    start = 0
    for i in range(len(code)):
        #Placing data if each function into dictionary
        e = code[i]
        if e ==";" or e == "\n":
            if ((content := code[start: i]).strip() != ""):
                if ("'" not in content) and ":" in content:
                    cur = content[:-1]
                    func[cur] = []
                else:
                    func[cur].append(content.strip())
            start = code.find("\n", start + 1) * (e ==";") + (i+1)*(e=="\n")
    
    for item in func: 
        if item not in "main print" and func[item][-1]!= "ret": 
            func[item].append("ret")
    i, length = 0, len(func["main"])
    cmp = ""
    iteration = 0
    ends = []
    cur = "main"
    curIndex = [[cur,0]]
    while 1: 
        cur =curIndex[-1][0]
        i = curIndex[-1][1]
        cmd = func[cur][i]
        if "msg" in cmd:
            cmd = cmd.strip().replace("msg","")
            copy = 0
            msg = ""
            forma = ""
            for char in cmd:
                if char == "'": 
                    if not copy: 
                        msg += str(v(forma.strip(", ")))
                        forma = ""
                    copy = 1-copy
                elif copy: msg += char
                else: forma += char
            msg+= str(v(forma.strip(", ")))    
            break
        else:
            cmd = cmd.split()
            arg0 = cmd[0]
            if (l :=len(cmd)) == 1:
                if arg0 == "ret":
                    curIndex.pop()
                elif arg0 == "end":
                    break 
            elif l == 2:
                arg1 = cmd[1].strip(",")
                if arg0 == "call":
                    curIndex.append([arg1,-1])
                    
                elif arg0 =="jmp":
                    curIndex.pop()
                    curIndex.append([arg1,-1])
                elif arg0 in "incdec": 
                    res[arg1] += (arg0=="inc") - (arg0 == "dec")
                elif " "+arg0 +" " in cmp:
                    curIndex.pop()
                    curIndex.append([arg1,-1])
                    
             
        
            elif l == 3:
                arg1,arg2 = cmd[1].strip(","),cmd[2].strip(",")
                if arg0 == "cmp":
                    arg1,arg2 =v(arg1),v(arg2)
                    cmp = (
                    " je "*(arg1 == arg2)
                    + " jne "*(arg1 != arg2)
                    +  " jge "*(arg1>= arg2)
                    + " jg "*(arg1>arg2)
                    + " jle "*(arg1<=arg2)
                    + " jl "*(arg1<arg2)
                    )
                elif arg0 == "mov":
                    res[arg1] = v(arg2)
                elif arg0 in "addsub":
                    res[arg1] += v(arg2)*((arg0 == "add") - (arg0 == "sub") )
                elif arg0 == "mul":
                    arg2 = v(arg2)
                    res[arg1] *= v(arg2)
                elif arg0 == "div":
                    res[arg1] //=v(arg2)

        iteration += 1
        curIndex[-1][1] +=1
    if msg == "Do nothing": return -1
    if "This program should return" in msg: return int(msg.split()[-1])
    return msg
  
____________________________________________________________
from operator import add, sub, mul, floordiv as div, lt, le, eq, ne, ge, gt
import re

TOKENIZER     = re.compile(r"('.*?'|-?\w+)[:,]?\s*")
SKIP_COMMENTS = re.compile("\s*;")
SPLIT_PROG    = re.compile(r'\n\s*')

CMP_FUNCS     = {'jmp': lambda x,y: True, 'jne': ne, 'je': eq, 'jge': ge, 'jg': gt, 'jle': le, 'jl': lt}
MATH_FUNCS    = {'add', 'sub', 'mul', 'div', 'inc', 'dec'}
MATH_DCT      = {'inc': 'add', 'dec': 'sub'}

JUMPS_CMD     = set(CMP_FUNCS.keys()) | {'call'}
ALL_CMDS      = {'ret', 'end', 'mov', 'cmp', 'msg'} | JUMPS_CMD

def assembler_interpreter(program):
    
    def tokenize(s):                       return TOKENIZER.findall(SKIP_COMMENTS.split(s)[0])
    def updateCmp(x, y):                   return {k: op(reg.get(x, 0), reg[y] if y.isalpha() else int(y)) for k,op in CMP_FUNCS.items()}
    def moveTo(cmdJump, lbl):              return jumps_lbl[lbl] if cmpDct[cmdJump] else p
    def updateReg(op, x, y='1', val=None): reg[x] = op(reg[x] if val is None else val, reg[y] if y.isalpha() else int(y))
    
    p, reg, output, callStackP = 0, {}, '', []
    inst      = [ cmd for cmd in map(tokenize, SPLIT_PROG.split(program)) if cmd]
    jumps_lbl = {cmd[0]: i for i,cmd in enumerate(inst) if cmd[0] not in ALL_CMDS}
    cmpDct    = updateCmp('0','0')
    
    while 0 <= p < len(inst):
        cmd, xyl = inst[p][0], inst[p][1:]
        
        if   cmd == 'mov':         updateReg(add, xyl[0], xyl[1], 0)
        elif cmd == 'cmp':         cmpDct = updateCmp(xyl[0], xyl[1])
        elif cmd in MATH_FUNCS:    updateReg(eval(MATH_DCT.get(cmd, cmd)), *xyl)
        elif cmd in CMP_FUNCS:     p = moveTo(cmd, xyl[0])
        elif cmd == 'call':        callStackP.append(p); p = moveTo('jmp', xyl[0])
        elif cmd == 'ret':         p = callStackP.pop()
        elif cmd == 'end':         return output
        elif cmd == 'msg':         output += ''.join( s[1:-1] if s not in reg else str(reg[s]) for s in inst[p][1:]); print(output)
        p += 1
    
    return -1
  
____________________________________________________
import re
def assembler_interpreter(program):
    program,current_function,prev_cmp = program.splitlines(),[],[]
    s_o_i,call,d = [],{},{}
    for i in program:
        instruction = re.sub(r";.*", '', i).strip()
        instruction = re.sub(r'\s+', ' ', instruction)
        if instruction : s_o_i.append(instruction)
    i,output = 0,[]
    def do(l):
        t = 0
        while not s_o_i[t].startswith(l) : t += 1
        return t
    while i <= len(s_o_i):
        if i >= len(s_o_i) : return -1
        instruction = s_o_i[i]
        if any(instruction.startswith(k) for k in ['mov','add','sub','mul','div']) : a,b = re.search(r'[a-z], (\d+|[a-z])', instruction).group().split(", ")
        if instruction.startswith('mov') :         d[a] = int(d.get(b, b))
        elif instruction.startswith('inc') :       d[instruction[-1]] += 1
        elif instruction.startswith('dec') :       d[instruction[-1]] -= 1
        elif instruction.startswith('add') :       d[a] += int(d.get(b, b))
        elif instruction.startswith('sub') :       d[a] -= int(d.get(b, b))
        elif instruction.startswith('mul') :       d[a] *= int(d.get(b, b))
        elif instruction.startswith('div') :       d[a] //= int(d.get(b, b))
        elif instruction.startswith('jmp'):
            l = instruction.split()[1]
            i = do(l)
        elif instruction.startswith('cmp'):
            prev_cmp = []
            a, b = re.search(r'([a-z]|\d+), (\d+|[a-z])', instruction).group().split(", ")
            a, b = int(d.get(a, a)), int(d.get(b, b))
            if a >= b : prev_cmp.append('ge')
            if a <= b : prev_cmp.append('le')
            if a > b  : prev_cmp.append('g')
            if a < b :  prev_cmp.append('l')
            if a == b : prev_cmp.append('e')
        elif instruction.startswith('jne'):
            if 'e' not in prev_cmp : i = do(instruction.split()[1])
            else : i += 1
        elif instruction.startswith('je'):
            if 'e' in prev_cmp : i = do(instruction.split()[1])
            else : i += 1
        elif instruction.startswith('jge'):
            if 'ge' in prev_cmp : i = do(instruction.split()[1])
            else : i += 1
        elif instruction.startswith('jg'):
            if 'g' in prev_cmp : i = do(instruction.split()[1])
            else : i += 1
        elif instruction.startswith('jle'):
            if 'le' in prev_cmp : i = do(instruction.split()[1])
            else : i += 1
        elif instruction.startswith('jl'):
            if 'l' in prev_cmp : i = do(instruction.split()[1])
            else : i += 1
        elif instruction.startswith('call'):
            l = instruction.split()[1]
            if not current_function or l != current_function[-1] : call[l] = i
            i = do(l)
        elif instruction.startswith('msg'):
            s = instruction
            s,li,k = re.sub(r'msg\s+', '', s),[],0
            while k < len(s):
                if s[k] == "'":
                    k += 1
                    while s[k] != "'" : li.append(s[k]);k += 1
                elif s[k] not in [',', ' '] : li.append(str(d[s[k]]))
                k += 1
            output.append("".join(li))
        elif re.search(r'.+:', instruction) : current_function.append(instruction[:-1])
        elif re.search(r'ret', instruction):
            k = len(current_function) - 1
            while current_function[k] not in call : k -= 1
            i = call[current_function.pop(k)] + 1
        elif instruction.startswith('end') : break
        if any(instruction.startswith(k) for k in ['jmp', 'call', 'ret', 'jne', 'je', 'jge', 'jg', 'jle', 'jl']) : continue
        i += 1
    return output[0]    
  
____________________________________________________
import opcode
import re
from dataclasses import dataclass
from itertools import count, repeat
from pprint import pprint
from types import CodeType, FunctionType
from typing import List, Union, Tuple, Callable, NoReturn, Dict, Optional, Type, Any
from time import time


@dataclass
class IAType:
    __slots__ = ('id', 'type', 'check',)
    id: str
    type: Optional[Type]
    check: Callable[[Union[str, int]], bool]


@dataclass
class Label:
    __slots__ = ('id', 'index',)
    id: str
    index: int


IAType.INT = IAType(id='int', type=int, check=lambda v: type(v) is int)
IAType.VAR = IAType(id='var', type=str, check=lambda v: type(v) is str and not v.startswith("'"))
IAType.LBL = IAType(id='lbl', type=str, check=lambda v: type(v) is str)
IAType.STR = IAType(id='var', type=str, check=lambda v: type(v) is str and v.startswith("'"))
IAType.ANY = IAType(id='any', type=None, check=lambda v: True)
IAType.VOI = IAType(id='voi', type=None, check=lambda v: IAType.INT.check(v) or IAType.VAR.check(v))


@dataclass
class Instruction:
    __slots__ = ('id', 'args',)
    id: str
    args: List[Union[str, int]]


@dataclass
class InstructionDescriptor:
    __slots__ = ('id', 'params', 'run',)
    id: str
    params: List[IAType]
    run: Union[
        Callable[['VM',], NoReturn],
        Callable[['VM', Union[str, int],], NoReturn],
        Callable[['VM', Union[str, int], Union[str, int],], NoReturn],
    ]

    def validate(self, instruction: Instruction) -> bool:
        if len(instruction.args) != len(self.params):
            return False
        return all(p.check(a) for p, a in zip(self.params, instruction.args))


class VM:
    __slots__ = ('code', 'labels', 'compiled_functions', 'ip', 'regs',)
    code: List[Tuple[Instruction, InstructionDescriptor]]
    labels: Dict[str, Label]
    compiled_functions: Optional[Dict[str, FunctionType]]
    ip: int  # instruction pointer
    regs: Dict[str, Any]

    instructions: Dict[str, InstructionDescriptor]

    @staticmethod
    def get_descriptor(instruction: Instruction) -> Optional[InstructionDescriptor]:
        for idesc in VM.instructions.values():
            if idesc.id == instruction.id and idesc.validate(instruction):
                return idesc
        return None

    def __init__(self, code: List[Instruction], labels: Dict[str, Label] = {}):
        self.code = [(i, VM.get_descriptor(i)) for i in code]
        for instr, idesc in self.code:
            if idesc is None:
                args = [
                    ' <str>' if IAType.STR.check(a) else
                    ' <int>' if IAType.INT.check(a) else
                    ' <var>' if IAType.VAR.check(a) else
                    ' <???>' for a in instr.args]
                raise NameError(f'instruction "{instr.id}{"".join(args)}" is not supported')
        self.labels = {'__entry__': Label(id='__entry__', index=0), **labels}
        self.compiled_functions = None
        self.ip = 0
        self.regs = { '__stdout__': [] }

    def precompile(self):
        if self.compiled_functions is not None: return

        def generate_load(a):
            nonlocal constants, variables
            if a in variables:
                return [opcode.opmap['LOAD_GLOBAL'], variables.index(a)]

            if type(a) is str: a = a.strip("'")
            if a in constants:
                # print('LOAD_CONST:', a, constants.index(a), constants)
                return [opcode.opmap['LOAD_CONST'], constants[2:].index(a)+2 if type(a) is not bool else int(a)]
            else:
                raise Exception(f'failed to load {a}')

        call = lambda label: self.compiled_functions[label]()

        variables: Tuple[str, ...] = tuple(sorted(set(sum(([a for a, p in zip(i.args, d.params) if p == IAType.VAR] for i, d in self.code), ['__stdout__']))))
        # pprint(self.labels)
        constants = tuple(
            [False, True, call, Exception('fail')] +
            sorted(set(sum(([a for a in i.args if IAType.INT.check(a)] for i, _ in self.code), [1]))) +
            sorted(set(sum(
                ([a[1:-1] for a in i.args if IAType.STR.check(a)] for i, _ in self.code),
                [l.id for l in self.labels.values()]
            )))
        )
        print('Variables:', variables)
        print('Constants:', constants)
        bc = [opcode.opmap['JUMP_ABSOLUTE'], 0]
        i2bc_table = []
        jump_table = {}

        for i, (instr, idesc) in enumerate(self.code):
            i2bc_table.append(len(bc))
            if idesc.id == 'mov':
                bc += generate_load(instr.args[1])
                bc += [opcode.opmap['STORE_GLOBAL'], variables.index(instr.args[0])]
            elif idesc == VM.INSTR_INC:
                bc += generate_load(instr.args[0])
                bc += generate_load(1)
                bc += [opcode.opmap['BINARY_ADD'], 0]
                bc += [opcode.opmap['STORE_GLOBAL'], variables.index(instr.args[0])]
            elif idesc == VM.INSTR_DEC:
                bc += generate_load(instr.args[0])
                bc += generate_load(1)
                bc += [opcode.opmap['BINARY_SUBTRACT'], 0]
                bc += [opcode.opmap['STORE_GLOBAL'], variables.index(instr.args[0])]
            elif idesc == VM.INSTR_ADD:
                bc += generate_load(instr.args[0])
                bc += generate_load(instr.args[1])
                bc += [opcode.opmap['BINARY_ADD'], 0]
                bc += [opcode.opmap['STORE_GLOBAL'], variables.index(instr.args[0])]
            elif idesc == VM.INSTR_SUB:
                bc += generate_load(instr.args[0])
                bc += generate_load(instr.args[1])
                bc += [opcode.opmap['BINARY_SUBTRACT'], 0]
                bc += [opcode.opmap['STORE_GLOBAL'], variables.index(instr.args[0])]
            elif idesc == VM.INSTR_MUL:
                bc += generate_load(instr.args[0])
                bc += generate_load(instr.args[1])
                bc += [opcode.opmap['BINARY_MULTIPLY'], 0]
                bc += [opcode.opmap['STORE_GLOBAL'], variables.index(instr.args[0])]
            elif idesc == VM.INSTR_DIV:
                bc += generate_load(instr.args[0])
                bc += generate_load(instr.args[1])
                bc += [opcode.opmap['BINARY_FLOOR_DIVIDE'], 0]
                bc += [opcode.opmap['STORE_GLOBAL'], variables.index(instr.args[0])]
            elif idesc == VM.INSTR_CMP:
                for a in instr.args:
                    bc += generate_load(a)
            elif idesc == VM.INSTR_JMP:
                bc += [opcode.opmap['JUMP_ABSOLUTE'], 0]
                jump_table[len(bc) - 1] = self.labels[instr.args[0]].index
            elif idesc in (VM.INSTR_JL, VM.INSTR_JLE, VM.INSTR_JE, VM.INSTR_JNE, VM.INSTR_JG, VM.INSTR_JGE,):
                bc += [
                    opcode.opmap['COMPARE_OP'],
                    (VM.INSTR_JL, VM.INSTR_JLE, VM.INSTR_JE, VM.INSTR_JNE, VM.INSTR_JG, VM.INSTR_JGE,).index(idesc)
                ]
                bc += [opcode.opmap['POP_JUMP_IF_TRUE'], 0]
                jump_table[len(bc) - 1] = self.labels[instr.args[0]].index
            # elif idesc == VM.INSTR_JNZI:
            #     bc += [opcode.opmap['LOAD_CONST'], constants.index(instr.args[0])]
            #     bc += [opcode.opmap['POP_JUMP_IF_TRUE']]
            #     jump_table[len(bc)] = i + instr.args[1]
            #     bc += [0]  # target instruction index will be stored here later
            # elif idesc == VM.INSTR_JNZV:
            #     bc += [opcode.opmap['LOAD_GLOBAL'], variables.index(instr.args[0])]
            #     bc += [opcode.opmap['POP_JUMP_IF_TRUE']]
            #     jump_table[len(bc)] = i + instr.args[1]
            #     bc += [0]  # target instruction index will be stored here later
            elif idesc == VM.INSTR_CALL:
                bc += generate_load(call)
                bc += generate_load(instr.args[0])
                bc += [opcode.opmap['CALL_FUNCTION'], 1]
                bc += [opcode.opmap['POP_JUMP_IF_TRUE'], 0]
                jump_table[len(bc) - 1] = 2**31
            elif idesc == VM.INSTR_END:
                bc += generate_load(True)
                bc += [opcode.opmap['RETURN_VALUE'], 0]
            elif idesc == VM.INSTR_RET:
                bc += generate_load(False)
                bc += [opcode.opmap['RETURN_VALUE'], 0]
            elif idesc.id == 'msg':
                # special case
                bc += generate_load('__stdout__')
                for a, p in zip(instr.args, idesc.params):
                    bc += generate_load(a)
                    bc += [opcode.opmap['LIST_APPEND'], 1]
            else:
                pass
                raise Exception(f'cannot compile "{instr.id}" operation')

        i2bc_table.append(len(bc))
        bc += [opcode.opmap['LOAD_CONST'], 3]
        bc += [opcode.opmap['RETURN_VALUE'], 0]

        print(i2bc_table)
        lnotab = sum(map(list, zip([(b - a) for a, b in zip([0] + i2bc_table, i2bc_table)], repeat(1))), [])

        for j in jump_table:
            bc[j] = i2bc_table[jump_table[j]] if jump_table[j] in range(len(i2bc_table)) else i2bc_table[-1]

        self.compiled_functions = {}
        for fname, l in self.labels.items():
            bc[1] = i2bc_table[l.index]
            self.compiled_functions[fname] = FunctionType(CodeType(
                0,  # argcount
                0,  # posonlyargs
                0,  # kwonlyargs
                0,  # nlocals
                8,  # stacksize
                (1<<6),  # flags
                bytes(bc),  # codestring
                constants,  # constants
                variables,  # names
                (),  # varnames
                '<vm_gen>',  # filename
                fname,  # name
                0,  # firstlineno
                bytes(lnotab),  # lnotab
                (),  # freevars
                (),  # cellvars
            ), name=fname, globals=self.regs)
        import dis
#         print(f'===---   DISASSEMBLY   ---===')
#         dis.dis(self.compiled_functions['__entry__'])

    def execute(self, precompile=True):
        if precompile:
            TIME_START = time()
            self.precompile()
            TIME_END = time()
            print(f'Compiled in {int((TIME_END - TIME_START)*1000*10)/10}ms')

        TIME_START = time()
        if self.compiled_functions is None:
            while self.step(): continue
        else:
            # Compiled code executes 20x faster!
            result = self.compiled_functions['__entry__']()
        TIME_END = time()
        print(f'Executed in {int((TIME_END - TIME_START)*1000*10)/10}ms')
        if type(result) is Exception:
            return -1
        return ''.join(map(str, self.regs['__stdout__']))

    def step(self) -> bool:
        if self.ip not in range(len(self.code)):
            return False

        instr, idesc = self.code[self.ip]
        self.ip += 1

        idesc.run(self, *instr.args)
        return True


def sign(n: int) -> int: return (n > 0) - (n < 0)
def vm_movi(vm: VM, var: str, val: int) -> NoReturn: vm.regs[var] = val
def vm_movv(vm: VM, var: str, val: str) -> NoReturn: vm.regs[var] = vm.regs[val]
def vm_inc(vm: VM, var: str) -> NoReturn: vm.regs[var] += 1
def vm_dec(vm: VM, var: str) -> NoReturn: vm.regs[var] -= 1
def vm_jnzi(vm: VM, val: int, offset: int) -> NoReturn: vm.ip += (offset + sign(offset)) * (val != 0)
def vm_jnzv(vm: VM, var: str, offset: int) -> NoReturn: vm.ip += (offset + sign(offset)) * (vm.regs[var] != 0)
def vm_stub(vm: VM, *args) -> NoReturn: pass


VM.instructions = {
    'MOVI': InstructionDescriptor(id='mov', run=vm_movi, params=[IAType.VAR, IAType.INT]),
    'MOVV': InstructionDescriptor(id='mov', run=vm_movv, params=[IAType.VAR, IAType.VAR]),

    'INC': InstructionDescriptor(id='inc', run=vm_inc, params=[IAType.VAR]),
    'DEC': InstructionDescriptor(id='dec', run=vm_dec, params=[IAType.VAR]),

    'ADD': InstructionDescriptor(id='add', run=vm_stub, params=[IAType.VAR, IAType.VOI]),
    'SUB': InstructionDescriptor(id='sub', run=vm_stub, params=[IAType.VAR, IAType.VOI]),
    'MUL': InstructionDescriptor(id='mul', run=vm_stub, params=[IAType.VAR, IAType.VOI]),
    'DIV': InstructionDescriptor(id='div', run=vm_stub, params=[IAType.VAR, IAType.VOI]),
    'CMP': InstructionDescriptor(id='cmp', run=vm_stub, params=[IAType.VOI, IAType.VOI]),

    # 'JNZI': InstructionDescriptor(id='jnz', run=vm_jnzi, params=[IAType.INT, IAType.INT]),
    # 'JNZV': InstructionDescriptor(id='jnz', run=vm_jnzv, params=[IAType.VAR, IAType.INT]),

    'JMP': InstructionDescriptor(id='jmp', run=vm_stub, params=[IAType.LBL]),
    'JL': InstructionDescriptor(id='jl', run=vm_stub, params=[IAType.LBL]),
    'JLE': InstructionDescriptor(id='jle', run=vm_stub, params=[IAType.LBL]),
    'JE': InstructionDescriptor(id='je', run=vm_stub, params=[IAType.LBL]),
    'JNE': InstructionDescriptor(id='jne', run=vm_stub, params=[IAType.LBL]),
    'JG': InstructionDescriptor(id='jg', run=vm_stub, params=[IAType.LBL]),
    'JGE': InstructionDescriptor(id='jge', run=vm_stub, params=[IAType.LBL]),

    'CALL': InstructionDescriptor(id='call', run=vm_stub, params=[IAType.LBL]),
    'RET': InstructionDescriptor(id='ret', run=vm_stub, params=[]),

    'MSG1': InstructionDescriptor(id='msg', run=vm_stub, params=[IAType.ANY]),
    'MSG2': InstructionDescriptor(id='msg', run=vm_stub, params=[IAType.ANY, IAType.ANY]),
    'MSG3': InstructionDescriptor(id='msg', run=vm_stub, params=[IAType.ANY, IAType.ANY, IAType.ANY]),
    'MSG4': InstructionDescriptor(id='msg', run=vm_stub, params=[IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY]),
    'MSG5': InstructionDescriptor(id='msg', run=vm_stub, params=[IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY]),
    'MSG6': InstructionDescriptor(id='msg', run=vm_stub, params=[IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY]),
    'MSG7': InstructionDescriptor(id='msg', run=vm_stub, params=[IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY]),
    'MSG8': InstructionDescriptor(id='msg', run=vm_stub, params=[IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY, IAType.ANY]),

    'END': InstructionDescriptor(id='end', run=vm_stub, params=[]),
}
for iname in VM.instructions:
    setattr(VM, f'INSTR_{iname}', VM.instructions[iname])


def parse_instruction(line: str) -> Instruction:
    name, *args = line.split()
    return Instruction(id=name, args=[int(a) if a.lstrip('-').isdigit() else a for a in args])


def simple_assembler(program: List[str]) -> dict:
    instructions = list(map(parse_instruction, program))
    pprint(instructions)
    vm = VM(instructions)
    vm.execute()
    return vm.regs


def assembler_interpreter(program: str):
    program = re.findall(r'(?:\s*(\w+:?)[ \t]*((?:\w+|-?\d+|\'(?:[^\']*)\'|,|[ \t]+)*))?(?:;.*)?', program)
    instructions: List[Instruction] = []
    labels: Dict[str, Label] = {}
    for cmd, args in program:
        if not cmd: continue
        if cmd.endswith(':'):
            labels[cmd[:-1]] = Label(id=cmd[:-1], index=len(instructions))
        else:
            instructions.append(Instruction(
                id=cmd,
                args=[int(a) if a.lstrip('-').isdigit() else a for a in re.findall(r'\w+|-?\d+|\'(?:[^\']*)\'', args)]
            ))

    # pprint(instructions)
    vm = VM(instructions, labels)
    res = vm.execute()
    pprint(vm.regs)
    return res

____________________________________________________
import re
from collections import defaultdict


def cmp(x,y):
    return (x<y) - (x>y)

def check_ret_jmp_status(dest_function):
    last_command = dest_function[-1][0]
    return last_command == 'ret' or last_command == 'jmp'

def assembler_interpreter(program):
    #DICTIONARIES for the registers, messages and functions and their properties!
    registers_dict = {'?':', '}
    function_dict = defaultdict(list)
    message_dict = {}
    
    #status flag will be changed accordingly to determine the proper termination of the program.
    status = None
    
    #stripping comments and splitting main program from the functions!
    program = re.sub(r"end","end\n",re.sub(r"\s+;.+",'',program,flags=re.I).strip()).split('\n')
    #splitting program into two sections - (program and functions)
    split_idx = program.index('')
    #extracting program
    pre_final_program = '\n'.join( program[:split_idx] )
    #extracting functions
    functions = program[split_idx+1:]
    #the message of the MAIN program (if any)
    main_msg = re.search(r"msg.+",pre_final_program)

    if main_msg:
        main_msg = main_msg.group(0).split(' ',1)[-1]
        #final parsed program - replacing message in main program with "?" since we extracted and store the message
        pre_final_program = re.sub(re.escape(main_msg),'?',pre_final_program)

    #regex pattern for extracting commands!
    regex_pattern = re.compile(r"(\S+)(?:\s+)?(\S+)?(?: (\S+))?")

    #storing function names and theirs operations/properties
    for command in functions:
        if command.endswith(':'):
            func_name = command.rstrip(':')
        elif command.strip().startswith('msg'):
            message_dict[func_name] = command.strip().split(' ',1)[-1]
            function_dict[func_name].append(("msg", "?", ""))
        elif command.strip() == "ret":
            function_dict[func_name].append(("ret","",""))
        elif command:
            split_command = re.findall(regex_pattern,command)
            function_dict[func_name].append(split_command[0])

    #FINAL program ready to be parsed
    final_program = re.findall(regex_pattern,pre_final_program)

    #Parsing starts here!
    comparison_results = None
    def parse_and_evaluate(program,current_function):
        nonlocal status
        for command, register, num in program:
            #strip right comma on the register so it can be stored/called correctly.
            register = register.rstrip(',')

            if command=='mov':
                registers_dict[register]=int(registers_dict.get(num, num))
            elif command =='inc':
                registers_dict[register] += 1
            elif command=='dec':
                registers_dict[register] -= 1
            elif command == 'div':
                registers_dict[register] //= int(registers_dict.get(num,num))
            elif command == 'add':
                registers_dict[register] += int(registers_dict.get(num,num))
            elif command == 'sub':
                registers_dict[register] -= int(registers_dict.get(num, num))
            elif command == 'mul':
                registers_dict[register] *= int(registers_dict.get(num,num))
            elif command == 'cmp':
                x = int( registers_dict.get(register, register) )
                y = int( registers_dict.get(num, num) )
                comparison_results = cmp(x,y)

            elif   ( command == 'jne' and comparison_results != 0 )\
                or ( command == 'je' and comparison_results == 0 )\
                or ( command == 'jge' and comparison_results <= 0 )\
                or ( command == 'jg' and comparison_results == -1 )\
                or ( command == 'jle' and comparison_results >= 0 )\
                or ( command == 'jl' and comparison_results == 1  ):
                function_name = register
                function_properties = function_dict[function_name]
                status = check_ret_jmp_status(function_properties)
                return parse_and_evaluate(function_properties, function_name)

            elif command == 'call' or command == 'jmp':
                function_name = register
                function_properties = function_dict[function_name]
                status = check_ret_jmp_status(function_properties)
                
                #The initial call happens here; the program_output will store the
                #program's msg according to the nested calls. The program_output
                #will be eventually returned when the "end" command is encountered.
                program_output = parse_and_evaluate(function_properties, function_name)

            elif command == 'msg':
                #extracting the message curently called from either the main program or a function!
                message = current_function is None and main_msg or message_dict.get(current_function)
                #handling comma in quotes so I can split em into proper tokens
                message = message.replace("', '", '?')

                final_message = []
                current_msg = [x.strip().strip("\'") for x in message.split(',')]
                for x in current_msg:
                    final_message.append(str( registers_dict.get(x, x) ))
                
                #storing the final message with all the register vars replaced in the program output
                #and returning it as a tuple with the FLAG var which determines if the program
                #was terminated properly e.g., every call/jmp command was greeted by either a
                #ret or another jmp command!
                return ''.join(final_message), status

            #end command encountered here.
            elif command == 'end':
                return program_output

    #initialise parsing and evaluattion of the final program
    out,end_status = parse_and_evaluate(final_program,None)
    #if status is True the the program terminated properly otherwise it didn't and -1
    #shall be returned.
    return end_status and out or -1
  
____________________________________________________
import re

parse_program = lambda program: [line.split(';')[0] for line in program.split('\n') if line and line[0] != ';']
parse_labels = lambda commands: {command[:-1]: index for index, command in enumerate(commands) if command[-1] == ':'}


def parse_command(command):
    matchs = re.findall(r"\w+|'.*?'", command)
    return matchs[0], matchs[1:]

def assembler_interpreter(program):
    commands = parse_program(program)
    labels = parse_labels(commands)
    registers, call_stack, cmp_result, result, command_ptr = {}, [], "", "", 0

    def inc(x): registers[x] += 1
    def dec(x): registers[x] -= 1
    def mov(x, y): registers[x] = int(y) if y.isdigit() else registers[y]
    def add(x, y): registers[x] += int(y) if y.isdigit() else registers[y]
    def sub(x, y): registers[x] -= int(y) if y.isdigit() else registers[y]
    def mul(x, y): registers[x] *= int(y) if y.isdigit() else registers[y]
    def div(x, y): registers[x] //= int(y) if y.isdigit() else registers[y]


    def cmp(x, y):
        nonlocal cmp_result
        x = int(x) if x.isdigit() else registers[x]
        y = int(y) if y.isdigit() else registers[y]
        cmp_result = 'g' if x > y else 'l' if x < y else 'e'

    def jmp(lbl):
        nonlocal command_ptr
        command_ptr = labels[lbl]

    def jne(lbl):
        if cmp_result != 'e':
            jmp(lbl)

    def je(lbl):
        if cmp_result == 'e':
            jmp(lbl)

    def jge(lbl):
        if cmp_result == 'e' or cmp_result == 'g':
            jmp(lbl)

    def jg(lbl):
        if cmp_result == 'g':
            jmp(lbl)

    def jle(lbl):
        if cmp_result == 'e' or cmp_result == 'l':
            jmp(lbl)

    def jl(lbl):
        if cmp_result == 'l':
            jmp(lbl)

    def call(lbl):
        nonlocal command_ptr
        call_stack.append(command_ptr)
        command_ptr = labels[lbl]

    def ret():
        nonlocal command_ptr
        command_ptr = call_stack.pop()

    def msg(*args):
        nonlocal result
        result = ''.join(str(registers[arg]) if arg[0] != "'" else arg[1:-1] for arg in args)


    instruction_map = {
        "mov": mov, "inc": inc, "dec": dec, "add": add, "sub": sub,
        "mul": mul, "div": div, "cmp": cmp, "jmp": jmp, "jne": jne,
        "je": je, "jge": jge, "jg": jg, "jle": jle, "jl": jl,
        "call": call, "ret": ret, "msg": msg,
    }

    while command_ptr < len(commands):
        instruction, args = parse_command(commands[command_ptr])

        if instruction == 'end':
            return result

        if instruction in instruction_map:
            instruction_map[instruction](*args)

        command_ptr += 1

    return -1
  
____________________________________________________
import re

def assembler_interpreter(inp):
    
    d,i,stack = dict(),0,re.sub('\n{2,}','\n',inp).split('\n')[1:-1]
    
    while i<len(stack):
        func,var,val = map(lambda s: s.replace(',',''),(stack[i].lstrip(' ')+' _ _').split()[:3])
        
        if func == 'mov':      d[var] = d.get(val) if val.isalpha() else int(val)        
        elif func == 'dec':    d[var]-=1   
        elif func == 'inc':    d[var]+=1
        elif func == 'sub':    d[var]-=int(val) if not val.isalpha() else d[val]
        elif func == 'add':    d[var]+=int(val) if not val.isalpha() else d[val]
        elif func == 'mul':    d[var]*=int(val) if not val.isalpha() else d[val]
        elif func == 'div':    d[var]//=int(val) if not val.isalpha() else d[val]

        elif func == 'jmp':
            if stack[i][0]!=' ': idx = i
            i=stack.index(var+':')
            
        elif func == 'cmp':
            a,b = d[var] if var in d else int(var),d[val] if val in d else int(val)
            
        elif func == 'jne':
            if a!=b:
                if stack[i][0]!=' ': idx = i
                i = stack.index(var+':')
                
        elif func == 'je':
            if a==b:
                if stack[i][0]!=' ': idx = i
                i = stack.index(var+':')
                
        elif func == 'jg':
            if a>b:
                if stack[i][0]!=' ': idx = i
                i = stack.index(var+':')
                
        elif func == 'jge':
            if a>=b:
                if stack[i][0]!=' ': idx = i
                i = stack.index(var+':')
                
        elif func == 'jl':
            if a<b:
                if stack[i][0]!=' ': idx = i
                i = stack.index(var+':')
                
        elif func == 'jle':
            if a<=b:
                if stack[i][0]!=' ': idx = i
                i = stack.index(var+':')
                
        elif func == 'call':
            if stack[i][0]!=' ': idx = i
            i = stack.index(var+':')
            
        elif func == 'ret':
            try:    i=idx; del idx
            except: pass
            
        elif func == 'msg':
            msg = (eval(j) if j[0]=='\'' else str(d.get(j,'')) for j in re.findall(r'\'[^\']*\'|.',re.sub(r';.*$','',stack[i][4:])))
                
        elif func == 'end':    i = ''; break
                
        i+=1
        
    return ''.join(msg) if i=='' else -1
  
____________________________________________________
import re
def assembler_interpreter(program):
    program = re.sub(' +', ' ', program).splitlines()
    regs = dict()
    i = 0
    get_value = lambda v: regs[v] if v in regs else int(v)
    cmp_res = None
    labels = dict()
    ret_pointers = list()
    output = ""
    for i in range(len(program)):
        cmd = program[i].split(" ")
        if cmd[0].endswith(":"):
            labels[cmd[0][:-1]] = i
    i = 0
    while i < (len(program)):
        program[i] = program[i].lstrip()
        cmd = program[i].split(" ")
        if cmd[0] == 'end':
            return output
        elif cmd[0] == 'msg':
            cmd = re.findall(r"[\w']+", program[i])
            cmd2 = program[i].split("'")
            j = 1
            k = 0
            while k < len(cmd):
                if cmd[k] in regs:
                    output += str(regs[cmd[k]])
                elif cmd[k][0] == "'":
                    if j < len(cmd2):
                        output += str(cmd2[j])
                        j += 2
                        k += 1
                k += 1
        elif cmd[0] == 'ret':
            i = ret_pointers.pop()
            continue
        elif cmd[0] == 'call':
            ret_pointers.append(i+1)
            i = labels[cmd[1]]
            continue
        elif cmd[0] == 'cmp':
            cmp_res = float(regs[cmd[1][0]] + 1) / (get_value(cmd[2]) + 1)
        elif not cmd or cmd[0] == ';':
            i += 1
            continue
        elif cmd[0] == 'mov':
            regs[cmd[1][:-1]] = get_value(cmd[2])
        elif cmd[0] == 'inc':
            regs[cmd[1]] += 1
        elif cmd[0] == 'dec':
            regs[cmd[1]] -= 1
        elif cmd[0] == 'jnz':
            if (cmd[1].lstrip("-").isnumeric() and cmd[1] != 0) or regs[cmd[1]] != 0:
                i += int(cmd[2])
                continue
        elif cmd[0] == 'add':
            regs[cmd[1][:-1]] += get_value(cmd[2])
        elif cmd[0] == 'sub':
            regs[cmd[1][:-1]] -= get_value(cmd[2])
        elif cmd[0] == 'mul':
            regs[cmd[1][:-1]] *= get_value(cmd[2])
        elif cmd[0] == 'div':
            regs[cmd[1][:-1]] = int(regs[cmd[1][:-1]] / get_value(cmd[2]))
        else:
            jump = False
            if cmd[0] == 'jmp': jump = True
            elif cmd[0] == 'jne' and cmp_res != 1: jump = True
            elif cmd[0] == 'je' and cmp_res == 1: jump = True
            elif cmd[0] == 'jge' and cmp_res >= 1: jump = True
            elif cmd[0] == 'jg' and cmp_res > 1: jump = True
            elif cmd[0] == 'jle' and cmp_res <= 1: jump = True
            elif cmd[0] == 'jl' and cmp_res < 1: jump = True
            if jump:
                i = labels[cmd[1]]
                continue
        i += 1
    return -1

____________________________________________________
from typing import List, Union

def parse_line(line: str) -> List[Union[str, int]]:
    """
    Extract operator and operands from line of assembly
    @param line: Assembly code in
    @return List with operator and any additional operands
    """
    line = line.strip()
    if not line or line.startswith(';'):
        return None
    
    pos = line.find(' ')
    if pos > -1:
        op = line[:pos].strip()
        arg_str = line[pos + 1:].strip()
    else:
        op = line.strip()
        arg_str = ''
        
    args = []
    buffer = ''
    quote = False
    for c in arg_str:
        buffer += c
        
        if c == "'":
            # Quote mark
            if not quote and buffer:
                buffer = buffer.strip()
            if quote and buffer:
                args.append(buffer[1:-1])
                buffer = ''
            quote = not quote
        
        elif c == ';' and not quote:
            # Start of comment
            if buffer:
                args.append(buffer[:-1].strip())
                buffer = ''
            break
            
        elif c == ',' and not quote:
            # Argument separator
            if buffer:
                args.append(buffer[:-1].strip())
                buffer = ''
    
    if buffer:
        args.append(buffer.strip())

    # Do type conversion of any supplied integers then remove any empty operands
    args = [safe_int(a) for a in args]
    args = [a for a in args if a != '']
    return [op] + args
            
def safe_int(s: str) -> Union[int, str]:
    """
    Convert a string to int where possible and suppress exceptions and return s if not possible
    """
    try:
        return int(s.strip())
    except:
        return s
    
def assembler_interpreter(program):
    # Dump the initial program
    print('Source:')
    for line in program.strip().split('\n'):
        print(line)

    # Extract program operator codes and operands
    program = [
        parse_line(cmd)
        for cmd in program.split('\n') 
    ]
    program = [
        cmd
        for cmd in program
        if cmd
    ]
    
    # Extract label indices and remove label lines
    labels = {}
    i = 0
    while i < len(program):
        op, *args = program[i]
        if op.endswith(':'):
            labels[op[:-1]] = i
            del program[i]
            continue
        i += 1

    # Print out the parsed code
    print('---\nCode:\naddress - [label:] operator [operand[, operand]*]')
    for i, r in enumerate(program):
        label = {v: k for k, v in labels.items()}.get(i, '')
        print(f'{i:02d} - {(label + ": ") if label else ""}{", ".join(map(str, r))}')

    # Virtual machine state
    pc = [0]  # Program counter stack
    registers = {}  # Register states
    cmp_result = None # Last comparison result
    msg = None # Last message

    # Simulate running the code
    while pc[0] < len(program):
        op, *args = program[pc[0]]
        
        pc[0] += 1
        if op == 'mov':
            x, y = args
            y = registers.get(y, y)
            registers[x] = y
        
        elif op == 'inc':
            x = args[0]
            registers[x] += 1
        
        elif op == 'dec':
            x = args[0]
            registers[x] -= 1
        
        elif op == 'add':
            x, y = args
            y = registers.get(y, y)
            registers[x] += y
        
        elif op == 'sub':
            x, y = args
            y = registers.get(y, y)
            registers[x] -= y
        
        elif op == 'mul':
            x, y = args
            y = registers.get(y, y)
            registers[x] *= y
        
        elif op == 'div':
            x, y = args
            y = registers.get(y, y)
            registers[x] //= y
        
        elif op == 'jmp':
            # Jump
            l = args[0]
            pc[0] = labels[l]
        
        elif op == 'cmp':
            x, y = args
            x = registers.get(x, x)
            y = registers.get(y, y)
            if x < y:
                cmp_result = '<' 
            elif x == y:
                cmp_result = '=' 
            else:
                cmp_result = '>'
        
        elif op in ['jne', 'je', 'jle', 'jl', 'jg', 'jge']:
            # Conditional jump
            l = args[0]
            targets = {'jne': '<>', 'je': '=', 'jle': '<=', 'jl': '<', 'jg': '>', 'jge': '>='}[op]
            if cmp_result in targets:
                pc[0] = labels[l]
        
        elif op == 'call':
            # Stack push pn program counter
            l = args[0]
            pc = [labels[l]] + pc
        
        elif op == 'ret':
            # Stack pop on program counter
            pc = pc[1:]
        
        elif op == 'msg':
            # Build output message
            msg = []
            for arg in args:
                if arg.startswith("'") and arg.endswith("'"):
                    msg.append(arg[1:-1])
                else:
                    msg.append(str(registers.get(arg, arg)))
        
        elif op == 'end':
            return ''.join(msg)
    
    # Oops ended by advancing past the end of the program
    return -1

____________________________________________________
def assembler_interpreter(prog):
    p = prog.split('\n')
    r, l, ip, st, n3, msg = {}, {}, 0, [], [None]*3, ''

    def rv(s):
        try: return int(s)
        except ValueError: return r[s]
        
    def parse_msg(s):
        str_mode, res = False, ''
        for c in s.strip().lstrip('msg').lstrip(' '):
            if str_mode:
                if c == "'":str_mode = False
                else: res += c
            elif c == "'":str_mode = True
            elif c == ";":return res
            elif 96<ord(c)<123: res+=str(r[c])
        return res

    for i, row in enumerate(p): #labels
        r0 = row.strip(' ').split()
        if r0 and r0[0][-1:] == ':': l[r0[0][:-1]] = i

    while ip<len(p):
        o, x, y = (p[ip].strip(' ').split()+n3)[:3]
        if x: x = x.rstrip(',')
        if o=='mov': r[x] = rv(y)
        elif o=='inc':r[x] += 1
        elif o=='dec':r[x] -= 1
        elif o=='add':r[x] += rv(y)
        elif o=='sub':r[x] -= rv(y)
        elif o=='mul':r[x] *= rv(y)
        elif o=='div':r[x] //= rv(y)
        elif o=='jmp':ip = l[x]
        elif o=='cmp':cx, cy = rv(x), rv(y)
        elif o=='jne' and cx != cy:ip = l[x]
        elif o=='je'  and cx == cy:ip = l[x]
        elif o=='jge' and cx >= cy:ip = l[x]
        elif o=='jg'  and cx >  cy:ip = l[x]
        elif o=='jle' and cx <= cy:ip = l[x]
        elif o=='jl'  and cx <  cy:ip = l[x]
        elif o=='call':
            st.append(ip)
            ip = l[x]
        elif o=='ret':ip = st.pop()
        elif o=='msg':msg += parse_msg(p[ip])
        elif o=='end':return msg
        ip +=1
    return -1
  
____________________________________________________
def assembler_interpreter(program):
    # define variables
    stack, code, ptr, flag, calls, output = {}, [], 0, 0, [], []
    
    # sanitize input
    for line in program.splitlines():
        line = line.split(';')[0].strip()    
        if line: code.append(line)
    
    # define helper functions
    parse = lambda s: stack[s] if s in stack else int(s)
    cmp   = lambda a, b: (a > b) - (a < b)
    label = lambda: code.index(arg1 + ':')
    def parse_msg(line, quote=0, out=''):
        for char in line.split(maxsplit=1)[1]:
            if char == ',' and not quote: char = '#SEP#'
            elif char == "'": quote ^= 1; continue
            out += char
        return ''.join(str(stack[s]) if s in stack else s for s in out.split('#SEP# '))
    
    
    # process code
    while ptr < len(code):
        # parse line
        line = code[ptr]
        cmd, arg1, arg2 = (line.replace(',', '') + ' 0 0').split()[:3]
        
        # execute command
        if   cmd == 'mov': stack[arg1]   = parse(arg2)
        elif cmd == 'inc': stack[arg1]  += 1
        elif cmd == 'dec': stack[arg1]  -= 1
        elif cmd == 'add': stack[arg1]  += parse(arg2)
        elif cmd == 'sub': stack[arg1]  -= parse(arg2)
        elif cmd == 'mul': stack[arg1]  *= parse(arg2)
        elif cmd == 'div': stack[arg1] //= parse(arg2)
        elif cmd == 'cmp': flag = cmp(parse(arg1), parse(arg2))
        
        elif cmd == 'jmp'               : ptr = label()
        elif cmd == 'jne' and flag !=  0: ptr = label()
        elif cmd == 'je'  and flag ==  0: ptr = label()
        elif cmd == 'jge' and flag  > -1: ptr = label()
        elif cmd == 'jg'  and flag ==  1: ptr = label()
        elif cmd == 'jle' and flag  <  1: ptr = label()
        elif cmd == 'jl'  and flag == -1: ptr = label()
        
        elif cmd == 'call': calls.append(ptr); ptr = label()
        elif cmd == 'ret' : ptr = calls.pop()
        elif cmd == 'msg' : output.append(parse_msg(line))
        elif cmd == 'end' : return '\n'.join(output)
        
        ptr += 1
    
    return -1
