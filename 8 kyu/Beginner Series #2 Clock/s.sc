55f9bca8ecaa9eac7100004a


object Kata {

  def past(h: Int, m: Int, s: Int): Int =
    (3_600 * h + 60 * m + s) * 1_000
}
__________________________
object Kata {
  def past(h: Int, m: Int, s: Int): Int = {
    val second = 1000
    val minute = 60 * second
    val hour = 60 * minute
    
    h * hour + m * minute + s * second
  }
}
__________________________
object Kata {
  def past(h: Int, m: Int, s: Int): Int = 1000 * (60 * ( 60 * h + m) + s) 
}
__________________________
object Kata {
  def past(h: Int, m: Int, s: Int): Int = (s + 60*m + 3600*h) * 1000
}
__________________________
object Kata {
  def past(h: Int, m: Int, s: Int): Int = {
    val secToMillisec = 1000
    val minToMillisec = 60 * secToMillisec
    val hoursToMillisec = 60 * minToMillisec
    
    h * hoursToMillisec + m * minToMillisec + s * secToMillisec
    }
}
__________________________
object Kata {

  def multiplyBy (a: Int) = (b:Int) => a * b
  def secondsToMiliseconds = multiplyBy(1000)
  def minutesToMiliseconds =  multiplyBy(60) andThen secondsToMiliseconds
  def hourToMiliseconds = multiplyBy(60) andThen minutesToMiliseconds
  def past(h: Int, m: Int, s: Int): Int =  hourToMiliseconds(h) + minutesToMiliseconds(m) + secondsToMiliseconds(s)
}
