55b2549a781b5336c0000103


import java.lang.Math;

public class Compare {
  public static int comparePowers(int[] number1, int[] number2) {
    var a = Math.log10(number1[0]) * number1[1];
    var b = Math.log10(number2[0]) * number2[1];

    return Double.compare(b, a);
  }
}
________________________________
public class Compare {
  public static int comparePowers(int[] number1, int[] number2) {
    double log1 = number1[1]* Math.log(number1[0]);
      double log2 = number2[1]* Math.log(number2[0]);
      if (log1>log2){
        System.out.println(-1);
        return -1;
      }
      if (log1==log2){
        System.out.println(0);
        return 0;
      }
      if (log1<log2){
        System.out.println(1);
        return 1;
      }
  
    return 0;
  }
}
________________________________
import java.lang.Math;

public class Compare {
  public static int comparePowers(int[] number1, int[] number2) {
    double n1 = number1[1]*Math.log(number1[0]);
    double n2 = number2[1]*Math.log(number2[0]);
    
    if (n1 > n2) return -1;
    else if (n1 == n2) return 0;
    return 1;
  }
}

