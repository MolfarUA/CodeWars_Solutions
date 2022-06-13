object Cube {

  def findNb(m: Long, n: Long = 0, v: Long = 0): Long =
    if (v == m) n-1 else if (v < m) findNb(m, n+1, v+n*n*n) else -1
}
_________________________________________
object Cube {
  def getVal(n: Long): Long = (n*(n+1)/2)*(n*(n+1)/2)
  def binarySearch(l: Long, r: Long, v: Long):Long = {
    //println(l,r)
    val mid = (l+r)>>1
    if(l == r-1) l
    else if(getVal(mid) > v) binarySearch(l,mid,v)
    else binarySearch(mid,r,v)
  }
  def findNb(m: Long): Long = {
    val v = binarySearch(0,100000,m)
    if(getVal(v) == m) v
    else -1
  }
}
_________________________________________
object Cube {
  def findNb(m: Long): Int = {
    @annotation.tailrec
    def _findNb(n: Int, acc: Long): Int = {
      acc match {
        case `m` => n - 1
        case gt if ( acc > m ) => -1
        case _ =>  _findNb(n + 1, acc + Math.pow(n, 3).toLong)
        }
      }
    _findNb(1, 0)
  }
}
