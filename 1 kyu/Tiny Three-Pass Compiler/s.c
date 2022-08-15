5265b0885fda8eac5900093b



#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>
#define div divide

typedef struct AST {
  enum op {imm, arg, plus, min, mul, div} op;
  struct AST *a, *b;
  int n;
} AST;

AST *Arg (int n)
{
    AST *node = calloc(1, sizeof(AST));
    node->op = arg;
    node->n = n;
    return node;
}

AST *Imm (int n)
{
    AST *node = Arg(n);
    node->op = imm;
    return node;
}

AST *Bin (enum op op, AST *a, AST *b)
{
    AST *node = calloc(1, sizeof(AST));
    node->a = a;
    node->b = b;
    node->op = op;
    return node;
}

// Turn a program string into an array of tokens (last entry is 0).
// Each token is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
// name or a number (as a string)
int nstrings;
int string_size;
char *strings;

const char builtin[] = "[\0]\0(\0)\0+\0-\0*\0/\0";
char *string_add(size_t n, const char *str)
{
  if (!strings) {
    string_size = 128;
    nstrings = 8;
    strings = calloc(string_size, sizeof(char));
    memcpy(strings, builtin, sizeof(builtin));
  }

  char *curr = strings;
  for (int i = 0; i < nstrings; i++) {
    size_t curr_length = strlen(curr);
    if (n == strlen(curr) && !strncmp(curr, str, n))
      return curr;
    curr += curr_length + 1;
  }

  strncpy(curr, str, n)[n] = '\0';
  nstrings++;
  return curr;
}

int num_toks = 0;

const char *find_end(const char *string, const char *stop)
{
    while (*string) {
      if (strchr(stop, *string))
        return string;
      string++;
    }

    //return the null terminating char at the end of the string
    return string;
}

char *get_token(const char *program, const char **rest)
{
  while (isspace(*program))
    program++;
  
  switch (program[0]){
      case '[':
      case ']':
      case '(':
      case ')':
      case '+':
      case '-':
      case '*':
      case '/':
          *rest = program + 1;
          break;
      default:
          *rest = find_end(program, " []()+-/*");
          break;
  }

  return string_add((int)(*rest - program), program);
}

char **tokenize(const char* program) {
  int capacity = 32;
  int filled = 0;
  const char *rest = program;
  char **tokens = calloc(capacity, sizeof(char*));
  
  while(*rest){
      if (filled == capacity){
        capacity *= 2;
        tokens = realloc(tokens, capacity);
      }
     tokens[filled] = get_token(rest, &rest);
     filled++;
  }

  tokens[filled] = NULL;
  return tokens;
}


// Returns an un-optimized AST

AST *parse_expression(int argc, char **argv, char **tokens, char ***rest);
AST *parse_term(int argc, char **argv, char **tokens, char ***rest);
AST *parse_factor(int argc, char **argv, char **tokens, char ***rest);

AST *parse_function(char **tokens, char ***rest)
{
    if (!strcmp(tokens[0], "[")){
        int argc = 0;
        while (strcmp(*++tokens, "]") != 0){
            argc++;
        }
        return parse_expression(argc, tokens - argc, tokens + 1, rest);
    }
  
    //Passing a NULL argument list will be a clue for later that we are parsing a simple expression
    return parse_expression(0, NULL, tokens, rest);
}

AST *parse_expression(int argc, char **argv, char **tokens, char ***rest)
{
    char ch = 0;
    AST *left = parse_term(argc, argv, tokens, rest);
    while (*rest && **rest) {
        AST *new_node = NULL;
        ch = ***rest;
        if (ch == '+'){
            (*rest)++;
            new_node = calloc(1, sizeof(AST));
            new_node->op = plus;
            new_node->a = left;
            new_node->b = parse_term(argc, argv, *rest, rest);
            left = new_node;
        } else if (ch == '-'){
            (*rest)++;
            new_node = calloc(1, sizeof(AST));
            new_node->op = min;
            new_node->a = left;
            new_node->b = parse_term(argc, argv, *rest, rest);
            left = new_node;
        } else {
            break;
        }
    }

    return left;
}

AST *parse_term(int argc, char **argv, char **tokens, char ***rest)
{
    char ch = 0;
    AST *left = parse_factor(argc, argv, tokens, rest);
    while (*rest && **rest) {
        AST *new_node = NULL;
        ch = ***rest;
        if (ch == '*'){
            (*rest)++;
            new_node = calloc(1, sizeof(AST));
            new_node->op = mul;
            new_node->a = left;
            new_node->b = parse_factor(argc, argv, *rest, rest);
            left = new_node;
        } else if (ch == '/'){
            (*rest)++;
            new_node = calloc(1, sizeof(AST));
            new_node->op = div;
            new_node->a = left;
            new_node->b = parse_factor(argc, argv, *rest, rest);
            left = new_node;
        } else {
            break;
        }
    }
    return left;
}

AST *parse_factor(int argc, char **argv, char **tokens, char ***rest)
{
    if (tokens[0][0] == '('){
        //Parse the encapulated expression
        AST *expr = parse_expression(argc, argv, tokens + 1, rest);
        (*rest)++;
        return expr;
    }

    //Try to match the current token to one of the argument names
    int num = -1;
    for (int i = 0; i < argc; i++){
        if (argv[i] == tokens[0]){
            num = i;
            break;
        }
    }

    AST *node = NULL;
    if (num > -1){
        //tokens[0] matched one of the arguments
        node = Arg(num);
    } else {
        //Token is an integer
        node = Imm(atoi(tokens[0]));
    }

    *rest = tokens + 1;
    return node;
}

void print_spaces(int n)
{while (n--) printf(" ");}

void print_tree(AST *node, int indent)
{
    const char *names[] = {
      "Imm", "Arg", "Plus", "Min", "Mul", "Div"
    };
    if (node) {
        int op = node->op;
        if (op == imm || op == arg){
            printf("%s(%i)", names[op], node->n);
        }
        else if (op > arg && op < div + 1){
            printf("%s(\n", names[op]);
            print_spaces(indent + 2);
            print_tree(node->a, indent + 2); printf(", "); print_tree(node->b, indent + 2);
            printf("\n");
            print_spaces(indent);
            printf(")");
        } else {
            printf("Error()");
        }
    }
}

AST *pass1 (const char* program) {
    char **tokens = tokenize (program);
    char **rest = NULL;
  
    if (tokens && *tokens) {
        return parse_function(tokens, &rest);
    }

    return NULL;
}

int execute(int op, int a, int b)
{
    switch (op){
        case plus:
          return a + b;
        case min:
          return a - b;
        case div:
          return a / b;
        case mul:
          return a * b;
        default:
          return 0;
    }
}

// Returns an AST with constant expressions reduced
AST *pass2 (AST *ast) {
    int a_is_imm, b_is_imm;
    a_is_imm = b_is_imm = 0;

    if (!ast)
        return ast;

    if (ast->a) {
        pass2(ast->a);
        a_is_imm = ast->a->op == imm;
    }
    if (ast->b) {
        pass2(ast->b);
        b_is_imm = ast->b->op == imm;
    }
    if (a_is_imm && b_is_imm){
        ast->n = execute(ast->op, ast->a->n, ast->b->n);
        free(ast->a); free(ast->b);
        ast->a = ast->b = NULL;
        ast->op = imm;
    }
  return ast;
}

// Returns assembly instructions

const char *instruction[] = {"IM", "AR", "AD", "SU", "MU", "DI", "SW", "PU", "PO"};
typedef enum {
  REG_SWAP = div + 1,
  STACK_PUSH,
  STACK_POP
} instruction_t;

char *pass3_reccur(AST *ast, char **current)
{
    if (!ast)
        return *current;

    if (ast->b) {
        pass3_reccur(ast->b, current);
    }

    if (ast->a) {
        if (ast->a->op < plus) {
            *current += sprintf(*current, "%s\n", instruction[REG_SWAP]);
            pass3_reccur(ast->a, current);
        } else {
            *current += sprintf(*current, "%s\n", instruction[STACK_PUSH]);
            pass3_reccur(ast->a, current);
            *current += sprintf(*current, "%s\n", instruction[REG_SWAP]);
            *current += sprintf(*current, "%s\n", instruction[STACK_POP]);
            *current += sprintf(*current, "%s\n", instruction[REG_SWAP]);
        }
    }  

    if (ast->op < plus){
        *current += sprintf(*current, "%s %i\n", instruction[ast->op], ast->n);
    } else {
        *current += sprintf(*current, "%s\n", instruction[ast->op]);
    }
  
    return *current;
}


char* pass3 (AST *ast) {
  char *code = malloc(512);
  char *current = code;
  code[0] = 0;
  pass3_reccur(ast, &current);
  return code;
}

char *compile (const char* program) {
    return pass3 (pass2 (pass1 (program)));
}

##############
#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define div divide
#define MAX_NUM_ARGS 100
#define MAX_LEN_IDENTIFIER 100
#define AST_NODE_FACTOR 7
#define MAX_STACK_SIZE 100

size_t tokens_len = 0;
char** args = 0;
size_t args_len = 0;
size_t ast_nodes_count = 0;

typedef enum OP_TYPE {imm, arg, plus, min, mul, div} OP_TYPE;

typedef struct AST {
    OP_TYPE op;
    struct AST *a, *b;
    int n;
} AST;

static OP_TYPE get_op(char operator) {
    switch (operator) {
        case '+': return plus;
        case '-': return min;
        case '*': return mul;
        case '/': return div;
        default: break;
    }

    return -1;
}

AST* Arg(int n) {
    AST* node = (AST*) malloc(sizeof(AST));
    node->a = 0;
    node->b = 0;
    node->op = arg;
    node->n = n;
    return node;
}

AST* Imm(int n) {
    AST* node = (AST*) malloc(sizeof(AST));
    node->a = 0;
    node->b = 0;
    node->op = imm;
    node->n = n;
    return node;
}

AST* Bin(OP_TYPE op, AST* restrict a, AST* restrict b) {
    AST* node = (AST*) malloc(sizeof(AST));
    node->a = a;
    node->b = b;
    node->op = op;
    node->n = -1;
    return node;
}

static void end_buffer(char** restrict tokens, char* restrict buffer, size_t* restrict token_p, int* restrict reading) {
    buffer[(*reading)++] = '\0';
    tokens[*token_p] = (char*) malloc(*reading * sizeof(char));
    *reading = 0;
    strcpy(tokens[(*token_p)++], buffer);
    free(buffer);
}

static void gen_arg_list(const char* restrict program) {
    char** args_copy = (char**) malloc(MAX_NUM_ARGS * sizeof(char*));
    char* program_copy = strdup(program);
    char* token = strtok(strtok(program_copy, "]"), " ");
    while ((token = strtok(0, " ")) != 0) args_copy[args_len++] = strdup(token);
    free(program_copy);

    args = malloc(args_len * sizeof(char*));
    memcpy(args, args_copy, args_len * sizeof(char*));
    free(args_copy);
}

static int lookup_arg(char* restrict arg) {
    for (size_t i = 0; i < args_len; ++i)
        if (strcmp(args[i], arg) == 0) return (int) i;

    return -1;
}

// Turn a program string into an array of tokens (last entry is 0).
// Each token is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
// name or a number (as a string)
char** tokenize(const char* program) {
    size_t len = strlen(program);
    char** tokens = (char**) malloc(len * sizeof(char*));
    size_t token_p = 0;

    char* buffer;
    int reading = 0;

    for (size_t i = 0; i < len; ++i) {
        if (program[i] == ' ') {
            if (reading > 0) end_buffer(tokens, buffer, &token_p, &reading);
            continue;
        }

        switch (program[i]) {
            case '[':
            case ']':
            case '(':
            case ')':
            case '+':
            case '-':
            case '*':
            case '/':
                if (reading > 0) end_buffer(tokens, buffer, &token_p, &reading);
                tokens[token_p] = (char*) malloc(2 * sizeof(char));
                tokens[token_p][0] = program[i];
                tokens[token_p++][1] = '\0';
                continue;
            default: // neither an operator nor a whitespace, thus, number or alphabetic character
                if (reading == 0) buffer = (char*) malloc(MAX_LEN_IDENTIFIER * sizeof(char));
                buffer[reading++] = program[i];
                break;
        }
    }

    gen_arg_list(program);

    tokens[token_p++] = 0;
    char** token_sized_copy = (char**) malloc(token_p * sizeof(char*));
    memcpy(token_sized_copy, tokens, token_p * sizeof(char*));
    free(tokens);
    tokens_len = token_p;
    return token_sized_copy;
}

static void add_op_node(AST** restrict ast_stack, int* restrict ast_sp, const OP_TYPE operator) {
    AST* right = ast_stack[(*ast_sp)--];
    AST* left = ast_stack[(*ast_sp)--];
    ast_stack[++(*ast_sp)] = Bin(operator, left, right);
    ++ast_nodes_count;
}

// * and / have precedence 1; + and - have precedence 0
static int compare_precedence(const char o1, const char o2) {
    int precedence = 0;
    if (o1 == '*' || o1 == '/') precedence += 2;
    if (o2 == '*' || o2 == '/') precedence -= 2;
    if (o1 == '+' || o1 == '-') ++precedence;
    if (o2 == '+' || o2 == '-') --precedence;
    return precedence;
}

// Returns an un-optimized AST
AST* pass1(const char* program) {
    char** tokens = tokenize(program);

    char** operator_stack = (char**) malloc(tokens_len * sizeof(char*));
    int operator_sp = -1;

    AST** ast_stack = (AST**) malloc(tokens_len * sizeof(AST*));
    int ast_sp = -1;

    // Start at args_len + 2 to ignore arg list
    for (size_t i = args_len + 2; i < tokens_len - 1; ++i) {
        switch (tokens[i][0]) {
            case '(':
                operator_stack[++operator_sp] = strdup(tokens[i]);
                continue;
            case ')':
                while (operator_sp >= 0) {
                    char popped = operator_stack[operator_sp--][0];
                    if (popped == '(') break;
                    else add_op_node(ast_stack, &ast_sp, get_op(popped));
                }
                continue;
            case '+':
            case '-':
            case '*':
            case '/':
                while (operator_sp >= 0) {
                    char popped = operator_stack[operator_sp][0];
                    if (popped != '(' && compare_precedence(popped, tokens[i][0]) >= 0) {
                        --operator_sp;
                        add_op_node(ast_stack, &ast_sp, get_op(popped));
                    } else break;
                }
                operator_stack[++operator_sp] = strdup(tokens[i]);
                continue;
            default: break;
        }

        if (tokens[i][0] >= 'a' && tokens[i][0] <= 'z')
            ast_stack[++ast_sp] = Arg(lookup_arg(tokens[i])), ++ast_nodes_count;
        else if (tokens[i][0] >= '0' && tokens[i][0] <= '9')
            ast_stack[++ast_sp] = Imm(strtol(tokens[i], 0, 10)), ++ast_nodes_count;
    }

    for (; operator_sp >= 0; --operator_sp)
        add_op_node(ast_stack, &ast_sp, get_op(operator_stack[operator_sp][0]));

    for (size_t i = 0; i < tokens_len; ++i) free(tokens[i]);
    free(tokens);

    for (size_t i = 0; i < args_len; ++i) free(args[i]);
    free(args);

    AST* ast = ast_stack[ast_sp];
    free(ast_stack);
    free(operator_stack);
    return ast;
}

static void replace_node(AST* restrict ast) {
    ast->op = imm;
    free(ast->a);
    free(ast->b);
    ast->a = 0;
    ast->b = 0;
}

// Returns an AST with constant expressions reduced
AST* pass2(AST* ast) {
    if (ast == 0) return 0;
    pass2(ast->a);
    pass2(ast->b);

    if (ast->a == 0 || ast->b == 0) return 0;
    else if (ast->a->op == imm && ast->b->op == imm) {
        switch (ast->op) {
            case mul:
                ast->n = ast->a->n * ast->b->n;
                replace_node(ast);
                break;
            case div:
                ast->n = ast->a->n / ast->b->n;
                replace_node(ast);
                break;
            case plus:
                ast->n = ast->a->n + ast->b->n;
                replace_node(ast);
                break;
            case min:
                ast->n = ast->a->n - ast->b->n;
                replace_node(ast);
                break;
            default: break;
        }
    }

    return ast;
}

char* get_asm_inst(OP_TYPE op) {
    switch (op) {
        case plus: return "AD";
        case min: return "SU";
        case mul: return "MU";
        case div: return "DI";
        default: return "-1";
    }
}

void post_order_code_gen(AST* restrict ast, char* restrict out, size_t* restrict out_p) {
    if (ast == 0) return;
    else if (ast->op == imm) {
        *out_p += sprintf(out + *out_p, "IM %d\n", ast->n);
    } else if (ast->op == arg) {
        *out_p += sprintf(out + *out_p, "AR %d\n", ast->n);
    } else {
        post_order_code_gen(ast->a, out, out_p);
        *out_p += sprintf(out + *out_p, "%s", "PU\n");
        post_order_code_gen(ast->b, out, out_p);
        *out_p += sprintf(out + *out_p, "%s%s\n", "SW\nPO\n", get_asm_inst(ast->op));
    }

    free(ast);
}

// Returns assembly instructions
char* pass3(AST* ast) {
    char* out = malloc(AST_NODE_FACTOR * ast_nodes_count * sizeof(char));
    size_t out_p = 0;
    post_order_code_gen(ast, out, &out_p);
    out[out_p] = '\0';
    return out;
}

char* compile(const char* program) {
    return pass3(pass2(pass1(program)));
}

#################################
#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define div divide
#define MAX_NUM_ARGS 100
#define MAX_LEN_IDENTIFIER 100
#define AST_NODE_FACTOR 7

size_t tokens_len = 0;
char** args = 0;
size_t args_len = 0;
size_t ast_nodes_count = 0;

typedef enum OP_TYPE {imm, arg, plus, min, mul, div} OP_TYPE;

typedef struct AST {
    OP_TYPE op;
    struct AST *a, *b;
    int n;
} AST;

static OP_TYPE get_op(char operator) {
    switch (operator) {
        case '+': return plus;
        case '-': return min;
        case '*': return mul;
        case '/': return div;
        default: break;
    }

    return -1;
}

AST* Arg(int n) {
    AST* node = (AST*) malloc(sizeof(AST));
    node->a = 0;
    node->b = 0;
    node->op = arg;
    node->n = n;
    return node;
}

AST* Imm(int n) {
    AST* node = (AST*) malloc(sizeof(AST));
    node->a = 0;
    node->b = 0;
    node->op = imm;
    node->n = n;
    return node;
}

AST* Bin(OP_TYPE op, AST* restrict a, AST* restrict b) {
    AST* node = (AST*) malloc(sizeof(AST));
    node->a = a;
    node->b = b;
    node->op = op;
    node->n = -1;
    return node;
}

static void end_buffer(char** restrict tokens, char* restrict buffer, size_t* restrict token_p, int* restrict reading) {
    buffer[(*reading)++] = '\0';
    tokens[*token_p] = (char*) malloc(*reading * sizeof(char));
    *reading = 0;
    strcpy(tokens[(*token_p)++], buffer);
    free(buffer);
}

static void gen_arg_list(const char* restrict program) {
    char** args_copy = (char**) malloc(MAX_NUM_ARGS * sizeof(char*));
    char* program_copy = strdup(program);
    char* token = strtok(strtok(program_copy, "]"), " ");
    while ((token = strtok(0, " ")) != 0) args_copy[args_len++] = strdup(token);
    free(program_copy);

    args = malloc(args_len * sizeof(char*));
    memcpy(args, args_copy, args_len * sizeof(char*));
    free(args_copy);
}

static int lookup_arg(char* restrict arg) {
    for (size_t i = 0; i < args_len; ++i)
        if (strcmp(args[i], arg) == 0) return (int) i;

    return -1;
}

// Turn a program string into an array of tokens (last entry is 0).
// Each token is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
// name or a number (as a string)
char** tokenize(const char* program) {
    size_t len = strlen(program);
    char** tokens = (char**) malloc(len * sizeof(char*));
    size_t token_p = 0;

    char* buffer;
    int reading = 0;

    for (size_t i = 0; i < len; ++i) {
        if (program[i] == ' ') {
            if (reading > 0) end_buffer(tokens, buffer, &token_p, &reading);
            continue;
        }

        switch (program[i]) {
            case '[':
            case ']':
            case '(':
            case ')':
            case '+':
            case '-':
            case '*':
            case '/':
                if (reading > 0) end_buffer(tokens, buffer, &token_p, &reading);
                tokens[token_p] = (char*) malloc(2 * sizeof(char));
                tokens[token_p][0] = program[i];
                tokens[token_p++][1] = '\0';
                continue;
            default: // neither an operator nor a whitespace, thus, number or alphabetic character
                if (reading == 0) buffer = (char*) malloc(MAX_LEN_IDENTIFIER * sizeof(char));
                buffer[reading++] = program[i];
                break;
        }
    }

    gen_arg_list(program);

    tokens[token_p++] = 0;
    char** token_sized_copy = (char**) malloc(token_p * sizeof(char*));
    memcpy(token_sized_copy, tokens, token_p * sizeof(char*));
    free(tokens);
    tokens_len = token_p;
    return token_sized_copy;
}

static void add_op_node(AST** restrict ast_stack, int* restrict ast_sp, const OP_TYPE operator) {
    AST* right = ast_stack[(*ast_sp)--];
    AST* left = ast_stack[(*ast_sp)--];
    ast_stack[++(*ast_sp)] = Bin(operator, left, right);
    ++ast_nodes_count;
}

// * and / have precedence 1; + and - have precedence 0
static int compare_precedence(const char o1, const char o2) {
    int precedence = 0;
    if (o1 == '*' || o1 == '/') precedence += 2;
    if (o2 == '*' || o2 == '/') precedence -= 2;
    if (o1 == '+' || o1 == '-') ++precedence;
    if (o2 == '+' || o2 == '-') --precedence;
    return precedence;
}

// Returns an un-optimized AST
AST* pass1(const char* program) {
    char** tokens = tokenize(program);

    char** operator_stack = (char**) malloc(tokens_len * sizeof(char*));
    int operator_sp = -1;

    AST** ast_stack = (AST**) malloc(tokens_len * sizeof(AST*));
    int ast_sp = -1;

    // Start at args_len + 2 to ignore arg list
    for (size_t i = args_len + 2; i < tokens_len - 1; ++i) {
        switch (tokens[i][0]) {
            case '(':
                operator_stack[++operator_sp] = strdup(tokens[i]);
                continue;
            case ')':
                while (operator_sp >= 0) {
                    char popped = operator_stack[operator_sp--][0];
                    if (popped == '(') break;
                    else add_op_node(ast_stack, &ast_sp, get_op(popped));
                }
                continue;
            case '+':
            case '-':
            case '*':
            case '/':
                while (operator_sp >= 0) {
                    char popped = operator_stack[operator_sp][0];
                    if (popped != '(' && compare_precedence(popped, tokens[i][0]) >= 0) {
                        --operator_sp;
                        add_op_node(ast_stack, &ast_sp, get_op(popped));
                    } else break;
                }
                operator_stack[++operator_sp] = strdup(tokens[i]);
                continue;
            default: break;
        }

        if (tokens[i][0] >= 'a' && tokens[i][0] <= 'z')
            ast_stack[++ast_sp] = Arg(lookup_arg(tokens[i])), ++ast_nodes_count;
        else if (tokens[i][0] >= '0' && tokens[i][0] <= '9')
            ast_stack[++ast_sp] = Imm(strtol(tokens[i], 0, 10)), ++ast_nodes_count;
    }

    for (; operator_sp >= 0; --operator_sp)
        add_op_node(ast_stack, &ast_sp, get_op(operator_stack[operator_sp][0]));

    for (size_t i = 0; i < tokens_len; ++i) free(tokens[i]);
    free(tokens);

    for (size_t i = 0; i < args_len; ++i) free(args[i]);
    free(args);

    AST* ast = ast_stack[ast_sp];
    free(ast_stack);
    free(operator_stack);
    return ast;
}

void traversal(AST* restrict ast, void (*action)(AST*, char*, size_t*), char* restrict out, size_t* restrict out_p) {
    if (ast == 0) return;
    traversal(ast->a, action, out, out_p);
    traversal(ast->b, action, out, out_p);
    (*action)(ast, out, out_p);
}

static void replace_node(AST* restrict ast) {
    ast->op = imm;
    free(ast->a);
    free(ast->b);
    ast->a = 0;
    ast->b = 0;
}

void constant_propagation(AST* restrict ast) {
    if (ast->a == 0 || ast->b == 0) return;
    else if (ast->a->op == imm && ast->b->op == imm) {
        switch (ast->op) {
            case mul:
                ast->n = ast->a->n * ast->b->n;
                replace_node(ast);
                break;
            case div:
                ast->n = ast->a->n / ast->b->n;
                replace_node(ast);
                break;
            case plus:
                ast->n = ast->a->n + ast->b->n;
                replace_node(ast);
                break;
            case min:
                ast->n = ast->a->n - ast->b->n;
                replace_node(ast);
                break;
            default: break;
        }
    }
}

// Returns an AST with constant expressions reduced
AST* pass2(AST* ast) {
    traversal(ast, (void (*)(AST *, char *, size_t *)) constant_propagation, 0, 0);
    return ast;
}

void code_gen(AST* restrict ast, char* restrict out, size_t* restrict out_p) {
    switch (ast->op) {
        case imm:
            *out_p += sprintf(out + *out_p, "IM %d\nPU\n", ast->n);
            break;
        case arg:
            *out_p += sprintf(out + *out_p, "AR %d\nPU\n", ast->n);
            break;
        case plus:
            *out_p += sprintf(out + *out_p, "%s", "PO\nSW\nPO\nAD\nPU\n");
            break;
        case min:
            *out_p += sprintf(out + *out_p, "%s", "PO\nSW\nPO\n\nSU\nPU\n");
            break;
        case mul:
            *out_p += sprintf(out + *out_p, "%s", "PO\nSW\nPO\nMU\nPU\n");
            break;
        case div:
            *out_p += sprintf(out + *out_p, "%s", "PO\nSW\nPO\nDI\nPU\n");
            break;
        default: break;
    }

    free(ast);
}

// Returns assembly instructions
char* pass3(AST* ast) {
    char* out = malloc(AST_NODE_FACTOR * ast_nodes_count * sizeof(char));
    size_t out_p = 0;
    traversal(ast, code_gen, out, &out_p);
    out[out_p] = '\0';
    return out;
}

char* compile(const char* program) {
    return pass3(pass2(pass1(program)));
}

##################################
#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define MAX_NUM_ARGS 100
#define MAX_LEN_IDENTIFIER 100
#define AST_NODE_FACTOR 7

typedef struct AST {
#define div divide
    enum op {imm, arg, plus, min, mul, div} op;
    struct AST *a, *b;
    int n;
} AST;

inline static enum op get_op(char operator) {
    switch (operator) {
        case '+': return plus;
        case '-': return min;
        case '*': return mul;
        case '/': return div;
        default: break;
    }

    return -1;
}

AST* Arg(int n) {
    AST* node = (AST*) malloc(sizeof(AST));
    node->a = 0;
    node->b = 0;
    node->op = arg;
    node->n = n;
    return node;
}

AST* Imm(int n) {
    AST* node = (AST*) malloc(sizeof(AST));
    node->a = 0;
    node->b = 0;
    node->op = imm;
    node->n = n;
    return node;
}

AST* Bin(enum op op, AST* restrict a, AST* restrict b) {
    AST* node = (AST*) malloc(sizeof(AST));
    node->a = a;
    node->b = b;
    node->op = op;
    node->n = -1;
    return node;
}

size_t tokens_len = 0;
char** args = 0;
size_t args_len = 0;
size_t ast_nodes_count = 0;

inline static void end_buffer(char** restrict tokens, char* restrict buffer, size_t* restrict token_p, int* restrict reading) {
    buffer[(*reading)++] = '\0';
    tokens[*token_p] = (char*) malloc(*reading * sizeof(char));
    *reading = 0;
    strcpy(tokens[(*token_p)++], buffer);
    free(buffer);
}

inline static void gen_arg_list(const char* restrict program) {
    char** args_copy = (char**) malloc(MAX_NUM_ARGS * sizeof(char*));
    char* program_copy = strdup(program);
    char* token = strtok(strtok(program_copy, "]"), " ");
    while ((token = strtok(0, " ")) != 0) args_copy[args_len++] = strdup(token);
    free(program_copy);

    args = malloc(args_len * sizeof(char*));
    memcpy(args, args_copy, args_len * sizeof(char*));
    free(args_copy);
}

inline static int lookup_arg(char* restrict arg) {
    for (size_t i = 0; i < args_len; ++i)
        if (strcmp(args[i], arg) == 0) return (int) i;

    return -1;
}

// Turn a program string into an array of tokens (last entry is 0).
// Each token is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
// name or a number (as a string)
char** tokenize(const char* restrict program) {
    size_t len = strlen(program);
    char** tokens = (char**) malloc(len * sizeof(char*));
    size_t token_p = 0;

    char* buffer;
    int reading = 0;

    for (size_t i = 0; i < len; ++i) {
        if (program[i] == ' ') {
            if (reading > 0) end_buffer(tokens, buffer, &token_p, &reading);
            continue;
        }

        switch (program[i]) {
            case '[':
            case ']':
            case '(':
            case ')':
            case '+':
            case '-':
            case '*':
            case '/':
                if (reading > 0) end_buffer(tokens, buffer, &token_p, &reading);
                tokens[token_p] = (char*) malloc(2 * sizeof(char));
                tokens[token_p][0] = program[i];
                tokens[token_p++][1] = '\0';
                continue;
            default: // neither an operator nor a whitespace, thus, number or alphabetic character
                if (reading == 0) buffer = (char*) malloc(MAX_LEN_IDENTIFIER * sizeof(char));
                buffer[reading++] = program[i];
                break;
        }
    }

    gen_arg_list(program);

    tokens[token_p++] = 0;
    char** token_sized_copy = (char**) malloc(token_p * sizeof(char*));
    memcpy(token_sized_copy, tokens, token_p * sizeof(char*));
    free(tokens);
    tokens_len = token_p;
    return token_sized_copy;
}

inline static void add_op_node(AST** restrict ast_stack, int* restrict ast_sp, const enum op operator) {
    AST* right = ast_stack[(*ast_sp)--];
    AST* left = ast_stack[(*ast_sp)--];
    ast_stack[++(*ast_sp)] = Bin(operator, left, right);
    ++ast_nodes_count;
}

// * and / have precedence 1; + and - have precedence 0
inline static int compare_precedence(const char o1, const char o2) {
    int precedence = 0;
    if (o1 == '*' || o1 == '/') precedence += 2;
    if (o2 == '*' || o2 == '/') precedence -= 2;
    if (o1 == '+' || o1 == '-') ++precedence;
    if (o2 == '+' || o2 == '-') --precedence;
    return precedence;
}

// Returns an un-optimized AST
AST* pass1(const char* restrict program) {
    char** tokens = tokenize(program);

    char** operator_stack = (char**) malloc(tokens_len * sizeof(char*));
    int operator_sp = -1;

    AST** ast_stack = (AST**) malloc(tokens_len * sizeof(AST*));
    int ast_sp = -1;

    // Start at args_len + 2 to ignore arg list
    for (size_t i = args_len + 2; i < tokens_len - 1; ++i) {
        switch (tokens[i][0]) {
            case '(':
                operator_stack[++operator_sp] = strdup(tokens[i]);
                continue;
            case ')':
                while (operator_sp >= 0) {
                    char popped = operator_stack[operator_sp--][0];
                    if (popped == '(') break;
                    else add_op_node(ast_stack, &ast_sp, get_op(popped));
                }
                continue;
            case '+':
            case '-':
            case '*':
            case '/':
                while (operator_sp >= 0) {
                    char popped = operator_stack[operator_sp][0];
                    if (popped != '(' && compare_precedence(popped, tokens[i][0]) >= 0) {
                        --operator_sp;
                        add_op_node(ast_stack, &ast_sp, get_op(popped));
                    } else break;
                }
                operator_stack[++operator_sp] = strdup(tokens[i]);
                continue;
            default: break;
        }

        if (tokens[i][0] >= 'a' && tokens[i][0] <= 'z')
            ast_stack[++ast_sp] = Arg(lookup_arg(tokens[i])), ++ast_nodes_count;
        else if (tokens[i][0] >= '0' && tokens[i][0] <= '9')
            ast_stack[++ast_sp] = Imm(strtol(tokens[i], 0, 10)), ++ast_nodes_count;
    }

    for (; operator_sp >= 0; --operator_sp)
        add_op_node(ast_stack, &ast_sp, get_op(operator_stack[operator_sp][0]));

    for (size_t i = 0; i < tokens_len; ++i) free(tokens[i]);
    free(tokens);

    for (size_t i = 0; i < args_len; ++i) free(args[i]);
    free(args);

    AST* ast = ast_stack[ast_sp];
    free(ast_stack);
    free(operator_stack);
    return ast;
}

void traversal(AST* restrict ast, void (*action)(AST*, char*, size_t*), char* restrict out, size_t* restrict out_p) {
    if (ast == 0) return;
    traversal(ast->a, action, out, out_p);
    traversal(ast->b, action, out, out_p);
    (*action)(ast, out, out_p);
}

inline static void replace_node(AST* restrict ast) {
    ast->op = imm;
    free(ast->a);
    free(ast->b);
    ast->a = 0;
    ast->b = 0;
}

void constant_propagation(AST* restrict ast) {
    if (ast->a == 0 || ast->b == 0) return;
    else if (ast->a->op == imm && ast->b->op == imm) {
        switch (ast->op) {
            case mul:
                ast->n = ast->a->n * ast->b->n;
                replace_node(ast);
                break;
            case div:
                ast->n = ast->a->n / ast->b->n;
                replace_node(ast);
                break;
            case plus:
                ast->n = ast->a->n + ast->b->n;
                replace_node(ast);
                break;
            case min:
                ast->n = ast->a->n - ast->b->n;
                replace_node(ast);
                break;
            default: break;
        }
    }
}

// Returns an AST with constant expressions reduced
AST* pass2(AST* restrict ast) {
    traversal(ast, (void (*)(AST *, char *, size_t *)) constant_propagation, 0, 0);
    return ast;
}

void code_gen(AST* restrict ast, char* restrict out, size_t* restrict out_p) {
    switch (ast->op) {
        case imm:
            *out_p += sprintf(out + *out_p, "IM %d\nPU\n", ast->n);
            break;
        case arg:
            *out_p += sprintf(out + *out_p, "AR %d\nPU\n", ast->n);
            break;
        case plus:
            *out_p += sprintf(out + *out_p, "%s", "PO\nSW\nPO\nAD\nPU\n");
            break;
        case min:
            *out_p += sprintf(out + *out_p, "%s", "PO\nSW\nPO\n\nSU\nPU\n");
            break;
        case mul:
            *out_p += sprintf(out + *out_p, "%s", "PO\nSW\nPO\nMU\nPU\n");
            break;
        case div:
            *out_p += sprintf(out + *out_p, "%s", "PO\nSW\nPO\nDI\nPU\n");
            break;
        default: break;
    }

    free(ast);
}

// Returns assembly instructions
char* pass3(AST* ast) {
    char* out = malloc(AST_NODE_FACTOR * ast_nodes_count * sizeof(char));
    size_t out_p = 0;
    traversal(ast, code_gen, out, &out_p);
    out[out_p] = '\0';
    return out;
}

char* compile(const char* program) {
    return pass3(pass2(pass1(program)));
}

##########################
#include <string.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#define div divide

char *strdup (const char*);
char* catn (char*, const char*, int);
char* cat (char*, const char*);
int count (const char*, int(*)(int));

#define new(T) calloc (sizeof(T),1)
#define len(T) (sizeof(T)/sizeof(T[0]))
#define append(a,v) (a = realloc (a, ++a##_size*sizeof(*a)), a[a##_size-1] = (v))

typedef struct AST {
  enum op {imm, arg, add, sub, mul, div} op;
  struct AST *a, *b;
  int n;
} AST;

AST *Arg (int n) { AST *ast = new (AST); ast->op = arg; ast->n = n; return ast; }
AST *Imm (int n) { AST *ast = new (AST); ast->op = imm; ast->n = n; return ast; }
AST *Bin (enum op op, AST *a, AST *b) { AST *ast = new (AST); ast->op = op; ast->a = a; ast->b = b; return ast; }
enum op op (char *s) { static char *ops[] = {"imm", "arg", "+", "-", "*", "/"}; for (unsigned long i = 0; i < len (ops); ++i) { if (!strcmp (s, ops[i])) return i; } return -1; }

char **tokens; int tokens_size;
char **args; int args_size;
char *instructions;
int cur;

int idx (char *arg) { for (int i = 0; args[i]; ++i) if (!strcmp (args[i], arg)) return i; return -1; } 
char* next (void) { return tokens[cur++]; }
char* front (void) { return tokens[cur]; }

AST *parse_expression ();

AST *parse_factor () {
  AST *ast;
  char *t = next ();
  if (t[0] == '(') {
    ast = parse_expression ();
    next ();
  } else if (count (t, isdigit) > 0)
    ast = Imm (atoi (t));
  else
    ast = Arg (idx (t));
  return ast;
}

AST *parse_term () {
  AST *ast = parse_factor (); char *t;
  while ((t = front ()) && strchr ("*/", *t) && next ())
    ast = Bin (op (t), ast, parse_factor ());
  return ast;
}

AST *parse_expression () {
  AST *ast = parse_term (); char *t;
  while ((t = front ()) && strchr ("+-", *t) && next ())
    ast = Bin (op (t), ast, parse_term ());
  return ast;
}

AST *parse_function () {
  next ();
  while (front () && front ()[0] != ']')
    append (args, strdup (next ()));  
  append (args, 0);
  next ();
  return parse_expression ();
}

char **tokenize (const char *program) {
  tokens = 0; tokens_size = cur = 0; int n;
  for (const char *p = program; *p; p += n) {
     if ((n = count (p, isspace)));
     else if (strchr ("+-*/()[]", *p))
        append (tokens, catn (0, p, n = 1));
     else if ((n = count (p, isdigit)) > 0)
        append (tokens, catn (0, p, n));
     else
        append (tokens, catn (0, p, n = count (p, isalpha)));
  }
  append (tokens, 0);
  return tokens;
}

AST *pass1 (const char *program) {
  args = 0; args_size = 0;
  tokenize (program);
  return parse_function ();
}

AST *pass2 (AST *ast) {
  if (ast && ast->a && ast->b) {
    AST *a = pass2 (ast->a);
    AST *b = pass2 (ast->b);
    if (a->op == imm && b->op == imm) {
      int v;
      switch (ast->op) {
      case add: v = a->n + b->n; break;
      case sub: v = a->n - b->n; break;
      case mul: v = a->n * b->n; break;
      case div: v = a->n / b->n; break;
      default: return ast;
      }
      ast = Imm (v);
    } else
      ast = Bin (ast->op, a, b);
  }
  return ast;
}

void gencode (AST *ast) {
  static char *opcodes[] = {"IM ", "AR ", "AD\n", "SU\n", "MU\n", "DI\n"};
  char num[22];
  if (ast->op == imm || ast->op == arg) {
    sprintf (num, "%d\n", ast->n);
    instructions = cat (instructions, cat (strdup (opcodes[ast->op]), num));
  } else {
    gencode (ast->a);
    instructions = cat (instructions, "PU\n");
    gencode (ast->b);
    instructions = cat (instructions, "SW\n");
    instructions = cat (instructions, "PO\n");
    instructions = cat (instructions, opcodes[ast->op]);
  }
}

char *pass3 (AST *ast) {
  instructions = 0;
  gencode (ast);
  return instructions;
}

char *compile (const char* program) {
    return pass3 (pass2 (pass1 (program)));
}

############################
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#define div divide

typedef enum op {imm, arg, plus, min, mul, div} op;
typedef struct AST {
  op op;
  struct AST *a, *b;
  int n;
} AST;

static void dispose(AST *ast) {
  if (!ast) { return; }

  dispose(ast->a);
  dispose(ast->b);
  free(ast);
}

AST *createAST(enum op op, AST *a, AST *b, int n) {
  AST *ast = malloc(sizeof(AST));
  if (!ast) {
    dispose(a);
    dispose(b);
  }
  *ast = (AST) { .op = op, .a = a, .b = b, .n = n };
  return ast;
}

AST *Arg (int n) { return createAST(arg, 0, 0, n); }
AST *Imm (int n) { return createAST(imm, 0, 0, n); }
AST *Bin (enum op op, AST *a, AST *b) { return createAST(op, a, b, 0); }

int addToken(char ***tokens, int *n, int *size, char *token) {
  if (*n == *size) {
    *size *= 2;
    char **tks = realloc(*tokens, (*size + 1) * sizeof(char *));
    if (!tks) {
      tks = malloc(*size * sizeof(char *));
      if (!tks) {
        return 0;
      }
      memcpy(tks, tokens, *n * sizeof(char *));
      free(*tokens);
    }
    *tokens = tks;
  }
  char *t = malloc(strlen(token) + 1);
  if (!t) {
    return 0;
  }
  strcpy(t, token);
  (*tokens)[*n] = t;
  (*n)++;
  return 1;
}

void cleanupTokens(char **tokens) {
  if (!tokens) {
    return;
  }
  for (char **p = tokens; *p; p++) {
    free(*p);
  }
  free(tokens);
}

// Turn a program string into an array of tokens (last entry is 0).
// Each token is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
// name or a number (as a string)

char **tokenize (const char* program) {
  int size = 32;
  char **result = malloc((size + 1) * sizeof(char *));
  int n = 0;

  for (const char *p = program; *p; p++) {
    if (isspace(*p)) {
      continue;
    }

    char *token = 0;
    if (strchr("[]()+-*/", *p)) {
      token = malloc(2);
      if (token) {
        token[0] = *p;
        token[1]= '\0';
      }
    } if (isalnum(*p)) {
      const char *start = p;
      int (*checker)(int) = isdigit(*p) ? &isdigit : &isalnum;
      for (; *p && checker(*p); p++);
      token = malloc(p - start + 1);
      memcpy(token, start, p - start);
      token[p - start] = '\0';
      p--;
    }

    if (!token) {
      result[n] = 0;
      cleanupTokens(result);
      return 0;
    }
    addToken(&result, &n, &size, token);
    free(token);
  }
  result[n] = 0;

  return result;
}

char *strdup(const char *s);
static char **argList(char **input, int *i) {
  int j = *i;
  if (input[j][0] != '[') {
    return 0;
  }
  for (j++; input[j] && input[j][0] != ']'; j++) {
    if (!isalnum(input[j][0])) {
      return 0;
    }
  }
  if (input[j][0] != ']') {
    return 0;
  }
  int count = j - *i - 1;
  char **result = malloc((count + 1) * sizeof(char *));
  for (int k = 0; k < count; k++) {
    result[k] = strdup(input[*i + 1 + k]);
    if (!result[k]) {
      cleanupTokens(result);
      return 0;
    }
  }
  result[count] = 0;

  *i = j + 1;

  return result;
}

static AST *variable(char **input, int *i, char **argNames) {
  if (!input || !input[*i] || !isalpha(input[*i][0]) || !argNames) {
    return 0;
  }

  int j = 0;
  for (; input[*i] && strcmp(argNames[j], input[*i]); j++);

  if (!input[*i]) {
    return 0;
  }

  (*i)++;

  return Arg(j);
}

static AST *number(char **input, int *i) {
  if (!input || !input[*i] || !isdigit(input[*i][0])) {
    return 0;
  }

  return Imm(atoi(input[(*i)++]));
}

static AST *expr(char **input, int *i, char **argNames);
static AST *factor(char **input, int *i, char **argNames) {
  AST *result = number(input, i) ?: variable(input, i, argNames);

  if (result) {
    return result;
  }

  if (!input || !input[*i] || input[*i][0] != '(') {
    return 0;
  }

  (*i)++;
  result = expr(input, i, argNames);
  if (!input || !input[*i] || input[*i][0] != ')') {
    dispose(result);
    return 0;
  }
  (*i)++;
  return result;
}

static AST *term(char **input, int *i, char **argNames) {
  AST *result = factor(input, i, argNames);

  while (result && input[*i] && strchr("*/", input[*i][0])) {
    op op = input[*i][0] == '*' ? mul : div;
    (*i)++;
    AST *rhs = factor(input, i, argNames);
    if (!rhs) {
      break;
    }
    result = Bin(op, result, rhs);
  }

  return result;
}

static AST *expr(char **input, int *i, char **argNames) {
  AST *result = term(input, i, argNames);

  while (result && input[*i] && strchr("+-", input[*i][0])) {
    op op = input[*i][0] == '+' ? plus : min;
    (*i)++;
    AST *rhs = term(input, i, argNames);
    if (!rhs) {
      break;
    }
    result = Bin(op, result, rhs);
  }
  return result;
}

static AST *funcDef(char **input, int *i) {
  char **argNames = argList(input, i);
  if (!argNames) {
    return 0;
  }

  AST *result = expr(input, i, argNames);
  cleanupTokens(argNames);

  return result;
}

static AST *prog(char **input) {
  int i = 0;
  AST *result = funcDef(input, &i);
  if (input[i]) {
    dispose(result);
    return 0;
  }
  return result;
}

// Returns an un-optimized AST

AST *pass1(const char* program) {
  char **tokens = tokenize(program);
  AST *result = prog(tokens);
  cleanupTokens(tokens);
  return result;
}

int eval(AST *ast, int *value) {
  if (!ast || ast->op == arg) {
    return 0;
  }
  if (ast->op == imm) {
    *value = ast->n;
    return 1;
  }
  int lhs = 0, rhs = 0;
  if (!eval(ast->a, &lhs) || !eval(ast->b, &rhs)) {
    return 0;
  }
  switch (ast->op) {
    case plus: *value = lhs + rhs; break;
    case min: *value = lhs - rhs; break;
    case mul: *value = lhs * rhs; break;
    case div: *value = lhs / rhs; break;
    default:
      return 0;
  }
  return 1;
}

AST *pass2_(AST **input) {
  if (!input) {
    return 0;
  }

  AST *ast = *input;
  if (!ast || ast->op == imm || ast->op == arg) {
    return ast;
  }

  AST *lhs = pass2_(&ast->a);
  AST *rhs = pass2_(&ast->b);

  if (lhs->op == imm && rhs->op == imm) {
    int validOp = 1;
    int value = 0;
    switch (ast->op) {
      case plus: value = lhs->n + rhs->n; break;
      case min: value = lhs->n - rhs->n; break;
      case mul: value = lhs->n * rhs->n; break;
      case div: value = lhs->n / rhs->n; break;
      default: validOp = 0; break;
    }
    if (validOp) {
      dispose(ast);
      ast = Imm(value);
      *input = ast;
    }
  }
  return ast;
}

// Returns an AST with constant expressions reduced

AST *pass2(AST *ast) {
  if (!ast) {
    return ast;
  }
  return pass2_(&ast);;
}

static int numDigits(int n) {
  int result = 0;
  for (; n; n /= 10) {
    result++;
  }
  return result ?: 1;
}

// Returns assembly instructions

char *pass3(AST *ast) {
  char *result = 0;

  if (!ast) {
    return result;
  }

  if (ast->op == imm || ast->op == arg) {
    int size = sizeof("%s %d") - 2 + numDigits(ast->n) + (ast->n < 0);
    result = malloc(size);
    if (result) {
      sprintf(result, "%s %d", ast->op == imm ? "IM" : "AR", ast->n);
    }
    return result;
  }

  char *op = 0;
  switch (ast->op) {
    case plus: op = "AD"; break;
    case min: op = "SU"; break;
    case mul: op = "MU"; break;
    case div: op = "DI"; break;
    default:
      break;
  }

  if (!op) {
    return 0;
  }

  char *lhs = pass3(ast->a);
  if (!lhs) {
    return 0;
  }

  char *rhs = pass3(ast->b);
  if (!rhs) {
    return 0;
  }

  char sp = '\n';
  unsigned long size = strlen(lhs) + 1 + sizeof("PU") + strlen(rhs) + 1 + sizeof("SW") + sizeof("PO") + strlen(op) + 1;
  result = malloc(size);
  if (!result) {
    return result;
  }
  sprintf(result, "%s%c%s%c%s%c%s%c%s%c%s", lhs, sp, "PU", sp, rhs, sp, "SW", sp, "PO", sp, op);
  return result;
}

char *compile(const char* program) {
    return pass3(pass2(pass1(program)));
}

######################################
