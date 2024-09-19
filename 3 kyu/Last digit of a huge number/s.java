public class Solution {
  public static int lastDigit(int[] array) {
    int r = 1, f = 0;
    for (int i = array.length - 1; i >= 0; i--) {
      int r1 = (int)Math.pow(array[i] % (i > 0 ? 4 : 10), r + 4 * f) % (i > 0 ? 4 : 10);
      f = array[i] <= 1 ? 0 : array[i] <= 3 && r <= 1 ? f : 1;
      r = r1;
    }
    return r;
  }
}
_________________________
import java.math.BigInteger;

public class Solution {
public static int lastDigit(int[] array) {
        if (array.length < 1) return 1;
        String s = String.valueOf(array[0]);
        if (array.length == 1) {
            return Integer.parseInt(s.substring(s.length() - 1));
        }
        int offset = array[0];
        if (offset == 1) return 1;
        if (offset != 0  && offset % 10 == 0) return  0;
        BigInteger pow = BigInteger.ONE;
        for (int i = array.length - 1; i >= 1; i--) {
            pow = BigInteger.valueOf(array[i]).pow(pow.intValue());
            if (pow.compareTo(BigInteger.valueOf(4)) > 0) pow = pow.mod(BigInteger.valueOf(4)).add(BigInteger.valueOf(4));
        }

        return BigInteger.valueOf(offset).modPow(pow, BigInteger.TEN).intValue();
    }
}
_________________________
public class Solution {
  public static int lastDigit(int[] array) {

        if (array.length == 0) return 1;

        boolean rightIsZero = false;

        boolean rightBiggerThan2 = false;

        int rightMod4 = 1;

        for (int i = array.length - 1; i > 0; --i) {

            if (rightIsZero) {

                rightMod4 = 1;

                rightIsZero = false;

                rightBiggerThan2 = false;

            } else {

                rightMod4 = (rightBiggerThan2 && (array[i] % 4 == 2)) ? 0 : trueMod(array[i], rightMod4, 4);

                rightIsZero = array[i] == 0;

                rightBiggerThan2 = !rightIsZero && !(array[i] == 1);

            }

        }
        return rightIsZero ? 1 : trueMod(array[0], rightMod4, 10);
  }
  public static int trueMod(int a, int n, int m) {

        return (int) Math.round((a % m) * Math.pow((a % m), (n + 3) % 4)) % m;

    }
}
