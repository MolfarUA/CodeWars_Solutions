object ExesAndOhs {

  def xo(str: String): Boolean =
    str.count(_.toLower == 'x') == str.count(_.toLower == 'o')
}
__________________________________
object ExesAndOhs {

  def xo(str: String): Boolean =
    str.foldLeft(0) {
      (acc, cur) => cur match {
        case 'x' | 'X' => acc + 1
        case 'o' | 'O' => acc - 1
        case _ => acc
      }
    } == 0
}
__________________________________
object ExesAndOhs {

  def xo(str: String): Boolean =
    str.toLowerCase match { case s => s.count(_ == 'x') == s.count(_ == 'o') }
}
__________________________________
object ExesAndOhs {

  def xo(str: String): Boolean = {
    val res = str.toLowerCase.groupBy(identity).mapValues(_.length)
    res.getOrElse('x',0) == res.getOrElse('o',0)
  }
}
__________________________________
object ExesAndOhs {

  def xo(str: String): Boolean = 
    str.toLowerCase.count(_ == 'o') == str.toLowerCase.count(_ == 'x')
}
__________________________________
object ExesAndOhs {

  def xo(str: String): Boolean = 
    str.foldLeft(0){
      (z, i) => i.toLower match {
        case 'x' => z+1
        case 'o' => z-1
        case _ => z
      }
    } == 0
}
