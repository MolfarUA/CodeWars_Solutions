54cb771c9b30e8b5250011d4


import java.math.BigInteger
import java.math.BigInteger.*


fun height(eggs: BigInteger, tries: BigInteger): BigInteger {
    if (eggs == ZERO || tries == ZERO) return ZERO
    val eggs = if (eggs > tries) tries else eggs
    var acc = ZERO ; var e = ZERO
    var binomial = tries
    while (e < eggs) {
        acc += binomial
        e += ONE
        binomial = binomial * (tries - e) / (e + ONE)
    }
    return acc
}
_________________________
import java.math.BigInteger
import java.math.BigInteger.ZERO
import java.math.BigInteger.ONE
import java.math.BigInteger.TWO
import java.math.BigInteger.valueOf

fun height(n: BigInteger, m: BigInteger) :BigInteger {
    val eggs = n.toInt();  val falls = m.toInt()
    if (eggs<=0||falls<=0)
        return ZERO
    if (eggs>=falls)
        return TWO.pow(falls).minus(ONE)
    val partials = (2..eggs).runningFold(valueOf(falls.toLong())){ p, k ->
        p.times(valueOf((falls+1-k).toLong())).div(valueOf(k.toLong())) }
    return partials.sumOf{ it }
}
_________________________
import java.math.BigInteger

fun height(n: BigInteger, m: BigInteger): BigInteger {
    var cur = BigInteger.ONE

    return (0 until n.toInt()).fold(BigInteger.ZERO) { sum, i ->
        cur = cur * (m - i.toBigInteger()) / (i + 1).toBigInteger()
        sum + cur
    }
}
