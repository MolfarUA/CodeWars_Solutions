544675c6f971f7399a000e79


public class StringToNumber {
  public static int stringToNumber(String str) {
    return Integer.parseInt(str);
  }
}
_______________________
public class StringToNumber {
  public static int stringToNumber(String str) {
    return Integer.valueOf(str);
  }
}
_______________________
public class StringToNumber {
  public static int stringToNumber(String str) {
    try {
    return Integer.parseInt(str);
    } catch (NumberFormatException NFE) {
      throw NFE;
    }
  }
}
_______________________
public class StringToNumber {
  public static int stringToNumber(String str) {
    
    return Integer.parseInt(str);
  }
}
_______________________
public class StringToNumber {
  public static int stringToNumber(String str) {
    //TODO: Convert str into a number
    return Integer.valueOf(str);
    // Integer.parseInt(str)
  }
  public static void main(String argw[]){
    stringToNumber("0");
  }
}
_______________________
public class StringToNumber {
  public static int stringToNumber(String str) {
    char[] charArray = str.toCharArray();
    int num = 0;
    int n = 1;

    for(int i = charArray.length - 1; i > 0; i--){
        num += (charArray[i] - 48) * n;
        n *=  10;
    }

    if(charArray[0] == '-'){
        num *= -1;
    }else{
        num += (charArray[0] - 48) * n;
    }
    
    return num;
  }
}
