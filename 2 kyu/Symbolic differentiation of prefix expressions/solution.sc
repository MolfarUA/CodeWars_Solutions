object PrefixDiff {
    
  def diff(expr: String): String = 
      pars(expr).differentiate.toString
  
    trait Expression {
      val args: List[Expression]
      val command: Command
      def eval: Expression
      def differentiate: Expression
      override def toString: String = s"(${command.name}${if (args.length > 0) " " else ""}${args.mkString(" ")})"
    }

    trait Command {
      val name: String
      override def toString: String = name
    }

    abstract class Term(val name: String) extends Expression with Command {
      val command: Term = this
      val eval: Term = this
      val args = List(command)
    }

    case object NAN extends Term("NAN") {
      def differentiate = NAN
    }

    case object NULL extends Term("") {
      def differentiate = NULL
    }

    case class Constant(c: Double) extends Term(if (c.toLong.toDouble == c) c.toLong.toString else c.toString) {
      def differentiate: Expression = Constant(0)
    }

    case class Variable(v: String) extends Term(v) {
      def differentiate: Expression = Constant(1)
    }

    abstract class Op(arg1: Expression, arg2: Expression, val name: String) extends Command with Expression {
      val args = List(arg1, arg2)
      val command = this
    }

    case class Minus(m1: Expression, m2: Expression) extends Op(m1, m2, "-") {
      def eval = Plus(m1, Times(m2, Constant(-1))).eval
      def differentiate = eval.differentiate
    }

    case class Plus(t1: Expression, t2: Expression) extends Op(t1, t2, "+") {
      def differentiate = {
        val t1d = t1.eval.differentiate
        val t2d = t2.eval.differentiate
        t1d match {
          case Constant(t) => if (t == 0) t2d else Plus(t1d, t2d).eval
          case _ => Plus(t1d, t2d).eval
        }
      }
      def eval = {
        (t1.eval, t2.eval) match {
          case (Constant(0), a) => a
          case (a, Constant(0)) => a
          case (Constant(a), Constant(b)) => Constant(a + b)
          case (Variable(a), Variable(b)) => if (a == b) Times(Variable(a), Constant(2)) else this
          case (a@Variable(_), b@Constant(_)) => Plus(a, b)
          case (a@Constant(_), b@Variable(_)) => Plus(a, b)
          case (Plus(a, b), Plus(c, d)) => Plus(Plus(a, c).eval, Plus(b, d).eval)
          case (a, b) => if (a == t1 && b == t2) this else Plus(a, b).eval
        }
      }
    }
  
    case class Times(t1: Expression, t2: Expression) extends Op(t1, t2, "*") {
      def differentiate = {
        val fPrime = t1.eval.differentiate
        val gPrime = t2.eval.differentiate
        (t1.eval, t2.eval) match {
          case (Constant(a), Variable(_)) => Constant(a)
          case (Variable(_), Constant(a)) => Constant(a)
          case (f, g) => Plus(Times(f, gPrime).eval, Times(g, fPrime).eval).eval //product rule
        }
      }
      def eval = {
        (t1.eval, t2.eval) match {
          case (Constant(0), _) | (_, Constant(0)) => Constant(0)
          case (Constant(1), a) => a
          case (b, Constant(1)) => b
          case (Constant(a), Constant(b)) => Constant(a * b)
          case (Constant(a), Times(Constant(b), c)) => Times(Constant(a*b), c)
          case (Constant(a), Times(b, Constant(c))) => Times(Constant(a*c), b)
          case (a@Variable(_), b@Variable(_)) => if (a.name == b.name) Power(a, Constant(2)) else Times(a, b)
          case (a, b) => if (a == t1 && b == t2) Times(a, b) else Times(a, b).eval
        }
      }
    }

    case class Divide(t1: Expression, t2: Expression) extends Op(t1, t2, "/") {
      def differentiate = {
        val fPrime = t1.eval.differentiate
        val gPrime = t2.eval.differentiate
        (t1.eval, t2.eval) match {
          case (a@Constant(_), b@Variable(_)) => Divide(Times(a, Constant(-1)).eval, Power(b, Constant(2)).eval).eval
          case (Variable(_), b@Constant(_)) => Divide(Constant(1), b).eval
          case (f, g) => Divide(Minus(Times(fPrime, g).eval, Times(f, gPrime).eval).eval, Power(g, Constant(2)).eval).eval //quotient rule
        }
      }
      def eval = {
        (t1.eval, t2.eval) match {
          case (Constant(0), _) => Constant(0)
          case (_, Constant(0)) => NAN
          case (b, Constant(1)) => b
          case (Constant(a), Constant(b)) => Constant(a / b)
          case (a@Variable(_), b@Variable(_)) => if (a.name == b.name) Constant(1) else Divide(a, b)
          case (a, b) => if (a == t1 && b == t2) Divide(a, b) else Divide(a, b).eval
        }
      }
    }

    case class Power(t1: Expression, t2: Expression) extends Op(t1, t2, "^") {
      def differentiate = {
        lazy val protoDiff = Times(Times(t2, Power(t1, Minus(t2, Constant(1)).eval).eval).eval, t1.differentiate).eval
        t2.eval match {
          case Constant(t) => if (t == 0) Constant(0) else protoDiff
          case _ => protoDiff
        }
      }
  
      def eval = {
        (t1.eval, t2.eval) match {
          case (Constant(0), _) => Constant(0)
          case (_, Constant(0)) => Constant(1)
          case (Constant(1), _) => Constant(1)
          case (b, Constant(1)) => b
          case (Constant(a), Constant(b)) => Constant(math.pow(a, b))
          case (a, b) => if (a == t1 && b == t2) Power(a, b) else Power(a, b).eval
        }
      }
    }

    abstract class Fn(arg1: Expression, val name: String, constHandler: Double => Double, val cmd: Expression => Fn) extends Command with Expression {
      val args = List(arg1)
      def eval = arg1.eval match {
        case Constant(a) => Constant(constHandler(a))
        case a => cmd(a)
      }
  
      val command = this
    }
  
    def ChainRule(f: Expression => Expression, gOfx: Expression) = {
      //f(g(x)) ==> f’(g(x))g’(x)
      Times(f(gOfx).differentiate, gOfx.differentiate).differentiate
    }
  
    case class Sin(t1: Expression) extends Fn(t1, "sin", a => math.sin(a), a => Sin(a)) {
      override def differentiate: Expression = //ChainRule(x => Cos(x), t1)
        Times(t1.eval.differentiate, Cos(t1.eval)).eval
    }
  
    case class Cos(t1: Expression) extends Fn(t1, "cos", a => math.cos(a), a => Cos(a)) {
      override def differentiate: Expression = Times(t1.eval.differentiate, Times(Constant(-1), Sin(t1.eval))).eval
    }

    case class Tan(t1: Expression) extends Fn(t1, "tan", a => math.tan(a), a => Tan(a)) {
      override def differentiate: Expression = Times(t1.eval.differentiate, Plus(Constant(1), Power(Tan(t1.eval), Constant(2)))).eval
  
      //(+ 1 (^ (tan x) 2))
      //Divide(Constant(1), Power(Cos(t1.eval).eval, Constant(2)).eval).eval
    }

    case class Exp(t1: Expression) extends Fn(t1, "exp", a => math.pow(math.E, a), a => Exp(a)) {
      override def differentiate: Expression = Times(t1.eval.differentiate, Exp(t1.eval)).eval
  
    }
  
    case class Ln(t1: Expression) extends Fn(t1, "ln", a => math.log(a), a => Ln(a)) {
      override def differentiate: Expression = Times(t1.eval.differentiate, Divide(Constant(1), t1.eval).eval).eval
    }

      def pars(s: String) = {
        println(s"pars $s")

      def parseConstant(s: String): Option[Expression] = {
        val p = """-?[0-9]+\.?[0-9]*""".r
        println(s"parseConst $s")
        if (p.matches(s)) Some(Constant(s.toDouble)) else None
      }

      def parseVariable(s: String): Option[Expression] = {
        val p = """[a-zA-Z]""".r
        println(s"parseVariable $s")
        if (p.matches(s)) Some(Variable(s)) else None
      }

      def parseFn(s: String, t: Expression): Option[Expression] = {
        println(s"parseFn $s")
        s match {
          case "sin" => Some(Sin(t))
          case "cos" => Some(Cos(t))
          case "tan" => Some(Tan(t))
          case "exp" => Some(Exp(t))
          case "ln" => Some(Ln(t))
          case _ => None
        }
      }

      def parseOp(s: String, t1: Expression, t2: Expression): Expression = {
        println(s"parseOp $s")
        s match {
          case "+" => Plus(t1, t2)
          case "-" => Minus(t1, t2)
          case "*" => Times(t1, t2)
          case "/" => Divide(t1, t2)
          case "^" => Power(t1, t2)
          case _ => NULL
        }
      }

      val expression = s.filterNot(i => i == '(' || i == ')').split(" ").reverse

      def process(stack: List[Expression], expression: Array[String]): Expression = {
        if (expression.isEmpty) stack.head
        else {
          val nxt = parseConstant(expression.head)
            .getOrElse(parseVariable(expression.head)
              .getOrElse(parseFn(expression.head, stack.head)
                .getOrElse(parseOp(expression.head, stack.head, stack.tail.head))))
          nxt match {
            case _: Constant | _: Variable => process(nxt :: stack, expression.tail)
            case _: Fn => process(nxt :: stack.tail, expression.tail)
            case _: Op => process(nxt :: stack.tail.tail, expression.tail)
          }
        }
      }

      process(List[Expression](), expression)
    }  
}
______________________________________________
object PrefixDiff {
  
    def isPolynom(s: String): Boolean = s.last == 'x'
  
    def isNumber(s: String): Boolean = s.forall(_.isDigit)
  
    def formatNumber(d: Double): String = if (d.isWhole) d.toInt.toString else d.toString 
  
    def formatPolynom(s: String): String = if (s.length == 1) "1" else s.dropRight(1)
  
    def chain(a: String, raw: String) = s"(* ${diffAux(a)} $raw)"
  
    def diffAux(expr: String): String = {

      def simpleDerivative(a: String): String = {
        a match {
          case "x" => "1"
          case x => "0"
        }
      }
      
      def sum(a: String, b: String): String = s"(+ ${diffAux(a)} ${diffAux(b)})"
      
      def difference(a: String, b: String): String = s"(- ${diffAux(a)} ${diffAux(b)})"
      
      def product(a: String, b: String): String = {
        val x = {
          val dA = diffAux(a)
          if (dA == "0") "0" else s"(* $b $dA)"
        }
        val y = {
          val dB = diffAux(b)
          if (dB == "0") "0" else s"(* $a $dB)"
        }
        s"(+ $x $y)"
      }
      
      def quotient(a: String, b: String): String = {
        val x = {
          val x0 = {
            val dA = diffAux(a)
            if (dA == "0") "0" else s"(* $b $dA)"
          }
          val x1 = {
            val dB = diffAux(b)
            if (dB == "0") "0" else s"(* $a $dB)"
          }
          s"(- $x0 $x1)"
        }
        val y = s"(^ $b 2)"
         s"(/ $x $y)"
      }
      
      def sin(a: String): String = chain(a, s"(cos $a)")
      
      def cos(a: String): String = chain(a, s"(* -1 (sin $a))")
      
      def tan(a: String): String = chain(a, s"(+ 1 (^ (tan $a) 2))")
      
      def exp(a: String): String = chain(a, s"(exp $a)")
      
      def ln(a: String): String = chain(a, s"(/ 1 $a)")
      
      def pow(a: String, b: String): String = chain(a, s"(* $b (^ $a (- $b 1)))")
      
      val args = {
        val noBrackets = if (expr(0) == '(') expr.drop(1).dropRight(1) else expr
        def parse(s: String, scoped: Boolean = false, acc: List[String] = List()): List[String] = {
          if (s == "") acc
          else {
            if (scoped) {
              val scanned = s.split("").toList.scan("(")(_ + _)
              val end = scanned.indexWhere(x => x.count(_ == '(') == x.count(_ == ')'))
              val message = scanned(end)
              parse(s.drop(end), !scoped, acc :+ message)
            }
            else {
              val end = s.indexOf("(")
              val message = if (end == -1) s else s.take(end)
              val parsed = message.split(" ").filter(_ != "")
              parse(s.drop(message.length + 1), !scoped, acc ++ parsed)
            }
          }
        }
        parse(noBrackets)
      }
      
      args(0) match {
        case "+" => sum(args(1), args(2))
        case "-" => difference(args(1), args(2))
        case "*" => product(args(1), args(2))
        case "/" => quotient(args(1), args(2))
        case "^" => pow(args(1), args(2))
        case "cos" => cos(args(1))
        case "sin" => sin(args(1))
        case "tan" => tan(args(1))
        case "exp" => exp(args(1))
        case "ln" => ln(args(1))
        case x => simpleDerivative(x)
      }
    }
  
    def diff(expr: String): String = {
      def evaluate(expr: String): String = {
        def sum(a: String, b: String): String = {
          (evaluate(a), evaluate(b)) match {
            case (x, y) if x == "0" => y
            case (x, y) if y == "0" => x
            case (x, y) if isNumber(x) && isNumber(y) => formatNumber(x.toDouble + y.toDouble)
            case (x, y) if isPolynom(x) && isPolynom(y) => formatNumber(formatPolynom(x).toDouble + formatPolynom(y).toDouble) ++ "x"
            case (x, y) => s"(+ $x $y)"
          }
        }

        def difference(a: String, b: String): String = {
          (evaluate(a), evaluate(b)) match {
            case (x, y) if x == "0" => "-" + y
            case (x, y) if y == "0" => x
            case (x, y) if isNumber(x) && isNumber(y) => formatNumber(x.toDouble - y.toDouble)
            case (x, y) if isPolynom(x) && isPolynom(y) => formatNumber(formatPolynom(x).toDouble - formatPolynom(y).toDouble) ++ "x"
            case (x, y) => s"(- $x $y)"
          }
        }

        def product(a: String, b: String): String = {
          (evaluate(a), evaluate(b)) match {
            case (x, y) if x == "1" => y
            case (x, y) if y == "1" => x
            case (x, y) if x == "0" || y == "0" => "0"
            case (x, y) if isNumber(x) && isNumber(y) => formatNumber(x.toDouble * y.toDouble)
            case (x, y) => s"(* $x $y)"
          }
        }

        def quotient(a: String, b: String): String = {
          (evaluate(a), evaluate(b)) match {
            case (x, y) if y == "1" => x
            case (x, y) if x == "0" => "0"
            case (x, y) if isNumber(x) && isNumber(y) => formatNumber(x.toDouble / y.toDouble)
            case (x, y) => s"(/ $x $y)"
          }
        }

        def sin(a: String): String = s"(sin ${evaluate(a)})"

        def cos(a: String): String = s"(cos ${evaluate(a)})"

        def tan(a: String): String = s"(tan ${evaluate(a)})"

        def exp(a: String): String = s"(exp ${evaluate(a)})"

        def ln(a: String): String = s"(ln ${evaluate(a)})"

        def pow(a: String, b: String): String = {
          (evaluate(a), evaluate(b)) match {
            case (x, y) if x == "1" => "1"
            case (x, y) if y == "1" => x
            case (x, y) if y == "0" => "1"
            case (x, y) if x == "0" => "0"
            case (x, y) if isNumber(x) && isNumber(y) => formatNumber(math.pow(x.toDouble, y.toDouble))
            case (x, y)  => s"(^ $x $y)"
          }
        }

        val args = {
          val noBrackets = if (expr(0) == '(') expr.drop(1).dropRight(1) else expr
          def parse(s: String, scoped: Boolean = false, acc: List[String] = List()): List[String] = {
            if (s == "") acc
            else {
              if (scoped) {
                val scanned = s.split("").toList.scan("(")(_ + _)
                val end = scanned.indexWhere(x => x.count(_ == '(') == x.count(_ == ')'))
                val message = s.take(end - 1)
                parse(s.drop(end), !scoped, acc :+ message)
              }
              else {
                val end = s.indexOf("(")
                val message = if (end == -1) s else s.take(end)
                val parsed = message.split(" ").filter(_ != "")
                parse(s.drop(message.length + 1), !scoped, acc ++ parsed)
              }
            }
          }
          parse(noBrackets)
        }

        args(0) match {
          case "+" => sum(args(1), args(2))
          case "-" => difference(args(1), args(2))
          case "*" => product(args(1), args(2))
          case "/" => quotient(args(1), args(2))
          case "^" => pow(args(1), args(2))
          case "cos" => cos(args(1))
          case "sin" => sin(args(1))
          case "tan" => tan(args(1))
          case "exp" => exp(args(1))
          case "ln" => ln(args(1))
          case x => x
        }
      }
      
      val diffExpanded = diffAux(expr)
      evaluate(diffExpanded)
    }
}
______________________________________________
object PrefixDiff {
  def isx(str: String): Boolean = str.indexOf("x")==(-1)
  def split(str: String): List[String]= {
    if(str.indexOf(" ")==(-1)) return List(str)
    if(str(1)=='+' || str(1)=='-'|| str(1)=='*' || str(1)=='/' || str(1)=='^') {

      val helpStr = str.substring(3,str.length-1).trim
      if(!helpStr.startsWith("(")) return List(str(1).toString,
        helpStr.substring(0,helpStr.indexOf(" ")),
          helpStr.substring(helpStr.indexOf(" ")+1)
      )
      var pointer = 0;
      var col = 0;
      do{
        if(helpStr(pointer)=='(') col+=1;
        if(helpStr(pointer)==')') col-=1;
        pointer+=1
      } while (col !=0)
      return List(
        str(1).toString,
        helpStr.substring(0,pointer),
        helpStr.substring(pointer+1)
      )
    }
    List(str.substring(1, str.indexOf(" ")), str.substring(str.indexOf(" ")+1, str.length-1))
  }
  def add(l: List[String]):String = {
    val x1 = diff(l(1))
    val x2 = diff(l(2))
    if(x1.indexOf("x")==(-1) && x2.indexOf("x")==(-1)) return s"${x1.toInt+x2.toInt}"
    if(x1.indexOf("x")==(-1) && x1.toInt==0) return s"${x2.toInt}"
    if(x2.indexOf("x")==(-1) && x2.toInt==0) return s"${x1.toInt}"
    s"(+ $x1 $x2)"
  }
  def dif(l: List[String]):String = {
    val x1 = diff(l(1))
    val x2 = diff(l(2))
    if(x1.indexOf("x")==(-1) && x2.indexOf("x")==(-1)) return s"${x1.toInt-x2.toInt}"
    if(x1.indexOf("x")==(-1) && x1.toInt==0) return s"(* -1 $x2)"
    if(x2.indexOf("x")==(-1) && x2.toInt==0) return s"$x1"
    s"(- $x1 $x2)"
  }
  def mul(l: List[String]):String ={
    val x11 = diff(l(1))
    val x12 = l(2)
    val x21 = diff(l(2))
    val x22 = l(1)
    var x1 =if(isx(x12)) s"(* $x12 $x11)" else s"(* $x11 $x12)"
    var x2=if(isx(x22)) s"(* $x22 $x21)" else s"(* $x21 $x22)"

    if((x11.indexOf("x")==(-1) && x11.toInt==0) || (x12.indexOf("x")==(-1) && x12.toInt==0)) x1 = "0"
    if((x21.indexOf("x")==(-1) && x21.toInt==0) || (x22.indexOf("x")==(-1) && x22.toInt==0)) x2 = "0"

    if(x11.indexOf("x")==(-1) && x12.indexOf("x")==(-1)) x1 = s"${x11.toInt*x12.toInt}"
    if(x21.indexOf("x")==(-1) && x22.indexOf("x")==(-1)) x2 = s"${x21.toInt*x22.toInt}"

    if(x1.indexOf("x")==(-1) && x2.indexOf("x")==(-1)) return s"${x1.toInt+x2.toInt}"
    if(isx(x1) && x1.toInt==0) return x2
    if(isx(x2) && x2.toInt==0) return x1

    s"(+ $x1 $x2)"
  }

  def div(l: List[String]):String ={
    val x11 = diff(l(1))
    val x12 = l(2)
    val x21 = diff(l(2))
    val x22 = l(1)
    var x1 =if(isx(x12)) s"(* $x12 $x11)" else s"(* $x11 $x12)"
    var x2=if(isx(x22)) s"(* $x22 $x21)" else s"(* $x21 $x22)"
    var num = s"(+ $x1 $x2)"
    val denum =if (isx(x12)) s"${x12.toInt*x12.toInt}" else s"(^ $x12 2)"

    if((x11.indexOf("x")==(-1) && x11.toInt==0) || (x12.indexOf("x")==(-1) && x12.toInt==0)) x1 = "0"
    if((x21.indexOf("x")==(-1) && x21.toInt==0) || (x22.indexOf("x")==(-1) && x22.toInt==0)) x2 = "0"

    if(x11.indexOf("x")==(-1) && x12.indexOf("x")==(-1)) x1 = s"${x11.toInt*x12.toInt}"
    if(x21.indexOf("x")==(-1) && x22.indexOf("x")==(-1)) x2 = s"${x21.toInt*x22.toInt}"

    if(x1.indexOf("x")==(-1) && x2.indexOf("x")==(-1)) num= s"${x1.toInt-x2.toInt}"
    if(isx(x1) && x1.toInt==0) num = s"-$x2"
    if(isx(x2) && x2.toInt==0) num= x1

    if(isx(num) && isx(denum)) return s"${num.toDouble/denum.toDouble}"
    s"(/ $num $denum)"
  }

  def pow(l: List[String]):String ={
    val t = if (l(2).toInt==2) s"(* 2 ${l(1)})" else s"(* ${l(2)} (^ ${l(1)} ${l(2).toInt-1}))"
    if(l(1).length==1 || split(l(1))(0)=="+" || split(l(1))(0)=="-") return t
    else s"(* $t ${diff(l(1))})"
  }
  def sin(l: List[String]):String = if(l(1).length==1 || split(l(1))(0)=="+" || split(l(1))(0)=="-") s"(cos ${l(1)})"
  else s"(* ${split(l(1))(1)} (cos ${l(1)}))"
  def cos(l: List[String]):String = if(l(1).length==1 || split(l(1))(0)=="+" || split(l(1))(0)=="-") s"(* -1 (sin ${l(1)}))"
  else s"(* ${split(l(1))(1)} (* -1 (sin ${l(1)})))"
  def tan(l: List[String]):String =if(l(1).length==1 || split(l(1))(0)=="+" || split(l(1))(0)=="-") s"(+ 1 (^ (tan ${l(1)}) 2))"
  else s"(* ${split(l(1))(1)} (+ 1 (^ (tan ${l(1)}) 2)))"
  def exp(l: List[String]):String = if(l(1).length==1 || split(l(1))(0)=="+" || split(l(1))(0)=="-") s"(exp ${l(1)})"
  else s"(* ${split(l(1))(1)} (exp ${l(1)}))"
  def log(l: List[String]):String = if(l(1).length==1 || split(l(1))(0)=="+" || split(l(1))(0)=="-") s"(/ 1 ${l(1)})"
  else s"(* ${split(l(1))(1)} (/ 1 ${l(1)}))"


  def diff(expr: String):String = {
    val parsedStr = split(expr)
    parsedStr.head match {
      case "+" => add(parsedStr)
      case "-" => dif(parsedStr)
      case "*" => mul(parsedStr)
      case "/" => div(parsedStr)
      case "x" => "1"
      case _ if parsedStr.length==1 => "0"
      case "^" => pow(parsedStr)
      case "sin" => sin(parsedStr)
      case "cos" => cos(parsedStr)
      case "tan" => tan(parsedStr)
      case "exp" => exp(parsedStr)
      case "ln" => log(parsedStr)
      case _ => s"Error(${parsedStr.mkString(" ")})"
    }
  }
  }
______________________________________________
object PrefixDiff {
    def diff(expr: String): String = mkString(operate(diff(Parser(expr)._1)))

  def diff(expr: Expression): Expression = expr match {
    case const(_) => const(0)
    case X => const(1)
    case ++(a, b) => ++(diff(a), diff(b))
    case --(a, b) => --(diff(a), diff(b))
    case **(a, b) => ++(**(diff(a), b), **(a, diff(b)))
    case div(a, b) => div(--(**(diff(a), b), **(a, diff(b))), pow(b, const(2)))
    case pow(a, b) => **(**(b, pow(a, --(b, const(1)))), diff(a))
    case cos(a) => **(diff(a), **(const(-1), sin(a)))
    case sin(a) => **(diff(a), cos(a))
    case tan(a) => **(diff(a), ++(const(1), pow(tan(a), const(2))))
    case exp(a) => **(diff(a), exp(a))
    case ln(a) => div(diff(a), a)
  }

  def operate(expr: Expression): Expression = {
    val expression = expr match {
      case ++(pow(sin(a), const(2)), pow(cos(b), const(2))) if a == b => const(1)
      case ++(pow(cos(a), const(2)), pow(sin(b), const(2))) if a == b => const(1)
      case ++(const(0), x) => x
      
      case ++(const(a), const(b)) => const(a + b)
      case ++(a, b) => ++(operate(a), operate(b))
      
      case --(a, b) if a == b => const(0)
      case --(const(a), const(b)) => const(a - b)
      case --(a, b) => --(operate(a), operate(b))

      case **(const(0), _) | **(_, const(0)) => const(0)
      case **(const(1), a) => a
      case **(a, const(1)) => a
      
      case **(a, b) => **(operate(a), operate(b))

      case div(const(0), _) => const(0)
      case div(a, const(1)) => a
      case div(a, b) if a == b => const(1)
      case div(a, b) => div(operate(a), operate(b))

      case pow(const(a), const(b)) => const(math.pow(a, b).toInt)
      case pow(const(0), _) => const(0)
      case pow(_, const(0)) => const(1)
      case pow(a, const(1)) => a
      case pow(a, b) => pow(operate(a), operate(b))

      case sin(const(a)) if a % math.Pi == 0 => const(0)
      case sin(a) => sin(operate(a))

      case cos(const(a)) if a % (math.Pi / 2) == 0 => const(0)
      case cos(a) => cos(operate(a))

      case tan(const(a)) if a % math.Pi == 0 => const(0)
      case tan(a) => tan(operate(a))

      case exp(const(0)) => const(1)
      case exp(ln(a)) => a
      case exp(a) => exp(operate(a))

      case ln(const(1)) => const(0)
      case ln(exp(a)) => a
      case ln(a) => ln(operate(a))

      case _ => expr
    }
    if (expression != expr) operate(expression) else expr
  }

  def mkString(expr: Expression): String = expr match {
    case exp(a) => s"(exp ${mkString(a)})"
    case tan(a) => s"(tan ${mkString(a)})"
    case cos(a) => s"(cos ${mkString(a)})"
    case sin(a) => s"(sin ${mkString(a)})"
    case ++(a, b) => s"(+ ${mkString(a)} ${mkString(b)})"
    case --(a, b) => s"(- ${mkString(a)} ${mkString(b)})"
    case **(a, b) => s"(* ${mkString(a)} ${mkString(b)})"
    case div(const(a), const(b)) => (a.toDouble / b).toString
    case div(a, b) => s"(/ ${mkString(a)} ${mkString(b)})"
    case pow(a, b) => s"(^ ${mkString(a)} ${mkString(b)})"
    case const(a) => a.toString
    case X => "x"
  }

  sealed trait Expression

  case class const(value: Int) extends Expression

  case object X extends Expression

  case class ++(a: Expression, b: Expression) extends Expression

  case class --(a: Expression, b: Expression) extends Expression

  case class **(a: Expression, b: Expression) extends Expression

  case class div(a: Expression, b: Expression) extends Expression

  case class pow(a: Expression, b: Expression) extends Expression

  case class cos(a: Expression) extends Expression

  case class sin(a: Expression) extends Expression

  case class tan(a: Expression) extends Expression

  case class exp(a: Expression) extends Expression

  case class ln(a: Expression) extends Expression

  object Parser {
    @scala.annotation.tailrec
    def apply(expr: String): (Expression, String) = expr.headOption match {
      case Some(c) if c.isDigit | c == '-' =>
        val (numb, tail) = getNumber(expr.tail)
        (const((c + numb).toInt), tail)
      case Some('x') => (X, expr.tail)
      case Some('(') =>
        expr.substring(1) match {
          case s"$s $t0" =>
            if (s.length == 1) {
              parseBi(s, t0)
            } else {
              parseMono(s, t0)
            }
        }
      case Some(' ') | Some(')') => Parser(expr.tail)
    }

    def parseMono(s: String, t0: String): (Expression, String) = {
      val f = s match {
        case "cos" => e => cos(e)
        case "sin" => e => sin(e)
        case "tan" => e => tan(e)
        case "exp" => e => exp(e)
        case "ln" => e => ln(e)
      }
      val (e, t) = Parser.apply(t0)
      (f(e), t.tail)
    }

    def parseBi(s: String, t0: String): (Expression, String) = {
      val f = s match {
        case "+" => (e1, e2) => ++(e1, e2)
        case "-" => (e1, e2) => --(e1, e2)
        case "*" => (e1, e2) => **(e1, e2)
        case "/" => (e1, e2) => div(e1, e2)
        case "^" => (e1, e2) => pow(e1, e2)
      }
      val (e1, t1) = Parser.apply(t0)
      val (e2, t2) = Parser(t1)
      (f(e1, e2), t2.tail)
    }

    def getNumber(expr: String): (String, String) = expr.headOption match {
      case Some(c) if c.isDigit =>
        val (num, tail) = getNumber(expr.tail)
        (c + num, tail)
      case _ => ("", expr)
    }
  }
}
