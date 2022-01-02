fun makeUpperCase(str: String) = str.toUpperCase()
_____________________________________________
fun makeUpperCase(txt: String): String {
    return txt.toUpperCase() // Kotlin 1.3
    // return txt.uppercase() Kotlin 1.4+
}
_____________________________________________
fun makeUpperCase(str: String): String {
    var result =  String()
    for (ch in str) {

        if(ch in 'a'..'z') {
            result += ch - 32
        } else{
            result += ch
        }
    }
    return result
}
_____________________________________________
fun makeUpperCase(str: String): String {
   return str.map {if(it.toInt() in 97..122){(it.toInt() -32).toChar()} else {it}}.joinToString("")
}
_____________________________________________
fun makeUpperCase(str: String): String {
    var upperCaseArray: String = ""
    for (char in str) upperCaseArray = upperCaseArray + (char.toUpperCase())
    return upperCaseArray
}
_____________________________________________
fun makeUpperCase(txt: String): String {
    return txt.uppercase()
}
