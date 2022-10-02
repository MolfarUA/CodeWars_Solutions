55c6126177c9441a570000cc


object WeightSort {

  def orderWeight(str: String): String =
    str.split(" ").sortBy(d => (d.map(_.asDigit).sum, d)).mkString(" ")
}
______________________________
object WeightSort {

  def orderWeight(s: String): String = {
    s.split(' ').sortBy(s => (s.map(_.asDigit).sum, s)).mkString(" ")
  }
}
______________________________
object WeightSort {

  def orderWeight(strng: String): String = strng.split(" ").sortBy(r => (r.map(_.toInt - 48).sum, r)).mkString(" ")
}
______________________________
object WeightSort {

  def orderWeight(strng: String): String = {
  if (strng.trim == "") "" // Handling the code for input empty string
    else {
    val outputTuple =  strng.split(" ").map(x => (x, x.toString.split("").map(_.toInt).sum))
    val output = outputTuple.sortBy(x => (x._2,x._1)).map(_._1).mkString(" ")
    output}
}}
