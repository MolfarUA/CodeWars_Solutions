5b853229cfde412a470000d0


public class TwiceAsOld{

  public static int TwiceAsOld(int dadYears, int sonYears){
    return Math.abs(dadYears - sonYears * 2);
  }

}
______________________________
import static java.lang.Math.abs;

public class TwiceAsOld {

  public static int TwiceAsOld(int d, int s) {
    return abs(d-s-s);
  }

}
______________________________
import static java.lang.Math.abs;

public class TwiceAsOld {

  public static int TwiceAsOld(int dadYears, int sonYears) {
    return abs(2 * sonYears - dadYears);
  }
}
______________________________
public class TwiceAsOld{

  public static int TwiceAsOld(int dadYears, int sonYears){
    return Math.abs(dadYears-sonYears-sonYears);
  
  }

}
______________________________
import java.util.stream.IntStream;

public class TwiceAsOld{

  public static int TwiceAsOld(int dadYears , int sonYears){
        return IntStream.of(sonYears , dadYears)
                .filter(i->dadYears / 2 > sonYears)
                .map(i -> dadYears - sonYears * 2)
                .findAny()
                .orElse(sonYears - dadYears + sonYears);
    }

}
