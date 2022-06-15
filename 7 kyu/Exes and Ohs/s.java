public class XO {
  
  public static boolean getXO (String str) {
    str = str.toLowerCase();
    return str.replace("o","").length() == str.replace("x","").length();
    
  }
}
__________________________________
public class XO {
  
  public static boolean getXO (String str) {
    str = str.toLowerCase();
    if(!str.contains("x") && !str.contains("o"))
      {
      return true;
    }
    else
      {
      int count_x =0;
      int count_o = 0;
      for(int i=0; i<str.length();i++)
        {
          if(str.charAt(i) == 'x')
            {
            count_x++;
          }
        else if(str.charAt(i) == 'o')
          {
          count_o++;
        }
      }
      return count_x==count_o;
    }
    
  }
}
__________________________________
import java.util.stream.Stream;
public class XO {
  
  public static boolean getXO (String str) {
    long exes = Stream.of(str.split(""))
                     .filter(i -> i.matches("(?i)x"))
                     .count();
    long oes = Stream.of(str.split(""))
                     .filter(i -> i.matches("(?i)o"))
                     .count();
   return exes==oes ? true:false; 
  }
}
__________________________________
public class XO {
  
  public static boolean getXO (String str) {
    
    String lStr = str.toLowerCase();
    long x = lStr.chars().filter(c -> c == 'x').count();
    long o = lStr.chars().filter(c -> c == 'o').count();
    
    return x == o;
    
  }
}
