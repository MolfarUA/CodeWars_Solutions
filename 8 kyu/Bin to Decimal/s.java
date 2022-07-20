57a5c31ce298a7e6b7000334


public class Converter{
  public static int binToDecimal(String inp){
    return Integer.parseInt(inp, 2);
  }
}
_________________________
abstract class Converter{
  public static int binToDecimal(String inp){
    return Integer.parseInt(inp, 2);
  }
}
_________________________
interface Converter {
  static int binToDecimal(String binary) {
    return Integer.parseInt(binary, 2);
  }
}
_________________________
public class Converter{
  public static int binToDecimal(String binary){
    String[] arr = binary.split("");
    
    int result = 0;
    int n = binary.length() - 1;
    
    for (String str: arr){
      result += Integer.parseInt(str) * Math.pow(2,n--);
    }
    
    return result;
  }
}
