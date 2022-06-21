5545f109004975ea66000086


package kata

func IsDivisible(n, x, y int) bool {
    return n % x == 0 && n % y == 0
}
_____________________
package kata

func IsDivisible(n, x, y int) bool {
    return n % x + n % y == 0
}
_____________________
package kata

func IsDivisible(n, x, y int) bool {
    return IsDivisibleN(n, x) && IsDivisibleN(n, y)
}

func IsDivisibleN(n, divisor int) bool {
  return n % divisor == 0
}
