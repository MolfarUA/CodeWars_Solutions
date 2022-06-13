import java.util.*;

public class Kata {

  public static int[] sortArray(final int[] array) {

    // Sort the odd numbers only
    final int[] sortedOdd = Arrays.stream(array).filter(e -> e % 2 == 1).sorted().toArray();
    
    // Then merge them back into original array
    for (int j = 0, s = 0; j < array.length; j++) {
      if (array[j] % 2 == 1) array[j] = sortedOdd[s++];
    }
    
    return array;
  }
  
}
_______________________________________________
import java.util.PrimitiveIterator.OfInt;
import java.util.stream.IntStream;

public class Kata {
  public static int[] sortArray(int[] array) {
    OfInt sortedOdds = IntStream
        .of(array)
        .filter(i -> i % 2 == 1)
        .sorted()
        .iterator();

    return IntStream
        .of(array)
        .map(i -> i % 2 == 0 ? i : sortedOdds.nextInt())
        .toArray();  
      }
}
_______________________________________________
public class Kata {
  public static int[] sortArray(int[] array) {
    
    int temp = 0;
    for (int i=0; i< array.length; i++) {
      if ((array[i] % 2) != 0) {
       for (int j=i; j< array.length; j++) {
          if ((array[j] % 2) != 0) {
            if (array[i] > array[j]) {
              temp = array[j];
              array[j] = array[i];
              array[i] = temp;
              }
          }
       }
      }
    }
     
    return array;
  }
}
_______________________________________________
public class Kata {
  public static int[] sortArray(int[] array) {
    for(int i=0;i<array.length-1;i++){
      if(array[i]%2!=0){
      for(int j=i+1;j<array.length;j++){
        if((array[j]%2!=0)&&(array[i]>array[j])){
          int tmp=array[i];
          array[i]=array[j];
          array[j]=tmp;
        }
      }
     }
    }
    return array;
  }
}
_______________________________________________
import java.util.Deque;
import java.util.Arrays;
import java.util.ArrayDeque;
import java.util.function.Supplier;
import java.util.stream.Collectors;


public class Kata {
  public static int[] sortArray(int[] array) {
    Deque deque = new ArrayDeque(Arrays.stream(array).filter(element -> element % 2 != 0).sorted().boxed().collect(Collectors.toList()));
    return Arrays.stream(array).map(element -> element % 2 != 0 ? (int) deque.pollFirst() : element).toArray();
  }
}
