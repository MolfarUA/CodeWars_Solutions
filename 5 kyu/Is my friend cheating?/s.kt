5547cc7dcad755e480000004


package solution

object RemovedNumbers {
    fun removNb(n: Long) = (1..n).fold(ArrayList<LongArray>()) { result, a ->
        val sum = (n * (n + 1)) / 2
        val b = (sum - a) / (a + 1)
        if (sum - b - a == b * a && b <= n) result.add(arrayOf(a, b).toLongArray())
        result
    }.toTypedArray()
}
______________________________
package solution

object RemovedNumbers {
 fun removNb(n: Long): Array<LongArray> {
    val c: Long = (n + 1) * n / 2L + 1;
    return (2..n + 1).filter { c % it == 0L && c / it <= n + 1 }
        .map { longArrayOf(it - 1, c / it - 1) }.toTypedArray()
}
}
______________________________
package solution

object RemovedNumbers {
    fun removNb(n: Long): Array<LongArray> {
        val sum = n * (n + 1) / 2
        return (1..n).filter { (sum - it) % (it + 1) == 0L && (sum - it) / (it + 1) <= n }
            .map { longArrayOf(it, (sum - it) / (it + 1)) }.toTypedArray()
    }
}
