export const calc = (expression: string): number => {
  let result = expression;
  while (/[()]/.test(result)) {
    result = result.replace(/\(([^()]+)\)/g, ($, $1) => String(calc($1)));
  }

  while (/[*/]/.test(result)) {
    result = result.replace(/([\d.]+)\s*([*/])\s*(-*[\d.]+)/, ($, $1, $2, $3) =>
      String($2 === "*" ? calc($1) * calc($3) : calc($1) / calc($3))
    );
  }

  const regExp = /(-*[\d.]+)\s*([+-])\s*(-*[\d.]+)/;
  while (regExp.test(result)) {
    result = result.replace(regExp, ($, $1, $2, $3) =>
      String($2 === "+" ? calc($1) + calc($3) : calc($1) - calc($3))
    );
  }

  return Number(result.replace(/-\s*-/g, ""));
}

____________________________________________________
const hasScob = /^(.*)\((.*?)\)(.*)$/;

const div = (exp: string): number => exp.split('/').map(Number).reduce((a, b) => a / b);

const mul = (exp: string): number => exp.split('*').map(div).reduce((a, b) => a * b);

const sub = (exp: string): number => exp.replace(/(?<=\D|^)--/, '').split(/(?<=\d)-/).map(mul).reduce((a, b) => a - b);

const add = (exp: string): number => exp.split('+').map(sub).reduce((a, b) => a + b);

export const calc = (exp: string): number => {
  exp = exp.replace(/ +/g, '');
  
  for (let match = exp.match(hasScob); match; match = exp.match(hasScob)) {
    const [_, left, core, right] = match;
    exp = left + calc(core) + right;
  }
  
  return add(exp);
}
______________________________________________
const ops: {op: string, fn: (a: number, b: number) => number}[] = [
  {op: "+", fn: (a, b) => a + b}, 
  {op: "~", fn: (a, b) => a - b}, 
  {op: "*", fn: (a, b) => a * b}, 
  {op: "/", fn: (a, b) => a / b}
];
const b = (v: string): string => {
  let s = v.replace(/[-~]{2}/g,"+").replace(/\/\+/g, "/")
    .replace(/\(([^()]*)\)/g, (_, x) => `${cal(x)}`);
  return s == v ? s : b(s);
}
const cal = (v: string, [{op, fn}, ...r] = ops): number => 
  v.split(op).map(r[0] ? v => cal(v, r) : Number).reduce(fn);
export const calc = (e: string): number => 
  cal(b(e.replace(/\s/g, "").replace(/([^*/]|^)(-)/g, "$1~")));
____________________________________
const get = (v: string) => parseFloat(v);
const ops: Record<string, (a: string, b: string) => number> = {
  '*': (a, b) => get(a) * get(b),
  '/': (a, b) => get(a) / get(b),
  '+': (a, b) => get(a) + get(b),
  '-': (a, b) => get(a) - get(b),
}

const steps: Parameters<string['replace']>[] = [
  [/ /g, () => ''],
  [/--|\++/g, () => '+'],
  [/\(([+-]?[\d.]+)\)/g, (_, v) => String(get(v))],
  [/(-?[\d.]+)([*/])([+-]?[\d.]+)/, (_, a, o, b) => String(ops[o](a, b))],
  [/(-?[\d.]+)([+-])([+-]?[\d.]+)/, (_, a, o, b) => String(ops[o](a, b))],
];

export const calc = (expr: string): number => {
  while (!/^-?[\d.]+$/.test(expr)) {
    for (let i = 0; i < steps.length; i++) {
      const next = expr.replace(...steps[i]);
      if (next != expr) i = 0;
      expr = next;
    }
  }
  return get(expr);
}
____________________________________________________
export function calc(expression: string): number {
  const tokens = tokenize(expression);
  const exp = parse(tokens);
  return exp.evaluate();
};

function parse(tokens: any): any {
  function split(i: any): any { return [tokens.slice(0, i), tokens.slice(i + 1), tokens[i]]; }
  function flat(): any {
    let j: any = 0;
    const res: any = [];
    for (let i: any = 0; i < tokens.length; i++) {
      if (tokens[i].kind == TokenKind.OPEN) j++;
      else if (tokens[i].kind == TokenKind.CLOSE) j--;
      else if (j == 0) res.push([i, tokens[i]]);
    }
    return res;
  }
  function findBinaryExp(): any {
    const operators = flat().filter(function(t: any) { return t[1].kind == TokenKind.BINARY; });
    if (operators.length == 0) return null;
    let j: any = 0;
    let precedence: any = Number.MAX_VALUE;
    for (let i: any = 0; i < operators.length; i++) {
      if (operators[i][1].precedence > precedence) break;
      j = operators[i][0];
      precedence = operators[i][1].precedence;
    }
    const binOp: any = split(j);
    return new BinaryExpression(parse(binOp[0]), parse(binOp[1]), binOp[2].symbols);
  }
  const binExp: any = findBinaryExp();
  if (binExp != null) return binExp;
  if (tokens[0].kind == TokenKind.UNARY) 
    return new UnaryExpression(parse(tokens.slice(1)), tokens[0].symbols);
  if (tokens[0].kind == TokenKind.NUMBER) 
    return new NumberExpression(Number(tokens[0].symbols));
  if (tokens[0].kind == TokenKind.OPEN)
    return parse(tokens.slice(1, tokens.length-1));
}

function tokenize(input: any): any {
  const tokens: any = [];
  let pos: any = 0;
  let lastToken: any = null;
  function done (i: any=0): any { return pos+i >= input.length; }
  function la (i: any=0) :any { return input[pos+i];}
  function isNumber (s: any): any { return /[0-9.]/.test(s); }
  function isNoise (t: any): any { return t.kind == TokenKind.WS; }
  function push (t: any): any { tokens.push(t); if (!isNoise(t)) lastToken = t; }
  for (; !done(); pos++) {
    let symbols: any = la();
    let i: any = pos;
    switch (symbols) {
      case "(": { push(new Token( TokenKind.OPEN, i, symbols )); break; }
      case ")": { push(new Token( TokenKind.CLOSE, i, symbols )); break; }
      case "+": { push(new BinaryToken( i, symbols )); break; }
      case "*": { push(new BinaryToken( i, symbols )); break; }
      case "/": { push(new BinaryToken( i, symbols )); break; }
      case " ": {
        while (!done(1) && la(1) == " ") {
          pos++;
          symbols += la();
        }
        push(new Token(TokenKind.WS, i, symbols));
        break;
      }
      default: {
        if (la() == "-") {
          if (lastToken != null) {
            if (lastToken.kind == TokenKind.CLOSE) {
              push(new BinaryToken(i, symbols));
              continue;
            } else if (lastToken.kind == TokenKind.NUMBER) {
              push(new BinaryToken(i, symbols));
              continue;
            }
          }
          if (!done(1) && la(1) == "(") {
            push(new Token(TokenKind.UNARY, i, symbols));
            continue;
          }
          pos++;
          symbols += la();
        }
        if (isNumber(la())) {
          while (!done(1) && isNumber(la(1))) {
            pos++;
            symbols += la();
          }
          push(new Token(TokenKind.NUMBER, i, symbols));
        }
        break;
      }
    }
  }
  return tokens.filter(function(t: any) {return t.kind!=TokenKind.WS;});
}

class NumberExpression {
  num: any;
  constructor(num: any) { this.num = num; }
  evaluate(): any { return this.num; }
}

class UnaryExpression {
  down: any;
  symbol: any;
  constructor(down: any, symbol: any) { this.down = down; this.symbol = symbol; }
  evaluate(): any {
    switch (this.symbol) {
      case "-": return - this.down.evaluate();
    }
  }
}

class BinaryExpression {
  left: any;
  right: any;
  symbol: any;
  constructor(left: any, right: any, symbol: any) { this.left = left; this.right = right; this.symbol = symbol; }
  evaluate(): any {
    switch (this.symbol) {
      case "+": return this.left.evaluate() + this.right.evaluate();
      case "-": return this.left.evaluate() - this.right.evaluate();
      case "*": return this.left.evaluate() * this.right.evaluate();
      case "/": return this.left.evaluate() / this.right.evaluate();
    }
  }
}

class Token {
  kind: any;
  pos: any;
  symbols: any;
  constructor(kind: any, pos: any, symbols: any) {
    this.kind = kind;
    this.pos = pos;
    this.symbols = symbols;
  }
}

class BinaryToken extends Token {
  precedence: any;
  constructor(pos: any, symbols: any) {
    super(TokenKind.BINARY, pos, symbols)
    switch (this.symbols) {
      case "+":
      case "-":
        this.precedence = 10; break;
      case "*":
      case "/":
        this.precedence = 20; break;
    }
  }
}

const TokenKind = {
  NUMBER : "number",
    OPEN : "open",
   CLOSE : "close",
   UNARY : "unary",
  BINARY : "binary",
      WS : "whitespace",
}
