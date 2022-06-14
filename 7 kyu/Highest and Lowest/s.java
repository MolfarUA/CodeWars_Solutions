import static java.util.Arrays.stream;

class Kata {
  static String highAndLow(String numbers) {
    var stats = stream(numbers.split(" ")).mapToInt(Integer::parseInt).summaryStatistics();
    return stats.getMax() + " " + stats.getMin();
  }
}
______________________________
public class Kata {
  public static String highAndLow(String numbers) {
        String[] array = numbers.split(" ");
        int min = Integer.MAX_VALUE;
        int max = Integer.MIN_VALUE;
        for (int i=0; i< array.length; i++){
            int value = Integer.parseInt(array[i]);
            if (value < min) min = value;
            if (value > max) max = value;
        }
        return String.format("%d %d", max, min);
  }
}
______________________________
import java.util.Collections;
import java.util.ArrayList;
public class Kata {
  public static String highAndLow(String numbers) {
    // Code here or
    String[] num = numbers.split(" ");
    ArrayList<Integer> list = new ArrayList<>();
    for(String s : num){
      list.add(Integer.parseInt(s));
    }
    Collections.sort(list);
    
    return list.get(list.size() - 1) + " " + list.get(0);
  }
}
______________________________
import java.util.*;

public class Kata {
  private static final String SPACE = " ";
  public static String highAndLow(String numbers) {
    TreeSet<Integer> numberSet = new TreeSet<Integer>();   
    String[] numberArr = numbers.split(SPACE);
    for(String numberVal: numberArr){
     numberSet.add(Integer.parseInt(numberVal));
    }                   
    return String.valueOf(numberSet.last()) + SPACE +String.valueOf(numberSet.first());                
      
  }
}
______________________________
public class Kata {
  public static String highAndLow(String numbers) {
    String[] s = numbers.split(" ");
    int high = Integer.parseInt(s[0]);
    int low = Integer.parseInt(s[0]);

    for(int i = 1; i<s.length;i++){
      if(Integer.parseInt(s[i])>=high){
        high = Integer.parseInt(s[i]);
      }
    }
    for(int j = 1;j<s.length;j++){
      if(Integer.parseInt(s[j]) <= low){
        low = Integer.parseInt(s[j]);
      }
    }
    String ergebnis = "" + high + " " + low;
    return ergebnis;
  }
}
