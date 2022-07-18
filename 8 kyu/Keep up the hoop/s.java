55cb632c1a5d7b3ad0000145


public class HelpAlex{
  public static String hoopCount(int n){
   return n<10?"Keep at it until you get it":"Great, now move on to tricks";
  }
}
_____________________________
public class HelpAlex{
  public static String hoopCount(int n){
     return n >= 10 ? "Great, now move on to tricks" : "Keep at it until you get it";
  }
}
_____________________________
import java.util.*;

public class HelpAlex{
  public static String hoopCount(int n){
    Map<Boolean, String> phrase = new HashMap<>();
    phrase.put(true, "Great, now move on to tricks");
    phrase.put(false, "Keep at it until you get it");
    
   return phrase.get(n >= 10);
  }
}
_____________________________
public class HelpAlex{
  public static String hoopCount(int n){
   String phrase = "";
    if(n >= 10){
      phrase = "Great, now move on to tricks";
    }else{
      phrase = "Keep at it until you get it";
    }
    return phrase;
  }
}
