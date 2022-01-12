#include <regex>
using namespace std;
size_t ti=0;
vector <string> tokenize (string program) {
    static regex re ("[A-Za-z_][A-Za-z0-9]*|[,\\{\\}\\(\\)]|->|\\d+");
    sregex_token_iterator it (program.begin (), program.end (), re);
    ti=0;
    return vector <string> (it, sregex_token_iterator ());
}
string join(const vector<string>& v, char c) {

   string s;

   for (vector<string>::const_iterator p = v.begin(); p != v.end(); ++p) {
      s += *p;
      if (p != v.end() - 1) s += c;
   }
  return s;
}
bool isName(string s){
  if (regex_match (s, regex("[A-Za-z_][A-Za-z0-9]*|\\d+") )) return true;
  return false;
}

string lambda(vector<string> tokens){
  vector<string> par;
  vector<string> sta;
  size_t ti2=ti;
  int lev=1;
  bool arePar=false;
  while (ti2<tokens.size() && lev!=0){
    if(tokens[ti2]=="{") lev++;
    else if(tokens[ti2]=="}") lev--;
    if(tokens[ti2]=="->" && lev==1){
      arePar=true;
      break;
    }
    ti2++;
  }
  if(arePar){
    while(ti<tokens.size() && tokens[ti]!="->"){
      if( tokens[ti] == "{"){
        ti++;
        par.push_back(lambda(tokens));
        if(par.back()=="") return "";
      } else if (isName(tokens[ti])){
        par.push_back(tokens[ti]);
        ti++;
      } else return "";
      if (ti<tokens.size()){
        if(tokens[ti]==","){
          ti++;
          if(ti<tokens.size()&& tokens[ti]=="->") return "";
        } else if(tokens[ti]!= "->") return "";
      } else return ""; 
    } 
    ti++;
    if (par.size()==0) return "";
  } 
  
  while(ti<tokens.size() && tokens[ti]!="}"){
    if( tokens[ti] == "{"){
      ti++;
      sta.push_back(lambda(tokens));
      if (sta.back()=="") return ""; 
    } else if (isName(tokens[ti])){
      sta.push_back(tokens[ti]);
      ti++;
    } else return "";
  }
  if (ti>=tokens.size()) return "";
  string res="("+join(par,',')+")";
  res+="{"+join(sta,';');
  if (sta.size()>0) res+=";}";
  else res+="}";
  ti++;
  return res;
} 

const char *transpile (const char* expression) {
  vector<string> tokens = tokenize(string(expression));
  string res;
  vector<string> args;
  if (tokens.size()==0 ||( !isName(tokens[0]) && tokens[0]!="{")) return "";
  if (tokens[0]=="{"){
    ti++;
    string temp=lambda(tokens);
    if (temp=="") return "";
    res=temp;
  } 
  else{
    res=tokens[0];
    ti++;
  } 
  //arguments between parenthesis
  if(tokens[ti]=="("){
    ti++;
    while(ti<tokens.size() && tokens[ti]!=")"){
      if(tokens[ti]=="{"){
        ti++;
        args.push_back(lambda(tokens));
        if(args.back()=="") return "";
      } 
      else if ( isName(  tokens[ti] )   )(args.push_back(tokens[ti++]));
      else return "";
      if (ti>=tokens.size()) return "";
      if (tokens[ti]==","){
        ti++;
        if(ti<tokens.size()&&tokens[ti]==")") return "";
      } 
      else if (tokens[ti]!=")")return "";
    }
    if(ti>=tokens.size()) return "";
    ti++; 
  }
  if(ti<tokens.size()){
    if(tokens[ti]=="{"){
      ti++;
      args.push_back(lambda(tokens));
      if (args.back()=="") return "";
    } else return "";
  } 
  if (ti<tokens.size()) return "";

  res+="("+join(args,',')+")";
  char *p = new char[res.size()];
  strcpy(p,res.c_str());
  return p;
}

_____________________________________________________
#include <iostream>
#include <math.h>
#include <string>
#include <utility>
#include <regex>
#include <sstream>
#include <iomanip>
#include <igloo/igloo_alt.h>
#include <algorithm>
#include <set>
#include <regex>
using namespace std;
using namespace igloo;
typedef long long ll;
typedef double db;
typedef pair<int, int> pii;
typedef vector<int> vi;
typedef vector<pii> vpii;
typedef vector<vi> vvi;
typedef vector<bool> vb;
typedef vector<string> vs;
typedef vector<char> vc;
typedef vector<vc> vvc;
typedef vector<char> NAMENUM;
typedef vvc LAM_PARAM;
typedef vvc LAM_STMT;
typedef pair<vvc, vvc> LAMBDA;

#define REP(i,a,b) for (int i=a; i<=b; i++)
#define REPR(i,a,b) for (int i=a; i>=b; i--)
#define fa(i,v) for (auto i: v)
#define all(c) c.begin(), c.end()
#define sz(x) ((int)((x).size()))
#define what_is(x) cerr << #x << " is " << x << "\n";
#define F first
#define S second
#define pb push_back
#define shift _shift(tokens)

bool fail = false;

void split(const string &s, char delim, vector<string> &elems) {
    stringstream ss(s);
    string item;
    while (getline(ss, item, delim)) {
        elems.push_back(item);
    }
}

vector<string> split(const string &s, char delim) {
    vector<string> elems;
    split(s, delim, elems);
    return elems;
}

bool include(vc& tokens, char c, vc v) {
    return tokens.empty() == false and find(all(v), c) != v.end();
}

void pr(vc& tokens) {
    fa(i, tokens) cout << i; cout << endl;
}

void _shift(vc &tokens)
{
    if (tokens.empty()) return;
    assert(!tokens.empty());
    tokens.erase(tokens.begin());
}

void skip(vc& tokens, vc ifEqual) {
    while (tokens.empty() == false and find(all(ifEqual), tokens.front()) != ifEqual.end() )
        shift;
}

struct NameNumber {
    string val;
    vector<char> invalid = {' ', ',', '-','(',')', '}', '\n', '{'};
    NameNumber(vc& tokens) {
        skip(tokens, {' ', '\n'});


        while (tokens.empty() == false and find(all(invalid), tokens.front()) == invalid.end()) {
            val.pb(tokens.front());
            shift;
        }
        skip(tokens, {' ', '\n'});
    }
    void print() {
        cout << "[NameNumber " + val + "] ";
    }
    NameNumber() {};
};

struct LambdaComponent {
    vector<NameNumber> val;
    int type = -1;
    bool isnil = true;
    LambdaComponent(vc& tokens, int type, vc separators, vc ender) {
        while (!include(tokens, tokens.front(), ender) and tokens.empty() == false) {
            if (include(tokens, tokens.front(), separators)) shift;
            val.pb(NameNumber(tokens));
        }
        while (include(tokens, tokens.front(), ender)) shift;
        this->type = type;
        isnil = val.empty();
    }

    LambdaComponent() {};

    void print() {
        cout << "[" << (type == 0 ? "LAMBDA_PARAM" : "LAMBDA_STMT") << " ";
        if (isnil) cout << "NIL";
        fa(i, val) i.print();
        cout << "]";
    }
    string trans() {
        if (val.empty()) return "";
        string res = "";
        for (int i = 0; i<sz(val)-1; i++) {
            res += val[i].val + ",;"[type];
        }
        res += val[sz(val)-1].val + (type == 1 ? ";" : "");
        return res;
    }
};

struct Lambda {
    LambdaComponent lambdaparams, lambdastmts;
    bool empty = true;
    bool isnil = true;
    Lambda(vc& tokens) {
        skip(tokens, {' ', '\n'});
        if (tokens.front() != '{') {
            return;
        }
        shift;
        bool hasParam = false;
        for (int i = 0; i < sz(tokens); i++) {
            if (tokens[i] == '}') break;
            hasParam |= tokens[i] == '-';
        }
        if (hasParam)
            lambdaparams = LambdaComponent(tokens, 0, {' ', ','}, {'-', '>'});
        else
            lambdaparams.type = 0;
        bool hasStmt = false;
        for (int i = 0; i < sz(tokens); i++) {
            if (tokens[i] == '}') break;
            hasStmt |= isalnum(tokens[i]);
        }
        if (hasStmt)
            lambdastmts = LambdaComponent(tokens, 1, {' '}, {'}'});
        else {
            lambdastmts.type = 1;
            shift;
        }
        empty = lambdastmts.isnil and lambdaparams.isnil;
        isnil = false;
    }


    void print() {
        cout << "[LAMBDA\n";
        if (isnil)
            cout << "\t" << "NIL\n";
        else if (empty)
            cout << "\t" << "EMPTY\n";
        else {

            cout << "\t"; lambdaparams.print(); cout << "\n";
            cout << "\t"; lambdastmts.print(); cout << "\n";
        }
        cout << "]";
    }
    Lambda() {};

    string trans() {
        return "(" + lambdaparams.trans() + "){" + lambdastmts.trans() + "}";
    }
};

struct Exp {
    Lambda _lambda;
    NameNumber _nameNumber;
    enum TypeExpression {LambdaType, NameType, Nil};
    TypeExpression type = Nil;
    Exp(vc& tokens) {
        skip(tokens, {' ', '\n'});
        skip(tokens, {' ', '\n'});
        if (tokens.front() == ')') {
            return;
        }
        if (tokens.front() == '{') {
            _lambda = Lambda(tokens);
            type = LambdaType;
        }
        else  {
            _nameNumber = NameNumber(tokens);
            type = NameType;
        }
    }

    void print() {
        cout << "[EXP ";
        if (_lambda.isnil)
            _nameNumber.print();
        else
            _lambda.print();
        cout << "]\n";
    }
    Exp() {};

    string trans() {
        if (_lambda.isnil)
            return _nameNumber.val;
        return _lambda.trans();
    }
};

struct Parameter {
    vector<Exp> _expressions;
    bool isnil = true;
    bool empty = true;
    Parameter(vc& tokens) {
        skip(tokens, {' ', '\n'});
        if (tokens.front() != '(') {
            cout << "Not found parameter\n";
            cout << "End Parsing parameter \n";
            return;
        }
        shift;
        skip(tokens, {' ', '\n'});
        if (tokens.front() == ',' or tokens.front() == '-') return;
        while (!include(tokens, tokens.front(), {')'}) and tokens.empty() == false) {
            if (include(tokens, tokens.front(), {',', ' ', '\n'})) shift;
            _expressions.pb(Exp(tokens));
        }
        while (include(tokens, tokens.front(), {')'})) shift;
        isnil = false;
        empty = _expressions.empty();
    }

    Parameter() {};
    void print() {
        cout << "[FUNC_PARAM ";
        if (isnil) cout << "NIL";
        else if (empty) cout << "EMPTY";
        else {
            cout << sz(_expressions) << "\n";
            fa(i, _expressions) i.print();
        }
        cout << "]\n";
    }
    string trans() {
        string res = "";
        if (empty) return "";
        for (int i = 0; i<sz(_expressions)-1; i++) {
            res += _expressions[i].trans() + ",";
        }
        res += _expressions[sz(_expressions)-1].trans();
        return res;
    }
};

struct Function {
    Exp _expression;
    Parameter _parameter;
    Lambda _lamda;
    bool isnil = true;
    Function(vc& tokens) {
        skip(tokens, {' ', '\n'});
        if (tokens.front() == '(')
            return;
        _expression = Exp(tokens);
        skip(tokens, {' ', '\n'});

        if (tokens.front() == '(') {
            _parameter = Parameter(tokens);
            if (_parameter.isnil) return;
            skip(tokens, {' ', '\n'});
            if (tokens.front() == '{') {
                _lamda = Lambda(tokens);
                skip(tokens, {' ', '\n','}'});
                if (tokens.empty() == false) {
                    isnil = true;
                    return;
                }

            }

            else if (tokens.empty() == false) {
                isnil = true;
                return;
            }
        } else {
            if (tokens.front() == '{')
                _lamda = Lambda(tokens);
            else if (tokens.empty() == false) {
                isnil = true;
                return;
            }
        }
        isnil = false;
    }

    void print() {
        cout << "\nFUNCTION DESCRIPTION\n";
        cout << "------------------------\n";
        cout << "FUNCTION EXPRESSION\n";
        _expression.print();
        cout << "------------------------\n";
        cout << "FUNCTION PARAMETERS\n";
        _parameter.print();
        cout << "------------------------\n";
        cout << "FUNCTION LAMBDA\n";
        _lamda.print();
        cout << "------------------------\n";
    }

    string trans() {
        if (_parameter.empty and _lamda.isnil) {
            return _expression.trans() + "()";
        }
        if (_parameter.isnil or _parameter.empty) {
            return _expression.trans() + "(" + _lamda.trans() + ")";
        }
        return _expression.trans() + "(" + _parameter.trans() + (_lamda.isnil ? "" : "," + _lamda.trans() ) + ")";
    }
};

bool checkValidName(string s) {
    char change_to = ' ';
    set<char> otherChars = {'-','>', ',','(',')','{','}'};

    auto transformation_operation = [otherChars, change_to](char c)
    {
        return otherChars.count(c) ? change_to : c;
    };
    std::transform(s.begin(), s.end(), s.begin(), transformation_operation);
    auto names = split(s, ' ');
    fa(i, names) {
        bool allDigit = true;
        fa(j, i) if (!isdigit(j)) allDigit = false;
        if (i!="" and isdigit(i[0]) and !allDigit) return false;
    }
    return true;
}


const char *transpile (const char* e) {
    cout << "#" << e  << "#" << endl;
    if (e == "") return "";
    vc tokens;
    vc invalidCharacter = {'%','^', '&', '*'};
    string tmp = string(e);
    if (!checkValidName(tmp)) return "";
    int cntParen = 0, cntCurly = 0;
    fa(i, tmp) {
        if (i == '(') cntParen ++;
        else if (i == '{') cntCurly++;
        else if (i == ')') {
            cntParen--;
            if (cntParen<0) return "";
        } else if (i == '}') {
            cntCurly--;
            if (cntCurly<0) return "";
        }
    }
    if (cntCurly or cntParen) return "";
    std::smatch m;
    regex nonComma("\\([\\s\\n]*\\w[\\s\\n]+\\w.*\\)|^[\\s\\n]*$|\\{[\\s\\n]*->|(\\{\\}){3,}|\\{[\\s\\n]*\\w[\\s\\n]+\\w.*\\}|->.*\\w[\\s\\n]*,[\\s\\n]*\\w\\}|,\\w\\s+[a-z]+\\}");
    if (regex_search(tmp, m, nonComma)) return "";

    fa(iter, tmp) {
        if (find(all(invalidCharacter), iter) != invalidCharacter.end())
            return "";
        tokens.pb(iter == '\n' ? ' ' : iter);
    }
    Function func(tokens);
    auto res = func.trans();

    cout << res << endl;
    cout << "@@" << func.isnil << endl;

    if (fail or func.isnil) return "";
    if (res.find(",)") != string::npos) return "";

    char *y = new char[res.length() + 1];

    std::strcpy(y, res.c_str());
    return y;
}

_____________________________________________________
#include <iostream>
#include <vector>

using namespace std;




bool invalid_character(char ch)
{
    if (ch == '_' || ch == ' ' || ch == '\n' || ch == ',' || ch == '('|| ch == ')'|| ch == '{' || ch == '}' || ch == '\0'){return false;}
    if (ch < '0'){return true;}
    if (ch <'A' && ch >'9'){return true;}
    if (ch > 'Z' && ch <'a'){return true;}
    if (ch > 'z'){return true;}
    
    return false;
}
void increase_size(char* &code, int& size)
{
    int n_size = 2*size;
    char* n_code = new char(n_size);
    for (int i = 0; i< size; i++)
    {
        *(n_code + i) = *(code + i);
    }
    size = n_size;
    code = n_code;
}
bool invalid_name_num(string str)
{
    bool num = false;
    if (str.length() == 0){return true;}
    if (str[0] >= '0' && str[0] <= '9'){num = true;}
    
    for (int i = 1; i< str.length(); i++)
    {
        if (num)
        {
            if (str[i] > '9'){return true;}
        }
    }
    return false;
}

string get_name_num (const char* &code, bool& invalid)
{
    string entry = "";
    while (*code != ' ' && *code != '\n' && *code != ',' && *code != '(' && *code != ')' && *code != '{' && *code != '}'&& *code != '\0' && *code != '-')
    {
        if (invalid_character(*code)){invalid = true; return "";}
        entry+= *code;
        code++;
    }
    if (invalid_name_num(entry)){invalid = true; return "";}
    return entry;
}

void trpile_name_num(string entry, char* &dart_code, int &size, int& i)
{
    long len = entry.length();
    for (int j = 0; j< len; j++)
    {
        if (i >= size){increase_size(dart_code, size);}
        *(dart_code + i) = entry[j];
        i++;
    }
}

bool lp_exists(const char* code)
{
    while (*code != '-' || *(code + 1) != '>')
    {
        if (*code == '}'){return false;}
        code++;
    }
    return true;
}
void lambda_parameter(const char* &code, char* &dart_code, int &size, bool &invalid, int& i)
{
    *(dart_code+ i) = '('; i++;
    if (*code == '{'){code++;}
    
    if (!lp_exists(code))
    {
        if (i+1 >= size){increase_size(dart_code, size);}
        *(dart_code + i) = ')'; i++;
        *(dart_code + i) = '{'; i++;
        return;
    }
    
    string entry = "";
    bool value = false;
  while (*code != '-' || *(code + 1) != '>')
    {
        while (*code == ' ' || *code == '\n'){code++;}
        if (*code == '}')
        {
            break;
        }
        else if (*code == ',')
        {
            if (!value){invalid = true; return;}
            if (i>= size){increase_size(dart_code, size);}
            *(dart_code + i) = *code; i++;
            code++;
            value = false;
        }
        else if (*code == '-' && *(code + 1) == '>')
        {
            if (!value){invalid = true; return;}
            code+=2;
            break;
        }
        else
        {
            if (value ){invalid = true; return;}
            entry = get_name_num(code, invalid);
            if (invalid){return;}
            trpile_name_num(entry, dart_code, size, i);
            value = true;
        }
        
            
    }
    if (*code == '-' && *(code + 1) == '>')
    {
      if (!value){invalid = true; return;}
      code+=2;
    }
    if (i+1 >= size){increase_size(dart_code, size);}
    *(dart_code + i) = ')'; i++;
    *(dart_code + i) = '{'; i++;
}

void lamda_stmt(const char* &code, char*& dart_code, int &size, int&i, bool &invalid)
{
    string entry = "";
    while ( *code != '}')
    {
        while (*code == ' ' || *code == '\n'){code++;}
        
        if (*code == '}')
        {
            if (i  >= size){increase_size(dart_code, size);}
            *(dart_code + i) = '}'; i++;
            code++;
            break;
        }
        else
        {
            entry = get_name_num(code, invalid);
            if (invalid){return;}
            trpile_name_num(entry, dart_code, size, i);
            if (i>= size){increase_size(dart_code, size);}
            *(dart_code + i) = ';' ; i++;
        }
        
        
    }
    if (*code == '}')
    {
        if (i  >= size){increase_size(dart_code, size);}
        *(dart_code + i) = '}'; i++;
        code++;
    }
}

void lamda(const char* &code, char*& dart_code, int &size, int&i, bool &invalid)
{
    lambda_parameter(code, dart_code, size, invalid, i);
    if (invalid){return;}
    lamda_stmt(code, dart_code, size, i, invalid);
    if (invalid){return;}
}
bool empty_para(const char *code)
{
    if (*code == ',' ){code++;}
    while (*code == ' ' || *code == '\n')
    {
        code++;
    }
    if (*code == ',' || *code == ')'){return true;}
    else {return false;}
}
bool empty_brackets(const char *code)
{
    if (*code == '('){code++;}
    while (*code == ' ' || *code == '\n')
    {
        code++;
    }
    if ( *code == ')'){return true;}
    else {return false;}
}
void parameters (const char* &code, char*& dart_code, int &size, int&i, bool &invalid)
{
    string entry = "";
    bool value = false;
    while ( *code != ')')
    {
        while (*code == ' ' || *code == '\n'){code++;}
        
        if (*code == ',')
        {
            if (i >= size){increase_size(dart_code, size);}
            if (!value){invalid = true;return;}
            if (empty_para(code)){invalid = true; return;}
            
            *(dart_code + i) = *code; i++;
            code++;
            value = false;
        }
        else if (*code == ')')
        {
            break;
        }
        else if (*code == '{')
        {
            if (value ){invalid = true; return;}

            value = true;
            lamda(code, dart_code, size, i, invalid);
            if (invalid){return;}

        }
        else
        {
            if (value ){invalid = true; return;}
            entry = get_name_num(code, invalid);
            if (invalid){return;}
            trpile_name_num(entry, dart_code, size, i);
            value = true;
        }
    }
    if (*code == ')'){code++;}
}

void expression(const char* &code, char*& dart_code, int &size, int&i, bool &invalid)
{
    while (*code != '(')
    {
        while (*code == ' ' || *code == '\n'){code++;}
        
        if (*code == '(')
        {
            return;
        }
        else if (*code == '{')
        {
            break;
            lamda(code, dart_code, size, i, invalid);
            if (invalid){return;}
        }
        else
        {
            string entry = get_name_num(code, invalid);
            if (invalid){return;}
            trpile_name_num(entry, dart_code, size, i);
        }
    }
}
void print(const char* ans)
{
    while (*ans!= '\0')
    {
        cout<<*(ans);
        ans++;
    }
  cout<<endl;
}

const char *transpile (const char* code)
{
    print(code);
    int gl_size = 100;
    char* dart_code = new char[gl_size];
    
    int i = 0;
    bool invalid_ch = false;
    bool paras = false;
    bool first_exp = false;
    bool second_exp = false;
    if (*code == '\0'){return "";}
    while (*code != '\0')
    {
        while((*code == '\n' || *code == ' ')){code++;}
        if (*code == '\0'){break;}
        if (invalid_character(*code)){return "";}
        if (paras && *code != '{'){return "";}
        if (*code == '{')
        {
            if (second_exp){return "";}
            if (first_exp){second_exp = true;}
            if (first_exp && !paras)
            {
                if (i >= gl_size){increase_size(dart_code, gl_size);}
                *(dart_code + i) = '('; i++;
                paras = true;
            }
            lamda(code, dart_code, gl_size, i, invalid_ch);
            if (invalid_ch){return "";}
            if (first_exp)
            {
                while (*code == ' ' || *code == '\n'){code++;}
                if (*code == '{')
                {
                    if (i >= gl_size){increase_size(dart_code, gl_size);}
                    *(dart_code + i) = ',';i++;
                    continue;
                    
                }
            }
            first_exp = true;
        }
        else if (*code == '(')
        {
            if (!first_exp){return "";}
            bool empty_par = false;
            if (empty_brackets(code)){empty_par = true;}

            if (i >= gl_size){increase_size(dart_code, gl_size);}
            *(dart_code + i) = '('; i++; code++;
            parameters(code, dart_code, gl_size, i, invalid_ch);

            if (invalid_ch){return "";}
            paras = true;
            
            while (*code == ' ' || *code == '\n'){code++;}

            if (*code == '{')
            {
                if (empty_par){continue;}
                if (i >= gl_size){increase_size(dart_code, gl_size);}
                *(dart_code + i) = ',';i++;
                continue;
                
            }
        }
        else
        {
            first_exp = true;
            expression(code, dart_code, gl_size, i, invalid_ch);
            if (invalid_ch){return "";}
        }
        
        
    }
    if (i == 0){return "";}
    if (i >= gl_size){increase_size(dart_code, gl_size);}
    *(dart_code + i) = ')';i++;
    
    
    char* ans = new char[i+1];
    for (int j = 0; j< i; j++)
    {
        *(ans + j) = *(dart_code + j);
    }
    *(ans + i) = '\0';
    
    
    return ans;
}
_____________________________________________________
#include <iostream>
#include <sstream>
#include <unordered_map>
#include <stack>
#include <cstring>
#include <vector>

struct Expr {
  virtual std::ostream& print(std::ostream& out) const {
    out << "EXPR";
    return out;
  }

  friend std::ostream& operator<<(std::ostream& os, const Expr& expr) {
    return expr.print(os);
  }
};

struct Id : Expr {
  virtual std::ostream& print(std::ostream& out) const {
    out << "ID";
    return out;
  }
};

struct Lambda : Expr {
  private:
    bool signalled;
  
  public:
  std::vector<Id *> parameters;
  std::vector<Id *> statements;

  void no_params() {
    signalled = true;
    if(parameters.size() > 1) {
      throw std::exception();
    }
    if(parameters.size() == 1) {
      //std::cout << "no params" << std::endl;
      Id *temp = parameters.back();
      parameters.pop_back();
      statements.push_back(temp);
    }
  }

  void signal() {
    if(!signalled) {
      signalled = true;
    }
  }

  void insert(Id *id) {
    if(!signalled) {
      parameters.push_back(id);
    } else {
      statements.push_back(id);
    }
  }

  virtual std::ostream& print(std::ostream& out) const {
    out << "(";
    if(parameters.size() > 0) {
      out << **parameters.begin();
      for(auto it = parameters.begin() + 1; it != parameters.end(); it++) {
        out << "," << **it;
      }
    }
    out << "){";
    for(auto *id : statements) {
      out << *id << ";";
    }
    out << "}";
    return out;
  }
};

struct Name : Id {
  const std::string name;
  Name(std::string name) : name(name) {};

  virtual std::ostream& print(std::ostream& out) const {
    out << name;
    return out;
  }
};

struct Number : Id {
  const int val;
  Number(int val) : val(val) {};

  virtual std::ostream& print(std::ostream& out) const {
    out << val;
    return out;
  }
};

struct Func {
  private:
    int tracker = 0;
    bool in_lambda = false;
  public:
  Expr* first = NULL;
  std::vector<Expr*> parameters;
  Lambda* lambda = NULL;

  friend std::ostream& operator<<(std::ostream& os, const Func& func) {
    if(func.first == nullptr) {
      os << "FIRST_NULL";
    } else {
      os << *func.first;
    }
    std::vector<Expr *> temp = func.parameters;
    if(func.lambda != nullptr)
      temp.push_back(func.lambda);
    os << '(';
    if(temp.size() > 0) {
      os << **temp.begin();
      for(std::vector<Expr *>::iterator it = temp.begin() + 1; it != temp.end(); it++) {
        os << "," << **it;
      }
    }
    os << ')';
    
    return os;
  }

  void update() {
    tracker++;
  }

  void signal() {
    switch(tracker) {
      case 0: {
        if(Lambda *l = dynamic_cast<Lambda *>(first)) {
          l->signal();
        }
        break;
      }
      case 1: {
        if(in_lambda) {
          //std::cout << "in lambda" << std::endl;
          for(auto it = parameters.rbegin(); it != parameters.rend(); it++) {
            if(Lambda *l = dynamic_cast<Lambda *>(*it)) {
              //std::cout << "found last lambda" << std::endl;
              l->signal();
              break;
            }
          }
        }
        break;
      }
      case 2: {
        if(this->lambda != nullptr)
          this->lambda->signal();
        break;
      }
    }
  }

  void no_params() {
    switch(tracker) {
      case 0: {
        if(Lambda *l = dynamic_cast<Lambda *>(first)) {
          l->no_params();
        }
        break;
      }
      case 1: {
        if(in_lambda) {
          //std::cout << "in lambda" << std::endl;
          for(auto it = parameters.rbegin(); it != parameters.rend(); it++) {
            if(Lambda *l = dynamic_cast<Lambda *>(*it)) {
              //std::cout << "found last lambda" << std::endl;
              l->no_params();
              break;
            }
          }
        }
        break;
      }
      case 2: {
        this->lambda->no_params();
        break;
      }
    }
  }

  void set_in_lambda(bool val) {
    this->in_lambda = val;
  }

  void insert(Expr *expr) {
    //std::cout << "insert" << std::endl;
    switch(tracker) {
      case 0: {
        //std::cout << "first" << std::endl;
        if(this->in_lambda) {
          //std::cout << "in lambda" << std::endl;
          if(Lambda *l = dynamic_cast<Lambda *>(first)) {
            l->insert(dynamic_cast<Id *>(expr));
          }
        } else {
          //std::cout << "not in lambda" << std::endl;
          first = expr;
        }
        break;
      }
      case 1: {
        //std::cout << "second" << std::endl;
        if(this->in_lambda) {
          //std::cout << "in lambda" << std::endl;
          for(auto it = parameters.rbegin(); it != parameters.rend(); it++) {
            if(Lambda *l = dynamic_cast<Lambda *>(*it)) {
              //std::cout << "found last lambda" << std::endl;
              l->insert(dynamic_cast<Id *>(expr));
              break;
            }
          }
        } else {
          //std::cout << "not in lambda" << std::endl;
          parameters.push_back(expr);
        }
        break;
      }
      case 2: {
        //std::cout << "third" << std::endl;
        if(this->in_lambda) {
          //std::cout << "in lambda" << std::endl;
          this->lambda->insert(dynamic_cast<Id *>(expr));
        } else {
          //std::cout << "not in lambda" << std::endl;
          this->lambda = dynamic_cast<Lambda *>(expr);
        }
        break;
      }
    }
    //std::cout << "end of insert" << std::endl;
  }
};

enum Token {
  //NTS ⇒ Non Terminal Symbol
  NTS_Start,                    //  S
  NTS_Function,                 //  F
  NTS_Function_prime,           //  F'
  NTS_Expression,               //  E
  NTS_Parameters,               //  P
  NTS_Parameters_prime,         //  P'
  NTS_Lambda,                   //  L
  NTS_Lambda_prime,             //  L'
  NTS_Lambda_1,                 //  L1
  NTS_Lambda_2,                 //  L2
  NTS_Lambda_Parameters,        //  Lp
  NTS_Lambda_Parameters_prime,  //  Lp'
  NTS_Lambda_Statements,        //  Ls
  NTS_Name,                     //  N
  NTS_Value,                    //  V
  NTS_Value_prime,              //  V'
  NTS_Identifier,               //  I
  NTS_Identifier_prime,         //  I'

  //TS ⇒ Terminal Symbol
  TS_Letter,                    //  a .. z A .. Z
  TS_Digit,                     //  0 .. 9
  TS_Underscore,                //  _
  TS_Comma,                     //  ,
  TS_Arrow_Dash,                //  -
  TS_Arrow_Head,                //  >
  TS_Bracket_Open,              //  (
  TS_Bracket_Close,             //  )
  TS_Brace_Open,                //  {
  TS_Brace_Close,               //  }
  TS_Whitespace,                //  '  ' '\t' '\n' '\r'
  TS_EOS,                       //  '\0'
  TS_INVALID                    //  Anything not caught
};

const Token lexer(const char c) {
  if(isalpha(c)) {
    return TS_Letter;
  } else if(isdigit(c)) {
    return TS_Digit;
  } else if(isspace(c)) {
    return TS_Whitespace;
  } else {
    switch(c) {
      case '_': return TS_Underscore;
      case ',': return TS_Comma;
      case '-': return TS_Arrow_Dash;
      case '>': return TS_Arrow_Head;
      case '(': return TS_Bracket_Open;
      case ')': return TS_Bracket_Close;
      case '{': return TS_Brace_Open;
      case '}': return TS_Brace_Close;
      case  0 : return TS_EOS;
      default : return TS_INVALID;
    }
  }
}

const std::unordered_map<Token, std::unordered_map<Token, int>> set_up_parse_table() {
  return std::unordered_map<Token, std::unordered_map<Token, int>>({
    {NTS_Start, {{TS_Letter,    1},
                {TS_Digit,      1},
                {TS_Underscore, 1},
                {TS_Brace_Open, 1},
                {TS_Whitespace, 50}}
    },
    {NTS_Function,  {{TS_Letter,    2},
                    {TS_Digit,      2},
                    {TS_Underscore, 2},
                    {TS_Brace_Open ,2},
                {TS_Whitespace, 50}}
    },
    {NTS_Function_prime,  {{TS_Bracket_Open,  4},
                          {TS_Brace_Open,     3},
                {TS_Whitespace, 50}}
    },
    {NTS_Expression,  {{TS_Letter,    5},
                      {TS_Digit,      5},
                      {TS_Underscore, 5},
                      {TS_Brace_Open ,6},
                {TS_Whitespace, 50}}
    },
    {NTS_Parameters,  {{TS_Letter,    7},
                      {TS_Digit,      7},
                      {TS_Underscore, 7},
                      {TS_Brace_Open ,7},
                      {TS_Bracket_Close, 34},
                {TS_Whitespace, 50}}
    },
    {NTS_Parameters_prime,  {{TS_Comma,         9},
                            {TS_Bracket_Close,  8},
                {TS_Whitespace, 50}}
    },
    {NTS_Lambda, {{TS_Brace_Open, 10},
                  {TS_EOS,        32},
                {TS_Whitespace, 50}}
    },
    {NTS_Lambda_prime,  {{TS_Brace_Open,  33},
                         {TS_EOS,         32},
                {TS_Whitespace, 50}}
    },
    {NTS_Lambda_1,  {{TS_Letter,    12},
                    {TS_Digit,      12},
                    {TS_Underscore, 12},
                    {TS_Brace_Close,11},
                {TS_Whitespace, 50}}
    },
    {NTS_Lambda_2,  {{TS_Letter,    14},
                    {TS_Digit,      14},
                    {TS_Underscore, 14},
                    {TS_Arrow_Dash, 31},
                    {TS_Comma,      13},
                    {TS_Brace_Close,14},
                {TS_Whitespace, 50}}
    },
    {NTS_Lambda_Parameters, {{TS_Letter,    15},
                            {TS_Digit,      15},
                            {TS_Underscore, 15},
                {TS_Whitespace, 50}}
    },
    {NTS_Lambda_Parameters_prime, {{TS_Comma,     17},
                                  {TS_Arrow_Dash, 16},
                {TS_Whitespace, 50}}
    },
    {NTS_Lambda_Statements, {{TS_Letter,    19},
                            {TS_Digit,      19},
                            {TS_Underscore, 19},
                            {TS_Brace_Close,18},
                {TS_Whitespace, 50}}
    },
    {NTS_Name, {{TS_Letter,     21},
                {TS_Digit,      20},
                {TS_Underscore, 21},
                {TS_Whitespace, 50}}
    },
    {NTS_Value, {{TS_Digit, 22}}
    },
    {NTS_Value_prime, {{TS_Digit,         24},
                       {TS_Comma,         23},
                       {TS_Arrow_Dash,    23},
                       {TS_Bracket_Open,  23},
                       {TS_Bracket_Close, 23},
                       {TS_Brace_Open,    23},
                       {TS_Brace_Close,   23},
                       {TS_Whitespace,    23},}
    },
    {NTS_Identifier,  {{TS_Letter,     25},
                       {TS_Underscore, 26}}
    },
    {NTS_Identifier_prime, {{TS_Letter,       28},
                           {TS_Digit,         29},
                           {TS_Underscore,    30},
                           {TS_Comma,         27},
                           {TS_Arrow_Dash,    27},
                           {TS_Bracket_Open,  27},
                           {TS_Bracket_Close, 27},
                           {TS_Brace_Open,    27},
                           {TS_Brace_Close,   27},
                           {TS_Whitespace,    27},}
    },
    {TS_EOS, {{TS_Whitespace, 50}}
    }
  });
}


const char *transpile(const char *expression) {
  std::cout << expression << std::endl;
  static const std::unordered_map<Token, std::unordered_map<Token, int>>table = set_up_parse_table();
  std::stack<Token> symbol_stack({TS_EOS, NTS_Start});

  std::string result;
  std::string buffer;

  Func func;

  while(symbol_stack.size() > 0) {
    //std::cout << std::endl;
    if(lexer(*expression) == TS_INVALID) {
      expression++;
    } else if (lexer(*expression) == symbol_stack.top()) {
      if(lexer(*expression) == TS_Bracket_Close) {
        //std::cout << "end of parameters" << std::endl;
        func.update();
      }
      if(lexer(*expression) == TS_Brace_Close) {
        //std::cout << "end of lambda" << std::endl;
        func.set_in_lambda(false);
      }
      result.push_back(*expression);
      buffer.push_back(*expression);
      expression++;
      symbol_stack.pop();
    } else {
      ////std::cout << "  RULE " << table.at(symbol_stack.top()).at(lexer(*expression)) << ", char = " << *expression << ", top = " << symbol_stack.top() << ", size = " << symbol_stack.size() << std::endl;
      int rule;
      try {
        rule = table.at(symbol_stack.top()).at(lexer(*expression));
      } catch (std::out_of_range e) {
        return "";
      }
      switch(rule) {
        case 1:   //  S → F 
          symbol_stack.pop();
          symbol_stack.push(NTS_Function);
          break;
        case 2:   //  F → E F' L 
          symbol_stack.pop();
          //symbol_stack.push(NTS_Lambda);
          symbol_stack.push(NTS_Function_prime);
          symbol_stack.push(NTS_Expression);
          break;
        case 3:   //  F' → L
          func.update();
          func.update();
          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda);
          break;
        case 4:   //  F' → "(" P ")" L'
          //std::cout << "start of parameters" << std::endl;
          func.update();

          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda_prime);
          symbol_stack.push(TS_Bracket_Close);
          symbol_stack.push(NTS_Parameters);
          symbol_stack.push(TS_Bracket_Open);
          break;
        case 5:   //  E → N 
          symbol_stack.pop();
          symbol_stack.push(NTS_Name);
          break;
        case 6:   //  E → L 
          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda);
          break;
        case 34:  //  P   → ε
          symbol_stack.pop();
          break;
        case 7:   //  P → E P' 
          symbol_stack.pop();
          symbol_stack.push(NTS_Parameters_prime);
          symbol_stack.push(NTS_Expression);
          break;
        case 8:   //  P' → ε 
          symbol_stack.pop();
          break;
        case 9:   //  P' → "," P 
          symbol_stack.pop();
          symbol_stack.push(NTS_Parameters_prime);
          symbol_stack.push(NTS_Expression);
          symbol_stack.push(TS_Comma);
          break;
        case 32:  //  L'  → ε
          symbol_stack.pop();
          break;
        case 33:  //  L'  → L
          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda);
          break;
        case 10:  //  L → "{" L1 "}" 
          //std::cout << "start of lambda" << std::endl;
          func.insert(new Lambda);
          func.set_in_lambda(true);
          symbol_stack.pop();
          symbol_stack.push(TS_Brace_Close);
          symbol_stack.push(NTS_Lambda_1);
          symbol_stack.push(TS_Brace_Open);
          break;
        case 11:  //  L1 → ε 
          symbol_stack.pop();
          break;
        case 12:  //  L1 → N L2 
          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda_2);
          symbol_stack.push(NTS_Name);
          break;
        case 13:  //  L2 → ',' Lp "->" Ls
          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda_Statements);
          symbol_stack.push(TS_Arrow_Head);
          symbol_stack.push(TS_Arrow_Dash);
          symbol_stack.push(NTS_Lambda_Parameters);
          symbol_stack.push(TS_Comma);
          break;
        case 31:  //  L2 → "->" Ls 
          func.signal();
          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda_Statements);
          symbol_stack.push(TS_Arrow_Head);
          symbol_stack.push(TS_Arrow_Dash);
          break;
        case 14:  //  L2  → Ls
          func.no_params();
          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda_Statements);
          break;
        case 15:  //  Lp → N Lp' 
          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda_Parameters_prime);
          symbol_stack.push(NTS_Name);
          break;
        case 16:  //  Lp' → ε 
          func.signal();
          symbol_stack.pop();
          break;
        case 17:  //  Lp' → "," Lp 
          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda_Parameters);
          symbol_stack.push(TS_Comma);
          break;
        case 18:  //  Ls → ε 
          symbol_stack.pop();
          break;
        case 19:  //  Ls → N Ls 
          symbol_stack.pop();
          symbol_stack.push(NTS_Lambda_Statements);
          symbol_stack.push(NTS_Name);
          break;
        case 20:  //  N → V 
          buffer.clear();

          symbol_stack.pop();
          symbol_stack.push(NTS_Value);
          break;
        case 21:  //  N → I 
          buffer.clear();

          symbol_stack.pop();
          symbol_stack.push(NTS_Identifier);
          break;
        case 22:  //  V → d V'
          symbol_stack.pop();
          symbol_stack.push(NTS_Value_prime);
          symbol_stack.push(TS_Digit);
          break;
        case 23: { //  V' → ε 
          int r = std::stoi(buffer);
          //std::cout << r << " == end of num" << std::endl;
          func.insert(new Number(r));
          symbol_stack.pop();
          break;
        }
        case 24:  //  V' → V 
          symbol_stack.pop();
          symbol_stack.push(NTS_Value);
          break;
        case 25:  //  I → c I' 
          symbol_stack.pop();
          symbol_stack.push(NTS_Identifier_prime);
          symbol_stack.push(TS_Letter);
          break;
        case 26:  //  I → '-' I' 
          symbol_stack.pop();
          symbol_stack.push(NTS_Identifier_prime);
          symbol_stack.push(TS_Underscore);
          break;
        case 27: { //  I' → ε 
          std::string r = buffer;
          //std::cout << r << " == end of name" << std::endl;
          func.insert(new Name(r));
          symbol_stack.pop();
          break;
        }
        case 28:  //  I' → c I' 
          symbol_stack.pop();
          symbol_stack.push(NTS_Identifier_prime);
          symbol_stack.push(TS_Letter);
          break;
        case 29:  //  I' → d I' 
          symbol_stack.pop();
          symbol_stack.push(NTS_Identifier_prime);
          symbol_stack.push(TS_Digit);
          break;
        case 30:  //  I' → "_" I' 
          symbol_stack.pop();
          symbol_stack.push(NTS_Identifier_prime);
          symbol_stack.push(TS_Underscore);
          break;
        case 50:
          expression++;
          break;
        default:
          break;
      }
    }
  }
  std::cout << func << std::endl << std::endl;

  std::stringstream test;
  test <<  func;
  result = test.str();
  char *ptr = new char[result.size() + 1];
  std::strcpy(ptr, result.c_str());
  return ptr;
}
