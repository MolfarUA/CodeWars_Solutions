559b8e46fa060b2c6a0000bf


package solution

import java.math.BigInteger

object Diagonal {

    fun diagonal(n: Int, p: Int): BigInteger {
        var r = BigInteger.valueOf(1L)
        var i = BigInteger.valueOf(1L)
        while (i <= BigInteger.valueOf((p + 1).toLong())) {
            r = r * (BigInteger.valueOf(n.toLong()) - i + BigInteger.valueOf(2L)) / i
            i = i + BigInteger.valueOf(1L)
        }
        return r
    }
}
_____________________________
package solution
import java.math.BigInteger

object Diagonal {
    fun diagonal(n: Int, p: Int): BigInteger = binomial((n + 1).toBigInteger(), (p + 1).toBigInteger())

    fun binomial(n: BigInteger, k: BigInteger): BigInteger = when {
        k == (0).toBigInteger() -> (1).toBigInteger()
        k > n / (2).toBigInteger() -> binomial(n, n - k)
        else -> n * binomial(n - (1).toBigInteger(), k - (1).toBigInteger()) / k
    }
}
_____________________________
package solution

import java.math.BigInteger

object Diagonal {

    fun diagonal(n: Int, p: Int): BigInteger = (n - p + 1..n + 1).map { it.toBigInteger() }.reduce { acc, i -> acc * i } / factorial(p + 1)
    
    private fun factorial(n: Int): BigInteger =
        if (n in listOf(0, 1)) BigInteger.ONE else (n downTo 2).map { it.toBigInteger() }.reduce { acc, i -> acc * i }
}
