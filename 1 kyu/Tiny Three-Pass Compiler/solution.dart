import "package:solution/preloaded.dart";

class Parser {
  final List<String> tokens;
  final Map<String, Ast> args = {};
  int pos = 0;
  
  Parser(String expression) :
    tokens = RegExp(r'\d+|[-+*/()\[\]]|[a-zA-Z]+').allMatches(expression).map((m) => m[0]).toList();
  
  String next() => pos < tokens.length ? tokens[pos++] : null;
  String peek() => pos < tokens.length ? tokens[pos] : null;

  Ast atom() {
    final tok = next();
    if (tok == '(') {
      var r = expr();
      next();
      return r;
    }
    if (args.containsKey(tok)) return args[tok];
    return UnOp("imm", int.parse(tok));
  }
  
  Ast chainl1(Map<String, Ast Function(Ast, Ast)> ops, Ast nextLevel()) {
    var lhs = nextLevel();
    while (ops.containsKey(peek())) {
      lhs = ops[next()](lhs, nextLevel());
    }
    return lhs;
  }

  Ast factor() => chainl1({'*': (a, b) => BinOp('*', a, b), '/': (a, b) => BinOp('/', a, b)}, atom);
  
  Ast expr() => chainl1({'+': (a, b) => BinOp('+', a, b), '-': (a, b) => BinOp('-', a, b)}, factor);
  
  Ast func() {
    if (next() != '[') throw Exception('[ expected');
    for (int i = 0; peek() != ']' && peek() != null; i++) {
      args[next()] = UnOp('arg', i);
    }
    next();
    return expr();
  }
}

class Compiler {
  List<String> compile(String prog) => pass3(pass2(pass1(prog)));

  Ast pass1(String prog) => Parser(prog).func();
  
  final ops = {
    '+': (int a, int b) => a + b,
    '-': (int a, int b) => a - b,
    '*': (int a, int b) => a * b,
    '/': (int a, int b) => a ~/ b
  };
  
  Ast pass2(Ast ast) {
    if (ast is BinOp) {
      final a = pass2(ast.a);
      final b = pass2(ast.b);
      if (a is UnOp && b is UnOp && a.op() == 'imm' && b.op() == 'imm') {
        return UnOp('imm', ops[ast.op()](a.n, b.n));
      }
      return BinOp(ast.op(), a, b);
    }
    return ast;
  }
  
  final opCmd = {'+': 'AD', '-': 'SU', '*': 'MU', '/': 'DI'};

  List<String> pass3(Ast ast) {
    if (ast is UnOp) {
      return ["${ast.op() == 'arg' ? 'AR' : 'IM'} ${ast.n}"];
    }
    if (ast is BinOp) {
      return [...pass3(ast.a), 'PU', ...pass3(ast.b), 'SW', 'PO', opCmd[ast.op()]];
    }
  }
}

_________________________________________________
import "package:solution/preloaded.dart";

class Compiler {
  List<String> args = [];
  List<String> tokens = [];
  int ndx = 0;

  String getToken() {
    return tokens[ndx++];
  }
  
  void ungetToken() {
    ndx--;
  }

  List<String> tokenize(String prog) {
    List<String> tokens = [];
    RegExp pattern = RegExp("[-+*/()\\[\\]]|[a-zA-Z]+|\\d+");
    pattern.allMatches(prog).toList().forEach((m) {
        tokens.add(m.group(0));
    });
    tokens.add("\$"); // end-of-stream
    return tokens;
  }

  List<String> compile(String prog) => pass3(pass2(pass1(prog)));

  bool isDigit(int s) => s >= '0'.codeUnitAt(0) && s <= '9'.codeUnitAt(0);
  bool isAlpha(int s) => s >= 'a'.codeUnitAt(0) && s <= 'z'.codeUnitAt(0)
  || s >= 'A'.codeUnitAt(0) && s <= 'Z'.codeUnitAt(0);
  
  void parseFunction() {
    getToken();
    var token = getToken();
    while (token != ']') {
      args.add(token);
      token = getToken();
    }
  }

  Ast parseFactor() {
    var token = getToken();
    Ast v;
    if (isDigit(token.codeUnitAt(0))) {
      v = UnOp('imm', int.parse(token));
    } else if (isAlpha(token.codeUnitAt(0))) {
      int n = args.indexOf(token);
      v = UnOp('arg', n);
    } else if (token == '(') {
      v = parseExpression();
      getToken();
    } else {
      ungetToken();
    }
    return v;
  }

  Ast parseExpression() {
    Ast v1 = parseTerm();
    while (true) {
      var token = getToken();
      if (token != '-' && token != '+') {
        ungetToken();
        break;
      } else {
        Ast v2 = parseTerm();
        if (token == '+') {
          v1 = BinOp('+', v1, v2);
        } else if (token == '-') {
          v1 = BinOp('-', v1, v2);
        } else {
          ungetToken();
        }
      }
    }
    return v1;
  }

  Ast parseTerm() {
    Ast v1 = parseFactor();
    while (true) {
      var token = getToken();
      if (token != '*' && token != '/') {
        ungetToken();
        break;
      } else {
        Ast v2 = parseFactor();
        if (token == '*') {
          v1 = BinOp('*', v1, v2);
        } else if (token == '/') {
          v1 = BinOp('/', v1, v2);
        } else {
          ungetToken();
        }
      }
    }
    return v1;
  }

  Ast reduceConstant(Ast ast) {
    var op = ast.op();
    if (op == 'imm' || op == 'arg') {
      return ast;
    }
    BinOp binOp = ast;;
    Ast a1 = reduceConstant(binOp.a);
    Ast b1 = reduceConstant(binOp.b);
    if (a1.op() == 'imm' && b1.op() == 'imm') {
      int n;
      UnOp a = a1;
      UnOp b = b1;
      if (op == '+') {
        n = a.n + b.n;
      } else if (op == '-') {
        n = a.n - b.n;
      } else if (op == '*') {
        n = a.n * b.n;
      } else {
        n = a.n ~/ b.n;
      }
      return UnOp('imm', n);
    }

    return BinOp(op, a1, b1);
  }

  List<String> assembly(Ast ast) {
    String op = ast.op();
    if (op == 'imm') {
      return ['IM ${(ast as UnOp).n}'];
    }
    if (op == 'arg') {
      return ['AR ${(ast as UnOp).n}'];
    }
    List<String> a = assembly((ast as BinOp).a);
    List<String> b = assembly((ast as BinOp).b);
    Map<String, String> ops = { '+': 'AD', '-': 'SU', '*': 'MU', '/': 'DI' };
    if (a.length == 1 && b.length == 1) {
      if (op == '-') {
        return [b[0], 'SW', a[0], ops[op]];
      }
      return [a[0], 'SW', b[0], ops[op]];
    }

    a.add('PU');
    b.add('SW');
    b.add('PO');
    b.add(ops[op]);
    return a + b;
  }
  /**
  * Returns an un-optimized AST
  */
  Ast pass1(String prog) {
    tokens = tokenize(prog);
    parseFunction();
    return parseExpression();
  }

  /**
  * Returns an AST with constant expressions reduced
  */
  Ast pass2(Ast ast) {
    return reduceConstant(ast);
  }

  List<String> pass3(Ast ast) {
    return assembly(ast);
  }
}

___________________________________________________
import "package:solution/preloaded.dart";

class Compiler {
  List<String> tokens;
  Map<String, int> args;

  static List<String> tokenize(String prog) {
    List<String> tokens = new List();
    RegExp pattern = new RegExp("[-+*/()\\[\\]]|[a-zA-Z]+|\\d+");
    pattern.allMatches(prog).toList().forEach((m) { tokens.add(m.group(0)); } );
    tokens.add("\$"); 
    return tokens;
  }

  String peek() => tokens.first;

  String consume() => tokens.removeAt(0);

  List<String> compile(String prog) => pass3(pass2(pass1(prog)));

  Ast func() {
    consume(); 
    int i = 0;
    while (!(peek() == "]")) {
      args[consume()] = i++;
    }
    consume(); 
    return expression();
  }

  Ast expression() {
    Ast result = term();
    while (peek() == ("+") || 
           peek() == ("-")) {
      result = new BinOp(consume(), result, term());
    }
    return result;
  }

  Ast term() {
    Ast result = factor();
    while (peek() == ("*") || 
           peek() == ("/")) {
      result = new BinOp(consume(), result, factor());
    }
    return result;
  }

  bool isDigit(int s) => s >= '0'.codeUnitAt(0) && s <= '9'.codeUnitAt(0);

  Ast factor() {
    String token = consume();
    if (token == ("(")) {
      Ast result = expression();
      consume(); 
      return result;
    } else if (isDigit(token.codeUnitAt(0))) {
      return new UnOp("imm", int.parse(token));
    } else {
      return new UnOp("arg", args[token]);
    }
  }

  int compute(String op, int n1, int n2) {
    switch (op) {
      case "+":
        return n1 + n2;
      case "-":
        return n1 - n2;
      case "*":
        return n1 * n2;
      case "/":
        return n1 ~/ n2;
    }
    return 0;
  }

  /**
   * Returns an un-optimized AST
   */
  Ast pass1(String prog) {
    tokens = tokenize(prog);
    args = new Map();
    return func();
  }

  /**
   * Returns an AST with constant expressions reduced
   */
  Ast pass2(Ast ast) {
    if (ast is BinOp) {
      BinOp binOp = ast;
      Ast a = pass2(binOp.a);
      Ast b = pass2(binOp.b);
      if (a is UnOp && a.op() == "imm" && 
        b is UnOp && b.op() == "imm") {
        return new UnOp("imm", compute(binOp.op(), a.n, b.n));
      }
      return new BinOp(binOp.op(), a, b);
    }
    return ast;
  }

  List<String> pass3(Ast ast) {
    if (ast.op() == "arg") {
      return ["AR ${(ast as UnOp).n}"];
    } else if (ast.op() == "imm") {
      return ["IM ${(ast as UnOp).n}"];
    } else {
      String opcode = _opcode(ast.op());
      BinOp binOp = ast as BinOp;
      List<String> t = new List();
      t.addAll(pass3(binOp.a));
      t.add("PU");
      t.addAll(pass3(binOp.b));
      t.add("SW");
      t.add("PO");
      t.add(opcode);
      return t;
    }
  }

  String _opcode(String op) {
    switch (op) {
      case "+":
        return "AD";
      case "-":
        return "SU";
      case "*":
        return "MU";
      case "/":
        return "DI";
    }
    throw "gg";
  }
}

______________________________________________________
import "package:solution/preloaded.dart";
class Compiler {
  static List<String> tokenize(String prog) {
    List<String> tokens = new List();
    RegExp pattern = new RegExp(r"[-+*/()\[\]]|[a-zA-Z]+|\d+");
    pattern.allMatches(prog).toList().forEach((m) {
      tokens.add(m.group(0));
    });
    tokens.add(r"$"); // end-of-stream
    return tokens;
  }

  List<String> compile(String prog) => pass3(pass2(pass1(prog)));

  bool isDigit(int s) => s >= '0'.codeUnitAt(0) && s <= '9'.codeUnitAt(0);

  /**
   * Returns an un-optimized AST
   */
  Ast pass1(String prog) {
    final tokens = tokenize(prog);

    final args = tokens
        .getRange(1, tokens.indexOf(']'))
        .toList()
        .asMap()
        .map((k, v) => MapEntry(v, k));

    bool isAddOrSub(String s) => '+-'.indexOf(s) > -1;
    bool isMulOrDiv(String s) => '*/'.indexOf(s) > -1;
    bool isOp(String s) => isAddOrSub(s) || isMulOrDiv(s);

    final ops = <String>[];
    final nodes = <Ast>[];

    void addOp(String s) {
      final b = nodes.removeLast();
      final a = nodes.removeLast();
      nodes.add(BinOp(s, a, b));
    }

    tokens.skip(args.length + 2).forEach((tok) {
      if (args.containsKey(tok)) {
        nodes.add(UnOp('arg', args[tok]));
      } else if (int.tryParse(tok) != null) {
        nodes.add(UnOp('imm', int.parse(tok)));
      } else if (tok == '(') {
        ops.add(tok);
      } else if (tok == ')') {
        while (ops.isNotEmpty && ops.last != '(') {
          addOp(ops.removeLast());
        }
        if (ops.isEmpty) throw 'Unbalanced parens';
        ops.removeLast();
      } else if (isAddOrSub(tok)) {
        while (ops.isNotEmpty && isOp(ops.last)) addOp(ops.removeLast());
        ops.add(tok);
      } else if (isMulOrDiv(tok)) {
        while (ops.isNotEmpty && isMulOrDiv(ops.last)) addOp(ops.removeLast());
        ops.add(tok);
      } else if (tok == r'$') {
        // noop
      } else {
        throw 'Unknown token $tok';
      }
    });

    while (ops.isNotEmpty) addOp(ops.removeLast());

    return nodes.last;
  }

  /**
   * Returns an AST with constant expressions reduced
   */
  Ast pass2(Ast node) {
    if (node is UnOp) return node;
    if (node is BinOp) {
      final a = pass2(node.a);
      final b = pass2(node.b);
      if (a is UnOp && b is UnOp && a.op() == 'imm' && b.op() == 'imm') {
        switch (node.op()) {
          case '*':
            return UnOp('imm', a.n * b.n);
          case '/':
            return UnOp('imm', a.n ~/ b.n);
          case '+':
            return UnOp('imm', a.n + b.n);
          case '-':
            return UnOp('imm', a.n - b.n);
          default:
            throw 'Invalid op ${node.op()}';
        }
      } else {
        return BinOp(node.op(), a, b);
      }
    }

    throw 'Invalid node';
  }

  List<String> pass3(Ast node) {
    final stack = <Ast>[node];
    final nodes = <Ast>[];
    while (stack.isNotEmpty) {
      final n = stack.removeLast();
      nodes.add(n);
      if (n is BinOp) {
        stack.add(n.a);
        stack.add(n.b);
      }
    }
    final ops = <String>[];
    nodes.reversed.forEach((n) {
      if (n is UnOp) {
        if (n.op() == 'imm') {
          ops.add('IM ${n.n}');
        } else {
          ops.add('AR ${n.n}');
        }
        ops.add('PU');
      } else if (n is BinOp) {
        ops.addAll(['PO', 'SW', 'PO']);
        if (n.op() == '*') ops.add('MU');
        if (n.op() == '/') ops.add('DI');
        if (n.op() == '+') ops.add('AD');
        if (n.op() == '-') ops.add('SU');
        ops.add('PU');
      }
    });
    ops.add('PO');

    return ops;
  }
}
