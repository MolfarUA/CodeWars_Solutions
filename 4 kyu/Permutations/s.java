5254ca2719453dcc0b00027d


import java.util.*;

class Permutations {
    
    public static void generate(String seq, String out, List<String> list){
        if (seq.isEmpty()){
            if (!list.contains(out))
                list.add(out);
        }
        else
            for(int i=0; i < seq.length(); i++)
                generate(remove(seq,i), out+seq.charAt(i), list);
    }
    
    public static String remove(String str, int idx){
        return str.substring(0, idx)+str.substring(idx+1);
    }
    
    public static List<String> singlePermutations(String s) {
        List<String> list = new ArrayList<>();
        for(int i=0; i < s.length(); i++){
            generate(remove(s,i), ""+s.charAt(i), list);
        }
        return list;
    }
}
______________________________
import static java.util.Collections.singletonList;
import static java.util.stream.Collectors.toList;

import java.util.List;

class Permutations {

  public static List<String> singlePermutations(final String s) {
    return permute("", s);
  }

  private static List<String> permute(final String prefix, final String s) {
  
    return s.isEmpty()
        ? singletonList(prefix)
        : s.chars()
            .distinct()
            .mapToObj(i -> (char) i)
            .map(c -> permute(prefix + c, takeOut(s, c)))
            .flatMap(List::stream)
            .collect(toList());
  }

  static String takeOut(final String s, final char c) {
    final int i = s.indexOf(c);
    return s.substring(0, i) + s.substring(i + 1);
  }
}
______________________________
import java.util.List;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

class Permutations {
    
    public static List<String> singlePermutations(String s) {
        Set<String> set = new HashSet<>();
        if (s.length() == 1) {
            set.add(s);
        } else {
            for (int i = 0; i < s.length(); i++) {
                List<String> temp = singlePermutations(s.substring(0, i) + s.substring(i + 1));
                for (String string : temp) {
                    set.add(s.charAt(i) + string);
                }
            }
        }

        return new ArrayList<>(set);
    }
}
