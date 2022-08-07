55caf1fd8063ddfa8e000018


import static java.util.stream.IntStream.iterate;
import static java.util.stream.Collectors.joining;

public class Progression {
  
  public static String arithmeticSequenceElements(int a, int d, long n) {
    return iterate(a, t -> t + d).limit(n).mapToObj(Integer::toString).collect(joining(", "));
  }
}
___________________________
import java.util.stream.Collectors;
import java.util.stream.LongStream;

class Progression {

  public static String arithmeticSequenceElements(int first, int step, long total) {
    return LongStream.range(0, total)
      .map(i -> first + step * i)
      .mapToObj(Long::toString)
      .collect(Collectors.joining(", "));
  }

}
___________________________
class Progression {
  
  public static String arithmeticSequenceElements(int first, int step, long total) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < total; i++) {
            sb.append(first).append(", ");
            first += step;
        }
        return sb.substring(0, sb.length() - 2);
  }
    
}
