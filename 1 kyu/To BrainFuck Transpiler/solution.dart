fun kcuf(RawCode : String,Origin : Boolean = false,Indent : String = "\t") : String
{
    var Code = ""
    var CodeAt = 0
    var Output = ""
    var Preserve = 9
    var PreserveMax = -1
    val Stack = Array(Preserve,{0})
    var StackAt = 0
    var VarAt = Preserve--
    val Var = mutableMapOf<String,Any>()
    val AST = mutableListOf<Array<Any>>()
    val ASTStack = java.util.Stack<Int>()
    var CurrentAST = AST
    val Proc = mutableMapOf<String,Array<Any>>()
    var ProcSig : String? = null
    var ProcVar : MutableList<String>? = null
    var ProcVarType : MutableList<Array<Any>?>? = null

    var Line = 0
    var LastCol = 0
    val CaseSensetive = {Q : String -> Q.toUpperCase()}
    val Clamp = {Q : Int ->
        val R = Q % 256
        if (R < 0) 256 + R else R}

    fun Bad(Q : String,J : Boolean = false) = fun(A : Any?)
    {
        throw Error((if (null == A) Q else if (A is Array<*>) String.format(Q,*A) else String.format(Q,A)) +
            "\n\tat $Line:${if (J) 1 + LastCol else 1 + CodeAt} '$Code'")
    }
    //  Parse Error
    val ErrorNumberExpected = Bad("A number is expected but got %s")
    val ErrorNameExpected = Bad("A variable name / command is expected but got %s")
    val ErrorCommand = Bad("Unexpected command %s",true)
    val ErrorCommandEnd = Bad("Expected end of line but got %s")
    val ErrorDefineInProc = Bad("Cannot define variables in procedures")
    val ErrorVarUndefined = Bad("Undefined variable %s",true)
    val ErrorVarRedeclare = Bad("Re-defined variable %s",true)
    val ErrorVarButList = Bad("Expected a variable but %s is a list",true)
    val ErrorListButVar = Bad("Expected a list but %s is a variable",true)
    val ErrorVarTypeMismatch = Bad("Type mismatch\n" +
        "\tin `%s`\n" +
        "\t%s was used as a %s at %s:%s `%s`\n" +
        "\tas well being used as a %s",true)
    val ErrorUnEOL = Bad("Unexpected end of line")
    val ErrorUnclosed = Bad("Unclosed %s, expected %s but got %s")
    val ErrorBadEscape = Bad("Unexpected char escape \\%s")
    val ErrorStringExpect = Bad("A string is expected but got %s")
    val ErrorStringUnclose = Bad("String is not closed")
    val ErrorProcNested = Bad("Procedures should not be nested",true)
    val ErrorProcUsed = Bad("Procedure re-defined %s")
    val ErrorDupParam = Bad("Duplicate parameter name %s",true)
    val ErrorEndNothing = Bad("Nothing to end")
    val ErrorEndUnclose = Bad("Unclosed block (ifeq / ifneq / ueq / proc)")
    //  Transform Error
    val ErrorNoProc = Bad("Undefined procedure %s%s")
    val ErrorProcLength = Bad("Procedure %s expects %s argument(s) but got %s%s")
    val ErrorRecursive = Bad("Recursive call %s")
    val ErrorArgTypeMismatch = Bad("Type mismatch\n" +
        "\ta %s is expected for parameter %s in `%s`\n" +
        "\tbut argument %s is a %s")

    fun _Taste(Q : Int = 0) = Code.getOrNull(CodeAt + Q) ?: '\u0000'
    fun Taste(Q : Int = 0) = Code.getOrNull(CodeAt + Q)?.toString() ?: ""
    val TasteEOL =
    {
        val R = _Taste()
        if (0 < R.toInt()) R.toString() else "EOL"
    }
    val Eat = {++CodeAt}
    val Save = {LastCol = CodeAt}
    val Walk = {Q : Regex -> while (Q.matches(Taste())) Eat()}
    val Discard = {CodeAt = Code.length}
    val White =
    {
        Walk(Regex("\\s"))
        if ('/' == _Taste() && '/' == _Taste(1) ||
            '-' == _Taste() && '-' == _Taste(1) ||
            '#' == _Taste()) Discard()
    }
    val Word =
    {
        val S = CodeAt
        Save()
        if (Regex("[^_A-Za-z$]").matches(Taste())) ErrorNameExpected(TasteEOL())
        Eat()
        Walk(Regex("[\\w$]"))
        val R = if (S < Code.length) CaseSensetive(Code.substring(S,CodeAt)) else ""
        White()
        R
    }
    val MakeName = {H : Boolean ->
    {
        val R = Word()
        if (R.isEmpty()) ErrorNameExpected(TasteEOL())
        val T = ProcVar?.indexOf(R) ?: -1
        if (T < 0)
        {
            if (!Var.containsKey(R)) ErrorVarUndefined(R)
            if (H != Var[R] is Number) if (H) ErrorVarButList(R) else ErrorListButVar(R)
        }
        else if (null == ProcVarType!![T]) ProcVarType!![T] = arrayOf(H,Line,1 + LastCol,Code)
        else if (H != ProcVarType!![T]!![0]) ErrorVarTypeMismatch(arrayOf
        (
            ProcSig,R,
            if (H) "list" else "variable",
            ProcVarType!![T]!![1],
            ProcVarType!![T]!![2],
            (ProcVarType!![T]!![3] as String).trim(),
            if (H) "variable" else "list"
        ))
        R
    }}
    val VarName = MakeName(true)
    val ListName = MakeName(false)
    val RawNumber =
    {
        val S = CodeAt
        if ('-' == _Taste()) Eat()
        Walk(Regex("\\d"))
        val R = Code.substring(S,CodeAt)
        if (R.isEmpty() || "-" == R) ErrorNumberExpected(TasteEOL())
        White()
        R.toInt()
    }
    val Number = {Clamp(RawNumber())}
    val CharEscape = mapOf(
        '\\' to '\\',
        '"' to '"',
        '\'' to '\'',
        '"' to '"',
        'n' to '\n',
        'r' to '\r',
        't' to '\t')
    val Char =
    {
        var R = _Taste()
        Eat()
        if ('\\' == R)
        {
            R = _Taste()
            if (!CharEscape.containsKey(R)) ErrorBadEscape(TasteEOL())
            R = CharEscape.getValue(R)
            Eat()
        }
        R
    }
    val NumberOrChar =
    {
        if ('\'' == _Taste())
        {
            Eat()
            val R = Char()
            if ('\'' != _Taste()) ErrorUnclosed(arrayOf("'","'",TasteEOL()))
            Eat()
            White()
            R.toInt()
        }
        else Number()
    }
    val VarNameOrNumber = {if (Regex("[-\\d']").matches(Taste())) NumberOrChar() else VarName()}
    val String =
    {
        var R = ""
        if ('"' != _Taste()) ErrorStringExpect(TasteEOL())
        Eat()
        while (!Taste().isEmpty() && '"' != _Taste()) R += Char()
        if ('"' != _Taste()) ErrorStringUnclose(null)
        Eat()
        White()
        R
    }
    val VarNameOrString = {if ('"' == _Taste()) 0 to String() else 1 to VarName()}

    val MsgList = arrayOf(
    {
        val R = mutableListOf<Pair<Int,String>>()
        while (!Taste().isEmpty()) R.add(VarNameOrString())
        R
    })

    val Begin = {ASTStack.add(CurrentAST.size)}
    val Machine = mapOf(
        "VAR" to
        {
            if (null != ProcSig) ErrorDefineInProc(null)
            if (Taste().isEmpty()) ErrorUnEOL(null)
            var V = Word()
            while (!V.isEmpty())
            {
                if (Var.containsKey(V)) ErrorVarRedeclare(V)
                if ('[' == _Taste())
                {
                    Eat()
                    White()
                    val N = RawNumber()
                    if (']' != _Taste()) ErrorUnclosed(arrayOf("[","]",TasteEOL()))
                    Eat()
                    White()
                    Var[V] = arrayOf(VarAt,N)
                    VarAt += 4 + N
                }
                else Var[V] = VarAt++
                V = Word()
            }
        },
        "SET" to arrayOf(VarName,VarNameOrNumber),
        "INC" to arrayOf(VarName,VarNameOrNumber),
        "DEC" to arrayOf(VarName,VarNameOrNumber),
        "ADD" to arrayOf(VarNameOrNumber,VarNameOrNumber,VarName),
        "SUB" to arrayOf(VarNameOrNumber,VarNameOrNumber,VarName),
        "MUL" to arrayOf(VarNameOrNumber,VarNameOrNumber,VarName),
        "DIVMOD" to arrayOf(VarNameOrNumber,VarNameOrNumber,VarName,VarName),
        "DIV" to arrayOf(VarNameOrNumber,VarNameOrNumber,VarName),
        "MOD" to arrayOf(VarNameOrNumber,VarNameOrNumber,VarName),

        "CMP" to arrayOf(VarNameOrNumber,VarNameOrNumber,VarName),

        "A2B" to arrayOf(VarNameOrNumber,VarNameOrNumber,VarNameOrNumber,VarName),
        "B2A" to arrayOf(VarNameOrNumber,VarName,VarName,VarName),

        "LSET" to arrayOf(ListName,VarNameOrNumber,VarNameOrNumber),
        "LGET" to arrayOf(ListName,VarNameOrNumber,VarName),

        "IFEQ" to arrayOf(VarName,VarNameOrNumber,Begin),
        "IFNEQ" to arrayOf(VarName,VarNameOrNumber,Begin),
        "WEQ" to arrayOf(VarName,VarNameOrNumber,Begin),
        "WNEQ" to arrayOf(VarName,VarNameOrNumber,Begin),
        "PROC" to
        {
            if (null != ProcSig) ErrorProcNested(null)
            val N = Word()
            if (Proc.containsKey(N)) ErrorProcUsed(N)
            CurrentAST = mutableListOf()
            ProcVar = mutableListOf()
            ProcVarType = mutableListOf()
            ProcSig = Code
            Proc[N] = arrayOf(CurrentAST,ProcVar!!,ProcVarType!!,ProcSig!!)
            while (!Taste().isEmpty())
            {
                val T = Word()
                if (ProcVar!!.contains(T)) ErrorDupParam(T)
                ProcVar!!.add(T)
                ProcVarType!!.add(null)
            }
        },
        "END" to arrayOf(
        {
            if (!ASTStack.isEmpty()) ASTStack.pop()
            else if (null == ProcSig) ErrorEndNothing(null)
            else
            {
                CurrentAST = AST
                ProcSig = null
                null
            }
        }),
        "CALL" to arrayOf(
        {
            val N = Word()
            val A = mutableListOf<String>()
            while (!Taste().isEmpty()) A.add(Word())
            listOf(N,A)
        }),

        "READ" to arrayOf(VarName),
        "MSG" to MsgList,
        "LN" to MsgList,

        "REM" to Discard,

        "DEBUG" to arrayOf(Discard),
        "STOP" to arrayOf(Discard))

    val EscapeMap = mapOf(
        '&' to "&amp;",
        '+' to "&plus;",
        '-' to "&minus;",
        '<' to "&lt;",
        '>' to "&gt;",
        ',' to "&comma;",
        '.' to "&stop;",
        '[' to "&leftsquare;",
        ']' to "&rightsquare;")
    val Escape = {Q : String -> Q.replace(Regex("[&+\\-<>,.\\[\\]]")){EscapeMap.getValue(it.value[0])}}

    val OpGotoCell = {Q : Int ->
        Output += if (Q < StackAt) "<".repeat(StackAt - Q)
            else ">".repeat(Q - StackAt)
        StackAt = Q
    }
    val OpAdd = {Q : Int ->
        val S = Clamp(Q)
        Output += if (128 < S) "-".repeat(256 - S) else "+".repeat(S)
    }
    val OpSolvePreserve = {Q : Int ->
        if (PreserveMax < Q) PreserveMax = Q
        Preserve - Q
    }
    val OpFly = {Q : Int -> StackAt = OpSolvePreserve(Q)}
    val OpGotoPreserve = {Q : Int -> OpGotoCell(OpSolvePreserve(Q))}
    val OpGetPreserve = {Q : Int -> Stack[OpSolvePreserve(Q)]}
    val OpSetPreserve = {Q : Int,S : Int -> Stack[OpSolvePreserve(Q)] = S}
    val OpModifyPreserve = {Q : Int,S : Int ->
        OpGotoPreserve(Q)
        OpAdd(S - OpGetPreserve(Q))
        OpSetPreserve(Q,S)
    }
    fun OpClearPreserve(Q : Int,J : Boolean = false)
    {
        if (J || 0 != OpGetPreserve(Q))
        {
            OpGotoPreserve(Q)
            Output += "[-]"
            OpSetPreserve(Q,0)
        }
    }
    val OpMsgList = {Q : String ->
        for (T in Q)
        {
            OpModifyPreserve(0,T.toInt())
            Output += '.'
        }
    }

    fun Generate
    (
        AST : MutableList<Array<Any>>,
        CallArg : MutableMap<String,String> = mutableMapOf(),
        CallStack : java.util.Stack<String> = java.util.Stack(),
        CallStackMessage : String = "",
        _CurrentIndent : String = ""
    ){
        var CurrentIndent = _CurrentIndent

        val OpSolveVar = {Q : String -> CallArg[Q] ?: Q}
        fun OpGoto(Q : Any,S : Int = 0)
        {
            if (Q is Int)
            {
                if (Q < 0) OpGotoCell(-Q)
                else OpGotoPreserve(Q)
            }
            else
            {
                val T = Var[OpSolveVar(Q as String)]
                if (T is Int) OpGotoCell(T)
                else OpGotoCell(S + (T as Array<Int>)[0])
            }
        }
        fun OpClear(Q : Any,J : Boolean = false)
        {
            when (Q)
            {
                is Int -> OpClearPreserve(Q,J)
                is Array<*> -> Q.forEach{OpClear(it!!,J)}
                else ->
                {
                    OpGoto(Q)
                    Output += "[-]"
                }
            }
        }
        fun OpBegin(Q : Any,S : Int = 0)
        {
            OpGoto(Q,S)
            Output += "[-"
        }
        fun OpEnd(Q : Any,S : Int = 0)
        {
            OpGoto(Q,S)
            Output += "]"
        }
        fun OpMove(Q : Any,S : Any,I : Int = 0)
        {
            OpBegin(Q,I)
            if (S is Array<*>) S.forEach{
                OpGoto(it!!)
                Output += '+'
            }
            else
            {
                OpGoto(S)
                Output += '+'
            }
            OpEnd(Q,I)
        }
        fun OpMoveReverse(Q : Any,S : Any,I : Int = 0)
        {
            OpBegin(Q,I)
            if (S is Array<*>) S.forEach{
                OpGoto(it!!)
                Output += '-'
            }
            else
            {
                OpGoto(S)
                Output += '-'
            }
            OpEnd(Q,I)
        }
        fun OpCopy(Q : Any,S : Any,T : Any,J : Boolean = true)
        {
            if (J) OpClear(T)
            OpMove(Q,if (S is Array<*>) arrayOf(*S,T) else arrayOf(S,T))
            OpMove(T,Q)
        }
        val OpPrepare = {Q : Any,S : Any,T : Any ->
            OpClear(S)
            if (Q is Int)
            {
                if (S is Array<*>)
                {
                    OpGoto(T)
                    OpAdd(Q)
                    OpMove(T,S)
                }
                else
                {
                    OpGoto(S)
                    OpAdd(Q)
                }
            }
            else OpCopy(Q,S,T)
        }
        fun OpPrepare01(Q : List<*>,W : Any = 0,A : Any = 1,T : Int = 2)
        {
            OpPrepare(Q[0]!!,W,T)
            OpPrepare(Q[1]!!,A,T)
        }
        val OpSet = {Q : Any,S : Any ->
            OpClear(Q)
            OpMove(S,Q)
        }
        val OpDivMod = {Arg : List<*> ->
            OpPrepare01(Arg,5,4,0)
            OpCopy(4,8,7)
            OpGoto(7)
            Output += "+<-" +
                "[>>>[->-[>+>>]>[+[-<+>]>+>>]<<<<<]<<-]>" +
                "[->>[->>>+<<<]<]"
            OpFly(6)
            OpClear(8,true)
            OpClear(4,true)
            if (null != Arg[2]) OpSet(Arg[2]!!,2) else OpClear(2,true)
            if (3 < Arg.size) OpSet(Arg[3]!!,3) else OpClear(3,true)
        }
        fun OpIFWhile(Arg : List<*>,Not : Boolean = false)
        {
            if (Arg[1] is Int)
            {
                OpClear(0)
                OpCopy(Arg[0]!!,0,1)
                OpGoto(0)
                OpAdd(-(Arg[1] as Int))
            }
            else
            {
                OpPrepare01(Arg)
                OpMoveReverse(1,0)
            }
            if (Not)
            {
                OpGoto(1)
                Output += "+>[[-]<-]<[>+<-<]"
                OpFly(2)
            }
            OpGoto(0)
        }

        AST.forEach{
            var Command = it[0] as String
            var Arg = it[1] as List<*>
            val Line = it[2]
            val CurrentCode = it[3] as String
            var NeedNewLine = true
            var NeedIndent = false
            Code = CurrentCode
            if (Origin)
            {
                if ("END" == Command) CurrentIndent = CurrentIndent.substring(Indent.length)
                Output += CurrentIndent + Escape(Code) + '\n'
                if ("END" != Command || null != Arg[0]) Output += CurrentIndent
            }
            when (Command)
            {
                "SET" ->
                {
                    OpGoto(Arg[0]!!)
                    Output += "[-]"
                    if (Arg[1] is Int)
                        OpAdd(Arg[1] as Int)
                    else
                        OpCopy(Arg[1]!!,Arg[0]!!,0)
                }
                "INC" ->
                {
                    when
                    {
                        Arg[1] is Int ->
                        {
                            OpGoto(Arg[0]!!)
                            OpAdd(Arg[1] as Int)
                        }
                        OpSolveVar(Arg[0] as String) == OpSolveVar(Arg[1] as String) ->
                        {
                            OpClear(0)
                            OpMove(Arg[0]!!,0)
                            OpBegin(0)
                            OpGoto(Arg[0]!!)
                            Output += "++"
                            OpEnd(0)
                        }
                        else -> OpCopy(Arg[1]!!,Arg[0]!!,0)
                    }
                }
                "DEC" ->
                {
                    if (Arg[1] is Int)
                    {
                        OpGoto(Arg[0]!!)
                        OpAdd(-(Arg[1] as Int))
                    }
                    else
                    {
                        OpCopy(Arg[1]!!,0,1)
                        OpMoveReverse(0,Arg[0]!!)
                    }
                }
                "ADD" ->
                {
                    OpPrepare01(Arg)
                    OpMove(1,0)
                    OpSet(Arg[2]!!,0)
                }
                "SUB" ->
                {
                    OpPrepare01(Arg)
                    OpMoveReverse(1,0)
                    OpSet(Arg[2]!!,0)
                }
                "MUL" ->
                {
                    OpPrepare01(Arg)
                    OpBegin(0)
                    OpCopy(1,2,3)
                    OpEnd(0)
                    OpClear(1,true)
                    OpSet(Arg[2]!!,2)
                }
                "DIVMOD","DIV" -> OpDivMod(Arg)
                "MOD" -> OpDivMod(listOf(Arg[0],Arg[1],null,Arg[2]))
                "CMP" ->
                {
                    val X = 4
                    val T0 = 3
                    val T1 = 2
                    OpPrepare01(Arg,arrayOf(T0,X),arrayOf(T1,1 + X),0)
                    OpMoveReverse(1 + X,X)

                    OpGoto(1 + X)
                    Output += "+>[[-]"
                    OpFly(X)

                    OpGoto(T1 - 1)
                    Output += "+<[>-]>["
                    OpFly(T1 - 1)
                    OpGoto(X)
                    Output += '+'
                    OpGoto(T0)
                    Output += "[-]"
                    OpGoto(T1 - 1)
                    Output += "->]<+"
                    OpGoto(T0)
                    Output += '['
                    OpGoto(T1)
                    Output += "-[>-]>["
                    OpFly(T1 - 1)
                    OpGoto(X)
                    Output += '+'
                    OpGoto(T0)
                    Output += "[-]+"
                    OpGoto(T1 - 1)
                    Output += "->]<+"
                    OpGoto(T0)
                    Output += "-]"

                    OpGoto(X)
                    Output += "[<-]<[>-<-<]"
                    OpFly(2 + X)

                    OpGoto(1 + X)
                    Output += "]<[-<]>"

                    OpClear(3,true)
                    OpClear(2,true)
                    OpClear(1,true)

                    OpSet(Arg[2]!!,X)
                }
                "A2B" ->
                {
                    val (A,B,C,R) = Arg
                    if (A is Int)
                    {
                        val a = Clamp(10 * (A - 48))
                        if (0 < a)
                        {
                            OpGoto(1)
                            OpAdd(a)
                        }
                    }
                    else
                    {
                        OpCopy(A!!,2,0)
                        OpGoto(2)
                        OpAdd(-48)
                        OpBegin(2)
                        OpGoto(1)
                        OpAdd(10)
                        OpEnd(2)
                    }
                    if (B is Int)
                    {
                        OpGoto(1)
                        OpAdd(B - 48)
                    }
                    else
                    {
                        OpCopy(B!!,1,0)
                        OpGoto(1)
                        OpAdd(-48)
                    }
                    OpBegin(1)
                    OpGoto(0)
                    OpAdd(10)
                    OpEnd(1)
                    if (C is Int)
                    {
                        OpGoto(0)
                        OpAdd(C - 48)
                    }
                    else
                    {
                        OpCopy(C!!,0,1)
                        OpGoto(0)
                        OpAdd(-48)
                    }
                    OpSet(R!!,0)
                }
                "B2A" ->
                {
                    val (R,A,B,C) = Arg
                    if (R is Int)
                    {
                        OpClear(A!!)
                        OpAdd(R / 100)
                        OpClear(B!!)
                        OpAdd(R / 10 % 10)
                        OpClear(C!!)
                        OpAdd(R % 10)
                    }
                    else
                    {
                        OpDivMod(listOf(R,10,B,C))
                        OpDivMod(listOf(B,10,A,B))
                    }
                    OpGoto(0)
                    OpAdd(48)
                    OpMove(0,arrayOf(Arg[1],Arg[2],Arg[3]))
                }
                "LSET" ->
                {
                    if (Arg[1] is Int)
                    {
                        OpGoto(Arg[0]!!)
                        OpAdd(Arg[1] as Int)
                        Output += "[->+>+<<]"
                    }
                    else
                        OpCopy(Arg[1]!!,arrayOf(-1 - (Var[OpSolveVar(Arg[0] as String)] as Array<Int>)[0],
                            -2 - (Var[OpSolveVar(Arg[0] as String)] as Array<Int>)[0]),Arg[0]!!,false)
                    if (Arg[2] is Int)
                    {
                        OpGoto(Arg[0]!!,3)
                        OpAdd(Arg[2] as Int)
                    }
                    else
                        OpCopy(Arg[2]!!,-3 - (Var[OpSolveVar(Arg[0] as String)] as Array<Int>)[0],Arg[0]!!,false)
                    OpGoto(Arg[0]!!)
                    Output += ">[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]" +
                        ">>>[-]<[->+<]<" +
                        "[[-<+>]<<<[->>>>+<<<<]>>-]<<"
                }
                "LGET" ->
                {
                    if (Arg[1] is Int)
                    {
                        OpGoto(Arg[0]!!)
                        OpAdd(Arg[1] as Int)
                        Output += "[->+>+<<]"
                    }
                    else
                        OpCopy(Arg[1]!!,arrayOf(-1 - (Var[OpSolveVar(Arg[0] as String)] as Array<Int>)[0],
                            -2 - (Var[OpSolveVar(Arg[0] as String)] as Array<Int>)[0]),Arg[0]!!,false)
                    OpGoto(Arg[0]!!)
                    Output += ">[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]" +
                        ">>>[-<+<<+>>>]<<<[->>>+<<<]>" +
                        "[[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<"
                    OpClear(Arg[2]!!)
                    OpMove(Arg[0]!!,Arg[2]!!,3)
                }
                "IFEQ","WEQ" ->
                {
                    OpIFWhile(Arg,true)
                    Output += '['
                    OpClear(0,true)
                    NeedIndent = true
                }
                "IFNEQ" ->
                {
                    OpIFWhile(Arg)
                    Output += '['
                    OpClear(0,true)
                    NeedIndent = true
                }
                "WNEQ" ->
                {
                    if (0 != Arg[1])
                    {
                        OpIFWhile(Arg)
                        Output += '['
                        OpClear(0,true)
                    }
                    else
                    {
                        OpGoto(Arg[0]!!)
                        Output += '['
                    }
                    NeedIndent = true
                }
                "END" ->
                {
                    if (null != Arg[0])
                    {
                        Command = AST[Arg[0] as Int][0] as String
                        Arg = AST[Arg[0] as Int][1] as List<*>
                        if ("WEQ" == Command)
                        {
                            OpIFWhile(Arg,true)
                            OpGoto(0)
                        }
                        else if ("WNEQ" == Command)
                        {
                            if (0 != Arg[1])
                            {
                                OpIFWhile(Arg)
                                OpGoto(0)
                            }
                            else OpGoto(Arg[0]!!)
                        }
                        else
                        {
                            OpClear(0)
                            OpGoto(0)
                        }
                        Output += ']'
                    }
                    else NeedNewLine = false
                }
                "CALL" ->
                {
                    Arg = Arg[0] as List<*>
                    val Arg0 = Arg[0] as String
                    val Arg1 = Arg[1] as MutableList<String>
                    val NextMessage = "$CallStackMessage\n\tat line $Line, procedure $Arg0"
                    if (!Proc.containsKey(Arg0)) ErrorNoProc(arrayOf(Arg0,NextMessage))
                    val T = Proc[Arg0]!!
                    ProcVar = T[1] as MutableList<String>
                    ProcVarType = T[2] as MutableList<Array<Any>?>
                    ProcSig = T[3] as String
                    if (ProcVar!!.size != Arg1.size)
                        ErrorProcLength(arrayOf(Arg0,ProcVar!![0].length,Arg1.size,NextMessage))
                    if (CallStack.contains(Arg0)) ErrorRecursive(NextMessage)
                    CallStack.add(Arg0)
                    if (Origin) Output += Escape(ProcSig!!) + '\n'
                    val D = mutableMapOf<String,String>()
                    ProcVar!!.forEachIndexed{F,V ->
                        D[V] = OpSolveVar(Arg1[F])
                        if (null != ProcVarType!![F])
                        {
                            val T = ProcVarType!![F]!![0] as Boolean
                            if (T != (Var[D[V]] is Int))
                            ErrorArgTypeMismatch(arrayOf
                            (
                                if (T) "variable" else "list",
                                V,
                                ProcSig,
                                Arg1[F],
                                if (T) "list" else "variable"
                            ))
                        }
                    }
                    Generate(Proc[Arg0]!![0] as MutableList<Array<Any>>,D,CallStack,NextMessage,CurrentIndent + Indent)
                    NeedNewLine = false
                    CallStack.pop()
                }
                "READ" ->
                {
                    OpGoto(Arg[0]!!)
                    Output += ','
                }
                "MSG","LN" ->
                {
                    (Arg[0] as MutableList<Pair<Int,String>>).forEach{(Type,Value) ->
                        if (0 == Type) OpMsgList(Value)
                        else
                        {
                            OpGoto(Value)
                            Output += '.'
                        }
                    }
                    if ("LN" == Command) OpMsgList("\n")
                }
                "DEBUG" -> Output += '_'
                "STOP" -> Output += '!'
            }
            if (Origin)
            {
                if (NeedNewLine) Output += '\n'
                if (NeedIndent) CurrentIndent += Indent
            }
        }
    }

    RawCode.split('\n').forEach{V ->
        ++Line
        Code = V
        CodeAt = 0
        White()
        if (!Taste().isEmpty())
        {
            val W = Word()
            if (!Machine.containsKey(W)) ErrorCommand(W)
            if (Machine[W] is Array<*>)
                CurrentAST.add(arrayOf(W,(Machine[W] as Array<() -> Any>).map{it()},Line,Code.trim()))
            else (Machine[W] as () -> Any)()
            if (!Taste().isEmpty()) ErrorCommandEnd(Taste())
            if (Origin && "VAR" == W) Output += Code.trim() + '\n'
        }
    }
    if (0 < ASTStack.size) ErrorEndUnclose(null)

    Generate(AST)
    return if (Origin) "Preserved $PreserveMax\n$Output" else Output.substring(Preserve - PreserveMax)
}
