public class Kata {
  public static int[] digitize(long n) {
        return new StringBuilder().append(n)
                                  .reverse()
                                  .chars()
                                  .map(Character::getNumericValue)
                                  .toArray();
  }
}
________________________
import java.lang.Math;
public class Kata {
  public static int[] digitize(long n) {
    String s = String.valueOf(n);
    int length = s.length();
    int[] array = new int[length];
    for ( int i = 0; i < length; i++){
      array[i] = (int) (s.charAt(length - i - 1)) - 48;
    }
    return array;
  }
}
________________________
class Kata {
    public static int[] digitize(long n) {
        int length = n == 0 ? 1 : (int) Math.log10(n) + 1;
        int[] digits = new int[length];
        for (int i = 0; i < length; i++, n /= 10) {
            digits[i] = (int) (n % 10);
        }
        return digits;
    }
}
________________________
public class Kata {
    public static int[] digitize(long n) {
        String[] nums = new StringBuilder(String.valueOf(n)).reverse().toString().split("");
        int[] result = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            result[i] = Integer.parseInt(nums[i]);
        }
        return result;
    }
}
________________________
class Kata {
  static int[] digitize(long n) {
    return new StringBuilder(String.valueOf(n))
        .reverse()
        .chars()
        .map(Character::getNumericValue)
        .toArray();
  }
}
