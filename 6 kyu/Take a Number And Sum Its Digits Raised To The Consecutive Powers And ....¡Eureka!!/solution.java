import java.util.List;
import java.util.stream.*;


class SumDigPower {
    
    public static List<Long> sumDigPow(long a, long b) {
        return LongStream.rangeClosed(a, b)
          .filter(i -> isValid(i))
          .boxed()
          .collect(Collectors.toList());
    }
    
    private static boolean isValid(long x){
      String value = Long.toString(x);
      return IntStream.range(0, value.length())
         .mapToDouble(i -> Math.pow(Character.getNumericValue(value.charAt(i)), i + 1))
         .sum() == x;
    }
}
_____________________________________________
import java.util.List;
import java.util.ArrayList;

class SumDigPower {
    
    public static List<Long> sumDigPow(long a, long b) {
        List<Long> result = new ArrayList<>();
        for (long i = a; i <= b; i++)
            if(isEureka(i))
                result.add(i);
        return result;
    }

    private static boolean isEureka(long n) {
        long tmp = n;
        long sum = 0;
        int power = length(n);
        while (tmp > 0) {
            sum += (long) Math.pow(tmp % 10, power);
            tmp /= 10;
            power--;
        } 
        return sum == n;    
    }

    private static int length(long n) {
        int length = 0;
        while (n > 0) {
            n /= 10;
            length++;
        }
        return length;
    }
}
_____________________________________________
import java.util.*;

class SumDigPower {
    
  public static List<Long> sumDigPow(long a, long b) {
    return (calculateList(a, b));
  }
    
  private static List<Long> calculateList(long a, long b) {
    List<Long> resultList = new ArrayList<Long>();
    for (long i = a; i < b; i++) {
      if (isEureka(i)) {
        resultList.add(i);
      }
    }
    return (resultList);
  }

  private static boolean isEureka(long number) {
    String longString = String.valueOf(number);
    long sum = 0;
    for (int i = 0; i < longString.length(); i++) {
      long digit = Long.parseLong(String.valueOf(longString.charAt(i)));
      sum += Math.pow(digit, i+1);
    }
    return (sum == number);
  }
    
    
}
