import 'dart:math';
var kcuf = (Code)
{
  var
  CodeAt = 0,
  Output = '',
  Preserve = 9,
  PreserveMax = -1,
  Stack = new List.generate(Preserve,(_) => 0),
  StackAt = Preserve--,
  Var = {},
  AST = [],
  ASTStack = [],
  CurrentAST = AST,
  Proc = {},
  CurrentProc,
  CurrentProcVar,

  Line = 0,LastCol,
  CaseSensetive = (Q) => Q.toUpperCase(),
  Clamp = (Q) => Q.toInt() % 256,

  IsNumber = (Q) => Q is num,
  IsArray = (Q) => Q is List,
  Has = (S,Q) => null != Q[S],

  Format = (Q,A,[F = -1]) => Q.replaceAllMapped(':-:',(_) => A[++F].toString()),
  Bad = (Q,[J = false]) => ([A = null])
  {
    throw new Exception(Format(Q,A) +
      '\n\tat ${Line}:${J ? 1 + LastCol : 1 + CodeAt} `${Code}`');
  },
  BadTransform = (Q) => ([A = null]) {throw new Exception(Format(Q,A));},
  ErrorNumberExpected = Bad('A number is expected but got :-:'),
  ErrorNameExpected = Bad('A variable name / command is expected but got :-:'),
  ErrorCommand = Bad('Unexpected command :-:',true),
  ErrorCommandEnd = Bad('Expected end of line but got :-:'),
  ErrorDefineInProc = Bad('Cannot define variables in procedures'),
  ErrorVarUndefined = Bad('Undefined variable :-:',true),
  ErrorVarRedeclare = Bad('Re-defined variable :-:',true),
  ErrorVarButList = Bad('Expected a variable but :-: is a list',true),
  ErrorListButVar = Bad('Expected a list but :-: is a variable',true),
  ErrorUnEOL = Bad('Unexpected end of line'),
  ErrorUnclosed = Bad('Unclosed :-:, expected :-: but got :-:'),
  ErrorBadEscape = Bad('Unexpected char escape \\:-:'),
  ErrorStringExpect = Bad('A string is expected but got :-:'),
  ErrorStringUnclose = Bad('String is not closed'),
  ErrorProcNested = Bad('Procedures should not be nested',true),
  ErrorProcUsed = Bad('Procedure re-defined :-:'),
  ErrorDupParam = Bad('Duplicate parameter name :-:',true),
  ErrorEndNothing = Bad('Nothing to end'),
  ErrorEndUnclose = Bad('Unclosed block (ifeq / ifneq / ueq / proc)'),
  ErrorNoProc = BadTransform('Undefined procedure :-::-:'),
  ErrorProcLength = BadTransform('Procedure :-: expects :-: argument(s) but got :-::-:'),
  ErrorRecursive = BadTransform('Recursive call :-:'),

  Taste = ([Q = 0]) => CodeAt + Q < Code.length ? Code[CodeAt + Q] : '',
  TasteEOL = ()
  {
    var R = Taste();
    return '' == R ? 'EOL' : R;
  },
  Eat = () => ++CodeAt,
  Save = () => LastCol = CodeAt,
  Walk = (Q) {for (;Q.hasMatch(Taste());) Eat();},
  Discard = () => CodeAt = Code.length,
  White = ()
  {
    Walk(new RegExp(r'\s'));
    if ('/' == Taste() && '/' == Taste(1) ||
      '-' == Taste() && '-' == Taste(1) ||
      '#' == Taste()) Discard();
  },
  Word = ()
  {
    var R = CodeAt;
    Save();
    if (new RegExp(r'[^$_A-Za-z]').hasMatch(Taste()))
      ErrorNameExpected([TasteEOL()]);
    Eat();
    Walk(new RegExp(r'[$\w]'));
    var U = CaseSensetive(Code.substring(R,min(CodeAt,Code.length as int)));
    White();
    return U;
  },
  VarName = ()
  {
    var R = Word();
    if ('' == R) ErrorNameExpected([TasteEOL()]);
    if (null == CurrentProcVar || !CurrentProcVar.contains(R))
    {
      if (!Has(R,Var)) ErrorVarUndefined([R]);
      if (!IsNumber(Var[R])) ErrorVarButList([R]);
    }
    return R;
  },
  ListName = ()
  {
    var R = Word();
    if (!Has(R,Var)) ErrorVarUndefined([R]);
    if (IsNumber(Var[R])) ErrorListButVar([R]);
    return R;
  },
  Number = ()
  {
    var R = CodeAt;
    if ('-' == Taste()) Eat();
    Walk(new RegExp(r'\d'));
    var U = Code.substring(R,min(CodeAt,Code.length as int));
    if ('' == R || '-' == R) ErrorNumberExpected([TasteEOL()]);
    White();
    return Clamp(num.parse(U));
  },
  CharEscape = {'\\' : '\\','"' : '"',"'" : "'",'n' : '\n','r' : '\r','t' : '\t'},
  Char = ()
  {
    var R = Taste();
    Eat();
    if ('\\' == R)
    {
      R = CharEscape[Taste()];
      if (null == R) ErrorBadEscape([TasteEOL()]);
      Eat();
    }
    return R;
  },
  NumberOrChar = ()
  {
    if ("'" != Taste()) return Number();
    Eat();
    var R = Char().codeUnitAt(0);
    if ("'" != Taste()) ErrorUnclosed(["'","'",TasteEOL()]);
    Eat();
    White();
    return R;
  },
  VarNameOrNumber = () => new RegExp(r"[-\d']").hasMatch(Taste()) ? NumberOrChar() : VarName(),
  String = ()
  {
    var R = '';
    if ('"' != Taste()) ErrorStringExpect([TasteEOL()]);
    Eat();
    for (;'' != Taste() && '"' != Taste();) R += Char();
    if ('"' != Taste()) ErrorStringUnclose();
    Eat();
    White();
    return R;
  },
  VarNameOrString = () => '"' == Taste() ? [0,String()] : [1,VarName()],

  MsgList = [()
  {
    var R = [VarNameOrString()];
    for (;'' != Taste();) R.add(VarNameOrString());
    return R;
  }],

  Begin = () => ASTStack.add(CurrentAST.length),
  Machine =
  {
    'VAR' : ()
    {
      var V,N;
      if (null != CurrentProc) ErrorDefineInProc();
      if ('' == Taste()) ErrorUnEOL();
      for (;'' != (V = Word());)
      {
        if (Has(V,Var)) ErrorVarRedeclare([V]);
        if ('[' == Taste())
        {
          Eat();
          White();
          N = Number();
          if (']' != Taste()) ErrorUnclosed(['[',']',TasteEOL()]);
          Eat();
          White();
          Var[V] = [StackAt,N];
          StackAt += 4 + N;
        }
        else Var[V] = StackAt++;
      }
    },

    'SET' : [VarName,VarNameOrNumber],

    'INC' : [VarName,VarNameOrNumber],
    'DEC' : [VarName,VarNameOrNumber],
    'ADD' : [VarNameOrNumber,VarNameOrNumber,VarName],
    'SUB' : [VarNameOrNumber,VarNameOrNumber,VarName],
    'MUL' : [VarNameOrNumber,VarNameOrNumber,VarName],
    'DIVMOD' : [VarNameOrNumber,VarNameOrNumber,VarName,VarName],
    'DIV' : [VarNameOrNumber,VarNameOrNumber,VarName],
    'MOD' : [VarNameOrNumber,VarNameOrNumber,VarName],

    'CMP' : [VarNameOrNumber,VarNameOrNumber,VarName],

    'A2B' : [VarNameOrNumber,VarNameOrNumber,VarNameOrNumber,VarName],
    'B2A' : [VarNameOrNumber,VarName,VarName,VarName],

    'LSET' : [ListName,VarNameOrNumber,VarNameOrNumber],
    'LGET' : [ListName,VarNameOrNumber,VarName],

    'IFEQ' : [VarName,VarNameOrNumber,Begin],
    'IFNEQ' : [VarName,VarNameOrNumber,Begin],
    'WEQ' : [VarName,VarNameOrNumber,Begin],
    'WNEQ' : [VarName,VarNameOrNumber,Begin],
    'PROC' : ()
    {
      var N,T;
      if (null != CurrentProc) ErrorProcNested();
      N = Word();
      if (Has(N,Proc)) ErrorProcUsed([N]);
      CurrentProcVar = [];
      for (;'' != Taste();)
      {
        T = Word();
        if (CurrentProcVar.contains(T)) ErrorDupParam([T]);
        CurrentProcVar.add(T);
      }
      Proc[N] = CurrentProc = [CurrentProcVar,CurrentAST = []];
    },
    'END' : [()
    {
      if (0 < ASTStack.length)
        return ASTStack.removeLast();
      if (null != CurrentProc)
      {
        CurrentAST = AST;
        CurrentProc = null;
      }
      else ErrorEndNothing();
    }],
    'CALL' : [()
    {
      var N = Word(),A = [];
      for (;'' != Taste();) A.add(Word());
      return [N,A];
    }],

    'READ' : [VarName],
    'MSG' : MsgList,
    'LN' : MsgList,

    'REM' : Discard,

    'DEBUG' : [Discard],
    'STOP' : [Discard]
  },

  OpGotoCell = (Q)
  {
    Output += Q < StackAt ?
      '<' * (StackAt - Q) :
      '>' * (Q - StackAt);
    StackAt = Q;
  },
  OpAdd = (Q)
  {
    Q = Clamp(Q);
    Output += 128 < Q ?
      '-' * (256 - Q) :
      '+' * Q;
  },
  OpSolvePreserve = (Q)
  {
    PreserveMax = max(Q,PreserveMax);
    return Preserve - Q;
  },
  OpFly = (Q) => StackAt = OpSolvePreserve(Q),
  OpGotoPreserve = (Q) => OpGotoCell(OpSolvePreserve(Q)),
  OpGetPreserve = (Q) => Stack[OpSolvePreserve(Q)],
  OpSetPreserve = (Q,S) => Stack[OpSolvePreserve(Q)] = S,
  OpModifyPreserve = (Q,S)
  {
    OpGotoPreserve(Q);
    OpAdd(S - OpGetPreserve(Q));
    OpSetPreserve(Q,S);
  },
  OpClearPreserve = (Q,[J = false])
  {
    if (J || 0 < OpGetPreserve(Q))
    {
      OpGotoPreserve(Q);
      Output += '[-]';
      OpSetPreserve(Q,0);
    }
  },
  OpMsgList = (Q)
  {
    var T,F = 0;
    for (;F < Q.length;++F)
    {
      T = Q.codeUnitAt(F);
      OpModifyPreserve(0,T);
      Output += '.';
    }
  };

  void Generate(AST,CallArg,CallStack,CallStackMessage)
  {
    var
    OpSolveVar = (Q) => Has(Q,CallArg) ? CallArg[Q] : Q,
    OpGoto = (Q,[S = 0])
    {
      if (IsNumber(Q))
      {
        if (Q < 0) OpGotoCell(-Q);
        else OpGotoPreserve(Q);
      }
      else if (IsNumber(Q = Var[OpSolveVar(Q)]))
        OpGotoCell(Q);
      else OpGotoCell(S + Q[0]);
    },
    _OpClear = (Q,J)
    {
      if (IsNumber(Q))
        OpClearPreserve(Q,J);
      else
      {
        OpGoto(Q);
        Output += '[-]';
      }
    },
    OpClear = (Q,[J = false])
    {
      if (IsArray(Q))
        Q.forEach((Q) => _OpClear(Q,J));
      else
        _OpClear(Q,J);
    },
    OpBegin = (Q,[S = 0])
    {
      OpGoto(Q,S);
      Output += '[-';
    },
    OpEnd = (Q,[S = 0])
    {
      OpGoto(Q,S);
      Output += ']';
    },
    OpMove = (Q,S,[I = 0])
    {
      OpBegin(Q,I);
      if (IsArray(S))
        S.forEach((V)
        {
          OpGoto(V);
          Output += '+';
        });
      else
      {
        OpGoto(S);
        Output += '+';
      }
      OpEnd(Q,I);
    },
    OpMoveReverse = (Q,S,[I = 0])
    {
      OpBegin(Q,I);
      if (IsArray(S))
        S.forEach((V)
        {
          OpGoto(V);
          Output += '-';
        });
      else
      {
        OpGoto(S);
        Output += '-';
      }
      OpEnd(Q,I);
    },
    OpCopy = (Q,S,T,[J = true])
    {
      if (J) OpClear(T);
      if (IsArray(S))
      {
        S = new List.from(S);
        S.add(T);
      }
      else S = [S,T];
      OpMove(Q,S);
      OpMove(T,Q);
    },
    OpPrepare = (Q,S,T)
    {
      OpClear(S);
      if (IsNumber(Q))
      {
        if (IsArray(S))
        {
          OpGoto(T);
          OpAdd(Q);
          OpMove(T,S);
        }
        else
        {
          OpGoto(S);
          OpAdd(Q);
        }
      }
      else OpCopy(Q,S,T);
    },
    OpPrepare01 = (Q,[W = 0,A = 1,T = 2])
    {
      OpPrepare(Q[0],W,T);
      OpPrepare(Q[1],A,T);
    },
    OpSet = (Q,S)
    {
      OpClear(Q);
      OpMove(S,Q);
    },
    OpDivMod = (Arg)
    {
      OpPrepare01(Arg,5,4,0);
      OpCopy(4,8,7);
      OpGoto(7);
      Output += '+<-' +
        '[>>>[->-[>+>>]>[+[-<+>]>+>>]<<<<<]<<-]>' +
        '[->>[->>>+<<<]<]';
      OpFly(6);
      OpClear(8,true);
      OpClear(4,true);
      if (null == Arg[2]) OpClear(2,true);
      else OpSet(Arg[2],2);
      if (3 < Arg.length && null != Arg[3]) OpSet(Arg[3],3);
      else OpClear(3,true);
    },
    OpIFWhile = (Arg,[Not = false])
    {
      if (IsNumber(Arg[1]))
      {
        OpClear(0);
        OpCopy(Arg[0],0,1);
        OpGoto(0);
        OpAdd(-Arg[1]);
      }
      else
      {
        OpPrepare01(Arg);
        OpMoveReverse(1,0);
      }
      if (Not)
      {
        OpGoto(1);
        Output += '+>[[-]<-]<[>+<-<]';
        OpFly(2);
      }
      OpGoto(0);
    };

    AST.forEach((V)
    {
      var Command = V[0],Arg = V[1],Line = V[2];
      switch (Command)
      {
        case 'SET' :
          OpGoto(Arg[0]);
          Output += '[-]';
          if (IsNumber(Arg[1]))
            OpAdd(Arg[1]);
          else
            OpCopy(Arg[1],Arg[0],0);
          break;
        case 'INC' :
          if (IsNumber(Arg[1]))
          {
            OpGoto(Arg[0]);
            OpAdd(Arg[1]);
          }
          else if (OpSolveVar(Arg[0]) == OpSolveVar(Arg[1]))
          {
            OpClear(0);
            OpMove(Arg[0],0);
            OpBegin(0);
            OpGoto(Arg[0]);
            Output += '++';
            OpEnd(0);
          }
          else
            OpCopy(Arg[1],Arg[0],0);
          break;
        case 'DEC' :
          if (IsNumber(Arg[1]))
          {
            OpGoto(Arg[0]);
            OpAdd(-Arg[1]);
          }
          else
          {
            OpCopy(Arg[1],0,1);
            OpMoveReverse(0,Arg[0]);
          }
          break;
        case 'ADD' :
          OpPrepare01(Arg);
          OpMove(1,0);
          OpSet(Arg[2],0);
          break;
        case 'SUB' :
          OpPrepare01(Arg);
          OpMoveReverse(1,0);
          OpSet(Arg[2],0);
          break;
        case 'MUL' :
          OpPrepare01(Arg);
          OpBegin(0);
          OpCopy(1,2,3);
          OpEnd(0);
          OpClear(1,true);
          OpSet(Arg[2],2);
          break;
        case 'DIVMOD' :
        case 'DIV' :
          OpDivMod(Arg);
          break;
        case 'MOD' :
          OpDivMod([Arg[0],Arg[1],null,Arg[2]]);
          break;
        case 'CMP' :
          var X = 4,T0 = 3,T1 = 2;
          OpPrepare01(Arg,[T0,X],[T1,1 + X],0);
          OpMoveReverse(1 + X,X);

          OpGoto(1 + X);
          Output += '+>[[-]';
          OpFly(X);

          OpGoto(T1 - 1);
          Output += '+<[>-]>[';
          OpFly(T1 - 1);
          OpGoto(X);
          Output += '+';
          OpGoto(T0);
          Output += '[-]';
          OpGoto(T1 - 1);
          Output += '->]<+';
          OpGoto(T0);
          Output += '[';
          OpGoto(T1);
          Output += '-[>-]>[';
          OpFly(T1 - 1);
          OpGoto(X);
          Output += '+';
          OpGoto(T0);
          Output += '[-]+';
          OpGoto(T1 - 1);
          Output += '->]<+';
          OpGoto(T0);
          Output += '-]';

          OpGoto(X);
          Output += '[<-]<[>-<-<]';
          OpFly(2 + X);

          OpGoto(1 + X);
          Output += ']<[-<]>';

          OpClear(3,true);
          OpClear(2,true);
          OpClear(1,true);

          OpSet(Arg[2],X);
          break;
        case 'A2B' :
          var
          A = Arg[0],
          B = Arg[1],
          C = Arg[2],
          R = Arg[3];
          if (IsNumber(A))
          {
            A = Clamp(10 * (A - 48));
            if (0 != A)
            {
              OpGoto(1);
              OpAdd(A);
            }
          }
          else
          {
            OpCopy(A,2,0);
            OpGoto(2);
            OpAdd(-48);
            OpBegin(2);
            OpGoto(1);
            OpAdd(10);
            OpEnd(2);
          }
          if (IsNumber(B))
          {
            OpGoto(1);
            OpAdd(B - 48);
          }
          else
          {
            OpCopy(B,1,0);
            OpGoto(1);
            OpAdd(-48);
          }
          OpBegin(1);
          OpGoto(0);
          OpAdd(10);
          OpEnd(1);
          if (IsNumber(C))
          {
            OpGoto(0);
            OpAdd(C - 48);
          }
          else
          {
            OpCopy(C,0,1);
            OpGoto(0);
            OpAdd(-48);
          }
          OpSet(R,0);
          break;
        case 'B2A' :
          var
          R = Arg[0],
          A = Arg[1],
          B = Arg[2],
          C = Arg[3];
          if (IsNumber(R))
          {
            OpClear(A);
            OpAdd(R ~/ 100);
            OpClear(B);
            OpAdd(R ~/ 10 % 10);
            OpClear(C);
            OpAdd(R % 10);
          }
          else
          {
            OpDivMod([R,10,B,C]);
            OpDivMod([B,10,A,B]);
          }
          OpGoto(0);
          OpAdd(48);
          OpMove(0,Arg.sublist(1));
          break;
        case 'LSET' :
          if (IsNumber(Arg[1]))
          {
            OpGoto(Arg[0]);
            OpAdd(Arg[1]);
            Output += '[->+>+<<]';
          }
          else
            OpCopy(Arg[1],[-1 - Var[Arg[0]][0],-2 - Var[Arg[0]][0]],Arg[0],false);
          if (IsNumber(Arg[2]))
          {
            OpGoto(Arg[0],3);
            OpAdd(Arg[2]);
          }
          else
            OpCopy(Arg[2],-3 - Var[Arg[0]][0],Arg[0],false);
          OpGoto(Arg[0]);
          Output += '>[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]' +
            '>>>[-]<[->+<]<' +
            '[[-<+>]<<<[->>>>+<<<<]>>-]<<';
          break;
        case 'LGET' :
          if (IsNumber(Arg[1]))
          {
            OpGoto(Arg[0]);
            OpAdd(Arg[1]);
            Output += '[->+>+<<]';
          }
          else
            OpCopy(Arg[1],[-1 - Var[Arg[0]][0],-2 - Var[Arg[0]][0]],Arg[0],false);
          OpGoto(Arg[0]);
          Output += '>[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]' +
            '>>>[-<+<<+>>>]<<<[->>>+<<<]>' +
            '[[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<';
          OpClear(Arg[2]);
          OpMove(Arg[0],Arg[2],3);
          break;
        case 'IFEQ' :
          OpIFWhile(Arg,true);
          Output += '[';
          OpClear(0,true);
          break;
        case 'IFNEQ' :
          OpIFWhile(Arg);
          Output += '[';
          OpClear(0,true);
          break;
        case 'WEQ' :
          OpIFWhile(Arg,true);
          Output += '[';
          OpClear(0,true);
          break;
        case 'WNEQ' :
          OpIFWhile(Arg);
          Output += '[';
          OpClear(0,true);
          break;
        case 'END' :
          if (null != Arg[0])
          {
            Command = AST[Arg[0]][0];
            Arg = AST[Arg[0]][1];
            if ('WEQ' == Command)
              OpIFWhile(Arg,true);
            else if ('WNEQ' == Command)
              OpIFWhile(Arg);
            else OpClear(0);
            OpGoto(0);
            Output += ']';
          }
          break;
        case 'CALL' :
          Arg = Arg[0];
          var
          T = CallStackMessage + '\n\tat line:${Line} ${Arg[0]}',
          F = Proc[Arg[0]],
          N = {},G = 0;
          if (!Has(Arg[0],Proc)) ErrorNoProc([Arg[0],T]);
          if (F[0].length != Arg[1].length) ErrorProcLength([Arg[0],F[0].length,Arg[1].length,T]);
          if (CallStack.contains(Arg[0])) ErrorRecursive([T]);
          CallStack.add(Arg[0]);
          for (;G < F[0].length;++G) N[F[0][G]] = OpSolveVar(Arg[1][G]);
          Generate(F[1],N,CallStack,T);
          CallStack.removeLast();
          break;
        case 'READ' :
          OpGoto(Arg[0]);
          Output += ',';
          break;
        case 'MSG' :
        case 'LN' :
          Arg[0].forEach((V)
          {
            if (0 < V[0])
            {
              OpGoto(V[1]);
              Output += '.';
            }
            else OpMsgList(V[1]);
          });
          if ('LN' == Command) OpMsgList('\n');
          break;
        case 'DEBUG' :
          Output += '_';
          break;
        case 'STOP' :
          Output += '!';
      }
    });
  }

  Code.split('\n').forEach((V)
  {
    ++Line;
    Code = V;
    CodeAt = 0;
    White();
    if ('' != Taste())
    {
      V = Word();
      if (!Has(V,Machine)) ErrorCommand([V]);
      if (IsArray(Machine[V]))
        CurrentAST.add([V,(Machine[V] as List<Function>).map((C) => C()).toList(),Line]);
      else (Machine[V] as Function)();
      if ('' != Taste()) ErrorCommandEnd([Taste()]);
    }
  });
  if (0 < ASTStack.length) ErrorEndUnclose();

  StackAt = 0;
  Generate(AST,{},[],'');
  return Output.substring(min(Output.length,Preserve - PreserveMax));
};
