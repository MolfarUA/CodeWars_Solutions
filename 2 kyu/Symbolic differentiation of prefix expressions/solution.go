package kata

import (
  "fmt"
  "math"
  "strconv"
)

func Diff(expr string) string {
  e, _ := Parse(expr, 0)
  result := DiffAndSimplify(e)
  fmt.Printf("%s => %s\n", e.ToString(), result)
  return result
}

func DiffAndSimplify(e Expression) string {
  d := e.Diff()
  length := len(d.ToString())
  for {
    d = d.Simplify()
    s := d.ToString()
    l := len(s)
    if l == length {
      return s
    }
    length = l
  }
}

func Parse(expr string, start int) (Expression, int) {
  end := len(expr)
  if expr[0] == '(' {
    start++
    end = FindClosingBrace(expr, start)
  }
  if end != -1 {
    return ParseExpression(expr[start:end]), end
  }
  return nil, end
}

func ParseExpression(s string) Expression {
  strs := make([]string, 0)
  str := ""

  for i := 0; i < len(s); i++ {
    c := s[i]
    switch c {
    case '(':
      end := FindClosingBrace(s, i)
      if end == -1 {
        return nil
      }
      strs = append(strs, s[i+1:end])
      i = end + 1
    case ')':
      return nil
    case ' ':
      strs = append(strs, str)
      str = ""
    default:
      str += string(c)
    }
  }
  if len(str) > 0 {
    strs = append(strs, str)
  }
  switch len(strs) {
  case 1:
    // this is either variable or a constant
    if strs[0] == "x" {
      return NewVariable()
    } else {
      n, e := strconv.ParseFloat(strs[0], 64)
      if e == nil {
        return NewNumber(n)
      }
      return nil
    }
  case 2:
    // this is a func
    switch strs[0] {
    case "sin", "cos", "tan", "ln", "exp":
      return NewFunction(strs[0], ParseExpression(strs[1]))
    }

  case 3:
    // this is an operation
    switch strs[0] {
    case "+", "-", "*", "/", "^":
      return NewOperation(strs[0][0], ParseExpression(strs[1]), ParseExpression(strs[2]))
    }
  }
  return nil
}

// func IsNum(c int32) int32 {
//  return c >= '0'
// }

func FindClosingBrace(expr string, pos int) int {
  depth := 0
  for {
    pos++
    switch expr[pos] {
    case ')':
      if depth == 0 {
        return pos
      }
      depth--
    case '(':
      depth++
    }
    if depth < 0 {
      return -1
    }
  }
}

const (
  TypeOperation = 0
  TypeFunc      = 1
  TypeVariable  = 2
  TypeNumber    = 3
  TypeZero      = 4
)

type Expression interface {
  Diff() Expression
  Simplify() Expression
  ToString() string
  Type() int
}

type Operation struct {
  op     byte
  param1 Expression
  param2 Expression
}

func NewOperation(op byte, p1, p2 Expression) *Operation {
  o := new(Operation)
  o.op = op
  o.param1 = p1
  o.param2 = p2

  return o
}

func (o *Operation) Type() int {
  return TypeOperation
}

func (o *Operation) Simplify() Expression {
  type1 := o.param1.Type()
  type2 := o.param2.Type()
  if (type1 == TypeNumber || type1 == TypeZero) && (type2 == TypeNumber || type2 == TypeZero) {
    n1 := GetNumber(o.param1)
    n2 := GetNumber(o.param2)
    switch o.op {
    case '+':
      return NewNumber(n1 + n2)
    case '-':
      return NewNumber(n1 - n2)
    case '*':
      return NewNumber(n1 * n2)
    case '/':
      return NewNumber(n1 / n2)
    case '^':
      return NewNumber(math.Pow(n1, n2))

    }
  }
  if (type1 == TypeZero) || (type2 == TypeZero) {
    switch o.op {
    case '+':
      if type1 == TypeZero {
        return o.param2
      } else {
        return o.param1
      }
    case '*':
      return NewZero()
    }
  }
  if o.op == '*' {
    if type1 == TypeNumber && GetNumber(o.param1) == 1 {
      return o.param2
    } else if type2 == TypeNumber && GetNumber(o.param2) == 1 {
      return o.param1
    }
  }
  if o.op == '^' && type2 == TypeNumber && GetNumber(o.param2) == 1{
    return o.param1
  }
  return NewOperation(o.op, o.param1.Simplify(), o.param2.Simplify())
}

func GetNumber(param Expression) float64 {
  switch param.Type() {
  case TypeNumber:
    return param.(*Number).value
  case TypeZero:
    return 0
  default:
    panic("cannot get number")
  }
}

func (o *Operation) Diff() Expression {
  var n Expression = nil
  switch o.op {
  case '+', '-':
    n = NewOperation(o.op, o.param1.Diff(), o.param2.Diff())
  case '*':
    n = NewOperation('+', NewOperation('*', o.param1.Diff(), o.param2), NewOperation('*', o.param1, o.param2.Diff()))
  case '/':
    if o.param2.Type() == TypeNumber {
      n = NewOperation('*', NewOperation('/', NewNumber(1), NewNumber(2)), o.param1.Diff())
    } else {
      n = NewOperation('/', NewOperation('-', NewOperation('*', o.param1.Diff(), o.param2), NewOperation('*', o.param1, o.param2.Diff())),
        NewOperation('^', o.param2, NewNumber(2)))
    }
  case '^':
    n = NewOperation('*', o.param2,  NewOperation('^', o.param1, NewOperation('-', o.param2, NewNumber(1))))
  }
  return n
}

func (o *Operation) ToString() string {
  return fmt.Sprintf("(%c %s %s)", o.op, o.param1.ToString(), o.param2.ToString())
}

type Function struct {
  fun   string
  param Expression
}

func NewFunction(fun string, param Expression) *Function {
  f := new(Function)
  f.fun = fun
  f.param = param
  return f
}

func (f *Function) Type() int {
  return TypeFunc
}

func (f *Function) Simplify() Expression {
  switch f.param.(type) {
  case *Zero:
    switch f.fun {
    case "sin", "tan":
      return NewZero()
    case "cos", "exp":
      return NewNumber(1)
    }
  default:
    f.param = f.param.Simplify()
  }
  return f
}
func (f *Function) Diff() Expression {
  var n Expression = nil
  switch f.fun {
  case "sin":
    n = NewFunction("cos", f.param)
  case "cos":
    n = NewOperation('*', NewNumber(-1), NewFunction("sin", f.param))
  case "tan":
    n = NewOperation('+', NewNumber(1), NewOperation('^', NewFunction("tan", f.param), NewNumber(2)))
  case "exp":
    n = NewFunction("exp", f.param)
  case "ln":
    n = NewOperation('/', NewNumber(1), f.param)
  }
  switch f.param.(type) {
  case *Zero, *Number:
    return NewZero()
  case *Variable:
    return n
  case *Operation, *Function:
    return NewOperation('*', f.param.Diff(), n)
  }
  return n
}

func (f *Function) ToString() string {
  return fmt.Sprintf("(%s %s)", f.fun, f.param.ToString())
}

type Number struct {
  value float64
}

func NewNumber(value float64) *Number {
  n := new(Number)
  n.value = value
  return n
}

func (n *Number) Type() int {
  return TypeNumber
}

func (n *Number) Diff() Expression {
  return NewZero()
}

func (n *Number) Simplify() Expression {
  return n
}

func (n *Number) ToString() string {
  return fmt.Sprintf("%g", n.value)
}

func (n *Number) Decrement() Expression {
  return NewNumber(n.value - 1)
}

type Variable struct {
}

func NewVariable() *Variable {
  return new(Variable)
}

func (v *Variable) Type() int {
  return TypeVariable
}

func (v *Variable) Diff() Expression {
  return NewNumber(1)
}
func (v *Variable) Simplify() Expression {
  return v
}
func (v *Variable) ToString() string {
  return "x"
}

type Zero struct {
}

func NewZero() *Zero {
  return new(Zero)
}

func (z *Zero) Type() int {
  return TypeZero
}

func (z *Zero) Diff() Expression {
  return z
}

func (z *Zero) Simplify() Expression {
  return z
}

func (z *Zero) ToString() string {
  return "0"
}
______________________________________________
package kata

import (
  "fmt"
  "math"
  "strconv"
)

var current_pos int = 0
var size int = 0
var current_token byte = ' '
var open_enc byte = '('
var open_var byte = 'x'
var open_plus byte = '+'
var open_min byte = '-'
var open_mul byte = '*'
var open_div byte = '/'
var open_pow byte = '^'
var open_sin byte = 's'
var open_cos byte = 'c'
var open_tan byte = 't'
var open_exp byte = 'e'
var open_ln byte = 'l'
var open_blank byte = ' '
var code_src string = ""
var code_derived string = ""
var token_value int = 0
var token_type int = 0
var TRACE_LEVEL = 0
var IDENTATION = -1

type Addition struct {
  firstOperator  *Factor
  secondOperator *Factor
}

func (a0 Addition) read() Addition {
  var a1 Addition
  var f1 Factor
  f1 = f1.read()
  a1.firstOperator = &f1
  var f2 Factor
  f2 = f2.read()
  a1.secondOperator = &f2
  return a1
}

type Subtraction struct {
  firstOperator  *Factor
  secondOperator *Factor
}

func (s0 Subtraction) read() Subtraction {
  var s1 Subtraction
  var f1 Factor
  f1 = f1.read()
  s1.firstOperator = &f1
  var f2 Factor
  f2 = f2.read()
  s1.secondOperator = &f2
  return s1
}

type Multiplication struct {
  firstOperator  *Factor
  secondOperator *Factor
}

func (m0 Multiplication) read() Multiplication {
  var m1 Multiplication
  var f1 Factor
  f1 = f1.read()
  m1.firstOperator = &f1
  var f2 Factor
  f2 = f2.read()
  m1.secondOperator = &f2
  return m1
}

type Division struct {
  firstOperator  *Factor
  secondOperator *Factor
}

func (d0 Division) read() Division {
  var d1 Division
  var f1 Factor
  f1 = f1.read()
  d1.firstOperator = &f1
  var f2 Factor
  f2 = f2.read()
  d1.secondOperator = &f2
  return d1
}

type Pow struct {
  base *Factor
  exp  int
}

func (d0 Pow) read() Pow {
  var d1 Pow
  var f1 Factor
  f1 = f1.read()
  d1.base = &f1
  var f2 Factor
  f2 = f2.read()
  d1.exp = token_value
  return d1
}

type Sin struct {
  base *Factor
}

func (d0 Sin) read() Sin {
  var d1 Sin
  var f1 Factor
  f1 = f1.read()
  d1.base = &f1
  return d1
}

type Cos struct {
  base *Factor
}

func (d0 Cos) read() Cos {
  var d1 Cos
  var f1 Factor
  f1 = f1.read()
  d1.base = &f1
  return d1
}

type Tan struct {
  base *Factor
}

func (d0 Tan) read() Tan {
  var d1 Tan
  var f1 Factor
  f1 = f1.read()
  d1.base = &f1
  return d1
}

type Exp struct {
  base *Factor
}

func (d0 Exp) read() Exp {
  var d1 Exp
  var f1 Factor
  f1 = f1.read()
  d1.base = &f1
  return d1
}

type Ln struct {
  base *Factor
}

func (d0 Ln) read() Ln {
  var d1 Ln
  var f1 Factor
  f1 = f1.read()
  d1.base = &f1
  return d1
}

type Factor struct {
  factorType     int
  operand        byte
  addition       *Addition
  subtraction    *Subtraction
  multiplication *Multiplication
  division       *Division
  pow            *Pow
  sin            *Sin
  cos            *Cos
  tan            *Tan
  exp            *Exp
  ln             *Ln
  value          float64
}

func (f0 Factor) read() Factor {
  IDENTATION++
  var f1 Factor
  f1.operand = next()
  switch f1.operand {
  case open_enc:
    f1 = f1.read()
    next()
  case open_plus:
    f1.factorType = 2
    trace("> read: Plus", 3)
    var inner Addition
    inner = inner.read()
    f1.addition = &inner
  case open_min:
    f1.factorType = 3
    trace("> read: Min", 3)
    var inner Subtraction
    inner = inner.read()
    f1.subtraction = &inner
  case open_mul:
    f1.factorType = 4
    trace("> read: Mul", 3)
    var inner Multiplication
    inner = inner.read()
    f1.multiplication = &inner
  case open_div:
    f1.factorType = 5
    trace("> read: Div", 3)
    var inner Division
    inner = inner.read()
    f1.division = &inner
  case open_pow:
    f1.factorType = 6
    trace("> read: Pow", 3)
    var inner Pow
    inner = inner.read()
    f1.pow = &inner
  case open_sin:
    f1.factorType = 7
    trace("> read: Sin", 3)
    var inner Sin
    inner = inner.read()
    f1.sin = &inner
  case open_cos:
    f1.factorType = 8
    trace("> read: Cos", 3)
    var inner Cos
    inner = inner.read()
    f1.cos = &inner
  case open_tan:
    f1.factorType = 9
    trace("> read: Tan", 3)
    var inner Tan
    inner = inner.read()
    f1.tan = &inner
  case open_exp:
    f1.factorType = 10
    trace("> read: Exp", 3)
    var inner Exp
    inner = inner.read()
    f1.exp = &inner
  case open_ln:
    f1.factorType = 11
    trace("> read: Ln", 3)
    var inner Ln
    inner = inner.read()
    f1.ln = &inner
  case open_var:
    f1.factorType = 1
    trace("> read: Var", 3)
  default:
    f1.factorType = 0
    trace("> read: Const", 3)
    f1.value = float64(token_value)
  }
  IDENTATION--
  return f1
}
func (f0 Factor) derive() Factor {
  IDENTATION++
  var f1 Factor
  switch f0.factorType {
  case 0:
    trace("> derive: Cons", 3)
    f1.factorType = 0
    f1.value = 0
  case 1:
    trace("> derive: Var", 3)
    f1.factorType = 0
    f1.value = 1
  case 2:
    trace("> derive: Add", 3)
    d1 := f0.addition.firstOperator.derive()
    d2 := f0.addition.secondOperator.derive()
    f1 = sum(d1, d2)
  case 3:
    trace("> derive: Sub", 3)
    d1 := f0.subtraction.firstOperator.derive()
    d2 := f0.subtraction.secondOperator.derive()
    f1 = sub(d1, d2)
  case 4:
    trace("> derive: Mul", 3)
    d1 := f0.multiplication.firstOperator.derive()
    d2 := f0.multiplication.secondOperator.derive()
    f1 = sum(mul(d1, *f0.multiplication.secondOperator), mul(*f0.multiplication.firstOperator, d2))
  case 5:
    trace("> derive: Div", 3)
    d1 := f0.division.firstOperator.derive()
    d2 := f0.division.secondOperator.derive()
    numer := sub(mul(d1, *f0.division.secondOperator), mul(*f0.division.firstOperator, d2))
    denom := pow(*f0.division.secondOperator, 2)
    f1 = div(numer, denom)
  case 6:
    trace("> derive: Pow", 3)
    d1 := f0.pow.base.derive()
    var k Factor
    k.factorType = 0
    k.value = float64(f0.pow.exp)
    f2 := pow(*f0.pow.base, f0.pow.exp-1)
    f1 = mul(mul(k, f2), d1)
  case 7:
    trace("> derive: Sin", 3)
    d1 := f0.sin.base.derive()
    f1 = mul(d1, cos(*f0.sin.base))
  case 8:
    trace("> derive: Cos", 3)
    var k Factor
    k.factorType = 0
    k.value = float64(-1)
    d1 := f0.cos.base.derive()
    d1 = mul(k, d1)
    f1 = mul(d1, sin(*f0.cos.base))
  case 9:
    trace("> derive: Tan", 3)
    var k Factor
    k.factorType = 0
    k.value = float64(1)
    d1 := f0.tan.base.derive()
    f1 = mul(d1, sum(k, pow(tan(*f0.tan.base), 2)))
  case 10:
    trace("> derive: Exp", 3)
    d1 := f0.exp.base.derive()
    f1 = mul(d1, f0)
  case 11:
    trace("> derive: Ln", 3)
    var k1 Factor
    k1.factorType = 0
    k1.value = float64(1)
    var k2 Factor
    k2.factorType = 1
    f1 = div(k1, k2)
  }
  IDENTATION--
  return f1
}
func sum(f1 Factor, f2 Factor) Factor {
  IDENTATION++
  var response Factor
  if (f1.factorType == 0) && (f1.value == 0) {
    trace("> Sum: first is zero", 3)
    IDENTATION--
    return f2
  }
  if (f2.factorType == 0) && (f2.value == 0) {
    trace("> Sum: second is zero", 3)
    IDENTATION--
    return f1
  }
  if (f1.factorType == 0) && (f2.factorType == 0) {
    trace("> Sum: both are constants", 3)
    response.factorType = 0
    response.value = f1.value + f2.value
  } else {
    trace("> Sum: some is not constant", 3)
    response.factorType = 2
    var inner Addition
    inner.firstOperator = &f1
    inner.secondOperator = &f2
    response.addition = &inner
  }
  IDENTATION--
  return response
}
func sub(f1 Factor, f2 Factor) Factor {
  IDENTATION++
  var response Factor
  if (f2.factorType == 0) && (f2.value == 0) {
    trace("> Sub: second is zero", 3)
    IDENTATION--
    return f1
  }
  if (f1.factorType == 0) && (f2.factorType == 0) {
    trace("> Sum: both are constants", 3)
    response.factorType = 0
    response.value = f1.value - f2.value
  } else {
    response.factorType = 3
    var inner Subtraction
    inner.firstOperator = &f1
    inner.secondOperator = &f2
    response.subtraction = &inner
  }
  IDENTATION--
  return response
}
func mul(f1 Factor, f2 Factor) Factor {
  IDENTATION++
  var response Factor
  if (f1.factorType == 0) && (f1.value == 0) {
    trace("> Mul: first is zero", 3)
    IDENTATION--
    return response
  }
  if (f1.factorType == 0) && (f1.value == 1) {
    trace("> Mul: first is one", 3)
    IDENTATION--
    return f2
  }
  if (f2.factorType == 0) && (f2.value == 0) {
    trace("> Mul: second is zero", 3)
    IDENTATION--
    return response
  }
  if (f2.factorType == 0) && (f2.value == 1) {
    trace("> Mul: second is one", 3)
    IDENTATION--
    return f1
  }
  if (f1.factorType == 0) && (f2.factorType == 0) {
    trace("> Mul: both are constants", 3)
    response.factorType = 0
    response.value = f1.value * f2.value
  } else {
    trace("> Mul: some is not constant", 3)
    response.factorType = 4
    var inner Multiplication
    inner.firstOperator = &f1
    inner.secondOperator = &f2
    response.multiplication = &inner
  }
  IDENTATION--
  return response
}
func div(f1 Factor, f2 Factor) Factor {
  IDENTATION++
  var response Factor
  if (f1.factorType == 0) && (f1.value == 0) {
    trace("> Div: first is zero", 3)
    IDENTATION--
    return response
  }
  if (f2.factorType == 0) && (f2.value == 1) {
    trace("> Div: second is one", 3)
    IDENTATION--
    return f1
  }
  if (f1.factorType == 0) && (f2.factorType == 0) {
    trace("> Div: both are constants", 3)
    response.factorType = 0
    response.value = f1.value / f2.value
  } else {
    trace("> Div: some is not constant", 3)
    response.factorType = 5
    var inner Division
    inner.firstOperator = &f1
    inner.secondOperator = &f2
    response.division = &inner
  }
  IDENTATION--
  return response
}
func pow(b1 Factor, e1 int) Factor {
  IDENTATION++
  if e1 == 1 {
    return b1
  }
  var response Factor
  if b1.factorType == 0 {
    trace("> Pow: both are constants", 3)
    response.factorType = 0
    response.value = math.Pow(b1.value, float64(e1))
  } else {
    trace("> Pow: some is not constant", 3)
    response.factorType = 6
    var inner Pow
    inner.base = &b1
    inner.exp = e1
    response.pow = &inner
  }
  IDENTATION--
  return response
}
func sin(b1 Factor) Factor {
  IDENTATION++
  var response Factor
  trace("> Sin: var", 3)
  response.factorType = 7
  var inner Sin
  inner.base = &b1
  response.sin = &inner
  IDENTATION--
  return response
}
func cos(b1 Factor) Factor {
  IDENTATION++
  var response Factor
  trace("> Cos: var", 3)
  response.factorType = 8
  var inner Cos
  inner.base = &b1
  response.cos = &inner
  IDENTATION--
  return response
}
func tan(b1 Factor) Factor {
  IDENTATION++
  var response Factor
  trace("> Tan: var", 3)
  response.factorType = 9
  var inner Tan
  inner.base = &b1
  response.tan = &inner
  IDENTATION--
  return response
}
func exp(b1 Factor) Factor {
  IDENTATION++
  var response Factor
  trace("> Exp: var", 3)
  response.factorType = 10
  var inner Exp
  inner.base = &b1
  response.exp = &inner
  IDENTATION--
  return response
}
func ln(b1 Factor) Factor {
  IDENTATION++
  var response Factor
  trace("> Ln: var", 3)
  response.factorType = 11
  var inner Ln
  inner.base = &b1
  response.ln = &inner
  IDENTATION--
  return response
}
func (f Factor) print() string {
  switch f.factorType {
  case 0:
    if f.value == float64(int64(f.value)) {
      return strconv.Itoa(int(f.value))
    }
    return strconv.FormatFloat(float64(f.value), 'f', -1, 64)
  case 1:
    return "x"
  case 2:
    return "(+ " + f.addition.firstOperator.print() + " " + f.addition.secondOperator.print() + ")"
  case 3:
    return "(- " + f.subtraction.firstOperator.print() + " " + f.subtraction.secondOperator.print() + ")"
  case 4:
    return "(* " + f.multiplication.firstOperator.print() + " " + f.multiplication.secondOperator.print() + ")"
  case 5:
    return "(/ " + f.division.firstOperator.print() + " " + f.division.secondOperator.print() + ")"
  case 6:
    return "(^ " + f.pow.base.print() + " " + strconv.Itoa(f.pow.exp) + ")"
  case 7:
    return "(sin " + f.sin.base.print() + ")"
  case 8:
    return "(cos " + f.cos.base.print() + ")"
  case 9:
    return "(tan " + f.tan.base.print() + ")"
  case 10:
    return "(exp " + f.exp.base.print() + ")"
  case 11:
    return "(ln " + f.ln.base.print() + ")"
  }
  return ""
}
func trace(chain string, trace_level int) {
  if trace_level < TRACE_LEVEL {
    prefix := ""
    for i := 0; i < IDENTATION; i++ {
      prefix += ">"
    }
    fmt.Println(prefix + chain)
  }
}
func next() byte {
  current_token = code_src[current_pos]
  if current_token == open_blank {
    current_pos++
    current_token = code_src[current_pos]
  }
  if isNumber() {
    cBegin := current_pos
    for !eof() && isNumber() {
      current_pos++
      i, _ := strconv.Atoi(code_src[cBegin:current_pos])
      token_value = i
    }
  } else {
    current_pos++
    switch current_token {
    case 's':
      current_pos++
      current_pos++
      token_type = 2
    case 'c':
      current_pos++
      current_pos++
      token_type = 3
    case 't':
      current_pos++
      current_pos++
      token_type = 4
    case 'e':
      current_pos++
      current_pos++
      token_type = 5
    case 'l':
      current_pos++
      current_pos++
      token_type = 6
    default:
      token_type = 7
    }
  }
  if current_token == open_blank {
    current_token = code_src[current_pos]
    current_pos++
  }
  return current_token
}
func isNumber() bool {
  b1 := (code_src[current_pos] >= '0') && (code_src[current_pos] <= '9')
  if b1 {
    trace("> isNumber: Yes", 3)
  }
  return b1
}
func initialize(expression string) {
  current_pos = 0
  code_src = expression
  size = len(expression)
  token_value = 0
  code_derived = ""
  IDENTATION = -1
}

func eof() bool {
  return current_pos == size
}

func Diff(expression string) string {
  initialize(expression)
  var f0 Factor
  f0 = f0.read()
  f1 := f0.derive()
  return f1.print()
}
______________________________________________
package kata

import (
  "fmt"
  "math"
  "regexp"
  "strconv"
)

var global_expression string
var simple_derivation map[string]func(...atomic_element) string
var complex_derivation map[string]func(child_node_derivation, original_content string) string

type atomic_element struct {
  element         string
  original_content string
  calc_derivative bool
}

func Diff(expression string) string {
  //if len(expression) == 1 {
    if number, _ := isNumber(string(expression[0])); number {
      return "0"
    }
    if symbol, _ := isSymbol(string(expression[0])); symbol {
      return "1"
    }
  //}
  global_expression = expression
  simple_derivation = map[string]func(...atomic_element) string{
    "+": deriveAddition,
    "-": deriveSubtraction,
    "*": deriveMultiplication,
    "^": derivePow,
    "/": deriveQuotient,
  }

  complex_derivation = map[string]func(string, string) string{
    "cos": deriveCosine,
    "sin": deriveSinus,
    "tan": deriveTangens,
    "exp": deriveExponentiation,
    "ln":  deriveLn,

  }
  _, node := iterate(1)
  return node.derivative
}

func deriveQuotient(elements ...atomic_element) string {
  j := len(elements)-1
  derivatives_string := []string{}
  derivatives_int := []int{}
  for _, element := range elements {
    if element.calc_derivative {
      if symbol, _ := isSymbol(element.element); symbol {
        s := elements[j].element
        if number, _ := isNumber(s); number {
          atoi, _ := strconv.Atoi(s)
          i := 1 * atoi
          derivatives_int = append(derivatives_int, i)
        }
        if b, _ := isSymbol(s); b {
          derivatives_string = append(derivatives_string, fmt.Sprintf("(* %s %s)", element.element, s))
        }
      }
      if number, _ := isNumber(element.element); number {
        derivatives_int = append(derivatives_int, 0)
      }
    } else {
      if number, _ := isNumber(element.element); number {
        s := elements[j].element
        if other_number, _ := isNumber(s); other_number {
          number_one, _ := strconv.Atoi(s)
          number_two, _ := strconv.Atoi(element.element)
          derivatives_int = append(derivatives_int, number_one*number_two)
        }
      }
      if symbol, _ := isSymbol(element.element); symbol {
        s := elements[j].element
        derivatives_string = append(derivatives_string, fmt.Sprintf("(* %s %s)", element.element, s))
      }
    }
    j -= 1
  }
  if len(derivatives_int) > 0 {
    counter := subtractElements(derivatives_int)
    denominator := ""
    if elements[len(elements)-1].original_content!="" {
      denominator = elements[len(elements)-1].original_content
    } else {
      denominator = elements[len(elements)-1].element
    }
    if number, _ := isNumber(denominator); number {
      int_denominator, _:= strconv.Atoi(denominator)
      float_denominator := math.Pow(float64(int_denominator), 2)
      i := float64(counter) / float_denominator
      return fmt.Sprintf("%.1f", i)
    } else {
      return fmt.Sprintf("(/ %d (^ (%s) 2))", counter, denominator)
    }
  }
  return ""
}

func subtractElements(derivatives_int []int) int {
  start_value := derivatives_int[0]
  for i := 1; i < len(derivatives_int); i++ {
    start_value -= derivatives_int[i]
  }
  return start_value
}

func derivePow(elements ...atomic_element) string {
  pow := 1
  constant := 1
  for _, element := range elements {
    if element.calc_derivative {
      if number, _ := isNumber(element.element); number {
        constant, _ = strconv.Atoi(element.element)
        pow = constant - 1
      }
    }
  }
  string_pow := strconv.Itoa(pow)
  string_constant := strconv.Itoa(constant)
  if pow != 1 {
    return fmt.Sprintf("(* %s (^ x %s))", string_constant, string_pow)
  }
  return fmt.Sprintf("(* %s x)", string_constant)
}

func deriveLn(child_node_derivative, original_content string) string {
  if child_node_derivative == "" && original_content == "" {
    return "(/ 1 x)"
  }
  if child_node_derivative != "1" {
    return fmt.Sprintf("(* %s (/ 1 (%s)))", child_node_derivative, original_content)
  }
  return fmt.Sprintf("(/ 1 %s)", original_content)

}

func deriveExponentiation(child_node_derivative, original_content string) string {
  if child_node_derivative == "" && original_content == "" {
    return "(exp x)"
  }
  if child_node_derivative != "1" {
    return fmt.Sprintf("(* %s (exp (%s)))", child_node_derivative, original_content)
  }
  return fmt.Sprintf("(exp %s)", original_content)

}

func deriveTangens(child_node_derivative, original_content string) string {
  if child_node_derivative == "" && original_content == "" {
    return "(+ 1 (^ (tan x) 2))"
  }
  if child_node_derivative != "1" {
    return fmt.Sprintf("(* %s (+ 1 (^ (tan (%s)) 2)))", child_node_derivative, original_content)
  }
  return fmt.Sprintf("(+ 1 (^ (tan %s) 2))", original_content)

}

func deriveCosine(child_node_derivative, original_content string) string {
  if child_node_derivative == "" && original_content == "" {
    return "(* -1 (sin x))"
  }
  if child_node_derivative != "1" {
    return fmt.Sprintf("(* %s (* -1 (sin (%s))))", child_node_derivative, original_content)
  }
  return fmt.Sprintf("(* -1 (sin (%s)))", original_content)
}

func deriveSinus(child_node_derivative, original_content string) string {
  if child_node_derivative == "" && original_content == "" {
    return "(cos x)"
  }
  if child_node_derivative != "1" {
    return fmt.Sprintf("(* %s (cos (%s)))", child_node_derivative, original_content)
  }
  return fmt.Sprintf("(cos (%s))", original_content)
}

func deriveMultiplication(elements ...atomic_element) string {
  symbol_counter := 0
  constant_elements := []string{}
  child_elements := ""
  for _, element := range elements {
    if element.calc_derivative {
      if symbol, _ := isSymbol(element.element); symbol {
        symbol_counter++
      } else {
        constant_elements = append(constant_elements, element.element)
      }
    } else {
      if number, _ := isNumber(element.element); number {
        constant_elements = append(constant_elements, element.element)
      } else {
        child_elements = element.element
      }
    }
  }
  constants := multiply_symbol_constants(constant_elements...)
  if child_elements != "" {
    itoa := strconv.Itoa(constants)
    return fmt.Sprintf("(* %s %s)", itoa, child_elements)
  }
  if len(constant_elements) == 0 && symbol_counter != 0 {
    return strconv.Itoa(symbol_counter)
  }
  if len(constant_elements) != 0 && symbol_counter == 0 {
    return strconv.Itoa(multiply_symbol_constants(constant_elements...))
  }
  //constants := multiply_symbol_constants(constant_elements...)
  itoa := strconv.Itoa(symbol_counter * constants)
  return itoa
}

func add_constants(elements ...string) int {
  finalValue := 0
  for _, element := range elements {
    atoi, _ := strconv.Atoi(element)
    finalValue += atoi
  }
  return finalValue
}

func multiply_symbol_constants(elements ...string) int {
  finalValue := 1
  for _, element := range elements {
    atoi, _ := strconv.Atoi(element)
    finalValue *= atoi
  }
  return finalValue
}

func deriveSubtraction(elements ...atomic_element) string {
  var start_value int
  if elements[0].calc_derivative {
    if symbol, _ := isSymbol(elements[0].element); symbol {
      start_value = 1
    } else {
      start_value = 0
    }
  } else {
    atoi, _ := strconv.Atoi(elements[0].element)
    start_value = atoi
  }

  for i := 1; i < len(elements); i++ {
    if symbol, _ := isSymbol(elements[i].element); symbol {
      start_value -= 1
    }
  }
  return strconv.Itoa(start_value)
}

func deriveAddition(elements ...atomic_element) string {
  derived_elements := []string{}
  for _, element := range elements {
    if element.calc_derivative {
      if symbol, _ := isSymbol(element.element); symbol {
        derived_elements = append(derived_elements, "1")
      }
    } else {
      derived_elements = append(derived_elements, element.element)
    }
  }
  constants := add_constants(derived_elements...)
  return strconv.Itoa(constants)
}

type Node struct {
  operator         string
  elements         []atomic_element
  original_content string
  derivative       string
  childNodes       []Node
}

func (n *Node) derive() {

  if f, ok := simple_derivation[n.operator]; ok {
    n.derivative = f(n.elements...)
    return
  }
  if f, ok := complex_derivation[n.operator]; ok {
    if n.childNodes != nil {
      n.derivative = f(n.childNodes[0].derivative, n.childNodes[0].original_content)
    } else {
      n.derivative = f("", "")
    }
    return
  }
}

func iterate(i int) (int, Node) {
  start_index_recursion := i
  operator := string(global_expression[i])
  var elements []atomic_element
  var childNode Node
  var childNodes []Node
  if letter, _ := isLetter(operator); letter {
    which_operator := check_which_operator(operator)
    operator = which_operator
    i += len(operator) - 1
  }
  for i := i + 1; i < len(global_expression); i+= 1 {
    if global_expression[i] != 32 && global_expression[i] != 40 && global_expression[i] != 41 {
      var element_to_append string
      if number, _:= isNumber(string(global_expression[i])); number {
        var i_counter int
        i_counter, element_to_append = search_up_to_next_number(i)
        i = i_counter
      }else {
        element_to_append = string(global_expression[i])
      }
      elements = append(elements, atomic_element{
        element:         element_to_append,
        calc_derivative: true,
      })
    }
    if global_expression[i] == '(' {
      i, childNode = iterate(i + 1)
      childNodes = append(childNodes, childNode)
      elements = append(elements, atomic_element{element: childNode.derivative, original_content: childNode.original_content, calc_derivative: false})
    }
    if global_expression[i] == ')' {
      end_index_recursion := i
      original_content := global_expression[start_index_recursion:end_index_recursion]
      node := Node{
        operator:         operator,
        elements:         elements,
        childNodes:       childNodes,
        original_content: original_content,
      }
      node.derive()
      return i + 1, node
    }
  }
  childNode = Node{}
  return 0, childNode
}

func funcName() int {
  return 1
}

func search_up_to_next_number(s int) (int, string) {
  for i := s; i < len(global_expression); i++ {
    number, _ := isNumber(string(global_expression[i]))
    if number {
      continue
    } else {
      return i, global_expression[s:i]
    }
  }
  return 0, ""
}

func isSpace(s string) (bool, error){
  return regexp.MatchString("\\s", s)
}

func check_which_operator(operator string) string {
  switch operator {
  case "s":
    return "sin"
  case "c":
    return "cos"
  case "t":
    return "tan"
  case "e":
    return "exp"
  case "l":
    return "ln"
  }
  return ""
}

func isSymbol(element string) (bool, error) {
  return regexp.MatchString("^x*$", element)
}

// Check whether operator is cos, sin, tan, exp or ln
func isLetter(operator string) (bool, error) {
  return regexp.MatchString("[a-z]", operator)
}

func isNumber(element string) (bool, error) {
  return regexp.MatchString("^\\d*$", element)
}
