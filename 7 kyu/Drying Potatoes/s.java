class Potatoes {
    
    public static int potatoes(int p0, int w0, int p1) {
        return w0 * (100 - p0) / (100 - p1);
    }
}
_______________________________________________
class Potatoes {
    
    public static int potatoes(int p0, int w0, int p1) {
        return (100 - p0) * w0 / (100 - p1);
    }
}
_______________________________________________
interface Potatoes {
  static int potatoes(int p0, int w0, int p1) {
    return w0 * (100 - p0) / (100 - p1);
  }
}
_______________________________________________
class Potatoes {
    
    public static int potatoes(int p0, int w0, int p1) {
    return (int) (100 * ((float) (w0 * (100 - p0))/100) / (100 - p1));
    }
}
_______________________________________________
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
class Potatoes {
    
  public static int potatoes(int p0, int w0, int p1) {
    BigDecimal bp0 = new BigDecimal(p0);
    BigDecimal bw0 = new BigDecimal(w0);
    BigDecimal bp1 = new BigDecimal(p1);
    bp0 = bp0.multiply(new BigDecimal(0.01, MathContext.DECIMAL32));
    bp1 = bp1.multiply(new BigDecimal(0.01, MathContext.DECIMAL32));
    BigDecimal multiply = bw0.multiply(bp0.subtract(bp1), MathContext.DECIMAL32);
    BigDecimal add = bp1.multiply(new BigDecimal(-1), MathContext.DECIMAL32).add(new BigDecimal(1));
    BigDecimal loseWater = multiply.divide(add, RoundingMode.HALF_UP);
    BigDecimal ans = bw0.subtract(loseWater);
    return ans.intValue();
  }
}
_______________________________________________
class Potatoes {
    
    public static int potatoes(int p0, int w0, int p1) {
        double w2 = w0/100.0;
            int w1 = (int)(100 * (w2 * (100 -p0))/(100 - p1));
            return w1;
    }
}
