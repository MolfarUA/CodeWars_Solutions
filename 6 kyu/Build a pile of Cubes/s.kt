package solution

object ASum {

    fun findNb(m: Long): Long {
        var n: Long = 0
        var cubeSize: Long = 0
        while (cubeSize < m) {
            cubeSize += n * n * n
            n++
        }
        return if (cubeSize == m) n - 1 else -1
    }
}
_________________________________________
package solution

object ASum {

    fun findNb(m: Long): Long {
        var sum = 0L
        return generateSequence(1L) { it + 1 }
            .onEach { sum += it*it*it }
            .takeWhile { sum <= m }
            .lastOrNull { sum == m } 
            ?: -1
    }
}
_________________________________________
package solution
import kotlin.math.pow

object ASum {
    fun findNb(m: Long): Long {
        var sum: Long = 0
        var x: Double = 0.0
        while(sum < m) sum+=(++x).pow(3).toLong()
        if (sum==m) return x.toLong() else return -1
    }
}
