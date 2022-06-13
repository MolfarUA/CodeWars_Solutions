public class FindOdd {
  public static int findIt(int[] A) {
    int xor = 0;
    for (int i = 0; i < A.length; i++) {
      xor ^= A[i];
    }
    return xor;
  }
}
_______________________________
import static java.util.Arrays.stream;

public class FindOdd {
  public static int findIt(int[] arr) {
    return stream(arr).reduce(0, (x, y) -> x ^ y);
  }
}
_______________________________
public class FindOdd {
  public static int findIt(int[] A) {
    int odd=0;
    for (int item: A)
      {
        odd = odd ^ item;// XOR will cancel out everytime you XOR with the same number so 1^1=0 but 1^1^1=1 so every pair should cancel out leaving the odd number out
      }
    
    return odd;
  }
}
_______________________________
import java.util.HashMap;
import java.util.Map;

public class FindOdd {
  public static int findIt(int[] a) {
    Map<Integer, Integer> counts = new HashMap<>(a.length);
    for(int i : a) {
      if(!counts.containsKey(i)) counts.put(i, 1);
      else counts.put(i, counts.get(i) + 1);
    }
    for(Map.Entry<Integer, Integer> entry : counts.entrySet()) if(entry.getValue() % 2 == 1) return entry.getKey();
    return 0;
  }
}
_______________________________
public class FindOdd {
  public static int findIt(int[] A) {
    int odd = 0;
    
    for (int i : A) {
      odd ^= i;
    }
  
    return odd;
  }
}
_______________________________
public class FindOdd {

  /**********************************************************************************************
  * Given an array, find the int that appears an odd number of times.
  * 
  * PRECONDITION: There will always be only one integer that appears an odd number of times.
  ***********************************************************************************************/
  public static int findIt(int[] A) {
    
    // for every int in A, check if that int appears an odd number of times
    for (int i : A) { 
      
      int temp = 0; // to get the number of times I find A[i];
      
      for (int j : A)
        if (j == i)  // get the number of A[i]'s in the array
          temp++;
          
      if (temp % 2 == 1) // if it is odd
        return i; // return the number that appeared an odd number of times
    }
    return 0;
  }
}
