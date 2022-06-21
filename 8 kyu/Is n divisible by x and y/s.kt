5545f109004975ea66000086


fun isDivisible(n: Int, x: Int, y: Int) = n % x == 0 && n % y == 0
_____________________
fun isDivisible(n: Int, x: Int, y: Int): Boolean {
    return n % x == 0 && n % y == 0
}
_____________________
fun isDivisible(n: Int, x: Int, y: Int): Boolean {
    if (n % x == 0 && n % y == 0) {
      return true
    } else {
      return false
    }
}
