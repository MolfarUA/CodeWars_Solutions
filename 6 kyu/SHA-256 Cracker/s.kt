587f0abdd8730aafd4000035


import java.security.MessageDigest
import javax.xml.bind.DatatypeConverter

fun crackSha256(hash: String, chars: String): String? {
    val hashBytes = DatatypeConverter.parseHexBinary(hash)
    val digest = MessageDigest.getInstance("SHA-256")
    return permutations(chars).firstOrNull { hashBytes.contentEquals(digest.digest(it.toByteArray())) }
}

private fun permutations(s: String): Sequence<String> = sequence {
    if (s.length <= 1) {
        yield(s)
    } else {
        for (i in 0 until s.length) {
            yieldAll(permutations(s.removeRange(i, i + 1)).map { s[i] + it })
        }
    }
}
_________________________
import java.math.BigInteger
import java.security.MessageDigest

fun crackSha256(hash: String, chars: String): String? = stringPermutationWithRecursion(chars)
    .firstOrNull {
        hash == "%064x".format(BigInteger(1, MessageDigest.getInstance("SHA-256").digest(it.toByteArray())))
    }

fun stringPermutationWithRecursion(string: String): Set<String> {
    if (string.length == 1)
        return setOf(string)

    val allCharsExceptLast = string.substringBeforeLast("")
    val lastChar = string.last()
    val permutations = stringPermutationWithRecursion(allCharsExceptLast)
    val allPermutations = mutableSetOf<String>()

    for (permutation in permutations) {
        val n = allCharsExceptLast.length
        for (i in 0..n) {
            val newP = permutation.substring(0, i) + lastChar + permutation.substring(i, n)
            allPermutations.add(newP)
        }
    }
    return allPermutations
}
_________________________
fun crackSha256(hash: String, chars: String): String? {
    
    print ("$hash ?= [$chars] ")
    
    val word = chars
    val len = word.length
    if (len > 10 || len < 1) return null
    val md = java.security.MessageDigest.getInstance("SHA-256")
    
    val factorials = mutableListOf(1)
    (1..len).forEach { factorials.add(factorials[it-1] * it) }
    
    (0..factorials[len]-1).forEach { i ->
        var onePermutation = ""
        var temp = word
        var positionCode = i
        (len downTo 1).forEach { position ->
            val selected = positionCode / factorials[position-1]
            onePermutation += temp.get(selected)
            positionCode = positionCode % factorials[position-1]
            temp = temp.substring(0,selected) + temp.substring(selected+1)
        }
            val hash_candidate = md      
                        .digest(onePermutation.toByteArray())
                        .fold("", { str, it -> str + "%02x".format(it) })
            if (hash_candidate == hash) {
                println ("FOUND $onePermutation")
                return onePermutation
            }
        
    }

    println ("NOT FOUND")
    return null
}
