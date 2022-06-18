57eb8fcdf670e99d9b000272


fun high(str: String): String {
    return str.split(' ').maxBy{ it.sumBy{ it - 'a' + 1 } }!!
}
_____________________________________________
fun high(str: String): String = str.split(' ').maxBy {
    it.sumBy { char -> char.toInt().minus(96) }
}.orEmpty()
_____________________________________________
fun high(str: String) = str.split(' ').maxBy { it.sumBy { it - '`' } }
_____________________________________________
fun high(str: String) = str.split(" ").maxBy { string -> string.sumBy { it.toLowerCase().toInt() - 96 } }
_____________________________________________
fun high(str: String) : String = str.split(" ").maxBy { it.sumBy { currentChar -> currentChar - '`' } } ?: ""
_____________________________________________
fun high(str: String) : String {
    val str = str.split(" ")
    var counter = 0
    var counter2 = 0
    var element = ""
    var element2 = ""
    for (i in str) {
        counter = 0
        element = ""
        for (j in i) {
            counter += j.code-96
            element += j
        }
        if (counter > counter2) {
            counter2 = counter
            element2 = element
        }
    }
    return element2
}
_____________________________________________
fun high(str: String) : String = 
    str.split("\\s+".toRegex()).maxByOrNull { it.map { it.code - 96 }.sum() } ?: ""
