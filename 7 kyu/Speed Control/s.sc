56484848ba95170a8000004d


object GpsSpeed {

  def gps(interval: Int, distances: Array[Double]): Int =
    (distances.sliding(2).collect { case Array(a, b) => b - a  }.maxOption.getOrElse(0d) * 3600 / interval).toInt
}
_____________________________
object GpsSpeed {

  def gps(s: Int, x: Array[Double]): Int = 
    x match {
      case xs if xs.length < 2   => 0
      case _ => (x zip x.tail).map{case (x1,x2) => 3600 * (x2 - x1) / s}.max.toInt
    }
}
_____________________________
object GpsSpeed {

  def gps(s: Int, x: Array[Double]): Int = {
    val y = x.reverse
    var z = List[Double]()
    for (i<-0 until (y.length -1)) 
      {z = (y(i)-y(i+1))::z}
    if (z == List())
      0
    else {
      val d = z.max
      (3600*d/s).toInt
    }
  }
}
_____________________________
object GpsSpeed {
    def gps(s: Int, x: Array[Double]): Int = {
        val distances = (1 until x.size).map(x(_)).zip(
            (0 until x.size - 1).map(x(_))
        ).map(x => (x._1 - x._2))
        val speeds = distances.map(_ * 3600 / s)
        if (speeds.nonEmpty) Math.floor(speeds.max).toInt else 0
    }
}
