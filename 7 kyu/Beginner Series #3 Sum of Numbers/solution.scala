object Sum {
  def getSum(a: Int, b: Int): Int = {
    if (a < b) (a to b).sum
    else (b to a).sum
  }
}

_______________________________________
object Sum {
  def getSum(a: Int, b: Int): Int = {
    Range(a min b, a max b).inclusive.sum
  }
}

_______________________________________
object Sum {

  def getSum(a: Int, b: Int): Int =
    ((a - b).abs + 1) * (a + b) / 2
}

_______________________________________
object Sum {
  def getSum(a: Int, b: Int): Int = {
    a.compare(b) match {
      case 1 => {
        (b to a).sum
      }
      case -1 => {
        (a to b).sum
      }
      case _ => a
    }
  }
}

_______________________________________
object Sum {
  def getSum(a: Int, b: Int): Int = {
    a.compare(b) match {
      case 1 => {
        (for (n <- b to a) yield n).sum
      }
      case -1 => {
        (for (n <- a to b) yield n).sum
      }
      case _ => a
    }
  }
}

_______________________________________
object Sum {
  def getSum(a: Int, b: Int): Int = {
    if (a > b) (b to a).sum else (a to b).sum
  }
}

_______________________________________
object Sum {

  def getSum(a: Int, b: Int): Int = {
    val (min, max) = (a min b, a max b)
    (max - min + 1) * (max + min) / 2
  }
}

_______________________________________
object Sum {
  def getSum(a: Int, b: Int): Int = {
    val max: Int = if (a >= b){a}else{b}
    val min: Int = if (a >= b){b}else{a}
    def partSum(start: Int, acc: Int): Int={
      if (start == max)
        {acc + max}
      else
        {partSum(start + 1, acc + start)}
    }
    partSum(min, 0)
  }
}
