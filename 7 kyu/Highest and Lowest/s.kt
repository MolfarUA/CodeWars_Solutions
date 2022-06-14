fun highAndLow(numbers: String): String
{
    val x = numbers.split(" ").map { it.toInt() }.sorted()
    return "${x.last()} ${x.first()}"
}
______________________________
fun highAndLow(numbers: String) =
    numbers.split(" ").map { it.toInt() }.run {
        "${this.maxOrNull()} ${this.minOrNull()}"
    }
______________________________
fun highAndLow(numbers: String): String {
    var minValue: Int? = null
    var maxValue: Int? = null
    val builder = StringBuilder()
    for ((i, c) in numbers.withIndex()) {
        if (c != ' ') {
            builder.append(c)
        }
        if (c == ' ' || i == numbers.lastIndex) {
            if (builder.isNotEmpty()) {
              val current = builder.toString().toInt()
              if (minValue == null) {
                  minValue = current
                  maxValue = current
              } else {
                  minValue = minOf(minValue, current)
                  maxValue = maxOf(maxValue!!, current)
              }
            }
            builder.clear()
        }
    }
    return "$maxValue $minValue"
}
______________________________
fun highAndLow(str: String): String {
    val split = str.split(" ").map { it.toInt() }
    return "${split.maxOrNull()} ${split.minOrNull()}"
}
______________________________
fun highAndLow(numbers: String): String {
    return numbers.split(" ").maxOf { it.toInt() }.toString() + " " + numbers.split(" ").minOf { it.toInt() }.toString()
}
______________________________
fun highAndLow(numbers: String) = numbers.split(" ").map { it.toInt() }.run { "${maxOrNull()} ${minOrNull()}" }
