54cb771c9b30e8b5250011d4


import java.math.BigInteger
import java.math.BigInteger.ZERO
import java.math.BigInteger.valueOf

object Faberge {
    def height(n: BigInteger, m: BigInteger): BigInteger = {
    var i = BigInt(1)
    (BigInt(1) to BigInt(n)).foldLeft(BigInt(0)){ (acc,e) =>
      i=i*(BigInt(m)-e+1)/e
      acc+i
    }.bigInteger
  }
}
_________________________
import java.math.BigInteger
import java.math.BigInteger.ZERO
import java.math.BigInteger.valueOf

object Faberge {
  def height(n: BigInteger, t: BigInteger): BigInteger = {
  var res = new BigInteger("0")
  var fac = new BigInteger("1")
  var rounds = new BigInteger("0")
  var one = new BigInteger("1")
  while (rounds.compareTo(n)<0){
    fac = (fac.multiply(t.subtract(rounds)).divide(rounds.add(one)))
    res = res.add(fac)
    rounds = rounds.add(one)
  }
  return res
  }
}
_________________________
import java.math.BigInteger
import java.math.BigInteger.ZERO
import java.math.BigInteger.ONE

object Faberge {
  def height(n: BigInteger, m: BigInteger): BigInteger = {
    var c = ONE
    var s = ZERO
    var i = ZERO
    while (i.compareTo(n) < 0) {
      c = c.multiply(m.subtract(i))
      i = i.add(ONE)
      c = c.divide(i)
      s = s.add(c)      
    }
    s
  }
}
