55aa075506463dac6600010d


object SumSquaredDivisors {

  val cache = collection.mutable.Map[Long, Option[String]]()

  def listSquared(m: Long, n: Long): String =
    (m to n)
      .flatMap { k =>
        cache.getOrElseUpdate(
          k,
          {
            val divisorsSum = (1L to k).collect { case d if (k.toDouble / d).isWhole => d*d }.sum
            Option.when(math.sqrt(divisorsSum).isWhole)(s"[$k, $divisorsSum]")
          }
        )
      }
      .mkString("[", ", ", "]")
}
________________________________
object SumSquaredDivisors {

  def listSquared(m: Long, n: Long): String = {
    val numbersWithDivSum = (m to n) map { num => num -> divisorsSum(num) } filter (p => math.sqrt(p._2).isWhole)
    numbersWithDivSum map { case (num, divSum) => s"[$num, ${divSum.toLong}]" } mkString("[", ", ", "]")
  }

  def divisorsSum(number: Long): Double = divisors(number).map(d => d * d).sum
  def divisors(number: Long): Seq[Long] = ((1L to number / 2L) filter (i => number % i == 0)) :+ number
}
________________________________
object SumSquaredDivisors {

  def listSquared(m: Long, n: Long): String = {
    val result = (m to n)
       .map(x => (x, getDivisors(x).map(xx => xx*xx).sum))
       .filter(isSquare)
       .map(pair => s"[${pair._1}, ${pair._2}]")
       .mkString(", ")
    s"[$result]"
  }
  
  def isSquare(tuple: Tuple2[Long, Long]): Boolean = {
    Math.sqrt(tuple._2).toInt * Math.sqrt(tuple._2).toInt == tuple._2
  }
  
  def getDivisors(n: Long): Set[Long] = {
    (1 to Math.sqrt(n).toInt)
       .filter(n % _ == 0)
       .flatMap(divisor => List(divisor, n / divisor))
       .toSet
  }
}
