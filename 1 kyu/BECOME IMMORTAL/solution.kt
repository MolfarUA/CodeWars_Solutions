import java.math.BigInteger
/**
 * set true to enable debug
 */
internal var debug = false

internal fun elderAge(n: Long, m: Long, k: Long, newp: Long): Long {
    fun calculate(n: Long, m: Long, k: Long, delta: Long): BigInteger {
        fun intervalSum(a: Long, b: Long): BigInteger {
            if (b < a) return BigInteger.ZERO
            val bigA = BigInteger.valueOf(a)
            val bigB = BigInteger.valueOf(b)
            return ((bigA+bigB)*(bigB-bigA+BigInteger.ONE)).shiftRight(1)
        }
        if (m > n) return calculate(m, n, k, delta)
        val nH = java.lang.Long.highestOneBit(n)
        val mH = if (m < nH) m else nH
        var result = intervalSum(Math.max(0, delta - k), delta + nH - k - 1) * BigInteger.valueOf(mH)
        if (n > nH) result = (result + calculate(n - nH, mH, k, delta + nH))
        if (m > mH) result = (result + calculate(nH, m - mH, k, delta + mH))
        if (n > nH && m > mH) result = (result + calculate(n - nH, m - mH, k, delta + (mH xor nH)))
        return result
    }
    return calculate(n, m, k, 0).mod(BigInteger.valueOf(newp)).toLong()
}
__________________________________
internal var debug = false

internal fun elderAge(m: Long, n: Long, l: Long, t: Long): Long {
  val base: Double = 2.toDouble()
  val small: Long = Math.min(m, n)
  val big: Long = Math.max(m, n)
  val power: Long = Math.pow(base, Math.floor(Math.log(big.toDouble()) / Math.log(base)).toDouble()).toLong()
  val rows: Long = Math.min(power, small)
  val first: Long = Math.max(0, -l)
  val terms: Long = Math.max(0, power - l - 1)
  var x = terms - first + 1
  var y = first + terms

  if (x % 2 > 0) y = Math.floor((y / 2).toDouble()).toLong()
  else if (y % 2 > 0) x = Math.floor((x / 2).toDouble()).toLong()

  val series: Long = if (y <= 0) 0 else ((y % t) * (x % t)) % t

  var sum = ((series % t) * (rows % t)) % t
  if (big > power) sum += elderAge(big - power, rows, l - power, t)
  if (small > rows) sum += elderAge(power, small - rows, l - rows, t)
  if (small > rows && big > power) sum += elderAge(big - power, small - rows, l, t)

  return sum % t
}
____________________________________________
internal var debug = false

internal fun mmul(x: Long, y: Long, m: Long) : Long = (x % m) * (y % m) % m

internal fun elderAge(m: Long, n: Long, l: Long, t: Long): Long {
    if (m < n) return elderAge(n, m, l, t)
    val k1 = 2 * m.takeHighestOneBit()
    if (m <= 0 || n <= 0 || l >= k1) return 0
    val k = if (n > 1) k1 / 2 else m
    val r = Math.min(n, k)
    var s = 0L
    if (k > l) {
        if (l >= 0) {
            var x = k - l
            var y = x - 1
            if (x % 2 == 0L) x /= 2 else y /= 2
            s = mmul(mmul(x, y, t), r, t)
        } else {
            var x = k
            var y = k - 1
            if (x % 2 == 0L) x /= 2 else y /= 2
            s = mmul(mmul(x, y, t) - mmul(l, k, t), r, t)
        }
    }
    s += elderAge(m - k, r, l - k, t)
    s += elderAge(k, n - r, l - k, t)
    s += elderAge(m - k, n - r, l, t)
    return s % t
}
____________________________________________
import kotlin.math.*

val debug = true

fun elderAge(row: Long, col: Long, loss: Long, newp: Long): Long {
    val biggerDim = max(row, col)
    val smallerDim = min(row, col)
    return elderAge(0, biggerDim, smallerDim, loss, newp)
}


private fun elderAge(
    offset: Long,
    biggerDim: Long,
    smallerDim: Long,
    loss: Long,
    mod: Long
): Long {
    val smallerPow2 = highestPowerOf2(smallerDim)
    val biggerPow2 = highestPowerOf2(biggerDim)

    val mainPart = modulatedSeqSum(
        start = max(0, offset - loss),
        end = max(0, offset + biggerPow2 - 1 - loss),
        length = max(1, biggerPow2 + min(0, offset - loss)),
        times = smallerPow2,
        mod = mod
    )

    val smallerSidePart = modulatedSeqSum(
        start = max(0, offset + smallerPow2 - loss),
        end = max(0, offset + (smallerPow2 * 2) - 1 - loss),
        length = max(1, smallerPow2 + min(0, offset + smallerPow2 - loss)),
        times = max(0, smallerDim - smallerPow2),
        mod = mod
    )

    var biggerSidePart = 0L
    if (biggerDim > biggerPow2 && biggerPow2 < 2 * smallerPow2) {
        biggerSidePart = modulatedSeqSum(
            start = max(0, offset + smallerPow2 - loss),
            end = max(0, offset + (smallerPow2 * 2) - 1 - loss),
            length = max(1, smallerPow2 + min(0, offset + smallerPow2 - loss)),
            times = max(0, min(biggerDim - smallerPow2, smallerPow2)),
            mod = mod
        )
    }

    var bottomReminderPart = 0L
    if (smallerDim > smallerPow2 && biggerPow2 > smallerPow2 * 2) {
        bottomReminderPart = modulatedSeqSum(
            start = max(0, offset + 2 * smallerPow2 - loss),
            end = max(0, offset + biggerPow2 - 1 - loss),
            length = max(0, biggerPow2 - 2 * smallerPow2 + min(0, offset + 2 * smallerPow2 - loss)),
            times = max(0, smallerDim - smallerPow2),
            mod = mod
        )
    }

    var mirroredPart = 0L
    if (smallerDim > smallerPow2 && biggerDim > smallerPow2) {
        mirroredPart = elderAge(
            offset = offset,
            biggerDim = max(0, min(biggerDim - smallerPow2, smallerPow2)),
            smallerDim = max(0, smallerDim - smallerPow2), // negative numbers here should never happen
            loss = loss,
            mod = mod
        )
    }


    var remainderPart = 0L
    if (biggerDim > biggerPow2 && biggerPow2 >= 2 * smallerPow2) {
        remainderPart = elderAge(
            offset = offset + biggerPow2,
            biggerDim = max(biggerDim - biggerPow2, smallerDim),
            smallerDim = min(biggerDim - biggerPow2, smallerDim),
            loss = loss,
            mod = mod
        )
    }
    return (mainPart + smallerSidePart + biggerSidePart + mirroredPart + remainderPart + bottomReminderPart) % mod
}

// if is needed because division modulo (by 0.5) is not always defined
fun modulatedSeqSum(start: Long, end: Long, length: Long, times: Long, mod: Long): Long =
    if ((start + end) % 2 == 0L) {
        (((0.5 * start % mod + 0.5 * end % mod) % mod) * (((length % mod) * (times % mod)) % mod) % mod).toLong()
    } else {
        ((((0.5 * length) % mod * (times % mod)) % mod * (start % mod + end % mod) % mod) % mod).toLong()
    }

fun highestPowerOf2(n: Long): Long {
    val p = (ln(n.toDouble()) / ln(2.0)).toLong()
    return 2.0.pow(p.toDouble()).toLong()
}
