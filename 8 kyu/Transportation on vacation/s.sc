568d0dd208ee69389d000016


object Rental {

  def cost(days: Int): Int = days match {
    case d if(d >= 7) => days * 40 - 50
    case d if(d >= 3) => days * 40 - 20
    case _ => days * 40
  }
}
__________________________
object Rental {

  def cost(days: Int): Int = {
    val dailyCost = 40
    val sevenDayDiscount = 50
    val threeDayDiscount = 20
   
    days match {
      case d if 0 until 3 contains d => d * dailyCost
      case d if 3 until 7 contains d => d * dailyCost - threeDayDiscount
      case d => d * dailyCost - sevenDayDiscount
    }
  
  }
}
__________________________
object Rental {

  def cost(days: Int): Int =
    days * 40 - (if (days >= 7) 50 else if (days >= 3) 20 else 0)
}
