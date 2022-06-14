class Persist {
  public static int persistence(long n) {
    long m = 1, r = n;

    if (r / 10 == 0)
      return 0;

    for (r = n; r != 0; r /= 10)
      m *= r % 10;

    return persistence(m) + 1;
    
  }
}
________________________________________
class Persist {
  public static int persistence(long n) {
    int times = 0;
    while (n >= 10) {
      n = Long.toString(n).chars().reduce(1, (r, i) -> r * (i - '0'));
      times++;
    }
    return times;
  }
}
________________________________________
class Persist {
   /**
     * given a positive integer produce its multiplicative persistence
     * @param n a positive integer
     * @return the multiplicative persistence of n
     */
    public static int persistence(long n) {
        if (n < 10) {
            return 0;
        }
        return 1 + persistence(multiplyDigits(n));
    }
    /**
     * given an integer produce the product of the given integers digits.
     * example: multiplyDigits(785) = 7 * 8 * 5 = 280
     * @param n
     * @return the product of the digits that comprise n
     */
    private static long multiplyDigits(long n) {
        if (n < 10) {
            return n;
        }
        return n % 10 * multiplyDigits(n / 10);
    }
}
________________________________________
import java.util.Arrays;

class Persist {

    public static int persistence(long n) {
        if (n < 10) return 0;

        final long newN = Arrays.stream(String.valueOf(n).split(""))
                .mapToLong(Long::valueOf)
                .reduce(1, (acc, next) -> acc * next);

        return persistence(newN) + 1;
    }
}
________________________________________
class Persist {
  public static int persistence(long n) {
    if (n<10) return 0;
    long n2 = 1;
    while(n!=0) {
      n2*=n%10;
      n/=10;
    }
    return 1+persistence(n2);
  }
}
