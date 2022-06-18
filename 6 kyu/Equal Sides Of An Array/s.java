public class Kata {
  public static int findEvenIndex(int[] arr) {
     for(int i = 0; i < arr.length; i++){
       if(leftSum(arr, i) == rightSum(arr, i))
         return i;
     }
     
     return -1;
  }
  
  public static long leftSum(int[] arr,int idx){
    long result = 0;
    
    for(int i = 0; i < idx; i++){
      result += arr[i];
    }
    
    return result;
  }
  
  public static long rightSum(int[] arr, int idx){
    long result = 0;
    
    for(int i = idx + 1; i < arr.length; i++){
      result += arr[i];
    }
    
    return result;
  }
}
________________________
import java.util.Arrays;

public class Kata {
  public static int findEvenIndex(int[] arr) {
    int left = 0;
    int right = Arrays.stream(arr).sum();
    for (int i=0; i<arr.length; i++){
      right -= arr[i];
      if (left == right) return i;
      left += arr[i];
    }
    return -1;
  }
}
________________________
public class Kata {
  public static int findEvenIndex(int[] arr) {
    int sum = 0, cSum = 0;
    for (int i = 0; i < arr.length; i++) sum += arr[i];
    for(int i = 0; i < arr.length; i++){
      if (cSum == sum - arr[i]) return i;
      cSum += arr[i];
      sum -= arr[i];
    }
    return -1;
  }
}
________________________
import java.util.stream.IntStream;

public class Kata {
  public static int findEvenIndex(int[] arr) {
    return IntStream.range(0, arr.length)
        .filter(n -> IntStream.of(arr).limit(n).sum() == IntStream.of(arr).skip(n + 1).sum())
        .findFirst().orElse(-1);
  }
}
