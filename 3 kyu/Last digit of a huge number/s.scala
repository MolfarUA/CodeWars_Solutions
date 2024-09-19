def lastDigit(xs: Seq[Int]): Int = 
  def pow(b: Int, e: Int): Int = 
    if e == 0 then 1 else Iterator.fill(e)(b).product
  xs.zipWithIndex
    .foldRight(1) {
      case ((x, i), a) => 
        val base = if i == 0 then x % 10 else if x < 4 then x else x % 4 + 4
        val exp = if a < 4 then a else a % 4 + 4
        pow(base, exp)
    } % 10
__________________
import NumberState.*


enum NumberState:
  case Zero
  case One
  case Reminder4(r: Int)


def lastDigit(xs: Seq[Int]): Int =
  if xs.isEmpty then 1
  else
    val pow = xs.tail.foldRight(One)(nextState)
    (xs.head % 10, pow) match
      case (_, Zero)         => 1
      case (n, One)          => n % 10
      case (0, _)            => 0
      case (1, _)            => 1
      case (2, Reminder4(0)) => 6
      case (2, Reminder4(1)) => 2
      case (2, Reminder4(2)) => 4
      case (2, Reminder4(3)) => 8
      case (3, Reminder4(0)) => 1
      case (3, Reminder4(1)) => 3
      case (3, Reminder4(2)) => 9
      case (3, Reminder4(3)) => 7
      case (4, Reminder4(0)) => 6
      case (4, Reminder4(1)) => 4
      case (4, Reminder4(2)) => 6
      case (4, Reminder4(3)) => 4
      case (5, _)            => 5
      case (6, _)            => 6
      case (7, Reminder4(0)) => 1
      case (7, Reminder4(1)) => 7
      case (7, Reminder4(2)) => 9
      case (7, Reminder4(3)) => 3
      case (8, Reminder4(0)) => 6
      case (8, Reminder4(1)) => 8
      case (8, Reminder4(2)) => 4
      case (8, Reminder4(3)) => 2
      case (9, Reminder4(0)) => 1
      case (9, Reminder4(1)) => 9
      case (9, Reminder4(2)) => 1
      case (9, Reminder4(3)) => 9
      case _                 => ???


def nextState(n: Int, pow: NumberState): NumberState =
  (n, pow) match
    case (_, Zero) => One
    case (0, _)    => Zero
    case (1, _)    => One
    case (n, One)  => Reminder4(n % 4)
    case (n, Reminder4(r)) =>
      (n % 4, r) match
        case (0, _) => Reminder4(0)
        case (1, _) => Reminder4(1)
        case (2, _) => Reminder4(0)
        case (3, 0) => Reminder4(1)
        case (3, 1) => Reminder4(3)
        case (3, 2) => Reminder4(1)
        case (3, 3) => Reminder4(3)
___________________________
def modPow(n :BigInt, exponent: BigInt, mod: BigInt) : Int = n.modPow(exponent, mod).toInt
def lastDigit(xs: Seq[Int]): Int = 
  val data = xs.length match {
    case(l) if l == 0 => return 1
    case(l)          => xs.tail.foldRight(1){
      case(value, curTotal) =>  
        var p = modPow(value, curTotal, 4)
        if(p == 0 && value > 0)                  p = 4
        if(p == 1 && value > 1 && curTotal != 0) p = 5
        (p)
    }
  }
  modPow(xs(0), data, 10)
