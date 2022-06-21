5263c6999e0f40dee200059d


val adj = mapOf(
    '1' to setOf('1', '2', '4'),
    '2' to setOf('2', '1', '3', '5'),
    '3' to setOf('3', '2', '6'),
    '4' to setOf('4', '1', '5', '7'),
    '5' to setOf('5', '2', '4', '6', '8'),
    '6' to setOf('6', '3', '5', '9'),
    '7' to setOf('7', '4', '8'),
    '8' to setOf('8', '0', '5', '7', '9'),
    '9' to setOf('9', '6', '8'),
    '0' to setOf('0', '8')
)

fun getPINs(observed: String): List<String> {
    return observed
        .map { adj[it] }.toTypedArray().fold(listOf(listOf<Char>())) { acc, set ->
            acc.flatMap { list -> set?.map { element -> list + element } ?: listOf() }
        }.toSet().map { String(it.toCharArray()) }
}
______________________________
fun getPINs(observed: String) = allPossibleCombinations(observed.map{getAdjacent(it)})

fun allPossibleCombinations (arr: List<List<Char>>) : List<String> {
  if(arr.size == 1) {
        return arr[0].map{"$it"}
  } else {
        val result = mutableListOf<String>()
        val allCombinationsOfRest = allPossibleCombinations(arr.drop(1))
        allCombinationsOfRest.indices.forEach {i->
          arr[0].indices.forEach {j->
            result.add("" + arr[0][j] + allCombinationsOfRest[i]);
          }
        }
        return result;
  }
}

fun getAdjacent (num : Char) : List<Char> =
//    ┌───┬───┬───┐
//    │ 1 │ 2 │ 3 │
//    ├───┼───┼───┤
//    │ 4 │ 5 │ 6 │
//    ├───┼───┼───┤
//    │ 7 │ 8 │ 9 │
//    └───┼───┼───┘
//        │ 0 │
//        └───┘
  when(num) {
      '1'  ->  listOf('1','4','2')
      '2'  ->  listOf('2','1','3','5')
      '3'  ->  listOf('3','2','6')
      '4'  ->  listOf('4','1','5','7')
      '5'  ->  listOf('5','4','2','6','8')
      '6'  ->  listOf('6','3','5','9')
      '7'  ->  listOf('7','4','8')
      '8'  ->  listOf('8','7','5','9','0')
      '9'  ->  listOf('9','8','6')
      '0'  ->  listOf('0','8')
      else ->  listOf(' ')
  }
______________________________
fun padLock(touched: Char) = when (touched) {
    '1' -> listOf(1, 2, 4)
    '2' -> listOf(1, 2, 3, 5)
    '3' -> listOf(2, 3, 6)
    '4' -> listOf(1, 4, 5, 7)
    '5' -> listOf(2, 4, 5, 6, 8)
    '6' -> listOf(3, 5, 6, 9)
    '7' -> listOf(4, 7, 8)
    '8' -> listOf(5, 7, 8, 9, 0)
    '9' -> listOf(6, 8, 9)
    '0' -> listOf(8, 0)
    else -> error("touched $touched")
}.map { it.toString() }

fun getPINs(observed: String): List<String> = observed
    .map { padLock(it) }
    .reduce { acc, pins -> pins.flatMap { a -> acc.map { it + a } } }
    .distinct()
