module BrainFuckTranspiler
  implicit none
  private
  public kcuf
  character,allocatable :: Y(:)
  type ArrayNode
    character,allocatable :: Data(:)
  endtype
  type Array
    integer At,Len
    type(ArrayNode),allocatable :: Data(:)
  endtype
  type ArrayPointer
    type(Array),pointer :: Data
  endtype
  type MapNode
    integer Hash
    character,allocatable :: Key(:),Value(:)
    type(MapNode),pointer :: Next
  endtype
  type Map
    type(MapNode),pointer :: Q
  endtype
  type(MapNode),pointer :: MapLast
  logical Error
  character(:),allocatable :: I,O
  integer :: &
    CodeAt,CodeOffset,CodeLen, &
    OAt,OLen, &
    Preserve = 8, PreserveMax, &
    StackAt, VarAt
  integer Stack(0:8)
  type VarType
    integer At,Len
  endtype
  type(VarType) VarTemp
  type(Map) Var(64)
  type(Array),pointer :: AST,CurrentAST
  type(Array) ASTStack
  type ProcType
    type(Array),pointer :: AST,Var,VarType
  endtype
  type(ProcType) ProcTemp
  type(Map) Proc(64)
  logical ProcIn
  type(Array),pointer :: ProcVar,ProcVarType

  logical L_
  type(Array),pointer :: Argument
  type(Map),pointer :: CallArg(:)
  type(Array) CallStack
  type Op
    logical H
    integer N
    character,pointer :: C(:)
  endtype
  type(Op) OpT
contains
  logical function Ensure(Q,S)
    integer Q,S
    Ensure = Q <= S
    do while (Q <= S)
      Q = Q + Q
    enddo
  end
  subroutine Copy(To,From)
    character,allocatable :: To(:)
    character From(:)
    if (allocated(To)) deallocate(To)
    allocate(To(size(From)))
    To = From
  end

  subroutine ArrayMake(Q)
    type(Array) Q
    Q%At = 0
    Q%Len = 32
    allocate(Q%Data(Q%Len))
  end
  subroutine ArrayCheck(Q)
    type(Array) Q
    type(ArrayNode),allocatable :: T(:)
    if (Ensure(Q%Len,Q%At)) then
      call move_alloc(Q%Data,T)
      allocate(Q%Data(Q%Len))
      Q%Data(:size(T)) = T
    endif
  end
  subroutine ArrayPush(Q,S)
    type(Array) Q
    character,optional :: S(:)
    call ArrayCheck(Q)
    Q%At = 1 + Q%At
    if (present(S)) call Copy(Q%Data(Q%At)%Data,S)
  end
  subroutine ArrayFree(Q)
    type(Array) Q
    deallocate(Q%Data)
  end
  integer function IndexOf(S,Q)
    character S(:)
    type(Array) Q
    integer F
    IndexOf = 0
    do F = 1,Q%At
      if (all(S == Q%Data(F)%Data)) then
        IndexOf = F
        return
      endif
    enddo
  end

  subroutine MapHash(Q,K,H,C)
    type(Map) Q(:)
    character K(:)
    integer H,F
    type(MapNode),pointer :: C
    H = -2128831035
    do F = 1,size(K)
      H = 16777619 * H
      H = ieor(ichar(K(F)),H)
    enddo
    C => Q(1 + modulo(H,size(Q)))%Q
  end
  subroutine MapInit(Q)
    type(Map) Q(:)
    Q = Map(null())
  end
  subroutine MapFree(Q)
    type(Map) Q(:)
    type(MapNode),pointer :: C,N
    integer F
    do F = 1,size(Q)
      C => Q(F)%Q
      do while (associated(C))
        N => C%Next
        deallocate(C%Key)
        deallocate(C%Value)
        deallocate(C)
        C => N
      enddo
      Q(F)%Q => C
    enddo
  end
  subroutine MapSet(Q,K,V)
    type(Map) Q(:)
    type(MapNode),pointer :: L,C
    character K(:),V(:)
    integer H
    call MapHash(Q,K,H,C)
    L => null()
    do while (associated(C))
      if (H == C%Hash) then
        if (all(K == C%Key)) then
          call Copy(C%Value,V)
          return
        endif
      endif
      L => C
      C => C%Next
    enddo
    allocate(C)
    C%Hash = H
    call Copy(C%Key,K)
    call Copy(C%Value,V)
    C%Next => null()
    if (associated(L)) then
      L%Next => C
    else
      Q(1 + modulo(H,size(Q)))%Q => C
    endif
  end
  logical function MapHas(Q,K)
    type(Map) Q(:)
    type(MapNode),pointer :: C
    character K(:)
    integer H
    call MapHash(Q,K,H,C)
    do while (associated(C))
      if (H == C%Hash) then
        if (all(K == C%Key)) then
          MapHas = .true.
          MapLast => C
          return
        endif
      endif
      C => C%Next
    enddo
    MapHas = .false.
  end


  subroutine OutputEnsure(Q)
    integer Q
    character(:),allocatable :: T
    if (Ensure(OLen,Q + OAt - 1)) then
      call move_alloc(O,T)
      allocate(character(OLen) :: O)
      O(:len(T)) = T
    endif
  end
  subroutine ErrorMake()
    Error = .true.
    OAt = 0
  end
  subroutine OutputString(Q)
    character(*) Q
    call OutputEnsure(len(Q))
    O(1 + OAt:) = Q
    OAt = OAt + len(Q)
  end
  subroutine OutputCharArray(Q)
    character Q(:)
    integer F
    call OutputEnsure(size(Q))
    do F = 1,size(Q)
      OAt = 1 + OAt
      O(OAt:) = Q(F)
    enddo
  end
  subroutine OutputInteger(Q)
    integer Q
    character(11) T
    write (T,'(I0)') Q
    call OutputString(T(:len_trim(T)))
  end
  subroutine OutputStringN(Q,S)
    character(*) Q
    integer S,F
    call OutputEnsure(S * len(Q))
    do F = 1,S
      O(1 + OAt:) = Q
      OAt = OAt + len(Q)
    enddo
  end

  subroutine ErrorTasteEOL()
    if (CodeLen < CodeAt) then
      call OutputString('EOL')
    else
      call OutputString(I(CodeOffset + CodeAt:CodeOffset + CodeAt))
    endif
  end
  subroutine ErrorNumberExpected()
    call ErrorMake()
    call OutputString('A number is expected but got ')
    call ErrorTasteEOL()
  end
  subroutine ErrorNameExpected()
    call ErrorMake()
    call OutputString('A variable name / command is expected but got ')
    call ErrorTasteEOL()
  end
  subroutine ErrorCommand(Q)
    character(*) Q
    call ErrorMake()
    call OutputString('Unexpected command ')
    call OutputString(Q)
  end
  subroutine ErrorCommandEnd()
    call ErrorMake()
    call OutputString('Expected end of line but got ')
    call ErrorTasteEOL()
  end
  subroutine ErrorDefineInProc()
    call ErrorMake()
    call OutputString('Cannot define variables in procedures')
  end
  subroutine ErrorVarUndefined(Q)
    character Q(:)
    call ErrorMake()
    call OutputString('Undefined variable ')
    call OutputCharArray(Q)
  end
  subroutine ErrorVarRedeclare(Q)
    character Q(:)
    call ErrorMake()
    call OutputString('Re-defined variable ')
    call OutputCharArray(Q)
  end
  subroutine ErrorVarButList(Q)
    character Q(:)
    call ErrorMake()
    call OutputString('Expected a variable but ')
    call OutputCharArray(Q)
    call OutputString(' is a list')
  end
  subroutine ErrorListButVar(Q)
    character Q(:)
    call ErrorMake()
    call OutputString('Expected a list but ')
    call OutputCharArray(Q)
    call OutputString(' is a variable')
  end
  subroutine ErrorVarTypeMismatch(Q,S)
    character Q(:)
    logical S
    call ErrorMake()
    call OutputString('Type mismatch, ')
    call OutputCharArray(Q)
    call OutputString(' was first used as a ')
    if (S) then
      call OutputString('var')
    else
      call OutputString('list')
    endif
  end
  subroutine ErrorUnEOL()
    call ErrorMake()
    call OutputString('Unexpected end of line')
  end
  subroutine ErrorUnclosed(Q)
    character(*) Q
    call ErrorMake()
    call OutputString('Unclosed ')
    call OutputString(Q)
    call OutputString(', got ')
    call ErrorTasteEOL()
  end
  subroutine ErrorBadEscape()
    call ErrorMake()
    call OutputString('Unexpected char escape \')
    call ErrorTasteEOL()
  end
  subroutine ErrorStringExpect()
    call ErrorMake()
    call OutputString('A string is expected but got ')
    call ErrorTasteEOL()
  end
  subroutine ErrorStringUnclose()
    call ErrorMake()
    call OutputString('String is not closed')
  end
  subroutine ErrorProcNested()
    call ErrorMake()
    call OutputString('Procedures should not be nested')
  end
  subroutine ErrorProcUsed(Q)
    character Q(:)
    call ErrorMake()
    call OutputString('Procedure re-defined ')
    call OutputCharArray(Q)
  end
  subroutine ErrorDupParam(Q)
    character Q(:)
    call ErrorMake()
    call OutputString('Duplicate parameter name ')
    call OutputCharArray(Q)
  end
  subroutine ErrorEndNothing()
    call ErrorMake()
    call OutputString('Nothing to end')
  end
  subroutine ErrorEndUnclose()
    call ErrorMake()
    call OutputString('Unclosed block (ifeq / ifneq / ueq / proc)')
  end
  subroutine ErrorNoProc(Q)
    character Q(:)
    call ErrorMake()
    call OutputString('Undefined procedure ')
    call OutputCharArray(Q)
  end
  subroutine ErrorProcLength(Q,W,E)
    character Q(:)
    integer W,E
    call ErrorMake()
    call OutputString('Procedure ')
    call OutputCharArray(Q)
    call OutputString(' expects ')
    call OutputInteger(W)
    call OutputString(' argument(s) but got ')
    call OutputInteger(E)
  end
  subroutine ErrorRecursive(Q)
    character Q(:)
    call ErrorMake()
    call OutputString('Recursive call ')
    call OutputCharArray(Q)
  end
  subroutine ErrorArgTypeMismatch(H,W,A,Q)
    logical H
    character W(:),Q(:)
    type(Op) A
    call ErrorMake()
    call OutputString('Type mismatch. A ')
    if (H) then
      call OutputString('var')
    else
      call OutputString('list')
    endif
    call OutputString(' is expected for parameter ')
    call OutputCharArray(W)
    call OutputString(' in `')
    call OutputCharArray(A%C)
    call OutputString(', but argument ')
    call OutputCharArray(Q)
    call OutputString(' is a ')
    if (H) then
      call OutputString('list')
    else
      call OutputString('var')
    endif
  end

  logical function VarIsNumber()
    type(VarType) T
    T = transfer(MapLast%Value,T)
    VarIsNumber = T%Len < 0
  end

  integer function Taste(Q)
    integer,optional :: Q
    integer T
    T = CodeAt
    if (present(Q)) T = T + Q
    Taste = 0
    if (T <= CodeLen) Taste = ichar(I(CodeOffset + T:))
  end
  subroutine Eat()
    CodeAt = 1 + CodeAt
  end
  subroutine Walk(Q)
    logical Q
    do while (Q(Taste()))
      call Eat()
    enddo
  end
  logical function TestSpace(Q)
    integer Q
    TestSpace = 8 < Q .and. Q < 14 .or. 32 == Q
  end
  logical function TestIdentifierPrefix(Q)
    integer Q
    TestIdentifierPrefix = 36 == Q .or. 95 == Q .or. 64 < Q .and. Q < 91 .or. 96 < Q .and. Q < 123
  end
  logical function TestIdentifierSuffix(Q)
    integer Q
    TestIdentifierSuffix = 36 == Q .or. 95 == Q .or. 47 < Q .and. Q < 58 .or. 64 < Q .and. Q < 91 .or. 96 < Q .and. Q < 123
  end
  logical function TestNumber(Q)
    integer Q
    TestNumber = 47 < Q .and. Q < 58
  end
  subroutine Discard()
    CodeAt = 1 + CodeLen
  end
  subroutine White()
    call Walk(TestSpace)
    if (45 == Taste() .and. 45 == Taste(1) .or. &
      47 == Taste() .and. 47 == Taste(1) .or. &
      35 == Taste()) call Discard()
  end
  function Word() result(R)
    character,pointer :: R(:)
    integer :: S,T,F
    S = CodeAt
    R => null()
    if (Error) return
    if (CodeAt <= CodeLen) then
      if (.not. TestIdentifierPrefix(Taste())) then
        call ErrorNameExpected()
        return
      endif
    endif
    call Walk(TestIdentifierSuffix)
    allocate(R(CodeAt - S))
    do F = S,CodeAt - 1
      T = ichar(I(CodeOffset + F:))
      if (96 < T) T = T - 32
      R(1 + F - S) = char(T)
    enddo
    call White()
  end
  function MakeName(H) result(R)
    logical H,T
    character,pointer :: R(:)
    integer F
    R => Word()
    if (.not. associated(R)) call ErrorNameExpected()
    if (size(R) < 1 .and. .not. Error) call ErrorNameExpected()
    if (Error) return
    if (ProcIn) then
      F = IndexOf(R,ProcVar)
      if (0 < F) then
        if (allocated(ProcVarType%Data(F)%Data)) then
          T = transfer(ProcVarType%Data(F)%Data,T)
          if (T .neqv. H) call ErrorVarTypeMismatch(R,H)
        else
          call Copy(ProcVarType%Data(F)%Data,transfer(H,Y))
        endif
        return
      endif
    endif
    if (.not. MapHas(Var,R)) then
      call ErrorVarUndefined(R)
      return
    endif
    if (H .neqv. VarIsNumber()) then
      if (H) then
        call ErrorVarButList(R)
      else
        call ErrorListButVar(R)
      endif
    endif
  end
  function VarName()
    character,pointer :: VarName(:)
    VarName => MakeName(.true.)
  end
  function ListName()
    character,pointer :: ListName(:)
    ListName => MakeName(.false.)
  end
  function RawNumber() result(R)
    integer S,R
    logical M
    M = 45 == Taste()
    if (M) call Eat()
    S = CodeAt
    R = 0
    do while (TestNumber(Taste()))
      R = 10 * R + Taste() - 48
      call Eat()
    enddo
    if (M) R = -R
    if (CodeAt == S) then
      call ErrorNumberExpected()
      return
    endif
    call White()
  end
  integer function Number()
    Number = modulo(RawNumber(),256)
  end
  function ReadChar() result(R)
    integer R
    R = Taste()
    call Eat()
    if (92 == R) then
      select case (Taste())
        case (92)
          R = 92
        case (34)
          R = 34
        case (39)
          R = 39
        case (110)
          R = 10
        case (114)
          R = 13
        case (116)
          R = 9
        case default
          call ErrorBadEscape()
      endselect
      call Eat()
    endif
  end
  integer function NumberOrChar()
    if (39 == Taste()) then
      call Eat()
      NumberOrChar = ReadChar()
      if (39 /= Taste()) then
        call ErrorUnclosed("'")
        return
      endif
      call Eat()
      call White()
    else
      NumberOrChar = Number()
    endif
  end
  function VarNameOrNumber() result(R)
    type(Op) R
    R%H = 39 == Taste() .or. 45 == Taste() .or. TestNumber(Taste())
    if (R%H) then
      R%N = NumberOrChar()
      R%C => null()
    else
      R%C => VarName()
    endif
  end
  function String() result(R)
    character,pointer :: R(:),T(:)
    integer At,Len
    At = 0
    Len = 32
    allocate(R(Len))
    if (34 /= Taste()) then
      call ErrorStringExpect()
      return
    endif
    call Eat()
    do while (0 < Taste() .and. 34 /= Taste())
      At = 1 + At
      if (Len < At) then
        T => R
        allocate(R(Len + Len))
        R(:Len) = T
        Len = Len + Len
        deallocate(T)
      endif
      R(At) = char(ReadChar())
      if (Error) return
    enddo
    if (34 /= Taste()) then
      call ErrorStringUnclose()
      return
    endif
    call Eat()
    call White()
    T => R
    allocate(R(At))
    R = T(:At)
    deallocate(T)
  end
  function VarNameOrString() result(R)
    type(Op) R
    R%H = 34 == Taste()
    if (R%H) then
      R%C => String()
    else
      R%C => VarName()
    endif
  end
  subroutine ArgInit(Q)
    integer Q
    allocate(Argument)
    Argument%At = 0
    Argument%Len = Q
    allocate(Argument%Data(Q))
  end
  subroutine ArgID(Q)
    integer Q
    Argument%Len = Argument%At
    Argument%At = Q
  end
  subroutine ArgMake(Q,S)
    integer Q,S(:),F
    call ArgInit(size(S))
    do F = 1,size(S)
      if (S(F) < 5) then
        OpT%H = .false.
        if (S(F) < 2) then
          OpT%C => VarName()
        else
          OpT%C => ListName()
        endif
        call ArrayPush(Argument,transfer(OpT,Y))
      else
        call ArrayPush(Argument,transfer(VarNameOrNumber(),Y))
      endif
      if (Error) exit
    enddo
    call ArgID(Q)
  end
  subroutine ASTFree(Q)
    type(Array),pointer :: Q
    type(ArrayPointer) ArgumentWrap
    integer F,G
    do F = 1,Q%At
      ArgumentWrap = transfer(Q%Data(F)%Data,ArgumentWrap)
      Argument => ArgumentWrap%Data
      do G = 1,Argument%Len
        OpT = transfer(Argument%Data(G)%Data,OpT)
        if (associated(OpT%C)) deallocate(OpT%C)
      enddo
      deallocate(Argument)
    enddo
    deallocate(Q)
  end

  subroutine OpGotoCell(Q)
    integer Q
    if (Q < StackAt) then
      call OutputStringN('<',StackAt - Q)
    else
      call OutputStringN('>',Q - StackAt)
    endif
    StackAt = Q
  end
  subroutine OpAdd(Q)
    integer Q,S
    S = modulo(Q,256)
    if (128 < S) then
      call OutputStringN('-',256 - S)
    else
      call OutputStringN('+',S)
    endif
  end
  integer function OpSolvePreserve(Q)
    integer Q
    if (PreserveMax < Q) PreserveMax = Q
    OpSolvePreserve = Preserve - Q
  end
  subroutine OpFly(Q)
    integer Q
    StackAt = OpSolvePreserve(Q)
  end
  subroutine OpGotoPreserve(Q)
    integer Q
    call OpGotoCell(OpSolvePreserve(Q))
  end
  integer function OpGetPreserve(Q)
    integer Q
    OpGetPreserve = Stack(OpSolvePreserve(Q))
  end
  subroutine OpSetPreserve(Q,S)
    integer Q,S
    Stack(OpSolvePreserve(Q)) = S
  end
  subroutine OpModifyPreserve(Q,S)
    integer Q,S
    call OpGotoPreserve(Q)
    call OpAdd(S - OpGetPreserve(Q))
    call OpSetPreserve(Q,S)
  end
  subroutine OpClearPreserve(Q,J)
    integer Q
    logical,optional :: J
    if (present(J)) then
      if (J) then
        call OpGotoPreserve(Q)
        call OutputString('[-]')
        call OpSetPreserve(Q,0)
      endif
    endif
    if (0 < OpGetPreserve(Q)) then
      call OpGotoPreserve(Q)
      call OutputString('[-]')
      call OpSetPreserve(Q,0)
    endif
  end
  subroutine OpMsgList(Q)
    character Q(:)
    integer F
    do F = 1,size(Q)
      call OpModifyPreserve(0,ichar(Q(F)))
      call OutputString('.')
    enddo
  end

  type(Op) function OpN(Q)
    integer Q
    OpN%H = .true.
    OpN%N = Q
  end
  type(Op) function OpC(Q)
    character,target :: Q(:)
    OpC%H = .false.
    OpC%C => Q
  end
  type(Op) function OpR(Arg,Q)
    type(Array) Arg
    integer Q
    OpR = transfer(Arg%Data(1 + Q)%Data,OpR)
  end
  subroutine OpSolveVar(Q)
    character Q(:)
    if (associated(CallArg)) then
        if (MapHas(CallArg,Q)) then
        L_ = MapHas(Var,MapLast%Value)
      else
        L_ = MapHas(Var,Q)
      endif
    else
      L_ = MapHas(Var,Q)
    endif
    VarTemp = transfer(MapLast%Value,VarTemp)
  end
  subroutine OpGoto(Q,S)
    type(Op) Q
    integer,optional :: S
    if (Q%H) then
      if (Q%N < 0) then
        call OpGotoCell(-Q%N)
      else
        call OpGotoPreserve(Q%N)
      endif
    else
      call OpSolveVar(Q%C)
      if (VarTemp%Len < 0) then
        call OpGotoCell(VarTemp%At)
      else if (present(S)) then
        call OpGotoCell(S + VarTemp%At)
      else
        call OpGotoCell(VarTemp%At)
      endif
    endif
  end
  subroutine OpClear(Q,J)
    type(Op) Q
    logical,optional :: J
    if (Q%H) then
      call OpClearPreserve(Q%N,J)
    else
      call OpGoto(Q)
      call OutputString('[-]')
    endif
  end
  subroutine OpBegin(Q,S)
    type(Op) Q
    integer,optional :: S
    call OpGoto(Q,S)
    call OutputString('[-')
  end
  subroutine OpEnd(Q,S)
    type(Op) Q
    integer,optional :: S
    call OpGoto(Q,S)
    call OutputString(']')
  end
  subroutine OpMove(Q,S,I)
    type(Op) Q,S
    integer,optional :: I
    call OpBegin(Q,I)
    call OpGoto(S)
    call OutputString('+')
    call OpEnd(Q,I)
  end
  subroutine OpMoveTwo(Q,S,W,I)
    type(Op) Q,S,W
    integer,optional :: I
    call OpBegin(Q,I)
    call OpGoto(S)
    call OutputString('+')
    call OpGoto(W)
    call OutputString('+')
    call OpEnd(Q,I)
  end
  subroutine OpMoveThree(Q,S,W,A,I)
    type(Op) Q,S,W,A
    integer,optional :: I
    call OpBegin(Q,I)
    call OpGoto(S)
    call OutputString('+')
    call OpGoto(W)
    call OutputString('+')
    call OpGoto(A)
    call OutputString('+')
    call OpEnd(Q,I)
  end
  subroutine OpMoveReverse(Q,S,I)
    type(Op) Q,S
    integer,optional :: I
    call OpBegin(Q,I)
    call OpGoto(S)
    call OutputString('-')
    call OpEnd(Q,I)
  end
  subroutine OpCopy(Q,S,T,J)
    type(Op) Q,S,T
    logical,optional :: J
    if (.not. present(J)) then
      call OpClear(T)
    elseif (J) then
      call OpClear(T)
    endif
    call OpMoveTwo(Q,S,T)
    call OpMove(T,Q)
  end
  subroutine OpCopyTwo(Q,S,W,T,J)
    type(Op) Q,S,W,T
    logical,optional :: J
    if (.not. present(J)) then
      call OpClear(T)
    elseif (J) then
      call OpClear(T)
    endif
    call OpMoveThree(Q,S,W,T)
    call OpMove(T,Q)
  end
  subroutine OpPrepare(Q,S,T)
    type(Op) Q,S
    integer T
    call OpClear(S)
    if (Q%H) then
      call OpGoto(S)
      call OpAdd(Q%N)
    else
      call OpCopy(Q,S,OpN(T))
    endif
  end
  subroutine OpPrepareTwo(Q,S,W,T)
    type(Op) Q,S,W
    integer T
    if (Q%H) then
      call OpGoto(OpN(T))
      call OpAdd(Q%N)
      call OpMoveTwo(OpN(T),S,W)
    else
      call OpCopyTwo(Q,S,W,OpN(T))
    endif
  end
  subroutine OpPrepare01(Arg,W_,A_,T_)
    type(Array) Arg
    integer,optional :: W_,A_,T_
    integer W,A,T
    W = 0
    A = 1
    T = 2
    if (present(W_)) W = W_
    if (present(A_)) A = A_
    if (present(T_)) T = T_
    call OpPrepare(OpR(Arg,0),OpN(W),T)
    call OpPrepare(OpR(Arg,1),OpN(A),T)
  end
  subroutine OpSet(Q,S)
    type(Op) Q,S
    call OpClear(Q)
    call OpMove(S,Q)
  end
  subroutine OpDivMod(Arg,D,M,Q,S)
    type(Array) Arg
    integer D,M
    type(Op),optional :: Q,S
    if (present(Q)) then
      call OpPrepare(Q,OpN(5),0)
    else
      call OpPrepare(OpR(Arg,0),OpN(5),0)
    endif
    if (present(S)) then
      call OpPrepare(S,OpN(4),0)
    else
      call OpPrepare(OpR(Arg,1),OpN(4),0)
    endif
    call OpCopy(OpN(4),OpN(8),OpN(7))
    call OpGoto(OpN(7))
    call OutputString('+<-')
    call OutputString('[>>>[->-[>+>>]>[+[-<+>]>+>>]<<<<<]<<-]>')
    call OutputString('[->>[->>>+<<<]<]')
    call OpFly(6)
    call OpClear(OpN(8),.true.)
    call OpClear(OpN(4),.true.)
    if (0 < D) then
      call OpSet(OpR(Arg,D),OpN(2))
    else
      call OpClear(OpN(2),.true.)
    endif
    if (0 < M) then
      call OpSet(OpR(Arg,M),OpN(3))
    else
      call OpClear(OpN(3),.true.)
    endif
  end
  subroutine OpIfWhile(Arg,Not)
    type(Array) Arg
    logical,optional :: Not
    OpT = OpR(Arg,1)
    if (OpT%H) then
      call OpClear(OpN(0))
      call OpCopy(OpR(Arg,0),OpN(0),OpN(1))
      call OpGoto(OpN(0))
      call OpAdd(-OpT%N)
    else
      call OpPrepare01(Arg)
      call OpMoveReverse(OpN(1),OpN(0))
    endif
    if (present(Not)) then
      if (Not) then
        call OpGoto(OpN(1))
        call OutputString('+>[[-]<-]<[>+<-<]')
        call OpFly(2)
      endif
    endif
    call OpGoto(OpN(0))
  end

  recursive subroutine Generate(AST_)
    type(Array),pointer :: AST_,AST,Arg
    type(Map),pointer :: CallArg_(:)
    type(ArrayPointer) Argument
    integer X,T0,T1,F
    AST => AST_
    CallArg_ => CallArg
    do F = 1,AST%At
      Argument = transfer(AST%Data(F)%Data,Argument)
      Arg => Argument%Data
      select case (Arg%At)
        case (8000) ! set
          call OpGoto(OpR(Arg,0))
          call OutputString('[-]')
          OpT = OpR(Arg,1)
          if (OpT%H) then
            call OpAdd(OpT%N)
          else
            call OpCopy(OpR(Arg,1),OpR(Arg,0),OpN(0))
          endif
        case (8010) ! inc
          OpT = OpR(Arg,1)
          if (OpT%H) then
            call OpGoto(OpR(Arg,0))
            call OpAdd(OpT%N)
          else
            call OpCopy(OpT,OpN(0),OpN(1))
            call OpMove(OpN(0),OpR(Arg,0))
          endif
        case (8011) ! dec
          OpT = OpR(Arg,1)
          if (OpT%H) then
            call OpGoto(OpR(Arg,0))
            call OpAdd(-OpT%N)
          else
            call OpCopy(OpT,OpN(0),OpN(1))
            call OpMoveReverse(OpN(0),OpR(Arg,0))
          endif
        case (8012) ! add
          call OpPrepare01(Arg)
          call OpMove(OpN(1),OpN(0))
          call OpSet(OpR(Arg,2),OpN(0))
        case (8013) ! sub
          call OpPrepare01(Arg)
          call OpMoveReverse(OpN(1),OpN(0))
          call OpSet(OpR(Arg,2),OpN(0))
        case (8014) ! mul
          call OpPrepare01(Arg)
          call OpBegin(OpN(0))
          call OpCopy(OpN(1),OpN(2),OpN(3))
          call OpEnd(OpN(0))
          call OpClear(OpN(1),.true.)
          call OpSet(OpR(Arg,2),OpN(2))
        case (8015) ! divmod
          call OpDivMod(Arg,2,3)
        case (8016) ! div
          call OpDivMod(Arg,2,0)
        case (8017) ! mod
          call OpDivMod(Arg,0,2)
        case (8020) ! cmp
          X = 4
          T0 = 3
          T1 = 2
          call OpPrepareTwo(OpR(Arg,0),OpN(T0),OpN(X),0)
          call OpPrepareTwo(OpR(Arg,1),OpN(T1),OpN(1 + X),0)
          call OpMoveReverse(OpN(1 + X),OpN(X))

          call OpGoto(OpN(1 + X))
          call OutputString('+>[[-]')
          call OpFly(X)

          call OpGoto(OpN(T1 - 1))
          call OutputString('+<[>-]>[')
          call OpFly(T1 - 1)
          call OpGoto(OpN(X))
          call OutputString('+')
          call OpGoto(OpN(T0))
          call OutputString('[-]')
          call OpGoto(OpN(T1 - 1))
          call OutputString('->]<+')
          call OpGoto(OpN(T0))
          call OutputString('[')
          call OpGoto(OpN(T1))
          call OutputString('-[>-]>[')
          call OpFly(T1 - 1)
          call OpGoto(OpN(X))
          call OutputString('+')
          call OpGoto(OpN(T0))
          call OutputString('[-]+')
          call OpGoto(OpN(T1 - 1))
          call OutputString('->]<+')
          call OpGoto(OpN(T0))
          call OutputString('-]')

          call OpGoto(OpN(X))
          call OutputString('[<-]<[>-<-<]')
          call OpFly(2 + X)

          call OpGoto(OpN(1 + X))
          call OutputString(']<[-<]>')

          call OpClear(OpN(3),.true.)
          call OpClear(OpN(2),.true.)
          call OpClear(OpN(1),.true.)

          call OpSet(OpR(Arg,2),OpN(X))
        case (8030) ! a2b
          call OpCopy(OpR(Arg,0),OpN(2),OpN(0))
          call OpGoto(OpN(2))
          call OpAdd(-48)
          call OpBegin(OpN(2))
          call OpGoto(OpN(1))
          call OpAdd(10)
          call OpEnd(OpN(2))

          call OpCopy(OpR(Arg,1),OpN(1),OpN(0))
          call OpGoto(OpN(1))
          call OpAdd(-48)

          call OpBegin(OpN(1))
          call OpGoto(OpN(0))
          call OpAdd(10)
          call OpEnd(OpN(1))

          call OpCopy(OpR(Arg,2),OpN(0),OpN(1))
          call OpGoto(OpN(0))
          call OpAdd(-48)

          call OpSet(OpR(Arg,3),OpN(0))
        case (8031) ! b2a
          call OpDivMod(Arg,2,3,OpR(Arg,0),OpN(10))
          call OpDivMod(Arg,1,2,OpR(Arg,2),OpN(10))
          call OpGoto(OpR(Arg,1))
          call OpAdd(48)
          call OpGoto(OpR(Arg,2))
          call OpAdd(48)
          call OpGoto(OpR(Arg,3))
          call OpAdd(48)
        case (8040) ! lset
          OpT = OpR(Arg,0)
          call OpSolveVar(OpT%C)
          OpT = OpR(Arg,1)
          if (OpT%H) then
            call OpGoto(OpR(Arg,0))
            call OpAdd(OpT%N)
            call OutputString('[->+>+<<]')
          else
            call OpCopyTwo(OpR(Arg,1),OpN(-1 - VarTemp%At),OpN(-2 - VarTemp%At),OpR(Arg,0),.false.)
          endif
          OpT = OpR(Arg,2)
          if (OpT%H) then
            call OpGoto(OpR(Arg,0),3)
            call OpAdd(OpT%N)
          else
            call OpCopy(OpR(Arg,2),OpN(-3 - VarTemp%At),OpR(Arg,0),.false.)
          endif
          call OpGoto(OpR(Arg,0))
          call OutputString('>[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]')
          call OutputString('>>>[-]<[->+<]<')
          call OutputString('[[-<+>]<<<[->>>>+<<<<]>>-]<<')
        case (8041) ! lget
          OpT = OpR(Arg,0)
          call OpSolveVar(OpT%C)
          OpT = OpR(Arg,1)
          if (OpT%H) then
            call OpGoto(OpR(Arg,0))
            call OpAdd(OpT%N)
            call OutputString('[->+>+<<]')
          else
            call OpCopyTwo(OpR(Arg,1),OpN(-1 - VarTemp%At),OpN(-2 - VarTemp%At),OpR(Arg,0),.false.)
          endif
          call OpGoto(OpR(Arg,0))
          call OutputString('>[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]')
          call OutputString('>>>[-<+<<+>>>]<<<[->>>+<<<]>')
          call OutputString('[[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<')
          call OpClear(OpR(Arg,2))
          call OpMove(OpR(Arg,0),OpR(Arg,2),3)
        case (8050,8052) ! ifeq,weq
          call OpIfWhile(Arg,.true.)
          call OutputString('[')
          call OpClear(OpN(0),.true.)
        case (8051) ! ifneq
          call OpIfWhile(Arg)
          call OutputString('[')
          call OpClear(OpN(0),.true.)
        case (8053) ! wneq
          OpT = OpR(Arg,1)
          if (0 < OpT%N) then
            call OpIfWhile(Arg)
            call OutputString('[')
            call OpClear(OpN(0),.true.)
          else
            call OpGoto(OpR(Arg,0))
            call OutputString('[')
          endif
        case (8054) ! end
          OpT = OpR(Arg,0)
          Argument = transfer(AST%Data(OpT%N)%Data,Argument)
          Arg => Argument%Data
          if (8052 == Arg%At) then
            call OpIfWhile(Arg,.true.)
            call OpGoto(OpN(0))
          else if (8053 == Arg%At) then
            OpT = OpR(Arg,1)
            if (0 < OpT%N) then
              call OpIfWhile(Arg)
              call OpGoto(OpN(0))
            else
              call OpGoto(OpR(Arg,0))
            endif
          else
            call OpClear(OpN(0))
            call OpGoto(OpN(0))
          endif
          call OutputString(']')
        case (8055) ! call
          OpT = OpR(Arg,0)
          if (.not. MapHas(Proc,OpT%C)) then
            call ErrorNoProc(OpT%C)
            exit
          endif
          ProcTemp = transfer(MapLast%Value,ProcTemp)
          ProcVar => ProcTemp%Var
          ProcVarType => ProcTemp%VarType
          if (1 + ProcVar%At /= Arg%Len) then
            call ErrorProcLength(OpT%C,ProcVar%At,Arg%Len - 1)
            exit
          endif
          if (0 < IndexOf(OpT%C,CallStack)) then
            call ErrorRecursive(OpT%C)
            exit
          endif
          call ArrayPush(CallStack,OpT%C)
          allocate(CallArg(64))
          call MapInit(CallArg)
          do X = 1,ProcVar%At
            OpT = OpR(Arg,X)
            if (associated(CallArg_)) then
                if (MapHas(CallArg_,OpT%C)) then
                call MapSet(CallArg,ProcVar%Data(X)%Data,MapLast%Value)
                L_ = MapHas(Var,MapLast%Value)
              else
                call MapSet(CallArg,ProcVar%Data(X)%Data,OpT%C)
                L_ = MapHas(Var,OpT%C)
              endif
            else
              call MapSet(CallArg,ProcVar%Data(X)%Data,OpT%C)
              L_ = MapHas(Var,OpT%C)
            endif
            VarTemp = transfer(MapLast%Value,VarTemp)
            if (allocated(ProcVarType%Data(X)%Data)) then
              L_ = transfer(ProcVarType%Data(X)%Data,L_)
              if (L_ .neqv. (VarTemp%Len < 0)) then
                call ErrorArgTypeMismatch(L_,ProcVar%Data(X)%Data,OpR(Arg,0),OpT%C)
                exit
              endif
            endif
          enddo
          if (.not. Error) call Generate(ProcTemp%AST)
          call MapFree(CallArg)
          deallocate(CallArg)
          CallArg => CallArg_
          CallStack%At = CallStack%At - 1
        case (8060) ! read
          call OpGoto(OpR(Arg,0))
          call OutputString(',')
        case (8061,8062) ! msg
          do X = 1,Arg%Len
            OpT = OpR(Arg,X - 1)
            if (OpT%H) then
              call OpMsgList(OpT%C)
            else
              call OpGoto(OpT)
              call OutputString('.')
            endif
          enddo
          if (8062 == Arg%At) call OpMsgList([char(10)])
        case (8400) ! debug
          call OutputString('_')
      endselect
    enddo
  end

  integer function kcuf(Output,Code)
    character(:),allocatable :: Output
    character(*) Code
    character(6) Command
    type(ArrayPointer) ArgumentWrap
    character,pointer :: V(:)
    integer F,G

    Error = .false.
    allocate(character(len(Code)) :: I)
    I = Code
    OAt = 0
    if (.not. allocated(O)) then
      OLen = 32
      allocate(character(OLen) :: O)
    endif
    PreserveMax = -1
    Stack = 0
    StackAt = 0
    VarAt = 1 + Preserve
    call MapInit(Var)
    allocate(AST)
    call ArrayMake(AST)
    CurrentAST => AST
    call ArrayMake(ASTStack)
    call MapInit(Proc)
    ProcIn = .false.
    call ArrayMake(CallStack)

    CodeOffset = 0
    do while (CodeOffset < len(Code))
      do F = 1 + CodeOffset,len(Code)
        if (10 == ichar(Code(F:))) exit
      enddo
      CodeAt = 1
      CodeLen = F - CodeOffset - 1
      call White()
      if (0 < Taste()) then
        V => Word()
        if (Error) exit
        Command = transfer(V,Command)
        G = size(V)
        deallocate(V)
        select case (Command(:G))
          case ('VAR')
            if (ProcIn) then
              call ErrorDefineInProc()
              exit
            endif
            if (Taste() < 1) then
              call ErrorUnEOL()
              exit
            endif
            V => Word()
            do while (0 < size(V) .and. .not. Error)
              if (MapHas(Var,V)) then
                call ErrorVarRedeclare(V)
                exit
              endif
              if (91 == Taste()) then
                call Eat()
                call White()
                VarTemp%Len = RawNumber()
                if (Error) exit
                if (93 /= Taste()) then
                  call ErrorUnclosed('[')
                  exit
                endif
                call Eat()
                call White()
                VarTemp%At = VarAt
                VarAt = 4 + VarAt + VarTemp%Len
              else
                VarTemp%At = VarAt
                VarTemp%Len = -1
                VarAt = 1 + VarAt
              endif
              call MapSet(Var,V,transfer(VarTemp,Y))
              deallocate(V)
              V => Word()
            enddo
            if (associated(V)) deallocate(V)

          case ('SET')
            call ArgMake(8000,[0,9])

          case ('INC')
            call ArgMake(8010,[0,9])
          case ('DEC')
            call ArgMake(8011,[0,9])
          case ('ADD')
            call ArgMake(8012,[9,9,0])
          case ('SUB')
            call ArgMake(8013,[9,9,0])
          case ('MUL')
            call ArgMake(8014,[9,9,0])
          case ('DIVMOD')
            call ArgMake(8015,[9,9,0,0])
          case ('DIV')
            call ArgMake(8016,[9,9,0])
          case ('MOD')
            call ArgMake(8017,[9,9,0])

          case ('CMP')
            call ArgMake(8020,[9,9,0])

          case ('A2B')
            call ArgMake(8030,[9,9,9,0])
          case ('B2A')
            call ArgMake(8031,[9,0,0,0])

          case ('LSET')
            call ArgMake(8040,[2,9,9])
          case ('LGET')
            call ArgMake(8041,[2,9,0])

          case ('IFEQ')
            call ArgMake(8050,[0,9])
            call ArrayPush(ASTStack,transfer(CurrentAST%At,Y))
          case ('IFNEQ')
            call ArgMake(8051,[0,9])
            call ArrayPush(ASTStack,transfer(CurrentAST%At,Y))
          case ('WEQ')
            call ArgMake(8052,[0,9])
            call ArrayPush(ASTStack,transfer(CurrentAST%At,Y))
          case ('WNEQ')
            call ArgMake(8053,[0,9])
            call ArrayPush(ASTStack,transfer(CurrentAST%At,Y))
          case ('PROC')
            if (ProcIn) then
              call ErrorProcNested()
              exit
            endif
            ProcIn = .true.
            V => Word()
            if (Error) exit
            if (MapHas(Proc,V)) then
              call ErrorProcUsed(V)
              exit
            endif
            allocate(CurrentAST)
            allocate(ProcVar)
            allocate(ProcVarType)
            call ArrayMake(CurrentAST)
            call ArrayMake(ProcVar)
            call ArrayMake(ProcVarType)
            ProcTemp%AST => CurrentAST
            ProcTemp%Var => ProcVar
            ProcTemp%VarType => ProcVarType
            call MapSet(Proc,V,transfer(ProcTemp,Y))
            do while (0 < Taste())
              V => Word()
              if (Error) exit
              if (0 < IndexOf(V,ProcVar)) then
                call ErrorDupParam(V)
                deallocate(V)
                exit
              endif
              call ArrayPush(ProcVar,V)
              call ArrayPush(ProcVarType)
            enddo
          case ('END')
            if (0 < ASTStack%At) then
              call ArgInit(1)
              OpT%C => null()
              OpT%N = 1 + transfer(ASTStack%Data(ASTStack%At)%Data,OpT%N)
              call ArrayPush(Argument,transfer(OpT,Y))
              ASTStack%At = ASTStack%At - 1
              call ArgID(8054)
            else if (ProcIn) then
              CurrentAST => AST
              ProcIn = .false.
            else
              call ErrorEndNothing()
            endif
          case ('CALL')
            call ArgInit(16)
            do while (0 < Taste() .and. .not. Error)
              OpT%C => Word()
              call ArrayPush(Argument,transfer(OpT,Y))
            enddo
            call ArgID(8055)

          case ('READ')
            call ArgMake(8060,[0])
          case ('MSG','LN')
            call ArgInit(16)
            do while (0 < Taste() .and. .not. Error)
              call ArrayPush(Argument,transfer(VarNameOrString(),Y))
            enddo
            if (2 < G) then
              call ArgID(8061)
            else
              call ArgID(8062)
            endif

          case ('REM')
            call Discard()

          case ('DEBUG')
            call ArgInit(0)
            call ArgID(8400)
            call Discard()

          case default
            call ErrorCommand(Command(:G))
        endselect
        if (0 < Taste() .and. .not. Error) call ErrorCommandEnd()
        if (associated(Argument)) then
          ArgumentWrap%Data => Argument
          call ArrayPush(CurrentAST,transfer(ArgumentWrap,Y))
          Argument => null()
        endif
        if (Error) exit
      endif
      CodeOffset = F
    enddo

    if (.not. Error) then
      if (0 < ASTStack%At) then
        call ErrorEndUnclose()
      endif
    endif
    CallArg => null()
    if (.not. Error) call Generate(AST)

    call ArrayFree(CallStack)
    call MapFree(Proc)
    call ArrayFree(ASTStack)
    call ASTFree(AST)
    call MapFree(Var)
    kcuf = 0
    if (Error) then
      allocate(character(OAt) :: Output)
      Output = O(:OAt)
      kcuf = 9
    else
      allocate(character(OAt - Preserve + PreserveMax) :: Output)
      Output = O(1 + Preserve - PreserveMax:OAt)
    endif
    deallocate(I)
  end
end
