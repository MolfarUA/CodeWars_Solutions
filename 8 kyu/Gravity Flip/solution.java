import java.util.Arrays;
import java.util.Collections;

public class Kata {
  public static int[] flip(char dir, int[] arr) {
        
    if (dir == 'L') {
          arr = Arrays.stream(arr)
                  .boxed()
                  .sorted(Collections.reverseOrder())
                  .mapToInt(Integer::intValue)
                  .toArray();
    } else{
      Arrays.sort(arr);
    }
    
    return arr;
  }
}

_____________________________________________
public class Kata {
  public static int[] flip(char dir, int[] arr) {
    int tmp = 0;

        if (dir == 'R') {
            for (int i = 0; i < arr.length; i++) {
                for (int j = 1; j < arr.length; j++) {
                    if (arr[j] < arr[j-1]) {
                        tmp = arr[j-1];
                        arr[j-1] = arr[j];
                        arr[j] = tmp;
                    }
                }
            }
        } else if (dir == 'L') {
            for (int i = 0; i < arr.length; i++) {
                for (int j = 1; j < arr.length; j++) {
                    if (arr[j] > arr[j-1]) {
                        tmp = arr[j-1];
                        arr[j-1] = arr[j];
                        arr[j] = tmp;
                    }
                }
            }
        }
        return arr;
    }
}

_____________________________________________
import java.util.Collections;
import java.util.stream.IntStream;

public class Kata {
    public static int[] flip(char dir, int[] arr) {
        return dir == 'R' ? IntStream.of(arr).sorted().toArray()
                : IntStream.of(arr).boxed().sorted(Collections.reverseOrder()).mapToInt(e -> e.intValue()).toArray();
  }
}

_____________________________________________
public class Kata {
  public static int[] flip(char dir, int[] arr) {
         int [] arrL = new int[arr.length];

         for (int i = arr.length - 1; i > 0; i--) {
              for (int j = 0; j < i; j++){
                  if (arr[j] > arr[j + 1]) {
                      int temp = arr[j];
                      arr[j] = arr[j + 1];
                      arr[j + 1] = temp;
                  }
              }
         }
         if (dir == 'R') {
                return arr;
            }
         if (dir == 'L') {
                for (int i = arrL.length - 1; i >= 0; i--) {
                    arrL[i] = arr [arrL.length - i - 1];
                }
            return arrL;
            } else return null;
}
  }
