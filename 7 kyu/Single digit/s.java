class Kata {
   
  static int singleDigit(int n) {
    return n < 10 ? n : singleDigit(Integer.bitCount(n));
  }
  
}
__________________________
public class Kata {   
  public static int singleDigit(int n) {
    if (n < 10) return n;
    return singleDigit(reduce(n));
  }
  
  public static int reduce(int n) {
    return Integer.toBinaryString(n).chars()
                  .map(Character::getNumericValue)
                  .sum();
  }
}
__________________________
import static java.util.stream.IntStream.iterate;

interface Kata {
  static int singleDigit(int n) {
    return iterate(n, Integer::bitCount).filter(i -> i < 10).findFirst().orElse(0);
  }
}
__________________________
interface Kata {
  static int singleDigit(int n) {
    return n > 9 ? singleDigit(Integer.bitCount(n)) : n;
  }
}
__________________________
import java.util.stream.IntStream;

class Kata {
  static int singleDigit(int n) {
    return IntStream.iterate(n, Integer::bitCount)
      .filter(i -> i < 10)
      .findFirst()
      .getAsInt();
  }
}
__________________________
class Kata {
   
    static int singleDigit(int n) {
        while (n >= 10) {
            n = Integer.bitCount(n);
        }
        return n;
    }
}
__________________________
import java.util.Arrays;
class Kata {   
  static int singleDigit(int n) {
        while (n > 9) {
            n = Arrays.stream(Integer.toBinaryString(n).split("")).map(s -> Integer.parseInt(s)).reduce((a, b) -> a + b).get();
        }
        return n;
  }
}
__________________________
interface Kata {
  static int singleDigit(int n) {
    return n < 10 ? n : singleDigit(Integer.toBinaryString(n).chars().map(c -> c - 48).sum());
  }
}
__________________________
import java.util.Arrays;
class Kata {
   
  static int singleDigit(int n) {
    while (n > 9){
      n = Arrays.stream(Integer.toBinaryString(n).split("")).mapToInt(Integer::parseInt).sum();
    }
    return n;
  }
}
