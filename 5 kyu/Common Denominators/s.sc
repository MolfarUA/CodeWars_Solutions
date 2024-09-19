54d7660d2daf68c619000d95


object Fracts {

  def convertFrac(lst: Array[(Long, Long)]): String = {
    def reduceFraction(f: (Long, Long)): (Long, Long) =
      f match { case (n, d) => val div = gcd(n, d); (n/div, d/div) }
    
    def gcd(a: Long, b: Long):Long=if (b==0) a.abs else gcd(b, a%b)
    def lcm(a: Long, b: Long)=(a*b).abs/gcd(a,b)
    
    val reducedFractions = lst.map(reduceFraction)
    val commonDenominator = reducedFractions.map(_._2).reduceLeft(lcm)
    reducedFractions.map { case (n, d) => (n * (commonDenominator/d), commonDenominator) }.mkString
  }
}
#################################
object Fracts {
  def gcd(a: Long, b: Long): Long = if (b == 0) a else gcd(b, a % b)
  def lcm(a: Long, b: Long): Long = a * b / gcd(a, b)
  
  def convertFrac(lst: Array[(Long, Long)]): String = {
    val updated = lst.map(t => (t._1 / gcd(t._1, t._2), t._2 / gcd(t._1, t._2)) )
    val den = updated.foldLeft(1L)( (acc, next) => lcm(acc, next._2))
    updated.map(t => s"(${t._1 * (den / t._2)},${den})").mkString
  }
}

##################################
object Fracts {
  def gcd(a: Long, b: Long): Long =
    if (b == 0) a else gcd (b, a % b)
  
  def lcm(a: Long, b: Long): Long =
    a * b / gcd(a, b)

  def convertFrac(lst: Array[(Long, Long)]): String = {
    val m = lst.foldLeft(1L) { case (acc, (n, d)) => lcm(acc, d / gcd(n, d)) }
    lst.map { case (n, d) => s"(${(n * (m * 1.0 / d)).toLong},$m)"}.mkString
  }
}
################################
object Fracts {
  def gcd(a: Long, b: Long): Long = if (b == 0) a else gcd(b, a % b)

  def lcm(a: Long, b: Long): Long = (a * b) / gcd(a, b)
  
  def convertFrac(lst: Array[(Long, Long)]): String = {
    if (lst.isEmpty) return ""
    val d = lst.foldLeft(1L) { (acc, n) =>
      lcm(acc, n._2 / gcd(n._1, n._2))
    }
    val res = lst.map { n =>
      val num = n._1 * d / n._2
      s"($num,$d)"
    }
    res.mkString("")
  }
}
