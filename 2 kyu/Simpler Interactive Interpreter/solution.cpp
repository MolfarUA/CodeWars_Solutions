#include <algorithm>
#include <iostream>
#include <string>
#include <cmath>
#include <set>

using type = double;

using callback = std::function<type(type, type)>;
const std::map<char, callback> operations = {
  {'+', std::plus<type>()},
  {'-', std::minus<type>()},
  {'/', std::divides<type>()},
  {'*', std::multiplies<type>()},
  {'%', [](const type &a, const type &b) -> type { return std::fmod(a, b); }}
};

const std::set<char> prioritized = { '*', '/', '%' };

struct node {
  node() = default;
  explicit node(type value): stored(value) {
  }
  
  double value() const {
    /// Lazy initialization
    if (!stored.has_value()) {
      if (!operation || !first || !second)
        throw std::runtime_error("Invalid node");
      stored = (*operation)(first->value(), second->value());
      std::cerr << " * " << first->value() << " " << op << " " << second->value() << " = " << stored.value() << std::endl;
    }
    
    return stored.value();
  }
  
  static node negate(node &&n) {
    node root;
    root.first = std::make_unique<node>(0);
    root.second = std::make_unique<node>(std::move(n));
    root.operation = std::make_unique<callback>(std::minus<type>());
    root.op = '-';
    return root;
  }
    
  mutable std::optional<type> stored;
    
  std::unique_ptr<node> first;
  std::unique_ptr<node> second;
  std::unique_ptr<callback> operation;
  /// Just for print
  char op;
};

/// Initialized variables
static std::map<std::string, type> variables;

/// Reads variable from memory
type read_variable(const std::string &i) {
  return std::isalpha(*i.c_str()) ? variables.at(i) : std::stod(i);
}

using const_iter = std::string::const_iterator;

const_iter find_last(const_iter begin, const_iter end, const char val) {
  auto isearch = end;
  for (auto iter = begin; iter != end; ++iter) {
    if (*iter == val)
      isearch = iter;
  }
  return isearch;
}

std::pair<const_iter, const_iter> read_block(const_iter begin, const_iter end) {
  if (begin == end)
    return {end, end};
  
  if (*begin == '(') {
    /// Returning group
    int level = 0;
    for (auto inode = begin; inode != end; ++inode) {
      if (*inode == '(')
        ++level;
      else if (*inode == ')')
        --level;
      
      if (level == 0)
        return {std::next(begin), inode};
    }
    throw std::runtime_error("Failed to find close brace");
  } else if (operations.count({*begin})) {
    /// Returning operation block
    return {begin, std::next(begin)};
  }
  
  /// Values and variables
  auto stop = std::find_if(begin, end, [&](const char c){
    return operations.count({c});
  });
  return {begin, stop};
}

/// Parsing expression
/// This method creates expression tree
node parse(const_iter begin, const_iter end) {
  std::cerr << "Parsing: [" << std::string(begin, end) << "]" << std::endl;
  if (begin == end)
    return node(0);
  
  /// Children nodes
  std::vector<std::pair<const_iter, const_iter>> blocks;
  
  auto start = begin;
  while (start != end) {
    auto range = read_block(start, end);
    blocks.push_back(range);
    start = range.second;
    if (start != end && *start == ')')
      ++start;
  }
  
  for (auto &r : blocks)
    std::cerr << " * block: " << std::string{r.first, r.second} << std::endl;
  
  auto l_any_c = [](const auto &c){ return operations.count(c); };
  
  auto read_block = [&](auto &block, bool negate = false) -> node {
    if (std::find_if(std::next(block.first), block.second, l_any_c) != block.second)
      /// Complex blocks
      return parse(block.first, block.second);
    return node((negate ? -1 : 1) * read_variable({blocks.back().first, blocks.back().second}));
  };
  
  /// Leafes
  if (blocks.size() == 1)
    return read_block(blocks.front());
  else if (blocks.size() == 2)
    return node::negate(parse(blocks.back().first, blocks.back().second));
  
  /// Searching for not prioritized dividor
  auto i_dividor = blocks.end();
  for (auto iblock = std::next(blocks.begin()); iblock != blocks.end(); ++iblock) {
    auto iprev = std::prev(iblock);
    if (std::distance(iblock->first, iblock->second) == 1 &&
        operations.count(*iblock->first) &&
        !prioritized.count(*iblock->first) && (
          !operations.count(*iprev->first) || 
          std::distance(iprev->first, iprev->second) > 1
        )) {
      i_dividor = iblock;
    }
  }
  
  auto l_prior = [](const auto &b){ return prioritized.count(*b.first); };
  if (i_dividor == blocks.end()) {
    /// And only after that prioritized operation
    /// In reverse order
    i_dividor = blocks.end();
    for (auto inode = blocks.begin(); inode != blocks.end(); ++inode)
      if (std::distance(inode->first, inode->second) && l_prior(*inode)) {
        i_dividor = inode;
      }
    
    if (i_dividor == blocks.end())
      throw std::runtime_error("Ivalid block: " + std::string{begin, end});
  }
  
  node root;
  root.first = std::make_unique<node>(parse(begin, i_dividor->first));
  root.second = std::make_unique<node>(parse(i_dividor->second, end));
  root.operation = std::make_unique<callback>(operations.at(*i_dividor->first));
  root.op = *i_dividor->first;
  
  return root;
}

double interpret(std::string expression) {  
  std::cerr << ">>> " << expression << std::endl;
  
  /// Cleaning spaces from expression to simpllify further parsing
  expression.erase(std::remove_if(expression.begin(), expression.end(), ::isspace), expression.end());
  if (expression.empty())
    throw std::runtime_error("Empty expression");
  
  /// Assign expressions
  auto i_assign = std::find(expression.begin(), expression.end(), '=');
  if (i_assign != expression.end()) {
    const auto tree = parse(std::next(i_assign), expression.end());
    auto &value = variables[expression.substr(0, std::distance(expression.begin(), i_assign))];
    return value = tree.value();
 } 
  
  /// Non-assign expressions
  return parse(expression.begin(), expression.end()).value();
}

________________________________________________________
#include <string>
#include <vector>
#include <memory>
#include <unordered_map>
#include <cmath>

bool is_num(std::string s){
    bool dot=false;//numbers with multiple dots are malformed
    bool first=false;
    for(char c:s){
        if(c=='.'&&!dot){
            dot=true;
        }else if(c<'0'||c>'9'){
            return false;
        }
        if(first)first=false;
    }
    return true;
}

bool is_ident(std::string s){
    if(s[0]>='0'&&s[0]<='9')return false;
    for(char c:s){
        if((c<'a'||c>'z')&&(c<'A'||c>'Z')&&(c<'0'&&c>'9')&&c!='_')return false;
    }
    return true;
}

double parse_num(std::string s){
    return std::stod(s);
}

bool is_op(char c){
    return c=='+'||c=='-'||c=='*'||c=='/'||c=='%'||c=='^';
}

bool is_separator(char c){
    return (c==' '||c=='\n'||c=='\t'||c=='\r');
}

struct token{
    enum TK_TYPE{
        TK_PAREN_OPEN,
        TK_PAREN_CLOSE,
        TK_ASSIGN,
        TK_OP,
        TK_NUM,
        TK_IDENT,
    }type;
    std::string data;
};

void commit(bool &reading,std::string &tmp,std::vector<token> &tks){
    if(reading){
        reading=false;
        if(is_num(tmp)){
            tks.push_back((token){token::TK_NUM,tmp});
        }else if(is_ident(tmp)){
            tks.push_back((token){token::TK_IDENT,tmp});
        }else{
            throw std::runtime_error("unexpected '"+tmp+"'");
        }
        tmp="";
    }
}

std::vector<token> scan(const std::string& s){
    std::vector<token> tks;
    std::string tmp;
    bool reading=false;
    for(char c:s){
        if(is_separator(c)){
            commit(reading,tmp,tks);
        }else if(c=='('){
            commit(reading,tmp,tks);
            tks.push_back({token::TK_PAREN_OPEN,std::string(1,c)});
        }else if(c==')'){
            commit(reading,tmp,tks);
            tks.push_back({token::TK_PAREN_CLOSE,std::string(1,c)});
        }else if(c=='='){
            commit(reading,tmp,tks);
            tks.push_back({token::TK_ASSIGN,std::string(1,c)});
        }else if(is_op(c)){
            commit(reading,tmp,tks);
            tks.push_back({token::TK_OP,std::string(1,c)});
        }else{
            reading=true;
            tmp+=c;
        }
    }
    if(tmp.size()>0){
        commit(reading,tmp,tks);
    }
    return tks;
}

struct node {
    virtual double get_value(std::unordered_map<std::string,double>&)=0;
    virtual ~node(){
    }
};

struct num : public node {
    double data;
    num(double d):data(d){}
    virtual double get_value(std::unordered_map<std::string,double>&) override {
        return data;
    }
};

struct var : public node {
    std::string name;
    bool negative;
    var(std::string s,bool neg):name(s),negative(neg){}
    virtual double get_value(std::unordered_map<std::string,double> &memory) override {
        try{
            return negative?-memory.at(name):memory.at(name);
        }catch(...){
            throw std::runtime_error("undefined variable '"+name+"'");
        }
    }
};

int operator_precedence(char c){
    switch(c){
    case '+':
        return 1;
    case '-':
        return 1;
    case '*':
        return 2;
    case '/':
        return 2;
    case '%':
        return 2;
    case '^':
        return 3;
    }
    throw std::runtime_error("unknown operator '"+std::string(1,c)+"'");
}

struct negexprgrp : public node {//negative expression group
    std::unique_ptr<node> expr;
    negexprgrp(const std::vector<token> tks,uint32_t &i);
    virtual double get_value(std::unordered_map<std::string,double> &memory) override;
};

struct expression : public node {//expression
    
    struct expr_data{//data or 
        expr_data(std::unique_ptr<node> f):factor(std::move(f)),is_op(false){}
        expr_data(char c):op(c),is_op(true){}
        char op;
        std::unique_ptr<node> factor;
        bool is_op;
    };
    
    std::vector<expr_data> expr;
    
    expression(const std::vector<token> tks,uint32_t &i){
        read_expr(tks,i,false);
    }
    expression(const std::vector<token> tks,uint32_t &i,bool b){
        read_expr(tks,i,b);
    }
    void read_expr(const std::vector<token> tks,uint32_t &i,bool parens){
        std::vector<char> op_stack;
        for(;;i++){
            if(i>=tks.size()){
                throw std::runtime_error("expected value, got EOF");
            }
            switch(tks[i].type){//read value
                case token::TK_IDENT:
                    expr.emplace_back(std::make_unique<var>(tks[i].data,false));
                    break;
                case token::TK_NUM:
                    expr.emplace_back(std::make_unique<num>(parse_num(tks[i].data)));
                    break;
                case token::TK_OP:
                    if((i+1)<tks.size()){
                        if(tks[i+1].type==token::TK_NUM||tks[i+1].type==token::TK_IDENT){//allow sign modifiers
                            if(tks[i].data[0]=='-'){//negative
                                i++;
                                if(tks[i].type==token::TK_NUM){
                                    expr.emplace_back(std::make_unique<num>(-parse_num(tks[i].data)));
                                }else{
                                    expr.emplace_back(std::make_unique<var>(tks[i].data,true));
                                }
                                break;
                            }else if(tks[i].data[0]=='+'){//positive (no change)
                                i++;
                                if(tks[i].type==token::TK_NUM){
                                    expr.emplace_back(std::make_unique<num>(parse_num(tks[i].data)));
                                }else{
                                    expr.emplace_back(std::make_unique<var>(tks[i].data,false));
                                }
                                break;
                            }
                        }else if(tks[i+1].type==token::TK_PAREN_OPEN){
                            if(tks[i].data[0]=='-'){//handle negative expression groups
                                i++;
                                expr.emplace_back(std::make_unique<negexprgrp>(tks,i));
                                break;
                            }
                        }
                    }
                    //if no sign modifiers found, throw
                    throw std::runtime_error("expected value, got '"+tks[i].data+"'");
                case token::TK_PAREN_OPEN:
                    i++;
                    read_expr(tks,i,true);
                    break;
                case token::TK_PAREN_CLOSE:
                    throw std::runtime_error("expected value, got ')'");
                default:
                    throw std::runtime_error("expected value, got '"+tks[i].data+"'");
            }
            i++;
            if(i<tks.size()){//read opeartor
                if(tks[i].type==token::TK_OP){
                    int precedence=operator_precedence(tks[i].data[0]);
                    while(op_stack.size()>0&&operator_precedence(op_stack.back())>=precedence){//shunting yard
                        expr.emplace_back(op_stack.back());
                        op_stack.pop_back();
                    }
                    op_stack.push_back(tks[i].data[0]);
                }else{
                    if(parens){
                        while(op_stack.size()>0){
                            expr.emplace_back(op_stack.back());
                            op_stack.pop_back();
                        }
                        if(expr.size()==0)throw std::runtime_error("empty expression");
                        return;
                    }else{
                        throw std::runtime_error("expected operator, got '"+tks[i].data+"'");
                    }
                }
            }else{
                if(parens){
                    throw std::runtime_error("expected ')', got EOF");
                }else{
                    while(op_stack.size()>0){
                        expr.emplace_back(op_stack.back());
                        op_stack.pop_back();
                    }
                    if(expr.size()==0)throw std::runtime_error("empty expression");
                    return;
                }
            }
        }
    }
    static double operate(double lhs,double rhs,char op){//execute operation
        switch(op){
            case '+':
                return lhs+rhs;
            case '-':
                return lhs-rhs;
            case '/':
                return lhs/rhs;
            case '*':
                return lhs*rhs;
            case '%':
                return fmod(lhs,rhs);
            case '^':
                return pow(lhs,rhs);
        }
        throw std::runtime_error("invalid operator");
    }
    virtual double get_value(std::unordered_map<std::string,double> &memory) override {
        std::vector<double> stack;
        for(auto &e:expr){//evaluate RPN
            if(e.is_op){
                double rhs=stack.back();
                stack.pop_back();
                double lhs=stack.back();
                stack.pop_back();
                stack.push_back(operate(lhs,rhs,e.op));
            }else{
                stack.push_back(e.factor->get_value(memory));
            }
        }
        if(stack.size()!=1)throw std::runtime_error("internal error, invalid stack size");
        return stack.back();
    }
};

negexprgrp::negexprgrp(const std::vector<token> tks,uint32_t &i){
    if(tks[i].type!=token::TK_PAREN_OPEN)throw std::runtime_error("expected '(', got '"+tks[i].data+"'");
    i++;
    expr=std::make_unique<expression>(tks,i,true);
}

double negexprgrp::get_value(std::unordered_map<std::string,double> &memory){
    return -expr->get_value(memory);
}


struct assignment : public node {
    std::string name;
    std::unique_ptr<expression> expr;
    assignment(const std::vector<token> tks,uint32_t &i){
        if(tks[0].type!=token::TK_IDENT){
            throw std::runtime_error("can't assign to '"+tks[0].data+"'");
        }
        name=tks[0].data;
        i=2;
        if(i<tks.size()){
            expr=std::make_unique<expression>(tks,i);
        }else{
            throw std::runtime_error("expected expression, got EOF");
        }
    }
    virtual double get_value(std::unordered_map<std::string,double> &memory) override {
        return memory[name]=expr->get_value(memory);
    }
};

struct assignment_op : public node {
    std::string name;
    std::unique_ptr<expression> expr;
    char op;
    assignment_op(const std::vector<token> tks,uint32_t &i){
        if(tks[0].type!=token::TK_IDENT){
            throw std::runtime_error("can't assign to '"+tks[0].data+"'");
        }
        name=tks[0].data;
        op=tks[1].data[0];
        i=3;
        if(i<tks.size()){
            expr=std::make_unique<expression>(tks,i);
        }else{
            throw std::runtime_error("expected expression, got EOF");
        }
    }
    virtual double get_value(std::unordered_map<std::string,double> &memory) override {
        double lhs;
        try{
            lhs=memory.at(name);
        }catch(...){
            throw std::runtime_error("undefined variable '"+name+"'");
        }
        double rhs=expr->get_value(memory);
        return memory[name]=expression::operate(lhs,rhs,op);
    }
};

std::unique_ptr<node> parse(const std::vector<token> tks){
    uint32_t i=0;
    if(tks.size()>1&&tks[1].type==token::TK_ASSIGN){//assignment
        return std::make_unique<assignment>(tks,i);
    }else if(tks.size()>2&&tks[1].type==token::TK_OP&&tks[2].type==token::TK_ASSIGN){//compound assignment
        return std::make_unique<assignment_op>(tks,i);
    }else{//expression
        return std::make_unique<expression>(tks,i);
    }
}

double interpret(std::string expression) {
    static std::unordered_map<std::string,double> memory;
    return parse(scan(expression))->get_value(memory);
}

________________________________________________________
#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <iostream>
#include <cmath>
struct Simbol{
    std::string name;
    double value;
};

void parse_space(std::string & expression,size_t &index){
    while(expression.size()>index&&expression[index]==' ')++index;
}
double assign_expresison(std::string & expression,size_t & index,std::vector<Simbol> &SimbolTable);
double additive(std::string &expression,size_t &index,std::vector<Simbol> &SimbolTable);
double multitive(std::string &expression,size_t &index,std::vector<Simbol> &SimbolTable);
double factor(std::string &expression,size_t &index,std::vector<Simbol> &SimbolTable);

bool IsIdChar(std::string& expression,size_t &index){
    return  expression[index]=='_'||isdigit(expression[index])
            ||isalpha(expression[index]);
}
void skip(std::string& expression,size_t &index,const char &c){
    if(expression[index]==c)index++;
    else throw("match error");
}

double find(std::string id,std::vector<Simbol> SimbolTable,std::string &expression){
    for(int index=SimbolTable.size()-1;index>=0;--index){
        if(SimbolTable[index].name==id){
            return SimbolTable[index].value;
        }
    }
    throw(std::runtime_error("can't find the identifier"+id+expression));
}

double number(std::string& expression,size_t &index){
    std::string str;
    
    parse_space(expression,index);
    while(isdigit(expression[index])){
        str.push_back(expression[index++]);
    }
    parse_space(expression,index);
    if(expression[index]=='.'){
        index++;
        parse_space(expression,index);
        str.push_back('.');
        while (isdigit(expression[index])){
            str.push_back(expression[index++]);
        }
    }
        return stod(str);
   
}

std::string identifier(std::string& expression,size_t &index,std::vector<Simbol> &SimbolTable){
    std::string res;
    if(isalpha(expression[index])||expression[index]=='_'){
        res.push_back(expression[index++]);
    }
    while(IsIdChar(expression,index)){
        res.push_back(expression[index++]);
    }
    return res;
}

double factor(std::string & expression,size_t & index,std::vector<Simbol> &SimbolTable){
    double sig=1;
    while(expression[index]=='-'){
        ++index;
        sig*=-1;
        parse_space(expression,index);
    }
    if(expression[index]=='-'||isdigit(expression[index]))return sig*number(expression,index);
    if(expression[index]=='('){
        ++index;
        parse_space(expression,index);
        double res=additive(expression,index,SimbolTable);
        parse_space(expression,index);
        ++index;
        return sig*res;
    }
    std::string id=identifier(expression,index,SimbolTable);
    parse_space(expression,index);
    if(index<expression.size()&&expression[index]=='='){
        index++;
        parse_space(expression,index);
        double rval=additive(expression,index,SimbolTable);
        parse_space(expression,index);
        SimbolTable.push_back({id,rval});
        return rval;
    }
    else 
        return sig*find(id,SimbolTable,expression);

}

double additive(std::string &expression,size_t &index,std::vector<Simbol> &SimbolTable){
    double res=0.0;
    res=multitive(expression,index,SimbolTable);
    parse_space(expression,index);
    while(index<expression.size()&&(expression[index]=='+'||expression[index]=='-')){
        int op=expression[index++];
        if(op=='+'){
            parse_space(expression,index);
            res+=multitive(expression,index,SimbolTable);
        }
        else if(op=='-'){
            parse_space(expression,index);
            res-=multitive(expression,index,SimbolTable);
        }
    }
    return res;
}
double multitive(std::string &expression,size_t &index,std::vector<Simbol> &SimbolTable){
    double res=0.0;
    res=factor(expression,index,SimbolTable);
    parse_space(expression,index);
    while(index<expression.size()&&(expression[index]=='*'||expression[index]=='/'||expression[index]=='%')){
        int op=expression[index++];
        if(op=='*'){
            parse_space(expression,index);
            res*=factor(expression,index,SimbolTable);
        }
        else if(op=='/'){
            parse_space(expression,index);
            res/=factor(expression,index,SimbolTable);
        }
        else if(op=='%'){
            parse_space(expression,index);
            res=fmod(res,factor(expression,index,SimbolTable));
        }
        parse_space(expression,index);
    }
    return res;
}

double interpret(std::string expression) {
    static std::vector<Simbol>SimbolTable;
    size_t index=0;
    parse_space(expression,index);
    return additive(expression,index,SimbolTable);
}
