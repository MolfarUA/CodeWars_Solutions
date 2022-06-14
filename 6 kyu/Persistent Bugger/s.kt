fun persistence(num: Int) = generateSequence(num) {
        it.toString().map(Character::getNumericValue).reduce { mult, element -> mult * element }
    }.takeWhile { it > 9 }.count()
________________________________________
fun persistence(num: Int) : Int {
    var counter = 0
    var n: Int
    var mul = num
    while (mul >= 10) {
        var temp = 1
        while (mul > 0) {
            n = mul % 10
            temp *= n
            mul /= 10
        }
        mul = temp
        counter++
    }
    return counter
}
________________________________________
fun persistence(num: Int): Int =
    if (num < 10) 0 else 1 + persistence(num.toString().map { it - '0' }.reduce(Int::times))

val zeroAscii = '0'.toInt()  // fixing the bug in tests
________________________________________
tailrec fun persistence(num: Int, counter: Int = 0): Int =
    if (num < 10) counter
    else persistence(num.toString().map(Character::getNumericValue).reduce(Int::times), counter+1)
________________________________________
fun persistence(input: Int) : Int {
    var ans = 0
    var num = input
    while (num >= 10) {
        var temp = 1
        while (num != 0) {
            temp *= num % 10
            num = num / 10
            println(num)
        }
        num = temp
        ans += 1
    }
    return ans
}
________________________________________
fun persistence(num: Int) : Int {
    return num.toString()
            .also { if (it.length == 1) return 0 }
            .fold(1) { acc, c -> acc * c.toString().toInt() }
            .let { persistence(it) + 1 }
}
