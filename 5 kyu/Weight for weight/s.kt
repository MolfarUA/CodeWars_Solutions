55c6126177c9441a570000cc


package weight

fun orderWeight(i: String) = i.split(' ').sortedWith(compareBy({ it.sumBy { it - '0' } }, { it })).joinToString(" ")
______________________________
package weight

fun orderWeight(string:String):String {
        return string.split(" ")
                .sortedWith(compareBy<String>{ it.toCharArray().map(Char::toString).map(String::toInt).sum() }.thenBy{ it })
                .joinToString(" ")
    }
______________________________
package weight

fun orderWeight(string:String): String =
    string.split(" ").sorted().sortedBy { it.map { it.toString().toInt() }.sum() }.joinToString(" ")
