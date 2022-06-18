544675c6f971f7399a000e79


fun stringToNumber(str: String) = str.toInt()
_______________________
fun stringToNumber(str: String): Int {
    val num = str.toInt()
    return num
}
_______________________
fun stringToNumber(str: String): Int = str.toInt()
_______________________
fun stringToNumber(str: String): Int {
    return Integer.parseInt(str)
}
_______________________
fun stringToNumber(str: String): Int {
    return str.toInt()
}
