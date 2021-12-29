object Kata {

  def alphabetPosition(text: String): String =
    text.filter(_.isLetter).map(_.toLower - 96).mkString(" ")
}

________________________________________________
object Kata {
  def alphabetPosition(text: String): String =
    text.filter(_.isLetter).map(_.toLower - 'a' + 1).mkString(" ")
}

________________________________________________
object Kata {

  def alphabetPosition(text: String): String =
    text.collect { case c if c.isLetter => c.toLower - 96 }.mkString(" ")
}

________________________________________________
object Kata {

  val LetterOffset = 96;

  def alphabetPosition(text: String): String = {
    text.foldLeft(Seq.empty[Int])((res, curr) => {
      if (curr.isLetter) res :+ (curr.toLower.toInt - LetterOffset) else res
    }).mkString(" ");
  }
}

________________________________________________
object Kata {

  val alphabet = " abcdefghijklmnopqrstuvwxyz"

  def alphabetPosition(text: String): String = 
    text
      .toLowerCase
      .map(c => alphabet.indexOf(c))
      .filter(_ > 0)
      .mkString(" ")
}

________________________________________________
object Kata {

  def alphabetPosition(text: String): String = 
   text.toUpperCase().replaceAll("[^A-Z]","").flatMap(x => s"${x.toInt - 64} ").trim
}
