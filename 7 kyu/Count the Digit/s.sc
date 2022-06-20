566fc12495810954b1000030


object CountDig {

  def nbDig(n: Int, d: Int): Int = {
    (0 to n).flatMap(i => (i*i).toString).count(j => j.asDigit==d)
  }
}
____________________________
object CountDig {

  def nbDig(n: Int, d: Int): Int =
    (for (k <- 0 to n) yield (k * k).toString.map(_.asDigit).count(_ == d)).sum
}
____________________________
object CountDig {

  def nbDig(n: Int, d: Int): Int =
    (0 to n).map(i => i*i).mkString.count(_ == '0' + d)
}
