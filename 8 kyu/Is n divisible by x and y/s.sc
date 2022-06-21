5545f109004975ea66000086


object Kata {

  def isDivisible(n: Int, x: Int, y: Int): Boolean = n % x == 0 & n % y == 0
}
_____________________
object Kata {
  def isDivisible(n: Int, x: Int, y: Int): Boolean = {
    return (n % x == 0 && n % y == 0);
  }
}
_____________________
object Kata {
  
  def isDivisible(n: Int, x: Int, y: Int): Boolean = curry(aCondition)(n)(x)(y)

  val curry: ((Int, Int, Int) => Boolean) => (Int => (Int => (Int => Boolean))) = f => n => x => y => f(n, x, y)
  val aCondition: (Int, Int, Int) => Boolean = (n, x, y) => n % x + n % y == 0
}
