import scala.annotation.tailrec

object BinomialExpansion {

  @tailrec
  def factorial(n: Int, acc: Int = 1, factorials: List[Long] = List(1)): List[Long] = {
    val newFactorials = factorials :+ factorials.last * acc
    if (acc >= n) newFactorials
    else factorial(n, acc + 1, newFactorials)
  }
  
  def parseA(s: String): Int = {
    s match {
      case "" => 1
      case "-" => -1
      case other => s.toInt
    }
  }
  
  def parseB(s: String): Int = {
    val sign = if (s(0) == '-') -1 else 1
    sign * s.drop(1).toInt
  }
  
  def expand(expr: String): String = {
    val pIndex = expr.indexOf("^")
    val n = expr.drop(pIndex + 1).toInt
    val base = expr.take(pIndex).drop(1).dropRight(1)
    val x = base.replaceAll("[^a-zA-Z]", "")
    val xIndex = base.indexOf(x)
    val a = parseA(base.take(xIndex))
    val b = parseB(base.drop(xIndex + 1))
    
    val factorials = factorial(n)
    
    def parseAnswer(l: List[Long]): String = {
      @tailrec
      def parseAux(l: List[Long], s: String = ""): String = {
        if (l.length == 0) s
        else {
          val sign = if (l(0) >= 0) "+" else ""
          val coef = l(0).toString match {
            case "1" => if(l.length == 1) "1" else ""
            case "-1" => if(l.length == 1) "-1" else "-"
            case x => x
          }
          val suffix = l.length match {
            case 1 => ""
            case 2 => x
            case other => x + "^" + (l.length - 1)
          }
          val term = if (coef == "0") "" else (sign.concat(coef).concat(suffix))
          parseAux(l.tail, s + term)
        }
      }
      val answer = parseAux(l)
      if(answer(0) == '+') answer.drop(1)
      else answer
    }
    
    def asPowersList(p: Int, acc: List[Long] = List()): List[Long] = {
      if (p == -1) acc
      else {
        val k = n - p
        val bin = factorials(n)/(factorials(k) * factorials(p))
        val c = bin * math.pow(a, p).toLong * math.pow(b, k).toLong
        asPowersList(p-1, acc :+ c)
      }
    }
    
    parseAnswer(asPowersList(n))
  }
}

___________________________________________________
object BinomialExpansion {

  type Member = (Long, Option[String])

  def expand(expr: String): String = {
    val p = "\\(([+-]?\\d*[a-zA-Z]*)([+-]?\\d*[a-zA-Z]*)\\)\\^(\\d+)".r
    val p(x, y, z) = expr
    val (m1, m2) = (parse(x), parse(y))
    coef(z.toInt).map({
      case (f, e1, e2) => product(pow(m1, e1), pow(m2, e2), f)
    })
      .filter(e => e._1 != 0)
      .map(mkString)
      .foldLeft("")(join)
  }

  def join(s1: String, s2: String): String = (s1, s2) match {
    case ("", a) => a
    case (a, b) if b.startsWith("-") => a + b
    case (a, b) => a + "+" + b
  }

  def product(m1: Member, m2: Member, f: Long): Member = product(m1, product(m2, f))

  def product(m1: Member, m2: Member): Member = (
    m1._1 * m2._1,
    Some(m1._2.filterNot(_ => m1._1 == 0).getOrElse("") + m2._2.filterNot(_ => m2._1 == 0).getOrElse("")).filterNot(_.isEmpty)
  )

  def product(m: Member, i: Long): Member = (m._1 * i, m._2)

  def pow(m: Member, e: Int): Member = (
    scala.math.pow(m._1, e).toLong,
    e match {
      case 0 => None
      case 1 => m._2
      case _ => m._2 map (_ + s"^$e")
    }
  )

  def mkString(m: Member): String = (m._1.toString, m._2) match {
    case ("0", _) => ""
    case ("1", x) => x.getOrElse("1")
    case ("-1", x) => "-" + x.getOrElse("1")
    case (i, o) => i + o.getOrElse("")
  }

  def parse(x: String): Member = {
    val p = "([+-]?\\d*)([a-zA-Z]*)".r
    val p(n, l) = x
    val f = n match {
      case "-" => -1
      case "" => 1
      case _ => n.toInt
    }
    (f, Option(l).filter(_ != ""))
  }

  def coef(pow: Int): IndexedSeq[(Long, Int, Int)] = (0 to pow).map(i => (choose(pow, i), pow - i, i))

  def choose(n: Int, k: Int): Long =
    if (k == 0 || k == n) 1
    else choose(n - 1, k - 1) + choose(n - 1, k)
}

___________________________________________________
object BinomialExpansion {

  def expand(expr: String): String = {
    val split = expr.replace(" ", "").split('^')
    val term = split(0).substring(1, split(0).length - 1) // substring removes brackets

    // split(1) is the power
    split(1).toLong match {
      case 0L => "1"
      case 1L => term
      case n =>
        // split variable and constant terms, along with signs
        val eq = term.replace("+", " +")
          .replace("-", " -").split(" ").filter(_.nonEmpty)
        //eq = ax + b
        val ax = eq(0)
        val (a, x) = ax.splitAt(ax.length - 1)
        // If a is empty, or just the + or - operator, append a 1 at the end
        val A = (if (a.exists(_.isDigit)) a else a + "1").toLong
        val B = eq(1).toLong
        if (B == 0) {
          // if B was 0, input expr was (Ax)^n, which is simply A^n*x^n
          val cf = Math.pow(A, n).toLong
          // if coefficient is 1 or -1, "hide" the 1
          if (cf == 1) s"$x^$n"
          else if (cf == -1) s"-$x^$n"
          else s"$cf$x^$n"
        } else {

          var r = 0L
          var nCr = 1L

          var res = ""
          while (r <= n) {
            // Math.pow returns a double. .toLong drops the pesky .0
            val coefficient = nCr * Math.pow(A, n - r).toLong * Math.pow(B, r).toLong
            // "hide" 1 in coefficient, and add in an artificial + is needed
            val cf =
              if (coefficient == 1) "+"
              else if (coefficient == -1) "-"
              else if (coefficient < 0) coefficient.toString
              else /*if (coefficient > 0)*/ s"+$coefficient" // Note that neither a nor b is 0 here. Thus coefficient is never 0


            res += (n - r match {
              case 0 =>
                // when power is 0, x term vanishes, leaving only constant.
                // If the constant is empty or is only + or -, append a 1
                if (cf.exists(_.isDigit)) cf else s"${cf}1"
              case 1 =>
                // "hide" something^1
                s"$cf$x"
              case p => s"$cf$x^$p"
            })

            r += 1
            // Note that nCr = nC(r-1) * (n - r + 1) / r
            // Doing multiplication and division separately ensure precision
            nCr *= n - r + 1
            nCr /= r
          }

          // Remove artificially added +, if it's at the begining of the result
          if (res.startsWith("+")) res.replaceFirst("\\+", "") else res
        }
    }
  }


}
