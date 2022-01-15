package binary

fun code(str: String) = str.map {
    "$it".toInt().toString(2).run {
        "0".repeat(length - 1) + "1" + this
    }
}.joinToString("")


fun decode(str: String): String {
    var bits = 0
    var tempStr = ""
    var counter = -1
    while( ++counter < str.length){
        if(str[counter] == '1'){
            tempStr += "${str.substring(counter + 1, counter + ++bits + 1).toInt(2)}"
            counter += bits
            bits = 0
        }else bits++
    }
    return tempStr
}
__________________________
package binary

fun code(str: String): String {
    val res = StringBuilder()
    for (c in str.toCharArray()) {
        val b = Integer.toBinaryString(Character.getNumericValue(c))
        res.append("0".repeat(b.length - 1) + "1" + b)
    }
    return res.toString()
}
fun decode(str: String): String {
    val res = StringBuilder()
    var i = 0; var k = 1
    while (i < str.length) {
        if (str[i] == '1') {
            res.append(str.substring(i + 1, i + 1 + k).toInt(2))
            i += k; k = 0
        }
        i++; k++
    }
    return res.toString()
}
__________________________
package binary

fun getCode(): Array<String> {
    var answer: Array<String> = emptyArray()
    val str: String = "0123456789"
    for (element in str) {
        var buf: Int = element.toString().toInt()
        var elementBinCode: String
        if (buf == 0) elementBinCode = "0" else elementBinCode = ""
        while (buf > 0) {
            elementBinCode += (buf % 2).toString()
            buf /= 2
        }
        elementBinCode = elementBinCode.reversed()
        val k: Int = elementBinCode.length - 1
        answer += "0".repeat(k) + "1" + elementBinCode
    }
    return answer
}

fun code(str: String): String {
    var answer: String = ""
    val code: Array<String> = getCode()
    for (x in str) {
        answer += code[x.toString().toInt()]
    }
    return answer
}

fun decode(str: String): String {
    var answer: String = ""
    var buf: Int = 0
    while (buf < str.length) {
        var t: Int = str[buf].toString().toInt()
        buf++
        if (t == 1) { // 1*
            t = str[buf].toString().toInt()
            buf++
            if (t == 1) { // 11*
                answer += "1"
                continue
            } else if (t == 0) {  // 10*
                answer += "0"
                continue
            }
        } else if (t == 0) { // 0*
            t = str[buf].toString().toInt()
            buf++
            if (t == 1) {  // 01*
                t = str[buf].toString().toInt()
                buf++
                if (t == 1) { // 011*
                    t = str[buf].toString().toInt()
                    buf++
                    if (t == 1) { // 0111*
                        answer += "3"
                        continue
                    } else if (t == 0) { // 0110*
                        answer += "2"
                        continue
                    }
                } else if (t == 0) { // 010*
                    print("ERROR!!!")
                    return ""
                }
            } else if (t == 0) { // 00*
                t = str[buf].toString().toInt()
                buf++
                if (t == 1) { // 001*
                    buf += 1
                    t = str[buf].toString().toInt()
                    buf++
                    if (t == 1) { // 00111*
                        t = str[buf].toString().toInt()
                        buf++
                        if (t == 1) { // 001111*
                            answer += "7"
                            continue
                        } else if (t == 0) { // 001110*
                            answer += "6"
                            continue
                        }
                    } else if (t == 0) { // 00110*
                        t = str[buf].toString().toInt()
                        buf++
                        if (t == 1) { // 001101*
                            answer += "5"
                            continue
                        } else if (t == 0) { // 001100*
                            answer += "4"
                            continue
                        }
                    }
                } else if (t == 0) { // 000*
                    buf += 4
                    t = str[buf].toString().toInt()
                    buf++
                    if (t == 1) { // 00011001 *
                        answer += "9"
                        continue
                    } else if (t == 0) { // 00011001 *
                        answer += "8"
                        continue
                    }
                }
            }
        }
    }
    return answer
}
__________________________
package binary

import java.lang.StringBuilder
import kotlin.coroutines.CoroutineContext

fun code(str: String): String {
    val stringBuilder = StringBuilder()
    str.forEach {
        val bits = it.toString().toUInt().toString(radix = 2)
        repeat(bits.count() - 1) {
            stringBuilder.append("0")
        }
        stringBuilder.append("1").append(bits)
    }
    return stringBuilder.toString()
}

fun decode(str: String): String {
    val numList = arrayListOf<String>()
    var tempIndex = 0
    generateSequence(str) {
        if (it.isNotEmpty()) {
            if (it.first() == '1') {
                val restOf = it.drop(1)
                tempIndex++
                numList.add(restOf.take(tempIndex).toUInt(radix = 2).toString(radix = 10))
                val remaining = restOf.drop(tempIndex)
                tempIndex = 0
                remaining
            } else {
                tempIndex++
                it.drop(1)
            }
        } else null
    }.count()
    return numList.joinToString("")
}
__________________________
package binary

fun encodeDigit(digit: Char): String {
    val binaryString = Integer.toBinaryString(Integer.parseInt(digit.toString()))
    return "0".repeat(binaryString.length - 1) + "1" + binaryString
}

fun code(str: String): String {
    var encodedString = ""
    for (digitChar in str) {
        encodedString += encodeDigit(digitChar)
    }
    return encodedString
}

fun decode(str: String): String {
    var decoded = ""
    var position = 0
    // Find the position where the actual binary encoded number is.
    // Get the actual encoded number and decode it.
    // Set the counter to the next position and continue.
    while (position < str.length) {
        var length = 0
        while (str[position + length] != '1') length++
        // Add one more step to jump over last '1'
        length += 1
        // Set position to where actual number begins.
        position += length
        decoded += Integer.parseInt(str.substring(position, position + length), 2).toString()
        // Set position to after the current number, to parse the next one.
        position += length
    }
    return decoded
}
__________________________
package binary

fun code(str: String): String {
    val totalEncoding = StringBuilder()
    for(character in str) {

        val binaryRepresentation = Integer.toBinaryString(Integer.parseInt(character.toString()))
        val codedDigit = "0".repeat(binaryRepresentation.length - 1) + "1" + binaryRepresentation
        totalEncoding.append(codedDigit)
    }
    return totalEncoding.toString()
}
fun decode(str: String): String {
    val decodedString = StringBuilder()
    var previousDigits: Int = 0
    var i: Int = 0
    while (i <= str.length-1) {
        if(str[i] == '1') {
            val currentCypheredNumber = str.substring(i + 1, i + previousDigits + 2)
            decodedString.append(currentCypheredNumber.toInt(2))
            i += previousDigits + 1
            previousDigits = 0
        }
        else {
            previousDigits++
        }
        i++
    }
    return decodedString.toString()
}
