55c04b4cc56a697bb0000048


public class Scramblies {
    
    public static boolean scramble(String str1, String str2) {
        if (str2.length() > str1.length()) return false;
        for (String s: str2.split("")) {
          if (!str1.contains(s))  return false;
          str1 = str1.replaceFirst(s,"");
        }        
       
        return true;
    }
}
______________________________
import java.util.LinkedList;

public class Scramblies {

    public static boolean scramble(String str1, String str2) {
        LinkedList<Character> linkedList = new LinkedList<Character>();
        for(char a: str1.toCharArray()){
            linkedList.add(a);
        }
        for(char a: str2.toCharArray()) {
            if(!linkedList.remove((Character)a)) {
                return false;
            }
        }
        return true;
    }
}
______________________________
import java.util.HashMap;
import java.util.Map;

public class Scramblies {

    public static boolean scramble(String str1, String str2) {
        Map<Character, Integer> word1 = countLetters(str1);
        Map<Character, Integer> word2 = countLetters(str2);

        for (Character c : word2.keySet()) {
            Integer n = word1.get(c);
            if (n == null || n < word2.get(c)) {
                return false;
            }
        }

        return true;
    }

    private static Map<Character, Integer> countLetters(String s) {
        Map<Character, Integer> map = new HashMap<Character, Integer>();
        for (char c : s.toCharArray()) {
            Integer n = map.get(c);
            if (n == null) {
                map.put(c, 1);
            } else {
                map.put(c, n + 1);
            }
        }
        return map;
    }
}
