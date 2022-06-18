object Kata {
  fun digitize(n:Long):IntArray {
    return n.toString().map(Character::getNumericValue).toIntArray().reversedArray()
  }
}
________________________
object Kata {
  fun digitize(n:Long):IntArray {
  
  var result = n.toString().map { it.toString().toInt() }.toIntArray();

    return result.reversedArray();
  }
}
________________________
object Kata {
    fun digitize(n: Long) = "$n".reversed().map { "$it".toInt() }.toIntArray()
}
________________________
object Kata {
  fun digitize(n:Long):IntArray {
      
        val aux = n.toString()
        val aux2 = aux.toCharArray()
        
        val final = aux2.map{it.digitToInt()}.reversed().toTypedArray().toIntArray()
           
        return final
  }
}
________________________
object Kata {
  fun digitize(n:Long):IntArray {
     val arrayOf = n.toString().reversed()
    println(arrayOf)
    val arr = Array(arrayOf.length) { 0 }

   var newArr = arrayOf
        .map { Character.getNumericValue(it) }

    return newArr.toIntArray()
  }
}
