59f9cad032b8b91e12000035



#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

#ifdef __x86_64__
  typedef long int Int;
#else
  typedef int Int;
#endif

int EnsureLast;
int Ensure(int* Q,int S)
{
  EnsureLast = 0;
  if (*Q <= S) for (EnsureLast = *Q;*Q <= S;) *Q *= 2;
  return EnsureLast;
}
char* Clone(const char* Q)
{
  char* R = malloc(sizeof(char) * (1 + strlen(Q)));
  strcpy(R,Q);
  return R;
}

int OP,OO;
char* O;
void OutputEnsure(int L)
{
  char* T = O;
  if (Ensure(&OO,OP + L))
  {
    O = malloc(sizeof(char) * OO);
    memcpy(O,T,sizeof(char) * EnsureLast);
    free(T);
  }
}
void OutputChar(char Q)
{
  OutputEnsure(1);
  O[OP++] = Q;
}
void OutputCharN(char Q,int S)
{
  OutputEnsure(S);
  for (;S--;) O[OP++] = Q;
}
void OutputInt(int Q)
{
  int T = Q,L = 0;
  for (;++L,T /= 10;);
  OutputEnsure(L + (Q < 0));
  if (Q < 0) O[OP++] = '-';
  Q = abs(Q);
  for (L = OP += L;O[--L] = 48 + Q % 10,Q /= 10;);
}
void OutputString(char* Q)
{
  OutputEnsure(strlen(Q));
  for (;*Q;) O[OP++] = *Q++;
}

typedef struct Array{int P,O;Int* D;}* Array;
Array ArrayMake()
{
  Array R = malloc(sizeof(struct Array));
  R->P = 0;
  R->O = 32;
  R->D = malloc(sizeof(Int) * R->O);
  memset(R->D,0,sizeof(Int) * R->O);
  return R;
}
void ArrayFree(Array Q)
{
  free(Q->D);
  free(Q);
}
void ArrayEnsure(Array Q)
{
  Int* T = Q->D;
  if (Ensure(&Q->O,Q->P))
  {
    Q->D = malloc(sizeof(Int) * Q->O);
    memcpy(Q->D,T,sizeof(Int) * EnsureLast);
    free(T);
  }
}
void ArrayPush(Array Q,Int S)
{
  ArrayEnsure(Q);
  Q->D[Q->P++] = S;
}

#define MapSize 64
typedef struct MapNode
{
  int H;
  char* K;
  Int V;
  struct MapNode* N;
}* MapNode;
typedef struct Map{MapNode D[MapSize];}* Map;
Map MapMake()
{
  Map R = malloc(sizeof(struct Map));
  memset(R->D,0,sizeof(R->D));
  return R;
}
void MapFree(Map Q,void S(Int))
{
  for (int F = MapSize;F;) for (MapNode C = Q->D[--F],T;(T = C);)
  {
    C = C->N;
    free(T->K);
    if (S) S(T->V);
    free(T);
  }
  free(Q);
}
int MapHash(const char* K)
{
  int R = -2128831035;
  for (;*K;) R = 16777619 * R | *K++;
  return R;
}
void MapSet(Map Q,const char* K,Int V)
{
  int H = MapHash(K);
  MapNode L = 0,C = Q->D[(MapSize - 1) & H];
  for (;C;L = C,C = C->N) if (H == C->H && !strcmp(K,C->K))
  {
    C->V = V;
    return;
  }
  C = malloc(sizeof(struct MapNode));
  C->H = H;
  C->K = Clone(K);
  C->V = V;
  C->N = 0;
  if (L) L->N = C;
  else Q->D[(MapSize - 1) & H] = C;
}
Int MapLast;
int MapHas(Map Q,const char* K)
{
  int H = MapHash(K);
  MapNode C = Q->D[(MapSize - 1) & H];
  for (;C;C = C->N) if (H == C->H && !strcmp(K,C->K))
  {
    MapLast = C->V;
    return 9;
  }
  return 0;
}

typedef struct VarType{int P,L;}* VarType;
typedef struct ProcType{Array AST,Var,VarType;}* ProcType;
typedef struct Op{int H;Int N;char* C;}* Op;

const char *I,*IE;
int Preserve = 9,PreserveMax,Stack[9],StackAt,VarAt,Error,F;
Map Var,Proc;
Array AST,ASTStack,CurrentAST,ProcVar,ProcVarType;

VarType VarT;
ProcType ProcT;
Op OpT;
Array Arg;
Map CallArg;
Array CallStack;

char CaseSensetive(char Q){return 96 < Q && Q < 123 ? Q - 32 : Q;}
int IndexOf(Array Q,const char* S)
{
  for (int F = Q->P;F;) if (!strcmp(S,(const char*)Q->D[--F])) return F;
  return -1;
}

char Taste(){return I < IE ? *I : 0;}
void ErrorMake()
{
  Error = 9;
  OP = 0;
}
void ErrorEOL()
{
  if (Taste()) OutputChar(Taste());
  else OutputString("EOL");
}
void ErrorNumberExpected()
{
  ErrorMake();
  OutputString("A number is expected but got ");
  ErrorEOL();
}
char* ErrorNameExpected()
{
  ErrorMake();
  OutputString("A variable name / command is expected but got ");
  ErrorEOL();
  return 0;
}
void ErrorCommand(char* Q)
{
  ErrorMake();
  OutputString("Unexpected command ");
  OutputString(Q);
}
void ErrorCommandEnd()
{
  ErrorMake();
  OutputString("Expected end of line but got ");
  ErrorEOL();
}
void ErrorDefineInProc()
{
  ErrorMake();
  OutputString("Cannot define variables in procedures");
}
char* ErrorVarUndefined(char* Q)
{
  ErrorMake();
  OutputString("Undefined variable ");
  OutputString(Q);
  return Q;
}
void ErrorVarRedeclare(char* Q)
{
  ErrorMake();
  OutputString("Re-defined variable ");
  OutputString(Q);
}
char* ErrorVarButList(char* Q)
{
  ErrorMake();
  OutputString("Expected a variable but ");
  OutputString(Q);
  OutputString(" is a list");
  return Q;
}
char* ErrorListButVar(char* Q)
{
  ErrorMake();
  OutputString("Expected a list but ");
  OutputString(Q);
  OutputString(" is a variable");
  return Q;
}
char* ErrorVarTypeMismatch(char* Q,int S)
{
  ErrorMake();
  OutputString("Type mismatch, ");
  OutputString(Q);
  OutputString(" was used as a ");
  OutputString(6 < S ? "var" : "list");
  return Q;
}
void ErrorUnEOL()
{
  ErrorMake();
  OutputString("Unexpected end of line");
}
void ErrorUnclosed(char Q,char S)
{
  ErrorMake();
  OutputString("Unclosed ");
  OutputChar(Q);
  OutputString(", expected ");
  OutputChar(S);
  OutputString(" but got ");
  ErrorEOL();
}
void ErrorBadEscape()
{
  ErrorMake();
  OutputString("Unexpected char escape \\");
  ErrorEOL();
}
char* ErrorStringExpect()
{
  ErrorMake();
  OutputString("A string is expected but got ");
  ErrorEOL();
  return 0;
}
void ErrorStringUnclose()
{
  ErrorMake();
  OutputString("String is not closed");
}
void ErrorProcNested()
{
  ErrorMake();
  OutputString("Procedures should not be nested");
}
void ErrorProcUsed(char* Q)
{
  ErrorMake();
  OutputString("Procedure re-defined ");
  OutputString(Q);
}
void ErrorDupParam(char* Q)
{
  ErrorMake();
  OutputString("Duplicate parameter name ");
  OutputString(Q);
}
void ErrorEndNothing()
{
  ErrorMake();
  OutputString("Nothing to end");
}
void ErrorEndUnclose()
{
  ErrorMake();
  OutputString("Unclosed block (ifeq / ifneq / ueq / proc)");
}
void ErrorNoProc(char* Q)
{
  ErrorMake();
  OutputString("Undefined procedure ");
  OutputString(Q);
}
void ErrorProcLength(char* Q,int W,int E)
{
  ErrorMake();
  OutputString("Procedure ");
  OutputString(Q);
  OutputString(" expects ");
  OutputInt(W);
  OutputString(" argument(s) but got ");
  OutputInt(E);
}
void ErrorRecursive(char* Q)
{
  ErrorMake();
  OutputString("Recursive call ");
  OutputString(Q);
}
void ErrorArgTypeMismatch(int H,char* W,char* A,char* Q)
{
  ErrorMake();
  OutputString("Type mismatch. A ");
  OutputString(6 < H ? "var" : "list");
  OutputString(" is expected for parameter ");
  OutputString(W);
  OutputString(" in `");
  OutputString(A);
  OutputString("`, but argument ");
  OutputString(Q);
  OutputString(" is a ");
  OutputString(6 < H ? "list" : "var");
}

void Walk(int Q(char)){for (;Q(Taste());) ++I;}
int TestSpace(char Q){return (8 < Q && Q < 14) || 32 == Q;}
int TestIdentifierPrefix(char Q){return 36 == Q || 95 == Q || (64 < Q && Q < 91) || (96 < Q && Q < 123);}
int TestIdentifierSuffix(char Q){return 36 == Q || 95 == Q || (47 < Q && Q < 58) || (64 < Q && Q < 91) || (96 < Q && Q < 123);}
int TestNumber(char Q){return 47 < Q && Q < 58;}
void Discard(){I = IE;}
void White()
{
  Walk(TestSpace);
  if (('/' == Taste() && '/' == I[1]) || ('-' == Taste() && '-' == I[1]) || '#' == Taste()) Discard();
}
char* Word()
{
  const char* S = I;
  char *R,*U;
  if (!Taste()) return 0;
  if (!TestIdentifierPrefix(Taste())) return ErrorNameExpected();
  ++I;
  Walk(TestIdentifierSuffix);
  R = U = malloc(sizeof(char) * (1 + I - S));
  for (;S < I;) *U++ = CaseSensetive(*S++);
  *U = 0;
  White();
  return R;
}
char* MakeName(Int H)
{
  char* R = Word();
  int T;
  if (!R) return ErrorNameExpected();
  if (ProcVar && ~(T = IndexOf(ProcVar,R)))
    if (ProcVarType->D[T])
    {
      if (H != ProcVarType->D[T]) return ErrorVarTypeMismatch(R,H);
    }
    else ProcVarType->D[T] = H;
  else
  {
    if (!MapHas(Var,R)) return ErrorVarUndefined(R);
    if ((6 < H) != (((VarType)MapLast)->L < 0)) return (6 < H ? ErrorVarButList : ErrorListButVar)(R);
  }
  return R;
}
char* VarName(){return MakeName(9);}
char* ListName(){return MakeName(5);}
int RawNumber()
{
  int R = 0,M = '-' == Taste() ? -1 : 1;
  const char* S;
  if (M < 0) ++I;
  S = I;
  for (;TestNumber(Taste());++I) R = 10 * R + Taste() - 48;
  if (I == S) ErrorNumberExpected();
  else White();
  return R * M;
}
int Number(){return 255 & RawNumber();}
char Char()
{
  char R = Taste();
  ++I;
  if ('\\' == R)
  {
    R = Taste();
    R = '\\' == R || '"' == R || '\'' == R ? R : 'n' == R ? '\n' : 'r' == R ? '\r' : 't' == R ? '\t' : 0;
    if (!R) ErrorBadEscape();
    ++I;
  }
  return R;
}
int NumberOrChar()
{
  int R;
  if ('\'' == Taste())
  {
    ++I;
    R = Char();
    if ('\'' == Taste()) ++I,White();
    else ErrorUnclosed('\'','\'');
  }
  else R = Number();
  return R;
}
Op VarNameOrNumber()
{
  OpT = malloc(sizeof(struct Op));
  OpT->C = 0;
  if ((OpT->H = '-' == Taste() || '\'' == Taste() || TestNumber(Taste()))) OpT->N = NumberOrChar();
  else OpT->C = VarName();
  return OpT;
}
char* String()
{
  char* R = 0;
  if ('"' != Taste()) return ErrorStringExpect();
  for (++I;Taste() && '"' != Taste();) OutputChar(Char());
  if ('"' == Taste())
  {
    ++I;
    White();
    O[OP] = 0;
    strcpy(R = malloc(sizeof(char) * (1 + OP)),O);
    OP = 0;
  }
  else ErrorStringUnclose();
  return R;
}
Op VarNameOrString()
{
  OpT = malloc(sizeof(struct Op));
  OpT->C = (OpT->H = '"' == Taste()) ? String() : VarName();
  return OpT;
}

void ArgID(int Q){Arg->O = Q;}
void ArgMake(int Q,...)
{
  int V;
  va_list S;
  va_start(S,Q);
  Arg = ArrayMake();
  for (;0 <= (V = va_arg(S,int)) && !Error;)
    if (V < 6)
    {
      OpT = malloc(sizeof(struct Op));
      OpT->H = 0;
      OpT->C = V < 3 ? VarName() : ListName();
      ArrayPush(Arg,(Int)OpT);
    }
    else ArrayPush(Arg,(Int)VarNameOrNumber());
  va_end(S);
  ArgID(Q);
}
void ASTFree(Array Q)
{
  for (int F = Q->P,G;F;) for (G = (Arg = (Array)Q->D[--F])->P;G;)
  {
    OpT = (Op)Arg->D[--G];
    if (OpT->C) free(OpT->C);
  }
  ArrayFree(Q);
}
void VarFree(Int Q){free((VarType)Q);}
void ProcFree(Int Q)
{
  ProcT = (ProcType)Q;
  ASTFree(ProcT->AST);
  for (int F = ProcT->Var->P;F;) free((char*)ProcT->Var->D[--F]);
  ArrayFree(ProcT->Var);
  ArrayFree(ProcT->VarType);
}

void OpGotoCell(int Q)
{
  if (Q < StackAt) OutputCharN('<',StackAt - Q);
  else OutputCharN('>',Q - StackAt);
  StackAt = Q;
}
void OpAdd(int Q)
{
  Q = 255 & Q;
  if (128 < Q) OutputCharN('-',256 - Q);
  else OutputCharN('+',Q);
}
int OpSolvePreserve(int Q)
{
  if (PreserveMax < Q) PreserveMax = Q;
  return Preserve - 1 - Q;
}
void OpFly(int Q){StackAt = OpSolvePreserve(Q);}
void OpGotoPreserve(int Q){OpGotoCell(OpSolvePreserve(Q));}
int OpGetPreserve(int Q){return Stack[OpSolvePreserve(Q)];}
void OpSetPreserve(int Q,int S){Stack[OpSolvePreserve(Q)] = S;}
void OpModifyPreserve(int Q,int S)
{
  OpGotoPreserve(Q);
  OpAdd(S - OpGetPreserve(Q));
  OpSetPreserve(Q,S);
}
void OpClearPreserve(int Q,int J)
{
  if (J || OpGetPreserve(Q))
  {
    OpGotoPreserve(Q);
    OutputString("[-]");
    OpSetPreserve(Q,0);
  }
}
void OpMsgList(const char* Q){for (;*Q;OutputChar('.')) OpModifyPreserve(0,*Q++);}

struct Op OpStack[8];
int OpStackAt = 0;
Op OpN(int Q)
{
  ++OpStackAt;
  OpStack[OpStackAt = 7 & OpStackAt].H = 9;
  OpStack[OpStackAt].N = Q;
  return OpStack + OpStackAt;
}
Op OpR(int Q){return (Op)Arg->D[Q];}
char* OpSolveVar(char* Q){return CallArg && MapHas(CallArg,Q) ? (char*)MapLast : Q;}
void OpPickVar(char* Q)
{
  MapHas(Var,OpSolveVar(Q));
  VarT = (VarType)MapLast;
}
void OpGoto(Op Q,int S)
{
  if (Q->H)
    if (Q->N < 0) OpGotoCell(-Q->N);
    else OpGotoPreserve(Q->N);
  else
  {
    OpPickVar(Q->C);
    OpGotoCell(VarT->L < 0 ? VarT->P : S + VarT->P);
  }
}
void OpClear(Op Q,int J)
{
  if (Q->H) OpClearPreserve(Q->N,J);
  else
  {
    OpGoto(Q,0);
    OutputString("[-]");
  }
}
void OpBegin(Op Q,int S)
{
  OpGoto(Q,S);
  OutputString("[-");
}
void OpEnd(Op Q,int S)
{
  OpGoto(Q,S);
  OutputString("]");
}
void OpMove(Op Q,Op S,int I)
{
  OpBegin(Q,I);
  OpGoto(S,0);
  OutputChar('+');
  OpEnd(Q,I);
}
void OpMoveTwo(Op Q,Op S,Op W,int I)
{
  OpBegin(Q,I);
  OpGoto(S,0);
  OutputChar('+');
  OpGoto(W,0);
  OutputChar('+');
  OpEnd(Q,I);
}
void OpMoveThree(Op Q,Op S,Op W,Op A,int I)
{
  OpBegin(Q,I);
  OpGoto(S,0);
  OutputChar('+');
  OpGoto(W,0);
  OutputChar('+');
  OpGoto(A,0);
  OutputChar('+');
  OpEnd(Q,I);
}
void OpMoveReverse(Op Q,Op S,int I)
{
  OpBegin(Q,I);
  OpGoto(S,0);
  OutputChar('-');
  OpEnd(Q,I);
}
void OpCopy(Op Q,Op S,Op T,int J)
{
  if (J) OpClear(T,0);
  OpMoveTwo(Q,S,T,0);
  OpMove(T,Q,0);
}
void OpCopyTwo(Op Q,Op S,Op W,Op T,int J)
{
  if (J) OpClear(T,0);
  OpMoveThree(Q,S,W,T,0);
  OpMove(T,Q,0);
}
void OpPrepare(Op Q,Op S,int T)
{
  OpClear(S,0);
  if (Q->H)
  {
    OpGoto(S,0);
    OpAdd(Q->N);
  }
  else OpCopy(Q,S,OpN(T),9);
}
void OpPrepareTwo(Op Q,Op S,Op W,int T)
{
  if (Q->H)
  {
    OpGoto(OpN(T),0);
    OpAdd(Q->N);
    OpMoveTwo(OpN(T),S,W,0);
  }
  else OpCopyTwo(Q,S,W,OpN(T),9);
}
void OpPrepare01(int W,int A,int T)
{
  OpPrepare(OpR(0),OpN(W),T);
  OpPrepare(OpR(1),OpN(A),T);
}
void OpSet(Op Q,Op S)
{
  OpClear(Q,0);
  OpMove(S,Q,0);
}
void OpDivModQS(int D,int M,Op Q,Op S)
{
  OpPrepare(Q,OpN(5),0);
  OpPrepare(S,OpN(4),0);
  OpCopy(OpN(4),OpN(8),OpN(7),9);
  OpGoto(OpN(7),0);
  OutputString("+<-");
  OutputString("[>>>[->-[>+>>]>[+[-<+>]>+>>]<<<<<]<<-]>");
  OutputString("[->>[->>>+<<<]<]");
  OpFly(6);
  OpClear(OpN(8),9);
  OpClear(OpN(4),9);
  if (D) OpSet(OpR(D),OpN(2));
  else OpClear(OpN(2),9);
  if (M) OpSet(OpR(M),OpN(3));
  else OpClear(OpN(3),9);
}
void OpDivMod(int D,int M){OpDivModQS(D,M,OpR(0),OpR(1));}
void OpIfWhile(int Not)
{
  if (OpR(1)->H)
  {
    OpClear(OpN(0),0);
    OpCopy(OpR(0),OpN(0),OpN(1),9);
    OpGoto(OpN(0),0);
    OpAdd(-OpR(1)->N);
  }
  else
  {
    OpPrepare01(0,1,2);
    OpMoveReverse(OpN(1),OpN(0),0);
  }
  if (Not)
  {
    OpGoto(OpN(1),0);
    OutputString("+>[[-]<-]<[>+<-<]");
    OpFly(2);
  }
  OpGoto(OpN(0),0);
}

void Generate(Array AST)
{
  int X,T0,T1,F;
  Map _CallArg = CallArg;
  for (F = 0;F < AST->P;++F) switch ((Arg = (Array)AST->D[F])->O)
  {
    case 8000 : // set
      OpGoto(OpR(0),0);
      OutputString("[-]");
      if (OpR(1)->H) OpAdd(OpR(1)->N);
      else OpCopy(OpR(1),OpR(0),OpN(0),9);
      break;
    case 8010 : // inc
      if (OpR(1)->H)
      {
        OpGoto(OpR(0),0);
        OpAdd(OpR(1)->N);
      }
      else
      {
        OpCopy(OpR(0),OpN(0),OpN(1),9);
        OpMove(OpN(0),OpR(0),0);
      }
      break;
    case 8011 : // dec
      if (OpR(1)->H)
      {
        OpGoto(OpR(0),0);
        OpAdd(-OpR(1)->N);
      }
      else
      {
        OpCopy(OpR(0),OpN(0),OpN(1),9);
        OpMove(OpN(0),OpR(0),0);
      }
      break;
    case 8012 : // add
      OpPrepare01(0,1,2);
      OpMove(OpN(1),OpN(0),0);
      OpSet(OpR(2),OpN(0));
      break;
    case 8013 : // sub
      OpPrepare01(0,1,2);
      OpMoveReverse(OpN(1),OpN(0),0);
      OpSet(OpR(2),OpN(0));
      break;
    case 8014 : // mul
      OpPrepare01(0,1,2);
      OpBegin(OpN(0),0);
      OpCopy(OpN(1),OpN(2),OpN(3),9);
      OpEnd(OpN(0),0);
      OpClear(OpN(1),9);
      OpSet(OpR(2),OpN(2));
      break;
    case 8015 : // divmod
      OpDivMod(2,3);
      break;
    case 8016 : // div
      OpDivMod(2,0);
      break;
    case 8017 : // mod
      OpDivMod(0,2);
      break;
    case 8020 : // cmp
      X = 4;
      T0 = 3;
      T1 = 2;
      OpPrepareTwo(OpR(0),OpN(T0),OpN(X),0);
      OpPrepareTwo(OpR(1),OpN(T1),OpN(1 + X),0);
      OpMoveReverse(OpN(1 + X),OpN(X),0);

      OpGoto(OpN(1 + X),0);
      OutputString("+>[[-]");
      OpFly(X);

      OpGoto(OpN(T1 - 1),0);
      OutputString("+<[>-]>[");
      OpFly(T1 - 1);
      OpGoto(OpN(X),0);
      OutputChar('+');
      OpGoto(OpN(T0),0);
      OutputString("[-]");
      OpGoto(OpN(T1 - 1),0);
      OutputString("->]<+");
      OpGoto(OpN(T0),0);
      OutputChar('[');
      OpGoto(OpN(T1),0);
      OutputString("-[>-]>[");
      OpFly(T1 - 1);
      OpGoto(OpN(X),0);
      OutputChar('+');
      OpGoto(OpN(T0),0);
      OutputString("[-]+");
      OpGoto(OpN(T1 - 1),0);
      OutputString("->]<+");
      OpGoto(OpN(T0),0);
      OutputString("-]");

      OpGoto(OpN(X),0);
      OutputString("[<-]<[>-<-<]");
      OpFly(2 + X);

      OpGoto(OpN(1 + X),0);
      OutputString("]<[-<]>");

      OpClear(OpN(3),9);
      OpClear(OpN(2),9);
      OpClear(OpN(1),9);

      OpSet(OpR(2),OpN(X));
      break;
    case 8030 : // a2b
      OpCopy(OpR(0),OpN(2),OpN(0),9);
      OpGoto(OpN(2),0);
      OpAdd(-48);
      OpBegin(OpN(2),0);
      OpGoto(OpN(1),0);
      OpAdd(10);
      OpEnd(OpN(2),0);

      OpCopy(OpR(1),OpN(1),OpN(0),9);
      OpGoto(OpN(1),0);
      OpAdd(-48);

      OpBegin(OpN(1),0);
      OpGoto(OpN(0),0);
      OpAdd(10);
      OpEnd(OpN(1),0);

      OpCopy(OpR(2),OpN(0),OpN(1),9);
      OpGoto(OpN(0),0);
      OpAdd(-48);

      OpSet(OpR(3),OpN(0));
      break;
    case 8031 : // b2a
      OpDivModQS(2,3,OpR(0),OpN(10));
      OpDivModQS(1,2,OpR(2),OpN(10));
      OpGoto(OpR(1),0);
      OpAdd(48);
      OpGoto(OpR(2),0);
      OpAdd(48);
      OpGoto(OpR(3),0);
      OpAdd(48);
      break;
    case 8040 : // lset
      OpPickVar(OpR(0)->C);
      if (OpR(1)->H)
      {
        OpGoto(OpR(0),0);
        OpAdd(OpR(1)->N);
        OutputString("[->+>+<<]");
      }
      else OpCopyTwo(OpR(1),OpN(-1 - VarT->P),OpN(-2 - VarT->P),OpR(0),0);
      if (OpR(2)->H)
      {
        OpGoto(OpR(0),3);
        OpAdd(OpR(2)->N);
      }
      else OpCopy(OpR(2),OpN(-3 - VarT->P),OpR(0),0);
      OpGoto(OpR(0),0);
      OutputString(">[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]");
      OutputString(">>>[-]<[->+<]<");
      OutputString("[[-<+>]<<<[->>>>+<<<<]>>-]<<");
      break;
    case 8041 : // lget
      OpPickVar(OpR(0)->C);
      if (OpR(1)->H)
      {
        OpGoto(OpR(0),0);
        OpAdd(OpR(1)->N);
        OutputString("[->+>+<<]");
      }
      else OpCopyTwo(OpR(1),OpN(-1 - VarT->P),OpN(-2 - VarT->P),OpR(0),0);
      OpGoto(OpR(0),0);
      OutputString(">[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]");
      OutputString(">>>[-<+<<+>>>]<<<[->>>+<<<]>");
      OutputString("[[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<");
      OpClear(OpR(2),0);
      OpMove(OpR(0),OpR(2),3);
      break;
    case 8050 : // ifeq
    case 8052 : // weq
      OpIfWhile(9);
      OutputChar('[');
      OpClear(OpN(0),9);
      break;
    case 8051 : // ifneq
      OpIfWhile(0);
      OutputChar('[');
      OpClear(OpN(0),9);
      break;
    case 8053 : // wneq
      if (OpR(1)->N)
      {
        OpIfWhile(0);
        OutputChar('[');
        OpClear(OpN(0),9);
      }
      else
      {
        OpGoto(OpR(0),0);
        OutputChar('[');
      }
      break;
    case 8054 : // end
      Arg = (Array)AST->D[OpR(0)->N];
      if (8052 == Arg->O)
      {
        OpIfWhile(9);
        OpGoto(OpN(0),0);
      }
      else if (8053 == Arg->O)
      {
        if (OpR(1)->N)
        {
          OpIfWhile(0);
          OpGoto(OpN(0),0);
        }
        else OpGoto(OpR(0),0);
      }
      else
      {
        OpClear(OpN(0),0);
        OpGoto(OpN(0),0);
      }
      OutputChar(']');
      break;
    case 8055 : // call
      OpT = OpR(0);
      if (!MapHas(Proc,OpT->C))
      {
        ErrorNoProc(OpT->C);
        break;
      }
      ProcT = (ProcType)MapLast;
      ProcVar = ProcT->Var;
      ProcVarType = ProcT->VarType;
      if (Arg->P - ProcVar->P - 1)
      {
        ErrorProcLength(OpT->C,ProcVar->P,Arg->P - 1);
        break;
      }
      if (~IndexOf(CallStack,OpT->C))
      {
        ErrorRecursive(OpT->C);
        break;
      }
      ArrayPush(CallStack,(Int)OpT->C);
      CallArg = MapMake();
      for (X = ProcVar->P;X && !Error;)
      {
        char* T = OpR(X--)->C;
        if (_CallArg && MapHas(_CallArg,T)) T = (char*)MapLast;
        MapSet(CallArg,(char*)ProcVar->D[X],(Int)T);
        if (ProcVarType->D[X])
        {
          MapHas(Var,T);
          if (ProcVarType->D[X] - (((VarType)MapLast)->L < 0 ? 9 : 5))
            ErrorArgTypeMismatch(ProcVarType->D[X],(char*)ProcVar->D[X],OpR(0)->C,OpR(1 + X)->C);
        }
      }
      if (!Error) Generate(ProcT->AST);
      MapFree(CallArg,0);
      CallArg = _CallArg;
      --CallStack->P;

      break;
    case 8060 : // read
      OpGoto(OpR(0),0);
      OutputChar(',');
      break;
    case 8061 : // msg
      for (X = 0;X < Arg->P;++X)
        if (OpR(X)->H) OpMsgList(OpR(X)->C);
        else
        {
          OpGoto(OpR(X),0);
          OutputChar('.');
        }
      break;
    case 8400 : // debug
      OutputChar('_');
  }
}

int kcuf(char** Output,const char* Code)
{
  char* V;
  int F;
  PreserveMax = -1;
  for (F = Preserve;F;) Stack[--F] = 0;
  StackAt = 0;
  VarAt = Preserve;
  Var = MapMake();
  AST = CurrentAST = ArrayMake();
  ASTStack = ArrayMake();
  Proc = MapMake();
  ProcVar = ProcVarType = 0;
  CallStack = ArrayMake();
  Error = 0;
  OP = 0;
  OO = 32;
  O = malloc(sizeof(char) * OO);
  CallArg = 0;

  for (IE = Code;*IE;)
  {
    for (I = IE;*IE && 10 != *IE;) ++IE;
    White();
    if (Taste())
    {
      V = Word();
      if (Error) goto End;
      Arg = 0;

      if (!strcmp(V,"VAR"))
      {
        if (ProcVar) ErrorDefineInProc();
        else if (!Taste()) ErrorUnEOL();
        else for (;free(V),V = Word();)
        {
          if (MapHas(Var,V))
          {
            ErrorVarRedeclare(V);
            break;
          }
          VarT = malloc(sizeof(struct VarType));
          MapSet(Var,V,(Int)VarT);
          if ('[' == Taste())
          {
            ++I;
            White();
            VarT->P = VarAt;
            VarAt += 4 + (VarT->L = RawNumber());
            if (']' != Taste())
            {
              ErrorUnclosed('[',']');
              break;
            }
            ++I;
            White();
          }
          else
          {
            VarT->P = VarAt++;
            VarT->L = -1;
          }
        }
      }

      else if (!strcmp(V,"SET")) ArgMake(8000,0,9,-1);

      else if (!strcmp(V,"INC")) ArgMake(8010,0,9,-1);
      else if (!strcmp(V,"DEC")) ArgMake(8011,0,9,-1);
      else if (!strcmp(V,"ADD")) ArgMake(8012,9,9,0,-1);
      else if (!strcmp(V,"SUB")) ArgMake(8013,9,9,0,-1);
      else if (!strcmp(V,"MUL")) ArgMake(8014,9,9,0,-1);
      else if (!strcmp(V,"DIVMOD")) ArgMake(8015,9,9,0,0,-1);
      else if (!strcmp(V,"DIV")) ArgMake(8016,9,9,0,-1);
      else if (!strcmp(V,"MOD")) ArgMake(8017,9,9,0,-1);

      else if (!strcmp(V,"CMP")) ArgMake(8020,9,9,0,-1);

      else if (!strcmp(V,"A2B")) ArgMake(8030,9,9,9,0,-1);
      else if (!strcmp(V,"B2A")) ArgMake(8031,9,0,0,0,-1);

      else if (!strcmp(V,"LSET")) ArgMake(8040,5,9,9,-1);
      else if (!strcmp(V,"LGET")) ArgMake(8041,5,9,0,-1);

      else if (!strcmp(V,"IFEQ")) ArgMake(8050,0,9,-1),ArrayPush(ASTStack,CurrentAST->P);
      else if (!strcmp(V,"IFNEQ")) ArgMake(8051,0,9,-1),ArrayPush(ASTStack,CurrentAST->P);
      else if (!strcmp(V,"WEQ")) ArgMake(8052,0,9,-1),ArrayPush(ASTStack,CurrentAST->P);
      else if (!strcmp(V,"WNEQ")) ArgMake(8053,0,9,-1),ArrayPush(ASTStack,CurrentAST->P);
      else if (!strcmp(V,"PROC"))
      {
        if (ProcVar) ErrorProcNested();
        else
        {
          free(V);
          V = Word();
          if (MapHas(Proc,V)) ErrorProcUsed(V);
          else
          {
            ProcT = malloc(sizeof(struct ProcType));
            ProcT->AST = CurrentAST = ArrayMake();
            ProcT->Var = ProcVar = ArrayMake();
            ProcT->VarType = ProcVarType = ArrayMake();
            MapSet(Proc,V,(Int)ProcT);
          }
          free(V);
          for (;!Error && Taste() && (V = Word());)
          {
            if (~IndexOf(ProcVar,V)) ErrorDupParam(V);
            ArrayPush(ProcVar,(Int)V);
            ArrayPush(ProcVarType,0);
          }
          V = 0;
        }
      }
      else if (!strcmp(V,"END"))
      {
        if (ASTStack->P)
        {
          Arg = ArrayMake();
          (OpT = malloc(sizeof(struct Op)))->C = 0;
          OpT->N = ASTStack->D[--ASTStack->P];
          ArrayPush(Arg,(Int)OpT);
          ArgID(8054);
        }
        else if (ProcVar)
        {
          CurrentAST = AST;
          ProcVar = 0;
        }
        else ErrorEndNothing();
      }
      else if (!strcmp(V,"CALL"))
      {
        Arg = ArrayMake();
        for (;Taste() && !Error;ArrayPush(Arg,(Int)OpT))
          (OpT = malloc(sizeof(struct Op)))->C = Word();
        ArgID(8055);
      }

      else if (!strcmp(V,"READ")) ArgMake(8060,0,-1);
      else if (!strcmp(V,"MSG"))
      {
        Arg = ArrayMake();
        for (;Taste() && !Error;) ArrayPush(Arg,(Int)VarNameOrString());
        ArgID(8061);
      }

      else if (!strcmp(V,"REM")) Discard();

      else ErrorCommand(V);
      if (V) free(V);
      if (Arg) ArrayPush(CurrentAST,(Int)Arg);
      if (!Error && Taste()) ErrorCommandEnd();
      if (Error) goto End;
    }
    if (*IE) ++IE;
  }
  if (!ASTStack->P) Generate(AST);
  else if (!Error) ErrorEndUnclose();

  End :
  O[OP] = 0;
  if (1 + PreserveMax < Preserve && !Error)
  {
    *Output = malloc(sizeof(char) * (OP - Preserve + PreserveMax + 2));
    strcpy(*Output,O + Preserve - PreserveMax - 1);
    free(O);
  }
  else *Output = O;
  ArrayFree(CallStack);
  MapFree(Proc,ProcFree);
  ArrayFree(ASTStack);
  ASTFree(AST);
  MapFree(Var,VarFree);
  return Error ? Error : 0;
}

#######################################
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

#ifdef __x86_64__
  typedef long int Int;
#else
  typedef int Int;
#endif

int EnsureLast;
int Ensure(int* Q,int S)
{
  EnsureLast = 0;
  if (*Q <= S) for (EnsureLast = *Q;*Q <= S;) *Q *= 2;
  return EnsureLast;
}
char* Clone(const char* Q)
{
  char* R = malloc(sizeof(char) * (1 + strlen(Q)));
  strcpy(R,Q);
  return R;
}

int OP,OO;
char* O;
void OutputEnsure(int L)
{
  char* T = O;
  if (Ensure(&OO,OP + L))
  {
    O = malloc(sizeof(char) * OO);
    memcpy(O,T,sizeof(char) * EnsureLast);
    free(T);
  }
}
void OutputChar(char Q)
{
  OutputEnsure(1);
  O[OP++] = Q;
}
void OutputCharN(char Q,int S)
{
  OutputEnsure(S);
  for (;S--;) O[OP++] = Q;
}
void OutputInt(int Q)
{
  int T = Q,L = 0;
  for (;++L,T /= 10;);
  OutputEnsure(L + (Q < 0));
  if (Q < 0) O[OP++] = '-';
  Q = abs(Q);
  for (L = OP += L;O[--L] = 48 + Q % 10,Q /= 10;);
}
void OutputString(char* Q)
{
  OutputEnsure(strlen(Q));
  for (;*Q;) O[OP++] = *Q++;
}

typedef struct Array{int P,O;Int* D;}* Array;
Array ArrayMake()
{
  Array R = malloc(sizeof(struct Array));
  R->P = 0;
  R->O = 32;
  R->D = malloc(sizeof(Int) * R->O);
  memset(R->D,0,sizeof(Int) * R->O);
  return R;
}
void ArrayFree(Array Q)
{
  free(Q->D);
  free(Q);
}
void ArrayEnsure(Array Q)
{
  Int* T = Q->D;
  if (Ensure(&Q->O,Q->P))
  {
    Q->D = malloc(sizeof(Int) * Q->O);
    memcpy(Q->D,T,sizeof(Int) * EnsureLast);
    free(T);
  }
}
void ArrayPush(Array Q,Int S)
{
  ArrayEnsure(Q);
  Q->D[Q->P++] = S;
}

#define MapSize 64
typedef struct MapNode
{
  int H;
  char* K;
  Int V;
  struct MapNode* N;
}* MapNode;
typedef struct Map{MapNode D[MapSize];}* Map;
Map MapMake()
{
  Map R = malloc(sizeof(struct Map));
  memset(R->D,0,sizeof(R->D));
  return R;
}
void MapFree(Map Q,void S(Int))
{
  for (int F = MapSize;F;) for (MapNode C = Q->D[--F],T;(T = C);)
  {
    C = C->N;
    free(T->K);
    if (S) S(T->V);
    free(T);
  }
  free(Q);
}
int MapHash(const char* K)
{
  int R = -2128831035;
  for (;*K;) R = 16777619 * R | *K++;
  return R;
}
void MapSet(Map Q,const char* K,Int V)
{
  int H = MapHash(K);
  MapNode L = 0,C = Q->D[(MapSize - 1) & H];
  for (;C;L = C,C = C->N) if (H == C->H && !strcmp(K,C->K))
  {
    C->V = V;
    return;
  }
  C = malloc(sizeof(struct MapNode));
  C->H = H;
  C->K = Clone(K);
  C->V = V;
  C->N = 0;
  if (L) L->N = C;
  else Q->D[(MapSize - 1) & H] = C;
}
Int MapLast;
int MapHas(Map Q,const char* K)
{
  int H = MapHash(K);
  MapNode C = Q->D[(MapSize - 1) & H];
  for (;C;C = C->N) if (H == C->H && !strcmp(K,C->K))
  {
    MapLast = C->V;
    return 9;
  }
  return 0;
}

typedef struct VarType{int P,L;}* VarType;
typedef struct ProcType{Array AST,Var,VarType;}* ProcType;
typedef struct Op{int H;Int N;char* C;}* Op;

const char *I,*IE;
int Preserve = 9,PreserveMax,Stack[9],StackAt,VarAt,Error,F;
Map Var,Proc;
Array AST,ASTStack,CurrentAST,ProcVar,ProcVarType;

VarType VarT;
ProcType ProcT;
Op OpT;
Array Arg;
Map CallArg;
Array CallStack;

char CaseSensetive(char Q){return 96 < Q && Q < 123 ? Q - 32 : Q;}
int IndexOf(Array Q,const char* S)
{
  for (int F = Q->P;F;) if (!strcmp(S,(const char*)Q->D[--F])) return F;
  return -1;
}

char Taste(){return I < IE ? *I : 0;}
void ErrorMake()
{
  Error = 9;
  OP = 0;
}
void ErrorEOL()
{
  if (Taste()) OutputChar(Taste());
  else OutputString("EOL");
}
void ErrorNumberExpected()
{
  ErrorMake();
  OutputString("A number is expected but got ");
  ErrorEOL();
}
char* ErrorNameExpected()
{
  ErrorMake();
  OutputString("A variable name / command is expected but got ");
  ErrorEOL();
  return 0;
}
void ErrorCommand(char* Q)
{
  ErrorMake();
  OutputString("Unexpected command ");
  OutputString(Q);
}
void ErrorCommandEnd()
{
  ErrorMake();
  OutputString("Expected end of line but got ");
  ErrorEOL();
}
void ErrorDefineInProc()
{
  ErrorMake();
  OutputString("Cannot define variables in procedures");
}
char* ErrorVarUndefined(char* Q)
{
  ErrorMake();
  OutputString("Undefined variable ");
  OutputString(Q);
  return Q;
}
void ErrorVarRedeclare(char* Q)
{
  ErrorMake();
  OutputString("Re-defined variable ");
  OutputString(Q);
}
char* ErrorVarButList(char* Q)
{
  ErrorMake();
  OutputString("Expected a variable but ");
  OutputString(Q);
  OutputString(" is a list");
  return Q;
}
char* ErrorListButVar(char* Q)
{
  ErrorMake();
  OutputString("Expected a list but ");
  OutputString(Q);
  OutputString(" is a variable");
  return Q;
}
char* ErrorVarTypeMismatch(char* Q,int S)
{
  ErrorMake();
  OutputString("Type mismatch, ");
  OutputString(Q);
  OutputString(" was used as a ");
  OutputString(6 < S ? "var" : "list");
  return Q;
}
void ErrorUnEOL()
{
  ErrorMake();
  OutputString("Unexpected end of line");
}
void ErrorUnclosed(char Q,char S)
{
  ErrorMake();
  OutputString("Unclosed ");
  OutputChar(Q);
  OutputString(", expected ");
  OutputChar(S);
  OutputString(" but got ");
  ErrorEOL();
}
void ErrorBadEscape()
{
  ErrorMake();
  OutputString("Unexpected char escape \\");
  ErrorEOL();
}
char* ErrorStringExpect()
{
  ErrorMake();
  OutputString("A string is expected but got ");
  ErrorEOL();
  return 0;
}
void ErrorStringUnclose()
{
  ErrorMake();
  OutputString("String is not closed");
}
void ErrorProcNested()
{
  ErrorMake();
  OutputString("Procedures should not be nested");
}
void ErrorProcUsed(char* Q)
{
  ErrorMake();
  OutputString("Procedure re-defined ");
  OutputString(Q);
}
void ErrorDupParam(char* Q)
{
  ErrorMake();
  OutputString("Duplicate parameter name ");
  OutputString(Q);
}
void ErrorEndNothing()
{
  ErrorMake();
  OutputString("Nothing to end");
}
void ErrorEndUnclose()
{
  ErrorMake();
  OutputString("Unclosed block (ifeq / ifneq / ueq / proc)");
}
void ErrorNoProc(char* Q)
{
  ErrorMake();
  OutputString("Undefined procedure ");
  OutputString(Q);
}
void ErrorProcLength(char* Q,int W,int E)
{
  ErrorMake();
  OutputString("Procedure ");
  OutputString(Q);
  OutputString(" expects ");
  OutputInt(W);
  OutputString(" argument(s) but got ");
  OutputInt(E);
}
void ErrorRecursive(char* Q)
{
  ErrorMake();
  OutputString("Recursive call ");
  OutputString(Q);
}
void ErrorArgTypeMismatch(int H,char* W,char* A,char* Q)
{
  ErrorMake();
  OutputString("Type mismatch. A ");
  OutputString(6 < H ? "var" : "list");
  OutputString(" is expected for parameter ");
  OutputString(W);
  OutputString(" in `");
  OutputString(A);
  OutputString("`, but argument ");
  OutputString(Q);
  OutputString(" is a ");
  OutputString(6 < H ? "list" : "var");
}

void Walk(int Q(char)){for (;Q(Taste());) ++I;}
int TestSpace(char Q){return (8 < Q && Q < 14) || 32 == Q;}
int TestIdentifierPrefix(char Q){return 36 == Q || 95 == Q || (64 < Q && Q < 91) || (96 < Q && Q < 123);}
int TestIdentifierSuffix(char Q){return 36 == Q || 95 == Q || (47 < Q && Q < 58) || (64 < Q && Q < 91) || (96 < Q && Q < 123);}
int TestNumber(char Q){return 47 < Q && Q < 58;}
void Discard(){I = IE;}
void White()
{
  Walk(TestSpace);
  if (('/' == Taste() && '/' == I[1]) || ('-' == Taste() && '-' == I[1]) || '#' == Taste()) Discard();
}
char* Word()
{
  const char* S = I;
  char *R,*U;
  if (!Taste()) return 0;
  if (!TestIdentifierPrefix(Taste())) return ErrorNameExpected();
  ++I;
  Walk(TestIdentifierSuffix);
  R = U = malloc(sizeof(char) * (1 + I - S));
  for (;S < I;) *U++ = CaseSensetive(*S++);
  *U = 0;
  White();
  return R;
}
char* MakeName(Int H)
{
  char* R = Word();
  int T;
  if (!R) return ErrorNameExpected();
  if (ProcVar && ~(T = IndexOf(ProcVar,R)))
    if (ProcVarType->D[T])
    {
      if (H != ProcVarType->D[T]) return ErrorVarTypeMismatch(R,H);
    }
    else ProcVarType->D[T] = H;
  else
  {
    if (!MapHas(Var,R)) return ErrorVarUndefined(R);
    if ((6 < H) != (((VarType)MapLast)->L < 0)) return (6 < H ? ErrorVarButList : ErrorListButVar)(R);
  }
  return R;
}
char* VarName(){return MakeName(9);}
char* ListName(){return MakeName(5);}
int RawNumber()
{
  int R = 0,M = '-' == Taste() ? -1 : 1;
  const char* S;
  if (M < 0) ++I;
  S = I;
  for (;TestNumber(Taste());++I) R = 10 * R + Taste() - 48;
  if (I == S) ErrorNumberExpected();
  else White();
  return R * M;
}
int Number(){return 255 & RawNumber();}
char Char()
{
  char R = Taste();
  ++I;
  if ('\\' == R)
  {
    R = Taste();
    R = '\\' == R || '"' == R || '\'' == R ? R : 'n' == R ? '\n' : 'r' == R ? '\r' : 't' == R ? '\t' : 0;
    if (!R) ErrorBadEscape();
    ++I;
  }
  return R;
}
int NumberOrChar()
{
  int R;
  if ('\'' == Taste())
  {
    ++I;
    R = Char();
    if ('\'' == Taste()) ++I,White();
    else ErrorUnclosed('\'','\'');
  }
  else R = Number();
  return R;
}
Op VarNameOrNumber()
{
  OpT = malloc(sizeof(struct Op));
  OpT->C = 0;
  if ((OpT->H = '-' == Taste() || '\'' == Taste() || TestNumber(Taste()))) OpT->N = NumberOrChar();
  else OpT->C = VarName();
  return OpT;
}
char* String()
{
  char* R = 0;
  if ('"' != Taste()) return ErrorStringExpect();
  for (++I;Taste() && '"' != Taste();) OutputChar(Char());
  if ('"' == Taste())
  {
    ++I;
    White();
    O[OP] = 0;
    strcpy(R = malloc(sizeof(char) * (1 + OP)),O);
    OP = 0;
  }
  else ErrorStringUnclose();
  return R;
}
Op VarNameOrString()
{
  OpT = malloc(sizeof(struct Op));
  OpT->C = (OpT->H = '"' == Taste()) ? String() : VarName();
  return OpT;
}

void ArgID(int Q){Arg->O = Q;}
void ArgMake(int Q,...)
{
  int V;
  va_list S;
  va_start(S,Q);
  Arg = ArrayMake();
  for (;0 <= (V = va_arg(S,int)) && !Error;)
    if (V < 6)
    {
      OpT = malloc(sizeof(struct Op));
      OpT->H = 0;
      OpT->C = V < 3 ? VarName() : ListName();
      ArrayPush(Arg,(Int)OpT);
    }
    else ArrayPush(Arg,(Int)VarNameOrNumber());
  va_end(S);
  ArgID(Q);
}
void ASTFree(Array Q)
{
  for (int F = Q->P,G;F;) for (G = (Arg = (Array)Q->D[--F])->P;G;)
  {
    OpT = (Op)Arg->D[--G];
    if (OpT->C) free(OpT->C);
  }
  ArrayFree(Q);
}
void VarFree(Int Q){free((VarType)Q);}
void ProcFree(Int Q)
{
  ProcT = (ProcType)Q;
  ASTFree(ProcT->AST);
  for (int F = ProcT->Var->P;F;) free((char*)ProcT->Var->D[--F]);
  ArrayFree(ProcT->Var);
  ArrayFree(ProcT->VarType);
}

void OpGotoCell(int Q)
{
  if (Q < StackAt) OutputCharN('<',StackAt - Q);
  else OutputCharN('>',Q - StackAt);
  StackAt = Q;
}
void OpAdd(int Q)
{
  Q = 255 & Q;
  if (128 < Q) OutputCharN('-',256 - Q);
  else OutputCharN('+',Q);
}
int OpSolvePreserve(int Q)
{
  if (PreserveMax < Q) PreserveMax = Q;
  return Preserve - 1 - Q;
}
void OpFly(int Q){StackAt = OpSolvePreserve(Q);}
void OpGotoPreserve(int Q){OpGotoCell(OpSolvePreserve(Q));}
int OpGetPreserve(int Q){return Stack[OpSolvePreserve(Q)];}
void OpSetPreserve(int Q,int S){Stack[OpSolvePreserve(Q)] = S;}
void OpModifyPreserve(int Q,int S)
{
  OpGotoPreserve(Q);
  OpAdd(S - OpGetPreserve(Q));
  OpSetPreserve(Q,S);
}
void OpClearPreserve(int Q,int J)
{
  if (J || OpGetPreserve(Q))
  {
    OpGotoPreserve(Q);
    OutputString("[-]");
    OpSetPreserve(Q,0);
  }
}
void OpMsgList(const char* Q){for (;*Q;OutputChar('.')) OpModifyPreserve(0,*Q++);}

struct Op OpStack[8];
int OpStackAt = 0;
Op OpN(int Q)
{
  ++OpStackAt;
  OpStack[OpStackAt = 7 & OpStackAt].H = 9;
  OpStack[OpStackAt].N = Q;
  return OpStack + OpStackAt;
}
Op OpR(int Q){return (Op)Arg->D[Q];}
char* OpSolveVar(char* Q){return CallArg && MapHas(CallArg,Q) ? (char*)MapLast : Q;}
void OpPickVar(char* Q)
{
  MapHas(Var,OpSolveVar(Q));
  VarT = (VarType)MapLast;
}
void OpGoto(Op Q,int S)
{
  if (Q->H)
    if (Q->N < 0) OpGotoCell(-Q->N);
    else OpGotoPreserve(Q->N);
  else
  {
    OpPickVar(Q->C);
    OpGotoCell(VarT->L < 0 ? VarT->P : S + VarT->P);
  }
}
void OpClear(Op Q,int J)
{
  if (Q->H) OpClearPreserve(Q->N,J);
  else
  {
    OpGoto(Q,0);
    OutputString("[-]");
  }
}
void OpBegin(Op Q,int S)
{
  OpGoto(Q,S);
  OutputString("[-");
}
void OpEnd(Op Q,int S)
{
  OpGoto(Q,S);
  OutputString("]");
}
void OpMove(Op Q,Op S,int I)
{
  OpBegin(Q,I);
  OpGoto(S,0);
  OutputChar('+');
  OpEnd(Q,I);
}
void OpMoveTwo(Op Q,Op S,Op W,int I)
{
  OpBegin(Q,I);
  OpGoto(S,0);
  OutputChar('+');
  OpGoto(W,0);
  OutputChar('+');
  OpEnd(Q,I);
}
void OpMoveThree(Op Q,Op S,Op W,Op A,int I)
{
  OpBegin(Q,I);
  OpGoto(S,0);
  OutputChar('+');
  OpGoto(W,0);
  OutputChar('+');
  OpGoto(A,0);
  OutputChar('+');
  OpEnd(Q,I);
}
void OpMoveReverse(Op Q,Op S,int I)
{
  OpBegin(Q,I);
  OpGoto(S,0);
  OutputChar('-');
  OpEnd(Q,I);
}
void OpCopy(Op Q,Op S,Op T,int J)
{
  if (J) OpClear(T,0);
  OpMoveTwo(Q,S,T,0);
  OpMove(T,Q,0);
}
void OpCopyTwo(Op Q,Op S,Op W,Op T,int J)
{
  if (J) OpClear(T,0);
  OpMoveThree(Q,S,W,T,0);
  OpMove(T,Q,0);
}
void OpPrepare(Op Q,Op S,int T)
{
  OpClear(S,0);
  if (Q->H)
  {
    OpGoto(S,0);
    OpAdd(Q->N);
  }
  else OpCopy(Q,S,OpN(T),9);
}
void OpPrepareTwo(Op Q,Op S,Op W,int T)
{
  if (Q->H)
  {
    OpGoto(OpN(T),0);
    OpAdd(Q->N);
    OpMoveTwo(OpN(T),S,W,0);
  }
  else OpCopyTwo(Q,S,W,OpN(T),9);
}
void OpPrepare01(int W,int A,int T)
{
  OpPrepare(OpR(0),OpN(W),T);
  OpPrepare(OpR(1),OpN(A),T);
}
void OpSet(Op Q,Op S)
{
  OpClear(Q,0);
  OpMove(S,Q,0);
}
void OpDivModQS(int D,int M,Op Q,Op S)
{
  OpPrepare(Q,OpN(5),0);
  OpPrepare(S,OpN(4),0);
  OpCopy(OpN(4),OpN(8),OpN(7),9);
  OpGoto(OpN(7),0);
  OutputString("+<-");
  OutputString("[>>>[->-[>+>>]>[+[-<+>]>+>>]<<<<<]<<-]>");
  OutputString("[->>[->>>+<<<]<]");
  OpFly(6);
  OpClear(OpN(8),9);
  OpClear(OpN(4),9);
  if (D) OpSet(OpR(D),OpN(2));
  else OpClear(OpN(2),9);
  if (M) OpSet(OpR(M),OpN(3));
  else OpClear(OpN(3),9);
}
void OpDivMod(int D,int M){OpDivModQS(D,M,OpR(0),OpR(1));}
void OpIfWhile(int Not)
{
  if (OpR(1)->H)
  {
    OpClear(OpN(0),0);
    OpCopy(OpR(0),OpN(0),OpN(1),9);
    OpGoto(OpN(0),0);
    OpAdd(-OpR(1)->N);
  }
  else
  {
    OpPrepare01(0,1,2);
    OpMoveReverse(OpN(1),OpN(0),0);
  }
  if (Not)
  {
    OpGoto(OpN(1),0);
    OutputString("+>[[-]<-]<[>+<-<]");
    OpFly(2);
  }
  OpGoto(OpN(0),0);
}

void Generate(Array AST)
{
  int X,T0,T1,F;
  Map _CallArg = CallArg;
  for (F = 0;F < AST->P;++F) switch ((Arg = (Array)AST->D[F])->O)
  {
    case 8000 : // set
      OpGoto(OpR(0),0);
      OutputString("[-]");
      if (OpR(1)->H) OpAdd(OpR(1)->N);
      else OpCopy(OpR(1),OpR(0),OpN(0),9);
      break;
    case 8010 : // inc
      if (OpR(1)->H)
      {
        OpGoto(OpR(0),0);
        OpAdd(OpR(1)->N);
      }
      else
      {
        OpCopy(OpR(0),OpN(0),OpN(1),9);
        OpMove(OpN(0),OpR(0),0);
      }
      break;
    case 8011 : // dec
      if (OpR(1)->H)
      {
        OpGoto(OpR(0),0);
        OpAdd(-OpR(1)->N);
      }
      else
      {
        OpCopy(OpR(0),OpN(0),OpN(1),9);
        OpMove(OpN(0),OpR(0),0);
      }
      break;
    case 8012 : // add
      OpPrepare01(0,1,2);
      OpMove(OpN(1),OpN(0),0);
      OpSet(OpR(2),OpN(0));
      break;
    case 8013 : // sub
      OpPrepare01(0,1,2);
      OpMoveReverse(OpN(1),OpN(0),0);
      OpSet(OpR(2),OpN(0));
      break;
    case 8014 : // mul
      OpPrepare01(0,1,2);
      OpBegin(OpN(0),0);
      OpCopy(OpN(1),OpN(2),OpN(3),9);
      OpEnd(OpN(0),0);
      OpClear(OpN(1),9);
      OpSet(OpR(2),OpN(2));
      break;
    case 8015 : // divmod
      OpDivMod(2,3);
      break;
    case 8016 : // div
      OpDivMod(2,0);
      break;
    case 8017 : // mod
      OpDivMod(0,2);
      break;
    case 8020 : // cmp
      X = 4;
      T0 = 3;
      T1 = 2;
      OpPrepareTwo(OpR(0),OpN(T0),OpN(X),0);
      OpPrepareTwo(OpR(1),OpN(T1),OpN(1 + X),0);
      OpMoveReverse(OpN(1 + X),OpN(X),0);

      OpGoto(OpN(1 + X),0);
      OutputString("+>[[-]");
      OpFly(X);

      OpGoto(OpN(T1 - 1),0);
      OutputString("+<[>-]>[");
      OpFly(T1 - 1);
      OpGoto(OpN(X),0);
      OutputChar('+');
      OpGoto(OpN(T0),0);
      OutputString("[-]");
      OpGoto(OpN(T1 - 1),0);
      OutputString("->]<+");
      OpGoto(OpN(T0),0);
      OutputChar('[');
      OpGoto(OpN(T1),0);
      OutputString("-[>-]>[");
      OpFly(T1 - 1);
      OpGoto(OpN(X),0);
      OutputChar('+');
      OpGoto(OpN(T0),0);
      OutputString("[-]+");
      OpGoto(OpN(T1 - 1),0);
      OutputString("->]<+");
      OpGoto(OpN(T0),0);
      OutputString("-]");

      OpGoto(OpN(X),0);
      OutputString("[<-]<[>-<-<]");
      OpFly(2 + X);

      OpGoto(OpN(1 + X),0);
      OutputString("]<[-<]>");

      OpClear(OpN(3),9);
      OpClear(OpN(2),9);
      OpClear(OpN(1),9);

      OpSet(OpR(2),OpN(X));
      break;
    case 8030 : // a2b
      OpCopy(OpR(0),OpN(2),OpN(0),9);
      OpGoto(OpN(2),0);
      OpAdd(-48);
      OpBegin(OpN(2),0);
      OpGoto(OpN(1),0);
      OpAdd(10);
      OpEnd(OpN(2),0);

      OpCopy(OpR(1),OpN(1),OpN(0),9);
      OpGoto(OpN(1),0);
      OpAdd(-48);

      OpBegin(OpN(1),0);
      OpGoto(OpN(0),0);
      OpAdd(10);
      OpEnd(OpN(1),0);

      OpCopy(OpR(2),OpN(0),OpN(1),9);
      OpGoto(OpN(0),0);
      OpAdd(-48);

      OpSet(OpR(3),OpN(0));
      break;
    case 8031 : // b2a
      OpDivModQS(2,3,OpR(0),OpN(10));
      OpDivModQS(1,2,OpR(2),OpN(10));
      OpGoto(OpR(1),0);
      OpAdd(48);
      OpGoto(OpR(2),0);
      OpAdd(48);
      OpGoto(OpR(3),0);
      OpAdd(48);
      break;
    case 8040 : // lset
      OpPickVar(OpR(0)->C);
      if (OpR(1)->H)
      {
        OpGoto(OpR(0),0);
        OpAdd(OpR(1)->N);
        OutputString("[->+>+<<]");
      }
      else OpCopyTwo(OpR(1),OpN(-1 - VarT->P),OpN(-2 - VarT->P),OpR(0),0);
      if (OpR(2)->H)
      {
        OpGoto(OpR(0),3);
        OpAdd(OpR(2)->N);
      }
      else OpCopy(OpR(2),OpN(-3 - VarT->P),OpR(0),0);
      OpGoto(OpR(0),0);
      OutputString(">[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]");
      OutputString(">>>[-]<[->+<]<");
      OutputString("[[-<+>]<<<[->>>>+<<<<]>>-]<<");
      break;
    case 8041 : // lget
      OpPickVar(OpR(0)->C);
      if (OpR(1)->H)
      {
        OpGoto(OpR(0),0);
        OpAdd(OpR(1)->N);
        OutputString("[->+>+<<]");
      }
      else OpCopyTwo(OpR(1),OpN(-1 - VarT->P),OpN(-2 - VarT->P),OpR(0),0);
      OpGoto(OpR(0),0);
      OutputString(">[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]");
      OutputString(">>>[-<+<<+>>>]<<<[->>>+<<<]>");
      OutputString("[[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<");
      OpClear(OpR(2),0);
      OpMove(OpR(0),OpR(2),3);
      break;
    case 8050 : // ifeq
    case 8052 : // weq
      OpIfWhile(9);
      OutputChar('[');
      OpClear(OpN(0),9);
      break;
    case 8051 : // ifneq
      OpIfWhile(0);
      OutputChar('[');
      OpClear(OpN(0),9);
      break;
    case 8053 : // wneq
      if (OpR(1)->N)
      {
        OpIfWhile(0);
        OutputChar('[');
        OpClear(OpN(0),9);
      }
      else
      {
        OpGoto(OpR(0),0);
        OutputChar('[');
      }
      break;
    case 8054 : // end
      Arg = (Array)AST->D[OpR(0)->N];
      if (8052 == Arg->O)
      {
        OpIfWhile(9);
        OpGoto(OpN(0),0);
      }
      else if (8053 == Arg->O)
      {
        if (OpR(1)->N)
        {
          OpIfWhile(0);
          OpGoto(OpN(0),0);
        }
        else OpGoto(OpR(0),0);
      }
      else
      {
        OpClear(OpN(0),0);
        OpGoto(OpN(0),0);
      }
      OutputChar(']');
      break;
    case 8055 : // call
      OpT = OpR(0);
      if (!MapHas(Proc,OpT->C))
      {
        ErrorNoProc(OpT->C);
        break;
      }
      ProcT = (ProcType)MapLast;
      ProcVar = ProcT->Var;
      ProcVarType = ProcT->VarType;
      if (Arg->P - ProcVar->P - 1)
      {
        ErrorProcLength(OpT->C,ProcVar->P,Arg->P - 1);
        break;
      }
      if (~IndexOf(CallStack,OpT->C))
      {
        ErrorRecursive(OpT->C);
        break;
      }
      ArrayPush(CallStack,(Int)OpT->C);
      CallArg = MapMake();
      for (X = ProcVar->P;X && !Error;)
      {
        char* T = OpR(X--)->C;
        if (_CallArg && MapHas(_CallArg,T)) T = (char*)MapLast;
        MapSet(CallArg,(char*)ProcVar->D[X],(Int)T);
        if (ProcVarType->D[X])
        {
          MapHas(Var,T);
          if (ProcVarType->D[X] - (((VarType)MapLast)->L < 0 ? 9 : 5))
            ErrorArgTypeMismatch(ProcVarType->D[X],(char*)ProcVar->D[X],OpR(0)->C,OpR(1 + X)->C);
        }
      }
      if (!Error) Generate(ProcT->AST);
      MapFree(CallArg,0);
      CallArg = _CallArg;
      --CallStack->P;

      break;
    case 8060 : // read
      OpGoto(OpR(0),0);
      OutputChar(',');
      break;
    case 8061 : // msg
      for (X = 0;X < Arg->P;++X)
        if (OpR(X)->H) OpMsgList(OpR(X)->C);
        else
        {
          OpGoto(OpR(X),0);
          OutputChar('.');
        }
      break;
    case 8400 : // debug
      OutputChar('_');
  }
}

int kcuf(char** Output,const char* Code)
{
  char* V;
  int F;
  PreserveMax = -1;
  for (F = Preserve;F;) Stack[--F] = 0;
  StackAt = 0;
  VarAt = Preserve;
  Var = MapMake();
  AST = CurrentAST = ArrayMake();
  ASTStack = ArrayMake();
  Proc = MapMake();
  ProcVar = ProcVarType = 0;
  CallStack = ArrayMake();
  Error = 0;
  OP = 0;
  OO = 32;
  O = malloc(sizeof(char) * OO);
  CallArg = 0;

  for (IE = Code;*IE;)
  {
    for (I = IE;*IE && 10 != *IE;) ++IE;
    White();
    if (Taste())
    {
      V = Word();
      if (Error) goto End;
      Arg = 0;

      if (!strcmp(V,"VAR"))
      {
        if (ProcVar) ErrorDefineInProc();
        else if (!Taste()) ErrorUnEOL();
        else for (;free(V),V = Word();)
        {
          if (MapHas(Var,V))
          {
            ErrorVarRedeclare(V);
            break;
          }
          VarT = malloc(sizeof(struct VarType));
          MapSet(Var,V,(Int)VarT);
          if ('[' == Taste())
          {
            ++I;
            White();
            VarT->P = VarAt;
            VarAt += 4 + (VarT->L = RawNumber());
            if (']' != Taste())
            {
              ErrorUnclosed('[',']');
              break;
            }
            ++I;
            White();
          }
          else
          {
            VarT->P = VarAt++;
            VarT->L = -1;
          }
        }
      }

      else if (!strcmp(V,"SET")) ArgMake(8000,0,9,-1);

      else if (!strcmp(V,"INC")) ArgMake(8010,0,9,-1);
      else if (!strcmp(V,"DEC")) ArgMake(8011,0,9,-1);
      else if (!strcmp(V,"ADD")) ArgMake(8012,9,9,0,-1);
      else if (!strcmp(V,"SUB")) ArgMake(8013,9,9,0,-1);
      else if (!strcmp(V,"MUL")) ArgMake(8014,9,9,0,-1);
      else if (!strcmp(V,"DIVMOD")) ArgMake(8015,9,9,0,0,-1);
      else if (!strcmp(V,"DIV")) ArgMake(8016,9,9,0,-1);
      else if (!strcmp(V,"MOD")) ArgMake(8017,9,9,0,-1);

      else if (!strcmp(V,"CMP")) ArgMake(8020,9,9,0,-1);

      else if (!strcmp(V,"A2B")) ArgMake(8030,9,9,9,0,-1);
      else if (!strcmp(V,"B2A")) ArgMake(8031,9,0,0,0,-1);

      else if (!strcmp(V,"LSET")) ArgMake(8040,5,9,9,-1);
      else if (!strcmp(V,"LGET")) ArgMake(8041,5,9,0,-1);

      else if (!strcmp(V,"IFEQ")) ArgMake(8050,0,9,-1),ArrayPush(ASTStack,CurrentAST->P);
      else if (!strcmp(V,"IFNEQ")) ArgMake(8051,0,9,-1),ArrayPush(ASTStack,CurrentAST->P);
      else if (!strcmp(V,"WEQ")) ArgMake(8052,0,9,-1),ArrayPush(ASTStack,CurrentAST->P);
      else if (!strcmp(V,"WNEQ")) ArgMake(8053,0,9,-1),ArrayPush(ASTStack,CurrentAST->P);
      else if (!strcmp(V,"PROC"))
      {
        if (ProcVar) ErrorProcNested();
        else
        {
          free(V);
          V = Word();
          if (MapHas(Proc,V)) ErrorProcUsed(V);
          else
          {
            ProcT = malloc(sizeof(struct ProcType));
            ProcT->AST = CurrentAST = ArrayMake();
            ProcT->Var = ProcVar = ArrayMake();
            ProcT->VarType = ProcVarType = ArrayMake();
            MapSet(Proc,V,(Int)ProcT);
          }
          free(V);
          for (;!Error && Taste() && (V = Word());)
          {
            if (~IndexOf(ProcVar,V)) ErrorDupParam(V);
            ArrayPush(ProcVar,(Int)V);
            ArrayPush(ProcVarType,0);
          }
          V = 0;
        }
      }
      else if (!strcmp(V,"END"))
      {
        if (ASTStack->P)
        {
          Arg = ArrayMake();
          (OpT = malloc(sizeof(struct Op)))->C = 0;
          OpT->N = ASTStack->D[--ASTStack->P];
          ArrayPush(Arg,(Int)OpT);
          ArgID(8054);
        }
        else if (ProcVar)
        {
          CurrentAST = AST;
          ProcVar = 0;
        }
        else ErrorEndNothing();
      }
      else if (!strcmp(V,"CALL"))
      {
        Arg = ArrayMake();
        for (;Taste() && !Error;ArrayPush(Arg,(Int)OpT))
          (OpT = malloc(sizeof(struct Op)))->C = Word();
        ArgID(8055);
      }

      else if (!strcmp(V,"READ")) ArgMake(8060,0,-1);
      else if (!strcmp(V,"MSG"))
      {
        Arg = ArrayMake();
        for (;Taste() && !Error;) ArrayPush(Arg,(Int)VarNameOrString());
        ArgID(8061);
      }

      else if (!strcmp(V,"REM")) Discard();

      else ErrorCommand(V);
      if (V) free(V);
      if (Arg) ArrayPush(CurrentAST,(Int)Arg);
      if (!Error && Taste()) ErrorCommandEnd();
      if (Error) goto End;
    }
    if (*IE) ++IE;
  }
  if (!ASTStack->P) Generate(AST);
  else if (!Error) ErrorEndUnclose();

  End :
  O[OP] = 0;
  if (1 + PreserveMax < Preserve && !Error)
  {
    *Output = malloc(sizeof(char) * (OP - Preserve + PreserveMax + 2));
    strcpy(*Output,O + Preserve - PreserveMax - 1);
    free(O);
  }
  else *Output = O;
  ArrayFree(CallStack);
  MapFree(Proc,ProcFree);
  ArrayFree(ASTStack);
  ASTFree(AST);
  MapFree(Var,VarFree);
  return Error ? Error : 0;
}

#######################################
#include <stddef.h>
#include <assert.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>

#define UNUSED(x) ((void) (x))

#define assert_is_instruction(node, in) do { \
  assert((node)->type == NODE_STATEMENT); \
  assert((node)->inst == (in)); \
  } while (0)

#define STATES_COUNT_HALF 128

struct strbuf {
  char *s;
  size_t alloc;
  size_t len;
};

struct tokens {
  char **items;
  char *buf;
  size_t buflen;
};

struct scanner {
  const char *c;
  char **t;
  char *b;
  int error;
  char *lt;
  struct tokens *tokens;
};

enum node_type {
  NODE_EMPTY = 0,
  NODE_NUMBER,
  NODE_PROGRAM,
  NODE_STATEMENT,
  NODE_STRING,
  NODE_VAR_NAME,
  NODE_VAR_SINGLE,
};

enum instruction {
  I_INVALID = 0,
  I_A2B,
  I_ADD,
  I_B2A,
  I_CALL,
  I_CMP,
  I_DEC,
  I_DIV,
  I_DIVMOD,
  I_END,
  I_IFEQ,
  I_IFNEQ,
  I_INC,
  I_LGET,
  I_LSET,
  I_MOD,
  I_MSG,
  I_MUL,
  I_PROC,
  I_READ,
  I_SET,
  I_SUB,
  I_VAR,
  I_WNEQ,
};

struct node {
  enum node_type type;
  union {
    enum instruction inst;
    char *string;
    unsigned char num;
  };
  struct node *child;
  struct node *baby;
  struct node *next;
  struct node *prev;
  struct node *parent;
  struct node *nextvar;
  struct node *locals;
  size_t pos;
  size_t len;
  unsigned char defined:1;
};

struct ast {
  char *buf;
  char *b;
  size_t alloc;
  size_t len;
  struct node *root;
  struct tokens *tokens;
};

struct parser {
  struct ast *ast;
  char **t;
};

struct compiler {
  struct ast *ast;
  struct strbuf *b;
  size_t pos;
  struct node *globals;
  struct node *procedures;
  struct node *calls;
  size_t top;
  size_t indent;
  size_t block;
};

void set_verbosity(unsigned char v);
const char *instruction_to_string(enum instruction inst);
void tokens_init(struct tokens *tokens, const char *code);
void tokens_destroy(struct tokens *tokens);
void scanner_init(struct scanner *s, const char *code, struct tokens *tokens);
void scanner_destroy(struct scanner *s);
void scanner_scan(struct scanner *s);
void ast_init(struct ast *ast, struct tokens *tokens);
void ast_destroy(struct ast *ast);
void ast_collect_strings(struct ast *ast, size_t pos);
void parser_init(struct parser *p, char **tokens, struct ast *ast);
void parser_destroy(struct parser *p);
int parser_parse(struct parser *p);
int kcuf(char **output, const char *code);

#define bug(x) assert(0 && (x))

static unsigned char verbosity = 0;

static const char S_INVALID[] = "?";
static const char S_A2B[] = "a2b";
static const char S_ADD[] = "add";
static const char S_B2A[] = "b2a";
static const char S_CALL[] = "call";
static const char S_CMP[] = "cmp";
static const char S_DEC[] = "dec";
static const char S_DIV[] = "div";
static const char S_DIVMOD[] = "divmod";
static const char S_END[] = "end";
static const char S_IFEQ[] = "ifeq";
static const char S_IFNEQ[] = "ifneq";
static const char S_INC[] = "inc";
static const char S_LGET[] = "lget";
static const char S_LSET[] = "lset";
static const char S_MOD[] = "mod";
static const char S_MSG[] = "msg";
static const char S_MUL[] = "mul";
static const char S_PROC[] = "proc";
static const char S_READ[] = "read";
static const char S_SET[] = "set";
static const char S_SUB[] = "sub";
static const char S_VAR[] = "var";
static const char S_WNEQ[] = "wneq";

enum error {
  SCANNER_ERROR = 2,
  INVALID_SYNTAX = 3,
  INVALID_ARRAY_SIZE = 4,
  UNDEFINED_VARIABALE = 5,
  DUPLICATE_VARIABLE = 6,
  NOT_A_SCALAR = 7,
  NOT_A_LIST = 8,
  EXTRA_END = 9,
  MISSING_END = 10,
  DUPLICATE_PROCEDURE = 11,
  UNDEFINED_PROCEDURE = 12,
  TOO_FEW_PARAMETERS = 13,
  TOO_MUCH_PARAMETERS = 14,
  DUPLICATE_PARAMETERS = 15,
  RECURSIVE_CALL = 16,
};

static char empty_string[] = "";

void set_verbosity(unsigned char v)
{
  verbosity = v;
}

static int char_is_brainfuck_command(char c)
{
  switch (c) {
  case '>':
  case '<':
  case '+':
  case '-':
  case '.':
  case ',':
  case '[':
  case ']':
    return 1;
  default:
    return 0;
  }

}

static struct string_instruction_map {
  const char *string;
  enum instruction inst;
} string_instruction_map[] = {
  {S_A2B, I_A2B},
  {S_ADD, I_ADD},
  {S_B2A, I_B2A},
  {S_CALL, I_CALL},
  {S_CMP, I_CMP},
  {S_DEC, I_DEC},
  {S_DIV, I_DIV},
  {S_DIVMOD, I_DIVMOD},
  {S_END, I_END},
  {S_IFEQ, I_IFEQ},
  {S_IFNEQ, I_IFNEQ},
  {S_INC, I_INC},
  {S_LGET, I_LGET},
  {S_LSET, I_LSET},
  {S_MOD, I_MOD},
  {S_MSG, I_MSG},
  {S_MUL, I_MUL},
  {S_PROC, I_PROC},
  {S_READ, I_READ},
  {S_SET, I_SET},
  {S_SUB, I_SUB},
  {S_VAR, I_VAR},
  {S_WNEQ, I_WNEQ},
  {NULL, I_INVALID},
};

static enum instruction string_to_instruction(char *s)
{
  struct string_instruction_map *item = string_instruction_map;
  for (; item->string; item++)
    if (strcmp(s, item->string) == 0)
      return item->inst;
  return I_INVALID;
}

const char *instruction_to_string(enum instruction inst)
{
  struct string_instruction_map *item = string_instruction_map;
  for (; item->string; item++)  /* LCOV_EXCL_LINE */
    if (inst == item->inst)
      return item->string;
  return S_INVALID;  /* LCOV_EXCL_LINE */
}

static void strbuf_init(struct strbuf *b)
{
  b->s = malloc(sizeof(*b->s));
  *b->s = '\0';
  b->alloc = 1;
  b->len = 0;
}

static void strbuf_destroy(struct strbuf *b)
{
  free(b->s);
  b->s = NULL;
  b->alloc = 0;
  b->len = 0;
}

static void strbuf_grow(struct strbuf *b, size_t len_diff)
{
  size_t new_len = b->len + len_diff;
  if (new_len < b->alloc)
    return;
  b->alloc = 2 * new_len;
  b->s = realloc(b->s, b->alloc * sizeof(*b->s));
  b->s[b->len] = '\0';
}

static void strbuf_write_char(struct strbuf *b, char c)
{
  strbuf_grow(b, 1);
  b->s[b->len++] = c;
  b->s[b->len] = '\0';
}

static void strbuf_vprintf(struct strbuf *b, const char *fmt, va_list ap)
{
  va_list cp;
  va_copy(cp, ap);
  size_t len = vsnprintf(NULL, 0, fmt, cp);
  va_end(cp);

  strbuf_grow(b, len);
  b->len += vsprintf(b->s + b->len, fmt, ap);
}

void tokens_init(struct tokens *t, const char *code)
{
  size_t len = strlen(code);
  t->buflen = 2 * len + 1;
  t->buf = calloc(t->buflen, sizeof(*t->buf));
  t->items = calloc(len + 1, sizeof(*t->items));
}

void tokens_destroy(struct tokens *t)
{
  free(t->items);
  t->items = NULL;

  free(t->buf);
  t->buf = NULL;

  t->buflen = 0;
}

void scanner_init(struct scanner *s, const char *code, struct tokens *tokens)
{
  s->tokens = tokens;
  s->c = code;
  s->t = s->tokens->items;
  s->b = s->tokens->buf;
  s->lt = empty_string;
  s->error = 0;
}

void scanner_destroy(struct scanner *s)
{
  s->c = NULL;
  s->t = NULL;
  s->b = NULL;
  s->lt = NULL;
  s->error = 0;
  s->tokens = NULL;
}

static size_t count_strings(char **strings)
{
  assert(strings);  /* LCOV_EXCL_LINE */
  size_t i = 0;
  for (; strings[i]; i++)
    continue;
  return i;
}

void ast_init(struct ast *ast, struct tokens *tokens)
{
  ast->alloc = count_strings(tokens->items) + 1;
  ast->len = 0;
  ast->root = malloc(ast->alloc * sizeof(*ast->root));
  ast->tokens = tokens;
  ast->buf = calloc(tokens->buflen, sizeof(*ast->buf));
  ast->b = ast->buf;
}

void ast_destroy(struct ast *ast)
{
  free(ast->root);
  ast->root = NULL;

  free(ast->buf);
  ast->buf = NULL;

  ast->alloc = 0;
  ast->len = 0;
  ast->tokens = NULL;
  ast->b = NULL;
}

static struct node *ast_node_alloc(struct ast *ast)
{
  return ast->root + ast->len++;
}

static void node_init(struct node *node)
{
  node->type = NODE_EMPTY;
  node->child = NULL;
  node->baby = NULL;
  node->next = NULL;
  node->prev = NULL;
  node->parent = NULL;
  node->nextvar = NULL;
  node->locals = NULL;
  node->pos = 0;
  node->len = 0;
  node->defined = 0;
}

static struct node *node_new(struct ast *ast)
{
  struct node *node = ast_node_alloc(ast);
  node_init(node);
  return node;
}

void parser_init(struct parser *p, char **tokens, struct ast *ast)
{
  p->ast = ast;
  p->t = tokens;
}

void parser_destroy(struct parser *p)
{
  p->ast = NULL;
  p->t = NULL;
}

static void compiler_init(struct compiler *co, struct ast *ast,
    struct strbuf *b)
{
  co->ast = ast;
  co->b = b;
  co->pos = 0;
  co->globals = NULL;
  co->procedures = NULL;
  co->calls = NULL;
  co->top = 0;
  co->indent = 0;
  co->block = 0;
}

static void compiler_destroy(struct compiler *co)
{
  co->ast = NULL;
  co->b = NULL;
  co->pos = 0;
  co->globals = NULL;
  co->procedures = NULL;
  co->calls = NULL;
  co->top = 0;
  co->indent = 0;
  co->block = 0;
}

static int is_var_prefix(char c)
{
  return isalpha(c) || c == '_' || c == '$';
}

static int is_int_start(const char *s)
{
  return isdigit(*s) || (*s == '-' && isdigit(s[1]));
}

/* SCANNER */

static void scanner_start_token(struct scanner *s)
{
  *s->t = s->b;
}

static void scanner_end_token(struct scanner *s)
{
  *s->b++ = '\0';
  s->lt = *s->t;
  s->t++;
}

static void scanner_add_empty_token(struct scanner *s)
{
  *s->t++ = s->lt = empty_string;
}

static int scanner_is_eol(struct scanner *s)
{
  return *s->c == '\n';
}

static void scanner_ignore_rest_of_the_line(struct scanner *s)
{
  while (*s->c && !scanner_is_eol(s))
    s->c++;
}

static int scanner_is_char_quote(struct scanner *s)
{
  return *s->c == '\'';
}

static int scanner_is_comment_start(struct scanner *s)
{
  switch (*s->c) {
  case '#':
    return 1;
  case '/':
  case '-':
    return s->c[1] == *s->c;
  default:
    return 0;
  }
}

static int scanner_is_int_start(struct scanner *s)
{
  return is_int_start(s->c);
}

static int scanner_is_single_char_token(struct scanner *s)
{
  switch (*s->c) {
  case '[':
  case ']':
    return 1;
  default:
    return 0;
  }
}

static int scanner_is_string_quote(struct scanner *s)
{
  return *s->c == '"';
}

static int scanner_is_var_prefix(struct scanner *s)
{
  return is_var_prefix(*s->c);
}

static int scanner_is_var_suffix(struct scanner *s)
{
  return scanner_is_var_prefix(s) || isdigit(*s->c);
}

static int scanner_error(struct scanner *s)
{
  s->error = SCANNER_ERROR;
  fprintf(stderr, "scanner error: remaining characters: \"%s\"\n", s->c);
  return 0;
}

static int scanner_scan_escaped_char_element(struct scanner *s)
{
  *s->b++ = *s->c++;
  if (!*s->c)
    return 0;

  switch (*s->c) {
  case '>':
  case '\\':
  case '\'':
  case '"':
  case 'n':
  case 'r':
  case 't':
    *s->b++ = *s->c++;
    return *s->c;
  default:
    return 0;
  }
}

static int scanner_scan_char_element(struct scanner *s)
{
  switch (*s->c) {
  case '\\':
    return scanner_scan_escaped_char_element(s);
  case '\'':
  case '"':
    return 0;
  default:
    break;
  }
  *s->b++ = *s->c++;
  return 1;
}

static int scanner_scan_char(struct scanner *s)
{
  assert(scanner_is_char_quote(s));  /* LCOV_EXCL_LINE */
  scanner_start_token(s);
  *s->b++ = *s->c++;
  if (!(scanner_scan_char_element(s) && scanner_is_char_quote(s)))
    return scanner_error(s);
  *s->b++ = *s->c++;
  scanner_end_token(s);
  return *s->c;
}

static int scanner_scan_comment(struct scanner *s)
{
  assert(scanner_is_comment_start(s));  /* LCOV_EXCL_LINE */
  scanner_ignore_rest_of_the_line(s);
  return *s->c;
}

static int scanner_scan_eol(struct scanner *s)
{
  assert(scanner_is_eol(s));  /* LCOV_EXCL_LINE */
  while (scanner_is_eol(s) || isblank(*s->c))
    s->c++;
  scanner_add_empty_token(s);
  return *s->c;
}

static int scanner_scan_int(struct scanner *s)
{
  assert(scanner_is_int_start(s));  /* LCOV_EXCL_LINE */
  scanner_start_token(s);
  *s->b++ = *s->c++;
  while(isdigit(*s->c))
    *s->b++ = *s->c++;
  scanner_end_token(s);
  return *s->c;
}

static int scanner_scan_single_char_token(struct scanner *s)
{
  assert(scanner_is_single_char_token(s));  /* LCOV_EXCL_LINE */
  scanner_start_token(s);
  *s->b++ = *s->c++;
  scanner_end_token(s);
  return *s->c;
}

static int scanner_scan_string(struct scanner *s)
{
  assert(scanner_is_string_quote(s));  /* LCOV_EXCL_LINE */
  scanner_start_token(s);
  *s->b++ = *s->c++;
  while (*s->c && *s->c != '"' && scanner_scan_char_element(s))
    continue;
  if (*s->c != '"')
    return scanner_error(s);
  *s->b++ = *s->c++;
  scanner_end_token(s);
  return *s->c;
}

static int scanner_scan_var_name(struct scanner *s)
{
  assert(scanner_is_var_prefix(s));  /* LCOV_EXCL_LINE */
  int is_first_token_on_line = !*s->lt;
  char *b = s->b;
  scanner_start_token(s);
  *s->b++ = tolower(*s->c++);
  while (scanner_is_var_suffix(s))
    *s->b++ = tolower(*s->c++);
  scanner_end_token(s);
  if (is_first_token_on_line && strcmp(s->lt, "rem") == 0) {
    s->b = b;
    *--s->t = NULL;
    s->lt = empty_string;
    scanner_ignore_rest_of_the_line(s);
  }
  return *s->c;
}

static int scanner_next_token(struct scanner *s)
{
  while (isblank(*s->c))
    s->c++;

  if (!*s->c)
    return 0;

  if (scanner_is_eol(s))
    return scanner_scan_eol(s);

  if (scanner_is_single_char_token(s))
    return scanner_scan_single_char_token(s);

  if (scanner_is_comment_start(s))
    return scanner_scan_comment(s);

  if (scanner_is_var_prefix(s))
    return scanner_scan_var_name(s);

  if (scanner_is_int_start(s))
    return scanner_scan_int(s);

  if (scanner_is_char_quote(s))
    return scanner_scan_char(s);

  if (scanner_is_string_quote(s))
    return scanner_scan_string(s);

  return scanner_error(s);
}

void scanner_scan(struct scanner *s)
{
  while(scanner_next_token(s))
    continue;
}

/*** PARSER ***/

static int node_is_instruction(struct node *node, enum instruction inst)
{
  return node && node->type == NODE_STATEMENT && node->inst == inst;
}

static int node_in_proc(struct node *node)
{
  for (struct node *p = node->parent; p; p = p->parent)
    if (node_is_instruction(p, I_PROC))
      return 1;
  return 0;
}

static void node_append_child(struct node *node, struct node *child)
{
  child->parent = node;
  child->next = NULL;

  if (node->baby) {
    child->prev = node->baby;
    node->baby = node->baby->next = child;
  } else {
    child->prev = NULL;
    node->child = node->baby = child;
  }
}

static void node_locals_insert(struct node *node, struct node *local)
{
  local->nextvar = node->locals;
  node->locals = local;
}

static void node_locals_pop(struct node *node)
{
  node->locals = node->locals->nextvar;
}

static struct node *parser_node_new(struct parser *p)
{
  return node_new(p->ast);
}

static int parser_is_var_prefix(struct parser *p)
{
  return *p->t && is_var_prefix(**p->t);
}

static char *parser_read_var_name(struct parser *p)
{
  char * const str = p->ast->b;
  p->ast->b += sprintf(p->ast->b, "%s", *p->t);
  *p->ast->b++ = '\0';
  return str;
}

static size_t read_char(char *s, char *c)
{
  if (*s != '\\') {
    *c = *s;
    return 1;
  }

  s++;
  switch (*s) {
  case 'n':
    *c = '\n';
    break;
  case 'r':
    *c = '\r';
    break;
  case 't':
    *c = '\t';
    break;
  default:
    *c = *s;
    break;
  }

  return 2;
}

static int parser_read_char(struct parser *p)
{
  char c;
  read_char(*p->t + 1, &c);
  return c;
}

static char *parser_read_string(struct parser *p)
{
  char * const str = p->ast->b;
  char *s = *p->t + 1;
  while (*s != '"')
    s += read_char(s, p->ast->b++);
  *p->ast->b++ = '\0';
  return str;
}

static int parser_read_number(struct parser *p)
{
  return atoi(*p->t);
}

static int parser_read_instruction(struct parser *p)
{
  return string_to_instruction(*p->t);
}

static int parser_parse_char(struct parser *p, struct node *parent)
{
  if (!(*p->t && **p->t == '\''))
    return INVALID_SYNTAX;

  struct node *node = parser_node_new(p);
  node->type = NODE_NUMBER;
  node->num = parser_read_char(p);
  node_append_child(parent, node);
  p->t++;
  return 0;
}

static int parser_parse_int(struct parser *p, struct node *parent)
{
  if (!(*p->t && is_int_start(*p->t)))
    return INVALID_SYNTAX;

  struct node *node = parser_node_new(p);
  node->type = NODE_NUMBER;
  node->num = parser_read_number(p);
  node_append_child(parent, node);
  p->t++;
  return 0;
}

static int parser_parse_number(struct parser *p, struct node *parent)
{
  return parser_parse_int(p, parent) && parser_parse_char(p, parent);
}

static int parser_parse_array_size(struct parser *p, struct node *parent)
{
  if (!(*p->t && isdigit(**p->t)))
    return INVALID_SYNTAX;

  struct node *node = parser_node_new(p);
  node->type = NODE_NUMBER;
  int size = parser_read_number(p);
  if (size < 1 || size > 256)
    return INVALID_ARRAY_SIZE;
  node->num = size - 1;
  node_append_child(parent, node);
  p->t++;
  return 0;
}

static int parser_parse_args_s(struct parser *p, struct node *parent)
{
  assert(*p->t);  /* LCOV_EXCL_LINE */
  if (**p->t != '"')
    return INVALID_SYNTAX;

  struct node *string = parser_node_new(p);
  string->type = NODE_STRING;
  string->string = parser_read_string(p);
  node_append_child(parent, string);
  p->t++;
  return 0;
}

static int parser_parse_args_v(struct parser *p, struct node *parent)
{
  if (!parser_is_var_prefix(p))
    return INVALID_SYNTAX;

  struct node *var_name = parser_node_new(p);
  var_name->type = NODE_VAR_NAME;
  var_name->string = parser_read_var_name(p);
  node_append_child(parent, var_name);
  p->t++;
  return 0;
}

static int parser_parse_args_vs(struct parser *p,
    struct node *parent)
{
  if (parser_parse_args_v(p, parent) && parser_parse_args_s(p, parent))
    return INVALID_SYNTAX;
  return 0;
}

static int parser_parse_args_vn(struct parser *p,
    struct node *parent)
{
  if (parser_parse_args_v(p, parent) && parser_parse_number(p, parent))
    return INVALID_SYNTAX;
  return 0;
}

static int parser_parse_args_vn_v_v_v(struct parser *p, struct node *parent)
{
  int err = parser_parse_args_vn(p, parent);
  if (err)
    return err;

  if ((err = parser_parse_args_v(p, parent)))
    return err;

  if ((err = parser_parse_args_v(p, parent)))
    return err;

  return parser_parse_args_v(p, parent);
}

static int parser_parse_args_vn_vn_v(struct parser *p, struct node *parent)
{
  int err = parser_parse_args_vn(p, parent);
  if (err)
    return err;

  if ((err = parser_parse_args_vn(p, parent)))
    return err;

  return parser_parse_args_v(p, parent);
}

static int parser_parse_args_vn_vn_v_v(struct parser *p, struct node *parent)
{
  int err = parser_parse_args_vn_vn_v(p, parent);
  if (err)
    return err;
  return parser_parse_args_v(p, parent);
}

static int parser_parse_args_vn_vn_vn_v(struct parser *p, struct node *parent)
{
  int err = parser_parse_args_vn(p, parent);
  if (err)
    return err;

  if ((err = parser_parse_args_vn(p, parent)))
    return err;

  if ((err = parser_parse_args_vn(p, parent)))
    return err;

  return parser_parse_args_v(p, parent);
}

static int parser_parse_args_msg(struct parser *p, struct node *parent)
{
  int err = INVALID_SYNTAX;
  while (*p->t && **p->t) {
    if ((err = parser_parse_args_vs(p, parent)))
      return err;
  }
  return err;
}

static int parser_parse_args_read(struct parser *p, struct node *parent)
{
  return parser_parse_args_v(p, parent);
}

static int parser_parse_args_v_vn(struct parser *p, struct node *parent)
{
  int err = parser_parse_args_v(p, parent);
  if (err)
    return err;

  return parser_parse_args_vn(p, parent);
}

static int parser_parse_args_v_vn_v(struct parser *p, struct node *parent)
{
  int err = parser_parse_args_v_vn(p, parent);
  if (err)
    return err;

  return parser_parse_args_vn(p, parent);
}

static int parser_parse_args_v_vn_vn(struct parser *p, struct node *parent)
{
  int err = parser_parse_args_v_vn(p, parent);
  if (err)
    return err;

  return parser_parse_args_vn(p, parent);
}

static int parser_parse_args_v_plus(struct parser *p, struct node *parent)
{
  int err = INVALID_SYNTAX;
  while (*p->t && **p->t) {
    if ((err = parser_parse_args_v(p, parent)))
      return err;
  }
  return err;
}

static int parser_parse_var_single(struct parser *p, struct node *statement)
{
  if (!parser_is_var_prefix(p))
    return INVALID_SYNTAX;

  struct node *var_single = parser_node_new(p);
  var_single->type = NODE_VAR_SINGLE;
  var_single->string = parser_read_var_name(p);
  node_append_child(statement, var_single);
  p->t++;
  if (*p->t && **p->t == '[') {
    p->t++;
    int err = parser_parse_array_size(p, var_single);
    if (err)
      return err;

    if (!(*p->t && **p->t == ']'))
      return INVALID_SYNTAX;
    p->t++;
  }
  return 0;
}

static int parser_parse_args_var(struct parser *p, struct node *statement)
{
  if (node_in_proc(statement))
    return INVALID_SYNTAX;

  int err = INVALID_SYNTAX;
  while (*p->t && **p->t) {
    if ((err = parser_parse_var_single(p, statement)))
      return err;
  }
  return err;
}

static int parser_parse_statements(struct parser *p, struct node *parent);

static int parser_parse_args_proc(struct parser *p, struct node *statement)
{
  if (node_in_proc(statement))
    return INVALID_SYNTAX;

  int err = parser_parse_args_v_plus(p, statement);
  if (err)
    return err;

  for (struct node *a = statement->child->next; a; a = a->next)
    for (struct node *b = a->next; b; b = b->next)
      if (strcmp(a->string, b->string) == 0)
        return DUPLICATE_PARAMETERS;

  return parser_parse_statements(p, statement);
}

static int parser_parse_block_v_vn(struct parser *p, struct node *statement)
{
  int err = parser_parse_args_v_vn(p, statement);
  if (err)
    return err;

  return parser_parse_statements(p, statement);
}

static int parser_parse_args(struct parser *p, struct node *statement)
{
  int err = 0;
  switch(statement->inst) {  /* LCOV_EXCL_LINE */
  case I_A2B:
    err = parser_parse_args_vn_vn_vn_v(p, statement);
    break;
  case I_ADD:
  case I_CMP:
  case I_DIV:
  case I_MOD:
  case I_MUL:
  case I_SUB:
    err = parser_parse_args_vn_vn_v(p, statement);
    break;
  case I_B2A:
    err = parser_parse_args_vn_v_v_v(p, statement);
    break;
  case I_CALL:
    err = parser_parse_args_v_plus(p, statement);
    break;
  case I_DIVMOD:
    err = parser_parse_args_vn_vn_v_v(p, statement);
    break;
  case I_DEC:
  case I_INC:
  case I_SET:
    err = parser_parse_args_v_vn(p, statement);
    break;
  case I_END:
    if (statement->parent->type == NODE_PROGRAM)
      err = EXTRA_END;
    break;
  case I_IFEQ:
  case I_IFNEQ:
  case I_WNEQ:
    err = parser_parse_block_v_vn(p, statement);
    break;
  case I_LGET:
    err = parser_parse_args_v_vn_v(p, statement);
    break;
  case I_LSET:
    err = parser_parse_args_v_vn_vn(p, statement);
    break;
  case I_MSG:
    err = parser_parse_args_msg(p, statement);
    break;
  case I_PROC:
    err = parser_parse_args_proc(p, statement);
    break;
  case I_READ:
    err = parser_parse_args_read(p, statement);
    break;
  case I_VAR:
    err = parser_parse_args_var(p, statement);
    break;
  case I_INVALID:
    err = INVALID_SYNTAX;
    break;
  default:  /* LCOV_EXCL_LINE */
    bug("missing handler");  /* LCOV_EXCL_LINE */
  }
  if (err)
    return err;

  if (*p->t && **p->t)
    return INVALID_SYNTAX;

  return 0;
}

static int parser_parse_statement(struct parser *p, struct node *parent)
{
  if (!**p->t)
    return 0;
  struct node *statement = parser_node_new(p);
  statement->type = NODE_STATEMENT;
  statement->inst = parser_read_instruction(p);
  node_append_child(parent, statement);
  p->t++;
  return parser_parse_args(p, statement);
}

static int parser_parse_statements(struct parser *p, struct node *parent)
{
  while (*p->t) {
    int err = parser_parse_statement(p, parent);
    if (err)
      return err;
    if (node_is_instruction(parent->baby, I_END))
      break;
    if (!(*p->t++))
      break;
  }
  return 0;
}

static int parser_parse_program(struct parser *p)
{
  struct node *prog = p->ast->root = parser_node_new(p);
  prog->type = NODE_PROGRAM;
  return parser_parse_statements(p, prog);
}

int parser_parse(struct parser *p)
{
  return parser_parse_program(p);
}

/*** COMPILER ****/

/** AST-INDEPENDENT **/

static size_t compiler_push_n(struct compiler *co, size_t n)
{
  size_t top = co->top;
  co->top += n;
  return top;
}

static size_t compiler_push(struct compiler *co)
{
  return compiler_push_n(co, 1);
}

static int compiler_call_insert(struct compiler *co, struct node *call)
{
  for (struct node *c = co->calls; c; c = c->nextvar)
    if (strcmp(c->child->string, call->child->string) == 0)
      return RECURSIVE_CALL;

  call->nextvar = co->calls;
  co->calls = call;
  return 0;
}

static void compiler_call_pop(struct compiler *co)
{
  co->calls = co->calls->nextvar;
}

static void compiler_pop_n(struct compiler *co, size_t old_top, size_t n)
{
  assert(co->top == old_top + n);  /* LCOV_EXCL_LINE */
  co->top -= n;
  assert(co->top == old_top);  /* LCOV_EXCL_LINE */
}

static void compiler_pop(struct compiler *co, size_t old_top)
{
  compiler_pop_n(co, old_top, 1);
}

static size_t compiler_globals_start(struct compiler *co)
{
  UNUSED(co);
  return 0;
}

static void compiler_write_char(struct compiler *co, char c)
{
  switch (c) {
  case '[':
    co->block++;
    break;
  case ']':
    assert(co->block);  /* LCOV_EXCL_LINE */
    co->block--;
    break;
  }
  strbuf_write_char(co->b, c);
}

/* COMMENTS */

static void compiler_vprintf(struct compiler *co, const char *fmt,
    va_list ap)
{
  strbuf_vprintf(co->b, fmt, ap);
}

static void compiler_vcomment(struct compiler *co, const char *fmt, va_list ap)
{
  size_t len = co->b->len;
  compiler_vprintf(co, fmt, ap);
  for (size_t i = len; i < co->b->len; i++)
    if (char_is_brainfuck_command(co->b->s[i]))
      co->b->s[i] = '?';
}

static void compiler_comment(struct compiler *co, const char *fmt, ...)
{
  if (!verbosity)
    return;
  va_list ap;
  va_start(ap, fmt);
  compiler_vcomment(co, fmt, ap);
  va_end(ap);
}

static void compiler_indent(struct compiler *co)
{
  co->indent++;
}

static void compiler_dedent(struct compiler *co)
{
  assert(co->indent);  /* LCOV_EXCL_LINE */
  co->indent--;
}

static void compiler_comment_indented(struct compiler *co, const char *fmt, ...)
{
  if (co->indent >= verbosity)
    return;

  compiler_comment(co, "\n");
  for (size_t i = 0; i < co->indent; i++)
    compiler_comment(co, "\t", i);
  va_list ap;
  va_start(ap, fmt);
  compiler_vcomment(co, fmt, ap);
  va_end(ap);
}

#define f (__func__ + 9)

#define compiler_comment_f(co) \
  compiler_comment_indented((co), "%s()", (f))

#define compiler_comment_f_n(co, n) \
  compiler_comment_indented((co), "%s(%hhu)", (f), (n))

#define compiler_comment_f_v(co, v) \
  compiler_comment_indented((co), "%s(%zd)", (f), (v))

#define compiler_comment_f_v_n(co, v, n) \
  compiler_comment_indented((co), "%s(%zd %hhu)", (f), (v), (n))

#define compiler_comment_f_v_n_n(co, v, n, k) \
  compiler_comment_indented((co), \
      "%s(%zd %hhu %hhu)", (f), (v), (n), (k))

#define compiler_comment_f_v_n_v(co, x, n, y) \
  compiler_comment_indented((co), \
      "%s(%zd %hhu %zd)", (f), (x), (n), (y))

#define compiler_comment_f_v_v(co, x, y) \
  compiler_comment_indented((co), "%s(%zd %zd)", (f), (x), (y))

#define compiler_comment_f_v_v_n(co, r, x, y) \
  compiler_comment_indented((co), \
      "%s(%zd %zd %hhu)", (f), (r), (x), (y))

#define compiler_comment_f_v_v_n_n(co, q, r, n, k) \
  compiler_comment_indented((co), \
      "%s(%zd %zd %hhu %hhu)", (f), (q), (r), (n), (k))

#define compiler_comment_f_v_v_n_v(co, q, r, n, v) \
  compiler_comment_indented((co), \
      "%s(%zd %zd %hhu %zd)", (f), (q), (r), (n), (v))

#define compiler_comment_f_v_v_v(co, r, x, y) \
  compiler_comment_indented((co), \
      "%s(%zd %zd %zd)", (f), (r), (x), (y))

#define compiler_comment_f_v_v_v_n(co, q, r, v, n) \
  compiler_comment_indented((co), \
      "%s(%zd %zd %zd %hhu)", (f), (q), (r), (v), (n))

#define compiler_comment_f_v_v_v_v(co, q, r, x, y) \
  compiler_comment_indented((co), \
      "%s(%zd %zd %zd %zd)", (f), (q), (r), (x), (y))

/* BRAINFUCK PRIMITIVES */

static void compiler_primitive_dec(struct compiler *co)
{
  compiler_indent(co);
  compiler_comment_indented(co, "");
  compiler_write_char(co, '-');
  compiler_dedent(co);
}

static void compiler_primitive_inc(struct compiler *co)
{
  compiler_indent(co);
  compiler_comment_indented(co, "");
  compiler_write_char(co, '+');
  compiler_dedent(co);
}

static void compiler_primitive_left(struct compiler *co)
{
  compiler_indent(co);
  compiler_comment_indented(co, "");
  compiler_write_char(co, '<');
  compiler_dedent(co);
}

static void compiler_primitive_left_n(struct compiler *co, size_t n)
{
  for (size_t i = 0; i < n; i++)
    compiler_primitive_left(co);
}

static void compiler_primitive_right(struct compiler *co)
{
  compiler_indent(co);
  compiler_comment_indented(co, "");
  compiler_write_char(co, '>');
  compiler_dedent(co);
}

static void compiler_primitive_right_n(struct compiler *co, size_t n)
{
  for (size_t i = 0; i < n; i++)
    compiler_primitive_right(co);
}

static void compiler_primitive_output(struct compiler *co)
{
  compiler_indent(co);
  compiler_comment_indented(co, "");
  compiler_write_char(co, '.');
  compiler_dedent(co);
}

static void compiler_primitive_input(struct compiler *co)
{
  compiler_indent(co);
  compiler_comment_indented(co, "");
  compiler_write_char(co, ',');
  compiler_dedent(co);
}

static void compiler_primitive_while(struct compiler *co)
{
  compiler_comment_indented(co, "");
  compiler_write_char(co, '[');
  compiler_indent(co);
}

static void compiler_primitive_end(struct compiler *co)
{
  compiler_dedent(co);
  compiler_comment_indented(co, "");
  compiler_write_char(co, ']');
}

/* PSEUDO-PRIMITIVES */

static void compiler_primitive_static_left(struct compiler *co)
{
  compiler_indent(co);
  compiler_comment_f(co);
  compiler_dedent(co);
  compiler_primitive_left(co);
  co->pos--;
}

static void compiler_primitive_static_right(struct compiler *co)
{
  compiler_indent(co);
  compiler_comment_f(co);
  compiler_dedent(co);
  compiler_primitive_right(co);
  co->pos++;
}

static void compiler_primitive_clear(struct compiler *co)
{
  compiler_indent(co);
  compiler_comment_f(co);
  compiler_primitive_while(co);
  compiler_primitive_dec(co);
  compiler_primitive_end(co);
  compiler_dedent(co);
}

static void compiler_primitive_inc_n(struct compiler *co, unsigned char n);

static void compiler_primitive_dec_n(struct compiler *co, unsigned char n)
{
  compiler_indent(co);
  compiler_comment_f_n(co, n);
  if (n > STATES_COUNT_HALF) {
    compiler_primitive_inc_n(co, -n);
  } else {
    for (size_t i = 0; i < n; i++)
      compiler_primitive_dec(co);
  }
  compiler_dedent(co);
}

static void compiler_primitive_inc_n(struct compiler *co, unsigned char n)
{
  compiler_indent(co);
  compiler_comment_f_n(co, n);
  if (n > STATES_COUNT_HALF) {
    compiler_primitive_dec_n(co, -n);
  } else {
    for (size_t i = 0; i < n; i++)
      compiler_primitive_inc(co);
  }
  compiler_dedent(co);
}

/* EXPLICIT POSITION */

static void compiler_move(struct compiler *co, size_t pos)
{
  compiler_indent(co);
  compiler_comment_f_v(co, pos);
  while (co->pos < pos)
    compiler_primitive_static_right(co);
  while (co->pos > pos)
    compiler_primitive_static_left(co);
  compiler_dedent(co);
}

static void compiler_while(struct compiler *co, size_t pos)
{
  compiler_move(co, pos);
  compiler_primitive_while(co);
}

static void compiler_end(struct compiler *co, size_t pos)
{
  compiler_move(co, pos);
  compiler_primitive_end(co);
}

static void compiler_output(struct compiler *co, size_t pos)
{
  compiler_move(co, pos);
  compiler_primitive_output(co);
}

static void compiler_input(struct compiler *co, size_t r)
{
  compiler_move(co, r);
  compiler_primitive_input(co);
}

static void compiler_clear(struct compiler *co, size_t r)
{
  compiler_move(co, r);
  compiler_primitive_clear(co);
}

static void compiler_clear_array(struct compiler *co, size_t r, size_t len)
{
  for (size_t i = 0; i < len; i++)
    compiler_clear(co, r + i);
}

static void compiler_dec(struct compiler *co, size_t r)
{
  compiler_indent(co);
  compiler_comment_f_v(co, r);
  compiler_move(co, r);
  compiler_primitive_dec(co);
  compiler_dedent(co);
}

static void compiler_inc(struct compiler *co, size_t r)
{
  compiler_indent(co);
  compiler_comment_f_v(co, r);
  compiler_move(co, r);
  compiler_primitive_inc(co);
  compiler_dedent(co);
}

static void compiler_dec_n(struct compiler *co, size_t r, unsigned char n)
{
  compiler_indent(co);
  compiler_comment_f_v(co, r);
  compiler_move(co, r);
  compiler_primitive_dec_n(co, n);
  compiler_dedent(co);
}

static void compiler_inc_n(struct compiler *co, size_t r, unsigned char n)
{
  compiler_indent(co);
  compiler_comment_f_v(co, r);
  compiler_move(co, r);
  compiler_primitive_inc_n(co, n);
  compiler_dedent(co);
}

static void compiler_set_n(struct compiler *co, size_t r, unsigned char n)
{
  compiler_indent(co);
  compiler_comment_f_v_n(co, r, n);
  compiler_clear(co, r);
  compiler_inc_n(co, r, n);
  compiler_dedent(co);
}

static void compiler_set_v(struct compiler *co, size_t r, size_t v)
{
  compiler_indent(co);
  compiler_comment_f_v_v(co, r, v);
  if (r != v) {
    size_t t = compiler_push(co);
    compiler_clear(co, t);
    compiler_clear(co, r);

    compiler_while(co, v);
    compiler_dec(co, v);
    compiler_inc(co, t);
    compiler_inc(co, r);
    compiler_end(co, v);

    compiler_while(co, t);
    compiler_dec(co, t);
    compiler_inc(co, v);
    compiler_end(co, t);

    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_dec_v(struct compiler *co, size_t r, size_t v)
{
  compiler_indent(co);
  compiler_comment_f_v_v(co, r, v);
  if (r == v) {
    compiler_clear(co, r);
  } else {
    size_t t = compiler_push(co);
    compiler_clear(co, t);

    compiler_while(co, v);
    compiler_dec(co, v);
    compiler_dec(co, r);
    compiler_inc(co, t);
    compiler_end(co, v);

    compiler_while(co, t);
    compiler_dec(co, t);
    compiler_inc(co, v);
    compiler_end(co, t);

    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_inc_v(struct compiler *co, size_t r, size_t v)
{
  compiler_indent(co);
  compiler_comment_f_v_v(co, r, v);
  size_t t = compiler_push(co);
  if (r == v) {
    compiler_set_v(co, t, r);
    compiler_inc_v(co, r, t);
  } else {
    compiler_clear(co, t);

    compiler_while(co, v);
    compiler_dec(co, v);
    compiler_inc(co, r);
    compiler_inc(co, t);
    compiler_end(co, v);

    compiler_while(co, t);
    compiler_dec(co, t);
    compiler_inc(co, v);
    compiler_end(co, t);
  }
  compiler_pop(co, t);
  compiler_dedent(co);
}

static void compiler_dec_if(struct compiler *co, size_t r, size_t v)
{
  assert(r != v);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_v(co, r, v);
  size_t t = compiler_push(co);
  compiler_set_v(co, t, v);
  compiler_while(co, t);
  compiler_dec(co, r);
  compiler_clear(co, t);
  compiler_end(co, t);
  compiler_pop(co, t);
  compiler_dedent(co);
}

static void compiler_inc_if(struct compiler *co, size_t r, size_t v)
{
  assert(r != v);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_v(co, r, v);
  size_t t = compiler_push(co);
  compiler_set_v(co, t, v);
  compiler_while(co, t);
  compiler_inc(co, r);
  compiler_clear(co, t);
  compiler_end(co, t);
  compiler_pop(co, t);
  compiler_dedent(co);
}

static void compiler_not(struct compiler *co, size_t r, size_t v)
{
  if (r == v) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, v);
    compiler_not(co, r, t);
    compiler_pop(co, t);
  } else {
    compiler_indent(co);
    compiler_comment_f_v_v(co, r, v);
    compiler_set_n(co, r, 1);
    compiler_dec_if(co, r, v);
    compiler_dedent(co);
  }
}

static void compiler_inc_if_not(struct compiler *co, size_t r, size_t v)
{
  assert(r != v);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_v(co, r, v);
  size_t t = compiler_push(co);
  compiler_not(co, t, v);
  compiler_inc_if(co, r, t);
  compiler_pop(co, t);
  compiler_dedent(co);
}

static void compiler_and(struct compiler *co, size_t r, size_t x, size_t y)
{
  assert(r != x);  /* LCOV_EXCL_LINE */
  assert(r != y);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_v_v(co, r, x, y);
  size_t t = compiler_push(co);
  compiler_set_n(co, t, 2);
  compiler_dec_if(co, t, x);
  compiler_dec_if(co, t, y);
  compiler_not(co, r, t);
  compiler_pop(co, t);
  compiler_dedent(co);
}

static void compiler_neq_vn(struct compiler *co, size_t r,
    size_t v, unsigned char n)
{
  compiler_set_v(co, r, v);
  compiler_dec_n(co, r, n);
}

static void compiler_neq_vv(struct compiler *co, size_t r, size_t x, size_t y)
{
  compiler_set_v(co, r, x);
  compiler_dec_v(co, r, y);
}

static void compiler_eq_vn(struct compiler *co, size_t r,
    size_t v, unsigned char n)
{
  compiler_neq_vn(co, r, v, n);
  compiler_not(co, r, r);
}

static void compiler_eq_vv(struct compiler *co, size_t r, size_t x, size_t y)
{
  compiler_neq_vv(co, r, x, y);
  compiler_not(co, r, r);
}

static void compiler_add_nn(struct compiler *co, size_t r,
    unsigned char n, unsigned char k)
{
  compiler_indent(co);
  compiler_comment_f_v_n_n(co, r, n, k);
  compiler_set_n(co, r, n + k);
  compiler_dedent(co);
}

static void compiler_add_vn(struct compiler *co, size_t r,
    size_t v, unsigned char n)
{
  compiler_indent(co);
  compiler_comment_f_v_v_n(co, r, v, n);
  compiler_set_v(co, r, v);
  compiler_inc_n(co, r, n);
  compiler_dedent(co);
}

static void compiler_add_vv(struct compiler *co, size_t r, size_t x, size_t y)
{
  compiler_indent(co);
  compiler_comment_f_v_v_v(co, r, x, y);
  if (r == x) {
    compiler_inc_v(co, r, y);
  } else if (r == y) {
    compiler_inc_v(co, r, x);
  } else {
    compiler_set_v(co, r, x);
    compiler_inc_v(co, r, y);
  }
  compiler_dedent(co);
}

static void compiler_sub_nn(struct compiler *co, size_t r,
    unsigned char n, unsigned char k)
{
  compiler_indent(co);
  compiler_comment_f_v_n_n(co, r, n, k);
  compiler_set_n(co, r, n - k);
  compiler_dedent(co);
}

static void compiler_sub_vn(struct compiler *co, size_t r,
    size_t v, unsigned char n)
{
  compiler_indent(co);
  compiler_comment_f_v_v_n(co, r, v, n);
  compiler_set_v(co, r, v);
  compiler_dec_n(co, r, n);
  compiler_dedent(co);
}

static void compiler_sub_nv(struct compiler *co, size_t r,
    unsigned char n, size_t v)
{
  compiler_indent(co);
  compiler_comment_f_v_n_v(co, r, n, v);
  if (r == v) {
    size_t t = compiler_push(co);
    compiler_set_n(co, t, n);
    compiler_dec_v(co, t, v);
    compiler_set_v(co, v, t);
    compiler_pop(co, t);
  } else {
    compiler_set_n(co, r, n);
    compiler_dec_v(co, r, v);
  }
  compiler_dedent(co);
}

static void compiler_sub_vv(struct compiler *co, size_t r, size_t x, size_t y)
{
  compiler_indent(co);
  compiler_comment_f_v_v_v(co, r, x, y);
  if (x == y) {
    compiler_clear(co, r);
  } else if (r == x) {
    compiler_dec_v(co, r, y);
  } else if (r == y) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, y);
    compiler_sub_vv(co, r, x, t);
    compiler_pop(co, t);
  } else {
    compiler_set_v(co, r, x);
    compiler_dec_v(co, r, y);
  }
  compiler_dedent(co);
}

static void compiler_mul_nn(struct compiler *co, size_t r,
    unsigned char n, unsigned char k)
{
  compiler_indent(co);
  compiler_comment_f_v_n_n(co, r, n, k);
  compiler_set_n(co, r, n * k);
  compiler_dedent(co);
}

static void compiler_mul_vv(struct compiler *co, size_t r, size_t x, size_t y)
{
  compiler_indent(co);
  compiler_comment_f_v_v_v(co, r, x, y);
  if (r == x) {
    size_t t = compiler_push(co);
    compiler_mul_vv(co, t, x, y);
    compiler_set_v(co, r, t);
    compiler_pop(co, t);
  } else if (r == y) {
    compiler_mul_vv(co, r, y, x);
  } else {
    compiler_clear(co, r);
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);

    compiler_while(co, t);
    compiler_dec(co, t);
    compiler_inc_v(co, r, y);
    compiler_end(co, t);

    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_mul_vn(struct compiler *co, size_t r,
    size_t v, unsigned char n)
{
  compiler_indent(co);
  compiler_comment_f_v_v_n(co, r, v, n);
  if (n == 0) {
    compiler_clear(co, r);
  } else if (n == 1) {
    compiler_set_v(co, r, v);
  } else {
    /* An expansion might be faster. */
    size_t t = compiler_push(co);
    compiler_set_n(co, t, n);
    compiler_mul_vv(co, r, v, t);
    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_cmp_nn(struct compiler *co, size_t r,
    unsigned char n, unsigned char k)
{
  compiler_indent(co);
  compiler_comment_f_v_n_n(co, r, n, k);
  if (n == k)
    compiler_clear(co, r);
  else if (n < k)
    compiler_set_n(co, r, -1);
  else
    compiler_set_n(co, r, 1);
  compiler_dedent(co);
}

static void compiler_cmp_vv(struct compiler *co, size_t r, size_t x, size_t y)
{
  compiler_indent(co);
  compiler_comment_f_v_v_v(co, r, x, y);
  if (x == y) {
    compiler_clear(co, r);
  } else if (r == x) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);
    compiler_cmp_vv(co, r, t, y);
    compiler_pop(co, t);
  } else if (r == y) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, y);
    compiler_cmp_vv(co, r, x, t);
    compiler_pop(co, t);
  } else {
    compiler_clear(co, r);

    size_t t = compiler_push(co);
    size_t tx = compiler_push(co);
    size_t ty = compiler_push(co);

    compiler_set_v(co, tx, x);
    compiler_set_v(co, ty, y);

    compiler_and(co, t, tx, ty);
    compiler_while(co, t);
    compiler_dec(co, tx);
    compiler_dec(co, ty);
    compiler_and(co, t, tx, ty);
    compiler_end(co, t);

    compiler_inc_if(co, r, tx);
    compiler_dec_if(co, r, ty);

    compiler_pop(co, ty);
    compiler_pop(co, tx);
    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_cmp_vn(struct compiler *co, size_t r,
    size_t v, unsigned char n)
{
  compiler_indent(co);
  compiler_comment_f_v_v_n(co, r, v, n);
  size_t t = compiler_push(co);
  compiler_set_n(co, t, n);
  compiler_cmp_vv(co, r, v, t);
  compiler_pop(co, t);
  compiler_dedent(co);
}

static void compiler_cmp_nv(struct compiler *co, size_t r,
    unsigned char n, size_t v)
{
  compiler_indent(co);
  compiler_comment_f_v_n_v(co, r, n, v);
  size_t t = compiler_push(co);
  compiler_set_n(co, t, n);
  compiler_cmp_vv(co, r, t, v);
  compiler_pop(co, t);
  compiler_dedent(co);
}

static void compiler_div_nn(struct compiler *co, size_t r,
    unsigned char n, unsigned char k)
{
  assert(k);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_n_n(co, r, n, k);
  compiler_set_n(co, r, n / k);
  compiler_dedent(co);
}

static void compiler_div_vv(struct compiler *co, size_t r, size_t x, size_t y)
{
  compiler_indent(co);
  compiler_comment_f_v_v_v(co, r, x, y);
  if (x == y) {
    compiler_set_n(co, r, 1);
  } else if (r == x) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);
    compiler_div_vv(co, r, t, y);
    compiler_pop(co, t);
  } else if (r == y){
    size_t t = compiler_push(co);
    compiler_set_v(co, t, y);
    compiler_div_vv(co, r, x, t);
    compiler_pop(co, t);
  } else {
    size_t tx = compiler_push(co);
    size_t ty = compiler_push(co);
    size_t t = compiler_push(co);

    compiler_clear(co, r);
    compiler_set_v(co, tx, x);

    compiler_set_v(co, ty, y);
    compiler_while(co, tx);

    compiler_and(co, t, tx, ty);
    compiler_while(co, t);
    compiler_dec(co, tx);
    compiler_dec(co, ty);

    compiler_and(co, t, tx, ty);
    compiler_end(co, t);

    compiler_inc_if_not(co, r, ty);
    compiler_set_v(co, ty, y);
    compiler_end(co, tx);

    compiler_pop(co, t);
    compiler_pop(co, ty);
    compiler_pop(co, tx);
  }
  compiler_dedent(co);
}

static void compiler_div_vn(struct compiler *co, size_t r,
    size_t v, unsigned char n)
{
  assert(n);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_v_n(co, r, v, n);
  if (n == 1) {
    compiler_set_v(co, r, v);
  } else {
    size_t t = compiler_push(co);
    compiler_set_n(co, t, n);
    compiler_div_vv(co, r, v, t);
    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_div_nv(struct compiler *co, size_t r,
    unsigned char n, size_t v)
{
  compiler_indent(co);
  compiler_comment_f_v_n_v(co, r, n, v);
  if (n == 0) {
    compiler_clear(co, r);
  } else {
    size_t t = compiler_push(co);
    compiler_set_n(co, t, n);
    compiler_div_vv(co, r, t, v);
    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_divmod_nn(struct compiler *co, size_t div, size_t mod,
    unsigned char n, unsigned char k)
{
  assert(div != mod);  /* LCOV_EXCL_LINE */
  assert(k);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_v_n_n(co, div, mod, n, k);
  compiler_set_n(co, div, n / k);
  compiler_set_n(co, mod, n % k);
  compiler_dedent(co);
}

static void compiler_divmod_vv(struct compiler *co, size_t div, size_t mod,
    size_t x, size_t y)
{
  assert(div != mod);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_v_v_v(co, div, mod, x, y);
  if (x == y) {
    compiler_set_n(co, div, 1);
    compiler_clear(co, mod);
  } else if (x == div || x == mod) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);
    compiler_divmod_vv(co, div, mod, t, y);
    compiler_pop(co, t);
  } else if (y == div || y == mod) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, y);
    compiler_divmod_vv(co, div, mod, x, t);
    compiler_pop(co, t);
  } else {
    /* fugly */
    compiler_div_vv(co, div, x, y);
    compiler_mul_vv(co, mod, div, y);
    compiler_sub_vv(co, mod, x, mod);
  }
  compiler_dedent(co);
}

static void compiler_divmod_vn(struct compiler *co, size_t div, size_t mod,
    size_t v, unsigned char n)
{
  assert(n);  /* LCOV_EXCL_LINE */
  assert(div != mod);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_v_v_n(co, div, mod, v, n);
  if (n == 1) {
    compiler_set_v(co, div, v);
    compiler_clear(co, mod);
  } else if (v == div || v == mod) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, v);
    compiler_divmod_vn(co, div, mod, t, n);
    compiler_pop(co, t);
  } else {
    size_t t = compiler_push(co);
    compiler_set_n(co, t, n);
    compiler_divmod_vv(co, div, mod, v, t);
    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_divmod_nv(struct compiler *co, size_t div, size_t mod,
    unsigned char n, size_t v)
{
  assert(div != mod);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_v_n_v(co, div, mod, n, v);
  if (n == 0) {
    compiler_clear(co, div);
    compiler_clear(co, mod);
  } else if (v == div || v == mod) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, v);
    compiler_divmod_nv(co, div, mod, n, t);
    compiler_pop(co, t);
  } else {
    size_t t = compiler_push(co);
    compiler_set_n(co, t, n);
    compiler_divmod_vv(co, div, mod, t, v);
    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_mod_nn(struct compiler *co, size_t r,
    unsigned char n, unsigned char k)
{
  assert(k);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_n_n(co, r, n, k);
  compiler_set_n(co, r, n % k);
  compiler_dedent(co);
}

static void compiler_mod_vv(struct compiler *co, size_t r, size_t x, size_t y)
{
  compiler_indent(co);
  compiler_comment_f_v_v_v(co, r, x, y);
  if (x == y) {
    compiler_clear(co, r);
  } else {
    size_t t = compiler_push(co);
    compiler_divmod_vv(co, t, r, x, y);
    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_mod_vn(struct compiler *co, size_t r,
    size_t v, unsigned char n)
{
  assert(n);  /* LCOV_EXCL_LINE */
  compiler_indent(co);
  compiler_comment_f_v_v_n(co, r, v, n);
  if (n == 1) {
    compiler_clear(co, r);
  } else {
    size_t t = compiler_push(co);
    compiler_set_n(co, t, n);
    compiler_mod_vv(co, r, v, t);
    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_mod_nv(struct compiler *co, size_t r,
    unsigned char n, size_t v)
{
  compiler_indent(co);
  compiler_comment_f_v_n_v(co, r, n, v);
  if (n == 0) {
    compiler_clear(co, r);
  } else {
    size_t t = compiler_push(co);
    compiler_set_n(co, t, n);
    compiler_mod_vv(co, r, t, v);
    compiler_pop(co, t);
  }
  compiler_dedent(co);
}

static void compiler_a2b_nnn(struct compiler *co, size_t r,
    unsigned char m, unsigned char n, unsigned char k) {
  compiler_set_n(co, r, 100 * m + 10 * n + k);
}

static void compiler_a2b_nnv(struct compiler *co, size_t r,
    unsigned char n, unsigned char k, size_t x)
{
  if (r == x) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);
    compiler_a2b_nnv(co, r, n, k, t);
    compiler_pop(co, t);
  } else {
    compiler_set_n(co, r, 100 * n + 10 *k);
    compiler_inc_v(co, r, x);
  }
}

static void compiler_a2b_nvn(struct compiler *co, size_t r,
    unsigned char n, size_t x, unsigned char k)
{
  if (r == x) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);
    compiler_a2b_nvn(co, r, n, t, k);
    compiler_pop(co, t);
  } else {
    compiler_mul_vn(co, r, x, 10);
    compiler_inc_n(co, r, 100 * n + k);
  }
}

static void compiler_a2b_nvv(struct compiler *co, size_t r,
    unsigned char n, size_t x, size_t y)
{
  if (r == x) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);
    compiler_a2b_nvv(co, r, n, t, y);
    compiler_pop(co, t);
  } else if (r == y) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, y);
    compiler_a2b_nvv(co, r, n, x, t);
    compiler_pop(co, t);
  } else {
    compiler_mul_vn(co, r, x, 10);
    compiler_inc_v(co, r, y);
    compiler_inc_n(co, r, 100 * n);
  }
}

static void compiler_a2b_vnn(struct compiler *co, size_t r,
    size_t x, unsigned char n, unsigned char k)
{
  if (r == x) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);
    compiler_a2b_vnn(co, r, t, n, k);
    compiler_pop(co, t);
  } else {
    compiler_mul_vn(co, r, x, 100);
    compiler_inc_n(co, r, 10 * n + k);
  }
}

static void compiler_a2b_vnv(struct compiler *co, size_t r,
    size_t x, unsigned char n, size_t y)
{
  if (r == x) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);
    compiler_a2b_vnv(co, r, t, n, y);
    compiler_pop(co, t);
  } else if (r == y) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, y);
    compiler_a2b_vnv(co, r, x, n, t);
    compiler_pop(co, t);
  } else {
    compiler_mul_vn(co, r, x, 100);
    compiler_inc_v(co, r, y);
    compiler_inc_n(co, r, 10 * n);
  }
}

static void compiler_a2b_vvn(struct compiler *co, size_t r,
    size_t x, size_t y, unsigned char n)
{
  if (r == x) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);
    compiler_a2b_vvn(co, r, t, y, n);
    compiler_pop(co, t);
  } else if (r == y) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, y);
    compiler_a2b_vvn(co, r, x, t, n);
    compiler_pop(co, t);
  } else {
    compiler_mul_vn(co, r, x, 10);
    compiler_inc_v(co, r, y);
    compiler_mul_vn(co, r, r, 10);
    compiler_inc_n(co, r, n);
  }
}

static void compiler_a2b_vvv(struct compiler *co, size_t r,
    size_t x, size_t y, size_t z)
{
  if (r == x) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, x);
    compiler_a2b_vvv(co, r, t, y, z);
    compiler_pop(co, t);
  } else if (r == y) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, y);
    compiler_a2b_vvv(co, r, x, t, z);
    compiler_pop(co, t);
  } else if (r == z) {
    size_t t = compiler_push(co);
    compiler_set_v(co, t, z);
    compiler_a2b_vvv(co, r, x, y, t);
    compiler_pop(co, t);
  } else {
    compiler_mul_vn(co, r, x, 10);
    compiler_inc_v(co, r, y);
    compiler_mul_vn(co, r, r, 10);
    compiler_inc_v(co, r, z);
  }
}

static void compiler_b2a_n(struct compiler *co,
    size_t p, size_t q, size_t r, unsigned char n)
{
  assert(p != q);  /* LCOV_EXCL_LINE */
  assert(p != r);  /* LCOV_EXCL_LINE */
  assert(q != r);  /* LCOV_EXCL_LINE */
  compiler_set_n(co, r, n % 10 + '0');
  n = n / 10;
  compiler_set_n(co, q, n % 10 + '0');
  n = n / 10;
  compiler_set_n(co, p, n + '0');
}

static void compiler_b2a_v(struct compiler *co,
    size_t p, size_t q, size_t r, size_t v)
{
  assert(p != q);  /* LCOV_EXCL_LINE */
  assert(p != r);  /* LCOV_EXCL_LINE */
  assert(q != r);  /* LCOV_EXCL_LINE */
  compiler_divmod_vn(co, q, r, v, 10);
  compiler_divmod_vn(co, p, q, q, 10);
  compiler_inc_n(co, p, '0');
  compiler_inc_n(co, q, '0');
  compiler_inc_n(co, r, '0');
}

static void compiler_lget_n(struct compiler *co, size_t lst, size_t len,
    unsigned char idx, size_t r)
{
  assert(idx < len);  /* LCOV_EXCL_LINE */
  compiler_set_v(co, r, lst + idx);
}

static void compiler_lget_v(struct compiler *co, size_t lst, size_t len,
    size_t idx, size_t r)
{
  /* lst[idx] == R */

  size_t sz = len + 3;
  size_t array = compiler_push_n(co, sz);
  size_t offset = array + 1 - lst;
  /* array == lst + offset - 1 */
  /* array + 1 == lst + offset */
  /* lst == array + 1 - offset */
  /* lst + offset == array + 1 */

  compiler_clear_array(co, array, sz);
  compiler_set_v(co, array + 1, idx);
  compiler_move(co, array);  /* sentinel */

  compiler_primitive_right(co);  /* > */
  /* lst + offset (idx) */
  compiler_primitive_while(co);  /* [ 1 */
  compiler_primitive_while(co);  /* [ 2 */
  compiler_primitive_dec(co);    /* - */
  compiler_primitive_right(co);  /* > */
  compiler_primitive_inc(co);    /* + */
  compiler_primitive_left(co);   /* < */
  compiler_primitive_end(co);    /* ] 2 */
  compiler_primitive_inc(co);    /* + keep 1 for return */
  compiler_primitive_right(co);  /* > */
  compiler_primitive_dec(co);    /* - */
  compiler_primitive_end(co);    /* ] 1 */
  /* lst + idx + offset */

  /* lst[idx + offset] == 0 */
  /* lst[idx + offset + 1] == 0 */
  /* lst[idx + offset + 2] == 0 */

  /* copy */
  compiler_primitive_left_n(co, offset);
  /* lst + idx */
  compiler_primitive_while(co);
  compiler_primitive_dec(co);
  compiler_primitive_right_n(co, offset + 1);
  /* lst + idx + offset + 1 */
  compiler_primitive_inc(co);
  compiler_primitive_right(co);
  /* lst + idx + offset + 2 */
  compiler_primitive_inc(co);
  compiler_primitive_left_n(co, offset + 2);
  /* lst + idx */
  compiler_primitive_end(co);
  /* lst + idx */

  /* lst[idx] == 0 */
  /* lst[idx + offset] == 0 */
  /* lst[idx + offset + 1] == R */
  /* lst[idx + offset + 2] == R */

  /* restore */
  compiler_primitive_right_n(co, offset + 2);
  /* lst + idx + offset + 2 */
  compiler_primitive_while(co);
  compiler_primitive_dec(co);
  compiler_primitive_left_n(co, offset + 2);
  /* lst + idx */
  compiler_primitive_inc(co);
  compiler_primitive_right_n(co, offset + 2);
  /* lst + idx + offset + 2 */
  compiler_primitive_end(co);

  /* lst[idx] == R */
  /* lst[idx + offset] == 0 */
  /* lst[idx + offset + 1] == R */
  /* lst[idx + offset + 2] == 0 */

  /* roll back */
  compiler_primitive_left_n(co, 3);
  /* lst + idx + offset - 1*/
  compiler_primitive_while(co);  /* [ 1 */
  compiler_primitive_dec(co);
  compiler_primitive_right_n(co, 2);
  compiler_primitive_while(co);  /* [ 2 */
  compiler_primitive_dec(co);
  compiler_primitive_left(co);
  compiler_primitive_inc(co);
  compiler_primitive_right(co);
  compiler_primitive_end(co);    /* ] 2 */
  compiler_primitive_left_n(co, 3);
  compiler_primitive_end(co);    /* ] 1 */

  compiler_set_v(co, r, array + 2);
  compiler_pop_n(co, array, sz);
}

static void compiler_lset_nn(struct compiler *co, size_t lst, size_t len,
    unsigned char idx, unsigned char val)
{
  assert(idx < len);  /* LCOV_EXCL_LINE */
  compiler_set_n(co, lst + idx, val);
}

static void compiler_lset_nv(struct compiler *co, size_t lst, size_t len,
    unsigned char idx, size_t val)
{
  assert(idx < len);  /* LCOV_EXCL_LINE */
  compiler_set_v(co, lst + idx, val);
}

static void compiler_lset_vn(struct compiler *co, size_t lst, size_t len,
    size_t idx, unsigned char val)
{
  size_t sz = len + 1;
  size_t array = compiler_push_n(co, sz);
  size_t offset = array + 1 - lst;
  compiler_clear_array(co, array, sz);
  compiler_set_v(co, array + 1, idx);
  compiler_move(co, array);  /* sentinel */

  /* roll */
  compiler_primitive_right(co);  /* > */
  compiler_primitive_while(co);  /* [ 1 */
  compiler_primitive_while(co);  /* [ 12 */
  compiler_primitive_dec(co);    /* - */
  compiler_primitive_right(co);  /* > */
  compiler_primitive_inc(co);    /* + */
  compiler_primitive_left(co);   /* < */
  compiler_primitive_end(co);    /* [ 12 */
  compiler_primitive_inc(co);    /* + keep 1 for return */
  compiler_primitive_right(co);  /* > */
  compiler_primitive_dec(co);    /* - */
  compiler_primitive_end(co);    /* ] 1 */

  /* set */
  compiler_primitive_left_n(co, offset);
  compiler_primitive_clear(co);
  compiler_primitive_inc_n(co, val);
  compiler_primitive_right_n(co, offset - 1);

  /* roll back */
  compiler_primitive_while(co);
  compiler_primitive_left(co);
  compiler_primitive_end(co);

  compiler_pop_n(co, array, sz);
}

static void compiler_lset_vv(struct compiler *co, size_t lst, size_t len,
    size_t idx, size_t v)
{
  size_t sz = len + 3;
  size_t array = compiler_push_n(co, sz);
  size_t offset = array + 2 - lst;
  /* array == lst + offset - 2 */
  /* array + 2 == lst + offset */
  /* lst == array + 2 - offset */
  /* lst + offset == array + 2 */

  compiler_clear_array(co, array, sz);
  compiler_set_v(co, array + 1, v);
  /* lst[offset - 1] == V */
  compiler_set_v(co, array + 2, idx);
  compiler_move(co, array);  /* sentinel */

  compiler_primitive_right(co);  /* > */
  compiler_primitive_right(co);  /* > */
  /* lst + offset */
  compiler_primitive_while(co);  /* [ 1 */
  compiler_primitive_while(co);  /* [ 2 */
  compiler_primitive_dec(co);    /* - */
  compiler_primitive_right(co);  /* > */
  compiler_primitive_inc(co);    /* + */
  compiler_primitive_left(co);   /* < */
  compiler_primitive_end(co);    /* ] 2 */
  compiler_primitive_left(co);   /* < */
  compiler_primitive_while(co);  /* [ 3 */
  compiler_primitive_dec(co);    /* - */
  compiler_primitive_right(co);  /* > */
  compiler_primitive_inc(co);    /* + */
  compiler_primitive_left(co);   /* < */
  compiler_primitive_end(co);    /* ] 3 */
  compiler_primitive_inc(co);    /* + keep 1 for return */
  compiler_primitive_right(co);  /* > */
  compiler_primitive_right(co);  /* > */
  compiler_primitive_dec(co);    /* - */
  compiler_primitive_end(co);    /* ] 1 */
  /* lst + idx + offset */

  /* lst[offset - 1] == 1 */
  /* lst[idx + offset - 1] == V */
  /* lst[idx + offset] == 0 */
  /* lst[idx + offset + 1] == 0 */

  /* set lst[idx] */
  compiler_primitive_left_n(co, offset);
  /* lst + idx */
  compiler_primitive_clear(co);
  compiler_primitive_right_n(co, offset - 1);
  /* lst + idx + offset - 1 */
  compiler_primitive_while(co);
  compiler_primitive_dec(co);
  compiler_primitive_right_n(co, 2);
  /* lst + idx + offset + 1 */
  compiler_primitive_inc(co);
  compiler_primitive_left_n(co, offset + 1);
  /* lst + idx */
  compiler_primitive_inc(co);
  compiler_primitive_right_n(co, offset - 1);
  /* lst + idx + offset - 1 */
  compiler_primitive_end(co);

  /* lst[idx] == V */
  /* lst[idx + offset - 1] == 0 */
  /* lst[idx + offset] == 0 */
  /* lst[idx + offset + 1] == V */

  /* restore lst[idx + offset] */
  compiler_primitive_right_n(co, 2);
  /* lst + idx + offset + 1 */
  compiler_primitive_while(co);
  compiler_primitive_dec(co);
  compiler_primitive_left(co);
  /* lst + idx + offset */
  compiler_primitive_inc(co);
  compiler_primitive_right(co);
  /* lst + idx + offset + 1 */
  compiler_primitive_end(co);

  compiler_primitive_left_n(co, 3);
  /* lst + idx + offset + -2 */
  compiler_primitive_while(co);
  compiler_primitive_left(co);
  compiler_primitive_end(co);

  compiler_pop_n(co, array, sz);
}

/** AST-DEPENDENT **/

static void compiler_print_arg(struct compiler *co, struct node *node)
{
  if (node->type == NODE_NUMBER) {
    compiler_comment(co, " %hhu", node->num);
  } else if (node->type == NODE_VAR_NAME) {
    compiler_comment(co, " %s", node->string);
  } else if (node->type == NODE_VAR_SINGLE) {
    compiler_comment(co, " %s", node->string);
    if (node->child) {
      int size = node->child->num + 1;
      compiler_comment(co, "[%d]", size);
    }
  } else {
    assert(node->type == NODE_STRING);  /* LCOV_EXCL_LINE */
    compiler_comment(co, " \"%s\"", node->string);
  }

}

static void compiler_print_arg_last(struct compiler *co, struct node *node)
{
  compiler_print_arg(co, node);
  compiler_comment(co, "\n");
}

static int compiler_find_list(struct compiler *co, struct node *node)
{
  assert(node->type == NODE_VAR_NAME);  /* LCOV_EXCL_LINE */
  for (struct node *n = co->globals; n; n = n->nextvar) {
    if (n->defined && strcmp(n->string, node->string) == 0) {
      if (!n->child) {
        fprintf(stderr, "Not a list: %s\n",
            node->string);
        return NOT_A_LIST;
      }
      node->pos = n->pos;
      node->len = n->len;
      return 0;
    }
  }
  fprintf(stderr, "Undefined variable: %s\n", node->string);
  return UNDEFINED_VARIABALE;
}

static int compiler_init_list(struct compiler *co, struct node *node)
{
  assert(node->type == NODE_VAR_NAME);  /* LCOV_EXCL_LINE */
  return compiler_find_list(co, node);
}

static int compiler_find_var(struct compiler *co, struct node *node)
{
  assert(node->type == NODE_VAR_NAME);  /* LCOV_EXCL_LINE */
  for (struct node *n = node->locals; n; n = n->nextvar) {
    if (strcmp(n->string, node->string) == 0) {
      node->pos = n->pos;
      return 0;
    }
  }
  for (struct node *n = co->globals; n; n = n->nextvar) {
    if (n->defined && strcmp(n->string, node->string) == 0) {
      if (n->child) {
        fprintf(stderr, "Not a scalar: %s\n",
            node->string);
        return NOT_A_SCALAR;
      }
      node->pos = n->pos;
      return 0;
    }
  }
  fprintf(stderr, "Undefined variable: %s\n", node->string);
  return UNDEFINED_VARIABALE;
}

static int compiler_init_var(struct compiler *co, struct node *node)
{
  if (node->type != NODE_VAR_NAME)
    return 0;
  node->locals = node->parent->locals;
  return compiler_find_var(co, node);
}

static struct node *compiler_find_proc(struct compiler *co, const char *s)
{
  for (struct node *n = co->procedures; n; n = n->nextvar)
    if (strcmp(n->child->string, s) == 0)
      return n;
  return NULL;
}

static int compile_node_msg_string(struct compiler *co, struct node *node)
{
  assert(node->type == NODE_STRING);  /* LCOV_EXCL_LINE */
  compiler_print_arg(co, node);
  if (!*node->string)
    return 0;

  size_t t = compiler_push(co);
  compiler_set_n(co, t, *node->string);
  compiler_output(co, t);
  for (char *s = node->string; s[1]; s++) {
    compiler_inc_n(co, t, s[1] - s[0]);
    compiler_output(co, t);
  }
  compiler_pop(co, t);
  return 0;
}

static int compile_node_msg_var(struct compiler *co, struct node *var)
{
  assert(var->type == NODE_VAR_NAME);  /* LCOV_EXCL_LINE */
  compiler_print_arg(co, var);

  int err = compiler_init_var(co, var);
  if (err)
    return err;

  compiler_output(co, var->pos);
  return 0;
}

static int compiler_register_var_single(struct compiler *co, struct node *node)
{
  assert(node->type == NODE_VAR_SINGLE);  /* LCOV_EXCL_LINE */
  node->len = node->child ? node->child->num + 1 : 1;
  compiler_push_n(co, node->len);
  size_t pos = compiler_globals_start(co);
  struct node *s = co->globals;

  for (struct node *n = s; n; s = n, n = n->nextvar) {
    if (strcmp(node->string, n->string) == 0) {
      fprintf(stderr, "Duplicate variable: %s\n",
          node->string);
      return DUPLICATE_VARIABLE;
    }
    pos += n->len;
  }

  if (s)
    s->nextvar = node;
  else
    co->globals = node;

  node->pos = pos;
  node->defined = 0;
  node->nextvar = NULL;
  compiler_indent(co);
  compiler_comment_indented(co, "%zd %s\n", node->pos, node->string);
  compiler_dedent(co);
  return 0;
}

static int compiler_register_var(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_VAR);  /* LCOV_EXCL_LINE */
  int err = 0;
  for (struct node *c = node->child; c && !err; c = c->next)
    err = compiler_register_var_single(co, c);
  return err;
}

static int compiler_register_globals(struct compiler *co, struct node *node)
{
  assert(node->type == NODE_PROGRAM);  /* LCOV_EXCL_LINE */
  for (struct node *c = node->child; c; c = c->next) {
    assert(c->type == NODE_STATEMENT);  /* LCOV_EXCL_LINE */
    if (c->inst != I_VAR)
      continue;
    int err = compiler_register_var(co, c);
    if (err)
      return err;
  }
  compiler_indent(co);
  compiler_comment_indented(co, "\nglobals_size: %zd", co->top);
  compiler_dedent(co);
  return 0;
}

static int compiler_register_proc(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_PROC);  /* LCOV_EXCL_LINE */
  assert(node->child);  /* LCOV_EXCL_LINE */
  struct node *s = co->procedures;
  struct node *name = node->child;

  for (struct node *n = s; n; s = n, n = n->nextvar) {
    if (strcmp(name->string, n->child->string) == 0) {
      fprintf(stderr, "Duplicate proc: %s\n", name->string);
      return DUPLICATE_PROCEDURE;
    }
  }

  if (s)
    s->nextvar = node;
  else
    co->procedures = node;

  node->nextvar = NULL;
  compiler_indent(co);
  compiler_comment_indented(co, "%s", node->string);
  compiler_dedent(co);
  return 0;
}

static int compiler_register_procedures(struct compiler *co, struct node *node)
{
  assert(node->type == NODE_PROGRAM);  /* LCOV_EXCL_LINE */
  for (struct node *c = node->child; c; c = c->next) {
    assert(c->type == NODE_STATEMENT);  /* LCOV_EXCL_LINE */
    if (c->inst != I_PROC)
      continue;
    int err = compiler_register_proc(co, c);
    if (err)
      return err;
  }
  return 0;
}

static void compiler_mark_globals_defined(struct compiler *co,
    struct node *node)
{
  assert_is_instruction(node, I_VAR);  /* LCOV_EXCL_LINE */
  for (struct node *c = node->child; c; c = c->next) {
    c->defined = 1;
    compiler_print_arg(co, c);
  }
}

/* TERMINAL STATEMENTS */

static int compile_node_a2b(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_A2B);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *b = a->next;
  struct node *c = b->next;
  struct node *r = c->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, b)))
    return err;
  if ((err = compiler_init_var(co, c)))
    return err;
  if ((err = compiler_init_var(co, r)))
    return err;

  compiler_print_arg(co, a);
  compiler_print_arg(co, b);
  compiler_print_arg(co, c);
  compiler_print_arg_last(co, r);

  switch (a->type) {
  case NODE_NUMBER:
    switch (b->type) {
    case NODE_NUMBER:
      switch (c->type) {
      case NODE_NUMBER:
        compiler_a2b_nnn(co, r->pos,
            a->num, b->num, c->num);
        break;
      default:
        compiler_a2b_nnv(co, r->pos,
            a->num, b->num, c->pos);
        break;
      }
      break;
    default:
      switch (c->type) {
      case NODE_NUMBER:
        compiler_a2b_nvn(co, r->pos,
            a->num, b->pos, c->num);
        break;
      default:
        compiler_a2b_nvv(co, r->pos,
            a->num, b->pos, c->pos);
        break;
      }
      break;
    }
    break;
  default:
    switch (b->type) {
    case NODE_NUMBER:
      switch (c->type) {
      case NODE_NUMBER:
        compiler_a2b_vnn(co, r->pos,
            a->pos, b->num, c->num);
        break;
      default:
        compiler_a2b_vnv(co, r->pos,
            a->pos, b->num, c->pos);
      }
      break;
    default:
      switch (c->type) {
      case NODE_NUMBER:
        compiler_a2b_vvn(co, r->pos,
            a->pos, b->pos, c->num);
        break;
      default:
        compiler_a2b_vvv(co, r->pos,
            a->pos, b->pos, c->pos);
        break;
      }
      break;
      break;
    }
    break;
  }
  compiler_inc_n(co, r->pos, 48);
  return 0;
}

static int compile_node_add(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_ADD);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *b = a->next;
  struct node *r = b->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, b)))
    return err;
  if ((err = compiler_init_var(co, r)))
    return err;

  compiler_print_arg(co, a);
  compiler_print_arg(co, b);
  compiler_print_arg_last(co, r);

  if (a->type == NODE_NUMBER && b->type == NODE_NUMBER) {
    compiler_add_nn(co, r->pos, a->num, b->num);
  } else if (a->type == NODE_VAR_NAME && b->type == NODE_VAR_NAME) {
    compiler_add_vv(co, r->pos, a->pos, b->pos);
  } else if (a->type == NODE_VAR_NAME) {
    compiler_add_vn(co, r->pos, a->pos, b->num);
  } else {
    compiler_add_vn(co, r->pos, b->pos, a->num);
  }
  return 0;
}

static int compile_node_b2a(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_B2A);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *p = a->next;
  struct node *q = p->next;
  struct node *r = q->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, p)))
    return err;
  if ((err = compiler_init_var(co, q)))
    return err;
  if ((err = compiler_init_var(co, r)))
    return err;

  compiler_print_arg(co, a);
  compiler_print_arg(co, p);
  compiler_print_arg(co, q);
  compiler_print_arg_last(co, r);
  if (a->type == NODE_NUMBER)
    compiler_b2a_n(co, p->pos, q->pos, r->pos, a->num);
  else
    compiler_b2a_v(co, p->pos, q->pos, r->pos, a->pos);
  return 0;
}

static int compile_node_cmp(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_CMP);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *b = a->next;
  struct node *r = b->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, b)))
    return err;
  if ((err = compiler_init_var(co, r)))
    return err;

  compiler_print_arg(co, a);
  compiler_print_arg(co, b);
  compiler_print_arg_last(co, r);

  if (a->type == NODE_NUMBER && b->type == NODE_NUMBER) {
    compiler_cmp_nn(co, r->pos, a->num, b->num);
  } else if (a->type == NODE_VAR_NAME && b->type == NODE_VAR_NAME) {
    compiler_cmp_vv(co, r->pos, a->pos, b->pos);
  } else if (a->type == NODE_VAR_NAME) {
    assert(b->type == NODE_NUMBER);  /* LCOV_EXCL_LINE */
    compiler_cmp_vn(co, r->pos, a->pos, b->num);
  } else {
    assert(a->type == NODE_NUMBER);  /* LCOV_EXCL_LINE */
    assert(b->type == NODE_VAR_NAME);  /* LCOV_EXCL_LINE */
    compiler_cmp_nv(co, r->pos, a->num, b->pos);
  }
  return 0;
}

static int compile_node_dec(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_DEC);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *b = a->next;

  compiler_print_arg(co, a);
  compiler_print_arg_last(co, b);

  int err = compiler_init_var(co, a);
  if (err)
    return err;

  if (b->type == NODE_NUMBER) {
    compiler_dec_n(co, a->pos, b->num);
    return 0;
  }

  assert(b->type == NODE_VAR_NAME);  /* LCOV_EXCL_LINE */
  if ((err = compiler_init_var(co, b)))
    return err;

  compiler_dec_v(co, a->pos, b->pos);
  return 0;
}

static int compile_node_div(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_DIV);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *b = a->next;
  struct node *r = b->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, b)))
    return err;
  if ((err = compiler_init_var(co, r)))
    return err;

  compiler_print_arg(co, a);
  compiler_print_arg(co, b);
  compiler_print_arg_last(co, r);

  if (a->type == NODE_NUMBER && b->type == NODE_NUMBER) {
    compiler_div_nn(co, r->pos, a->num, b->num);
  } else if (a->type == NODE_VAR_NAME && b->type == NODE_VAR_NAME) {
    compiler_div_vv(co, r->pos, a->pos, b->pos);
  } else if (a->type == NODE_VAR_NAME) {
    compiler_div_vn(co, r->pos, a->pos, b->num);
  } else {
    compiler_div_nv(co, r->pos, a->num, b->pos);
  }
  return 0;
}

static int compile_node_divmod(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_DIVMOD);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *b = a->next;
  struct node *q = b->next;
  struct node *r = q->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, b)))
    return err;
  if ((err = compiler_init_var(co, q)))
    return err;
  if ((err = compiler_init_var(co, r)))
    return err;

  compiler_print_arg(co, a);
  compiler_print_arg(co, b);
  compiler_print_arg_last(co, r);

  if (a->type == NODE_NUMBER && b->type == NODE_NUMBER) {
    compiler_divmod_nn(co, q->pos, r->pos, a->num, b->num);
  } else if (a->type == NODE_VAR_NAME && b->type == NODE_VAR_NAME) {
    compiler_divmod_vv(co, q->pos, r->pos, a->pos, b->pos);
  } else if (a->type == NODE_VAR_NAME) {
    compiler_divmod_vn(co, q->pos, r->pos, a->pos, b->num);
  } else {
    compiler_divmod_nv(co, q->pos, r->pos, a->num, b->pos);
  }
  return 0;
}

static int compile_node_inc(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_INC);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *b = a->next;

  compiler_print_arg(co, a);
  compiler_print_arg_last(co, b);

  int err = compiler_init_var(co, a);
  if (err)
    return err;

  if (b->type == NODE_NUMBER) {
    compiler_inc_n(co, a->pos, b->num);
    return 0;
  }

  if ((err = compiler_init_var(co, b)))
    return err;

  compiler_inc_v(co, a->pos, b->pos);
  return 0;
}

static int compile_node_lget(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_LGET);  /* LCOV_EXCL_LINE */
  struct node *lst = node->child;
  struct node *idx = lst->next;
  struct node *r = idx->next;

  int err;
  if ((err = compiler_init_list(co, lst)))
    return err;
  if ((err = compiler_init_var(co, idx)))
    return err;
  if ((err = compiler_init_var(co, r)))
    return err;

  compiler_print_arg(co, lst);
  compiler_print_arg(co, idx);
  compiler_print_arg_last(co, r);

  if (idx->type == NODE_NUMBER)
    compiler_lget_n(co, lst->pos, lst->len, idx->num, r->pos);
  else
    compiler_lget_v(co, lst->pos, lst->len, idx->pos, r->pos);
  return 0;
}

static int compile_node_lset(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_LSET);  /* LCOV_EXCL_LINE */
  struct node *lst = node->child;
  struct node *idx = lst->next;
  struct node *val = idx->next;

  int err;
  if ((err = compiler_init_list(co, lst)))
    return err;
  if ((err = compiler_init_var(co, idx)))
    return err;
  if ((err = compiler_init_var(co, val)))
    return err;

  compiler_print_arg(co, lst);
  compiler_print_arg(co, idx);
  compiler_print_arg_last(co, val);

  switch (idx->type) {
  case NODE_NUMBER:
    switch(val->type) {
    case NODE_NUMBER:
      compiler_lset_nn(co, lst->pos, lst->len,
          idx->num, val->num);
      break;
    default:
      compiler_lset_nv(co, lst->pos, lst->len,
          idx->num, val->pos);
      break;
    }
    break;
  default:
    switch(val->type) {
    case NODE_NUMBER:
      compiler_lset_vn(co, lst->pos, lst->len,
          idx->pos, val->num);
      break;
    default:
      compiler_lset_vv(co, lst->pos, lst->len,
          idx->pos, val->pos);
      break;
    }
    break;
  }
  return 0;
}

static int compile_node_mod(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_MOD);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *b = a->next;
  struct node *r = b->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, b)))
    return err;
  if ((err = compiler_init_var(co, r)))
    return err;

  compiler_print_arg(co, a);
  compiler_print_arg(co, b);
  compiler_print_arg_last(co, r);

  if (a->type == NODE_NUMBER && b->type == NODE_NUMBER) {
    compiler_mod_nn(co, r->pos, a->num, b->num);
  } else if (a->type == NODE_VAR_NAME && b->type == NODE_VAR_NAME) {
    compiler_mod_vv(co, r->pos, a->pos, b->pos);
  } else if (a->type == NODE_VAR_NAME) {
    compiler_mod_vn(co, r->pos, a->pos, b->num);
  } else {
    compiler_mod_nv(co, r->pos, a->num, b->pos);
  }
  return 0;
}

static int compile_node_msg(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_MSG);  /* LCOV_EXCL_LINE */
  int err = 0;
  for (struct node *a = node->child; a && !err; a = a->next) {
    if (a->type == NODE_STRING)
      err = compile_node_msg_string(co, a);
    else
      err = compile_node_msg_var(co, a);
  }
  return err;
}

static int compile_node_mul(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_MUL);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *b = a->next;
  struct node *r = b->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, b)))
    return err;
  if ((err = compiler_init_var(co, r)))
    return err;

  compiler_print_arg(co, a);
  compiler_print_arg(co, b);
  compiler_print_arg_last(co, r);

  if (a->type == NODE_NUMBER && b->type == NODE_NUMBER) {
    compiler_mul_nn(co, r->pos, a->num, b->num);
  } else if (a->type == NODE_VAR_NAME && b->type == NODE_VAR_NAME) {
    compiler_mul_vv(co, r->pos, a->pos, b->pos);
  } else if (a->type == NODE_VAR_NAME) {
    compiler_mul_vn(co, r->pos, a->pos, b->num);
  } else {
    compiler_mul_vn(co, r->pos, b->pos, a->num);
  }
  return 0;
}

static int compile_node_read(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_READ);  /* LCOV_EXCL_LINE */
  struct node *var = node->child;
  compiler_print_arg_last(co, var);
  int err = compiler_init_var(co, var);
  if (err)
    return err;
  compiler_input(co, var->pos);
  return 0;
}

static int compile_node_set(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_SET);  /* LCOV_EXCL_LINE */

  struct node *a = node->child;
  struct node *b = a->next;

  compiler_print_arg(co, a);
  compiler_print_arg_last(co, b);

  assert(a->type == NODE_VAR_NAME);  /* LCOV_EXCL_LINE */

  int err = compiler_init_var(co, a);
  if (err)
    return err;

  switch (b->type) {
  case NODE_NUMBER:
    compiler_set_n(co, a->pos, b->num);
    return 0;
  default:
    if ((err = compiler_init_var(co, b)))
      return err;

    if (a->pos == b->pos)
      return 0;

    compiler_set_v(co, a->pos, b->pos);
    return 0;
  }
}

static int compile_node_sub(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_SUB);  /* LCOV_EXCL_LINE */
  struct node *a = node->child;
  struct node *b = a->next;
  struct node *r = b->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, b)))
    return err;
  if ((err = compiler_init_var(co, r)))
    return err;

  compiler_print_arg(co, a);
  compiler_print_arg(co, b);
  compiler_print_arg_last(co, r);

  if (a->type == NODE_NUMBER && b->type == NODE_NUMBER) {
    compiler_sub_nn(co, r->pos, a->num, b->num);
  } else if (a->type == NODE_VAR_NAME && b->type == NODE_VAR_NAME) {
    compiler_sub_vv(co, r->pos, a->pos, b->pos);
  } else if (a->type == NODE_VAR_NAME) {
    compiler_sub_vn(co, r->pos, a->pos, b->num);
  } else {
    compiler_sub_nv(co, r->pos, a->num, b->pos);
  }
  return 0;
}

/* NON-TERMINAL STATEMENTS */

static int compile_node_statement(struct compiler *co, struct node *node);

static int compile_block(struct compiler *co,
    struct node *statements)
{
  struct node *n = statements;
  for (; n; n = n->next) {
    if (node_is_instruction(n, I_END))
      break;
    int err = compile_node_statement(co, n);
    if (err)
      return err;
  }

  if (!n)
    return MISSING_END;

  return 0;
}

typedef void CompileConditionVN(struct compiler *co, size_t r,
    size_t v, unsigned char n);

typedef void CompileConditionVV(struct compiler *co, size_t r,
    size_t x, size_t y);

static int compile_node_if(struct compiler *co, struct node *node,
    CompileConditionVN cc_vn, CompileConditionVV cc_vv)
{
  struct node *a = node->child;
  struct node *b = a->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, b)))
    return err;

  size_t t = compiler_push(co);
  if (b->type == NODE_NUMBER)
    cc_vn(co, t, a->pos, b->num);
  else
    cc_vv(co, t, a->pos, b->pos);

  compiler_while(co, t);
  if ((err = compile_block(co, b->next)))
    return err;

  compiler_clear(co, t);
  compiler_end(co, t);
  compiler_pop(co, t);
  return 0;
}

static int compile_node_ifeq(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_IFEQ);  /* LCOV_EXCL_LINE */
  return compile_node_if(co, node, compiler_eq_vn, compiler_eq_vv);
}

static int compile_node_ifneq(struct compiler *co, struct node *node)
{
  assert_is_instruction(node, I_IFNEQ);  /* LCOV_EXCL_LINE */
  return compile_node_if(co, node, compiler_neq_vn, compiler_neq_vv);
}

static int compile_node_wneq(struct compiler *co, struct node *node)
{
  struct node *a = node->child;
  struct node *b = a->next;

  int err;
  if ((err = compiler_init_var(co, a)))
    return err;
  if ((err = compiler_init_var(co, b)))
    return err;

  size_t t = compiler_push(co);
  if (b->type == NODE_NUMBER)
    compiler_neq_vn(co, t, a->pos, b->num);
  else
    compiler_neq_vv(co, t, a->pos, b->pos);

  compiler_while(co, t);
  if ((err = compile_block(co, b->next)))
    return err;

  if (b->type == NODE_NUMBER)
    compiler_neq_vn(co, t, a->pos, b->num);
  else
    compiler_neq_vv(co, t, a->pos, b->pos);
  compiler_end(co, t);

  compiler_pop(co, t);
  return 0;
}

static int compile_node_call(struct compiler *co, struct node *call)
{
  assert_is_instruction(call, I_CALL);  /* LCOV_EXCL_LINE */
  int err;

  if ((err = compiler_call_insert(co, call))) {
    return err;
  }

  struct node *proc = compiler_find_proc(co, call->child->string);
  if (!proc)
    return UNDEFINED_PROCEDURE;

  assert_is_instruction(proc, I_PROC);  /* LCOV_EXCL_LINE */
  struct node *p = proc->child->next;
  struct node *c = call->child->next;
  while (c && p->type == NODE_VAR_NAME) {
    c->locals = call->locals;
    if ((err = compiler_find_var(co, c)))
      return err;
    node_locals_insert(proc, p);
    p->pos = c->pos;
    p = p->next;
    c = c->next;
  }

  if (c)
    return TOO_MUCH_PARAMETERS;

  if (p->type != NODE_STATEMENT)
    return TOO_FEW_PARAMETERS;

  if ((err = compile_block(co, p)))
    return err;

  while (proc->locals)
    node_locals_pop(proc);

  compiler_call_pop(co);
  return 0;
}

static int compile_node_statement(struct compiler *co, struct node *node)
{
  assert(node->type == NODE_STATEMENT);  /* LCOV_EXCL_LINE */
  node->locals = node->parent->locals;
  compiler_comment(co, "\n%s", instruction_to_string(node->inst));
  switch (node->inst) {  /* LCOV_EXCL_LINE */
  case I_A2B:
    return compile_node_a2b(co, node);
  case I_ADD:
    return compile_node_add(co, node);
  case I_B2A:
    return compile_node_b2a(co, node);
  case I_CALL:
    return compile_node_call(co, node);
  case I_CMP:
    return compile_node_cmp(co, node);
  case I_DEC:
    return compile_node_dec(co, node);
  case I_DIV:
    return compile_node_div(co, node);
  case I_DIVMOD:
    return compile_node_divmod(co, node);
  case I_IFEQ:
    return compile_node_ifeq(co, node);
  case I_IFNEQ:
    return compile_node_ifneq(co, node);
  case I_INC:
    return compile_node_inc(co, node);
  case I_LGET:
    return compile_node_lget(co, node);
  case I_LSET:
    return compile_node_lset(co, node);
  case I_MOD:
    return compile_node_mod(co, node);
  case I_MSG:
    return compile_node_msg(co, node);
  case I_MUL:
    return compile_node_mul(co, node);
  case I_PROC:
    return 0;
  case I_READ:
    return compile_node_read(co, node);
  case I_SET:
    return compile_node_set(co, node);
  case I_SUB:
    return compile_node_sub(co, node);
  case I_VAR:
    compiler_mark_globals_defined(co, node);
    return 0;
  case I_WNEQ:
    return compile_node_wneq(co, node);
  default:  /* LCOV_EXCL_LINE */
    bug("missing handler");  /* LCOV_EXCL_LINE */
  }
}

static int compile_node_program(struct compiler *co, struct node *node)
{
  assert(node->type == NODE_PROGRAM);  /* LCOV_EXCL_LINE */
  int err;
  if ((err = compiler_register_globals(co, node)))
    return err;
  if ((err = compiler_register_procedures(co, node)))
    return err;
  size_t globals_size = co->top;
  for (struct node *c = node->child; c; c = c->next) {
    if ((err = compile_node_statement(co, c)))
      return err;
    assert(co->top == globals_size);  /* LCOV_EXCL_LINE */
    assert(co->indent == 0);  /* LCOV_EXCL_LINE */
    assert(co->block == 0);  /* LCOV_EXCL_LINE */
    assert(!co->calls);  /* LCOV_EXCL_LINE */
  }
  assert(co->top == globals_size);  /* LCOV_EXCL_LINE */
  return 0;
}

static int compiler_compile(struct compiler *co)
{
  assert(co->ast);  /* LCOV_EXCL_LINE */
  return compile_node_program(co, co->ast->root);
}

/* KCUF */

int kcuf(char **output, const char *code)
{
  int err;
  *output = NULL;

  struct tokens tokens;
  tokens_init(&tokens, code);

  struct scanner scanner;
  scanner_init(&scanner, code, &tokens);
  scanner_scan(&scanner);
  if ((err = scanner.error))
    goto cleanup_scanner;

  struct ast ast;
  ast_init(&ast, &tokens);

  struct parser parser;
  parser_init(&parser, tokens.items, &ast);
  if ((err = parser_parse(&parser)))
    goto cleanup_parser;

  struct strbuf brainfuck;
  strbuf_init(&brainfuck);

  struct compiler compiler;
  compiler_init(&compiler, &ast, &brainfuck);
  compiler_comment(&compiler, "CODE BEGIN\n%s\nCODE_END\n", code);
  if ((err = compiler_compile(&compiler)))
    goto cleanup_compiler;

  *output = strdup(brainfuck.s);

cleanup_compiler:
  compiler_destroy(&compiler);
  strbuf_destroy(&brainfuck);
cleanup_parser:
  parser_destroy(&parser);
  ast_destroy(&ast);
cleanup_scanner:
  scanner_destroy(&scanner);
  tokens_destroy(&tokens);
  return err;
}
