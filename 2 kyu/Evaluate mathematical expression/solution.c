#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef const char* string;

string token;
void skip (int n, int (*equal) (int)) { while (n-- && *token) ++token; while (equal (*token)) ++token; }
void ws (int n) { skip (n, isblank); }

double val ();

double calcMultiplicative (double left) {
  ws (0);
  if (*token=='*') {
    ws (1); return calcMultiplicative (left * val());
  } else if (*token=='/') {
    ws (1); return calcMultiplicative (left / val());
  }
  return left;
}

double calcAdditive (double left) {
  ws (0);
  while (strchr ("+-*/", *token)) {
    if (*token=='*' || *token=='/')
      left = calcMultiplicative (left);
    if (*token=='+') {
      ws (1); left += calcMultiplicative (val ());
    } else if (*token=='-') {
      ws (1); left -= calcMultiplicative (val ());
    } else break;
  }
  return left;
}

double calcExpr () {
  ws (1);
  double v = calcAdditive (val ());
  ws (0); ++token;
  return v;
}

double val () {
  if (*token=='(') {
    return calcExpr ();
  } else if (*token=='-') {
    ++token;
    return -val ();
  } else {
    char* e; double v = strtod (token, &e); token = e;
    return v;
  }
}

double calculate (string expression) {
  token = expression; ws (0);
  return calcAdditive (val ());
}
_________________________________________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
#include <time.h>

/* ----------------
     Utilities
 ---------------- */

// debugging
#define DEBUG

static inline void* memdup(const void* src, size_t size) {
  return memcpy(malloc(size), src, size);
}

#define ALLOC(type, ...) \
  (type *)memdup((type []){__VA_ARGS__}, sizeof(type));

#define ERR_HANDLE(fmt, ...) \
  { \
    printf(fmt, __VA_ARGS__); \
    exit(-1); \
  }

/* ----------------
       Lexer
 ---------------- */

struct token {
  enum {
    T_HEAD = 1,
    T_NUM = 2,
    T_LPAREN = '(',
    T_RPAREN = ')',
    T_EXP = '^',
    T_MUL = '*',
    T_DIV = '/',
    T_MOD = '%',
    T_ADD = '+',
    T_SUB = '-'
  } type;
  double value;
  struct token* next;
};
typedef struct token token_t;

token_t* new_token(char type, double value) {
  return ALLOC(token_t, {
    .type = type,
    .value = value,
    .next = 0
  });
}

#ifdef DEBUG
static inline const char* tok_name(int type) {
  switch (type) {
    case 1:
      return "T_HEAD";
    case 2:
      return "T_NUM";
    case '(':
      return "T_LPAREN";
    case ')':
      return "T_RPAREN";
    case '^':
      return "T_EXP";
    case '*':
      return "T_MULTIPLY";
    case '/':
      return "T_DIVIDE";
    case '%':
      return "T_MODULUS";
    case '+':
      return "T_ADD";
    case '-':
      return "T_SUB";
    default:
      return "Unknown Token Type!";
  }
}

void print_tok(token_t* head) {
  for (token_t* tmp = head; tmp; tmp = tmp->next)
    printf("TOKEN(%s, %lf, %#lx, %#lx)\n", tok_name(tmp->type), tmp->value, tmp, tmp->next);
  return;
}
#endif

token_t* tokenize_expr(char* buffer) {

  #define TOK_APPEND(offset, entry) \
    { \
      offset->next = entry; \
      offset = offset->next; \
    }
    
  #define IS_NUM(input) \
    ('0' <= input && input <= '9')
    
  token_t* head = new_token(T_HEAD, 0), *tmp = head;
  char token;
  for (token = *buffer; *buffer; token = *(++buffer)) {
    if (IS_NUM(token)) {
      TOK_APPEND(tmp, new_token(T_NUM, strtod(buffer, &buffer))); 
      --buffer; // expensive-ish?
      continue;
    }
    switch (token) {
      case ' ':
        continue;
      case '\n':
        continue;
      case '(' ... ')':
        goto tok_apnd;
      case '^':
        goto tok_apnd;      
      case '*':
        goto tok_apnd;
      case '/':
        goto tok_apnd;
      case '%':
        goto tok_apnd;
      case '+':
        goto tok_apnd;
      case '-':
    tok_apnd:
        TOK_APPEND(tmp, new_token(token, 0));
        break;
      default:
        ERR_HANDLE("Error: Expected Token but received '%c' %s:%d\n", token, __FILE__, __LINE__);
        break;
    }
  }
  if (head->next)
    return head;
  ERR_HANDLE("Error: Token Stream is empty %s:%d\n", __FILE__, __LINE__);
}

static inline void destroy_list(token_t* head) {
  for (token_t* tmp = head; tmp; tmp = tmp->next)
    free(tmp);
  return;
}

/* ----------------
      Parser
 ---------------- */

struct node {
  token_t* token;
  struct node* left, *right;
};
typedef struct node node_t;

node_t* new_node(token_t* token, node_t* left, node_t* right) {
  return ALLOC(node_t, {
    .token = token,
    .left = left,
    .right = right
  });
}

/*
  it is too expensive to constantly pass references to a single pointer, more efficient to make it
  global in this case.
*/
token_t* current_token = 0;

// no semantics checking, we only focus on parsing at this phase
void eat_tok(int type) {
  if (!current_token || !current_token->next)
    return;
//    ERR_HANDLE("Error: Current token is NULL %s:%d\n", __FILE__, __LINE__);
  if (current_token->type != type)
    ERR_HANDLE("Error: Expected Token '%c' %s:%d\n", type, __FILE__, __LINE__);
  current_token = current_token->next;
  return;
}

node_t* parse(token_t*),
  *parse_expr(),
  *parse_term(),
  *parse_power(),
  *parse_unary(),
  *parse_factor();

static inline node_t* parse_integer();

node_t* parse(token_t* head) {
  current_token = head->next;
  return parse_expr();
}

// <expr>    ::= <term> ( "+" | "-" ) <expr> | <term>
node_t* parse_expr() {
  node_t* result = parse_term();
  token_t* tmp_token;
  char type;
  while ((type = current_token->type) && type == '+' || type == '-') {
    tmp_token = current_token;
    eat_tok(type);
    result = new_node(tmp_token, result, parse_term());
  }
  return result;
}

// <term>    ::= <power> ( "*" | "/" ) <term> | <power>
node_t* parse_term() {
  node_t* result = parse_power();
  token_t* tmp_token;
  char token;
  while ((token = current_token->type) && token == '*' || token == '/' || token == '%') {
    tmp_token = current_token;
    eat_tok(token);
    result = new_node(tmp_token, result, parse_power());
  }
  return result;
}

// <power>    ::= <unary> "^" <power> | <unary>
node_t* parse_power() {
  node_t* result = parse_unary();
  token_t* tmp_token;
  while (current_token->type == '^') {
    tmp_token = current_token;
    eat_tok(T_EXP);
    result = new_node(tmp_token, parse_power(), result);
  }
  return result;
}

// <unary>    ::= "-" <unary> | <factor>
node_t* parse_unary() {
  token_t* tmp_token;
  char token;
  if ((token = current_token->type) && current_token->next && token == '-') {
    tmp_token = current_token;
    eat_tok(token);
    return new_node(tmp_token, 0, parse_unary());
  } else
    return parse_factor();
}

// <factor>  ::= "(" <expr> ")" | <integer>
node_t* parse_factor() {
  node_t* result;
  if (current_token->type == '(') {
    eat_tok(T_LPAREN);
    result = parse_expr();
    eat_tok(T_RPAREN);
    return result;
  } else if (current_token->type == T_NUM)
    return parse_integer();
  ERR_HANDLE("Unreachable: %d %s:%d\n", current_token->type, __FILE__, __LINE__);
}

// <integer> ::= <digit> | <digit> <integer>
static inline node_t* parse_integer() {
  token_t* tmp_token = current_token;
  eat_tok(T_NUM);
  return new_node(tmp_token, 0, 0);
}

/* ----------------
        AST
 ---------------- */

double compile_ast(node_t*);
void destroy_ast(node_t*),
  dump_ast(node_t*);

// evaluate ast with simple postorder
double compile_ast(node_t* root) {
  if (!root)
    return 0;
/*
  if (!root->left && !root->right) // leaf node is always integer
    return root->token->value;
*/
  // traverse postorder again
  double l = compile_ast(root->left),
    r = compile_ast(root->right);
  switch (root->token->type) {
    case T_NUM: // avoid dereferencing 2 pointers, just check node type
      return root->token->value;
    case '^':
      return powl(l, r);
    case '*':
      return l * r;
    case '/':
      return l / r;
    case '%':
      return fmod(l, r);
    case '+':
      return l + r;
    case '-':
      return l - r; // handles unary as well, 0 - rvalue = - rvalue
    default:
      ERR_HANDLE("Unknown Operator! %s:%d\n", __FILE__, __LINE__);
  }
}

double calculate(const char* expression) {
  // lol, all my homies love memory leaks
  return compile_ast(parse(tokenize_expr(expression)));
}
_________________________________________________________________
#include <stdlib.h>

static size_t evalnexpr(const char *expr, double *res)
{
    char c, *p, ops[2];
    double opds[3];
    int n, nop, nopd, opmod, sign;
    union {
        double fp;
        unsigned long bin;
    } opd;
    opds[0] = nopd = nop = opmod = sign = 0;
    for (n = 0; ; ++n) {
        c = expr[n];
        if (c == ' ')
            continue;
        else if (c == ')')
            c = 0;
        else if (c == '(') {
            ++n;
            n += evalnexpr(expr+n, opds+nopd++);
        }
        if (!opmod || c == '(' || !c) {
            if (!opmod && c != '(') {
                opds[nopd] = strtod(expr+n, &p);
                if (expr+n == p) {
                    if (c == '-')
                        sign = ~sign;
                    continue;
                }
                ++nopd;
                n = p - expr - 1;
            }
            if (sign) {
                opd.fp = opds[nopd-1];
                opd.bin ^= (unsigned long)sign << 63;
                opds[nopd-1] = opd.fp;
                sign = 0;
            }
            if (nopd > 1 && (!c || ops[nop-1] == '*' || ops[nop-1] == '/')) {
                do {
                    --nopd;
                    switch (ops[--nop]) {
                    case '*':
                        opds[nopd-1] *= opds[nopd];
                        break;
                    case '/':
                        opds[nopd-1] /= opds[nopd];
                        break;
                    case '+':
                        opds[nopd-1] += opds[nopd];
                        break;
                    case '-':
                        opds[nopd-1] -= opds[nopd];
                        break;
                    }
                } while (nopd > 1 && !c);
            }
            if (!c)
                return *res = *opds, n;
        }
        else {
            if (nop == 1 && (c == '+' || c == '-')) {
                if (*ops == '+')
                    opds[0] += opds[1];
                else
                    opds[0] -= opds[1];
                --nop, --nopd;
            }
            ops[nop++] = c;
        }
        opmod = ~opmod;
    }
    return *res = *opds, n;
}

double calculate(const char *expr)
{
    double res;
    evalnexpr(expr, &res);
    return res;
}
_____________________________________________________________________
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef unsigned long ulong;

double expression(char* exp, ulong *i);
double term(char* exp, ulong *i);
double factor(char* exp, ulong *i);
double number(char* exp, ulong *i);

bool done(char* exp, ulong i) 
{
    return i < 0 || i > strlen(exp);
}

char peek(char* exp, ulong i) 
{
    return done(exp, i) ? '\0' : exp[i];  
}

char shift(char* exp, ulong *i) 
{
    char c = exp[*i];
    *i += 1;
    return c;
}

char* normalise(const char* exp)
{
    char* dest = (char*) calloc(strlen(exp), sizeof(char));
    char* buf = dest;
    while (*exp != '\0')
    {
        if (*exp != ' ') *buf++ = *exp;
        *exp++;
    }
    *buf = '\0';
    return dest;
}

double expression(char* exp, ulong *i)
{
    double num = term(exp, i);
    while (peek(exp, *i) == '+' || peek(exp, *i) == '-') 
    {
        if (shift(exp, i) == '+') num += term(exp, i);
        else num -= term(exp, i);
    }
    return num;
}

double term(char* exp, ulong *i)
{
    double num = factor(exp, i);
    while (peek(exp, *i) == '*' || peek(exp, *i) == '/') 
    {
        if (shift(exp, i) == '*') num *= factor(exp, i);
        else num /= factor(exp, i);
    }
    return num;
}

double factor(char* exp, ulong *i)
{
    if (isdigit(peek(exp, *i))) return number(exp, i);
    if (peek(exp, *i) == '(') 
    {
        shift(exp, i);
        double nxt = expression(exp, i);
        shift(exp, i);
        return nxt;
    }
    if (peek(exp, *i) == '-') 
    {
        shift(exp, i);
        return -factor(exp, i);
    }
    return 0.0;
}

double number(char* exp, ulong *i) 
{
    char* dest = (char*) calloc(strlen(exp), sizeof(char));
    char* buf = dest;
    while (isdigit(peek(exp, *i)) || peek(exp, *i) == '.') 
    {
        *buf++ = shift(exp, i);
    }
    *buf = '\0';
    char *ptr;
    double ret = strtod(dest, &ptr);
    free(dest);
    dest = NULL;
    return ret;
}

double calculate (const char* input)
{
    char* exp = normalise(input);
    ulong i = 0;
    printf("%s\n", exp);
    return expression(exp, &i);
}
