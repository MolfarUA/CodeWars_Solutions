fun findMissingLetter(array: CharArray) = (array.first()..array.last()).first { it !in array }
________________________
fun findMissingLetter(array: CharArray): Char = (array.first()..array.last()).filterNot { it in array }.first()
________________________
fun findMissingLetter(array: CharArray): Char {
    val alph = mapOf(
        'a' to 1, 'b' to 2,
        'c' to 3, 'd' to 4,
        'e' to 5, 'f' to 6,
        'g' to 7, 'h' to 8,
        'i' to 9, 'j' to 10,
        'k' to 11, 'l' to 12,
        'm' to 13, 'n' to 14,
        'o' to 15, 'p' to 16,
        'q' to 17, 'r' to 18,
        's' to 19, 't' to 20,
        'u' to 21, 'v' to 22,
        'w' to 23, 'x' to 24,
        'y' to 25, 'z' to 26
        )
    val lowercased = array.map { it.toLowerCase() }
    var missingLetter = 'a'
    
    lowercased.forEachIndexed { index, letter -> 
      if (index > 0) {
        if (alph[letter]!!.minus(alph[lowercased[index - 1]]!!) == 2) {
          for ((key, value) in alph) {
            if (value == alph[letter - 1]) {
                   missingLetter = key
            }
          }
        }
      }
    }
    
    if (array[0] == array[0].toUpperCase()) {
        missingLetter = missingLetter.toUpperCase()
    }
    
    return missingLetter
}
________________________
fun findMissingLetter(array: CharArray): Char =
    array.toList().windowed(2).first { it[0].inc() != it[1] }.first().inc()
