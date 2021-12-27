object Immortal {
  /**
    * set true to enable debug
    */
  val debug = true
  
  def larger_pow(x: BigInt, t: BigInt = 1): BigInt = {
    if (t < x) return larger_pow(x, t << 1)
    return t
  }

  def range_sum(l: BigInt, r: BigInt): BigInt = {
    return ((l + r) * (r - l + 1) / 2)
  }

  def elderAge(mA: BigInt, nA: BigInt, l: BigInt, t: BigInt): Long = {
    var n = nA
    var m = mA
    if (m == 0 || n == 0) return 0
    if (m > n) {
      val tmp = m
      m = n
      n = tmp
    }
    
    var ln = larger_pow(n)
    var lm = larger_pow(m)
    if (l > ln) return 0

    if (lm == ln) return ((range_sum(1, ln - l - 1) * (m + n - ln) + elderAge(ln - n, lm - m, l, t)).mod(t)).toLong
    
    if (lm < ln) {
        lm = (ln / 2)
        var tmp = range_sum(1, ln - l - 1) * m - (ln - n) * range_sum((lm - l).max(0), ln - l - 1)
        if (l <= lm) tmp += (lm - l) * (lm - m) * (ln - n) + elderAge(lm - m, ln - n, 0, t)
        else tmp += elderAge(lm - m, ln - n, l - lm, t)
        return tmp.mod(t).toLong
     }
     
     return 0
  }
}
____________________________________
import java.math.BigDecimal

object Immortal {
  /**
    * set true to enable debug
    */
  val debug = false

  def elderAge(m: Long, n: Long, l: Long, t: Long): Long = if (m <= 0 || n <= 0) 0
  else if (m < n) elderAge(n, m, l, t)
  else {
    val minRecM = biggestPowOfTwo(m)
    ((calcSum(l, minRecM, t) * (Math.min(n, minRecM) % t)) % t + elderAge(m - minRecM, n - minRecM, l, t) % t + elderAge(minRecM, n - minRecM, l - minRecM, t) % t + elderAge(m - minRecM, Math.min(n, minRecM), l - minRecM, t) % t) % t
  }

  def biggestPowOfTwo(n: Long): Long = if (n == 1) 1
  else 2 * biggestPowOfTwo(n / 2)

  def calcSum(l: Long, m: Long, t: Long): Long = if (l > m) 0
  else new BigDecimal((Math.abs(Math.min(l, 0)) + m - 1 - l) % (2 * t)).multiply(new BigDecimal((m - l - Math.abs(Math.min(l, 0))) % (2 * t))).divide(new BigDecimal(2)).divideAndRemainder(new BigDecimal(t))(1).longValue
  
}
______________________________
object Immortal {
    /**
     * set true to enable debug
     */
    val debug = false

    def process(m0: Long, n0: Long, l: Long, t:Long): Long = {
      val (mm, nn) = if(m0>=n0) (m0,n0) else (n0,m0)

      if(mm<100L){
        (0L until mm).flatMap(i=>(0L until nn).map(j=>{
          Math.max((i ^ j)-l, 0L)
        })).sum%t
      }
      else if(nn==1L) {
        if((mm-l)%2L==0L) (((Math.max(mm-l, 0L)/2L)%t) *(Math.max(mm-l-1L, 0L)%t))%t
        else (((Math.max(mm-l-1L, 0L)/2L)%t) *(Math.max(mm-l, 0L)%t))%t
      }
      else{
        val p = Math.log(mm)/Math.log(2L)
        val m1 = (if(p.toLong==p) mm else Math.pow(2L, p.toLong)).toLong

        val l0 = Math.max(0L, l-m1)
        val l1 =  Math.max(0L, m1-l)
        val l2 = Math.max(0L, m1-l0)
        val l2i = Math.max(0L, m1-l0-1L)

        val s = if(l1%2L==0L) (((l1/2)%t)*(Math.max(0L, m1-l-1L)%t))%t else (((Math.max(0L, m1-l-1L)/2)%t)*(l1%t))%t

        if(m1<mm) {
          if(nn<=m1){
            ((((nn%t)*s)%t)+(process(mm-m1, nn, l0, t)+((((nn%t)*((mm-m1)%t))%t)*(l1%t))%t)%t)%t
          }
          else ((((((m1%t)*s)%t)+((((({
            if(l2%2L==0L) (l2i%t) *((l2/2L)%t)
            else ((l2i/2L)%t)*(l2%t)
          }%t)+(((m1%t) *(l1%t))%t))%t)*(((nn-m1)+(mm-m1))%t))%t))%t)+process(mm-m1, nn-m1, l, t))%t
        }
        else if(nn<=m1) ((nn%t)*s)%t
        else ((((m1%t)*s)%t)+((((({
          if(l2%2L==0L) (l2i%t) *((l2/2L)%t)
          else ((l2i/2L)%t)*(l2%t)
        }%t)+((m1 *l1)%t))%t)*((nn-m1)%t))%t))%t
      }
    }

    def elderAge(m: Long, n: Long, l: Long, t: Long): Long = {
      process(m, n, l, t)%t
    }
  }
  
______________________________________________
object Immortal {
  /**
    * set true to enable debug
    */
  val debug = true
  val limit = 17179869184L

  def process(m0: Long, n0: Long, l: Long, t:Long): Long = {
      val (mm, nn) = if(m0>=n0) (m0,n0) else (n0,m0)

      if(mm<100L){
        (0L until mm).flatMap(i=>(0L until nn).map(j=>{
          Math.max((i ^ j)-l, 0L)
        })).sum%t
      }
      else if(nn==1L) {
        if((mm-l)%2L==0L) (((Math.max(mm-l, 0L)/2L)%t) *(Math.max(mm-l-1L, 0L)%t))%t
        else (((Math.max(mm-l-1L, 0L)/2L)%t) *(Math.max(mm-l, 0L)%t))%t
      }
      else{
        val p = Math.log(mm)/Math.log(2L)
        val m1 = (if(p.toLong==p) mm else Math.pow(2L, p.toLong)).toLong

        val l0 = Math.max(0L, l-m1)
        val l1 =  Math.max(0L, m1-l)
        val l1i =  Math.max(0L, m1-l-1L)
        val l2 = Math.max(0L, m1-l0)
        val l2i = Math.max(0L, m1-l0-1L)

        val s = if(l1%2L==0L) (((l1/2)%t)*(l1i%t))%t else (((l1i/2)%t)*(l1%t))%t

        if(m1<mm) {
          if(nn<=m1){
            ((((nn%t)*s)%t)+(process(mm-m1, nn, l0, t)+((((nn%t)*((mm-m1)%t))%t)*(l1%t))%t)%t)%t
          }
          else ((((((m1%t)*s)%t)+((((({
            if(l2%2L==0L) (l2i%t) *((l2/2L)%t)
            else ((l2i/2L)%t)*(l2%t)
          }%t)+(((m1%t) *(l1%t))%t))%t)*(((nn-m1)+(mm-m1))%t))%t))%t)+process(mm-m1, nn-m1, l, t))%t
        }
        else if(nn<=m1) ((nn%t)*s)%t
        else ((((m1%t)*s)%t)+((((({
          if(l2%2L==0L) (l2i%t) *((l2/2L)%t)
          else ((l2i/2L)%t)*(l2%t)
        }%t)+((m1 *l1)%t))%t)*((nn-m1)%t))%t))%t
      }
    }

    def elderAge(m: Long, n: Long, l: Long, t: Long): Long = {
      process(m, n, l, t)%t
    }
  }
