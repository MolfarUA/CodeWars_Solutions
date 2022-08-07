54cb771c9b30e8b5250011d4


import java.math.BigInteger;

public class Faberge {
  public static BigInteger height(BigInteger n, BigInteger m) {
    BigInteger x = n;
    BigInteger t = BigInteger.ONE;
    BigInteger h = BigInteger.ZERO;
    while (x.compareTo(BigInteger.ZERO) != 0) {
      BigInteger e = t.multiply(m.subtract(n).add(x)).divide(n.add(BigInteger.ONE).subtract(x));
      x = x.subtract(BigInteger.ONE);
      t = e;
      h = h.add(e);
    }
    return h;
  }
}
_________________________
import java.math.BigInteger;

import static java.math.BigInteger.ZERO;
import static java.math.BigInteger.valueOf;

public class Faberge {
  public static BigInteger height(BigInteger n, BigInteger m) {
    if (n.equals(ZERO) || m.equals(ZERO)) return ZERO;
    if (n.compareTo(m) > 0) n = m;
    BigInteger c = valueOf(1);
    BigInteger b = valueOf(1);
    BigInteger a = valueOf(0);
    while (c.compareTo(n) <= 0) {
      BigInteger d = m.add(valueOf(1)).subtract(c).multiply(b).divide(c);
      c = c.add(valueOf(1));
      b = d;
      a = a.add(d);
    }
    return a;
  }
}
_________________________
import java.math.BigInteger;

public class Faberge {
  public static BigInteger height(BigInteger n, BigInteger m) {
    if (n >= m) return BigInteger.TWO ** m - 1
    BigInteger c = 1, s = 0
    for (BigInteger i = 0; i < n; i++) {
      c = c * (m - i) / (i + 1)
      s += c
    }
    return s
  }
}
