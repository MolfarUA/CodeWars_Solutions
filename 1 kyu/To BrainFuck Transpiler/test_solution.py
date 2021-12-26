# global kcuf,NOPRINT
def lolol() :
    import re
    def __BF__(Code,Input = '',Extend = False) :
        AST = []
        Stack = [0]
        StackAt = [0]
        InputAt = [0]
        Output = ['']
        PC = [0]

        Clamp = lambda Q : Q % 256
        def StackCheck(Q) :
            R = len(Stack)
            if R <= Q :
                while R <= Q : R += R
                Q = len(Stack)
                while Q < R :
                    Q += 1
                    Stack.append(0)

        def OpInc(Q) :
            Stack[StackAt[0]] = Clamp(Q + Stack[StackAt[0]])
        def OpDec(Q) :
            Stack[StackAt[0]] = Clamp(Stack[StackAt[0]] - Q)
        def OpRight(Q) :
            StackAt[0] += Q
            StackCheck(StackAt[0])
        def OpLeft(Q) :
            StackAt[0] -= Q
            if StackAt[0] < 0 :
                Bad("Bad attemp to access cell[%s]. Current output [%s]'%s'" % (StackAt[0],len(Output[0]),Output[0]))
        def OpRead(_) :
            Stack[StackAt[0]] = ord(Input[InputAt[0]]) % 256 if InputAt[0] < len(Input) else 0
            InputAt[0] += 1
        def OpWrite(_) :
            Output[0] += chr(Stack[StackAt[0]])
        def OpBegin(Q) :
            if not Stack[StackAt[0]] : PC[0] = Q
        def OpEnd(Q) :
            if Stack[StackAt[0]] : PC[0] = Q

        def OpOptmizedMove(Q) :
            for Shift,Multi in Q[1] :
                StackCheck(Shift + StackAt[0])
                Stack[Shift + StackAt[0]] = Clamp(Stack[Shift + StackAt[0]] - Multi * Stack[StackAt[0]])
            Stack[StackAt[0]] = 0
            PC[0] = Q[0]

        OpExtend = {
            '_' : lambda _ : print("%s [%s]" % (StackAt[0],','.join(str(V) for V in Stack))),
            '!' : lambda _ : Bad('Debug')
        }
        ExtendRegExp = '[^+\-<>,.[\]_!]'

        def Bad(Q) :
            raise Exception(Q)

        AllLoop = []
        LoopStack = []
        Last = [None]
        Count = [0]
        def ClearLast() :
            if '+' == Last[0] : AST.append([OpInc,Count[0]])
            elif '-' == Last[0] : AST.append([OpDec,Count[0]])
            elif '<' == Last[0] : AST.append([OpLeft,Count[0]])
            elif '>' == Last[0] : AST.append([OpRight,Count[0]])
            elif ',' == Last[0] : AST.append([OpRead,None])
            elif '.' == Last[0] : AST.append([OpWrite,None])
            elif '[' == Last[0] :
                AllLoop.append(len(AST))
                LoopStack.append(len(AST))
                AST.append([OpBegin])
            elif ']' == Last[0] :
                if not len(LoopStack) : Bad('Closing not started loop')
                T = LoopStack.pop()
                AST[T].append(len(AST))
                AST.append([OpEnd,T])
            else :
                AST.append([OpExtend[Last[0]],None])
            Last[0] = None

        Code = re.sub(ExtendRegExp if Extend else '[^+\-<>,.[\]]','',Code)
        for T in Code :
            if Last[0] == T : Count[0] += 1
            else :
                if Last[0] : ClearLast()
                Last[0] = T
                if '[' == T or ']' == T or ',' == T or '.' == T :
                    ClearLast()
                else : Count[0] = 1
        if Last[0] : ClearLast()
        if len(LoopStack) : Bad('Unclosed loop')

        for V in AllLoop :
            Current = 0
            ID = {}
            while True :
                V += 1
                T = AST[V]
                if OpInc == T[0] :
                    ID[Current] = (ID[Current] if Current in ID else 0) + T[1]
                elif OpDec == T[0] :
                    ID[Current] = (ID[Current] if Current in ID else 0) - T[1]
                elif OpLeft == T[0] :
                    Current -= T[1]
                elif OpRight == T[0] :
                    Current += T[1]
                elif OpEnd == T[0] :
                    if not Current and 1 == abs(ID[0]) :
                        AST[T[1]] = [OpOptmizedMove,(V,[[V,ID[0] * ID[V]] for V in ID if V])]
                    break
                else : break

        PC[0] = 0
        while PC[0] < len(AST) :
            T = AST[PC[0]]
            T[0](T[1])
            PC[0] += 1

        return Output[0]
    def Check(RawCode,Input = '',Expect = '',Message = '') :
        RawCode = re.sub('(?m)^["\']+',lambda V : re.sub('.',lambda C : C.group(0).lower() if random.random() < .5 else C.group(0).upper(),V.group(0)),RawCode)
        if not NOPRINT : print(RawCode)
        print('<b>Input :</b>',[ord(V) for V in Input])
        print('<b>Expected output :</b>',[ord(V) for V in Expect])
        Code = kcuf(RawCode)
        print('<b>Output code length :</b> ' + str(len(Code)))
        test.assert_equals(__BF__(Code,Input),Expect,Message)

    END = lambda : print('<COMPLETEDIN::>')

    random = __import__('RA/ND')
    test.describe('Fixed Tests')

    test.it('Works for var, read, msg, comment')
    Check("""
var X//This is a comment
read X--This is also a comment
msg "Bye" X#No doubt it is a comment
rem &&Some comment~!@#$":<
""",'?','Bye?')
    END()

    test.it('Works for set, inc, dec')
    Check("""
var A B
sEt A 'a'
msg a B
set B 50
msG A b
inc A 10
dec B -20
msg A B
""",'','a\0a2kF')
    END()

    test.it('Works for kinds of numbers')
    Check("""
var X
set X  114514
msg X
set X -114514
msg X
set X 'X'
msg X
""",'','\x52\xae\x58')
    END()

    test.it('Works for add, sub, mul')
    Check("""
var A B C
read A
read B
add a b c
msg a b c
sub a b a
msg a b c
mul b a c
msg a b c
""",'0\x07','\x30\x07\x37\x29\x07\x37\x29\x07\x1f')
    END()

    test.it('Works for divmod, div, mod')
    Check("""
var A B C D
set A 79
set B 13
divmod A B C D
msg A B C D
div C D C
msg A B C D
mod A D A
msg A B C D
""",'','\x4f\x0d\x06\x01\x4f\x0d\x06\x01\x00\x0d\x06\x01')
    END()

    test.it('Works for cmp')
    Check("""
var X K
read X
cmp 80 X K
msg X K
cmp X 'z' K
msg X K
cmp X X K
msg X K
""",'\x80','\x80\xff\x80\x01\x80\x00')
    END()

    test.it('Works for a2b, b2a')
    Check("""
var A B C D
set a 247
b2a A B C D
msg A B C D
inc B 1
dec C 2
inc D 5
a2b B C D A
msg A B C D // A = (100 * (2 + 1) + 10 * (4 - 2) + (7 + 5)) % 256 = 76 = 0x4c
""",'','\xf7\x32\x34\x37\x4c\x33\x32\x3c')
    END()

    test.it('Works for lset, lget')
    Check("""
var L  [ 20 ]  I X
lset L 10 80
set X 20
lset L 5 X
set X 9
lset L X X
set I 4
lget L I X
msg X
lget L 5 X
msg X
lget L 9 X
msg X
lget L 10 X
msg X
lget L 19 X
msg X
""",'','\x00\x14\x09\x50\x00')
    END()

    test.it('Works for ifeq, ifneq, wneq')
    Check("""
var F L[5] X
set F 0
add 10 10 X
wneq F 5
    lset L F X
    inc F 1
    dec X 1
end
//L == [20,19,18,17,16]

wneq F 0
    inc F -1
    lget L F X
    msg X
end

set F 10
wneq F 0
    ifeq F 10
        set F 5
    end
    dec F 1
    lget L F X
    ifneq X 18
        msg F X
    end
end
ifeq F 0
    ifneq X 50
        msg ";-)"
    end
end
""",'','\x10\x11\x12\x13\x14\x04\x10\x03\x11\x01\x13\x00\x14;-)')
    END()

    test.it('Works for proc')
    Check("""
var A B T
set A 'U'
set B 'V'

msg"Outer Before : "A B"\\n"
call swap B A
msg"Outer After : "A B"\\n"

proc swap x y
    msg "Inner Before : "x y"\\n"
    set T x
    call say T
    set x y
    set y T
    msg "Inner After : "x y"\\n"
end
proc say x
    msg "It is " x " now\\n"
end
""",'','Outer Before : UV\n' +
    'Inner Before : VU\n' +
    'It is V now\n' +
    'Inner After : UV\n' +
    'Outer After : VU\n')
    END()

    END() # describe('Fixed Tests')

    test.describe('Invalid Input')

    def ErrorWhen(Desc,Code) :
        test.it('Error Type : ' + Desc)
        test.expect_error(Desc,lambda : Check(Code))
        END()

    ErrorWhen('Unknown instructions',"""
var a
mov a 5
""")
    ErrorWhen('Arguments for an instruction are too much or not enough',"""
var x
set x
""")
    ErrorWhen('Undefined var names',"""
msg x
""")
    ErrorWhen('Duplicate var names',"""
var Q
var q[20]
""")
    ErrorWhen('Define variables inside a procedure',"""
proc nice
    var evil
end
""")
    ErrorWhen('Unclosed [] pair',"""
var x[60 Y
""")
    ErrorWhen('Expect a variable but got something else',"""
var c 20
set 20 20
add "what" 'x' c
// all lines above cause this error respectively
""")
    ErrorWhen('Expect a variable but got a list',"""
var L[40] X[20]
LSet L 0 X
""")
    ErrorWhen('Expect a list but got a variable',"""
var L X
LGet L 0 X
""")
    ErrorWhen('Unclosed \'\' pair',"""
var x
set x 'z
""")
    ErrorWhen('Unclosed "" pair',"""
msg " nope
""")
    ErrorWhen('Nested produces',"""
proc a
proc b
end
end
""")
    ErrorWhen('Duplicate procedure names',"""
proc Q a
end
proc Q q
end
""")
    ErrorWhen('Duplicate parameter names',"""
proc Q q Q
end
""")
    ErrorWhen('End before begining a block',"""
end
msg " That's end"
""")
    ErrorWhen('Unclosed blocks',"""
var a
set a 20
ifeq a 19
msg "eq"
""")
    ErrorWhen('Undefined produce',"""
var Yes
caLL Say Yes
""")
    ErrorWhen('The length of arguments does not match the length of parameters',"""
var P Q
call What P Q
proc What Is The Answer
    msg "42"
end
""")
    ErrorWhen('Recursive call',"""
var A
set a 20
call Wrap a
proc Say x
    msg "It is "x
    call Wrap X
end
Proc Wrap X
    call Say x
eNd
""")

    END() # describe('Invalid Input')

    test.describe('Advanced Tests')

    CHR = lambda *Q : ''.join(chr(V) for V in Q)
    Clamp = lambda Q : int(Q) % 256
    Edge = [0,1,2,125,126,127,128,129,130,254,255]

    test.it('Works for divmod')
    for L in Edge :
        for R in Edge :
            if R :
                Div = Clamp(L // R)
                Mod = Clamp(L % R)
                Check("""
vaR toString __proto__ hasOwnProperty ValueOf
reAd __protO__
rEad toStrinG
diVMod __prOTO__ toStrinG hasOWNProperty valueOf
msg TOsTrinG __proto__ HasOwnProperty valueOF
                """,CHR(L,R),CHR(R,L,Div,Mod),'%s `divmod` %s == (%s,%s)' % (L,R,Div,Mod))
    END()

    test.it('Works for cmp')
    for L in Edge :
        for R in Edge :
            CMP = Clamp(-1 if L < R else 1 if R < L else 0)
            Check("""
var __defineGetter__  hasOwnProperty __lookupGetter__ __lookupSetter__ propertyIsEnumerable constructor toString toLocaleString valueOf isPrototypeOf
reAd __defineGetter__
rEad constructor
call __PROto__ constructor __defineGetter__
msg constructor __defineGetter__ valueOf

proc __proto__ __defineSetter__ constructor
    cmp __defineSetter__ constructor valueOf
end
            """,CHR(R,L),CHR(L,R,CMP),'%s `cmp` %s == %s' % (L,R,CMP))
    END()
    END() # describe('Advanced Tests')



    test.describe('Random Tests')

    ZTN = '0123456789'
    ATZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    VarPrefix = '$_' + ATZ + ATZ.lower()
    VarSuffix = VarPrefix + ZTN
    Rnd = lambda Q,S = None : Q[Rnd(len(Q))] if type(Q) in (str,list) else Q + Rnd(S - Q) if None != S else random.randint(0,Q - 1)
    RndName = lambda : Rnd(VarPrefix) + ''.join(Rnd(VarSuffix) for _ in range(Rnd(20,40)))
    RndNameN = lambda Q : [RndName() for _ in range(Q)]

    def PoolValid0() :
        A,B,C,D = RndNameN(4)
        N = Rnd(2,4)
        Code = str.format("""
var {A} {B} {C} {D}
read {A}
read {B}
set {C} 0
wneq {C} {N}
    add {A} {B} {D}
    mul {A} {D} {B}
    sub {D} {B} {A}
    inc {C} 257
end
msg {A} {B} " -- " {C} {D}
        """,A=A,B=B,C=C,D=D,N=N)
        InputA = Rnd(256)
        InputB = Rnd(256)

        A = InputA
        B = InputB
        C = 0
        D = 0
        while C < N :
            D = Clamp(A + B)
            B = Clamp(A * D)
            A = Clamp(D - B)
            C += 1
        return [Code,CHR(InputA,InputB),CHR(A,B) + ' -- ' + CHR(C,D)]
    def PoolValid1() :
        A,B = RndNameN(2)
        Code = str.format("""
var {A} {B}
read {A}
divmod {A} 2 {A} {B}
ifeq {B} 0
    msg "Even" {A}
    mod {A} 2 {B}
    ifneq {B} 1
        msg "Still#Even"
    end
end
ifneq {B} 0
    msg "Old"
end
        """,A=A,B=B)
        InputA = Rnd(256)
        Output = ''

        A = InputA
        B = 1 & A
        A >>= 1
        if not B :
            Output += 'Even' + CHR(A)
            B = A % 2
            if not B : Output += 'Still#Even'
        if B : Output += 'Old'
        return [Code,CHR(InputA),Output]
    def PoolValid2() :
        A,B,C = RndNameN(3)
        Size = Rnd(2) + 20
        Require = [Rnd(Size) for _ in range(5)]
        Code = str.format("""
var {A}    [       {Size}        ]         {B} {C}
set {B} {Size}
wneq {B} 0
    dec {B} 1
    read {C}
    lSet {A} {B} {C}
end
{W}
        """,A=A,B=B,C=C,Size=Size,W='\n'.join(str.format('lget {A} {V} {C}\nmsg {C}',A=A,C=C,V=V) for V in Require))
        Input = [Rnd(256) for _ in range(Size)]
        Output = [Input[Size - 1 - V] for V in Require]

        return [Code,CHR(*Input),CHR(*Output)]
    def PoolValid3() :
        A,B,C,D,A2B,B2A = RndNameN(6)
        Code = str.format("""
var {A} {B} {C} {D}
read {A}
cmp 100 {A} {B}
ifeq {B} -1
    call {B2A} {A}
end
ifneq {B} 0
    msg "7//77"
end
ifeq {B} 1
    call {A2B} {A}
end
proc {B2A} $$
    b2a $$ $$ {C} {D}
    msg {A} {C} {D}
end
proc {A2B} $_
    a2b $_ $_ $_ $_
    call {B2A} $_
end
        """,A=A,B=B,C=C,D=D,A2B=A2B,B2A=B2A)
        InputA = Rnd(256)
        Output = ''

        B2A = lambda Q : ('00' + str(Q))[-3:]
        if 100 < InputA :
            Output += B2A(InputA)
        if 100 != InputA :
            Output += '7//77'
        if 100 > InputA :
            Output += B2A(Clamp(100 * (InputA - 48) + 10 * (InputA - 48) + (InputA - 48)))
        return [Code,CHR(InputA),Output]
    PoolValid = [PoolValid0,PoolValid1,PoolValid2,PoolValid3]

    def PoolInvalid0() :
        # Unknown instructions
        A,B,C,D = RndNameN(4)
        N = Rnd(2,4)
        return str.format("""
var {A} {B} {C} {D}
read {A}
read {B}
set {C} 0
wneq {C} {N}
    add {A} {B} {D}
    mul {A} {D} {B}
    sub {D} {B} {A}
    inc {C} 257
end
type {A} {B} " -- " {C} {D}
        """,A=A,B=B,C=C,D=D,N=N)
    def PoolInvalid1() :
        # Arguments for an instruction are too much or not enough
        A,B,C,D = RndNameN(4)
        N = Rnd(2,4)
        return str.format("""
var {A} {B} {C} {D}
read {A}
read {B}
set {C} 0
wneq {C} {N}
    add {A} {B} {D}
    mul {D} {B}
    sub {D} {B} {A}
    inc {C} 257
end
msg {A} {B} " -- " {C} {D}
        """,A=A,B=B,C=C,D=D,N=N)
    def PoolInvalid2() :
        # Undefined var names
        A,B,C,D = RndNameN(4)
        N = Rnd(2,4)
        return str.format("""
var {A} {B} {C} {D}
read {A}
read {B}
set {C} 0
wneq {C} {N}
    add {A} {B} {D}
    mul {A} {D} {W}
    sub {D} {B} {A}
    inc {C} 257
end
msg {A} {B} " -- " {C} {D}
        """,A=A,B=B,C=C,D=D,N=N,W=RndName())
    def PoolInvalid3() :
        # Duplicate var names
        A,B,C,D = RndNameN(4)
        N = Rnd(2,4)
        return str.format("""
var {A} {B}
read {A}
var {B} {C} {D}
read {B}
set {C} 0
wneq {C} {N}
    add {A} {B} {D}
    mul {A} {D} {B}
    sub {D} {B} {A}
    inc {C} 257
end
msg {A} {B} " -- " {C} {D}
        """,A=A,B=B,C=C,D=D,N=N)
    def PoolInvalid4() :
        # Define variables inside a procedure
        A,B,C,D,A2B,B2A = RndNameN(6)
        return str.format("""
var {A} {B} {C} {D}
read {A}
cmp 100 {A} {B}
ifeq {B} -1
    call {B2A} {A}
end
ifneq {B} 0
    msg "7//77"
end
ifeq {B} 1
    call {A2B} {A}
end
proc {B2A} $$
    b2a $$ $$ {C} {D}
    msg {A} {C} {D}
end
proc {A2B} $_
    var {W}
    a2b $_ $_ $_ $_
    call {B2A} $_
end
        """,A=A,B=B,C=C,D=D,A2B=A2B,B2A=B2A,W=RndName())
    def PoolInvalid5() :
        # Unclosed `[]` pair
        A,B,C = RndNameN(3)
        Size = Rnd(2) + 20
        Require = [Rnd(Size) for _ in range(5)]
        return str.format("""
var {A}[{Size} {B} {C}
set {B} {Size}
wneq {B} 0
    dec {B} 1
    read {C}
    lSet {A} {B} {C}
end
{W}
        """,A=A,B=B,C=C,Size=Size,W='\n'.join(str.format('lget {A} {V} {C}\nmsg {C}',A=A,C=C,V=V) for V in Require))
    def PoolInvalid6() :
        # Expect a variable but got something else
        A,B,C,D,A2B,B2A = RndNameN(6)
        return str.format("""
var {A} {B} {C} {D}
read {A}
cmp 100 {A} {B}
ifeq {B} -1
    call {B2A} {A}
end
ifneq {B} 0
    msg "7//77"
end
ifeq {B} 1
    call {A2B} '{W}'
end
proc {B2A} $$
    b2a $$ $$ {C} {D}
    msg {A} {C} {D}
end
proc {A2B} $_
    a2b $_ $_ $_ $_
    call {B2A} $_
end
        """,A=A,B=B,C=C,D=D,A2B=A2B,B2A=B2A,W=Rnd(10))
    def PoolInvalid7() :
        # Expect a variable but got a list
        A,B,C,D,A2B,B2A = RndNameN(6)
        return str.format("""
var {A} {B} {C} {D} [{W}]
read {A}
cmp 100 {A} {B}
ifeq {B} -1
    call {B2A} {A}
end
ifneq {B} 0
    msg "7//77"
end
ifeq {B} 1
    call {A2B} {A}
end
proc {B2A} $$
    b2a $$ $$ {C} {D}
    msg {A} {C} {D}
end
proc {A2B} $_
    a2b $_ $_ $_ $_
    call {B2A} $_
end
        """,A=A,B=B,C=C,D=D,A2B=A2B,B2A=B2A,W=Rnd(2) + 20)
    def PoolInvalid8() :
        # Expect a list but got a variable
        A,B,C = RndNameN(3)
        Size = Rnd(2) + 20
        Require = [Rnd(Size) for _ in range(5)]
        return str.format("""
var {A}    [      {Size}     ]       {B} {C}
set {B} {Size}
wneq {B} 0
    dec {B} 1
    read {C}
    lSet {B} {B} {C}
end
{W}
        """,A=A,B=B,C=C,Size=Size,W='\n'.join(str.format('lget {A} {V} {C}\nmsg {C}',A=A,C=C,V=V) for V in Require))
    def PoolInvalid9() :
        # Unclosed `''` pair
        A,B,C = RndNameN(3)
        Size = Rnd(2) + 20
        Require = [Rnd(Size) for _ in range(5)]
        return str.format("""
var {A}    [      {Size}     ]       {B} {C}
set {B} {Size}
wneq {B} 0
    dec {B} 1
    read {C}
    lSet {B} {B} {C}
    set {B} '9
end
{W}
        """,A=A,B=B,C=C,Size=Size,W='\n'.join(str.format('lget {A} {V} {C}\nmsg {C}',A=A,C=C,V=V) for V in Require))
    def PoolInvalidA() :
        # Unclosed `""` pair
        A,B,C = RndNameN(3)
        Size = Rnd(2) + 20
        Require = [Rnd(Size) for _ in range(5)]
        return str.format("""
var {A}    [      {Size}     ]       {B} {C}
set {B} {Size}
wneq {B} 0
    dec {B} 2
    read {C}
    lSet {B} {B} {C}
    msg "Good
end
{W}
        """,A=A,B=B,C=C,Size=Size,W='\n'.join(str.format('lget {A} {V} {C}\nmsg {C}',A=A,C=C,V=V) for V in Require))
    def PoolInvalidB() :
        # End before begining a block
        A,B = RndNameN(2)
        return str.format("""
var {A} {B}
read {A}
divmod {A} 2 {A} {B}
ifeq {B} 0
    msg "Even" {A}
        mod {A} 2 {B}
        ifneq {B} 1
            msg "Still#Even"
        end
    end
end
ifneq {B} 0
    msg "Old"
end
        """,A=A,B=B)
    def PoolInvalidC() :
        # Unclosed blocks
        A,B = RndNameN(2)
        return str.format("""
var {A} {B}
read {A}
divmod {A} 2 {A} {B}
ifeq {B} 0
    msg "Even" {A}
    mod {A} 2 {B}
    ifneq {B} 1
        msg "Still#Even"
    end
ifneq {B} 0
    msg "Old"
end
        """,A=A,B=B)
    def PoolInvalidD() :
        # Undefined produce
        A,B = RndNameN(2)
        return str.format("""
var {A} {B}
read {A}
divmod {A} 2 {A} {B}
ifeq {B} 0
    msg "Even" {A}
    mod {A} 2 {B}
    ifneq {B} 1
        msg "Still#Even"
        call {A}
    end
ifneq {B} 0
    msg "Old"
end
        """,A=A,B=B)
    PoolInvalid = [
        PoolInvalid0,PoolInvalid1,PoolInvalid2,PoolInvalid3,
        PoolInvalid4,PoolInvalid5,PoolInvalid6,PoolInvalid7,
        PoolInvalid8,PoolInvalid9,PoolInvalidA,PoolInvalidB,
        PoolInvalidC,PoolInvalidD
    ]

    test.it('Works for random tests')
    for _ in range(200) :
        if random.random() < .5 :
            T = Rnd(PoolValid)()
            Check(*T)
        else :
            T = Rnd(PoolInvalid)()
            test.expect_error('',lambda : Check(T,'','Should throw an error','Expect Error'))
    END()

    END() # describe('Random Tests')
Test = test = __import__('TE/ST')
lolol()
