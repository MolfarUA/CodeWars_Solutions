#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

extern char *strdup (const char *);

char **tokenize (const char *src) {
    char *expr = strdup (src);
    const int size = strlen (expr) - 1;
    char *it = expr + 1, buff[32];
    char **token = malloc (3 * sizeof (char*));
    int i, j = 0;

    while (it - expr < size) {
      i = 0;

      if (*it == '(') {
        do { buff[i++] = *it; } while (*it++ != ')');
      } else {
        while (it - expr < size && *it != ' ') buff[i++] = *it++;
      }
      buff[i] = '\0';
      token[j++] = strdup (buff);
      it++;
    }

    return token;
  }
void removezero (char *src) {
  char *ptr = &src[strlen (src) - 1];

  while (*ptr == '0') *ptr-- = '\0';
  if (*ptr == '.') *ptr = '\0';
}
bool isnum (const char *expr) {

    for (int i = 0; expr[i] != '\0'; i++) {
        if (isalpha (expr[i])) return false;
        if (isspace (expr[i])) return false;
    }
    return true;
}

const char *calc (const char *arg1, char op, const char *arg2) {
    char *res = malloc (32 * sizeof (char)), *it;

    if (arg1[0] == '0' || arg2[0] == '0') {
        if (op == '*') return strdup ("0");
        if (op == '+') return arg1[0] == '0' ? arg2 : arg1;
    }

    if (strcmp (arg1, "1") == 0 || strcmp (arg2, "1") == 0) {
        if (op == '^') return arg1;
        if (op == '*') return strcmp (arg1, "1") == 0 ? arg2 : arg1;
        if (op == '/' && strcmp (arg2, "1") == 0) return arg1;
    }

    if (isnum (arg1) && isnum (arg2)) {
        double a = strtod (arg1, &it), b = strtod (arg2, &it);
        double val;

        switch (op) {
            case '+' : val = a + b; break;
            case '-' : val = a - b; break;
            case '*' : val = a * b; break;
            case '/' : val = a / b; break;
            case '^' : val = pow (a, b); break;
        }

        sprintf (res, "%f", val);
    } else {
        sprintf (res, "(%c %s %s)", op, arg1, arg2);
    }
    removezero(res);

    return res;
}
const char *diff (const char *input) {

    if (isnum(input)) return "0";
    if (input[0] == 'x') return "1";

    char **expr = tokenize (input);
    char *op = expr[0], arg1[32], buff[32];

    if (strcmp(op, "+") == 0) {   // add : a + b => a' + b'
        return calc (diff(expr[1]), '+', diff (expr[2]));
    }
    if (strcmp(op, "-") == 0) {   // add : a - b => a' - b'
        return calc (diff(expr[1]), '-', diff (expr[2]));
    }
    if (strcmp(op, "*") == 0) {   // mul : a * b => a.b' + a'.b
        const char *a = calc (expr[1], '*', diff (expr[2])), *b = calc (diff(expr[1]), '*', expr[2]);

        return calc (a, '+', b);
    }
    if (strcmp(op, "/") == 0) {   // div : a / b => (a'* b − b'* a) / (b * b)
        const char *a = calc (diff(expr[1]), '*', expr[2]), *b = calc (expr[1], '*', diff (expr[2]));
        const char *num = calc (a, '-', b), *den = calc (expr[2], '^', "2");
        return calc (num, '/', den);
    }
    if (strcmp(op, "^") == 0) {   // pow : x^a   => a.x^(a - 1)
        const char *ex = calc (expr[2], '-', "1");
        return calc (expr[2], '*', calc ("x", '^', ex));
    }
    if (strcmp(op, "ln") == 0) {  // ln  : ln(x) => 1 / x
        const char *ex = diff (expr[1]);
        return calc (ex, '/', expr[1]);
    }
    if (strcmp(op, "sin") == 0) { // sin : sin x => cos x
        const char *ex = diff (expr[1]);

        sprintf (buff, "(cos %s)", expr[1]);
        return calc (ex, '*', buff);
    }
    if (strcmp(op, "cos") == 0) { // cos : cos x => -sin x
        char ex[32];
        sprintf (ex, "-%s", diff (expr[1]));
        sprintf (buff, "(sin %s)", expr[1]);
        return calc (ex, '*', buff);
    }
    if (strcmp(op, "exp") == 0) { // exp : a^x   => a^x . ln (a)
        const char *ex = diff (expr[1]);
        sprintf (buff, "(exp %s)", expr[1]);

        return calc (ex, '*', buff);
    }
    if (strcmp(op, "tan") == 0) { // tan : tan x => 1 / (cos²(x))
        const char *ex = diff (expr[1]);
        sprintf (buff, "(cos %s)", expr[1]);
        sprintf (arg1,"%s", calc (buff, '^', "2"));

        return calc (ex, '/', arg1);
    }
    return "";
}
______________________________________________
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

extern char *strdup (const char *);

char **tokenize (const char *src) {
    char *expr = strdup (src);
    const int size = strlen (expr) - 1;
    char *it = expr + 1, buff[32];
    char **token = malloc (3 * sizeof (char*));
    int i, j = 0;

    while (it - expr < size) {
      i = 0;

      if (*it == '(') {
        do { buff[i++] = *it; } while (*it++ != ')');
      } else {
        while (it - expr < size && *it != ' ') buff[i++] = *it++;
      }
      buff[i] = '\0';
      token[j++] = strdup (buff);
      it++;
    }

    return token;
  }
void removezero (char *src) {
  char *ptr = &src[strlen (src) - 1];

  while (*ptr == '0') *ptr-- = '\0';
  if (*ptr == '.') *ptr = '\0';
}
bool isnum (const char *expr) {

    for (int i = 0; expr[i] != '\0'; i++) {
        if (isalpha (expr[i])) return false;
        if (isspace (expr[i])) return false;
    }
    return true;
}

const char *calc (const char *arg1, char op, const char *arg2) {
    char *res = malloc (32 * sizeof (char)), *it;

    if (arg1[0] == '0' || arg2[0] == '0') {
        if (op == '*') return strdup ("0");
        if (op == '+') return arg1[0] == '0' ? arg2 : arg1;
    }

    if (strcmp (arg1, "1") == 0 || strcmp (arg2, "1") == 0) {
        if (op == '^') return arg1;
        if (op == '*') return strcmp (arg1, "1") == 0 ? arg2 : arg1;
        if (op == '/' && strcmp (arg2, "1") == 0) return arg1;
    }

    if (isnum (arg1) && isnum (arg2)) {
        double a = strtod (arg1, &it), b = strtod (arg2, &it);
        double val;

        switch (op) {
            case '+' : val = a + b; break;
            case '-' : val = a - b; break;
            case '*' : val = a * b; break;
            case '/' : val = a / b; break;
            case '^' : val = pow (a, b); break;
        }

        sprintf (res, "%f", val);
    } else {
        sprintf (res, "(%c %s %s)", op, arg1, arg2);
    }
    removezero(res);
    //printf ("%s", res);
    return res;
}
const char *diff (const char *input) {

    if (isnum(input)) return "0";
    if (input[0] == 'x') return "1";

    char **expr = tokenize (input);
    char *op = expr[0], arg1[32], buff[32];

    if (strcmp(op, "+") == 0) {   // add : a + b => a' + b'
        return calc (diff(expr[1]), '+', diff (expr[2]));
    }
    if (strcmp(op, "-") == 0) {   // add : a - b => a' - b'
        return calc (diff(expr[1]), '-', diff (expr[2]));
    }
    if (strcmp(op, "*") == 0) {   // mul : a * b => a.b' + a'.b
        const char *a = calc (expr[1], '*', diff (expr[2])), *b = calc (diff(expr[1]), '*', expr[2]);

        //printf ("%s %s", expr[1], diff (expr[2]));
        return calc (a, '+', b);
    }
    if (strcmp(op, "/") == 0) {   // div : a / b => (a'* b − b'* a) / (b * b)
        const char *a = calc (diff(expr[1]), '*', expr[2]), *b = calc (expr[1], '*', diff (expr[2]));
        const char *num = calc (a, '-', b), *den = calc (expr[2], '^', "2");
        return calc (num, '/', den);
    }
    if (strcmp(op, "^") == 0) {   // pow : x^a   => a.x^(a - 1)
        const char *ex = calc (expr[2], '-', "1");
        return calc (expr[2], '*', calc ("x", '^', ex));
    }
    if (strcmp(op, "ln") == 0) {  // ln  : ln(x) => 1 / x
        const char *ex = diff (expr[1]);
        return calc (ex, '/', expr[1]);
    }
    if (strcmp(op, "sin") == 0) { // sin : sin x => cos x
        const char *ex = diff (expr[1]);

        sprintf (buff, "(cos %s)", expr[1]);
        //printf ("%s\n", expr[1]);
        return calc (ex, '*', buff);
    }
    if (strcmp(op, "cos") == 0) { // cos : cos x => -sin x
        char ex[32];
        sprintf (ex, "-%s", diff (expr[1]));
        sprintf (buff, "(sin %s)", expr[1]);
        return calc (ex, '*', buff);
    }
    if (strcmp(op, "exp") == 0) { // exp : a^x   => a^x . ln (a)
        const char *ex = diff (expr[1]);
        sprintf (buff, "(exp %s)", expr[1]);

        return calc (ex, '*', buff);
    }
    if (strcmp(op, "tan") == 0) { // tan : tan x => 1 / (cos²(x))
        const char *ex = diff (expr[1]);
        sprintf (buff, "(cos %s)", expr[1]);
        sprintf (arg1,"%s", calc (buff, '^', "2"));

        return calc (ex, '/', arg1);
    }
    return "";
}
______________________________________________
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct node_s node_s;

struct node_s {
    int op;
    double num;
    node_s *args[2];
};

static void
node_free (node_s *node) {
    if (!node) return;
    node_free(node->args[0]);
    node_free(node->args[1]);
    free(node);
}

static node_s * node_new (int op, node_s *arg0, node_s *arg1) {
    node_s *node = calloc(1, sizeof(node_s));
    node->op = op;
    node->args[0] = arg0;
    node->args[1] = arg1;
    return node;
}

static node_s * node_new_num (double num) {
    node_s *node = calloc(1, sizeof(node_s));
    node->num = num;
    return node;
}

static node_s * node_clone (const node_s *other) {
    if (!other) return NULL;
    node_s *node = calloc(1, sizeof(node_s));
    node->op = other->op;
    node->num = other->num;
    node->args[0] = node_clone(other->args[0]);
    node->args[1] = node_clone(other->args[1]);
    return node;
}

static inline int node_is_num (node_s const *node) {
    return node && node->op == 0;
}

static inline int node_eq_num (node_s const *node, int num) {
    return node && node->op == 0 && node->num == num;
}

static node_s * node_simplify (node_s *node) {
    if (!node) return NULL;

    if (node->args[0]) {
        node->args[0] = node_simplify(node->args[0]);
    }
    if (node->args[1]) {
        node->args[1] = node_simplify(node->args[1]);
    }

    if (node->op == '+') {
        if (node_eq_num(node->args[0], 0)) {
            node_s * node_new = node->args[1];
            node->args[1] = NULL;
            node_free(node);
            return node_new;
        }
        if (node_eq_num(node->args[1], 0)) {
            node_s * node_new = node->args[0];
            node->args[0] = NULL;
            node_free(node);
            return node_new;
        }
        if (node_is_num(node->args[0]) && node_is_num(node->args[1])) {
            node->op = 0;
            node->num = node->args[0]->num + node->args[1]->num;
            node_free(node->args[0]); node->args[0] = NULL;
            node_free(node->args[1]); node->args[1] = NULL;
            return node;
        }
    }

    if (node->op == '-') {
        if (node_eq_num(node->args[1], 0)) {
            node_s * node_new = node->args[0];
            node->args[0] = NULL;
            node_free(node);
            return node_new;
        }
        if (node_is_num(node->args[0]) && node_is_num(node->args[1])) {
            node->op = 0;
            node->num = node->args[0]->num - node->args[1]->num;
            node_free(node->args[0]); node->args[0] = NULL;
            node_free(node->args[1]); node->args[1] = NULL;
            return node;
        }
    }

    if (node->op == '*') {
        if (node_eq_num(node->args[0], 0) || node_eq_num(node->args[1], 0)) {
            node_free(node);
            return node_new_num(0);
        }
        if (node_eq_num(node->args[0], 1)) {
            node_s * node_new = node->args[1];
            node->args[1] = NULL;
            node_free(node);
            return node_new;
        }
        if (node_eq_num(node->args[1], 1)) {
            node_s * node_new = node->args[0];
            node->args[0] = NULL;
            node_free(node);
            return node_new;
        }
        if (node_is_num(node->args[0]) && node_is_num(node->args[1])) {
            node->op = 0;
            node->num = node->args[0]->num*node->args[1]->num;
            node_free(node->args[0]); node->args[0] = NULL;
            node_free(node->args[1]); node->args[1] = NULL;
            return node;
        }
    }

    if (node->op == '/') {
        if (node_eq_num(node->args[0], 0)) {
            node_free(node);
            return node_new_num(0);
        }
        if (node_eq_num(node->args[1], 1)) {
            node_s * node_new = node->args[0];
            node->args[0] = NULL;
            node_free(node);
            return node_new;
        }
        if (node_is_num(node->args[0]) && node_is_num(node->args[1])) {
            node->op = 0;
            node->num = node->args[0]->num/node->args[1]->num;
            node_free(node->args[0]); node->args[0] = NULL;
            node_free(node->args[1]); node->args[1] = NULL;
            return node;
        }
    }

    if (node->op == '^') {
        if (node_eq_num(node->args[1], 0)) {
            node->op = 0;
            node->num = 1;
            node_free(node->args[0]); node->args[0] = NULL;
            node_free(node->args[1]); node->args[1] = NULL;
            return node;
        }
        if (node_eq_num(node->args[1], 1)) {
            node_s *node_new = node->args[0];
            node->args[0] = NULL;
            node_free(node);
            return node_new;
        }
        if (node_eq_num(node->args[0], 0)) {
            node_free(node);
            return node_new_num(0);
        }
        if (node_eq_num(node->args[0], 1)) {
            node_free(node);
            return node_new_num(1);
        }
        if (node_is_num(node->args[0]) && node_is_num(node->args[1])) {
            node->op = 0;
            node->num = pow(node->args[0]->num, node->args[1]->num);
            node_free(node->args[0]); node->args[0] = NULL;
            node_free(node->args[1]); node->args[1] = NULL;
            return node;
        }
    }

    return node;
}

static node_s * node_read (const char **ps)
{
    const char *s = *ps;

    while (*s == ' ') { ++s; }
    if (*s == 0) return NULL;

    node_s *node = calloc(1, sizeof(node_s));;

    if (*s == '(') {
        ++s;

        node->op = *s++;
        while (*s && *s != ' ') { ++s; }

        if (strchr("elcst", node->op)) {
            node->args[0] = node_read(&s);
        }
        if (strchr("+-*/^", node->op)) {
            node->args[0] = node_read(&s);
            node->args[1] = node_read(&s);
        }

        if (*s == ')') { ++s; }
    } else if (*s == 'x') {
        ++s;
        node->op = 'x';
    } else {
        const char *end = s;
        node->num = strtod(s, (char **)&end);
        s = end;
    }

    *ps = s;
    return node;
}

static void str_write (char **ps, size_t *plen, char *v) {
    char *s = *ps;
    size_t len = *plen;
    size_t v_len = strlen(v);
    if (v_len == 0) return;

    *ps = s = realloc(s, len + v_len + 1);
    memcpy(s + len, v, v_len);
    *plen = len + v_len;
}

static void node_write (node_s const * node, char **ps, size_t *plen)
{
    char buf[80];

    if (!node) {
        return;
    }

    if (node->op == 0) {
        sprintf(buf, "%g", node->num);
        str_write(ps, plen, buf);
        return;
    }

    if (node->op == 'x') {
        str_write(ps, plen, "x");
        return;
    }

    str_write(ps, plen, "(");

    switch (node->op) {
    case 'e':
        str_write(ps, plen, "exp");
        break;
    case 'l':
        str_write(ps, plen, "ln");
        break;
    case 'c':
        str_write(ps, plen, "cos");
        break;
    case 's':
        str_write(ps, plen, "sin");
        break;
    case 't':
        str_write(ps, plen, "tan");
        break;
    default:
        sprintf(buf, "%c", node->op);
        str_write(ps, plen, buf);
    }

    if (node->args[0]) {
        str_write(ps, plen, " ");
        node_write(node->args[0], ps, plen);
    }
    if (node->args[1]) {
        str_write(ps, plen, " ");
        node_write(node->args[1], ps, plen);
    }

    str_write(ps, plen, ")");
}

static node_s * node_diff (const node_s *node)
{
    if (!node) return NULL;

    node_s *n1 = NULL;

    if (node->op == 0) {
        n1 = node_new_num(0);
    } else if (node->op == 'x') {
        n1 = node_new_num(1);
    } else if (node->op == '+') {
        n1 = node_new('+', node_diff(node->args[0]), node_diff(node->args[1]));
    } else if (node->op == '-') {
        n1 = node_new('-', node_diff(node->args[0]), node_diff(node->args[1]));
    } else if (node->op == '*') {
        n1 = node_new('+',
            node_new('*', node_diff(node->args[0]), node_clone(node->args[1])),
            node_new('*', node_clone(node->args[0]), node_diff(node->args[1]))
        );
    } else if (node->op == '/') {
        n1 = node_new('/',
            node_new('-',
                node_new('*', node_diff(node->args[0]), node_clone(node->args[1])),
                node_new('*', node_clone(node->args[0]), node_diff(node->args[1]))),
            node_new('^', node_clone(node->args[1]), node_new_num(2))
        );
    } else if (node->op == '^') {
        if (node_is_num(node->args[0])) {
            double a = node->args[0]->num;
            n1 = node_new('*',
                node_new('*',
                    node_new('^', node_new_num(a), node_clone(node->args[0])),
                    node_new('l', node_new_num(a), NULL)
                ),
                node_diff(node->args[0])
            );
        } else if (node_is_num(node->args[1])) {
            double a = node->args[1]->num;
            n1 = node_new('*',
                node_new('*',
                    node_new_num(a),
                    node_new('^', node_clone(node->args[0]), node_new_num(a - 1))
                ),
                node_diff(node->args[0])
            );
        } else {
            n1 =
                node_new('*',
                    node_clone(node),
                    node_new('+',
                        node_new('*',
                            node_diff(node->args[1]),
                            node_new('l', node_clone(node->args[0]), NULL)
                        ),
                        node_new('/',
                            node_new('*', node_clone(node->args[1]), node_diff(node->args[0])),
                            node_clone(node->args[0])
                        )
                    )
                );
        }
    } else if (node->op == 'e') {
        n1 = node_new('*',
            node_diff(node->args[0]),
            node_new('e', node_clone(node->args[0]), NULL)
        );
    } else if (node->op == 'l') {
        n1 = node_new('/', node_diff(node->args[0]), node_clone(node->args[0]));
    } else if (node->op == 'c') {
        n1 = node_new('*',
            node_diff(node->args[0]),
            node_new('*', node_new_num(-1), node_new('s', node_clone(node->args[0]), NULL))
        );
    } else if (node->op == 's') {
        n1 = node_new('*',
            node_diff(node->args[0]),
            node_new('c', node_clone(node->args[0]), NULL)
        );
    } else if (node->op == 't') {
        n1 = node_new('*',
            node_diff(node->args[0]),
            node_new('^', node_new('c', node_clone(node->args[0]), NULL), node_new_num(-2))
        );
    }

    return node_simplify(n1);
}

const char* diff (const char* input) {
    char *s = malloc(1);
    size_t len = 0;

    node_s *node = node_read(&input);
    node = node_simplify(node);

    node_s *n1 = node_diff(node);
    n1 = node_simplify(n1);

    node_write(n1, &s, &len);

    node_free(n1);
    node_free(node);

    s[len] = 0;
    return s;
}
______________________________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#define BUF_SIZE 256
#define NOT_ALL_ARGUMENTS_DECOMPOSED 1

typedef struct expr {
    char *name;
    struct expr **args;
} expr_t;

expr_t *plus_d(expr_t *expr);
expr_t *minus_d(expr_t *expr);
expr_t *mul_d(expr_t *expr);
expr_t *div_d(expr_t *expr);
expr_t *pow_d(expr_t *expr);
expr_t *cos_d(expr_t *expr);
expr_t *sin_d(expr_t *expr);
expr_t *tan_d(expr_t *expr);
expr_t *exp_d(expr_t *expr);
expr_t *ln_d(expr_t *expr);
expr_t *common_derivative(expr_t *expr);

expr_t *plus_s(expr_t *expr);
expr_t *minus_s(expr_t *expr);
expr_t *mul_s(expr_t *expr);
expr_t *div_s(expr_t *expr);
expr_t *pow_s(expr_t *expr);
expr_t *common_simplify(expr_t *expr);

const char *op_func_names[] = { "+", "-", "*", "/", "^", "cos", "sin", "tan", "exp", "ln", NULL };
expr_t* (*op_func_derivatives[]) (expr_t *expr)  = { plus_d, minus_d, mul_d, div_d, pow_d, cos_d, sin_d, tan_d, exp_d, ln_d };

const char *op_simple_names[] = { "+", "-", "*", "/", "^", NULL };
expr_t* (*op_simple[]) (expr_t *expr)  = { plus_s, minus_s, mul_s, div_s, pow_s };

int index_of(const char *arr[], char *name) {
    for (int i = 0; arr[i] != NULL; i++) {
        if (strcmp(name, arr[i]) == 0) {
            return i;
        }
    }
    return -1;
}

char *dup_str(const char *str) {
    size_t size = strlen(str) + 1;
    char *dup = (char *)calloc(size, sizeof(char));
    memcpy(dup, str, size);
    return dup;
}

char *double_to_str(double num) {
    char *str = (char *)malloc(16 * sizeof(char));
    sprintf(str, "%lf", num);
    while (str[strlen(str) - 1] == '0') {
        str[strlen(str) - 1] = '\0';
    }
    if (str[strlen(str) - 1] == '.') {
        str[strlen(str) - 1] = '\0';
    }
    return str;
}

int str_to_double(const char *str) {
    return atof(str);
}

expr_t *dup_expr(expr_t *expr) {
    expr_t *dup = (expr_t *)malloc(sizeof(expr_t));
    dup->name = dup_str(expr->name);
    if (expr->args == NULL) {   //0 args
        dup->args = NULL;
    }
    else {
        dup->args = (expr_t **)calloc(3, sizeof(expr_t *));
        int count = 0;
        for (expr_t **arg = expr->args; *arg != NULL; arg++) {
            dup->args[count] = dup_expr(*arg);
            count++;
        }
        dup->args[count] = NULL;
    }
    return dup;
}

void free_expr(expr_t *expr) {
    free(expr->name);
    if (expr->args != NULL) {
        for (expr_t **arg = expr->args; *arg != NULL; arg++) {
            free_expr(*arg);
        }
    }
    free(expr);
}

expr_t *make_expr_0_args(const char *name) {
    expr_t *expr = (expr_t *)malloc(sizeof(expr_t));
    expr->name = dup_str(name);
    expr->args = NULL;
    return expr;
}

expr_t *make_expr_1_arg(const char *name, expr_t *arg) {
    expr_t *expr = (expr_t *)malloc(sizeof(expr_t));
    expr->name = dup_str(name);
    expr->args = (expr_t **)calloc(3, sizeof(expr_t *));
    expr->args[0] = dup_expr(arg);
    expr->args[1] = NULL;
    return expr;
}

expr_t *make_expr_2_args(const char *name, expr_t *arg1, expr_t *arg2) {
    expr_t *expr = (expr_t *)malloc(sizeof(expr_t));
    expr->name = dup_str(name);
    expr->args = (expr_t **)calloc(3, sizeof(expr_t *));
    expr->args[0] = dup_expr(arg1);
    expr->args[1] = dup_expr(arg2);
    expr->args[2] = NULL;
    return expr;
}

expr_t *plus_d(expr_t *expr) {      //(u + v)' = u' + v'
    if (strcmp(expr->name, "+") != 0) return NULL;

    expr_t *u = expr->args[0];
    expr_t *v = expr->args[1];

    return make_expr_2_args("+",
                            common_derivative(u),
                            common_derivative(v));
}

expr_t *minus_d(expr_t *expr) {     //(u - v)' = u' - v'
    if (strcmp(expr->name, "-") != 0) return NULL;

    expr_t *u = expr->args[0];
    expr_t *v = expr->args[1];

    return make_expr_2_args("-",
                            common_derivative(u),
                            common_derivative(v));
}

expr_t *mul_d(expr_t *expr) {       //(uv)' = u'v + uv'
    if (strcmp(expr->name, "*") != 0) return NULL;

    expr_t *u = expr->args[0];
    expr_t *v = expr->args[1];

    return make_expr_2_args("+",
                             make_expr_2_args("*",
                                              common_derivative(u),
                                              dup_expr(v)),
                             make_expr_2_args("*",
                                              dup_expr(u),
                                              common_derivative(v)));
}

expr_t *div_d(expr_t *expr) {       //(u/v)' = (u'v - uv')/v^2
    if (strcmp(expr->name, "/") != 0) return NULL;

    expr_t *u = expr->args[0];
    expr_t *v = expr->args[1];

    return make_expr_2_args("/",
                            make_expr_2_args("-",
                                             make_expr_2_args("*",
                                                              common_derivative(u),
                                                              dup_expr(v)),
                                             make_expr_2_args("*",
                                                              dup_expr(u),
                                                              common_derivative(v))),
                            make_expr_2_args("^",
                                             dup_expr(v),
                                             make_expr_0_args("2")));
}

expr_t *pow_d(expr_t *expr) {       //(u^n)' = (n*u^(n-1)) * u'
    if (strcmp(expr->name, "^") != 0) return NULL;
    if (expr->args[1]->args != NULL) return NULL;

    expr_t *u = expr->args[0];
    expr_t *n = expr->args[1];
    return make_expr_2_args("*",
                            make_expr_2_args("*",
                                             dup_expr(n),
                                             make_expr_2_args("^",
                                                              dup_expr(u),
                                                              make_expr_2_args("-",
                                                                               dup_expr(n),
                                                                               make_expr_0_args("1")))),
                            common_derivative(u));
}

expr_t *cos_d(expr_t *expr) {       //(cos u)' = (-1 * sin u) * u'
    if (strcmp(expr->name, "cos") != 0) return NULL;
    expr_t *u = expr->args[0];
    return make_expr_2_args("*",
                            make_expr_2_args("*",
                                             make_expr_0_args("-1"),
                                             make_expr_1_arg("sin", u)),
                            common_derivative(u));
}

expr_t *sin_d(expr_t *expr) {       //(sin u)' = (cos u) * u'
    if (strcmp(expr->name, "sin") != 0) return NULL;
    expr_t *u = expr->args[0];
    return make_expr_2_args("*",
                            make_expr_1_arg("cos", u),
                            common_derivative(u));
}

expr_t *tan_d(expr_t *expr) {       //(tan u)' = u' / (cos u) ^ 2
    if (strcmp(expr->name, "tan") != 0) return NULL;
    expr_t *u = expr->args[0];
    return make_expr_2_args("/",
                            common_derivative(u),
                            make_expr_2_args("^",
                                             make_expr_1_arg("cos", u),
                                             make_expr_0_args("2")));
}

expr_t *exp_d(expr_t *expr) {       //(exp(u))' = exp(u) * u'
    if (strcmp(expr->name, "exp") != 0) return NULL;
    expr_t *u = expr->args[0];
    return make_expr_2_args("*",
                            make_expr_1_arg("exp", u),
                            common_derivative(u));
}

expr_t *ln_d(expr_t *expr) {        //(ln(u))' = u' / u
    if (strcmp(expr->name, "ln") != 0) return NULL;
    expr_t *u = expr->args[0];
    return make_expr_2_args("/",
                            common_derivative(u),
                            dup_expr(u));
}

expr_t *common_derivative(expr_t *expr) {
    if (expr->args == NULL) {       //no args - const or x
        return make_expr_0_args(strcmp(expr->name, "x") == 0 ? "1" : "0");
    }
    else {      //1 or 2 args - op or func
        int index = index_of(op_func_names, expr->name);
        if (index == -1) return NULL;
        return op_func_derivatives[index](expr);
    }
}

expr_t *plus_s(expr_t *expr) {
    expr_t *arg1 = common_simplify(expr->args[0]);
    expr_t *arg2 = common_simplify(expr->args[1]);
    if (arg1->args == NULL && strcmp(arg1->name, "x") != 0 &&
        arg2->args == NULL && strcmp(arg2->name, "x") != 0) {
        double val1 = str_to_double(arg1->name);
        double val2 = str_to_double(arg2->name);
        char *val = double_to_str(val1 + val2);
        expr_t *simple = make_expr_0_args(val);
        free(val);
        return simple;
    }
    if (strcmp(arg1->name, "0") == 0) {
        return arg2;
    }
    if (strcmp(arg2->name, "0") == 0) {
        return arg1;
    }
    return make_expr_2_args("+", arg1, arg2);
}

expr_t *minus_s(expr_t *expr) {
    expr_t *arg1 = common_simplify(expr->args[0]);
    expr_t *arg2 = common_simplify(expr->args[1]);
    if (arg1->args == NULL && strcmp(arg1->name, "x") != 0 &&
        arg2->args == NULL && strcmp(arg2->name, "x") != 0) {
        double val1 = str_to_double(arg1->name);
        double val2 = str_to_double(arg2->name);
        char *val = double_to_str(val1 - val2);
        expr_t *simple = make_expr_0_args(val);
        free(val);
        return simple;
    }
    if (strcmp(arg2->name, "0") == 0) {
        return arg1;
    }
    return make_expr_2_args("-", arg1, arg2);
}

expr_t *mul_s(expr_t *expr) {
    expr_t *arg1 = common_simplify(expr->args[0]);
    expr_t *arg2 = common_simplify(expr->args[1]);
    if (arg1->args == NULL && strcmp(arg1->name, "x") != 0 &&
        arg2->args == NULL && strcmp(arg2->name, "x") != 0) {
        double val1 = str_to_double(arg1->name);
        double val2 = str_to_double(arg2->name);
        char *val = double_to_str(val1 * val2);
        expr_t *simple = make_expr_0_args(val);
        free(val);
        return simple;
    }
    if (strcmp(arg1->name, "0") == 0 || strcmp(arg2->name, "0") == 0) {
        return make_expr_0_args("0");
    }
    if (strcmp(arg1->name, "1") == 0) {
        return arg2;
    }
    if (strcmp(arg2->name, "1") == 0) {
        return arg1;
    }
    if (arg2->args == NULL && strcmp(arg2->name, "x") != 0) {
        return make_expr_2_args("*", arg2, arg1);
    }
    else {
        return make_expr_2_args("*", arg1, arg2);
    }
}

expr_t *div_s(expr_t *expr) {
    expr_t *arg1 = common_simplify(expr->args[0]);
    expr_t *arg2 = common_simplify(expr->args[1]);
    if (arg1->args == NULL && strcmp(arg1->name, "x") != 0 &&
            arg2->args == NULL && strcmp(arg2->name, "x") != 0) {
        double val1 = str_to_double(arg1->name);
        double val2 = str_to_double(arg2->name);
        char *val = double_to_str(val1 / val2);
        expr_t *simple = make_expr_0_args(val);
        free(val);
        return simple;
    }
    return make_expr_2_args("/", arg1, arg2);
}

expr_t *pow_s(expr_t *expr) {
    expr_t *arg1 = common_simplify(expr->args[0]);
    expr_t *arg2 = common_simplify(expr->args[1]);
    if (arg1->args == NULL && strcmp(arg1->name, "x") != 0) {
        double val1 = str_to_double(expr->args[0]->name);
        double val2 = str_to_double(expr->args[1]->name);
        char *val = double_to_str((int) pow(val1, val2));
        expr_t *simple = make_expr_0_args(val);
        free(val);
        return simple;
    }
    if (strcmp(arg2->name, "0") == 0) {
        return make_expr_0_args("1");
    }
    if (strcmp(arg2->name, "1") == 0) {
        return arg1;
    }
    return make_expr_2_args("^", arg1, arg2);
}

expr_t *common_simplify(expr_t *expr) {
    if (expr == NULL) return NULL;
    if (expr->args == NULL) {   //0 args
        return dup_expr(expr);
    }
    else if (expr->args[1] == NULL) {   //1 args - func
        return make_expr_1_arg(dup_str(expr->name), common_simplify(expr->args[0]));
    }
    else if (expr->args[2] == NULL) {   //2 args - op
        int index = index_of(op_simple_names, expr->name);
        if (index == -1) return NULL;
        return op_simple[index](expr);
    }
    return dup_expr(expr);
}

expr_t *extra_simplify(expr_t *expr) {
    if (expr == NULL) return NULL;
    if (expr->args == NULL) {   //0 args
        return dup_expr(expr);
    }
    else if (expr->args[1] == NULL) {   //1 args - func
        return make_expr_1_arg(dup_str(expr->name), extra_simplify(expr->args[0]));
    }
    else if (expr->args[2] == NULL) {   //2 args - op
        expr_t *arg1 = extra_simplify(expr->args[0]);
        expr_t *arg2 = extra_simplify(expr->args[1]);
        if (arg1->args == NULL && strcmp(arg1->name, "x") != 0) {
            if (strcmp(arg2->name, expr->name) == 0) {
                if (arg2->args[0]->args == NULL && strcmp(arg2->args[0]->name, "x") != 0) {
                    return common_simplify(make_expr_2_args(expr->name,
                                                            make_expr_2_args(expr->name,
                                                                             arg1,
                                                                             arg2->args[0]),
                                                            dup_expr(arg2->args[1])));
                }
                if (arg2->args[1]->args == NULL && strcmp(arg2->args[1]->name, "x") != 0) {
                    return common_simplify(make_expr_2_args(expr->name,
                                                            make_expr_2_args(expr->name,
                                                                             arg1,
                                                                             arg2->args[1]),
                                                            dup_expr(arg2->args[0])));
                }
            }
        }
        if (arg2->args == NULL && strcmp(arg2->name, "x") != 0) {
            if (strcmp(arg1->name, expr->name) == 0) {
                if (arg1->args[0]->args == NULL && strcmp(arg1->args[0]->name, "x") != 0) {
                    return common_simplify(make_expr_2_args(expr->name,
                                                            make_expr_2_args(expr->name,
                                                                             arg2,
                                                                             arg1->args[0]),
                                                            dup_expr(arg1->args[1])));
                }
                if (arg1->args[1]->args == NULL && strcmp(arg1->args[1]->name, "x") != 0) {
                    return common_simplify(make_expr_2_args(expr->name,
                                                            make_expr_2_args(expr->name,
                                                                             arg2,
                                                                             arg1->args[1]),
                                                            dup_expr(arg1->args[0])));
                }
            }
        }
        return make_expr_2_args(expr->name, arg1, arg2);
    }
    return dup_expr(expr);
}

char *construct_string(expr_t *expr) {
    if (expr == NULL) return NULL;
    char *str = (char *)calloc(BUF_SIZE, sizeof(char));
    if (expr->args == NULL) {   //0 args
        sprintf(str, "%s", expr->name);
    }
    else if (expr->args[1] == NULL) {   //1 args
        char *arg = construct_string(expr->args[0]);
        sprintf(str, "(%s %s)", expr->name, arg);
        free(arg);
    }
    else if (expr->args[2] == NULL) {   //2 args
        char *arg1 = construct_string(expr->args[0]);
        char *arg2 = construct_string(expr->args[1]);
        sprintf(str, "(%s %s %s)", expr->name, arg1, arg2);
        free(arg1);
        free(arg2);
    }
    return str;
}

expr_t *decompose(const char *expr) {
    if (expr == NULL || strlen(expr) == 0) return NULL;
    expr_t *decomposed = (expr_t *)malloc(sizeof(expr_t));
    if (expr[0] == '(') {     //op or func
        char *name = (char *)calloc(BUF_SIZE, sizeof(char));
        const char *ch;
        for (ch = expr + 1; *ch != ' '; ch++) {
            name[strlen(name)] = *ch;
        }
        decomposed->name = name;
        decomposed->args = (expr_t **)calloc(3, sizeof(expr_t *));
        int cur_arg = 0;

        while (NOT_ALL_ARGUMENTS_DECOMPOSED) {
            if (*ch == ')') break; //end of op or func

            ch++;
            expr_t *arg = decompose(ch);
            decomposed->args[cur_arg] = arg;
            cur_arg++;
            if (arg == NULL) break;

            char *str = construct_string(arg);
            ch += strlen(str);
            free(str);
        }
    }
    else {      //const or x
        char *name = (char *)calloc(BUF_SIZE, sizeof(char));
        const char *ch = expr;
        while (isdigit(*ch) || *ch == 'x') {
            name[strlen(name)] = *ch;
            ch++;
        }
        decomposed->name = name;
        decomposed->args = NULL;
    }
    return decomposed;
}

const char *diff(const char *expr) {
    expr_t *decomposed = decompose(expr);
    expr_t *derived = common_derivative(decomposed);
    free_expr(decomposed);
    expr_t *simplified = common_simplify(derived);
    free_expr(derived);
    expr_t *extra_simplified = extra_simplify(simplified);
    free(simplified);
    char *str = construct_string(extra_simplified);
    free_expr(extra_simplified);
    return str;
}
