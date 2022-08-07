54b72c16cd7f5154e9000457


fun decodeBits(bits: String): String {
    val bis = bits.trim { it == '0' }
    val timeUnit = Regex("0+|1+").findAll(bis).fold(bis.length) { smallest, x -> if (x.value.length < smallest) x.value.length else smallest }
    return bis.replace("111".repeat(timeUnit), "-")
              .replace("000".repeat(timeUnit), " ")
              .replace("1".repeat(timeUnit), ".")
              .replace("0".repeat(timeUnit), "")
}

fun decodeMorse(code: String) = code.split(" ").map { if (it == "") " " else MORSE_CODE[it] }.joinToString("")
_____________________________
fun decodeBits(bits: String): String {
    val sanitized = bits.trim('0')
    val timeUnit = Regex("0+|1+").findAll(sanitized).minBy { it.value.length }!!.value.length
    return sanitized
        .replace(Regex("1{$timeUnit,}")) { if (it.value.length == timeUnit) "." else "-" }
        .replace(Regex("0+")) { if (it.value.length == timeUnit) "" else if (it.value.length == timeUnit * 3) " " else "   " }
}

fun decodeMorse(code: String): String {
    return Regex("[-.]+| {3}").findAll(code).map { it.value }
        .map { if (it.isBlank()) " " else MORSE_CODE[it] }
        .joinToString("")
}
_____________________________
fun decodeBits(bits: String): String = bits.trim('0')
    .let { it to (Regex("(0+|1+)").findAll(it).map { it.value.length }.min() ?: 0) }
    .run { first.replace("0".repeat(second), "0").replace("1".repeat(second), "1") }
    .replace("111", "-").replace("1", ".")
    .replace("0000000", "   ").replace("000", " ").replace("0", "")

fun decodeMorse(code: String): String = code.trim()
    .split(" ").joinToString("") { MORSE_CODE[it] ?: " " }.replace(Regex(" +"), " ")
_____________________________
fun decodeBits(
    bits: String
): String = bits.trim { it == '0' }.let { "0+|1+".toRegex().findAll(it) }.asSequence().map { it.value }.run {
    this to map { it.length }.min()!!.let {
        mapOf(
            "1".repeat(it) to ".",
            "111".repeat(it) to "-",
            "000".repeat(it) to " ",
            "0000000".repeat(it) to "  "
        )
    }
}.let { (tokens, bitsToMorse) -> tokens.joinToString("") { bitsToMorse[it].orEmpty() } }

fun decodeMorse(
    code: String
): String = code.trim().split(" ").joinToString("") { MORSE_CODE[it] ?: " " }.replace(" +".toRegex(), " ")
