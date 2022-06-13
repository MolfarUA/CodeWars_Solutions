object Potatoes {

  def potatoes(p0: Int, w0: Int, p1: Int): Int = w0 * (100 - p0) / (100 - p1)
}
_______________________________________________
object Potatoes {
  val potatoes: (Int, Int, Int) => Int = (x, y, z) => y*(100-x)/(100-z)
}
_______________________________________________
object Potatoes {
  val potatoes: (Int, Int, Int) => Int = (x, y, z) => y*(100-x)/(100-z)
}
_______________________________________________
object Potatoes {
  val potatoes: (Int, Int, Int) => Int = (p0, w0, p1) => (w0*(100-p0)/(100-p1)).toInt
}
