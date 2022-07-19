51c8e37cee245da6b40000bd


fun solution(input: String, markers: CharArray): String =
   input.lines().map { line ->
       line.split(*markers).first().trimEnd()
   }.joinToString("\n")
__________________________________
    fun solution(input: String, markers: CharArray): String =
            input.split("\n").joinToString("\n") {
                it.takeWhile { char -> !markers.contains(char) }.trim()
            }.trim()
__________________________________
fun solution(input: String, markers: CharArray) =
    input.lines().joinToString("\n") { it.takeWhile { !markers.contains(it) }.trim() }
__________________________________
fun solution(input: String, markers: CharArray): String =
        input.split("\n").map { line -> line.takeWhile { !markers.contains(it) }.trimEnd() }.joinToString("\n")
__________________________________
fun solution(input: String, markers: CharArray): String {
   val regex = Regex("""[${markers.sortedBy{it}.joinToString("")}].*$""");
   return input.split("\n").map{it.replace(regex, "").trim()}.joinToString("\n")
}
