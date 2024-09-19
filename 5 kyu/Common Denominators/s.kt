package solution

object Fracts {
    
    fun convertFrac(lst: Array<LongArray>): String {
        val denoms = lst.map{ simplify(it) }.map{ it[1] }
        
        val ld = lcm(denoms.toLongArray())
        // numerator = fract * least denom, denom = ld (obviously)
        val commonFract = lst.map{ longArrayOf(((ld * it[0]) / it[1].toDouble()).toLong(), ld) }
        return commonFract.fold(""){ str, i -> str + "(${i[0]},${i[1]})" } // format
    }
    
    // least common multiple --> ggt(a, b) * kgv(a, b) = |a * b|
    fun lcm(numbers: LongArray): Long = numbers.fold(1L){ res, i -> i * res / gcd(i, res) }
    
    // greatest common divisor
    tailrec fun gcd(a: Long, b: Long): Long = when (b) {
        0L -> a
        else -> gcd(b, a % b)
    }
    
    // SIMPLIFY FIRST!!! lcm != lcd
    fun simplify(fract: LongArray): LongArray {
        val gcdenom = gcd(fract[0], fract[1])
        return longArrayOf(fract[0] / gcdenom, fract[1] / gcdenom)
    }
}
##############################
package solution

object Fracts {  
    fun gcd(a: Long, b: Long): Long = if (b == 0L) a else gcd(b, a % b)
    fun convertFrac(lst0: Array<LongArray>): String {
        val lst = lst0.map { (a, b) -> gcd(a, b).let { arrayOf(a/it, b/it) } }
        val d = lst.map{it[1]}.fold(1L) { a, b -> (a / gcd(a, b)) * b }
        return lst.map { (a, b) -> d / b * a }.joinToString ("") { n -> "($n,$d)" }
    }
}
################################
package solution
import kotlin.math.max


object Fracts {
    
    fun gcd(n1: Int, n2: Int): Int {
        var n1 = n1
        var n2 = n2
        while (n1 != n2) {
            if (n1> n2)
                n1 -= n2
            else
                n2 -= n1
        }
        return n1
    }

    fun hcf(n1: Int, n2: Int): Int{
        return (n1*n2)/gcd(n1,n2)
    }

    fun convertFrac(lst: Array<LongArray>): String {
        var filteredLst: MutableList<LongArray> = lst.toMutableList()
        var k: Int // here numbers gcd

        var denominators = 1

        for (i in 0 until filteredLst.size){
            k = gcd(filteredLst[i][0].toInt(), filteredLst[i][1].toInt())

            filteredLst[i][0] = filteredLst[i][0] / k
            filteredLst[i][1] = filteredLst[i][1] / k

            denominators = hcf(filteredLst[i][1].toInt(), denominators)
        }

        var ans = ""
        for (number in filteredLst){
            ans += "(${number[0] * (denominators / number[1])},$denominators)"
        }

        return ans
    }
}
