5b609ebc8f47bd595e000627


import java.util.HashMap;
import java.util.Map;

public class Solution {

    private final static Double G = 6.67e-11;

    public static double solution(double[] arrVal, String[] arrUnit) {
        Map<String, Double> convertions = new HashMap<>();
        convertions.put("kg", 1.0);
        convertions.put("g", 1e-3);
        convertions.put("mg", 1e-6);
        convertions.put("μg", 1e-9);
        convertions.put("lb", 0.453592);
        convertions.put("m", 1.0);
        convertions.put("cm", 1e-2);
        convertions.put("mm", 1e-3);
        convertions.put("μm", 1e-6);
        convertions.put("ft", 0.3048);

        double m1 = arrVal[0] * convertions.get(arrUnit[0]);
        double m2 = arrVal[1] * convertions.get(arrUnit[1]);
        double r = arrVal[2] * convertions.get(arrUnit[2]);

        return G * m1 * m2 / r / r;
    }

}
____________________________________
import java.util.Map;

class Solution {
  static double solution(double[] arrVal, String[] arrUnit) {
    var units = Map.of("g", 1e-3, "mg", 1e-6, "μg", 1e-9, "lb", .45359, "cm", .01, "mm", .001, "μm", 1e-6, "ft", .3048);
    double m1 = arrVal[0] * units.getOrDefault(arrUnit[0], 1.);
    double m2 = arrVal[1] * units.getOrDefault(arrUnit[1], 1.);
    double r = arrVal[2] * units.getOrDefault(arrUnit[2], 1.);
    return 6.67e-11 * m1 * m2 / r / r;
  }
}
____________________________________
public class Solution {

  public static double solution(double[] arrVal, String[] arrUnit) {

    double newtons = 6.67e-11 * arrVal[0] * arrVal[1] / (arrVal[2] * arrVal[2]);

    for (String el : arrUnit) {  // convert like a boss
      newtons /= (el=="g") ? 1e3 : (el=="mg") ? 1e6 : (el=="μg") ? 1e9 : (el=="ft") ? 0.3048 * 0.3048 : 1;
      newtons *= (el=="lb") ? 0.453592 : (el=="cm") ? 1e4 : (el=="mm") ? 1e6 : (el=="μm") ? 1e12 : 1;
    }

    return newtons;

  }
}
