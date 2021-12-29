package mix

fun mix(s1:String, s2:String):String {
    val m1 = ('a'..'z').associateBy({ it }, { s1.filter { c -> it == c }.length })
    val m2 = ('a'..'z').associateBy({ it }, { s2.filter { c -> it == c }.length })

    var l = mutableListOf<String>()
    for (c in 'a'..'z') {
        val v1 = m1.get(c)!!
        val v2 = m2.get(c)!!
        if (v1 < 2 && v2 < 2) {
            continue
        }
        if (v1 == v2) {
            l.add("=:" + c.toString().repeat(v1))
        } else if (v1 > v2) {
            l.add("1:" + c.toString().repeat(v1))
        } else if (v2 > v1) {
            l.add("2:" + c.toString().repeat(v2))
        }
    }

    return l.sortedWith(compareBy({ -it.length }, { it })).joinToString("/")
}

__________________________________________________
package mix

fun mix(s1: String, s2: String) = run {
    val result = hashMapOf<Char, Pair<Int, Char>>() // 字符，多少个字符，谁最多

    fun String.some(i: Char) = asSequence().filterNot { it.isWhitespace() || it.isUpperCase() }.groupBy { it }
            .forEach { (k, v) ->
                val s = v.size
                if (s > 1) {
                    val pair = result[k]
                    if (pair != null) {
                        if (pair.first < s) result[k] = s to i
                        else if (pair.first == s) result[k] = s to '='
                    } else result[k] = s to i
                }
            }
    s1.some('1')
    s2.some('2')

    result.entries.sortedWith(compareByDescending<Map.Entry<Char, Pair<Int, Char>>> { it.value.first }
            .thenBy { it.value.second }.thenBy { it.key })
            .joinToString("/") { "${it.value.second}:${it.key.toString().repeat(it.value.first)}" }
}

__________________________________________________
package mix

fun mix(s1: String, s2: String): String {
    val filteredS1 = s1.filterForTask()
    val filteredS2 = s2.filterForTask()
    
    return filteredS1.mapToNeededString(filteredS2, '1').plus(filteredS2.mapToNeededString(filteredS1, '2')).distinct()
        .filter { it.isNotEmpty() }
        .sortedBy { it.first() }.sortedByDescending { it.length }
        .joinToString("/")
}


private fun List<Pair<Int, Char>>.mapToNeededString(list: List<Pair<Int, Char>>, char: Char) = this.map { pair ->
    with(list.find { it.second == pair.second } ?: Pair(0, 'x')) {
        when {
            pair.first > this.first -> "$char:${pair.second.toString().repeat(pair.first)}"
            pair.first < this.first -> ""
            else -> "=:${pair.second.toString().repeat(pair.first)}"
        }
    }
}

private fun String.filterForTask() = with(this.filter { it.isLetter() && it.isLowerCase() }) {
    this.map { char -> Pair(this.count { it == char }, char) }.distinct().sortedBy { it.second }
        .filter { pair -> pair.first > 1 }
}

__________________________________________________
package mix

import java.util.*
import kotlin.collections.HashMap

fun mix(s1: String, s2: String): String {
    val map1 = createMap(s1)
    val map2 = createMap(s2)

    val resultMap = HashMap<Char, Element>()

    for ((key, value) in map1) {
        if (value <= 1) continue
        resultMap[key] = Element("1", key, value)
    }

    for ((key, value) in map2) {
        if (value <= 1) continue
        val lastValue = resultMap[key]
        if (lastValue == null || lastValue.numberRepeat < value) {
            resultMap[key] = Element("2", key, value)
        } else if (lastValue.numberRepeat == value) {
            resultMap[key] = Element("=", key, value)
        }
    }

    return resultMap.values.sorted().joinToString(separator = "/") { it.content }
}


fun createMap(s: String): Map<Char, Int> {
    val map = HashMap<Char, Int>()
    s.forEach {
        if (it.isLowerCase()) {
            map[it] = map[it]?.plus(1) ?: 1
        }
    }
    return map
}

class Element(indexString: String, symbol: Char, val numberRepeat: Int) : Comparable<Element> {
    val content = indexString + ":" + symbol.toString().repeat(numberRepeat)

    override fun compareTo(other: Element): Int {
        return if (other.numberRepeat.compareTo(numberRepeat) != 0) other.numberRepeat.compareTo(numberRepeat)
        else content.compareTo(other.content)
    }
}
