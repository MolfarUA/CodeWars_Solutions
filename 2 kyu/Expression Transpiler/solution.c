#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char *cat (const char *s0, ...);
char *segment (const char *s, const char *e);

typedef struct list {
  struct list *next;
  void *data;
} list;

list *node (void *data);
list *concat (list *l1, list *l2);

char *token, *stream;
enum { Empty, Symbol, Arrow, Name, Number } type;

char *next () {
  char *t = token, *s = stream;
  while (isspace (*s)) s++, stream++;
  if (!*s) { type = Empty; token = s; return t; }
  if (isdigit (*s)) {
    type = Number; while (isdigit (*++s)); 
  } else if (isalpha (*s) || *s=='_') {
    type = Name; while (isalnum (*++s) || *s=='_');
  } else if (*s=='-' && *(s+1)=='>') {
    type = Arrow; s+=2;
  } else
    type = Symbol, ++s;
  token = segment (stream, s); stream = s;
  return t;
}

int lookat (char c) { return Symbol==type && c==*token; }
int symbol (char c) { int ok = lookat (c); if (ok) next (); return ok; }
int arrow () { int ok = Arrow==type; if (ok) next (); return ok; }
char *id () { return Name==type || Number==type ? next () : 0; }

typedef struct {
  list *params;
  list *stats;
} lambda;

typedef struct {
  char *name;
  lambda *l;
} expr;

typedef struct {
  expr *func;
  list *params;
} function;

#define new(type) (calloc (1, sizeof(type)))
#define require(e) if (!(e)) return 0

char *targetLambda (lambda *l) {
  char *p="", *s=p; list *ps = l->params, *ss = l->stats;
  if (ps) for (p = ps->data; (ps=ps->next);) p = cat (p, ",", ps->data, 0);
  for (; ss; ss=ss->next) s = cat (s, ss->data, ";", 0);
  return cat ("(", p, "){", s, "}", 0);
}

char *targetExpr (expr *e) { return e->name ? e->name : targetLambda (e->l); }

char *targetParams (list *ps) {
  char *p; if (!ps) return "";
  for (p = targetExpr (ps->data); (ps=ps->next);) p = cat (p, ",", targetExpr (ps->data), 0);
  return p;
}

char *targetFunction (function *f) { return f ? cat (targetExpr (f->func), "(", targetParams (f->params), ")", 0) : ""; }

list *parseIds (list *l, char sep) {
  char *s = id (); if (!s) return l;
  if (sep) symbol (sep);
  return parseIds (concat (l, node (s)), sep);
}

lambda *parseLambda (lambda *l) {
  require (symbol ('{'));
  if (symbol ('}')) return l;
  char *s; require (s = id());
  l->stats = node (s);
  if (!symbol ('}')) {
    if (arrow ()) {
      l->params = l->stats, l->stats = 0;
    } else if (symbol (',')) {
      require ((l->params = parseIds (l->stats, ',')) && arrow ());
      l->stats = 0;
    }
    l->stats = parseIds (l->stats, 0);
    require (symbol ('}'));
  }
  return l;
}

expr *parseExpr (expr *e) { return (e->name = id ()) || (e->l = parseLambda (new (lambda))) ? e : 0; }

list *parseParams (list *p) {
  expr *e = parseExpr (new (expr));
  require (e);
  p = concat (p, node (e));
  return symbol (',') ? parseParams (p) : p;
}

function *parseFunction (function *f) {
  expr *e = parseExpr (new (expr));
  require (e && type==Symbol);
  f->func = e;
  if (symbol ('(')) {
    if (!lookat (')')) require (f->params = parseParams (0));
    require (symbol (')'));
    if (lookat ('{')) {
      require (e = parseExpr (new (expr)));
      f->params = concat (f->params, node (e));
    }
  } else {
    require (lookat ('{') && (e = parseExpr (new (expr))));
    f->params = node (e);
  }
  return f;
}

char *transpile (const char* expr) {
  stream = (char *)expr; next ();
  function *f = parseFunction (new (function));
  return Empty==type ? targetFunction (f) : "";
}

_____________________________________________________
char *cat (const char *s0, ...);              // cat all strings together, stop at argument value 0
char *segment (const char *s, const char *e); // create string from characters between s (inclusive) and e (exclusive)

typedef struct list {
  struct list *next;
  void *data;
} list;

list *node (void *data);           // create one-element list
list *concat (list *l1, list *l2); // concatenate two lists, modifies l1

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

#define MAX_LEN 100

typedef struct 
{
    char* lambdaP[MAX_LEN];
    char* lambdaS[MAX_LEN];
}lambdaT;

typedef struct 
{
    int type;
  void* pVal;
}paramT;


int GetType(char* s)
{
    char c = *s;
    if (c == ' ')
        return 0;
    if ((c == '_') || ((c >= 'a') && (c <= 'z')) || ((c >= 'A') && (c <= 'Z')))
        return 1;
    if ((c >= '0') && (c <= '9'))
        return 2;
    if (c == '(')
        return 3;
    if (c == '{')
        return 4;
    return -1;
}

int GetName(char* expr, int t, char* rez)
{
    char c;
    int j = 0, i = 0;
    int len = strlen(expr);
    while(j < len)
    {
        c = expr[j];
        if((!((c >= '0') && (c <= '9'))) && (!((c >= 'A') && (c <= 'Z'))) && (!((c >= 'a') && (c <= 'z'))) && (c != '_'))
            break;
        j++;
    }
    memcpy(rez, expr, j);
    rez[j] = 0;
    if (t == 2)
    {
        while(i < j)
        {
            c = expr[i];
            if((c < '0') || (c > '9'))
              return -1;
            i++;
        }
    }
    else
    {
        while(i < j)
        {
            c = expr[i];
            if((!((c >= '0') && (c <= '9'))) && (!((c >= 'A') && (c <= 'Z'))) && (!((c >= 'a') && (c <= 'z'))) && (c != '_'))
                return -1;
            i++;
        }
    }
    return j;
}

int GetLambdaParams(char* expr, int len, char** par, char* refBuf, int* refBufOffset, char sep)
{
    int i = 0, j, k = 0;

    while (i < len)
    {
        if (expr[i] == sep)
        {
            if ((sep != ' ') && (k == 0))
                return -1;
            k = 0;
            i++;
            continue;
        }
        int t = GetType(expr + i);
        switch (t)
        {
            case 0:
                i++; break;
            case 1:
            case 2:
                if (k != 0)
                    return -1;
                k = *refBufOffset;
                j = GetName(expr + i, t, refBuf + k);
                if(j < 0)
                    return -1;
                i += j;
                *(par++) = refBuf + k;
                *par = NULL;
                k += j;
                refBuf[k] = 0;
                *refBufOffset = k+1;
                k = 1;
                break;
            default:
                return -1;
        }
    }
    return i;
}

int GetLambda(char* expr, int len, lambdaT* lamb, char* refBuf, int* refBufOffset)
{
    lamb->lambdaP[0] = (char*)NULL;
    lamb->lambdaS[0] = NULL;
    int j = 0, l;
    char c;
    while((j < len) && ((c = expr[j]) != 0))
    {
        if(c == '}')
            break;
        j++;
    }
    if (c == 0)
        return -1;;
    int k = 1;
    while((k < j) && ((c = expr[k]) != 0))
    {
        if(c == '-')
        {
            if(expr[k+1] == '>')
                break;
        }
        k++;
    }
    if (c == '-')
    {
        l = k;
        while(l > 0)
        {
            if(expr[l-1] == ' ')
                l--;
            else
                break;
        }
        if (l == 1)
          return -1;
  
        if(GetLambdaParams(expr+1, l-1, (char**)(&lamb->lambdaP), refBuf, refBufOffset, ',') < 0)
          return -1;
        k += 2;
    }
    else
        k = 1;
    if(k < j)
    {
        if(GetLambdaParams(expr+k,j-k,(char**)(&lamb->lambdaS),refBuf,refBufOffset, ' ') < 0)
            return -1;
    }
    return j + 1;
}

int GetParams(char* expr, int l, paramT* paramS, lambdaT* lambdas, char* refBuf, int* refBufOffset)
{
    int j = 0;
    char c;
    while((j < l) && ((c = expr[j]) != 0))
    {
        if(c == ')')
            break;
        j++;
    }
    if (j >= l)
        return -1;
    int parOffset = 0;
    int lambOffset = 0;
    int k = 1, l0, l1, state = 0;
    while (k < j)
    {
        if ((state == 1) && (expr[k] == ','))
        {
            state = 2;
            k++;
            continue;
        }
        l0 = GetType(expr + k);
        switch (l0)
        {
            case 0:
                k++; break;
            case 1:
            case 2:
                if (state == 1)
                    return -1;
                l1 = *refBufOffset;
                l0 = GetName(expr+k, l0, refBuf + l1);
                if(l0 < 0)
                    return -1;
                paramS[parOffset].type = 0;
                paramS[parOffset++].pVal = refBuf + l1;
                l1 += l0;
                refBuf[l1] = 0;
                *refBufOffset = l1 + 1;
                state = 1;
                k += l0;
                break;
            case 4:
                if (state == 1)
                    return -1;
                l0 = GetLambda(expr + k, j, &lambdas[lambOffset], refBuf, refBufOffset);
                if(l0 < 0)
                    return -1;
                k += l0;
                paramS[parOffset].type = 1;
                paramS[parOffset++].pVal = &lambdas[lambOffset++];
                    state = 1;
                break;
            default:
                return -1;
        }
    }
    if (state == 2)
        return -1;
    paramS[parOffset].type = -1;
    return j+1;
}

char* PrintLambda(lambdaT *pLambda, char* pBuf)
{
    bool first = true;
    int i = 0;
    *(pBuf++) = '(';
    while(pLambda->lambdaP[i] != NULL)
    {
        if (first)
            first = false;
        else
            *(pBuf++) = ',';
        strcpy(pBuf, pLambda->lambdaP[i++]);
        pBuf += strlen(pBuf);
    }
    strcpy(pBuf, "){");
    while(*pBuf != 0)
        pBuf++;
    i = 0;
    while(pLambda->lambdaS[i] != NULL)
    {
        pBuf += sprintf(pBuf, "%s;" ,pLambda->lambdaS[i]);
        i++;
    }
    *(pBuf++) = '}';
    *(pBuf) = 0;
    return pBuf;
}

char* PrintParams(paramT* paramS, char* pBuf)
{
    bool first = true;
    while(paramS->type >= 0)
    {
        if (first)
            first = false;
        else
            *(pBuf++) = ',';
        if (paramS->type == 0)
            pBuf = strcpy(pBuf, (char*)paramS->pVal);
        else
            pBuf = PrintLambda((lambdaT*)paramS->pVal, pBuf);
        while(*pBuf != 0)
            pBuf++;
        paramS++;
    }
    *pBuf = 0;
    return pBuf;
}


char *transpile (const char* expression)
{
    char lBuf[500], wBuf[500], name[20];
    char c, *pwBuf;
    int i = 0, j, wOffset = 0;
    int len = 0;
    lambdaT lambdas[20];
    paramT paramS[20];
    lambdaT lambda0, lambda1;
    bool l0Is = false, l1Is = false;
    char* rez = malloc(100);
    rez[0] = 0;

    while((c = expression[len]) != 0)
    {
        if(c == '\n')
            c = ' ';
        lBuf[len++] = c;
    }
    lBuf[len] = 0;
    rez[0] = 0;
    if (len == 0)
        return rez;
    name[0] = 0;
    paramS[0].type = -1;
    while (i < len)
    {
        switch (GetType(lBuf + i))
        {
            case 0:
                i++;
                break;
            case 1:
                if (name[0] != 0)
                    return "";
                j = GetName(lBuf+i, 1, name);
                if(j < 0)
                  return rez;
                i += j;
                break;
            case 2:
                if (name[0] != 0)
                    return rez;
                j = GetName(lBuf+i, 2, name);
                if(j < 0)
                  return rez;
                i += j;
                break;
            case 3:
                j = GetParams(lBuf+i, len-i, paramS, lambdas, wBuf, &wOffset);
                if(j < 0)
                  return rez;
                i += j;
                break;
            case 4:
                if (!l0Is)
                {
                    j = GetLambda(lBuf + i, len - i, &lambda0, wBuf, &wOffset);
                    if(j < 0)
                        return rez;
                    i += j;
                    l0Is = true;
                }
                else
                {
                    if (!l1Is)
                    {
                        j = GetLambda(lBuf + i, len - i, &lambda1, wBuf, &wOffset);
                        if(j < 0)
                            return rez;
                        i += j;
                        l1Is = true;
                    }
                    else
                        return rez;
                }
                break;
      default:
        return rez;
        break;
        }
    if(i < 0)
      return rez;
    }
    if (name[0] != 0)
    {
        if (!l0Is)
        {
          PrintParams(paramS, lBuf);
          sprintf(rez, "%s(%s)", name, lBuf);
        }
        else
        {
            pwBuf = PrintParams(paramS, lBuf);
            if(pwBuf != lBuf)
                *(pwBuf)++ = ',';
            PrintLambda(&lambda0, pwBuf);
            sprintf(rez, "%s(%s)", name, lBuf);
        }
    }
    else
    {
        if (!l1Is)
        {
            if (!l0Is)
                return "";
            pwBuf = PrintLambda(&lambda0, rez);
            *(pwBuf++) = '(';
            pwBuf = PrintParams(paramS, pwBuf);
            *(pwBuf++) = ')';
            *(pwBuf) = 0;
        }
        else
        {
            pwBuf = PrintLambda(&lambda0, rez);
            *(pwBuf++) = '(';
            pwBuf = PrintParams(paramS, pwBuf);
            if (*(pwBuf-1) != '(')
                *(pwBuf++) += ',';
            pwBuf = PrintLambda(&lambda1, pwBuf);
            *(pwBuf++) = ')';
            *(pwBuf) = 0;
        }
    }
    return rez;
}
_____________________________________________________
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char *cat (const char *s0, ...);
char *segment (const char *s, const char *e);

typedef struct list {
  struct list *next;
  void *data;
} list;

list *node (void *data);
list *concat (list *l1, list *l2);

char *token, *stream;
enum { Empty, Symbol, Arrow, Name, Number } type;

char *next () {
  char *t = token, *s = stream;
  while (isspace (*s)) s++, stream++;
  if (!*s) { type = Empty; token = s; return t; }
  if (isdigit (*s)) {
    type = Number; while (isdigit (*++s)); 
  } else if (isalpha (*s) || *s=='_') {
    type = Name; while (isalnum (*++s) || *s=='_');
  } else if (*s=='-' && *(s+1)=='>') {
    type = Arrow; s+=2;
  } else
    type = Symbol, ++s;
  token = segment (stream, s); stream = s;
  return t;
}

int lookat (char c) { return Symbol==type && c==*token; }
int symbol (char c) { int ok = lookat (c); if (ok) next (); return ok; }
int arrow () { int ok = Arrow==type; if (ok) next (); return ok; }
char *id () { return Name==type || Number==type ? next () : 0; }

typedef struct {
  list *params;
  list *stats;
} lambda;

typedef struct {
  char *name;
  lambda *l;
} expr;

typedef struct {
  expr *func;
  list *params;
} function;

#define new(type) (calloc (1, sizeof(type)))
#define require(e) if (!(e)) return 0

char *targetLambda (lambda *l) {
  char *p="", *s=p; list *ps = l->params, *ss = l->stats;
  if (ps) for (p = ps->data; ps=ps->next;) p = cat (p, ",", ps->data, 0);
  for (; ss; ss=ss->next) s = cat (s, ss->data, ";", 0);
  return cat ("(", p, "){", s, "}", 0);
}

char *targetExpr (expr *e) { return e->name ? e->name : targetLambda (e->l); }

char *targetParams (list *ps) {
  char *p; if (!ps) return "";
  for (p = targetExpr (ps->data); ps=ps->next;) p = cat (p, ",", targetExpr (ps->data), 0);
  return p;
}

char *targetFunction (function *f) { return f ? cat (targetExpr (f->func), "(", targetParams (f->params), ")", 0) : ""; }

list *parseIds (list *l, char sep) {
  char *s = id (); if (!s) return l;
  if (sep) symbol (sep);
  return parseIds (concat (l, node (s)), sep);
}

lambda *parseLambda (lambda *l) {
  require (symbol ('{'));
  if (symbol ('}')) return l;
  char *s; require (s = id());
  l->stats = node (s);
  if (!symbol ('}')) {
    if (arrow ()) {
      l->params = l->stats, l->stats = 0;
    } else if (symbol (',')) {
      require ((l->params = parseIds (l->stats, ',')) && arrow ());
      l->stats = 0;
    }
    l->stats = parseIds (l->stats, 0);
    require (symbol ('}'));
  }
  return l;
}

expr *parseExpr (expr *e) { return (e->name = id ()) || (e->l = parseLambda (new (lambda))) ? e : 0; }

list *parseParams (list *p) {
  expr *e = parseExpr (new (expr));
  require (e);
  p = concat (p, node (e));
  return symbol (',') ? parseParams (p) : p;
}

function *parseFunction (function *f) {
  expr *e = parseExpr (new (expr));
  require (e && type==Symbol);
  f->func = e;
  if (symbol ('(')) {
    if (!lookat (')')) require (f->params = parseParams (0));
    require (symbol (')'));
    if (lookat ('{')) {
      require (e = parseExpr (new (expr)));
      f->params = concat (f->params, node (e));
    }
  } else {
    require (lookat ('{') && (e = parseExpr (new (expr))));
    f->params = node (e);
  }
  return f;
}

char *transpile (const char* expr) {
  stream = expr; next ();
  function *f = parseFunction (new (function));
  return Empty==type ? targetFunction (f) : "";
}

_____________________________________________________
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char *cat (const char *s0, ...);
char *segment (const char *s, const char *e);

typedef struct list {
  struct list *next;
  void *data;
} list;

list *node (void *data);
list *concat (list *l1, list *l2);

char *token, *stream;
enum { Empty, Symbol, Arrow, Name, Number } type;

char *next () {
  char *t = token, *s = stream;
  while (isspace (*s)) s++, stream++;
  if (!*s) { type = Empty; token = s; return t; }
  if (isdigit (*s)) {
    type = Number; while (isdigit (*++s)); 
  } else if (isalpha (*s) || *s=='_') {
    type = Name; while (isalnum (*++s) || *s=='_');
  } else if (*s=='-' && *(s+1)=='>') {
    type = Arrow; s+=2;
  } else
    type = Symbol, ++s;
  token = segment (stream, s); stream = s;
  return t;
}

int lookat (char c) { return Symbol==type && c==*token; }
int symbol (char c) { int ok = lookat (c); if (ok) next (); return ok; }
int arrow () { int ok = Arrow==type; if (ok) next (); return ok; }
char *id () { return type == Name || type == Number ? next () : 0; }

typedef struct {
  list *params;
  list *stats;
} lambda;

typedef struct {
  char *name;
  lambda *l;
} expr;

typedef struct {
  expr *func;
  list *params;
} function;

#define new(type) (calloc (1, sizeof(type)))
#define require(e) if (!(e)) return 0

char *targetLambda (lambda *l) {
  char *p="", *s=p; list *ps = l->params, *ss = l->stats;
  if (ps) for (p = ps->data; ps=ps->next;) p = cat (p, ",", ps->data, 0);
  for (; ss; ss=ss->next) s = cat (s, ss->data, ";", 0);
  return cat ("(", p, "){", s, "}", 0);
}

char *targetExpr (expr *e) {
  if (e->name) return e->name;
  return targetLambda (e->l);
}

char *targetParams (list *ps) {
  char *p; if (!ps) return "";
  for (p = targetExpr (ps->data); ps=ps->next;) p = cat (p, ",", targetExpr (ps->data), 0);
  return p;
}

char *targetFunction (function *f) {
  if (!f) return "";
  return cat (targetExpr (f->func), "(", targetParams (f->params), ")", 0);
}

list *parseIds (list *l, char sep) {
  char *s = id ();
  if (!s) return l;
  l = concat (l, node (s));
  if (sep) symbol (sep);
  return parseIds (l, sep);
}

lambda *parseLambda () {
  require (symbol ('{'));
  lambda *l = new (lambda); char *s;
  if (symbol ('}')) return l;
  require (s = id());
  l->stats = node (s);
  if (!symbol ('}')) {
    if (arrow ()) {
      l->params = l->stats, l->stats = 0;
    } else if (symbol (',')) {
      require ((l->params = parseIds (l->stats, ',')) && arrow ());
      l->stats = 0;
    }
    l->stats = parseIds (l->stats, 0);
    require (symbol ('}'));
  }
  return l;
}

expr *parseExpr () {
  expr *e = new (expr);
  !(e->name = id ()) && !(e->l = parseLambda ()) && (e = 0);
  return e;
}

list *parseParams (list *p) {
  expr *e = parseExpr ();
  require (e);
  p = concat (p, node (e));
  return symbol (',') ? parseParams (p) : p;
}

function *parseFunction () {
  expr *e = parseExpr ();
  require (e && type==Symbol);
  function *f = new (function); f->func = e;
  if (symbol ('(')) {
    list *p = 0;
    if (!lookat (')')) require (p = parseParams (0));
    require (symbol (')'));
    if (lookat ('{')) {
      require (e = parseExpr ());
      p = concat (p, node (e));
    }
    f->params = p;
  } else {
    require (lookat ('{') && (e = parseExpr ()));
    f->params = node (e);
  }
  return f;
}

char *transpile (const char* expr) {
  stream = expr; next ();
  function *f = parseFunction ();
  if (type!=Empty) return "";
  return targetFunction (f);
}
