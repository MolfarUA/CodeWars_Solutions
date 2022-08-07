57cfdf34902f6ba3d300001e


public class SortAndStar {

    public static String twoSort(String[] s) {
        java.util.Arrays.sort(s);

        return String.join("***",s[0].split(""));
    }
}
___________________________
import java.util.Arrays;
public class SortAndStar {

  public static String twoSort(String[] s) {
    return String.join("***", Arrays.stream(s).sorted().findFirst().orElse("").split(""));
  }
}
___________________________
import java.util.*;
public class SortAndStar {

  public static String twoSort(String[] s) {
    Arrays.sort(s);
    return s[0].replaceAll("([a-zA-Z])", "***$1").substring(3);
  }
}
