54cb771c9b30e8b5250011d4


import java.math.BigInteger;

public class Faberge {

  public static BigInteger height(BigInteger n, BigInteger m) {
    int eggs  = n.intValue();
    int falls = m.intValue();
    if (eggs>falls) return height(m, m);
    // Number of binomial coefficients we will calculate (no need to compute more than half of them
    // since C(falls,k)=C(falls,n-k), and no need to compute more than the number of eggs)
    int coeffs = Integer.min(falls/2+(falls%2),eggs);
    // Array that's storing the binomial coefficients C(falls,k), i.e. one line of Pascal's triangle (truncated)
    BigInteger[] a = new BigInteger[coeffs+1];
    // First column of Pascal's triangle is always 1
    a[0] = BigInteger.ONE;
    for(int k = 1; k<=falls && k<=coeffs; k++)
      // Formula for getting C(falls,k) from C(falls,k-1)
      a[k] = a[k-1].multiply(BigInteger.valueOf(falls-k+1)).divide(BigInteger.valueOf(k));
    // Now we sum them up
    BigInteger res = BigInteger.ZERO;
    for(int k = 1; k <= eggs; k++) res = res.add((k>coeffs)?a[falls-k]:a[k]);
    return res;
    }
    
}
_________________________
import java.math.BigInteger;

public class Faberge {
    public static BigInteger height(BigInteger eggs, BigInteger tries) {
        BigInteger result = BigInteger.ZERO;
        BigInteger tempResult = BigInteger.ONE;
        for (int i=1; i<=eggs.intValue(); result = result.add(tempResult), i++) {
            tempResult = tempResult.multiply(tries.add(BigInteger.valueOf(1-i))).divide(BigInteger.valueOf(i));
        }
        return result;
    }
}
_________________________
import java.math.BigInteger;

public class Faberge {
  public static BigInteger height(final BigInteger n, final BigInteger m) {
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
import java.util.HashMap;
import java.util.Map;

public class Faberge {
  public static BigInteger height(BigInteger n, BigInteger m) {
    Map<BigInteger, BigInteger> map = new HashMap<BigInteger, BigInteger>();
    
    BigInteger result = BigInteger.ZERO;
    for (BigInteger i=BigInteger.ONE; i.compareTo(n) != 1; i = i.add(BigInteger.valueOf(1))) {
      BigInteger beforeValue = map.containsKey(i.subtract(BigInteger.ONE)) ? map.get(i.subtract(BigInteger.ONE)) : BigInteger.valueOf(1);
      BigInteger sorat = beforeValue.multiply(m.subtract(i).add(BigInteger.ONE));
      BigInteger makhraj = i;
      map.put(i, sorat.divide(makhraj));
      result = result.add(map.get(i));
    }
    
    return result;
  }
}
