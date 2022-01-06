struct RegExp;

RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* orr (RegExp *left, RegExp *right);
RegExp* str (RegExp *first);
RegExp* add (RegExp *str, RegExp *next);

struct state { const char *s; RegExp *r; };



state  oneOf (const char *input, const char *s) {
    if(*input && strchr(s,*input))
        return (state) {input+1, (RegExp*)256 };
    else
    return (state) {input, NULL };
}

state noneOf (const char *input, const char *s) {
     if(*input && !strchr(s,*input))
        return (state) {input+1, (RegExp*)256 };
    else
        return (state) {input, NULL };
}

state parseExpr (const char *input);
state parseSeq (const char *input);
state parseNormal (const char *input) {
    
    state s = noneOf (input, "()*|.");
    if (s.r)
        s.r = normal (*input);
    return s;
}

state parseAny  (const char *input) {
    state s = oneOf (input, ".");
    if (s.r)
        s.r = any ();
    return s;
}

state parseMany (const char *input) {
    state a, s = parseExpr (input);
    if (s.r)
        a = oneOf (s.s, "*");
    if( s.r && a.r )
        return (state){a.s, zeroOrMore (s.r)};
    else
        return s;

}

state parseOr (const char *input) {
    state a,s = parseSeq (input);
    a = oneOf (s.s, "|");
    if (a.r) {
        a = parseSeq (a.s);
        return (state) {a.s, orr (s.r, a.r)};
    }
    else 
      return s;

}
RegExp *parseRegExp (const char *input) {
    state s = parseOr (input);
    if(*s.s)
        return 0;
    else
        return s.r;

}

state parseExpr (const char *input) {
  RegExp *r; state s = parseNormal (input);
  if (!s.r)
    s = parseAny (s.s);
  if (!s.r) { 
    s = oneOf (s.s, "("); 
    if (s.r) 
      s = parseOr (s.s);
    if (r=s.r) 
      s = oneOf (s.s, ")"); 
    s.r = s.r ? r : 0;
  }
  return s;
}

state parseSeq (const char *input) {
  state s = parseMany (input), a = parseMany (s.s); 
  RegExp *r = str (s.r);
  if (a.r) { 
    while (a.r) { 
      add (r, a.r); 
      a = parseMany (a.s); 
    } 
    s = (state) {a.s, r}; 
  }
  return s;
}
____________________________________________________________
struct RegExp;

RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* orr (RegExp *left, RegExp *right);
RegExp* str (RegExp *first);
RegExp* add (RegExp *str, RegExp *next);

struct state { const char *s; RegExp *r; };

state  oneOf (const char *input, const char *s) { return *input &&  strchr (s, *input) ? (state) {input+1, (RegExp*)256 } : (state) {input}; }
state noneOf (const char *input, const char *s) { return *input && !strchr (s, *input) ? (state) {input+1, (RegExp*)256 } : (state) {input}; }
state parseExpr (const char *input); state parseSeq (const char *input);
state parseNormal (const char *input) { state s = noneOf (input, "()*|."); if (s.r) s.r = normal (*input); return s; }
state parseAny  (const char *input) { state s = oneOf (input, "."); if (s.r) s.r = any (); return s; }
state parseMany (const char *input) { state a,s = parseExpr (input); if (s.r) a = oneOf (s.s, "*"); return s.r && a.r ? (state){a.s, zeroOrMore (s.r)} : s; }
state parseOr (const char *input) { state a,s = parseSeq (input); return (a = oneOf (s.s, "|")).r ? a = parseSeq (a.s), (state){a.s, orr (s.r, a.r)} : s; }
RegExp *parseRegExp (const char *input) { state s = parseOr (input); return *s.s ? 0 : s.r; }

state parseExpr (const char *input) {
  RegExp *r; state s = parseNormal (input);
  if (!s.r) s = parseAny (s.s);
  if (!s.r) { s = oneOf (s.s, "("); if (s.r) s = parseOr (s.s); if (r=s.r) s = oneOf (s.s, ")"); s.r = s.r ? r : 0; }
  return s;
}

state parseSeq (const char *input) {
  state s = parseMany (input), a = parseMany (s.s); RegExp *r = str (s.r);
  if (a.r) { while (a.r) { add (r, a.r); a = parseMany (a.s); } s = (state) {a.s, r}; }
  return s;
}
____________________________________________________________
struct RegExp;

RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* orr (RegExp *left, RegExp *right);
RegExp* str (RegExp *first);
RegExp* add (RegExp *str, RegExp *next);

RegExp *parse_single(const char * &input);
RegExp *parse_star(const char * &input);
RegExp *parse_sequence(const char * &input);
RegExp *parse_or(const char * &input);

RegExp *parse_single(const char * &input) {
  switch(*input) {
      case '.':
          input++;
          return any();
      case '(': 
      {
          input++;
          auto res = parse_or(input);
          if (*input != ')') {
            throw input;
          } else {
            input ++;
          }
          return res;
      }
      case ')':
      case '|':
      case '*': 
      case '\0':
          throw input;
      default:
          return normal(*input++);
  }
}


RegExp *parse_star(const char * &input) {
  // note that a** is not allowed
  auto res = parse_single(input);
  if (*input == '*') { 
    res = zeroOrMore(res);
    input ++;
  }
  return res;
}

RegExp *parse_sequence(const char * &input) {
  auto res = parse_star(input);
  if (!*input || *input == '|' || *input == ')') {
    // not a sequence, such a single element
    return res;
  }
  // make it a sequence and parse more
  res = str(res);
  while (*input && *input != '|' && *input != ')') {
    res = add(res, parse_star(input));
  }
  return res;
}

RegExp *parse_or(const char * &input) {
  auto res = parse_sequence(input);
  if (*input == '|') {
    input += 1;
    return orr(res, parse_sequence(input));
  } else {
    return res;
  }
}

RegExp *parseRegExp (const char *input) {
  const char * original = input;
  try {
      return parse_or(input);
  } catch (const char *pos) {
    // std::cerr << "Unexpected character in regex at position " << (pos - original) << "\n";
    return nullptr;
  }
}
____________________________________________________________
#include <numeric>
#include <unordered_set>

struct RegExp;

/// This is definetly not C++
RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* orr (RegExp *left, RegExp *right);
RegExp* str (RegExp *first);
RegExp* add (RegExp *str, RegExp *next);

/// I need it ;)
char *pretty (RegExp *r);

std::string close_brace(const char *start_brace) {
//     std::cout << "Searching close brace from: " << start_brace << std::endl;
    auto end = start_brace;
    auto counter = 0u;
    /// Searching close brace
    while (*end++ != 0 && (*end != ')' || counter)) {
      if (*end == '(')
        ++counter;
      else if (*end == ')')
        --counter;
    }
    
    return std::string{++start_brace, end};
}

using concat_t = std::function<RegExp*(RegExp*,RegExp*)>;

struct block_t {
  block_t(RegExp *_rex, bool _simple = false):
    rex(std::make_optional(_rex)),
    simple(_simple)
  {}
  
  block_t(concat_t _op, bool _orr = false):
    op(std::make_optional(_op)),
    orr(_orr)
  {}
  
  std::optional<RegExp*> rex;
  std::optional<concat_t> op;
  bool simple = false;
  bool orr = false;
};

RegExp *accumulate(std::vector<block_t>::iterator begin, std::vector<block_t>::iterator end) {
  if (begin == end)
    return nullptr;
  
  /// Accumulating all objects on level
  concat_t op = add;
  std::string op_sym = "?";
  return std::accumulate(std::next(begin), end, begin->rex.value(), [&](RegExp *acc, block_t &block){
    if (block.op.has_value()) {
      op = block.op.value();
      op_sym = block.orr ? " | " : " + ";
      return acc;
    }
    
    std::cout << "acc: " << pretty(acc) << op_sym << pretty(block.rex.value()) << std::endl;
    return op(acc, block.rex.value());
  });
}

void sequenize(std::vector<block_t> &blocks) {
  auto iblock = blocks.begin();
  
  do {
    if (!iblock->simple) {
      continue;
    }
    
    const auto iend = std::find_if(iblock, blocks.end(), [](const block_t &block){
      return (block.orr) || (!block.op.has_value() && !block.simple);
    });
    
    const auto block_size = std::distance(iblock, iend);    
    std::cout << "Block (" << pretty(iblock->rex.value()) <<  ")" 
              << "["
                << (iblock->simple ? "s" : "")
                << (iblock->orr ? "o" : "")
              << "]" 
              <<" size: " << block_size << std::endl;
    
    if (block_size < 3)
      continue;
    
    iblock->rex = str(iblock->rex.value());
    iblock->rex = accumulate(iblock, iend);
    iblock = std::prev(blocks.erase(std::next(iblock), iend));
    
  } while (++iblock != blocks.end());
}

bool validate_braces(const char *input) {
  int level = 0;
  
  do {
    if (*input == '(')
      ++level;
    else if (*input == ')') {
      --level;
    }
    
    if (level < 0) {
      std::cout << "invalid: < 0" << std::endl;
      return false;
    }
  } while(*++input);
  
  return level == 0;
}

bool validate_stars(const char *input) {
  bool star = false;
  do {
    if (*input == '*') {
      if (!star)
        star = true;
      else
        return false;
    } else
      star = false;
  } while(*++input);
  
  return true;
}

RegExp *parseRegExp (const char *input) {
  std::cout << std::endl << ">>> " << input << std::endl;
  std::cout << "__________" << std::endl;
  
  if (!validate_stars(input))
    return nullptr;
  
  if (!validate_braces(input))
    return nullptr;
  
  std::vector<block_t> expressions;
  
  auto add_op = [&expressions]() {
    if (!expressions.empty() && !expressions.back().op.has_value())
      expressions.push_back({add});
  };
  
  auto *c = input;
  do {
    std::cout << "sym: \"" << *c << "\"" << std::endl;
    switch (*c) {
    case ')':
        return nullptr;
    case '(': 
        {
          const std::string block = close_brace(c);
          add_op();
          auto *rex = parseRegExp(block.c_str());
          std::cout << "group: " << block << std::endl;
          expressions.push_back({rex, true});
          c += block.size() + 1u;
        }
        break;
    case '.':
        add_op();
        expressions.push_back({any(), true});
        break;
    case '|':
        expressions.push_back({orr, true});
        break;
    case '*':
        if (expressions.empty() || expressions.back().op.has_value())
          return nullptr;
        expressions.back().rex = zeroOrMore(expressions.back().rex.value());
        break;
    default:
        if (*c != '\0') {
          auto *n = normal(*c);
          add_op();
          expressions.push_back({n, true});
        }
        break;
    }
    
  } while(*c++ != 0);
  
  if (expressions.empty())
    return nullptr;
  else if (expressions.size() == 1)
    return expressions.front().rex.value();
  
  /// Modifying char sequences
  sequenize(expressions);
  
  std::cout << "Accumulating: " << expressions.size() << std::endl;  
  return accumulate(expressions.begin(), expressions.end());
}
____________________________________________________________
struct RegExp;

RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* orr (RegExp *left, RegExp *right);
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
    return nullptr;
  
  default: { // atom, "("
    // RE -> Term RETail
    
    RegExp *const ast = parseTerm(input);
    if (!ast) return nullptr;
    
    return parseRETail(input, ast);
  }
  }
}

RegExp *parseRETail(const char **const input, RegExp *const head) {
  switch (**input) {
  case '|': {
    // RETail -> "|" Term
    
    (*input)++;
    
    RegExp *const ast = parseTerm(input);
    if (!ast) return nullptr;
      
    return orr(head, ast);
  }
      
  case ')':
  case '\0':
    // RETail -> empty
    return head;
      
  default:
    // Syntax error.
    return nullptr;
  }
}

RegExp *parseTermAux(const char **const input, RegExp *const term, const bool first) {
  switch (**input) {
  case ')':
  case '*':
  case '|':
  case '\0':
    // Syntax error.
    return nullptr;
      
  default: { // atom, "("
    // Term -> Factor TermTail
    
    RegExp *const ast = parseFactor(input);
    if (!ast) return nullptr;
    
    return parseTermTail(input, term ? add(term, ast) : ast, first);
  }
  }
}

RegExp *parseTerm(const char **const input) {
  return parseTermAux(input, nullptr, true);
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
    return nullptr;
  
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
    return nullptr;
      
  default: { // atom, "("
    // Factor -> Item Stars
    
    RegExp *const ast = parseItem(input);
    if (!ast) return nullptr;
    
    return parseStars(input, ast);
  }
  }
}

RegExp *parseItem(const char **const input) {
  switch (**input) {
  case '(': {
    // Item -> "(" RE ")"
    
    (*input)++;
      
    RegExp *const ast = parseRE(input);
    if (!ast) return nullptr;
      
    if (*(*input)++ != ')') return nullptr;
    
    return ast;
  }
  
  case ')':
  case '*':
  case '|':
  case '\0':
    // Syntax error.
    return nullptr;
      
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

RegExp *parseRegExp (const char *input) {
  RegExp *const ast = parseRE((const char **)&input);
  return *input == '\0' ? ast : nullptr;
}
____________________________________________________________
struct RegExp;

RegExp* any ();
RegExp* normal (char c);
RegExp* zeroOrMore (RegExp *starred);
RegExp* orr (RegExp *left, RegExp *right);
RegExp* str (RegExp *first);
RegExp* add (RegExp *str, RegExp *next);

RegExp *parseVector(std::vector<RegExp *> &st)
{  
  RegExp *r = !st.empty() ? st[0] : NULL;
  if (st.size() >= 2)
  {
    r = str(r);
    for (size_t i = 1; i < st.size(); i++)
      r = add(r, st[i]);
  }

  st.clear();
  return r;
}

RegExp *parseRegExp (std::string input)
{
  std::vector<RegExp *> st;
  for (size_t i = 0; i < input.length(); i++)
  {
    if (input[i] == '(')
    {
      size_t found = std::string::npos;
      for (size_t j = i + 1, p = 1; j < input.length(); j++)
      {
        if (input[j] == '(')
          p++;
        else if (input[j] == ')')
        {
          if (--p == 0)
          {
            found = j;
            break;
          }
        }
      }
      if (found == std::string::npos)
        return NULL;
      RegExp *r = parseRegExp(input.substr(i + 1, found - i - 1));
      if (r == NULL)
        return NULL;
      st.push_back(r);
      i = found;
    }
    else if (input[i] == '|')
    {
      RegExp *r1 = parseVector(st);
      if (r1 == NULL)
        return NULL;
      RegExp *r2 = parseRegExp(input.substr(i + 1));
      if (r2 == NULL)
        return NULL;
      return orr(r1, r2);
    }
    else if (input[i] == ')')
    {
      return NULL;
    }
    else if (input[i] == '*')
    {
      if (st.empty())
        return NULL;
      if (i > 0 && input[i - 1] == '*')
        return NULL;
      RegExp *r = st.back(); st.pop_back();
      st.push_back(zeroOrMore(r));
    }
    else if (input[i] == '.')
    {
      st.push_back(any());
    }
    else
    {
      st.push_back(normal(input[i]));
    }
  }
  return parseVector(st);
}

RegExp *parseRegExp (const char *input)
{
  return parseRegExp(std::string(input));
}
