56f173a35b91399a05000cb7


import java.util.stream.Stream;
public class Kata {
  public static int findLongest(final String str) {
    return Stream.of(str.split(" ")).mapToInt(s -> s.length()).max().getAsInt();
  }
}
__________________________
import java.util.stream.Stream;

class Kata {
  static int findLongest(String str) {
    return Stream.of(str.split(" ")).mapToInt(String::length).max().orElse(0);
  }
}
__________________________
import java.util.*;

public class Kata {

  public static int findLongest(String str) {
    String[] spl = str.split(" ");
    int longest = 0;
    for (int i = 0; i < spl.length; i++) {
      if (spl[i].length() > longest) {
        longest = spl[i].length();
      }
      }
      return longest;
  }
  
}
