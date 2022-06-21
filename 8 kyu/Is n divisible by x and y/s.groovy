5545f109004975ea66000086


class Kata {
  static def isDivisible(n, x, y) {
    n % x + n % y == 0
  }
}
_____________________
class Kata {
  static boolean isDivisible(n, x, y) {
    n % x == 0 && n % y == 0
  }
}
_____________________
class Kata {
  static def isDivisible(n, x, y) {
    return n % x + n % y == 0
  }
}
