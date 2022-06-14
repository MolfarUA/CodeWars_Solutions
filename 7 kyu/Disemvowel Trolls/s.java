public class Troll {
    public static String disemvowel(String Z) {
        return Z.replaceAll("(?i)[aeiou]" , "");
    }
}
______________________________
public class Troll {
  public static String disemvowel(String str) {
      return str.replaceAll("[aAeEiIoOuU]", "");
  } 
}
______________________________
import java.util.regex.Pattern;

public class Troll {

    /**
     * Pre compiled pattern to match all vowels in a given string.
     */
    private static final Pattern DISEMVOWEL_PATTERN = Pattern.compile("[AaEeIiOoUu]");

    /**
     * Remove all vowels from the given input string.
     *
     * @param str The string to remove vowels from.
     *
     * @return A copy of the original string with all vowels removed.
     */
    public static String disemvowel(String str) {
        return DISEMVOWEL_PATTERN.matcher(str).replaceAll("");
    }
}
______________________________
public class Troll {
  public static String disemvowel(String str) {
      return str.replaceAll("[aeiouAEIOU]", "");
  } 
}
______________________________
public class Troll {
    public static String disemvowel(String str) {
    
        //This is setting up something to add to and return.
        String output = "";
        
        //This iterates (steps through) the string.
        for(int i = 0; i < str.length(); i++) {
        
        //! means not in Java, so it checks if our current letter is not a vowel, or is a consonant.
          if(str.charAt(i) != 'a' 
              && str.charAt(i) != 'e' 
              && str.charAt(i) != 'i' 
              && str.charAt(i) != 'o' 
              && str.charAt(i) != 'u'
              && str.charAt(i) != 'A' 
              && str.charAt(i) != 'E' 
              && str.charAt(i) != 'I' 
              && str.charAt(i) != 'O' 
              && str.charAt(i) != 'U') {
              
            //Here, we add the consonant to the string we will output.
            output = output + str.charAt(i);
          }
        }
        
        //We give the output back after running through the program (The original sentence, just without vowels)
        return output;
        
        //Hope you found this explanation helpful if you're new to programming! I know it's not the best solution, but it's easy enough to understand. :P
    }
}
