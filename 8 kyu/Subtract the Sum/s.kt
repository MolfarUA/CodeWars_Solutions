56c5847f27be2c3db20009c3

fun subtractSum(n: Int) = "apple"
_______________________________________
fun subtractSum(n: Int): String = "apple"
_______________________________________
fun subtractSum(n: Int): String {
    val fruit = arrayOf("kiwi","pear","banana","melon","pineapple","apple","cucumber","orange","grape","cherry")
    val list = arrayOf(0,0,1,0,2,3,2,3,4,5,4,6,4,6,7,8,7,8,5,8,9,1,9,1,0,2,0,5,3,2,3,4,3,4,6,7,5,7,8,7,8,9,1,9,1,5,1,1,2,1,2,3,4,3,5,6,4,6,7,6,7,8,9,5,9,1,9,1,0,1,0,2,5,2,3,4,3,4,6,4,6,6,8,7,8,9,8,9,1,9,5,0,2,0,2,3,2,3,4,5,4)
    var num = n
    
    if(num >= 10 && num < 10000) {
        for(i in 0..num) {
            var sum = num-(num.toString().toList().map{it.toString().toInt()}.sum())
            num = sum
            if(sum<=100) break
        }
    }
    
    return fruit[list[num]]
} 
_______________________________________
fun subtractSum(n: Int): String {
    return "apple"
}
_______________________________________
fun subtractSum(n: Int): String {

    var num = n - n.weight
    while (num !in 1..100) num -= num.weight

    return arrayOf("kiwi", "pear", "kiwi", "banana", "melon", "banana", "melon", "pineapple", "apple", "pineapple",
        "cucumber", "pineapple", "cucumber", "orange", "grape", "orange", "grape", "apple", "grape", "cherry",
        "pear", "cherry", "pear", "kiwi", "banana", "kiwi", "apple", "melon", "banana", "melon",
        "pineapple", "melon", "pineapple", "cucumber", "orange", "apple", "orange", "grape", "orange", "grape",
        "cherry", "pear", "cherry", "pear", "apple", "pear", "kiwi", "banana", "kiwi", "banana",
        "melon", "pineapple", "melon", "apple", "cucumber", "pineapple", "cucumber", "orange", "cucumber", "orange",
        "grape", "cherry", "apple", "cherry", "pear", "cherry", "pear", "kiwi", "pear", "kiwi",
        "banana", "apple", "banana", "melon", "pineapple", "melon", "pineapple", "cucumber", "pineapple", "cucumber",
        "apple", "grape", "orange", "grape", "cherry", "grape", "cherry", "pear", "cherry", "apple",
        "kiwi", "banana", "kiwi", "banana", "melon", "banana", "melon", "pineapple", "apple", "pineapple"
    )[num - 1]
}

val Int.weight: Int get() = this.toString().toCharArray().sumOf { it.digitToIntOrNull() ?: 0 }
