58c5577d61aefcf3ff000081


public class RailFenceCipher {
  
  public static String encode(String s, int n) {
    return process(s, n, true);
  }
  
  public static String decode(String s, int n) {
    return process(s, n, false);
  }
  
  private static String process(String s, int n, boolean enc) {
    int len = s.length();
    int d = n * 2 - 2;
    StringBuilder sb = new StringBuilder(s);
    int counter = 0;
    for (int i = 0; i < n; i++) {
      int next = i == n - 1 ? d : d - i * 2;
      int index = i;
      
      while (index < len) {
        sb.setCharAt((enc ? counter++ : index), s.charAt(enc ? index : counter++));
        index += next;
        next = (next == d ? d : d - next);
      }
    }
    
    return sb.toString();
  }
}
_____________________________
import java.util.stream.*;
import java.util.*;

public class RailFenceCipher {
    
    
    private static <T> Stream<T> fencer(int n, Stream<T> str) {
        List<List<T>> rails = IntStream.range(0,n)
                                       .mapToObj( r -> new ArrayList<T>() )
                                       .collect(Collectors.toList());
        int[] data = {0,1};
        int   x=0, dx=1;
        str.forEachOrdered( t -> {
            rails.get(data[x]).add(t);
            if (data[x]==n-1 && data[dx]>0 || data[x]==0 && data[dx]<0)
                data[dx] *= -1;
            data[x] += data[dx];
        });
        return rails.stream().flatMap( lst -> lst.stream() );
    }
    
    
    static String encode(String s, int n) {
        return fencer(n, s.chars().mapToObj( c -> ""+(char) c))
                  .collect(Collectors.joining());
    }
    
    
    static String decode(String s, int n) {
        char[] arr = new char[s.length()];
        int[]  j   = {0};
        fencer(n, IntStream.range(0,s.length()).boxed())
            .forEachOrdered( i -> arr[i] = s.charAt(j[0]++) );
        return new String(arr);
    }
}
_____________________________
import java.util.*;
import java.util.stream.*;
public class RailFenceCipher {
    static String encode(String s, int n) {
        return Arrays.stream(getMatrixFilledWithCharsFromString(n, s, false)).map(array -> Arrays.stream(array).filter(Objects::nonNull).collect(Collectors.joining())).collect(Collectors.joining());
    }

    static String decode(String s, int n) {
        String[][] matrix = getMatrixFilledWithCharsFromString(n, s, true);
        String res = "";
        for(int i = 0, j = 0, step = -1; i < s.length(); i++, j += step) {
            step = (j == n - 1 || j == 0) ? -1 * step : step;
            res += matrix[j][i];
        }
        return res;
    }
    
    private static String[][] getMatrixFilledWithCharsFromString(int n, String s, boolean isDecoding) {
        String[][] matrix = new String[n][s.length()];
        for (int i = 0, j = 0, step = -1; i < s.length(); i++, j += step) {
            step = (j == n - 1 || j == 0) ? -1 * step : step;
            matrix[j][i] = isDecoding ? "" : "" + s.charAt(i);
        }
        return isDecoding ? getMatrixWithValuesForDecoding(matrix, s, n) : matrix;
    }

    private static String[][] getMatrixWithValuesForDecoding(String[][] matrix, String s, int n) {
        for (int i = 0, counter = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[0].length; j++) {
                matrix[i][j] = matrix[i][j] != null ? "" + s.charAt(counter++) : null;
            }
        }
        return matrix;
    }
}
