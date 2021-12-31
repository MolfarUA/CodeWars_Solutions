package dbllinear

fun dblLinear(n: Int) = with(sortedSetOf(1)) {
    for (i in 1..n) {
        val x = first().also { remove(it) }
        add(x * 2 + 1)
        add(x * 3 + 1)
    }
    first()
}

__________________________________________________
package dbllinear

fun dblLinear(n:Int) = with(sortedSetOf(1)) {
        for(i in 1..n) {
            val x = pollFirst()
            add((x * 2) + 1)
            add((x * 3) + 1)
        }
        first()
}

__________________________________________________
package dbllinear

fun dblLinear(n: Int): Int {
  val list = mutableListOf(1)
  var x = 0
  var y = 0

  while(list.size <= n) {
    val a = 2 * list[x] + 1
    val b = 3 * list[y] + 1

    when {
      a > b -> {
        list.add(b)
        y++
      }
      a < b -> {
        list.add(a)
        x++
      }
      else -> {
        list.add(a)
        x++
        y++
      }
    }
  }
  return list[n]
}
