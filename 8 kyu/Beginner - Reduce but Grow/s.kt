57f780909f7e8e3183000078


package reducebutgrow

fun grow(arr: IntArray): Int = arr.reduce { a, b -> a * b }
_______________________
package reducebutgrow

fun grow(arr: IntArray) = arr.reduce(Int::times)
_______________________
package reducebutgrow

fun grow(arr: IntArray): Int {
    var result : Int =1
    arr.forEach {
        result *= it
    }
    return result
}
