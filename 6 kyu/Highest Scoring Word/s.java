57eb8fcdf670e99d9b000272


import java.util.*;

public class Kata {
  public static String high(String s) {
    return Arrays.stream(s.split(" "))
                .max(Comparator.comparingInt(
                        a -> a.chars().map(i -> i - 96).sum()
                )).get(); 
  }
}
_____________________________________________
public class Kata {

  public static String high(String s) {
    
    String winner = "";
    int highScore = 0;
    
    for (String word : s.split(" ")) {
        int score = 0;
        for (char c : word.toCharArray()) {
          score += c - 'a' + 1;
        }
        if (score > highScore) {          
          winner = word;
          highScore = score;
        }
    }
    
    return winner;
  }

}
_____________________________________________
public class Kata {
  public static int count(String s1) {
    int count=0;
    for (int i = 0; i < s1.length(); i++) 
      count +=(int)(s1.charAt(i))-96;
    return count;
    }
  public static String high(String s) {
    String[] a = s.split(" ");
    int max = 0, count=0;
    for (int i = 0; i < a.length; i++) {
      if (count<count(a[i])) {
        count = count(a[i]);
        max=i;
      }
    }
    return a[max];
  }
}
_____________________________________________
public class Kata {

  public static String high(String s) {
    int score = 0;
    String word = "";
    for (String w : s.split(" ")) {
      int cscore = 0;
      for (char c : w.toCharArray()) {
        cscore += Character.getNumericValue(c)-9;
      }
      if (cscore > score) {
        word = w;
        score = cscore;
      }
    }
    return word;
  }

}
