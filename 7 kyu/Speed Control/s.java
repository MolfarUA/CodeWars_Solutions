56484848ba95170a8000004d


import java.util.*;
import java.util.stream.*;

public class GpsSpeed {
    
    public static int gps(int s, double[] x) {
        double maxSpeed = IntStream
          .range(0, x.length - 1)
          .mapToDouble(i -> (x[i+1] - x[i]) * 3600.0 / (double) s )
          .max().orElse(0.0);
        return (int) Math.floor(maxSpeed);
    }
}
_____________________________
public class GpsSpeed {
    
    public static int gps(int s, double[] x)
    {
      int max = 0;
      for (int i = 0; i < x.length - 1; i++) max = (int) Math.max(max, (x[i + 1] - x[i]) * 3600 / s);
      return max;
    }
}
_____________________________
public class GpsSpeed {
    
    public static int gps(int s, double[] x) {
       double maxDiff = 0.0;
        for(int i = 0; i < x.length -1; i++){
          maxDiff = Math.max(x[i+1] - x[i], maxDiff);
        }
          return (int)Math.floor(maxDiff*3600.0/s);
    }
}
