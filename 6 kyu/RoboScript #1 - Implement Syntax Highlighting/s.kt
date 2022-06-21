58708934a44cfccca60000c4


fun highlight(code: String): String {
    return Regex("F+|R+|L+|\\d+").replace(code) {
        val colour = when (it.value[0]) {
            'F' -> "pink"
            'L' -> "red"
            'R' -> "green"
            else -> "orange"
        }
        "<span style=\"color: $colour\">${it.value}</span>"
    }
}
__________________________
fun highlight(code: String): String {
    return code.replace(Regex("F+|L+|R+|[0-9]+")) {
        "<span style=\"color: %s\">%s</span>"
            .format(
                when (it.groupValues[0][0]) {
                    'F' -> "pink";
                    'L' -> "red";
                    'R' -> "green";
                    else -> "orange";
                }, it.groupValues[0]);
    };
}
__________________________
fun highlight(code: String): String = code
    .replace("F+".toRegex()) { syntax(it.value, "pink")}
    .replace("L+".toRegex()) { syntax(it.value, "red")}
    .replace("R+".toRegex()) { syntax(it.value, "green")}
    .replace("[0-9]+".toRegex()) { syntax(it.value, "orange")}

fun syntax(value: String , color:String):String = "<span style=\"color: $color\">$value</span>"
