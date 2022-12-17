56c5847f27be2c3db20009c3


object Kata {

  def subtractSum(n: Int) = "apple"
}
_______________________________________
object Kata {
  def subtractSum(n: Int): String = "apple" // fruit name like "apple"
}
_______________________________________
object Kata {
  
  def subtractSum(n: Int): String = {
  // break n into individual digits
    val sum = n.toString().toCharArray().map(n=> n.toString.toInt).reduce((total, n) =>  n+ total)
//     n.toString().toCharArray().reduce(total, n =>  n.toString.toInt + total)
  val newN = n - sum
  println(sum)
  newN match {
  case 1|3|24|26|47|49|68|70|91|93 => return "kiwi"
  case 2|21|23|42|44|46|65|67|69|88 => return "pear"
  case 96|94|92|73|71|50|48|4|6|25|29 => return "banana"
  case 5|7|28|30|32|51|53|74|76|95|97 => return "melon"
  case 9|18|27|36|45|54|63|72|81|90|99 => return "apple"
  case 8|10|12|31|33|52|56|75|77|79|98|100 => return "pineapple"

  case _ => return subtractSum(newN)
  }
  //add together
   // 
  } // fruit name like "apple"
}

