52f677797c461daaf7000740


private tailrec fun gcd(x: Long, y: Long): Long = if (y == 0L) x else gcd(y, x % y)
fun solution(numbers: LongArray)  = numbers.fold(0L, ::gcd) * numbers.size
_______________________________
private tailrec fun gcd(a:Long, b:Long):Long = if (a%b == 0L) b else gcd(b, a%b)
fun solution(numbers: LongArray): Long {
    return numbers.size * numbers.reduce(::gcd)
}
_______________________________
fun solution(numbers: LongArray): Long {
    if (numbers.size == 1) return numbers.first()
    val arr = numbers.distinct()
    var result = arr.first()
    for (i in 1 until arr.size) result = gcd(result, arr[i])
    return result * numbers.size
}

fun gcd(first: Long, second: Long): Long {
        var a = first
        var b = second
        while (b > 0) {
            val temp = b
            b = a % b
            a = temp
        }
        return a
}
_______________________________
fun nod(a: Long, b: Long): Long {
    return if (b == 0L) a
    else nod(b, a % b)
}

fun solution(numbers: LongArray): Long {
    for (i in 0 until numbers.size - 1) {
        numbers[i + 1] = nod(numbers[i], numbers[i + 1])
    }
    val sum = numbers.size * numbers[numbers.size - 1]
    return sum
}
