object Bus {
  def number(busStops: List[(Int, Int)]): Int = {
    busStops.map{case (on, off) => on - off}.sum
  }
}
_____________________________________
object Bus {
  def number(busStops: List[(Int, Int)]): Int =
    busStops.foldLeft(0) { (acc, pair) => acc + pair._1 - pair._2 }
}
_____________________________________
object Bus {
  def number(busStops: List[(Int, Int)]): Int = {
    busStops.map(t => t._1 - t._2).sum
  }
}
_____________________________________
object Bus {
  def number(busStops: List[(Int, Int)]): Int = busStops match {
    case Nil => 0;
    case (in, out)::tail => in - out + number(tail)
  }
}
