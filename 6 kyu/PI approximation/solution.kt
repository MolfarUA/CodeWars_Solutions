package solution

import kotlin.math.PI;
import kotlin.math.abs;

object PiApprox {
    fun iterPi2String(epsilon: Double): String {
        var pi = 0.0
        var iter = 0
        while(abs(pi * 4 - PI  ) > epsilon){
            if(iter % 2 == 0)
                pi += 1.0/(iter * 2 + 1)
            else
                pi -= 1.0/(iter * 2 + 1)
            iter++;
        }
        return "[%d, %.10f]".format(iter, pi*4.0)
    }
}
________________________________________
package solution

import kotlin.math.PI
import kotlin.math.absoluteValue

object PiApprox {
    fun iterPi2String(epsilon: Double): String {
    val pi_system = PI / 4
    val epsilon4 = epsilon / 4
    var pi = 1.0
    var based = 1.0
    var sign = 1
    var epoch = 1
    while((pi_system-pi).absoluteValue>epsilon4){
        based += 2
        sign =- sign
        pi += sign/based
        epoch++
    }
    return String.format("[%d, %10.10f]",epoch, pi*4)
    }
}
________________________________________
package solution

object PiApprox {
    fun iterPi2String(epsilon: Double): String {
    var leibnizPI: Double = 1.0
    var countIteration = 1
    val mathPIDevideFour: Double = Math.PI/4

    while (kotlin.math.abs((leibnizPI - mathPIDevideFour)*4) > epsilon) {
        val negative = if(countIteration%2 == 0) 1 else -1
        val divide:Double = (negative * (1 / ((countIteration * 2.0) + 1.0)))
        leibnizPI += divide
        countIteration++
    }
    val formattedPI = String.format("%.10f", 4*leibnizPI)
    return "[$countIteration, $formattedPI]"
}
}
________________________________________
package solution

import kotlin.math.*

object PiApprox {
    fun iterPi2String(epsilon: Double): String {
        // your code
        var i: Int = 0
        var res: Double = 0.0
        while(true){
            if (i== 0 || i%2 == 0) res += 4.0/(2*i + 1) else res -= 4.0/(2*i + 1)
            i++
            if (abs(res - PI) < epsilon) break
        }
        return "[$i, " + String.format("%.10f", res) + "]"
    }
}
________________________________________
import kotlin.math.absoluteValue
import java.text.DecimalFormat

object PiApprox {
    fun iterPi2String(epsilon: Double): String {
        var approx = 0.0
        var i = 0
        val PI_QUARTER = kotlin.math.PI / 4.0

        while ((PI_QUARTER - approx).absoluteValue > epsilon/4.0) {
            if (i % 2 == 0) approx += 1.0/(i*2+1.0)
            else approx -= 1.0/(i*2+1.0)
            i++
        }

        approx *= 4.0
        return "[$i, ${String.format("%.10f", approx)}]"
    }
}
________________________________________
package solution

import kotlin.math.*

object PiApprox {
    fun iterPi2String(epsilon: Double): String {
        var n = 0
        var pi = .0
        var sign = 4.0
        for (x in 1..Int.MAX_VALUE step 2) {
            n++
            pi += sign.also{sign=-it} / x
            if (abs(PI - pi) < epsilon) break
        }
        return "[%d, %.10f]".format(n, pi)
    }
}
________________________________________
package solution
import kotlin.math.abs

object PiApprox {
    fun iterPi2String(epsilon: Double): String {
        var iteration = 0
    var piCalc: Double = 0.0
    var denominator = 1.0
    var result = 0.0


    while (abs(Math.PI - result) > epsilon) {
        if (iteration % 2 == 0) {
            piCalc += 1 / denominator
        } else {
            piCalc -= 1 / denominator
        }

        result = piCalc * 4
        denominator += 2
        iteration++
    }
    
    return "[${iteration}, ${result.formatDecimal(10)}]"
    }
    
}

fun Double.formatDecimal(decimalPlaces: Int) = "%.${decimalPlaces}f".format(this)
