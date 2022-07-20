54d496788776e49e6b00052f


import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class SumOfDivided {

    public static String sumOfDivided(int[] l) {
        final int maxValue = Arrays.stream(l).map(num -> Math.abs(num)).max().getAsInt();
        return eratosteneSieve(maxValue).stream()
                .reduce("",
                        (resultString, primeNum) -> {
                            List<Integer> divisibleNum = Arrays.stream(l).filter(num -> num % primeNum == 0).boxed().collect(Collectors.toList());
                            return divisibleNum.size() > 0
                                    ? resultString + String.format("(%d %d)", primeNum, divisibleNum.stream().mapToInt(Integer::intValue).sum())
                                    : resultString;
                        },
                        (not, used) -> null);
    }

    public static List<Integer> eratosteneSieve(final int x) {
        final List<Integer> candidates = IntStream.rangeClosed(2, x).boxed().collect(Collectors.toList());
        return candidates.stream()
                .filter(num -> num <= Math.sqrt(x))
                .reduce(candidates,
                        (resList, currNum) -> resList.stream()
                        .filter(num -> num % currNum != 0 || num.equals(currNum))
                        .collect(Collectors.toList()),
                        (not, used) -> null);
    }
}
________________________________________________
import java.lang.Math;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;
import java.util.LinkedList;
import java.util.Map;
import java.util.TreeMap;
import java.util.HashMap;
import java.util.stream.Collectors;

public class SumOfDivided {

  /*
  *  We use a cache of already known primes to minimize double computation.
  */
  private static SortedSet<Integer> primeCache = new TreeSet<>();
  private static Map<Integer, Integer> map = new HashMap<>();

  public static String sumOfDivided(int[] l) {
    initalize();
    
    for(int i=0; i<l.length; i++) {
      int absNum = Math.abs(l[i]);
      updatePrimeCache(absNum);
      updateMap(l[i]);
    }
    
    return convertMapToString();
  }
  
  private static void initalize(){
    map = new HashMap<>();
    if(primeCache.isEmpty()){
      primeCache.add(2);
    }
  }
  
  /*
  *  We update the prime cache so it contains all primes up to number. 
  */
  private static void updatePrimeCache(int number) {
    Integer largestKnownPrime  = primeCache.last();
    if(largestKnownPrime > number) {
      return;
    }
    
    for(int p=largestKnownPrime+1; p <= number; p++) {
      if(isPrime(p)) {
        primeCache.add(p);
        largestKnownPrime = p;
      }
    }
  }
  
  private static boolean isPrime(int p) {
    for(int i=2; i<=Math.sqrt(p); i++) {
      if(p%i == 0) return false;
    } 
    
    return true;
  }
  
  private static void updateMap(int num) {
    for(Integer prime: primeCache) {
      if(num%prime == 0) {
        Integer sum = map.getOrDefault(prime, 0);
        sum += num;
        map.put(prime, sum);
      }
    }
  }
  
  private static String convertMapToString() {
    TreeMap<Integer, Integer> sortedMap = new TreeMap(map); 
    return sortedMap.entrySet()
      .stream()
      .map(entry -> "(" + entry.getKey() + " " + entry.getValue() + ")")
      .collect(Collectors.joining(""));
  }
}
________________________________________________
import java.util.*;

public class SumOfDivided {
  public static String sumOfDivided(int[] l) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int number:l) {
            int i = number < 0 ? -number:number;
            for(int j = 2; j <= i; j++) {
                if (i%j == 0) map.put(j, map.get(j) == null ? number : map.get(j)+number);
                while(i%j == 0) i /= j;
            }
        }
        return map.entrySet().stream()
                .sorted(Comparator.comparing(Map.Entry::getKey))
                .map(e -> String.format("(%d %d)",e.getKey(),e.getValue()))
                .reduce((x,y) -> x+y)
                .get();
    }
}
