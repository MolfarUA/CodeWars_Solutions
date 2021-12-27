fun duplicateCount(text: String) = text.groupBy(Char::toLowerCase).count { it.value.count() > 1 }
_________________
fun duplicateCount(text: String): Int {
    return text.groupingBy { it.toLowerCase() }.eachCount().values.count { it > 1 }
}
________________
fun duplicateCount(text: String) = text.groupBy(Char::toLowerCase).count { it.value.size > 1}
_________________
fun duplicateCount(text: String): Int {
     return text
        .toLowerCase()
        .split("")
        .filter { s -> s != "" }
        .groupingBy { s -> s }
        .eachCount()
        .filter { entry -> entry.value > 1 }
        .size
}
____________________
fun duplicateCount(text: String): Int {
    val counter = HashMap<Char, Int>()
    text.toLowerCase().forEach {
        counter.merge(it, 1, Integer::sum)
    }
    return counter.values
        .filter { it > 1 }
        .count()
}
