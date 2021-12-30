Array.prototype.last = function() {
    return this[this.length-1];
}

function Interpreter()
{
    this.vars = {};
    this.functions = {};
}

Interpreter.prototype.tokenize = function (program)
{
    if (program === "")
        return [];

    var regex = /\s*([-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*/g;
    return program.split(regex).filter(function (s) { return !s.match(/^\s*$/); });
};

Interpreter.prototype.input = function (expr)
{

    var _this = this;
    var tokens = this.tokenize(expr);
    var ops = [];
    var stack = [];

    tokens.forEach(function(token) {

      if(_this.isOperator(token)) {
        if(_this.getOperatorRank(ops.last()) < _this.getOperatorRank(token) || (stack.length >= 2 && stack[stack.length-2] == '(' ) ) { 
          ops.push(token);
        } else {
          var b = stack.pop();
          var a = stack.pop();
          stack.push(_this.doOp(a, ops.pop(), b));
          ops.push(token);
        }
      }else if(token == "(") {
        stack.push(token);
      } else if(_this.isNumber(token)) {
        stack.push(token);
      } else if(_this.isIdentifier(token)) {
        stack.push(token);
      } else if(token == ")") {
        while(stack.length > 0){
          var b = stack.pop();
          var a = stack.pop();
          if(stack.last() == "(") {
            stack.pop();
            stack.push(_this.doOp(a, ops.pop(), b));
            break;
          }
        };
        
      }
    });
    
    while(stack.length > 1) {
      var b = stack.pop();
      var a = stack.pop();
      stack.push(_this.doOp(a, ops.pop(), b));
    }
    return (tokens.length > 0)?_this.getVal(stack.pop()):"";
};

Interpreter.prototype.isDigit = function(token) {
  return (token.length == 1 && token >= "0" && token <= "9");
};

Interpreter.prototype.isLetter = function(token) {
  return token.length == 1 && (token >= "a" && token <= "z" || token >="A" && token <= "Z");
}

Interpreter.prototype.isOperator = function(token) {
  return ["+", "-", "*", "/", "%", "="].indexOf(token) >= 0;
}

Interpreter.prototype.getOperatorRank = function(token) {
  switch(token) {
    case "=": return 0;
    case "+":
    case "-": return 1;
    case "*":
    case "/":
    case "%": return 2;
  }
  return -1;
}

Interpreter.prototype.isIdentifier = function(token) {
  var regex = /^[a-zA-Z]([a-zA-Z_0-9]*)?$/g;
  return regex.test(token);
}

Interpreter.prototype.isNumber = function(token) {
  var regex = /^[\+\-]?\d*[\.]?\d+$/g;
  return regex.test(token);
}
Interpreter.prototype.getVal = function(a) {
  if(this.isNumber(a)) {
    a = Number(a);
  } else if(this.isIdentifier(a)) {
    var aa = this.vars[a];
    if(typeof aa === "undefined") {
      throw "No variable with name '" + a + "' was found.";
    }
    a = aa;
  }
  return a;
}
Interpreter.prototype.doOp = function(a, op, b) {
  if(op != "=") {
    var aa = this.getVal(a);
    var bb = this.getVal(b);
   
    switch(op) {
      case "+": return aa + bb;
      case "-": return aa - bb;
      case "*": return aa * bb;
      case "/": return aa / bb;
      case "%": return aa % bb;
      case "=": this.vars[a] = bb; return a;
    }
  } else {
    this.vars[a] = this.getVal(b);
    return a;
  }
}

________________________________________________________
class Token {

  constructor(type, value) {
    this.type = type;
    this.value = value;
  }
  
  toString() {
    return `Token(${this.type}, ${this.value})`;
  }
  
}

Object.assign(Token, {
  PLUS: 'PLUS',
  MINUS: 'MINUS',
  MUL: 'MUL',
  DIV: 'DIV',
  MOD: 'MOD',
  ASSIGN: 'ASSIGN',
  LPAREN: 'LPAREN',
  RPAREN: 'RPAREN',
  IDENTIFIER: 'IDENTIFIER',
  NUMBER: 'NUMBER'
});



/********** LEXER **********/

const isDigit = char => /^\d$/.test(char);
const isLetter = char => /^[a-zA-Z]$/.test(char);
const isIdChar = char => char === '_' || isLetter(char) || isDigit(char);
const isWhitespace = char => /^\s$/.test(char);

class Lexer {
  
  constructor() {
  
  }
  
  receiveNewInput(input) {
    this.input = input;
    this.pos = 0;
    this.maxPos = this.input.length - 1;
    this.currentChar = this.input[this.pos];
  }
  
  error() {
    throw new Error(`Unexpected character: ${this.currentChar}`);
  }
  
  advance() {
    this.pos++;
    this.currentChar = this.pos > this.maxPos ? null : this.input[this.pos];
  }
  
  skipWhitespace() {
    while (isWhitespace(this.currentChar)) {
      this.advance();
    }
  }
  
  getNumber() {
  
    let number = '';
    
    while (isDigit(this.currentChar)) {
      number += this.currentChar;
      this.advance();
    }
    
    if (this.currentChar === '.') {
    
      number += this.currentChar;
      this.advance();
      
      if (!isDigit(this.currentChar)) {
        this.error();
      }
      
      while (isDigit(this.currentChar)) {
        number += this.currentChar;
        this.advance();
      }
    }
    
    return parseFloat(number);
  }
  
  getIdentifier() {
    
    let identifier = this.currentChar;
    this.advance();
    
    while (isIdChar(this.currentChar)) {
      identifier += this.currentChar;
      this.advance();
    }
    
    return identifier;
  }
  
  getNextToken() {
    
    while (this.currentChar !== null) {
      
      let c = this.currentChar;
      
      if (isWhitespace(c)) {
        this.skipWhitespace();
        continue;
      }
      
      if (isDigit(c)) {
        return new Token(Token.NUMBER, this.getNumber());
      }
      
      if (isLetter(c) || c === '_') {
        return new Token(Token.IDENTIFIER, this.getIdentifier());
      }
      
      switch(c) {
        case '+':
          this.advance();
          return new Token(Token.PLUS, c);
        case '-':
          this.advance();
          return new Token(Token.MINUS, c);
        case '*':
          this.advance();
          return new Token(Token.MUL, c);
        case '/':
          this.advance();
          return new Token(Token.DIV, c);
        case '%':
          this.advance();
          return new Token(Token.MOD, c);
        case '=':
          this.advance();
          return new Token(Token.ASSIGN, c);
        case '(':
          this.advance();
          return new Token(Token.LPAREN, c);
        case ')':
          this.advance();
          return new Token(Token.RPAREN, c);
      }
      
      this.error();
    }
    
    return new Token(Token.EOF, null);
  }

}



/********** AST **********/

class ASTNode {
  constructor() {
  }
}

class AssignmentNode extends ASTNode {
  constructor(token, expr) {
    super();
    this.token = token;
    this.expr = expr;
  }
}

class BinaryOpNode extends ASTNode {
  constructor(token, left, right) {
    super();
    this.token = token;
    this.left = left;
    this.right = right;
  }
}

class VariableNode extends ASTNode {
  constructor(token) {
    super();
    this.token = token;
  }
}

class NumberNode extends ASTNode {
  constructor(token) {
    super();
    this.token = token;
  }
}



/********** PARSER **********/

class Parser {

  constructor() {
    this.lexer = new Lexer();
  }
  
  receiveNewInput(input) {
    this.lexer.receiveNewInput(input);
    this.currentToken = this.lexer.getNextToken();
  }
  
  error() {
    throw new SyntaxError(`Unexpected token: ${this.currentToken}`);
  }
  
  eat(tokenType) {
    if (this.currentToken.type !== tokenType) {
      this.error();
    }
    this.currentToken = this.lexer.getNextToken();
  }
  
  expr() {
    
    let node = this.term();
    
    while ([Token.PLUS, Token.MINUS].indexOf(this.currentToken.type) > -1) {
      let token = this.currentToken;
      this.eat(token.type);
      node = new BinaryOpNode(token, node, this.term());
    }
    
    return node;
  }
  
  term() {
    
    let node = this.factor();
    
    while ([Token.MUL, Token.DIV, Token.MOD].indexOf(this.currentToken.type) > -1) {
      let token = this.currentToken;
      this.eat(token.type);
      node = new BinaryOpNode(token, node, this.factor());
    }
    
    return node;
  }
  
  factor() {
  
    let token = this.currentToken;
    
    if (token.type === Token.NUMBER) {
      this.eat(Token.NUMBER);
      return new NumberNode(token);
    }
    
    if (token.type === Token.IDENTIFIER) {
      
      this.eat(Token.IDENTIFIER);
      
      if (this.currentToken.type === Token.ASSIGN) {
        this.eat(Token.ASSIGN);
        return new AssignmentNode(token, this.expr());
      } else {
        return new VariableNode(token);
      }
    }
    
    if (token.type === Token.LPAREN) {
      this.eat(Token.LPAREN);
      let node = this.expr();
      this.eat(Token.RPAREN);
      return node;
    }
  }
  
  parse() {
    let ast = this.expr();
    return ast;
  }
  
}



/********** INTERPRETER **********/

class SymbolTable {
  
  constructor() {
    this.table = {};
  }
  
  get(varName) {
    if (this.table.hasOwnProperty(varName))
      return this.table[varName];
    else
      throw new ReferenceError(`${varName} is not defined`);
  }
  
  set(varName, value) {
    this.table[varName] = value;
  }

}

class NodeVisitor {
  
  visit(node) {
    let methodName = `visit${node.constructor.name}`;
    let visitor = this[methodName];
    return visitor ? visitor(node) : this.genericVisit(node);
  }
  
  genericVisit(node) {
    throw new Error('No method: visit' + node.constructor.name);
  }
  
}

class Interpreter extends NodeVisitor {
  
  constructor() {
  
    super();
  
    this.parser = new Parser();
    this.symbolTable = new SymbolTable();
    
    this.visitAssignmentNode = this.visitAssignmentNode.bind(this);
    this.visitBinaryOpNode = this.visitBinaryOpNode.bind(this);
    this.visitVariableNode = this.visitVariableNode.bind(this);
    this.visitNumberNode = this.visitNumberNode.bind(this);
  }
  
  input(input) {
    if (!input) return '';
    this.parser.receiveNewInput(input);
    let ast = this.parser.parse();
    return this.visit(ast);
  }
  
  visitAssignmentNode(node) {
    let varName = node.token.value;
    let value = this.visit(node.expr);
    this.symbolTable.set(varName, value);
    return value;
  }
  
  visitBinaryOpNode(node) {
  
    let lValue = this.visit(node.left);
    let rValue = this.visit(node.right);
    
    switch (node.token.type) {
      case Token.PLUS:
        return lValue + rValue;
      case Token.MINUS:
        return lValue - rValue;
      case Token.MUL:
        return lValue * rValue;
      case Token.DIV:
        return lValue / rValue;
      case Token.MOD:
        return lValue % rValue;
    }
  }
  
  visitVariableNode(node) {
    let varName = node.token.value;
    return this.symbolTable.get(varName);
  }
  
  visitNumberNode(node) {
    return node.token.value;
  }
  
}

        Best Practices3
        Clever1
    0
    Fork
    Link

Azuaron, johnshumiston, dubdjon, Spins, user9578508, user6398180, user4025778

function Interpreter() {
  this.vars = {}, this.functions = {};
}
Interpreter.prototype.tokenize = function(program) {
  if(program == "") return [];
  var regex = /\s*([-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*/g;
  return program.split(regex).filter(s => !s.match(/^\s*$/)).map(v => v.match(/^\d+\.?\d*$/) ? +v : v);
};
Interpreter.prototype.input = function(program) {
    var tokens = this.tokenize(program), itpr = this;
    if(tokens.length < 1) return "";
    let accept = sym => tokens[0] == sym && tokens.shift();
    let acceptNumber = () => !isNaN(tokens[0]) && tokens.shift();
    let acceptLetter = pred => tokens[0].length == 1 && 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.indexOf(tokens[0]) > -1 && tokens.shift();
    let acceptAny = arr => arr.some(a => a == tokens[0]) && tokens.shift();
    let doOp = (x, op, y) => [(a, b) => a + b, (a, b) => a - b, (a, b) => a * b, (a, b) => a / b, (a, b) => a % b][("+-*/%".indexOf(op))](x, y);
    function unit() {
      if(accept('(')) {
        let e = expr();
        accept(')');
        return e;
      }
      let a;
      if(a = acceptLetter(v => itpr.vars[v] != null)) {
        if(itpr.vars[a] == null) throw "No var declared: " + a;
        return itpr.vars[a];
      }
      return acceptNumber();
    }
    let unary = () => accept('-') ? -unit() : unit();
    function factor() {
      for(var x = unary(); op = acceptAny(['*','/', '%']); x = doOp(x, op, unary()));
      return x;
    }
    function expr() {
      if(tokens.indexOf('=') > -1) {
        for(var c = acceptLetter(() => true), x = null; op = accept('='); x = expr());
        itpr.vars[c] = x;
        return x;
      } else {
        for(var x = factor(); op = acceptAny(['+','-']); x = doOp(x, op, factor()));
        return x;
      }
    }
    return expr();
};

________________________________________________________
function Interpreter()
{
    this.vars = {};
    this.functions = {};
}

Interpreter.prototype.tokenize = function (program)
{
    if (program === "")
        return [];

    var regex = /\s*([-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*/g;
    return program.split(regex).filter(function (s) { return !s.match(/^\s*$/); });
};
const user = {}
Interpreter.prototype.input = function (expr)
{
    if(expr.includes('(')){
      let a = expr.lastIndexOf('('), b = expr.slice(a+1), c = b.indexOf(')')
      let interpreter = new Interpreter()
      return interpreter.input(expr.slice(0,a)+interpreter.input(b.slice(0,c))+b.slice(c+1))
    }

    if(!expr) return ''
    const v = x => +isNaN(x) ? user[x] : +x
    const f = {
      '*':(a,b)=>v(a) * v(b),
      '/':(a,b)=>v(a) / v(b),
      '%':(a,b)=>v(a) % v(b),
      '+':(a,b)=>v(a) + v(b),
      '-':(a,b)=>v(a) - v(b),
      '=':((a,b)=>user[a]=isNaN(+b)?user[b]:+b)
    }
    var tokens = this.tokenize(expr);
    
    for (let x of '*/%,+-,='.split(',')){
      let redo = true
      while(redo) {
        redo=false
        l:for (let t of tokens)
          for (let op of x)
            if (t === op) {
              let i = tokens.indexOf(op)
              tokens = [...tokens.slice(0,i-1), f[op](tokens[i-1],tokens[i+1]), ...tokens.slice(i+2)]
              redo=true
              break l
            }
      }
    }
        
        
    console.log(tokens)
    if (tokens.length === 1) {
      if (!user[tokens[0]] && isNaN(+tokens[0])) throw 'error'
      return isNaN(+tokens[0]) ? user[tokens[0]] : tokens[0]
    }
};

________________________________________________________
class Interpreter {
  constructor () { this.variables = {}; }

  input (s) {
    const attribution = /^(.+)=(.+)$/i;
    const parentesis = /\(([^(]*?)\)/;
    const term = /(.*[^*/]\b)([+-])(.+)/;
    const factor = /(.+)([*/%])(.+)/;
    const digit = /^[-+]?\d+(\.\d+)?$/;
    const variable = /^[_a-z][_a-z0-9]*$/;

    s = s.replace(/\s/g, '').replace(/--/g, '+');
    
    let exec;
    
    if (exec = attribution.exec(s)) {
      const x = this.input(exec[2]);
      this.variables[exec[1]] = x;
      return x;
    }
    
    while (exec = parentesis.exec(s))
      s = s.replace(parentesis, this.input(exec[1]));

    while (exec = term.exec(s)) {
      const left = +this.input(exec[1]);
      const right = +this.input(exec[3]);
      const operand = exec[2];
      const result = operand === '+' ? left + right : left - right;
      s = s.replace(term, result);
    }

    while (exec = factor.exec(s)) {
      const left = +this.input(exec[1]);
      const right = +this.input(exec[3]);
      const operand = exec[2];
      const result = operand === '*' ? left * right : operand === '/' ? left / right : left % right;
      s = s.replace(factor, result);
    }

    if (exec = digit.exec(s)) return Number(exec[0]);

    if (exec = variable.exec(s)) {
      const v = this.variables[exec[0]];
      if (!v) throw `ERROR: Invalid identifier. No variable '${s}' exists.`;
      return v;
    }

    return s;
  }
}

________________________________________________________
function Interpreter()
{
    this.vars = {};
    this.functions = {
      '+': (a, b) => a + b,
      '-': (a, b) => a - b,
      '*': (a, b) => a * b,
      '/': (a, b) => a / b,
      '%': (a, b) => a % b
    };
}

Interpreter.prototype.tokenize = function (program)
{
    if (program === "")
        return [];

    var regex = /\s*([-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*/g;
    return program.split(regex).filter(function (s) { return !s.match(/^\s*$/); });
};

Interpreter.prototype.input = function (expr)
{
  var tokens = this.tokenize(expr);
  if(!tokens.length) return ""
  
  const ast = this.parse(tokens)
  return this.evaluate(ast)
};

Interpreter.prototype.parse = function(tokens) {
  
  const parse_with = (operators, parser) => {
    let result = parser()
    while(operators.includes(tokens[0])) {
      const op = tokens.shift()
      const right = parser()
      result = {
        type: op,
        left: result,
        right
      }
    }
    return result
  }
  
  const parse_expression = () => 
    parse_with(['+', '-'], () => 
    parse_with(['*', '/', '%'], () => {
      const cur = tokens.shift()
      if(cur == '(') {
        const expr = parse_expression()
        tokens.shift()
        return expr
      }
      
      if(/^[A-Za-z_][A-Za-z0-9_]*/.test(cur)) {
        return {
          type: 'var',
          id: cur
        }
      }
      return {
        type: 'num',
        val: Number(cur)
      }
    }))
  
  let result = parse_expression()
  if(tokens.shift() == '=') {
    result = {
      type: '=',
      left: result,
      right: parse_expression()
    }
  }
  return result
}

Interpreter.prototype.evaluate = function(ast) {
  switch(ast.type) {
      case 'var':
      if(!this.vars[ast.id]) throw 0
      return this.vars[ast.id]
      
      case 'num':
      return ast.val
      
      case '=':
      this.vars[ast.left.id] = this.evaluate(ast.right)
      return this.vars[ast.left.id]
      
      default:
      return this.functions[ast.type](this.evaluate(ast.left), this.evaluate(ast.right))
  }
}
