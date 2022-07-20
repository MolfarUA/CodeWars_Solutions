5470c635304c127cad000f0d


typedef struct RegExp RegExp;

RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* or (RegExp *left, RegExp *right);
RegExp* str (RegExp *first);
RegExp* add (RegExp *str, RegExp *next);


RegExp *parseRegExp (char *input);
RegExp *parse_or(char *input, int *i);
RegExp *parse_str(char *input, int *i);
RegExp *parse_zero_or_more(char *input, int *i);
RegExp *parse_group(char *input, int *i);
RegExp *parse_any(char *input, int *i);
RegExp *parse_normal(char *input, int *i);


RegExp *parseRegExp (char *input) {
  int i = 0;
  RegExp *ast = parse_or(input, &i);
  if (i != strlen(input)) return 0;
  return ast;
}

RegExp *parse_or(char *input, int *i) {
  RegExp *next = parse_str(input, i);
  if (input[*i] == '|') {
    (*i)++;
    return or(next, parse_str(input, i));
  } else {
    return next;
  }
};

RegExp *parse_str(char *input, int *i) {
  RegExp *r = parse_zero_or_more(input, i);
  RegExp *n = parse_zero_or_more(input, i);
  if (n) {
    r = str(r);
    add(r, n);
    while ( n = parse_zero_or_more(input, i) ) add(r, n);
  }
  return r;
};


RegExp *parse_zero_or_more(char *input, int *i) {
  RegExp *next = parse_group(input, i);
  if (next && input[*i] == '*') {
    (*i)++;
    return zeroOrMore(next);
  }
  return next;
};


RegExp *parse_group(char *input, int *i) {
  if (input[*i] == '(') {
    (*i)++;
    RegExp *next = parse_or(input, i);
    if (input[*i] != ')') return 0;
    (*i)++;
    return next;
  } else {
    return parse_any(input, i);
  }
};

RegExp *parse_any(char *input, int *i) {
  return input[*i] == '.' ? ((*i)++, any()) : parse_normal(input, i);
}

RegExp *parse_normal(char *input, int *i) {
  switch (input[*i]) {
    case '*':
    case '|':
    case '(':
    case ')':
    case '\0':
      return 0;
    default:
      return normal(input[(*i)++]);
  }
}
____________________________________________________________
typedef struct RegExp RegExp;

RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* or (RegExp *left, RegExp *right);
RegExp* str (RegExp *first);
RegExp* add (RegExp *str, RegExp *next);

typedef struct state { char *s; void *r; } state;

state  oneOf (char *input, char *s) { return *input &&  strchr (s, *input) ? (state) {input+1, (void*)*input } : (state) {input}; }
state noneOf (char *input, char *s) { return *input && !strchr (s, *input) ? (state) {input+1, (void*)*input } : (state) {input}; }
state parseExpr (char *input); state parseSeq (char *input);
state parseNormal (char *input) { state s = noneOf (input, "()*|."); if (s.r) s.r = normal (*input); return s; }
state parseAny  (char *input) { state s = oneOf (input, "."); if (s.r) s.r = any (); return s; }
state parseMany (char *input) { state a,s = parseExpr (input); if (s.r) a = oneOf (s.s, "*"); return s.r && a.r ? (state){a.s, zeroOrMore (s.r)} : s; }
state parseOr (char *input) { state a,s = parseSeq (input); return (a = oneOf (s.s, "|")).r ? a = parseSeq (a.s), (state){a.s, or (s.r, a.r)} : s; }
RegExp *parseRegExp (char *input) { state s = parseOr (input); return *s.s ? 0 : s.r; }

state parseExpr (char *input) {
  RegExp *r; state s = parseNormal (input);
  if (!s.r) s = parseAny (s.s);
  if (!s.r) { s = oneOf (s.s, "("); if (s.r) s = parseOr (s.s); if (r=s.r) s = oneOf (s.s, ")"); s.r = s.r ? r : 0; }
  return s;
}

state parseSeq (char *input) {
  state s = parseMany (input), a = parseMany (s.s); RegExp *r = str (s.r);
  if (a.r) { while (a.r) { add (r, a.r); a = parseMany (a.s); } s = (state) {a.s, r}; }
  return s;
}
____________________________________________________________
#include <stdbool.h>
#include <stdlib.h>

typedef struct RegExp RegExp;

RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* or (RegExp *left, RegExp *right);
RegExp* str (RegExp *first);
RegExp* add (RegExp *str, RegExp *next);

// Grammar:
//
//   RE       -> Term RETail
//   RETail   -> "|" Term | empty
//   Term     -> Factor TermTail
//   TermTail -> Term | empty
//   Factor   -> Item Stars
//   Item     -> atom | "(" RE ")"    atom is either a "normal" character or ".".
//   Stars    -> "*" | empty
//
// First sets:
//
//   RE       : atom, "("
//   RETail   : "|", empty
//   Term     : atom, "("
//   TermTail : atom, "(", empty
//   Factor   : atom, "("
//   Item     : atom, "("
//   Stars    : "*", empty
//
// Follow sets:
//
//   RE       : ")", empty
//   RETail   : ")", empty
//   Term     : ")", "|", empty
//   TermTail : ")", "|", empty
//   Factor   : atom, "(", ")", "|", empty
//   Item     : atom, "(", ")", "*", "|", empty
//   Stars    : atom, "(", ")", "|", empty
//
// Predict sets:
//
//   RE       -> Term RETail     : atom, "("
//   RETail   -> "|" Term        : "|"
//   RETail   -> empty           : ")", empty
//   Term     -> Factor TermTail : atom, "("
//   TermTail -> Term            : atom, "("
//   TermTail -> empty           : ")", "|", empty
//   Factor   -> Item Stars      : atom, "("
//   Item     -> atom            : atom
//   Item     -> "(" RE ")"      : "("
//   Stars    -> "*" Stars       : "*"
//   Stars    -> empty           : atom, "(", ")", "|", empty

static RegExp *parseRE(const char **input);
static RegExp *parseRETail(const char **input, RegExp *head);
static RegExp *parseTerm(const char **input);
static RegExp *parseTermTail(const char **input, RegExp *term, bool first);
static RegExp *parseFactor(const char **input);
static RegExp *parseItem(const char **input);
static RegExp *parseStars(const char **input, RegExp *item);

RegExp *parseRE(const char **const input) {
  switch (**input) {
  case ')':
  case '*':
  case '|':
  case '\0':
    // Syntax error.
    return NULL;
  
  default: { // atom, "("
    // RE -> Term RETail
    
    RegExp *const ast = parseTerm(input);
    if (!ast) return NULL;
    
    return parseRETail(input, ast);
  }
  }
}

RegExp *parseRETail(const char **const input, RegExp *const head) {
  switch (**input) {
  case '|':
    // RETail -> "|" Term
    
    (*input)++;
    
    RegExp *const ast = parseTerm(input);
    if (!ast) return NULL;
      
    return or(head, ast);
      
  case ')':
  case '\0':
    // RETail -> empty
    return head;
      
  default:
    // Syntax error.
    return NULL;
  }
}

RegExp *parseTermAux(const char **const input, RegExp *const term, const bool first) {
  switch (**input) {
  case ')':
  case '*':
  case '|':
  case '\0':
    // Syntax error.
    return NULL;
      
  default: { // atom, "("
    // Term -> Factor TermTail
    
    RegExp *const ast = parseFactor(input);
    if (!ast) return NULL;
    
    return parseTermTail(input, term ? add(term, ast) : ast, first);
  }
  }
}

RegExp *parseTerm(const char **const input) {
  return parseTermAux(input, NULL, true);
}

RegExp *parseTermTail(const char **const input, RegExp *const term, const bool first) {
  switch (**input) {
  case ')':
  case '|':
  case '\0':
    // TermTail -> empty
    return term;
  
  case '*':
    // Syntax error.
    return NULL;
  
  default: // atom, "("
    // TermTail -> Term
    return parseTermAux(input, first ? str(term) : term, false);
  }
}

RegExp *parseFactor(const char **const input) {
  switch (**input) {
  case ')':
  case '*':
  case '|':
  case '\0':
    // Syntax error.
    return NULL;
      
  default: { // atom, "("
    // Factor -> Item Stars
    
    RegExp *const ast = parseItem(input);
    if (!ast) return NULL;
    
    return parseStars(input, ast);
  }
  }
}

RegExp *parseItem(const char **const input) {
  switch (**input) {
  case '(':
    // Item -> "(" RE ")"
    
    (*input)++;
      
    RegExp *const ast = parseRE(input);
    if (!ast) return NULL;
      
    if (*(*input)++ != ')') return NULL;
    
    return ast;
  
  case ')':
  case '*':
  case '|':
  case '\0':
    // Syntax error.
    return NULL;
      
  case '.': // atom
    // Item -> atom
    (*input)++;
    return any();
      
  default: // atom
    // Item -> atom
    return normal(*(*input)++);
  }
}

RegExp *parseStars(const char **const input, RegExp *const item) {
  if (**input == '*') {
    // Stars -> "*"
    (*input)++;
    return zeroOrMore(item);
  } else {
    // Stars -> empty
    return item;
  }
}

RegExp *parseRegExp (char *input) {
  RegExp *const ast = parseRE((const char **)&input);
  return *input == '\0' ? ast : NULL;
}
____________________________________________________________
#include <stdlib.h>
#include <stdbool.h>

typedef struct RegExp RegExp;

RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* or (RegExp *left, RegExp *right);
RegExp* str (RegExp *first);
RegExp* add (RegExp *str, RegExp *next);

typedef struct {
  char *input;
} state;

static RegExp *parse(state *s, bool canOr);

RegExp *parseRegExp (char *input) {
  state s;
  s.input = input;
  RegExp *result = parse(&s, true);
  return result;
}

static RegExp *parse(state *s, bool canOr) {
  RegExp *l0 = NULL, *l1 = NULL, *right;
  bool wasStar = false;
  for (;;) {
    if (*s->input == ')')
      break;
    char c = *s->input++;
    if (c == 0)
      break;

    if (c == '*') {
      if (l1 == NULL) return NULL;
      if (wasStar) return NULL;
      l1 = zeroOrMore(l1);
      wasStar = true;
      continue;
    }
    wasStar = false;
    
    if (c == '|') {
      if (!canOr)
        return NULL;

      if (l0)
        l1 = add(l0, l1);
      else if (!l1)
        return NULL;

      right = parse(s, false);
      if (!right)
        return NULL;

      return or(l1, right);
    }

    if (c == '.')
      right = any();
    else if (c == '(') {
      right = parse(s, true);
      if (!right || *s->input++ != ')')
        return NULL;
    } else {
      right = normal(c);
    }

    if (l0)
      l0 = add(l0, l1);
    else if (l1)
      l0 = str(l1);
    l1 = right;
  }

  if (l0)
    return add(l0, l1);
  else
    return l1;
}
____________________________________________________________
#include <stdint.h>
#include <string.h>

typedef struct RegExp RegExp;

RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* or (RegExp *left, RegExp *right);
RegExp* str (RegExp *first);
RegExp* add (RegExp *str, RegExp *next);

typedef struct state { char *s; void *r; } state;

state  oneOf (char *input, char *s) { return *input &&  strchr (s, *input) ? (state) {input+1, (void*)(uintptr_t)*input } : (state) {input, NULL}; }
state noneOf (char *input, char *s) { return *input && !strchr (s, *input) ? (state) {input+1, (void*)(uintptr_t)*input } : (state) {input, NULL}; }
state parseExpr (char *input); state parseSeq (char *input);
state parseNormal (char *input) { state s = noneOf (input, "()*|."); if (s.r) s.r = normal (*input); return s; }
state parseAny  (char *input) { state s = oneOf (input, "."); if (s.r) s.r = any (); return s; }
state parseMany (char *input) { state a,s = parseExpr (input); if (s.r) a = oneOf (s.s, "*"); return s.r && a.r ? (state){a.s, zeroOrMore (s.r)} : s; }
state parseOr (char *input) { state a,s = parseSeq (input); return (a = oneOf (s.s, "|")).r ? a = parseSeq (a.s), (state){a.s, or (s.r, a.r)} : s; }
RegExp *parseRegExp (char *input) { state s = parseOr (input); return *s.s ? 0 : s.r; }

state parseExpr (char *input) {
  RegExp *r; state s = parseNormal (input);
  if (!s.r) s = parseAny (s.s);
  if (!s.r) { s = oneOf (s.s, "("); if (s.r) s = parseOr (s.s); if ((r=s.r)) s = oneOf (s.s, ")"); s.r = s.r ? r : 0; }
  return s;
}

state parseSeq (char *input) {
  state s = parseMany (input), a = parseMany (s.s); RegExp *r = str (s.r);
  if (a.r) { while (a.r) { add (r, a.r); a = parseMany (a.s); } s = (state) {a.s, r}; }
  return s;
}
