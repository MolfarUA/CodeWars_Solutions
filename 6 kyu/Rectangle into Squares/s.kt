55466989aeecab5aac00003e


package squares

tailrec fun sqInRect(l:Int, w:Int, list:List<Int> = listOf<Int>()):List<Int>? {
    return if (l == w && list.isEmpty()) {
        null
    } else if (l == w) {
        list.plus(l)        
    } else {
        val c = minOf(l, w)
        sqInRect(maxOf(l, w) - c, c, list.plus(c))
    }
}
______________________________
package squares

fun sqInRect(lng:Int, wdth:Int): List<Int>? {
    if (lng == wdth) return null
    
    val result = mutableListOf<Int>()
    
    var currentLength = lng
    var currentWidth = wdth
    
    while (currentLength > 0 && currentWidth > 0) {
        val minSide = Math.min(currentLength, currentWidth)
        
        if (currentLength > currentWidth) currentLength -= minSide
        else currentWidth -= minSide
        
        result += minSide
    }
    
    return result
}
______________________________
package squares

import kotlin.math.abs

fun sqInRect(lng:Int, wdth:Int):List<Int>? {
    return if(lng == wdth) null
    else generateSequence(listOf(lng, wdth).sorted()) {
        listOf(it[0], it[1]-it[0]).sorted()
    }.takeWhile{it[0] > 0}.map{it[0]}.toList()
}
