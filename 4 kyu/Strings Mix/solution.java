import java.util.*;
import java.util.stream.Collectors;

public class Mixing {
    public static String mix(String s1, String s2) {
    
        List<String> finalStr = new ArrayList();

        for (char c = 'a'; c <= 'z'; c++) {
            String s1_char = s1.replaceAll("[^"+c+"]+","");
            String s2_char = s2.replaceAll("[^"+c+"]+","");

            int s1_length = s1_char.length();
            int s2_length = s2_char.length();

            if(s1_length>1 || s2_length>1){
                if(s1_length == s2_length){
                    finalStr.add("=:"+s1_char);
                }
                if(s1_length>s2_length){
                    finalStr.add("1:"+s1_char);
                }
                if(s1_length<s2_length){
                    finalStr.add("2:"+s2_char);
                }
            }
        }
        Comparator<String> length = (x,y) -> y.length()-x.length();
        Comparator<String> type_value = (x,y) -> Character.compare(x.charAt(0),y.charAt(0));

        return finalStr.stream().sorted(length.thenComparing(type_value)).collect(Collectors.joining("/"));
    }

}

__________________________________________________
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

public class Mixing {

    public static String mix(String s1, String s2) {
        HashMap<Character,Count> map=new HashMap<>();
        for(char c:s1.toCharArray()){
            if(map.containsKey(c)){
                map.get(c).times1++;
            }
            else{
                Count count=new Count();
                count.c=c;
                count.times1++;
                map.put(c,count);
            }
        }
        for(char c:s2.toCharArray()){
            if(map.containsKey(c)){
                map.get(c).times2++;
            }
            else{
                Count count=new Count();
                count.c=c;
                count.times2++;
                map.put(c,count);
            }
        }
        List<Count> list=new ArrayList<Count>(map.values());
        Collections.sort(list);
        StringBuilder sb=new StringBuilder();
        for(Count c:list){
            if(c.getMax()>1&&c.c>='a'&&c.c<='z'){
                if(sb.length()!=0)
                    sb.append("/");
                sb.append(c.getMaxIndexString());
                sb.append(":");
                for(int i=0;i<c.getMax();i++){
                    sb.append(c.c);
                }
            }
        }
        return sb.toString();
    }
    private static class Count implements Comparable<Count>{
        char c;
        int times1=0;
        int times2=0;
        @Override
        public int compareTo(Count b){
            if(b.getMax()!=getMax())
                return b.getMax()-getMax();
            if(getMaxIndexString()!=b.getMaxIndexString()){
                return getMaxIndexString()-b.getMaxIndexString();
            }
            return c-b.c;
        }
        public int getMax(){
            return Math.max(times1,times2);
        }
        public int getMaxIndex(){
            return times1>times2?1:2;
        }
        public char getMaxIndexString(){
            return times1==times2?'=':times1>times2?'1':'2';
        }
    }
}

__________________________________________________
import java.util.*;

public class Mixing {
  
        private static int i = 0;
    
    public static void main(String[] args) {
    }

    public static String mix(String s1, String s2) {
        System.out.println(s1);
        System.out.println("-----------");
        System.out.println(s2);
        i = 0;
        StringBuilder stringBuilder = new StringBuilder();
        List<Section> s1List = countLetters(s1);
        List<Section> s2List = countLetters(s2);

        for (Section section : s2List) {
            s1List.add(section);
        }

        Collections.sort(s1List);

        List<Section> sectionsToRemove = new ArrayList<>();
        for (Section section : s1List) {
            if (section.from == 1) {
                continue;
            }
            for (Section other : s1List) {
                if (section.letter.equals(other.letter) && section.from != other.from) {
                    if (section.amount > other.amount) {
                        sectionsToRemove.add(other);
                    } else if (section.amount < other.amount) {
                        sectionsToRemove.add(section);
                    } else {
                        section.setEqual(true);
                        sectionsToRemove.add(other);
                    }
                }
            }
        }

        for (Section section : sectionsToRemove) {
            s1List.remove(section);
        }

        Collections.sort(s1List);
        for (Section section : s1List) {
            stringBuilder.append(section.getString() + "/");
        }

        return removeLastCharacter(stringBuilder.toString());
    }

    private static List<Section> countLetters(String s) {
        i++;
        List<Section> sectionList = new ArrayList<>();
        List<Character> stringList = new ArrayList<>();
        for (char c : s.toCharArray()) {
            stringList.add(c);
        }
        Collections.sort(stringList);

        Map<Character, Integer> countMap = new HashMap<>();
        char cache = ' ';
        int count = 1;
        for (Character character : stringList) {
            if (character.toString().isBlank() || Character.isUpperCase(character)) {
                continue;
            }
            if(!Character.isLetter(character)) {
                continue;
            }
            if (cache != character) {
                count = 1;
            }
            if (count != 1) {
                countMap.put(character, count);
            }
            cache = character;
            count++;
        }

        countMap.forEach((character, integer) -> sectionList.add(new Section(integer, character.toString(), i)));
        return sectionList;
    }

    private static String removeLastCharacter(String str) {
        String result = "";
        if ((str != null) && (str.length() > 0)) {
            result = str.substring(0, str.length() - 1);
        }
        return result;
    }
}

class Section implements Comparable {

    public int amount;
    public String letter;
    public int from;
    public boolean isEqual;

    public Section(int amount, String letter, int from) {
        this.amount = amount;
        this.letter = letter;
        this.from = from;
        this.isEqual = false;
    }

    public String getString() {
        return getAmountAsString(letter, amount);
    }

    private String getAmountAsString(String c, Integer i) {
        String returningString;
        StringBuilder stringBuilder = new StringBuilder();
        for (int j = 0; j < i; j++) {
            stringBuilder.append(c);
        }
        returningString = stringBuilder.toString();
        if (isEqual) {
            returningString = "=:" + returningString;
        } else {
            returningString = this.from + ":" + returningString;
        }
        return returningString;
    }

    public void setEqual(boolean equal) {
        isEqual = equal;
    }

    @Override
    public int compareTo(Object o) {
        Section other = (Section) o;
        if (this.amount > other.amount) {
            return -1;
        } else if (this.amount < other.amount) {
            return 1;
        }
        if (isEqual) {
            return 1;
        }
        if (other.isEqual) {
            return -1;
        }
        if (from == 2 && other.from == 1) {
            return 1;
        }
        if (from == 1 && other.from == 2) {
            return -1;
        }
        return this.letter.compareTo(other.letter);
    }
}

__________________________________________________
import java.util.*;

public class Mixing {
    
    public static String mix(String s1, String s2) {

        //标记哪些字符出现过，true:出现过；false:没出现过
        boolean[] flag = new boolean[26];

        Map<Integer, Set<Character>> seqMap1 = getSequence(s1, flag);
        Map<Integer, Set<Character>> seqMap2 = getSequence(s2, flag);
        Set<Integer> keys1 = seqMap1.keySet();
        Set<Integer> keys2 = seqMap2.keySet();
        SortedSet sortedSet = new TreeSet<Integer>((a, b) ->b.compareTo(a));
        sortedSet.addAll(keys1);
        sortedSet.addAll(keys2);
        StringBuilder sb = new StringBuilder();
        Iterator<Integer> iterator = sortedSet.iterator();
        while (iterator.hasNext()) {
            Integer times = iterator.next();
            Set values1 = seqMap1.get(times);
            Set values2 = seqMap2.get(times);
            genResult(values1, values2, times, sb, flag);
        }
        if (sb.length()>1) {
            return sb.substring(0, sb.length()-1).toString();
        }
        return new String();

    }


    private static void genResult(Set<Character> vals1, Set<Character> vals2, Integer times, StringBuilder sb, boolean[] flag) {

        if (vals1==null) {
            vals1 = new HashSet<>();
        }

        if (vals2==null) {
            vals2 = new HashSet<>();
        }

        SortedSet all = new TreeSet<Character>();
        all.addAll(vals1);
        all.addAll(vals2);

        Set insect = new HashSet<Character>();
        insect.addAll(vals1);
        insect.retainAll(vals2);

        Set exSect1 = new HashSet<Character>();
        exSect1.addAll(vals1);
        exSect1.removeAll(vals2);

        Set exSect2 = new HashSet<Character>();
        exSect2.addAll(vals2);
        exSect2.removeAll(vals1);

        Iterator<Character> iterator = all.iterator();
        //频率一样
        List<Character> charEq = new ArrayList<>();
        //取1
        List<Character> charSet1 = new ArrayList<>();
        //取2
        List<Character> charSet2 = new ArrayList<>();
        while (iterator.hasNext()) {
            Character ch = iterator.next();
            if (!flag[ch-'a']) {
                continue;
            }
            if (insect.contains(ch)) {
                charEq.add(ch);
            }
            if (exSect1.contains(ch)) {
                charSet1.add(ch);
            }
            if (exSect2.contains(ch)) {
                charSet2.add(ch);
            }
            flag[ch-'a'] = false;
            continue;
        }
        String[] prefixs = {"1:", "2:", "=:"};
        List<List<Character>> characters = new ArrayList<>();
        characters.add(charSet1);
        characters.add(charSet2);
        characters.add(charEq);
        decorate(characters, prefixs, sb, times);
    }

    private static void decorate(List<List<Character>> characters, String[] prefixs, StringBuilder sb, int times) {
        for (int i=0; i<3; i++) {
            List<Character> chs = characters.get(i);
            for (char ch:chs) {
                sb.append(prefixs[i]);
                char[] tmp = new char[times];
                Arrays.fill(tmp, ch);
                sb.append(tmp).append('/');
            }
        }
    }


    private static  Map<Integer, Set<Character>> getSequence(String str, boolean[] flag) {
        Map<Integer, Set<Character>> result = new HashMap<>();
        int[] times = new int[26];
        for (char ch:str.toCharArray()) {
            if (ch-'a'<0 || ch-'a'>25) {
                continue;
            }
            times[ch-'a']++;
            flag[ch-'a'] = true;
            if (times[ch-'a']>2) {
                Set<Character> tmp = result.get(times[ch-'a']-1);
                tmp.remove(ch);
                if (tmp.size()==0) {
                    result.remove(times[ch-'a']-1);
                }
                tmp = result.get(times[ch-'a']);
                if (tmp==null) {
                    tmp = new HashSet<>();
                    result.put(times[ch-'a'], tmp);
                }
                tmp.add(ch);
            }
            if (times[ch-'a']==2) {
                Set<Character> tmp = result.get(2);
                if (tmp==null) {
                    tmp = new HashSet<>();
                    tmp.add(ch);
                    result.put(2, tmp);
                } else {
                    tmp.add(ch);
                }
            }
        }
        return result;
    }
}

__________________________________________________
import java.util.*;

public class Mixing {
    
  public static String mix(String s1, String s2) {
    HashMap<Character, String> m1 = count(s1);
    HashMap<Character, String> m2 = count(s2);
    String r = "";
    if (m1.isEmpty() && m2.isEmpty()) return r;
    SortedSet<Character> s = new TreeSet<>(m1.keySet());
    s.addAll(m2.keySet());
    
    List<String> l = new ArrayList<>();
    for (Character c : s){
      if (m1.containsKey(c) && m2.containsKey(c)){
        if (m1.get(c).length() > m2.get(c).length()) l.add("1:" + m1.get(c) + '/');
        else if (m2.get(c).length() > m1.get(c).length()) l.add("2:" + m2.get(c) + '/');
        else l.add("=:" + m1.get(c) + '/');
      }
      else if (m1.containsKey(c)) l.add("1:" + m1.get(c) + '/');
      else l.add("2:" + m2.get(c) + '/');
    }
    Collections.sort(l,(t1, t2) -> t1.compareTo(t2));
    Collections.sort(l, 
          (t1, t2) -> Integer.valueOf(t2.length()).compareTo(Integer.valueOf(t1.length())));
    for (String t : l) r += t;
    r = r.substring(0, r.length() - 1);
    return r;
  }
  
  public static HashMap<Character, String> count(String s){
    HashMap<Character, String> m = new HashMap<>();
    for (char c : s.toCharArray()){
      if (c < 97 || c > 122) continue;
      if (m.replace(c, m.get(c) + c) == null) m.put(c, "" + c);
    }
    List<Character> l = new ArrayList<>(m.keySet());
    l.stream()
        .filter(k -> m.get(k).length() < 2)
        .forEach(k -> m.remove(k));
    return m;
  }
}
