#include<iostream>
#include<string>

double addtive(const std::string & expression,int & Index);
double multitive(const std::string & expression,int & Index);

double calc(const std::string expression) {
  int Index=0;
  return addtive(expression,Index);
}
void skip_white(const std::string & expression,int & Index){
    while(Index < expression.size() && expression[Index] == ' ' ) ++Index;
}

double parse_num(const std::string & expression,int & Index){
    std::string res;
    while(std::isdigit(expression[Index])){
        res.push_back(expression[Index++]);
    }
    if(expression[Index] == '.') {
        res.push_back('.');
        ++Index;
    }
    else return std::stod(res);
    while(std::isdigit(expression[Index])){
        res.push_back(expression[Index++]);
    }
    return std::stod(res);
}
double factor(const std::string & expression,int & Index){
    double sign = 1;
    double res = 0;
    if(expression[Index] == '-') {
        sign *= -1;
        ++Index;
    }
    if(expression[Index] == '('){
        Index++;
        skip_white(expression,Index);
        res = addtive(expression,Index);
        skip_white(expression,Index);
        Index++;
    }
    else res = parse_num(expression,Index);
    return res*sign;
}

double addtive(const std::string & expression,int & Index){
    double res = 0;
    res = multitive(expression,Index);
    skip_white(expression,Index);
    while(expression[Index] == '+' || expression[Index] == '-' ){
        char op = expression[Index++];
        skip_white(expression,Index);
        if(op == '+'){
            res+=multitive(expression,Index);
        }
        else{
            res-=multitive(expression,Index);
        }
        skip_white(expression,Index);
    }
    return res;
}
double multitive(const std::string & expression,int & Index){
    double res = 0;
    res = factor(expression,Index);
    skip_white(expression,Index);
    while(expression[Index] == '*' || expression[Index] == '/' ){
        char op = expression[Index++];
        skip_white(expression,Index);
        if(op == '*'){
            res*=factor(expression,Index);
        }
        else{
            res/=factor(expression,Index);
        }
        skip_white(expression,Index);
    }
    return res;
}
______________________________________________________
#include <string>
#include <functional>
#include <optional>
#include <cmath>
#include <regex>
#include <algorithm>

using operation = std::function<double(double, double)>;

/// Arithmetic operations. Just to remember.
static std::map<char, operation> ops = {
  {'+', std::plus<double>()},
  {'-', std::minus<double>()},
  {'*', std::multiplies<double>()},
  {'(', std::multiplies<double>()},
  {'/', std::divides<double>()},
};

/// Expression tree. I thought that i definetly needs tree.
struct level {
  level() {}
  level(double value): leaf(value) {}

  std::optional<double> leaf;
  std::vector<level> children;
  std::vector<char> operations;  
  
  operator double() {
    shrink({'*', '/'});
    shrink({'+', '-'});
    return *leaf;
  }
  
  void shrink(const std::string &approved) {
    int i = 0;
    for (const char op : operations) {
      if (approved.find(op) != std::string::npos) {
        auto operation = ops.at(op);
        const auto ret = operation(children[i], children[i+1]);
        children[i+1].leaf = ret;
        children[i].leaf = std::numeric_limits<double>::quiet_NaN();
      }
      ++i;
    }
    
    children.erase(std::remove_if(children.begin(), children.end(),
                   [](const auto &node){ return node.leaf && std::isnan(*node.leaf);}),
                   children.end());
    
    operations.erase(std::remove_if(operations.begin(), operations.end(),
                   [&approved](const auto &op){ return approved.find(op) != std::string::npos;}),
                   operations.end());
    
    if (children.size() == 1) {
      leaf = children.front();
      children.clear();
    }
  }
};

const std::regex re_number("[-]?[\\d]+");

/// Parsing string expression. Long boring function.
level parse(const std::string &expression) {
  level l;
  std::stringstream block;
  
  int minus = 0;
  
  auto add_block = [&l, &minus](std::stringstream &block){
    if (block.tellp() == 0)
      return;
    
    std::smatch match;
    const std::string str = block.str();
    if (std::regex_match(str, match, re_number))
      l.children.push_back(std::stod(str));
    else 
      l.children.push_back(parse(str));
    
    /// Counting minuses
    if (minus % 2 != 0) {
      l.children.push_back(-1);
      l.operations.push_back('*');
    }
    minus = 0;
    
    block.str({});
  };
  
  int deep = 0;
  for (const auto c : expression) {
    /// Counting minuses on block
    if (block.tellp() == 0 && c == '-' && !deep) {
      ++minus;
      continue;
    }
  
    if (c == '(') {
      ++deep;
      if (deep == 1)
        continue;
    }
    else if (c == ')')
      --deep;
      
    if ((c >= '0' && c <= '9') || deep) {
      block << c;
      continue;
    }
    
    if (block.tellp() && !deep && (c == '-' || c == '+' || c == '/' || c == '*' || c == '(')) {
      add_block(block);
      l.operations.push_back(c);
      
      if (c == '(')
        block << c;
    }
    
  }
  
  add_block(block);
  
  return l;
}

double calc(std::string expression) {
  /// Removing ' '. I don't like it.
  expression.erase(std::remove(expression.begin(), expression.end(), ' '), expression.end());
  return parse(expression);
}
_______________________________________________
#include <string>
#include <vector>
#include <cctype>
#include <memory>

using std::vector;
using std::string;

struct Token {
  using Iter = vector<Token>::const_iterator;
  string str;
  enum Type{Float, Int, LParen, RParen, Add, Sub, Mul, Div, Minus} type;
  Token(const string &s, Type t):str(s),type(t){}
};

vector<Token> tokenize(const char *c) {
   vector<Token> tokens;
  auto &&is_bin_op = [](Token::Type t) {
      return t == Token::Add || t == Token::Sub || 
             t == Token::Mul || t == Token::Div;
  };
  while(*c) {
    while(*c && isspace(*c)) ++c;
    switch(*c) {
      case '(': tokens.push_back({string(1, *c++),Token::LParen});break;
      case ')': tokens.push_back({string(1, *c++),Token::RParen});break;
      case '+': tokens.push_back({string(1, *c++), Token::Add});break;
      case '*': tokens.push_back({string(1, *c++), Token::Mul});break;
      case '/': tokens.push_back({string(1, *c++), Token::Div});break;
      case '-': 
            if((isdigit(*(c+1)) || *(c+1)=='(') &&
                (tokens.empty() || 
                 tokens.back().type == Token::LParen ||
                 is_bin_op(tokens.back().type))) 
            {
                tokens.push_back({string(1, *c++), Token::Minus});break;
            }
            else {
                tokens.push_back({string(1, *c++), Token::Sub});break;
            }
      default:
        auto start = c;
        if(*c == '-') ++c;
        while(isdigit(*c)) ++c;
        if(*c == '.') {
          ++c;
          while(isdigit(*c)) ++c; 
          tokens.push_back({string(start, c), Token::Float});
        }
        else 
          tokens.push_back({string(start, c), Token::Int});
    }
  }
  return tokens;
}

struct ASTNode {
  using Ptr = std::shared_ptr<ASTNode>;
  
  Token token;
  Ptr left, right;
  ASTNode(const Token& t, const Ptr &l=nullptr, const Ptr &r=nullptr):
      token(t),left(l),right(r){}
};


ASTNode::Ptr expr(Token::Iter &, Token::Iter &); 

ASTNode::Ptr factor(Token::Iter &s, Token::Iter &e) {
    switch(s->type) {
        case Token::Float:
        case Token::Int:
            return std::make_shared<ASTNode>(*s++);
        case Token::LParen:
            {
                ++s;
                auto &&exp= expr(s, e);
                ++s;
                return std::move(exp);
            }
        case Token::Minus:
            {
                auto &&op = *s++;
                return std::make_shared<ASTNode>(op, factor(s, e));
            }
        default:
            return nullptr;
    }
}

ASTNode::Ptr term(Token::Iter &s, Token::Iter &e) {
    auto &&tree = factor(s, e);
    while(s != e && (s->type == Token::Mul || s->type == Token::Div)) {
        auto &&op = *s++;
        auto &&prand = factor(s, e);
        tree = std::make_shared<ASTNode>(op, tree, prand);
    }
    return std::move(tree);
}

ASTNode::Ptr expr(Token::Iter &s, Token::Iter &e) {
    auto &&tree = term(s, e);
    while(s != e && (s->type == Token::Add || s->type == Token::Sub)) {
        auto &&op = *s++;
        auto &&prand = term(s, e);
        tree = std::make_shared<ASTNode>(op, tree, prand);
    }
    return std::move(tree);
}

ASTNode::Ptr parse(const vector<Token> &tokens) {
    auto &&start = tokens.begin(), &&end = tokens.end();
    return expr(start, end);
}

double eval(const ASTNode::Ptr &tree) {
    switch(tree->token.type) {
        case Token::Int: return std::stoi(tree->token.str);
        case Token::Float: return std::stod(tree->token.str);
        case Token::Add: return eval(tree->left) + eval(tree->right);
        case Token::Sub: return eval(tree->left) - eval(tree->right);
        case Token::Mul: return eval(tree->left) * eval(tree->right);
        case Token::Div: return eval(tree->left) / eval(tree->right);
        case Token::Minus: return -eval(tree->left);
        default:
            return 0.0; //will never reach here if the expresion is correct;
    }
}
                               

double calc(const string &expression) {
  std::cout << expression << std::endl;
  return eval(parse(tokenize(expression.c_str())));
}
________________________________________________________________
#include <string>
#include<bits/stdc++.h>
#define ll long long
#define dll double
#define mxn 100002
using namespace std;
string s;
dll q[mxn];
ll st,qt,len;
inline dll dfs(){
  ll l=qt+1,zf=1;
  dll x=0,z=0;
  char fh=' ';
  while(st<len-1){
    if((s[st]>='0'&&s[st]<='9')||s[st]=='('){
      x=0;
      if(s[st]=='(') st++,x=dfs();
      else while(s[st]>='0'&&s[st]<='9')
        x=x*10+s[st]-'0',st++;
      x*=zf;
      zf=1;
      if(fh==' ') q[++qt]=x;
      else if(fh=='*') q[qt]*=x;
      else q[qt]/=x;
      fh=' ';
    }else if(s[st]=='-') zf*=-1,st++;
    else if(s[st]=='*') fh='*',st++;
    else if(s[st]=='/') fh='/',st++;
    else if(s[st]==')'){st++;break;}
    else st++;
    
  }
  while(qt>=l) z+=q[qt--];
  return z;
}
dll calc(std::string expression) {
  s=expression+'.';qt=st=0;len=s.length();
  return dfs();
}
