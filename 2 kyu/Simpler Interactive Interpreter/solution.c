#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

typedef int Type;

struct variable {
  char *name;
  Type value;
  struct variable *next;
};

enum StatusCodes {
    OK_CODE = 0,
    EMPTY_CODE = 1,
    INVALID_SYNTAX = 2,
    NAME_ERROR = 3,
    DIVISION_BY_ZERO = 4,
};

typedef enum StatusCodes Err;

struct tokens {
  char **ts;
  char *buf;
};

#define TOKENS_INIT {0}

enum node_type {
  NODE_TYPE_ADD,
  NODE_TYPE_ASS,
  NODE_TYPE_DIV,
  NODE_TYPE_MOD,
  NODE_TYPE_MUL,
  NODE_TYPE_NEG,
  NODE_TYPE_NUM,
  NODE_TYPE_SUB,
  NODE_TYPE_VAR,
};

struct ast_node {
  enum node_type type;
  union {
    Type num;
    const char *var;
    struct ast_node *left;
  };
  struct ast_node *right;
};

struct ast_repo {
  struct ast_node *nodes;
  bool *taken;
  size_t len;
};

#define AST_REPO_INIT {0}

unsigned int hash(const char *str);
int initInterpreter();
void closeInterpreter();
void tokenize(struct tokens *tokens, const char *input);
void tokens_destroy(struct tokens *tokens);
Err parse(struct ast_node **result, struct ast_repo *repo, char **tokens);
void ast_repo_destroy(struct ast_repo *repo);
int evaluate(const char *input, Type *result);

static Err eval(const struct ast_node *node, Type *result);

static Err parse_assignment(struct ast_node **result, struct ast_repo *repo,
    char **tokens, size_t len);

/*
 * http://www.cse.yorku.ca/~oz/hash.html
 */
unsigned int hash(const char *str)
{
  unsigned int hash = 5381;
  int c;
  while ((c = *str++))
    hash = (hash * 33) ^ c;
  return hash;
}

static size_t rev_index(size_t len, size_t i)
{
  return len - i - 1;
}

#define SLOTS 31

struct variable *variables[SLOTS] = {NULL};

static size_t get_slot(const char *str)
{
  return hash(str) % SLOTS;
}

static void set_var(const char *varname, Type value)
{
  size_t slot = get_slot(varname);
  struct variable *prev = NULL;
  struct variable *var = variables[slot];
  while (var) {
    if (strcmp(varname, var->name) == 0) {
      var->value = value;
      return;
    }
    prev = var;
    var = var->next;
  }
  var = malloc(sizeof(*var));
  var->next = NULL;
  var->name = strdup(varname);
  var->value = value;
  if (prev)
    prev->next = var;
  else
    variables[slot] = var;
}

static Err get_var(const char *varname, Type *result)
{
  size_t slot = get_slot(varname);
  struct variable *var = variables[slot];
  while (var) {
    if (strcmp(varname, var->name) == 0)
      break;
    var = var->next;
  }
  if (!var)
    return NAME_ERROR;
  *result = var->value;
  return 0;
}

static void clear_slot(size_t slot)
{
  struct variable *var = variables[slot];
  while (var) {
    struct variable *next = var->next;
    free(var->name);
    free(var);
    variables[slot] = var = next;
  }
}

static void clear_variables()
{
  for (size_t slot = 0; slot < SLOTS; slot++)
    clear_slot(slot);
}

int initInterpreter()
{
  return 0;
}

void closeInterpreter()
{
  clear_variables();
}

static size_t count_printable(const char *s)
{
  size_t count = 0;
  for (; *s; s++)
    if (isgraph(*s))
      count++;
  return count;
}

static const char *skip_whitespace(const char *s)
{
  while (*s && !isgraph(*s))
    s++;
  return s;
}

static const char *copy_number(char **b, const char *s)
{
  while (isdigit(*s) || *s == '.')
    *(*b)++ = *s++;
  return s;
}

static const char *copy_ident(char **b, const char *s)
{
  while (*s == '_' || isalnum(*s))
    *(*b)++ = *s++;
  return s;
}

void tokenize(struct tokens *tokens, const char *input)
{
  size_t max_tokens = count_printable(input);
  if (!max_tokens)
    return;
  tokens->ts = calloc(max_tokens + 1, sizeof(*tokens->ts));
  tokens->buf = calloc(2 * max_tokens, sizeof(*tokens->buf));
  char **t = tokens->ts;
  char *b = tokens->buf;
  const char *s = input;
  while (*(s = skip_whitespace(s))) {
    *t++ = b;
    if (isdigit(*s)) {
      s = copy_number(&b, s);
    } else if (*s == '_' || isalpha(*s)) {
      s = copy_ident(&b, s);
    } else {
      *b++ = *s++;
    }
    *b++ = '\0';
  }
}

void tokens_destroy(struct tokens *tokens)
{
  free(tokens->ts);
  tokens->ts = NULL;
  free(tokens->buf);
  tokens->buf = NULL;
}

static size_t count_tokens(char **tokens)
{
  if (!tokens)
    return 0;
  size_t count = 0;
  for (char **t = tokens; *t; t++)
    count++;
  return count;
}

static bool token_is_single_char(const char *token)
{
  return !token[1];
}

static bool token_is_char(const char *token, char c)
{
  return token_is_single_char(token) && *token == c;
}

static char **find_token(char **tokens, size_t len,
    bool (predicate)(const char *token))
{
  size_t depth = 0;
  for (size_t i = 0; i < len; i++) {
    char *t = tokens[i];
    if (token_is_char(t, '(')) {
      depth++;
    } else if (token_is_char(t, ')')) {
      if (!depth)
        break;
      depth--;
    } else if (!depth && predicate(tokens[i])) {
      return tokens + i;
    }
  }
  return NULL;
}

static char **find_token_rev(char **tokens, size_t len,
    bool (predicate)(const char *token))
{
  size_t depth = 0;
  for (size_t j = 0; j < len; j++) {
    size_t i = rev_index(len, j);
    char *t = tokens[i];
    if (token_is_char(t, ')')) {
      depth++;
    } else if (token_is_char(t, '(')) {
      if (!depth)
        break;
      depth--;
    } else if (!depth && predicate(tokens[i])) {
      return tokens + i;
    }
  }
  return NULL;
}

static bool token_is_var(const char *token)
{
  return *token == '_' || isalpha(*token);
}

static bool token_is_num(const char *token)
{
  return isdigit(*token);
}

static bool token_is_var_or_num_or_left_brace(const char *token)
{
  return *token == '_' || isalnum(*token) || token_is_char(token, ')');
}

static bool token_is_add(const char *token)
{
  if (!token_is_single_char(token))
    return false;

  switch(*token) {
  case '+':
  case '-':
    return true;
  default:
    return false;
  }
}

static bool token_is_assignment(const char *token)
{
  return token_is_char(token, '=');
}

static bool token_is_mul(const char *token)
{
  if (!token_is_single_char(token))
    return false;

  switch (*token) {
  case '*':
  case '/':
  case '%':
    return true;
  default:
    return false;
  }
}

static void ast_repo_init(struct ast_repo *repo, size_t len)
{
  repo->nodes = calloc(len, sizeof(*repo->nodes));
  repo->taken = calloc(len, sizeof(*repo->taken));
  repo->len = len;
}

void ast_repo_destroy(struct ast_repo *repo)
{
  free(repo->nodes);
  repo->nodes = NULL;

  free(repo->taken);
  repo->taken = NULL;

  repo->len = 0;
}

static struct ast_node *ast_node_alloc(struct ast_repo *repo)
{
  struct ast_node *node = NULL;
  for (size_t i = 0; i < repo->len; i++) {  /* GCOV_EXCL_LINE */
    if (!repo->taken[i]) {
      repo->taken[i] = true;
      node = repo->nodes + i;
      break;
    }
  }
  return node;
}

static struct ast_node *new_node(struct ast_repo *repo, enum node_type type)
{
  struct ast_node *node = ast_node_alloc(repo);
  node->type = type;
  node->left = NULL;
  node->right = NULL;
  return node;
}

static struct ast_node *new_number(struct ast_repo *repo, Type number)
{
  struct ast_node *node = new_node(repo, NODE_TYPE_NUM);
  node->num = number;
  return node;
}

static struct ast_node *new_variable(struct ast_repo *repo, char *var)
{
  struct ast_node *node = new_node(repo, NODE_TYPE_VAR);
  node->var = var;
  return node;
}

static struct ast_node *new_negative(struct ast_repo *repo,
    struct ast_node *left)
{
  struct ast_node *node = new_node(repo, NODE_TYPE_NEG);
  node->left = left;
  return node;
}

static enum node_type binop_char_to_node_type(char binop)
{
  switch (binop) {
  case '+':
    return NODE_TYPE_ADD;
  case '=':
    return NODE_TYPE_ASS;
  case '/':
    return NODE_TYPE_DIV;
  case '%':
    return NODE_TYPE_MOD;
  case '*':
    return NODE_TYPE_MUL;
  case '-':
  default:
    return NODE_TYPE_SUB;
  }
}

static struct ast_node *new_binop(struct ast_repo *repo, char binop,
    struct ast_node *left, struct ast_node *right)
{
  enum node_type type = binop_char_to_node_type(binop);
  struct ast_node *node = new_node(repo, type);
  node->left = left;
  node->right = right;
  return node;
}

static Err parse_num(struct ast_node **result, struct ast_repo *repo,
    char **tokens, size_t len, bool negative)
{
  if (len != 1)
    return INVALID_SYNTAX;

  Type number = atoi(*tokens);
  if (negative)
    number = -number;

  *result = new_number(repo, number);
  return 0;
}

static bool flips_sign(char c)
{
  return c == '-';
}

static Err parse_var(struct ast_node **result, struct ast_repo *repo,
    char *token, bool negative)
{
  if (!token_is_var(token))
    return INVALID_SYNTAX;

  *result = new_variable(repo, token);
  if (negative)
    *result = new_negative(repo, *result);

  return 0;
}

static bool is_braced(char **tokens, size_t len)
{
  return len >= 3 && token_is_char(*tokens, '(')
    && token_is_char(tokens[len - 1], ')');
}

static Err parse_brace(struct ast_node **result, struct ast_repo *repo,
    char **tokens, size_t len, bool negative)
{
  if (!is_braced(tokens, len))
    return INVALID_SYNTAX;

  Err err = parse_assignment(result, repo, tokens + 1, len - 2);
  if (err)
    return err;

  if (negative)
    *result = new_negative(repo, *result);

  return 0;
}

static Err parse_unary(struct ast_node **result, struct ast_repo *repo,
    char **tokens, size_t len)
{
  bool negative = false;
  for (; token_is_add(*tokens); len--, tokens++)
    negative ^= flips_sign(**tokens);

  if (token_is_var(*tokens))
    return parse_var(result, repo, *tokens, negative);

  if (token_is_num(*tokens))
    return parse_num(result, repo, tokens, len, negative);

  return parse_brace(result, repo, tokens, len, negative);

}

static Err parse_mul(struct ast_node **result, struct ast_repo *repo,
    char **tokens, size_t len)
{
  char **t = find_token_rev(tokens, len, token_is_mul);
  if (!t)
    return parse_unary(result, repo, tokens, len);

  size_t i = t - tokens;
  if (!i)
    return INVALID_SYNTAX;

  Err err;
  struct ast_node *left = NULL;
  if ((err = parse_assignment(&left, repo, tokens, i)))
    return err;

  struct ast_node *right = NULL;
  if ((err = parse_assignment(&right, repo, tokens + i + 1, len - i - 1)))
    return err;

  *result = new_binop(repo, *tokens[i], left, right);
  return 0;
}

static Err parse_add(struct ast_node **result, struct ast_repo *repo,
    char **tokens, size_t len)
{
  for (size_t j = 0; j < len; j++) {  /* GCOV_EXCL_LINE */
    size_t i = rev_index(len, j);
    char **t = find_token_rev(tokens, len - j, token_is_add);
    if (!t)
      break;

    i = t - tokens;
    j = rev_index(len, i);
    if (!j)
      return INVALID_SYNTAX;

    if (!i)
      break;

    if (!token_is_var_or_num_or_left_brace(tokens[i - 1]))
      continue;

    Err err;
    struct ast_node *left;
    if ((err = parse_assignment(&left, repo, tokens, i)))
      return err;

    struct ast_node *right;
    if ((err = parse_assignment(&right, repo, tokens + i + 1,
            len - i - 1 )))
      return err;

    *result = new_binop(repo, *tokens[i], left, right);
    return 0;
  }

  return parse_mul(result, repo, tokens, len);
}

static Err parse_assignment(struct ast_node **result, struct ast_repo *repo,
    char **tokens, size_t len)
{
  if (!len)
    return INVALID_SYNTAX;

  char **t = find_token(tokens, len, token_is_assignment);
  if (!t)
    return parse_add(result, repo, tokens, len);

  if (t - tokens != 1)
    return INVALID_SYNTAX;

  Err err;
  struct ast_node *left;
  if ((err = parse_var(&left, repo, *tokens, false)))
    return err;

  struct ast_node *right;
  if ((err = parse_assignment(&right, repo, tokens + 2, len - 2)))
    return err;

  *result = new_binop(repo, *tokens[1], left, right);
  return 0;
}

Err parse(struct ast_node **result, struct ast_repo *repo, char **tokens)
{
  size_t len = count_tokens(tokens);
  if (!len)
    return EMPTY_CODE;
  ast_repo_init(repo, len);
  return parse_assignment(result, repo, tokens, len);
}

static Err eval_ass(const struct ast_node *node, Type *result)
{
  Err err = eval(node->right, result);
  if (err)
    return err;
  set_var(node->left->var, *result);
  return 0;
}

static Err eval_binop(const struct ast_node *node, Type *result)
{
  Err err;
  Type left, right;

  if ((err = eval(node->left, &left)))
    return err;

  if ((err = eval(node->right, &right)))
    return err;

  switch (node->type) {
  case NODE_TYPE_ADD:
    *result = left + right;
    return 0;
  case NODE_TYPE_DIV:
    if (!right)
      return DIVISION_BY_ZERO;
    *result = left / right;
    return 0;
  case NODE_TYPE_MOD:
    if (!right)
      return DIVISION_BY_ZERO;
    *result = left % right;
    return 0;
  case NODE_TYPE_MUL:
    *result = left * right;
    return 0;
  case NODE_TYPE_SUB:
  default:
    *result = left - right;
    return 0;
  }
}

static Err eval_neg(const struct ast_node *node, Type *result)
{
  Err err;
  if ((err = eval(node->left, result)))
    return err;
  *result = -1 * *result;
  return 0;
}

static Err eval_num(const struct ast_node *node, Type *result)
{
  *result = node->num;
  return 0;
}

static Err eval_var(const struct ast_node *node, Type *result)
{
  return get_var(node->var, result);
}

static Err (*get_evalfunc(const struct ast_node *node))
  (const struct ast_node *node, Type *result)
{
  switch (node->type) {
  case NODE_TYPE_NEG:
    return eval_neg;
  case NODE_TYPE_NUM:
    return eval_num;
  case NODE_TYPE_VAR:
    return eval_var;
  case NODE_TYPE_ASS:
    return eval_ass;
  case NODE_TYPE_ADD:
  case NODE_TYPE_DIV:
  case NODE_TYPE_MOD:
  case NODE_TYPE_MUL:
  case NODE_TYPE_SUB:
  default:
    return eval_binop;
  }
}

static Err eval(const struct ast_node *node, Type *result)
{
  return get_evalfunc(node)(node, result);
}

int evaluate(const char *input, Type *result)
{
  Err err = EMPTY_CODE;
  if (!input)
    goto exit;

  struct tokens tokens = TOKENS_INIT;
  tokenize(&tokens, input);

  struct ast_repo repo = AST_REPO_INIT;
  struct ast_node *node = NULL;
  if ((err = parse(&node, &repo, tokens.ts)))
    goto cleanup;

  err = eval(node, result);
cleanup:
  ast_repo_destroy(&repo);
  tokens_destroy(&tokens);
exit:
  return err;
}

________________________________________________________
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

#define HASHSIZE 101

#define IS_VAR(x) (x == '_' || isalpha(x))

typedef int Type;

enum StatusCodes { OK_CODE, EMPTY_CODE, VAR_ERROR, ZERO_DIVISON, PARENTH_ERR, OPER_ERR, INVALID_CHAR };
enum {NONE, INTEGER, CHAR, DBLE, HASHV};
int status;

struct hashv {
    char *key;
    double val;
};

typedef union _Data {
  int i;
  char c;
  double d;
  struct hashv h;
} Data;

typedef struct node {
    Data data;
    struct node *next;
} Node;

typedef struct {
    int type, size;
    Node *root;
} Stack;

const Data nul = {0};

Stack *new (int type) {
    Stack *next = malloc (sizeof(Stack));
    next->root = NULL;
    next->type = type;
    next->size = 0;
    return next;
  }
_Bool is_empty (const Stack *stack) {
    return ((stack->root == NULL) ? 1 : 0);
}
void push (Stack *stack, void *raw) {
    stack->size++;
    Node *head = stack->root;

    Data data;
    switch (stack->type) {
        case INTEGER : data.i = *(int *)raw; break;
        case CHAR : data.c = *(char *)raw; break;
        case DBLE : data.d = *(double *)raw; break;
        case HASHV :

            data.h = *(struct hashv *)raw;
            data.h.key = strdup (data.h.key);

            while (head) {
                Data *curr = &head->data;

                if (strcmp (curr->h.key, data.h.key) == 0) {
                    curr->h.val = data.h.val;
                    return;
                }
                head = head->next;
            }
            break;
        default : break;
    }

    Node *cell = stack->root;
    stack->root = malloc (sizeof (Node));
    stack->root->data = data;
    stack->root->next = cell;
  }
Data pop (Stack *stack) {

    if (is_empty(stack)) return nul;
    stack->size--;
    Node *cell = stack->root;
    Data value = stack->root->data;
    stack->root = stack->root->next;

    free (cell);

    return value;
}
Data top (const Stack *stack) {
    return (is_empty(stack)) ? nul : stack->root->data;
}

struct hashv *lookup (const Stack *stack, char *key) {

    Node *root = stack->root;

    while (root) {

        Data *curr = &root->data;
        if (strcmp (curr->h.key, key) == 0) {
            return &curr->h;
        }

        root = root->next;
    }
    return NULL;
}

int getsub (char *it) {
    int pile = 0, index = -1;
    int size = strlen (it);

    do {
        if (*it == '(') pile++;
        if (*it == ')') pile--;
        if (pile == 0) return index;
        index++;
    } while (*it++ != '\0');

    return size;
}
int getop (char c) {
    if (c == '-' || c == '+') return 1;
    if (c == '*' || c == '/' || c == '%') return 2;
    return 0;
}

double operation (double a, double b, char op) {

    if (b == 0 && (op == '/' || op == '%')) {
        status = ZERO_DIVISON;
        return 0;
    }
    double val;

    switch (op) {
        case '+' : val = a + b; break;
        case '-' : val = a - b; break;
        case '*' : val = a * b; break;
        case '/' : val = a / b; break;
        case '%' : val = fmod (a, b); break;
    }

    return val;
}
double calc (char *expr) {
    const int size = strlen (expr);
    char *it = expr;

    bool running = true;
    int i, sign = 1;
    double val;
    char buff[2048];

    Stack *ops = new (CHAR), *values = new (DBLE);
    static Stack vars = {HASHV, 0, NULL};

    while (running) {

        if (*it == '-' && getop (*(it - 1))) {
            sign = -1;
        }

        if (IS_VAR (*it)) {

            i = 0;
            while (IS_VAR (*it) || isdigit (*it)) buff[i++] = *it++;
            buff[i] = '\0';

            struct hashv *np = lookup (&vars, buff);

            if (np == NULL) {
                status = VAR_ERROR;
            } else {
                val = np->val * sign;
                sign = 1;
                push (values, &val);
            }

        } else if (isdigit (*it)) {
            val = strtod (it, &it) * sign;
            push (values, &val);

            sign = 1;
        } else if (getop (*it)) {

            while (!is_empty (ops) && getop (top(ops).c) >= getop (*it)) {
                char op = pop (ops).c;
                double b = pop (values).d, a = pop (values).d;
                val = operation (a, b, op);
                push (values, &val);
            }

            push (ops, &*it);
            it++;
        } else if (*it == '=') {
            status = OK_CODE;
            val = calc (it + 1) * sign;
            struct hashv np = {buff, val, NULL};
            push (&vars, &np);
            return val;
        } else if (*it == '(') {
            int len = getsub (it);
            memcpy (buff, it + 1, len);
            buff[len] = '\0';
            val = calc (buff);
            push (values, &val);

            it += (len + 2);
        } else {
            if (*it != ' ') status = INVALID_CHAR;
                
            it++;
        }

        if ((it - expr) >= size) running = false;
    }

    while (!is_empty (ops)) {
        char op = pop (ops).c;
        double b = pop (values).d, a = pop (values).d;
        val = operation (a, b, op);
        push (values, &val);
    }

    return top (values).d;
}
int check (char *input) {
    char *expr = strdup (input), *it = expr;
    const int size = strlen (expr);

    int par = 0, nop = 0, nval = 0, spa = 0;

    while (*it) {
        if (isdigit (*it)) {
            strtod (it, &it);
            nval++;
        }
        if (IS_VAR (*it)) {

            while (IS_VAR (*it) || isdigit (*it)) it++;

            nval++;
        }
        if (getop (*it)) nop++;
        if (*it == '(')  par++;
        if (*it == ')')  par--;
        if (*it == ' ')  spa++;
        if (*it == '=') {
            if (it == &expr[size - 1]) return OPER_ERR;
            nop++;
        }

        if ((it - expr) < size) it++;
    }
    if (spa == size) return EMPTY_CODE;
    if (par != 0) return PARENTH_ERR;

    if (nval > 1 && nop == 0) return OPER_ERR;
    if (nop >= nval) return OPER_ERR;

    return OK_CODE;
  }
int initInterpreter () {
    return OK_CODE;
}
void closeInterpreter (void) {
    return;
}

int evaluate (char *input, Type *result) {
  /* evaluate: evaluate the string expression, and return a status code
  (any value other than OK_CODE and EMPTY_CODE is treated as an error).
  The result of evaluating the expression is placed in a variable
  by the pointer 'result' if the function returns OK_CODE. */
    status = check (input);

    if (status == OK_CODE) {
        *result = calc (input);
    } else {
        *result = 0;
    }

    return status;
}

________________________________________________________
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//-----

typedef int Type;

// Status codes
enum StatusCodes {
    OK_CODE = 0,          // Success
    EMPTY_CODE = 1,       // Input string consists entirely of whitespaces
    SYNTAX_ERROR_CODE,
    UNKNOWN_VAR_CODE,
    DIV_BY_0_CODE
};

typedef struct token_s {
    int type; // "+-*/%()", 'n' - number, 'v' - variable
    Type num;
    char var[];
} token_s;

typedef struct interpreter_s {
    token_s **var;
    size_t n_var;
} interpreter_s;

static interpreter_s Ipr = {};

//-----

static token_s * tok_new (int type) {
    token_s *tok = malloc(sizeof(token_s));
    tok->type = type;
    return tok;
}

static token_s * tok_new_num (Type num) {
    token_s *tok = malloc(sizeof(token_s));
    tok->type = 'n';
    tok->num = num;
    return tok;
}

static token_s * tok_new_var (const char *name, size_t name_len) {
    token_s *tok = malloc(sizeof(token_s) + 1 + name_len);
    tok->type = 'v';
    memcpy(tok->var, name, name_len);
    tok->var[name_len] = 0;
    return tok;
}

//-----

static int get_var (const char *name, Type *value)
{
    for (size_t i = 0; i < Ipr.n_var; ++i) {
        if (strcmp(Ipr.var[i]->var, name) == 0) {
            *value = Ipr.var[i]->num;
            return OK_CODE;
        }
    }

    *value = 0;
    return UNKNOWN_VAR_CODE;
}

static void set_var (const char *name, Type value)
{
    for (size_t i = 0; i < Ipr.n_var; ++i) {
        if (strcmp(Ipr.var[i]->var, name) == 0) {
            Ipr.var[i]->num = value;
            return;
        }
    }

    size_t i = Ipr.n_var++;
    Ipr.var = realloc(Ipr.var, Ipr.n_var*sizeof(token_s *));
    Ipr.var[i] = tok_new_var(name, strlen(name));
    Ipr.var[i]->num = value;
}

//-----

/* initInterpreter: initialize the interpreter if necessary and return
   a status code (any value other than OK_CODE is treated as an error) */
int initInterpreter(void)
{
    return OK_CODE;
}

/* closeInterpreter: close the interpreter and free memory if necessary */
void closeInterpreter(void)
{
    if (Ipr.var) {
        for (size_t i = 0; i < Ipr.n_var; ++i) {
            free(Ipr.var[i]);
        }
        free(Ipr.var);
    }
}


/* evaluate: evaluate the string expression, and return a status code
   (any value other than OK_CODE and EMPTY_CODE is treated as an error).
   The result of evaluating the expression is placed in a variable
   by the pointer 'result' if the function returns OK_CODE. */
int evaluate (char *input, Type *result)
{
    int err = OK_CODE;

    token_s **tokens = NULL;
    size_t n_tokens = 0;

    token_s *token = NULL;
    const char *s_begin;

    while (*input) {
        if (isspace(*input)) { ++input; continue; }

        if (isalpha(*input) || *input == '_') {
            s_begin = input;
            do { ++input; } while (*input && (*input == '_' || isalnum(*input)));
            token = tok_new_var(s_begin, input - s_begin);
        } else if (isdigit(*input)) {
            token = tok_new_num(0);
            do {
                token->num = token->num*10 + (*input - '0');
                ++input;
            } while (isdigit(*input));
        } else {
            token = tok_new(*input);
            ++input;
        }

        if (token) {
            tokens = realloc(tokens, (n_tokens + 1)*sizeof(token_s *));
            tokens[n_tokens++] = token;
            token = NULL;
        }
    }

    if (n_tokens == 0) {
        err = EMPTY_CODE;
    }

    // replace variables with values
    for (size_t i = 0; i < n_tokens; ++i) {
        if (tokens[i]->type != 'v') continue;
        if (i + 1 < n_tokens && tokens[i + 1]->type == '=') continue;
        Type value = 0;
        if (get_var(tokens[i]->var, &value) != OK_CODE) { err = UNKNOWN_VAR_CODE;  }
        free(tokens[i]);
        tokens[i] = tok_new_num(value);
    }

    while (n_tokens > 1) {
        size_t n_tokens_prev = n_tokens;

        // processing '(', ')'
        for (size_t i = 0; i + 2 < n_tokens; ++i) {
            if (tokens[i]->type == '(' && tokens[i + 1]->type == 'n' && tokens[i + 2]->type == ')') {
                free(tokens[i]);
                free(tokens[i + 2]);
                tokens[i] = tokens[i + 1];
                if (n_tokens > i + 3) {
                    memmove(tokens + i + 1, tokens + i + 3, (n_tokens - (i + 3))*sizeof(token_s *));
                }
                n_tokens -= 2;
            }
        }

        // processing '*', '/', '%'
        for (size_t i = 1; i + 1 < n_tokens;) {
            if (strchr("*/%", tokens[i]->type)) {
                if (tokens[i - 1]->type != 'n') { ++i; continue; }
                if (tokens[i + 1]->type != 'n') { ++i; continue; }

                switch (tokens[i]->type) {
                case '*':
                    tokens[i - 1]->num *= tokens[i + 1]->num;
                    break;
                case '/':
                    if (tokens[i + 1]->num == 0) {
                        err = DIV_BY_0_CODE;
                        tokens[i - 1]->num = 0;
                    } else {
                        tokens[i - 1]->num /= tokens[i + 1]->num;
                    }
                    break;
                case '%':
                    if (tokens[i + 1]->num == 0) {
                        err = DIV_BY_0_CODE;
                        tokens[i - 1]->num = 0;
                    } else {
                        tokens[i - 1]->num %= tokens[i + 1]->num;
                    }
                    break;
                }

                free(tokens[i]);
                free(tokens[i + 1]);
                if (n_tokens > i + 2) {
                    memmove(tokens + i, tokens + i + 2, (n_tokens - (i + 2))*sizeof(token_s *));
                }
                n_tokens -= 2;
            } else {
                ++i;
            }
        }

        // processing '+', '-'
        for (size_t i = 1; i + 1 < n_tokens;) {
            if (tokens[i]->type == '+' || tokens[i]->type == '-') {
                if (tokens[i - 1]->type != 'n') { ++i; continue; }
                if (tokens[i + 1]->type != 'n') { ++i; continue; }

                if (i >= 2 && strchr("*/%", tokens[i - 2]->type)) { ++i; continue; }
                if (i + 2 < n_tokens && strchr("*/%", tokens[i + 2]->type)) { ++i; continue; }

                switch (tokens[i]->type) {
                case '+':
                    tokens[i - 1]->num += tokens[i + 1]->num;
                    break;
                case '-':
                    tokens[i - 1]->num -= tokens[i + 1]->num;
                    break;
                }

                free(tokens[i]);
                free(tokens[i + 1]);
                if (n_tokens > i + 2) {
                    memmove(tokens + i, tokens + i + 2, (n_tokens - (i + 2))*sizeof(token_s *));
                }
                n_tokens -= 2;
            } else {
                ++i;
            }
        }

        // processing assignment
        if (n_tokens == 3 && tokens[0]->type == 'v' && tokens[1]->type == '=' && tokens[2]->type == 'n') {
            set_var(tokens[0]->var, tokens[2]->num);
            free(tokens[0]);
            free(tokens[1]);
            tokens[0] = tokens[2];
            n_tokens = 1;
        }

        if (n_tokens == n_tokens_prev) break;
    }

    if (n_tokens == 1 && tokens[0]->type == 'n') {
        *result = tokens[0]->num;
    } else if (err == OK_CODE) {
        err = SYNTAX_ERROR_CODE;
    }

    for (size_t i = 0; i < n_tokens; ++i) {
        free(tokens[i]);
    }
    free(tokens);

    return err;
}
