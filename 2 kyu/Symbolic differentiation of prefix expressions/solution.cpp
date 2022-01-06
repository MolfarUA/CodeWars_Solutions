#include <sstream>
#include <memory>
#include <cmath>
#include <map>
#include <functional>

struct Node {
    typedef std::shared_ptr<Node> ptr_t;
    virtual bool has_variable() const = 0;
    virtual bool is_variable() const { return false; }
    virtual bool is_add() const { return false; }
    virtual bool is_mul() const { return false; }
    virtual void print(std::string& s) const = 0;
    virtual ptr_t eval() const = 0;
        
    virtual ptr_t derivative() const = 0;
    virtual ptr_t copy() const = 0;
};

struct C : public Node {
    double value;
    C(double value) : value(value) {}
    bool has_variable() const { return false; }
    void print(std::string& s) const {
        static std::ostringstream oss;
        oss << value;
        s += oss.str();
        oss.str("");
    }
    ptr_t eval() const { return std::make_shared<C>(value); }
    ptr_t derivative() const { return std::make_shared<C>(0); }
    ptr_t copy() const { return std::make_shared<C>(value); }
};

struct Addition : public Node {
    ptr_t left, right;
    Addition(ptr_t left, ptr_t right) : left(left), right(right) {};
    virtual bool has_variable() const { return left->has_variable() || right->has_variable(); }
    virtual void print(std::string& s) const {
        s += "(+ ";
        left->print(s);
        s += " ";
        right->print(s);
        s += ")";
    }
    ptr_t eval() const {
        ptr_t l = left->eval(), r = right->eval();
        if(!l->has_variable() && !r->has_variable()) {
            return std::make_shared<C>(static_cast<C*>(l.get())->value + static_cast<C*>(r.get())->value);
        }
        
        if(!l->has_variable()) {
            const double& val = static_cast<C*>(l.get())->value;
            if(val == 0) return r;
        }
        
        if(!r->has_variable()) {
            const double& val = static_cast<C*>(r.get())->value;
            if(val == 0) return l;
        }
        return std::make_shared<Addition>(l, r);
    }
    ptr_t derivative() const {
        return std::make_shared<Addition>(left->derivative(), right->derivative());
    }
    ptr_t copy() const { return std::make_shared<Addition>(left->copy(), right->copy()); }
};

struct Subtraction : public Node {
    ptr_t left, right;
    Subtraction(ptr_t left, ptr_t right) : left(left), right(right) {};
    bool has_variable() const { return left->has_variable() || right->has_variable(); }
    void print(std::string& s) const {
        s += "(- ";
        left->print(s);
        s += " ";
        right->print(s);
        s += ")";
    }
    ptr_t eval() const {
        ptr_t l = left->eval(), r = right->eval();
        if(!l->has_variable() && !r->has_variable()) {
            return std::make_shared<C>(static_cast<C*>(l.get())->value - static_cast<C*>(r.get())->value);
        }
        return std::make_shared<Subtraction>(l, r);
    }
    ptr_t derivative() const {
        return std::make_shared<Subtraction>(left->derivative(), right->derivative());
    }
    ptr_t copy() const { return std::make_shared<Subtraction>(left->copy(), right->copy()); }
};

struct Multiplication : public Node {
    ptr_t left, right;
    Multiplication(ptr_t left, ptr_t right) : left(left), right(right) {};
    bool is_mul() const { return true; }
    bool has_variable() const { return left->has_variable() || right->has_variable(); }
    void print(std::string& s) const {
        s += "(* ";
        left->print(s);
        s += " ";
        right->print(s);
        s += ")";
    }
    ptr_t eval() const {
        ptr_t l = left->eval(), r = right->eval();

        if(l->has_variable()) std::swap(l, r);
        if(!l->has_variable() && !r->has_variable())
            return std::make_shared<C>(static_cast<C*>(l.get())->value * static_cast<C*>(r.get())->value);
        
        if(!l->has_variable()) {
            double& val = static_cast<C*>(l.get())->value;
            if(val == 1) return r;
            if(val == 0) return std::make_shared<C>(0);
            
            if(r->is_mul()) {
                return std::make_shared<Multiplication>(std::make_shared<Multiplication>(l, static_cast<Multiplication*>(r.get())->left), static_cast<Multiplication*>(r.get())->right)->eval();
            }
        }
        
        if(!r->has_variable()) {
            double& val = static_cast<C*>(r.get())->value;
            if(val == 1) return l;
            if(val == 0) return std::make_shared<C>(0);
        }
                
        return std::make_shared<Multiplication>(l, r);
    }
    ptr_t derivative() const {
        return std::make_shared<Addition>(
                                          std::make_shared<Multiplication>(left->derivative(), right->copy()),
                                          std::make_shared<Multiplication>(left->copy(), right->derivative())
                                         );
    }
    ptr_t copy() const { return std::make_shared<Multiplication>(left->copy(), right->copy()); }
};

struct Ln;
struct Pow : public Node {
    ptr_t left, right;
    Pow(ptr_t left, ptr_t right) : left(left), right(right) {};
    bool has_variable() const { return left->has_variable() || right->has_variable(); }
    void print(std::string& s) const {
        s += "(^ ";
        left->print(s);
        s += " ";
        right->print(s);
        s += ")";
    }
    ptr_t eval() const {
        ptr_t l = left->eval(), r = right->eval();
        if(!l->has_variable() && !r->has_variable())
            return std::make_shared<C>(std::pow(static_cast<C*>(l.get())->value, static_cast<C*>(r.get())->value));
        
        if(!r->has_variable()) {
            const double& val = static_cast<C*>(r.get())->value;
            if(val == 0) return std::make_shared<C>(1);
            if(val == 1) return l;
        }
        
        return std::make_shared<Pow>(l, r);
    }
    ptr_t derivative() const {
        return std::make_shared<Multiplication>(std::make_shared<Pow>(left->copy(),std::make_shared<Subtraction>(right->copy(),std::make_shared<C>(1))),std::make_shared<Addition>(std::make_shared<Multiplication>(right->copy(),left->derivative()),std::make_shared<Multiplication>(std::make_shared<Multiplication>(left->copy(),std::make_shared<Ln>(left->copy())),right->derivative())));
    }
    ptr_t copy() const { return std::make_shared<Pow>(left->copy(), right->copy()); }
};

struct Division : public Node {
    ptr_t left, right;
    Division(ptr_t left, ptr_t right) : left(left), right(right) {};
    bool has_variable() const { return left->has_variable() || right->has_variable(); }
    void print(std::string& s) const {
        s += "(/ ";
        left->print(s);
        s += " ";
        right->print(s);
        s += ")";
    }
    ptr_t eval() const {
        ptr_t l = left->eval(), r = right->eval();
        if(!l->has_variable() && !r->has_variable()) {
            return std::make_shared<C>(static_cast<C*>(l.get())->value / static_cast<C*>(r.get())->value);
        }
        return std::make_shared<Division>(l, r);
    }
    ptr_t derivative() const {
        return std::make_shared<Division>(std::make_shared<Subtraction>(std::make_shared<Multiplication>(left->derivative(), right->copy()), std::make_shared<Multiplication>(left->copy(), right->derivative())), std::make_shared<Pow>(right->copy(), std::make_shared<C>(2)));
    }
    ptr_t copy() const { return std::make_shared<Division>(left->copy(), right->copy()); }
};

struct Sin;
struct Cos : public Node {
    ptr_t inner;
    Cos(ptr_t inner) : inner(inner) {};
    bool has_variable() const { return inner->has_variable(); }
    void print(std::string& s) const {
        s += "(cos ";
        inner->print(s);
        s += ")";
    }
    ptr_t eval() const {
        ptr_t l = inner->eval();
        if(!l->has_variable())
            return std::make_shared<C>(std::cos(static_cast<C*>(l.get())->value));
        return std::make_shared<Cos>(l);
    }

    ptr_t derivative() const {
        return std::make_shared<Multiplication>(std::make_shared<C>(-1), std::make_shared<Multiplication>(inner->derivative(), std::make_shared<Sin>(inner->copy()))); // FIXME
    }
    ptr_t copy() const { return std::make_shared<Cos>(inner->copy()); }
};

struct Sin : public Node {
    ptr_t inner;
    Sin(ptr_t inner) : inner(inner) {};
    bool has_variable() const { return inner->has_variable(); }
    void print(std::string& s) const {
        s += "(sin ";
        inner->print(s);
        s += ")";
    }
    ptr_t eval() const {
        ptr_t l = inner->eval();
        if(!l->has_variable())
            return std::make_shared<C>(std::sin(static_cast<C*>(l.get())->value));
        return std::make_shared<Sin>(l);
    }

    ptr_t derivative() const {
        return std::make_shared<Multiplication>(inner->derivative(), std::make_shared<Cos>(inner->copy()));
    }
    ptr_t copy() const { return std::make_shared<Sin>(inner->copy()); }
};

struct Tan : public Node {
    ptr_t inner;
    Tan(ptr_t inner) : inner(inner) {};
    bool has_variable() const { return inner->has_variable(); }
    void print(std::string& s) const {
        s += "(tan ";
        inner->print(s);
        s += ")";
    }
    ptr_t eval() const {
        ptr_t l = inner->eval();
        if(!l->has_variable())
            return std::make_shared<C>(std::tan(static_cast<C*>(l.get())->value));
        return std::make_shared<Tan>(l);
    }

    ptr_t derivative() const {
        return std::make_shared<Division>(inner->derivative(), std::make_shared<Pow>(std::make_shared<Cos>(inner->copy()),std::make_shared<C>(2)));
    }
    ptr_t copy() const { return std::make_shared<Tan>(inner->copy()); }
};

struct Ln : public Node {
    ptr_t inner;
    Ln(ptr_t inner) : inner(inner) {};
    bool has_variable() const { return inner->has_variable(); }
    void print(std::string& s) const {
        s += "(ln ";
        inner->print(s);
        s += ")";
    }
    ptr_t eval() const {
        ptr_t l = inner->eval();
        if(!l->has_variable())
            return std::make_shared<C>(std::log(static_cast<C*>(l.get())->value));
        return std::make_shared<Ln>(l);
    }

    ptr_t derivative() const {
        return std::make_shared<Division>(inner->derivative(), inner->copy()); // FIXME
    }
    ptr_t copy() const { return std::make_shared<Ln>(inner->copy()); }
};

struct Exp : public Node {
    ptr_t inner;
    Exp(ptr_t inner) : inner(inner) {};
    bool has_variable() const { return inner->has_variable(); }
    void print(std::string& s) const {
        s += "(exp ";
        inner->print(s);
        s += ")";
    }
    ptr_t eval() const {
        ptr_t l = inner->eval();
        if(!l->has_variable())
            return std::make_shared<C>(std::exp(static_cast<C*>(l.get())->value));
        return std::make_shared<Exp>(l);
    }

    ptr_t derivative() const {
        return std::make_shared<Multiplication>(inner->derivative(), this->copy());
    }
    ptr_t copy() const { return std::make_shared<Exp>(inner->copy()); }
};

struct X : public Node {
    bool has_variable() const { return true; }
    void print(std::string& s) const { s += "x"; }
    bool is_variable() const { return true; }
    ptr_t eval() const { return std::make_shared<X>(); }
    ptr_t derivative() const {
        return std::make_shared<C>(1); // FIXME
    }
    ptr_t copy() const { return std::make_shared<X>(); }
};


Node::ptr_t parse(std::string::const_iterator begin,
                  std::string::const_iterator end){
    if(begin == end) return nullptr;
    if(*begin == '(') { begin++; end--; }
    
    if(*begin == 'x') return std::make_shared<X>();
    
    static const std::map<std::string, std::function<Node::ptr_t(Node::ptr_t, Node::ptr_t)>> binary {
        {"+", [](Node::ptr_t l, Node::ptr_t r){ return std::make_shared<Addition>(l, r); }},
        {"-", [](Node::ptr_t l, Node::ptr_t r){ return std::make_shared<Subtraction>(l, r); }},
        {"*", [](Node::ptr_t l, Node::ptr_t r){ return std::make_shared<Multiplication>(l, r); }},
        {"/", [](Node::ptr_t l, Node::ptr_t r){ return std::make_shared<Division>(l, r); }},
        {"^", [](Node::ptr_t l, Node::ptr_t r){ return std::make_shared<Pow>(l, r); }},
    };

    static const std::map<std::string, std::function<Node::ptr_t(Node::ptr_t)>> unary {
        {"cos", [](Node::ptr_t i){ return std::make_shared<Cos>(i); }},
        {"sin", [](Node::ptr_t i){ return std::make_shared<Sin>(i); }},
        {"tan", [](Node::ptr_t i){ return std::make_shared<Tan>(i); }},
        {"ln" , [](Node::ptr_t i){ return std::make_shared<Ln>(i);  }},
        {"exp", [](Node::ptr_t i){ return std::make_shared<Exp>(i); }},
    };
    
    std::string::const_iterator mid = std::find(begin, end, ' ');
    std::string action(begin, mid);

    if(binary.find(action) != binary.end()) {
        begin = mid + 1;
        mid = std::find_if(begin, end,
        [count = 0](char c) mutable {
            count += (c == '(') - (c == ')');
            return count == 0 && c == ' ';
        });
        
        return binary.at(action)(parse(begin, mid), parse(mid + 1, end));
    }
    else if(unary.find(action) != unary.end()) {
        return unary.at(action)(parse(mid + 1, end));
    }
    
    return std::make_shared<C>(std::stod(std::string(begin, end)));
}

std::string diff(const std::string &s) {
    std::string res;
    parse(s.begin(), s.end())
    ->eval()
    ->derivative()
    ->eval()
    ->print(res);
    return res;
}
______________________________________________
#include <cctype>
#include <regex>
#include <cmath>

using namespace std;

inline bool is_number(const string &token) { return isdigit(token.back()); }

string nb_to_string(int n) { return to_string(n); }
string nb_to_string(double n)
{
  string str = to_string(n);
  while (str.back() == '0') str.pop_back();
  if (str.back() == '.') str.pop_back();
  return str;
}

string operation(const string &op, const string &operand1, const string &operand2)
{
    if (is_number(operand1) && is_number(operand2))
    {
      if (op == "+") return nb_to_string(stod(operand1)+stod(operand2));
      if (op == "-") return nb_to_string(stod(operand1)-stod(operand2));
      if (op == "*") return nb_to_string(stod(operand1)*stod(operand2));
      if (op == "/") return nb_to_string(stod(operand1)/stod(operand2));
      if (op == "^") return nb_to_string(pow(stod(operand1), stod(operand2)));
    }
            
    if (op == "^" && operand2 == "0") return "1";
    if (op == "^" && operand2 == "1") return operand1;
    if (op == "+" && operand1 == "0") return operand2;
    if (op == "+" && operand2 == "0") return operand1;
    if (op == "-" && operand2 == "0") return operand1;
    if (op == "-" && operand1 == "0") return operation("*", "-1", operand2);
    if (op == "*" && operand1 == "1") return operand2;
    if (op == "*" && operand2 == "1") return operand1;
    if (op == "*" && (operand2 == "0" || operand1 == "0")) return "0";
    if (op == "/" && operand2 == "1") return operand1;
    
    return string("(") + op + " " + operand1 + " " + operand2 + ")";
}

tuple<string, string, int> differentiate(const vector<string> &tokens, int i)
{
  static const vector<string> bin_ops = {"+","-","*","/","^"};

  if (tokens[i] == "x") return make_tuple("x", "1", i+1);
  if (is_number(tokens[i])) return make_tuple(tokens[i], "0", i+1);
  
  string expression, derivative;
  
  //assert(tokens[i] == '(');
  i++;
  string op = tokens[i++];
  bool binary = (find(bin_ops.begin(), bin_ops.end(), op) != bin_ops.end());
  
  auto &&res1 = differentiate(tokens, i);
  auto &&res2 = binary ? differentiate(tokens, get<2>(res1)) : make_tuple("","",get<2>(res1));
  i = get<2>(res2);
  
  expression = binary ? operation(op, get<0>(res1), get<0>(res2)) : string("(") + op + " " + get<0>(res1) + ")";
  
  if (op == "+" || op == "-") derivative = operation(op, get<1>(res1), get<1>(res2));
  else if (op == "*") derivative = operation("+", operation("*", get<1>(res1), get<0>(res2)),
                                                  operation("*", get<0>(res1), get<1>(res2)));
  else if (op == "/") derivative = operation("/", operation("-", operation("*", get<1>(res1), get<0>(res2)),
                                                  operation("*", get<0>(res1), get<1>(res2))),
                                                  operation("^", get<0>(res2), "2"));
  else if (op == "^") derivative = operation("*", operation("*", get<0>(res2), get<1>(res1)),
                                                  operation("^", get<0>(res1), operation("-", get<0>(res2), "1"))); // assert(is_number(get<0>(res2)));
  else if (op == "exp") derivative = operation("*", get<1>(res1), string("(exp ") + get<0>(res1) + ")");
  else if (op == "ln") derivative = operation("/", get<1>(res1), get<0>(res1));
  else if (op == "cos") derivative = operation("*", get<1>(res1), operation("*", "-1", string("(sin ") + get<0>(res1) + ")"));
  else if (op == "sin") derivative = operation("*", get<1>(res1), string("(cos ") + get<0>(res1) + ")");
  else derivative = operation("*", get<1>(res1), operation("+", "1", operation("^", string("(tan ") + get<0>(res1) + ")", "2"))); // assert(op == "tan");
  
  //assert(tokens[i] == ')');
  return make_tuple(expression, derivative, i+1);
}

string diff(const string &s)
{
  static const regex tokenizer("-?[\\d]+|[()*+-/^x]|cos|sin|tan|exp|ln");
  vector<string> tokens(sregex_token_iterator(s.begin(), s.end(), tokenizer), sregex_token_iterator());
  return get<1>(differentiate(tokens, 0));
}
______________________________________________
#include <sstream>
#include <vector>
#include <map>
#include <cmath>
#include <functional>

using namespace std;

using func = function<double(double,double)>;

template<class T = void> struct power {
    const T operator ()(const T &lhs, const T &rhs) {
        return pow (lhs, rhs);
    }
};

map<string, func> oper {{"+", plus<double>()},{"-", minus<double>()},
              {"*", multiplies<double>()}, {"/", divides<double>()}, {"^", power<double>()} };

vector<string> tokenize2 (string expr) {

  string::iterator it = expr.begin () + 1;
  vector<string> tok;
  expr.pop_back ();
  
  while (it < expr.end()) {
      string buff;

      if (*it == '(') {
          do { buff += *it; } while (*it++ != ')');
      } else {
          while (*it && *it != ' ') buff += *it++;
      }
      tok.push_back(buff);
      it++;
  }
  return tok;
}
bool isnum (const string &exp) {
    for (auto &it : exp) {
        if (isalpha (it)) return false;
        if (isspace (it)) return false;
        if (oper[{it}]) return false;
    }
    return true;
}

string calc (string a, string op, string b) {
    ostringstream os;
  
    if (a == "0" || b == "0") {
        if (op == "*") return "0";
        if (op == "+") return a == "0" ? b : a;
        if (op == "-" && b == "0") return a;
    }

    if (a == "1" || b == "1") {
        if (op == "*") return a == "1" ? b : a;
        if (op == "^") return a;
        if (op == "/" && b == "1") return a;
    }

    if (isnum (a) && isnum (b)) {
        os << oper[op] (stod (a), stod (b));
    } else {
        os << "(" << op << " " << a << " " << b << ")";
    }
    return os.str();
}
string diff (const string &src) {
    
    if (count (src.begin(), src.end(), ' ') == 0) {
        if (src == "x") return "1";
        return "0";
    }

    vector expr = tokenize2 (src);
    string op = expr.front();

    if (oper[op]) {

        string arg1 = expr[1], arg2 = expr[2];
        string dx1 = diff (arg1), dx2 = diff (arg2);

        if (op == "+") {                   //  add : a + b => a' + b'
            return calc (dx1, op, dx2);
        } else if (op == "-") {            //  add : a - b => a' - b'
            return calc (dx1, op, dx2);
        } else if (op == "*") {            //  mul : a * b => a'* b + a * b'
            string a = calc (dx1, op, arg2), b = calc (arg1, op, dx2);
            return calc (a, "+", b);
        } else if (op == "/") {            //  div : a / b => (a'* b − b'* a) / (b * b)
            string a = calc (dx1, "*", arg2), b = calc (dx2, "*", arg1);
            string nom = calc (a, "-", b), den = calc (arg2, "^", "2");

            return calc (nom, "/", den);
        } else if (op == "^") {            // x² => 2 * x^(2-1) : * 2 (^ x (2 - 1))
            string ex = calc (arg2, "-", "1");
            arg1 = calc ("x", "^", ex);

            return calc (arg2, "*", arg1);
        }
    } else {
        string arg1 = expr[1], arg2, ex = diff (arg1);
      
        if (op == "ln") {
            return calc ("1", "/", arg1);
        }
        if (op == "cos") {
            arg2 = "(sin " + arg1 + ")";
            return calc ("-" + ex, "*", arg2);
        }
        if (op == "sin") {
            arg2 = "(cos " + arg1 + ')';
            return calc (ex, "*", arg2);
        }
        if (op == "exp") {
            arg2 = "(exp " + arg1 + ')';
            return calc (ex, "*", arg2);
        }
        if (op == "tan") {
            arg2 = "(cos " + arg1 + ')';
            arg2 = calc (arg2, "^", "2");
            return calc (ex, "/", arg2);
        }
    }

    return "";
}
______________________________________________
#include <string>
#include <string_view>
#include <sstream>
#include <cstdlib>
#include <cmath>
#include <memory>
using namespace std;

inline void ltrim(string_view& s)
{
  while(s[0] == ' ') s.remove_prefix(1);
}

class Expr;
typedef unique_ptr<Expr> ExprHandle;

struct VarMarker {} X;

class Expr
{
  char op;
  double num;
  ExprHandle a0, a1;
  inline void assign(char o, ExprHandle r0, ExprHandle r1)
  {
    op = o;
    num = 0;
    a0 = move(r0);
    a1 = move(r1);
  }
  inline void assign(double d)
  {
    op = '0';
    num = d;
    a0.reset();
    a1.reset();
  }
  ExprHandle moveme();
public:
  Expr() : op(), num(0), a0(), a1() {}
  explicit Expr(const VarMarker&) : op('x'), num(0), a0(), a1() {}
  Expr(char f, ExprHandle a) : op(f), num(0), a0(move(a)), a1() {}
  Expr(char b, ExprHandle a0, ExprHandle a1) : op(b), num(0), a0(move(a0)), a1(move(a1)) {}
  explicit Expr(double d) : op('0'), num(d), a0(), a1() {}
  Expr(const Expr& e) : op(e.op), num(e.num),
    a0(e.a0 ? e.a0->clone() : nullptr),
    a1(e.a1 ? e.a1->clone() : nullptr) {}
  Expr(Expr&& e) : op(e.op), num(e.num), a0(move(e.a0)), a1(move(e.a1)) {}
  
  ExprHandle clone() const {return ExprHandle{new Expr(*this)};};
  inline Expr& operator = (const Expr& e)
  {
    op = e.op;
    num = e.num;
    a0 = ExprHandle(e.a0 ? e.a0->clone() : nullptr);
    a1 = ExprHandle(e.a1 ? e.a1->clone() : nullptr);
    return *this;
  }
  inline Expr& operator = (Expr&& e)
  {
    op = e.op;
    num = e.num;
    a0 = move(e.a0);
    a1 = move(e.a1);
    return *this;
  }
  
  void diff();
  void simplify();
  string toString();
};

template<class... Args>
ExprHandle make_expr(Args&&... args)
{
  return make_unique<Expr>(forward<Args>(args)...);
}

ExprHandle Expr::moveme()
{
  return make_expr(move(*this));
}

ExprHandle parse(string_view& input)
{
  if(input[0] == '(')
  {
    char op = input[1];
    switch(op)
    {
      case '+': case '-': case '*': case '/': case '^':
      {
        input.remove_prefix(2);
        ltrim(input);
        ExprHandle a0 = parse(input);
        ltrim(input);
        ExprHandle a1 = parse(input);
        ltrim(input);
        input.remove_prefix(1);
        return make_expr(op, move(a0), move(a1));
      }
      case 's': case 'c': case 't': case 'e': case 'l':
      {
        input.remove_prefix(op == 'l' ? 3 : 4);
        ltrim(input);
        ExprHandle a = parse(input);
        ltrim(input);
        input.remove_prefix(1);
        return make_expr(op, move(a));
      }
      default:
        throw 1;
    }
  }
  else if(input[0] == 'x')
  {
    input.remove_prefix(1);
    return make_expr(X);
  }
  else
  {
    char *e;
    double value = strtod(input.data(), &e);
    input.remove_prefix(e - input.data());
    return make_expr(value);
  }
}

void Expr::diff()
{
  switch(op)
  {
    case 'x':
      op = '0'; // D x = 1
      num = 1;
      break;
    case '0':
      num = 0; // D 1 = 0
      break;
    case '+':
    case '-':
      // D(+- f g) = (+- Df Dg)
      a0->diff();
      a1->diff();
      break;
    case '*':
    {
      // D(* f g) = (+ (* Df g) (* f Dg))
      ExprHandle e0 = clone(), e1 = moveme();
      e0->a0->diff(); // (* Df g)
      e1->a1->diff(); // (* f Dg)
      assign('+', move(e0), move(e1));
      break;
    }
    case '/':
    {
      // D(/ f g) = (/ (- (* Df g) (* f Dg)) (^ g 2))
      ExprHandle den = make_expr('^', a1->clone(), make_expr(2)); // (^ g 2)
      op = '*';
      ExprHandle e0 = clone(), e1 = moveme();
      e0->a0->diff(); // (* Df g)
      e1->a1->diff(); // (* f Dg)
      ExprHandle num = make_expr('-', move(e0), move(e1)); // (- (* Df g) (* f Dg))
      assign('/', move(num), move(den));
      break;
    }
    default:
    {
      // Chain rule: D(f g) = (* (Df g) Dg)
      ExprHandle a = a0->clone();
      a->diff(); // Dg
      switch(op)
      {
        case '^':
        {
          // assert(a1->op == '0');
          // assert(a1->num >= 2);
          // D (^ x c) = (* c (^ x c-1))
          ExprHandle e = a1->clone();
          a1->num--;
          assign('*', move(e), moveme());
          break;
        }
        case 's':
          // D (s x) = (c x)
          op = 'c';
          break;
        case 'c':
          // D (c x) = (* -1 (s x))
          op = 's';
          assign('*', make_expr(-1), moveme());
          break;
        case 't':
          // D (t x) = (^ (c x) -2)
          op = 'c';
          assign('^', moveme(), make_expr(-2));
          break;
        case 'e':
          // D (e x) = (e x)
          break;
        case 'l':
          // D (l x) = (/ 1 x)
          assign('/', make_expr(1), move(a0));
          break;
      }
      assign('*', moveme(), move(a));
      break;
    }
  }
}

void Expr::simplify()
{
  //cerr << "Simplifying " << toString() << endl;
  switch(op)
  {
    case '0':
    case 'x':
      break;
    case '+':
      a0->simplify();
      a1->simplify();
      if(a0->op == '0' && a1->op == '0')
        assign(a0->num + a1->num); // (+ 1 2) => 3
      else if(a0->op == '0' && a0->num == 0)
        (*this) = move(*a1.release()); // (+ 0 ?) => ?
      else if(a1->op == '0' && a1->num == 0)
        (*this) = move(*a0.release()); // (+ ? 0) => ?
      break;
    case '-':
      a0->simplify();
      a1->simplify();
      if(a0->op == '0' && a1->op == '0')
        assign(a0->num - a1->num); // (- 3 2) => 1
      else if(a0->op == '0' && a0->num == 0)
      {
        op = '*';
        a0 = make_expr(-1); // (- 0 ?) => (* -1 ?)
      }
      else if(a1->op == '0' && a1->num == 0)
        (*this) = move(*a0.release()); // (- ? 0) => ?
      break;
    case '*':
      a0->simplify();
      a1->simplify();
      if(a0->op == '0' && a1->op == '0')
        assign(a0->num * a1->num); // (* 2 3) => 6
      else if((a0->op == '0' && a0->num == 0) ||
              (a1->op == '0' && a1->num == 1))
        (*this) = move(*a0.release()); // (* 0 ?) => 0, (* ? 1) => ?
      else if((a0->op == '0' && a0->num == 1) ||
              (a1->op == '0' && a1->num == 0))
        (*this) = move(*a1.release()); // (* ? 0) => 0, (* 1 ?) => ?
      else if(a0->op != '0' && a1->op == '0')
        a0.swap(a1); // (* () 3) => (* 3 ())
      break;
    case '/':
      a0->simplify();
      a1->simplify();
      if(a0->op == '0' && a1->op == '0')
        assign(a0->num / a1->num); // (/ 6 2) => 3
      else if((a0->op == '0' && a0->num == 0) ||
              (a1->op == '0' && a1->num == 1))
        (*this) = move(*a0.release()); // (/ 0 ?) => 0, (/ ? 1) => ?
      break;
    case '^':
      a0->simplify();
      a1->simplify();
      // assert(a1->op == '0')
      if(a0->op == '0')
        assign(pow(a0->num, a1->num)); // (^ 3 2) => 9
      else if(a0->op == '^')
      {
        // assert(a0->a1->op == '0')
        a0->a1->num *= a1->num;
        (*this) = move(*a0.release()); // (^ (^ ? 2) 3) => (^ ? 6)
        simplify();
      }
      else if(a1->num == 0)
        assign(1); // (^ ? 0) = 1
      else if(a1->num == 1)
        (*this) = move(*a0.release()); // (^ ? 1) => ?
      break;
    default:
      a0->simplify(); // (f ?)
      return;
  }
}

string Expr::toString()
{
  stringstream ss;
  switch(op)
  {
    case 'x':
      return "x"s;
    case '0':
      ss << num;
      return ss.str();
    case '+': case '-': case '*': case '/': case '^':
      ss << '(' << op << ' ' <<
        (a0 ? a0->toString() : "null"s) << ' ' <<
        (a1 ? a1->toString() : "null"s) << ')';
      return ss.str();
    default:
      ss << '(';
      switch(op)
      {
        case 'c': ss << "cos"; break;
        case 's': ss << "sin"; break;
        case 't': ss << "tan"; break;
        case 'e': ss << "exp"; break;
        case 'l': ss << "ln"; break;
      }
      ss << ' ' << (a0 ? a0->toString() : "null"s) << ')';
      return ss.str();
  }
}

string diff(string_view input)
{
  ExprHandle e = parse(input);
  //cerr << e->toString() << endl;
  e->diff();
  //cerr << e->toString() << endl;
  e->simplify();
  //cerr << e->toString() << endl << "====" << endl;
  return e->toString();
}
