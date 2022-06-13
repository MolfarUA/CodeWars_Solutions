object Kata {
  def createPhoneNumber(numbers: Seq[Int]) = {
    "(%d%d%d) %d%d%d-%d%d%d%d".format(numbers:_*)
  }
}
_______________________________
object Kata {
  def createPhoneNumber(numbers: Seq[Int]) = {
    s"(${numbers.take(3).mkString}) ${numbers.slice(3,6).mkString}-${numbers.drop(6).mkString}"
  }
}
_______________________________
object Kata {
  def createPhoneNumber(numbers: Seq[Int]) = {
    "(" + numbers.slice(0,3).mkString+ ") "+ numbers.slice(3,6).mkString+ "-" + numbers.slice(6,10).mkString
  }
}
_______________________________
object Kata {

  def createPhoneNumber(numbers: Seq[Int]) = {
    val ns = numbers.mkString
    s"(${ns.take(3)}) ${ns.slice(3, 6)}-${ns.drop(6)}"
  }
}
