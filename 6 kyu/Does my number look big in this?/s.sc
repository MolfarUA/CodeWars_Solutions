object Kata {

  def narcissistic(n: Int): Boolean =
    n == n.toString.map(i => math.pow(i.asDigit, n.toString.size)).sum
}
________________________
object Kata {

  def narcissistic(n: Int): Boolean = n.toString.map(x => scala.math.pow(x.asDigit, n.toString.length)).sum == n
}
________________________
object Kata {

  def narcissistic(n: Int): Boolean = {
    val digits = n.toString.map(_.asDigit)
    val power = digits.length

    digits.map { digit =>
      scala.math.pow(digit, power)
    }.sum.toInt == n
  }
}
________________________
object Kata {

  def narcissistic(n: Int): Boolean =
    n == s"$n".map(i => math.pow(i.asDigit, s"$n".size)).sum
}
________________________
object Kata {

  def narcissistic(n: Int): Boolean = {
    val nStr = n.toString
    val power = nStr.length
    nStr.map(x => Math.pow(x - '0', power)).reduce(_ + _) == n
  }
}
