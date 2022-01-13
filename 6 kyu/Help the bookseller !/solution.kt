package solution

object StockList {
    fun stockSummary(lstOfArt: Array<String>, lstOfCat: Array<String>): String {
        if (lstOfArt.isEmpty()) return ""
        val counts = lstOfArt.groupingBy { it.take(1) }.fold(0) { acc, s -> acc + s.split(" ")[1].toInt() }
        return lstOfCat.joinToString(" - ") { "($it : ${counts.getOrDefault(it, 0)})" }
    }
}
________________________________________
package solution

object StockList {
    fun stockSummary(lstOfArt: Array<String>, lstOfCat: Array<String>): String {
        // your code
        if (lstOfArt.isEmpty() || lstOfCat.isEmpty()) return ""

        val map = lstOfCat.associate { it to 0 }.toMutableMap()
        lstOfArt.forEach {
            val firstLetter = it[0].toString()
            if(map.containsKey(firstLetter))
                map[firstLetter] = map[firstLetter]?.plus(it.split(" ")[1].toInt())!!
        }

        val resString = StringBuilder()
        map.forEach { (k, v) -> resString.append("($k : $v) - ")  }
        return resString.toString().dropLast(3)
    }
}
________________________________________
package solution

object StockList {
       fun stockSummary(lstOfArt: Array<String>, lstOfCat: Array<String>) =  if(lstOfCat.isEmpty() || lstOfArt.isEmpty()) "" else lstOfCat.joinToString(" - ") { category ->
            val sum = lstOfArt.filter {
                it.startsWith(category)
            }.map {
                it.split(" ")[1].toInt()
            }.sum()
            "($category : $sum)"
    }
}
________________________________________
package solution

object StockList {
 fun stockSummary(lstOfArt: Array<String>, lstOfCat: Array<String>): String {
     if(lstOfArt.size <1 || lstOfCat.size <1) return ""
    val map = mutableMapOf<Char,Int>()
    val result = StringBuilder()
    for(i in lstOfArt){
        val(a,b) = i.split(" ")
     map[a[0]] = if(map[a[0]] == null) b.toInt() else map[a[0]]!! +b.toInt()
    }
    for(i in lstOfCat)
        result.append("($i : ${map[i[0]]?:0}) - ")
      return result.substring(0 until result.length-2).trim()
}
}
________________________________________
package solution

object StockList {
    fun stockSummary(lstOfArt: Array<String>, lstOfCat: Array<String>): String {
        if(lstOfArt.isEmpty() || lstOfCat.isEmpty()) return ""
        val map = mutableMapOf<String,Int>()
        for(art in lstOfArt){
            val arrArt = art.split(" ")
            val cat = arrArt[0].first().toString()
            map[cat] = (map[cat] ?: 0) + arrArt[1].toInt()
        }
        val result = arrayListOf<String>()
        for(cat in lstOfCat){
            result.add("($cat : ${map.getOrDefault(cat, 0)})")
        }
        return result.joinToString(" - ")
    }
}
________________________________________
package solution

object StockList {
    fun stockSummary(lstOfArt: Array<String>, lstOf1stLetter: Array<String>): String {
        if (lstOfArt.isEmpty()) {
            return ""
        }
        var result = ""
        for (m in lstOf1stLetter) {
            var tot = 0
            for (l in lstOfArt) {
                if (l[0] == m[0])
                    tot += l.split(" ".toRegex()).toTypedArray()[1].toInt()
            }
            if (!result.isEmpty())
                result += " - "
            result += "($m : $tot)"
        }
        return result
    }
}
