package besttravel

fun chooseBestSum(t:Int, k:Int, ls:List<Int>):Int {
    fun calcBest(startFrom: Int, accumulated: Int, k: Int): Int {
        if (ls.size - startFrom < k) return -1
        if (accumulated > t) return -1
        if (k == 0) return accumulated
        return calcBest(startFrom + 1, accumulated + ls[startFrom], k - 1)
            .coerceAtLeast(calcBest(startFrom + 1, accumulated, k))
    }
    return calcBest(0, 0, k)
}
_______________________________________
package besttravel

fun chooseBestSum(t:Int, k:Int, ls:List<Int>, n:Int = 0, d:Int = 0):Int {
  if (k == 0 && d <= t) return d
  if (d > t || n >= ls.size) return -1
  return maxOf(chooseBestSum(t, k - 1, ls, n + 1, d + ls[n]), chooseBestSum(t, k, ls, n + 1, d))
}
_______________________________________
package besttravel

fun <T> List<T>.combinations(n: Int): List<List<T>> =
    this.foldIndexed(listOf())
    { i, acc, e ->
        acc + if (n > 1) {
            this.drop(i + 1)
                .combinations(n - 1)
                .map { it + e }
        } else listOf(listOf(e))
    }

fun chooseBestSum(t:Int, k:Int, ls:List<Int>):Int {
    if(k > ls.size) return -1
    if(k == ls.size) return ls.sum().let { if (it <= t) it else -1 }
    return ls.combinations(k)
        .map(List<Int>::sum)
        .filter { it <= t }.max() ?: -1
}
_______________________________________
package besttravel

fun chooseBestSum(t:Int, k:Int, ls:List<Int>):Int {
    val result = combinations(t, k, ls, 0)
    if (result > 0) {
        return result
    }
    return -1
}

fun combinations(t:Int, k:Int, ls:List<Int>, i:Int):Int {
    if (k == 0 && t >= 0) {
        return 0
    } else if (k < 0 || i>= ls.size) {
        return Integer.MIN_VALUE
    } else  {
        return Integer.max(combinations(t, k, ls, i + 1), ls.get(i) + combinations(t - ls.get(i), k - 1, ls, i + 1))
    }
}
_______________________________________
package besttravel

fun chooseBestSum(t: Int, k: Int, ls: List<Int>, array: IntArray = IntArray(k), start: Int = 0, end: Int = ls.size - 1, currentIndex: Int = 0, sum: HashSet<Int> = hashSetOf()): Int {
    if (currentIndex == k) {
        if (array.sum() <= t) sum.add(array.sum())
        return sum.max() ?: -1
    }

    for (i in start..end) {
        array[currentIndex] = ls[i]
        chooseBestSum(t, k, ls, array, i + 1, end, currentIndex + 1, sum)
    }
    return sum.max() ?: -1
}
_______________________________________
package besttravel

import java.util.ArrayList
import java.util.Arrays

fun chooseBestSum(t:Int, k:Int, ls:List<Int>):Int {
    var result = -1
    for (i in ls.indices)
    {
      if (ls.get(i) <= t)
      {
        if (k == 1)
        {
          result = Math.max(result, ls.get(i))
        }
        else
        {
          val temp = chooseBestSum(t - ls.get(i), k - 1, ls.subList(i + 1, ls.size))
          if (temp != -1)
          {
            result = Math.max(result, ls.get(i) + temp)
          }
        }
      }
    }
    if (result < 0) return -1
    return result
}
