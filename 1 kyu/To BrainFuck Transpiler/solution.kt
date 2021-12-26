#include <tuple>
using namespace std;

int cp=0; int ap=0; string bf; size_t line=0; int cx=0;
unordered_map<string,size_t> vars; //variables
unordered_map<string,size_t> cmds; // map of commands functios
unordered_map<string,size_t> currprocs; // current procs to track recursion
unordered_map<string,size_t> lists; // lists list
unordered_map<string,size_t>::iterator it; 

unordered_map<string,pair<size_t,int>> consts;  // constants
unordered_map<string,pair<size_t,int>>::iterator itc; 

unordered_map<string,string> pv;  // procedures variables to (to change name and avoid global conflict)
unordered_map<string,string>::iterator itv;

unordered_map<string,pair<size_t,size_t>> procs; // procs names, initial point and parameters number
unordered_map<string,pair<size_t,size_t>>::iterator itp;

vector<tuple<string,int, int,int,string>> ret;  // return type, return line, pointer position before and after ennding code, ending code
vector<vector<string>> scv; // tokenized code

typedef void (*pfunc)(vector<string>);
unordered_map<string, pfunc> fMap; 
unordered_map<string, pfunc>::iterator itf; 


bool isConstant(string str){
  return (str[0]=='\'' || str[0]=='-' || (str[0]>='0' && str[0]<='9'));
}
int bfMove(int des){
  if (cp==des) return cp;
  char c='<';
  if (cp<des) c='>';
  bf+=string(abs(des-cp),c);
  cp=des;
  return cp; 
}
int val(string s){
  if(s[0]=='-' || isdigit(s[0]) || s[0]=='\''){
    return consts[s].first;
  } else {
    it=vars.find(s);
    if(it==vars.end()) throw "Undefined var "+s ;
    return it->second;
  }
}
pair<size_t,int> val3(string s){
  int t;
  bfMove(ap++);
  if(s[0]=='-' || isdigit(s[0])){
    t=(stoi(s)%256+256)%256;
  } 
  else {
    if(s.size()==3){
      t=(int)s[1];
    } 
    else{
      switch(s[2]){
        case 'n': t='\n';  break;  case 'r': t='\r';  break; // this is not tested but anyway is here
        case 't': t='\t';  break;  case '\\': t='\\'; break;
        case '\'': t='\''; break;  case '"' : t='"';  break;
      }
    }
  } 
  bf+="[-]"+string(t,'+');
  return make_pair(cp,t);
}
void bfSet(int x,int y){
  if (x==y) return;
  int t0=ap++;
  bfMove(t0); bf+="[-]";  bfMove(x); bf+="[-]"; bfMove(y); bf+="["; bfMove(x); bf+="+";
  bfMove(t0); bf+="+"; bfMove(y); bf+="-]"; bfMove(t0); bf+="[-"; bfMove(y); bf+="+";
  bfMove(t0); bf+="]";
}
void bfInc(int x, int y){
  int t0=ap++;
  bfMove(t0); bf+="[-]";  bfMove(y); bf+="["; bfMove(x); bf+="+";
  bfMove(t0); bf+="+"; bfMove(y); bf+="-]"; bfMove(t0); bf+="[-"; bfMove(y); bf+="+";
  bfMove(t0); bf+="]";
}
void bfDec(int x, int y){
  int t0=ap++;
  bfMove(t0); bf+="[-]";  bfMove(y); bf+="["; bfMove(x); bf+="-";
  bfMove(t0); bf+="+"; bfMove(y); bf+="-]"; bfMove(t0); bf+="[-"; bfMove(y); bf+="+";
  bfMove(t0); bf+="]";
}
void bfMul(int x, int y){
  int t0=ap++;
  int t1=ap++;
  bfMove(t0);bf+="[-]";
  bfMove(t1);bf+="[-]";
  bfMove(x);bf+="[";bfMove(t1);bf+="+"; bfMove(x); bf+="-]";
  bfMove(t1); bf+="[";
  bfMove(y); bf+="[";bfMove(x); bf+="+"; bfMove(t0); bf+="+"; bfMove(y); bf+="-]";
  bfMove(t0); bf+="["; bfMove(y); bf+="+"; bfMove(t0); bf+="-]";
  bfMove(t1); bf+="-]";
}
void bfDivmod(int n0, int d0, int q0, int r0){   //# >n d       //# >0 d-n%d n%d n/d
  int n=ap++;
  int d=ap++;
  int r=ap++;
  int q=ap++;
  bfSet(d,d0);
  bfSet(n,n0);
  bfMove(n);
  bf+="[->[->+>>]>[<<+>>[-<+>]>+>>]<<<<<]>[>>>]>[[-<+>]>+>>]<<<<<";
  bfSet(q0,q);
  bfSet(r0,r);
}
void bfCmp(int x0, int y0, int z0){
  int z=ap++;  
  int x=ap++;
  int y=ap++;
  int t0; t0=ap++;
  int t1; t1=ap++;
  bfSet(x,x0);
  bfSet(y,y0);
  bfMove(z); bf+="[-]>[>>[-]+>[-]<<[<->->-]>[<<[<[-]+>-]>>->]<<<]+>[<<->->[-]]<<";  
  bfSet(z0,z);  
}
void bfA2b(int a0, int a1, int a2, int b0){
  int b=ap++;
  int t0=ap++;
  int t1=val3("10").first;
  bfSet(t0,a0);bfMove(t0);bf+=string(48,'-');
  bfSet(b,t0);
  bfMul(b,t1);
  bfSet(t0,a1);bfMove(t0);bf+=string(48,'-');
  bfInc(b,t0);
  bfMul(b,t1);
  bfSet(t0,a2);bfMove(t0);bf+=string(48,'-');
  bfInc(b,t0);
  bfSet(b0,b); // this is not the most efficient way but is the way required to pass test;
}
void bfB2a( int b, int a0, int a1, int a2){
  int t0=ap++;
  int t2=val3("10").first;
  bfDivmod(b,t2,t0,a2); bfMove(a2);bf+=string(48,'+');
  bfDivmod(t0,t2,a0,a1);bfMove(a1);bf+=string(48,'+');
  bfMove(a0);bf+=string(48,'+');
}
void bfLset(int sp,int y, int z){
  int da=sp+3;
  bfMove(z); bf+="[-"; bfMove(sp); bf+="+"; bfMove(da); bf+="+"; bfMove(z); bf+="]"; bfMove(sp); bf+="[-"; bfMove(z);
  bf+="+"; bfMove(sp) ;bf+="]";
  bfMove(y); bf+="[-"; bfMove(sp); bf+="+>+>+<<"; bfMove(y); bf+="]";
  bfMove(sp); bf+="[-"; bfMove(y); bf+="+"; bfMove(sp); bf+="]";
  bf+=">[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]>>>[-]<[->+<]<[[-<+>]<<<[->>>>+<<<<]>>-]<<";
}
void bfLget(int sp, int z, int x){
  int da=sp+3;
  bfMove(z); bf+="[-"; bfMove(sp); bf+="+>+>+<<"; bfMove(z); bf+="]";
  bfMove(sp); bf+="[-"; bfMove(z); bf+="+"; bfMove(sp); bf+="]";
  bf+=">[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]>>>[-<+<<+>>>]<<<[->>>+<<<]>[[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<";
  bfMove(x); bf+="[-]";
  bfMove(da); bf+="[-"; bfMove(x); bf+="+"; bfMove(da); bf+="]";
}
void fread(vector<string> sc){
  if (sc.size()!=2) throw string("wrong arg num");
  bfMove(vars[sc[1]]);
  bf+="[-],";
}
void fmsg(vector<string> sc){
  for (size_t i=1;i<sc.size();i++){
   string a=sc[i];
   if(a[0]=='"'){
     bfMove(ap);
     for (size_t j=1;j<a.size()-1;j++){
       int w;
       if (a[j]=='\\' ){
         j++;
         switch(a[j]){
             case 'n': w='\n'; break;
             case 'r': w='\r'; break;
             case 't': w='\t'; break;
             case '\\': w='\\'; break;
             case '\'': w='\''; break;
             case '"' : w='"'; break;
         }
      }else w=a[j];
       bf+="[-]"+string(w,'+')+".";
     }
     bf+="[-]";
   } 
   else{
     it=vars.find(a);
     if(it==vars.end()) throw "var not defined "+a;
     bfMove(it->second); bf+=".";
   }
  }
}
void fvar(vector<string> sc){
  for (size_t i=1;i<sc.size();i++){
    it=vars.find(sc[i]);
    if(it!=vars.end()) throw "duplicated var "+sc[i];
    it=lists.find(sc[i]);
    if(it!=lists.end()) throw "duplicated var "+sc[i];
    if (i+1<sc.size() && sc[i+1]=="["){
      if(i+3>=sc.size() || sc[i+3]!="]"){
        throw string("unclosed ]");
      } else{
        lists[sc[i]]=ap;
        ap+=stoi(sc[i+2])+4;
        i+=3;
      }
    } 
    else{
      vars[sc[i]]=ap++;  
    }
  }
}
void fend(vector<string> sc){
  if(ret.size()==0) throw string("End before block");
  tuple<string,int,int,int,string> r;
  r=ret.back();
  if(get<0>(r)==""){
    bfMove(get<1>(r));
    bf+=get<4>(r);
    bf+="]";
    cp=get<2>(r);
  } else{
    line=get<3>(r);
    currprocs.erase(get<0>(r));
  }
  ret.pop_back();
}
void fcall(vector<string> sc){
  itp=procs.find(sc[1]);
  if(itp==procs.end()) throw "proc "+sc[1]+" not defined";

  it=currprocs.find(sc[1]);
  if(it!=currprocs.end()) throw "Recursion of "+sc[1];
  currprocs[sc[1]]=1;
  if(sc.size()!=procs[sc[1]].second){
    throw string("Invalid proc param");
  } 
  for (size_t k=2;k<sc.size();k++){
    vars[sc[1]+"__"+to_string(k-2)]=val(sc[k]);
  }
  ret.push_back(make_tuple(sc[1],cp,cp,line,""));
  line=procs[sc[1]].first;
}
void fcmp(vector<string> sc){
  if (sc.size()!=4) throw string("wrong arg num");
  it=vars.find(sc[3]);
  if(it==vars.end()) throw "var not defined "+sc[3];
  int r=it->second;
  bfCmp(val(sc[1]),val(sc[2]),r);
}
void fset(vector<string> sc){
  if (sc.size()!=3) throw string("wrong arg num");
  it=vars.find(sc[1]);
  if(it==vars.end()) throw "var not defined";
  if(isConstant(sc[2])){
    bfMove(it->second);bf+="[-]"+string(consts[sc[2]].second,'+');
  }
  else bfSet(it->second,val(sc[2]));
}
void flset(vector<string> sc){
  if (sc.size()!=4) throw string("wrong arg num");
  it=lists.find(sc[1]);
  if(it==lists.end()) throw "list not defined"+sc[1];
  bfLset(it->second,val(sc[2]),val(sc[3]));
}
void flget(vector<string> sc){
  if (sc.size()!=4) throw string("wrong arg num");
  it=lists.find(sc[1]);
  if(it==lists.end()) throw "list not defined "+sc[1];
  int a=it->second;
  it=vars.find(sc[3]);
  if(it==vars.end()) throw "var not defined "+sc[3];
  int b=it->second;
  bfLget(a,val(sc[2]),b);
}
void fifeq(vector<string> sc){
  if (sc.size()!=3) throw string("wrong arg num");
  it=vars.find(sc[1]);
  if(it==vars.end()) throw "Undefined var "+sc[1];
  int a=it->second;
  int x=ap++;
  int y=ap++;
  bfSet(y,val(sc[2]));
  bfSet(x,a); 
  bfMove(x); bf+="[->-<]+>[<->[-]]<[";
  ret.push_back(make_tuple("",cp,cp,-1,"[-]"));
}
void fifneq(vector<string> sc){
  if (sc.size()!=3) throw string("wrong arg num");
  it=vars.find(sc[1]);
  if(it==vars.end()) throw "var not defined "+sc[1];
  int a=it->second;
  int x=ap++;
  int y=ap++;
  bfSet(y,val(sc[2]));
  bfSet(x,a); 
  bfMove(x); bf+="[->-<]>[[-]<+>]<[";
  ret.push_back(make_tuple("",cp,cp,-1,"[-]"));
}
void fwneq(vector<string> sc){
  int cp2=cp;
  int bfs=bf.size();
  if (sc.size()!=3) throw string("wrong arg num");
  it=vars.find(sc[1]);
  if(it==vars.end()) throw "Var not defined "+sc[1];
  int a=it->second;
  int x=ap++;
  int y=ap++;
  bfSet(y,val(sc[2]));
  bfSet(x,a); 
  bfMove(x); bf+="[->-<]>[[-]<+>]<"; 
  string rs=bf.substr(bfs,bf.size()-bfs);
  ret.push_back(make_tuple("",cp2,cp,-1,rs));
  bf+="[";
}
void finc(vector<string> sc){
  if (sc.size()!=3) throw string("wrong arg num");
  it=vars.find(sc[1]);
  if(it==vars.end()) throw "var not defined "+sc[1];
  if(isConstant(sc[2])){
    bfMove(it->second); bf+=string(consts[sc[2]].second,'+');
  } 
  else bfInc(it->second,val(sc[2]));
}
void fdec(vector<string> sc){
  if (sc.size()!=3) throw string("wrong arg num");
  it=vars.find(sc[1]);
  if(it==vars.end()) throw "var not defined "+sc[1];
  if(isConstant(sc[2])){
    bfMove(it->second); bf+=string(consts[sc[2]].second,'-');
  }
  else 
    bfDec(it->second,val(sc[2]));
}
void fadd(vector<string> sc){
  if (sc.size()!=4) throw string("wrong arg num");
  it=vars.find(sc[3]);
  if(it==vars.end()) throw "var not defined "+sc[3];
  int x=it->second;
  if(x!=val(sc[1]))
    bfSet(x,val(sc[1]));
  bfInc(x,val(sc[2]));
}
void fsub(vector<string> sc){
  if (sc.size()!=4) throw string("wrong arg num");
  it=vars.find(sc[3]);
  if(it==vars.end()) throw "var not defined "+sc[3];
  int x=it->second;
  if(x!=val(sc[1]))
    bfSet(x,val(sc[1]));
  bfDec(x,val(sc[2]));
}
void fmul(vector<string> sc){
  if (sc.size()!=4) throw string("wrong arg num");
  it=vars.find(sc[3]);
  if(it==vars.end()) throw "var not defined "+sc[3];
  int x=it->second;
  if(x!=val(sc[1]))
    bfSet(x,val(sc[1]));
  bfMul(x,val(sc[2]));
}
void fdivmod(vector<string> sc){
  if (sc.size()!=5) throw string("wrong arg num");
  it=vars.find(sc[3]);
  if(it==vars.end()) throw "var not defined "+sc[3];
  int q=it->second;
  it=vars.find(sc[4]);
  if(it==vars.end()) throw "var not defined "+sc[4];
  int r=it->second;
  bfDivmod(val(sc[1]),val(sc[2]),q,r);
}
void fdiv(vector<string> sc){
  if (sc.size()!=4) throw string("wrong arg num");
  it=vars.find(sc[3]);
  if(it==vars.end()) throw "var not defined "+sc[3];
  int q=it->second;
  bfDivmod(val(sc[1]),val(sc[2]),q,ap++);
}
void fmod(vector<string> sc){
  if (sc.size()!=4) throw string("wrong arg num");
  it=vars.find(sc[3]);
  if(it==vars.end()) throw "var not defined "+sc[3];
  int r=it->second;
  bfDivmod(val(sc[1]),val(sc[2]),ap++,r);
}
void fa2b(vector<string> sc){
  if (sc.size()!=5) throw string("wrong arg num");
  it=vars.find(sc[4]);
  if(it==vars.end()) throw "var not defined "+sc[4];
  int b=it->second;
  bfA2b(val(sc[1]),val(sc[2]),val(sc[3]),b);
}
void fb2a(vector<string> sc){
  if (sc.size()!=5) throw string("wrong arg num");
  it=vars.find(sc[2]);
  if(it==vars.end()) throw "var not defined "+sc[2];
  int a0=it->second;
  it=vars.find(sc[3]);
  if(it==vars.end()) throw "var not defined "+sc[3];
  int a1=it->second;
  it=vars.find(sc[4]);
  if(it==vars.end()) throw "var not defined "+sc[4];
  int a2=it->second;
  bfB2a(val(sc[1]),a0,a1,a2);
}
void fproc(vector<string> sc){
  line=scv.size();
}
void frem(vector<string> sc){}

std::string kcuf(const std::string& code) /* throws std::string */ {
  if(fMap.size()==0){
    fMap["var"]=fvar; fMap["set"]=fset;  fMap["inc"]=finc; fMap["dec"]=fdec; fMap["add"]=fadd; fMap["sub"]=fsub; fMap["mul"]=fmul; fMap["divmod"]=fdivmod;
    fMap["div"]=fdiv; fMap["mod"]=fmod;  fMap["cmp"]=fcmp; fMap["a2b"]=fa2b; fMap["b2a"]=fb2a; fMap["lset"]=flset; fMap["lget"]=flget; fMap["ifeq"]=fifeq;
    fMap["ifneq"]=fifneq; fMap["wneq"]=fwneq; fMap["proc"]=fproc; fMap["end"]=fend; fMap["call"]=fcall; fMap["read"]=fread; fMap["msg"]=fmsg; fMap["rem"]=frem;
  }

  bf=""; ap=cp=0;
  scv.clear();  vars.clear(); lists.clear(); consts.clear(); procs.clear(); currprocs.clear(); ret.clear();
  
  stringstream prog(code);
  string t;
  int elvl=0;bool pf=false;
  while(getline(prog,t)){
    vector<string> tok;
    size_t x=0;
    string tk;
    while(x<t.size()){
      bool isCt=false;
      if ((t[x]>='a' && t[x]<='z') || (t[x]>='A' && t[x]<='Z') || t[x]=='_' || t[x]=='$'){
        while( x<t.size() && (  (t[x]>='a' && t[x]<='z') || (t[x]>='A' && t[x]<='Z') || t[x]=='_' || t[x]=='$'||
              (t[x]>='0' &&t[x]<='9'))) tk+=t[x++];
        transform(tk.begin(),tk.end(),tk.begin(),::tolower);
      }
      else if(isspace(t[x])){
        while(isspace(t[x])) x++;
      }
      else if(( t[x]>='0' && t[x]<='9') ){
        while(x<t.size() && (t[x]>='0' && t[x]<='9')) tk+=t[x++];
        isCt=true;
      }
      else if(t[x]=='"'){
        tk+=t[x++];
        while( x<t.size() && (t[x]!='"' || (tk.back()=='\\' && t[x]=='"'))) tk+=t[x++] ;
        if (x>=t.size()) throw string("no match \" ");
        tk+=t[x++] ;
      }
      else if(t[x]=='\'' ){
        tk+=t[x++];
        if(x+1<t.size() && t[x]!='\\' && t[x+1]=='\''){
          tk+=t.substr(x,2);
          isCt=true; x+=2;
        }
        else if(x+2<t.size() && t[x]=='\\' && t[x+2]=='\''){
          tk+=t.substr(x,3);
          isCt=true; x+=3;
        } else throw string("unmatched quotes");
      }
      else if(t[x]=='-'){
        x++;
        if(x<t.size() && t[x]=='-'){
          x=t.size();
        }
        else if(x<t.size() && t[x]>='0'&& t[x]<='9'){
          tk='-';
          while(x<t.size() && t[x]>='0'&& t[x]<='9') tk+=t[x++];
          isCt=true;
        }
      }
      else if(t[x]=='[' ){
        tk="["; x++;  
      }
      else if(t[x]==']' ){
        tk="]"; x++;
      }
      else if(t[x]=='#'){
        x=t.size();
      }
      else if(t[x]=='/'){
        if (x+1>=t.size() || t[x+1]!='/') throw string("Invalid Input 1");
        x=t.size();
      }
      else if(t[x]=='&'){
        if (x+1>=t.size() || t[x+1]!='&') throw string("Invalid Input 2");
        x=t.size();
      }
      else throw string("Invalid input 3 ")+"<"+t[x]+">"+to_string(t[x])+"->"+ t;
      if(isCt){
        itc=consts.find(tk);
        if(itc==consts.end()) consts[tk]=val3(tk);
      }
      if(tk.size()>0){
        tok.push_back(tk);tk="";
      }
    }
    if (tok.size()>0){
      if( tok[0]=="proc"){
        if(pf) throw "Nested procedure "+tok[1];
        if(procs.find(tok[1])!=procs.end()) throw "Duplicated procedure "+tok[1];
        pf=true; elvl=1;
        string proc=tok[1];
        sort(tok.begin()+2,tok.end());
        string pa="";
        for (size_t i=2;i<tok.size();i++){
          if(tok[i]==pa) throw string("Duplicated parameter");
          pa=tok[i];
          pv[tok[i]]=proc+"__"+to_string(i-2);
          vars[proc+"__"+to_string(i-2)]=-1;
        }
        procs[tok[1]]=make_pair(scv.size(),tok.size());
      } else if(tok[0]=="ifeq" || tok[0]=="ifneq" || tok[0]=="wneq"){
        elvl++;
      } else if (tok[0]=="end"){
        elvl--;    
        if (pf && elvl==0){
          pf=false; pv.clear();
        }
      } else if(pf && tok[0]=="var") throw string("Define variables inside a procedure.");
      if (pf && tok.size()>1){
        for (size_t x=1;x<tok.size();x++){
          itv=pv.find(tok[x]);
          if(itv!=pv.end()) tok[x]=itv->second;
        }
      }
      scv.push_back(tok);
    }
  }
  line=0;
  while(line<scv.size()){
    string cmd=scv[line][0];
    itf=fMap.find(cmd);
    if(itf==fMap.end())throw string("Unknown Intructions");
    itf->second(scv[line]);
    line++;
  }
  if(ret.size()!=0) throw string ("unclosed blocks");
  return bf;
}


####################################################
import java.lang.AssertionError
import java.lang.Exception
import kotlin.math.sign
import kotlin.system.measureTimeMillis

typealias Generator = (Int) -> String

inline fun bfAssert(test: Boolean, lazyMessage: () -> Any) {
    if(!test) throw AssertionError(lazyMessage())
}

fun bfAssert(test: Boolean) {
    bfAssert(test) { "Assertion failed"}
}

enum class Token(val symbol: String){
    VAR("var"), SET("set"), INC("inc"), DEC("dec"), ADD("add"),
    SUB("sub"), MUL("mul"), DIVMOD("divmod"), DIV("div"),
    MOD("mod"), CMP("cmp"), A2B("a2b"), B2A("b2a"), LSET("lset"),
    LGET("lget"), IFEQ("ifeq"), IFNEQ("ifneq"), WNEQ("wneq"),
    PROC("proc"), END("end"), CALL("call"),
    READ("read"), MSG("msg")
}

open class Operand()
open class VarOperand(_name : String) : Operand() {
    val varName = _name.toUpperCase()
    override fun equals(other: Any?): Boolean =
        other is VarOperand && other.varName == varName
    override fun toString(): String = varName
    override fun hashCode() = varName.hashCode()
}

class ListOperand(varName: String, val size: Int) : VarOperand(varName) {}
class StringOperand(private val strValue : String) : Operand() {
    override fun toString()= "\"$strValue\""

    fun content() = strValue.drop(1).dropLast(1)
}
class ConstOperand(private val intValue : Int) : Operand() {
    fun content() : Int {
        if(intValue in 0..255) return intValue
        if(intValue < 0) return (intValue % 256) + 256
        return intValue % 256
    }
}
class Statement(val name: Token, val operands : Array<Operand>)

class Parser(private val tokens : MutableList<String>) {

    fun getStatements(): Array<Statement>{
        val result = mutableListOf<Statement>()
        while(tokens.isNotEmpty()){
            result.add(parseStatement())
        }
        return result.toTypedArray()
    }

    private fun parseStatement(): Statement = when(current().toLowerCase()) {
        "var" -> parseVarCreation()
        "set" -> parseSet()
        "inc" -> parseInc()
        "dec" -> parseDec()
        "add" -> parseAdd()
        "sub" -> parseSub()
        "mul" -> parseMul()
        "divmod" -> parseDivMod()
        "div" -> parseDiv()
        "mod" -> parseMod()
        "cmp" -> parseCmp()
        "a2b"-> parseA2B()
        "b2a" -> parseB2A()
        "lset" -> parseLSet()
        "lget" -> parseLGet()
        "ifeq" -> parseIfEq()
        "ifneq" -> parseIfNEq()
        "wneq" -> parseWneq()
        "proc" -> parseProc()
        "end" -> parseEnd()
        "call" -> parseCall()
        "read" -> parseRead()
        "msg" -> parseMsg()
        else -> throw Exception("Unknown command '${current()}'")
    }

    private fun skip() = when(tokens.size){
        0 -> throw  Exception()
        else -> tokens.removeAt(0)
    }

    private fun current() = when(tokens.size){
        0 -> throw Exception("No more tokens")
        else -> tokens[0]
    }

    private fun currentIs(tk: String) = tokens.size > 0 && current() == tk

    private fun currentMatch(tx: Regex) = current().matches(tx)

    private fun isEnd() = tokens.isEmpty() || currentIs("\n")

    private fun mustEnd() = when{
        tokens.isEmpty() -> ""
        currentIs("\n") -> skip()
        else -> throw  Exception("Expected EOL/EOF, found '${current()}'")
    }

    private fun mustBe(str: String) = when(current().toLowerCase()) {
        str.toLowerCase() -> skip()
        else -> throw Exception("Expected '$str' instead go '${tokens[0]}'")
    }

    private fun mustBe(tk : Token) =  mustBe(tk.symbol)

    private fun parseVarDeclaration(): VarOperand {
        val name = parseVarName().varName
        if(currentIs("[")){
            skip()
            bfAssert(currentMatch("""^\d+$""".toRegex())) {"Expected number, got '${current()}'"}
            val size = skip().toInt()
            mustBe("]")
            return ListOperand(name, size)
        }
        return VarOperand(name)
    }

    private fun parseVarName() = when(currentMatch("""^[a-zA-Z_$]+(\w|\$)*$""".toRegex())){
        true -> VarOperand(skip())
        else -> throw  Exception("Invalid var name '${current()}'")
    }

    private fun parseVarOrString() = when {
        current().startsWith("\"") && current().endsWith("\"") -> StringOperand(skip())
        else -> parseVarName()
    }

    private fun parseVarOrNumber() = when{
        currentMatch("^'.'$".toRegex()) -> ConstOperand(skip()[1].toInt())
        currentMatch("^-?\\d+$".toRegex()) -> ConstOperand(skip().toInt())
        else -> parseVarName()
    }

    private fun valNumberStatement(prefix: Token) : Statement {
        mustBe(prefix)
        val target = parseVarName()
        val apply = parseVarOrNumber()
        mustEnd()
        return Statement(prefix, arrayOf(target, apply))
    }

    private fun doubleValStatement(prefix: Token) : Statement {
        mustBe(prefix)
        val firstOp = parseVarOrNumber()
        val secondOp = parseVarOrNumber()
        val targetVar = parseVarName()
        mustEnd()
        return Statement(prefix, arrayOf(firstOp, secondOp, targetVar))
    }

    private fun parseSet() = valNumberStatement(Token.SET)
    private fun parseInc() = valNumberStatement(Token.INC)
    private fun parseDec() = valNumberStatement( Token.DEC)
    private fun parseIfEq() = valNumberStatement(Token.IFEQ)
    private fun parseIfNEq() = valNumberStatement(Token.IFNEQ)
    private fun parseWneq() = valNumberStatement(Token.WNEQ)
    private fun parseAdd() = doubleValStatement(Token.ADD)
    private fun parseSub() = doubleValStatement(Token.SUB)
    private fun parseMul() = doubleValStatement(Token.MUL)
    private fun parseDiv() = doubleValStatement(Token.DIV)
    private fun parseMod() = doubleValStatement(Token.MOD)
    private fun parseCmp() = doubleValStatement(Token.CMP)

    private fun parseDivMod(): Statement {
        mustBe(Token.DIVMOD)
        val firstOp = parseVarOrNumber()
        val secondOd = parseVarOrNumber()
        val firstVar = parseVarName()
        val sndVar = parseVarName()
        mustEnd()
        return Statement(Token.DIVMOD, arrayOf(firstOp, secondOd, firstVar, sndVar))
    }

    private fun parseVarCreation(): Statement{
        mustBe(Token.VAR)
        val operands = mutableListOf<VarOperand>()
        while(!isEnd()){
            operands.add(parseVarDeclaration())
        }
        mustEnd()
        return Statement(Token.VAR, operands.toTypedArray())
    }

    private fun parseA2B(): Statement {
        mustBe(Token.A2B)
        val toDec = 1.rangeTo(3).map { parseVarOrNumber() }.toTypedArray()
        val target = parseVarName()
        mustEnd()
        return Statement(Token.A2B, arrayOf(*toDec, target))
    }

    private fun parseB2A(): Statement {
        mustBe(Token.B2A)
        val toDec = parseVarOrNumber()
        val targets = 1.rangeTo(3).map { parseVarName() }.toTypedArray()
        mustEnd()
        return Statement(Token.B2A, arrayOf(toDec, *targets))
    }

    private fun parseLSet(): Statement {
        mustBe(Token.LSET)
        val listName = parseVarName()
        val index = parseVarOrNumber()
        val value = parseVarOrNumber()
        mustEnd()
        return Statement(Token.LSET, arrayOf(listName, index, value))
    }

    private fun parseLGet(): Statement {
        mustBe(Token.LGET)
        val listName = parseVarName()
        val index = parseVarOrNumber()
        val target = parseVarName()
        mustEnd()
        return Statement(Token.LGET, arrayOf(listName, index, target))
    }

    private fun parseArgs(prefix: Token): Statement {
        mustBe(prefix)
        val varName = mutableListOf<Operand>()
        while(!isEnd()){
            varName.add(parseVarName())
        }
        mustEnd()
        return Statement(prefix, varName.toTypedArray())
    }

    private fun parseProc() = parseArgs(Token.PROC)
    private fun parseCall() = parseArgs(Token.CALL)

    private fun parseEnd(): Statement {
        mustBe("end")
        mustEnd()
        return Statement(Token.END, arrayOf())
    }

    private fun parseRead(): Statement {
        mustBe("read")
        val target = parseVarName()
        mustEnd()
        return Statement(Token.READ, arrayOf(target))
    }

    private fun parseMsg(): Statement{
        mustBe("msg")
        val target = mutableListOf<Operand>()
        while(!isEnd()){
            target.add(parseVarOrString())
        }
        mustEnd()
        return Statement(Token.MSG, target.toTypedArray())
    }
}

class Procedure(_name: String, val variables : Array<String>, val code : Array<Instruction>) {
    val name = _name.toUpperCase()
    override fun equals(other: Any?) =
        other is Procedure && other.name == name
    override fun hashCode() = name.hashCode()
}

open class Instruction(val type: Token, val operands : Array<Operand>)

class CondInstruction(type: Token,
                      operands: Array<Operand>,
                      val instrs : Array<Instruction>) : Instruction(type, operands)


class StackCount {
    private var index = 0

    fun get() = index

    fun push(incr : Int = 1) : Int{
        val res = index
        index += incr
        return res
    }

    fun pop(decr : Int = 1) : String {
        index -= decr
        return ""
    }
}

class CallStack {
    private var stack = mutableListOf<Procedure>()
    private val variablesIndex = mutableListOf<MutableMap<String, Pair<VarOperand, Int>>>(mutableMapOf())

    private fun varNames() = variablesIndex.last()

    fun varIdx(varName : VarOperand) = varNames()[varName.varName]!!.second

    fun varNameExists(varname: VarOperand) = varNames().containsKey(varname.varName)

    fun isListVar(op: Operand) : Boolean {
        if(op is ConstOperand) return false
        val varName = op as VarOperand
        bfAssert(varNameExists(varName))
        val operand = varNames()[op.varName]!!.first
        return (operand is ListOperand)
    }

    fun setVarIdx(varName : VarOperand, index : Int) {
        bfAssert(isRoot()) { "Can only declare variables at the root" }
        varNames()[varName.varName] = Pair(varName, index)
    }

    fun push(proc : Procedure, varName : List<VarOperand>) {
        if(stack.contains(proc)) throw  Exception("Cannot call recursively method")
        stack.add(proc)
        val top = varNames()
        val nwVars = mutableMapOf<String, Pair<VarOperand, Int>>()
        val procVars = proc.variables
        for((index, value) in varName.withIndex()) {
            val nwIndex = top[value.varName]!!.second
            if(value is ListOperand){
                nwVars[procVars[index]] = Pair(ListOperand(procVars[index], value.size), nwIndex)
            } else {
                nwVars[procVars[index]] = Pair( VarOperand(procVars[index]), nwIndex)
            }
        }
        top.forEach{ nwVars.putIfAbsent(it.key, it.value)}
        variablesIndex.add(nwVars)
    }

    fun pop()  {
        if(stack.isEmpty()) throw Exception("Cannot pop empty stack")
        stack.removeAt(stack.size - 1)
        variablesIndex.removeAt(variablesIndex.size - 1)
    }

    fun isRoot()  = stack.isEmpty()

}

class Transpiler(var statement: MutableList<Statement>) {

    private val sc = StackCount()
    private val cs = CallStack()
    private var cursor = 0
    private val procedures = mutableMapOf<String, Procedure>()
    private val instructions = mutableListOf<Instruction>()

    private fun push(i : Int = 1) = sc.push(i)
    private fun pop(i : Int = 1) = sc.pop(i)

    private fun varIdx(varName : VarOperand) = cs.varIdx(varName)

    private fun goto(idx: Int) : String{
        if(cursor == idx) return ""
        val res = when(cursor){
            in 0..idx -> ">".repeat(idx - cursor)
            else -> "<".repeat(cursor - idx)
        }
        cursor = idx
        return res
    }

    private fun forceCursor(idx : Int) : String {
        cursor = idx
        return ""
    }

    private fun toInstruction(st: Statement) : Instruction  = when(st.name){
        Token.IFNEQ, Token.IFEQ, Token.WNEQ -> condBody(st)
        Token.PROC -> throw Exception("Expected instruction, got procedure")
        else -> Instruction(st.name, st.operands)
    }


    private fun condBody(declaration: Statement): Instruction {
        val instrs = mutableListOf<Instruction>()
        while(!endBlock()){
            val nxt = next()
            instrs.add(toInstruction(nxt))
        }
        mustBe(Token.END)
        return CondInstruction(declaration.name, declaration.operands, instrs.toTypedArray())
    }

    private fun parseProc(declaration: Statement) : Procedure{
        if(declaration.operands.isEmpty()) throw Exception("Missing name of procedure")
        val procName = (declaration.operands[0] as VarOperand).varName
        val instrs = mutableListOf<Instruction>()
        while(!endBlock()){
            val nxt = next()
            val inst = toInstruction(nxt)
            bfAssert(inst.type != Token.VAR && inst.type != Token.PROC) { "Can't define var inside procedure, nor procedure"}
            instrs.add(inst)
        }
        mustBe(Token.END)
        val parameters = declaration.operands.drop(1).map { (it as VarOperand).varName }.toTypedArray()
        bfAssert(parameters.distinct().size == parameters.size) { "Avoid duplicate parameters name" }
        return Procedure(procName, parameters, instrs.toTypedArray())
    }

    fun rootParsing() {
        while(statement.isNotEmpty()){
            val next = statement.removeAt(0)
            when (next.name) {
                Token.VAR -> storeVariables(next)
                Token.END -> throw Exception("Unexpected 'end' token")
                Token.PROC -> {
                    val proc = parseProc(next)
                    bfAssert(!procedures.containsKey(proc.name)) {"Procedure ${proc.name} declared twice"}
                    procedures[proc.name] = proc
                }
                else -> instructions.add(toInstruction(next))
            }
        }
    }

    private fun storeVariables(vars: Statement) {
        for(o in vars.operands) {
            val oVar = o as VarOperand
            bfAssert(!cs.varNameExists(oVar)) {"Can't have twice the save var"}
            cs.setVarIdx(oVar, sc.get())
            sc.push((oVar as? ListOperand)?.size?.plus(4) ?: 1)
        }
    }

    private fun endBlock() = statement.isNotEmpty() && statement[0].name == Token.END

    private fun next() = statement.removeAt(0)

    private fun mustBe(tk: Token) = when{
        statement.isEmpty() || statement[0].name != tk -> throw Exception("Unexpected token")
        else -> statement.removeAt(0)
    }

    private fun inc(increment: Int = 1) = "+".repeat(increment)
    private fun dec(decrement: Int = 1) = "-".repeat(decrement)
    private fun goInc(idx : Int, increment : Int = 1) = "${goto(idx)}${inc(increment)}"
    private fun goDec(idx : Int, decrement : Int = 1) = "${goto(idx)}${dec(decrement)}"
    private fun loop(test: Int, block : () -> String) =  "${goto(test)}[${block()}${goto(test)}]"

    private fun cp(from: Int, vararg to: Int) : String {
        val tmp = push()
        return """
        ${loop(from) {
            to.joinToString("", prefix = "-") { "${goto(it)}+" } + "${goto(tmp)}+"
        }}
        ${loop(tmp) {  "-${goto(from)}+"  }}
        ${pop()}
        """
    }

    private fun mv(from: Int, vararg to: Int) = """
        ${loop(from) {  to.joinToString("", prefix = "-") { "${goto(it)}+" } }}
    """

    private fun reset(idx: Int) = loop(idx) { "-" }

    private fun assertVarOrNumber(op : Operand){
        bfAssert(op is VarOperand && !cs.isListVar(op) || op is ConstOperand)
    }

    private fun assertNotList(op : Operand) {
        bfAssert(!cs.isListVar(op)) { "Can't process a list in this context"}
    }

    private fun createSetter(op : Operand, canMv : Boolean = false) : Generator = when(op) {
            is ConstOperand -> ({ inc(op.content()) })
            is VarOperand -> ({ if(canMv) mv(varIdx(op), it) else cp(varIdx(op), it)})
            else -> throw Exception("Cannot make generator from $op")
    }

    private fun createGetter(op : VarOperand) : Generator {
        val idx = varIdx(op)
        return ({ "${reset(idx)}${mv(it, idx)}" })
    }

    private fun createIncrGetter(op : VarOperand, postInc : Int) : Generator {
        val idx = varIdx(op)
        return {"${reset(idx)}${mv(it, idx)}${goInc(idx, postInc)}"}
    }

    private fun doSet(from : Operand, to : VarOperand): String {
        assertNotList(from)
        assertNotList(to)
        bfAssert(from is VarOperand || from is ConstOperand) { "From must be var or const"}
        val toIdx = varIdx(to)
        if(from is ConstOperand) {
            return "${goto(toIdx)}${reset(toIdx)}${inc(from.content())}"
        }
        val next1 = push()
        val fromIdx = varIdx(from as VarOperand)
        return "${reset(toIdx)}${mv(fromIdx, next1)}${mv(next1, fromIdx, toIdx)}${pop()}"
    }

    private fun doRead(target: VarOperand) = "${goto(varIdx(target))},"

    // Possible improvement : do not reset and incr/decr only the necessary
    private fun outChar(chr: Char) = "${inc(chr.toInt())}.[-]"

    private fun output(op : Operand) = when(op){
        is ListOperand -> throw Exception("Cannot output value of list $op")
        is VarOperand -> "${goto(varIdx(op))}."
        is ConstOperand -> "${goto(push())}${inc(op.content())}.${pop()}"
        is StringOperand ->
            """${goto(push())}${op.content().replace("\\n","\n").map(::outChar).joinToString("")}${pop()}"""
        else -> throw Exception("Unknown operand $op")
    }

    private fun doMsg(values: Array<Operand>) : String {
        return values.joinToString("") { output(it) }
    }

    private fun doInc(target: VarOperand, incrementOf : Operand) : String {
        assertNotList(target)
        assertNotList(incrementOf)
        val tIdx = varIdx(target)
        if(incrementOf is ConstOperand) {
            return "${goto(tIdx)}${inc(incrementOf.content())}"
        }
        val incIdx = varIdx(incrementOf as VarOperand)
        val ne1 = push()
        return "${mv(incIdx, ne1)}${mv(ne1, tIdx, incIdx)}${pop()}"
    }

    private fun doDec(target : VarOperand, decrementOf : Operand) : String {
        assertNotList(target)
        assertNotList(decrementOf)
        val tIdx = varIdx(target)
        if(decrementOf is ConstOperand){
            return "${goto(tIdx)}${dec(decrementOf.content())}"
        }
        val decIdx = varIdx(decrementOf as VarOperand)
        val ne1 = push()
        return "${mv(decIdx, ne1)}${loop(ne1) {"-${goto(tIdx)}-${goto(decIdx)}+"} }${pop()}"
    }

    private inline fun sum(xSetter : Generator, ySetter : Generator, xGetter : Generator, chr: Char) : String {
        val x = push()
        val y = push()
        return """
            ${reset(x)}${xSetter(x)}
            ${reset(y)}${ySetter(y)}
            ${goto(y)}[${goto(x)}$chr${goDec(y)}]
            ${xGetter(x)}
        ${pop(2)}
        """
    }

    private fun doAdd(op1 : Operand, op2: Operand, target: VarOperand) : String{
        assertVarOrNumber(op1)
        assertVarOrNumber(op2)
        assertNotList(target)
        if(op1 is ConstOperand && op2 is ConstOperand){
            return "${goto(varIdx(target))}${inc(op1.content() + op2.content())}"
        }
        return sum(
                createSetter(op1, target == op1),
                createSetter(op2, target == op2),
                createGetter(target),
                '+'
        )
    }

    private fun doSub(op1 : Operand, op2 : Operand, target: VarOperand) : String {
        assertVarOrNumber(op1)
        assertVarOrNumber(op2)
        assertNotList(target)
        if(op1 is ConstOperand && op2 is ConstOperand){
            return "${goto(varIdx(target))}${inc(op1.content() - op2.content())}"
        }
        return sum(
                createSetter(op1, target == op1),
                createSetter(op2, target == op2),
                createGetter(target),
                '-'
        )
    }

    private inline fun mul(xSetter: Generator, ySetter : Generator, xGetter : Generator) : String {
        val x = push()
        val y = push()
        val temp0 = push()
        val temp1 = push()
        return """
        ${reset(x)}${xSetter(x)}
        ${reset(y)}${ySetter(y)}
        ${reset(temp0)}${reset(temp1)}
        ${goto(x)}[${goInc(temp1)}${goDec(x)}]
        ${goto(temp1)}[
            ${goto(y)}[${goInc(x)}${goInc(temp0)}${goDec(y)}]
            ${goto(temp0)}[${goInc(y)}${goDec(temp0)}]
            ${goDec(temp1)}
        ]
        ${xGetter(x)}
        ${pop(4)}
        """
    }

    private fun doMul(op1 : Operand, op2: Operand, target: VarOperand) : String {
        assertVarOrNumber(op1)
        assertVarOrNumber(op2)
        assertNotList(target)
        val tIdx = varIdx(target)
        if(op1 is ConstOperand && op2 is ConstOperand)  return "${goto(tIdx)}${inc(op1.content()*op2.content())}"
        return mul(createSetter(op1, target == op1), createSetter(op2, target == op2), createGetter(target))
    }

    private inline fun divMod(aSetter : Generator, bSetter : Generator, cGetter: Generator, dGetter : Generator) : String {
        val n = push()
        val d = push()
        val mod = push()
        val div = push()
        return """
        ${reset(n)}${aSetter(n)}
        ${reset(d)}${bSetter(d)}
        ${reset(mod)}
        ${reset(div)}
        ${goto(n)}
        [->[->+>>]>[<<+>>[-<+>]>+>>]<<<<<]>[>>>]>[[-<+>]>+>>]<<<<<
        ${forceCursor(n)/* Cursor is at n now */}
        ${cGetter(div)}
        ${dGetter(mod)}
        ${pop(4)}
        """
    }

    private fun doDiv(op1: Operand, op2 : Operand, target: VarOperand) : String {
        assertVarOrNumber(op1)
        assertVarOrNumber(op2)
        assertNotList(target)

        if(op1 is ConstOperand && op2 is ConstOperand){
            val div = op1.content() / op2.content()
            return "${goto(varIdx(target))}${inc(div)}"
        }
        return divMod(createSetter(op1, target == op1 ), createSetter(op2, target == op2), createGetter(target), {""})
    }

    private fun doDivMod(op1 : Operand,
                         op2 : Operand,
                         target1 : VarOperand,
                         target2 : VarOperand) : String {
        assertVarOrNumber(op1)
        assertVarOrNumber(op2)
        assertNotList(target1)
        assertNotList(target2)
        if(op1 is ConstOperand && op2 is ConstOperand) {
            val quotient = op1.content() / op2.content()
            val remainder = op1.content() % op2.content()
            return "${reset(varIdx(target1))}${inc(quotient)}${reset(varIdx(target2))}${inc(remainder)}"
        }

        return divMod(
                createSetter(op1, op1 == target1 || op1 == target2),
                createSetter(op2, op2 == target2 || op2 == target1),
                createGetter(target1),
                createGetter(target2)
        )
    }

    private fun doMod(op1 : Operand, op2 : Operand, target : VarOperand) : String {
        assertVarOrNumber(op1)
        assertVarOrNumber(op2)
        assertNotList(target)
        if(op1 is ConstOperand && op2 is ConstOperand) {
            val remainder = op1.content() % op2.content()
            return "${reset(varIdx(target))}${inc(remainder)}"
        }
        return divMod(createSetter(op1, target == op1), createSetter(op2, target == op2), {""}, createGetter(target))
    }

    private inline fun compare(aSetter : Generator, bSetter : Generator, cGetter: Generator  ) : String {
        val result = push()
        val a = push()
        val b = push()
        val flag1 = push()
        val end = push()
        return """
            ${reset(result)}
            ${reset(a)}${aSetter(a)}
            ${reset(b)}${bSetter(b)}
            ${reset(flag1)}
            ${reset(end)}
            ${goto(a)}
            [
                ${dec()}
                ${goInc(flag1)}
                ${goto(b)}
                [->-]>
                [<<+[[-]<+>]>>->]
                <<<
            ]
            >[[-]<<->>]<<
            ${forceCursor(result)}
            ${cGetter(result)}
            ${pop(5)}
        """
    }

    private fun doCmp(op1 : Operand, op2 : Operand, target : VarOperand) : String{
        assertVarOrNumber(op1)
        assertVarOrNumber(op2)
        assertNotList(target)

        val targetIdx = varIdx(target)
        if(op1 is ConstOperand && op2 is ConstOperand){
            val result = (op1.content()   - op2.content()).sign
            return "${reset(targetIdx)}${if(result < 0) dec(1) else inc(result)}"
        }

        return compare(
                createSetter(op1, target == op1),
                createSetter(op2, target == op2),
                { "${reset(targetIdx)}${mv(it, targetIdx)}"}
        )
    }

    private inline fun a2B(aSetter : Generator, bSetter : Generator, cSetter : Generator, dGetter : Generator) : String {
        val buff = push()
        val buff2 = push()
        val result = push()
        val buff3 = push()
        val a = push()
        val b = push()
        val c = push()
        val limit = push()
        return """
            ${reset(buff)}
            ${reset(buff2)}
            ${reset(result)}
            ${reset(buff3)}
            ${reset(limit)}
            ${reset(a)}
            ${aSetter(a)}
            ${reset(b)}
            ${bSetter(b)}
            ${reset(c)}
            ${cSetter(c)}
            ${goto(buff3)}
            >------------------------------------------------[<<+>>-]>
            [
                <<<
                [<+>-]<
                [>++++++++++<-]>
                >>>
                ------------------------------------------------
                [<<<+>>>-]>
                [
                    <<<<
                    [<+>-]<
                    [>++++++++++<-]>
                    >>>>
                    ------------------------------------------------
                    [<<<<+>>>>-]
                ]
                <
            ]
            <<<
            ${forceCursor(result)}
            ${dGetter(result)}
            ${pop(8)}
        """
    }

    private fun doA2B(a : Operand, b : Operand, c : Operand, d :VarOperand) : String {
        assertVarOrNumber(a)
        assertVarOrNumber(b)
        assertVarOrNumber(c)
        assertNotList(d)

        val targetIdx = varIdx(d)
        if(a is ConstOperand && b is ConstOperand && c is ConstOperand){
            val result = 100 * (a.content() - 48) + 10 * (b.content() - 48) + (c.content() - 48)
            return "${reset(targetIdx)}${inc(result)}"
        }

        return a2B(
                createSetter(a),
                createSetter(b),
                createSetter(c, c == d),
                { "${reset(targetIdx)}${mv(it, targetIdx)}" }
        )
    }

    private fun b2a(aSetter : Generator, bGetter : Generator, cGetter : Generator, dGetter: Generator): String {
        val aTmp = push()
        return """
            ${divMod(aSetter, { "${reset(it)}${goInc(it, 100)}"}, bGetter, { "${reset(aTmp)} ${mv(it,aTmp)})} "})}
            ${divMod({ "${reset(it)}${mv(aTmp, it)}"}, { "${reset(it)}${goInc(it, 10)}" }, cGetter, dGetter)}
            ${pop()}
        """
    }

    private fun doB2A(a : Operand, b : VarOperand, c : VarOperand, d : VarOperand) : String {
        assertVarOrNumber(a)
        assertNotList(b)
        assertNotList(c)
        assertNotList(d)

        if(a is ConstOperand){
            val aVal = a.content()
            val bValue = (aVal / 100)
            val cValue = ( (aVal % 100) / 10)
            val dValue = (aVal % 10)
            return "${reset(varIdx(b))}${inc(bValue + 48)}${reset(varIdx(c))}${inc(cValue + 48)}${reset(varIdx(d))}${inc(dValue + 48)}"
        }

        return b2a(
                createSetter(a, a == b || a == c || a == d),
                createIncrGetter(b, 48),
                createIncrGetter(c, 48),
                createIncrGetter(d, 48)
        )
    }

    private fun doLSet(a : VarOperand, b : Operand, c : Operand) : String {
        assertVarOrNumber(c)
        bfAssert(cs.isListVar(a))
        if(b is ConstOperand) {
            val index0 = varIdx(a) + b.content() + 4

            return if(c is VarOperand) {
                "${reset(index0)}${cp(varIdx(c), index0)}"
            } else{
                "${reset(index0)}${goInc(index0, (c as ConstOperand).content())}"
            }
        }
        val listStart = varIdx(a)
        val cSetter : Generator = when(c){
            is VarOperand -> ({cp(varIdx(c), it)})
            is ConstOperand -> ({goInc(it, c.content())})
            else -> throw Exception("Cant set list with list")
        }
        return """
            ${reset(listStart)}
            ${reset(listStart+1)}${cp(varIdx(b as VarOperand), listStart +1)}
            ${reset(listStart+2)}+
            ${cSetter(listStart + 3)}
            ${goto(listStart)}
            >[>>>[-<<<<+>>>>]<
            [->+<]
            <+[->+<]
            <[->+<]
            >-]
            >>>[-]<[->+<]<
            -[
            [-<+>]
            <<<[->>>>+<<<<]
            >>-]
            <<
        """
    }

    private fun doLGet(a : VarOperand, b : Operand, c : VarOperand) : String {
        assertVarOrNumber(c)
        bfAssert(cs.isListVar(a))
        val cIndex = varIdx(c)
        if(b is ConstOperand)
            return "${reset(cIndex)}${cp(varIdx(a) + b.content() + 4, cIndex)}"

        val listStart = varIdx(a)

        return """
            ${reset(listStart)}
            ${reset(listStart+1)}${cp(varIdx(b as VarOperand), listStart +1)}
            ${reset(listStart+2)}+
            ${reset(listStart + 3)}
            ${goto(listStart)}
            >[>>>[-<<<<+>>>>]<
            <+[->+<]
            <[->+<]
            >-]
            >>>[-<+<<+>>>]<<<[->>>+<<<]>
            -[
            [-<+>]
            >[-<+>]<
            <<<[->>>>+<<<<]
            >>-]
            <<
            ${reset(cIndex)}
            ${mv(listStart+3, cIndex)}
        """
    }

    private fun xor(x : Int, y : Int, z : Int) : String {
        val xTmp = push()
        val yTmp = push()
        return """
            ${reset(z)}
            ${reset(xTmp)}
            ${reset(yTmp)}
            ${goto(x)}
            [${goDec(y)}${goInc(xTmp)}${goInc(yTmp)}${goDec(x)}]
            ${goto(y)}
            [${goInc(z)}${mv(y, yTmp)}${goto(y)}]
            ${mv(yTmp, y)}${mv(xTmp, x)}
            ${pop(2)}
        """
    }

    private fun doIfEq(instruction : CondInstruction) : String {
        val (left, right) = instruction.operands
        assertNotList(left)
        assertNotList(right)
        val instr = instruction.instrs
        val aIdx = varIdx(left as VarOperand)
        return if(right is ConstOperand) {
            val tmp0 = push()
            val tmp1 = push()
            """
                ${reset(tmp0)}+
                ${reset(tmp1)}
                ${goDec(aIdx, right.content())}
                [
                    ${goInc(aIdx, right.content())}
                    ${goDec(tmp0)}
                    ${goto(aIdx)}[${goInc(tmp1)}${goDec(aIdx)}]
                ]
                ${goto(tmp1)}[${goInc(aIdx)}${goDec(tmp1)}]
                ${goto(tmp0)}
                [
                    ${goInc(aIdx, right.content())}
                    ${transpileInstructions(instr.asIterable())}
                    ${goDec(tmp0)}
                ]
                ${pop(2)}
            """
        } else {
            val bIdx = varIdx(right as VarOperand)
            val tmp0 = push()
            val z = push()
            """
                ${reset(tmp0)}+
                ${xor(aIdx, bIdx ,z)}
                ${goto(z)}
                [
                    ${goDec(tmp0)}
                    ${reset(z)}
                ]
                ${goto(tmp0)}
                [
                    ${transpileInstructions(instr.asIterable())}
                    ${goDec(tmp0)}
                ]
                ${pop(2)}
            """
        }
    }

    private fun doIfNEq(instruction : CondInstruction) : String {
        val (left, right) = instruction.operands
        assertNotList(left)
        assertNotList(right)
        val instr = instruction.instrs
        val aIdx = varIdx(left as VarOperand)

        return if(right is ConstOperand) {
            val tmp0 = push()
            val tmp1 = push()
            """
                ${reset(tmp0)}+
                ${reset(tmp1)}
                ${goDec(aIdx, right.content())}
                [
                    ${goInc(aIdx, right.content())}
                    ${goDec(tmp0)}
                    ${transpileInstructions(instr.asIterable())}
                    ${goto(aIdx)}[${goInc(tmp1)}${goDec(aIdx)}]
                ]
                ${goto(tmp1)}[${goInc(aIdx)}${goDec(tmp1)}]
                ${goto(tmp0)}
                [
                    ${goInc(aIdx, right.content())}
                    ${goDec(tmp0)}
                ]
                ${pop(2)}
            """
        } else {
            val bIdx = varIdx(right as VarOperand)
            val z = push()
            """
                ${xor(aIdx, bIdx ,z)}
                ${goto(z)}
                [
                    ${transpileInstructions(instr.asIterable())}
                    ${reset(z)}
                ]
                ${pop()}
            """
        }
    }

    private fun doWNeq(instructions : CondInstruction) : String {
        val (left, right) = instructions.operands
        val instrs = instructions.instrs
        assertNotList(left)
        bfAssert(left is VarOperand)
        assertNotList(right)
        val a = (left as VarOperand)
        val aIndex = varIdx(a)
        if(right is ConstOperand) {
            return """
                ${goDec(aIndex, right.content())}
                ${loop(aIndex) {"""
                    ${goInc(aIndex, right.content())}
                    ${transpileInstructions(instrs.asIterable())}
                    ${goDec(aIndex, right.content())}
                """}}
                ${goInc(aIndex, right.content())}
            """
        } else {
            val bIndex = varIdx(right as VarOperand)
            val z = push()
            return """
                ${xor(aIndex, bIndex, z)}
                ${loop(z) {"""${transpileInstructions(instrs.asIterable())}
                    ${xor(aIndex, bIndex, z)}
                """ }}
                ${pop()}
            """
        }
    }

    private fun call(proc : Procedure, operands: List<VarOperand>) : String {
        cs.push(proc, operands)
        val res = transpileInstructions(proc.code.asIterable())
        cs.pop()
        return res
    }

    private fun doCall(operands : Array<Operand>) : String {
        bfAssert(operands.isNotEmpty() && operands.all { it is VarOperand } ) {"Need at least one element, all var names" }
        val varnames = operands.map { it as VarOperand }
        val fnName = varnames[0].varName
        bfAssert(procedures.contains(fnName)){"The procedure $fnName does not exist"}
        val proc = procedures[fnName]!!
        return call(proc, varnames.drop(1))
    }

    fun instructionToBf(int : Instruction) = when(int.type) {
        Token.SET -> doSet(int.operands[1], int.operands[0] as VarOperand)
        Token.READ -> doRead(int.operands[0] as VarOperand)
        Token.MSG -> doMsg(int.operands)
        Token.INC -> doInc(int.operands[0] as VarOperand, int.operands[1])
        Token.DEC -> doDec(int.operands[0] as VarOperand, int.operands[1])
        Token.ADD -> doAdd(int.operands[0], int.operands[1], int.operands[2] as VarOperand)
        Token.SUB -> doSub(int.operands[0], int.operands[1], int.operands[2] as VarOperand)
        Token.MUL -> doMul(int.operands[0], int.operands[1], int.operands[2] as VarOperand)
        Token.DIV -> doDiv(int.operands[0], int.operands[1], int.operands[2] as VarOperand)
        Token.DIVMOD -> doDivMod(
            int.operands[0],
            int.operands[1],
            int.operands[2] as VarOperand,
            int.operands[3] as VarOperand)
        Token.MOD -> doMod(int.operands[0], int.operands[1], int.operands[2] as VarOperand)
        Token.CMP -> doCmp(int.operands[0], int.operands[1], int.operands[2] as VarOperand)
        Token.A2B -> doA2B(int.operands[0], int.operands[1], int.operands[2], int.operands[3] as VarOperand)
        Token.B2A -> doB2A(
                int.operands[0],
                int.operands[1] as VarOperand,
                int.operands[2] as VarOperand,
                int.operands[3] as VarOperand)
        Token.LSET -> doLSet(
                int.operands[0] as VarOperand, int.operands[1], int.operands[2])
        Token.LGET -> doLGet(int.operands[0] as VarOperand, int.operands[1], int.operands[2] as VarOperand)
        Token.IFEQ -> doIfEq(int as CondInstruction)
        Token.IFNEQ -> doIfNEq(int as CondInstruction)
        Token.WNEQ -> doWNeq(int as CondInstruction)
        Token.CALL -> doCall(int.operands)
        else -> throw Exception("Unknown instruction ${int.type}")
    }

    private fun transpileInstructions(toTranspile : Iterable<Instruction>) =
            toTranspile.joinToString("") { instructionToBf(it)  }

    fun transpile() = transpileInstructions(instructions)

}

fun isComment(token: String) = "^(#|//|--|rem )".toRegex(RegexOption.IGNORE_CASE).containsMatchIn(token)

fun <T> MutableList<T>.removeDuplicates(): MutableList<T>{
    for(i in this.size-2 downTo 0){
        if(this[i+1] == this[i] && this[i] == "\n"){
            this.removeAt(i+1)
        }
    }
    return this
}

fun kcuf(code: String): String {
    val reg = Regex("""".+?"|'.'|(--|#|/{2}|rem).*|-?\d+|[a-zA-Z_$]+(\w|[$])*|[\[\]=]|\n""", RegexOption.IGNORE_CASE);
    val tokens = reg.findAll(code)
                    .map { it.value }
                    .filterNot(::isComment)
                    .toMutableList()
                    .removeDuplicates()
    val parser = Parser(tokens)
    val transpiler = Transpiler(parser.getStatements().toMutableList())
    transpiler.rootParsing()
    return transpiler.transpile()
}

//
// If printing the code is annoying or a waste of your bandwith (~220 KB for final test).
// Please uncomment the following line.
val just = NOPRINT()

#####################################
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
