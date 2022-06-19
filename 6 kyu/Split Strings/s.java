515de9ae9dcfc28eb6000001


public class StringSplit {
    public static String[] solution(String s) {
        s = (s.length() % 2 == 0)?s:s+"_";
        return s.split("(?<=\\G.{2})");
    }
}
________________________________
import java.util.*;

public class StringSplit {
    public static String[] solution(String s) {
        List<String> result = new ArrayList<String>();
        if(s.length() %2 == 1){
          s = s+"_";
        }
        for(int i=0;i<s.length() - 1;i+=2){
           result.add(s.substring(i, i+2));
        }
        return result.toArray( new String[0] );
    }
}
________________________________
class StringSplit {
  static String[] solution(String s) {
    return (s + (s.length() % 2 > 0 ? "_" : "")).split("(?<=\\G.{2})");
  }
}
________________________________
public class StringSplit {
  public static String[] solution(String s) {
    return s.length() % 2 == 0 ? s.split("(?<=\\G.{2})") 
      : (s + "_").split("(?<=\\G.{2})");
  }
}
________________________________
public class StringSplit {
    public static String[] solution(String s){String[] result = new String [s.length()%2==0? s.length()/2:(s.length()+1)/2];
  if(s.length() == 0) {return result;}
  try {
    for(int i = 0, j = 0; i < result.length; i++,j+=2) {
      result[i] = (s.charAt(j)+""+s.charAt(j+1));
      if(i == result.length-1) {return result;}
    }
  }catch(Exception e) {}
    result[result.length-1] = (s.charAt(s.length()-1)+"_");
  
      return result;
  }
}
