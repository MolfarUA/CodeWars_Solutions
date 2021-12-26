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

##################################################
#pragma clang optimize off

#include <iostream>
#include <sstream>
#include <string>
#include <exception>
#include <string>
#include <memory>
#include <list>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <functional>

void error(const std::string& initiator, const std::string& problem);
constexpr uint64_t hash(const char* str);

namespace Transpile {

struct Variable {
    typedef std::shared_ptr<Variable> ptr_t;
    size_t start;
    bool is_list = false;
    size_t size = 1;
};

struct Processable;
class Processor {
public:
    typedef std::shared_ptr<Processable> proc_ptr_t;
    typedef Variable::ptr_t var_ptr_t;

    Processor(const proc_ptr_t prog);
    std::string run();

    void add_variable(const std::string& name, size_t size = 0);
    var_ptr_t get_variable(const std::string& name, bool i_need_list = false);

    var_ptr_t get_buffer(unsigned char def = 0);
    var_ptr_t get_auto_buffer(unsigned char def = 0);
    std::vector<var_ptr_t> get_consecutive_buffer(size_t size);

    void free_buffer(const var_ptr_t);
    void free_buffer(const std::vector<var_ptr_t>&);
    void free_auto_buffers();

    void move_to(const var_ptr_t);
    void move_to(size_t);

    void move_next();
    void move_prev();

    void clear(const var_ptr_t);
    void clear(size_t);
    void clear();

    void inc(const var_ptr_t, const var_ptr_t);
    void inc(const var_ptr_t, size_t to = 1);
    void inc(size_t, size_t);
    void inc(size_t);

    void dec(const var_ptr_t, const var_ptr_t);
    void dec(const var_ptr_t, size_t to = 1);
    void dec(size_t, size_t);
    void dec(size_t);

    void loop(const var_ptr_t, std::function<void()> body);
    void loop(size_t, std::function<void()> body);
    void loop(std::function<void()> body);

    void loop_while(const var_ptr_t, std::function<void()> body);

    void mov(const var_ptr_t, const var_ptr_t);

    void set(const var_ptr_t, unsigned char);
    void set(const var_ptr_t, const var_ptr_t);

    void add(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void sub(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void mul(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void divmod(const var_ptr_t, const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void div(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void mod(const var_ptr_t, const var_ptr_t, const var_ptr_t);

    void gt(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void eq(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void neq(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void cmp(const var_ptr_t, const var_ptr_t, const var_ptr_t);

    void if_then(const var_ptr_t, std::function<void()> true_block, std::function<void()> false_block);
    void if_eq(const var_ptr_t, const var_ptr_t, std::function<void()> block);
    void if_neq(const var_ptr_t, const var_ptr_t, std::function<void()> block);
    void while_neq(const var_ptr_t, const var_ptr_t, std::function<void()> block);

    void a2b(const var_ptr_t, const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void b2a(const var_ptr_t, const var_ptr_t, const var_ptr_t, const var_ptr_t);

    void lset(const var_ptr_t, size_t idx, const var_ptr_t);
    void lset(const var_ptr_t, size_t idx, unsigned char);
    void lset(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void lset(const var_ptr_t, const var_ptr_t, unsigned char);

    void lget(const var_ptr_t, size_t idx, const var_ptr_t);
    void lget(const var_ptr_t, const var_ptr_t, const var_ptr_t);

    void call(const std::string& proc_name, const std::list<std::string>& var_names);

    void read(const var_ptr_t);
    void msg(const var_ptr_t);
    void msg(const std::string&);

private:
    const proc_ptr_t prog;
    struct Procedure {
        std::list<std::pair<uint64_t, var_ptr_t>> args;
        proc_ptr_t body;
    };

    std::ostringstream out;
    std::unordered_map<uint64_t, Procedure> procedures;
    std::unordered_map<uint64_t, var_ptr_t> variables;
    std::list<uint64_t> call_stack;
    std::list<var_ptr_t> buffers;
    std::list<var_ptr_t> auto_buffers;
    size_t seek;

    void register_procedures();
    size_t find_block(size_t size = 1);
    size_t first_unused(size_t idx, size_t size);
    void allocate(const var_ptr_t);

};

}




namespace Transpile {

struct Processable {
    virtual ~Processable() = default;
    virtual void process(Processor&) const;
};

}




namespace Symbols {
typedef int64_t number_t;
typedef uint8_t cell_t;
typedef std::string string_t;

struct BasicSymbol {
    typedef std::shared_ptr<BasicSymbol> ptr_t;
    virtual ~BasicSymbol() = default;
};

struct VarName : BasicSymbol {
    typedef std::shared_ptr<VarName> ptr_t;
    const string_t name;

    VarName(const string_t& name) : name { name } {}
};

struct VarNameOrNumber : BasicSymbol {
    typedef std::shared_ptr<VarNameOrNumber> ptr_t;
    enum type_t { VAR, NUM };

    const VarName::ptr_t var = nullptr;
    const cell_t num = 0;

    bool is_var() const { return type == VAR; }

    VarNameOrNumber(const VarName::ptr_t var) : type { VAR }, var { var } {}
    VarNameOrNumber(number_t num);
private:
    const type_t type;
};

struct VarNameOrString : BasicSymbol {
    typedef std::shared_ptr<VarNameOrString> ptr_t;
    enum type_t { VAR, STR };

    const VarName::ptr_t var = nullptr;
    const std::shared_ptr<string_t> str = nullptr;

    bool is_var() const { return type == VAR; }

    VarNameOrString(const VarName::ptr_t var) : type { VAR }, var { var } {}
    VarNameOrString(const std::shared_ptr<string_t> str) : type { STR }, str { str } {}
private:
    const type_t type;

};

struct ListName : VarName {
    typedef std::shared_ptr<ListName> ptr_t;

    const number_t size;

    ListName(const string_t& name, number_t size) : VarName { name }, size { size } {}
};

typedef VarName ProcedureName;
typedef VarName ProcedureParameter;

struct VarSingle : BasicSymbol {
    typedef std::shared_ptr<VarSingle> ptr_t;
    enum type_t { VAR, LST };

    const type_t type;
    const VarName::ptr_t var = nullptr;
    const ListName::ptr_t lst = nullptr;

    VarSingle(const VarName::ptr_t var) : type { VAR }, var { var } {}
    VarSingle(const ListName::ptr_t lst) : type { LST }, lst { lst } {}
};

struct BasicStatement : BasicSymbol, Transpile::Processable {
    typedef std::shared_ptr<BasicStatement> ptr_t;
};

struct Block : BasicStatement {
    typedef std::shared_ptr<Block> ptr_t;
    typedef std::list<BasicStatement::ptr_t> list_t;

    const list_t stmts;
    Block(const list_t& stmts) : stmts { stmts } {}
    Block(list_t&& stmts) : stmts { std::move(stmts) } {}

    virtual void process(Transpile::Processor&) const;
};

struct Var : BasicStatement {
    typedef std::shared_ptr<Var> ptr_t;
    typedef std::list<VarSingle::ptr_t> list_t;

    const list_t vars;
    Var(list_t&& vars) : vars { std::move(vars) } {}
    void process(Transpile::Processor&) const;
};

struct TwoArgStatement : BasicStatement {
    typedef std::shared_ptr<TwoArgStatement> ptr_t;

    const VarName::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;

    TwoArgStatement(const VarName::ptr_t arg0, const VarNameOrNumber::ptr_t arg1) : arg0 { arg0 }, arg1 { arg1 } {}
};

struct Set : TwoArgStatement {
    typedef std::shared_ptr<Set> ptr_t;
    Set(const VarName::ptr_t arg0, const VarNameOrNumber::ptr_t arg1) : TwoArgStatement { arg0, arg1 } {}
    void process(Transpile::Processor&) const;
};

struct Inc : TwoArgStatement {
    typedef std::shared_ptr<Inc> ptr_t;
    Inc(const VarName::ptr_t arg0, const VarNameOrNumber::ptr_t arg1) : TwoArgStatement { arg0, arg1 } {}
    void process(Transpile::Processor&) const;
};

struct Dec : TwoArgStatement {
    typedef std::shared_ptr<Dec> ptr_t;
    Dec(const VarName::ptr_t arg0, const VarNameOrNumber::ptr_t arg1) : TwoArgStatement { arg0, arg1 } {}
    void process(Transpile::Processor&) const;
};

struct ThreeArgStatement : BasicStatement {
    typedef std::shared_ptr<ThreeArgStatement> ptr_t;

    const VarNameOrNumber::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;
    const VarName::ptr_t arg2;

    ThreeArgStatement(const VarNameOrNumber::ptr_t arg0,
                      const VarNameOrNumber::ptr_t arg1,
                      const VarName::ptr_t arg2) :
    arg0 { arg0 }, arg1 { arg1 }, arg2{ arg2 } {}
};

struct Add : ThreeArgStatement {
    typedef std::shared_ptr<Add> ptr_t;
    Add(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct Sub : ThreeArgStatement {
    typedef std::shared_ptr<Sub> ptr_t;
    Sub(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct Mul : ThreeArgStatement {
    typedef std::shared_ptr<Mul> ptr_t;
    Mul(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct DivMod : BasicStatement {
    typedef std::shared_ptr<DivMod> ptr_t;

    const VarNameOrNumber::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;
    const VarName::ptr_t arg2;
    const VarName::ptr_t arg3;

    DivMod(const VarNameOrNumber::ptr_t arg0,
           const VarNameOrNumber::ptr_t arg1,
           const VarName::ptr_t arg2,
           const VarName::ptr_t arg3) :
    arg0 { arg0 }, arg1 { arg1 }, arg2 { arg2 }, arg3 { arg3 } {}
    void process(Transpile::Processor&) const;
};

struct Div : ThreeArgStatement {
    typedef std::shared_ptr<Div> ptr_t;
    Div(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct Mod : ThreeArgStatement {
    typedef std::shared_ptr<Mod> ptr_t;
    Mod(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct Cmp : ThreeArgStatement {
    typedef std::shared_ptr<Cmp> ptr_t;
    Cmp(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct A2B : BasicStatement {
    typedef std::shared_ptr<A2B> ptr_t;

    const VarNameOrNumber::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;
    const VarNameOrNumber::ptr_t arg2;
    const VarName::ptr_t arg3;

    A2B(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarNameOrNumber::ptr_t arg2,
        const VarName::ptr_t arg3) :
    arg0 { arg0 }, arg1 { arg1 }, arg2 { arg2 }, arg3 { arg3 } {}
    void process(Transpile::Processor&) const;
};

struct B2A : BasicStatement {
    typedef std::shared_ptr<B2A> ptr_t;

    const VarNameOrNumber::ptr_t arg0;
    const VarName::ptr_t arg1;
    const VarName::ptr_t arg2;
    const VarName::ptr_t arg3;

    B2A(const VarNameOrNumber::ptr_t arg0,
        const VarName::ptr_t arg1,
        const VarName::ptr_t arg2,
        const VarName::ptr_t arg3) :
    arg0 { arg0 }, arg1 { arg1 }, arg2 { arg2 }, arg3 { arg3 } {}
    void process(Transpile::Processor&) const;
};

struct LSet : BasicStatement {
    typedef std::shared_ptr<LSet> ptr_t;

    const VarName::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;
    const VarNameOrNumber::ptr_t arg2;

    LSet(const VarName::ptr_t arg0,
         const VarNameOrNumber::ptr_t arg1,
         const VarNameOrNumber::ptr_t arg2) :
    arg0 { arg0 }, arg1 { arg1 }, arg2 { arg2 } {}
    void process(Transpile::Processor&) const;
};

struct LGet : BasicStatement {
    typedef std::shared_ptr<LGet> ptr_t;

    const VarName::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;
    const VarName::ptr_t arg2;

    LGet(const VarName::ptr_t arg0,
         const VarNameOrNumber::ptr_t arg1,
         const VarName::ptr_t arg2) :
    arg0 { arg0 }, arg1 { arg1 }, arg2 { arg2 } {}
    void process(Transpile::Processor&) const;
};

struct IfEq : TwoArgStatement, Block {
    typedef std::shared_ptr<IfEq> ptr_t;
    IfEq(TwoArgStatement&& stmt, Block&& block): TwoArgStatement { std::move(stmt) }, Block { std::move(block) } {}
    void process(Transpile::Processor&) const;
};

struct IfNEq : TwoArgStatement, Block {
    typedef std::shared_ptr<IfNEq> ptr_t;
    IfNEq(const TwoArgStatement& stmt, const Block& block): TwoArgStatement { stmt }, Block { block } {}
    void process(Transpile::Processor&) const;
};

struct WNEq : TwoArgStatement, Block {
    typedef std::shared_ptr<WNEq> ptr_t;
    WNEq(const TwoArgStatement& stmt, const Block& block): TwoArgStatement { stmt }, Block { block } {}
    void process(Transpile::Processor&) const;
};

struct Callable : BasicStatement {
    typedef std::shared_ptr<Callable> ptr_t;
    typedef std::list<ProcedureParameter::ptr_t> param_list_t;

    const std::string name;
    const param_list_t params;

    Callable(const ProcedureName::ptr_t name, param_list_t&& params) : name { name->name }, params { params } {}
};

struct Proc : Callable, Block {
    typedef std::shared_ptr<Proc> ptr_t;
    Proc(Callable&& call, Block&& block);
    void process(Transpile::Processor&) const;
};

struct End : BasicStatement {
    typedef std::shared_ptr<End> ptr_t;
};

struct Call : Callable {
    typedef std::shared_ptr<Call> ptr_t;
    Call(Callable&& call) : Callable { std::move(call) } {}
    void process(Transpile::Processor&) const;
};

struct Read : BasicStatement {
    typedef std::shared_ptr<Read> ptr_t;

    const VarName::ptr_t var;

    Read(const VarName::ptr_t var) : var { var } {}
    void process(Transpile::Processor&) const;
};

struct Msg : BasicStatement {
    typedef std::shared_ptr<Msg> ptr_t;
    typedef std::list<VarNameOrString::ptr_t> list_t;

    const list_t msgs;

    Msg(const list_t& msgs) : msgs { msgs } {}
    Msg(list_t&& msgs) : msgs { std::move(msgs) } {}
    void process(Transpile::Processor&) const;
};

struct Program : Block {
    typedef std::shared_ptr<Program> ptr_t;
    Program(const list_t& stmts) : Block { stmts } {}
    Program(list_t&& stmts) : Block { std::move(stmts) } {}
};

}




namespace Parser {

struct Parsed {
    const Symbols::Program::ptr_t program;
    static Parsed parse(const std::string& prog);

private:
    Parsed(const Symbols::Program::ptr_t program) : program { program } {}

    typedef std::string::const_iterator it_t;
    template<class T> struct spair { T val; it_t it; };
    enum context_t { GLOBAL, PROCEDURE };

    static constexpr char EOL = '\n';
    static it_t skip_spaces(it_t begin, it_t end);
    static bool is_end(const Symbols::BasicStatement::ptr_t stmt);
    static bool isVarPrefix(char c);
    static bool isVarSuffix(char c);

    static Symbols::Program::ptr_t tryBuildAST(it_t begin, it_t end);

    static spair<Symbols::Program::ptr_t> tryProgram(it_t begin, it_t end);
    static spair<Symbols::BasicStatement::ptr_t> tryStatement(it_t begin, it_t end, context_t context);
    static spair<bool> tryCommentPrefix(it_t begin, it_t end);
    static it_t tryComment(it_t begin, it_t end);
    static spair<char> tryCharElement(it_t begin, it_t end);
    static spair<Symbols::Var::ptr_t> tryVar(it_t begin, it_t end);
    static spair<Symbols::VarSingle::ptr_t> tryVarSingle(it_t begin, it_t end);
    static spair<Symbols::ListName::ptr_t> tryListName(it_t begin, it_t end);
    static spair<Symbols::VarName::ptr_t> tryVarName(it_t begin, it_t end);
    static spair<Symbols::number_t> tryNumber(it_t begin, it_t end);
    static spair<Symbols::number_t> tryChar(it_t begin, it_t end);
    static spair<Symbols::VarNameOrNumber::ptr_t> tryVarNameOrNumber(it_t begin, it_t end);
    static spair<Symbols::DivMod::ptr_t> tryDivMod(it_t begin, it_t end);
    static spair<Symbols::A2B::ptr_t> tryA2B(it_t begin, it_t end);
    static spair<Symbols::B2A::ptr_t> tryB2A(it_t begin, it_t end);
    static spair<Symbols::LSet::ptr_t> tryLSet(it_t begin, it_t end);
    static spair<Symbols::LGet::ptr_t> tryLGet(it_t begin, it_t end);
    static spair<Symbols::Read::ptr_t> tryRead(it_t begin, it_t end);
    static spair<Symbols::Msg::ptr_t> tryMsg(it_t begin, it_t end);
    static spair<Symbols::IfEq::ptr_t> tryIfEq(it_t begin, it_t end, context_t context);
    static spair<Symbols::Block::ptr_t> tryBlock(it_t begin, it_t end, context_t context);
    static spair<Symbols::IfNEq::ptr_t> tryIfNEq(it_t begin, it_t end, context_t context);
    static spair<Symbols::WNEq::ptr_t> tryWNEq(it_t begin, it_t end, context_t context);
    static spair<std::shared_ptr<std::string>> tryString(it_t begin, it_t end);
    static spair<Symbols::VarNameOrString::ptr_t> tryVarNameOrString(it_t begin, it_t end);
    static spair<Symbols::Callable::ptr_t> tryCallable(it_t begin, it_t end);
    static spair<Symbols::Proc::ptr_t> tryProc(it_t begin, it_t end);
    static spair<Symbols::Call::ptr_t> tryCall(it_t begin, it_t end);

    template<class T>
    static spair<std::shared_ptr<T>> tryTwoArgStatement(it_t begin, it_t end) {
        it_t it = skip_spaces(begin, end);
        if(it == end) return { nullptr, begin };

        auto arg0 = tryVarName(it, end);
        if(!arg0.val) return { nullptr, begin };
        it = arg0.it;

        auto arg1 = tryVarNameOrNumber(it, end);
        if(!arg1.val) return { nullptr, begin };
        it = arg1.it;

        return { std::make_shared<T>(arg0.val, arg1.val), it };
    }

    template<class T>
    static spair<std::shared_ptr<T>> tryThreeArgStatement(it_t begin, it_t end) {
        it_t it = skip_spaces(begin, end);
        if(it == end) return { nullptr, begin };

        auto arg0 = tryVarNameOrNumber(it, end);
        if(!arg0.val) return { nullptr, begin };
        it = arg0.it;

        auto arg1 = tryVarNameOrNumber(it, end);
        if(!arg1.val) return { nullptr, begin };
        it = arg1.it;

        auto arg2 = tryVarName(it, end);
        if(!arg2.val) return { nullptr, begin };
        it = arg2.it;

        return { std::make_shared<T>(arg0.val, arg1.val, arg2.val), it };
    }

};
constexpr char Parsed::EOL;

}






namespace Transpile {

Processor::Processor(const proc_ptr_t prog) : prog { prog } {
    register_procedures();
}

std::string Processor::run() {
    out.clear();
    variables.clear();
    seek = 0;

    prog->process(*this);

    return out.str();
}

void Processor::register_procedures() {
    auto program = std::dynamic_pointer_cast<Symbols::Program>(prog);
    if(program) {
        for(auto stmt : program->stmts) {
            auto proc = std::dynamic_pointer_cast<Symbols::Proc>(stmt);
            if(!proc) continue;

            const auto& name = proc->name;
            auto idx = hash(name.c_str());
            if(procedures.find(idx) != procedures.end())
                error("Processor", "Redefinition of procedure " + name);

            Procedure tmp;
            tmp.body = std::make_shared<Symbols::Block>(proc->stmts);
            for(auto arg : proc->params)
                tmp.args.push_back({ hash(arg->name.c_str()), nullptr });

            procedures[idx] = std::move(tmp);
        }
    }
}

void Processor::add_variable(const std::string& name, size_t size) {
    auto idx = hash(name.c_str());
    if(variables.find(idx) != variables.end())
        error("Processor", "Redefnition of variable " + name);

    auto var = std::make_shared<Variable>();
    if(!size) {
        var->start = find_block();
    }
    else {
        var->start = find_block(5 + size * 2);
        var->is_list = true;
        var->size = size;
    }

    allocate(var);
    variables[idx] = var;
}

Processor::var_ptr_t Processor::get_variable(const std::string& name, bool i_need_list) {
    auto idx = hash(name.c_str());

    for(auto it = call_stack.crbegin(); it != call_stack.crend(); ++it) {
        auto& proc = procedures.at(*it);
        auto find = std::find_if(proc.args.cbegin(), proc.args.cend(), [idx](const auto& p){ return p.first == idx; });
        if(find != proc.args.cend()) return find->second;
    }

    if(variables.find(idx) == variables.end())
        error("Processor", "Undefined variable " + name);

    auto var = variables.at(idx);

    if(!i_need_list && var->is_list)
        error("Processor", "Variable " + name + " is a list.");

    if(i_need_list && !var->is_list)
        error("Processor", "Variable " + name + " is not a list.");

    return variables.at(idx);
}

size_t Processor::find_block(size_t size) {
    return first_unused(0, size);
}

size_t Processor::first_unused(size_t idx, size_t size) {
    for(size_t test = idx; test < idx + size; test++) {
        for(const auto& var : variables)
            if(var.second->start == test)
                return first_unused(test + (var.second->is_list ? var.second->size * 2 + 5 : 1), size);
        for(const auto& buff : buffers)
            if(buff->start == test)
                return first_unused(test + 1, size);
        }
    return idx;
}

void Processor::allocate(const var_ptr_t var) {
    clear(var->start);
    if(var->is_list) {
        move_to(var->start);
        for(size_t i = 0; i < var->size; i++) {
            move_next(); clear();
            move_next(); clear(); inc(1);
        }
        for(size_t i = 0; i < 4; i++) {
            move_next(); clear();
        }
    }
}

Processor::var_ptr_t Processor::get_buffer(unsigned char def) {
    auto buff = std::make_shared<Variable>();
    buff->start = find_block();
    buff->is_list = false;
    buff->size = 1;

    set(buff, def);
    buffers.push_back(buff);

    return buff;
}

Processor::var_ptr_t Processor::get_auto_buffer(unsigned char def) {
    auto res = get_buffer(def);
    auto_buffers.push_back(res);
    return res;
}

std::vector<Processor::var_ptr_t> Processor::get_consecutive_buffer(size_t size) {
    size_t start = find_block(size);
    std::vector<var_ptr_t> res;

    std::generate_n(std::back_inserter(res), size, [this, s = start]() mutable {
        auto res = std::make_shared<Variable>();
        res->start = s++;
        res->is_list = false;
        res->size = 1;

        clear(res);
        buffers.push_back(res);

        return res;
    });

    return res;
}

void Processor::free_buffer(const var_ptr_t buff) {
    auto f = std::find(buffers.begin(), buffers.end(), buff);
    if(f != buffers.end())
        buffers.erase(f);
}

void Processor::free_buffer(const std::vector<var_ptr_t>& buffs) {
    for(auto buff : buffs) free_buffer(buff);
}

void Processor::free_auto_buffers() {
    for(auto buff : auto_buffers) free_buffer(buff);
    auto_buffers.clear();
}



void Processor::move_to(const var_ptr_t var) {
    move_to(var->start);
}

void Processor::move_to(size_t idx) {
    if(idx > seek) out << std::string(idx - seek, '>');
    else out << std::string(seek - idx, '<');
    seek = idx;
}

void Processor::move_next() {
    out << '>'; seek += 1;
}

void Processor::move_prev() {
    if(seek == 0) error("Processor", "Out of range");
    out << '<'; seek -= 1;
}

void Processor::clear(const var_ptr_t var) {
    clear(var->start);
}

void Processor::clear(size_t idx) {
    move_to(idx); clear();
}

void Processor::clear() {
    out << "[-]";;
}

void Processor::inc(const var_ptr_t var, const var_ptr_t val) {
    if(var == val) {auto tmp = get_buffer();set(tmp, var);inc(var, tmp);free_buffer(tmp);return;}

    auto tmp = get_buffer();
    loop(val, [this, var, tmp, val]{
        inc(var, 1); inc(tmp, 1); dec(val, 1);
    });
    mov(val, tmp);

    free_buffer(tmp);
}

void Processor::inc(const var_ptr_t var, size_t to) {
    inc(var->start, to);
}

void Processor::inc(size_t idx, size_t to) {
    move_to(idx); inc(to);
}

void Processor::inc(size_t to) {
    out << std::string(to, '+');
}

void Processor::dec(const var_ptr_t var, const var_ptr_t val) {
    if(var == val) {
        clear(var);
        return;
    }

    auto tmp = get_buffer();
    loop_while(val, [this, var, tmp]{
        dec(var); inc(tmp);
    });
    mov(val, tmp);

    free_buffer(tmp);
}

void Processor::dec(const var_ptr_t var, size_t to) {
    dec(var->start, to);
}

void Processor::dec(size_t idx, size_t to) {
    move_to(idx); dec(to);
}

void Processor::dec(size_t to) {
    out << std::string(to, '-');
}

void Processor::loop(const var_ptr_t var, std::function<void()> body) {
    move_to(var); out << '[';
    body();
    move_to(var); out << ']';
}

void Processor::loop(size_t idx, std::function<void()> body) {
    move_to(idx); out << '[';
    body();
    move_to(idx); out << ']';
}

void Processor::loop(std::function<void()> body) {
    out << '['; body(); out << ']';
}

void Processor::loop_while(const var_ptr_t var, std::function<void()> body) {
    move_to(var);
    out << '[';
    body();
    dec(var);
    out << ']';
}

void Processor::mov(const var_ptr_t var, const var_ptr_t val) {
    clear(var);
    loop_while(val, [this, var]{ inc(var); });
}

void Processor::set(const var_ptr_t var, unsigned char val) {
    clear(var); inc(var, val);
}

void Processor::set(const var_ptr_t var, const var_ptr_t val) {
    if(var == val) return;
    clear(var); inc(var, val);
}

void Processor::add(const var_ptr_t lhs, const var_ptr_t rhs, const var_ptr_t res) {
    if(lhs == res) {auto tmp = get_buffer();set(tmp, lhs);add(tmp, rhs, res);free_buffer(tmp);return;}
    if(rhs == res) {auto tmp = get_buffer();set(tmp, rhs);add(lhs, tmp, res);free_buffer(tmp);return;}
    set(res, lhs); inc(res, rhs);
}

void Processor::sub(const var_ptr_t lhs, const var_ptr_t rhs, const var_ptr_t res) {
    if(lhs == rhs) {clear(res);return;}
    if(lhs == res) {auto tmp = get_buffer();set(tmp, lhs);sub(tmp, rhs, res);free_buffer(tmp);return;}
    if(rhs == res) {auto tmp = get_buffer();set(tmp, rhs);sub(lhs, tmp, res);free_buffer(tmp);return;}
    set(res, lhs); dec(res, rhs);
}

void Processor::mul(const var_ptr_t lhs, const var_ptr_t rhs, const var_ptr_t res) {
    if(lhs == res) {auto tmp = get_buffer();set(tmp, lhs);mul(tmp, rhs, res);free_buffer(tmp);return;}
    if(rhs == res) {auto tmp = get_buffer();set(tmp, rhs);mul(lhs, tmp, res);free_buffer(tmp);return;}

    auto x = res;
    clear(x);
    auto y = rhs;

    auto tmp0 = get_buffer();
    auto tmp1 = get_buffer();

    set(tmp1, lhs);
    loop_while(tmp1, [this, tmp0, x, y] {
        loop_while(y, [this, x, tmp0] {
            inc(x); inc(tmp0);
        });
        mov(y, tmp0);
    });

    free_buffer(tmp0);
    free_buffer(tmp1);
}

void Processor::divmod(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c, const var_ptr_t d) {
    if(a == b) {
        set(c, 1);
        set(d, 0);
        return;
    }

    auto buff = get_consecutive_buffer(6);

    set(buff[0], a);
    set(buff[1], b);
    move_to(buff[0]);
    out << "[->[->+>>]>[<<+>>[-<+>]>+>>]<<<<<]>[>>>]>[[-<+>]>+>>]<<<<<";

    mov(c, buff[3]);
    mov(d, buff[2]);

    free_buffer(buff);
}

void Processor::div(const var_ptr_t lhs, const var_ptr_t rhs, const var_ptr_t res) {
    if(lhs == rhs) {set(res, 1); return;}
    if(lhs == res) {auto tmp = get_buffer();set(tmp, lhs);div(tmp, rhs, res);free_buffer(tmp);return;}
    if(rhs == res) {auto tmp = get_buffer();set(tmp, rhs);div(lhs, tmp, res);free_buffer(tmp);return;}

    auto tmp0 = get_buffer();
    auto tmp1 = get_buffer();
    auto tmp2 = get_buffer();
    auto tmp3 = get_buffer();

    auto x = res;
    clear(x);
    auto y = rhs;

    set(tmp0, lhs);
    loop(tmp0, [this, x, y, tmp0, tmp1, tmp2, tmp3] {
        loop_while(y, [this, tmp1, tmp2] { inc(tmp1); inc(tmp2); });
        mov(y, tmp2);
        loop_while(tmp1, [this, x, tmp0, tmp1, tmp2, tmp3] {
            inc(tmp2);
            dec(tmp0);
            loop_while(tmp0, [this, tmp2, tmp3] {
                clear(tmp2); inc(tmp3);
            });
            mov(tmp0, tmp3);
            loop_while(tmp2, [this, x, tmp1] {
                dec(tmp1);
                loop(tmp1, [this, x, tmp1] {
                    dec(x); clear(tmp1);
                });
                inc(tmp1);
            });
        });
        inc(x);
    });

    free_buffer(tmp0);
    free_buffer(tmp1);
    free_buffer(tmp2);
    free_buffer(tmp3);
}

void Processor::mod(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c) {
    auto buff = get_consecutive_buffer(6);
    set(buff[1], a);
    set(buff[2], b);
    move_to(buff[1]);
    out << "[>->+<[>]>[<+>-]<<[<]>-]";
    mov(c, buff[3]);
    free_buffer(buff);
}

void Processor::gt(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c) {
    if(a == b) { set(c, 0); return; }

    auto tmp0 = get_buffer();
    auto tmp1 = get_buffer();
    auto x = get_buffer();
    auto y = get_buffer();
    auto z = c;

    clear(z);
    set(x, a);
    set(y, b);

    loop_while(x, [this, y, z, tmp0, tmp1] {
        inc(tmp0);
        loop_while(y, [this, tmp0, tmp1] {
            clear(tmp0); inc(tmp1);
        });
        loop_while(tmp0, [this, z] { inc(z); });
        loop_while(tmp1, [this, y] { inc(y); });
        dec(y);
    });

    free_buffer(tmp0);
    free_buffer(tmp1);
    free_buffer(x);
    free_buffer(y);
}

void Processor::eq(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c) {
    if(a == b) { set(c, 1); return; }

    set(c, a);

    auto tmp0 = get_buffer();
    auto tmp1 = get_buffer();

    auto x = c;
    auto y = b;

    mov(tmp1, x);
    inc(x);
    loop_while(y, [this, tmp0, tmp1] { dec(tmp1); inc(tmp0); });
    loop_while(tmp0, [this, y] { inc(y); });
    loop(tmp1, [this, x, tmp1]{ dec(x); clear(tmp1); });

    free_buffer(tmp0);
    free_buffer(tmp1);
}

void Processor::neq(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c) {
    if(a == b) { set(c, 0); return; }

    set(c, a);

    auto tmp0 = get_buffer();
    auto tmp1 = get_buffer();

    auto x = c;
    auto y = b;

    mov(tmp1, x);
    loop_while(y, [this, tmp0, tmp1] { dec(tmp1); inc(tmp0); });
    loop_while(tmp0, [this, y] { inc(y); });
    loop(tmp1, [this, x, tmp1]{ dec(x); clear(tmp1); });

    free_buffer(tmp0);
    free_buffer(tmp1);
}

void Processor::cmp(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c) {
    if(a == b) { set(c, 0); return; }
    if(a == c) {auto t = get_buffer();set(t, a);cmp(t, b, c);free_buffer(t);return;}
    if(b == c) {auto t = get_buffer();set(t, b);cmp(a, t, c);free_buffer(t);return;}

    clear(c);
    if_neq(a, b, [this, a, b, c] {
        auto flag_gt = get_buffer();
        gt(a, b, flag_gt);
        if_then(flag_gt, [this, c] { inc(c); }, [this, c] { dec(c); });
        free_buffer(flag_gt);
    });
}


void Processor::if_then(const var_ptr_t flag, std::function<void()> true_block, std::function<void()> false_block) {
    auto tmp0 = get_buffer(1);
    auto tmp1 = get_buffer();

    loop(flag, [this, flag, tmp0, tmp1, true_block] {
        true_block();
        dec(tmp0);
        mov(tmp1, flag);
    });
    mov(flag, tmp1);
    loop_while(tmp0, false_block);

    free_buffer(tmp0);
    free_buffer(tmp1);
}

void Processor::if_eq(const var_ptr_t a, const var_ptr_t b, std::function<void()> block) {
    auto flag = get_buffer();

    eq(a, b, flag);
    loop(flag, [this, flag, block] {
        block();
        clear(flag);
    });

    free_buffer(flag);
}

void Processor::if_neq(const var_ptr_t a, const var_ptr_t b, std::function<void()> block) {
    auto flag = get_buffer();

    neq(a, b, flag);
    loop(flag, [this, flag, block] {
        block();
        clear(flag);
    });

    free_buffer(flag);
}

void Processor::while_neq(const var_ptr_t a, const var_ptr_t b, std::function<void()> block) {
    auto flag = get_buffer();

    neq(a, b, flag);
    loop(flag, [this, a, b, flag, block] {
        block();
        neq(a, b, flag);
    });

    free_buffer(flag);
}

void Processor::a2b(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c, const var_ptr_t d) {
    if(a == d) {auto t = get_buffer();set(t, a);a2b(t, b, c, d);free_buffer(t);return;}
    if(b == d) {auto t = get_buffer();set(t, b);a2b(a, t, c, d);free_buffer(t);return;}
    if(c == d) {auto t = get_buffer();set(t, c);a2b(a, b, t, d);free_buffer(t);return;}

    auto tmp = get_buffer();
    auto num = get_buffer();

    set(num, 48);
    sub(a, num, tmp);
    inc(num, 100 - 48);
    mul(tmp, num, tmp);
    mov(d, tmp);

    dec(num, 100 - 48);
    sub(b, num, tmp);
    dec(num, 48 - 10);
    mul(tmp, num, tmp);
    loop_while(tmp, [this, d]{ inc(d); });

    inc(num, 48 - 10);
    sub(c, num, tmp);
    loop_while(tmp, [this, d]{ inc(d); });

    free_buffer(tmp);
    free_buffer(num);
}

void Processor::b2a(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c, const var_ptr_t d) {
    if(a == b) {auto t = get_buffer();mov(t, a);b2a(t, b, c, d);free_buffer(t);return;}
    if(a == c) {auto t = get_buffer();mov(t, a);b2a(t, b, c, d);free_buffer(t);return;}
    if(a == d) {auto t = get_buffer();mov(t, a);b2a(t, b, c, d);free_buffer(t);return;}

    auto num = get_buffer(100);


    div(a, num, b);
    inc(b, 48);


    set(num, 10);
    div(a, num, c);
    mod(c, num, c);
    inc(c, 48);


    mod(a, num, d);
    free_buffer(num);
    inc(d, 48);
}

void Processor::lset(const var_ptr_t lst, size_t idx, const var_ptr_t val) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto elem = std::make_shared<Variable>();
    elem->start = lst->start + 1 + idx * 2;

    set(elem, val);
}

void Processor::lset(const var_ptr_t lst, size_t idx, unsigned char val) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto elem = std::make_shared<Variable>();
    elem->start = lst->start + 1 + idx * 2;

    set(elem, val);
}

void Processor::lset(const var_ptr_t lst, var_ptr_t idx, const var_ptr_t val) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto idx_buff = std::make_shared<Variable>();
    idx_buff->start = lst->start + 1 + lst->size * 2;

    set(idx_buff, idx);

    auto val_buff = std::make_shared<Variable>();
    val_buff->start = lst->start + 3 + lst->size * 2;

    set(val_buff, val);

    move_to(idx_buff);
    out << "[-<[<<]+>>->>[>>]>>+<<<]<[<<]>[-]>[>>]>[-<<<[<<]>+>[>>]>]>[-<<<<[<<]+<<->>[>>]>>]<<<";
}

void Processor::lset(const var_ptr_t lst, var_ptr_t idx, unsigned char val) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto idx_buff = std::make_shared<Variable>();
    idx_buff->start = lst->start + 1 + lst->size * 2;

    set(idx_buff, idx);

    auto val_buff = std::make_shared<Variable>();
    val_buff->start = lst->start + 3 + lst->size * 2;

    set(val_buff, val);

    move_to(idx_buff);
    out << "[-<[<<]+>>->>[>>]>>+<<<]<[<<]>[-]>[>>]>[-<<<[<<]>+>[>>]>]>[-<<<<[<<]+<<->>[>>]>>]<<<";
}

void Processor::lget(const var_ptr_t lst, size_t idx, const var_ptr_t var) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto elem = std::make_shared<Variable>();
    elem->start = lst->start + 1 + idx * 2;

    set(var, elem);
}


void Processor::lget(const var_ptr_t lst, var_ptr_t idx, const var_ptr_t val) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto idx_buff = std::make_shared<Variable>();
    idx_buff->start = lst->start + 1 + lst->size * 2;

    set(idx_buff, idx);

    auto val_buff = std::make_shared<Variable>();
    val_buff->start = lst->start + 3 + lst->size * 2;


    move_to(idx_buff);
    out << "[-<[<<]+>>->>[>>]>>+<<<]<[<<]>[->[>>]<+>>+<<<[<<]>]>[>>]<[-<[<<]>+>[>>]<]>>>[-<<<<[<<]<<->>+>>[>>]>>]<<<";

    mov(val, val_buff);
}

void Processor::call(const std::string& proc_name, const std::list<std::string>& var_names) {
    uint64_t proc_hash = hash(proc_name.c_str());
    if(std::find(call_stack.cbegin(), call_stack.cend(), proc_hash) != call_stack.cend())
        error("Processor", "Nested calls are not allowed");

    if(procedures.find(proc_hash) == procedures.end())
        error("Processor", "Procedure witn name " + proc_name + " does not exist");

    auto& proc = procedures.at(proc_hash);
    if(proc.args.size() != var_names.size())
        error("Processor", "Argument number doesn not match");

    auto args_it = proc.args.begin();
    auto vars_it = var_names.begin();
    while(vars_it != var_names.end())
        (args_it++)->second = get_variable(*vars_it++);

    call_stack.push_back(proc_hash);

    proc.body->process(*this);

    call_stack.pop_back();
}

void Processor::read(const var_ptr_t var) {
    move_to(var); out << ',';
}

void Processor::msg(const var_ptr_t var) {
    move_to(var); out << '.';
}

void Processor::msg(const std::string& str) {
    if(str.empty()) return;

    auto buff = get_buffer();
    char prev = 0;
    for(char c : str) {
        if(c > prev) {
            if(c > c - prev) inc(buff, c - prev);
            else set(buff, c);
        }
        else if(c < prev) {
            if(prev > prev - c) dec(buff, prev - c);
            else set(buff, c);
        }

        msg(buff);
        prev = c;
    }

    free_buffer(buff);
}


}





void Transpile::Processable::process(Processor&) const {
    std::clog << "Does nothing" << std::endl;
}





void error(const std::string& initiator, const std::string& problem) {
    std::string what = "[" + initiator + "]: " + problem;
    throw std::runtime_error(what);
}

constexpr uint64_t hash(const char* str) {
    return *str ? static_cast<unsigned int>(*str) + 33 * hash(str + 1) : 5381;
}





namespace Symbols {

VarNameOrNumber::VarNameOrNumber(number_t num) : type { NUM }, num { 0 } {
    while(num < 0) num += 256;
    const_cast<cell_t&>(this->num) = num % 256;
}

Proc::Proc(Callable&& call, Block&& block) : Callable { std::move(call) }, Block { std::move(block) } {
    for(auto it = params.begin(); it != params.end(); it++) {
        auto test = std::find_if(std::next(it), params.end(),
                                 [&cur = *it](const auto& param) {
                                    return cur->name == param->name;
                                 });
        if(test != params.end())
            error("Proc", "Repeating argument names");
    }
}

void Block::process(Transpile::Processor& proc) const {
    for(const auto& stmt : stmts) stmt->process(proc);
}

void Proc::process(Transpile::Processor& proc) const {}

void Var::process(Transpile::Processor& proc) const {
    for(const auto& var : vars) {
        switch (var->type) {
            case VarSingle::VAR:
                proc.add_variable(var->var->name);
                break;
            case VarSingle::LST:
                proc.add_variable(var->lst->name, var->lst->size);
                break;
        }
    }
}

void Set::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg0->name);
    if(arg1->is_var())
        proc.set(var, proc.get_variable(arg1->var->name));
    else
        proc.set(var, arg1->num);
}

void Inc::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg0->name);
    if(arg1->is_var())
        proc.inc(var, proc.get_variable(arg1->var->name));
    else
        proc.inc(var, arg1->num);
}

void Dec::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg0->name);
    if(arg1->is_var())
        proc.dec(var, proc.get_variable(arg1->var->name));
    else
        proc.dec(var, arg1->num);

}

void Add::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg2->name);

    int mode = (!arg0->is_var()) * 2 + (!arg1->is_var());
    switch(mode) {
        case (true * 2 + true): {
            proc.set(var, (arg0->num + arg1->num) % 256);
            break;
        }
        case (false * 2 + false): {
            proc.add(proc.get_variable(arg0->var->name), proc.get_variable(arg1->var->name), var);
            break;
        }
        case (false * 2 + true): {
            proc.set(var, proc.get_variable(arg0->var->name));
            proc.inc(var, arg1->num);
            break;
        }
        case (true * 2 + false): {
            proc.set(var, proc.get_variable(arg1->var->name));
            proc.inc(var, arg0->num);
            break;
        }
    }

}

void Sub::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg2->name);

    int mode = (!arg0->is_var()) * 2 + (!arg1->is_var());
    switch(mode) {
        case (true * 2 + true): {
            proc.set(var, (256 + arg0->num - arg1->num) % 256);
            break;
        }
        case (false * 2 + false): {
            proc.sub(proc.get_variable(arg0->var->name), proc.get_variable(arg1->var->name), var);
            break;
        }
        case (false * 2 + true): {
            proc.set(var, proc.get_variable(arg0->var->name));
            proc.dec(var, arg1->num);
            break;
        }
        case (true * 2 + false): {
            auto val = proc.get_variable(arg1->var->name);
            if(val == var) {
                auto tmp = proc.get_buffer();
                proc.mov(tmp, var);
                proc.set(var, arg0->num);
                proc.dec(var, tmp);
                proc.free_buffer(tmp);
            }
            else {
                proc.set(var, arg0->num);
                proc.dec(var, val);
            }

            break;
        }
    }

}

void Mul::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg2->name);
    if(!arg0->is_var() && !arg1->is_var()) {
        proc.set(var, (arg0->num * arg1->num) % 256);
        return;
    }

    proc.mul(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
             arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
             var);
    proc.free_auto_buffers();
}

void DivMod::process(Transpile::Processor& proc) const {
    if(!arg0->is_var() && !arg1->is_var()) {
        proc.set(proc.get_variable(arg2->name), arg0->num / arg1->num);
        proc.set(proc.get_variable(arg3->name), arg0->num % arg1->num);
        return;
    }

    proc.divmod(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
                arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
                proc.get_variable(arg2->name),
                proc.get_variable(arg3->name));
    proc.free_auto_buffers();
}

void Div::process(Transpile::Processor& proc) const {
    if(!arg0->is_var() && !arg1->is_var()) {
        proc.set(proc.get_variable(arg2->name), arg0->num / arg1->num);
        return;
    }

    proc.div(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
             arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
             proc.get_variable(arg2->name));
    proc.free_auto_buffers();
}

void Mod::process(Transpile::Processor& proc) const {
    if(!arg0->is_var() && !arg1->is_var()) {
        proc.set(proc.get_variable(arg2->name), arg0->num % arg1->num);
        return;
    }

    proc.mod(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
             arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
             proc.get_variable(arg2->name));
    proc.free_auto_buffers();
}

void Cmp::process(Transpile::Processor& proc) const {
    if(!arg0->is_var() && !arg1->is_var()) {
        proc.set(proc.get_variable(arg2->name), (256 + (arg0->num > arg1->num) - (arg0->num < arg1->num)) % 256);
        return;
    }

    proc.cmp(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
             arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
             proc.get_variable(arg2->name));
    proc.free_auto_buffers();
}

void A2B::process(Transpile::Processor& proc) const {
    if(!arg0->is_var() && !arg1->is_var() && !arg2->is_var()) {
        proc.set(proc.get_variable(arg3->name), 100 * (arg0->num - 48) + 10 * (arg1->num - 48) + arg2->num - 48);
        return;
    }

    proc.a2b(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
             arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
             arg2->is_var() ? proc.get_variable(arg2->var->name) : proc.get_auto_buffer(arg2->num),
             proc.get_variable(arg3->name));
    proc.free_auto_buffers();
}

void B2A::process(Transpile::Processor& proc) const {
    if(!arg0->is_var()) {
        proc.set(proc.get_variable(arg1->name), 48 + (arg0->num / 100));
        proc.set(proc.get_variable(arg2->name), 48 + (arg0->num / 10 % 10));
        proc.set(proc.get_variable(arg3->name), 48 + (arg0->num % 10));

        return;

    }

    proc.b2a(proc.get_variable(arg0->var->name),
             proc.get_variable(arg1->name),
             proc.get_variable(arg2->name),
             proc.get_variable(arg3->name));
    proc.free_auto_buffers();
}

void LSet::process(Transpile::Processor& proc) const {
    auto lst = proc.get_variable(arg0->name, true);

    int mode = arg1->is_var() + 2 * arg2->is_var();
    switch(mode) {
        case (false + 2 * false):
            proc.lset(lst, arg1->num, arg2->num);
            break;
        case (true + 2 * false):
            proc.lset(lst, proc.get_variable(arg1->var->name), arg2->num);
            break;
        case (false + 2 * true):
            proc.lset(lst, arg1->num, proc.get_variable(arg2->var->name));
            break;
        case (true + 2 * true):
            proc.lset(lst, proc.get_variable(arg1->var->name), proc.get_variable(arg2->var->name));
            break;
    }
}

void LGet::process(Transpile::Processor& proc) const {
    auto lst = proc.get_variable(arg0->name, true);
    auto var = proc.get_variable(arg2->name);

    if(arg1->is_var())
        proc.lget(lst, proc.get_variable(arg1->var->name), var);
    else
        proc.lget(lst, arg1->num, var);

    proc.free_auto_buffers();
}

void IfEq::process(Transpile::Processor& proc) const {
    auto a = proc.get_variable(arg0->name);
    auto b = arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_buffer(arg1->num);

    proc.if_eq(a, b, [this, &proc] {
        this->Block::process(proc);
    });

    if(!arg1->is_var()) proc.free_buffer(b);
}

void IfNEq::process(Transpile::Processor& proc) const {
    auto a = proc.get_variable(arg0->name);
    auto b = arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_buffer(arg1->num);

    proc.if_neq(a, b, [this, &proc] {
        this->Block::process(proc);
    });

    if(!arg1->is_var()) proc.free_buffer(b);
}

void WNEq::process(Transpile::Processor& proc) const {
    auto a = proc.get_variable(arg0->name);
    auto b = arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_buffer(arg1->num);

    proc.while_neq(a, b, [this, &proc] {
        this->Block::process(proc);
    });

    if(!arg1->is_var()) proc.free_buffer(b);
}

void Call::process(Transpile::Processor& proc) const {
    std::list<std::string> args;
    std::transform(params.cbegin(), params.cend(), std::back_inserter(args),
                  [](const auto& param) { return param->name; });
    proc.call(name, args);
}

void Read::process(Transpile::Processor& proc) const {
    proc.read(proc.get_variable(var->name));
}

void Msg::process(Transpile::Processor& proc) const {
    for(const auto& msg : msgs) {
        if(msg->is_var())
            proc.msg(proc.get_variable(msg->var->name));
        else
            proc.msg(*msg->str);
    }
}

}





namespace Parser {

Parsed Parsed::parse(const std::string &prog) {
    auto ast = tryBuildAST(prog.cbegin(), prog.cend());
    if(!ast) error("Parser", "Unable to parse program");

    return Parsed { ast };
}

Parsed::it_t Parsed::skip_spaces(it_t begin, it_t end) {
    while(!(begin == end || *begin == EOL) && isblank(*begin))
        ++begin;
    return begin;
}

bool Parsed::is_end(const Symbols::BasicStatement::ptr_t stmt) {
    return std::dynamic_pointer_cast<Symbols::End>(stmt) != nullptr;
}

bool Parsed::isVarPrefix(char c) {
    return c == '_' || c == '$' || isalpha(c);
}

bool Parsed::isVarSuffix(char c) {
    return isdigit(c) || isVarPrefix(c);
}

Symbols::Program::ptr_t Parsed::tryBuildAST(it_t begin, it_t end) {
    auto prog = tryProgram(begin, end);
    if(prog.it != end) return nullptr;
    return prog.val;
}



Parsed::spair<Symbols::Program::ptr_t> Parsed::tryProgram(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    Symbols::Program::list_t list;
    while(it != end) {
        auto stmt = tryStatement(it, end, GLOBAL);
        if(stmt.val){
            if(is_end(stmt.val)) error("Parser:Program", "Unexpected end");
            list.push_back(stmt.val);
        }
        it = tryComment(stmt.it, end);
        it = skip_spaces(it, end);

        if(it != end && *it != EOL) {
            error("Parser::Program", "Malformed program is passed. Unable to parse.\n" +
                  std::string(it, std::find(it, end, EOL)));
        }

        if(it != end) it = std::next(it);
    }

    return { std::make_shared<Symbols::Program>(std::move(list)), it };
}

Parsed::spair<Symbols::BasicStatement::ptr_t> Parsed::tryStatement(it_t begin, it_t end, context_t context) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    std::string cmd;
    while(it != end && isalnum(*it)) {
        cmd.push_back(tolower(*it++));
    }
    if(cmd.empty()) return { nullptr, begin };

    spair<Symbols::BasicStatement::ptr_t> res = { nullptr, begin };
    switch (hash(cmd.c_str())) {
        case hash("var"): {
            if(context == PROCEDURE)
                error("Parser:Statement", "Var is now allowed inside of procedure");

            auto var = tryVar(it, end);
            if(var.val) res = { var.val, var.it };
            break;
        }
        case hash("set"): {
            auto test = tryTwoArgStatement<Symbols::Set>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("inc"): {
            auto test = tryTwoArgStatement<Symbols::Inc>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("dec"): {
            auto test = tryTwoArgStatement<Symbols::Dec>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("add"): {
            auto test = tryThreeArgStatement<Symbols::Add>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("sub"): {
            auto test = tryThreeArgStatement<Symbols::Sub>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("mul"): {
            auto test = tryThreeArgStatement<Symbols::Mul>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("divmod"): {
            auto test = tryDivMod(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("div"): {
            auto test = tryThreeArgStatement<Symbols::Div>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("mod"): {
            auto test = tryThreeArgStatement<Symbols::Mod>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("cmp"): {
            auto test = tryThreeArgStatement<Symbols::Cmp>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("a2b"): {
            auto test = tryA2B(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("b2a"): {
            auto test = tryB2A(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("lset"): {
            auto test = tryLSet(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("lget"): {
            auto test = tryLGet(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("ifeq"): {
            auto test = tryIfEq(it, end, context);
            if(test.val) res = { std::dynamic_pointer_cast<Symbols::Block>(test.val), test.it };
            break;
        }
        case hash("ifneq"): {
            auto test = tryIfNEq(it, end, context);
            if(test.val) res = { std::dynamic_pointer_cast<Symbols::Block>(test.val), test.it };
            break;
        }
        case hash("wneq"): {
            auto test = tryWNEq(it, end, context);
            if(test.val) res = { std::dynamic_pointer_cast<Symbols::Block>(test.val), test.it };
            break;
        }
        case hash("proc"): {
            if(context == PROCEDURE)
                error("Parser:Statement", "Procedure declaration inside of procedure is now allowed.");

            auto test = tryProc(it, end);
            if(test.val) res = { std::dynamic_pointer_cast<Symbols::Block>(test.val), test.it };
            break;
        }
        case hash("end"): {
            res = { std::make_shared<Symbols::End>(), it };
            break;
        }
        case hash("call"): {
            auto test = tryCall(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("read"): {
            auto test = tryRead(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("msg"): {
            auto test = tryMsg(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
    }

    return res;
}

Parsed::spair<bool> Parsed::tryCommentPrefix(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);

    if(std::distance(it, end) >= 3) {
        if(
           tolower(*(it + 0)) == 'r' &&
           tolower(*(it + 1)) == 'e' &&
           tolower(*(it + 2)) == 'm') return { true, it + 3 };
    }
    if(std::distance(it, end) >= 2) {
        std::string tmp { it, it + 2};
        if(tmp == "--" || tmp == "//") return { true, it + 2 };
    }
    if(std::distance(it, end) >= 1) {
        if(*it == '#') return { true, it + 1 };
    }

    return { false, begin };
}

Parsed::it_t Parsed::tryComment(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return begin;

    auto pref = tryCommentPrefix(it, end);
    if(!pref.val) return begin;

    return std::find(pref.it, end, EOL);
}

Parsed::spair<char> Parsed::tryCharElement(it_t begin, it_t end) {
    if(begin == end) return { 0, begin };
    it_t it = begin;

    char res = *it;
    switch(res) {
        case '\'':
        case '"':
            return { 0, begin };
            break;

        case '\\':
            it = std::next(it);
            res = *it;
            switch(res) {
                case '\\':
                case '\'':
                case '"':
                    break;

                case 'n': res = '\n'; break;
                case 'r': res = '\r'; break;
                case 't': res = '\t'; break;

                default: return { 0, begin };
            }
    }
    it = std::next(it);

    return { res, it };
}

Parsed::spair<Symbols::Var::ptr_t> Parsed::tryVar(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    Symbols::Var::list_t list;
    for(auto var = tryVarSingle(it, end); var.val; var = tryVarSingle(it = var.it, end))
        list.push_back(var.val);

    if(list.empty()) return { nullptr, begin };

    return { std::make_shared<Symbols::Var>(std::move(list)), it };
}

Parsed::spair<Symbols::VarSingle::ptr_t> Parsed::tryVarSingle(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto list = tryListName(it, end);
    if(list.val)
        return { std::make_shared<Symbols::VarSingle>(list.val), list.it };

    auto varname = tryVarName(it, end);
    if(varname.val)
        return { std::make_shared<Symbols::VarSingle>(varname.val), varname.it };

    return { nullptr, begin };
}

Parsed::spair<Symbols::ListName::ptr_t> Parsed::tryListName(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto name = tryVarName(it, end);
    if(!name.val) return { nullptr, begin };

    it = skip_spaces(name.it, end);
    if(it == end || *it != '[') return { nullptr, begin };
    it = std::next(it);

    auto num = tryNumber(it, end);
    if(num.it == it) return { nullptr, begin };

    it = skip_spaces(num.it, end);
    if(it == end || *it != ']') return { nullptr, begin };

    return { std::make_shared<Symbols::ListName>(name.val->name, num.val), std::next(it) };
}

Parsed::spair<Symbols::VarName::ptr_t> Parsed::tryVarName(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end || !isVarPrefix(*it)) return { nullptr, begin };

    std::string name;
    while(it != end && isVarSuffix(*it))
        name.push_back(tolower(*it++));

    return { std::make_shared<Symbols::VarName>(name), it };
}

Parsed::spair<Symbols::number_t> Parsed::tryNumber(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { 0, begin };

    char neg = 1;
    if(*it == '-') {
        neg = -1;
        it = std::next(it);
        if(it == end) return { 0, begin };
    }

    if(isdigit(*it)) {
        Symbols::number_t res = 0;
        while(isdigit(*it)) {
            res *= 10; res += *it++ - '0';
        }
        return { res * neg, it };
    }

    auto ch = tryChar(it, end);
    if(ch.it != it) return { ch.val * neg, ch.it };

    return { 0, begin };
}

Parsed::spair<Symbols::number_t> Parsed::tryChar(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { 0, begin };

    if(*it != '\'') return { 0, begin };
    it = std::next(it);

    auto ch = tryCharElement(it, end);
    if(ch.it == it) return { 0, begin };
    it = ch.it;

    if(it == end || *it != '\'') return { 0, begin };

    return { ch.val, std::next(it) };
}

Parsed::spair<Symbols::VarNameOrNumber::ptr_t> Parsed::tryVarNameOrNumber(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto varname = tryVarName(it, end);
    if(varname.val)
        return { std::make_shared<Symbols::VarNameOrNumber>(varname.val), varname.it };

    auto number = tryNumber(it, end);
    if(number.it != it)
        return { std::make_shared<Symbols::VarNameOrNumber>(number.val), number.it };

    return { nullptr, begin };
}

Parsed::spair<Symbols::DivMod::ptr_t> Parsed::tryDivMod(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarNameOrNumber(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    auto arg1 = tryVarNameOrNumber(it, end);
    if(!arg1.val) return { nullptr, begin };
    it = arg1.it;

    auto arg2 = tryVarName(it, end);
    if(!arg2.val) return { nullptr, begin };
    it = arg2.it;

    auto arg3 = tryVarName(it, end);
    if(!arg3.val) return { nullptr, begin };
    it = arg3.it;

    return { std::make_shared<Symbols::DivMod>(arg0.val, arg1.val, arg2.val, arg3.val), it };
}

Parsed::spair<Symbols::A2B::ptr_t> Parsed::tryA2B(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarNameOrNumber(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    auto arg1 = tryVarNameOrNumber(it, end);
    if(!arg1.val) return { nullptr, begin };
    it = arg1.it;

    auto arg2 = tryVarNameOrNumber(it, end);
    if(!arg2.val) return { nullptr, begin };
    it = arg2.it;

    auto arg3 = tryVarName(it, end);
    if(!arg3.val) return { nullptr, begin };
    it = arg3.it;

    return { std::make_shared<Symbols::A2B>(arg0.val, arg1.val, arg2.val, arg3.val), it };
}

Parsed::spair<Symbols::B2A::ptr_t> Parsed::tryB2A(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarNameOrNumber(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    auto arg1 = tryVarName(it, end);
    if(!arg1.val) return { nullptr, begin };
    it = arg1.it;

    auto arg2 = tryVarName(it, end);
    if(!arg2.val) return { nullptr, begin };
    it = arg2.it;

    auto arg3 = tryVarName(it, end);
    if(!arg3.val) return { nullptr, begin };
    it = arg3.it;

    return { std::make_shared<Symbols::B2A>(arg0.val, arg1.val, arg2.val, arg3.val), it };
}

Parsed::spair<Symbols::LSet::ptr_t> Parsed::tryLSet(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarName(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    auto arg1 = tryVarNameOrNumber(it, end);
    if(!arg1.val) return { nullptr, begin };
    it = arg1.it;

    auto arg2 = tryVarNameOrNumber(it, end);
    if(!arg2.val) return { nullptr, begin };
    it = arg2.it;

    return { std::make_shared<Symbols::LSet>(arg0.val, arg1.val, arg2.val), it };
}

Parsed::spair<Symbols::LGet::ptr_t> Parsed::tryLGet(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarName(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    auto arg1 = tryVarNameOrNumber(it, end);
    if(!arg1.val) return { nullptr, begin };
    it = arg1.it;

    auto arg2 = tryVarName(it, end);
    if(!arg2.val) return { nullptr, begin };
    it = arg2.it;

    return { std::make_shared<Symbols::LGet>(arg0.val, arg1.val, arg2.val), it };
}

Parsed::spair<Symbols::Read::ptr_t> Parsed::tryRead(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarName(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    return { std::make_shared<Symbols::Read>(arg0.val), it };
}

Parsed::spair<Symbols::Block::ptr_t> Parsed::tryBlock(it_t begin, it_t end, context_t context) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    Symbols::Block::list_t list;
    bool is_ended = false;
    while(it != end) {
        auto stmt = tryStatement(it, end, context);
        it = stmt.it;
        if(stmt.val) {
            if(is_end(stmt.val)) { is_ended = true; break; }
            list.push_back(stmt.val);
        }

        it = tryComment(it, end);
        it = skip_spaces(it, end);

        if(it != end) {
            if(*it != EOL)
                error("Parser:Block", "Malformed program is passed. Unable to parse.");
            it = std::next(it);
        }
    }

    if(!is_ended)
        error("Parser:Block", "No end.");

    return { std::make_shared<Symbols::Block>(std::move(list)), it };
}

Parsed::spair<Symbols::IfEq::ptr_t> Parsed::tryIfEq(it_t begin, it_t end, context_t context) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto args = tryTwoArgStatement<Symbols::TwoArgStatement>(it, end);
    if(!args.val) return { nullptr, begin };
    it = args.it;

    auto block = tryBlock(it, end, context);
    if(!block.val) return { nullptr, begin };
    it = block.it;

    return { std::make_shared<Symbols::IfEq>(std::move(*args.val), std::move(*block.val)), it };
}

Parsed::spair<Symbols::IfNEq::ptr_t> Parsed::tryIfNEq(it_t begin, it_t end, context_t context) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto args = tryTwoArgStatement<Symbols::TwoArgStatement>(it, end);
    if(!args.val) return { nullptr, begin };
    it = args.it;

    auto block = tryBlock(it, end, context);
    if(!block.val) return { nullptr, begin };
    it = block.it;

    return { std::make_shared<Symbols::IfNEq>(std::move(*args.val), std::move(*block.val)), it };
}

Parsed::spair<Symbols::WNEq::ptr_t> Parsed::tryWNEq(it_t begin, it_t end, context_t context) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto args = tryTwoArgStatement<Symbols::TwoArgStatement>(it, end);
    if(!args.val) return { nullptr, begin };
    it = args.it;

    auto block = tryBlock(it, end, context);
    if(!block.val) return { nullptr, begin };
    it = block.it;

    return { std::make_shared<Symbols::WNEq>(std::move(*args.val), std::move(*block.val)), it };
}

Parsed::spair<Symbols::Msg::ptr_t> Parsed::tryMsg(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    Symbols::Msg::list_t list;
    for(auto var = tryVarNameOrString(it, end); var.val; var = tryVarNameOrString(it = var.it, end))
        list.push_back(var.val);

    if(list.empty()) return { nullptr, begin };

    return { std::make_shared<Symbols::Msg>(std::move(list)), it };
}

Parsed::spair<std::shared_ptr<std::string>> Parsed::tryString(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end || *it != '"') return { nullptr, begin };
    it = std::next(it);

    auto res = std::make_shared<std::string>();
    for(auto ch = tryCharElement(it, end); it != ch.it;
        ch = tryCharElement(it = ch.it, end))
        res->push_back(ch.val);

    if(it == end || *it != '"') return { nullptr, begin };

    return { res, std::next(it) };
}

Parsed::spair<Symbols::VarNameOrString::ptr_t> Parsed::tryVarNameOrString(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto varname = tryVarName(it, end);
    if(varname.val)
        return { std::make_shared<Symbols::VarNameOrString>(varname.val), varname.it };

    auto str = tryString(it, end);
    if(str.it != it)
        return { std::make_shared<Symbols::VarNameOrString>(str.val), str.it };

    return { nullptr, begin };
}

Parsed::spair<Symbols::Callable::ptr_t> Parsed::tryCallable(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto name = tryVarName(it, end);
    if(!name.val) return { nullptr, begin };
    it = name.it;

    Symbols::Callable::param_list_t list;
    for(auto arg = tryVarName(it, end); arg.val;
        arg = tryVarName(it = arg.it, end))
        list.push_back(arg.val);

    return { std::make_shared<Symbols::Callable>(name.val, std::move(list)), it };
}

Parsed::spair<Symbols::Proc::ptr_t> Parsed::tryProc(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto args = tryCallable(it, end);
    if(!args.val) return { nullptr, begin };
    it = args.it;

    auto block = tryBlock(it, end, PROCEDURE);
    if(!block.val) return { nullptr, begin };
    it = block.it;

    return { std::make_shared<Symbols::Proc>(std::move(*args.val), std::move(*block.val)), it };
}

Parsed::spair<Symbols::Call::ptr_t> Parsed::tryCall(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto args = tryCallable(it, end);
    if(!args.val) return { nullptr, begin };
    it = args.it;

    return { std::make_shared<Symbols::Call>(std::move(*args.val)), it };
}

}

std::string kcuf(const std::string& code) {
    try {
        using namespace Parser;
        using namespace Transpile;

        Parsed p = Parsed::parse(code);
        Processor proc(p.program);

        return proc.run();
    }
    catch(const std::exception& ex) {
        throw std::string { ex.what() };
    }
}

#################################################################
#pragma clang optimize off

#include <iostream>
#include <sstream>
#include <string>
#include <exception>
#include <string>
#include <memory>
#include <list>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <functional>

void error(const std::string& initiator, const std::string& problem);
constexpr uint64_t hash(const char* str);

namespace Transpile {

struct Variable {
    typedef std::shared_ptr<Variable> ptr_t;
    size_t start;
    bool is_list = false;
    size_t size = 1;
};

struct Processable;
class Processor {
public:
    typedef std::shared_ptr<Processable> proc_ptr_t;
    typedef Variable::ptr_t var_ptr_t;

    Processor(const proc_ptr_t prog);
    std::string run();

    void add_variable(const std::string& name, size_t size = 0);
    var_ptr_t get_variable(const std::string& name, bool i_need_list = false);

    var_ptr_t get_buffer(unsigned char def = 0);
    var_ptr_t get_auto_buffer(unsigned char def = 0);
    std::vector<var_ptr_t> get_consecutive_buffer(size_t size);

    void free_buffer(const var_ptr_t);
    void free_buffer(const std::vector<var_ptr_t>&);
    void free_auto_buffers();

    void move_to(const var_ptr_t);
    void move_to(size_t);

    void move_next();
    void move_prev();

    void clear(const var_ptr_t);
    void clear(size_t);
    void clear();

    void inc(const var_ptr_t, const var_ptr_t);
    void inc(const var_ptr_t, size_t to = 1);
    void inc(size_t, size_t);
    void inc(size_t);

    void dec(const var_ptr_t, const var_ptr_t);
    void dec(const var_ptr_t, size_t to = 1);
    void dec(size_t, size_t);
    void dec(size_t);

    void loop(const var_ptr_t, std::function<void()> body);
    void loop(size_t, std::function<void()> body);
    void loop(std::function<void()> body);

    void loop_while(const var_ptr_t, std::function<void()> body);

    void mov(const var_ptr_t, const var_ptr_t);

    void set(const var_ptr_t, unsigned char);
    void set(const var_ptr_t, const var_ptr_t);

    void add(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void sub(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void mul(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void divmod(const var_ptr_t, const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void div(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void mod(const var_ptr_t, const var_ptr_t, const var_ptr_t);

    void gt(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void eq(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void neq(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void cmp(const var_ptr_t, const var_ptr_t, const var_ptr_t);

    void if_then(const var_ptr_t, std::function<void()> true_block, std::function<void()> false_block);
    void if_eq(const var_ptr_t, const var_ptr_t, std::function<void()> block);
    void if_neq(const var_ptr_t, const var_ptr_t, std::function<void()> block);
    void while_neq(const var_ptr_t, const var_ptr_t, std::function<void()> block);

    void a2b(const var_ptr_t, const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void b2a(const var_ptr_t, const var_ptr_t, const var_ptr_t, const var_ptr_t);

    void lset(const var_ptr_t, size_t idx, const var_ptr_t);
    void lset(const var_ptr_t, size_t idx, unsigned char);
    void lset(const var_ptr_t, const var_ptr_t, const var_ptr_t);
    void lset(const var_ptr_t, const var_ptr_t, unsigned char);

    void lget(const var_ptr_t, size_t idx, const var_ptr_t);
    void lget(const var_ptr_t, const var_ptr_t, const var_ptr_t);

    void call(const std::string& proc_name, const std::list<std::string>& var_names);

    void read(const var_ptr_t);
    void msg(const var_ptr_t);
    void msg(const std::string&);

private:
    const proc_ptr_t prog;
    struct Procedure {
        std::list<std::pair<uint64_t, var_ptr_t>> args;
        proc_ptr_t body;
    };

    std::ostringstream out;
    std::unordered_map<uint64_t, Procedure> procedures;
    std::unordered_map<uint64_t, var_ptr_t> variables;
    std::list<uint64_t> call_stack;
    std::list<var_ptr_t> buffers;
    std::list<var_ptr_t> auto_buffers;
    size_t seek;

    void register_procedures();
    size_t find_block(size_t size = 1);
    size_t first_unused(size_t idx, size_t size);
    void allocate(const var_ptr_t);

};

}




namespace Transpile {

struct Processable {
    virtual ~Processable() = default;
    virtual void process(Processor&) const;
};

}




namespace Symbols {
typedef int64_t number_t;
typedef uint8_t cell_t;
typedef std::string string_t;

struct BasicSymbol {
    typedef std::shared_ptr<BasicSymbol> ptr_t;
    virtual ~BasicSymbol() = default;
};

struct VarName : BasicSymbol {
    typedef std::shared_ptr<VarName> ptr_t;
    const string_t name;

    VarName(const string_t& name) : name { name } {}
};

struct VarNameOrNumber : BasicSymbol {
    typedef std::shared_ptr<VarNameOrNumber> ptr_t;
    enum type_t { VAR, NUM };

    const VarName::ptr_t var = nullptr;
    const cell_t num = 0;

    bool is_var() const { return type == VAR; }

    VarNameOrNumber(const VarName::ptr_t var) : type { VAR }, var { var } {}
    VarNameOrNumber(number_t num);
private:
    const type_t type;
};

struct VarNameOrString : BasicSymbol {
    typedef std::shared_ptr<VarNameOrString> ptr_t;
    enum type_t { VAR, STR };

    const VarName::ptr_t var = nullptr;
    const std::shared_ptr<string_t> str = nullptr;

    bool is_var() const { return type == VAR; }

    VarNameOrString(const VarName::ptr_t var) : type { VAR }, var { var } {}
    VarNameOrString(const std::shared_ptr<string_t> str) : type { STR }, str { str } {}
private:
    const type_t type;

};

struct ListName : VarName {
    typedef std::shared_ptr<ListName> ptr_t;

    const number_t size;

    ListName(const string_t& name, number_t size) : VarName { name }, size { size } {}
};

typedef VarName ProcedureName;
typedef VarName ProcedureParameter;

struct VarSingle : BasicSymbol {
    typedef std::shared_ptr<VarSingle> ptr_t;
    enum type_t { VAR, LST };

    const type_t type;
    const VarName::ptr_t var = nullptr;
    const ListName::ptr_t lst = nullptr;

    VarSingle(const VarName::ptr_t var) : type { VAR }, var { var } {}
    VarSingle(const ListName::ptr_t lst) : type { LST }, lst { lst } {}
};

struct BasicStatement : BasicSymbol, Transpile::Processable {
    typedef std::shared_ptr<BasicStatement> ptr_t;
};

struct Block : BasicStatement {
    typedef std::shared_ptr<Block> ptr_t;
    typedef std::list<BasicStatement::ptr_t> list_t;

    const list_t stmts;
    Block(const list_t& stmts) : stmts { stmts } {}
    Block(list_t&& stmts) : stmts { std::move(stmts) } {}

    virtual void process(Transpile::Processor&) const;
};

struct Var : BasicStatement {
    typedef std::shared_ptr<Var> ptr_t;
    typedef std::list<VarSingle::ptr_t> list_t;

    const list_t vars;
    Var(list_t&& vars) : vars { std::move(vars) } {}
    void process(Transpile::Processor&) const;
};

struct TwoArgStatement : BasicStatement {
    typedef std::shared_ptr<TwoArgStatement> ptr_t;

    const VarName::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;

    TwoArgStatement(const VarName::ptr_t arg0, const VarNameOrNumber::ptr_t arg1) : arg0 { arg0 }, arg1 { arg1 } {}
};

struct Set : TwoArgStatement {
    typedef std::shared_ptr<Set> ptr_t;
    Set(const VarName::ptr_t arg0, const VarNameOrNumber::ptr_t arg1) : TwoArgStatement { arg0, arg1 } {}
    void process(Transpile::Processor&) const;
};

struct Inc : TwoArgStatement {
    typedef std::shared_ptr<Inc> ptr_t;
    Inc(const VarName::ptr_t arg0, const VarNameOrNumber::ptr_t arg1) : TwoArgStatement { arg0, arg1 } {}
    void process(Transpile::Processor&) const;
};

struct Dec : TwoArgStatement {
    typedef std::shared_ptr<Dec> ptr_t;
    Dec(const VarName::ptr_t arg0, const VarNameOrNumber::ptr_t arg1) : TwoArgStatement { arg0, arg1 } {}
    void process(Transpile::Processor&) const;
};

struct ThreeArgStatement : BasicStatement {
    typedef std::shared_ptr<ThreeArgStatement> ptr_t;

    const VarNameOrNumber::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;
    const VarName::ptr_t arg2;

    ThreeArgStatement(const VarNameOrNumber::ptr_t arg0,
                      const VarNameOrNumber::ptr_t arg1,
                      const VarName::ptr_t arg2) :
    arg0 { arg0 }, arg1 { arg1 }, arg2{ arg2 } {}
};

struct Add : ThreeArgStatement {
    typedef std::shared_ptr<Add> ptr_t;
    Add(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct Sub : ThreeArgStatement {
    typedef std::shared_ptr<Sub> ptr_t;
    Sub(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct Mul : ThreeArgStatement {
    typedef std::shared_ptr<Mul> ptr_t;
    Mul(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct DivMod : BasicStatement {
    typedef std::shared_ptr<DivMod> ptr_t;

    const VarNameOrNumber::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;
    const VarName::ptr_t arg2;
    const VarName::ptr_t arg3;

    DivMod(const VarNameOrNumber::ptr_t arg0,
           const VarNameOrNumber::ptr_t arg1,
           const VarName::ptr_t arg2,
           const VarName::ptr_t arg3) :
    arg0 { arg0 }, arg1 { arg1 }, arg2 { arg2 }, arg3 { arg3 } {}
    void process(Transpile::Processor&) const;
};

struct Div : ThreeArgStatement {
    typedef std::shared_ptr<Div> ptr_t;
    Div(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct Mod : ThreeArgStatement {
    typedef std::shared_ptr<Mod> ptr_t;
    Mod(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct Cmp : ThreeArgStatement {
    typedef std::shared_ptr<Cmp> ptr_t;
    Cmp(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarName::ptr_t arg2) :
    ThreeArgStatement { arg0, arg1, arg2 } {}
    void process(Transpile::Processor&) const;
};

struct A2B : BasicStatement {
    typedef std::shared_ptr<A2B> ptr_t;

    const VarNameOrNumber::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;
    const VarNameOrNumber::ptr_t arg2;
    const VarName::ptr_t arg3;

    A2B(const VarNameOrNumber::ptr_t arg0,
        const VarNameOrNumber::ptr_t arg1,
        const VarNameOrNumber::ptr_t arg2,
        const VarName::ptr_t arg3) :
    arg0 { arg0 }, arg1 { arg1 }, arg2 { arg2 }, arg3 { arg3 } {}
    void process(Transpile::Processor&) const;
};

struct B2A : BasicStatement {
    typedef std::shared_ptr<B2A> ptr_t;

    const VarNameOrNumber::ptr_t arg0;
    const VarName::ptr_t arg1;
    const VarName::ptr_t arg2;
    const VarName::ptr_t arg3;

    B2A(const VarNameOrNumber::ptr_t arg0,
        const VarName::ptr_t arg1,
        const VarName::ptr_t arg2,
        const VarName::ptr_t arg3) :
    arg0 { arg0 }, arg1 { arg1 }, arg2 { arg2 }, arg3 { arg3 } {}
    void process(Transpile::Processor&) const;
};

struct LSet : BasicStatement {
    typedef std::shared_ptr<LSet> ptr_t;

    const VarName::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;
    const VarNameOrNumber::ptr_t arg2;

    LSet(const VarName::ptr_t arg0,
         const VarNameOrNumber::ptr_t arg1,
         const VarNameOrNumber::ptr_t arg2) :
    arg0 { arg0 }, arg1 { arg1 }, arg2 { arg2 } {}
    void process(Transpile::Processor&) const;
};

struct LGet : BasicStatement {
    typedef std::shared_ptr<LGet> ptr_t;

    const VarName::ptr_t arg0;
    const VarNameOrNumber::ptr_t arg1;
    const VarName::ptr_t arg2;

    LGet(const VarName::ptr_t arg0,
         const VarNameOrNumber::ptr_t arg1,
         const VarName::ptr_t arg2) :
    arg0 { arg0 }, arg1 { arg1 }, arg2 { arg2 } {}
    void process(Transpile::Processor&) const;
};

struct IfEq : TwoArgStatement, Block {
    typedef std::shared_ptr<IfEq> ptr_t;
    IfEq(TwoArgStatement&& stmt, Block&& block): TwoArgStatement { std::move(stmt) }, Block { std::move(block) } {}
    void process(Transpile::Processor&) const;
};

struct IfNEq : TwoArgStatement, Block {
    typedef std::shared_ptr<IfNEq> ptr_t;
    IfNEq(const TwoArgStatement& stmt, const Block& block): TwoArgStatement { stmt }, Block { block } {}
    void process(Transpile::Processor&) const;
};

struct WNEq : TwoArgStatement, Block {
    typedef std::shared_ptr<WNEq> ptr_t;
    WNEq(const TwoArgStatement& stmt, const Block& block): TwoArgStatement { stmt }, Block { block } {}
    void process(Transpile::Processor&) const;
};

struct Callable : BasicStatement {
    typedef std::shared_ptr<Callable> ptr_t;
    typedef std::list<ProcedureParameter::ptr_t> param_list_t;

    const std::string name;
    const param_list_t params;

    Callable(const ProcedureName::ptr_t name, param_list_t&& params) : name { name->name }, params { params } {}
};

struct Proc : Callable, Block {
    typedef std::shared_ptr<Proc> ptr_t;
    Proc(Callable&& call, Block&& block);
    void process(Transpile::Processor&) const;
};

struct End : BasicStatement {
    typedef std::shared_ptr<End> ptr_t;
};

struct Call : Callable {
    typedef std::shared_ptr<Call> ptr_t;
    Call(Callable&& call) : Callable { std::move(call) } {}
    void process(Transpile::Processor&) const;
};

struct Read : BasicStatement {
    typedef std::shared_ptr<Read> ptr_t;

    const VarName::ptr_t var;

    Read(const VarName::ptr_t var) : var { var } {}
    void process(Transpile::Processor&) const;
};

struct Msg : BasicStatement {
    typedef std::shared_ptr<Msg> ptr_t;
    typedef std::list<VarNameOrString::ptr_t> list_t;

    const list_t msgs;

    Msg(const list_t& msgs) : msgs { msgs } {}
    Msg(list_t&& msgs) : msgs { std::move(msgs) } {}
    void process(Transpile::Processor&) const;
};

struct Program : Block {
    typedef std::shared_ptr<Program> ptr_t;
    Program(const list_t& stmts) : Block { stmts } {}
    Program(list_t&& stmts) : Block { std::move(stmts) } {}
};

}




namespace Parser {

struct Parsed {
    const Symbols::Program::ptr_t program;
    static Parsed parse(const std::string& prog);

private:
    Parsed(const Symbols::Program::ptr_t program) : program { program } {}

    typedef std::string::const_iterator it_t;
    template<class T> struct spair { T val; it_t it; };
    enum context_t { GLOBAL, PROCEDURE };

    static constexpr char EOL = '\n';
    static it_t skip_spaces(it_t begin, it_t end);
    static bool is_end(const Symbols::BasicStatement::ptr_t stmt);
    static bool isVarPrefix(char c);
    static bool isVarSuffix(char c);

    static Symbols::Program::ptr_t tryBuildAST(it_t begin, it_t end);

    static spair<Symbols::Program::ptr_t> tryProgram(it_t begin, it_t end);
    static spair<Symbols::BasicStatement::ptr_t> tryStatement(it_t begin, it_t end, context_t context);
    static spair<bool> tryCommentPrefix(it_t begin, it_t end);
    static it_t tryComment(it_t begin, it_t end);
    static spair<char> tryCharElement(it_t begin, it_t end);
    static spair<Symbols::Var::ptr_t> tryVar(it_t begin, it_t end);
    static spair<Symbols::VarSingle::ptr_t> tryVarSingle(it_t begin, it_t end);
    static spair<Symbols::ListName::ptr_t> tryListName(it_t begin, it_t end);
    static spair<Symbols::VarName::ptr_t> tryVarName(it_t begin, it_t end);
    static spair<Symbols::number_t> tryNumber(it_t begin, it_t end);
    static spair<Symbols::number_t> tryChar(it_t begin, it_t end);
    static spair<Symbols::VarNameOrNumber::ptr_t> tryVarNameOrNumber(it_t begin, it_t end);
    static spair<Symbols::DivMod::ptr_t> tryDivMod(it_t begin, it_t end);
    static spair<Symbols::A2B::ptr_t> tryA2B(it_t begin, it_t end);
    static spair<Symbols::B2A::ptr_t> tryB2A(it_t begin, it_t end);
    static spair<Symbols::LSet::ptr_t> tryLSet(it_t begin, it_t end);
    static spair<Symbols::LGet::ptr_t> tryLGet(it_t begin, it_t end);
    static spair<Symbols::Read::ptr_t> tryRead(it_t begin, it_t end);
    static spair<Symbols::Msg::ptr_t> tryMsg(it_t begin, it_t end);
    static spair<Symbols::IfEq::ptr_t> tryIfEq(it_t begin, it_t end, context_t context);
    static spair<Symbols::Block::ptr_t> tryBlock(it_t begin, it_t end, context_t context);
    static spair<Symbols::IfNEq::ptr_t> tryIfNEq(it_t begin, it_t end, context_t context);
    static spair<Symbols::WNEq::ptr_t> tryWNEq(it_t begin, it_t end, context_t context);
    static spair<std::shared_ptr<std::string>> tryString(it_t begin, it_t end);
    static spair<Symbols::VarNameOrString::ptr_t> tryVarNameOrString(it_t begin, it_t end);
    static spair<Symbols::Callable::ptr_t> tryCallable(it_t begin, it_t end);
    static spair<Symbols::Proc::ptr_t> tryProc(it_t begin, it_t end);
    static spair<Symbols::Call::ptr_t> tryCall(it_t begin, it_t end);

    template<class T>
    static spair<std::shared_ptr<T>> tryTwoArgStatement(it_t begin, it_t end) {
        it_t it = skip_spaces(begin, end);
        if(it == end) return { nullptr, begin };

        auto arg0 = tryVarName(it, end);
        if(!arg0.val) return { nullptr, begin };
        it = arg0.it;

        auto arg1 = tryVarNameOrNumber(it, end);
        if(!arg1.val) return { nullptr, begin };
        it = arg1.it;

        return { std::make_shared<T>(arg0.val, arg1.val), it };
    }

    template<class T>
    static spair<std::shared_ptr<T>> tryThreeArgStatement(it_t begin, it_t end) {
        it_t it = skip_spaces(begin, end);
        if(it == end) return { nullptr, begin };

        auto arg0 = tryVarNameOrNumber(it, end);
        if(!arg0.val) return { nullptr, begin };
        it = arg0.it;

        auto arg1 = tryVarNameOrNumber(it, end);
        if(!arg1.val) return { nullptr, begin };
        it = arg1.it;

        auto arg2 = tryVarName(it, end);
        if(!arg2.val) return { nullptr, begin };
        it = arg2.it;

        return { std::make_shared<T>(arg0.val, arg1.val, arg2.val), it };
    }

};
constexpr char Parsed::EOL;

}






namespace Transpile {

Processor::Processor(const proc_ptr_t prog) : prog { prog } {
    register_procedures();
}

std::string Processor::run() {
    out.clear();
    variables.clear();
    seek = 0;

    prog->process(*this);

    return out.str();
}

void Processor::register_procedures() {
    auto program = std::dynamic_pointer_cast<Symbols::Program>(prog);
    if(program) {
        for(auto stmt : program->stmts) {
            auto proc = std::dynamic_pointer_cast<Symbols::Proc>(stmt);
            if(!proc) continue;

            const auto& name = proc->name;
            auto idx = hash(name.c_str());
            if(procedures.find(idx) != procedures.end())
                error("Processor", "Redefinition of procedure " + name);

            Procedure tmp;
            tmp.body = std::make_shared<Symbols::Block>(proc->stmts);
            for(auto arg : proc->params)
                tmp.args.push_back({ hash(arg->name.c_str()), nullptr });

            procedures[idx] = std::move(tmp);
        }
    }
}

void Processor::add_variable(const std::string& name, size_t size) {
    auto idx = hash(name.c_str());
    if(variables.find(idx) != variables.end())
        error("Processor", "Redefnition of variable " + name);

    auto var = std::make_shared<Variable>();
    if(!size) {
        var->start = find_block();
    }
    else {
        var->start = find_block(5 + size * 2);
        var->is_list = true;
        var->size = size;
    }

    allocate(var);
    variables[idx] = var;
}

Processor::var_ptr_t Processor::get_variable(const std::string& name, bool i_need_list) {
    auto idx = hash(name.c_str());

    for(auto it = call_stack.crbegin(); it != call_stack.crend(); ++it) {
        auto& proc = procedures.at(*it);
        auto find = std::find_if(proc.args.cbegin(), proc.args.cend(), [idx](const auto& p){ return p.first == idx; });
        if(find != proc.args.cend()) return find->second;
    }

    if(variables.find(idx) == variables.end())
        error("Processor", "Undefined variable " + name);

    auto var = variables.at(idx);

    if(!i_need_list && var->is_list)
        error("Processor", "Variable " + name + " is a list.");

    if(i_need_list && !var->is_list)
        error("Processor", "Variable " + name + " is not a list.");

    return variables.at(idx);
}

size_t Processor::find_block(size_t size) {
    return first_unused(0, size);
}

size_t Processor::first_unused(size_t idx, size_t size) {
    for(size_t test = idx; test < idx + size; test++) {
        for(const auto& var : variables)
            if(var.second->start == test)
                return first_unused(test + (var.second->is_list ? var.second->size * 2 + 5 : 1), size);
        for(const auto& buff : buffers)
            if(buff->start == test)
                return first_unused(test + 1, size);
        }
    return idx;
}

void Processor::allocate(const var_ptr_t var) {
    clear(var->start);
    if(var->is_list) {
        move_to(var->start);
        for(size_t i = 0; i < var->size; i++) {
            move_next(); clear();
            move_next(); clear(); inc(1);
        }
        for(size_t i = 0; i < 4; i++) {
            move_next(); clear();
        }
    }
}

Processor::var_ptr_t Processor::get_buffer(unsigned char def) {
    auto buff = std::make_shared<Variable>();
    buff->start = find_block();
    buff->is_list = false;
    buff->size = 1;

    set(buff, def);
    buffers.push_back(buff);

    return buff;
}

Processor::var_ptr_t Processor::get_auto_buffer(unsigned char def) {
    auto res = get_buffer(def);
    auto_buffers.push_back(res);
    return res;
}

std::vector<Processor::var_ptr_t> Processor::get_consecutive_buffer(size_t size) {
    size_t start = find_block(size);
    std::vector<var_ptr_t> res;

    std::generate_n(std::back_inserter(res), size, [this, s = start]() mutable {
        auto res = std::make_shared<Variable>();
        res->start = s++;
        res->is_list = false;
        res->size = 1;

        clear(res);
        buffers.push_back(res);

        return res;
    });

    return res;
}

void Processor::free_buffer(const var_ptr_t buff) {
    auto f = std::find(buffers.begin(), buffers.end(), buff);
    if(f != buffers.end())
        buffers.erase(f);
}

void Processor::free_buffer(const std::vector<var_ptr_t>& buffs) {
    for(auto buff : buffs) free_buffer(buff);
}

void Processor::free_auto_buffers() {
    for(auto buff : auto_buffers) free_buffer(buff);
    auto_buffers.clear();
}



void Processor::move_to(const var_ptr_t var) {
    move_to(var->start);
}

void Processor::move_to(size_t idx) {
    if(idx > seek) out << std::string(idx - seek, '>');
    else out << std::string(seek - idx, '<');
    seek = idx;
}

void Processor::move_next() {
    out << '>'; seek += 1;
}

void Processor::move_prev() {
    if(seek == 0) error("Processor", "Out of range");
    out << '<'; seek -= 1;
}

void Processor::clear(const var_ptr_t var) {
    clear(var->start);
}

void Processor::clear(size_t idx) {
    move_to(idx); clear();
}

void Processor::clear() {
    out << "[-]";;
}

void Processor::inc(const var_ptr_t var, const var_ptr_t val) {
    if(var == val) {auto tmp = get_buffer();set(tmp, var);inc(var, tmp);free_buffer(tmp);return;}

    auto tmp = get_buffer();
    loop(val, [this, var, tmp, val]{
        inc(var, 1); inc(tmp, 1); dec(val, 1);
    });
    mov(val, tmp);

    free_buffer(tmp);
}

void Processor::inc(const var_ptr_t var, size_t to) {
    inc(var->start, to);
}

void Processor::inc(size_t idx, size_t to) {
    move_to(idx); inc(to);
}

void Processor::inc(size_t to) {
    out << std::string(to, '+');
}

void Processor::dec(const var_ptr_t var, const var_ptr_t val) {
    if(var == val) {
        clear(var);
        return;
    }

    auto tmp = get_buffer();
    loop_while(val, [this, var, tmp]{
        dec(var); inc(tmp);
    });
    mov(val, tmp);

    free_buffer(tmp);
}

void Processor::dec(const var_ptr_t var, size_t to) {
    dec(var->start, to);
}

void Processor::dec(size_t idx, size_t to) {
    move_to(idx); dec(to);
}

void Processor::dec(size_t to) {
    out << std::string(to, '-');
}

void Processor::loop(const var_ptr_t var, std::function<void()> body) {
    move_to(var); out << '[';
    body();
    move_to(var); out << ']';
}

void Processor::loop(size_t idx, std::function<void()> body) {
    move_to(idx); out << '[';
    body();
    move_to(idx); out << ']';
}

void Processor::loop(std::function<void()> body) {
    out << '['; body(); out << ']';
}

void Processor::loop_while(const var_ptr_t var, std::function<void()> body) {
    move_to(var);
    out << '[';
    body();
    dec(var);
    out << ']';
}

void Processor::mov(const var_ptr_t var, const var_ptr_t val) {
    clear(var);
    loop_while(val, [this, var]{ inc(var); });
}

void Processor::set(const var_ptr_t var, unsigned char val) {
    clear(var); inc(var, val);
}

void Processor::set(const var_ptr_t var, const var_ptr_t val) {
    if(var == val) return;
    clear(var); inc(var, val);
}

void Processor::add(const var_ptr_t lhs, const var_ptr_t rhs, const var_ptr_t res) {
    if(lhs == res) {auto tmp = get_buffer();set(tmp, lhs);add(tmp, rhs, res);free_buffer(tmp);return;}
    if(rhs == res) {auto tmp = get_buffer();set(tmp, rhs);add(lhs, tmp, res);free_buffer(tmp);return;}
    set(res, lhs); inc(res, rhs);
}

void Processor::sub(const var_ptr_t lhs, const var_ptr_t rhs, const var_ptr_t res) {
    if(lhs == rhs) {clear(res);return;}
    if(lhs == res) {auto tmp = get_buffer();set(tmp, lhs);sub(tmp, rhs, res);free_buffer(tmp);return;}
    if(rhs == res) {auto tmp = get_buffer();set(tmp, rhs);sub(lhs, tmp, res);free_buffer(tmp);return;}
    set(res, lhs); dec(res, rhs);
}

void Processor::mul(const var_ptr_t lhs, const var_ptr_t rhs, const var_ptr_t res) {
    if(lhs == res) {auto tmp = get_buffer();set(tmp, lhs);mul(tmp, rhs, res);free_buffer(tmp);return;}
    if(rhs == res) {auto tmp = get_buffer();set(tmp, rhs);mul(lhs, tmp, res);free_buffer(tmp);return;}

    auto x = res;
    clear(x);
    auto y = rhs;

    auto tmp0 = get_buffer();
    auto tmp1 = get_buffer();

    set(tmp1, lhs);
    loop_while(tmp1, [this, tmp0, x, y] {
        loop_while(y, [this, x, tmp0] {
            inc(x); inc(tmp0);
        });
        mov(y, tmp0);
    });

    free_buffer(tmp0);
    free_buffer(tmp1);
}

void Processor::divmod(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c, const var_ptr_t d) {
    if(a == b) {
        set(c, 1);
        set(d, 0);
        return;
    }

    auto buff = get_consecutive_buffer(6);

    set(buff[0], a);
    set(buff[1], b);
    move_to(buff[0]);
    out << "[->[->+>>]>[<<+>>[-<+>]>+>>]<<<<<]>[>>>]>[[-<+>]>+>>]<<<<<";

    mov(c, buff[3]);
    mov(d, buff[2]);

    free_buffer(buff);
}

void Processor::div(const var_ptr_t lhs, const var_ptr_t rhs, const var_ptr_t res) {
    if(lhs == rhs) {set(res, 1); return;}
    if(lhs == res) {auto tmp = get_buffer();set(tmp, lhs);div(tmp, rhs, res);free_buffer(tmp);return;}
    if(rhs == res) {auto tmp = get_buffer();set(tmp, rhs);div(lhs, tmp, res);free_buffer(tmp);return;}

    auto tmp0 = get_buffer();
    auto tmp1 = get_buffer();
    auto tmp2 = get_buffer();
    auto tmp3 = get_buffer();

    auto x = res;
    clear(x);
    auto y = rhs;

    set(tmp0, lhs);
    loop(tmp0, [this, x, y, tmp0, tmp1, tmp2, tmp3] {
        loop_while(y, [this, tmp1, tmp2] { inc(tmp1); inc(tmp2); });
        mov(y, tmp2);
        loop_while(tmp1, [this, x, tmp0, tmp1, tmp2, tmp3] {
            inc(tmp2);
            dec(tmp0);
            loop_while(tmp0, [this, tmp2, tmp3] {
                clear(tmp2); inc(tmp3);
            });
            mov(tmp0, tmp3);
            loop_while(tmp2, [this, x, tmp1] {
                dec(tmp1);
                loop(tmp1, [this, x, tmp1] {
                    dec(x); clear(tmp1);
                });
                inc(tmp1);
            });
        });
        inc(x);
    });

    free_buffer(tmp0);
    free_buffer(tmp1);
    free_buffer(tmp2);
    free_buffer(tmp3);
}

void Processor::mod(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c) {
    auto buff = get_consecutive_buffer(6);
    set(buff[1], a);
    set(buff[2], b);
    move_to(buff[1]);
    out << "[>->+<[>]>[<+>-]<<[<]>-]";
    mov(c, buff[3]);
    free_buffer(buff);
}

void Processor::gt(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c) {
    if(a == b) { set(c, 0); return; }

    auto tmp0 = get_buffer();
    auto tmp1 = get_buffer();
    auto x = get_buffer();
    auto y = get_buffer();
    auto z = c;

    clear(z);
    set(x, a);
    set(y, b);

    loop_while(x, [this, y, z, tmp0, tmp1] {
        inc(tmp0);
        loop_while(y, [this, tmp0, tmp1] {
            clear(tmp0); inc(tmp1);
        });
        loop_while(tmp0, [this, z] { inc(z); });
        loop_while(tmp1, [this, y] { inc(y); });
        dec(y);
    });

    free_buffer(tmp0);
    free_buffer(tmp1);
    free_buffer(x);
    free_buffer(y);
}

void Processor::eq(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c) {
    if(a == b) { set(c, 1); return; }

    set(c, a);

    auto tmp0 = get_buffer();
    auto tmp1 = get_buffer();

    auto x = c;
    auto y = b;

    mov(tmp1, x);
    inc(x);
    loop_while(y, [this, tmp0, tmp1] { dec(tmp1); inc(tmp0); });
    loop_while(tmp0, [this, y] { inc(y); });
    loop(tmp1, [this, x, tmp1]{ dec(x); clear(tmp1); });

    free_buffer(tmp0);
    free_buffer(tmp1);
}

void Processor::neq(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c) {
    if(a == b) { set(c, 0); return; }

    set(c, a);

    auto tmp0 = get_buffer();
    auto tmp1 = get_buffer();

    auto x = c;
    auto y = b;

    mov(tmp1, x);
    loop_while(y, [this, tmp0, tmp1] { dec(tmp1); inc(tmp0); });
    loop_while(tmp0, [this, y] { inc(y); });
    loop(tmp1, [this, x, tmp1]{ dec(x); clear(tmp1); });

    free_buffer(tmp0);
    free_buffer(tmp1);
}

void Processor::cmp(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c) {
    if(a == b) { set(c, 0); return; }
    if(a == c) {auto t = get_buffer();set(t, a);cmp(t, b, c);free_buffer(t);return;}
    if(b == c) {auto t = get_buffer();set(t, b);cmp(a, t, c);free_buffer(t);return;}

    clear(c);
    if_neq(a, b, [this, a, b, c] {
        auto flag_gt = get_buffer();
        gt(a, b, flag_gt);
        if_then(flag_gt, [this, c] { inc(c); }, [this, c] { dec(c); });
        free_buffer(flag_gt);
    });
}


void Processor::if_then(const var_ptr_t flag, std::function<void()> true_block, std::function<void()> false_block) {
    auto tmp0 = get_buffer(1);
    auto tmp1 = get_buffer();

    loop(flag, [this, flag, tmp0, tmp1, true_block] {
        true_block();
        dec(tmp0);
        mov(tmp1, flag);
    });
    mov(flag, tmp1);
    loop_while(tmp0, false_block);

    free_buffer(tmp0);
    free_buffer(tmp1);
}

void Processor::if_eq(const var_ptr_t a, const var_ptr_t b, std::function<void()> block) {
    auto flag = get_buffer();

    eq(a, b, flag);
    loop(flag, [this, flag, block] {
        block();
        clear(flag);
    });

    free_buffer(flag);
}

void Processor::if_neq(const var_ptr_t a, const var_ptr_t b, std::function<void()> block) {
    auto flag = get_buffer();

    neq(a, b, flag);
    loop(flag, [this, flag, block] {
        block();
        clear(flag);
    });

    free_buffer(flag);
}

void Processor::while_neq(const var_ptr_t a, const var_ptr_t b, std::function<void()> block) {
    auto flag = get_buffer();

    neq(a, b, flag);
    loop(flag, [this, a, b, flag, block] {
        block();
        neq(a, b, flag);
    });

    free_buffer(flag);
}

void Processor::a2b(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c, const var_ptr_t d) {
    if(a == d) {auto t = get_buffer();set(t, a);a2b(t, b, c, d);free_buffer(t);return;}
    if(b == d) {auto t = get_buffer();set(t, b);a2b(a, t, c, d);free_buffer(t);return;}
    if(c == d) {auto t = get_buffer();set(t, c);a2b(a, b, t, d);free_buffer(t);return;}

    auto tmp = get_buffer();
    auto num = get_buffer();

    set(num, 48);
    sub(a, num, tmp);
    inc(num, 100 - 48);
    mul(tmp, num, tmp);
    mov(d, tmp);

    dec(num, 100 - 48);
    sub(b, num, tmp);
    dec(num, 48 - 10);
    mul(tmp, num, tmp);
    loop_while(tmp, [this, d]{ inc(d); });

    inc(num, 48 - 10);
    sub(c, num, tmp);
    loop_while(tmp, [this, d]{ inc(d); });

    free_buffer(tmp);
    free_buffer(num);
}

void Processor::b2a(const var_ptr_t a, const var_ptr_t b, const var_ptr_t c, const var_ptr_t d) {
    if(a == b) {auto t = get_buffer();mov(t, a);b2a(t, b, c, d);free_buffer(t);return;}
    if(a == c) {auto t = get_buffer();mov(t, a);b2a(t, b, c, d);free_buffer(t);return;}
    if(a == d) {auto t = get_buffer();mov(t, a);b2a(t, b, c, d);free_buffer(t);return;}

    auto num = get_buffer(100);


    div(a, num, b);
    inc(b, 48);


    set(num, 10);
    div(a, num, c);
    mod(c, num, c);
    inc(c, 48);


    mod(a, num, d);
    free_buffer(num);
    inc(d, 48);
}

void Processor::lset(const var_ptr_t lst, size_t idx, const var_ptr_t val) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto elem = std::make_shared<Variable>();
    elem->start = lst->start + 1 + idx * 2;

    set(elem, val);
}

void Processor::lset(const var_ptr_t lst, size_t idx, unsigned char val) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto elem = std::make_shared<Variable>();
    elem->start = lst->start + 1 + idx * 2;

    set(elem, val);
}

void Processor::lset(const var_ptr_t lst, var_ptr_t idx, const var_ptr_t val) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto idx_buff = std::make_shared<Variable>();
    idx_buff->start = lst->start + 1 + lst->size * 2;

    set(idx_buff, idx);

    auto val_buff = std::make_shared<Variable>();
    val_buff->start = lst->start + 3 + lst->size * 2;

    set(val_buff, val);

    move_to(idx_buff);
    out << "[-<[<<]+>>->>[>>]>>+<<<]<[<<]>[-]>[>>]>[-<<<[<<]>+>[>>]>]>[-<<<<[<<]+<<->>[>>]>>]<<<";
}

void Processor::lset(const var_ptr_t lst, var_ptr_t idx, unsigned char val) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto idx_buff = std::make_shared<Variable>();
    idx_buff->start = lst->start + 1 + lst->size * 2;

    set(idx_buff, idx);

    auto val_buff = std::make_shared<Variable>();
    val_buff->start = lst->start + 3 + lst->size * 2;

    set(val_buff, val);

    move_to(idx_buff);
    out << "[-<[<<]+>>->>[>>]>>+<<<]<[<<]>[-]>[>>]>[-<<<[<<]>+>[>>]>]>[-<<<<[<<]+<<->>[>>]>>]<<<";
}

void Processor::lget(const var_ptr_t lst, size_t idx, const var_ptr_t var) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto elem = std::make_shared<Variable>();
    elem->start = lst->start + 1 + idx * 2;

    set(var, elem);
}


void Processor::lget(const var_ptr_t lst, var_ptr_t idx, const var_ptr_t val) {
    if(!lst->is_list) error("Processor", "List expected but var passed");

    auto idx_buff = std::make_shared<Variable>();
    idx_buff->start = lst->start + 1 + lst->size * 2;

    set(idx_buff, idx);

    auto val_buff = std::make_shared<Variable>();
    val_buff->start = lst->start + 3 + lst->size * 2;


    move_to(idx_buff);
    out << "[-<[<<]+>>->>[>>]>>+<<<]<[<<]>[->[>>]<+>>+<<<[<<]>]>[>>]<[-<[<<]>+>[>>]<]>>>[-<<<<[<<]<<->>+>>[>>]>>]<<<";

    mov(val, val_buff);
}

void Processor::call(const std::string& proc_name, const std::list<std::string>& var_names) {
    uint64_t proc_hash = hash(proc_name.c_str());
    if(std::find(call_stack.cbegin(), call_stack.cend(), proc_hash) != call_stack.cend())
        error("Processor", "Nested calls are not allowed");

    if(procedures.find(proc_hash) == procedures.end())
        error("Processor", "Procedure witn name " + proc_name + " does not exist");

    auto& proc = procedures.at(proc_hash);
    if(proc.args.size() != var_names.size())
        error("Processor", "Argument number doesn not match");

    auto args_it = proc.args.begin();
    auto vars_it = var_names.begin();
    while(vars_it != var_names.end())
        (args_it++)->second = get_variable(*vars_it++);

    call_stack.push_back(proc_hash);

    proc.body->process(*this);

    call_stack.pop_back();
}

void Processor::read(const var_ptr_t var) {
    move_to(var); out << ',';
}

void Processor::msg(const var_ptr_t var) {
    move_to(var); out << '.';
}

void Processor::msg(const std::string& str) {
    if(str.empty()) return;

    auto buff = get_buffer();
    char prev = 0;
    for(char c : str) {
        if(c > prev) {
            if(c > c - prev) inc(buff, c - prev);
            else set(buff, c);
        }
        else if(c < prev) {
            if(prev > prev - c) dec(buff, prev - c);
            else set(buff, c);
        }

        msg(buff);
        prev = c;
    }

    free_buffer(buff);
}


}





void Transpile::Processable::process(Processor&) const {
    std::clog << "Does nothing" << std::endl;
}





void error(const std::string& initiator, const std::string& problem) {
    std::string what = "[" + initiator + "]: " + problem;
    throw std::runtime_error(what);
}

constexpr uint64_t hash(const char* str) {
    return *str ? static_cast<unsigned int>(*str) + 33 * hash(str + 1) : 5381;
}





namespace Symbols {

VarNameOrNumber::VarNameOrNumber(number_t num) : type { NUM }, num { 0 } {
    while(num < 0) num += 256;
    const_cast<cell_t&>(this->num) = num % 256;
}

Proc::Proc(Callable&& call, Block&& block) : Callable { std::move(call) }, Block { std::move(block) } {
    for(auto it = params.begin(); it != params.end(); it++) {
        auto test = std::find_if(std::next(it), params.end(),
                                 [&cur = *it](const auto& param) {
                                    return cur->name == param->name;
                                 });
        if(test != params.end())
            error("Proc", "Repeating argument names");
    }
}

void Block::process(Transpile::Processor& proc) const {
    for(const auto& stmt : stmts) stmt->process(proc);
}

void Proc::process(Transpile::Processor& proc) const {}

void Var::process(Transpile::Processor& proc) const {
    for(const auto& var : vars) {
        switch (var->type) {
            case VarSingle::VAR:
                proc.add_variable(var->var->name);
                break;
            case VarSingle::LST:
                proc.add_variable(var->lst->name, var->lst->size);
                break;
        }
    }
}

void Set::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg0->name);
    if(arg1->is_var())
        proc.set(var, proc.get_variable(arg1->var->name));
    else
        proc.set(var, arg1->num);
}

void Inc::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg0->name);
    if(arg1->is_var())
        proc.inc(var, proc.get_variable(arg1->var->name));
    else
        proc.inc(var, arg1->num);
}

void Dec::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg0->name);
    if(arg1->is_var())
        proc.dec(var, proc.get_variable(arg1->var->name));
    else
        proc.dec(var, arg1->num);

}

void Add::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg2->name);

    int mode = (!arg0->is_var()) * 2 + (!arg1->is_var());
    switch(mode) {
        case (true * 2 + true): {
            proc.set(var, (arg0->num + arg1->num) % 256);
            break;
        }
        case (false * 2 + false): {
            proc.add(proc.get_variable(arg0->var->name), proc.get_variable(arg1->var->name), var);
            break;
        }
        case (false * 2 + true): {
            proc.set(var, proc.get_variable(arg0->var->name));
            proc.inc(var, arg1->num);
            break;
        }
        case (true * 2 + false): {
            proc.set(var, proc.get_variable(arg1->var->name));
            proc.inc(var, arg0->num);
            break;
        }
    }

}

void Sub::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg2->name);

    int mode = (!arg0->is_var()) * 2 + (!arg1->is_var());
    switch(mode) {
        case (true * 2 + true): {
            proc.set(var, (256 + arg0->num - arg1->num) % 256);
            break;
        }
        case (false * 2 + false): {
            proc.sub(proc.get_variable(arg0->var->name), proc.get_variable(arg1->var->name), var);
            break;
        }
        case (false * 2 + true): {
            proc.set(var, proc.get_variable(arg0->var->name));
            proc.dec(var, arg1->num);
            break;
        }
        case (true * 2 + false): {
            auto val = proc.get_variable(arg1->var->name);
            if(val == var) {
                auto tmp = proc.get_buffer();
                proc.mov(tmp, var);
                proc.set(var, arg0->num);
                proc.dec(var, tmp);
                proc.free_buffer(tmp);
            }
            else {
                proc.set(var, arg0->num);
                proc.dec(var, val);
            }

            break;
        }
    }

}

void Mul::process(Transpile::Processor& proc) const {
    auto var = proc.get_variable(arg2->name);
    if(!arg0->is_var() && !arg1->is_var()) {
        proc.set(var, (arg0->num * arg1->num) % 256);
        return;
    }

    proc.mul(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
             arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
             var);
    proc.free_auto_buffers();
}

void DivMod::process(Transpile::Processor& proc) const {
    if(!arg0->is_var() && !arg1->is_var()) {
        proc.set(proc.get_variable(arg2->name), arg0->num / arg1->num);
        proc.set(proc.get_variable(arg3->name), arg0->num % arg1->num);
        return;
    }

    proc.divmod(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
                arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
                proc.get_variable(arg2->name),
                proc.get_variable(arg3->name));
    proc.free_auto_buffers();
}

void Div::process(Transpile::Processor& proc) const {
    if(!arg0->is_var() && !arg1->is_var()) {
        proc.set(proc.get_variable(arg2->name), arg0->num / arg1->num);
        return;
    }

    proc.div(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
             arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
             proc.get_variable(arg2->name));
    proc.free_auto_buffers();
}

void Mod::process(Transpile::Processor& proc) const {
    if(!arg0->is_var() && !arg1->is_var()) {
        proc.set(proc.get_variable(arg2->name), arg0->num % arg1->num);
        return;
    }

    proc.mod(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
             arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
             proc.get_variable(arg2->name));
    proc.free_auto_buffers();
}

void Cmp::process(Transpile::Processor& proc) const {
    if(!arg0->is_var() && !arg1->is_var()) {
        proc.set(proc.get_variable(arg2->name), (256 + (arg0->num > arg1->num) - (arg0->num < arg1->num)) % 256);
        return;
    }

    proc.cmp(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
             arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
             proc.get_variable(arg2->name));
    proc.free_auto_buffers();
}

void A2B::process(Transpile::Processor& proc) const {
    if(!arg0->is_var() && !arg1->is_var() && !arg2->is_var()) {
        proc.set(proc.get_variable(arg3->name), 100 * (arg0->num - 48) + 10 * (arg1->num - 48) + arg2->num - 48);
        return;
    }

    proc.a2b(arg0->is_var() ? proc.get_variable(arg0->var->name) : proc.get_auto_buffer(arg0->num),
             arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_auto_buffer(arg1->num),
             arg2->is_var() ? proc.get_variable(arg2->var->name) : proc.get_auto_buffer(arg2->num),
             proc.get_variable(arg3->name));
    proc.free_auto_buffers();
}

void B2A::process(Transpile::Processor& proc) const {
    if(!arg0->is_var()) {
        proc.set(proc.get_variable(arg1->name), 48 + (arg0->num / 100));
        proc.set(proc.get_variable(arg2->name), 48 + (arg0->num / 10 % 10));
        proc.set(proc.get_variable(arg3->name), 48 + (arg0->num % 10));

        return;

    }

    proc.b2a(proc.get_variable(arg0->var->name),
             proc.get_variable(arg1->name),
             proc.get_variable(arg2->name),
             proc.get_variable(arg3->name));
    proc.free_auto_buffers();
}

void LSet::process(Transpile::Processor& proc) const {
    auto lst = proc.get_variable(arg0->name, true);

    int mode = arg1->is_var() + 2 * arg2->is_var();
    switch(mode) {
        case (false + 2 * false):
            proc.lset(lst, arg1->num, arg2->num);
            break;
        case (true + 2 * false):
            proc.lset(lst, proc.get_variable(arg1->var->name), arg2->num);
            break;
        case (false + 2 * true):
            proc.lset(lst, arg1->num, proc.get_variable(arg2->var->name));
            break;
        case (true + 2 * true):
            proc.lset(lst, proc.get_variable(arg1->var->name), proc.get_variable(arg2->var->name));
            break;
    }
}

void LGet::process(Transpile::Processor& proc) const {
    auto lst = proc.get_variable(arg0->name, true);
    auto var = proc.get_variable(arg2->name);

    if(arg1->is_var())
        proc.lget(lst, proc.get_variable(arg1->var->name), var);
    else
        proc.lget(lst, arg1->num, var);

    proc.free_auto_buffers();
}

void IfEq::process(Transpile::Processor& proc) const {
    auto a = proc.get_variable(arg0->name);
    auto b = arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_buffer(arg1->num);

    proc.if_eq(a, b, [this, &proc] {
        this->Block::process(proc);
    });

    if(!arg1->is_var()) proc.free_buffer(b);
}

void IfNEq::process(Transpile::Processor& proc) const {
    auto a = proc.get_variable(arg0->name);
    auto b = arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_buffer(arg1->num);

    proc.if_neq(a, b, [this, &proc] {
        this->Block::process(proc);
    });

    if(!arg1->is_var()) proc.free_buffer(b);
}

void WNEq::process(Transpile::Processor& proc) const {
    auto a = proc.get_variable(arg0->name);
    auto b = arg1->is_var() ? proc.get_variable(arg1->var->name) : proc.get_buffer(arg1->num);

    proc.while_neq(a, b, [this, &proc] {
        this->Block::process(proc);
    });

    if(!arg1->is_var()) proc.free_buffer(b);
}

void Call::process(Transpile::Processor& proc) const {
    std::list<std::string> args;
    std::transform(params.cbegin(), params.cend(), std::back_inserter(args),
                  [](const auto& param) { return param->name; });
    proc.call(name, args);
}

void Read::process(Transpile::Processor& proc) const {
    proc.read(proc.get_variable(var->name));
}

void Msg::process(Transpile::Processor& proc) const {
    for(const auto& msg : msgs) {
        if(msg->is_var())
            proc.msg(proc.get_variable(msg->var->name));
        else
            proc.msg(*msg->str);
    }
}

}





namespace Parser {

Parsed Parsed::parse(const std::string &prog) {
    auto ast = tryBuildAST(prog.cbegin(), prog.cend());
    if(!ast) error("Parser", "Unable to parse program");

    return Parsed { ast };
}

Parsed::it_t Parsed::skip_spaces(it_t begin, it_t end) {
    while(!(begin == end || *begin == EOL) && isblank(*begin))
        ++begin;
    return begin;
}

bool Parsed::is_end(const Symbols::BasicStatement::ptr_t stmt) {
    return std::dynamic_pointer_cast<Symbols::End>(stmt) != nullptr;
}

bool Parsed::isVarPrefix(char c) {
    return c == '_' || c == '$' || isalpha(c);
}

bool Parsed::isVarSuffix(char c) {
    return isdigit(c) || isVarPrefix(c);
}

Symbols::Program::ptr_t Parsed::tryBuildAST(it_t begin, it_t end) {
    auto prog = tryProgram(begin, end);
    if(prog.it != end) return nullptr;
    return prog.val;
}



Parsed::spair<Symbols::Program::ptr_t> Parsed::tryProgram(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    Symbols::Program::list_t list;
    while(it != end) {
        auto stmt = tryStatement(it, end, GLOBAL);
        if(stmt.val){
            if(is_end(stmt.val)) error("Parser:Program", "Unexpected end");
            list.push_back(stmt.val);
        }
        it = tryComment(stmt.it, end);
        it = skip_spaces(it, end);

        if(it != end && *it != EOL) {
            error("Parser::Program", "Malformed program is passed. Unable to parse.\n" +
                  std::string(it, std::find(it, end, EOL)));
        }

        if(it != end) it = std::next(it);
    }

    return { std::make_shared<Symbols::Program>(std::move(list)), it };
}

Parsed::spair<Symbols::BasicStatement::ptr_t> Parsed::tryStatement(it_t begin, it_t end, context_t context) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    std::string cmd;
    while(it != end && isalnum(*it)) {
        cmd.push_back(tolower(*it++));
    }
    if(cmd.empty()) return { nullptr, begin };

    spair<Symbols::BasicStatement::ptr_t> res = { nullptr, begin };
    switch (hash(cmd.c_str())) {
        case hash("var"): {
            if(context == PROCEDURE)
                error("Parser:Statement", "Var is now allowed inside of procedure");

            auto var = tryVar(it, end);
            if(var.val) res = { var.val, var.it };
            break;
        }
        case hash("set"): {
            auto test = tryTwoArgStatement<Symbols::Set>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("inc"): {
            auto test = tryTwoArgStatement<Symbols::Inc>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("dec"): {
            auto test = tryTwoArgStatement<Symbols::Dec>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("add"): {
            auto test = tryThreeArgStatement<Symbols::Add>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("sub"): {
            auto test = tryThreeArgStatement<Symbols::Sub>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("mul"): {
            auto test = tryThreeArgStatement<Symbols::Mul>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("divmod"): {
            auto test = tryDivMod(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("div"): {
            auto test = tryThreeArgStatement<Symbols::Div>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("mod"): {
            auto test = tryThreeArgStatement<Symbols::Mod>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("cmp"): {
            auto test = tryThreeArgStatement<Symbols::Cmp>(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("a2b"): {
            auto test = tryA2B(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("b2a"): {
            auto test = tryB2A(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("lset"): {
            auto test = tryLSet(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("lget"): {
            auto test = tryLGet(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("ifeq"): {
            auto test = tryIfEq(it, end, context);
            if(test.val) res = { std::dynamic_pointer_cast<Symbols::Block>(test.val), test.it };
            break;
        }
        case hash("ifneq"): {
            auto test = tryIfNEq(it, end, context);
            if(test.val) res = { std::dynamic_pointer_cast<Symbols::Block>(test.val), test.it };
            break;
        }
        case hash("wneq"): {
            auto test = tryWNEq(it, end, context);
            if(test.val) res = { std::dynamic_pointer_cast<Symbols::Block>(test.val), test.it };
            break;
        }
        case hash("proc"): {
            if(context == PROCEDURE)
                error("Parser:Statement", "Procedure declaration inside of procedure is now allowed.");

            auto test = tryProc(it, end);
            if(test.val) res = { std::dynamic_pointer_cast<Symbols::Block>(test.val), test.it };
            break;
        }
        case hash("end"): {
            res = { std::make_shared<Symbols::End>(), it };
            break;
        }
        case hash("call"): {
            auto test = tryCall(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }

        case hash("read"): {
            auto test = tryRead(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
        case hash("msg"): {
            auto test = tryMsg(it, end);
            if(test.val) res = { test.val, test.it };
            break;
        }
    }

    return res;
}

Parsed::spair<bool> Parsed::tryCommentPrefix(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);

    if(std::distance(it, end) >= 3) {
        if(
           tolower(*(it + 0)) == 'r' &&
           tolower(*(it + 1)) == 'e' &&
           tolower(*(it + 2)) == 'm') return { true, it + 3 };
    }
    if(std::distance(it, end) >= 2) {
        std::string tmp { it, it + 2};
        if(tmp == "--" || tmp == "//") return { true, it + 2 };
    }
    if(std::distance(it, end) >= 1) {
        if(*it == '#') return { true, it + 1 };
    }

    return { false, begin };
}

Parsed::it_t Parsed::tryComment(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return begin;

    auto pref = tryCommentPrefix(it, end);
    if(!pref.val) return begin;

    return std::find(pref.it, end, EOL);
}

Parsed::spair<char> Parsed::tryCharElement(it_t begin, it_t end) {
    if(begin == end) return { 0, begin };
    it_t it = begin;

    char res = *it;
    switch(res) {
        case '\'':
        case '"':
            return { 0, begin };
            break;

        case '\\':
            it = std::next(it);
            res = *it;
            switch(res) {
                case '\\':
                case '\'':
                case '"':
                    break;

                case 'n': res = '\n'; break;
                case 'r': res = '\r'; break;
                case 't': res = '\t'; break;

                default: return { 0, begin };
            }
    }
    it = std::next(it);

    return { res, it };
}

Parsed::spair<Symbols::Var::ptr_t> Parsed::tryVar(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    Symbols::Var::list_t list;
    for(auto var = tryVarSingle(it, end); var.val; var = tryVarSingle(it = var.it, end))
        list.push_back(var.val);

    if(list.empty()) return { nullptr, begin };

    return { std::make_shared<Symbols::Var>(std::move(list)), it };
}

Parsed::spair<Symbols::VarSingle::ptr_t> Parsed::tryVarSingle(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto list = tryListName(it, end);
    if(list.val)
        return { std::make_shared<Symbols::VarSingle>(list.val), list.it };

    auto varname = tryVarName(it, end);
    if(varname.val)
        return { std::make_shared<Symbols::VarSingle>(varname.val), varname.it };

    return { nullptr, begin };
}

Parsed::spair<Symbols::ListName::ptr_t> Parsed::tryListName(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto name = tryVarName(it, end);
    if(!name.val) return { nullptr, begin };

    it = skip_spaces(name.it, end);
    if(it == end || *it != '[') return { nullptr, begin };
    it = std::next(it);

    auto num = tryNumber(it, end);
    if(num.it == it) return { nullptr, begin };

    it = skip_spaces(num.it, end);
    if(it == end || *it != ']') return { nullptr, begin };

    return { std::make_shared<Symbols::ListName>(name.val->name, num.val), std::next(it) };
}

Parsed::spair<Symbols::VarName::ptr_t> Parsed::tryVarName(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end || !isVarPrefix(*it)) return { nullptr, begin };

    std::string name;
    while(it != end && isVarSuffix(*it))
        name.push_back(tolower(*it++));

    return { std::make_shared<Symbols::VarName>(name), it };
}

Parsed::spair<Symbols::number_t> Parsed::tryNumber(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { 0, begin };

    char neg = 1;
    if(*it == '-') {
        neg = -1;
        it = std::next(it);
        if(it == end) return { 0, begin };
    }

    if(isdigit(*it)) {
        Symbols::number_t res = 0;
        while(isdigit(*it)) {
            res *= 10; res += *it++ - '0';
        }
        return { res * neg, it };
    }

    auto ch = tryChar(it, end);
    if(ch.it != it) return { ch.val * neg, ch.it };

    return { 0, begin };
}

Parsed::spair<Symbols::number_t> Parsed::tryChar(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { 0, begin };

    if(*it != '\'') return { 0, begin };
    it = std::next(it);

    auto ch = tryCharElement(it, end);
    if(ch.it == it) return { 0, begin };
    it = ch.it;

    if(it == end || *it != '\'') return { 0, begin };

    return { ch.val, std::next(it) };
}

Parsed::spair<Symbols::VarNameOrNumber::ptr_t> Parsed::tryVarNameOrNumber(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto varname = tryVarName(it, end);
    if(varname.val)
        return { std::make_shared<Symbols::VarNameOrNumber>(varname.val), varname.it };

    auto number = tryNumber(it, end);
    if(number.it != it)
        return { std::make_shared<Symbols::VarNameOrNumber>(number.val), number.it };

    return { nullptr, begin };
}

Parsed::spair<Symbols::DivMod::ptr_t> Parsed::tryDivMod(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarNameOrNumber(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    auto arg1 = tryVarNameOrNumber(it, end);
    if(!arg1.val) return { nullptr, begin };
    it = arg1.it;

    auto arg2 = tryVarName(it, end);
    if(!arg2.val) return { nullptr, begin };
    it = arg2.it;

    auto arg3 = tryVarName(it, end);
    if(!arg3.val) return { nullptr, begin };
    it = arg3.it;

    return { std::make_shared<Symbols::DivMod>(arg0.val, arg1.val, arg2.val, arg3.val), it };
}

Parsed::spair<Symbols::A2B::ptr_t> Parsed::tryA2B(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarNameOrNumber(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    auto arg1 = tryVarNameOrNumber(it, end);
    if(!arg1.val) return { nullptr, begin };
    it = arg1.it;

    auto arg2 = tryVarNameOrNumber(it, end);
    if(!arg2.val) return { nullptr, begin };
    it = arg2.it;

    auto arg3 = tryVarName(it, end);
    if(!arg3.val) return { nullptr, begin };
    it = arg3.it;

    return { std::make_shared<Symbols::A2B>(arg0.val, arg1.val, arg2.val, arg3.val), it };
}

Parsed::spair<Symbols::B2A::ptr_t> Parsed::tryB2A(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarNameOrNumber(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    auto arg1 = tryVarName(it, end);
    if(!arg1.val) return { nullptr, begin };
    it = arg1.it;

    auto arg2 = tryVarName(it, end);
    if(!arg2.val) return { nullptr, begin };
    it = arg2.it;

    auto arg3 = tryVarName(it, end);
    if(!arg3.val) return { nullptr, begin };
    it = arg3.it;

    return { std::make_shared<Symbols::B2A>(arg0.val, arg1.val, arg2.val, arg3.val), it };
}

Parsed::spair<Symbols::LSet::ptr_t> Parsed::tryLSet(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarName(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    auto arg1 = tryVarNameOrNumber(it, end);
    if(!arg1.val) return { nullptr, begin };
    it = arg1.it;

    auto arg2 = tryVarNameOrNumber(it, end);
    if(!arg2.val) return { nullptr, begin };
    it = arg2.it;

    return { std::make_shared<Symbols::LSet>(arg0.val, arg1.val, arg2.val), it };
}

Parsed::spair<Symbols::LGet::ptr_t> Parsed::tryLGet(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarName(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    auto arg1 = tryVarNameOrNumber(it, end);
    if(!arg1.val) return { nullptr, begin };
    it = arg1.it;

    auto arg2 = tryVarName(it, end);
    if(!arg2.val) return { nullptr, begin };
    it = arg2.it;

    return { std::make_shared<Symbols::LGet>(arg0.val, arg1.val, arg2.val), it };
}

Parsed::spair<Symbols::Read::ptr_t> Parsed::tryRead(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto arg0 = tryVarName(it, end);
    if(!arg0.val) return { nullptr, begin };
    it = arg0.it;

    return { std::make_shared<Symbols::Read>(arg0.val), it };
}

Parsed::spair<Symbols::Block::ptr_t> Parsed::tryBlock(it_t begin, it_t end, context_t context) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    Symbols::Block::list_t list;
    bool is_ended = false;
    while(it != end) {
        auto stmt = tryStatement(it, end, context);
        it = stmt.it;
        if(stmt.val) {
            if(is_end(stmt.val)) { is_ended = true; break; }
            list.push_back(stmt.val);
        }

        it = tryComment(it, end);
        it = skip_spaces(it, end);

        if(it != end) {
            if(*it != EOL)
                error("Parser:Block", "Malformed program is passed. Unable to parse.");
            it = std::next(it);
        }
    }

    if(!is_ended)
        error("Parser:Block", "No end.");

    return { std::make_shared<Symbols::Block>(std::move(list)), it };
}

Parsed::spair<Symbols::IfEq::ptr_t> Parsed::tryIfEq(it_t begin, it_t end, context_t context) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto args = tryTwoArgStatement<Symbols::TwoArgStatement>(it, end);
    if(!args.val) return { nullptr, begin };
    it = args.it;

    auto block = tryBlock(it, end, context);
    if(!block.val) return { nullptr, begin };
    it = block.it;

    return { std::make_shared<Symbols::IfEq>(std::move(*args.val), std::move(*block.val)), it };
}

Parsed::spair<Symbols::IfNEq::ptr_t> Parsed::tryIfNEq(it_t begin, it_t end, context_t context) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto args = tryTwoArgStatement<Symbols::TwoArgStatement>(it, end);
    if(!args.val) return { nullptr, begin };
    it = args.it;

    auto block = tryBlock(it, end, context);
    if(!block.val) return { nullptr, begin };
    it = block.it;

    return { std::make_shared<Symbols::IfNEq>(std::move(*args.val), std::move(*block.val)), it };
}

Parsed::spair<Symbols::WNEq::ptr_t> Parsed::tryWNEq(it_t begin, it_t end, context_t context) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto args = tryTwoArgStatement<Symbols::TwoArgStatement>(it, end);
    if(!args.val) return { nullptr, begin };
    it = args.it;

    auto block = tryBlock(it, end, context);
    if(!block.val) return { nullptr, begin };
    it = block.it;

    return { std::make_shared<Symbols::WNEq>(std::move(*args.val), std::move(*block.val)), it };
}

Parsed::spair<Symbols::Msg::ptr_t> Parsed::tryMsg(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    Symbols::Msg::list_t list;
    for(auto var = tryVarNameOrString(it, end); var.val; var = tryVarNameOrString(it = var.it, end))
        list.push_back(var.val);

    if(list.empty()) return { nullptr, begin };

    return { std::make_shared<Symbols::Msg>(std::move(list)), it };
}

Parsed::spair<std::shared_ptr<std::string>> Parsed::tryString(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end || *it != '"') return { nullptr, begin };
    it = std::next(it);

    auto res = std::make_shared<std::string>();
    for(auto ch = tryCharElement(it, end); it != ch.it;
        ch = tryCharElement(it = ch.it, end))
        res->push_back(ch.val);

    if(it == end || *it != '"') return { nullptr, begin };

    return { res, std::next(it) };
}

Parsed::spair<Symbols::VarNameOrString::ptr_t> Parsed::tryVarNameOrString(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto varname = tryVarName(it, end);
    if(varname.val)
        return { std::make_shared<Symbols::VarNameOrString>(varname.val), varname.it };

    auto str = tryString(it, end);
    if(str.it != it)
        return { std::make_shared<Symbols::VarNameOrString>(str.val), str.it };

    return { nullptr, begin };
}

Parsed::spair<Symbols::Callable::ptr_t> Parsed::tryCallable(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto name = tryVarName(it, end);
    if(!name.val) return { nullptr, begin };
    it = name.it;

    Symbols::Callable::param_list_t list;
    for(auto arg = tryVarName(it, end); arg.val;
        arg = tryVarName(it = arg.it, end))
        list.push_back(arg.val);

    return { std::make_shared<Symbols::Callable>(name.val, std::move(list)), it };
}

Parsed::spair<Symbols::Proc::ptr_t> Parsed::tryProc(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto args = tryCallable(it, end);
    if(!args.val) return { nullptr, begin };
    it = args.it;

    auto block = tryBlock(it, end, PROCEDURE);
    if(!block.val) return { nullptr, begin };
    it = block.it;

    return { std::make_shared<Symbols::Proc>(std::move(*args.val), std::move(*block.val)), it };
}

Parsed::spair<Symbols::Call::ptr_t> Parsed::tryCall(it_t begin, it_t end) {
    it_t it = skip_spaces(begin, end);
    if(it == end) return { nullptr, begin };

    auto args = tryCallable(it, end);
    if(!args.val) return { nullptr, begin };
    it = args.it;

    return { std::make_shared<Symbols::Call>(std::move(*args.val)), it };
}

}

std::string kcuf(const std::string& code) {
    try {
        using namespace Parser;
        using namespace Transpile;

        Parsed p = Parsed::parse(code);
        Processor proc(p.program);

        return proc.run();
    }
    catch(const std::exception& ex) {
        throw std::string { ex.what() };
    }
}
