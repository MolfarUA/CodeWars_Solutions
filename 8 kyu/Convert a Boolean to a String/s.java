public class BooleanToString {
  public static String convert(boolean b){
    return b ? "true" : "false";
  }
}
_________________________________
public class BooleanToString {
  public static String convert(boolean b){
    return Boolean.toString(b);
  }
}
_________________________________
public class BooleanToString {
  
  public static String convert(boolean b){

    return String.valueOf(b);

  }

}
_________________________________
public class BooleanToString {
  public static String convert(boolean b){
    return b+"";
  }
}
_________________________________
public class BooleanToString {
  public static String convert(boolean b){
      
    boolean value = b;
    if(value != true){
      return "false";
    } 
    else {
      return "true";
    }
  }

}
