public class Kata {
  public static String findNeedle(Object[] haystack) {
    return String.format("found the needle at position %d", java.util.Arrays.asList(haystack).indexOf("needle"));
  }
}
________________________
import java.util.*;

public class Kata {
  public static String findNeedle(Object[] haystack) {
    return "found the needle at position " + Arrays.asList(haystack).indexOf("needle");
  }
}
________________________
public class Kata {
    public static String findNeedle(Object[] haystack) {
    
        for (int i = 0; i < haystack.length; i++) {
            if (haystack[i] == "needle") {
                return "found the needle at position " + i;
            }
        }
        return "needle be lost, yo";
    }
}
________________________
public class Kata {
  public static String findNeedle(Object[] haystack) {
    int i = 0;
    while(!String.valueOf(haystack[i]).equals("needle")){
      i++;
    } 
    return "found the needle at position " + i;
  }
}
________________________
import static java.util.Arrays.asList;

class Kata {
  static String findNeedle(Object[] haystack) {
    return "found the needle at position " + asList(haystack).indexOf("needle");
  }
}
