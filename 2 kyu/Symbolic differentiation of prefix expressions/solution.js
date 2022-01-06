const diff = (() => {

  class Node {
    simplify() {
      return this;
    }

    derivative() {
      this.notImplementedError('derivative');
    }

    toString() {
      this.notImplementedError('toString');
    }

    notImplementedError(funcName) {
      throw new Error('Houston we have a problem!');
    }
  }

  class UnaryFuncNode extends Node {
    constructor(arg, funcName) {
      super();
      this.arg = arg;
      this.funcName = funcName;
    }

    simplify() {
      return new this.constructor(this.arg.simplify());
    }

    toString() {
      return `(${this.funcName} ${this.arg})`;
    }
  }

  class BinaryOpNode extends Node {
    constructor(left, right, op) {
      super();
      this.left = left;
      this.right = right;
      this.op = op;
    }

    simplify() {
      return new this.constructor(this.left.simplify(), this.right.simplify());
    }

    toString() {
      return `(${this.op} ${this.left} ${this.right})`;
    }
  }

  class ConstNode extends Node {
    constructor(value) {
      super();
      this.value = value;
    }

    derivative() {
      return new ConstNode(0);
    }

    toString() {
      return `${this.value}`;
    }
  }

  class VarNode extends Node {
    constructor(symbol) {
      super();
      this.symbol = symbol;
    }

    derivative() {
      return new ConstNode(1);
    }

    toString() {
      return this.symbol;
    }
  }

  class AddNode extends BinaryOpNode {
    constructor(left, right) {
      super(left, right, '+');
    }

    derivative() {
      return new AddNode(this.left.derivative(), this.right.derivative());
    }

    simplify() {
      let left = this.left.simplify();
      let right = this.right.simplify();
      if (left instanceof ConstNode && right instanceof ConstNode) {
        return new ConstNode(left.value + right.value);
      }
      if (left instanceof ConstNode && left.value === 0) {
        return right;
      }
      if (right instanceof ConstNode && right.value === 0) {
        return left;
      }
      return new AddNode(left, right);
    }
  }

  class SubNode extends BinaryOpNode {
    constructor(left, right) {
      super(left, right, '-');
    }

    derivative() {
      return new SubNode(this.left.derivative(), this.right.derivative());
    }

    simplify() {
      const left = this.left.simplify();
      const right = this.right.simplify();
      if (left instanceof ConstNode && right instanceof ConstNode) {
        return new ConstNode(left.value - right.value);
      }
      if (right instanceof ConstNode && right.value === 0) {
        return left;
      }
      return new SubNode(left, right);
    }
  }

  class MulNode extends BinaryOpNode {
    constructor(left, right) {
      super(left, right, '*');
    }

    derivative() {
      const left = new MulNode(this.left, this.right.derivative());
      const right = new MulNode(this.left.derivative(), this.right);
      return new AddNode(left, right);
    }

    simplify() {
      const left = this.left.simplify();
      const right = this.right.simplify();
      if (left instanceof ConstNode && right instanceof ConstNode) {
        return new ConstNode(left.value * right.value);
      }
      if (left instanceof ConstNode) {
        if (left.value === 0) {
          return new ConstNode(0);
        }
        if (left.value === 1) {
          return right;
        }
      }
      if (right instanceof ConstNode) {
        if (right.value === 0) {
          return new ConstNode(0);
        }
        if (right.value === 1) {
          return left;
        }
      }
      return new MulNode(left, right);
    }
  }

  class DivNode extends BinaryOpNode {
    constructor(num, den) {
      super(num, den, '/');
      this.num = num;
      this.den = den;
    }

    derivative() {
      const numLeft = new MulNode(this.num.derivative(), this.den);
      const numRight = new MulNode(this.num, this.den.derivative());
      const num = new SubNode(numLeft, numRight);
      const den = new PowNode(this.den, new ConstNode(2));
      return new DivNode(num, den);
    }

    simplify() {
      const num = this.num.simplify();
      const den = this.den.simplify();
      if (den instanceof ConstNode) {
        if (num instanceof ConstNode) {
          return new ConstNode(num.value / den.value);
        }
        if (den.value === 1) {
          return num;
        }
      }
      return new DivNode(num, den);
    }
  }

  class PowNode extends BinaryOpNode {
    constructor(arg, pow) {
      super(arg, pow, '^');
      this.arg = arg;
      this.pow = pow;
    }

    derivative() {
      const dInner = this.arg.derivative();
      const powerMinusOne = new SubNode(this.pow, new ConstNode(1));
      const dOuter = new MulNode(this.pow, new PowNode(this.arg, powerMinusOne));
      return new MulNode(dInner, dOuter);
    }

    simplify() {
      let arg = this.arg.simplify();
      let pow = this.pow.simplify();
      if (arg instanceof ConstNode && pow instanceof ConstNode) {
        return new ConstNode(Math.pow(arg.value, pow.value));
      }
      if (pow instanceof ConstNode) {
        if (pow.value === 0) {
          return new ConstNode(1);
        }
        if (pow.value === 1) {
          return arg;
        }
      }
      return new PowNode(arg, pow);
    }
  }

  class ExpNode extends UnaryFuncNode {
    constructor(arg) {
      super(arg, 'exp');
    }

    derivative() {
      return new MulNode(this.arg.derivative(), this);
    }
  }

  class LnNode extends UnaryFuncNode {
    constructor(arg) {
      super(arg, 'ln');
    }

    derivative() {
      return new DivNode(this.arg.derivative(), this.arg);
    }
  }

  class SinNode extends UnaryFuncNode {
    constructor(arg) {
      super(arg, 'sin');
    }

    derivative() {
      return new MulNode(this.arg.derivative(), new CosNode(this.arg));
    }
  }

  class CosNode extends UnaryFuncNode {
    constructor(arg) {
      super(arg, 'cos');
    }

    derivative() {
      return new MulNode(this.arg.derivative(), new MulNode(new ConstNode(-1), new SinNode(this.arg)));
    }
  }

  class TanNode extends UnaryFuncNode {
    constructor(arg) {
      super(arg, 'tan');
    }

    derivative() {
      let dInner = this.arg.derivative();
      let tanSquared = new PowNode(this, new ConstNode(2));
      let dOuter = new AddNode(new ConstNode(1), tanSquared);
      return new MulNode(dInner, dOuter);
    }
  }

  const tokenRe = /x|-?\d+|\(|\)|\+|-|\*|\/|\^|sin|cos|tan|exp|ln/g;

  class Parser {
    constructor(expr) {
      this.tokenize(expr);
      this.pos = 0;
      this.advance();
    }

    tokenize(expr) {
      this.tokens = tokenRe[Symbol.match](expr);
    }

    advance() {
      this.currentToken = this.pos < this.tokens.length ? this.tokens[this.pos++] : 'EOF';
    }

    error() {
      throw new Error(`Houston we have a problem!`);
    }

    eat(token) {
      if (this.currentToken === token) {
        this.advance();
      } else {
        this.error();
      }
    }

    parse() {
      let node = this.expr();
      return node;
    }

    expr() {
      if (this.currentToken === '(') {
        this.eat(this.currentToken);
        let node = this.expr();
        this.eat(')');
        return node;
      }
      if (/-?\d+/.test(this.currentToken)) {
        let node = new ConstNode(parseInt(this.currentToken));
        this.eat(this.currentToken);
        return node;
      }
      if (this.currentToken === 'x') {
        let node = new VarNode(this.currentToken);
        this.eat(this.currentToken);
        return node;
      }
      if (['sin', 'cos', 'tan', 'exp', 'ln'].includes(this.currentToken)) {
        let func = this.currentToken;
        this.eat(func);
        let arg = this.expr();
        switch (func) {
          case 'sin':
            return new SinNode(arg);
          case 'cos':
            return new CosNode(arg);
          case 'tan':
            return new TanNode(arg);
          case 'exp':
            return new ExpNode(arg);
          case 'ln':
            return new LnNode(arg);
          default: 
            return null;
        }
      }
      if ('+-*/^'.includes(this.currentToken)) {
        let op = this.currentToken;
        this.eat(op);
        let left = this.expr();
        let right = this.expr();
        switch (op) {
          case '+':
            return new AddNode(left, right);
          case '-':
            return new SubNode(left, right);
          case '*':
            return new MulNode(left, right);
          case '/':
            return new DivNode(left, right);
          case '^':
            return new PowNode(left, right);
          default: 
            return null;
        }
      }
      this.error();
    }
  }

  return expr => new Parser(expr).parse().derivative().simplify().toString();
})();
______________________________________________
const DEBUG = false ;

const diff = expr => show(optimise(evaluate(parse(tokenise(expr))))) ;

const tokenise = expression => DEBUG && console.log("<hr>tokenise",expression) ||
  ( expression.match( /-?(\d*\.)?\d+|\w+|[-+/*^]/g ) || [] ).map( t => isNumber(t) ? Number(t) : t )
;

const parse = tokens => { DEBUG && console.log("<hr>parse",tokens);
  const doOp = (op,left,right) => new Node(op,left,right) ;
  const accept = s => [...s].some( v => v===tokens[0] ) && tokens.shift();
  const variable = () => doOp(tokens.shift()) ;
  const constant = () => isNumber(tokens[0]) ? tokens.shift() : variable() ;
  const binary = (op) => ( op = accept(BINARY) ) ? doOp(op,expr(),expr()) : constant() ;
  const expr = (op) => ( op = accept(UNARY) ) ? doOp(op,expr()) : binary() ;
  return expr();
};

const evaluate = node => DEBUG && console.log("<hr>evaluate",show(node)) ||
  isNumber(node)           ? 0 :
  BINARY.includes(node.op) ? [ node => new Node(node.op,evaluate(node.left),evaluate(node.right)),
                               node => new Node(node.op,evaluate(node.left),evaluate(node.right)),
                               node => new Node(node.op,new Node("-",new Node("*",evaluate(node.left),node.right),new Node("*",node.left,evaluate(node.right))),new Node("^",node.right,2)),
                               node => new Node("+",new Node("*",evaluate(node.left),node.right),new Node("*",node.left,evaluate(node.right))),
                               node => new Node("*",evaluate(node.left),new Node("*",node.right,new Node(node.op,node.left,new Node("-",node.right,1)))),
                             ] [BINARY.indexOf(node.op)] (node) :
  UNARY.includes(node.op)  ? [ node => new Node("*",evaluate(node.left),new Node("cos",node.left)),
                               node => new Node("*",evaluate(node.left),new Node("*",-1,new Node("sin",node.left))),
                               node => new Node("*",evaluate(node.left),new Node("+",1,new Node("^",node,2))),
                               node => new Node("*",evaluate(node.left),node),
                               node => new Node("*",evaluate(node.left),new Node("/",1,node.left)),
                             ] [UNARY.indexOf(node.op)] (node) :
  /* variable */             1
;

const optimise = node => DEBUG && console.log("<hr>optimise",show(node)) ||
  BINARY.includes(node.op) ? [ left => right => isNumber(left) && isNumber(right) ? left-right : right===0 ? left : new Node(node.op,left,right) ,
                               left => right => isNumber(left) && isNumber(right) ? left+right : left===0 ? right : right===0 ? left : new Node(node.op,left,right)  ,
                               left => right => isNumber(left) && isNumber(right) ? left/right : left===0 ? 0 : right===1 ? left : new Node(node.op,left,right) ,
                               left => right => isNumber(left) && isNumber(right) ? left*right : left===0 || right===0 ? 0 : left===1 ? right : right===1 ? left : new Node(node.op,left,right) ,
                               left => right => isNumber(left) && isNumber(right) ? Math.pow(left,right) : left===0 ? 0 : left===1 ? 1 : right===0 ? 1 : right===1 ? left : new Node(node.op,left,right) ,
                             ] [BINARY.indexOf(node.op)] (optimise(node.left)) (optimise(node.right)) :
  UNARY.includes(node.op)  ? new Node(node.op,optimise(node.left)) :
  /* number or variable */ node
;

const show = node =>
  isNumber(node)           ? `${node}` :
  BINARY.includes(node.op) ? `(${node.op} ${show(node.left)} ${show(node.right)})` :
  UNARY.includes(node.op)  ? `(${node.op} ${show(node.left)})` :
  /* variable */             `${node.op}`
;

function Node(op,left,right) {
  this.op = op;
  this.left = left;
  this.right = right;
}

const isNumber = t => Number.isFinite(Number(t)) ;
const BINARY = "-+/*^";
const UNARY = ["sin","cos","tan","exp","ln"];
______________________________________________
function diff(expr) {
  if (expr == 'x') return '1';
  if (!expr.includes('x')) return '0';
  let [op, f, g] = splitTerms(expr);
  let [df, dg, res] = [diff(f), g?diff(g):''];
  if ('+-'.includes(op)) res = `(${op} ${df} ${dg})`;
  if (op == '*') res = `(+ (* ${df} ${g}) (* ${f} ${dg}))`;
  if (op == '/') res = `(/ (- (* ${df} ${g}) (* ${f} ${dg})) (^ ${g} 2))`;
  if (op == '^') res = (df=='0'?`(* ${expr} (ln ${f}))`:`(* (* ${g} (^ ${f} ${Number(g)-1})) ${df})`);
  if (op == 'cos') res = `(* ${df} (* -1 (sin ${f})))`;
  if (op == 'sin') res = `(* ${df} (cos ${f}))`;
  if (op == 'tan') res = `(/ ${df} (^ (cos ${f}) 2))`;
  if (op == 'ln') res = `(/ ${df} ${f})`;
  if (op == 'exp') res = `(* ${df} (exp ${f}))`;
  return res?simp(res):expr;
}

function simp(expr) {
  let [op, f, g] = splitTerms(expr);
  if (!f) return expr;
  let [sf, sg] = [simp(f), g?simp(g):''];
  if (op == '+') {
    if (sf == '0' || sg == '0') return sf == '0' ? sg : sf;
    if (isConst(sf) && isConst(sg)) return (Number(sf)+Number(sg))+'';
  } else if (op == '-') {
    if (sf == '0' || sg == '0') return sf == '0' ? (-1*Number(sg))+'' : sf;
    if (isConst(sf) && isConst(sg)) return (Number(sf)-Number(sg))+'';
  } else if (op == '*') {
    if (sf == '0' || sg == '0') return '0'
    if (sf == '1' || sg == '1') return sf == '1' ? sg : sf;
    if (isConst(sf) && isConst(sg)) return (Number(sf)*Number(sg))+'';
  } else if (op == '/') {
    if (sf == '0') return '0'
    if (isConst(sf) && isConst(sg)) return (Number(sf)/Number(sg))+'';
  } else if (op == '^') {
    if (sf == '0') return '0';
    if (sg == '0') return '1';
    if (sg == '1') return sf;
    if (isConst(sf) && isConst(sg)) return (Number(sf)**Number(sg))+'';
  }
  return sg?`(${op} ${sf} ${sg})`:`(${op} ${sf})`;
}

const isConst=e=>e&&e.split(' ').length==1&&(!e.includes('x'));

function splitTerms(expr) {
  if (!expr.includes(' ')) return [expr];
  let c = 0;
  return expr.slice(1,-1).split('').map(v=>{
    if (v == ' ' && c == 0) return '|';
    if (v == '(') c++;
    if (v == ')') c--;
    return v;
  }).join('').split('|');
}
______________________________________________
function diff(expr) {
  const e = parse(expr);
  const ep = diffExpr(e);
  const se = simplify(ep);
  return print(se);
}

function parse(e) {
  const tokens = lex(e);
  
  let token;
  
  function nextToken() {
    token = tokens.shift();
  }
  
  function accept(str) {
    if (token === str) {
      nextToken();
      return true;
    }
    return false;
  }
  
  function expect(str) {
    if (!accept(str)) {
      throw new Error(`Expected ${str} but got ${token}`);
    }
  }
  
  function expr() {
    if (accept('x')) {
      return makeSymbol();
    } else if (accept('(')) {
      return operation();
    } else {
      const op = makeConstant(parseInt(token, 10));
      nextToken();
      return op;
    }
  }
  
  function operation() {
    const type = operationType();
    const operands = [];
    while (token !== ')') {
      operands.push(expr());
    }
    nextToken();
    return makeOperation(type, ...operands);
  }
  
  function operationType() {
    if (!(token === '+' || token === '-' || token === '*' || token === '/' || token === '^' || token === 'cos' || token === 'sin' || token === 'tan' || token === 'exp' || token === 'ln')) {
      throw new Error(`Expected operation but got ${token}`);
    }
    const op = token;
    nextToken();
    return op;
  }
  
  nextToken();
  return expr();
}

function lex(expr) {
  const tokenizer = /[x+*/^()-]|cos|sin|tan|exp|ln|[0-9]+/g;
  let tokens = [];
  let token;
  while ((token = tokenizer.exec(expr)) !== null) {
    tokens.push(token[0]);
  }
  return tokens;
}

function print(e) {
  switch (e.type) {
  case 'symbol':
    return 'x';
  case 'constant':
    return '' + e.value;
  case 'operation':
    return `(${e.op} ${e.operands.map(o => print(o)).join(' ')})`;
  }
}

function diffExpr(e) {
  switch (e.type) {
  case 'symbol':
    return makeConstant(1);
  case 'constant':
    return makeConstant(0);
  case 'operation':
    switch (e.op) {
    case '+':
    case '-':
      return makeOperation(e.op, diffExpr(e.operands[0]), diffExpr(e.operands[1]));
    case '*':
      return makeOperation('+', makeOperation('*', diffExpr(e.operands[0]), e.operands[1]), makeOperation('*', diffExpr(e.operands[1]), e.operands[0]));
    case '/':
      return makeOperation('/', makeOperation('-', makeOperation('*', diffExpr(e.operands[0]), e.operands[1]), makeOperation('*', diffExpr(e.operands[1]), e.operands[0])), makeOperation('^', e.operands[1], makeConstant(2)));
    case '^':
      return makeOperation('*', makeConstant(e.operands[1].value), makeOperation('^', makeSymbol(), makeConstant(e.operands[1].value - 1)));
    case 'cos':
      return chain(e, o => makeOperation('*', makeConstant(-1), makeOperation('sin', o)));
    case 'sin':
      return chain(e, o => makeOperation('cos', o));
    case 'tan':
      return chain(e, o => makeOperation('+', makeConstant(1), makeOperation('^', makeOperation('tan', o), makeConstant(2))));
    case 'exp':
      return chain(e, o => makeOperation('exp', o));
    case 'ln':
      return chain(e, o => makeOperation('/', makeConstant(1), o));
    }
  }
}

function chain(e, fp, gx) {
  return makeOperation('*', fp(e.operands[0]), diffExpr(e.operands[0]));
}

function simplify(e) {
  if (e.type !== 'operation') {
    return e;
  }
  const simplified = makeOperation(e.op, ...e.operands.map(o => simplify(o)));
  // constants only
  if (simplified.operands.every(o => o.type === 'constant')) {
    return makeConstant(evaluateConstantOperation(simplified));
  }
  if (simplified.op === '*') {
    // multiply by zero
    if (isConstant(simplified.operands[0], 0) || isConstant(simplified.operands[1], 0)) {
      return makeConstant(0);
    }
    // multiply by one
    if (isConstant(simplified.operands[0], 1)) {
      return simplified.operands[1];
    }
    if (isConstant(simplified.operands[1], 1)) {
      return simplified.operands[0];
    }
    if (simplified.operands[1].type === 'constant') {
      return makeOperation('*', simplified.operands[1], simplified.operands[0]);
    }
  }
  if (simplified.op === '+') {
    // add zero
    if (isConstant(simplified.operands[0], 0)) {
      return simplified.operands[1];
    }
    if (isConstant(simplified.operands[1], 0)) {
      return simplified.operands[0];
    }
  }
  if (simplified.op === '-') {
    if (isConstant(simplified.operands[1], 0)) {
      return simplified.operands[0];
    }
  }
  if (simplified.op === '^') {
    if (isConstant(simplified.operands[1], 0)) {
      return makeConstant(1);
    }
    if (isConstant(simplified.operands[1], 1)) {
      return simplified.operands[0];
    }
  }
  return simplified;
}

function evaluateConstantOperation(e) {
  switch (e.op) {
  case '+':
    return e.operands[0].value + e.operands[1].value;
  case '-':
    return e.operands[0].value - e.operands[1].value;
  case '*':
    return e.operands[0].value * e.operands[1].value;
  case '/':
    return e.operands[0].value / e.operands[1].value;
  case '^':
    return Math.pow(e.operands[0].value, e.operands[1].value);
  }
}

function makeConstant(value) {
  return { type: 'constant', value };
}

function makeSymbol() {
  return { type: 'symbol' };
}

function makeOperation(op, ...operands) {
  return { type: 'operation', op, operands };
}

function isConstant(e, value) {
  return e.type === 'constant' && e.value === value;
}
