object CamelCase {

  def toCamelCase(str: String): String = str.split("[_-]").reduce((a, b) => a + b.capitalize)
}
________________________
object CamelCase {
  val toCamelCase = "[_-](.)".r.replaceAllIn(_: String, _.group(1).toUpperCase)
}
________________________
object CamelCase {

  def toCamelCase(str: String): String = {
    val splitted = str.split("-|_")  
    (splitted.head ++ splitted.tail.map(word => word.capitalize)).mkString("") 
  }
}
________________________
object CamelCase {

  def toCamelCase(str: String): String =
    s"""${str.take(1)}${str.split("[-_]").map(_.capitalize).mkString.drop(1)}""" 
}
________________________
import scala.annotation.tailrec

object CamelCase {

  def toCamelCase(s: String): String =
    toCamelCase(s.toList, Nil).reverse.mkString

  @tailrec
  def toCamelCase(input: List[Char], output: List[Char]): List[Char] = {
    input match {
      case Nil                    => output
      case ('_' | '-') :: Nil     => output
      case ('_' | '-') :: s :: xs => toCamelCase(xs, s.toUpper :: output)
      case s :: xs                => toCamelCase(xs, s :: output)
    }
  }
}
