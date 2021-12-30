#include <string>
#include <regex>
#include <stack>
using namespace std;

vector <string> tokenize (string program) {
    static regex re ("[A-Za-z][A-Za-z0-9_]*:?|\\'[^\\']*\\'|\\d+|;.*$");
    sregex_token_iterator it (program.begin (), program.end (), re);
    return vector <string> (it, sregex_token_iterator ());
}
int val(string s,unordered_map<string,int> regs){
  if(isdigit(s[0])) return stoi(s);
  return(regs[s]);
}  

std::string assembler_interpreter(std::string program) {
  unordered_map<string,int> regs;
  unordered_map<string,int> label;
  stack<int> retline;
  vector<vector<string>> scv;

  stringstream prog(program);
  string temp;
  while(getline(prog,temp)){
    vector<string> tok= tokenize(temp);
    if (tok.size()>0 && tok[0][0]!=';'){
      scv.push_back(tok);
      if(tok[0].back()==':') label[tok[0].substr(0,tok[0].size()-1)]=scv.size()-1;
    }
  }
  size_t cp=0;
  int cmp=0;
  string res="";
  while(cp<scv.size()){
    vector<string> sc=scv[cp];
    string cmd=sc[0];
    if(cmd=="mov") regs[sc[1]]=val(sc[2],regs);
    else if (cmd=="inc") regs[sc[1]]++;
    else if (cmd=="dec") regs[sc[1]]--;
    else if (cmd=="add") regs[sc[1]]+=val(sc[2],regs);
    else if (cmd=="sub") regs[sc[1]]-=val(sc[2],regs);
    else if (cmd=="mul") regs[sc[1]]*=val(sc[2],regs);
    else if (cmd=="div") regs[sc[1]]/=val(sc[2],regs);
    else if (cmd=="jmp") cp=label[sc[1]];
    else if (cmd=="cmp") cmp=val(sc[1],regs)-val(sc[2],regs);
    else if (cmd=="jne") { if(cmp!=0) cp=label[sc[1]];}
    else if (cmd=="je")  { if(cmp==0) cp=label[sc[1]];}
    else if (cmd=="jge") { if(cmp>=0) cp=label[sc[1]];}
    else if (cmd=="jg")  { if(cmp>0)  cp=label[sc[1]];}
    else if (cmd=="jle") { if(cmp<=0) cp=label[sc[1]];}
    else if (cmd=="jl")  { if(cmp<0)  cp=label[sc[1]];}
    else if (cmd=="call") { retline.push(cp);cp=label[sc[1]];}
    else if (cmd=="ret")  { cp=retline.top();retline.pop();}
    else if (cmd=="end")  return res;
    else if (cmd=="msg") {
      for (size_t i=1;i<sc.size();i++){
        if(sc[i][0]=='\'') res+=sc[i].substr(1,sc[i].size()-2);
        else if(sc[i][0]!=';') res+=to_string(val(sc[i],regs));
      }
    }
    cp++;
  }
  return "-1";
}

____________________________________________________
#include <string_view>
#include <optional>
#include <charconv>
#include <variant>
#include <sstream>
#include <vector>
#include <stack>
#include <map>

using Value = int;
using Register = std::string_view;
struct Msg { std::string_view msg; };

template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };
template<class... Ts> overloaded(Ts...) -> overloaded<Ts...>;

struct ImmReg {
    std::variant<Value, Register> content;

    ImmReg(std::string_view sv) {
        if (int imm; std::from_chars(sv.data(), sv.data() + sv.size(), imm).ec ==
                     std::errc())
            content = imm;
        else
            content = sv;
    }

    Value eval(std::map<Register, Value> &map) const {
        return std::visit(overloaded {
                [](const Value v) { return v; },
                [&](const Register r) { return map[r]; }
        }, content);
    }
};

namespace BinOp {
    enum Kind { None = 0, Mov, Add, Sub, Mul, Div };

    Kind from_sv(std::string_view sv) {
        if (sv == "mov") return Mov;
        if (sv == "add") return Add;
        if (sv == "sub") return Sub;
        if (sv == "mul") return Mul;
        if (sv == "div") return Div;
        return None;
    }

    struct Inst { Kind kind; Register op1; ImmReg op2; };
}

namespace UnaryOp {
    enum Kind { None = 0, Inc, Dec };

    Kind from_sv(std::string_view sv) {
        if (sv == "inc") return Inc;
        if (sv == "dec") return Dec;
        return None;
    }
    struct Inst { Kind kind; Register reg; };
}

namespace Jmp {
    enum Trait { Less = 1, Equal = 2, Greater = 4, Call = 16 };

    int compare(Value lhs, Value rhs) {
        return lhs < rhs ? Less : (rhs < lhs ? Greater : Equal);
    }

    int from_sv(std::string_view sv) {
        if (sv == "jmp") return Less | Equal | Greater;
        if (sv == "jne") return Less | Greater;
        if (sv == "je" ) return Equal;
        if (sv == "jge") return Equal | Greater;
        if (sv == "jg" ) return Greater;
        if (sv == "jle") return Less | Equal;
        if (sv == "jl" ) return Less;
        if (sv == "call")return Less | Equal | Greater | Call;
        return 0;
    }
    struct Inst { int mask; std::optional<size_t> target; };
}

struct CmpInst { ImmReg op1, op2; };
struct RetInst {};
struct MsgInst { std::vector<std::variant<Msg, Register>> args; };
struct EndInst {};

using Instruction = std::variant<BinOp::Inst, UnaryOp::Inst, Jmp::Inst, CmpInst, RetInst, MsgInst, EndInst>;

struct Lexer {
    // Data types
    struct Eof     {};
    struct NewLine {};
    struct Colon   {};
    struct Ident   { std::string_view lexeme; };
    struct Msg     { std::string_view str;    };
    using Token = std::variant<Eof, NewLine, Colon, Ident, Msg>;

    // Members
    std::string_view::const_iterator it, end;

    // Constructor
    Lexer(std::string_view program)
            : it(program.cbegin())
            , end(program.cend()) {}

    // Member functions
    void skipSpace() {
        while (it != end && *it != '\n' && (isspace(*it) || *it == ',')) { ++it; }
        if (it != end && *it == ';') {
            ++it;
            while (it != end && *it != '\n')
              ++it;
        }
    }

    Token lex() {
        skipSpace();
        if (it == end)
            return Eof();
        switch (*it) {
            default: {
                assert(isalnum(*it) || *it == '-' || *it == '_');
                auto begin = &*it;
                size_t len = 1;
                while (++it != end && (isalnum(*it) || *it == '_'))
                  ++len;
                return Ident{ std::string_view(begin, len) };
            }
            case '\n': { ++it; return NewLine(); }
            case ':': { ++it; return Colon(); }
            case '\'': {
                ++it;
                const char *begin = &*it;
                size_t len = 0;
                while (it != end && *it != '\'') { ++len; ++it; }
                assert(it != end && *it == '\'');
                ++it;
                return Msg { std::string_view(begin, len) };
            }
        }
    }

    static bool isCrEof(const Token &t) {
        return std::holds_alternative<Lexer::NewLine>(t)
               || std::holds_alternative<Lexer::Eof>(t);
    }
};

struct Parser {
    Lexer lexer;
    std::vector<Instruction> insts;
    std::map<std::string_view,
            std::pair<std::optional<size_t>, std::vector<size_t>>> label_map;

    Parser(std::string_view program) : lexer(program) {}

    auto lex() { return lexer.lex(); }

    std::vector<Instruction> parse() {
        for (;;) {
            auto maybe_i = parse_line();
            if (!maybe_i.has_value())
                break;
            insts.push_back(std::move(maybe_i.value()));
        }
      
        // Fix target
        for (auto &[_, p] : label_map) {
            assert(p.first.has_value());
            auto value = p.first.value();
            for (auto &idx : p.second) {
                auto &inst = insts[idx];
                assert(std::holds_alternative<Jmp::Inst>(inst));
                std::get<Jmp::Inst>(inst).target = value;
            }
        }
        return std::move(insts);
    }

    Lexer::Token getFirstNonNewLine() {
        auto token = lex();
        return std::holds_alternative<Lexer::NewLine>(token)
               ? getFirstNonNewLine()
               : token;
    }

    std::optional<Instruction> parse_line() {
        auto first = getFirstNonNewLine();
        if (!std::holds_alternative<Lexer::Ident>(first))
            return std::nullopt;
        auto lexeme = std::get<Lexer::Ident>(first).lexeme;

        if (auto k = BinOp::from_sv(lexeme); k) {
            auto op1 = std::get<Lexer::Ident>(lex()).lexeme;
            auto op2 = std::get<Lexer::Ident>(lex()).lexeme;
            return BinOp::Inst { k, op1, op2 };
        }

        if (auto k = UnaryOp::from_sv(lexeme); k) {
            auto reg = std::get<Lexer::Ident>(lex()).lexeme;
            return UnaryOp::Inst { k, reg };
        }

        if (auto m = Jmp::from_sv(lexeme); m) {
            auto target = std::get<Lexer::Ident>(lex()).lexeme;
            label_map[target].second.push_back(insts.size());
            return Jmp::Inst { m, std::nullopt };
        }

        if (lexeme == "cmp") {
            auto op1 = std::get<Lexer::Ident>(lex()).lexeme;
            auto op2 = std::get<Lexer::Ident>(lex()).lexeme;
            return CmpInst { op1, op2 };
        }

        if (lexeme == "ret") {
            return RetInst {};
        }

        if (lexeme == "msg") {
            decltype(MsgInst{}.args) args;
            bool cont = true;
            while (cont) {
                auto token = lex();
                std::visit(overloaded {
                        [&](const Lexer::Msg &msg) { args.push_back(Msg {msg.str}); },
                        [&](const Lexer::Ident &id) { args.push_back(id.lexeme); },
                        [&](auto _) { cont = false; }
                }, token);
            }
            return MsgInst { std::move(args) };
        }

        if (lexeme == "end") {
            return EndInst {};
        }

        lex(); // Eat ':'
        label_map[lexeme].first = insts.size();

        return parse_line();
    }
};

std::string assembler_interpreter(const std::string &program) {
    std::map<Register, Value> registers;
    std::stack<size_t> ret_stk;
    size_t pc = 0;
    int comp_result = 0;
    auto insts = Parser(program).parse();
    bool end = false;
    std::stringstream os;

    while (!end && pc < insts.size()) {
        auto &inst = insts[pc];

        std::visit(overloaded {
                [&](const BinOp::Inst &i) {
                    auto rhs = i.op2.eval(registers);
                    switch (i.kind) {
                        default: { assert("BinOp kind error" && false); }
                        case BinOp::Mov: { registers[i.op1]  = rhs; break; }
                        case BinOp::Add: { registers[i.op1] += rhs; break; }
                        case BinOp::Sub: { registers[i.op1] -= rhs; break; }
                        case BinOp::Mul: { registers[i.op1] *= rhs; break; }
                        case BinOp::Div: { registers[i.op1] /= rhs; break; }
                    }
                },

                [&](const UnaryOp::Inst &i) {
                    switch (i.kind) {
                        default: assert("Uop kind error" && false);
                        case UnaryOp::Inc: { ++registers[i.reg]; break; }
                        case UnaryOp::Dec: { --registers[i.reg]; break; }
                    }
                },

                [&](const Jmp::Inst &i) {
                    if (i.mask & Jmp::Call) {
                        ret_stk.push(pc);
                        pc = i.target.value() - 1;
                    } else if (i.mask & comp_result) {
                        pc = i.target.value() - 1;
                    }
                },

                [&](const CmpInst &i) {
                    auto lhs = i.op1.eval(registers);
                    auto rhs = i.op2.eval(registers);
                    comp_result = Jmp::compare(lhs, rhs);
                },

                [&](const RetInst &i) {
                    pc = ret_stk.top();
                    ret_stk.pop();
                },

                [&](const MsgInst &i) {
                    for (const auto &arg: i.args) {
                        std::visit(overloaded {
                                [&](const Msg        m) { os << m.msg; },
                                [&](const Register reg) { os << registers[reg]; },
                        }, arg);
                    }
                },

                [&](const EndInst &i) {
                    end = true;
                },

        }, inst);

        ++pc;
    }

    return end ? os.str() : "-1";
}

____________________________________________________
#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <stack>
#include <algorithm>
//----------------------------------------------------------------------------------
class Cmd
{
public:
    explicit Cmd(const std::string& str);

private:
    static std::string GetReg(const std::string& str, size_t index);
    static int GetNum(const std::string& str, size_t index);

    const size_t m_arg1index;
    const size_t m_arg2index;

public:
    const std::string m_type;
    const std::string m_label;
    const std::string m_reg1;
    const int m_num1;
    const std::string m_reg2;
    const int m_num2;
};
//----------------------------------------------------------------------------------
typedef std::unordered_map<std::string, int> Regs;
typedef std::vector<std::string> Program;
typedef std::unordered_map<std::string, int> Labels;
typedef std::stack<int> RetStack;
typedef void(*Handler)(Regs&, Cmd&, int&, int&, Labels&, RetStack&, std::string&);
typedef std::unordered_map<std::string, Handler> Handlers;
//----------------------------------------------------------------------------------
void InitProgram(Program& program, std::string& input);
void InitLabels(const Program& program, Labels& labels);
//----------------------------------------------------------------------------------
void Mov(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue, 
        Labels& labels, RetStack& retStack, std::string& retStr);
void Add(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Sub(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Mul(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Div(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Inc(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Dec(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Jmp(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Cmp(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Jne(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Je(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Jge(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Jg(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Jle(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Jl(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Call(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Ret(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
void Msg(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr);
//----------------------------------------------------------------------------------
std::string assembler_interpreter(std::string input)
{
    static Handlers handlers = { 
            {"mov", Mov}, {"inc", Inc}, {"dec", Dec}, 
            {"add", Add}, {"sub", Sub}, {"mul", Mul}, {"div", Div},
            {"jmp", Jmp}, {"cmp", Cmp}, {"jne", Jne}, {"je", Je},
            {"jge", Jge}, {"jg", Jg}, {"jle", Jle}, {"jl", Jl},
            {"call", Call}, {"ret", Ret}, {"msg", Msg} };

    Program program;
    InitProgram(program, input);
    Labels labels;
    InitLabels(program, labels);
    RetStack retStack;
    int cmpValue;
    Regs regs;
    std::string realRetStr = "-1";
    std::string retStr;

    for (int index = 0; index < program.size(); ++index)
    {
        if ((std::string::npos != program[index].find(":"))
                && ("msg" != program[index].substr(0, 3)))   // only label
            continue;
        
        if ("end" == program[index].substr(0, 3))
        {
            realRetStr = retStr;
            break;
        }

        Cmd cmd(program[index]);
        handlers[cmd.m_type](regs, cmd, index, cmpValue, labels, retStack, retStr);
    }

    return realRetStr;
}
//----------------------------------------------------------------------------------
Cmd::Cmd(const std::string& str)
    : m_arg1index(str.find(" ", 0) + 1)
    , m_arg2index(str.find(" ", m_arg1index) + 1)
    , m_type(str.substr(0, m_arg1index - 1))
    , m_label(str.substr(m_arg1index))
    , m_reg1(GetReg(str, m_arg1index))
    , m_num1(("" == m_reg1) ? GetNum(str, m_arg1index) : 0)
    , m_reg2(GetReg(str, m_arg2index))
    , m_num2(("" == m_reg2) ? GetNum(str, m_arg2index) : 0)
{ }
//----------------------------------------------------------------------------------
std::string Cmd::GetReg(const std::string& str, size_t index)
{
    if ((str.length() <= index) || !isalpha(str[index]))
        return "";
    
    return str.substr(index, 1);
}
//----------------------------------------------------------------------------------
int Cmd::GetNum(const std::string& str, size_t index)
{
    if (str.length() <= index) 
        return 0;
    
    return strtod(str.c_str() + index, 0);
}
//----------------------------------------------------------------------------------
void InitProgram(Program& program, std::string& input)
{
    std::replace(input.begin(), input.end(), '\0', '\n'); 

    while (!input.empty())
    {
        auto len = input.find("\n");
        std::string cmd = input.substr(0, len);
        if (len < input.length())
            input.erase(0, len + 1);
        else
            input = "";

        // remove comments and spaces
        std::replace(cmd.begin(), cmd.end(), '\t', ' ');
        while (std::string::npos != cmd.find("  "))
           cmd.erase(cmd.find("  "), 1);
        while (' ' == cmd[0])
           cmd.erase(0, 1);
        while (' ' == cmd[cmd.length()-1])
           cmd.erase(cmd.length() - 1, 1);
        auto commentStart = cmd.find(";");
        if (std::string::npos != commentStart)
                cmd.erase(commentStart);
        if ("" == cmd)
                continue;

        // save command
        program.push_back(cmd);
    }
}
//----------------------------------------------------------------------------------
void InitLabels(const Program& program, Labels& labels)
{
    for (int index = 0; index < program.size(); ++index)
    {
        auto nameEnd = program[index].find(":");
        if (std::string::npos != nameEnd)
        {
            labels[program[index].substr(0, nameEnd)] = index;
        }
    }
}
//----------------------------------------------------------------------------------
void Mov(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue, 
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    regs[cmd.m_reg1] = ((cmd.m_reg2 == "") ? cmd.m_num2 : regs[cmd.m_reg2]);
}
//----------------------------------------------------------------------------------
void Add(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue, 
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    regs[cmd.m_reg1] += ((cmd.m_reg2 == "") ? cmd.m_num2 : regs[cmd.m_reg2]);
}
//----------------------------------------------------------------------------------
void Sub(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    regs[cmd.m_reg1] -= ((cmd.m_reg2 == "") ? cmd.m_num2 : regs[cmd.m_reg2]);
}
//----------------------------------------------------------------------------------
void Mul(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue, 
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    regs[cmd.m_reg1] *= ((cmd.m_reg2 == "") ? cmd.m_num2 : regs[cmd.m_reg2]);
}
//----------------------------------------------------------------------------------
void Div(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue, 
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    regs[cmd.m_reg1] /= ((cmd.m_reg2 == "") ? cmd.m_num2 : regs[cmd.m_reg2]);
}
//----------------------------------------------------------------------------------
void Inc(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue, 
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    ++regs[cmd.m_reg1];
}
//----------------------------------------------------------------------------------
void Dec(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue, 
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    --regs[cmd.m_reg1];
}
//----------------------------------------------------------------------------------
void Jmp(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    cmdIndex = labels[cmd.m_label];
}
//----------------------------------------------------------------------------------
void Cmp(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    auto val1 = ((cmd.m_reg1 == "") ? cmd.m_num1 : regs[cmd.m_reg1]);
    auto val2 = ((cmd.m_reg2 == "") ? cmd.m_num2 : regs[cmd.m_reg2]);
    cmpValue = val1 - val2;
}
//----------------------------------------------------------------------------------
void Jne(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    if (cmpValue != 0)
        cmdIndex = labels[cmd.m_label];
}
//----------------------------------------------------------------------------------
void Je(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    if (cmpValue == 0)
        cmdIndex = labels[cmd.m_label];
}
//----------------------------------------------------------------------------------
void Jge(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    if (cmpValue >= 0)
        cmdIndex = labels[cmd.m_label];
}
//----------------------------------------------------------------------------------
void Jg(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    if (cmpValue > 0)
        cmdIndex = labels[cmd.m_label];
}
//----------------------------------------------------------------------------------
void Jle(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    if (cmpValue <= 0)
        cmdIndex = labels[cmd.m_label];
}
//----------------------------------------------------------------------------------
void Jl(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    if (cmpValue < 0)
        cmdIndex = labels[cmd.m_label];
}
//----------------------------------------------------------------------------------
void Call(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    retStack.push(cmdIndex);
    cmdIndex = labels[cmd.m_label];
}
//----------------------------------------------------------------------------------
void Ret(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    cmdIndex = retStack.top();
    retStack.pop();
}
//----------------------------------------------------------------------------------
void Msg(Regs& regs, Cmd& cmd, int& cmdIndex, int& cmpValue,
        Labels& labels, RetStack& retStack, std::string& retStr)
{
    std::string toFormat = cmd.m_label;
    retStr = "";
    while (!toFormat.empty())
    {
        while ((toFormat[0] == ' ') || (toFormat[0] == ','))
            toFormat.erase(0, 1);

        if (toFormat[0] == '\'')
        {
            auto close = toFormat.find('\'', 1);
            retStr += toFormat.substr(1, close - 1);
            toFormat.erase(0, close + 1);
        }
        else if (isalpha(toFormat[0]))
        {
            std::string reg = toFormat.substr(0, 1);
            retStr += std::to_string(regs[reg]);
            toFormat.erase(0, 1);
        }
    }
}

____________________________________________________
#include <string>
#include <map>
#include <vector>

using namespace std;

void ignorRest(const char*& str)
{  
    while(*str != 0 && *str++ != '\n');
}

string getString(const char* &str)
{
    string res = "";
    for (str++; *str != 0 && (*str != '\'' || (*(str-1)=='\\')); res += *str == '\\' ? *((++str)++) : *str++);
    return (*str=='\''?str++:str), res;
}

string getToken(const char* &str)
{
    string res = "";
    while (*str == ' ' || *str == ';' || *str =='\n' || *str=='\t') if (*str == ';') ignorRest(str); else str++;
    if (*str == '\'') return getString(str);
    for (; *str != 0 && *str != '\n' && *str != ' ' && *str != ',' && *str!=':' ; res += *str++);
    return res;
}

void findAllLables(const char* str, map<string, const char*> &lables)
{    
    while (*str != 0)
    {
        string token = getToken(str);
        if(*str != 0 && *str++ == ':') lables[token] = str;
    }
}

long long getNum(const char* &str)
{
    long long res = 0; bool negativ = *str=='-' && *(++str)!= 0;
    for (char ch = *str; ch != '\0' && !(ch < '0' || ch > '9'); str++, ch = *str)
        res = res * 10 + ch - '0';
    return negativ ? -res : res;
}

bool isDigit(const char* &str)
{
    while (*str == ' ') str++;
    return (*str >= '0' && *str <= '9') || (*str=='-' && (*(str+1) >= '0' && *(str+1) <= '9'));
}

std::string assembler_interpreter(std::string program)
{
    string output = "";
    vector<const char*> callStack;
    map<string, const char*> lables;
    map<string, long long> registers;
    long long cmp1, cmp2;
    const char* str = program.c_str();

    findAllLables(str, lables);

    while (str != 0 && *str!=0)
    {
        string cmd = getToken(str);
        if (str != 0 && *str++ == ':' || cmd == "") continue;

        if (cmd == "mov") { string param1 = getToken(str); registers[param1] = isDigit(++str) ? getNum(str) : registers[getToken(str)]; }
        if (cmd == "inc") { registers[getToken(str)]++; }
        if (cmd == "dec") { registers[getToken(str)]--; }
        if (cmd == "add") { string param1 = getToken(str); registers[param1] += isDigit(++str) ? getNum(str) : registers[getToken(str)]; }
        if (cmd == "sub") { string param1 = getToken(str); registers[param1] -= isDigit(++str) ? getNum(str) : registers[getToken(str)]; }
        if (cmd == "mul") { string param1 = getToken(str); registers[param1] *= isDigit(++str) ? getNum(str) : registers[getToken(str)]; }
        if (cmd == "div") { string param1 = getToken(str); registers[param1] /= isDigit(++str) ? getNum(str) : registers[getToken(str)]; }
        if (cmd == "jmp") { str = lables[getToken(str)]; }
        if (cmd == "cmp") { cmp1 = isDigit(str) ? getNum(str) : registers[getToken(str)]; cmp2 = isDigit(++str) ? getNum(str) : registers[getToken(str)]; }        
        if (cmd == "jne") { string lbl = getToken(str); if (cmp1 != cmp2) str = lables[lbl]; }
        if (cmd == "je")  { string lbl = getToken(str); if (cmp1 == cmp2) str = lables[lbl]; }
        if (cmd == "jge") { string lbl = getToken(str); if (cmp1 >= cmp2) str = lables[lbl]; }
        if (cmd == "jg")  { string lbl = getToken(str); if (cmp1 > cmp2)  str = lables[lbl]; }
        if (cmd == "jle") { string lbl = getToken(str); if (cmp1 <= cmp2) str = lables[lbl]; }
        if (cmd == "jl")  { string lbl = getToken(str); if (cmp1 < cmp2)  str = lables[lbl]; }
        if (cmd == "call"){ string lbl = getToken(str); callStack.push_back(str); str = lables[lbl]; }
        if (cmd == "ret") { if (callStack.size() > 0) { str = callStack[callStack.size() - 1]; callStack.pop_back(); } }
        if (cmd == "msg") { output = ""; while (str!= 0 && *str != '\n' && *str != 0 && *str != ';') { if (*str == ',' || *str == ' ') { str++; continue; } if (*str == '\'')output += getString(str); else output += to_string(registers[getToken(str)]);} }
        if (cmd == "end") { return output; }
        ignorRest(str);
    }
   
    return "-1";
}
