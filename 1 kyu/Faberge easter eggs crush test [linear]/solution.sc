object Faberge {    
    def height(n: BigInt, m: BigInt): BigInt = {
      val MOD: BigInt = BigInt(998244353)
      var h = BigInt(0);
      var u = BigInt(1);
      for (i <- BigInt(1) to n) {
        u = (u * (m + 1 - i) * i.modInverse(MOD)).mod(MOD);
        h = (h + u).mod(MOD);
      }
      return h;
    }
}
__________________________________________________
import java.math.BigInteger

object Faberge {
    
    val mo = BigInt(998244353).bigInteger;
  
    var reg = new Array[BigInteger](80001);
    reg(0) = BigInteger.valueOf(0);
    reg(1) = BigInteger.valueOf(1);
    var j = 2;
    while (j <= 80000) {
        var bj = BigInteger.valueOf(j);
        reg(j) = mo.subtract(mo.divide(bj)).multiply(reg(mo.mod(bj).intValue()).mod(mo));
        j += 1;
    }
    
    def height(n: BigInt, m0: BigInt): BigInt = {
        var m = m0.bigInteger;
        var h = BigInteger.ZERO;
        var t = BigInteger.ONE;
        var i = 1;
        m = m.mod(mo);
        while (i <= n.bigInteger.intValue()) {
            var bi = BigInteger.valueOf(i);
            t = t.multiply(m.subtract(bi).add(BigInteger.ONE)).multiply(reg(i)).mod(mo);
            h = h.add(t);
            i += 1;
        }
        return h.mod(mo);
    }
}
__________________________________________________
object Faberge {
    
  val MOD:BigInt = BigInt(998244353)
    
    def sub_height(n:BigInt,k:BigInt):BigInt = {
      var (s,nm,dm,i) = (BigInt(0),BigInt(1),BigInt(1),BigInt(0))
      while(i<k){
        val nn = (nm*(n-i))%MOD
        val nd = (dm*(i+1))%MOD
        s = (s+nn*nd.modPow(MOD-2, MOD))%MOD
        nm=nn
        dm=nd
        i+=1
      }
      s
    }

    def height(n: BigInt, m: BigInt): BigInt = {
      val mm = m%MOD

      if(n>mm) (BigInt(2).modPow(mm,MOD)- 1) % MOD
      else if (n>mm/2L) ((MOD-2) + BigInt(2).modPow(mm,MOD) - height(mm-n-1,mm))%MOD
      else sub_height(mm%MOD, n)
    }
}
__________________________________________________
object Faberge {
  
    val MOD: BigInt = BigInt(998244353)
    val mod = 998244353


    val sum_prod: Array[BigInt] = (2 to 80000).foldLeft(Array(BigInt(0),BigInt(1)))((a, i)=>a:+((MOD-(MOD/i))*a(mod%i))%MOD)

    def height(n: BigInt, m: BigInt): BigInt = {
      val nm = m%MOD
      var (s, p) = (BigInt(0),BigInt(1))

      (1 to n.intValue).foreach(i=>{
        p = (((p*(nm- i +1))%mod)* sum_prod(i))%mod
        s = (s+p)%mod
      })
      s%mod
    }
}
