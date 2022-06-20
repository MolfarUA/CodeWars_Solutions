559b8e46fa060b2c6a0000bf


import java.math.BigInteger;

public class Diagonal {

  public static BigInteger diagonal(int n, int p) {
    BigInteger result = binomial(n,p).add(binomial(n,p+1));
    return result;
  }
  private static BigInteger binomial(final int N, final int K) {
    BigInteger ret = BigInteger.ONE;
    for (int k = 0; k < K; k++) {
        ret = ret.multiply(BigInteger.valueOf(N-k))
                 .divide(BigInteger.valueOf(k+1));
    }
    return ret;
  }
}
_____________________________
import static java.lang.String.valueOf;
import java.math.BigInteger;

public class Diagonal {

  public static BigInteger diagonal(int n, int p) {
      BigInteger result = BigInteger.valueOf(0l);
        for(int line = 1; line <= n+1; line++) {
            BigInteger C = BigInteger.valueOf(1l);
            for(int i = 1; i <= p+1; i++) {
                if (i == p+1) {
                    result = result.add(C);
                }
                C = C.multiply (BigInteger.valueOf(line - i))
                  .divide(BigInteger.valueOf(i));
            }
        }
        return result;
    }
}  
_____________________________
import static java.math.BigInteger.ONE;
import static java.math.BigInteger.valueOf;

import java.math.BigInteger;

interface Diagonal {
  static BigInteger diagonal(int n, int p) {
    var sum = ONE;
    var bp = valueOf(p);
    for (BigInteger i = ONE, prev = ONE; i.intValue() < n - p + 1; i = i.add(ONE)) {
      prev = prev.multiply(bp.add(i)).divide(i);
      sum = sum.add(prev);
    }
    return sum;
  }
}
