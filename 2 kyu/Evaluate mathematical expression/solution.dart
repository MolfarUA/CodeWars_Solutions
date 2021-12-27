calc(String expression) {
  expression = expression.replaceAll(" ", "");
  while (expression.contains("(")) {
    String sub = expression.substring(0,expression.indexOf(")"));
    sub = sub.substring(sub.lastIndexOf("(")+1);
    expression = expression.replaceAll("($sub)", '${engine(sub)}');
  }
  return engine(expression);
}

double engine(String str) {
  str = str.replaceAll("--","+").replaceAll("+-","-");
  str += "+";
  String number = str[0];
  String operator1 = "", operator2 = "";
  double number1, number2;
  for (int b = 1; b <= str.length; b++) {
    if (!["-","+","*","/"].contains(str[b])) number += str[b];
    else {
      double number3 = double.parse(number);
      if (operator2 == "") number2 = number3;
      else operator2 == "*" ? number2 *= number3 : number2 /= number3;
      if (str[b] == "+" || str[b] == "-") {
        if (operator1 == "") number1 = number2;
        else operator1 == "+" ? number1 += number2 : number1 -= number2;
        operator1 = str[b];
        operator2 = "";
      }
      else operator2 = str[b];
      b++;
      if (b < str.length) number = str[b];
    }
  }
  return number1;
}
____________________________________________
class ExpressionParser 
{
    String exp;
    int i = 0;
  
    ExpressionParser(String exp)
    {
        this.exp = exp.replaceAll(new RegExp(r"\s"), "");
    }
  
    double expression() 
    {
        double num = this.term();
        while (this.peek() == "+" || this.peek() == "-") 
        {
            if (this.shift() == "+") num += this.term();
            else num -= this.term();
        }
        return num;
    }
  
    double term() 
    {
        double num = this.factor();
        while (this.peek() == "*" || this.peek() == "/") 
        {
            if (this.shift() == "*") num *= this.factor();
            else num /= this.factor();
        }
        return num;
    }
  
    double factor()
    {
        if (isDigit(this.peek())) return this.number();
        if (this.peek() == "(")
        {
            this.shift();
            double subexp = this.expression();
            this.shift();
            return subexp;
        }
        else if (this.peek() == "-")
        {
            this.shift();
            return -this.factor();
        }
        return 0.0;
    } 
  
    double number() 
    {
        String num = this.shift();
        while (isDigit(this.peek()) || this.peek() == ".") 
        {
            num += this.shift();
        }
        return double.parse(num);
    }
  
    bool isDigit(String s) 
    {
        return s.length > 0 && "0123456789".contains(s);
    }
  
    String shift() 
    {
        String val = this.peek();
        this.i++;
        return val;
    }
  
    String peek()
    { 
        return this.i >= this.exp.length ? "" : this.exp[i];
    }
}

double calc(String expression) 
{
    var parser = new ExpressionParser(expression);
    return parser.expression();
}
____________________________________________________
class Evaluator {
  final List<String> tokens;
  int pos = 0;
  
  Evaluator(String expression) :
    tokens = RegExp(r'\d+(?:\.\d+)?|[-+*/()]').allMatches(expression).map((m) => m[0]).toList();
  
  String next() => pos < tokens.length ? tokens[pos++] : null;
  String peek() => pos < tokens.length ? tokens[pos] : null;

  double atom() {
    var tok = next();
    if (tok == '-') return -atom();
    if (tok == '(') {
      var r = expr();
      next();
      return r;
    }
    return double.parse(tok);
  }
  
  double chainl1(Map<String, double Function(double, double)> ops, double nextLevel()) {
    var lhs = nextLevel();
    while (ops.containsKey(peek())) {
      lhs = ops[next()](lhs, nextLevel());
    }
    return lhs;
  }

  double factor() => chainl1({'*': (a, b) => a * b, '/': (a, b) => a / b}, atom);
  
  double expr() => chainl1({'+': (a, b) => a + b, '-': (a, b) => a - b}, factor);
}

double calc(String expression) => Evaluator(expression).expr();
___________________________________________________________
import 'dart:collection';

class Token {
  static const String operators = '+-*/';
  static const Set<String> functions = {'minus'};

  final String value;

  const Token(this.value);

  bool get isNumber {
    if (num.tryParse(value) != null) {
      return true;
    } else {
      return false;
    }
  }

  bool get isOpenBracket => value == '(';

  bool get isCloseBracket => value == ')';

  bool get isOperator => operators.contains(value);

  bool get isFunction => functions.contains(value);

  int get precedence => value == '+' || value == '-' ? 1 : 2;

  num toNumber() => num.parse(value);

  @override
  String toString() => value;

  @override
  int get hashCode => value.hashCode;

  @override
  bool operator ==(Object other) => other is Token && other.value == value;
}

class Tokenizer {
  final Set<String> _delimiters = '${Token.operators}()'.split('').toSet();

  Iterable<Token> tokenize(String expression) sync* {
    String data = expression.replaceAll(' ', '');
    String sequence = '';

    for (int i = 0; i < data.length; i++) {
      final char = data[i];

      if (char == '-' && (i == 0 || (Token(data[i - 1]).isOperator || Token(data[i - 1]).isOpenBracket))) {
        final next = Token(data[i + 1]);
        if (next.isNumber) {
          sequence += char;
        } else if (next.isOpenBracket) {
          if (sequence.isNotEmpty) {
            yield Token(sequence);
          }
          yield const Token('minus');
          sequence = '';
        }
      } else if (_delimiters.contains(char)) {
        if (sequence.isNotEmpty) {
          yield Token(sequence);
        }
        yield Token(char);
        sequence = '';
      } else {
        sequence += char;
      }
    }

    if (sequence.isNotEmpty) {
      yield Token(sequence);
    }
  }
}

  Queue<Token> _infixToRpn(String expression) {
    final Queue<Token> stack = Queue();
    final Queue<Token> output = Queue();

    final tokens = Tokenizer().tokenize(expression);
    for (final token in tokens) {
      if (token.isNumber) {
        output.add(token);
      } else if (token.isFunction) {
        stack.add(token);
      } else if (token.isOperator) {
        while (stack.isNotEmpty && stack.last.isOperator && token.precedence <= stack.last.precedence) {
          output.add(stack.removeLast());
        }
        stack.add(token);
      } else if (token.isOpenBracket) {
        stack.add(token);
      } else if (token.isCloseBracket) {
        while (stack.isNotEmpty && !stack.last.isOpenBracket) {
          output.add(stack.removeLast());
        }
        stack.removeLast();
        if (stack.isNotEmpty && stack.last.isFunction) {
          output.add(stack.removeLast());
        }
      }
    }
    while (stack.isNotEmpty) {
      output.add(stack.removeLast());
    }
    return output;
  }

  num _rpnAlgorithm(Queue<Token> input) {
    final stack = Queue<num>();

    for (final token in input) {
      if (token.isNumber) {
        stack.add(token.toNumber());
      } else if (token.isFunction) {
        final operand = stack.removeLast();
        stack.add(-operand);
      } else if (token.isOperator) {
        final operand2 = stack.removeLast();
        final operand1 = stack.removeLast();
        switch(token.value) {
          case '+':
            stack.add(operand1 + operand2);
            break;

          case '-':
            stack.add(operand1 - operand2);
            break;

          case '*':
            stack.add(operand1 * operand2);
            break;

          case '/':
            stack.add(operand1 / operand2);
            break;
        }
      }
    }
    return stack.removeLast();
  }

num calc(String expression) {
    final input = _infixToRpn(expression);
    return _rpnAlgorithm(input);
}
