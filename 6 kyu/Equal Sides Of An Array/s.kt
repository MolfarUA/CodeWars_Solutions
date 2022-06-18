object EqualSidesOfAnArray {
  fun findEvenIndex(arr:IntArray):Int {
    for (i in arr.indices) {
      if (arr.sliceArray(0..i).sum() == arr.sliceArray(i..(arr.size - 1)).sum()) {
        return i
      }
    }
    return -1
  }
}
________________________
object EqualSidesOfAnArray {
    fun findEvenIndex(arr: IntArray) = arr.indices.indexOfFirst { arr.take(it).sum() == arr.drop(it + 1).sum() }
}
________________________
object EqualSidesOfAnArray {
    fun findEvenIndex(arr: IntArray): Int {
        if (arr.isEmpty()) return 0
        val sumTotal = arr.sum()
        arr.foldIndexed(0) { index, sumLeft, value ->
            if (sumLeft * 2 + value == sumTotal) return index
            sumLeft + value
        }
        return -1
    }
}
________________________
object EqualSidesOfAnArray {
  fun findEvenIndex(arr:IntArray):Int {
     var rightSum = arr.sum()
     var leftSum = 0
     for (i in 0..arr.size-1) {
        rightSum = rightSum - arr[i]
        if (rightSum == leftSum) return i
        leftSum = leftSum + arr[i]
     }
    return -1
  }
}
________________________
object EqualSidesOfAnArray {
  fun findEvenIndex(arr:IntArray):Int {
    return (
      arr.mapIndexed({ i:Int ,v:Int -> 
        arr.slice(0..i-1).sum() - arr.slice(i+1..arr.size).sum() 
      }) 
      .indexOf(0)
    )
  }
}
