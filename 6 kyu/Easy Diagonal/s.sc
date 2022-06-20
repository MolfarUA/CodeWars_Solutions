559b8e46fa060b2c6a0000bf


object Diagonal {
  
  private def chooSE(n: Int, p: Int): BigInt = {
    var pp = p
    if (pp > n) return 0
    if (pp > n - pp) pp = n - pp
    var N: BigInt = BigInt(n)
    var ret: BigInt = 1
    for (i <- 0 until pp) {
      ret *= N - BigInt(i)
      ret /= BigInt(i) + 1
    }
    ret
  }
  def diagonal(n: Int, p: Int): BigInt = {
    chooSE(n+1, p+1)
  }
}
_____________________________
object Diagonal {
  
  def diagonal(n: Int, p: Int): BigInt = {
    var i = 1
    var last = new Array[BigInt](1)
    last(0) = 1
    while (i < (n + 2)) {
      val max = (i + 1) min (p + 2)
      val arr = new Array[BigInt](max)
      var j = 0
      while (j < max) {
        var sum: BigInt = 0
        if (j - 1 >= 0 && j - 1 < last.length) sum += last(j - 1)
        if (j >= 0 && j < last.length) sum += last(j)
        arr(j) = sum
        //print(sum + " ")
        j += 1
      }
      //println("")
      if (i == n + 1) return arr(p + 1)
      i += 1
      last = arr
    }
    
    return BigInt(0)
  }
}
_____________________________
object Diagonal {

  def diagonal(n: Int, p: Int): BigInt = {
    if (p == 0) n + 1
    else {
      val k = { 
        if (n / 2 < p) - 1 * (p - n) -1 
        else p
        }
      
      (BigInt(1) to n).sliding(k).map(s => s.product).sum/(BigInt(1) to k).product
    }
  }
}
