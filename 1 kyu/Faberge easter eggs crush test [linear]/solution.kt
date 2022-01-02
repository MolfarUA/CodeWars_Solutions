import java.math.BigInteger

object Faberge {
    val mod = 998244353.toBigInteger()

    fun height(n: BigInteger, m: BigInteger): BigInteger {
        if (n >= m) return (BigInteger.TWO.modPow(m, mod) - BigInteger.ONE) % mod
        var c = BigInteger.ONE
        var s = BigInteger.ZERO
        var i = BigInteger.ZERO
        while (i < n) {
            c = c * (m - i) * (i + BigInteger.ONE).modInverse(mod) % mod
            s += c
            ++i
        }
        return s % mod
    }
}
__________________________________________________
import java.math.BigDecimal
import java.math.BigInteger
import java.math.RoundingMode

object Faberge {
val mod = 998244353.toBigInteger()
    val preAllocate = mutableListOf(BigInteger.ZERO, BigInteger.ONE)

    init {
        for (haha_i in 2L until (80000L + 1L)) {
            preAllocate.add(
                mod - mod.toBigDecimal().divide(BigDecimal.valueOf(haha_i), RoundingMode.FLOOR)
                    .toBigInteger() * preAllocate[(mod % BigInteger.valueOf(haha_i)).toInt()] % mod
            )
        }
    }


    fun height(n: BigInteger, m: BigInteger): BigInteger {
        var h = BigInteger.ZERO
        var t = BigInteger.ONE
        val m1 = m % mod

        for (i in 1 until (n.toInt() + 1)) {
            t = t * (m1 - BigInteger.valueOf(i.toLong()) + BigInteger.ONE) * preAllocate[i] % mod
            h = (h + t) % mod
        }
        return h % mod
    }
}
__________________________________________________
import java.math.BigInteger

object Faberge {
    val MOD = 998244353.toBigInteger()

    fun height(n: BigInteger, m: BigInteger): BigInteger {
        var h = BigInteger.ZERO;
        var a = BigInteger.ONE;
        for (i in 1..n.intValueExact())
        {
            var inv = (i).toBigInteger().modInverse(MOD);
            a = a.multiply(m.add((1 - i).toBigInteger())).multiply(inv).mod(MOD)
            h = h.add(a).mod(MOD);
        }
        return h;
    }
}
__________________________________________________
import java.math.BigInteger
import java.math.BigInteger.*

object Faberge {
    val mo = 998244353.toBigInteger()

    fun height(n: BigInteger, m: BigInteger): BigInteger {
        var h = ZERO
        var t = ONE
        var i = ONE
        while (i <= n) {
            t = t * (m - i + ONE) * i.modInverse(mo) % mo
            h += t
            i += ONE
        }
        return h % mo
    }
}
__________________________________________________
import java.math.BigInteger
import java.math.BigInteger.ONE
import java.math.BigInteger.valueOf

object Faberge {
    private val mod = 998244353.toBigInteger()
    private val hahaInv: List<BigInteger> by lazy {
        val value = mutableListOf(0.toBigInteger(), 1.toBigInteger())
        for (i in (2..80000).map { it.toBigInteger() }) {
            value.add((mod.minus(mod.divide(i)).multiply(value[mod.mod(i).toInt()]).mod(mod)))
        }
        value
    }
    fun height(n: BigInteger, m: BigInteger): BigInteger {
        val m = m.mod(mod)
        var h = valueOf(0)
        var t = valueOf(1)
        for (i in (1..n.toLong()).map { valueOf(it) }) {
            t = t.multiply(m.minus(i).plus(ONE)).multiply(hahaInv[i.toInt()]).mod(mod);
            h = h.plus(t).mod(mod);
        }
        return h;
    }
}
