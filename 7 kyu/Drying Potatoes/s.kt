package potatoes

fun potatoes(p0: Int, w0: Int, p1: Int) = w0 * (100 - p0) / (100 - p1)
_______________________________________________
package potatoes

fun potatoes(p0:Int, w0:Int, p1:Int):Int {
    return w0 * (100 - p0) / (100 - p1);
}
_______________________________________________
package potatoes

fun potatoes(p0: Int, w0: Int, p1: Int): Int = Math.floor((w0 * (100-p0) / (100-p1)).toDouble()).toInt()
_______________________________________________
package potatoes

fun potatoes(initialWaterPercent:Int, initialWeight:Int, finalWaterPercent:Int):Int {
    val initialDryMatterWeight = (100 - initialWaterPercent) * initialWeight  / 100.00f
    val totalFinalWeight = initialDryMatterWeight * 100 / (100 - finalWaterPercent)
    return totalFinalWeight.toInt()
}
_______________________________________________
package potatoes

import java.math.BigDecimal
fun potatoes(p0: Int, w0: Int, p1: Int): Int {
    val initWeight = w0.toBigDecimal()
    val dryMatter: BigDecimal = initWeight.minus(p0.toBigDecimal().movePointLeft(2).multiply(initWeight))
    val dryPAfter = BigDecimal(100 - p1).movePointLeft(2)
    return dryMatter.div(dryPAfter).toInt()
}
