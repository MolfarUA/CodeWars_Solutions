5a2be17aee1aaefe2a000151


import java.util.stream.*;

public class Sum {

  public static int arrayPlusArray(int[] arr1, int[] arr2) {
    return IntStream.of(arr1).sum() + IntStream.of(arr2).sum();
  }

}
_________________________
public class Sum {

  public static int arrayPlusArray(int[] arr1, int[] arr2) {
    int arrSum = 0;
    for(int num : arr1) {arrSum += num;}
    for(int num : arr2) {arrSum += num;}
    return arrSum;
  }

}
_________________________
import java.util.Arrays;
import java.util.stream.Stream;

public class Sum {

  public static int arrayPlusArray(int[] arr1, int[] arr2) {
    return Stream.of(arr1, arr2).flatMapToInt(Arrays::stream).sum();
  }

}
