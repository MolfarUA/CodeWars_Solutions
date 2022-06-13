public class Kata {
  public static String createPhoneNumber(int[] numbers) {
    return String.format("(%d%d%d) %d%d%d-%d%d%d%d",numbers[0],numbers[1],numbers[2],numbers[3],numbers[4],numbers[5],numbers[6],numbers[7],numbers[8],numbers[9]);
  }
}
_______________________________
public class Kata {
  public static String createPhoneNumber(int[] numbers) {
    return String.format("(%d%d%d) %d%d%d-%d%d%d%d", java.util.stream.IntStream.of(numbers).boxed().toArray());
  }
}
_______________________________
public class Kata {
  public static String createPhoneNumber(int[] numbers) {
    String phoneNumber = new String("(xxx) xxx-xxxx");
    
    for (int i : numbers) {
      phoneNumber = phoneNumber.replaceFirst("x", Integer.toString(i));
    }
    
    return phoneNumber;
  }
}
_______________________________
import java.util.Arrays;

public class Kata {

    private static String PHONE_FORMAT = "(%d%d%d) %d%d%d-%d%d%d%d";

    public static String createPhoneNumber(int[] numbers) {
        Integer[] numbersInt = Arrays.stream(numbers).boxed().toArray(Integer[]::new);
        return String.format(PHONE_FORMAT, numbersInt);
    }
}
_______________________________
public class Kata {
  public static String createPhoneNumber(int[] numbers) {
    // Your code here!
    StringBuilder sb = new StringBuilder();
    sb.append("(");
    //int start = 0
    for(int i = 0;i<3;i++){
      sb.append(String.valueOf(numbers[i])); 
    }
    sb.append(") ");
    for(int i = 3;i<6;i++){
      sb.append(String.valueOf(numbers[i]));
    }
    sb.append("-");
    for(int i= 6;i<10;i++){
      sb.append(String.valueOf(numbers[i]));
    }
    return sb.toString();
  }
}
