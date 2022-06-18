import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.lang.StringBuilder;

class Solution{

  static String toCamelCase(String s){
    Matcher m = Pattern.compile("[_|-](\\w)").matcher(s);
    StringBuffer sb = new StringBuffer();
    while (m.find()) {
        m.appendReplacement(sb, m.group(1).toUpperCase());
    }
    return m.appendTail(sb).toString();
  }
}
________________________
import java.util.Arrays;

class Solution{

  static String toCamelCase(String str){
    String[] words = str.split("[-_]");
    return Arrays.stream(words, 1, words.length)
            .map(s -> s.substring(0, 1).toUpperCase() + s.substring(1))
            .reduce(words[0], String::concat);
  }
}
________________________
import java.lang.StringBuilder;
class Solution{

  static String toCamelCase(String s){
    String[] words = s.split("[_\\-]");
    s=words[0];
    for(int i=1; i<words.length; i++)
      s+=words[i].substring(0,1).toUpperCase()+words[i].substring(1).toLowerCase();
    return s;
  }
}
________________________
import java.lang.StringBuilder;
class Solution{

  static String toCamelCase(String s){
    StringBuffer sb = new StringBuffer();
    
    boolean flToUpperCase = false;
    for ( char ch: s.toCharArray() ) {
      if ( ch == '-' || ch == '_' )
        flToUpperCase = true;
      else {
        sb.append( ( flToUpperCase ) ? Character.toUpperCase(ch) : ch );
        flToUpperCase = false;
      }
    }
    
    return sb.toString();
  }
}
________________________
import java.lang.StringBuilder;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class Solution{

  static String toCamelCase(String s){
    return Pattern.compile("[-|_](.)").matcher(s).replaceAll(r -> r.group(1).toUpperCase());
  }
}
________________________
import java.util.Arrays;

class Solution{

  static String toCamelCase(String s){
    String[] words = s.split("[-_]+");
    return Arrays.stream(words)
        .skip(1)
        .map(w -> w.substring(0, 1).toUpperCase().concat(w.substring(1)))
        .reduce(words[0], String::concat);
  }
}
