import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Kata {
   public static String makePassword(String phrase){
      return phrase.length() == 0 ? "" : Stream.of(phrase.split(" "))
              .map(s -> s.substring(0,1))
              .map(s -> s.equalsIgnoreCase("i") ? "1" : s.equalsIgnoreCase("o") ? "0" : s.equalsIgnoreCase("s") ? "5" : s)
              .collect(Collectors.joining());
   }
}
__________________________________
import java.util.Arrays;
import java.util.stream.Collectors;

public class Kata {
   public static String makePassword(String phrase){
     return phrase.equals("") ? "" : Arrays.asList(phrase.split(" ")).stream()
        .map(o -> o.substring(0,1)).collect(Collectors.joining(""))
        .replaceAll("[oO]", "0")
        .replaceAll("[iI]", "1")
        .replaceAll("[sS]", "5");
   }
}
__________________________________
interface Kata {
  static String makePassword(String phrase) {
    return phrase.replaceAll("\\s*(\\w)\\w+", "$1").replaceAll("o|O", "0").replaceAll("i|I", "1").replaceAll("s|S", "5");
  }
}
__________________________________
public class Kata {
   public static String makePassword(String words){
     String res = "";
     words = words.replaceAll("i","1").replaceAll("o", "0").replaceAll("s", "5").replaceAll("I","1").replaceAll("O", "0").replaceAll("S", "5");
     String[] arry = words.split(" ");
     String[] f;
     for (int c = 0; c < arry.length; c++){
       f = arry[c].split("");
       res += f[0];
     }
     return res;
   }
}
