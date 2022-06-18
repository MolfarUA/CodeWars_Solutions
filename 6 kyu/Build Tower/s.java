576757b1df89ecf5bd00073b


public class Kata {
  
  public static String[] TowerBuilder(int n) {
    String t[] = new String[n], e;
    
    for (int i = 0; i < n; i++)
      t[i] = (e = " ".repeat(n-i-1)) + "*".repeat(i+i+1) + e;
    
    return t;
  }
  
}
_____________________________
import static java.util.stream.IntStream.range;

interface Kata {
  static String[] towerBuilder(int f) {
    return range(0, f).mapToObj(i -> String.format("%1$s%2$s%1$s", " ".repeat(f - i - 1), "*".repeat(2 * i + 1))).toArray(String[]::new);
  }
}
_____________________________
public class Kata
{
  public static String[] TowerBuilder(int nFloors)
  {
        String[] arr = new String[nFloors];
        for (int i = 0; i < arr.length; i++) {
            String repeat = " ".repeat((arr.length * 2 - ((i + 1) * 2 - 1)) / 2);
            arr[i] = repeat + "*".repeat((i + 1) * 2 - 1) + repeat;
        }
        return arr;
  }
}
_____________________________
public class Kata
{
  public static String[] TowerBuilder(int nFloors){
              if (nFloors == 0) {
            return new String[0];
        }
    
        String[] array = new String[nFloors];
        StringBuilder stringBuilder = new StringBuilder();
        for (int i = 0; i < (nFloors * 2) - 1; i++) {
            stringBuilder.append("*");
        }
        int first = 0;
        int last = stringBuilder.length() - 1;

        array[nFloors - 1] = stringBuilder.toString();
        for (int i = nFloors - 2; i >= 0; i--) {
            stringBuilder.setCharAt(first, ' ');
            stringBuilder.setCharAt(last, ' ');
            array[i] = stringBuilder.toString();

            first++;
            last--;
        }
        
        return array;
  }
}
_____________________________
public class Kata
{
  public static String[] towerBuilder(int nFloors)
  {
    String[] floors = new String[nFloors];
    int pointCount = 1;
    int spaceCount = nFloors - 1;
    
    for (int i = 0; i < nFloors; i++) {
      String floor = "";
      for (int q = 0; q < spaceCount; q++) floor += " ";
      for (int w = 0; w < pointCount*2 - 1; w++) floor += "*";
      for (int e = 0; e < spaceCount; e++) floor += " ";
      floors[i] = floor;
      spaceCount--;
      pointCount++;
    }
    return floors;
  }
}
