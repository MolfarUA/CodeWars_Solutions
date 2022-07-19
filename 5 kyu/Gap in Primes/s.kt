561e9c843a2ef5a40c0000a4


package gap

import kotlin.math.sqrt

fun isPrime(x: Long) = (2L..sqrt(x.toDouble()).toLong()).none { x % it == 0L }

fun gap(g: Int, m: Long, n: Long):LongArray {
    return (m..n)
            .filter(::isPrime)
            .zipWithNext()
            .firstOrNull { it.second - it.first == g.toLong() }
            ?.let { longArrayOf(it.first, it.second) } ?: longArrayOf()
}
__________________________________
package gap
import java.math.BigInteger

fun gap(g: Int, m: Long, n: Long)=(m..n).filter{BigInteger.valueOf(it).isProbablePrime(10)}
    .windowed(2).find{it.last()-it.first()==g.toLong()}?.toLongArray()?:longArrayOf()
__________________________________
package gap
import java.lang.Math.sqrt

fun isPrime_(x: Long) = (2L..sqrt(x.toDouble()).toLong()).none { x % it == 0L }

fun gap(g: Int, m: Long, n: Long): LongArray {
    return (m..n)
        .filter(::isPrime_)
        .zipWithNext()
        .firstOrNull { it.second - it.first == g.toLong() }
        ?.let { longArrayOf(it.first, it.second) } ?: longArrayOf()
}
__________________________________
package gap

import kotlin.math.sqrt

fun gap(g: Int, m: Long, n: Long): LongArray {
        var prime = 0L
        (m..n).forEach {
            if (isPrime(it)) {
                if ((it - prime).compareTo(g) == 0) {
                    return longArrayOf(prime, it)
                }
                prime = it
            }
        }

        return longArrayOf()
    }

    private fun isPrime(n: Long): Boolean {
        (2..sqrt(n.toDouble()).toLong()).forEach {
            if ((n % it).compareTo(0) == 0) return false
        }

        return true
    }
