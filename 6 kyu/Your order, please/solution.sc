object Text {

  def order(str: String): String =
    str.split(' ').sortBy(_.find(_.isDigit)).mkString(" ")
}

_____________________________________________
object Text {

  def order(str: String): String =
    str.split(' ').sortBy(_.sorted).mkString(" ")
}

_____________________________________________
object Text {

  val IntRegEx = "(\\d+)".r

  def order(str: String): String = str.split(" ").sortBy{w => IntRegEx.findFirstIn(w).map(_.toInt).getOrElse(10)}.mkString(" ")
}

_____________________________________________
object Text {
  def numberInWord(s: String): Int = s.filter(_.isDigit)(0)
  def order(str: String): String = str.split(" ").sortWith(numberInWord(_) < numberInWord(_)).reduce(_+" "+_)
}

_____________________________________________
object Text {
  def order(str: String): String = str match {
    case "" => ""
    case _ => str.split(" ")
      .map(word => (word, word.filter(_.isDigit).head.asDigit))
      .sortBy(_._2).map(_._1).mkString(" ")
  }
}
