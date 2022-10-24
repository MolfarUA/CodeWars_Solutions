51b6249c4612257ac0000005


package romannumerals

fun decode(str: String): Int 
{
    var ans = 0
    var prev = '_'
    for (token in str) 
    {        
        when (token)
        {
            'I' ->                                  ans += 1   
            'V' -> if (prev == 'I') ans += 3   else ans += 5
            'X' -> if (prev == 'I') ans += 8   else ans += 10
            'L' -> if (prev == 'X') ans += 30  else ans += 50
            'C' -> if (prev == 'X') ans += 80  else ans += 100
            'D' -> if (prev == 'C') ans += 300 else ans += 500
            'M' -> if (prev == 'C') ans += 800 else ans += 1000
        }
        prev = token
    }
    return ans
}
__________________________________
package romannumerals

val numbersMap = mapOf('M' to 1000, 'D' to 500, 'C' to 100, 'L' to 50, 'X' to 10, 'V' to 5, 'I' to 1)

fun decode(str: String): Int {

    var rawNumbers = str.map { char -> numbersMap.getOrElse(char, { null }) }.filterNotNull()
    var normalizedNumbers = rawNumbers.mapIndexed { i, num -> if (num < rawNumbers.elementAtOrElse(i + 1) { Int.MIN_VALUE }) -num else num }
    return normalizedNumbers.toIntArray().sum()
}
__________________________________
package romannumerals

fun decode (str:String):Int {
    var number=0
    var num=0
    var lastnum = 1000
    for (ch in str){
        when (ch){
            'I' ->  num = 1
            'V' -> num  =5
            'X' -> num = 10
            'L' -> num =50
            'C' -> num =100
            'D' -> num =500
            'M' -> num =1000
        }
        if (num <= lastnum) number +=num
            else number = number + (num-lastnum-lastnum)
        lastnum= num

    }

    return number
}
