fun toCamelCase(str: String) =
    str.split('-', '_').mapIndexed { i, it -> if (i != 0) it.capitalize() else it }.joinToString("")
________________________
fun toCamelCase(str:String):String = str.split(Regex("_|-")).reduce{ fullString, word -> fullString + word.capitalize() }
________________________
fun toCamelCase(str: String): String =
    str.split("-", "_").mapIndexed { i, s -> if (i == 0) s else s.capitalize() }.joinToString("")
________________________
fun toCamelCase(str: String): String =
    str.split("_", "-").mapIndexed { i, s -> if (i > 0) s.capitalize() else s }.joinToString("")
________________________
fun toCamelCase(str:String):String {
    return str.split("-", "_")
        .mapIndexed { index, el ->
            if (index == 0)
                el
            else 
                el.capitalize()
        }
        .joinToString("")
}
________________________
fun toCamelCase(str:String):String{
    var ans = str.split("-", "_")
    var ans1 = ans.filterIndexed{index, i -> index !=0 }.
        joinToString("") { (it.first().toUpperCase() + it.substringAfter(it.first())) }
    return ans[0]+ans1
}
