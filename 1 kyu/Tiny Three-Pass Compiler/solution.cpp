#include <vector>
#include <string>
#include <regex>
#include <cctype>
#include <map>

using namespace std;

class AST {
public:
  AST(std::string op, AST* a, AST* b) : op(op), a(a), b(b), n(0) { }
  AST(std::string op, int n) : op(op), a(nullptr), b(nullptr), n(n) { }
  ~AST() { if (a) delete a; if (b) delete b; }

  // Do constant folding
  void reduce();
  
  // Translate this AST to assembly instructions, putting the resulting value in R0
  std::vector<std::string> translate();
  
  // Dump to std::cerr
  void dump() const {
    if (op == "imm")      std::cerr << "imm " << n << "";
    else if (op == "arg") std::cerr << "arg " << n << "";
    else {
      std::cerr << "(";
      a->dump();
      std::cerr << " " << op << " ";
      b->dump();
      std::cerr << ")";
    }
  }

public:
  std::string op;
  AST* a, *b;
  int n;
};

void AST::reduce() {
  if (op == "imm" || op == "arg") return;
  
  assert(a && b && "expected binary expression!");
  
  // Reduce subexpressions first
  a->reduce();
  b->reduce();
  
  // Can this node be reduced? Are both operands constant?
  if (a->op != "imm" || b->op != "imm") return;
  
  // It can be reduced.
  int l = a->n, r = b->n;
  
  if      (op == "+") n = l + r;
  else if (op == "-") n = l - r;
  else if (op == "*") n = l * r;
  else if (op == "/") n = l / r;
  
  // Rewrite this node, its a constant now
  op = "imm";
  
  // Delete previous operands
  delete a;
  delete b;
  
  a = b = nullptr;
}

std::vector<std::string> AST::translate() {
  if (op == "arg") return { std::string("AR ") + std::to_string(n) };
  if (op == "imm") return { std::string("IM ") + std::to_string(n) };
  
  assert(a && b && "expected binary expression!");

  std::vector<std::string> leftinstr  = a->translate(); // Compute left operand
  
  leftinstr.push_back("PU"); // push value to make room for computation of right operand
  
  std::vector<std::string> rightinstr = b->translate();
  leftinstr.insert(leftinstr.end(), rightinstr.begin(), rightinstr.end()); // Compute right operand

  leftinstr.push_back("SW"); // put the right operand in R1
  leftinstr.push_back("PO"); // pop left operand into R0
  
  // The right value is now constructed in R1 and the left value in R0, do the final operation
  
  // Add the opcode according to op
  if (op == "+")      leftinstr.push_back("AD");
  else if (op == "-") leftinstr.push_back("SU");
  else if (op == "*") leftinstr.push_back("MU");
  else if (op == "/") leftinstr.push_back("DI");
  
  return leftinstr;
}

class Parser {
public:
  Parser(std::vector<std::string>& program) : program(program), tokeniter(program.begin()) { }
  AST* parse();
  
private:
  inline std::string getCurrentToken() { return *tokeniter; }
  inline std::string consumeToken() { return *tokeniter++; }
  // Unfortunately incorrect programs are out of scope of this exercise, so this never fails anyway
  inline void expect(std::string) { ++tokeniter; } 

  void readArgInfo();
  AST* parseExpression();
  // A simple precedence expression parser
  AST* parseExpression(int precedence);
  AST* parsePrimaryExpression();
  
  inline int getPrecedence() { return precedenceTable[getCurrentToken()]; }
  
private:
  std::vector<std::string>& program;
  std::vector<std::string>::iterator tokeniter;
  
  std::map<std::string, int> argindices;
  int currentindex = 0;
  
  static std::map<std::string, int> precedenceTable;
};

std::map<std::string, int> Parser::precedenceTable = { {"+", 1}, {"-", 1}, {"*", 2}, {"/", 2}, {")", 0} };

AST* Parser::parse() {
  readArgInfo(); // Associate arguments with their index in the list
  return parseExpression(); // Parse the trailing expression with this information
}

void Parser::readArgInfo() {
  expect("[");
  
  std::string token;
  while ((token = consumeToken()) != "]") {
    argindices[token] = currentindex++;
  }
}

AST* Parser::parseExpression() {
  return parseExpression(0); // Zero is lower than any operator precedence
}

AST* Parser::parseExpression(int precedence) {
  AST* left = parsePrimaryExpression();
  
  int prec;
  while (tokeniter != program.end() && (prec = getPrecedence()) > precedence) {
    auto token = consumeToken();
    AST* right = parseExpression(prec);
    left = new AST(token, left, right);
  }
  
  return left;
}

AST* Parser::parsePrimaryExpression() {
  auto token = consumeToken();
  if (token == "(") {
    AST* parenthesized = parseExpression();
    expect(")");
    return parenthesized;
  }
  
  assert(!token.empty());
  char first = *token.begin();  
  if (std::isalpha(first))
    return new AST("arg", argindices[token]);

  return new AST("imm", atoi(token.c_str()));
}

struct Compiler {
  vector <string> compile (string program) {
    return pass3 (pass2 (pass1 (program)));
  }

  // Turn a program string into a vector of tokens.  Each token
  // is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
  // name or a number (as a string)
  vector <string> tokenize (string program) {
    static regex re ("[-+*/()[\\]]|[A-Za-z]+|\\d+");
    sregex_token_iterator it (program.begin (), program.end (), re);
    return vector <string> (it, sregex_token_iterator ());
  }

  // Returns an un-optimized AST
  AST *pass1 (string program) {
    auto tokens = tokenize (program);
    
    Parser parser(tokens);
    return parser.parse();
  }

  // Returns an AST with constant expressions reduced
  AST *pass2 (AST *ast) {
    ast->reduce();
    return ast;
  }

  // Returns assembly instructions
  vector <string> pass3 (AST *ast) {
    return ast->translate();
  }
};

####################
#include <cctype>
#include <cstddef>
#include <cstdio>
#include <functional>
#include <iterator>
#include <regex>
#include <string>
#include <unordered_map>
#include <vector>

struct AST {
  std::string op;
  AST *a;
  AST *b;
  std::size_t n;
  
  AST() = default;
  AST(std::string op, AST *a, AST *b) {
    this->op = op;
    this->a = a;
    this->b = b;
    this->n = 0;
  }
  AST(std::string op, AST *a, AST *b, size_t n) {
    this->op = op;
    this->a = a;
    this->b = b;
    this->n = n;
  }
  AST(std::string op, size_t n) {
    this->op = op;
    this->a = nullptr;
    this->b = nullptr;
    this->n = n;
  }
};

struct Compiler {

  std::vector<std::string> compile(std::string program) {
    return pass3(pass2(pass1(program)));
  }

  // Turn a program string into a vector of tokens.  Each token
  // is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
  // name or a number (as a string)
  std::vector<std::string> tokenize(std::string program) {
    static std::regex re("[-+*/()[\\]]|[A-Za-z]+|\\d+");
    std::sregex_token_iterator it(program.begin(), program.end(), re);
    return std::vector<std::string>(it, std::sregex_token_iterator());
  }

  AST *func(std::string **p, const std::string *q) {
    auto iter = *p;
    std::unordered_map<std::string, size_t> map;
    size_t cnt = 0;
    iter++;
    while (iter != q && *iter != "]") {
      map.insert({*iter++, cnt++});
    }
    iter++;
    auto ast = expr(&iter, q, map);
    *p = iter;
    return ast;
  }
  AST *expr(std::string **p, const std::string *q,
            const std::unordered_map<std::string, size_t> &map) {
    auto iter = *p;
    auto ast = term(&iter, q, map);
    while (iter != q && (*iter == "+" || *iter == "-")) {
      auto op = *iter++;
      auto lhs = ast;
      auto rhs = term(&iter, q, map);
      ast = new AST{op, lhs, rhs};
    }
    *p = iter;
    return ast;
  }
  AST *term(std::string **p, const std::string *q,
            const std::unordered_map<std::string, size_t> &map) {
    auto iter = *p;
    auto ast = factor(&iter, q, map);
    while (iter != q && (*iter == "*" || *iter == "/")) {
      auto op = *iter++;
      auto lhs = ast;
      auto rhs = factor(&iter, q, map);
      ast = new AST{op, lhs, rhs};
    }
    *p = iter;
    return ast;
  }
  AST *factor(std::string **p, const std::string *q,
              const std::unordered_map<std::string, size_t> &map) {
    auto iter = *p;
    AST *ast;
    if (*iter == "(") {
      iter++;
      ast = expr(&iter, q, map);
      iter++;
    } else if (std::isdigit((*iter)[0])) {
      ast = new AST{"imm", nullptr, nullptr,
                    (size_t)strtol(iter->c_str(), nullptr, 10)};
      iter++;
    } else if (std::isalpha((*iter)[0])) {
      ast = new AST{"arg", nullptr, nullptr, map.find(*iter)->second};
      iter++;
    } else {
      throw 0;
    }
    *p = iter;
    return ast;
  }

  // Returns an un-optimized AST
  AST *pass1(std::string program) {
    auto tokens = tokenize(program);
    auto p = tokens.data(), q = tokens.data() + tokens.size();
    return func(&p, q);
  }

  std::unordered_map<std::string, std::function<size_t(size_t, size_t)>> eval{
      {"+", [](size_t v1, size_t v2) -> size_t { return v1 + v2; }},
      {"-", [](size_t v1, size_t v2) -> size_t { return v1 - v2; }},
      {"*", [](size_t v1, size_t v2) -> size_t { return v1 * v2; }},
      {"/", [](size_t v1, size_t v2) -> size_t { return v1 / v2; }},
  };

  AST *pass2(AST *ast) {
    if (ast->op == "+" || ast->op == "-" || ast->op == "*" || ast->op == "/") {
      auto op = ast->op;
      auto lhs = pass2(ast->a);
      auto rhs = pass2(ast->b);
      if (lhs->op == "imm" && rhs->op == "imm") {
        ast = new AST{"imm", nullptr, nullptr, eval[op](lhs->n, rhs->n)};
      } else {
        ast->a = lhs;
        ast->b = rhs;
      }
    }
    return ast;
  }

  std::unordered_map<std::string, std::string> op {
    {"+", "AD"}, {"-", "SU"}, {"*", "MU"}, { "/", "DI" }
  };

  void emit(AST *ast, std::vector<std::string> &vec) {
    if (ast->op == "+" || ast->op == "-" || ast->op == "*" || ast->op == "/") {
      emit(ast->a, vec);
      vec.push_back("PU");
      emit(ast->b, vec);
      vec.push_back("SW");
      vec.push_back("PO");
      vec.push_back(op[ast->op]);
    } else if (ast->op == "imm")
      vec.push_back("IM " + std::to_string(ast->n));
    else
      vec.push_back("AR " + std::to_string(ast->n));
  }

  std::vector<std::string> pass3(AST *ast) {
    std::vector<std::string> vec;
    emit(ast, vec);
    return vec;
  }
};

###################################
#include <vector>
#include <string>
#include <regex>
#include <cstdint>
#include <map>
#include <queue>
#include <iostream>

struct AST
{
    AST(const std::string &, int);
    AST(const std::string &, AST *, AST *);

    std::string op;
    int n;
    AST *a;
    AST *b;
};

AST::AST(const std::string &op, int n)
    : op(op)
    , n(n)
    , a(nullptr)
    , b(nullptr)
{
}

AST::AST(const std::string &op, AST *a, AST *b)
    : op(op)
    , n(0)
    , a(a)
    , b(b)
{
}

struct Compiler {

  std::vector <std::string> compile (std::string program);

  // Turn a program string into a vector of tokens.  Each token
  // is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
  // name or a number (as a string)
  std::vector <std::string> tokenize (std::string program);

  // Returns an un-optimized AST
  AST *pass1 (std::string program);

  // Returns an AST with constant expressions reduced
  AST *pass2 (AST *ast);

  // Returns assembly instructions
  std::vector <std::string> pass3 (AST *ast);
};


namespace {

std::map<std::string, std::uint32_t> op_priority = {
    { "-", 1 },
    { "+", 1 },
    { "/", 2 },
    { "*", 2 }
};

} // namespace


std::vector <std::string> Compiler::compile(std::string program)
{
    return pass3(pass2(pass1(program)));
}

// Turn a program string into a vector of tokens.  Each token
// is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
// name or a number (as a string)
std::vector <std::string> Compiler::tokenize(std::string program)
{
    static std::regex re("[-+*/()[\\]]|[A-Za-z]+|\\d+");
    std::sregex_token_iterator it(program.begin(), program.end(), re);
    return std::vector <std::string>(it, std::sregex_token_iterator());
}

namespace {

std::vector<std::string> variables(const std::vector<std::string>& tokens)
{
    const auto it = std::find(tokens.begin(), tokens.end(), "]");
    return std::vector(tokens.begin() + 1, it);
}

std::vector<std::string> expr_tokens(const std::vector<std::string> &tokens)
{
    const auto it = std::find(tokens.begin(), tokens.end(), "]");
    return std::vector(it + 1, tokens.end());
}

bool is_number(const std::string &s)
{
    std::string::const_iterator it = s.begin();
    while (it != s.end() && std::isdigit(*it))
    {
        ++it;
    }
    return !s.empty() && it == s.end();
}

bool is_variable(const std::string &s)
{
    std::string::const_iterator it = s.begin();
    while (it != s.end() && std::isalpha(*it))
    {
        ++it;
    }
    return !s.empty() && it == s.end();
}

bool is_operation(const std::string& s)
{
    return (s == "-") || (s == "+") || (s == "/") || (s == "*");
}

std::vector<std::string> rpn(const std::vector<std::string> &tokens)
{
    std::vector<std::string> result;
    std::vector<std::string> stack;

    for (const auto &t : tokens)
    {
        if (is_number(t))
        {
            result.push_back(t);
        }
        else if (is_variable(t))
        {
            result.push_back(t);
        }
        else if (t == "(")
        {
            stack.push_back(t);
        }
        else if (t == ")")
        {
            while (!stack.empty() && stack.back() != "(")
            {
                result.push_back(stack.back());
                stack.pop_back();
            }

            if (!stack.empty() && stack.back() == "(")
            {
                stack.pop_back();
            }
            else
            {
                std::cout << "rpn(): open bracet missing" << std::endl;
                return std::vector<std::string>();
            }
        }
        else if (is_operation(t))
        {
            while (!stack.empty() && op_priority[stack.back()] >= op_priority[t])
            {
                result.push_back(stack.back());
                stack.pop_back();
            }
            stack.push_back(t);
        }
        else
        {
            std::cout << "unknown token : " << t << std::endl;
            return std::vector<std::string>();
        }
    }

    while (!stack.empty())
    {
        result.push_back(stack.back());
        stack.pop_back();
    }

    return result;
}

AST *rpn_to_ast(const std::vector<std::string> &rpn, const std::vector<std::string> &vars)
{
    std::vector<AST *> result;

    for (const auto &t : rpn)
    {
        if (is_number(t))
        {
            result.push_back(new AST("imm", std::stoi(t)));
        }
        else if (is_variable(t))
        {
            const auto it = std::find(vars.begin(), vars.end(), t);
            const auto idx = std::distance(vars.begin(), it);
            result.push_back(new AST("arg", idx));
        }
        else if (is_operation(t))
        {
            if (result.size() < 2)
            {
                std::cout << "invalid count of args for binary operation : " << t << std::endl;
                return nullptr;
            }

            const auto rhs = result.back();
            result.pop_back();
            const auto lhs = result.back();
            result.pop_back();
            result.push_back(new AST(t, lhs, rhs));
        }
    }

    if (result.size() != 1)
    {
        std::cout << "internal error : result stack has more than one element" << std::endl;
        return nullptr;
    }

    return result.front();
}

} // namespace

// Returns an un-optimized AST
AST* Compiler::pass1(std::string program)
{
    const auto tokens = tokenize(program);
    const auto vars = variables(tokens);
    const auto expr = expr_tokens(tokens);
    const auto rpn_form = rpn(expr);
    return rpn_to_ast(rpn_form, vars);
}

namespace {

bool is_op(AST *node)
{
    return !(node->op == "imm" || node->op == "arg");
}
  
void op_printer(AST*& op, AST*)
{
    std::cout << "{ " << op->op << " : ";

    if (is_op(op->a))
    {
        std::cout << op->a->op << ", ";
    }
    else
    {
        std::cout << op->a->op << "[" << op->a->n << "], ";
    }

    if (is_op(op->b))
    {
        std::cout << op->b->op;
    }
    else
    {
        std::cout << op->b->op << "[" << op->b->n << "]";
    }

    std::cout << "}; ";
}

template<typename Job>
void bfs(AST *&root, Job &&job)
{
    if (root == nullptr)
    {
        return;
    }

    struct op_queue_element
    {
        op_queue_element(AST* t_op, AST* t_parent)
            : op(t_op)
            , parent(t_parent)
        {}

        AST *op;
        AST *parent;
    };

    std::queue<op_queue_element> q;
    q.emplace(root, nullptr);

    while (!q.empty())
    {
        auto current = q.front();

        if (is_op(current.op))
        {
            job(current.op, current.parent);

            q.emplace(current.op->a, current.op);
            q.emplace(current.op->b, current.op);
        }

        q.pop();
    }
}

int evaluate(int a, int b, const std::string& op)
{
    if (op == "+")
    {
        return a + b;
    }
    else if (op == "-")
    {
        return a - b;
    }
    else if (op == "*")
    {
        return a * b;
    }
    return a / b;
}

void imm_resolver(AST*& node)
{
    if (!is_op(node))
    {
        return;
    }

    if (node->a->op == "imm" && node->b->op == "imm")
    {
        auto old_node = node;
        node = new AST("imm", evaluate(node->a->n, node->b->n, node->op));

        delete old_node->a;
        delete old_node->b;
        delete old_node;
    }
}

template<typename Job>
void dfw(AST*& node, Job&& job)
{
    if (node->a)
    {
        dfw(node->a, job);
    }

    if (node->b)
    {
        dfw(node->b, job);
    }

    job(node);
}

} // namespace

AST* Compiler::pass2(AST* root)
{
    dfw(root, imm_resolver);
    return root;
}


namespace {

class assembler
{
public:
    void operator()(AST *&node)
    {
        if (node->op == "imm")
        {
            m_inst.push_back("IM " + std::to_string(node->n));
            m_inst.push_back("PU");
        }
        else if (node->op == "arg")
        {
            m_inst.push_back("AR " + std::to_string(node->n));
            m_inst.push_back("PU");
        }
        else
        {
            m_inst.push_back("PO");
            m_inst.push_back("SW");
            m_inst.push_back("PO");
        
            if (node->op == "+")
            {
                m_inst.push_back("AD");
            }
            else if (node->op == "-")
            {
                m_inst.push_back("SU");
            }
            else if (node->op == "*")
            {
                m_inst.push_back("MU");
            }
            else
            {
                m_inst.push_back("DI");
            }

            m_inst.push_back("PU");
        }
    }

    std::vector<std::string> istructions() const
    {
        return m_inst;
    }

private:
    std::vector<std::string> m_inst;
};

} // namespace

// Returns assembly instructions
std::vector <std::string> Compiler::pass3(AST* ast)
{
    assembler asm_job;
    dfw(ast, asm_job);
    return asm_job.istructions();
}

##################
#include <vector>
#include <map>
#include <string>
#include <regex>

struct AST {
  AST(const std::string& op, int n) : op(op), n(n) {}
  AST(const std::string& op, AST* a, AST* b) : op(op), a(a), b(b)  {}
  ~AST() { delete a; delete b; }

  std::string op;
  AST* a = nullptr;
  AST* b = nullptr;
  int n = 0;
};

struct Compiler {

  std::vector <std::string> compile (std::string program) {
    return pass3 (pass2 (pass1 (program)));
  }

  // Turn a program string into a vector of tokens.  Each token
  // is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
  // name or a number (as a string)
  std::vector <std::string> tokenize (std::string program) {
    static std::regex re ("[-+*/()[\\]]|[A-Za-z]+|\\d+");
    std::sregex_token_iterator it (program.begin (), program.end (), re);
    return std::vector <std::string> (it, std::sregex_token_iterator ());
  }
  
  static AST* parse_expressions(const std::vector<std::string>& tokens, int start, int end, const std::map<std::string, int>& args) {
    std::vector<AST*> nodes;
    std::vector<std::string> ops;
    for (int i = start; i < end; ++i) {
      const auto& tok = tokens[i];
      if (tok[0] == '(') {
        int j, open = 1;
        for (j = i + 1; j < end && open; ++j) {
          if (tokens[j][0] == '(') ++open;
          else if (tokens[j][0] == ')') --open;
        }
        nodes.push_back(parse_expressions(tokens, i + 1, j - 1, args));
        i = j - 1;
      } else if (tok == "*" || tok == "/" || tok == "+" || tok == "-") {
        ops.push_back(tok);
      } else if (args.count(tok)) {
        nodes.push_back(new AST("arg", args.find(tok)->second));
      } else {
        nodes.push_back(new AST("imm", std::stoi(tok)));
      }
    }
    // we can remove the quadratic complexity here, but for a POC this is "ok"
    for (size_t i = 0; i < ops.size(); ) {
      if (ops[i] == "*" || ops[i] == "/") {
        nodes[i] = new AST(ops[i], nodes[i], nodes[i + 1]);
        nodes.erase(nodes.begin() + i + 1);
        ops.erase(ops.begin() + i);
      } else ++i;
    }
    AST* result = nodes[0];
    for (size_t i = 0; i < ops.size(); ++i) result = new AST(ops[i], result, nodes[i + 1]);
    return result;
  }

  // Returns an un-optimized AST
  AST *pass1 (std::string program) {
    auto tokens = tokenize (program);
    std::map<std::string, int> args;
    size_t p = 0;
    if (tokens[0][0] != '[') return nullptr;
    for (p = 1; p < tokens.size() && tokens[p][0] != ']'; ++p) args.emplace(tokens[p], args.size());
    return parse_expressions(tokens, p + 1, tokens.size(), args);
  }

  // Returns an AST with constant expressions reduced
  AST *pass2 (AST *ast) {
    if (!ast) return nullptr;
    pass2(ast->a);
    pass2(ast->b);
    if (ast->a && ast->b && ast->a->op == "imm" && ast->b->op == "imm") {
      switch (ast->op[0]) {
          case '+': ast->n = ast->a->n + ast->b->n; break;
          case '-': ast->n = ast->a->n - ast->b->n; break;
          case '*': ast->n = ast->a->n * ast->b->n; break;
          case '/': ast->n = ast->a->n / ast->b->n; break;
      }
      ast->op = "imm";
      delete ast->a; ast->a = nullptr;
      delete ast->b; ast->b = nullptr;
    }
    return ast;
  }
  
  static void generate_instructions(AST* ast, std::vector<std::string>& instructions) {
    if (!ast) return;
    if (ast->a && ast->b) {
      generate_instructions(ast->a, instructions);
      instructions.emplace_back("PU");
      generate_instructions(ast->b, instructions);
      instructions.emplace_back("SW");
      instructions.emplace_back("PO");
      if (ast->op == "+") instructions.emplace_back("AD");
      else if (ast->op == "-") instructions.emplace_back("SU");
      else if (ast->op == "*") instructions.emplace_back("MU");
      else if (ast->op == "/") instructions.emplace_back("DI");
    } else {
      if (ast->op == "imm") instructions.emplace_back("IM " + std::to_string(ast->n));
      else if (ast->op == "arg") instructions.emplace_back("AR " + std::to_string(ast->n));
    }
  }

  // Returns assembly instructions
  std::vector <std::string> pass3 (AST *ast) {
    std::vector<std::string> instructions;
    generate_instructions(ast, instructions);
    return instructions;
  }
};

##########################
#include <iostream>
#include <vector>
#include <string>
#include <regex>
#include <stack>
#include <utility>


using namespace std;

struct AST
{
    AST* a = nullptr, *b = nullptr;
    string op;
    int n = 0;

    AST(string const& op) : op(op) {}
    AST(string const& op, AST* a, AST* b) : op(op), a(a), b(b){}
    AST(string const& op, int n) : op(op), n(n) {}
};

struct Compiler {

  std::vector <std::string> compile (std::string program) {
    return pass3 (pass2 (pass1 (program)));
  }

  // Turn a program string into a vector of tokens.  Each token
  // is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
  // name or a number (as a string)
  std::vector <std::string> tokenize (std::string program) {
    static std::regex re ("[-+*/()[\\]]|[A-Za-z]+|\\d+");
    std::sregex_token_iterator it (program.begin (), program.end (), re);
    return std::vector <std::string> (it, std::sregex_token_iterator ());
  }



    AST* parse_expression(vector<string>& tokens, unordered_map<string, AST*>& vars)
    {
        static auto extract_expression = [](vector<string> const& tokens, size_t& offset) -> vector<string>
        {
            int ob_count = 0;

            for (size_t i = offset; i < tokens.size(); i++)
            {
                if (tokens[i] == "(") ob_count++;
                else if (tokens[i] == ")") ob_count--;

                if (ob_count == 0)
                {
                    auto r = vector<string>(tokens.begin()+ offset+1, tokens.begin() + i);
                    offset = i;
                    return r;
                }
            }
            return {};
        };
        vector<AST*> syntax_chain;

        static const vector<string> order_of_operations = {"/","*", "+", "-"};


        for (size_t i = 0; i < tokens.size(); i++)
        {
            string& token = tokens[i];

            if (token == "[")
            {
                int idx = 0;
                while (++i < tokens.size())
                {
                    token = tokens[i];
                    if (token == "]") break;

                    if (!vars[token])
                        vars[token] = new AST("arg", idx++);
                }
            }
            else if (token == "(")
            {
                auto v = extract_expression(tokens, i);
                syntax_chain.push_back(parse_expression(v, vars));
            }
            else if (token == "+")
                syntax_chain.push_back(new AST("+"));
            else if (token == "-")
                syntax_chain.push_back(new AST("-"));
            else if (token == "*")
                syntax_chain.push_back(new AST("*"));
            else if (token == "/")
                syntax_chain.push_back(new AST("/"));
            else if (token[0] >= '0' && token[0] <= '9')
                syntax_chain.push_back(new AST("imm", stoi(token)));
            else // Assume variable
                syntax_chain.push_back(vars[token]);
        }

        for (auto& op : order_of_operations)
        {
            for (int i = 0; i < syntax_chain.size(); i++)
            {
                if (syntax_chain[i]->op == op)
                {
                    syntax_chain[i]->a = syntax_chain[i-1];
                    syntax_chain[i]->b = syntax_chain[i+1];
                    syntax_chain.erase(syntax_chain.begin() + i + 1);
                    syntax_chain.erase(syntax_chain.begin() + i - 1);
                    i--;
                    if (i > 0 && syntax_chain[i]->op == "+" && syntax_chain[i-1]->op == "-")
                    {
                        swap(syntax_chain[i]->a, syntax_chain[i]->b);
                        syntax_chain[i]->op = "-";
                    }
                }
            }
        }
        return syntax_chain[0];
    }


  // Returns an un-optimized AST
  AST *pass1 (std::string const& program) {
    auto tokens = tokenize (program);
    unordered_map<string, AST*> vars;
    return parse_expression(tokens,vars);
  }

  // Returns an AST with constant expressions reduced
  AST *pass2 (AST *ast)
  {
      if (ast->a) pass2(ast->a);
      if (ast->b) pass2(ast->b);

      if (ast->a && ast->b)
      {
          if (ast->a->op == "imm" && ast->b->op == "imm")
          {
              if (ast->op == "+") ast->n = ast->a->n + ast->b->n;
              else if (ast->op == "/") ast->n = ast->a->n / ast->b->n;
              else if (ast->op == "-") ast->n = ast->a->n - ast->b->n;
              else if (ast->op == "*") ast->n = ast->a->n * ast->b->n;

              delete ast->a;
              delete ast->b;
              ast->op = "imm";
              ast->a = nullptr, ast->b = nullptr;
          }
      }

      return ast;
  }

  void pass3(AST* ast, vector<string>& result)
  {
      if (ast->a && ast->b)
      {
          if (ast->a)
          {
              if (ast->a->op == "imm")
                  result.emplace_back("IM " + to_string(ast->a->n));
              else if (ast->a->op == "arg")
                  result.emplace_back("AR " + to_string(ast->a->n));
              else
                  pass3(ast->a,result);
          }

          if (ast->b)
          {
              if (ast->b->op == "imm") {
                  result.emplace_back("SW");
                  result.emplace_back("IM " + to_string(ast->b->n));
                  if (ast->op != "+" && ast->op != "*")
                  result.emplace_back("SW");
              }
              else if (ast->b->op == "arg") {
                  result.emplace_back("SW");
                  result.emplace_back("AR " + to_string(ast->b->n));
                  if (ast->op != "+" && ast->op != "*")
                      result.emplace_back("SW");

              }else
              {
                  result.emplace_back("PU");
                  pass3(ast->b,result);
                  result.emplace_back("SW");
                  result.emplace_back("PO");
              }
          }

          if (ast->op == "+") result.emplace_back("AD");
          else if (ast->op == "/") result.emplace_back("DI");
          else if (ast->op == "-") result.emplace_back("SU");
          else if (ast->op == "*") result.emplace_back("MU");
      }
  }

  // Returns assembly instructions
  std::vector <std::string> pass3 (AST *ast)
  {
      vector<string> result;
      pass3(ast,result);
      return result;
  }
};

######################
#include <vector>
#include <algorithm>
#include <cctype>
#include <string>
#include <regex>

struct AST {
  std::string op; AST *a, *b; int n;

  AST (std::string op, AST *a, AST *b) { this->op = op; this->a = a; this->b = b; n = 0; }
  AST (std::string op, int n) { this->op = op; this->n = n; a = b = 0; }
};

struct Compiler {

  std::vector <std::string> compile (std::string program) {
    return pass3 (pass2 (pass1 (program)));
  }

  std::vector <std::string> tokenize (std::string program) {
    static std::regex re ("[-+*/()[\\]]|[A-Za-z]+|\\d+");
    std::sregex_token_iterator it (program.begin (), program.end (), re);
    return std::vector <std::string> (it, std::sregex_token_iterator ());
  }

  AST *pass1 (std::string program) {
    args.clear (); cur = 0; tokens = tokenize (program);
    return parse_function ();
  }

  AST *pass2 (AST *ast) {
    if (ast && ast->a && ast->b) {
      AST *a = pass2 (ast->a);
      AST *b = pass2 (ast->b);
      if (a->op == "imm" && b->op == "imm") {
        int v;
        switch (ast->op[0]) {
        case '+': v = a->n + b->n; break;
        case '-': v = a->n - b->n; break;
        case '*': v = a->n * b->n; break;
        case '/': v = a->n / b->n; break;
        }
        ast = new AST ("imm", v);
      } else
        ast = new AST (ast->op, a, b);
    }
    return ast;
  }

  std::vector <std::string> pass3 (AST *ast) {
    instructions.clear ();
    gencode (ast);
    return instructions;
  }

private:

  std::vector <std::string> args, tokens, instructions; int cur;

  void gencode (AST *ast) {
    static std::map <std::string, std::string> loads {{"imm", "IM "}, {"arg", "AR "}};
    static std::map <std::string, std::string> ops {{"+", "AD"}, {"-", "SU"}, {"*", "MU"}, {"/", "DI"}};
    if (ast->op == "imm" || ast->op == "arg") {
      instructions.push_back (loads[ast->op] + std::to_string (ast->n));
    } else {
      gencode (ast->a);
      instructions.push_back ("PU");
      gencode (ast->b);
      instructions.push_back ("SW");
      instructions.push_back ("PO");
      instructions.push_back (ops[ast->op]);
    }
  }

  std::string next () { return tokens[cur++]; }
  std::string front () { return tokens[cur]; }
  bool empty () { return cur >= (int)tokens.size (); }

  AST *parse_factor () {
    AST *ast;
    std::string t = next ();
    if (t == "(") {
      ast = parse_expression ();
      next ();
    } else if (std::all_of (t.begin (), t.end (), isdigit)) {
      ast = new AST ("imm", stoi (t));
    } else {
      auto it = find (args.begin (), args.end (), t);
      ast = new AST ("arg", distance (args.begin (), it));
    }
    return ast;
  }

  AST *parse_term () {
    AST *ast = parse_factor ();
    while (!empty () && (front () == "*" || front () == "/"))
      ast = new AST (next (), ast, parse_factor ());
    return ast;
  }

  AST *parse_expression () {
    AST *ast = parse_term ();
    while (!empty () && (front () == "+" || front () == "-"))
      ast = new AST (next (), ast, parse_term ());
    return ast;
  }

  AST *parse_function () {
    next ();
    while (front () != "]")
      args.push_back (next ());
    next ();
    return parse_expression ();
  }

};

#########################
#include <vector>
#include <string>
#include <regex>

using namespace std;

using VI = std::vector<int>;
using VS = std::vector<std::string>;
using VC = std::vector<char>;

struct AST {
    string op; AST* a, * b;
    int n;
    AST(string op, AST* a, AST* b) : op(op), a(a), b(b), n(0) {}
    AST(string op, int n) : op(op), n(n), a(0), b(0) {}
};

struct Compiler {

    VS tokens, args, pass3V;
    int idx;

    VS compile(string program) {
        return pass3(pass2(pass1(program)));
    }

    VS tokenize(string program) {
        static regex re("[-+*/()[\\]]|[A-Za-z]+|\\d+");
        sregex_token_iterator it(program.begin(), program.end(), re);
        return VS(it, sregex_token_iterator());
    }

    AST* pass1(string program) { 
        return parse(program);
    }

    AST* pass2(AST* ast) {
        return reduce(ast);
    }

    VS pass3(AST* ast) {
        return getInstr(ast);
    }

    // pass1------------------------------------------------------
    AST* parse(string program) {
        tokens = tokenize(program), args.clear(), idx = 0, tokens[idx++];
        while (tokens[idx] != "]") args.push_back(tokens[idx++]);
        return tokens[idx++], parseExpr(0);
    }

    AST* parseExpr(bool endOfExpr) {
        AST* ast = parseTerm();
        while (!(idx >= tokens.size()) && (tokens[idx] == "+" || tokens[idx] == "-")) 
            ast = new AST(tokens[idx++], ast, parseTerm());
        return endOfExpr ? idx++, ast : ast;
    }

    AST* parseTerm() {
        AST* ast = parseFactor();
        while (!(idx >= tokens.size()) && (tokens[idx] == "*" || tokens[idx] == "/")) 
            ast = new AST(tokens[idx++], ast, parseFactor());
        return ast;
    }

    AST* parseFactor() {
        string i = tokens[idx++];
        return (i == "(" ? parseExpr(1) : // newExpr
            find(args.begin(), args.end(), i) == args.end() ? new AST("imm", stoi(i)) : //imm value
            new AST("arg", distance(args.begin(), find(args.begin(), args.end(), i)))); //an argument
    }
    
    // pass2------------------------------------------------------
    AST* reduce(AST* ast) {
        if (ast->a && ast->b) {
            AST *a = reduce(ast->a), *b = reduce(ast->b);
            if (a->op == "imm" && b->op == "imm")
                return new AST("imm", (ast->op == "+" ? a->n + b->n : ast->op == "-" ? a->n - b->n :
                    ast->op == "*" ? a->n * b->n : a->n / b->n));
            return new AST(ast->op, a, b); //another node
        } return ast;
    }

    // pass3------------------------------------------------------
    VS getInstr(AST* ast) {
        if (!ast->a) return pass3V.push_back((ast->op == "imm" ? "IM " : "AR ") + to_string(ast->n)), pass3V;
        getInstr(ast->a); //Computing left operand
        pass3V.push_back("PU"); //Clearing r0 for right oper
        getInstr(ast->b); //Computing right oper
        pass3V.insert(pass3V.end(), {"SW", "PO", (ast->op == "+" ? "AD" : ast->op == "-" ? "SU" : ast->op == "*" ? "MU" : "DI")});
        return pass3V;
    }
};

#########################
#include <utility>
#include <vector>
#include <string>
#include <regex>
#include <cassert>
#include <iostream>

using namespace std;

struct AST;

struct AST{
    AST( std::string opCode, AST* nodeA, AST* nodeB, int v )
        : op(std::move( opCode )), a( nodeA ), b( nodeB ), n( v ) {}
    AST( std::string opCode, AST* nodeA, AST* nodeB )
        : op(std::move( opCode )), a( nodeA ), b( nodeB ), n( 0 ) {}
    AST( std::string opCode, int v )
        : op(std::move( opCode )), n( v ) {}
    std::string op;
    AST* a = nullptr; // Sad, tests are not compatible witn smart pointers.
    AST* b = nullptr;
    int                    n;

    std::string toJSon() const {
        if( op == "arg" or op == "imm" ) return "AST ( " + op + ", " + std::to_string( n ) + " )";
        else return "AST ( " + op + ", " + a->toJSon() + ", " + b->toJSon() + " )";
    }

};


class VarStore
{
public:
    void addVariable( const std::string & c )
    {
        size_t idx = m_varList.size();
        m_varList.push_back( c );
        m_varMapToIndex.insert( { c, idx } );
    }
    int getVarIdx( const std::string & name ) { return m_varMapToIndex[name]; } // yeah... should be const and checked.

private:
    std::vector< std::string > m_varList;
    std::map< std::string, int > m_varMapToIndex;

};

//-----------------------------------------------------------------------------
class Parser
{
public:
    Parser( const std::vector<std::string> & input ) : code{input} {}

    AST* parse();
    AST* expression();
    AST* factor();
    AST* exponential();
    AST* primary();

private:

    std::vector<std::string > code;
    size_t curr = 0;
    VarStore varStore;

    bool eof() const { return curr == code.size(); }
    const std::string & prev() const { return code[ curr - 1 ]; }
    const std::string & next() {
        if( !eof() ) {
            ++curr;
            return prev();
        }
        assert(false);
    }
    const std::string & peek() const { return code[curr]; }
    bool check( std::string c ) const { return !eof() and peek() == c; }
    bool match( std::string c ) {
        if( check( c ) ){
            next();
            return true;
        }
        return false;
    }
    bool consume( std::string c ) {
        if( !match( c )) std::cout << "Syntax error: expected [" << c << "].\n" ;
        return true;
    }

};
//-----------------------------------------------------------------------------
AST* Parser::parse() {
    match("[");
    auto tok = peek();
    while( std::isalpha(tok[0]) ) {
        varStore.addVariable( tok );
        next();
        tok = peek();
    }
    match("]");
    return expression();
}

//-----------------------------------------------------------------------------
AST* Parser::expression() {
    auto left = factor();
    while( match( "+" ) or match( "-" )) {
        auto op = prev();
        auto right = factor();
        left =  new AST( op, std::move( left), std::move( right), 0 );
    }
    return left;
}

//-----------------------------------------------------------------------------
AST* Parser::factor() {
    auto left = primary();
    while( match( "*" ) or match( "/" )) {
        auto op = prev();
        auto right = primary();
        left = new AST( op, std::move(left), std::move(right), 0 );
    }
    return left;
}

//-----------------------------------------------------------------------------
AST* Parser::primary()
{
    auto tok = next();

    if( isdigit( tok[0] )) return new AST( "imm", nullptr, nullptr, std::stod( tok) );
    else if( isalpha( tok[0] )) return new AST( "arg", nullptr, nullptr, varStore.getVarIdx( tok ));
    else if( tok == "(" ) {
        auto node = expression();
        consume( ")" );
        return node;
    }
    std::cout << "syntax error :)  unexpected char " << tok << '\n';
    return {};
}

//-----------------------------------------------------------------------------
AST* optimize( AST* node )
{
    if( node->a ) {
        auto tmp = optimize( std::move( node->a ));
        if( tmp != node->a ) {
            delete node->a;
            node->a = tmp;
        }
    }
    if( node->b ) {
        auto tmp = optimize( std::move( node->b ));
        if( tmp != node->b ) {
            delete node->b;
            node->b = tmp;
        }
    }
    if( node->a and node->a->op == "imm" and node->b and node->b->op == "imm" ) {
        if( node->op == "+"  ) node->n = node->a->n + node->b->n;
        if( node->op == "-"  ) node->n = node->a->n - node->b->n;
        if( node->op == "*"  ) node->n = node->a->n * node->b->n;
        if( node->op == "/"  ) node->n = node->a->n / node->b->n;
        node->op = "imm";
        delete node->a;
        node->a = nullptr;
        delete node->b;
        node->b = nullptr;
    }
    return node;
}

//-----------------------------------------------------------------------------
void astToByteCode( const AST &node, std::vector<string> &out )
{
    if( node.op == "imm" ) {
        out.push_back( "IM " + std::to_string( node.n ) + '\n');
        out.push_back( "PU\n");
        return ;
    }
    if( node.op == "arg" ) {
        out.push_back( "AR " + std::to_string( node.n ) + '\n');
        out.push_back( "PU\n");
        return;
    }
    astToByteCode( *node.a, out );
    astToByteCode( *node.b, out );
    out.push_back( "PO\n" );
    out.push_back( "SW\n" );
    out.push_back( "PO\n" );
    if( node.op == "+"  ) out.push_back( "AD\n" );
    else if( node.op == "-"  ) out.push_back( "SU\n" );
    else if( node.op == "*"  ) out.push_back( "MU\n" );
    else if( node.op == "/"  ) out.push_back( "DI\n" );
    out.push_back( "PU\n" );
}


//-----------------------------------------------------------------------------
struct Compiler {

    vector <string> tokenize (string program) {
        static regex re ("[-+*/()[\\]]|[A-Za-z]+|\\d+");
        sregex_token_iterator it (program.begin (), program.end (), re);
        return vector <string> (it, sregex_token_iterator ());
    }

    vector <string> compile (string program) {
        return pass3 (pass2 (pass1 (program)));
    }

    // Turn a program string into a vector of tokens.  Each token
    // is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
    // name or a number (as a string)

    AST  *pass1 ( string program) {
        Parser p( tokenize( program ));
        return p.parse();
    }
    // Returns an AST with constant expressions reduced
    AST *pass2 (AST *ast) {
        return optimize( ast );
    }

    // Returns assembly instructions
    vector <string> pass3 (AST *ast) {
        std::vector< std::string > bcode;
        ::astToByteCode( *ast, bcode );
        return bcode;
    }
};
