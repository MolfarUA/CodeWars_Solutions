56484848ba95170a8000004d


package gps

fun gps(s: Int, x: DoubleArray) = x.toList()
    .windowed(2) { it[1] - it[0] }
    .map { 3600 * it / s }
    .max()
    ?.toInt() ?: 0
_____________________________
package gps

fun gps(s: Int, x: DoubleArray) = x.asSequence().zipWithNext { a, b -> (b - a) * 3600 / s }.max()?.toInt() ?: 0
_____________________________
package gps

fun gps(s:Int, x:DoubleArray) = x.mapIndexed { index: Int, d: Double ->
    (3600 * (x.getOrElse(index + 1) { d } - d))/s
}.max()?.toInt() ?: 0
_____________________________
package gps

fun gps(s:Int, x:DoubleArray) = if (x.size < 2) 0 else 
    (0 until x.lastIndex).map{ (3600 * (x[it + 1] - x[it])) / s }.max()!!.toInt()
