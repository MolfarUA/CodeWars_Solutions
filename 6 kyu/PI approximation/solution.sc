import scala.math.{Pi, abs}

object PiApprox {
  val reg = "0+$".r.unanchored

  def iterPi2String(epsilon: Double): String = {
    var counter = 0
    var pi = 0d
    while(abs((pi * 4) - Pi) > epsilon) {
      pi = pi + nthLeibnitzSeries(counter)
      counter = counter + 1
    }
    val formattedNumber = reg.replaceAllIn("%.10f".format(pi * 4), "")
    
    "[%d, %s]".format(counter, formattedNumber)
  }
  
  def nthLeibnitzSeries(cursor: Int): Double = {
    val value = 1d / (1 + (2 * cursor)).toDouble
    if (cursor % 2 == 0) value else - value
  }
}
________________________________________
object PiApprox {
  
  def iterPi2StringRec(iteration: Int, approx: Double, epsilon: Double): String = {
    val newApprox = if (iteration % 2 == 0) approx - 1.0 / (iteration * 2 - 1) else approx + 1.0 / (iteration * 2 - 1)
    if ((java.lang.Math.PI - newApprox * 4).abs < epsilon) "[%d, %1.10f]".format(iteration, newApprox * 4) else iterPi2StringRec(iteration + 1, newApprox, epsilon)
  }

  def iterPi2String(epsilon: Double): String = iterPi2StringRec(1, 0, epsilon)
}
________________________________________
object PiApprox {
  def sign(n: Double): Double = if (n%2 == 0) 1 else -1
  
  def iterPi2String(epsilon: Double, n: Double = 0, acc: Double = 0): String = {
    val iteration = acc + (1.0/(2*n+1) * sign(n))
    if (math.abs(math.Pi - (iteration*4)) <= epsilon) {
      s"[${(n+1).toInt}, ${"%.10f".format(iteration*4).take(12)}]"
    }
    else {
      iterPi2String(epsilon, n+1, iteration)
    }
  }
}
________________________________________
import scala.math.{Pi, abs}

object PiApprox {

  def iterPi2String(epsilon: Double): String = {
    
    @annotation.tailrec
    def estimate(acc: Double, denom: Long, sign: Double, i: Int): (Int, Double) = {
      if (abs(acc * 4.0 - Pi) >= epsilon)
        estimate(acc + sign/denom, denom + 2, -sign, i+1)
      else
        (i, acc * 4.0)
    }
    
    val rounder = math.pow(10, 10)
    val e = estimate(1, 3, -1, 1)    
    s"[${e._1}, ${(e._2 * rounder).round / rounder}]"
  }
}
________________________________________
object PiApprox {

  def iterPi2String(epsilon: Double): String = {
    var pi4 = 1.0
    var sign = -1.0
    var iterations = 1
    var denom = 3.0
    while (Math.abs(4.0 * pi4 - Math.PI) >= epsilon) {
      pi4 += sign * (1.0 / denom)
      sign *= -1.0
      denom += 2.0
      iterations += 1
    }
    return "[%d, %.10f]".format(iterations, 4.0 * pi4)
  }
}
