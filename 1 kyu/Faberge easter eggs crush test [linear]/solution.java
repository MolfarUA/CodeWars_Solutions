import java.math.BigInteger;

public class Faberge {

  private static BigInteger mo = BigInteger.valueOf(998244353);

  static final int MAX_NUMBER = 100_000;
  static final BigInteger[] MOD_INVERSES = new BigInteger[MAX_NUMBER + 1];

  // precompute modular inverses
  static {
    MOD_INVERSES[0] = BigInteger.ONE;
    for (int i = 1; i <= MAX_NUMBER; ++i) {
      MOD_INVERSES[i] = BigInteger.valueOf(i).modInverse(mo);
    }
  }

  public static BigInteger height(BigInteger n, BigInteger m) {

    // reduce number of tries according to modulus
    m = m.mod(mo);

    if (n.compareTo(m) >= 0) {
      return BigInteger.TWO.modPow(m, mo).subtract(BigInteger.ONE);
    }

    // sums up at most half of the binomial coefficients
    BigInteger flipped = null;
    if (BigInteger.TWO.multiply(n).compareTo(m) > 0) {
      n = m.subtract(n).subtract(BigInteger.ONE);
      flipped = BigInteger.TWO.modPow(m, mo).subtract(BigInteger.TWO);
    }


    BigInteger res = BigInteger.ZERO;
    BigInteger tmp = BigInteger.ONE;

    for (int i = 1; i <= n.intValue(); ++i) {
      tmp = tmp.multiply(m.add(BigInteger.valueOf(1 - i))).multiply(MOD_INVERSES[i]).mod(mo);
      res = res.add(tmp).mod(mo);
    }

    if (flipped != null) {
      return flipped.subtract(res).mod(mo);
    }
    return res;
  }
}
__________________________________________________
import java.math.BigInteger;

public class Faberge {
  private static BigInteger mo = BigInteger.valueOf(998244353);
  
  public static BigInteger height(BigInteger n, BigInteger m) {
    BigInteger ret = BigInteger.ZERO;
    BigInteger binom = BigInteger.ONE;
    for (BigInteger i = BigInteger.ONE; i.compareTo(n) <= 0; i = i.add(BigInteger.ONE)) {
      binom = binom.multiply(m.subtract(i).add(BigInteger.ONE)).multiply(i.modInverse(mo)).mod(mo);
      ret = ret.add(binom).mod(mo);
    }
    return ret;
  }

}
__________________________________________________
import java.math.BigInteger;

public class Faberge{
    private static BigInteger moduler = BigInteger.valueOf(998244353);

    public static BigInteger height(BigInteger n, BigInteger m){
        BigInteger sum = BigInteger.ZERO;
        BigInteger res = BigInteger.ONE;
        m = m.mod(moduler);

        for (BigInteger i = BigInteger.ONE; i.compareTo(n) <= 0; i = i.add(BigInteger.ONE)){
            res = (res.multiply(m.subtract(i).add(BigInteger.ONE))).mod(moduler)
                    .multiply(i.modPow(moduler.subtract(BigInteger.valueOf(2)), moduler));

            sum = sum.add(res).mod(moduler);
        }

        return sum;
    }
}
