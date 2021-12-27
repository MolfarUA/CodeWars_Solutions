function calc(expr) {

    var expressionToParse = expr.replace(/\s+/g, '').split('');
    
    function peek() {
        return expressionToParse[0] || '';
    }
    
    function get() {
        return expressionToParse.shift();
    }
    
    function number() {
        var result = get();
        while (peek() >= '0' && peek() <= '9' || peek() == '.') {
            result += get();
        }
        return parseFloat(result);
    }
    
    function factor() {
        if (peek() >= '0' && peek() <= '9') {
            return number();
        } else if (peek() == '(') {
            get(); // '('
            var result = expression();
            get(); // ')'
            return result;
        } else if (peek() == '-') {
            get();
            return -factor();
        }
        return 0; // error
    }
    
    function term() {
        var result = factor();
        while (peek() == '*' || peek() == '/') {
            if (get() == '*') {
                result *= factor();
            } else {
                result /= factor();
            }
        }
        return result;
    }
    
    function expression() {
        var result = term();
        while (peek() == '+' || peek() == '-') {
            if (get() == '+') {
                result += term();
            } else {
                result -= term();
            }
        }
        return result;
    }

    return expression();
}
________________________________________________
var calc = function (expression) {
  var tokens = expression.match(/\d+\.\d+|\d+|[-+*/\(\)]/g).map(function(t){ return isNaN(t) ? t : Number(t); });
  function accept(sym){ return (tokens[0] == sym) && tokens.shift() }
  function acceptNumber(){ return !isNaN(tokens[0]) && tokens.shift() }
  function acceptAny(arr){ return arr.some( function(a){ return a == tokens[0]} ) && tokens.shift() }
  function doOp(x, op, y){ return [function(a,b){ return a + b;}, function(a,b){ return a - b; }, function(a,b){ return a * b; }, function(a,b){ return a / b; }][("+-*/".indexOf(op))](x,y); }
  function unit(){ return accept('(') ? (e = expr(), accept(')'), e) : acceptNumber(); }
  function unary(){ return accept('-') ? -unit() : unit(); }
  function factor(){ for (var x = unary(); op = acceptAny(['*','/']); x = doOp(x, op, unary())); return x; }
  function expr(){ for (var x = factor(); op = acceptAny(['+','-']); x = doOp(x, op, factor())); return x; }
  return expr();
};
_________________________________________________
calc=e=>HODOR(e);HODOOR=Object.keys;String.prototype.H0D0R = String.prototype.includes;String.prototype.HODOR = String.prototype.replace;String.prototype.H0DOR=String.prototype.split;hODOr=RegExp;HoD0R=Number;

var HOD0OR = {
  '\u002F' : {HODOR:"\u002F", HoDOR: (H0DOR,H0D0R)=>HoD0R(H0DOR)/HoD0R(H0D0R)},
  '\u002A' : {HODOR:"\\\u002A", HoDOR: (H0DOR,H0D0R)=>HoD0R(H0DOR)*HoD0R(H0D0R)},
  '\u002D' : {HODOR:"\u002D", HoDOR: (H0DOR,H0D0R)=>HoD0R(H0DOR)-HoD0R(H0D0R)},
  '\u002B' : {HODOR:"\\\u002B", HoDOR: (H0DOR,H0D0R)=>HoD0R(H0DOR)+HoD0R(H0D0R)}
}

function HODOR(hOdOR){
  hOdOR=HODOr(hOdOR);
  return hOdOR.H0D0R("(") ? 
          HODOR(hOdOR.HODOR(/\([^()]+\)/g,HoDOr=>HODoR(HoDOr).HODOR(/[(|)]+/g,""))) : 
            HoD0R(HODoR(hOdOR));
};

function HODoR(hOdOR){
  HODOOR(HOD0OR).forEach(H0D0R=>{
    hodor = hODOr(`-*(\\d+\\.*\\d*)+${HOD0OR[H0D0R].HODOR}-*(\\d+\\.*\\d*)+`);
    while(hOdOR.includes(H0D0R)&& hodor.test(hOdOR)){
      hOdOR = HODOr(hOdOR).HODOR(hodor,H0DOR=>HOD0OR[H0D0R].HoDOR(...(H0DOR.H0DOR(H0D0R))))
    }
  });
  return hOdOR;
}

const HODOr=(hOdOR)=>hOdOR.HODOR(/\s/g,"").HODOR(/(--)+-/g,"-").HODOR("--","+").HODOR("+-+","-").HODOR(/\++/g,"+").HODOR("/+","/").HODOR("*+","*");
____________________________________________
function calc(s){
var [rPS,rAS,rMD]=[/(-)?\(([^(]+?)\)/g,/(-?\d+(?:\.\d+)?) *([+\-]) *(-?\d+(?:\.\d+)?)/g,/(-?\d+(?:\.\d+)?) *([*\/]) *(-?\d+(?:\.\d+)?)/g]
while(rPS.test(s))
s=s.replace(rPS,(v,a,b)=>(a?-1:1)*calc(b));
while(rMD.test(s))
s=s.replace(rMD,(v,a,o,b)=>o=="*"?+a*+b:+a/+b);
while(rAS.test(s))
s=s.replace(rAS,(v,a,o,b)=>o=="-"?+a-+b:+a+ +b);
return +s;
}
_____________________________________________
const OPERATIONS = ['+', '-', '*', '/'];
const DIGITS = "1234567890";

const calc = (expression) => {
  if (!isNaN(expression)) return Number(expression);
  
  if (expression.includes("(")) {
    const newExpression = expression.replace(/\(([^)^(]+)\)/, (match, expr) => calc(expr));
    return calc(newExpression);
  }
  
  expression = expression.replace(/- -|--/g, "+");
  
  let operation = OPERATIONS.filter(op => expression.includes(op))[0];
  let index = expression.indexOf(operation);
  
  if (operation === "-" || operation === "+") {
    if (!DIGITS.includes(expression[index-1])) {
      for (let i = 1; i <= 2; i += 1) {
        if (OPERATIONS.includes(expression[index-i])) {
          operation = expression[index-i];
          index -= i;
          break;
        }
      }
    }
  }
  
  const left = expression.substr(0, index);
  const right = expression.substr(index + 1);
  
  return applyOperation(calc(left), calc(right), operation);
};

const applyOperation = (a, b, op) => {
  if (op === "+") return a + b;
  if (op === "-") return a - b;
  if (op === "*") return a * b;
  if (op === "/") return a / b;
}
