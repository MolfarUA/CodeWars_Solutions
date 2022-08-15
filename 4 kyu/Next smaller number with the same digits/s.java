5659c6d896bc135c4c00021e


public class Kata
{
  public static long nextSmaller(long n){
        char[] carr = String.valueOf(n).toCharArray();
        int len = carr.length, i;
        for (i = len - 1; i > 0; i--) {
            if (carr[i] < carr[i - 1]) break;
        }
        if (i == 0) return -1;
        else {
            int x = carr[i - 1], min = i;
            for (int j = i + 1; j < len; j++) {
                if (carr[j] < x && carr[j] > carr[min]) {
                    min = j;
                }
            }           
            char temp = carr[i-1];
            carr[i-1] = carr[min];
            carr[min] = temp;            
            String[] sarr = String.valueOf(carr).split("");            
            java.util.Arrays.sort(sarr, i, len, java.util.Collections.reverseOrder());
            long r = Long.valueOf(String.join("", sarr));
            return String.valueOf(r).length() == len ? r : -1;
        }
  }
}
_______________________________
import java.util.Arrays;
import java.util.Collections;
import java.util.stream.Stream;

public class Kata {
  public static long nextSmaller(long n) {
        Integer[] val = Long.toString(n).chars().map(c -> c - '0').boxed().toArray(Integer[]::new);
        int len = val.length;
        for (int i = len - 1; i > 0; i--) {
            if (val[i - 1] > val[i]) {
                int maxIdx = i;
                for (int j = i + 1; j < len; j++) {
                    if (val[i - 1] > val[j] && val[j] > val[maxIdx]) maxIdx = j;
                }
                val[i - 1] = val[i - 1] + val[maxIdx];
                val[i - 1] = val[i - 1] - (val[maxIdx] = val[i - 1] - val[maxIdx]);

                Arrays.sort(val, i, len, Collections.reverseOrder());
                return val[0] == 0 ? - 1L : Long.valueOf(String.join("", Stream.of(val).map(String::valueOf).toArray(String[]::new)));
            }
        }
        return -1L;
    }
}
_______________________________
import java.util.*;
public class Kata{
  public static long nextSmaller(long n){
    Long[] k = String.valueOf(n).chars().mapToLong(x -> x - 48).boxed().toArray(Long[]::new);
    for (int i = k.length - 2; i >= 0; i--) {
      for (int j = k.length - 1; j > i; j--) {
        if (k[i] > k[j]) {
          k[i] ^= k[j]; k[j] ^= k[i]; k[i] ^= k[j];
          Arrays.sort(k, i + 1, k.length, Comparator.reverseOrder());
          return k[0] != 0 ? Arrays.stream(k).reduce((x, y) -> x * 10 + y).get() : -1;
          }}}
    return -1;
  }
}
