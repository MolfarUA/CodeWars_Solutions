59f9cad032b8b91e12000035


kcuf = (Code) ->
  __ = __
  CodeAt = 0
  Output = ''
  Preserve = 9
  PreserveMax = -1
  Stack = Array(Preserve).fill(0)
  StackAt = Preserve--
  Var = {}
  AST = []
  ASTStack = []
  CurrentAST = AST
  Proc = {}
  CurrentProc = __
  CurrentProcVar = __

  Line = 0
  LastCol = __
  CaseSensetive = (Q) -> Q.toUpperCase()
  Clamp = (Q) -> if (Q %= 256) < 0 then 256 + Q else Q

  IsNumber = (Q) -> 'number' == typeof Q
  IsArray = Array.isArray
  _Has = Var.hasOwnProperty
  Has = (S,Q) -> _Has.call Q,S

  Format = (Q,A,F = -1) -> Q.replace /:-:/g,() -> A[++F]
  Bad = (Q,J) -> (A...) ->
    throw new Error Format(Q,A) +
      "\n\tat #{Line}:#{if J then 1 + LastCol else 1 + CodeAt} \"#{Code}\""
  BadTransform = (Q) -> (A...) -> throw new Error Format Q,A
  ErrorNumberExpected = Bad 'A number is expected but got :-:'
  ErrorNameExpected = Bad 'A variable name / command is expected but got :-:'
  ErrorCommand = Bad 'Unexpected command :-:',true
  ErrorCommandEnd = Bad 'Expected end of line but got :-:'
  ErrorDefineInProc = Bad 'Cannot define variables in procedures'
  ErrorVarUndefined = Bad 'Undefined variable :-:',true
  ErrorVarRedeclare = Bad 'Re-defined variable :-:',true
  ErrorVarButList = Bad 'Expected a variable but :-: is a list',true
  ErrorListButVar = Bad 'Expected a list but :-: is a variable',true
  ErrorUnEOL = Bad 'Unexpected end of line'
  ErrorUnclosed = Bad 'Unclosed :-:, expected :-: but got :-:'
  ErrorBadEscape = Bad 'Unexpected char escape \\:-:'
  ErrorStringExpect = Bad 'A string is expected but got :-:'
  ErrorStringUnclose = Bad 'String is not closed'
  ErrorProcNested = Bad 'Procedures should not be nested',true
  ErrorProcUsed = Bad 'Procedure re-defined :-:'
  ErrorDupParam = Bad 'Duplicate parameter name :-:',true
  ErrorEndNothing = Bad 'Nothing to end'
  ErrorEndUnclose = Bad 'Unclosed block (ifeq / ifneq / ueq / proc)'
  ErrorNoProc = BadTransform 'Undefined procedure :-::-:'
  ErrorProcLength = BadTransform 'Procedure :-: expects :-: argument(s) but got :-::-:'
  ErrorRecursive = BadTransform 'Recursive call :-:'

  Taste = (Q = 0) -> Code.charAt CodeAt + Q
  TasteEOL = () -> Taste() || 'EOL'
  Eat = () -> ++CodeAt
  Save = () -> LastCol = CodeAt
  Walk = (Q) ->
    Eat() while Q.test Taste()
    __
  Discard = () -> CodeAt = Code.length
  White = () ->
    Eat() while /\s/.test Taste()
    if '/' == Taste() && '/' == Taste(1) || '-' == Taste() && '-' == Taste(1) || '#' == Taste()
      Discard()
  Word = () ->
    R = CodeAt
    Save()
    /[^$_a-z]/i.test(Taste()) && ErrorNameExpected TasteEOL()
    Eat()
    Walk /[$\w]/
    R = CaseSensetive Code.slice R,CodeAt
    White()
    R
  VarName = () ->
    R = Word()
    R || ErrorNameExpected TasteEOL()
    if !CurrentProcVar || !~CurrentProcVar.indexOf R
      Has(R,Var) || ErrorVarUndefined R
      IsNumber(Var[R]) || ErrorVarButList R
    R
  ListName = () ->
    R = Word()
    Has(R,Var) || ErrorVarUndefined R
    IsNumber(Var[R]) && ErrorListButVar R
    R
  Number = () ->
    R = CodeAt
    '-' == Taste() && Eat()
    Walk /\d/
    R = Code.slice R,CodeAt
    R && '-' != R || ErrorNumberExpected TasteEOL()
    White()
    Clamp(+R)
  CharEscape = '\\' : '\\','"' : '"',"'" : "'",n : '\n',r : '\r',t : '\t'
  Char = (R) ->
    R = Taste()
    Eat()
    if '\\' == R
      R = CharEscape[Taste()]
      R || ErrorBadEscape TasteEOL()
      Eat()
    R
  NumberOrChar = (R) ->
    if "'" == Taste()
      Eat()
      R = Char().charCodeAt()
      "'" == Taste() || ErrorUnclosed "'","'",TasteEOL()
      Eat()
      White()
      R
    else Number()
  VarNameOrNumber = () -> if /[-\d']/.test Taste() then NumberOrChar() else VarName()
  String = (R) ->
    R = ''
    '"' == Taste() || ErrorStringExpect TasteEOL()
    Eat()
    R += Char() while Taste() && '"' != Taste()
    '"' == Taste() || ErrorStringUnclose()
    Eat()
    White()
    return R
  VarNameOrString = () -> if '"' == Taste() then [0,String()] else [1,VarName()]

  MsgList = [(R) ->
    R = [VarNameOrString()]
    R.push VarNameOrString() while Taste()
    R]

  Begin = () -> ASTStack.push CurrentAST.length
  Machine =
  {
    VAR : (V,N) ->
      CurrentProc && ErrorDefineInProc()
      Taste() || ErrorUnEOL()
      while V = Word()
        Has(V,Var) && ErrorVarRedeclare V
        if '[' == Taste()
          Eat()
          White()
          N = Number()
          ']' == Taste() || ErrorUnclosed '[',']',TasteEOL()
          Eat()
          White()
          Var[V] = [StackAt,N]
          StackAt += 4 + N
        else Var[V] = StackAt++
      __

    SET : [VarName,VarNameOrNumber]

    INC : [VarName,VarNameOrNumber]
    DEC : [VarName,VarNameOrNumber]
    ADD : [VarNameOrNumber,VarNameOrNumber,VarName]
    SUB : [VarNameOrNumber,VarNameOrNumber,VarName]
    MUL : [VarNameOrNumber,VarNameOrNumber,VarName]
    DIVMOD : [VarNameOrNumber,VarNameOrNumber,VarName,VarName]
    DIV : [VarNameOrNumber,VarNameOrNumber,VarName]
    MOD : [VarNameOrNumber,VarNameOrNumber,VarName]

    CMP : [VarNameOrNumber,VarNameOrNumber,VarName]

    A2B : [VarNameOrNumber,VarNameOrNumber,VarNameOrNumber,VarName]
    B2A : [VarNameOrNumber,VarName,VarName,VarName]

    LSET : [ListName,VarNameOrNumber,VarNameOrNumber]
    LGET : [ListName,VarNameOrNumber,VarName]

    IFEQ : [VarName,VarNameOrNumber,Begin]
    IFNEQ : [VarName,VarNameOrNumber,Begin]
    WEQ : [VarName,VarNameOrNumber,Begin]
    WNEQ : [VarName,VarNameOrNumber,Begin]
    PROC : (N,T) ->
      CurrentProc && ErrorProcNested()
      N = Word()
      Has(N,Proc) && ErrorProcUsed N
      CurrentProcVar = []
      while Taste()
        T = Word()
        CurrentProcVar.includes(T) && ErrorDupParam T
        CurrentProcVar.push T
      Proc[N] = CurrentProc = [CurrentProcVar,CurrentAST = []]
    END : [() ->
      if ASTStack.length
        ASTStack.pop()
      else if CurrentProc
        CurrentAST = AST
        CurrentProc = null
      else ErrorEndNothing()]
    CALL : [(N,A) ->
      N = Word()
      A = []
      A.push Word() while Taste()
      [N,A]]

    READ : [VarName]
    MSG : MsgList
    LN : MsgList

    REM : Discard

    DEBUG : [Discard]
    STOP : [Discard]
  }

  OpGotoCell = (Q) ->
    Output += if Q < StackAt then '<'.repeat StackAt - Q else '>'.repeat Q - StackAt
    StackAt = Q
  OpAdd = (Q) ->
    Q = Clamp Q
    Output += if 128 < Q then '-'.repeat 256 - Q else '+'.repeat Q
  OpSolvePreserve = (Q) ->
    PreserveMax = Math.max Q,PreserveMax
    Preserve - Q
  OpFly = (Q) -> StackAt = OpSolvePreserve Q
  OpGotoPreserve = (Q) -> OpGotoCell OpSolvePreserve Q
  OpGetPreserve = (Q) -> Stack[OpSolvePreserve Q]
  OpSetPreserve = (Q,S) -> Stack[OpSolvePreserve Q] = S
  OpModifyPreserve = (Q,S) ->
    OpGotoPreserve Q
    OpAdd S - OpGetPreserve Q
    OpSetPreserve Q,S
  OpClearPreserve = (Q,J) ->
    if J || OpGetPreserve Q
      OpGotoPreserve Q
      Output += '[-]'
      OpSetPreserve Q,0
  OpMsgList = (Q,T) ->
    F = 0
    while F < Q.length
      T = Q.charCodeAt F
      OpModifyPreserve 0,T
      Output += '.'
      ++F
    __

  Generate = (AST,CallArg = {},CallStack = [],CallStackMessage = '') ->
    OpSolveVar = (Q) -> if Has Q,CallArg then CallArg[Q] else Q
    OpGoto = (Q,S = 0) ->
      if IsNumber Q
        if Q < 0
          OpGotoCell -Q
        else OpGotoPreserve Q
      else if IsNumber Q = Var[OpSolveVar Q]
        OpGotoCell Q
      else OpGotoCell S + Q[0]
    OpClear = (Q,J) ->
      if IsNumber Q
        OpClearPreserve Q,J
      else if IsArray Q
        Q.forEach (Q) -> OpClear Q,J
      else
        OpGoto Q
        Output += '[-]'
    OpBegin = (Q,S = 0) ->
      OpGoto Q,S
      Output += '[-'
    OpEnd = (Q,S = 0) ->
      OpGoto Q,S
      Output += ']'
    OpMove = (Q,S,I = 0) ->
      OpBegin Q,I
      if IsArray S
        S.forEach (V) ->
          OpGoto V
          Output += '+'
      else
        OpGoto S
        Output += '+'
      OpEnd Q,I
    OpMoveReverse = (Q,S,I = 0) ->
      OpBegin Q,I
      if IsArray S
        S.forEach (V) ->
          OpGoto(V)
          Output += '-'
      else
        OpGoto S
        Output += '-'
      OpEnd Q,I
    OpCopy = (Q,S,T,J = true) ->
      J && OpClear T
      OpMove Q,if IsArray S then [S...,T] else [S,T]
      OpMove T,Q
    OpPrepare = (Q,S,T) ->
      OpClear S
      if IsNumber Q
        if IsArray S
          OpGoto T
          OpAdd Q
          OpMove T,S
        else
          OpGoto S
          OpAdd Q
      else OpCopy Q,S,T
    OpPrepare01 = ([Q,S],W = 0,A = 1,T = 2) ->
      OpPrepare Q,W,T
      OpPrepare S,A,T
    OpSet = (Q,S) ->
      OpClear Q
      OpMove S,Q
    OpDivMod = (Arg) ->
      OpPrepare01 Arg,5,4,0
      OpCopy 4,8,7
      OpGoto 7
      Output += '+<-' +
        '[>>>[->-[>+>>]>[+[-<+>]>+>>]<<<<<]<<-]>' +
        '[->>[->>>+<<<]<]'
      OpFly 6
      OpClear 8,true
      OpClear 4,true
      if Arg[2] then OpSet Arg[2],2 else OpClear 2,true
      if Arg[3] then OpSet Arg[3],3 else OpClear 3,true
    OpIFWhile = (Arg,Not) ->
      if IsNumber Arg[1]
        OpClear 0
        OpCopy Arg[0],0,1
        OpGoto 0
        OpAdd -Arg[1]
      else
        OpPrepare01 Arg
        OpMoveReverse 1,0
      if Not
        OpGoto 1
        Output += '+>[[-]<-]<[>+<-<]'
        OpFly 2
      OpGoto 0

    AST.forEach ([Command,Arg,Line]) ->
      switch Command
        when 'SET'
          OpGoto Arg[0]
          Output += '[-]'
          if  IsNumber Arg[1]
            OpAdd Arg[1]
          else OpCopy Arg[1],Arg[0],0
        when 'INC'
          if IsNumber Arg[1]
            OpGoto Arg[0]
            OpAdd Arg[1]
          else if OpSolveVar(Arg[0]) == OpSolveVar Arg[1]
            OpClear 0
            OpMove Arg[0],0
            OpBegin 0
            OpGoto Arg[0]
            Output += '++'
            OpEnd 0
          else OpCopy Arg[1],Arg[0],0
        when 'DEC'
          if IsNumber Arg[1]
            OpGoto Arg[0]
            OpAdd -Arg[1]
          else
            OpCopy Arg[1],0,1
            OpMoveReverse 0,Arg[0]
        when 'ADD'
          OpPrepare01 Arg
          OpMove 1,0
          OpSet Arg[2],0
        when 'SUB'
          OpPrepare01 Arg
          OpMoveReverse 1,0
          OpSet Arg[2],0
        when 'MUL'
          OpPrepare01 Arg
          OpBegin 0
          OpCopy 1,2,3
          OpEnd 0
          OpClear 1,true
          OpSet Arg[2],2
        when 'DIVMOD','DIV'
          OpDivMod Arg
        when 'MOD'
          OpDivMod [Arg[0],Arg[1],null,Arg[2]]
        when 'CMP'
          X = 4
          T0 = 3
          T1 = 2
          OpPrepare01 Arg,[T0,X],[T1,1 + X],0
          OpMoveReverse 1 + X,X

          OpGoto 1 + X
          Output += '+>[[-]'
          OpFly X

          OpGoto T1 - 1
          Output += '+<[>-]>['
          OpFly T1 - 1
          OpGoto X
          Output += '+'
          OpGoto T0
          Output += '[-]'
          OpGoto T1 - 1
          Output += '->]<+'
          OpGoto T0
          Output += '['
          OpGoto T1
          Output += '-[>-]>['
          OpFly T1 - 1
          OpGoto X
          Output += '+'
          OpGoto T0
          Output += '[-]+'
          OpGoto T1 - 1
          Output += '->]<+'
          OpGoto T0
          Output += '-]'

          OpGoto X
          Output += '[<-]<[>-<-<]'
          OpFly 2 + X

          OpGoto 1 + X
          Output += ']<[-<]>'

          OpClear 3,true
          OpClear 2,true
          OpClear 1,true

          OpSet Arg[2],X
        when 'A2B'
          [A,B,C,R] = Arg
          if IsNumber A
            if A = Clamp 10 * (A - 48)
              OpGoto 1
              OpAdd A
          else
            OpCopy A,2,0
            OpGoto 2
            OpAdd -48
            OpBegin 2
            OpGoto 1
            OpAdd 10
            OpEnd 2
          if IsNumber B
            OpGoto 1
            OpAdd B - 48
          else
            OpCopy B,1,0
            OpGoto 1
            OpAdd -48
          OpBegin 1
          OpGoto 0
          OpAdd 10
          OpEnd 1
          if IsNumber C
            OpGoto 0
            OpAdd C - 48
          else
            OpCopy C,0,1
            OpGoto 0
            OpAdd -48
          OpSet R,0
        when 'B2A'
          [R,A,B,C] = Arg
          if IsNumber R
            OpClear A
            OpAdd 0 | R / 100
            OpClear B
            OpAdd 0 | R / 10 % 10
            OpClear C
            OpAdd R % 10
          else
            OpDivMod [R,10,B,C]
            OpDivMod [B,10,A,B]
          OpGoto 0
          OpAdd 48
          OpMove 0,Arg.slice 1
        when 'LSET'
          if IsNumber Arg[1]
            OpGoto Arg[0]
            OpAdd Arg[1]
            Output += '[->+>+<<]'
          else
            OpCopy Arg[1],[-1 - Var[Arg[0]][0],-2 - Var[Arg[0]][0]],Arg[0],false
          if IsNumber Arg[2]
            OpGoto Arg[0],3
            OpAdd Arg[2]
          else
            OpCopy Arg[2],-3 - Var[Arg[0]][0],Arg[0],false
          OpGoto Arg[0]
          Output += '>[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]' +
            '>>>[-]<[->+<]<' +
            '[[-<+>]<<<[->>>>+<<<<]>>-]<<'
        when 'LGET'
          if IsNumber Arg[1]
            OpGoto Arg[0]
            OpAdd Arg[1]
            Output += '[->+>+<<]'
          else
            OpCopy Arg[1],[-1 - Var[Arg[0]][0],-2 - Var[Arg[0]][0]],Arg[0],false
          OpGoto Arg[0]
          Output += '>[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]' +
            '>>>[-<+<<+>>>]<<<[->>>+<<<]>' +
            '[[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<'
          OpClear Arg[2]
          OpMove Arg[0],Arg[2],3
        when 'IFEQ'
          OpIFWhile Arg,true
          Output += '['
          OpClear 0,true
        when 'IFNEQ'
          OpIFWhile Arg
          Output += '['
          OpClear 0,true
        when 'WEQ'
          OpIFWhile Arg,true
          Output += '['
          OpClear 0,true
        when 'WNEQ'
          OpIFWhile Arg
          Output += '['
          OpClear 0,true
        when 'END'
          if null != Arg[0]
            [Command,Arg] = AST[Arg[0]]
            if 'WEQ' == Command
              OpIFWhile Arg,true
            else if 'WNEQ' == Command
              OpIFWhile Arg
            else OpClear 0
            OpGoto 0
            Output += ']'
        when 'CALL'
          Arg = Arg[0]
          T = CallStackMessage + "\n\tat line:#{Line} #{Arg[0]}"
          F = Proc[Arg[0]]
          Has(Arg[0],Proc) || ErrorNoProc Arg[0],T
          F[0].length == Arg[1].length || ErrorProcLength Arg[0],F[0].length,Arg[1].length,T
          CallStack.includes(Arg[0]) && ErrorRecursive T
          CallStack.push Arg[0]
          Generate(F[1],F[0].reduce(((D,V,F) ->
            D[V] = OpSolveVar(Arg[1][F])
            D),{}),CallStack,T)
          CallStack.pop()
        when 'READ'
          OpGoto Arg[0]
          Output += ','
        when 'MSG','LN'
          Arg[0].forEach ([Type,Value]) ->
            if Type
              OpGoto Value
              Output += '.'
            else OpMsgList Value
          OpMsgList '\n' if 'LN' == Command
        when 'DEBUG'
          Output += '_'
        when 'STOP'
          Output += '!'
      __

  Code.split("\n").forEach (V) ->
    ++Line
    Code = V
    CodeAt = 0
    White()
    if Taste()
      V = Word()
      Has(V,Machine) || ErrorCommand V
      if IsArray Machine[V]
        CurrentAST.push([V,Machine[V].map((C) -> C()),Line])
      else Machine[V]()
      Taste() && ErrorCommandEnd Taste()
  ASTStack.length && ErrorEndUnclose()

  StackAt = 0
  Generate AST
  Output.slice Preserve - PreserveMax
