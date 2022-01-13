public class PiApprox 
{
    public static String iterPi2String(Double epsilon) 
    {
        Double pi4 = 1.0
        Double sign = -1.0
        def iterations = 1
        Double denom = 3.0
      
        while (Math.abs(4.0 * pi4 - Math.PI) >= epsilon) 
        {
            pi4 += sign * (1.0 / denom)
            sign *= -1.0
            denom += 2.0
            iterations++
        }
      
        return String.format("[%d, %.10f]", iterations, 4.0 * pi4)
    }
}
________________________________________
public class PiApprox {

    public static String iterPi2String(Double epsilon) {
      int n = 0;
      double piAprox=0;
      while( Math.abs(Math.PI-4*piAprox) > epsilon ){
        piAprox+=(Math.pow(-1,n)) / (2*n+1);
        n++;      
      }
      return String.format("[%d, %1.10f]",n,4*piAprox);
  }
}
________________________________________
import static java.lang.Math.*
import static java.math.RoundingMode.*
import java.text.DecimalFormat


public class PiApprox {

    public static String iterPi2String(Double epsilon) {
        int it, sign = -1
        double acc = 1.0, den = 3.0, pi4 = PI / 4.0, epsilon4 = epsilon / 4.0
        for (it = 1; abs(acc - pi4) > epsilon4; it++) {
            acc += sign / den
            den += 2.0
            sign *= -1
        }

        [it, String.format("%.10f", 4.0 * acc)]
    }
}
________________________________________
import static java.lang.Math.*
import java.text.DecimalFormat
import static java.math.RoundingMode.*

public class PiApprox {

    public static String iterPi2String(Double epsilon) {
      int it, sign = -1
      double acc = 1.0, den = 3.0, pi4 = PI/4.0, epsilon4 = epsilon/4.0
      for (it=1; abs(acc - pi4) > epsilon4; it++){
          acc += sign/den
          den += 2.0
          sign *= -1
      }
      
      return [it, String.format("%.10f", 4.0*acc)]
    }
}
________________________________________
public class PiApprox {

    public static String iterPi2String(Double epsilon) {
        double piVal = 0.0;
        int i = 0;
        while (Math.abs(piVal - Math.PI) > epsilon)
            piVal += 4 * Math.pow(-1, i) / (2 * i++ + 1);
        return "[" + i + ", " + (Math.round(1e10 * piVal) / 1e10) + "]";
    }
}
