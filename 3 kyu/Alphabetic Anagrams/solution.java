import java.math.BigInteger;

public class Anagrams {
  public BigInteger listPosition(String word) {
  
     BigInteger rank = BigInteger.ONE;
        BigInteger suffixPermCount = BigInteger.ONE;
        java.util.Map<Character, BigInteger> charCounts =
                new java.util.HashMap<>();
        for (int i = word.length() - 1; i > -1; i--) {
            char x = word.charAt(i);
            BigInteger xCount = charCounts.containsKey(x) ? charCounts.get(x).add(BigInteger.ONE) : BigInteger.ONE;
            charCounts.put(x, xCount);
            for (java.util.Map.Entry<Character, BigInteger> e : charCounts.entrySet()) {
                if (e.getKey() < x) {
                    rank = rank.add(suffixPermCount.multiply(e.getValue()).divide(xCount));
                }
                // System.out.println(rank);
            }
            suffixPermCount = suffixPermCount.multiply(BigInteger.valueOf(word.length() - i));
            suffixPermCount = suffixPermCount.divide(xCount);
        }
        return rank;

    }

}

___________________________________________________
import java.math.BigInteger;

public class Anagrams {
  
  
  private BigInteger factorial( int N)
  {
    BigInteger result = BigInteger.valueOf(1);
    for( int i = 2; i <= N; i++) result = result.multiply(BigInteger.valueOf(i));
    return result;
  }
  private BigInteger permutationWithoutChar( int N, int[]counts)
  {
    BigInteger result = factorial(N);
    for(int i = 0; i < counts.length; i++)
    {
      if (counts[i] > 1)
        result = result.divide(factorial(counts[i]));
    }
    return result;
  }
  
  public BigInteger listPosition(String word) {

        if (word.equals(""))
            return BigInteger.valueOf(1);
        int [] letterCounts = new int[26];
        for ( int i = 0; i < word.length();i++) letterCounts[ word.charAt(i) -'A' ]++;

        char firstLetter = word.charAt(0);
        String tword = word;
        BigInteger result = BigInteger.valueOf(0);
        for (int i = 1; i < tword.length(); i++)
        {
            char c = tword.charAt(i);
            if ( c < firstLetter && c != '.' )
            {
                letterCounts[ c-'A' ]--;
                result = result.add(permutationWithoutChar( word.length()-1,letterCounts ));
                letterCounts[ c-'A' ]++;
                tword = tword.replace( c, '.');

            }
        }

        return result.add(listPosition( word.substring(1)));
    }
}

___________________________________________________
import java.math.BigInteger;
import java.util.*;
public class Anagrams {
  public BigInteger listPosition(String word) {
    Map<Character, Integer> map=new HashMap<Character, Integer> ();
    BigInteger fac=new BigInteger("1");
    BigInteger ans=new BigInteger("1");
    BigInteger count=new BigInteger("0");
    for(int i=word.length()-1;i>=0;--i)
    {
      count=count.add(new BigInteger("1"));
      fac=fac.multiply(count);
      if(map.get(word.charAt(i))==null)
      map.put(word.charAt(i),0);
      map.put(word.charAt(i),map.get(word.charAt(i))+1);
      fac=fac.divideAndRemainder(new BigInteger(String.valueOf(map.get(word.charAt(i)))))[0];
      for(Character c:map.keySet())
      {
        if(c<word.charAt(i))
        {
          ans=ans.add(fac.divideAndRemainder(count)[0].multiply(new BigInteger(String.valueOf(map.get(c)))));
        }
      }    
    
  }
  return ans;
  }
}

___________________________________________________
import java.math.BigInteger;
import java.util.*;
public class Anagrams {

  static final int N = 26;
  static BigInteger[] factorial = new BigInteger[N+1];
  static{
      BigInteger bi = new BigInteger("1");
      factorial[1] = bi;
      for (int i = 2; i <= N; i++)  {
          bi = bi.multiply(BigInteger.valueOf(i));
          factorial[i] = bi;
      }
  }
  static BigInteger permutations(String s) {
      Map<Character,Integer> cc = new HashMap<>();
      int n = s.length();
      for (int i = 0; i < n; i++) {
          char c = s.charAt(i);
          int count = cc.containsKey(c) ? cc.get(c) : 0;
          cc.put(c,count+1);
      }
      BigInteger result = factorial[n];
      for (Integer x : cc.values()) if (x > 1) result = result.divide(factorial[x]);
      return result;
  }
  public BigInteger listPosition(String word) {
      char[] one = word.toCharArray();
      Arrays.sort(one);
      if (word.equals(String.valueOf(one))) return BigInteger.ONE;
      
      char c = word.charAt(0);
      int i = -1, n = one.length;
      BigInteger result = new BigInteger("0");
      char last = '-';
      while (++i < n) {
          if (c <= one[i]) break;
          if (one[i] == last) continue;
          String werd = word.replaceFirst(""+one[i], "");
          result = result.add(permutations(werd));
          last = one[i];
      }
      return result.add(listPosition(word.substring(1)));
  }
}
