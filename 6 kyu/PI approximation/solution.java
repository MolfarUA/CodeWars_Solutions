public class PiApprox {
  
  public static String iterPi2String(Double epsilon) {
     int i = 0, j = 1;
     double pi = 0.0;
     while( Math.abs(Math.PI - pi*4) > epsilon) {
       if(i % 2 == 0) pi += 1.0/j;
       else pi -= 1.0/j;
       j += 2;
       i++;
     }
     return String.format("[%d, %.10f]", i, pi*4);
  }
}
________________________________________
public class PiApprox {
  
  public static String iterPi2String(Double epsilon) {
    double pi4 = 0;
    int i = 0;
    while (Math.abs(Math.PI - pi4 * 4) >= epsilon && i < 1_000_000_000) {
      int denom = i * 2 + 1;
      if (i % 2 == 1) {
        pi4 -= 1.0 / denom;
      } else {
        pi4 += 1.0 / denom;
      }
      i++;
    }
    return String.format("[%d, %.10f]", i, pi4 * 4);
  }
}
________________________________________
public class PiApprox {
    public static String iterPi2String(Double epsilon) {
        int i = 0;
        double s = 0;
        for (int j = 1; Math.abs(Math.PI - s*4) >= epsilon; j += 2) {
            if (i % 2 == 0) s += 1.0/j;
            else s -= 1.0/j;
            i++;
        }
        return "[" + i + ", " + ((double)Math.round(s*4 * 10000000000d) / 10000000000d) + "]";
    }
}
________________________________________
import java.util.Locale;

public class PiApprox {
  
  public static String iterPi2String(Double epsilon) {
     String res = "";
        double n = 1.0; double value = 0.0; int counter = 0;
        while (Math.abs((Math.PI - 4 * value)) > epsilon) {
            value += 1.0 / n;
            n = -n;
            if (n > 0) n += 2.0;
            if (n < 0) n -= 2;
            counter += 1;
        }
        res += res + "[" + String.valueOf(counter) + ", " + String.format(Locale.US, "%.11g", 4 * value) + "]";
        return res;
  }
}
________________________________________
public class PiApprox {
  
  public static String iterPi2String(Double epsilon) {
    double result = 0;
    int n = 0;
    for (int i = 0; Math.abs(Math.PI - result * 4) > epsilon; i++) {
      result += Math.pow(-1, i) / (2 * i + 1);
      n++;
    }
    return String.format("[%d, %.10f]", n, result * 4);
  }
}
